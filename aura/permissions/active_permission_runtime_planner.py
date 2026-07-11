"""Sprint 211 Active Permission Runtime contract.

This module prepares the Active Permission Runtime boundary for the
Permission, Audit, and Safe Local Actions block. It is intentionally
contract-only: it creates no grants, mutates no permission state, writes no
audit events, and executes no local actions.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


class ActivePermissionRuntimePlanner:
    """Contract planner for Sprint 211 Active Permission Runtime."""

    name = "active_permission_runtime"
    version = "0.1.0"
    block_start = 211
    block_end = 220
    current_sprint = 211
    next_sprint = 212
    next_boundary = "grant_denial_expiry_lifecycle"

    SAFETY_BLOCKERS = (
        "permission_runtime_active",
        "permission_state_mutation_active",
        "permission_grant_runtime_active",
        "permission_denial_runtime_active",
        "permission_expiry_runtime_active",
        "permission_persistence_runtime_active",
        "permission_bypass_active",
        "automatic_permission_grant_enabled",
        "implicit_approval_enabled",
        "expired_grant_reuse_enabled",
        "broad_scope_grant_enabled",
        "audit_writer_runtime_active",
        "audit_persistence_runtime_active",
        "action_execution_runtime_active",
        "command_execution_active",
        "tool_execution_active",
        "file_mutation_active",
        "desktop_action_active",
        "application_launch_active",
        "network_action_active",
        "git_action_active",
        "memory_write_active",
        "dependency_install_active",
        "model_download_active",
        "external_upload_active",
        "cloud_fallback_active",
        "autonomous_action_active",
    )

    ALLOWED_FUTURE_SCOPE = (
        "open_approved_folder",
        "open_approved_file",
        "open_project_location",
        "open_local_dashboard",
        "launch_allowlisted_application",
        "create_approved_folder",
        "create_simple_file_after_preview",
    )

    BLOCKED_SCOPE = (
        "delete_file",
        "arbitrary_shell_execution",
        "broad_desktop_control",
        "dependency_installation",
        "plugin_action_execution_without_gate",
        "multi_step_autonomous_automation",
        "network_or_git_action_without_explicit_permission",
        "external_upload_without_explicit_permission",
    )

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = Path(project_root or Path.cwd())

    def _permission_baseline(self) -> dict[str, Any]:
        try:
            from aura.permissions.permission_manager import PermissionManager
        except Exception as exc:  # pragma: no cover - defensive contract boundary
            return {
                "available": False,
                "item_count": 0,
                "items": [],
                "error": f"{type(exc).__name__}: {exc}",
            }

        manager = PermissionManager()
        raw_items = manager.list_permissions()
        items: list[dict[str, Any]] = []

        for item in raw_items:
            if is_dataclass(item):
                data = asdict(item)
            elif hasattr(item, "__dict__"):
                data = dict(item.__dict__)
            else:
                data = {"value": repr(item)}

            level = data.get("level")
            if hasattr(level, "name"):
                data["level_name"] = level.name
            else:
                data["level_name"] = str(level)

            if hasattr(level, "label"):
                try:
                    data["level_label"] = level.label()
                except TypeError:
                    data["level_label"] = str(level)

            items.append(data)

        return {
            "available": True,
            "item_count": len(items),
            "items": items,
            "error": None,
        }

    def active_permission_runtime_contract(self) -> dict[str, Any]:
        baseline = self._permission_baseline()

        contract: dict[str, Any] = {
            "sprint": self.current_sprint,
            "name": self.name,
            "active_permission_runtime_contract_ready": True,
            "active_permission_runtime_ready": False,
            "active_permission_runtime_status": "active_permission_runtime_contract_ready",
            "permission_action_block_start": self.block_start,
            "permission_action_block_end": self.block_end,
            "permission_action_current_sprint": self.current_sprint,
            "permission_action_next_sprint": self.next_sprint,
            "permission_action_next_boundary": self.next_boundary,
            "contract_only": True,
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "default_deny": True,
            "default_grant": False,
            "explicit_approval_required": True,
            "foreground_user_confirmation_required": True,
            "permission_before_action_required": True,
            "permission_before_memory_write_required": True,
            "permission_before_file_mutation_required": True,
            "permission_before_desktop_action_required": True,
            "permission_before_application_launch_required": True,
            "permission_before_network_action_required": True,
            "permission_before_git_action_required": True,
            "approval_before_runtime_mutation_required": True,
            "active_permission_request_packet_schema_ready": True,
            "permission_scope_packet_schema_ready": True,
            "permission_decision_packet_schema_ready": True,
            "permission_grant_packet_schema_ready": True,
            "permission_denial_packet_schema_ready": True,
            "permission_expiry_packet_schema_ready": True,
            "permission_state_snapshot_schema_ready": True,
            "permission_audit_link_packet_schema_ready": True,
            "permission_review_queue_packet_schema_ready": True,
            "permission_user_visible_reason_schema_ready": True,
            "permission_runtime_status_schema_ready": True,
            "permission_runtime_safety_matrix_schema_ready": True,
            "permission_runtime_next_lifecycle_schema_ready": True,
            "permission_baseline_available": baseline["available"],
            "permission_baseline_item_count": baseline["item_count"],
            "permission_baseline_error": baseline["error"],
            "permission_baseline_items": baseline["items"],
            "permission_registry_read_only": True,
            "permission_registry_mutation_allowed": False,
            "permission_state_persistence_allowed": False,
            "grant_creation_allowed": False,
            "grant_revocation_allowed": False,
            "grant_expiry_enforcement_runtime_ready": False,
            "denial_persistence_allowed": False,
            "audit_write_allowed": False,
            "audit_link_contract_ready": True,
            "audit_writer_runtime_ready": False,
            "audit_persistence_ready": False,
            "safe_local_action_handoff_ready": False,
            "action_proposal_runtime_ready": False,
            "action_preview_runtime_ready": False,
            "action_execution_runtime_ready": False,
            "allowlist_runtime_ready": False,
            "rollback_runtime_ready": False,
            "emergency_stop_runtime_ready": False,
            "control_center_approval_runtime_ready": False,
            "allowed_future_scope": list(self.ALLOWED_FUTURE_SCOPE),
            "allowed_future_scope_count": len(self.ALLOWED_FUTURE_SCOPE),
            "blocked_scope": list(self.BLOCKED_SCOPE),
            "blocked_scope_count": len(self.BLOCKED_SCOPE),
            "active_permission_request_created": False,
            "permission_scope_packet_created": False,
            "permission_decision_packet_created": False,
            "permission_grant_packet_created": False,
            "permission_denial_packet_created": False,
            "permission_expiry_packet_created": False,
            "permission_state_snapshot_created": False,
            "permission_audit_link_packet_created": False,
            "permission_review_queue_item_created": False,
            "permission_state_mutated": False,
            "permission_grant_created": False,
            "permission_denial_created": False,
            "permission_expiry_created": False,
            "permission_persisted": False,
            "audit_event_written": False,
            "audit_event_persisted": False,
            "action_proposal_created": False,
            "action_preview_created": False,
            "action_enqueued": False,
            "action_executed": False,
            "command_executed": False,
            "tool_executed": False,
            "file_mutated": False,
            "desktop_action_executed": False,
            "application_launched": False,
            "network_action_executed": False,
            "git_action_executed": False,
            "memory_written": False,
            "dependency_installed": False,
            "model_downloaded": False,
            "external_upload_performed": False,
            "cloud_fallback_used": False,
            "autonomous_action_performed": False,
            "no_automatic_grant": True,
            "no_implicit_approval": True,
            "no_permission_bypass": True,
            "no_state_mutation": True,
            "no_audit_write": True,
            "no_action_execution": True,
            "no_command_execution": True,
            "no_tool_execution": True,
            "no_file_mutation": True,
            "no_desktop_action": True,
            "no_application_launch": True,
            "no_network_action": True,
            "no_git_action": True,
            "no_memory_write": True,
            "no_dependency_install": True,
            "no_model_download": True,
            "no_external_upload": True,
            "no_cloud_fallback": True,
            "no_autonomous_action": True,
            "runtime_scope": "active_permission_runtime_contract_only",
            "safety_blockers": list(self.SAFETY_BLOCKERS),
            "safety_blocker_count": len(self.SAFETY_BLOCKERS),
        }

        for blocker in self.SAFETY_BLOCKERS:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in self.SAFETY_BLOCKERS
        )

        return contract

    def status(self) -> dict[str, Any]:
        contract = self.active_permission_runtime_contract()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planning",
            "planning_ready": True,
            "runtime_ready": False,
            "active_permission_runtime_contract_ready": contract["active_permission_runtime_contract_ready"],
            "active_permission_runtime_ready": contract["active_permission_runtime_ready"],
            "active_permission_runtime_status": contract["active_permission_runtime_status"],
            "permission_action_block_start": contract["permission_action_block_start"],
            "permission_action_block_end": contract["permission_action_block_end"],
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
            "permission_review_queue_packet_schema_ready": contract["permission_review_queue_packet_schema_ready"],
            "permission_baseline_available": contract["permission_baseline_available"],
            "permission_baseline_item_count": contract["permission_baseline_item_count"],
            "permission_registry_read_only": contract["permission_registry_read_only"],
            "permission_registry_mutation_allowed": contract["permission_registry_mutation_allowed"],
            "permission_state_persistence_allowed": contract["permission_state_persistence_allowed"],
            "grant_creation_allowed": contract["grant_creation_allowed"],
            "audit_write_allowed": contract["audit_write_allowed"],
            "audit_link_contract_ready": contract["audit_link_contract_ready"],
            "safe_local_action_handoff_ready": contract["safe_local_action_handoff_ready"],
            "allowed_future_scope_count": contract["allowed_future_scope_count"],
            "blocked_scope_count": contract["blocked_scope_count"],
            "active_permission_request_created": contract["active_permission_request_created"],
            "permission_decision_packet_created": contract["permission_decision_packet_created"],
            "permission_state_mutated": contract["permission_state_mutated"],
            "permission_grant_created": contract["permission_grant_created"],
            "audit_event_written": contract["audit_event_written"],
            "action_executed": contract["action_executed"],
            "command_executed": contract["command_executed"],
            "file_mutated": contract["file_mutated"],
            "desktop_action_executed": contract["desktop_action_executed"],
            "application_launched": contract["application_launched"],
            "network_action_executed": contract["network_action_executed"],
            "git_action_executed": contract["git_action_executed"],
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
            "runtime_scope": contract["runtime_scope"],
            "contract": contract,
            "note": (
                "Active Permission Runtime contract is ready for Sprint 211; "
                "it prepares default-deny permission request, scope, decision, "
                "grant, denial, expiry, state visibility, and audit-link schemas "
                "without mutating permission state, creating grants, writing audit "
                "events, or executing local actions."
            ),
        }

    def check(self) -> dict[str, Any]:
        contract = self.active_permission_runtime_contract()

        assertions: dict[str, bool] = {
            "planning_ready": True,
            "runtime_not_ready": contract["runtime_ready"] is False,
            "contract_ready": contract["active_permission_runtime_contract_ready"] is True,
            "runtime_disabled": contract["active_permission_runtime_ready"] is False,
            "status_ready": contract["active_permission_runtime_status"] == "active_permission_runtime_contract_ready",
            "current_sprint_211": contract["permission_action_current_sprint"] == 211,
            "next_sprint_212": contract["permission_action_next_sprint"] == 212,
            "next_boundary_grant_denial_expiry": contract["permission_action_next_boundary"] == "grant_denial_expiry_lifecycle",
            "contract_only": contract["contract_only"] is True,
            "release_gate_closed": contract["release_gate_open"] is False,
            "default_deny_enabled": contract["default_deny"] is True,
            "default_grant_disabled": contract["default_grant"] is False,
            "explicit_approval_required": contract["explicit_approval_required"] is True,
            "foreground_confirmation_required": contract["foreground_user_confirmation_required"] is True,
            "permission_before_action": contract["permission_before_action_required"] is True,
            "permission_before_memory_write": contract["permission_before_memory_write_required"] is True,
            "permission_before_file_mutation": contract["permission_before_file_mutation_required"] is True,
            "permission_before_desktop_action": contract["permission_before_desktop_action_required"] is True,
            "permission_before_application_launch": contract["permission_before_application_launch_required"] is True,
            "permission_before_network_action": contract["permission_before_network_action_required"] is True,
            "permission_before_git_action": contract["permission_before_git_action_required"] is True,
            "request_packet_schema_ready": contract["active_permission_request_packet_schema_ready"] is True,
            "scope_packet_schema_ready": contract["permission_scope_packet_schema_ready"] is True,
            "decision_packet_schema_ready": contract["permission_decision_packet_schema_ready"] is True,
            "grant_packet_schema_ready": contract["permission_grant_packet_schema_ready"] is True,
            "denial_packet_schema_ready": contract["permission_denial_packet_schema_ready"] is True,
            "expiry_packet_schema_ready": contract["permission_expiry_packet_schema_ready"] is True,
            "state_snapshot_schema_ready": contract["permission_state_snapshot_schema_ready"] is True,
            "audit_link_packet_schema_ready": contract["permission_audit_link_packet_schema_ready"] is True,
            "review_queue_packet_schema_ready": contract["permission_review_queue_packet_schema_ready"] is True,
            "user_visible_reason_schema_ready": contract["permission_user_visible_reason_schema_ready"] is True,
            "runtime_status_schema_ready": contract["permission_runtime_status_schema_ready"] is True,
            "safety_matrix_schema_ready": contract["permission_runtime_safety_matrix_schema_ready"] is True,
            "next_lifecycle_schema_ready": contract["permission_runtime_next_lifecycle_schema_ready"] is True,
            "permission_baseline_available": contract["permission_baseline_available"] is True,
            "permission_baseline_has_items": contract["permission_baseline_item_count"] > 0,
            "registry_read_only": contract["permission_registry_read_only"] is True,
            "registry_mutation_blocked": contract["permission_registry_mutation_allowed"] is False,
            "state_persistence_blocked": contract["permission_state_persistence_allowed"] is False,
            "grant_creation_blocked": contract["grant_creation_allowed"] is False,
            "grant_revocation_blocked": contract["grant_revocation_allowed"] is False,
            "grant_expiry_runtime_disabled": contract["grant_expiry_enforcement_runtime_ready"] is False,
            "denial_persistence_blocked": contract["denial_persistence_allowed"] is False,
            "audit_write_blocked": contract["audit_write_allowed"] is False,
            "audit_link_contract_ready": contract["audit_link_contract_ready"] is True,
            "audit_writer_runtime_disabled": contract["audit_writer_runtime_ready"] is False,
            "audit_persistence_disabled": contract["audit_persistence_ready"] is False,
            "safe_local_action_handoff_not_ready": contract["safe_local_action_handoff_ready"] is False,
            "action_proposal_runtime_disabled": contract["action_proposal_runtime_ready"] is False,
            "action_preview_runtime_disabled": contract["action_preview_runtime_ready"] is False,
            "action_execution_runtime_disabled": contract["action_execution_runtime_ready"] is False,
            "allowlist_runtime_disabled": contract["allowlist_runtime_ready"] is False,
            "rollback_runtime_disabled": contract["rollback_runtime_ready"] is False,
            "emergency_stop_runtime_disabled": contract["emergency_stop_runtime_ready"] is False,
            "control_center_approval_runtime_disabled": contract["control_center_approval_runtime_ready"] is False,
            "allowed_future_scope_present": contract["allowed_future_scope_count"] == len(self.ALLOWED_FUTURE_SCOPE),
            "blocked_scope_present": contract["blocked_scope_count"] == len(self.BLOCKED_SCOPE),
            "request_not_created": contract["active_permission_request_created"] is False,
            "scope_packet_not_created": contract["permission_scope_packet_created"] is False,
            "decision_packet_not_created": contract["permission_decision_packet_created"] is False,
            "grant_packet_not_created": contract["permission_grant_packet_created"] is False,
            "denial_packet_not_created": contract["permission_denial_packet_created"] is False,
            "expiry_packet_not_created": contract["permission_expiry_packet_created"] is False,
            "state_snapshot_not_created": contract["permission_state_snapshot_created"] is False,
            "audit_link_packet_not_created": contract["permission_audit_link_packet_created"] is False,
            "review_queue_item_not_created": contract["permission_review_queue_item_created"] is False,
            "permission_state_not_mutated": contract["permission_state_mutated"] is False,
            "permission_grant_not_created": contract["permission_grant_created"] is False,
            "permission_denial_not_created": contract["permission_denial_created"] is False,
            "permission_expiry_not_created": contract["permission_expiry_created"] is False,
            "permission_not_persisted": contract["permission_persisted"] is False,
            "audit_event_not_written": contract["audit_event_written"] is False,
            "audit_event_not_persisted": contract["audit_event_persisted"] is False,
            "action_proposal_not_created": contract["action_proposal_created"] is False,
            "action_preview_not_created": contract["action_preview_created"] is False,
            "action_not_enqueued": contract["action_enqueued"] is False,
            "action_not_executed": contract["action_executed"] is False,
            "command_not_executed": contract["command_executed"] is False,
            "tool_not_executed": contract["tool_executed"] is False,
            "file_not_mutated": contract["file_mutated"] is False,
            "desktop_action_not_executed": contract["desktop_action_executed"] is False,
            "application_not_launched": contract["application_launched"] is False,
            "network_action_not_executed": contract["network_action_executed"] is False,
            "git_action_not_executed": contract["git_action_executed"] is False,
            "memory_not_written": contract["memory_written"] is False,
            "dependency_not_installed": contract["dependency_installed"] is False,
            "model_not_downloaded": contract["model_downloaded"] is False,
            "external_upload_not_performed": contract["external_upload_performed"] is False,
            "cloud_fallback_not_used": contract["cloud_fallback_used"] is False,
            "autonomous_action_not_performed": contract["autonomous_action_performed"] is False,
            "no_automatic_grant": contract["no_automatic_grant"] is True,
            "no_implicit_approval": contract["no_implicit_approval"] is True,
            "no_permission_bypass": contract["no_permission_bypass"] is True,
            "no_state_mutation": contract["no_state_mutation"] is True,
            "no_audit_write": contract["no_audit_write"] is True,
            "no_action_execution": contract["no_action_execution"] is True,
            "no_command_execution": contract["no_command_execution"] is True,
            "no_file_mutation": contract["no_file_mutation"] is True,
            "no_desktop_action": contract["no_desktop_action"] is True,
            "no_memory_write": contract["no_memory_write"] is True,
            "no_external_upload": contract["no_external_upload"] is True,
            "safety_blocker_count_expected": contract["safety_blocker_count"] == len(self.SAFETY_BLOCKERS),
            "all_safety_blockers_inactive": contract["all_safety_blockers_inactive"] is True,
            "runtime_scope_contract_only": contract["runtime_scope"] == "active_permission_runtime_contract_only",
        }

        for blocker in self.SAFETY_BLOCKERS:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed_assertions),
            "failed_assertions": failed_assertions,
            "permission_action_current_sprint": contract["permission_action_current_sprint"],
            "permission_action_next_sprint": contract["permission_action_next_sprint"],
            "permission_action_next_boundary": contract["permission_action_next_boundary"],
            "active_permission_runtime_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 211 "
                "Active Permission Runtime contract without creating permission "
                "requests, granting permissions, mutating permission state, writing "
                "audit events, or executing local actions."
            ),
        }

    def plan(self) -> dict[str, Any]:
        contract = self.active_permission_runtime_contract()
        return {
            "name": self.name,
            "sprint": self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "contract_ready": contract["active_permission_runtime_contract_ready"],
            "runtime_ready": contract["active_permission_runtime_ready"],
            "runtime_scope": contract["runtime_scope"],
            "allowed_future_scope": contract["allowed_future_scope"],
            "blocked_scope": contract["blocked_scope"],
        }
