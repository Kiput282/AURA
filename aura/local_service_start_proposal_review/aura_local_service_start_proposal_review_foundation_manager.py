"""AURA Local Service Start Proposal Review Foundation.

Sprint 103.

Planner-only proposal/review foundation for future local service start requests.
It prepares service start proposal review blueprints without starting services,
binding ports, probing networks, changing permissions, dispatching actions,
executing tools/commands, connecting ORION, writing memory, or performing git runtime.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class AuraLocalServiceStartProposalReviewFoundationManager:
    """Prepare local service start proposal review plans without starting services."""

    name = "aura_local_service_start_proposal_review_foundation"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_service_start_proposal_review_status",
        "service_start_candidate_inventory_plan",
        "service_start_preflight_requirement_plan",
        "port_binding_review_plan",
        "process_launch_boundary_plan",
        "permission_requirement_plan",
        "risk_classification_plan",
        "rollback_kill_switch_plan",
        "audit_event_plan",
        "user_approval_decision_plan",
        "local_service_start_proposal_review_context",
    ]

    BLUEPRINTS = {
        "service_start_candidates": [
            "local_console_static_preview",
            "local_console_api_mock",
            "control_center_status_endpoint",
            "permission_review_queue_preview",
            "chat_session_preview_endpoint",
            "safe_local_web_runtime_candidate",
            "orion_handshake_mock_service",
            "high_risk_external_service_deferred",
        ],
        "preflight_requirements": [
            "explicit_service_name",
            "explicit_user_intent",
            "safe_runtime_profile_reference",
            "permission_scope_reference",
            "port_policy_reference",
            "dry_run_preview_required",
            "rollback_path_required",
            "audit_event_required",
            "manual_final_approval_required",
        ],
        "port_binding_reviews": [
            "localhost_only_preference",
            "public_interface_forbidden_by_default",
            "port_conflict_check_required_for_future",
            "reserved_port_blocklist_required",
            "external_tunnel_forbidden_by_default",
            "websocket_port_requires_future_review",
            "api_port_requires_future_review",
            "orion_port_requires_future_review",
        ],
        "process_launch_boundaries": [
            "no_process_launch_now",
            "no_daemon_start_now",
            "no_background_worker_start_now",
            "no_web_server_start_now",
            "no_api_server_start_now",
            "no_websocket_start_now",
            "no_orion_client_start_now",
            "future_launch_requires_user_approval",
        ],
        "permission_requirements": [
            "read_project_for_proposal_view",
            "review_project_for_preflight_packet",
            "explicit_service_start_approval_future",
            "explicit_port_binding_approval_future",
            "explicit_network_approval_future",
            "explicit_orion_approval_future",
            "high_risk_runtime_approval_deferred",
        ],
        "risk_classifications": [
            "metadata_only_low_risk",
            "local_static_preview_low_risk",
            "api_mock_medium_risk",
            "websocket_medium_risk",
            "orion_handshake_medium_high_risk",
            "external_network_high_risk",
            "desktop_or_external_action_deferred_high_risk",
        ],
        "rollback_kill_switch_items": [
            "cancel_before_start",
            "abort_during_preflight",
            "stop_service_future_requirement",
            "release_port_future_requirement",
            "orion_disconnect_future_requirement",
            "audit_cancel_event_required",
            "manual_emergency_stop_visibility",
        ],
        "audit_event_items": [
            "proposal_created_event",
            "candidate_service_identity_event",
            "risk_classification_event",
            "permission_requirement_event",
            "port_policy_event",
            "dry_run_preview_event",
            "approval_decision_event",
            "cancel_or_reject_event",
        ],
        "user_approval_decisions": [
            "approve_preview_only",
            "reject_proposal",
            "request_more_information",
            "approve_future_dry_run",
            "approve_future_service_start",
            "defer_high_risk",
            "cancel_before_runtime",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_service_start",
        "runtime_port_binding",
        "runtime_network_probe",
        "runtime_permission_change",
        "runtime_action_dispatch",
        "runtime_action_execution",
        "runtime_tool_execution",
        "runtime_command_execution",
        "runtime_orion_handshake",
        "runtime_memory_write",
        "runtime_git_operation",
        "web_server_runtime",
        "api_server_runtime",
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
        "runtime_services_started",
        "runtime_ports_bound",
        "runtime_network_probes",
        "runtime_permissions_changed",
        "runtime_actions_dispatched",
        "runtime_actions_executed",
        "runtime_tools_executed",
        "runtime_commands_executed",
        "runtime_orion_handshakes",
        "runtime_memory_writes",
        "runtime_git_operations",
        "runtime_execution_features",
    ]

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

    def _blueprint_items(self, key: str) -> list[dict[str, Any]]:
        return [
            {
                "id": item,
                "proposal_review_only": True,
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
            "local_service_start_proposal_review_foundation_only": True,
            "service_start_proposal_review_blueprint_only": True,
            "service_start_candidate_inventory_blueprint_only": True,
            "service_start_preflight_requirement_blueprint_only": True,
            "port_binding_review_blueprint_only": True,
            "process_launch_boundary_blueprint_only": True,
            "permission_requirement_blueprint_only": True,
            "risk_classification_blueprint_only": True,
            "rollback_kill_switch_blueprint_only": True,
            "audit_event_blueprint_only": True,
            "user_approval_decision_blueprint_only": True,
            "foundation_only": True,
            "proposal_review_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            **self._runtime_false_flags(),
        }

    def summary(self) -> dict[str, Any]:
        counts = {f"{key}_count": len(value) for key, value in self.BLUEPRINTS.items()}
        return {
            "local_service_start_proposal_review_foundation_ready": True,
            "service_start_candidate_inventory_plan_ready": True,
            "service_start_preflight_requirement_plan_ready": True,
            "port_binding_review_plan_ready": True,
            "process_launch_boundary_plan_ready": True,
            "permission_requirement_plan_ready": True,
            "risk_classification_plan_ready": True,
            "rollback_kill_switch_plan_ready": True,
            "audit_event_plan_ready": True,
            "user_approval_decision_plan_ready": True,
            **counts,
            "total_local_service_start_proposal_blueprint_count": sum(counts.values()),
            **self._runtime_zero_counters(),
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": " ".join(str(target or "AURA local service start proposal review").split()),
            "principle": "Local service start proposals may be reviewed, but no service may be started or bound to a port.",
            "plan_types": self.PLAN_TYPES,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def service_start_candidate_inventory_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_start_candidate_inventory_plan", target)
        plan["service_start_candidates"] = self._blueprint_items("service_start_candidates")
        return plan

    def service_start_preflight_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_start_preflight_requirement_plan", target)
        plan["preflight_requirements"] = self._blueprint_items("preflight_requirements")
        return plan

    def port_binding_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("port_binding_review_plan", target)
        plan["port_binding_reviews"] = self._blueprint_items("port_binding_reviews")
        return plan

    def process_launch_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("process_launch_boundary_plan", target)
        plan["process_launch_boundaries"] = self._blueprint_items("process_launch_boundaries")
        return plan

    def permission_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_requirement_plan", target)
        plan["permission_requirements"] = self._blueprint_items("permission_requirements")
        return plan

    def risk_classification_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("risk_classification_plan", target)
        plan["risk_classifications"] = self._blueprint_items("risk_classifications")
        return plan

    def rollback_kill_switch_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("rollback_kill_switch_plan", target)
        plan["rollback_kill_switch_items"] = self._blueprint_items("rollback_kill_switch_items")
        return plan

    def audit_event_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("audit_event_plan", target)
        plan["audit_event_items"] = self._blueprint_items("audit_event_items")
        return plan

    def user_approval_decision_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("user_approval_decision_plan", target)
        plan["user_approval_decisions"] = self._blueprint_items("user_approval_decisions")
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
            "local_service_start_proposal_review_data_ready": True,
            "plan_types": self.PLAN_TYPES,
            "plan_type_count": len(self.PLAN_TYPES),
            **self.summary(),
            **self.safety_boundary(),
        }
