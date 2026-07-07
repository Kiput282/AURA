"""AURA Safe Local Action Contract Review Foundation.

Sprint 115.

Planner-only and contract-review-only foundation for future safe local action
contracts without opening files/folders/software, creating files/folders, writing
files, starting services, dispatching actions, executing tools/commands,
connecting ORION, writing memory, or performing git runtime.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class AuraSafeLocalActionContractReviewFoundationManager:
    """Prepare safe local action contract review plans without local action runtime."""

    name = "aura_safe_local_action_contract_review_foundation"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "safe_local_action_contract_review_status",
        "local_open_contract_review_plan",
        "controlled_create_contract_review_plan",
        "controlled_write_preview_contract_review_plan",
        "action_preview_packet_contract_plan",
        "permission_scope_contract_review_plan",
        "side_effect_boundary_contract_plan",
        "rollback_cancel_contract_review_plan",
        "dashboard_contract_payload_plan",
        "future_action_runtime_boundary_plan",
        "safe_local_action_contract_review_context",
    ]

    BLUEPRINTS = {
        "local_open_contract_items": [
            "open_project_folder_contract",
            "open_specific_file_contract",
            "open_allowlisted_software_contract",
            "open_dashboard_contract",
            "open_project_location_contract",
            "deny_arbitrary_path_open_contract",
            "open_preview_required_contract",
            "open_manual_approval_required_contract",
        ],
        "controlled_create_contract_items": [
            "create_folder_contract",
            "create_simple_file_contract",
            "create_template_file_contract",
            "target_path_allowlist_contract",
            "content_preview_required_contract",
            "create_permission_required_contract",
            "create_rollback_preview_required_contract",
            "deny_bulk_create_contract",
        ],
        "controlled_write_preview_contract_items": [
            "write_preview_only_contract",
            "single_file_write_boundary_contract",
            "simple_text_write_boundary_contract",
            "template_write_boundary_contract",
            "diff_preview_required_contract",
            "explicit_confirmation_required_contract",
            "deny_mass_edit_contract",
            "deny_hidden_mutation_contract",
        ],
        "action_preview_packet_contract_items": [
            "action_id_required_contract",
            "intent_summary_required_contract",
            "target_summary_required_contract",
            "side_effect_summary_required_contract",
            "risk_summary_required_contract",
            "permission_reference_required_contract",
            "rollback_reference_required_contract",
            "cancel_option_required_contract",
        ],
        "permission_scope_contract_items": [
            "read_project_scope_contract",
            "safe_local_open_scope_contract",
            "controlled_create_scope_contract",
            "controlled_write_scope_contract",
            "service_start_scope_deferred_contract",
            "scope_allowlist_required_contract",
            "deny_unknown_scope_contract",
            "manual_approval_required_contract",
        ],
        "side_effect_boundary_contract_items": [
            "deny_delete_contract",
            "deny_mass_edit_contract",
            "deny_arbitrary_shell_contract",
            "deny_network_runtime_contract",
            "deny_service_start_contract",
            "deny_port_binding_contract",
            "deny_orion_runtime_contract",
            "deny_external_action_contract",
        ],
        "rollback_cancel_contract_items": [
            "rollback_preview_required_contract",
            "cancel_before_execution_contract",
            "deny_missing_rollback_contract",
            "deny_missing_cancel_path_contract",
            "revert_plan_reference_contract",
            "no_partial_runtime_commit_contract",
            "safe_idle_after_cancel_contract",
            "user_visible_cancel_result_contract",
        ],
        "dashboard_contract_payload_items": [
            "dashboard_action_id_payload_contract",
            "dashboard_action_type_payload_contract",
            "dashboard_target_payload_contract",
            "dashboard_preview_payload_contract",
            "dashboard_permission_payload_contract",
            "dashboard_risk_payload_contract",
            "dashboard_rollback_payload_contract",
            "dashboard_decision_state_payload_contract",
        ],
        "future_action_runtime_boundary_items": [
            "future_action_runtime_requires_permission_contract",
            "future_action_runtime_requires_manual_approval_contract",
            "future_action_runtime_requires_audit_reference_contract",
            "future_action_runtime_requires_safe_runtime_profile_contract",
            "future_action_runtime_requires_rollback_preview_contract",
            "future_action_runtime_requires_emergency_stop_contract",
            "future_action_runtime_requires_allowlist_contract",
            "future_action_runtime_remains_disabled_now_contract",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_safe_local_action_activation",
        "runtime_local_open_execution",
        "runtime_controlled_create_execution",
        "runtime_controlled_write_execution",
        "runtime_action_preview_execution",
        "runtime_action_dispatch",
        "runtime_action_execution",
        "runtime_permission_change",
        "runtime_audit_event_write",
        "runtime_tool_execution",
        "runtime_command_execution",
        "runtime_file_read",
        "runtime_file_write",
        "runtime_file_modify",
        "runtime_file_delete",
        "runtime_service_start",
        "runtime_port_binding",
        "runtime_network_probe",
        "runtime_orion_handshake",
        "runtime_memory_write",
        "runtime_git_operation",
        "api_server_runtime",
        "web_server_runtime",
        "frontend_runtime",
        "backend_runtime",
        "orion_client_runtime",
        "desktop_control",
        "file_read",
        "file_write",
        "file_modify",
        "file_delete",
        "command_execution",
        "tool_execution",
        "real_tool_execution",
        "external_action_execution",
        "memory_write",
        "git_commit",
        "git_push",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_safe_local_actions_activated",
        "runtime_local_open_actions_executed",
        "runtime_controlled_create_actions_executed",
        "runtime_controlled_write_actions_executed",
        "runtime_action_previews_executed",
        "runtime_actions_dispatched",
        "runtime_actions_executed",
        "runtime_permissions_changed",
        "runtime_audit_events_written",
        "runtime_tools_executed",
        "runtime_commands_executed",
        "runtime_files_read",
        "runtime_files_written",
        "runtime_files_modified",
        "runtime_files_deleted",
        "runtime_services_started",
        "runtime_ports_bound",
        "runtime_network_probes",
        "runtime_orion_handshakes",
        "runtime_memory_writes",
        "runtime_git_operations",
        "runtime_execution_features",
    ]

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

    def _items(self, key: str) -> list[dict[str, Any]]:
        return [
            {
                "id": item,
                "safe_local_action_contract_review_only": True,
                "runtime_enabled": False,
            }
            for item in self.BLUEPRINTS[key]
        ]

    def _runtime_false_flags(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _runtime_zero_counters(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "safe_local_action_contract_review_foundation_only": True,
            "safe_local_action_contract_review_blueprint_only": True,
            "contract_review_only": True,
            "review_only": True,
            "foundation_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "runtime_upgrade_deferred": True,
            "manual_approval_required_for_future_runtime": True,
            **self._runtime_false_flags(),
        }

    def summary(self) -> dict[str, Any]:
        counts = {f"{key}_count": len(value) for key, value in self.BLUEPRINTS.items()}
        return {
            "safe_local_action_contract_review_foundation_ready": True,
            "local_open_contract_review_plan_ready": True,
            "controlled_create_contract_review_plan_ready": True,
            "controlled_write_preview_contract_review_plan_ready": True,
            "action_preview_packet_contract_plan_ready": True,
            "permission_scope_contract_review_plan_ready": True,
            "side_effect_boundary_contract_plan_ready": True,
            "rollback_cancel_contract_review_plan_ready": True,
            "dashboard_contract_payload_plan_ready": True,
            "future_action_runtime_boundary_plan_ready": True,
            **counts,
            "total_safe_local_action_contract_review_blueprint_count": sum(counts.values()),
            **self._runtime_zero_counters(),
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": " ".join(str(target or "AURA safe local action contract review").split()),
            "principle": "Safe local action contracts may be reviewed, but no local action may execute and no file or desktop state may be changed.",
            "plan_types": self.PLAN_TYPES,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def local_open_contract_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_open_contract_review_plan", target)
        plan["local_open_contract_items"] = self._items("local_open_contract_items")
        return plan

    def controlled_create_contract_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("controlled_create_contract_review_plan", target)
        plan["controlled_create_contract_items"] = self._items("controlled_create_contract_items")
        return plan

    def controlled_write_preview_contract_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("controlled_write_preview_contract_review_plan", target)
        plan["controlled_write_preview_contract_items"] = self._items("controlled_write_preview_contract_items")
        return plan

    def action_preview_packet_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("action_preview_packet_contract_plan", target)
        plan["action_preview_packet_contract_items"] = self._items("action_preview_packet_contract_items")
        return plan

    def permission_scope_contract_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_scope_contract_review_plan", target)
        plan["permission_scope_contract_items"] = self._items("permission_scope_contract_items")
        return plan

    def side_effect_boundary_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("side_effect_boundary_contract_plan", target)
        plan["side_effect_boundary_contract_items"] = self._items("side_effect_boundary_contract_items")
        return plan

    def rollback_cancel_contract_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("rollback_cancel_contract_review_plan", target)
        plan["rollback_cancel_contract_items"] = self._items("rollback_cancel_contract_items")
        return plan

    def dashboard_contract_payload_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dashboard_contract_payload_plan", target)
        plan["dashboard_contract_payload_items"] = self._items("dashboard_contract_payload_items")
        return plan

    def future_action_runtime_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("future_action_runtime_boundary_plan", target)
        plan["future_action_runtime_boundary_items"] = self._items("future_action_runtime_boundary_items")
        return plan

    def context(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "plan_types": self.PLAN_TYPES,
            "blueprints": self.BLUEPRINTS,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "context_ready": True,
            "safe_local_action_contract_review_data_ready": True,
            "plan_types": self.PLAN_TYPES,
            "plan_type_count": len(self.PLAN_TYPES),
            **self.summary(),
            **self.safety_boundary(),
        }
