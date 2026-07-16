from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any


class AuraLauncherServiceControlsPlanner:
    VERSION = "1.1.1"
    ANCHOR_VERSION = "1.1.0"
    CURRENT_SPRINT = 251
    NEXT_SPRINT = 252
    NEXT_VERSION = "1.1.2"
    BOUNDARY = "aura_launcher_service_controls"
    NEXT_BOUNDARY = "manual_start_stop_status_runtime"
    OWNER = "AuraLauncherServiceControlsPlanner"
    CONTRACT_MODE = "read_only_launcher_service_controls_integration"
    REVIEW_MODE = "source_contract_evidence_snapshot"
    DELIVERY_MODE = "integration_facade_read_only"
    EXPECTED_ASSERTION_COUNT = 120
    SPRINT_250_ANCHOR_ASSERTIONS = 96
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
        "launcher_surface_contract",
        "canonical_service_state_model",
        "manual_start_preview_boundary",
        "manual_stop_preview_boundary",
        "status_and_health_visibility",
        "restart_and_recovery_preview",
        "log_visibility_boundary",
        "permission_audit_and_ownership",
        "safe_idle_failure_behavior",
        "integration_acceptance_scenario",
    )

    DIMENSION_SPECS = {
        "launcher_surface_contract": {
            "sources": (
                "aura/partner_runtime/"
                "service_persistence_and_launcher_planner.py",
                "aura/launcher_monitor/"
                "aura_launcher_health_monitor_foundation_manager.py",
                "aura/control_center_service_monitor_panel_foundation/"
                "aura_control_center_service_monitor_panel_foundation_manager.py",
            ),
            "groups": (
                ("launcher_identity", ("launcher",)),
                ("service_projection", ("service",)),
                ("status_monitor", ("status", "monitor")),
                ("manual_entry", ("manual", "explicit", "review")),
            ),
        },
        "canonical_service_state_model": {
            "sources": (
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_determinism_planner.py",
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/local_service_runtime_foundation/"
                "aura_local_service_runtime_foundation_manager.py",
            ),
            "groups": (
                ("lifecycle_state", ("lifecycle", "state")),
                ("stopped_state", ("stopped", "stop")),
                ("running_ready_state", ("running", "ready")),
                ("failure_state", ("failed", "error", "safe_idle")),
            ),
        },
        "manual_start_preview_boundary": {
            "sources": (
                "aura/local_service_start_proposal_review/"
                "aura_local_service_start_proposal_review_foundation_manager.py",
                "aura/service_control_command_review_foundation/"
                "aura_service_control_command_review_foundation_manager.py",
                "aura/service_permission_gate_runtime_boundary/"
                "aura_service_permission_gate_runtime_boundary_manager.py",
            ),
            "groups": (
                ("start_request", ("start",)),
                ("proposal_preview", ("proposal", "preview", "review")),
                ("approval_gate", ("approval", "permission", "confirm")),
                ("execution_deferred", ("disabled", "deferred", "no_start")),
            ),
        },
        "manual_stop_preview_boundary": {
            "sources": (
                "aura/service_control_command_review_foundation/"
                "aura_service_control_command_review_foundation_manager.py",
                "aura/service_lifecycle_runtime/"
                "aura_service_lifecycle_runtime_manager.py",
                "aura/runtime_action_execution_preview_packet/"
                "aura_runtime_action_execution_preview_packet_foundation_manager.py",
            ),
            "groups": (
                ("stop_request", ("stop",)),
                ("bounded_preview", ("preview", "review", "proposal")),
                ("ownership_check", ("owner", "ownership", "process")),
                ("execution_boundary", ("execution", "disabled", "allow")),
            ),
        },
        "status_and_health_visibility": {
            "sources": (
                "aura/health_status_api_runtime/"
                "aura_health_status_api_runtime_manager.py",
                "aura/local_service_health_endpoint_foundation/"
                "aura_local_service_health_endpoint_foundation_manager.py",
                "aura/control_center_read_only_status_panel_foundation/"
                "aura_control_center_read_only_status_panel_foundation_manager.py",
            ),
            "groups": (
                ("status_surface", ("status",)),
                ("health_surface", ("health",)),
                ("readiness_surface", ("ready", "readiness")),
                ("read_only_visibility", ("read_only", "read-only", "visibility")),
            ),
        },
        "restart_and_recovery_preview": {
            "sources": (
                "aura/service_recovery_restart_policy_foundation/"
                "aura_service_recovery_restart_policy_foundation_manager.py",
                "aura/runtime_recovery_drill_boundary_review/"
                "aura_runtime_recovery_drill_boundary_review_foundation_manager.py",
                "aura/runtime_error_rollback_preview/"
                "aura_runtime_error_rollback_preview_foundation_manager.py",
            ),
            "groups": (
                ("restart_sequence", ("restart",)),
                ("recovery_path", ("recovery",)),
                ("rollback_preview", ("rollback", "preview")),
                ("safe_idle_return", ("safe_idle", "safe-idle")),
            ),
        },
        "log_visibility_boundary": {
            "sources": (
                "aura/launcher_monitor/"
                "aura_launcher_health_monitor_foundation_manager.py",
                "aura/control_center_action_log_panel_foundation/"
                "aura_control_center_action_log_panel_foundation_manager.py",
                "aura/log_rotation_storage_cleanup/"
                "aura_log_rotation_storage_cleanup_planner.py",
            ),
            "groups": (
                ("log_surface", ("log",)),
                ("read_visibility", ("read", "view", "visibility")),
                ("retention_rotation", ("retention", "rotation", "rotated")),
                ("mutation_protection", ("delete", "truncate", "mutation", "protected")),
            ),
        },
        "permission_audit_and_ownership": {
            "sources": (
                "aura/service_permission_gate_runtime_boundary/"
                "aura_service_permission_gate_runtime_boundary_manager.py",
                "aura/service_audit_link_foundation/"
                "aura_service_audit_link_foundation_manager.py",
                "aura/permissions/"
                "active_permission_runtime_planner.py",
            ),
            "groups": (
                ("permission_gate", ("permission",)),
                ("approval_requirement", ("approval", "grant", "confirm")),
                ("audit_link", ("audit", "event", "trace")),
                ("ownership_boundary", ("owner", "ownership", "process")),
            ),
        },
        "safe_idle_failure_behavior": {
            "sources": (
                "aura/local_service_safe_idle_boot_boundary/"
                "aura_local_service_safe_idle_boot_boundary_manager.py",
                "aura/service_recovery_restart_policy_foundation/"
                "aura_service_recovery_restart_policy_foundation_manager.py",
                "aura/runtime_safety_freeze_manual_approval_barrier/"
                "aura_runtime_safety_freeze_manual_approval_barrier_foundation_manager.py",
            ),
            "groups": (
                ("safe_idle_default", ("safe_idle", "safe-idle")),
                ("failure_boundary", ("failure", "failed", "error")),
                ("recovery_boundary", ("recovery", "restart")),
                ("freeze_or_approval", ("freeze", "approval", "manual")),
            ),
        },
        "integration_acceptance_scenario": {
            "sources": (
                "aura/partner_runtime/"
                "service_persistence_and_launcher_planner.py",
                "aura/local_interaction_runtime_stabilization/"
                "aura_local_interaction_runtime_stabilization_manager.py",
                "aura/dashboard_runtime_readiness_view_model/"
                "aura_dashboard_runtime_readiness_view_model_foundation_manager.py",
            ),
            "groups": (
                ("launcher_handoff", ("launcher",)),
                ("service_integration", ("service",)),
                ("dashboard_projection", ("dashboard", "control_center")),
                ("acceptance_stabilization", ("acceptance", "stabilization", "ready")),
            ),
        },
    }

    INTEGRATION_SCENARIOS = (
        "ATLAS boots with AURA service stopped by default",
        "launcher reads canonical stopped state without process mutation",
        "start request returns bounded preview and approval requirement",
        "status correlates ownership health port and safe-idle state",
        "logs remain read-only and clearly scoped",
        "restart is stop verification start health verification",
        "failure returns to safe-idle without orphan process",
        "Sprint 252 activates controls without replacing this schema",
    )

    RUNTIME_BOUNDARY = {
        "service_start_execution_enabled": False,
        "service_stop_execution_enabled": False,
        "service_restart_execution_enabled": False,
        "process_control_enabled": False,
        "socket_activation_enabled": False,
        "network_access_enabled": False,
        "systemd_mutation_enabled": False,
        "autostart_mutation_enabled": False,
        "log_mutation_enabled": False,
        "permission_mutation_enabled": False,
        "audit_write_enabled": False,
        "recovery_execution_enabled": False,
        "command_execution_enabled": False,
    }

    SOURCE_CONTRACT = {
        "python_source_read_only": True,
        "ast_inspection_only": True,
        "canonical_data_content_read": False,
        "runtime_manager_imported": False,
        "service_runtime_executed": False,
        "subprocess_used": False,
        "network_access_used": False,
        "file_mutation_used": False,
        "systemd_access_used": False,
        "log_content_read": False,
    }

    SCOPE_BOUNDARY = {
        "integration_facade_only": True,
        "canonical_lifecycle_owner_reused": True,
        "duplicate_service_manager_created": False,
        "manual_start_deferred_to_sprint_252": True,
        "manual_stop_deferred_to_sprint_252": True,
        "manual_restart_deferred_to_later_activation": True,
        "autostart_remains_disabled": True,
        "safe_idle_required": True,
        "manual_approval_required": True,
        "loopback_only_required": True,
    }

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
        return state in AuraLauncherServiceControlsPlanner.REVIEW_STATES

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
            "sprint_250_anchor_assertions": (
                self.SPRINT_250_ANCHOR_ASSERTIONS
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
            "integration_scenarios": list(
                self.INTEGRATION_SCENARIOS
            ),
        }

    def snapshot(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._packet))

    def review(self) -> dict[str, Any]:
        return self.snapshot()

    def status(self) -> dict[str, Any]:
        packet = self._packet
        status_valid = all(
            (
                packet["dimension_count"] == 10,
                sum(
                    packet["state_counts"].values()
                ) == packet["dimension_count"],
                self._state_valid(
                    packet["overall_state"]
                ),
                len(packet["review_digest"]) == 64,
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
            "runtime_activation_enabled": False,
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
            "integration_scenarios": list(
                self.INTEGRATION_SCENARIOS
            ),
            "canonical_lifecycle_owner": (
                "aura.service_lifecycle_runtime"
            ),
            "canonical_launcher_anchor": (
                "aura.partner_runtime."
                "service_persistence_and_launcher_planner"
            ),
            "activation_deferred_to_sprint": 252,
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
        status = self.status()
        runtime = dict(self.RUNTIME_BOUNDARY)

        return {
            **status,
            "base_check_count": len(checks),
            "assertion_count": len(checks),
            "failed_assertion_count": len(
                failed
            ),
            "failed_assertions": failed,
            "alpha_ready": (
                not failed
                and status["status_valid"]
                and status["overall_state"]
                == "secure"
            ),
            "sprint_250_anchor_assertions": (
                self.SPRINT_250_ANCHOR_ASSERTIONS
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
            "source_contract": dict(
                self.SOURCE_CONTRACT
            ),
            "scope_boundary": dict(
                self.SCOPE_BOUNDARY
            ),
            **runtime,
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in checks
            ],
        }
