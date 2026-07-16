from __future__ import annotations

import ast
import hashlib
import os
import re
from pathlib import Path
from typing import Any


class RestartLogsFailureVisibilityPlanner:
    """Sprint 253 Phase B contract for restart, logs, and failures."""

    OWNER = "RestartLogsFailureVisibilityPlanner"
    VERSION = "1.1.3"
    ANCHOR_VERSION = "1.1.2"
    CURRENT_SPRINT = 253
    NEXT_SPRINT = 254
    NEXT_VERSION = "1.1.4"
    BOUNDARY = "restart_logs_failure_visibility"
    NEXT_BOUNDARY = "process_ownership_service_state_persistence"
    CONTRACT_MODE = "supervised_restart_and_bounded_log_visibility"
    DELIVERY_MODE = "phase_b_supervised_restart_and_bounded_log_tail"
    EXPECTED_ASSERTION_COUNT = 168
    ASSERTIONS_PER_DIMENSION = 12
    REVIEW_STATES = ("secure", "review", "warning", "unavailable")
    DIMENSION_ORDER = (
        "restart_request_contract",
        "canonical_process_ownership",
        "stop_verification_boundary",
        "fresh_start_verification_boundary",
        "health_verification_boundary",
        "rollback_and_safe_idle",
        "canonical_log_allowlist",
        "bounded_log_tail_visibility",
        "log_redaction_boundary",
        "failure_packet_schema",
        "failure_stage_taxonomy",
        "cli_execution_surface",
        "mutation_and_execution_boundary",
        "integration_anchor_stability",
    )
    FAILURE_STAGES = (
        "preflight",
        "ownership",
        "stop_request",
        "stop_verification",
        "restart_gap",
        "process_launch",
        "ownership_write",
        "health_verification",
        "rollback",
        "final_state",
    )
    FAILURE_PACKET_FIELDS = (
        "schema_version",
        "boundary",
        "operation",
        "stage",
        "reason_code",
        "message",
        "lifecycle_state",
        "ownership_state",
        "pid",
        "exit_code",
        "signal",
        "health_ok",
        "listener_count",
        "process_count",
        "rollback_attempted",
        "rollback_complete",
        "safe_idle",
        "log_excerpt",
        "log_excerpt_redacted",
        "recovery_suggestion",
    )
    RUNTIME_BOUNDARY = {
        "status_observation_enabled": True,
        "proc_metadata_read_enabled": True,
        "log_metadata_read_enabled": True,
        "bounded_log_content_read_enabled": True,
        "failure_visibility_enabled": True,
        "restart_preview_enabled": True,
        "service_restart_execution_enabled": True,
        "service_start_execution_enabled": True,
        "service_stop_execution_enabled": True,
        "process_creation_enabled": True,
        "process_signal_enabled": True,
        "socket_creation_enabled": False,
        "network_probe_enabled": True,
        "systemd_mutation_enabled": False,
        "autostart_mutation_enabled": False,
        "permission_mutation_enabled": False,
        "audit_write_enabled": False,
        "log_mutation_enabled": False,
        "recovery_execution_enabled": True,
        "external_command_execution_enabled": True,
        "child_loopback_listener_activation_enabled": True,
        "non_loopback_binding_enabled": False,
        "arbitrary_pid_signal_enabled": False,
        "arbitrary_log_path_enabled": False,
    }
    SOURCE_CONTRACT = {
        "planner_source_read_only": True,
        "planner_ast_inspection_only": True,
        "planner_runtime_execution": False,
        "planner_subprocess_used": False,
        "planner_network_access_used": False,
        "planner_socket_creation_used": False,
        "planner_systemd_access_used": False,
        "planner_file_mutation_used": False,
        "canonical_data_content_read": False,
        "canonical_log_content_read": False,
        "log_metadata_read": True,
        "bounded_log_read_on_explicit_request_only": True,
    }
    LOG_ALLOWLIST = (
        "logs/aura.log",
        "logs/<recognized-rotated-aura-log>",
        "/tmp/aura-manual-start-stop-status-<uid>.log",
    )
    MAX_METADATA_ENTRIES = 32
    MAX_TAIL_LINES = 200
    MAX_TAIL_BYTES = 65536
    ACTIVE_LOG_NAME = "aura.log"
    ROTATED_LOG_PATTERN = re.compile(
        r"^aura\.\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d{6}\.log"
        r"(?:\.(?:gz|zip))?$"
    )
    SOURCE_PATHS = {
        "executor": (
            "aura/restart_logs_failure_visibility/"
            "restart_logs_failure_visibility_executor.py"
        ),
        "manager": (
            "aura/restart_logs_failure_visibility/"
            "restart_logs_failure_visibility_alpha_manager.py"
        ),
        "cli": (
            "aura/restart_logs_failure_visibility/"
            "restart_logs_failure_visibility_cli.py"
        ),
        "manual_executor": (
            "aura/manual_start_stop_status_runtime/"
            "manual_start_stop_status_runtime_executor.py"
        ),
        "lifecycle_manager": (
            "aura/service_lifecycle_runtime/"
            "aura_service_lifecycle_runtime_manager.py"
        ),
        "log_planner": (
            "aura/log_rotation_storage_cleanup/"
            "aura_log_rotation_storage_cleanup_planner.py"
        ),
        "launcher_planner": (
            "aura/aura_launcher_service_controls/"
            "aura_launcher_service_controls_planner.py"
        ),
        "core_cli": "aura/core/cli.py",
    }
    ANCHOR_ASSERTIONS = {
        "manual_start_stop_status_runtime": 144,
        "aura_launcher_service_controls": 120,
        "service_lifecycle_determinism": 25,
        "log_rotation_storage_cleanup": 40,
        "backup_restore_rehearsal": 96,
        "configuration_integrity": 61,
        "active_permission_runtime": 3115,
        "genesis_final_release": 1258,
    }

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.project_root = Path(
            project_root if project_root is not None else Path.cwd()
        ).resolve()
        self.logs_path = self.project_root / "logs"
        self.runtime_log_path = Path(
            f"/tmp/aura-manual-start-stop-status-{os.getuid()}.log"
        )

    @staticmethod
    def _digest(path: Path) -> str | None:
        if not path.is_file():
            return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _listener_count(port: int = 8765) -> int:
        count = 0
        for path in (Path("/proc/net/tcp"), Path("/proc/net/tcp6")):
            if not path.is_file():
                continue
            for line in path.read_text(encoding="utf-8").splitlines()[1:]:
                fields = line.split()
                if len(fields) < 4:
                    continue
                try:
                    local_port = int(fields[1].rsplit(":", 1)[1], 16)
                except (ValueError, IndexError):
                    continue
                if local_port == port and fields[3] == "0A":
                    count += 1
        return count

    @staticmethod
    def _strict_main_processes() -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        current_pid = os.getpid()
        proc = Path("/proc")
        if not proc.is_dir():
            return records

        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            pid = int(entry.name)
            if pid == current_pid:
                continue
            try:
                raw = (entry / "cmdline").read_bytes()
            except (
                FileNotFoundError,
                PermissionError,
                ProcessLookupError,
                OSError,
            ):
                continue

            argv = [
                item.decode("utf-8", errors="replace")
                for item in raw.split(b"\0")
                if item
            ]
            if (
                argv
                and Path(argv[0]).name.lower().startswith("python")
                and any(Path(item).name == "main.py" for item in argv[1:])
            ):
                records.append({"pid": pid, "argv": argv})

        return records

    def _source_record(self, key: str) -> dict[str, Any]:
        relative = self.SOURCE_PATHS[key]
        path = self.project_root / relative
        record: dict[str, Any] = {
            "key": key,
            "path": relative,
            "exists": path.is_file(),
            "sha256": self._digest(path),
            "size_bytes": path.stat().st_size if path.is_file() else None,
            "ast_valid": False,
            "classes": [],
            "methods": [],
            "literals": [],
            "names": [],
        }
        if not path.is_file():
            return record

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            return record

        classes: set[str] = set()
        methods: set[str] = set()
        literals: set[str] = set()
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.add(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.add(node.name)
            elif (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and len(node.value) <= 180
            ):
                literals.add(node.value)
            elif isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.alias):
                names.add(node.name)
                if node.asname:
                    names.add(node.asname)

        record.update(
            {
                "ast_valid": True,
                "classes": sorted(classes),
                "methods": sorted(methods),
                "literals": sorted(literals),
                "names": sorted(names),
            }
        )
        return record

    def _source_records(self) -> dict[str, dict[str, Any]]:
        return {
            key: self._source_record(key)
            for key in sorted(self.SOURCE_PATHS)
        }

    @staticmethod
    def _metadata(path: Path, classification: str) -> dict[str, Any]:
        stat = path.stat()
        return {
            "path": path.as_posix(),
            "classification": classification,
            "exists": path.is_file(),
            "size_bytes": stat.st_size,
            "mode": oct(stat.st_mode & 0o777),
            "uid": stat.st_uid,
            "gid": stat.st_gid,
            "mtime_ns": stat.st_mtime_ns,
            "content_read": False,
        }

    def log_visibility(self) -> dict[str, Any]:
        entries: list[dict[str, Any]] = []
        if self.logs_path.is_dir() and not self.logs_path.is_symlink():
            active = self.logs_path / self.ACTIVE_LOG_NAME
            if active.is_file() and not active.is_symlink():
                entries.append(self._metadata(active, "active_canonical_log"))

            rotated = [
                path
                for path in sorted(self.logs_path.iterdir())
                if (
                    path.is_file()
                    and not path.is_symlink()
                    and self.ROTATED_LOG_PATTERN.fullmatch(path.name)
                )
            ]
            for path in rotated[: self.MAX_METADATA_ENTRIES - len(entries)]:
                entries.append(
                    self._metadata(path, "recognized_rotated_log")
                )

        if (
            len(entries) < self.MAX_METADATA_ENTRIES
            and self.runtime_log_path.is_file()
            and not self.runtime_log_path.is_symlink()
        ):
            entries.append(
                self._metadata(
                    self.runtime_log_path,
                    "temporary_owned_runtime_log",
                )
            )

        return {
            "schema_version": 1,
            "boundary": self.BOUNDARY,
            "mode": "metadata_plus_bounded_allowlisted_tail",
            "allowlist": list(self.LOG_ALLOWLIST),
            "allowed_sources": [
                "active",
                "latest-rotated",
                "runtime",
            ],
            "entry_count": len(entries),
            "entries": entries,
            "max_entries": self.MAX_METADATA_ENTRIES,
            "max_tail_lines": self.MAX_TAIL_LINES,
            "max_tail_bytes": self.MAX_TAIL_BYTES,
            "tail_available": True,
            "content_read": False,
            "content_read_on_request_only": True,
            "redaction_required": True,
            "arbitrary_path_allowed": False,
            "symlink_following_allowed": False,
            "mutation_allowed": False,
            "phase_b_activation_required": False,
        }

    def failure_visibility(self) -> dict[str, Any]:
        listener_count = self._listener_count()
        processes = self._strict_main_processes()
        safe_idle = listener_count == 0 and not processes

        return {
            "schema_version": 1,
            "boundary": self.BOUNDARY,
            "mode": "schema_and_live_summary",
            "failure_packet_fields": list(self.FAILURE_PACKET_FIELDS),
            "failure_stages": list(self.FAILURE_STAGES),
            "redaction_required": True,
            "max_log_excerpt_lines": 40,
            "max_log_excerpt_bytes": 16384,
            "raw_environment_allowed": False,
            "secrets_allowed": False,
            "arbitrary_file_excerpt_allowed": False,
            "live_summary": {
                "lifecycle_state": (
                    "stopped" if safe_idle else "runtime_evidence_visible"
                ),
                "listener_count": listener_count,
                "strict_main_process_count": len(processes),
                "safe_idle": safe_idle,
                "failure_record_available": False,
                "failure_log_content_read": False,
            },
            "example": {
                "schema_version": 1,
                "boundary": self.BOUNDARY,
                "operation": "restart",
                "stage": "health_verification",
                "reason_code": "health_contract_not_ready",
                "message": (
                    "Service did not satisfy the bounded health contract."
                ),
                "lifecycle_state": "failed",
                "ownership_state": "owned_or_cleared",
                "pid": None,
                "exit_code": None,
                "signal": None,
                "health_ok": False,
                "listener_count": 0,
                "process_count": 0,
                "rollback_attempted": True,
                "rollback_complete": True,
                "safe_idle": True,
                "log_excerpt": [],
                "log_excerpt_redacted": True,
                "recovery_suggestion": (
                    "Review bounded logs before another approved restart."
                ),
            },
        }

    def restart_preview(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "boundary": self.BOUNDARY,
            "operation": "restart",
            "available": True,
            "execution_enabled": True,
            "phase": self.DELIVERY_MODE,
            "approval_required": True,
            "required_flags": [
                "--approve-restart",
                "--confirm-localhost",
            ],
            "sequence": [
                "exclusive_control_lock",
                "read_canonical_status",
                "verify_owned_or_stopped",
                "stop_owned_process_when_running",
                "verify_listener_and_process_absent",
                "bounded_restart_gap",
                "fresh_process_start",
                "write_temporary_ownership_record",
                "verify_exact_process_identity",
                "verify_loopback_listener",
                "verify_health_contract",
                "return_running_or_safe_idle_failure",
            ],
            "idempotent_stopped_policy": "fresh_start_after_approval",
            "idempotent_running_policy": "owned_stop_then_fresh_start",
            "unowned_runtime_policy": "reject_without_signal",
            "rollback_policy": "bounded_owned_cleanup_to_safe_idle",
            "systemd_used": False,
            "autostart_used": False,
            "non_loopback_allowed": False,
            "arbitrary_pid_signal_allowed": False,
        }

    def _dimension_checks(
        self,
        sources: dict[str, dict[str, Any]],
        logs: dict[str, Any],
        failures: dict[str, Any],
        restart: dict[str, Any],
    ) -> dict[str, list[tuple[str, bool]]]:
        executor = sources["executor"]
        manager = sources["manager"]
        cli = sources["cli"]
        manual = sources["manual_executor"]
        lifecycle = sources["lifecycle_manager"]
        log_planner = sources["log_planner"]
        launcher = sources["launcher_planner"]
        core_cli = sources["core_cli"]

        executor_methods = set(executor["methods"])
        manual_methods = set(manual["methods"])
        lifecycle_literals = set(lifecycle["literals"])
        log_literals = set(log_planner["literals"])
        cli_literals = set(cli["literals"])
        core_names = set(core_cli["names"])
        launcher_literals = set(launcher["literals"])

        return {
            "restart_request_contract": [
                ("schema_v1", restart["schema_version"] == 1),
                ("boundary_exact", restart["boundary"] == self.BOUNDARY),
                ("operation_restart", restart["operation"] == "restart"),
                ("available_true", restart["available"] is True),
                (
                    "execution_enabled",
                    restart["execution_enabled"] is True,
                ),
                (
                    "approval_required",
                    restart["approval_required"] is True,
                ),
                (
                    "approve_flag",
                    "--approve-restart" in restart["required_flags"],
                ),
                (
                    "localhost_flag",
                    "--confirm-localhost" in restart["required_flags"],
                ),
                ("sequence_bounded", len(restart["sequence"]) == 12),
                (
                    "stopped_policy_defined",
                    bool(restart["idempotent_stopped_policy"]),
                ),
                (
                    "running_policy_defined",
                    bool(restart["idempotent_running_policy"]),
                ),
                (
                    "unowned_policy_rejects",
                    "reject" in restart["unowned_runtime_policy"],
                ),
            ],
            "canonical_process_ownership": [
                ("executor_exists", executor["exists"]),
                ("executor_ast_valid", executor["ast_valid"]),
                (
                    "executor_class_present",
                    "RestartLogsFailureVisibilityExecutor"
                    in executor["classes"],
                ),
                ("executor_restart_method", "restart" in executor_methods),
                ("executor_tail_method", "tail" in executor_methods),
                ("executor_status_method", "status" in executor_methods),
                ("executor_lock_method", "_lock" in executor_methods),
                ("manual_exists", manual["exists"]),
                ("manual_ast_valid", manual["ast_valid"]),
                (
                    "manual_class_present",
                    "ManualStartStopStatusRuntimeExecutor"
                    in manual["classes"],
                ),
                ("manual_start_method", "start" in manual_methods),
                ("manual_stop_method", "stop" in manual_methods),
            ],
            "stop_verification_boundary": [
                ("manual_stop", "stop" in manual_methods),
                (
                    "manual_terminate_owned",
                    "_terminate_owned" in manual_methods,
                ),
                ("manual_status", "status" in manual_methods),
                (
                    "sequence_stop_owned",
                    "stop_owned_process_when_running"
                    in restart["sequence"],
                ),
                (
                    "sequence_verify_absent",
                    "verify_listener_and_process_absent"
                    in restart["sequence"],
                ),
                (
                    "sequence_verify_owned",
                    "verify_owned_or_stopped" in restart["sequence"],
                ),
                (
                    "stop_execution_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_stop_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "process_signal_enabled",
                    self.RUNTIME_BOUNDARY["process_signal_enabled"] is True,
                ),
                (
                    "external_execution_enabled",
                    self.RUNTIME_BOUNDARY[
                        "external_command_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "arbitrary_pid_disabled",
                    self.RUNTIME_BOUNDARY[
                        "arbitrary_pid_signal_enabled"
                    ]
                    is False,
                ),
                ("systemd_disabled", restart["systemd_used"] is False),
                ("autostart_disabled", restart["autostart_used"] is False),
            ],
            "fresh_start_verification_boundary": [
                ("manual_start", "start" in manual_methods),
                (
                    "manual_preflight",
                    "_ensure_stopped_preflight" in manual_methods,
                ),
                (
                    "manual_health_probe",
                    "_health_probe" in manual_methods,
                ),
                (
                    "sequence_fresh_start",
                    "fresh_process_start" in restart["sequence"],
                ),
                (
                    "sequence_ownership_write",
                    "write_temporary_ownership_record"
                    in restart["sequence"],
                ),
                (
                    "sequence_identity_verify",
                    "verify_exact_process_identity" in restart["sequence"],
                ),
                (
                    "sequence_loopback_verify",
                    "verify_loopback_listener" in restart["sequence"],
                ),
                (
                    "process_creation_enabled",
                    self.RUNTIME_BOUNDARY["process_creation_enabled"] is True,
                ),
                (
                    "start_execution_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_start_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "child_listener_enabled",
                    self.RUNTIME_BOUNDARY[
                        "child_loopback_listener_activation_enabled"
                    ]
                    is True,
                ),
                (
                    "non_loopback_disabled",
                    self.RUNTIME_BOUNDARY[
                        "non_loopback_binding_enabled"
                    ]
                    is False,
                ),
                (
                    "fresh_start_after_approval",
                    restart["idempotent_stopped_policy"]
                    == "fresh_start_after_approval",
                ),
            ],
            "health_verification_boundary": [
                ("lifecycle_exists", lifecycle["exists"]),
                ("lifecycle_ast_valid", lifecycle["ast_valid"]),
                (
                    "lifecycle_class_present",
                    "AuraServiceLifecycleRuntimeManager"
                    in lifecycle["classes"],
                ),
                ("health_endpoint_literal", "/health" in lifecycle_literals),
                ("running_literal", "running" in lifecycle_literals),
                ("failed_literal", "failed" in lifecycle_literals),
                (
                    "sequence_health_verify",
                    "verify_health_contract" in restart["sequence"],
                ),
                (
                    "network_probe_enabled",
                    self.RUNTIME_BOUNDARY["network_probe_enabled"] is True,
                ),
                (
                    "socket_creation_disabled",
                    self.RUNTIME_BOUNDARY["socket_creation_enabled"] is False,
                ),
                (
                    "status_observation_enabled",
                    self.RUNTIME_BOUNDARY[
                        "status_observation_enabled"
                    ]
                    is True,
                ),
                (
                    "proc_metadata_enabled",
                    self.RUNTIME_BOUNDARY["proc_metadata_read_enabled"]
                    is True,
                ),
                (
                    "loopback_only",
                    restart["non_loopback_allowed"] is False,
                ),
            ],
            "rollback_and_safe_idle": [
                (
                    "rollback_policy_defined",
                    bool(restart["rollback_policy"]),
                ),
                (
                    "rollback_mentions_safe_idle",
                    "safe_idle" in restart["rollback_policy"],
                ),
                (
                    "rollback_attempted_field",
                    "rollback_attempted"
                    in failures["failure_packet_fields"],
                ),
                (
                    "rollback_complete_field",
                    "rollback_complete"
                    in failures["failure_packet_fields"],
                ),
                (
                    "safe_idle_field",
                    "safe_idle" in failures["failure_packet_fields"],
                ),
                (
                    "rollback_stage",
                    "rollback" in failures["failure_stages"],
                ),
                (
                    "final_state_stage",
                    "final_state" in failures["failure_stages"],
                ),
                (
                    "safe_idle_live",
                    failures["live_summary"]["safe_idle"] is True,
                ),
                (
                    "listener_zero",
                    failures["live_summary"]["listener_count"] == 0,
                ),
                (
                    "process_zero",
                    failures["live_summary"][
                        "strict_main_process_count"
                    ]
                    == 0,
                ),
                (
                    "recovery_enabled",
                    self.RUNTIME_BOUNDARY["recovery_execution_enabled"]
                    is True,
                ),
                (
                    "restart_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_restart_execution_enabled"
                    ]
                    is True,
                ),
            ],
            "canonical_log_allowlist": [
                ("log_planner_exists", log_planner["exists"]),
                ("log_planner_ast_valid", log_planner["ast_valid"]),
                (
                    "active_log_literal",
                    self.ACTIVE_LOG_NAME in log_literals,
                ),
                ("logs_literal", "logs" in log_literals),
                (
                    "canonical_log_literal",
                    "canonical_log" in log_literals,
                ),
                ("allowlist_three", len(logs["allowlist"]) == 3),
                (
                    "active_allowlisted",
                    "logs/aura.log" in logs["allowlist"],
                ),
                (
                    "rotated_allowlisted",
                    any("rotated" in item for item in logs["allowlist"]),
                ),
                (
                    "runtime_allowlisted",
                    any("/tmp/" in item for item in logs["allowlist"]),
                ),
                (
                    "arbitrary_path_disabled",
                    logs["arbitrary_path_allowed"] is False,
                ),
                (
                    "symlink_following_disabled",
                    logs["symlink_following_allowed"] is False,
                ),
                (
                    "mutation_disabled",
                    logs["mutation_allowed"] is False,
                ),
            ],
            "bounded_log_tail_visibility": [
                (
                    "mode_bounded",
                    logs["mode"]
                    == "metadata_plus_bounded_allowlisted_tail",
                ),
                ("tail_available", logs["tail_available"] is True),
                (
                    "content_read_default_false",
                    logs["content_read"] is False,
                ),
                (
                    "content_on_request_only",
                    logs["content_read_on_request_only"] is True,
                ),
                (
                    "redaction_required",
                    logs["redaction_required"] is True,
                ),
                (
                    "max_entries_bounded",
                    1 <= logs["max_entries"] <= 64,
                ),
                (
                    "max_lines_bounded",
                    1 <= logs["max_tail_lines"] <= 500,
                ),
                (
                    "max_bytes_bounded",
                    1024 <= logs["max_tail_bytes"] <= 131072,
                ),
                (
                    "entry_count_bounded",
                    logs["entry_count"] <= logs["max_entries"],
                ),
                (
                    "allowed_sources_exact",
                    logs["allowed_sources"]
                    == ["active", "latest-rotated", "runtime"],
                ),
                (
                    "bounded_content_enabled",
                    self.RUNTIME_BOUNDARY[
                        "bounded_log_content_read_enabled"
                    ]
                    is True,
                ),
                (
                    "arbitrary_log_disabled",
                    self.RUNTIME_BOUNDARY[
                        "arbitrary_log_path_enabled"
                    ]
                    is False,
                ),
            ],
            "log_redaction_boundary": [
                (
                    "failure_redaction_required",
                    failures["redaction_required"] is True,
                ),
                (
                    "excerpt_lines_bounded",
                    failures["max_log_excerpt_lines"] <= 100,
                ),
                (
                    "excerpt_bytes_bounded",
                    failures["max_log_excerpt_bytes"] <= 32768,
                ),
                (
                    "raw_environment_disabled",
                    failures["raw_environment_allowed"] is False,
                ),
                (
                    "secrets_disabled",
                    failures["secrets_allowed"] is False,
                ),
                (
                    "arbitrary_excerpt_disabled",
                    failures["arbitrary_file_excerpt_allowed"] is False,
                ),
                (
                    "excerpt_field_present",
                    "log_excerpt" in failures["failure_packet_fields"],
                ),
                (
                    "redacted_field_present",
                    "log_excerpt_redacted"
                    in failures["failure_packet_fields"],
                ),
                (
                    "example_excerpt_list",
                    isinstance(failures["example"]["log_excerpt"], list),
                ),
                (
                    "example_redacted_true",
                    failures["example"]["log_excerpt_redacted"] is True,
                ),
                ("executor_redact_method", "_redact" in executor_methods),
                (
                    "log_mutation_disabled",
                    self.RUNTIME_BOUNDARY["log_mutation_enabled"] is False,
                ),
            ],
            "failure_packet_schema": [
                ("schema_v1", failures["schema_version"] == 1),
                ("boundary_exact", failures["boundary"] == self.BOUNDARY),
                (
                    "field_count_exact",
                    len(failures["failure_packet_fields"]) == 20,
                ),
                (
                    "stage_field",
                    "stage" in failures["failure_packet_fields"],
                ),
                (
                    "reason_field",
                    "reason_code" in failures["failure_packet_fields"],
                ),
                (
                    "ownership_field",
                    "ownership_state"
                    in failures["failure_packet_fields"],
                ),
                (
                    "health_field",
                    "health_ok" in failures["failure_packet_fields"],
                ),
                (
                    "listener_field",
                    "listener_count" in failures["failure_packet_fields"],
                ),
                (
                    "process_field",
                    "process_count" in failures["failure_packet_fields"],
                ),
                (
                    "recovery_field",
                    "recovery_suggestion"
                    in failures["failure_packet_fields"],
                ),
                (
                    "example_complete",
                    set(failures["failure_packet_fields"])
                    == set(failures["example"]),
                ),
                (
                    "visibility_enabled",
                    self.RUNTIME_BOUNDARY["failure_visibility_enabled"]
                    is True,
                ),
            ],
            "failure_stage_taxonomy": [
                (
                    "ten_stages",
                    len(failures["failure_stages"]) == 10,
                ),
                (
                    "preflight_stage",
                    "preflight" in failures["failure_stages"],
                ),
                (
                    "ownership_stage",
                    "ownership" in failures["failure_stages"],
                ),
                (
                    "stop_request_stage",
                    "stop_request" in failures["failure_stages"],
                ),
                (
                    "stop_verify_stage",
                    "stop_verification" in failures["failure_stages"],
                ),
                (
                    "restart_gap_stage",
                    "restart_gap" in failures["failure_stages"],
                ),
                (
                    "launch_stage",
                    "process_launch" in failures["failure_stages"],
                ),
                (
                    "ownership_write_stage",
                    "ownership_write" in failures["failure_stages"],
                ),
                (
                    "health_stage",
                    "health_verification" in failures["failure_stages"],
                ),
                (
                    "rollback_stage",
                    "rollback" in failures["failure_stages"],
                ),
                (
                    "final_state_stage",
                    "final_state" in failures["failure_stages"],
                ),
                (
                    "example_stage_valid",
                    failures["example"]["stage"]
                    in failures["failure_stages"],
                ),
            ],
            "cli_execution_surface": [
                ("cli_exists", cli["exists"]),
                ("cli_ast_valid", cli["ast_valid"]),
                (
                    "cli_handler_present",
                    "handle_restart_logs_failure_visibility_command"
                    in cli["methods"],
                ),
                (
                    "restart_command_literal",
                    "restart-logs-failure-visibility-restart"
                    in cli_literals,
                ),
                (
                    "tail_command_literal",
                    "restart-logs-failure-visibility-tail"
                    in cli_literals,
                ),
                ("manager_exists", manager["exists"]),
                ("manager_ast_valid", manager["ast_valid"]),
                (
                    "manager_restart_method",
                    "restart" in manager["methods"],
                ),
                (
                    "manager_tail_method",
                    "tail" in manager["methods"],
                ),
                ("core_cli_exists", core_cli["exists"]),
                ("core_cli_ast_valid", core_cli["ast_valid"]),
                (
                    "core_handler_name",
                    "handle_restart_logs_failure_visibility_command"
                    in core_names,
                ),
            ],
            "mutation_and_execution_boundary": [
                (
                    "restart_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_restart_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "start_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_start_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "stop_enabled",
                    self.RUNTIME_BOUNDARY[
                        "service_stop_execution_enabled"
                    ]
                    is True,
                ),
                (
                    "process_creation_enabled",
                    self.RUNTIME_BOUNDARY["process_creation_enabled"] is True,
                ),
                (
                    "process_signal_enabled",
                    self.RUNTIME_BOUNDARY["process_signal_enabled"] is True,
                ),
                (
                    "network_probe_enabled",
                    self.RUNTIME_BOUNDARY["network_probe_enabled"] is True,
                ),
                (
                    "socket_creation_disabled",
                    self.RUNTIME_BOUNDARY["socket_creation_enabled"] is False,
                ),
                (
                    "systemd_disabled",
                    self.RUNTIME_BOUNDARY["systemd_mutation_enabled"] is False,
                ),
                (
                    "autostart_disabled",
                    self.RUNTIME_BOUNDARY[
                        "autostart_mutation_enabled"
                    ]
                    is False,
                ),
                (
                    "permission_mutation_disabled",
                    self.RUNTIME_BOUNDARY[
                        "permission_mutation_enabled"
                    ]
                    is False,
                ),
                (
                    "audit_write_disabled",
                    self.RUNTIME_BOUNDARY["audit_write_enabled"] is False,
                ),
                (
                    "log_mutation_disabled",
                    self.RUNTIME_BOUNDARY["log_mutation_enabled"] is False,
                ),
            ],
            "integration_anchor_stability": [
                ("version_exact", self.VERSION == "1.1.3"),
                ("anchor_version_exact", self.ANCHOR_VERSION == "1.1.2"),
                ("sprint_exact", self.CURRENT_SPRINT == 253),
                ("next_sprint_exact", self.NEXT_SPRINT == 254),
                (
                    "boundary_exact",
                    self.BOUNDARY == "restart_logs_failure_visibility",
                ),
                (
                    "next_boundary_exact",
                    self.NEXT_BOUNDARY
                    == "process_ownership_service_state_persistence",
                ),
                ("launcher_exists", launcher["exists"]),
                ("launcher_ast_valid", launcher["ast_valid"]),
                (
                    "launcher_restart_literal",
                    any("restart" in item for item in launcher_literals),
                ),
                (
                    "manual_anchor_144",
                    self.ANCHOR_ASSERTIONS[
                        "manual_start_stop_status_runtime"
                    ]
                    == 144,
                ),
                (
                    "lifecycle_anchor_25",
                    self.ANCHOR_ASSERTIONS[
                        "service_lifecycle_determinism"
                    ]
                    == 25,
                ),
                (
                    "log_anchor_40",
                    self.ANCHOR_ASSERTIONS[
                        "log_rotation_storage_cleanup"
                    ]
                    == 40,
                ),
            ],
        }

    def _build_packet(self) -> dict[str, Any]:
        sources = self._source_records()
        logs = self.log_visibility()
        failures = self.failure_visibility()
        restart = self.restart_preview()
        dimensions = self._dimension_checks(
            sources,
            logs,
            failures,
            restart,
        )

        dimension_packets: list[dict[str, Any]] = []
        assertion_packets: list[dict[str, Any]] = []
        findings: list[dict[str, Any]] = []

        for dimension_id in self.DIMENSION_ORDER:
            checks = dimensions[dimension_id]
            if len(checks) != self.ASSERTIONS_PER_DIMENSION:
                raise RuntimeError(
                    f"{dimension_id} has {len(checks)} assertions; "
                    f"expected {self.ASSERTIONS_PER_DIMENSION}"
                )

            failed = [name for name, passed in checks if not passed]
            state = "secure" if not failed else "warning"
            dimension_packets.append(
                {
                    "dimension_id": dimension_id,
                    "state": state,
                    "assertion_count": len(checks),
                    "failed_assertion_count": len(failed),
                    "failed_assertions": failed,
                }
            )
            for name, passed in checks:
                assertion_packets.append(
                    {
                        "assertion_id": f"{dimension_id}.{name}",
                        "dimension_id": dimension_id,
                        "passed": bool(passed),
                    }
                )
                if not passed:
                    findings.append(
                        {
                            "dimension_id": dimension_id,
                            "assertion_id": name,
                            "state": "warning",
                            "message": (
                                "Phase B evidence did not satisfy "
                                "the contract assertion."
                            ),
                        }
                    )

        failed_count = sum(
            not assertion["passed"] for assertion in assertion_packets
        )
        state_counts = {
            state: sum(
                dimension["state"] == state
                for dimension in dimension_packets
            )
            for state in self.REVIEW_STATES
        }

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "delivery_mode": self.DELIVERY_MODE,
            "deterministic": True,
            "assertion_count": len(assertion_packets),
            "failed_assertion_count": failed_count,
            "expected_assertion_count": self.EXPECTED_ASSERTION_COUNT,
            "alpha_ready": failed_count == 0,
            "overall_state": (
                "secure" if failed_count == 0 else "warning"
            ),
            "dimension_count": len(dimension_packets),
            "state_counts": state_counts,
            "finding_count": len(findings),
            "findings": findings,
            "dimensions": dimension_packets,
            "assertions": assertion_packets,
            "runtime_boundary": dict(self.RUNTIME_BOUNDARY),
            "source_contract": dict(self.SOURCE_CONTRACT),
            "restart_executor_available": (
                sources["executor"]["exists"]
                and sources["executor"]["ast_valid"]
            ),
            "bounded_log_tail_available": True,
            "restart_preview": restart,
            "log_visibility": logs,
            "failure_visibility": failures,
            "source_records": sources,
            "anchor_assertions": dict(self.ANCHOR_ASSERTIONS),
        }

    def status(self) -> dict[str, Any]:
        packet = self._build_packet()
        return {
            key: packet[key]
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
                "delivery_mode",
                "alpha_ready",
                "overall_state",
                "dimension_count",
                "state_counts",
                "finding_count",
                "runtime_boundary",
                "restart_executor_available",
                "bounded_log_tail_available",
                "restart_preview",
                "log_visibility",
                "failure_visibility",
                "anchor_assertions",
            )
        }

    def context(self) -> dict[str, Any]:
        packet = self._build_packet()
        return {
            "owner": packet["owner"],
            "version": packet["version"],
            "boundary": packet["boundary"],
            "phase": packet["delivery_mode"],
            "purpose": (
                "Provide explicitly approved supervised restart, "
                "bounded allowlisted log tail with redaction, and "
                "normalized failure visibility."
            ),
            "canonical_process_owner": (
                "ManualStartStopStatusRuntimeExecutor with lifecycle "
                "semantics owned by AuraServiceLifecycleRuntimeManager"
            ),
            "restart_policy": packet["restart_preview"],
            "log_policy": packet["log_visibility"],
            "failure_policy": packet["failure_visibility"],
            "runtime_boundary": packet["runtime_boundary"],
            "source_contract": packet["source_contract"],
            "next_boundary_state": "provisional_not_yet_canonical",
        }

    def review(self) -> dict[str, Any]:
        packet = self._build_packet()
        return {
            "owner": packet["owner"],
            "version": packet["version"],
            "boundary": packet["boundary"],
            "overall_state": packet["overall_state"],
            "dimension_count": packet["dimension_count"],
            "state_counts": packet["state_counts"],
            "finding_count": packet["finding_count"],
            "findings": packet["findings"],
            "dimensions": packet["dimensions"],
        }

    def check(self) -> dict[str, Any]:
        return self._build_packet()
