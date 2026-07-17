from __future__ import annotations

import fcntl
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from aura.process_ownership_service_state_persistence.persistent_service_state_store import (
    PersistentServiceStateError,
    PersistentServiceStateStore,
)


class ManualRuntimeControlError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = str(code)
        self.details = dict(details or {})

    def packet(self) -> dict[str, Any]:
        return {
            "ok": False,
            "error": self.code,
            "message": str(self),
            "details": dict(self.details),
        }


class ManualStartStopStatusRuntimeExecutor:
    SCHEMA_VERSION = 2
    HOST = "127.0.0.1"
    PORT = 8765
    START_TIMEOUT_SECONDS = 12.0
    STOP_TIMEOUT_SECONDS = 8.0
    KILL_TIMEOUT_SECONDS = 3.0
    HEALTH_REQUEST_TIMEOUT_SECONDS = 1.0
    POLL_INTERVAL_SECONDS = 0.1
    PROCESS_ROLE_SERVICE_RUNTIME = "service_runtime"
    PROCESS_ROLE_CONTROL_PLANE = "control_plane"
    PROCESS_ROLE_UNCLASSIFIED = "unclassified_main"

    def __init__(
        self,
        project_root: str | Path,
        *,
        state_path: str | Path | None = None,
        lock_path: str | Path | None = None,
        log_path: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        uid = os.getuid()
        runtime_prefix = (
            f"aura-manual-start-stop-status-{uid}"
        )
        tmp = Path("/tmp")
        persistent_state_path = (
            self.project_root
            / "data"
            / "runtime"
            / "service_state.json"
        )

        self.state_path = Path(
            state_path
            if state_path is not None
            else persistent_state_path
        )
        self.state_store = PersistentServiceStateStore(
            self.project_root,
            state_path=self.state_path,
        )
        self.lock_path = Path(
            lock_path
            if lock_path is not None
            else tmp / f"{runtime_prefix}.lock"
        )
        self.log_path = Path(
            log_path
            if log_path is not None
            else tmp / f"{runtime_prefix}.log"
        )

        self.main_path = (
            self.project_root / "main.py"
        ).resolve()
        self.python_path = Path(
            sys.executable
        ).absolute()
        self.expected_argv = (
            str(self.python_path),
            str(self.main_path),
            "service-lifecycle-start",
            "--confirm-localhost",
        )

    @staticmethod
    def _now_utc() -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _read_proc_start_ticks(
        pid: int,
    ) -> int | None:
        path = Path(f"/proc/{pid}/stat")

        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            OSError,
        ):
            return None

        if ")" not in text:
            return None

        remainder = text.rsplit(")", 1)[1].strip()
        fields = remainder.split()

        # After removing pid + comm, index 0 is field 3.
        starttime_index = 22 - 3

        if len(fields) <= starttime_index:
            return None

        try:
            return int(
                fields[starttime_index]
            )
        except ValueError:
            return None

    @staticmethod
    def _read_cmdline(
        pid: int,
    ) -> list[str] | None:
        path = Path(f"/proc/{pid}/cmdline")

        try:
            raw = path.read_bytes()
        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            OSError,
        ):
            return None

        argv = [
            item.decode(
                "utf-8",
                errors="replace",
            )
            for item in raw.split(b"\0")
            if item
        ]

        return argv or None

    @staticmethod
    def _read_cwd(
        pid: int,
    ) -> str | None:
        path = Path(f"/proc/{pid}/cwd")

        try:
            return str(path.resolve())
        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            OSError,
        ):
            return None

    @staticmethod
    def _socket_inodes_for_pid(
        pid: int,
    ) -> set[str]:
        fd_root = Path(f"/proc/{pid}/fd")
        inodes: set[str] = set()

        try:
            entries = list(
                fd_root.iterdir()
            )
        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            OSError,
        ):
            return inodes

        for entry in entries:
            try:
                target = os.readlink(entry)
            except (
                FileNotFoundError,
                PermissionError,
                ProcessLookupError,
                OSError,
            ):
                continue

            if (
                target.startswith("socket:[")
                and target.endswith("]")
            ):
                inodes.add(
                    target[len("socket:[") : -1]
                )

        return inodes

    @staticmethod
    def _listener_records(
        port: int,
    ) -> list[dict[str, Any]]:
        records = []

        for source in (
            Path("/proc/net/tcp"),
            Path("/proc/net/tcp6"),
        ):
            if not source.is_file():
                continue

            try:
                lines = source.read_text(
                    encoding="utf-8"
                ).splitlines()[1:]
            except OSError:
                continue

            for line in lines:
                fields = line.split()

                if len(fields) < 10:
                    continue

                try:
                    address_hex, port_hex = (
                        fields[1].rsplit(":", 1)
                    )
                    local_port = int(
                        port_hex,
                        16,
                    )
                except (
                    ValueError,
                    IndexError,
                ):
                    continue

                if (
                    local_port != port
                    or fields[3] != "0A"
                ):
                    continue

                records.append(
                    {
                        "source": str(source),
                        "address_hex": address_hex,
                        "port": local_port,
                        "state_hex": fields[3],
                        "inode": fields[9],
                    }
                )

        return records

    def classify_main_process_role(
        self,
        argv: list[str] | tuple[str, ...],
        cwd: str | None,
    ) -> str:
        tokens = [str(item) for item in argv]

        if len(tokens) < 2:
            return self.PROCESS_ROLE_UNCLASSIFIED

        executable = Path(tokens[0]).name.lower()

        if not executable.startswith("python"):
            return self.PROCESS_ROLE_UNCLASSIFIED

        indexes = [
            index
            for index, item in enumerate(
                tokens[1:],
                start=1,
            )
            if Path(item).name == "main.py"
        ]

        if len(indexes) != 1 or cwd is None:
            return self.PROCESS_ROLE_UNCLASSIFIED

        try:
            cwd_path = Path(cwd).resolve()
            script = Path(tokens[indexes[0]])
            script_path = (
                script.resolve()
                if script.is_absolute()
                else (cwd_path / script).resolve()
            )
        except OSError:
            return self.PROCESS_ROLE_UNCLASSIFIED

        if (
            cwd_path != self.project_root
            or script_path != self.main_path
        ):
            return self.PROCESS_ROLE_UNCLASSIFIED

        if tuple(tokens) == self.expected_argv:
            return self.PROCESS_ROLE_SERVICE_RUNTIME

        return self.PROCESS_ROLE_CONTROL_PLANE

    def _observed_main_processes(
        self,
    ) -> list[dict[str, Any]]:
        processes = []
        current_pid = os.getpid()
        proc_root = Path("/proc")

        if not proc_root.is_dir():
            return processes

        for entry in proc_root.iterdir():
            if not entry.name.isdigit():
                continue

            pid = int(entry.name)

            if pid == current_pid:
                continue

            argv = self._read_cmdline(pid)

            if not argv:
                continue

            executable = Path(
                argv[0]
            ).name.lower()
            has_main = any(
                Path(item).name == "main.py"
                for item in argv[1:]
            )

            if (
                executable.startswith("python")
                and has_main
            ):
                cwd = self._read_cwd(pid)
                processes.append(
                    {
                        "pid": pid,
                        "argv": argv,
                        "start_ticks": (
                            self._read_proc_start_ticks(
                                pid
                            )
                        ),
                        "cwd": cwd,
                        "process_role": (
                            self.classify_main_process_role(
                                argv,
                                cwd,
                            )
                        ),
                    }
                )

        return processes

    def _strict_main_processes(
        self,
    ) -> list[dict[str, Any]]:
        processes = []
        current_pid = os.getpid()
        proc_root = Path("/proc")

        if not proc_root.is_dir():
            return processes

        for entry in proc_root.iterdir():
            if not entry.name.isdigit():
                continue

            pid = int(entry.name)

            if pid == current_pid:
                continue

            argv = self._read_cmdline(pid)

            if not argv:
                continue

            executable = Path(
                argv[0]
            ).name.lower()
            has_main = any(
                Path(item).name == "main.py"
                for item in argv[1:]
            )

            if (
                executable.startswith("python")
                and has_main
            ):
                cwd = self._read_cwd(pid)
                process_role = (
                    self.classify_main_process_role(
                        argv,
                        cwd,
                    )
                )

                if (
                    process_role
                    == self.PROCESS_ROLE_CONTROL_PLANE
                ):
                    continue

                processes.append(
                    {
                        "pid": pid,
                        "argv": argv,
                        "start_ticks": (
                            self._read_proc_start_ticks(
                                pid
                            )
                        ),
                        "cwd": cwd,
                        "process_role": process_role,
                    }
                )

        return processes

    @contextmanager
    def _exclusive_lock(
        self,
    ) -> Iterator[None]:
        self.lock_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        descriptor = os.open(
            self.lock_path,
            os.O_RDWR | os.O_CREAT,
            0o600,
        )

        try:
            with os.fdopen(
                descriptor,
                "r+",
                encoding="utf-8",
            ) as handle:
                fcntl.flock(
                    handle.fileno(),
                    fcntl.LOCK_EX,
                )
                yield
                fcntl.flock(
                    handle.fileno(),
                    fcntl.LOCK_UN,
                )
        except BaseException:
            try:
                os.close(descriptor)
            except OSError:
                pass
            raise

    def _read_state(
        self,
    ) -> dict[str, Any] | None:
        try:
            return self.state_store.read()
        except PersistentServiceStateError as exc:
            raise ManualRuntimeControlError(
                exc.code,
                str(exc),
                details=exc.details,
            ) from exc

    def _write_state(
        self,
        packet: dict[str, Any],
    ) -> None:
        try:
            self.state_store.write(packet)
        except PersistentServiceStateError as exc:
            raise ManualRuntimeControlError(
                exc.code,
                str(exc),
                details=exc.details,
            ) from exc

    def _remove_state(self) -> None:
        try:
            self.state_store.remove()
        except PersistentServiceStateError as exc:
            raise ManualRuntimeControlError(
                exc.code,
                str(exc),
                details=exc.details,
            ) from exc

    def _command_digest(self) -> str:
        payload = json.dumps(
            list(self.expected_argv),
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(
            payload
        ).hexdigest()

    def _record_matches_process(
        self,
        record: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        try:
            pid = int(record["pid"])
            start_ticks = int(
                record.get(
                    "process_start_ticks",
                    record["proc_start_ticks"],
                )
            )
        except (
            KeyError,
            TypeError,
            ValueError,
        ):
            return (
                False,
                {
                    "reason": (
                        "record_missing_pid_identity"
                    )
                },
            )

        actual_ticks = (
            self._read_proc_start_ticks(pid)
        )
        argv = self._read_cmdline(pid)
        cwd = self._read_cwd(pid)
        current_boot_id = (
            PersistentServiceStateStore.boot_id()
        )
        record_uid = record.get(
            "host_uid",
            record.get("owner_uid"),
        )

        checks = {
            "schema_version_match": (
                record.get("schema_version")
                == self.SCHEMA_VERSION
            ),
            "pid_exists": actual_ticks
            is not None,
            "start_ticks_match": (
                actual_ticks == start_ticks
            ),
            "argv_match": (
                argv
                == list(self.expected_argv)
            ),
            "cwd_match": (
                cwd
                == str(self.project_root)
            ),
            "uid_match": (
                record_uid
                == os.getuid()
            ),
            "boot_id_match": (
                bool(current_boot_id)
                and record.get("boot_id")
                == current_boot_id
            ),
            "command_digest_match": (
                record.get("command_sha256")
                == self._command_digest()
            ),
            "bind_host_match": (
                record.get("bind_host")
                == self.HOST
            ),
            "bind_port_match": (
                record.get("bind_port")
                == self.PORT
            ),
        }

        return (
            all(checks.values()),
            {
                "pid": pid,
                "record_start_ticks": start_ticks,
                "actual_start_ticks": actual_ticks,
                "record_boot_id": record.get(
                    "boot_id"
                ),
                "current_boot_id": current_boot_id,
                "record_uid": record_uid,
                "current_uid": os.getuid(),
                "argv": argv,
                "cwd": cwd,
                "checks": checks,
            },
        )

    def _owned_listener_records(
        self,
        pid: int,
    ) -> list[dict[str, Any]]:
        inodes = self._socket_inodes_for_pid(
            pid
        )

        return [
            record
            for record in self._listener_records(
                self.PORT
            )
            if record["inode"] in inodes
        ]

    def _health_probe(
        self,
    ) -> dict[str, Any]:
        url = (
            f"http://{self.HOST}:{self.PORT}/health"
        )

        try:
            with urllib.request.urlopen(
                url,
                timeout=(
                    self.HEALTH_REQUEST_TIMEOUT_SECONDS
                ),
            ) as response:
                status_code = int(
                    response.status
                )
                body = response.read().decode(
                    "utf-8"
                )
        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ) as exc:
            return {
                "ok": False,
                "url": url,
                "reason": str(exc),
                "status_code": None,
                "payload": None,
            }

        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            return {
                "ok": False,
                "url": url,
                "reason": (
                    f"invalid_json:{exc}"
                ),
                "status_code": status_code,
                "payload": None,
            }

        ok = all(
            (
                status_code == 200,
                isinstance(payload, dict),
                payload.get("status") == "ok",
                payload.get("safe_idle") is True,
                payload.get(
                    "command_execution"
                )
                is False,
            )
        )

        return {
            "ok": ok,
            "url": url,
            "reason": (
                "healthy"
                if ok
                else "health_contract_mismatch"
            ),
            "status_code": status_code,
            "payload": payload,
        }

    def _audit_packet(
        self,
        *,
        action: str,
        decision: str,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "event_type": (
                "manual_service_control"
            ),
            "action": action,
            "decision": decision,
            "timestamp_utc": self._now_utc(),
            "actor_uid": os.getuid(),
            "permission_mode": (
                "explicit_cli_confirmation"
            ),
            "persisted": False,
            "persistence_boundary": (
                "Sprint 253 audit and log visibility"
            ),
            "details": dict(details),
        }

    def status(
        self,
        *,
        probe_health: bool = True,
    ) -> dict[str, Any]:
        record = self._read_state()
        listeners = self._listener_records(
            self.PORT
        )
        observed_processes = (
            self._observed_main_processes()
        )
        strict_processes = [
            item
            for item in observed_processes
            if item["process_role"]
            != self.PROCESS_ROLE_CONTROL_PLANE
        ]
        control_plane_processes = [
            item
            for item in observed_processes
            if item["process_role"]
            == self.PROCESS_ROLE_CONTROL_PLANE
        ]
        record_matches = False
        identity: dict[str, Any] = {
            "reason": "no_record"
        }
        owned_listeners: list[
            dict[str, Any]
        ] = []
        health = {
            "ok": False,
            "executed": False,
            "reason": "not_executed",
        }

        if record is not None:
            (
                record_matches,
                identity,
            ) = self._record_matches_process(
                record
            )

            if record_matches:
                pid = int(record["pid"])
                owned_listeners = (
                    self._owned_listener_records(
                        pid
                    )
                )

                if (
                    probe_health
                    and owned_listeners
                ):
                    health = self._health_probe()
                    health["executed"] = True

        record_classification = (
            self.state_store.classify(
                record,
                matches_process=record_matches,
            )
        )

        if record_matches:
            if owned_listeners:
                lifecycle_state = (
                    "running"
                    if health.get("ok")
                    else "running_unverified"
                )
                ownership_state = (
                    "verified_owned_process"
                )
                safe_idle = False
                reason = (
                    "owned process and listener "
                    "verified"
                )
            else:
                lifecycle_state = (
                    "starting_or_degraded"
                )
                ownership_state = (
                    "verified_process_without_listener"
                )
                safe_idle = False
                reason = (
                    "owned process exists without "
                    "canonical listener"
                )
        elif strict_processes or listeners:
            lifecycle_state = (
                "ownership_conflict"
            )
            ownership_state = (
                "unowned_runtime_visible"
            )
            safe_idle = False
            reason = (
                "runtime evidence exists without "
                "a matching temporary ownership record"
            )
        else:
            lifecycle_state = "stopped"
            ownership_state = (
                record_classification
                if record is not None
                else "clear"
            )
            safe_idle = True
            reason = (
                "persistent state requires explicit recovery"
                if record is not None
                else (
                    "no strict Python main.py process "
                    "and no canonical listener"
                )
            )

        return {
            "ok": True,
            "version": "1.1.2",
            "boundary": (
                "manual_start_stop_status_runtime"
            ),
            "bind_host": self.HOST,
            "bind_port": self.PORT,
            "lifecycle_state": lifecycle_state,
            "ownership_state": ownership_state,
            "safe_idle": safe_idle,
            "status_reason": reason,
            "state_path": str(
                self.state_path
            ),
            "lock_path": str(
                self.lock_path
            ),
            "log_path": str(
                self.log_path
            ),
            "state_record_exists": (
                record is not None
            ),
            "state_record_matches_process": (
                record_matches
            ),
            "state_record_classification": (
                record_classification
            ),
            "state_record_scope": (
                "persistent_project_runtime"
            ),
            "persistent_state_enabled": True,
            "persistent_state_schema_version": (
                self.SCHEMA_VERSION
            ),
            "state_recovery_requires_explicit_control": True,
            "state_record": record,
            "process_identity": identity,
            "native_process_role_classification": True,
            "observed_main_process_count": len(
                observed_processes
            ),
            "observed_main_processes": (
                observed_processes
            ),
            "control_plane_process_count": len(
                control_plane_processes
            ),
            "control_plane_processes": (
                control_plane_processes
            ),
            "strict_main_process_count": len(
                strict_processes
            ),
            "strict_main_processes": (
                strict_processes
            ),
            "listener_count": len(
                listeners
            ),
            "listener_records": listeners,
            "owned_listener_count": len(
                owned_listeners
            ),
            "owned_listener_records": (
                owned_listeners
            ),
            "health": health,
            "status_observation_enabled": True,
            "process_control_used": False,
            "signal_sent": False,
            "service_start_executed": False,
            "service_stop_executed": False,
        }

    def _ensure_stopped_preflight(
        self,
    ) -> dict[str, Any]:
        status = self.status(
            probe_health=True
        )

        if (
            status["state_record_matches_process"]
            and status["lifecycle_state"]
            in {
                "running",
                "running_unverified",
                "starting_or_degraded",
            }
        ):
            return {
                "already_running": True,
                "status": status,
            }

        if (
            status["strict_main_process_count"]
            or status["listener_count"]
        ):
            raise ManualRuntimeControlError(
                "ownership_conflict",
                (
                    "Manual start refused because "
                    "unowned runtime evidence is visible."
                ),
                details={
                    "status": status,
                },
            )

        if status["state_record_exists"]:
            self._remove_state()

        return {
            "already_running": False,
            "status": status,
        }

    def _terminate_owned(
        self,
        record: dict[str, Any],
        *,
        allow_kill_fallback: bool,
    ) -> dict[str, Any]:
        matches, identity = (
            self._record_matches_process(
                record
            )
        )

        if not matches:
            raise ManualRuntimeControlError(
                "ownership_verification_failed",
                (
                    "Refusing to signal a process "
                    "that does not match the ownership record."
                ),
                details={
                    "identity": identity,
                },
            )

        pid = int(record["pid"])
        started = time.monotonic()
        os.kill(
            pid,
            signal.SIGTERM,
        )
        term_sent = True
        kill_sent = False
        deadline = (
            time.monotonic()
            + self.STOP_TIMEOUT_SECONDS
        )

        while time.monotonic() < deadline:
            if (
                self._read_proc_start_ticks(
                    pid
                )
                is None
                and not self._listener_records(
                    self.PORT
                )
            ):
                return {
                    "stopped": True,
                    "term_sent": term_sent,
                    "kill_sent": kill_sent,
                    "elapsed_milliseconds": int(
                        (
                            time.monotonic()
                            - started
                        )
                        * 1000
                    ),
                }

            time.sleep(
                self.POLL_INTERVAL_SECONDS
            )

        if not allow_kill_fallback:
            return {
                "stopped": False,
                "term_sent": term_sent,
                "kill_sent": kill_sent,
                "elapsed_milliseconds": int(
                    (
                        time.monotonic()
                        - started
                    )
                    * 1000
                ),
            }

        matches_after, identity_after = (
            self._record_matches_process(
                record
            )
        )

        if not matches_after:
            if (
                self._read_proc_start_ticks(
                    pid
                )
                is None
            ):
                return {
                    "stopped": True,
                    "term_sent": term_sent,
                    "kill_sent": kill_sent,
                    "elapsed_milliseconds": int(
                        (
                            time.monotonic()
                            - started
                        )
                        * 1000
                    ),
                }

            raise ManualRuntimeControlError(
                "ownership_changed_during_stop",
                (
                    "Owned process identity changed "
                    "before bounded fallback."
                ),
                details={
                    "identity": identity_after,
                },
            )

        os.kill(
            pid,
            signal.SIGKILL,
        )
        kill_sent = True
        kill_deadline = (
            time.monotonic()
            + self.KILL_TIMEOUT_SECONDS
        )

        while time.monotonic() < kill_deadline:
            if (
                self._read_proc_start_ticks(
                    pid
                )
                is None
                and not self._listener_records(
                    self.PORT
                )
            ):
                return {
                    "stopped": True,
                    "term_sent": term_sent,
                    "kill_sent": kill_sent,
                    "elapsed_milliseconds": int(
                        (
                            time.monotonic()
                            - started
                        )
                        * 1000
                    ),
                }

            time.sleep(
                self.POLL_INTERVAL_SECONDS
            )

        return {
            "stopped": False,
            "term_sent": term_sent,
            "kill_sent": kill_sent,
            "elapsed_milliseconds": int(
                (
                    time.monotonic()
                    - started
                )
                * 1000
            ),
        }

    def start(
        self,
        *,
        approved: bool,
        confirmed_localhost: bool,
    ) -> dict[str, Any]:
        if not approved:
            raise ManualRuntimeControlError(
                "approval_required",
                (
                    "Manual start requires "
                    "--approve-start."
                ),
            )

        if not confirmed_localhost:
            raise ManualRuntimeControlError(
                "localhost_confirmation_required",
                (
                    "Manual start requires "
                    "--confirm-localhost."
                ),
            )

        with self._exclusive_lock():
            preflight = (
                self._ensure_stopped_preflight()
            )

            if preflight["already_running"]:
                status = preflight["status"]

                return {
                    "ok": True,
                    "action": "manual_start",
                    "result": "already_running",
                    "idempotent": True,
                    "process_created": False,
                    "status": status,
                    "audit_event": (
                        self._audit_packet(
                            action="manual_start",
                            decision="already_running",
                            details={
                                "idempotent": True,
                            },
                        )
                    ),
                }

            self.log_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            log_descriptor = os.open(
                self.log_path,
                os.O_WRONLY
                | os.O_CREAT
                | os.O_APPEND,
                0o600,
            )
            environment = dict(
                os.environ
            )
            environment["PYTHONUNBUFFERED"] = "1"
            started_at = time.monotonic()

            try:
                with os.fdopen(
                    log_descriptor,
                    "ab",
                    buffering=0,
                ) as log_handle:
                    process = subprocess.Popen(
                        list(self.expected_argv),
                        cwd=str(
                            self.project_root
                        ),
                        stdin=subprocess.DEVNULL,
                        stdout=log_handle,
                        stderr=subprocess.STDOUT,
                        env=environment,
                        start_new_session=True,
                        close_fds=True,
                    )
            except BaseException as exc:
                try:
                    os.close(log_descriptor)
                except OSError:
                    pass
                raise ManualRuntimeControlError(
                    "process_launch_failed",
                    (
                        "Canonical lifecycle process "
                        "could not be launched."
                    ),
                    details={
                        "reason": str(exc),
                        "argv": list(
                            self.expected_argv
                        ),
                    },
                ) from exc

            start_ticks = (
                self._read_proc_start_ticks(
                    process.pid
                )
            )

            if start_ticks is None:
                try:
                    process.terminate()
                except OSError:
                    pass
                raise ManualRuntimeControlError(
                    "process_identity_unavailable",
                    (
                        "Launched process identity "
                        "could not be verified."
                    ),
                    details={
                        "pid": process.pid,
                    },
                )

            timestamp = self._now_utc()
            record = {
                "schema_version": (
                    self.SCHEMA_VERSION
                ),
                "pid": process.pid,
                "process_start_ticks": start_ticks,
                "proc_start_ticks": start_ticks,
                "boot_id": (
                    PersistentServiceStateStore.boot_id()
                ),
                "argv": list(
                    self.expected_argv
                ),
                "command_sha256": (
                    self._command_digest()
                ),
                "cwd": str(
                    self.project_root
                ),
                "host_uid": os.getuid(),
                "owner_uid": os.getuid(),
                "bind_host": self.HOST,
                "bind_port": self.PORT,
                "started_at": timestamp,
                "updated_at": timestamp,
                "created_at_utc": timestamp,
                "start_new_session": True,
                "state_scope": (
                    "persistent_project_runtime"
                ),
            }
            try:
                self._write_state(record)
            except Exception as exc:
                rollback = {
                    "term_sent": False,
                    "kill_sent": False,
                    "stopped": False,
                }

                try:
                    process.terminate()
                    rollback["term_sent"] = True
                    process.wait(
                        timeout=(
                            self.KILL_TIMEOUT_SECONDS
                        )
                    )
                    rollback["stopped"] = True
                except subprocess.TimeoutExpired:
                    process.kill()
                    rollback["kill_sent"] = True

                    try:
                        process.wait(
                            timeout=(
                                self.KILL_TIMEOUT_SECONDS
                            )
                        )
                        rollback["stopped"] = True
                    except subprocess.TimeoutExpired:
                        rollback["stopped"] = False
                except OSError:
                    rollback["stopped"] = (
                        process.poll()
                        is not None
                    )

                raise ManualRuntimeControlError(
                    "state_write_failed_after_launch",
                    (
                        "Temporary ownership state "
                        "could not be written after launch."
                    ),
                    details={
                        "pid": process.pid,
                        "rollback": rollback,
                        "reason": str(exc),
                    },
                ) from exc

            deadline = (
                time.monotonic()
                + self.START_TIMEOUT_SECONDS
            )
            last_health: dict[str, Any] = {
                "ok": False,
                "reason": "not_attempted",
            }

            while time.monotonic() < deadline:
                return_code = process.poll()

                if return_code is not None:
                    self._remove_state()
                    raise ManualRuntimeControlError(
                        "process_exited_during_start",
                        (
                            "Canonical lifecycle process "
                            "exited before readiness."
                        ),
                        details={
                            "return_code": (
                                return_code
                            ),
                            "log_path": str(
                                self.log_path
                            ),
                        },
                    )

                matches, identity = (
                    self._record_matches_process(
                        record
                    )
                )

                if not matches:
                    rollback = (
                        self._terminate_owned(
                            record,
                            allow_kill_fallback=True,
                        )
                    )
                    self._remove_state()
                    raise ManualRuntimeControlError(
                        "ownership_lost_during_start",
                        (
                            "Process ownership could not "
                            "be maintained during startup."
                        ),
                        details={
                            "identity": identity,
                            "rollback": rollback,
                        },
                    )

                owned_listeners = (
                    self._owned_listener_records(
                        process.pid
                    )
                )

                if owned_listeners:
                    last_health = (
                        self._health_probe()
                    )

                    if last_health.get("ok"):
                        status = self.status(
                            probe_health=True
                        )

                        return {
                            "ok": True,
                            "action": (
                                "manual_start"
                            ),
                            "result": "started",
                            "idempotent": False,
                            "process_created": True,
                            "pid": process.pid,
                            "time_to_ready_milliseconds": int(
                                (
                                    time.monotonic()
                                    - started_at
                                )
                                * 1000
                            ),
                            "status": status,
                            "audit_event": (
                                self._audit_packet(
                                    action=(
                                        "manual_start"
                                    ),
                                    decision="approved",
                                    details={
                                        "pid": process.pid,
                                        "health": (
                                            last_health
                                        ),
                                    },
                                )
                            ),
                        }

                time.sleep(
                    self.POLL_INTERVAL_SECONDS
                )

            rollback = self._terminate_owned(
                record,
                allow_kill_fallback=True,
            )

            if rollback["stopped"]:
                self._remove_state()
                timeout_code = "start_timeout"
            else:
                timeout_code = (
                    "start_timeout_rollback_incomplete"
                )

            raise ManualRuntimeControlError(
                timeout_code,
                (
                    "Canonical lifecycle process did "
                    "not become healthy before timeout."
                ),
                details={
                    "timeout_seconds": (
                        self.START_TIMEOUT_SECONDS
                    ),
                    "last_health": last_health,
                    "rollback": rollback,
                    "log_path": str(
                        self.log_path
                    ),
                },
            )

    def stop(
        self,
        *,
        approved: bool,
    ) -> dict[str, Any]:
        if not approved:
            raise ManualRuntimeControlError(
                "approval_required",
                (
                    "Manual stop requires "
                    "--approve-stop."
                ),
            )

        with self._exclusive_lock():
            record = self._read_state()
            status_before = self.status(
                probe_health=True
            )

            if record is None:
                if (
                    status_before[
                        "strict_main_process_count"
                    ]
                    == 0
                    and status_before[
                        "listener_count"
                    ]
                    == 0
                ):
                    return {
                        "ok": True,
                        "action": "manual_stop",
                        "result": "already_stopped",
                        "idempotent": True,
                        "signal_sent": False,
                        "status": status_before,
                        "audit_event": (
                            self._audit_packet(
                                action="manual_stop",
                                decision=(
                                    "already_stopped"
                                ),
                                details={
                                    "idempotent": True,
                                },
                            )
                        ),
                    }

                raise ManualRuntimeControlError(
                    "ownership_record_required",
                    (
                        "Manual stop refused because "
                        "runtime evidence exists without "
                        "an ownership record."
                    ),
                    details={
                        "status": status_before,
                    },
                )

            matches, identity = (
                self._record_matches_process(
                    record
                )
            )

            if not matches:
                if (
                    status_before[
                        "strict_main_process_count"
                    ]
                    == 0
                    and status_before[
                        "listener_count"
                    ]
                    == 0
                ):
                    self._remove_state()

                    return {
                        "ok": True,
                        "action": "manual_stop",
                        "result": (
                            "stale_record_cleared"
                        ),
                        "idempotent": True,
                        "signal_sent": False,
                        "status": self.status(
                            probe_health=False
                        ),
                        "audit_event": (
                            self._audit_packet(
                                action="manual_stop",
                                decision=(
                                    "stale_record_cleared"
                                ),
                                details={
                                    "identity": identity,
                                },
                            )
                        ),
                    }

                raise ManualRuntimeControlError(
                    "ownership_verification_failed",
                    (
                        "Manual stop refused because "
                        "the process identity does not "
                        "match the ownership record."
                    ),
                    details={
                        "identity": identity,
                        "status": status_before,
                    },
                )

            stopped = self._terminate_owned(
                record,
                allow_kill_fallback=True,
            )

            if not stopped["stopped"]:
                raise ManualRuntimeControlError(
                    "stop_timeout",
                    (
                        "Owned lifecycle process did "
                        "not stop within the bounded timeout."
                    ),
                    details={
                        "stop_result": stopped,
                        "status": self.status(
                            probe_health=False
                        ),
                    },
                )

            self._remove_state()
            status_after = self.status(
                probe_health=False
            )

            if (
                status_after[
                    "strict_main_process_count"
                ]
                != 0
                or status_after[
                    "listener_count"
                ]
                != 0
            ):
                raise ManualRuntimeControlError(
                    "shutdown_verification_failed",
                    (
                        "Runtime evidence remains after "
                        "the owned process stopped."
                    ),
                    details={
                        "status": status_after,
                        "stop_result": stopped,
                    },
                )

            return {
                "ok": True,
                "action": "manual_stop",
                "result": "stopped",
                "idempotent": False,
                "signal_sent": True,
                "term_sent": stopped[
                    "term_sent"
                ],
                "kill_sent": stopped[
                    "kill_sent"
                ],
                "time_to_stopped_milliseconds": (
                    stopped[
                        "elapsed_milliseconds"
                    ]
                ),
                "status": status_after,
                "audit_event": (
                    self._audit_packet(
                        action="manual_stop",
                        decision="approved",
                        details={
                            "pid": record["pid"],
                            "stop_result": stopped,
                        },
                    )
                ),
            }
