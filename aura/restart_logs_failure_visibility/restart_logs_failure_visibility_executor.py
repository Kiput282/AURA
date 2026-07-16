from __future__ import annotations

import errno
import fcntl
import os
import re
import stat
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from aura.manual_start_stop_status_runtime.manual_start_stop_status_runtime_executor import (
    ManualRuntimeControlError,
    ManualStartStopStatusRuntimeExecutor,
)


class RestartLogsFailureVisibilityError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        stage: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.stage = stage
        self.details = details or {}

    def packet(self) -> dict[str, Any]:
        return {
            "ok": False,
            "error": self.code,
            "message": self.message,
            "stage": self.stage,
            "details": self.details,
        }


class RestartLogsFailureVisibilityExecutor:
    SCHEMA_VERSION = 1
    MAX_TAIL_LINES = 200
    MAX_TAIL_BYTES = 65536
    RESTART_GAP_SECONDS = 0.25
    SOURCES = ("active", "latest-rotated", "runtime")
    ROTATED = re.compile(
        r"^aura\.\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d{6}\.log"
        r"(?:\.(?:gz|zip))?$"
    )
    SECRET_PATTERNS = (
        re.compile(
            r"(?i)\b(password|passwd|secret|token|api[_-]?key)"
            r"\b(\s*[:=]\s*)([^\s,;]+)"
        ),
        re.compile(
            r"(?i)\b(authorization)(\s*[:=]\s*)"
            r"(bearer\s+)?([^\s,;]+)"
        ),
        re.compile(
            r"(?i)\b(bearer)(\s+)([A-Za-z0-9._~+/=-]{8,})"
        ),
    )

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.project_root = Path(
            project_root if project_root is not None else Path.cwd()
        ).resolve()
        self.manual = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        uid = os.getuid()
        self.lock_path = Path(
            f"/tmp/aura-restart-logs-failure-visibility-{uid}.lock"
        )
        self.runtime_log_path = Path(
            f"/tmp/aura-manual-start-stop-status-{uid}.log"
        )
        self.logs_path = self.project_root / "logs"

    @staticmethod
    def _temporary_mode_is_private(
        metadata: os.stat_result,
    ) -> bool:
        return (
            stat.S_IMODE(metadata.st_mode)
            & 0o077
        ) == 0

    @staticmethod
    def _close_descriptor(
        descriptor: int,
    ) -> None:
        try:
            os.close(descriptor)
        except OSError:
            pass

    def _open_restart_lock(
        self,
    ) -> tuple[int, os.stat_result]:
        flags = (
            os.O_CREAT
            | os.O_RDWR
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )

        try:
            descriptor = os.open(
                self.lock_path,
                flags,
                0o600,
            )
        except OSError as exc:
            code = (
                "restart_lock_symlink_rejected"
                if exc.errno == errno.ELOOP
                else "restart_lock_open_failed"
            )
            raise RestartLogsFailureVisibilityError(
                code,
                (
                    "The supervised restart lock "
                    "could not be opened safely."
                ),
                stage="preflight",
                details={
                    "path": self.lock_path.as_posix(),
                    "reason": str(exc),
                },
            ) from exc

        metadata = os.fstat(descriptor)
        mode = stat.S_IMODE(
            metadata.st_mode
        )

        if not stat.S_ISREG(
            metadata.st_mode
        ):
            self._close_descriptor(
                descriptor
            )
            raise RestartLogsFailureVisibilityError(
                "restart_lock_type_rejected",
                (
                    "The supervised restart lock "
                    "is not a regular file."
                ),
                stage="preflight",
                details={
                    "path": (
                        self.lock_path.as_posix()
                    ),
                },
            )

        if metadata.st_uid != os.getuid():
            self._close_descriptor(
                descriptor
            )
            raise RestartLogsFailureVisibilityError(
                "restart_lock_owner_rejected",
                (
                    "The supervised restart lock "
                    "is not owned by this user."
                ),
                stage="preflight",
                details={
                    "path": (
                        self.lock_path.as_posix()
                    ),
                    "uid": metadata.st_uid,
                },
            )

        if not self._temporary_mode_is_private(
            metadata
        ):
            self._close_descriptor(
                descriptor
            )
            raise RestartLogsFailureVisibilityError(
                "restart_lock_mode_rejected",
                (
                    "The supervised restart lock "
                    "permissions are too broad."
                ),
                stage="preflight",
                details={
                    "path": (
                        self.lock_path.as_posix()
                    ),
                    "mode": oct(mode),
                },
            )

        return descriptor, metadata

    @contextmanager
    def _lock(self) -> Iterator[None]:
        (
            descriptor,
            opened_metadata,
        ) = self._open_restart_lock()
        handle = os.fdopen(
            descriptor,
            "r+",
            encoding="utf-8",
        )

        try:
            fcntl.flock(
                handle.fileno(),
                fcntl.LOCK_EX
                | fcntl.LOCK_NB,
            )
        except BlockingIOError as exc:
            handle.close()
            raise RestartLogsFailureVisibilityError(
                "restart_control_busy",
                (
                    "Another supervised restart "
                    "owns the control lock."
                ),
                stage="preflight",
            ) from exc

        try:
            yield
        finally:
            try:
                fcntl.flock(
                    handle.fileno(),
                    fcntl.LOCK_UN,
                )
            finally:
                handle.close()

                try:
                    current = (
                        self.lock_path.lstat()
                    )
                except FileNotFoundError:
                    current = None

                if (
                    current is not None
                    and current.st_dev
                    == opened_metadata.st_dev
                    and current.st_ino
                    == opened_metadata.st_ino
                    and current.st_uid
                    == os.getuid()
                ):
                    self.lock_path.unlink(
                        missing_ok=True
                    )

    @staticmethod
    def _live(packet: dict[str, Any]) -> dict[str, Any]:
        value = packet.get("live_status")
        return value if isinstance(value, dict) else packet

    @staticmethod
    def _pick(
        packet: dict[str, Any],
        *names: str,
        default: Any = None,
    ) -> Any:
        for name in names:
            if name in packet:
                return packet[name]
        return default

    def _resolve_source(self, source: str) -> tuple[Path, str]:
        if source not in self.SOURCES:
            raise RestartLogsFailureVisibilityError(
                "invalid_log_source",
                "Log source is not allowlisted.",
                stage="log_preflight",
                details={"allowed_sources": list(self.SOURCES)},
            )
        if source == "active":
            path = self.logs_path / "aura.log"
            classification = "active_canonical_log"
        elif source == "runtime":
            path = self.runtime_log_path
            classification = "temporary_owned_runtime_log"
        else:
            candidates = []
            if self.logs_path.is_dir() and not self.logs_path.is_symlink():
                candidates = [
                    item
                    for item in self.logs_path.iterdir()
                    if (
                        item.is_file()
                        and not item.is_symlink()
                        and self.ROTATED.fullmatch(item.name)
                    )
                ]
            if not candidates:
                raise RestartLogsFailureVisibilityError(
                    "log_source_unavailable",
                    "No recognized rotated AURA log is available.",
                    stage="log_preflight",
                )
            path = max(
                candidates,
                key=lambda item: item.stat().st_mtime_ns,
            )
            classification = "latest_recognized_rotated_log"

        if path.is_symlink():
            raise RestartLogsFailureVisibilityError(
                "log_symlink_rejected",
                "Symlink log sources are not allowed.",
                stage="log_preflight",
            )
        if not path.is_file():
            raise RestartLogsFailureVisibilityError(
                "log_source_unavailable",
                "The allowlisted log source is unavailable.",
                stage="log_preflight",
                details={"path": path.as_posix()},
            )
        return path, classification

    @classmethod
    def _redact(cls, line: str) -> str:
        line = cls.SECRET_PATTERNS[0].sub(
            lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]",
            line,
        )
        line = cls.SECRET_PATTERNS[1].sub(
            lambda m: (
                f"{m.group(1)}{m.group(2)}"
                f"{m.group(3) or ''}[REDACTED]"
            ),
            line,
        )
        return cls.SECRET_PATTERNS[2].sub(
            lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]",
            line,
        )

    def tail(
        self,
        *,
        source: str,
        lines: int,
    ) -> dict[str, Any]:
        if (
            isinstance(lines, bool)
            or not isinstance(lines, int)
            or not 1 <= lines <= self.MAX_TAIL_LINES
        ):
            raise RestartLogsFailureVisibilityError(
                "invalid_line_count",
                "Line count must be between 1 and 200.",
                stage="log_preflight",
            )

        path, classification = (
            self._resolve_source(source)
        )
        flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )

        try:
            descriptor = os.open(
                path,
                flags,
            )
        except FileNotFoundError as exc:
            raise RestartLogsFailureVisibilityError(
                "log_source_unavailable",
                (
                    "The allowlisted log source "
                    "is unavailable."
                ),
                stage="log_preflight",
                details={
                    "path": path.as_posix(),
                },
            ) from exc
        except OSError as exc:
            code = (
                "log_symlink_rejected"
                if exc.errno == errno.ELOOP
                else "log_open_failed"
            )
            raise RestartLogsFailureVisibilityError(
                code,
                (
                    "The allowlisted log source "
                    "could not be opened safely."
                ),
                stage="log_preflight",
                details={
                    "path": path.as_posix(),
                    "reason": str(exc),
                },
            ) from exc

        before = os.fstat(descriptor)
        mode = stat.S_IMODE(
            before.st_mode
        )

        if not stat.S_ISREG(
            before.st_mode
        ):
            self._close_descriptor(
                descriptor
            )
            raise RestartLogsFailureVisibilityError(
                "log_type_rejected",
                (
                    "The allowlisted log source "
                    "is not a regular file."
                ),
                stage="log_preflight",
                details={
                    "path": path.as_posix(),
                },
            )

        if (
            classification
            == "temporary_owned_runtime_log"
        ):
            if before.st_uid != os.getuid():
                self._close_descriptor(
                    descriptor
                )
                raise RestartLogsFailureVisibilityError(
                    "runtime_log_owner_rejected",
                    (
                        "The temporary runtime log "
                        "is not owned by this user."
                    ),
                    stage="log_preflight",
                    details={
                        "path": path.as_posix(),
                        "uid": before.st_uid,
                    },
                )

            if not self._temporary_mode_is_private(
                before
            ):
                self._close_descriptor(
                    descriptor
                )
                raise RestartLogsFailureVisibilityError(
                    "runtime_log_mode_rejected",
                    (
                        "The temporary runtime log "
                        "permissions are too broad."
                    ),
                    stage="log_preflight",
                    details={
                        "path": path.as_posix(),
                        "mode": oct(mode),
                    },
                )

        window = min(
            before.st_size,
            self.MAX_TAIL_BYTES,
        )

        with os.fdopen(
            descriptor,
            "rb",
        ) as handle:
            if window:
                handle.seek(
                    -window,
                    os.SEEK_END,
                )
            raw = handle.read(window)
            after = os.fstat(
                handle.fileno()
            )

        if (
            before.st_dev != after.st_dev
            or before.st_ino
            != after.st_ino
        ):
            raise RestartLogsFailureVisibilityError(
                "log_identity_changed",
                (
                    "Log identity changed during "
                    "the bounded read."
                ),
                stage="log_read",
            )

        visible = raw.decode(
            "utf-8",
            errors="replace",
        ).splitlines()[-lines:]
        redacted = [self._redact(line) for line in visible]

        return {
            "ok": True,
            "schema_version": self.SCHEMA_VERSION,
            "boundary": "restart_logs_failure_visibility",
            "operation": "bounded_log_tail",
            "source": source,
            "classification": classification,
            "path": path.as_posix(),
            "requested_lines": lines,
            "returned_lines": len(redacted),
            "max_lines": self.MAX_TAIL_LINES,
            "max_bytes": self.MAX_TAIL_BYTES,
            "bytes_read": len(raw),
            "file_size_bytes": after.st_size,
            "redaction_applied": True,
            "truncated_to_byte_window": after.st_size > window,
            "lines": redacted,
            "mutation_performed": False,
            "symlink_followed": False,
        }

    def status(self) -> dict[str, Any]:
        manual = self.manual.status()
        return {
            "schema_version": self.SCHEMA_VERSION,
            "boundary": "restart_logs_failure_visibility",
            "restart_executor_available": True,
            "bounded_log_tail_available": True,
            "allowed_log_sources": list(self.SOURCES),
            "restart_gap_seconds": self.RESTART_GAP_SECONDS,
            "manual_runtime_status": manual,
            "live_status": self._live(manual),
            "systemd_execution": False,
            "autostart_execution": False,
            "non_loopback_binding": False,
            "arbitrary_pid_signal": False,
            "arbitrary_log_path": False,
            "log_mutation": False,
            "descriptor_nofollow_enabled": True,
            "temporary_file_owner_check": True,
            "temporary_file_mode_check": True,
            "descriptor_fstat_check": True,
        }

    def _safe_idle(self) -> bool:
        live = self._live(self.manual.status())
        return (
            self._pick(live, "lifecycle_state") == "stopped"
            and self._pick(live, "listener_count", default=0) == 0
            and self._pick(
                live,
                "strict_main_process_count",
                "process_count",
                default=0,
            )
            == 0
        )

    def restart(self) -> dict[str, Any]:
        with self._lock():
            started = time.monotonic()
            before = self.manual.status()
            live = self._live(before)
            state = self._pick(
                live,
                "lifecycle_state",
                default="unknown",
            )
            ownership = self._pick(
                live,
                "ownership_state",
                default="unknown",
            )
            listeners = self._pick(
                live,
                "listener_count",
                default=0,
            )
            processes = self._pick(
                live,
                "strict_main_process_count",
                "process_count",
                default=0,
            )

            if (
                (listeners or processes)
                and ownership
                not in {"verified_owned_process", "owned"}
            ):
                raise RestartLogsFailureVisibilityError(
                    "unowned_runtime_rejected",
                    "Restart refused for unowned runtime evidence.",
                    stage="ownership",
                    details={"before": before},
                )

            stop_result = None
            try:
                if state != "stopped":
                    stop_result = self.manual.stop(approved=True)

                if not self._safe_idle():
                    raise RestartLogsFailureVisibilityError(
                        "restart_stop_verification_failed",
                        "Runtime evidence remains after stop.",
                        stage="stop_verification",
                    )

                time.sleep(self.RESTART_GAP_SECONDS)
                start_result = self.manual.start(
                    approved=True,
                    confirmed_localhost=True,
                )
                after = self.manual.status()
                after_live = self._live(after)
                result_name = self._pick(
                    start_result,
                    "result",
                    "status",
                )
                ready = (
                    self._pick(
                        after_live,
                        "lifecycle_state",
                    )
                    == "running"
                    and self._pick(
                        after_live,
                        "listener_count",
                        default=0,
                    )
                    >= 1
                    and self._pick(
                        after_live,
                        "strict_main_process_count",
                        "process_count",
                        default=0,
                    )
                    >= 1
                    and self._pick(
                        after_live,
                        "ownership_state",
                    )
                    in {"verified_owned_process", "owned"}
                    and result_name
                    in {"started", "already_running", "running"}
                )
                if not ready:
                    raise RestartLogsFailureVisibilityError(
                        "restart_health_verification_failed",
                        "Fresh service did not satisfy readiness.",
                        stage="health_verification",
                        details={
                            "start_result": start_result,
                            "after": after,
                        },
                    )

            except RestartLogsFailureVisibilityError:
                try:
                    self.manual.stop(approved=True)
                except Exception:
                    pass
                raise
            except ManualRuntimeControlError as exc:
                try:
                    self.manual.stop(approved=True)
                except Exception:
                    pass
                try:
                    cause = exc.packet()
                except Exception:
                    cause = {
                        "error": type(exc).__name__,
                        "message": str(exc),
                    }
                raise RestartLogsFailureVisibilityError(
                    "restart_manual_runtime_failed",
                    "Canonical manual runtime rejected restart.",
                    stage="process_launch",
                    details={"cause": cause},
                ) from exc

            return {
                "ok": True,
                "schema_version": self.SCHEMA_VERSION,
                "boundary": "restart_logs_failure_visibility",
                "operation": "restart",
                "result": "restarted",
                "before_lifecycle_state": state,
                "stop_result": stop_result,
                "start_result": start_result,
                "after_status": after,
                "time_to_restarted_milliseconds": int(
                    (time.monotonic() - started) * 1000
                ),
                "restart_gap_milliseconds": int(
                    self.RESTART_GAP_SECONDS * 1000
                ),
                "ownership_verified": True,
                "health_contract_verified": True,
                "loopback_only": True,
                "systemd_used": False,
                "autostart_used": False,
                "failure": None,
            }
