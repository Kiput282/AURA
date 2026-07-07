
"""AURA Runtime Action Queue Review Layer Foundation.

Planner-only/review-only foundation for future runtime action queue review.
It prepares action queue item blueprints, queue state blueprints, review
priority rules, dependency/blocker contracts, permission link requirements,
execution preflight check blueprints, approval/denial transition rules,
timeout/expiry policies, audit visibility fields, and safety policy without
creating runtime queue items, dispatching actions, executing actions, running
plugins, writing files, executing commands, controlling desktop, or invoking
real tools.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraRuntimeActionQueueReviewLayerFoundationManager:
    """Prepare runtime action queue review plans without runtime action execution."""

    name = "aura_runtime_action_queue_review_layer_foundation"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}
        with self.identity_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def normalize_text(self, text: Any) -> str:
        return " ".join(str(text or "").strip().split())

    def review_layer_plan_types(self) -> list[str]:
        return [
            "runtime_action_queue_review_layer_status",
            "action_queue_item_blueprint_plan",
            "queue_state_blueprint_plan",
            "review_priority_rule_plan",
            "dependency_blocker_contract_plan",
            "permission_link_requirement_plan",
            "execution_preflight_check_blueprint_plan",
            "approval_denial_transition_rule_plan",
            "timeout_expiry_policy_plan",
            "runtime_action_audit_visibility_plan",
            "runtime_action_queue_review_layer_context",
        ]

    def review_layer_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "layer_name": "AURA Runtime Action Queue Review Layer Foundation",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_mode": "runtime_action_review_blueprint_only",
            "runtime_mode": "review_only",
            "runtime_action_authority": "ATLAS",
            "future_executor": "ORION_or_local_agent_when_future_runtime_is_approved",
            "queue_runtime_allowed": False,
            "action_dispatch_allowed": False,
            "action_execution_allowed": False,
            "plugin_execution_allowed": False,
            "file_write_allowed": False,
            "command_execution_allowed": False,
            "desktop_control_allowed": False,
            "tool_execution_allowed": False,
        }

    def action_queue_item_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "local_open_action_item",
                "purpose": "Future queue item for safe local open actions after explicit review.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "controlled_file_write_action_item",
                "purpose": "Future queue item linked to controlled file write approval draft.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "local_web_runtime_action_item",
                "purpose": "Future queue item linked to safe local web runtime gate.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "plugin_action_item",
                "purpose": "Future queue item for permission-gated plugin actions.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "orion_client_action_item",
                "purpose": "Future queue item for ORION/local client actions.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "screen_observation_action_item",
                "purpose": "Future queue item for permission-gated screen observation actions.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "voice_bridge_action_item",
                "purpose": "Future queue item for voice bridge actions.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "workspace_action_item",
                "purpose": "Future queue item for project/workspace scoped actions.",
                "runtime_queue_enabled": False,
            },
            {
                "id": "emergency_stop_action_item",
                "purpose": "Future queue item for emergency stop review visibility.",
                "runtime_queue_enabled": False,
            },
        ]

    def queue_state_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "draft_action",
                "meaning": "Future action proposal drafted but not queued.",
                "runtime_state_enabled": False,
            },
            {
                "id": "pending_review",
                "meaning": "Future action awaiting review.",
                "runtime_state_enabled": False,
            },
            {
                "id": "blocked_by_permission",
                "meaning": "Future action blocked by missing permission.",
                "runtime_state_enabled": False,
            },
            {
                "id": "blocked_by_preflight",
                "meaning": "Future action blocked by preflight failure.",
                "runtime_state_enabled": False,
            },
            {
                "id": "approved_for_execution",
                "meaning": "Future action approved but not yet executed.",
                "runtime_state_enabled": False,
            },
            {
                "id": "denied",
                "meaning": "Future action denied by review.",
                "runtime_state_enabled": False,
            },
            {
                "id": "cancelled",
                "meaning": "Future action cancelled before execution.",
                "runtime_state_enabled": False,
            },
            {
                "id": "expired",
                "meaning": "Future action expired before approval.",
                "runtime_state_enabled": False,
            },
        ]

    def review_priority_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "emergency_stop_highest_priority",
                "purpose": "Future emergency stop queue items must always be highest priority.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "file_write_requires_high_review",
                "purpose": "Future file write actions require elevated review priority.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "command_execution_requires_high_review",
                "purpose": "Future command execution actions require elevated review priority.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "network_or_web_runtime_requires_review",
                "purpose": "Future network/web runtime actions require explicit review.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "desktop_control_requires_highest_review",
                "purpose": "Future desktop control requires strict review priority.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "low_risk_open_actions_can_be_grouped",
                "purpose": "Future low-risk open actions may be grouped for review.",
                "runtime_priority_enabled": False,
            },
            {
                "id": "priority_visible_to_control_center",
                "purpose": "Future priority must be visible to Control Center.",
                "runtime_priority_enabled": False,
            },
        ]

    def dependency_blocker_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "permission_review_dependency",
                "purpose": "Future action depends on permission review queue approval.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "capability_registry_dependency",
                "purpose": "Future action depends on capability registry state.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "safe_local_web_gate_dependency",
                "purpose": "Future web runtime action depends on safe local web runtime gate.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "file_write_approval_dependency",
                "purpose": "Future file write action depends on controlled file write approval draft.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "orion_client_presence_dependency",
                "purpose": "Future ORION action depends on approved client availability.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "workspace_scope_dependency",
                "purpose": "Future action depends on approved workspace/project scope.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "kill_switch_dependency",
                "purpose": "Future action depends on available stop/kill switch where needed.",
                "runtime_dependency_enabled": False,
            },
            {
                "id": "audit_visibility_dependency",
                "purpose": "Future action depends on auditable review/decision path.",
                "runtime_dependency_enabled": False,
            },
        ]

    def permission_link_requirements(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "permission_request_reference_required",
                "purpose": "Future queued action must link to permission request review when needed.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "scope_reference_required",
                "purpose": "Future queued action must specify permission scope.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "reviewer_decision_reference_required",
                "purpose": "Future approval/denial must reference reviewer decision.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "expiry_reference_required",
                "purpose": "Future permission-bound action must include expiry/timeout reference.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "revocation_reference_supported",
                "purpose": "Future permission revocation must be linkable to queued actions.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "least_privilege_scope_required",
                "purpose": "Future action must require the smallest necessary scope.",
                "runtime_permission_link_enabled": False,
            },
            {
                "id": "permission_link_visible_to_control_center",
                "purpose": "Future permission link must be visible in Control Center.",
                "runtime_permission_link_enabled": False,
            },
        ]

    def execution_preflight_check_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "safe_idle_or_approved_mode_check",
                "purpose": "Future execution must confirm safe_idle or approved runtime mode.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "permission_approved_check",
                "purpose": "Future execution must confirm permission approval.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "capability_online_check",
                "purpose": "Future execution must confirm capability is online and allowed.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "risk_level_check",
                "purpose": "Future execution must confirm risk level is acceptable.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "target_scope_check",
                "purpose": "Future execution must confirm target scope/path/app/window.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "dependency_clear_check",
                "purpose": "Future execution must confirm dependencies/blockers are clear.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "kill_switch_ready_check",
                "purpose": "Future execution must confirm stop/kill switch readiness.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "audit_ready_check",
                "purpose": "Future execution must confirm audit visibility is ready.",
                "runtime_preflight_enabled": False,
            },
            {
                "id": "executor_available_check",
                "purpose": "Future execution must confirm approved executor availability.",
                "runtime_preflight_enabled": False,
            },
        ]

    def approval_denial_transition_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "draft_to_pending_review",
                "purpose": "Future transition from draft to pending review.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "pending_to_blocked_by_permission",
                "purpose": "Future transition when permission is missing.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "pending_to_blocked_by_preflight",
                "purpose": "Future transition when preflight is not ready.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "pending_to_approved",
                "purpose": "Future transition after explicit approval.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "pending_to_denied",
                "purpose": "Future transition after explicit denial.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "approved_to_cancelled",
                "purpose": "Future transition when approval is cancelled before execution.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "pending_to_expired",
                "purpose": "Future transition when review expires.",
                "runtime_transition_enabled": False,
            },
            {
                "id": "blocked_to_pending_after_fix",
                "purpose": "Future transition back to review after blocker is fixed.",
                "runtime_transition_enabled": False,
            },
        ]

    def timeout_expiry_policies(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "approval_timeout_policy",
                "purpose": "Future approval expires after a defined time window.",
                "runtime_timeout_enabled": False,
            },
            {
                "id": "session_bound_approval_policy",
                "purpose": "Future approval may be bound to active session.",
                "runtime_timeout_enabled": False,
            },
            {
                "id": "high_risk_short_expiry_policy",
                "purpose": "Future high-risk actions get shorter approval expiry.",
                "runtime_timeout_enabled": False,
            },
            {
                "id": "permission_revocation_expiry_policy",
                "purpose": "Future permission revocation expires queued actions.",
                "runtime_timeout_enabled": False,
            },
            {
                "id": "stale_preflight_expiry_policy",
                "purpose": "Future stale preflight results expire approvals.",
                "runtime_timeout_enabled": False,
            },
            {
                "id": "expiry_audit_visibility_policy",
                "purpose": "Future expiry state must be visible in audit.",
                "runtime_timeout_enabled": False,
            },
        ]

    def audit_visibility_fields(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "runtime_action_event_id",
                "purpose": "Future runtime action queue review event identifier.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "action_queue_item_id",
                "purpose": "Future queue item identifier visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "action_type",
                "purpose": "Future action type visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "queue_state",
                "purpose": "Future queue state visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "risk_level",
                "purpose": "Future risk level visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "permission_reference",
                "purpose": "Future permission reference visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "dependency_blocker_summary",
                "purpose": "Future dependency/blocker summary visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "preflight_result",
                "purpose": "Future preflight result visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_decision",
                "purpose": "Future approval/denial decision visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "expiry_state",
                "purpose": "Future timeout/expiry state visibility.",
                "runtime_audit_enabled": False,
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare runtime action queue item blueprint planning.",
            "Prepare queue state blueprint planning.",
            "Prepare review priority rule planning.",
            "Prepare dependency and blocker contract planning.",
            "Prepare permission link requirement planning.",
            "Prepare execution preflight check blueprint planning.",
            "Prepare approval and denial transition rule planning.",
            "Prepare timeout and expiry policy planning.",
            "Prepare runtime action audit visibility planning.",
            "Expose runtime action queue review layer status.",
            "Keep runtime action queue review layer foundation-only, review-only, proposal-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "runtime_action_queue_runtime",
            "runtime_action_queue_item_creation",
            "runtime_action_queue_item_persistence",
            "runtime_action_queue_item_mutation",
            "runtime_action_queue_submission",
            "runtime_action_queue_review_runtime",
            "runtime_action_approval_runtime",
            "runtime_action_denial_runtime",
            "runtime_action_dispatch_runtime",
            "runtime_action_execution",
            "runtime_action_activation",
            "runtime_behavior_change",
            "local_action_runtime",
            "local_action_bridge_runtime",
            "plugin_action_execution",
            "plugin_runtime",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "desktop_control",
            "file_write_runtime",
            "controlled_file_write_runtime",
            "file_read_runtime",
            "file_modify_runtime",
            "file_delete_runtime",
            "command_execution",
            "test_execution",
            "code_execution",
            "dependency_install",
            "package_download",
            "internet_search",
            "network_action",
            "web_server_runtime",
            "http_server_start",
            "local_web_server_start",
            "api_server_runtime",
            "api_route_runtime",
            "api_request_handling",
            "api_response_serving",
            "frontend_runtime",
            "backend_runtime",
            "dashboard_render_runtime",
            "route_creation_runtime",
            "static_file_serving_runtime",
            "port_binding",
            "browser_launch",
            "websocket_runtime",
            "session_runtime",
            "chat_runtime",
            "service_runtime",
            "launcher_runtime",
            "orion_client_runtime",
            "client_connection",
            "client_pairing_runtime",
            "client_heartbeat_runtime",
            "screen_capture_runtime",
            "short_recording_runtime",
            "voice_bridge_runtime",
            "avatar_runtime",
            "three_d_environment_runtime",
            "game_companion_runtime",
            "blender_bridge_runtime",
            "vscode_project_bridge_runtime",
            "emergency_stop_runtime",
            "permission_grant_runtime",
            "permission_deny_runtime",
            "permission_resolution_runtime",
            "permission_scope_activation_runtime",
            "permission_scope_revocation_runtime",
            "approval_runtime",
            "denial_runtime",
            "memory_write",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "runtime_action_queue_review_layer_foundation_only": True,
            "action_queue_item_blueprint_only": True,
            "queue_state_blueprint_only": True,
            "review_priority_rule_blueprint_only": True,
            "dependency_blocker_contract_blueprint_only": True,
            "permission_link_requirement_blueprint_only": True,
            "execution_preflight_check_blueprint_only": True,
            "approval_denial_transition_rule_blueprint_only": True,
            "timeout_expiry_policy_blueprint_only": True,
            "audit_visibility_blueprint_only": True,
            "review_only": True,
            "proposal_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "runtime_action_queue_review_layer_data_ready": True,
            "runtime_action_queue_runtime": False,
            "runtime_action_queue_item_creation": False,
            "runtime_action_queue_item_persistence": False,
            "runtime_action_queue_item_mutation": False,
            "runtime_action_queue_submission": False,
            "runtime_action_queue_review_runtime": False,
            "runtime_action_approval_runtime": False,
            "runtime_action_denial_runtime": False,
            "runtime_action_dispatch_runtime": False,
            "runtime_action_execution": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "local_action_runtime": False,
            "local_action_bridge_runtime": False,
            "plugin_action_execution": False,
            "plugin_runtime": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "desktop_control": False,
            "file_write_runtime": False,
            "controlled_file_write_runtime": False,
            "file_read_runtime": False,
            "file_modify_runtime": False,
            "file_delete_runtime": False,
            "command_execution": False,
            "test_execution": False,
            "code_execution": False,
            "dependency_install": False,
            "package_download": False,
            "internet_search": False,
            "network_action": False,
            "web_server_runtime": False,
            "http_server_start": False,
            "local_web_server_start": False,
            "api_server_runtime": False,
            "api_route_runtime": False,
            "api_request_handling": False,
            "api_response_serving": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "dashboard_render_runtime": False,
            "route_creation_runtime": False,
            "static_file_serving_runtime": False,
            "port_binding": False,
            "browser_launch": False,
            "websocket_runtime": False,
            "session_runtime": False,
            "chat_runtime": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "orion_client_runtime": False,
            "client_connection": False,
            "client_pairing_runtime": False,
            "client_heartbeat_runtime": False,
            "screen_capture_runtime": False,
            "short_recording_runtime": False,
            "voice_bridge_runtime": False,
            "avatar_runtime": False,
            "three_d_environment_runtime": False,
            "game_companion_runtime": False,
            "blender_bridge_runtime": False,
            "vscode_project_bridge_runtime": False,
            "emergency_stop_runtime": False,
            "permission_grant_runtime": False,
            "permission_deny_runtime": False,
            "permission_resolution_runtime": False,
            "permission_scope_activation_runtime": False,
            "permission_scope_revocation_runtime": False,
            "approval_runtime": False,
            "denial_runtime": False,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "memory_write": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def review_layer_summary(self) -> dict[str, Any]:
        action_items = self.action_queue_item_blueprints()
        queue_states = self.queue_state_blueprints()
        priority_rules = self.review_priority_rules()
        blocker_contracts = self.dependency_blocker_contracts()
        permission_links = self.permission_link_requirements()
        preflight_checks = self.execution_preflight_check_blueprints()
        transition_rules = self.approval_denial_transition_rules()
        timeout_policies = self.timeout_expiry_policies()
        audit_fields = self.audit_visibility_fields()
        return {
            "runtime_action_queue_review_layer_foundation_ready": True,
            "action_queue_item_blueprint_plan_ready": True,
            "queue_state_blueprint_plan_ready": True,
            "review_priority_rule_plan_ready": True,
            "dependency_blocker_contract_plan_ready": True,
            "permission_link_requirement_plan_ready": True,
            "execution_preflight_check_blueprint_plan_ready": True,
            "approval_denial_transition_rule_plan_ready": True,
            "timeout_expiry_policy_plan_ready": True,
            "runtime_action_audit_visibility_plan_ready": True,
            "action_queue_item_blueprint_count": len(action_items),
            "queue_state_blueprint_count": len(queue_states),
            "review_priority_rule_count": len(priority_rules),
            "dependency_blocker_contract_count": len(blocker_contracts),
            "permission_link_requirement_count": len(permission_links),
            "execution_preflight_check_blueprint_count": len(preflight_checks),
            "approval_denial_transition_rule_count": len(transition_rules),
            "timeout_expiry_policy_count": len(timeout_policies),
            "audit_visibility_field_count": len(audit_fields),
            "total_review_layer_blueprint_count": (
                len(action_items)
                + len(queue_states)
                + len(priority_rules)
                + len(blocker_contracts)
                + len(permission_links)
                + len(preflight_checks)
                + len(transition_rules)
                + len(timeout_policies)
                + len(audit_fields)
            ),
            "runtime_queue_items_created": 0,
            "runtime_queue_items_persisted": 0,
            "runtime_queue_items_mutated": 0,
            "runtime_queue_items_submitted": 0,
            "runtime_queue_items_reviewed": 0,
            "runtime_queue_items_approved": 0,
            "runtime_queue_items_denied": 0,
            "runtime_queue_items_cancelled": 0,
            "runtime_queue_items_expired": 0,
            "runtime_actions_dispatched": 0,
            "runtime_actions_executed": 0,
            "runtime_local_actions_executed": 0,
            "runtime_plugin_actions_executed": 0,
            "runtime_file_writes_executed": 0,
            "runtime_commands_executed": 0,
            "runtime_tool_calls_executed": 0,
            "runtime_desktop_actions_executed": 0,
            "runtime_orion_actions_executed": 0,
            "runtime_emergency_stops_triggered": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA runtime action queue review layer foundation"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "runtime_actions_may_be_reviewed_as_blueprints_but_must_not_execute",
            "review_layer_identity": self.review_layer_identity(),
            "review_layer_plan_types": self.review_layer_plan_types(),
            "review_layer_summary": self.review_layer_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def action_queue_item_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("action_queue_item_blueprint_plan", target)
        plan["action_queue_item_blueprints"] = self.action_queue_item_blueprints()
        plan["rule"] = "Action queue item blueprints do not create runtime queue items."
        return plan

    def queue_state_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("queue_state_blueprint_plan", target)
        plan["queue_state_blueprints"] = self.queue_state_blueprints()
        plan["rule"] = "Queue state blueprints do not mutate runtime queue state."
        return plan

    def review_priority_rule_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("review_priority_rule_plan", target)
        plan["review_priority_rules"] = self.review_priority_rules()
        plan["rule"] = "Review priority planning does not schedule or execute runtime actions."
        return plan

    def dependency_blocker_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dependency_blocker_contract_plan", target)
        plan["dependency_blocker_contracts"] = self.dependency_blocker_contracts()
        plan["rule"] = "Dependency and blocker contracts do not inspect or clear runtime blockers."
        return plan

    def permission_link_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_link_requirement_plan", target)
        plan["permission_link_requirements"] = self.permission_link_requirements()
        plan["rule"] = "Permission link requirements do not grant or deny runtime permissions."
        return plan

    def execution_preflight_check_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("execution_preflight_check_blueprint_plan", target)
        plan["execution_preflight_check_blueprints"] = self.execution_preflight_check_blueprints()
        plan["rule"] = "Execution preflight check blueprints do not execute runtime preflight checks."
        return plan

    def approval_denial_transition_rule_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("approval_denial_transition_rule_plan", target)
        plan["approval_denial_transition_rules"] = self.approval_denial_transition_rules()
        plan["rule"] = "Approval/denial transition rules do not approve, deny, dispatch, or execute actions."
        return plan

    def timeout_expiry_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("timeout_expiry_policy_plan", target)
        plan["timeout_expiry_policies"] = self.timeout_expiry_policies()
        plan["rule"] = "Timeout and expiry policy planning does not expire runtime queue items."
        return plan

    def runtime_action_audit_visibility_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("runtime_action_audit_visibility_plan", target)
        plan["audit_visibility_fields"] = self.audit_visibility_fields()
        plan["rule"] = "Audit visibility planning does not write or fetch audit events."
        return plan

    def safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("runtime_action_queue_review_layer_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Runtime action queue review layer must not create runtime queue items.",
            "Runtime action queue review layer must not persist runtime queue items.",
            "Runtime action queue review layer must not mutate runtime queue items.",
            "Runtime action queue review layer must not approve or deny runtime actions.",
            "Runtime action queue review layer must not dispatch runtime actions.",
            "Runtime action queue review layer must not execute runtime actions.",
            "Runtime action queue review layer must not run plugins or tools.",
            "Runtime action queue review layer must not write files or execute commands.",
            "Runtime action queue review layer must not control desktop or ORION.",
            "Runtime action queue review layer must remain foundation-only, review-only, proposal-only, metadata-only, and safe_idle-first.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "review_layer_identity": self.review_layer_identity(),
            "review_layer_plan_types": self.review_layer_plan_types(),
            "action_queue_item_blueprints": self.action_queue_item_blueprints(),
            "queue_state_blueprints": self.queue_state_blueprints(),
            "review_priority_rules": self.review_priority_rules(),
            "dependency_blocker_contracts": self.dependency_blocker_contracts(),
            "permission_link_requirements": self.permission_link_requirements(),
            "execution_preflight_check_blueprints": self.execution_preflight_check_blueprints(),
            "approval_denial_transition_rules": self.approval_denial_transition_rules(),
            "timeout_expiry_policies": self.timeout_expiry_policies(),
            "audit_visibility_fields": self.audit_visibility_fields(),
            "review_layer_summary": self.review_layer_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.review_layer_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "runtime_action_queue_review_layer_foundation_ready": True,
            "action_queue_item_blueprint_plan_ready": True,
            "queue_state_blueprint_plan_ready": True,
            "review_priority_rule_plan_ready": True,
            "dependency_blocker_contract_plan_ready": True,
            "permission_link_requirement_plan_ready": True,
            "execution_preflight_check_blueprint_plan_ready": True,
            "approval_denial_transition_rule_plan_ready": True,
            "timeout_expiry_policy_plan_ready": True,
            "runtime_action_audit_visibility_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "runtime_action_queue_review_layer_data_ready": True,
            "review_layer_plan_types": self.review_layer_plan_types(),
            "plan_type_count": len(self.review_layer_plan_types()),
            **summary,
            **boundary,
        }
