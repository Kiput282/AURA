"""Sprint 211 Active Permission Runtime alpha surface."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.permissions.active_permission_runtime_planner import (
    ActivePermissionRuntimePlanner,
)


class ActivePermissionRuntimeAlphaManager:
    """Read-only alpha status for the Active Permission Runtime contract."""

    name = "active_permission_runtime_alpha"
    version = "0.1.0"

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = Path(project_root or Path.cwd())
        self.planner = ActivePermissionRuntimePlanner(project_root=self.project_root)

    def status(self) -> dict[str, Any]:
        status = self.planner.status()
        check = self.planner.check()
        contract = status["contract"]

        return {
            "name": self.name,
            "version": self.version,
            "status": "online",
            "runtime_ready": False,
            "planning_ready": True,
            "active_permission_runtime_alpha_ready": True,
            "sprint_211_active_permission_runtime_contract_ready": contract["active_permission_runtime_contract_ready"],
            "active_permission_runtime_ready": contract["active_permission_runtime_ready"],
            "active_permission_runtime_status": contract["active_permission_runtime_status"],
            "permission_action_current_sprint": contract["permission_action_current_sprint"],
            "permission_action_next_sprint": contract["permission_action_next_sprint"],
            "permission_action_next_boundary": contract["permission_action_next_boundary"],
            "default_deny": contract["default_deny"],
            "explicit_approval_required": contract["explicit_approval_required"],
            "foreground_user_confirmation_required": contract["foreground_user_confirmation_required"],
            "permission_before_action_required": contract["permission_before_action_required"],
            "active_permission_request_packet_schema_ready": contract["active_permission_request_packet_schema_ready"],
            "permission_scope_packet_schema_ready": contract["permission_scope_packet_schema_ready"],
            "permission_decision_packet_schema_ready": contract["permission_decision_packet_schema_ready"],
            "permission_grant_packet_schema_ready": contract["permission_grant_packet_schema_ready"],
            "permission_denial_packet_schema_ready": contract["permission_denial_packet_schema_ready"],
            "permission_expiry_packet_schema_ready": contract["permission_expiry_packet_schema_ready"],
            "permission_state_snapshot_schema_ready": contract["permission_state_snapshot_schema_ready"],
            "permission_audit_link_packet_schema_ready": contract["permission_audit_link_packet_schema_ready"],
            "permission_baseline_available": contract["permission_baseline_available"],
            "permission_baseline_item_count": contract["permission_baseline_item_count"],
            "permission_registry_read_only": contract["permission_registry_read_only"],
            "permission_registry_mutation_allowed": contract["permission_registry_mutation_allowed"],
            "grant_creation_allowed": contract["grant_creation_allowed"],
            "audit_write_allowed": contract["audit_write_allowed"],
            "safe_local_action_handoff_ready": contract["safe_local_action_handoff_ready"],
            "allowed_future_scope_count": contract["allowed_future_scope_count"],
            "blocked_scope_count": contract["blocked_scope_count"],
            "active_permission_request_created": contract["active_permission_request_created"],
            "permission_state_mutated": contract["permission_state_mutated"],
            "permission_grant_created": contract["permission_grant_created"],
            "audit_event_written": contract["audit_event_written"],
            "action_executed": contract["action_executed"],
            "command_executed": contract["command_executed"],
            "file_mutated": contract["file_mutated"],
            "desktop_action_executed": contract["desktop_action_executed"],
            "application_launched": contract["application_launched"],
            "memory_written": contract["memory_written"],
            "external_upload_performed": contract["external_upload_performed"],
            "no_automatic_grant": contract["no_automatic_grant"],
            "no_implicit_approval": contract["no_implicit_approval"],
            "no_permission_bypass": contract["no_permission_bypass"],
            "no_state_mutation": contract["no_state_mutation"],
            "no_action_execution": contract["no_action_execution"],
            "no_command_execution": contract["no_command_execution"],
            "no_file_mutation": contract["no_file_mutation"],
            "no_desktop_action": contract["no_desktop_action"],
            "no_memory_write": contract["no_memory_write"],
            "no_external_upload": contract["no_external_upload"],
            "safety_blocker_count": contract["safety_blocker_count"],
            "all_safety_blockers_inactive": contract["all_safety_blockers_inactive"],
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check["failed_assertion_count"],
            "failed_assertions": check["failed_assertions"],
            "runtime_scope": contract["runtime_scope"],
            "sections": 1,
            "note": (
                "Active Permission Runtime Alpha is online for Sprint 211. "
                "It exposes the default-deny permission runtime contract without "
                "granting permissions, mutating state, writing audit events, or "
                "executing local actions."
            ),
        }
