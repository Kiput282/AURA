"""AURA ORION Client Boundary Contract Foundation.

Sprint 116.

Planner-only and boundary-contract-only foundation for future ATLAS <-> ORION
client boundaries without starting ORION client runtime, attempting handshakes,
capturing screen, starting voice/avatar sessions, executing local actions,
controlling desktop, starting services, probing networks, mutating files,
writing audit events, writing memory, or performing git runtime.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class AuraOrionClientBoundaryContractFoundationManager:
    """Prepare ORION client boundary contracts without ORION runtime."""

    name = "aura_orion_client_boundary_contract_foundation"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "orion_client_boundary_contract_status",
        "orion_client_identity_boundary_plan",
        "atlas_orion_authority_boundary_plan",
        "orion_sense_permission_boundary_plan",
        "orion_local_action_boundary_plan",
        "orion_emergency_stop_boundary_plan",
        "orion_dashboard_status_boundary_plan",
        "orion_runtime_handshake_boundary_plan",
        "orion_data_flow_redaction_boundary_plan",
        "future_orion_runtime_boundary_plan",
        "orion_client_boundary_contract_context",
    ]

    BLUEPRINTS = {
        "orion_client_identity_boundary_items": [
            "orion_client_id_required_contract",
            "orion_device_name_required_contract",
            "orion_runtime_role_declared_contract",
            "orion_capability_advertisement_preview_contract",
            "orion_trust_state_visible_contract",
            "orion_client_version_visible_contract",
            "orion_identity_no_auto_trust_contract",
            "orion_identity_manual_review_required_contract",
        ],
        "atlas_orion_authority_boundary_items": [
            "atlas_permission_authority_contract",
            "atlas_planner_authority_contract",
            "atlas_audit_authority_contract",
            "orion_client_body_role_contract",
            "orion_no_permission_mutation_contract",
            "orion_no_policy_override_contract",
            "orion_no_unreviewed_action_contract",
            "atlas_final_decision_required_contract",
        ],
        "orion_sense_permission_boundary_items": [
            "screen_capture_requires_permission_contract",
            "voice_input_requires_permission_contract",
            "camera_input_requires_permission_contract",
            "window_context_requires_permission_contract",
            "clipboard_context_requires_permission_contract",
            "obs_context_requires_permission_contract",
            "game_context_requires_permission_contract",
            "senses_default_disabled_contract",
        ],
        "orion_local_action_boundary_items": [
            "local_open_requires_approval_contract",
            "controlled_create_requires_approval_contract",
            "controlled_write_requires_approval_contract",
            "desktop_control_deferred_contract",
            "game_control_deferred_contract",
            "blender_automation_deferred_contract",
            "obs_automation_deferred_contract",
            "orion_action_runtime_disabled_contract",
        ],
        "orion_emergency_stop_boundary_items": [
            "emergency_stop_required_contract",
            "emergency_stop_user_visible_contract",
            "emergency_stop_blocks_actions_contract",
            "emergency_stop_blocks_senses_contract",
            "emergency_stop_blocks_handshake_contract",
            "emergency_stop_reset_requires_user_contract",
            "emergency_stop_state_dashboard_visible_contract",
            "safe_idle_after_stop_contract",
        ],
        "orion_dashboard_status_boundary_items": [
            "orion_connection_status_payload_contract",
            "orion_permission_status_payload_contract",
            "orion_sense_status_payload_contract",
            "orion_action_status_payload_contract",
            "orion_emergency_stop_payload_contract",
            "orion_runtime_deferred_payload_contract",
            "orion_risk_status_payload_contract",
            "orion_v1_cutline_payload_contract",
        ],
        "orion_runtime_handshake_boundary_items": [
            "handshake_requires_manual_approval_contract",
            "handshake_requires_safe_runtime_profile_contract",
            "handshake_requires_permission_scope_contract",
            "handshake_requires_audit_reference_contract",
            "handshake_requires_emergency_stop_contract",
            "handshake_requires_client_identity_contract",
            "handshake_requires_network_boundary_review_contract",
            "handshake_remains_disabled_now_contract",
        ],
        "orion_data_flow_redaction_boundary_items": [
            "screen_data_redaction_contract",
            "voice_data_redaction_contract",
            "camera_data_redaction_contract",
            "file_path_redaction_contract",
            "token_secret_redaction_contract",
            "private_window_redaction_contract",
            "user_visible_summary_required_contract",
            "raw_data_not_persisted_contract",
        ],
        "future_orion_runtime_boundary_items": [
            "future_orion_runtime_requires_permission_contract",
            "future_orion_runtime_requires_manual_approval_contract",
            "future_orion_runtime_requires_audit_review_contract",
            "future_orion_runtime_requires_safe_profile_contract",
            "future_orion_runtime_requires_rollback_preview_contract",
            "future_orion_runtime_requires_emergency_stop_contract",
            "future_orion_runtime_requires_scope_allowlist_contract",
            "future_orion_runtime_remains_disabled_now_contract",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_orion_client_boundary_activation",
        "runtime_orion_client_start",
        "runtime_orion_handshake_attempt",
        "runtime_orion_handshake_complete",
        "runtime_screen_capture_start",
        "runtime_voice_session_start",
        "runtime_avatar_session_start",
        "runtime_local_action_execution",
        "runtime_desktop_control_execution",
        "runtime_orion_event_emit",
        "runtime_orion_state_write",
        "runtime_permission_change",
        "runtime_audit_event_write",
        "runtime_action_dispatch",
        "runtime_action_execution",
        "runtime_tool_execution",
        "runtime_command_execution",
        "runtime_file_read",
        "runtime_file_write",
        "runtime_file_modify",
        "runtime_file_delete",
        "runtime_service_start",
        "runtime_port_binding",
        "runtime_network_probe",
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
        "runtime_orion_client_boundaries_activated",
        "runtime_orion_clients_started",
        "runtime_orion_handshakes_attempted",
        "runtime_orion_handshakes_completed",
        "runtime_screen_captures_started",
        "runtime_voice_sessions_started",
        "runtime_avatar_sessions_started",
        "runtime_local_actions_executed",
        "runtime_desktop_controls_executed",
        "runtime_orion_events_emitted",
        "runtime_orion_states_written",
        "runtime_permissions_changed",
        "runtime_audit_events_written",
        "runtime_actions_dispatched",
        "runtime_actions_executed",
        "runtime_tools_executed",
        "runtime_commands_executed",
        "runtime_files_read",
        "runtime_files_written",
        "runtime_files_modified",
        "runtime_files_deleted",
        "runtime_services_started",
        "runtime_ports_bound",
        "runtime_network_probes",
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
                "orion_client_boundary_contract_only": True,
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
            "orion_client_boundary_contract_foundation_only": True,
            "orion_client_boundary_contract_blueprint_only": True,
            "boundary_contract_only": True,
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
            "orion_client_boundary_contract_foundation_ready": True,
            "orion_client_identity_boundary_plan_ready": True,
            "atlas_orion_authority_boundary_plan_ready": True,
            "orion_sense_permission_boundary_plan_ready": True,
            "orion_local_action_boundary_plan_ready": True,
            "orion_emergency_stop_boundary_plan_ready": True,
            "orion_dashboard_status_boundary_plan_ready": True,
            "orion_runtime_handshake_boundary_plan_ready": True,
            "orion_data_flow_redaction_boundary_plan_ready": True,
            "future_orion_runtime_boundary_plan_ready": True,
            **counts,
            "total_orion_client_boundary_contract_blueprint_count": sum(counts.values()),
            **self._runtime_zero_counters(),
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": " ".join(str(target or "AURA ORION client boundary contract").split()),
            "principle": "ORION may be modeled as a future client/body boundary, but no ORION runtime, handshake, sense capture, local action, or desktop control may start.",
            "plan_types": self.PLAN_TYPES,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def orion_client_identity_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_client_identity_boundary_plan", target)
        plan["orion_client_identity_boundary_items"] = self._items("orion_client_identity_boundary_items")
        return plan

    def atlas_orion_authority_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("atlas_orion_authority_boundary_plan", target)
        plan["atlas_orion_authority_boundary_items"] = self._items("atlas_orion_authority_boundary_items")
        return plan

    def orion_sense_permission_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_sense_permission_boundary_plan", target)
        plan["orion_sense_permission_boundary_items"] = self._items("orion_sense_permission_boundary_items")
        return plan

    def orion_local_action_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_local_action_boundary_plan", target)
        plan["orion_local_action_boundary_items"] = self._items("orion_local_action_boundary_items")
        return plan

    def orion_emergency_stop_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_emergency_stop_boundary_plan", target)
        plan["orion_emergency_stop_boundary_items"] = self._items("orion_emergency_stop_boundary_items")
        return plan

    def orion_dashboard_status_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_dashboard_status_boundary_plan", target)
        plan["orion_dashboard_status_boundary_items"] = self._items("orion_dashboard_status_boundary_items")
        return plan

    def orion_runtime_handshake_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_runtime_handshake_boundary_plan", target)
        plan["orion_runtime_handshake_boundary_items"] = self._items("orion_runtime_handshake_boundary_items")
        return plan

    def orion_data_flow_redaction_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_data_flow_redaction_boundary_plan", target)
        plan["orion_data_flow_redaction_boundary_items"] = self._items("orion_data_flow_redaction_boundary_items")
        return plan

    def future_orion_runtime_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("future_orion_runtime_boundary_plan", target)
        plan["future_orion_runtime_boundary_items"] = self._items("future_orion_runtime_boundary_items")
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
            "orion_client_boundary_contract_data_ready": True,
            "plan_types": self.PLAN_TYPES,
            "plan_type_count": len(self.PLAN_TYPES),
            **self.summary(),
            **self.safety_boundary(),
        }
