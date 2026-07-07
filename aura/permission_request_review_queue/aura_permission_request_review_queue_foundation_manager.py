
"""AURA Permission Request Review Queue Foundation.

Planner-only foundation for future permission request review queues.
It prepares request blueprints, queue state blueprints, review packet
fields, scope boundary blueprints, decision proposal contracts, reviewer
checklist metadata, audit visibility fields, and safety policy without
granting, denying, resolving, activating, or executing permissions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraPermissionRequestReviewQueueFoundationManager:
    """Prepare permission request review queue plans without runtime."""

    name = "aura_permission_request_review_queue_foundation"
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

    def review_queue_plan_types(self) -> list[str]:
        return [
            "permission_request_review_queue_status",
            "permission_request_blueprint_plan",
            "queue_state_blueprint_plan",
            "review_packet_field_plan",
            "permission_scope_boundary_plan",
            "decision_proposal_contract_plan",
            "reviewer_checklist_plan",
            "audit_visibility_field_plan",
            "permission_request_safety_policy_plan",
            "permission_request_review_queue_context",
            "permission_request_review_queue_status_packet",
        ]

    def queue_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "queue_name": "AURA Permission Request Review Queue Foundation",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_mode": "review_queue_blueprint_only",
            "runtime_mode": "proposal_only",
            "permission_authority": "ATLAS",
            "local_executor": "ORION_or_local_agent_when_future_runtime_is_approved",
            "runtime_permission_grant_allowed": False,
            "runtime_permission_deny_allowed": False,
            "runtime_permission_resolution_allowed": False,
            "runtime_action_execution_allowed": False,
        }

    def permission_request_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "screen_capture_request",
                "title": "Screen Capture Request",
                "purpose": "Reserve future review for one-time or scoped screen screenshot permission.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "short_recording_request",
                "title": "Short Recording Request",
                "purpose": "Reserve future review for short screen recording or low-FPS frame sampling permission.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "voice_bridge_request",
                "title": "Voice Bridge Request",
                "purpose": "Reserve future review for microphone capture, push-to-talk, or speaker output bridge permissions.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "orion_client_bridge_request",
                "title": "ORION Client Bridge Request",
                "purpose": "Reserve future review for trusted ATLAS-ORION client bridge permission.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "avatar_environment_request",
                "title": "Avatar and 3D Environment Request",
                "purpose": "Reserve future review for avatar, 3D environment, expression, and lip sync bridge permissions.",
                "risk_level": "medium",
                "runtime_permission_enabled": False,
            },
            {
                "id": "blender_bridge_request",
                "title": "Blender Bridge Request",
                "purpose": "Reserve future review for Blender scene, selected object, material, UV map, texture, and addon workflow permissions.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "vscode_project_bridge_request",
                "title": "VS Code Project Bridge Request",
                "purpose": "Reserve future review for project file, editor, patch, lint, test, and terminal bridge permissions.",
                "risk_level": "critical",
                "runtime_permission_enabled": False,
            },
            {
                "id": "local_file_action_request",
                "title": "Local File Action Request",
                "purpose": "Reserve future review for open/create/write/move/delete file and folder permissions.",
                "risk_level": "critical",
                "runtime_permission_enabled": False,
            },
            {
                "id": "app_open_request",
                "title": "App Open Request",
                "purpose": "Reserve future review for opening allowlisted local software.",
                "risk_level": "medium",
                "runtime_permission_enabled": False,
            },
            {
                "id": "obs_streaming_bridge_request",
                "title": "OBS and Streaming Bridge Request",
                "purpose": "Reserve future review for OBS, streaming presence, stream-safe voice/avatar, and content pipeline permissions.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "game_companion_request",
                "title": "Game Companion Request",
                "purpose": "Reserve future review for game window observation, low-FPS sampling, event-triggered observation, and commentary mode permissions.",
                "risk_level": "high",
                "runtime_permission_enabled": False,
            },
            {
                "id": "plugin_action_request",
                "title": "Plugin Action Request",
                "purpose": "Reserve future review for plugin-specific action permissions and bridge scopes.",
                "risk_level": "critical",
                "runtime_permission_enabled": False,
            },
        ]

    def queue_state_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "draft",
                "meaning": "Request blueprint is being prepared and is not reviewable yet.",
                "runtime_state_enabled": False,
            },
            {
                "id": "submitted",
                "meaning": "Request blueprint has been submitted for future review.",
                "runtime_state_enabled": False,
            },
            {
                "id": "pending_review",
                "meaning": "Request blueprint is waiting for user review in a future queue.",
                "runtime_state_enabled": False,
            },
            {
                "id": "needs_scope",
                "meaning": "Request blueprint is too broad and needs a narrower scope before approval proposal.",
                "runtime_state_enabled": False,
            },
            {
                "id": "approved_proposal",
                "meaning": "Request blueprint can represent an approval proposal, not a runtime grant.",
                "runtime_state_enabled": False,
            },
            {
                "id": "denied_proposal",
                "meaning": "Request blueprint can represent a denial proposal, not a runtime deny action.",
                "runtime_state_enabled": False,
            },
            {
                "id": "expired",
                "meaning": "Request blueprint can represent an expired request.",
                "runtime_state_enabled": False,
            },
            {
                "id": "cancelled",
                "meaning": "Request blueprint can represent a user-cancelled request.",
                "runtime_state_enabled": False,
            },
        ]

    def review_packet_fields(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "request_id",
                "purpose": "Future unique review request identifier.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "request_type",
                "purpose": "Future permission request type.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "source_agent",
                "purpose": "Future request source such as ATLAS, ORION, plugin, or local bridge.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "target_resource",
                "purpose": "Future requested app, window, file, folder, plugin, device, or bridge target.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "requested_scope",
                "purpose": "Future one-time, session, workspace, app, mode, plugin, or bridge scope.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "requested_duration",
                "purpose": "Future request duration or expiry metadata.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "risk_level",
                "purpose": "Future risk level for user review.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "reason",
                "purpose": "Future plain-language reason for the request.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "expected_effect",
                "purpose": "Future user-visible explanation of what the permission would allow.",
                "runtime_collection_enabled": False,
            },
            {
                "id": "safe_alternative",
                "purpose": "Future safer or narrower alternative recommendation.",
                "runtime_collection_enabled": False,
            },
        ]

    def permission_scope_boundaries(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "one_time_scope",
                "purpose": "Limit a future permission to one requested action.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "session_scope",
                "purpose": "Limit a future permission to a temporary session.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "workspace_scope",
                "purpose": "Limit a future permission to a workspace root.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "app_window_scope",
                "purpose": "Limit a future permission to a selected app or window.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "mode_scope",
                "purpose": "Limit a future permission to a named AURA mode.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "plugin_scope",
                "purpose": "Limit a future permission to one plugin or plugin action set.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "bridge_scope",
                "purpose": "Limit a future permission to one bridge such as screen, voice, Blender, VS Code, OBS, game, or avatar.",
                "runtime_scope_activation_enabled": False,
            },
            {
                "id": "emergency_stop_scope",
                "purpose": "Reserve future emergency stop revocation and stop-state boundary.",
                "runtime_scope_activation_enabled": False,
            },
        ]

    def decision_proposal_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "allow_once_proposal",
                "meaning": "Blueprint for a future allow-once proposal, not a runtime grant.",
                "runtime_decision_enabled": False,
            },
            {
                "id": "allow_session_proposal",
                "meaning": "Blueprint for a future session approval proposal, not a runtime grant.",
                "runtime_decision_enabled": False,
            },
            {
                "id": "allow_scoped_proposal",
                "meaning": "Blueprint for a future scoped approval proposal, not a runtime grant.",
                "runtime_decision_enabled": False,
            },
            {
                "id": "require_narrower_scope_proposal",
                "meaning": "Blueprint for asking the user to narrow scope before approval.",
                "runtime_decision_enabled": False,
            },
            {
                "id": "deny_proposal",
                "meaning": "Blueprint for a future denial proposal, not a runtime deny action.",
                "runtime_decision_enabled": False,
            },
            {
                "id": "expire_or_cancel_proposal",
                "meaning": "Blueprint for request expiration or user cancellation metadata.",
                "runtime_decision_enabled": False,
            },
        ]

    def reviewer_checklist_items(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "verify_intent",
                "question": "Does the request match the user's current intent?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_target",
                "question": "Is the requested target clearly identified?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_scope",
                "question": "Is the requested scope narrow enough?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_duration",
                "question": "Is the requested duration limited?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_risk",
                "question": "Is the risk level visible and understandable?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_safe_alternative",
                "question": "Is there a safer alternative to the requested permission?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_audit_visibility",
                "question": "Would the future action be auditable?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_revocation",
                "question": "Can the future permission be revoked or stopped?",
                "runtime_review_enabled": False,
            },
            {
                "id": "verify_emergency_stop",
                "question": "Is emergency stop behavior clear for risky local actions?",
                "runtime_review_enabled": False,
            },
        ]

    def audit_visibility_fields(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "review_event_id",
                "purpose": "Future review event identifier.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_state",
                "purpose": "Future queue state visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_source",
                "purpose": "Future ATLAS, ORION, plugin, bridge, or local agent review source.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_target",
                "purpose": "Future requested target visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_scope",
                "purpose": "Future requested or approved-proposal scope visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_risk_level",
                "purpose": "Future risk level audit visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_outcome_proposal",
                "purpose": "Future proposal outcome visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "review_timestamp",
                "purpose": "Future review timestamp visibility.",
                "runtime_audit_enabled": False,
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare permission request blueprint planning.",
            "Prepare queue state blueprint planning.",
            "Prepare review packet field planning.",
            "Prepare permission scope boundary planning.",
            "Prepare decision proposal contract planning.",
            "Prepare reviewer checklist planning.",
            "Prepare audit visibility field planning.",
            "Prepare permission request safety policy planning.",
            "Expose permission request review queue status.",
            "Keep review queue planner-only, proposal-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "permission_request_queue_runtime",
            "permission_request_collection_runtime",
            "permission_request_persistence_runtime",
            "permission_request_mutation_runtime",
            "permission_request_submission_runtime",
            "permission_request_review_runtime",
            "permission_resolution_runtime",
            "permission_grant_runtime",
            "permission_deny_runtime",
            "permission_scope_activation_runtime",
            "permission_scope_revocation_runtime",
            "approval_runtime",
            "denial_runtime",
            "session_permission_runtime",
            "scoped_permission_runtime",
            "plugin_permission_runtime",
            "mode_permission_runtime",
            "workspace_permission_runtime",
            "app_permission_runtime",
            "bridge_permission_runtime",
            "emergency_stop_runtime",
            "orion_client_runtime",
            "orion_client_connection",
            "client_pairing_runtime",
            "client_heartbeat_runtime",
            "screen_capture_runtime",
            "short_recording_runtime",
            "voice_bridge_runtime",
            "avatar_runtime",
            "three_d_environment_runtime",
            "obs_bridge_runtime",
            "game_companion_runtime",
            "blender_bridge_runtime",
            "vscode_project_bridge_runtime",
            "local_action_bridge_runtime",
            "runtime_action_activation",
            "runtime_behavior_change",
            "dashboard_render_runtime",
            "api_server_runtime",
            "api_route_runtime",
            "api_request_handling",
            "api_response_serving",
            "http_server_start",
            "web_server_runtime",
            "local_web_server_start",
            "frontend_runtime",
            "backend_runtime",
            "route_creation_runtime",
            "static_file_serving_runtime",
            "port_binding",
            "browser_launch",
            "websocket_runtime",
            "chat_runtime",
            "session_runtime",
            "plugin_runtime",
            "service_runtime",
            "launcher_runtime",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "command_execution",
            "test_execution",
            "code_execution",
            "dependency_install",
            "package_download",
            "internet_search",
            "network_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "permission_request_review_queue_foundation_only": True,
            "permission_request_blueprint_only": True,
            "queue_state_blueprint_only": True,
            "review_packet_field_blueprint_only": True,
            "permission_scope_boundary_blueprint_only": True,
            "decision_proposal_contract_blueprint_only": True,
            "reviewer_checklist_blueprint_only": True,
            "audit_visibility_blueprint_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "permission_request_review_queue_data_ready": True,
            "permission_request_queue_runtime": False,
            "permission_request_collection_runtime": False,
            "permission_request_persistence_runtime": False,
            "permission_request_mutation_runtime": False,
            "permission_request_submission_runtime": False,
            "permission_request_review_runtime": False,
            "permission_resolution_runtime": False,
            "permission_grant_runtime": False,
            "permission_deny_runtime": False,
            "permission_scope_activation_runtime": False,
            "permission_scope_revocation_runtime": False,
            "approval_runtime": False,
            "denial_runtime": False,
            "session_permission_runtime": False,
            "scoped_permission_runtime": False,
            "plugin_permission_runtime": False,
            "mode_permission_runtime": False,
            "workspace_permission_runtime": False,
            "app_permission_runtime": False,
            "bridge_permission_runtime": False,
            "emergency_stop_runtime": False,
            "orion_client_runtime": False,
            "orion_client_connection": False,
            "client_pairing_runtime": False,
            "client_heartbeat_runtime": False,
            "screen_capture_runtime": False,
            "short_recording_runtime": False,
            "voice_bridge_runtime": False,
            "avatar_runtime": False,
            "three_d_environment_runtime": False,
            "obs_bridge_runtime": False,
            "game_companion_runtime": False,
            "blender_bridge_runtime": False,
            "vscode_project_bridge_runtime": False,
            "local_action_bridge_runtime": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "dashboard_render_runtime": False,
            "api_server_runtime": False,
            "api_route_runtime": False,
            "api_request_handling": False,
            "api_response_serving": False,
            "http_server_start": False,
            "web_server_runtime": False,
            "local_web_server_start": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "route_creation_runtime": False,
            "static_file_serving_runtime": False,
            "port_binding": False,
            "browser_launch": False,
            "websocket_runtime": False,
            "chat_runtime": False,
            "session_runtime": False,
            "plugin_runtime": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "command_execution": False,
            "test_execution": False,
            "code_execution": False,
            "dependency_install": False,
            "package_download": False,
            "internet_search": False,
            "network_action": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "desktop_control": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def review_queue_summary(self) -> dict[str, Any]:
        request_blueprints = self.permission_request_blueprints()
        queue_states = self.queue_state_blueprints()
        review_fields = self.review_packet_fields()
        scope_boundaries = self.permission_scope_boundaries()
        decision_contracts = self.decision_proposal_contracts()
        checklist_items = self.reviewer_checklist_items()
        audit_fields = self.audit_visibility_fields()
        return {
            "permission_request_review_queue_foundation_ready": True,
            "permission_request_blueprint_plan_ready": True,
            "queue_state_blueprint_plan_ready": True,
            "review_packet_field_plan_ready": True,
            "permission_scope_boundary_plan_ready": True,
            "decision_proposal_contract_plan_ready": True,
            "reviewer_checklist_plan_ready": True,
            "audit_visibility_field_plan_ready": True,
            "permission_request_safety_policy_ready": True,
            "permission_request_blueprint_count": len(request_blueprints),
            "queue_state_count": len(queue_states),
            "review_packet_field_count": len(review_fields),
            "permission_scope_boundary_count": len(scope_boundaries),
            "decision_proposal_contract_count": len(decision_contracts),
            "reviewer_checklist_item_count": len(checklist_items),
            "audit_visibility_field_count": len(audit_fields),
            "total_review_queue_blueprint_count": (
                len(request_blueprints)
                + len(queue_states)
                + len(review_fields)
                + len(scope_boundaries)
                + len(decision_contracts)
                + len(checklist_items)
                + len(audit_fields)
            ),
            "runtime_permission_requests_created": 0,
            "runtime_permission_requests_collected": 0,
            "runtime_permission_requests_persisted": 0,
            "runtime_permission_requests_mutated": 0,
            "runtime_permission_requests_submitted": 0,
            "runtime_permission_requests_reviewed": 0,
            "runtime_permissions_granted": 0,
            "runtime_permissions_denied": 0,
            "runtime_permissions_resolved": 0,
            "runtime_permission_scopes_activated": 0,
            "runtime_permission_scopes_revoked": 0,
            "runtime_actions_triggered": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA permission request review queue foundation"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "permission_requests_may_be_reviewed_as_blueprints_but_must_not_grant_or_deny_permissions",
            "queue_identity": self.queue_identity(),
            "review_queue_plan_types": self.review_queue_plan_types(),
            "review_queue_summary": self.review_queue_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def permission_request_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_request_blueprint_plan", target)
        plan["permission_request_blueprints"] = self.permission_request_blueprints()
        plan["rule"] = "Request blueprints do not create runtime permission requests."
        return plan

    def queue_state_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("queue_state_blueprint_plan", target)
        plan["queue_state_blueprints"] = self.queue_state_blueprints()
        plan["rule"] = "Queue state blueprints do not mutate runtime queue state."
        return plan

    def review_packet_field_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("review_packet_field_plan", target)
        plan["review_packet_fields"] = self.review_packet_fields()
        plan["rule"] = "Review packet fields do not collect runtime request data."
        return plan

    def permission_scope_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_scope_boundary_plan", target)
        plan["permission_scope_boundaries"] = self.permission_scope_boundaries()
        plan["rule"] = "Scope boundary planning does not activate permission scopes."
        return plan

    def decision_proposal_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("decision_proposal_contract_plan", target)
        plan["decision_proposal_contracts"] = self.decision_proposal_contracts()
        plan["rule"] = "Decision proposal contracts do not grant or deny permissions."
        return plan

    def reviewer_checklist_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("reviewer_checklist_plan", target)
        plan["reviewer_checklist_items"] = self.reviewer_checklist_items()
        plan["rule"] = "Reviewer checklist planning does not review runtime requests."
        return plan

    def audit_visibility_field_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("audit_visibility_field_plan", target)
        plan["audit_visibility_fields"] = self.audit_visibility_fields()
        plan["rule"] = "Audit visibility planning does not write or fetch audit events."
        return plan

    def permission_request_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_request_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Review queue foundation must not create runtime permission requests.",
            "Review queue foundation must not persist runtime permission requests.",
            "Review queue foundation must not mutate queue state.",
            "Review queue foundation must not submit runtime requests.",
            "Review queue foundation must not review live requests.",
            "Review queue foundation must not grant permissions.",
            "Review queue foundation must not deny permissions.",
            "Review queue foundation must not activate or revoke runtime scopes.",
            "Review queue foundation must not trigger local actions.",
            "Review queue foundation must remain planner-only, proposal-only, metadata-only, and safe_idle-first.",
        ]
        return plan

    def status_packet(self) -> dict[str, Any]:
        plan = self.base_plan("permission_request_review_queue_status_packet", "AURA permission request review queue status packet")
        plan["status_packet_ready"] = True
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "queue_identity": self.queue_identity(),
            "review_queue_plan_types": self.review_queue_plan_types(),
            "permission_request_blueprints": self.permission_request_blueprints(),
            "queue_state_blueprints": self.queue_state_blueprints(),
            "review_packet_fields": self.review_packet_fields(),
            "permission_scope_boundaries": self.permission_scope_boundaries(),
            "decision_proposal_contracts": self.decision_proposal_contracts(),
            "reviewer_checklist_items": self.reviewer_checklist_items(),
            "audit_visibility_fields": self.audit_visibility_fields(),
            "review_queue_summary": self.review_queue_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.review_queue_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "permission_request_review_queue_foundation_ready": True,
            "permission_request_blueprint_plan_ready": True,
            "queue_state_blueprint_plan_ready": True,
            "review_packet_field_plan_ready": True,
            "permission_scope_boundary_plan_ready": True,
            "decision_proposal_contract_plan_ready": True,
            "reviewer_checklist_plan_ready": True,
            "audit_visibility_field_plan_ready": True,
            "permission_request_safety_policy_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "status_packet_ready": True,
            "permission_request_review_queue_data_ready": True,
            "review_queue_plan_types": self.review_queue_plan_types(),
            "plan_type_count": len(self.review_queue_plan_types()),
            **summary,
            **boundary,
        }
