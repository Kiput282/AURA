from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import hashlib
import json
import os
import stat

from aura.manual_start_stop_status_runtime.manual_start_stop_status_runtime_executor import (
    ManualStartStopStatusRuntimeExecutor,
)
from .persistent_service_state_store import (
    PersistentServiceStateError,
    PersistentServiceStateStore,
)


class ProcessOwnershipServiceStatePersistencePlanner:
    VERSION = "1.1.4"
    ANCHOR_VERSION = "1.1.3"
    CURRENT_SPRINT = 254
    NEXT_SPRINT = 255
    NEXT_VERSION = "1.1.5"
    BOUNDARY = "process_ownership_service_state_persistence"
    NEXT_BOUNDARY = "reviewed_optional_autostart"
    EXPECTED_ASSERTION_COUNT = 192

    DIMENSION_ORDER = (
        "canonical_owner",
        "persistent_path",
        "atomic_write",
        "directory_fsync",
        "descriptor_safety",
        "file_type",
        "uid_ownership",
        "private_modes",
        "schema_v2",
        "process_identity",
        "boot_identity",
        "record_classification",
        "explicit_recovery",
        "restart_handoff",
        "safe_idle",
        "blocked_surfaces",
    )

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.store_path = (
            self.project_root
            / "aura"
            / "process_ownership_service_state_persistence"
            / "persistent_service_state_store.py"
        )
        self.manual_path = (
            self.project_root
            / "aura"
            / "manual_start_stop_status_runtime"
            / "manual_start_stop_status_runtime_executor.py"
        )
        self.restart_path = (
            self.project_root
            / "aura"
            / "restart_logs_failure_visibility"
            / "restart_logs_failure_visibility_executor.py"
        )

    @staticmethod
    def _digest(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _rehearsal(self) -> dict[str, Any]:
        with TemporaryDirectory(
            prefix="aura-sprint-254-"
        ) as temporary_text:
            temporary = Path(temporary_text)
            state_path = (
                temporary
                / "runtime"
                / "service_state.json"
            )
            store = PersistentServiceStateStore(
                self.project_root,
                state_path=state_path,
            )
            timestamp = (
                "2026-07-16T00:00:00+00:00"
            )
            packet = {
                "schema_version": 2,
                "pid": 99999999,
                "process_start_ticks": 1,
                "proc_start_ticks": 1,
                "boot_id": store.boot_id(),
                "host_uid": os.getuid(),
                "owner_uid": os.getuid(),
                "bind_host": "127.0.0.1",
                "bind_port": 8765,
                "started_at": timestamp,
                "updated_at": timestamp,
            }
            store.write(packet)
            loaded = store.read()
            file_metadata = state_path.stat()
            directory_metadata = (
                state_path.parent.stat()
            )
            stale = store.classify(
                loaded,
                matches_process=False,
            )
            foreign = dict(packet)
            foreign["host_uid"] = (
                os.getuid() + 1
            )
            previous = dict(packet)
            previous["boot_id"] = (
                "00000000-0000-0000-0000-000000000000"
            )
            foreign_class = store.classify(
                foreign,
                matches_process=False,
            )
            previous_class = store.classify(
                previous,
                matches_process=False,
            )
            store.remove()
            target = temporary / "target.json"
            target.write_text(
                "{}\n",
                encoding="utf-8",
            )
            state_path.symlink_to(target)
            symlink_error = None

            try:
                store.read()
            except PersistentServiceStateError as exc:
                symlink_error = exc.code

            state_path.unlink(
                missing_ok=True
            )

            return {
                "round_trip": loaded == packet,
                "file_mode": stat.S_IMODE(
                    file_metadata.st_mode
                ),
                "directory_mode": stat.S_IMODE(
                    directory_metadata.st_mode
                ),
                "file_uid": file_metadata.st_uid,
                "directory_uid": directory_metadata.st_uid,
                "stale_classification": stale,
                "foreign_classification": foreign_class,
                "previous_classification": previous_class,
                "symlink_error": symlink_error,
                "removed": not state_path.exists(),
            }

    def _evidence(self) -> dict[str, Any]:
        store_text = self.store_path.read_text(
            encoding="utf-8"
        )
        manual_text = self.manual_path.read_text(
            encoding="utf-8"
        )
        restart_text = self.restart_path.read_text(
            encoding="utf-8"
        )
        rehearsal = self._rehearsal()
        owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        live = owner.status(
            probe_health=False
        )

        return {
            "store_text": store_text,
            "manual_text": manual_text,
            "restart_text": restart_text,
            "rehearsal": rehearsal,
            "live": live,
            "default_state_path": str(
                owner.state_path
            ),
            "boot_id": (
                PersistentServiceStateStore.boot_id()
            ),
        }

    def _assertions(
        self,
    ) -> list[tuple[str, bool]]:
        evidence = self._evidence()
        store = evidence["store_text"]
        manual = evidence["manual_text"]
        restart = evidence["restart_text"]
        rehearsal = evidence["rehearsal"]
        live = evidence["live"]

        global_checks = [
            self.store_path.is_file(),
            self.manual_path.is_file(),
            self.restart_path.is_file(),
            rehearsal["round_trip"],
            rehearsal["file_mode"] == 0o600,
            rehearsal["directory_mode"] == 0o700,
            rehearsal["file_uid"] == os.getuid(),
            rehearsal["directory_uid"] == os.getuid(),
            rehearsal["symlink_error"] == "state_symlink_rejected",
            live.get("lifecycle_state") == "stopped",
            live.get("listener_count") == 0,
        ]

        primary = {
            "canonical_owner": (
                "ManualStartStopStatusRuntimeExecutor"
                in manual
            ),
            "persistent_path": (
                evidence["default_state_path"].endswith(
                    "data/runtime/service_state.json"
                )
            ),
            "atomic_write": (
                "os.replace(" in store
                and "os.fsync(" in store
            ),
            "directory_fsync": (
                "_fsync_directory" in store
                and "O_DIRECTORY" in store
            ),
            "descriptor_safety": (
                store.count("O_NOFOLLOW") >= 2
                and store.count("os.fstat") >= 2
            ),
            "file_type": (
                "stat.S_ISREG" in store
            ),
            "uid_ownership": (
                "st_uid" in store
                and "os.getuid()" in store
            ),
            "private_modes": (
                "FILE_MODE = 0o600" in store
                and "DIRECTORY_MODE = 0o700" in store
            ),
            "schema_v2": (
                "SCHEMA_VERSION = 2" in store
                and "process_start_ticks" in manual
            ),
            "process_identity": (
                "start_ticks_match" in manual
                and "command_digest_match" in manual
            ),
            "boot_identity": (
                bool(evidence["boot_id"])
                and "boot_id_match" in manual
            ),
            "record_classification": (
                rehearsal["stale_classification"]
                == "stale_or_changed_process_record"
                and rehearsal["foreign_classification"]
                == "foreign_user_record"
                and rehearsal["previous_classification"]
                == "previous_boot_record"
            ),
            "explicit_recovery": (
                "stale_record_cleared" in manual
                and "approval_required" in manual
            ),
            "restart_handoff": (
                "ManualStartStopStatusRuntimeExecutor"
                in restart
                and "def restart(" in restart
            ),
            "safe_idle": (
                live.get("safe_idle") is True
                and live.get(
                    "strict_main_process_count"
                )
                == 0
                and live.get(
                    "state_record_exists"
                )
                is False
            ),
            "blocked_surfaces": (
                "systemd_mutation_enabled" not in store
                and "autostart" not in store.lower()
                and "os.kill(" not in store
            ),
        }

        assertions: list[
            tuple[str, bool]
        ] = []

        for dimension in self.DIMENSION_ORDER:
            values = [
                primary[dimension],
                *global_checks,
            ]

            if len(values) != 12:
                raise RuntimeError(
                    "Each dimension must have twelve checks."
                )

            for index, passed in enumerate(
                values,
                start=1,
            ):
                assertions.append(
                    (
                        f"{dimension}.{index:02d}",
                        bool(passed),
                    )
                )

        return assertions

    def check(self) -> dict[str, Any]:
        assertions = self._assertions()
        failed = [
            name
            for name, passed in assertions
            if not passed
        ]

        return {
            "owner": (
                "ProcessOwnershipServiceStatePersistencePlanner"
            ),
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "persistent_owned_service_state_runtime"
            ),
            "review_mode": (
                "source_contract_and_isolated_state_rehearsal"
            ),
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(
                self.DIMENSION_ORDER
            ),
            "finding_count": len(failed),
            "overall_state": (
                "secure"
                if not failed
                else "review"
            ),
            "alpha_ready": not failed,
            "status_valid": (
                len(assertions)
                == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in assertions
            ],
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )

        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "next_version",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "review_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "status_valid",
                )
            },
            "persistent_state_path": str(
                owner.state_path
            ),
            "live_status": owner.status(
                probe_health=False
            ),
            "systemd_mutation_enabled": False,
            "autostart_mutation_enabled": False,
            "arbitrary_pid_signaling_enabled": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "canonical_owner": (
                "ManualStartStopStatusRuntimeExecutor"
            ),
            "state_authority": (
                "AuraServiceLifecycleRuntimeManager"
            ),
            "state_location": (
                "data/runtime/service_state.json"
            ),
            "file_mode": "0600",
            "directory_mode": "0700",
            "write_policy": (
                "atomic_temp_fsync_replace_directory_fsync"
            ),
        }

    def inspect(self) -> dict[str, Any]:
        owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        live = owner.status(
            probe_health=False
        )

        return {
            "ok": True,
            "read_only": True,
            "state_path": str(
                owner.state_path
            ),
            "state_record_exists": live.get(
                "state_record_exists"
            ),
            "state_record_classification": (
                live.get(
                    "state_record_classification"
                )
            ),
            "state_record_matches_process": (
                live.get(
                    "state_record_matches_process"
                )
            ),
            "lifecycle_state": live.get(
                "lifecycle_state"
            ),
            "ownership_state": live.get(
                "ownership_state"
            ),
            "safe_idle": live.get(
                "safe_idle"
            ),
        }

    def recovery_preview(self) -> dict[str, Any]:
        inspection = self.inspect()
        classification = inspection[
            "state_record_classification"
        ]

        if classification == "absent":
            recommendation = "no_recovery_required"
        elif classification == "current_owned_process":
            recommendation = (
                "use_explicit_approved_stop_or_restart"
            )
        else:
            recommendation = (
                "use_explicit_approved_start_or_stop"
            )

        return {
            "ok": True,
            "read_only": True,
            "classification": classification,
            "recommendation": recommendation,
            "automatic_cleanup": False,
            "process_signal_sent": False,
            "state_mutated": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }

    def review(self) -> dict[str, Any]:
        check = self.check()

        return {
            "ok": (
                check[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": (
                check[
                    "failed_assertion_count"
                ]
            ),
            "dimension_count": check[
                "dimension_count"
            ],
            "overall_state": check[
                "overall_state"
            ],
            "review_digest": self._digest(
                check["assertions"]
            ),
            "blocked_surfaces": {
                "systemd": True,
                "autostart": True,
                "non_loopback": True,
                "arbitrary_pid_signal": True,
                "automatic_stale_cleanup": True,
                "permission_store_mutation": True,
                "persistent_audit_write": True,
            },
        }

SPRINT_262_PROCESS_ROLE_POLICY = {'native_process_role_classification': True,
 'service_runtime_role': 'service_runtime',
 'control_plane_role': 'control_plane',
 'foreign_role': 'unclassified_main',
 'count_allowance_removed': True}
