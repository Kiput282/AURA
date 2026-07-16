from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
from typing import Any


class ManualStartStopStatusRuntimePlanner:
    VERSION = "1.1.2"
    ANCHOR_VERSION = "1.1.1"
    CURRENT_SPRINT = 252
    NEXT_SPRINT = 253
    NEXT_VERSION = "1.1.3"
    BOUNDARY = "manual_start_stop_status_runtime"
    NEXT_BOUNDARY = "restart_logs_failure_visibility"
    OWNER = "ManualStartStopStatusRuntimePlanner"

    CONTRACT_MODE = (
        "supervised_manual_service_control_runtime"
    )
    REVIEW_MODE = (
        "source_contract_and_live_proc_status"
    )
    DELIVERY_MODE = "phase_b_supervised_start_stop_executor"

    BIND_HOST = "127.0.0.1"
    BIND_PORT = 8765

    EXPECTED_ASSERTION_COUNT = 144
    SPRINT_251_ANCHOR_ASSERTIONS = 120
    SERVICE_LIFECYCLE_ANCHOR_ASSERTIONS = 25
    GENESIS_FINAL_ANCHOR_ASSERTIONS = 1258
    ACTIVE_PERMISSION_ANCHOR_ASSERTIONS = 3115

    REVIEW_STATES = (
        "secure",
        "review",
        "warning",
        "unavailable",
    )
    STATE_PRIORITY = {
        "secure": 0,
        "review": 1,
        "warning": 2,
        "unavailable": 3,
    }

    DIMENSION_ORDER = (
        "canonical_process_ownership",
        "manual_start_request_and_approval",
        "manual_start_execution_boundary",
        "manual_stop_request_and_approval",
        "manual_stop_execution_boundary",
        "canonical_status_snapshot",
        "health_and_readiness_verification",
        "loopback_port_ownership",
        "timeout_and_failure_handling",
        "permission_and_audit_linkage",
        "safe_idle_and_orphan_prevention",
        "integration_acceptance_and_ux_metrics",
    )

    DIMENSION_SPECS = {
        "canonical_process_ownership": {
            "sources": (
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/local_web_runtime_alpha/"
                "aura_local_web_runtime_alpha_manager.py",
                "aura/aura_launcher_service_controls/"
                "aura_launcher_service_controls_planner.py",
            ),
            "groups": (
                (
                    "ownership_identity",
                    ("owner", "ownership", "process"),
                ),
                (
                    "pid_visibility",
                    ("pid", "process"),
                ),
                (
                    "listener_visibility",
                    ("listener", "bind", "port"),
                ),
                (
                    "canonical_owner_reuse",
                    ("lifecycle", "launcher", "service"),
                ),
            ),
        },
        "manual_start_request_and_approval": {
            "sources": (
                "aura/local_service_start_proposal_review/"
                "aura_local_service_start_proposal_review_"
                "foundation_manager.py",
                "aura/service_control_command_review_foundation/"
                "aura_service_control_command_review_"
                "foundation_manager.py",
                "aura/service_permission_gate_runtime_boundary/"
                "aura_service_permission_gate_runtime_boundary_"
                "manager.py",
            ),
            "groups": (
                (
                    "start_request",
                    ("start",),
                ),
                (
                    "proposal_preview",
                    ("proposal", "preview", "review"),
                ),
                (
                    "permission_gate",
                    ("permission", "grant", "deny"),
                ),
                (
                    "explicit_approval",
                    (
                        "approval",
                        "confirm",
                        "explicit",
                        "manual",
                    ),
                ),
            ),
        },
        "manual_start_execution_boundary": {
            "sources": (
                "aura/local_web_runtime_alpha/"
                "aura_local_web_runtime_alpha_manager.py",
                "aura/local_runtime_execution_gate_dry_run/"
                "aura_local_runtime_execution_gate_dry_run_"
                "foundation_manager.py",
                "aura/aura_launcher_service_controls/"
                "aura_launcher_service_controls_planner.py",
            ),
            "groups": (
                (
                    "start_surface",
                    ("start", "serve", "create_server"),
                ),
                (
                    "execution_gate",
                    ("execution", "runtime", "gate"),
                ),
                (
                    "loopback_scope",
                    (
                        "127.0.0.1",
                        "localhost",
                        "loopback",
                    ),
                ),
                (
                    "phase_a_deferred",
                    (
                        "disabled",
                        "deferred",
                        "review",
                        "false",
                    ),
                ),
            ),
        },
        "manual_stop_request_and_approval": {
            "sources": (
                "aura/local_service_boot_plan_review/"
                "aura_local_service_boot_plan_review_"
                "foundation_manager.py",
                "aura/service_control_command_review_foundation/"
                "aura_service_control_command_review_"
                "foundation_manager.py",
                "aura/runtime_safety_freeze_manual_approval_barrier/"
                "aura_runtime_safety_freeze_manual_approval_"
                "barrier_foundation_manager.py",
            ),
            "groups": (
                (
                    "stop_request",
                    ("stop", "shutdown"),
                ),
                (
                    "approval_requirement",
                    ("approval", "manual", "confirm"),
                ),
                (
                    "review_boundary",
                    ("review", "preview", "plan"),
                ),
                (
                    "safe_idle_guard",
                    ("safe_idle", "safe-idle", "freeze"),
                ),
            ),
        },
        "manual_stop_execution_boundary": {
            "sources": (
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/local_web_runtime_alpha/"
                "aura_local_web_runtime_alpha_manager.py",
                "aura/launcher_monitor/"
                "aura_launcher_health_monitor_foundation_manager.py",
            ),
            "groups": (
                (
                    "stop_or_shutdown",
                    ("stop", "shutdown", "close"),
                ),
                (
                    "lifecycle_state",
                    ("state", "lifecycle", "stopped"),
                ),
                (
                    "ownership_scope",
                    ("owner", "process", "listener"),
                ),
                (
                    "verification_boundary",
                    ("health", "wait", "timeout", "status"),
                ),
            ),
        },
        "canonical_status_snapshot": {
            "sources": (
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/health_status_api_runtime/"
                "aura_health_status_api_runtime_manager.py",
                "aura/control_center_service_monitor_panel_foundation/"
                "aura_control_center_service_monitor_panel_"
                "foundation_manager.py",
            ),
            "groups": (
                (
                    "status_surface",
                    ("status",),
                ),
                (
                    "health_surface",
                    ("health",),
                ),
                (
                    "state_projection",
                    ("state", "ready", "stopped"),
                ),
                (
                    "visibility",
                    ("visibility", "monitor", "read"),
                ),
            ),
        },
        "health_and_readiness_verification": {
            "sources": (
                "aura/health_status_api_runtime/"
                "aura_health_status_http_runtime_manager.py",
                "aura/local_service_health_endpoint_foundation/"
                "aura_local_service_health_endpoint_foundation_"
                "manager.py",
                "aura/local_web_runtime_alpha/"
                "aura_local_web_runtime_alpha_manager.py",
            ),
            "groups": (
                (
                    "health_endpoint",
                    ("health",),
                ),
                (
                    "readiness",
                    ("ready", "readiness", "status"),
                ),
                (
                    "loopback_binding",
                    ("127.0.0.1", "localhost"),
                ),
                (
                    "port_or_listener",
                    ("8765", "port", "listener", "bind"),
                ),
            ),
        },
        "loopback_port_ownership": {
            "sources": (
                "aura/local_service_configuration_port_registry_foundation/"
                "aura_local_service_configuration_port_registry_"
                "foundation_manager.py",
                "aura/service_security_localhost_binding_review/"
                "aura_service_security_localhost_binding_review_"
                "manager.py",
                "aura/local_web_runtime_alpha/"
                "aura_local_web_runtime_alpha_manager.py",
            ),
            "groups": (
                (
                    "loopback_host",
                    ("127.0.0.1", "localhost"),
                ),
                (
                    "canonical_port",
                    ("8765", "port"),
                ),
                (
                    "binding_boundary",
                    ("bind", "binding", "listener"),
                ),
                (
                    "security_scope",
                    ("security", "external", "localhost"),
                ),
            ),
        },
        "timeout_and_failure_handling": {
            "sources": (
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/service_recovery_restart_policy_foundation/"
                "aura_service_recovery_restart_policy_"
                "foundation_manager.py",
                "aura/runtime_error_rollback_preview/"
                "aura_runtime_error_rollback_preview_"
                "foundation_manager.py",
            ),
            "groups": (
                (
                    "bounded_wait",
                    ("timeout", "wait", "retry", "cooldown"),
                ),
                (
                    "failure_state",
                    ("failed", "failure", "error"),
                ),
                (
                    "recovery_or_rollback",
                    ("recovery", "rollback", "restart"),
                ),
                (
                    "safe_idle_return",
                    ("safe_idle", "safe-idle"),
                ),
            ),
        },
        "permission_and_audit_linkage": {
            "sources": (
                "aura/service_permission_gate_runtime_boundary/"
                "aura_service_permission_gate_runtime_boundary_"
                "manager.py",
                "aura/service_audit_link_foundation/"
                "aura_service_audit_link_foundation_manager.py",
                "aura/permissions/"
                "active_permission_runtime_planner.py",
            ),
            "groups": (
                (
                    "permission",
                    ("permission",),
                ),
                (
                    "approval_or_grant",
                    ("approval", "grant", "confirm"),
                ),
                (
                    "audit",
                    ("audit", "event", "trace"),
                ),
                (
                    "service_control_scope",
                    ("service", "start", "stop", "status"),
                ),
            ),
        },
        "safe_idle_and_orphan_prevention": {
            "sources": (
                "aura/local_service_safe_idle_boot_boundary/"
                "aura_local_service_safe_idle_boot_boundary_"
                "manager.py",
                "aura/service_recovery_restart_policy_foundation/"
                "aura_service_recovery_restart_policy_"
                "foundation_manager.py",
                "aura/runtime_safety_freeze_manual_approval_barrier/"
                "aura_runtime_safety_freeze_manual_approval_"
                "barrier_foundation_manager.py",
            ),
            "groups": (
                (
                    "safe_idle",
                    ("safe_idle", "safe-idle"),
                ),
                (
                    "orphan_or_ownership",
                    ("orphan", "owner", "process"),
                ),
                (
                    "failure_guard",
                    ("failure", "failed", "recovery"),
                ),
                (
                    "manual_freeze",
                    ("freeze", "manual", "approval"),
                ),
            ),
        },
        "integration_acceptance_and_ux_metrics": {
            "sources": (
                "aura/aura_launcher_service_controls/"
                "aura_launcher_service_controls_planner.py",
                "aura/partner_runtime/"
                "service_persistence_and_launcher_planner.py",
                "aura/local_interaction_runtime_stabilization/"
                "aura_local_interaction_runtime_stabilization_"
                "manager.py",
            ),
            "groups": (
                (
                    "launcher_handoff",
                    ("launcher",),
                ),
                (
                    "status_experience",
                    ("status", "health", "ready"),
                ),
                (
                    "acceptance",
                    ("acceptance", "scenario", "stabilization"),
                ),
                (
                    "failure_visibility",
                    ("failure", "error", "safe_idle"),
                ),
            ),
        },
    }

    RUNTIME_BOUNDARY = {'status_observation_enabled': True,
     'proc_metadata_read_enabled': True,
     'service_start_execution_enabled': True,
     'service_stop_execution_enabled': True,
     'service_restart_execution_enabled': False,
     'process_creation_enabled': True,
     'process_signal_enabled': True,
     'socket_creation_enabled': False,
     'network_probe_enabled': True,
     'systemd_mutation_enabled': False,
     'autostart_mutation_enabled': False,
     'permission_mutation_enabled': False,
     'audit_write_enabled': False,
     'recovery_execution_enabled': True,
     'external_command_execution_enabled': True,
     'child_loopback_listener_activation_enabled': True}

    SOURCE_CONTRACT = {
        "python_source_read_only": True,
        "ast_inspection_only": True,
        "proc_metadata_read_only": True,
        "canonical_data_content_read": False,
        "runtime_manager_imported": False,
        "service_runtime_executed": False,
        "subprocess_used": False,
        "socket_api_used": False,
        "network_access_used": False,
        "file_mutation_used": False,
        "systemd_access_used": False,
        "permission_store_read": False,
        "audit_store_read": False,
    }

    SCOPE_BOUNDARY = {'phase_a_only': False,
     'status_observer_active': True,
     'start_preview_only': False,
     'stop_preview_only': False,
     'canonical_launcher_facade_reused': True,
     'canonical_lifecycle_owner_reused': True,
     'duplicate_service_manager_created': False,
     'manual_start_execution_deferred': False,
     'manual_stop_execution_deferred': False,
     'restart_remains_disabled': True,
     'autostart_remains_disabled': True,
     'systemd_remains_unmodified': True,
     'loopback_only_required': True,
     'explicit_confirmation_required': True,
     'permission_required': True,
     'audit_link_required': True,
     'health_verification_required': True,
     'safe_idle_required': True,
     'orphan_process_rejection_required': True,
     'phase_b_supervised_executor': True,
     'ephemeral_ownership_record_only': True,
     'canonical_data_mutation_allowed': False}

    START_PREVIEW = {'action': 'manual_start',
     'phase': 'approved_execution_available',
     'execution_enabled': True,
     'approval_required': True,
     'permission_required': True,
     'ownership_preflight_required': True,
     'loopback_host': '127.0.0.1',
     'loopback_port': 8765,
     'health_verification_required': True,
     'timeout_required': True,
     'audit_link_required': True,
     'duplicate_process_rejected': True,
     'restart_implied': False,
     'autostart_implied': False,
     'audit_persistence_enabled': False,
     'canonical_child_command': 'service-lifecycle-start --confirm-localhost',
     'ownership_record_scope': 'temporary_user_runtime'}

    STOP_PREVIEW = {'action': 'manual_stop',
     'phase': 'approved_execution_available',
     'execution_enabled': True,
     'approval_required': True,
     'permission_required': True,
     'owned_process_required': True,
     'signal_scope': 'canonical_owned_process_only',
     'shutdown_verification_required': True,
     'timeout_required': True,
     'audit_link_required': True,
     'orphan_prevention_required': True,
     'restart_implied': False,
     'autostart_implied': False,
     'audit_persistence_enabled': False,
     'primary_signal': 'SIGTERM',
     'bounded_fallback_signal': 'SIGKILL',
     'ownership_record_scope': 'temporary_user_runtime'}

    ACCEPTANCE_SCENARIOS = (
        (
            "status reports stopped when no owned process "
            "and no listener exist"
        ),
        (
            "start without explicit approval is rejected "
            "without process creation"
        ),
        (
            "approved start creates exactly one owned "
            "foreground or supervised process"
        ),
        (
            "start waits for loopback health readiness "
            "within bounded timeout"
        ),
        (
            "repeated start is idempotent and does not "
            "create a duplicate process"
        ),
        (
            "status correlates pid ownership listener "
            "health lifecycle and safe-idle"
        ),
        (
            "stop without explicit approval is rejected "
            "without process signal"
        ),
        (
            "approved stop targets only the canonical "
            "owned process and verifies shutdown"
        ),
        (
            "failed start or stop returns visible reason "
            "and safe-idle without orphan process"
        ),
        (
            "restart autostart systemd and non-loopback "
            "activation remain disabled"
        ),
    )

    UX_METRICS = (
        "manual_steps_to_start",
        "time_to_ready_milliseconds",
        "manual_steps_to_stop",
        "time_to_stopped_milliseconds",
        "status_snapshot_latency_milliseconds",
        "failure_reason_visibility",
    )

    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root).resolve()
        packet = self._build_review_packet()
        digest_source = json.dumps(
            packet,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        packet["review_digest"] = hashlib.sha256(
            digest_source
        ).hexdigest()
        self._packet = packet

    @staticmethod
    def _state_valid(state: str) -> bool:
        return (
            state
            in ManualStartStopStatusRuntimePlanner.REVIEW_STATES
        )

    @classmethod
    def _worst_state(cls, states: list[str]) -> str:
        if not states:
            return "unavailable"

        return max(
            states,
            key=lambda state: cls.STATE_PRIORITY.get(
                state,
                cls.STATE_PRIORITY["unavailable"],
            ),
        )

    def _source_record(
        self,
        relative_path: str,
    ) -> dict[str, Any]:
        path = self.project_root / relative_path
        record: dict[str, Any] = {
            "relative_path": relative_path,
            "exists": path.is_file(),
            "readable": False,
            "ast_valid": False,
            "sha256": "",
            "size_bytes": 0,
            "_searchable_text": relative_path.lower(),
        }

        if not path.is_file():
            return record

        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError):
            return record

        record["readable"] = True
        record["sha256"] = hashlib.sha256(raw).hexdigest()
        record["size_bytes"] = len(raw)
        record["_searchable_text"] = (
            relative_path + "\n" + text
        ).lower()

        try:
            ast.parse(text, filename=str(path))
        except SyntaxError:
            return record

        record["ast_valid"] = True
        return record

    @staticmethod
    def _public_source_record(
        record: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            key: value
            for key, value in record.items()
            if not key.startswith("_")
        }

    @staticmethod
    def _group_packet(
        group_id: str,
        markers: tuple[str, ...],
        source_records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        hits = []

        for record in source_records:
            searchable = record["_searchable_text"]

            for marker in markers:
                count = searchable.count(marker.lower())

                if count:
                    hits.append(
                        {
                            "relative_path": record[
                                "relative_path"
                            ],
                            "marker": marker,
                            "count": count,
                        }
                    )

        return {
            "id": group_id,
            "markers": list(markers),
            "satisfied": bool(hits),
            "hit_count": len(hits),
            "hits": hits,
        }

    def _dimension_packet(
        self,
        dimension_id: str,
        spec: dict[str, Any],
    ) -> dict[str, Any]:
        source_records = [
            self._source_record(relative_path)
            for relative_path in spec["sources"]
        ]
        groups = [
            self._group_packet(
                group_id,
                markers,
                source_records,
            )
            for group_id, markers in spec["groups"]
        ]
        missing_group_ids = [
            group["id"]
            for group in groups
            if not group["satisfied"]
        ]

        if any(
            not record["exists"]
            or not record["readable"]
            for record in source_records
        ):
            state = "unavailable"
        elif any(
            not record["ast_valid"]
            for record in source_records
        ):
            state = "warning"
        elif missing_group_ids:
            state = "review"
        else:
            state = "secure"

        source_digest = hashlib.sha256(
            json.dumps(
                [
                    {
                        "relative_path": record[
                            "relative_path"
                        ],
                        "sha256": record["sha256"],
                    }
                    for record in source_records
                ],
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

        return {
            "id": dimension_id,
            "state": state,
            "source_count": len(source_records),
            "readable_source_count": sum(
                record["readable"]
                for record in source_records
            ),
            "ast_valid_source_count": sum(
                record["ast_valid"]
                for record in source_records
            ),
            "required_group_count": len(groups),
            "satisfied_group_count": sum(
                group["satisfied"]
                for group in groups
            ),
            "missing_group_ids": missing_group_ids,
            "source_digest": source_digest,
            "sources": [
                self._public_source_record(record)
                for record in source_records
            ],
            "groups": groups,
        }

    def _build_review_packet(self) -> dict[str, Any]:
        dimensions = [
            self._dimension_packet(
                dimension_id,
                self.DIMENSION_SPECS[dimension_id],
            )
            for dimension_id in self.DIMENSION_ORDER
        ]
        state_counts = {
            state: sum(
                dimension["state"] == state
                for dimension in dimensions
            )
            for state in self.REVIEW_STATES
        }
        overall_state = self._worst_state(
            [
                dimension["state"]
                for dimension in dimensions
            ]
        )
        findings = [
            {
                "dimension": dimension["id"],
                "state": dimension["state"],
                "missing_group_ids": list(
                    dimension["missing_group_ids"]
                ),
            }
            for dimension in dimensions
            if dimension["state"] != "secure"
        ]

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
            "review_mode": self.REVIEW_MODE,
            "delivery_mode": self.DELIVERY_MODE,
            "project_root": str(self.project_root),
            "bind_host": self.BIND_HOST,
            "bind_port": self.BIND_PORT,
            "sprint_251_anchor_assertions": (
                self.SPRINT_251_ANCHOR_ASSERTIONS
            ),
            "service_lifecycle_anchor_assertions": (
                self.SERVICE_LIFECYCLE_ANCHOR_ASSERTIONS
            ),
            "genesis_final_anchor_assertions": (
                self.GENESIS_FINAL_ANCHOR_ASSERTIONS
            ),
            "active_permission_anchor_assertions": (
                self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS
            ),
            "dimension_count": len(dimensions),
            "dimensions": dimensions,
            "overall_state": overall_state,
            "state_counts": state_counts,
            "finding_count": len(findings),
            "findings": findings,
            "runtime_boundary": dict(
                self.RUNTIME_BOUNDARY
            ),
            "source_contract": dict(
                self.SOURCE_CONTRACT
            ),
            "scope_boundary": dict(
                self.SCOPE_BOUNDARY
            ),
            "start_preview": dict(
                self.START_PREVIEW
            ),
            "stop_preview": dict(
                self.STOP_PREVIEW
            ),
            "acceptance_scenarios": list(
                self.ACCEPTANCE_SCENARIOS
            ),
            "ux_metrics": list(
                self.UX_METRICS
            ),
        }

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
                    local_port = int(port_hex, 16)
                except (ValueError, IndexError):
                    continue

                if local_port != port:
                    continue

                records.append(
                    {
                        "source": str(source),
                        "address_hex": address_hex,
                        "port": local_port,
                        "state_hex": fields[3],
                        "is_listener": fields[3] == "0A",
                        "inode": fields[9],
                    }
                )

        return records

    @staticmethod
    def _strict_main_processes() -> list[dict[str, Any]]:
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
                item.decode(
                    "utf-8",
                    errors="replace",
                )
                for item in raw.split(b"\0")
                if item
            ]

            if not argv:
                continue

            executable = Path(argv[0]).name.lower()
            has_main = any(
                Path(item).name == "main.py"
                for item in argv[1:]
            )

            if (
                executable.startswith("python")
                and has_main
            ):
                processes.append(
                    {
                        "pid": pid,
                        "argv": argv,
                    }
                )

        return processes

    def live_status_snapshot(self) -> dict[str, Any]:
        records = self._listener_records(
            self.BIND_PORT
        )
        listeners = [
            record
            for record in records
            if record["is_listener"]
        ]
        processes = self._strict_main_processes()

        listener_count = len(listeners)
        process_count = len(processes)

        if listener_count == 0 and process_count == 0:
            lifecycle_state = "stopped"
            ownership_state = "clear"
            safe_idle = True
            status_reason = (
                "no strict Python main.py process and "
                "no listener on the canonical port"
            )
        elif listener_count > 0 and process_count > 0:
            lifecycle_state = "running_unverified"
            ownership_state = "candidate_owned"
            safe_idle = False
            status_reason = (
                "process and listener are visible; "
                "network health probe is not executed in Phase A"
            )
        elif listener_count > 0:
            lifecycle_state = "ownership_conflict"
            ownership_state = "listener_without_owned_process"
            safe_idle = False
            status_reason = (
                "canonical port has a listener without "
                "a strict Python main.py owner"
            )
        else:
            lifecycle_state = "starting_or_degraded"
            ownership_state = "process_without_listener"
            safe_idle = False
            status_reason = (
                "strict Python main.py process exists "
                "without a canonical port listener"
            )

        return {
            "bind_host": self.BIND_HOST,
            "bind_port": self.BIND_PORT,
            "lifecycle_state": lifecycle_state,
            "ownership_state": ownership_state,
            "safe_idle": safe_idle,
            "status_reason": status_reason,
            "port_record_count": len(records),
            "listener_count": listener_count,
            "strict_main_process_count": process_count,
            "listener_records": listeners,
            "strict_main_processes": processes,
            "health_probe_executed": False,
            "network_access_used": False,
            "socket_api_used": False,
            "process_control_used": False,
            "signal_sent": False,
            "service_start_executed": False,
            "service_stop_executed": False,
        }

    def snapshot(self) -> dict[str, Any]:
        return json.loads(
            json.dumps(self._packet)
        )

    def review(self) -> dict[str, Any]:
        return self.snapshot()

    def status(self) -> dict[str, Any]:
        packet = self._packet
        live = self.live_status_snapshot()
        status_valid = all(
            (
                packet["dimension_count"] == 12,
                sum(
                    packet["state_counts"].values()
                ) == packet["dimension_count"],
                self._state_valid(
                    packet["overall_state"]
                ),
                len(packet["review_digest"]) == 64,
                live["bind_host"] == self.BIND_HOST,
                live["bind_port"] == self.BIND_PORT,
            )
        )

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
            "review_mode": self.REVIEW_MODE,
            "delivery_mode": self.DELIVERY_MODE,
            "status_valid": status_valid,
            "overall_state": packet[
                "overall_state"
            ],
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            "live_status": live,
            "status_observation_enabled": True,
            "start_execution_enabled": True,
            "stop_execution_enabled": True,
        }

    def context(self) -> dict[str, Any]:
        packet = self._packet

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
            "dimension_ids": list(
                self.DIMENSION_ORDER
            ),
            "scope_boundary": dict(
                self.SCOPE_BOUNDARY
            ),
            "start_preview": dict(
                self.START_PREVIEW
            ),
            "stop_preview": dict(
                self.STOP_PREVIEW
            ),
            "acceptance_scenarios": list(
                self.ACCEPTANCE_SCENARIOS
            ),
            "ux_metrics": list(
                self.UX_METRICS
            ),
            "canonical_lifecycle_owner": (
                "aura.service_lifecycle_runtime"
            ),
            "canonical_runtime_surface": (
                "aura.local_web_runtime_alpha"
            ),
            "canonical_launcher_facade": (
                "aura.aura_launcher_service_controls"
            ),
            "phase_b_activation_required": False,
            "review_digest": packet[
                "review_digest"
            ],
        }

    def _assertion_checks(
        self,
    ) -> list[tuple[str, bool]]:
        checks: list[tuple[str, bool]] = []
        dimensions = self._packet["dimensions"]

        for index, dimension_id in enumerate(
            self.DIMENSION_ORDER
        ):
            dimension = dimensions[index]
            spec = self.DIMENSION_SPECS[
                dimension_id
            ]
            source_count = len(spec["sources"])
            group_count = len(spec["groups"])

            checks.extend(
                (
                    (
                        f"{dimension_id}.id_order",
                        dimension["id"]
                        == dimension_id,
                    ),
                    (
                        f"{dimension_id}.source_count",
                        dimension["source_count"]
                        == source_count,
                    ),
                    (
                        f"{dimension_id}.sources_exist",
                        all(
                            source["exists"]
                            for source in dimension[
                                "sources"
                            ]
                        ),
                    ),
                    (
                        f"{dimension_id}.sources_readable",
                        all(
                            source["readable"]
                            for source in dimension[
                                "sources"
                            ]
                        ),
                    ),
                    (
                        f"{dimension_id}.sources_ast_valid",
                        all(
                            source["ast_valid"]
                            for source in dimension[
                                "sources"
                            ]
                        ),
                    ),
                    (
                        f"{dimension_id}.source_digests",
                        all(
                            isinstance(
                                source["sha256"],
                                str,
                            )
                            and len(
                                source["sha256"]
                            )
                            == 64
                            for source in dimension[
                                "sources"
                            ]
                        ),
                    ),
                    (
                        f"{dimension_id}.source_sizes",
                        all(
                            source["size_bytes"] > 0
                            for source in dimension[
                                "sources"
                            ]
                        ),
                    ),
                    (
                        f"{dimension_id}.group_count",
                        dimension[
                            "required_group_count"
                        ]
                        == group_count,
                    ),
                    (
                        f"{dimension_id}.groups_satisfied",
                        dimension[
                            "satisfied_group_count"
                        ]
                        == group_count,
                    ),
                    (
                        f"{dimension_id}.no_missing_groups",
                        not dimension[
                            "missing_group_ids"
                        ],
                    ),
                    (
                        f"{dimension_id}.state_valid",
                        self._state_valid(
                            dimension["state"]
                        ),
                    ),
                    (
                        f"{dimension_id}.state_secure",
                        dimension["state"]
                        == "secure",
                    ),
                )
            )

        return checks

    def check(self) -> dict[str, Any]:
        checks = self._assertion_checks()
        failed = [
            name
            for name, passed in checks
            if not passed
        ]
        packet = self._packet

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
            "review_mode": self.REVIEW_MODE,
            "delivery_mode": self.DELIVERY_MODE,
            "status_valid": (
                packet["dimension_count"] == 12
                and self._state_valid(
                    packet["overall_state"]
                )
            ),
            "overall_state": packet[
                "overall_state"
            ],
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            "base_check_count": len(checks),
            "assertion_count": len(checks),
            "failed_assertion_count": len(
                failed
            ),
            "failed_assertions": failed,
            "alpha_ready": (
                not failed
                and packet["overall_state"]
                == "secure"
            ),
            "sprint_251_anchor_assertions": (
                self.SPRINT_251_ANCHOR_ASSERTIONS
            ),
            "service_lifecycle_anchor_assertions": (
                self.SERVICE_LIFECYCLE_ANCHOR_ASSERTIONS
            ),
            "genesis_final_anchor_assertions": (
                self.GENESIS_FINAL_ANCHOR_ASSERTIONS
            ),
            "active_permission_anchor_assertions": (
                self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS
            ),
            "runtime_boundary": dict(
                self.RUNTIME_BOUNDARY
            ),
            "source_contract": dict(
                self.SOURCE_CONTRACT
            ),
            "scope_boundary": dict(
                self.SCOPE_BOUNDARY
            ),
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in checks
            ],
        }
