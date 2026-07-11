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

# Sprint 212 extension: Grant, Denial, and Expiry Lifecycle.
#
# This intentionally wraps the Sprint 211 planner instead of enabling a real
# permission runtime. It prepares lifecycle schemas and safety visibility only.
if not getattr(ActivePermissionRuntimePlanner, "_s212_extension_installed", False):
    _S211_STATUS = ActivePermissionRuntimePlanner.status
    _S211_CHECK = ActivePermissionRuntimePlanner.check
    _S211_PLAN = ActivePermissionRuntimePlanner.plan

    def _s212_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.SAFETY_BLOCKERS)
        extra = (
            "grant_lifecycle_runtime_active",
            "grant_packet_creation_active",
            "grant_state_mutation_active",
            "grant_persistence_active",
            "denial_lifecycle_runtime_active",
            "denial_packet_creation_active",
            "denial_persistence_active",
            "expiry_lifecycle_runtime_active",
            "expiry_evaluation_runtime_active",
            "expiry_state_mutation_active",
            "expired_grant_reuse_active",
            "automatic_grant_renewal_active",
            "grant_without_request_active",
            "grant_without_explicit_approval_active",
            "grant_without_scope_active",
            "grant_without_expiry_active",
            "grant_without_audit_link_active",
            "broad_permission_grant_active",
            "permission_lifecycle_bypass_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s212_grant_denial_expiry_lifecycle_contract(self) -> dict[str, Any]:
        s211 = self.active_permission_runtime_contract()
        blockers = _s212_safety_blockers(self)

        contract: dict[str, Any] = dict(s211)
        contract.update(
            {
                "grant_denial_expiry_lifecycle_contract_ready": True,
                "grant_denial_expiry_lifecycle_runtime_ready": False,
                "grant_denial_expiry_lifecycle_status": "grant_denial_expiry_lifecycle_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 212,
                "permission_action_next_sprint": 213,
                "permission_action_next_boundary": "runtime_audit_writer",
                "previous_active_permission_runtime_contract_ready": s211[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "explicit_approval_required": True,
                "foreground_user_confirmation_required": True,
                "approval_before_grant_required": True,
                "request_before_grant_required": True,
                "scope_before_grant_required": True,
                "expiry_before_grant_required": True,
                "denial_reason_required": True,
                "audit_link_before_persistence_required": True,
                "grant_request_packet_schema_ready": True,
                "grant_scope_packet_schema_ready": True,
                "grant_decision_packet_schema_ready": True,
                "grant_packet_schema_ready": True,
                "grant_expiry_packet_schema_ready": True,
                "grant_revocation_packet_schema_ready": True,
                "denial_packet_schema_ready": True,
                "denial_reason_packet_schema_ready": True,
                "denial_review_packet_schema_ready": True,
                "expiry_check_packet_schema_ready": True,
                "expiry_event_packet_schema_ready": True,
                "lifecycle_state_snapshot_schema_ready": True,
                "lifecycle_audit_link_packet_schema_ready": True,
                "lifecycle_review_queue_packet_schema_ready": True,
                "lifecycle_user_visible_reason_schema_ready": True,
                "lifecycle_runtime_status_schema_ready": True,
                "lifecycle_safety_matrix_schema_ready": True,
                "lifecycle_next_audit_writer_schema_ready": True,
                "grant_lifecycle_runtime_ready": False,
                "grant_packet_creation_allowed": False,
                "grant_state_mutation_allowed": False,
                "grant_persistence_allowed": False,
                "grant_revocation_allowed": False,
                "denial_lifecycle_runtime_ready": False,
                "denial_packet_creation_allowed": False,
                "denial_persistence_allowed": False,
                "expiry_lifecycle_runtime_ready": False,
                "expiry_evaluation_runtime_ready": False,
                "expiry_state_mutation_allowed": False,
                "expired_grant_reuse_allowed": False,
                "automatic_grant_renewal_allowed": False,
                "broad_scope_grant_allowed": False,
                "permission_lifecycle_bypass_allowed": False,
                "audit_write_allowed": False,
                "audit_writer_runtime_ready": False,
                "audit_persistence_ready": False,
                "safe_local_action_handoff_ready": False,
                "action_proposal_runtime_ready": False,
                "action_preview_runtime_ready": False,
                "action_execution_runtime_ready": False,
                "control_center_approval_runtime_ready": False,
                "grant_request_packet_created": False,
                "grant_scope_packet_created": False,
                "grant_decision_packet_created": False,
                "grant_packet_created": False,
                "grant_expiry_packet_created": False,
                "grant_revocation_packet_created": False,
                "denial_packet_created": False,
                "denial_reason_packet_created": False,
                "denial_review_packet_created": False,
                "expiry_check_packet_created": False,
                "expiry_event_packet_created": False,
                "lifecycle_state_snapshot_created": False,
                "lifecycle_audit_link_packet_created": False,
                "lifecycle_review_queue_item_created": False,
                "grant_lifecycle_runtime_active": False,
                "grant_packet_creation_active": False,
                "grant_state_mutation_active": False,
                "grant_persistence_active": False,
                "denial_lifecycle_runtime_active": False,
                "denial_packet_creation_active": False,
                "denial_persistence_active": False,
                "expiry_lifecycle_runtime_active": False,
                "expiry_evaluation_runtime_active": False,
                "expiry_state_mutation_active": False,
                "expired_grant_reuse_active": False,
                "automatic_grant_renewal_active": False,
                "grant_without_request_active": False,
                "grant_without_explicit_approval_active": False,
                "grant_without_scope_active": False,
                "grant_without_expiry_active": False,
                "grant_without_audit_link_active": False,
                "broad_permission_grant_active": False,
                "permission_lifecycle_bypass_active": False,
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
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_denial_persistence": True,
                "no_expiry_mutation": True,
                "no_expired_grant_reuse": True,
                "no_automatic_grant_renewal": True,
                "no_broad_scope_grant": True,
                "no_grant_without_request": True,
                "no_grant_without_explicit_approval": True,
                "no_grant_without_scope": True,
                "no_grant_without_expiry": True,
                "no_grant_without_audit_link": True,
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
                "runtime_scope": "grant_denial_expiry_lifecycle_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s212_status(self) -> dict[str, Any]:
        status = _S211_STATUS(self)
        contract = self.grant_denial_expiry_lifecycle_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "grant_denial_expiry_lifecycle_contract_ready": contract[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "grant_denial_expiry_lifecycle_runtime_ready": contract[
                    "grant_denial_expiry_lifecycle_runtime_ready"
                ],
                "grant_denial_expiry_lifecycle_status": contract[
                    "grant_denial_expiry_lifecycle_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "default_deny": contract["default_deny"],
                "default_grant": contract["default_grant"],
                "explicit_approval_required": contract["explicit_approval_required"],
                "approval_before_grant_required": contract[
                    "approval_before_grant_required"
                ],
                "request_before_grant_required": contract[
                    "request_before_grant_required"
                ],
                "scope_before_grant_required": contract[
                    "scope_before_grant_required"
                ],
                "expiry_before_grant_required": contract[
                    "expiry_before_grant_required"
                ],
                "denial_reason_required": contract["denial_reason_required"],
                "grant_request_packet_schema_ready": contract[
                    "grant_request_packet_schema_ready"
                ],
                "grant_scope_packet_schema_ready": contract[
                    "grant_scope_packet_schema_ready"
                ],
                "grant_decision_packet_schema_ready": contract[
                    "grant_decision_packet_schema_ready"
                ],
                "grant_packet_schema_ready": contract["grant_packet_schema_ready"],
                "grant_expiry_packet_schema_ready": contract[
                    "grant_expiry_packet_schema_ready"
                ],
                "denial_packet_schema_ready": contract["denial_packet_schema_ready"],
                "denial_reason_packet_schema_ready": contract[
                    "denial_reason_packet_schema_ready"
                ],
                "expiry_check_packet_schema_ready": contract[
                    "expiry_check_packet_schema_ready"
                ],
                "expiry_event_packet_schema_ready": contract[
                    "expiry_event_packet_schema_ready"
                ],
                "lifecycle_state_snapshot_schema_ready": contract[
                    "lifecycle_state_snapshot_schema_ready"
                ],
                "lifecycle_audit_link_packet_schema_ready": contract[
                    "lifecycle_audit_link_packet_schema_ready"
                ],
                "grant_packet_creation_allowed": contract[
                    "grant_packet_creation_allowed"
                ],
                "grant_state_mutation_allowed": contract[
                    "grant_state_mutation_allowed"
                ],
                "grant_persistence_allowed": contract["grant_persistence_allowed"],
                "denial_packet_creation_allowed": contract[
                    "denial_packet_creation_allowed"
                ],
                "expiry_evaluation_runtime_ready": contract[
                    "expiry_evaluation_runtime_ready"
                ],
                "expired_grant_reuse_allowed": contract[
                    "expired_grant_reuse_allowed"
                ],
                "automatic_grant_renewal_allowed": contract[
                    "automatic_grant_renewal_allowed"
                ],
                "permission_lifecycle_bypass_allowed": contract[
                    "permission_lifecycle_bypass_allowed"
                ],
                "grant_request_packet_created": contract[
                    "grant_request_packet_created"
                ],
                "grant_packet_created": contract["grant_packet_created"],
                "denial_packet_created": contract["denial_packet_created"],
                "expiry_event_packet_created": contract[
                    "expiry_event_packet_created"
                ],
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
                "no_grant_creation": contract["no_grant_creation"],
                "no_grant_persistence": contract["no_grant_persistence"],
                "no_expired_grant_reuse": contract["no_expired_grant_reuse"],
                "no_automatic_grant_renewal": contract[
                    "no_automatic_grant_renewal"
                ],
                "no_grant_without_request": contract["no_grant_without_request"],
                "no_grant_without_explicit_approval": contract[
                    "no_grant_without_explicit_approval"
                ],
                "no_grant_without_scope": contract["no_grant_without_scope"],
                "no_grant_without_expiry": contract["no_grant_without_expiry"],
                "no_grant_without_audit_link": contract[
                    "no_grant_without_audit_link"
                ],
                "no_audit_write": contract["no_audit_write"],
                "no_action_execution": contract["no_action_execution"],
                "no_command_execution": contract["no_command_execution"],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_memory_write": contract["no_memory_write"],
                "no_external_upload": contract["no_external_upload"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "grant_denial_expiry_lifecycle_contract": contract,
                "contract": contract,
                "note": (
                    "Grant, Denial, and Expiry Lifecycle contract is ready for "
                    "Sprint 212; it prepares grant, denial, and expiry schemas "
                    "without creating grant packets, mutating permission state, "
                    "persisting permissions, writing audit events, or executing "
                    "local actions."
                ),
            }
        )
        return status

    def _s212_check(self) -> dict[str, Any]:
        s211 = _S211_CHECK(self)
        contract = self.grant_denial_expiry_lifecycle_contract()

        assertions: dict[str, bool] = {
            "sprint_211_check_still_clean": s211["failed_assertion_count"] == 0,
            "contract_ready": contract[
                "grant_denial_expiry_lifecycle_contract_ready"
            ]
            is True,
            "runtime_disabled": contract[
                "grant_denial_expiry_lifecycle_runtime_ready"
            ]
            is False,
            "status_ready": contract["grant_denial_expiry_lifecycle_status"]
            == "grant_denial_expiry_lifecycle_contract_ready",
            "current_sprint_212": contract["permission_action_current_sprint"] == 212,
            "next_sprint_213": contract["permission_action_next_sprint"] == 213,
            "next_boundary_runtime_audit_writer": contract[
                "permission_action_next_boundary"
            ]
            == "runtime_audit_writer",
            "previous_contract_chain_complete": contract[
                "previous_contract_chain_complete"
            ]
            is True,
            "contract_only": contract["contract_only"] is True,
            "runtime_not_ready": contract["runtime_ready"] is False,
            "runtime_activation_blocked": contract["runtime_activation_allowed"]
            is False,
            "release_gate_closed": contract["release_gate_open"] is False,
            "default_deny_enabled": contract["default_deny"] is True,
            "default_grant_disabled": contract["default_grant"] is False,
            "explicit_approval_required": contract["explicit_approval_required"]
            is True,
            "approval_before_grant_required": contract[
                "approval_before_grant_required"
            ]
            is True,
            "request_before_grant_required": contract[
                "request_before_grant_required"
            ]
            is True,
            "scope_before_grant_required": contract[
                "scope_before_grant_required"
            ]
            is True,
            "expiry_before_grant_required": contract[
                "expiry_before_grant_required"
            ]
            is True,
            "denial_reason_required": contract["denial_reason_required"] is True,
            "audit_link_before_persistence_required": contract[
                "audit_link_before_persistence_required"
            ]
            is True,
            "grant_request_schema_ready": contract[
                "grant_request_packet_schema_ready"
            ]
            is True,
            "grant_scope_schema_ready": contract[
                "grant_scope_packet_schema_ready"
            ]
            is True,
            "grant_decision_schema_ready": contract[
                "grant_decision_packet_schema_ready"
            ]
            is True,
            "grant_packet_schema_ready": contract["grant_packet_schema_ready"]
            is True,
            "grant_expiry_schema_ready": contract[
                "grant_expiry_packet_schema_ready"
            ]
            is True,
            "grant_revocation_schema_ready": contract[
                "grant_revocation_packet_schema_ready"
            ]
            is True,
            "denial_packet_schema_ready": contract["denial_packet_schema_ready"]
            is True,
            "denial_reason_schema_ready": contract[
                "denial_reason_packet_schema_ready"
            ]
            is True,
            "expiry_check_schema_ready": contract[
                "expiry_check_packet_schema_ready"
            ]
            is True,
            "expiry_event_schema_ready": contract[
                "expiry_event_packet_schema_ready"
            ]
            is True,
            "lifecycle_state_snapshot_schema_ready": contract[
                "lifecycle_state_snapshot_schema_ready"
            ]
            is True,
            "lifecycle_audit_link_schema_ready": contract[
                "lifecycle_audit_link_packet_schema_ready"
            ]
            is True,
            "lifecycle_review_queue_schema_ready": contract[
                "lifecycle_review_queue_packet_schema_ready"
            ]
            is True,
            "grant_lifecycle_runtime_disabled": contract[
                "grant_lifecycle_runtime_ready"
            ]
            is False,
            "grant_packet_creation_blocked": contract[
                "grant_packet_creation_allowed"
            ]
            is False,
            "grant_state_mutation_blocked": contract[
                "grant_state_mutation_allowed"
            ]
            is False,
            "grant_persistence_blocked": contract["grant_persistence_allowed"]
            is False,
            "denial_packet_creation_blocked": contract[
                "denial_packet_creation_allowed"
            ]
            is False,
            "denial_persistence_blocked": contract["denial_persistence_allowed"]
            is False,
            "expiry_evaluation_runtime_disabled": contract[
                "expiry_evaluation_runtime_ready"
            ]
            is False,
            "expired_grant_reuse_blocked": contract[
                "expired_grant_reuse_allowed"
            ]
            is False,
            "automatic_grant_renewal_blocked": contract[
                "automatic_grant_renewal_allowed"
            ]
            is False,
            "broad_scope_grant_blocked": contract["broad_scope_grant_allowed"]
            is False,
            "permission_lifecycle_bypass_blocked": contract[
                "permission_lifecycle_bypass_allowed"
            ]
            is False,
            "audit_write_blocked": contract["audit_write_allowed"] is False,
            "safe_action_handoff_disabled": contract[
                "safe_local_action_handoff_ready"
            ]
            is False,
            "action_execution_disabled": contract[
                "action_execution_runtime_ready"
            ]
            is False,
            "grant_request_not_created": contract[
                "grant_request_packet_created"
            ]
            is False,
            "grant_packet_not_created": contract["grant_packet_created"] is False,
            "denial_packet_not_created": contract["denial_packet_created"]
            is False,
            "expiry_event_not_created": contract["expiry_event_packet_created"]
            is False,
            "lifecycle_snapshot_not_created": contract[
                "lifecycle_state_snapshot_created"
            ]
            is False,
            "lifecycle_audit_link_not_created": contract[
                "lifecycle_audit_link_packet_created"
            ]
            is False,
            "permission_state_not_mutated": contract["permission_state_mutated"]
            is False,
            "permission_grant_not_created": contract["permission_grant_created"]
            is False,
            "permission_denial_not_created": contract["permission_denial_created"]
            is False,
            "permission_expiry_not_created": contract["permission_expiry_created"]
            is False,
            "permission_not_persisted": contract["permission_persisted"]
            is False,
            "audit_event_not_written": contract["audit_event_written"] is False,
            "action_not_executed": contract["action_executed"] is False,
            "command_not_executed": contract["command_executed"] is False,
            "tool_not_executed": contract["tool_executed"] is False,
            "file_not_mutated": contract["file_mutated"] is False,
            "desktop_action_not_executed": contract[
                "desktop_action_executed"
            ]
            is False,
            "application_not_launched": contract["application_launched"]
            is False,
            "network_action_not_executed": contract["network_action_executed"]
            is False,
            "git_action_not_executed": contract["git_action_executed"] is False,
            "memory_not_written": contract["memory_written"] is False,
            "external_upload_not_performed": contract[
                "external_upload_performed"
            ]
            is False,
            "cloud_fallback_not_used": contract["cloud_fallback_used"] is False,
            "autonomous_action_not_performed": contract[
                "autonomous_action_performed"
            ]
            is False,
            "no_automatic_grant": contract["no_automatic_grant"] is True,
            "no_grant_creation": contract["no_grant_creation"] is True,
            "no_grant_persistence": contract["no_grant_persistence"] is True,
            "no_expired_grant_reuse": contract["no_expired_grant_reuse"]
            is True,
            "no_automatic_grant_renewal": contract[
                "no_automatic_grant_renewal"
            ]
            is True,
            "no_grant_without_request": contract["no_grant_without_request"]
            is True,
            "no_grant_without_explicit_approval": contract[
                "no_grant_without_explicit_approval"
            ]
            is True,
            "no_grant_without_scope": contract["no_grant_without_scope"] is True,
            "no_grant_without_expiry": contract["no_grant_without_expiry"]
            is True,
            "no_grant_without_audit_link": contract[
                "no_grant_without_audit_link"
            ]
            is True,
            "no_audit_write": contract["no_audit_write"] is True,
            "no_action_execution": contract["no_action_execution"] is True,
            "no_command_execution": contract["no_command_execution"] is True,
            "no_tool_execution": contract["no_tool_execution"] is True,
            "no_file_mutation": contract["no_file_mutation"] is True,
            "no_desktop_action": contract["no_desktop_action"] is True,
            "no_memory_write": contract["no_memory_write"] is True,
            "no_external_upload": contract["no_external_upload"] is True,
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "all_safety_blockers_inactive": contract[
                "all_safety_blockers_inactive"
            ]
            is True,
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "grant_denial_expiry_lifecycle_contract_only",
        }

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s211_failed = [
            f"sprint_211::{name}" for name in s211.get("failed_assertions", [])
        ]
        all_failed = s211_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s211["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 212 "
                "Grant, Denial, and Expiry Lifecycle contract without creating "
                "grants, denials, expiry events, mutating permission state, "
                "persisting permissions, writing audit events, or executing "
                "local actions."
            ),
        }

    def _s212_plan(self) -> dict[str, Any]:
        contract = self.grant_denial_expiry_lifecycle_contract()
        return {
            "name": self.name,
            "sprint": 212,
            "next_sprint": 213,
            "next_boundary": "runtime_audit_writer",
            "contract_ready": contract[
                "grant_denial_expiry_lifecycle_contract_ready"
            ],
            "runtime_ready": contract[
                "grant_denial_expiry_lifecycle_runtime_ready"
            ],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "grant_request": contract["grant_request_packet_schema_ready"],
                "grant_scope": contract["grant_scope_packet_schema_ready"],
                "grant_decision": contract["grant_decision_packet_schema_ready"],
                "grant": contract["grant_packet_schema_ready"],
                "grant_expiry": contract["grant_expiry_packet_schema_ready"],
                "denial": contract["denial_packet_schema_ready"],
                "expiry_check": contract["expiry_check_packet_schema_ready"],
                "expiry_event": contract["expiry_event_packet_schema_ready"],
                "audit_link": contract["lifecycle_audit_link_packet_schema_ready"],
            },
            "blocked_runtime": {
                "grant_creation": contract["grant_packet_creation_allowed"],
                "grant_state_mutation": contract["grant_state_mutation_allowed"],
                "grant_persistence": contract["grant_persistence_allowed"],
                "audit_write": contract["audit_write_allowed"],
                "action_execution": contract["action_execution_runtime_ready"],
            },
        }

    ActivePermissionRuntimePlanner.grant_denial_expiry_lifecycle_contract = (
        _s212_grant_denial_expiry_lifecycle_contract
    )
    ActivePermissionRuntimePlanner.status = _s212_status
    ActivePermissionRuntimePlanner.check = _s212_check
    ActivePermissionRuntimePlanner.plan = _s212_plan
    ActivePermissionRuntimePlanner._s212_extension_installed = True

# Sprint 213 extension: Runtime Audit Writer.
#
# This intentionally wraps the Sprint 212 planner instead of enabling a real
# audit writer. It prepares audit-writer schemas and safety visibility only.
if not getattr(ActivePermissionRuntimePlanner, "_s213_extension_installed", False):
    _S212_STATUS = ActivePermissionRuntimePlanner.status
    _S212_CHECK = ActivePermissionRuntimePlanner.check
    _S212_PLAN = ActivePermissionRuntimePlanner.plan

    def _s213_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.grant_denial_expiry_lifecycle_contract()["safety_blockers"])
        extra = (
            "runtime_audit_writer_active",
            "audit_event_packet_creation_active",
            "audit_event_write_active",
            "audit_log_append_active",
            "audit_persistence_active",
            "audit_storage_write_active",
            "audit_correlation_write_active",
            "audit_permission_lifecycle_link_write_active",
            "audit_grant_denial_expiry_link_write_active",
            "audit_review_queue_enqueue_active",
            "audit_export_active",
            "audit_redaction_runtime_active",
            "audit_retention_mutation_active",
            "audit_failure_recovery_action_active",
            "audit_background_flush_active",
            "audit_network_sync_active",
            "audit_cloud_upload_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s213_runtime_audit_writer_contract(self) -> dict[str, Any]:
        s212 = self.grant_denial_expiry_lifecycle_contract()
        blockers = _s213_safety_blockers(self)

        contract: dict[str, Any] = dict(s212)
        contract.update(
            {
                "runtime_audit_writer_contract_ready": True,
                "runtime_audit_writer_runtime_ready": False,
                "runtime_audit_writer_status": "runtime_audit_writer_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 213,
                "permission_action_next_sprint": 214,
                "permission_action_next_boundary": "action_proposal_preview_runtime",
                "previous_active_permission_runtime_contract_ready": s212[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_grant_denial_expiry_lifecycle_contract_ready": s212[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "audit_event_packet_schema_ready": True,
                "audit_event_type_catalog_schema_ready": True,
                "audit_writer_input_packet_schema_ready": True,
                "audit_write_request_schema_ready": True,
                "audit_write_decision_schema_ready": True,
                "audit_append_only_log_schema_ready": True,
                "audit_persistence_gate_schema_ready": True,
                "audit_correlation_packet_schema_ready": True,
                "audit_actor_context_schema_ready": True,
                "audit_permission_lifecycle_link_schema_ready": True,
                "audit_grant_denial_expiry_link_schema_ready": True,
                "audit_redaction_boundary_schema_ready": True,
                "audit_failure_safe_idle_schema_ready": True,
                "audit_retention_policy_schema_ready": True,
                "audit_review_queue_packet_schema_ready": True,
                "audit_control_center_visibility_schema_ready": True,
                "audit_writer_safety_matrix_schema_ready": True,
                "audit_writer_next_action_preview_schema_ready": True,
                "audit_event_type_catalog": [
                    "permission_request_observed",
                    "permission_grant_decision_observed",
                    "permission_denial_decision_observed",
                    "permission_expiry_observed",
                    "permission_lifecycle_snapshot_observed",
                    "action_proposal_preview_observed",
                    "runtime_safety_blocker_observed",
                    "audit_writer_boundary_check_observed",
                ],
                "audit_event_type_count": 8,
                "audit_write_allowed": False,
                "audit_writer_runtime_ready": False,
                "audit_persistence_ready": False,
                "audit_event_packet_creation_allowed": False,
                "audit_event_write_allowed": False,
                "audit_log_append_allowed": False,
                "audit_persistence_allowed": False,
                "audit_storage_write_allowed": False,
                "audit_correlation_write_allowed": False,
                "audit_permission_lifecycle_link_write_allowed": False,
                "audit_grant_denial_expiry_link_write_allowed": False,
                "audit_review_queue_enqueue_allowed": False,
                "audit_export_allowed": False,
                "audit_redaction_runtime_ready": False,
                "audit_retention_mutation_allowed": False,
                "audit_failure_recovery_action_allowed": False,
                "audit_background_flush_allowed": False,
                "audit_network_sync_allowed": False,
                "audit_cloud_upload_allowed": False,
                "permission_state_mutation_allowed": False,
                "permission_state_persistence_allowed": False,
                "grant_packet_creation_allowed": False,
                "grant_state_mutation_allowed": False,
                "grant_persistence_allowed": False,
                "denial_packet_creation_allowed": False,
                "denial_persistence_allowed": False,
                "expiry_state_mutation_allowed": False,
                "action_proposal_runtime_ready": False,
                "action_preview_runtime_ready": False,
                "action_execution_runtime_ready": False,
                "control_center_approval_runtime_ready": False,
                "runtime_audit_writer_active": False,
                "audit_event_packet_creation_active": False,
                "audit_event_write_active": False,
                "audit_log_append_active": False,
                "audit_persistence_active": False,
                "audit_storage_write_active": False,
                "audit_correlation_write_active": False,
                "audit_permission_lifecycle_link_write_active": False,
                "audit_grant_denial_expiry_link_write_active": False,
                "audit_review_queue_enqueue_active": False,
                "audit_export_active": False,
                "audit_redaction_runtime_active": False,
                "audit_retention_mutation_active": False,
                "audit_failure_recovery_action_active": False,
                "audit_background_flush_active": False,
                "audit_network_sync_active": False,
                "audit_cloud_upload_active": False,
                "audit_event_packet_created": False,
                "audit_writer_input_packet_created": False,
                "audit_write_request_created": False,
                "audit_write_decision_created": False,
                "audit_correlation_packet_created": False,
                "audit_actor_context_created": False,
                "audit_permission_lifecycle_link_created": False,
                "audit_grant_denial_expiry_link_created": False,
                "audit_review_queue_item_created": False,
                "audit_redaction_applied": False,
                "audit_retention_policy_applied": False,
                "audit_control_center_event_emitted": False,
                "audit_event_written": False,
                "audit_event_persisted": False,
                "audit_log_appended": False,
                "audit_storage_written": False,
                "permission_state_mutated": False,
                "permission_grant_created": False,
                "permission_denial_created": False,
                "permission_expiry_created": False,
                "permission_persisted": False,
                "grant_packet_created": False,
                "denial_packet_created": False,
                "expiry_event_packet_created": False,
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
                "no_audit_event_creation": True,
                "no_audit_write": True,
                "no_audit_persistence": True,
                "no_audit_log_append": True,
                "no_audit_storage_write": True,
                "no_audit_correlation_write": True,
                "no_audit_permission_lifecycle_link_write": True,
                "no_audit_grant_denial_expiry_link_write": True,
                "no_audit_review_queue_enqueue": True,
                "no_audit_export": True,
                "no_audit_redaction_runtime": True,
                "no_audit_retention_mutation": True,
                "no_audit_failure_recovery_action": True,
                "no_audit_background_flush": True,
                "no_audit_network_sync": True,
                "no_audit_cloud_upload": True,
                "no_permission_state_mutation": True,
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_denial_persistence": True,
                "no_expiry_mutation": True,
                "no_action_proposal_creation": True,
                "no_action_preview_creation": True,
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
                "runtime_scope": "runtime_audit_writer_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s213_status(self) -> dict[str, Any]:
        status = _S212_STATUS(self)
        contract = self.runtime_audit_writer_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "runtime_audit_writer_contract_ready": contract[
                    "runtime_audit_writer_contract_ready"
                ],
                "runtime_audit_writer_runtime_ready": contract[
                    "runtime_audit_writer_runtime_ready"
                ],
                "runtime_audit_writer_status": contract[
                    "runtime_audit_writer_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "audit_event_packet_schema_ready": contract[
                    "audit_event_packet_schema_ready"
                ],
                "audit_event_type_catalog_schema_ready": contract[
                    "audit_event_type_catalog_schema_ready"
                ],
                "audit_writer_input_packet_schema_ready": contract[
                    "audit_writer_input_packet_schema_ready"
                ],
                "audit_write_request_schema_ready": contract[
                    "audit_write_request_schema_ready"
                ],
                "audit_write_decision_schema_ready": contract[
                    "audit_write_decision_schema_ready"
                ],
                "audit_append_only_log_schema_ready": contract[
                    "audit_append_only_log_schema_ready"
                ],
                "audit_persistence_gate_schema_ready": contract[
                    "audit_persistence_gate_schema_ready"
                ],
                "audit_correlation_packet_schema_ready": contract[
                    "audit_correlation_packet_schema_ready"
                ],
                "audit_actor_context_schema_ready": contract[
                    "audit_actor_context_schema_ready"
                ],
                "audit_permission_lifecycle_link_schema_ready": contract[
                    "audit_permission_lifecycle_link_schema_ready"
                ],
                "audit_grant_denial_expiry_link_schema_ready": contract[
                    "audit_grant_denial_expiry_link_schema_ready"
                ],
                "audit_redaction_boundary_schema_ready": contract[
                    "audit_redaction_boundary_schema_ready"
                ],
                "audit_review_queue_packet_schema_ready": contract[
                    "audit_review_queue_packet_schema_ready"
                ],
                "audit_control_center_visibility_schema_ready": contract[
                    "audit_control_center_visibility_schema_ready"
                ],
                "audit_event_type_count": contract["audit_event_type_count"],
                "audit_write_allowed": contract["audit_write_allowed"],
                "audit_writer_runtime_ready": contract["audit_writer_runtime_ready"],
                "audit_persistence_ready": contract["audit_persistence_ready"],
                "audit_event_packet_creation_allowed": contract[
                    "audit_event_packet_creation_allowed"
                ],
                "audit_event_write_allowed": contract["audit_event_write_allowed"],
                "audit_log_append_allowed": contract["audit_log_append_allowed"],
                "audit_persistence_allowed": contract["audit_persistence_allowed"],
                "audit_storage_write_allowed": contract["audit_storage_write_allowed"],
                "audit_correlation_write_allowed": contract[
                    "audit_correlation_write_allowed"
                ],
                "audit_review_queue_enqueue_allowed": contract[
                    "audit_review_queue_enqueue_allowed"
                ],
                "audit_export_allowed": contract["audit_export_allowed"],
                "audit_redaction_runtime_ready": contract[
                    "audit_redaction_runtime_ready"
                ],
                "audit_event_packet_created": contract[
                    "audit_event_packet_created"
                ],
                "audit_write_request_created": contract["audit_write_request_created"],
                "audit_write_decision_created": contract[
                    "audit_write_decision_created"
                ],
                "audit_correlation_packet_created": contract[
                    "audit_correlation_packet_created"
                ],
                "audit_event_written": contract["audit_event_written"],
                "audit_event_persisted": contract["audit_event_persisted"],
                "audit_log_appended": contract["audit_log_appended"],
                "audit_storage_written": contract["audit_storage_written"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "permission_grant_created": contract["permission_grant_created"],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "file_mutated": contract["file_mutated"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
                "memory_written": contract["memory_written"],
                "external_upload_performed": contract["external_upload_performed"],
                "no_audit_event_creation": contract["no_audit_event_creation"],
                "no_audit_write": contract["no_audit_write"],
                "no_audit_persistence": contract["no_audit_persistence"],
                "no_audit_log_append": contract["no_audit_log_append"],
                "no_audit_storage_write": contract["no_audit_storage_write"],
                "no_audit_correlation_write": contract[
                    "no_audit_correlation_write"
                ],
                "no_audit_review_queue_enqueue": contract[
                    "no_audit_review_queue_enqueue"
                ],
                "no_permission_state_mutation": contract[
                    "no_permission_state_mutation"
                ],
                "no_action_execution": contract["no_action_execution"],
                "no_command_execution": contract["no_command_execution"],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_memory_write": contract["no_memory_write"],
                "no_external_upload": contract["no_external_upload"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "runtime_audit_writer_contract": contract,
                "contract": contract,
                "note": (
                    "Runtime Audit Writer contract is ready for Sprint 213; "
                    "it prepares audit event, append-only log, persistence gate, "
                    "correlation, permission lifecycle link, redaction, retention, "
                    "review queue, and Control Center visibility schemas without "
                    "creating audit packets, writing audit events, appending logs, "
                    "persisting audit data, mutating permissions, or executing "
                    "local actions."
                ),
            }
        )
        return status

    def _s213_check(self) -> dict[str, Any]:
        s212 = _S212_CHECK(self)
        contract = self.runtime_audit_writer_contract()

        true_keys = (
            "runtime_audit_writer_contract_ready",
            "previous_active_permission_runtime_contract_ready",
            "previous_grant_denial_expiry_lifecycle_contract_ready",
            "previous_contract_chain_complete",
            "contract_only",
            "default_deny",
            "audit_event_packet_schema_ready",
            "audit_event_type_catalog_schema_ready",
            "audit_writer_input_packet_schema_ready",
            "audit_write_request_schema_ready",
            "audit_write_decision_schema_ready",
            "audit_append_only_log_schema_ready",
            "audit_persistence_gate_schema_ready",
            "audit_correlation_packet_schema_ready",
            "audit_actor_context_schema_ready",
            "audit_permission_lifecycle_link_schema_ready",
            "audit_grant_denial_expiry_link_schema_ready",
            "audit_redaction_boundary_schema_ready",
            "audit_failure_safe_idle_schema_ready",
            "audit_retention_policy_schema_ready",
            "audit_review_queue_packet_schema_ready",
            "audit_control_center_visibility_schema_ready",
            "audit_writer_safety_matrix_schema_ready",
            "audit_writer_next_action_preview_schema_ready",
            "no_audit_event_creation",
            "no_audit_write",
            "no_audit_persistence",
            "no_audit_log_append",
            "no_audit_storage_write",
            "no_audit_correlation_write",
            "no_audit_permission_lifecycle_link_write",
            "no_audit_grant_denial_expiry_link_write",
            "no_audit_review_queue_enqueue",
            "no_audit_export",
            "no_audit_redaction_runtime",
            "no_audit_retention_mutation",
            "no_audit_failure_recovery_action",
            "no_audit_background_flush",
            "no_audit_network_sync",
            "no_audit_cloud_upload",
            "no_permission_state_mutation",
            "no_permission_persistence",
            "no_grant_creation",
            "no_grant_persistence",
            "no_denial_persistence",
            "no_expiry_mutation",
            "no_action_proposal_creation",
            "no_action_preview_creation",
            "no_action_execution",
            "no_command_execution",
            "no_tool_execution",
            "no_file_mutation",
            "no_desktop_action",
            "no_application_launch",
            "no_network_action",
            "no_git_action",
            "no_memory_write",
            "no_dependency_install",
            "no_model_download",
            "no_external_upload",
            "no_cloud_fallback",
            "no_autonomous_action",
            "all_safety_blockers_inactive",
        )

        false_keys = (
            "runtime_audit_writer_runtime_ready",
            "runtime_ready",
            "runtime_activation_allowed",
            "release_gate_open",
            "default_grant",
            "audit_write_allowed",
            "audit_writer_runtime_ready",
            "audit_persistence_ready",
            "audit_event_packet_creation_allowed",
            "audit_event_write_allowed",
            "audit_log_append_allowed",
            "audit_persistence_allowed",
            "audit_storage_write_allowed",
            "audit_correlation_write_allowed",
            "audit_permission_lifecycle_link_write_allowed",
            "audit_grant_denial_expiry_link_write_allowed",
            "audit_review_queue_enqueue_allowed",
            "audit_export_allowed",
            "audit_redaction_runtime_ready",
            "audit_retention_mutation_allowed",
            "audit_failure_recovery_action_allowed",
            "audit_background_flush_allowed",
            "audit_network_sync_allowed",
            "audit_cloud_upload_allowed",
            "permission_state_mutation_allowed",
            "permission_state_persistence_allowed",
            "grant_packet_creation_allowed",
            "grant_state_mutation_allowed",
            "grant_persistence_allowed",
            "denial_packet_creation_allowed",
            "denial_persistence_allowed",
            "expiry_state_mutation_allowed",
            "action_proposal_runtime_ready",
            "action_preview_runtime_ready",
            "action_execution_runtime_ready",
            "control_center_approval_runtime_ready",
            "audit_event_packet_created",
            "audit_writer_input_packet_created",
            "audit_write_request_created",
            "audit_write_decision_created",
            "audit_correlation_packet_created",
            "audit_actor_context_created",
            "audit_permission_lifecycle_link_created",
            "audit_grant_denial_expiry_link_created",
            "audit_review_queue_item_created",
            "audit_redaction_applied",
            "audit_retention_policy_applied",
            "audit_control_center_event_emitted",
            "audit_event_written",
            "audit_event_persisted",
            "audit_log_appended",
            "audit_storage_written",
            "permission_state_mutated",
            "permission_grant_created",
            "permission_denial_created",
            "permission_expiry_created",
            "permission_persisted",
            "grant_packet_created",
            "denial_packet_created",
            "expiry_event_packet_created",
            "action_proposal_created",
            "action_preview_created",
            "action_enqueued",
            "action_executed",
            "command_executed",
            "tool_executed",
            "file_mutated",
            "desktop_action_executed",
            "application_launched",
            "network_action_executed",
            "git_action_executed",
            "memory_written",
            "dependency_installed",
            "model_downloaded",
            "external_upload_performed",
            "cloud_fallback_used",
            "autonomous_action_performed",
        )

        assertions: dict[str, bool] = {
            "sprint_212_check_still_clean": s212["failed_assertion_count"] == 0,
            "status_ready": contract["runtime_audit_writer_status"]
            == "runtime_audit_writer_contract_ready",
            "current_sprint_213": contract["permission_action_current_sprint"] == 213,
            "next_sprint_214": contract["permission_action_next_sprint"] == 214,
            "next_boundary_action_proposal_preview": contract[
                "permission_action_next_boundary"
            ]
            == "action_proposal_preview_runtime",
            "audit_event_type_count_expected": contract["audit_event_type_count"] == 8,
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "runtime_audit_writer_contract_only",
        }

        for key in true_keys:
            assertions[f"{key}_true"] = contract[key] is True

        for key in false_keys:
            assertions[f"{key}_false"] = contract[key] is False

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s212_failed = [
            f"sprint_212::{name}" for name in s212.get("failed_assertions", [])
        ]
        all_failed = s212_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s212["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "runtime_audit_writer_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 213 "
                "Runtime Audit Writer contract without creating audit packets, "
                "writing audit events, appending audit logs, persisting audit "
                "data, mutating permissions, creating grants, or executing "
                "local actions."
            ),
        }

    def _s213_plan(self) -> dict[str, Any]:
        contract = self.runtime_audit_writer_contract()
        return {
            "name": self.name,
            "sprint": 213,
            "next_sprint": 214,
            "next_boundary": "action_proposal_preview_runtime",
            "contract_ready": contract["runtime_audit_writer_contract_ready"],
            "runtime_ready": contract["runtime_audit_writer_runtime_ready"],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "audit_event_packet": contract["audit_event_packet_schema_ready"],
                "audit_write_request": contract["audit_write_request_schema_ready"],
                "audit_write_decision": contract["audit_write_decision_schema_ready"],
                "append_only_log": contract["audit_append_only_log_schema_ready"],
                "persistence_gate": contract["audit_persistence_gate_schema_ready"],
                "correlation": contract["audit_correlation_packet_schema_ready"],
                "permission_lifecycle_link": contract[
                    "audit_permission_lifecycle_link_schema_ready"
                ],
                "grant_denial_expiry_link": contract[
                    "audit_grant_denial_expiry_link_schema_ready"
                ],
                "review_queue": contract["audit_review_queue_packet_schema_ready"],
                "control_center_visibility": contract[
                    "audit_control_center_visibility_schema_ready"
                ],
            },
            "blocked_runtime": {
                "audit_event_creation": contract[
                    "audit_event_packet_creation_allowed"
                ],
                "audit_write": contract["audit_write_allowed"],
                "audit_log_append": contract["audit_log_append_allowed"],
                "audit_persistence": contract["audit_persistence_allowed"],
                "permission_mutation": contract["permission_state_mutation_allowed"],
                "action_execution": contract["action_execution_runtime_ready"],
            },
        }

    ActivePermissionRuntimePlanner.runtime_audit_writer_contract = (
        _s213_runtime_audit_writer_contract
    )
    ActivePermissionRuntimePlanner.status = _s213_status
    ActivePermissionRuntimePlanner.check = _s213_check
    ActivePermissionRuntimePlanner.plan = _s213_plan
    ActivePermissionRuntimePlanner._s213_extension_installed = True

# Sprint 214 extension: Action Proposal and Preview Runtime.
#
# This stays contract-only. It prepares action proposal, preview, approval
# handoff, permission/audit correlation, and safety visibility without creating
# proposals, previews, queue items, file changes, desktop actions, app launches,
# command/tool execution, or real local actions.
if not getattr(ActivePermissionRuntimePlanner, "_s214_extension_installed", False):
    _S213_STATUS = ActivePermissionRuntimePlanner.status
    _S213_CHECK = ActivePermissionRuntimePlanner.check
    _S213_PLAN = ActivePermissionRuntimePlanner.plan

    def _s214_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.runtime_audit_writer_contract()["safety_blockers"])
        extra = (
            "action_proposal_runtime_active",
            "action_preview_runtime_active",
            "action_proposal_packet_creation_active",
            "action_preview_packet_creation_active",
            "action_preview_render_active",
            "action_risk_assessment_active",
            "action_permission_resolution_active",
            "action_audit_correlation_active",
            "action_user_approval_handoff_active",
            "action_review_queue_enqueue_active",
            "action_queue_enqueue_active",
            "action_execution_dispatch_active",
            "safe_local_action_handoff_active",
            "local_open_action_runtime_active",
            "allowlisted_application_launch_runtime_active",
            "controlled_file_creation_runtime_active",
            "controlled_folder_creation_runtime_active",
            "preview_to_execution_bypass_active",
            "approval_without_preview_active",
            "action_without_permission_active",
            "action_without_audit_correlation_active",
            "multi_step_action_chain_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s214_action_proposal_preview_runtime_contract(self) -> dict[str, Any]:
        s213 = self.runtime_audit_writer_contract()
        blockers = _s214_safety_blockers(self)

        contract: dict[str, Any] = dict(s213)
        contract.update(
            {
                "action_proposal_preview_runtime_contract_ready": True,
                "action_proposal_preview_runtime_ready": False,
                "action_proposal_preview_runtime_status": "action_proposal_preview_runtime_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 214,
                "permission_action_next_sprint": 215,
                "permission_action_next_boundary": "safe_local_open_actions",
                "previous_active_permission_runtime_contract_ready": s213[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_grant_denial_expiry_lifecycle_contract_ready": s213[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "previous_runtime_audit_writer_contract_ready": s213[
                    "runtime_audit_writer_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "preview_before_action_required": True,
                "explicit_approval_before_execution_required": True,
                "permission_before_action_required": True,
                "audit_correlation_before_action_required": True,
                "safe_scope_before_action_required": True,
                "single_action_preview_required": True,
                "action_intent_packet_schema_ready": True,
                "action_proposal_packet_schema_ready": True,
                "action_preview_packet_schema_ready": True,
                "action_risk_summary_schema_ready": True,
                "action_scope_packet_schema_ready": True,
                "action_permission_requirement_schema_ready": True,
                "action_audit_correlation_schema_ready": True,
                "action_user_visible_preview_schema_ready": True,
                "action_user_approval_handoff_schema_ready": True,
                "action_denial_handoff_schema_ready": True,
                "action_review_queue_packet_schema_ready": True,
                "action_execution_blocker_schema_ready": True,
                "action_safety_matrix_schema_ready": True,
                "action_next_safe_open_schema_ready": True,
                "allowed_action_preview_type_catalog": [
                    "open_approved_folder_preview",
                    "open_approved_file_preview",
                    "open_project_location_preview",
                    "open_dashboard_preview",
                    "launch_allowlisted_application_preview",
                    "create_controlled_folder_preview",
                    "create_simple_file_preview",
                ],
                "allowed_action_preview_type_count": 7,
                "blocked_action_type_catalog": [
                    "delete_file",
                    "arbitrary_shell",
                    "broad_desktop_control",
                    "dependency_install",
                    "plugin_action_without_gate",
                    "multi_step_autonomous_chain",
                    "network_action",
                    "credential_access",
                ],
                "blocked_action_type_count": 8,
                "action_proposal_runtime_ready": False,
                "action_preview_runtime_ready": False,
                "action_execution_runtime_ready": False,
                "control_center_approval_runtime_ready": False,
                "safe_local_action_handoff_ready": False,
                "action_proposal_packet_creation_allowed": False,
                "action_preview_packet_creation_allowed": False,
                "action_preview_render_allowed": False,
                "action_risk_assessment_allowed": False,
                "action_permission_resolution_allowed": False,
                "action_audit_correlation_allowed": False,
                "action_user_approval_handoff_allowed": False,
                "action_review_queue_enqueue_allowed": False,
                "action_queue_enqueue_allowed": False,
                "action_execution_dispatch_allowed": False,
                "local_open_action_runtime_ready": False,
                "allowlisted_application_launch_runtime_ready": False,
                "controlled_file_creation_runtime_ready": False,
                "controlled_folder_creation_runtime_ready": False,
                "file_mutation_allowed": False,
                "desktop_action_allowed": False,
                "application_launch_allowed": False,
                "command_execution_allowed": False,
                "tool_execution_allowed": False,
                "audit_write_allowed": False,
                "audit_event_packet_creation_allowed": False,
                "audit_event_write_allowed": False,
                "audit_log_append_allowed": False,
                "audit_persistence_allowed": False,
                "permission_state_mutation_allowed": False,
                "permission_state_persistence_allowed": False,
                "grant_packet_creation_allowed": False,
                "grant_persistence_allowed": False,
                "action_intent_packet_created": False,
                "action_proposal_packet_created": False,
                "action_preview_packet_created": False,
                "action_risk_summary_created": False,
                "action_scope_packet_created": False,
                "action_permission_requirement_created": False,
                "action_audit_correlation_created": False,
                "action_user_visible_preview_created": False,
                "action_user_approval_handoff_created": False,
                "action_denial_handoff_created": False,
                "action_review_queue_item_created": False,
                "action_execution_blocker_created": False,
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
                "external_upload_performed": False,
                "cloud_fallback_used": False,
                "autonomous_action_performed": False,
                "permission_state_mutated": False,
                "permission_grant_created": False,
                "audit_event_written": False,
                "audit_event_persisted": False,
                "audit_log_appended": False,
                "audit_storage_written": False,
                "no_action_intent_packet_creation": True,
                "no_action_proposal_creation": True,
                "no_action_preview_creation": True,
                "no_action_risk_assessment": True,
                "no_action_permission_resolution": True,
                "no_action_audit_correlation_creation": True,
                "no_action_user_approval_handoff": True,
                "no_action_review_queue_enqueue": True,
                "no_action_queue_enqueue": True,
                "no_action_execution_dispatch": True,
                "no_preview_to_execution_bypass": True,
                "no_action_without_preview": True,
                "no_action_without_explicit_approval": True,
                "no_action_without_permission": True,
                "no_action_without_audit_correlation": True,
                "no_multi_step_action_chain": True,
                "no_safe_local_action_handoff": True,
                "no_local_open_action": True,
                "no_file_mutation": True,
                "no_desktop_action": True,
                "no_application_launch": True,
                "no_command_execution": True,
                "no_tool_execution": True,
                "no_network_action": True,
                "no_git_action": True,
                "no_memory_write": True,
                "no_external_upload": True,
                "no_cloud_fallback": True,
                "no_autonomous_action": True,
                "no_permission_state_mutation": True,
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_audit_event_creation": True,
                "no_audit_write": True,
                "no_audit_persistence": True,
                "runtime_scope": "action_proposal_preview_runtime_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s214_status(self) -> dict[str, Any]:
        status = _S213_STATUS(self)
        contract = self.action_proposal_preview_runtime_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "action_proposal_preview_runtime_contract_ready": contract[
                    "action_proposal_preview_runtime_contract_ready"
                ],
                "action_proposal_preview_runtime_ready": contract[
                    "action_proposal_preview_runtime_ready"
                ],
                "action_proposal_preview_runtime_status": contract[
                    "action_proposal_preview_runtime_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "preview_before_action_required": contract[
                    "preview_before_action_required"
                ],
                "explicit_approval_before_execution_required": contract[
                    "explicit_approval_before_execution_required"
                ],
                "permission_before_action_required": contract[
                    "permission_before_action_required"
                ],
                "audit_correlation_before_action_required": contract[
                    "audit_correlation_before_action_required"
                ],
                "action_intent_packet_schema_ready": contract[
                    "action_intent_packet_schema_ready"
                ],
                "action_proposal_packet_schema_ready": contract[
                    "action_proposal_packet_schema_ready"
                ],
                "action_preview_packet_schema_ready": contract[
                    "action_preview_packet_schema_ready"
                ],
                "action_risk_summary_schema_ready": contract[
                    "action_risk_summary_schema_ready"
                ],
                "action_scope_packet_schema_ready": contract[
                    "action_scope_packet_schema_ready"
                ],
                "action_permission_requirement_schema_ready": contract[
                    "action_permission_requirement_schema_ready"
                ],
                "action_audit_correlation_schema_ready": contract[
                    "action_audit_correlation_schema_ready"
                ],
                "action_user_visible_preview_schema_ready": contract[
                    "action_user_visible_preview_schema_ready"
                ],
                "action_user_approval_handoff_schema_ready": contract[
                    "action_user_approval_handoff_schema_ready"
                ],
                "action_review_queue_packet_schema_ready": contract[
                    "action_review_queue_packet_schema_ready"
                ],
                "allowed_action_preview_type_count": contract[
                    "allowed_action_preview_type_count"
                ],
                "blocked_action_type_count": contract["blocked_action_type_count"],
                "action_proposal_runtime_ready": contract[
                    "action_proposal_runtime_ready"
                ],
                "action_preview_runtime_ready": contract[
                    "action_preview_runtime_ready"
                ],
                "action_execution_runtime_ready": contract[
                    "action_execution_runtime_ready"
                ],
                "action_proposal_packet_creation_allowed": contract[
                    "action_proposal_packet_creation_allowed"
                ],
                "action_preview_packet_creation_allowed": contract[
                    "action_preview_packet_creation_allowed"
                ],
                "action_preview_render_allowed": contract[
                    "action_preview_render_allowed"
                ],
                "action_risk_assessment_allowed": contract[
                    "action_risk_assessment_allowed"
                ],
                "action_permission_resolution_allowed": contract[
                    "action_permission_resolution_allowed"
                ],
                "action_audit_correlation_allowed": contract[
                    "action_audit_correlation_allowed"
                ],
                "action_user_approval_handoff_allowed": contract[
                    "action_user_approval_handoff_allowed"
                ],
                "action_review_queue_enqueue_allowed": contract[
                    "action_review_queue_enqueue_allowed"
                ],
                "action_queue_enqueue_allowed": contract[
                    "action_queue_enqueue_allowed"
                ],
                "action_execution_dispatch_allowed": contract[
                    "action_execution_dispatch_allowed"
                ],
                "safe_local_action_handoff_ready": contract[
                    "safe_local_action_handoff_ready"
                ],
                "local_open_action_runtime_ready": contract[
                    "local_open_action_runtime_ready"
                ],
                "file_mutation_allowed": contract["file_mutation_allowed"],
                "desktop_action_allowed": contract["desktop_action_allowed"],
                "application_launch_allowed": contract[
                    "application_launch_allowed"
                ],
                "action_intent_packet_created": contract[
                    "action_intent_packet_created"
                ],
                "action_proposal_packet_created": contract[
                    "action_proposal_packet_created"
                ],
                "action_preview_packet_created": contract[
                    "action_preview_packet_created"
                ],
                "action_risk_summary_created": contract[
                    "action_risk_summary_created"
                ],
                "action_audit_correlation_created": contract[
                    "action_audit_correlation_created"
                ],
                "action_user_visible_preview_created": contract[
                    "action_user_visible_preview_created"
                ],
                "action_user_approval_handoff_created": contract[
                    "action_user_approval_handoff_created"
                ],
                "action_review_queue_item_created": contract[
                    "action_review_queue_item_created"
                ],
                "action_proposal_created": contract["action_proposal_created"],
                "action_preview_created": contract["action_preview_created"],
                "action_enqueued": contract["action_enqueued"],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "file_mutated": contract["file_mutated"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "permission_grant_created": contract["permission_grant_created"],
                "audit_event_written": contract["audit_event_written"],
                "audit_event_persisted": contract["audit_event_persisted"],
                "no_action_proposal_creation": contract[
                    "no_action_proposal_creation"
                ],
                "no_action_preview_creation": contract[
                    "no_action_preview_creation"
                ],
                "no_action_user_approval_handoff": contract[
                    "no_action_user_approval_handoff"
                ],
                "no_action_queue_enqueue": contract["no_action_queue_enqueue"],
                "no_action_execution_dispatch": contract[
                    "no_action_execution_dispatch"
                ],
                "no_preview_to_execution_bypass": contract[
                    "no_preview_to_execution_bypass"
                ],
                "no_action_without_preview": contract[
                    "no_action_without_preview"
                ],
                "no_action_without_explicit_approval": contract[
                    "no_action_without_explicit_approval"
                ],
                "no_action_without_permission": contract[
                    "no_action_without_permission"
                ],
                "no_action_without_audit_correlation": contract[
                    "no_action_without_audit_correlation"
                ],
                "no_multi_step_action_chain": contract[
                    "no_multi_step_action_chain"
                ],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_application_launch": contract["no_application_launch"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "action_proposal_preview_runtime_contract": contract,
                "contract": contract,
                "note": (
                    "Action Proposal and Preview Runtime contract is ready for "
                    "Sprint 214; it prepares proposal, preview, permission, audit "
                    "correlation, approval handoff, review queue, and safety "
                    "schemas without creating proposals, previews, queue items, "
                    "mutating files, launching apps, or executing local actions."
                ),
            }
        )
        return status

    def _s214_check(self) -> dict[str, Any]:
        s213 = _S213_CHECK(self)
        contract = self.action_proposal_preview_runtime_contract()

        true_keys = (
            "action_proposal_preview_runtime_contract_ready",
            "previous_active_permission_runtime_contract_ready",
            "previous_grant_denial_expiry_lifecycle_contract_ready",
            "previous_runtime_audit_writer_contract_ready",
            "previous_contract_chain_complete",
            "contract_only",
            "default_deny",
            "preview_before_action_required",
            "explicit_approval_before_execution_required",
            "permission_before_action_required",
            "audit_correlation_before_action_required",
            "safe_scope_before_action_required",
            "single_action_preview_required",
            "action_intent_packet_schema_ready",
            "action_proposal_packet_schema_ready",
            "action_preview_packet_schema_ready",
            "action_risk_summary_schema_ready",
            "action_scope_packet_schema_ready",
            "action_permission_requirement_schema_ready",
            "action_audit_correlation_schema_ready",
            "action_user_visible_preview_schema_ready",
            "action_user_approval_handoff_schema_ready",
            "action_denial_handoff_schema_ready",
            "action_review_queue_packet_schema_ready",
            "action_execution_blocker_schema_ready",
            "action_safety_matrix_schema_ready",
            "action_next_safe_open_schema_ready",
            "no_action_intent_packet_creation",
            "no_action_proposal_creation",
            "no_action_preview_creation",
            "no_action_risk_assessment",
            "no_action_permission_resolution",
            "no_action_audit_correlation_creation",
            "no_action_user_approval_handoff",
            "no_action_review_queue_enqueue",
            "no_action_queue_enqueue",
            "no_action_execution_dispatch",
            "no_preview_to_execution_bypass",
            "no_action_without_preview",
            "no_action_without_explicit_approval",
            "no_action_without_permission",
            "no_action_without_audit_correlation",
            "no_multi_step_action_chain",
            "no_safe_local_action_handoff",
            "no_local_open_action",
            "no_file_mutation",
            "no_desktop_action",
            "no_application_launch",
            "no_command_execution",
            "no_tool_execution",
            "no_network_action",
            "no_git_action",
            "no_memory_write",
            "no_external_upload",
            "no_cloud_fallback",
            "no_autonomous_action",
            "no_permission_state_mutation",
            "no_permission_persistence",
            "no_grant_creation",
            "no_grant_persistence",
            "no_audit_event_creation",
            "no_audit_write",
            "no_audit_persistence",
            "all_safety_blockers_inactive",
        )

        false_keys = (
            "action_proposal_preview_runtime_ready",
            "runtime_ready",
            "runtime_activation_allowed",
            "release_gate_open",
            "default_grant",
            "action_proposal_runtime_ready",
            "action_preview_runtime_ready",
            "action_execution_runtime_ready",
            "control_center_approval_runtime_ready",
            "safe_local_action_handoff_ready",
            "action_proposal_packet_creation_allowed",
            "action_preview_packet_creation_allowed",
            "action_preview_render_allowed",
            "action_risk_assessment_allowed",
            "action_permission_resolution_allowed",
            "action_audit_correlation_allowed",
            "action_user_approval_handoff_allowed",
            "action_review_queue_enqueue_allowed",
            "action_queue_enqueue_allowed",
            "action_execution_dispatch_allowed",
            "local_open_action_runtime_ready",
            "allowlisted_application_launch_runtime_ready",
            "controlled_file_creation_runtime_ready",
            "controlled_folder_creation_runtime_ready",
            "file_mutation_allowed",
            "desktop_action_allowed",
            "application_launch_allowed",
            "command_execution_allowed",
            "tool_execution_allowed",
            "audit_write_allowed",
            "audit_event_packet_creation_allowed",
            "audit_event_write_allowed",
            "audit_log_append_allowed",
            "audit_persistence_allowed",
            "permission_state_mutation_allowed",
            "permission_state_persistence_allowed",
            "grant_packet_creation_allowed",
            "grant_persistence_allowed",
            "action_intent_packet_created",
            "action_proposal_packet_created",
            "action_preview_packet_created",
            "action_risk_summary_created",
            "action_scope_packet_created",
            "action_permission_requirement_created",
            "action_audit_correlation_created",
            "action_user_visible_preview_created",
            "action_user_approval_handoff_created",
            "action_denial_handoff_created",
            "action_review_queue_item_created",
            "action_execution_blocker_created",
            "action_proposal_created",
            "action_preview_created",
            "action_enqueued",
            "action_executed",
            "command_executed",
            "tool_executed",
            "file_mutated",
            "desktop_action_executed",
            "application_launched",
            "network_action_executed",
            "git_action_executed",
            "memory_written",
            "external_upload_performed",
            "cloud_fallback_used",
            "autonomous_action_performed",
            "permission_state_mutated",
            "permission_grant_created",
            "audit_event_written",
            "audit_event_persisted",
            "audit_log_appended",
            "audit_storage_written",
        )

        assertions: dict[str, bool] = {
            "sprint_213_check_still_clean": s213["failed_assertion_count"] == 0,
            "status_ready": contract["action_proposal_preview_runtime_status"]
            == "action_proposal_preview_runtime_contract_ready",
            "current_sprint_214": contract["permission_action_current_sprint"] == 214,
            "next_sprint_215": contract["permission_action_next_sprint"] == 215,
            "next_boundary_safe_local_open_actions": contract[
                "permission_action_next_boundary"
            ]
            == "safe_local_open_actions",
            "allowed_preview_count_expected": contract[
                "allowed_action_preview_type_count"
            ]
            == len(contract["allowed_action_preview_type_catalog"]),
            "blocked_action_count_expected": contract["blocked_action_type_count"]
            == len(contract["blocked_action_type_catalog"]),
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "action_proposal_preview_runtime_contract_only",
        }

        for key in true_keys:
            assertions[f"{key}_true"] = contract[key] is True

        for key in false_keys:
            assertions[f"{key}_false"] = contract[key] is False

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s213_failed = [
            f"sprint_213::{name}" for name in s213.get("failed_assertions", [])
        ]
        all_failed = s213_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s213["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "runtime_audit_writer_contract": contract,
            "action_proposal_preview_runtime_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 214 "
                "Action Proposal and Preview Runtime contract without creating "
                "proposals, previews, approval handoffs, queue items, audit "
                "events, permission mutations, file mutations, app launches, "
                "commands, tools, or local action execution."
            ),
        }

    def _s214_plan(self) -> dict[str, Any]:
        contract = self.action_proposal_preview_runtime_contract()
        return {
            "name": self.name,
            "sprint": 214,
            "next_sprint": 215,
            "next_boundary": "safe_local_open_actions",
            "contract_ready": contract[
                "action_proposal_preview_runtime_contract_ready"
            ],
            "runtime_ready": contract["action_proposal_preview_runtime_ready"],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "action_intent_packet": contract[
                    "action_intent_packet_schema_ready"
                ],
                "action_proposal_packet": contract[
                    "action_proposal_packet_schema_ready"
                ],
                "action_preview_packet": contract[
                    "action_preview_packet_schema_ready"
                ],
                "action_risk_summary": contract[
                    "action_risk_summary_schema_ready"
                ],
                "action_permission_requirement": contract[
                    "action_permission_requirement_schema_ready"
                ],
                "action_audit_correlation": contract[
                    "action_audit_correlation_schema_ready"
                ],
                "action_user_visible_preview": contract[
                    "action_user_visible_preview_schema_ready"
                ],
                "action_user_approval_handoff": contract[
                    "action_user_approval_handoff_schema_ready"
                ],
                "action_review_queue": contract[
                    "action_review_queue_packet_schema_ready"
                ],
            },
            "blocked_runtime": {
                "action_proposal_creation": contract[
                    "action_proposal_packet_creation_allowed"
                ],
                "action_preview_creation": contract[
                    "action_preview_packet_creation_allowed"
                ],
                "action_queue_enqueue": contract["action_queue_enqueue_allowed"],
                "action_execution": contract["action_execution_runtime_ready"],
                "file_mutation": contract["file_mutation_allowed"],
                "desktop_action": contract["desktop_action_allowed"],
                "application_launch": contract["application_launch_allowed"],
            },
        }

    ActivePermissionRuntimePlanner.action_proposal_preview_runtime_contract = (
        _s214_action_proposal_preview_runtime_contract
    )
    ActivePermissionRuntimePlanner.status = _s214_status
    ActivePermissionRuntimePlanner.check = _s214_check
    ActivePermissionRuntimePlanner.plan = _s214_plan
    ActivePermissionRuntimePlanner._s214_extension_installed = True

# Sprint 215 extension: Safe Local Open Actions.
#
# This remains contract-only. It prepares safe local open action schemas and
# safety visibility for approved folder/file/project/dashboard open previews.
# It does not open files/folders, access arbitrary paths, read files, list
# directories, dispatch shell/OS/browser/file-manager open commands, mutate
# files, control desktop, launch applications, or execute local actions.
if not getattr(ActivePermissionRuntimePlanner, "_s215_extension_installed", False):
    _S214_STATUS = ActivePermissionRuntimePlanner.status
    _S214_CHECK = ActivePermissionRuntimePlanner.check
    _S214_PLAN = ActivePermissionRuntimePlanner.plan

    def _s215_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.action_proposal_preview_runtime_contract()["safety_blockers"])
        extra = (
            "safe_local_open_actions_runtime_active",
            "safe_local_open_request_creation_active",
            "safe_local_open_target_resolution_active",
            "safe_local_open_preview_creation_active",
            "safe_local_open_preview_render_active",
            "safe_local_open_approval_handoff_active",
            "safe_local_open_review_queue_enqueue_active",
            "safe_local_open_dispatch_active",
            "approved_folder_open_runtime_active",
            "approved_file_open_runtime_active",
            "project_location_open_runtime_active",
            "dashboard_open_runtime_active",
            "path_allowlist_resolution_active",
            "path_canonicalization_runtime_active",
            "path_existence_check_runtime_active",
            "path_access_runtime_active",
            "file_read_runtime_active",
            "directory_listing_runtime_active",
            "shell_open_dispatch_active",
            "os_open_dispatch_active",
            "browser_open_dispatch_active",
            "file_manager_launch_active",
            "open_without_preview_active",
            "open_without_approval_active",
            "open_without_permission_active",
            "open_without_audit_correlation_active",
            "open_non_allowlisted_path_active",
            "open_arbitrary_path_active",
            "open_mutating_path_active",
            "open_network_path_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s215_safe_local_open_actions_contract(self) -> dict[str, Any]:
        s214 = self.action_proposal_preview_runtime_contract()
        blockers = _s215_safety_blockers(self)

        contract: dict[str, Any] = dict(s214)
        contract.update(
            {
                "safe_local_open_actions_contract_ready": True,
                "safe_local_open_actions_runtime_ready": False,
                "safe_local_open_actions_status": "safe_local_open_actions_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 215,
                "permission_action_next_sprint": 216,
                "permission_action_next_boundary": "allowlisted_application_launch",
                "previous_active_permission_runtime_contract_ready": s214[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_grant_denial_expiry_lifecycle_contract_ready": s214[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "previous_runtime_audit_writer_contract_ready": s214[
                    "runtime_audit_writer_contract_ready"
                ],
                "previous_action_proposal_preview_runtime_contract_ready": s214[
                    "action_proposal_preview_runtime_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "preview_before_open_required": True,
                "explicit_approval_before_open_required": True,
                "permission_before_open_required": True,
                "audit_correlation_before_open_required": True,
                "allowlist_before_open_required": True,
                "canonical_path_before_open_required": True,
                "safe_local_scope_before_open_required": True,
                "single_open_action_required": True,
                "safe_local_open_request_schema_ready": True,
                "safe_local_open_target_schema_ready": True,
                "safe_local_open_preview_schema_ready": True,
                "safe_local_open_path_policy_schema_ready": True,
                "safe_local_open_allowlist_schema_ready": True,
                "safe_local_open_permission_requirement_schema_ready": True,
                "safe_local_open_audit_correlation_schema_ready": True,
                "safe_local_open_user_visible_preview_schema_ready": True,
                "safe_local_open_approval_handoff_schema_ready": True,
                "safe_local_open_denial_handoff_schema_ready": True,
                "safe_local_open_execution_blocker_schema_ready": True,
                "safe_local_open_review_queue_schema_ready": True,
                "safe_local_open_safety_matrix_schema_ready": True,
                "safe_local_open_next_allowlisted_app_schema_ready": True,
                "allowed_safe_open_target_catalog": [
                    "approved_folder",
                    "approved_file",
                    "approved_project_location",
                    "approved_dashboard",
                ],
                "allowed_safe_open_target_count": 4,
                "blocked_safe_open_target_catalog": [
                    "arbitrary_path",
                    "hidden_path",
                    "system_path",
                    "credential_file",
                    "network_location",
                    "executable_file",
                    "delete_or_mutate_target",
                    "shell_command",
                    "broad_desktop_control",
                ],
                "blocked_safe_open_target_count": 9,
                "safe_local_action_handoff_ready": False,
                "local_open_action_runtime_ready": False,
                "safe_local_open_request_creation_allowed": False,
                "safe_local_open_target_resolution_allowed": False,
                "safe_local_open_preview_creation_allowed": False,
                "safe_local_open_preview_render_allowed": False,
                "safe_local_open_approval_handoff_allowed": False,
                "safe_local_open_review_queue_enqueue_allowed": False,
                "safe_local_open_dispatch_allowed": False,
                "approved_folder_open_runtime_ready": False,
                "approved_file_open_runtime_ready": False,
                "project_location_open_runtime_ready": False,
                "dashboard_open_runtime_ready": False,
                "path_allowlist_resolution_allowed": False,
                "path_canonicalization_allowed": False,
                "path_existence_check_allowed": False,
                "path_access_runtime_ready": False,
                "file_read_runtime_ready": False,
                "directory_listing_runtime_ready": False,
                "shell_open_dispatch_allowed": False,
                "os_open_dispatch_allowed": False,
                "browser_open_dispatch_allowed": False,
                "file_manager_launch_allowed": False,
                "action_execution_runtime_ready": False,
                "action_execution_dispatch_allowed": False,
                "command_execution_allowed": False,
                "tool_execution_allowed": False,
                "file_mutation_allowed": False,
                "desktop_action_allowed": False,
                "application_launch_allowed": False,
                "audit_write_allowed": False,
                "audit_event_packet_creation_allowed": False,
                "audit_event_write_allowed": False,
                "audit_log_append_allowed": False,
                "audit_persistence_allowed": False,
                "permission_state_mutation_allowed": False,
                "permission_state_persistence_allowed": False,
                "grant_packet_creation_allowed": False,
                "grant_persistence_allowed": False,
                "safe_local_open_request_created": False,
                "safe_local_open_target_packet_created": False,
                "safe_local_open_preview_packet_created": False,
                "safe_local_open_path_policy_created": False,
                "safe_local_open_allowlist_packet_created": False,
                "safe_local_open_permission_requirement_created": False,
                "safe_local_open_audit_correlation_created": False,
                "safe_local_open_user_visible_preview_created": False,
                "safe_local_open_approval_handoff_created": False,
                "safe_local_open_denial_handoff_created": False,
                "safe_local_open_execution_blocker_created": False,
                "safe_local_open_review_queue_item_created": False,
                "safe_local_open_action_created": False,
                "safe_local_open_action_enqueued": False,
                "safe_local_open_action_executed": False,
                "approved_folder_opened": False,
                "approved_file_opened": False,
                "project_location_opened": False,
                "dashboard_opened": False,
                "path_allowlist_resolved": False,
                "path_canonicalized": False,
                "path_existence_checked": False,
                "path_accessed": False,
                "file_read_performed": False,
                "directory_listing_performed": False,
                "shell_open_dispatched": False,
                "os_open_dispatched": False,
                "browser_open_dispatched": False,
                "file_manager_launched": False,
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
                "external_upload_performed": False,
                "cloud_fallback_used": False,
                "autonomous_action_performed": False,
                "permission_state_mutated": False,
                "permission_grant_created": False,
                "audit_event_written": False,
                "audit_event_persisted": False,
                "audit_log_appended": False,
                "audit_storage_written": False,
                "no_safe_local_open_request_creation": True,
                "no_safe_local_open_target_resolution": True,
                "no_safe_local_open_preview_creation": True,
                "no_safe_local_open_preview_render": True,
                "no_safe_local_open_approval_handoff": True,
                "no_safe_local_open_review_queue_enqueue": True,
                "no_safe_local_open_dispatch": True,
                "no_approved_folder_open": True,
                "no_approved_file_open": True,
                "no_project_location_open": True,
                "no_dashboard_open": True,
                "no_path_allowlist_resolution": True,
                "no_path_canonicalization": True,
                "no_path_existence_check": True,
                "no_path_access": True,
                "no_file_read": True,
                "no_directory_listing": True,
                "no_shell_open_dispatch": True,
                "no_os_open_dispatch": True,
                "no_browser_open_dispatch": True,
                "no_file_manager_launch": True,
                "no_open_without_preview": True,
                "no_open_without_explicit_approval": True,
                "no_open_without_permission": True,
                "no_open_without_audit_correlation": True,
                "no_open_non_allowlisted_path": True,
                "no_open_arbitrary_path": True,
                "no_open_mutating_path": True,
                "no_open_network_path": True,
                "no_action_execution_dispatch": True,
                "no_action_execution": True,
                "no_command_execution": True,
                "no_tool_execution": True,
                "no_file_mutation": True,
                "no_desktop_action": True,
                "no_application_launch": True,
                "no_network_action": True,
                "no_git_action": True,
                "no_memory_write": True,
                "no_external_upload": True,
                "no_cloud_fallback": True,
                "no_autonomous_action": True,
                "no_permission_state_mutation": True,
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_audit_event_creation": True,
                "no_audit_write": True,
                "no_audit_persistence": True,
                "runtime_scope": "safe_local_open_actions_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s215_status(self) -> dict[str, Any]:
        status = _S214_STATUS(self)
        contract = self.safe_local_open_actions_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "safe_local_open_actions_contract_ready": contract[
                    "safe_local_open_actions_contract_ready"
                ],
                "safe_local_open_actions_runtime_ready": contract[
                    "safe_local_open_actions_runtime_ready"
                ],
                "safe_local_open_actions_status": contract[
                    "safe_local_open_actions_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "preview_before_open_required": contract[
                    "preview_before_open_required"
                ],
                "explicit_approval_before_open_required": contract[
                    "explicit_approval_before_open_required"
                ],
                "permission_before_open_required": contract[
                    "permission_before_open_required"
                ],
                "audit_correlation_before_open_required": contract[
                    "audit_correlation_before_open_required"
                ],
                "allowlist_before_open_required": contract[
                    "allowlist_before_open_required"
                ],
                "canonical_path_before_open_required": contract[
                    "canonical_path_before_open_required"
                ],
                "safe_local_scope_before_open_required": contract[
                    "safe_local_scope_before_open_required"
                ],
                "single_open_action_required": contract[
                    "single_open_action_required"
                ],
                "safe_local_open_request_schema_ready": contract[
                    "safe_local_open_request_schema_ready"
                ],
                "safe_local_open_target_schema_ready": contract[
                    "safe_local_open_target_schema_ready"
                ],
                "safe_local_open_preview_schema_ready": contract[
                    "safe_local_open_preview_schema_ready"
                ],
                "safe_local_open_path_policy_schema_ready": contract[
                    "safe_local_open_path_policy_schema_ready"
                ],
                "safe_local_open_allowlist_schema_ready": contract[
                    "safe_local_open_allowlist_schema_ready"
                ],
                "safe_local_open_permission_requirement_schema_ready": contract[
                    "safe_local_open_permission_requirement_schema_ready"
                ],
                "safe_local_open_audit_correlation_schema_ready": contract[
                    "safe_local_open_audit_correlation_schema_ready"
                ],
                "safe_local_open_user_visible_preview_schema_ready": contract[
                    "safe_local_open_user_visible_preview_schema_ready"
                ],
                "safe_local_open_approval_handoff_schema_ready": contract[
                    "safe_local_open_approval_handoff_schema_ready"
                ],
                "safe_local_open_review_queue_schema_ready": contract[
                    "safe_local_open_review_queue_schema_ready"
                ],
                "allowed_safe_open_target_count": contract[
                    "allowed_safe_open_target_count"
                ],
                "blocked_safe_open_target_count": contract[
                    "blocked_safe_open_target_count"
                ],
                "safe_local_action_handoff_ready": contract[
                    "safe_local_action_handoff_ready"
                ],
                "local_open_action_runtime_ready": contract[
                    "local_open_action_runtime_ready"
                ],
                "safe_local_open_request_creation_allowed": contract[
                    "safe_local_open_request_creation_allowed"
                ],
                "safe_local_open_target_resolution_allowed": contract[
                    "safe_local_open_target_resolution_allowed"
                ],
                "safe_local_open_preview_creation_allowed": contract[
                    "safe_local_open_preview_creation_allowed"
                ],
                "safe_local_open_preview_render_allowed": contract[
                    "safe_local_open_preview_render_allowed"
                ],
                "safe_local_open_approval_handoff_allowed": contract[
                    "safe_local_open_approval_handoff_allowed"
                ],
                "safe_local_open_review_queue_enqueue_allowed": contract[
                    "safe_local_open_review_queue_enqueue_allowed"
                ],
                "safe_local_open_dispatch_allowed": contract[
                    "safe_local_open_dispatch_allowed"
                ],
                "approved_folder_open_runtime_ready": contract[
                    "approved_folder_open_runtime_ready"
                ],
                "approved_file_open_runtime_ready": contract[
                    "approved_file_open_runtime_ready"
                ],
                "project_location_open_runtime_ready": contract[
                    "project_location_open_runtime_ready"
                ],
                "dashboard_open_runtime_ready": contract[
                    "dashboard_open_runtime_ready"
                ],
                "path_allowlist_resolution_allowed": contract[
                    "path_allowlist_resolution_allowed"
                ],
                "path_canonicalization_allowed": contract[
                    "path_canonicalization_allowed"
                ],
                "path_access_runtime_ready": contract["path_access_runtime_ready"],
                "file_read_runtime_ready": contract["file_read_runtime_ready"],
                "directory_listing_runtime_ready": contract[
                    "directory_listing_runtime_ready"
                ],
                "shell_open_dispatch_allowed": contract[
                    "shell_open_dispatch_allowed"
                ],
                "os_open_dispatch_allowed": contract["os_open_dispatch_allowed"],
                "browser_open_dispatch_allowed": contract[
                    "browser_open_dispatch_allowed"
                ],
                "file_manager_launch_allowed": contract[
                    "file_manager_launch_allowed"
                ],
                "file_mutation_allowed": contract["file_mutation_allowed"],
                "desktop_action_allowed": contract["desktop_action_allowed"],
                "application_launch_allowed": contract[
                    "application_launch_allowed"
                ],
                "safe_local_open_request_created": contract[
                    "safe_local_open_request_created"
                ],
                "safe_local_open_target_packet_created": contract[
                    "safe_local_open_target_packet_created"
                ],
                "safe_local_open_preview_packet_created": contract[
                    "safe_local_open_preview_packet_created"
                ],
                "safe_local_open_approval_handoff_created": contract[
                    "safe_local_open_approval_handoff_created"
                ],
                "safe_local_open_review_queue_item_created": contract[
                    "safe_local_open_review_queue_item_created"
                ],
                "safe_local_open_action_created": contract[
                    "safe_local_open_action_created"
                ],
                "safe_local_open_action_enqueued": contract[
                    "safe_local_open_action_enqueued"
                ],
                "safe_local_open_action_executed": contract[
                    "safe_local_open_action_executed"
                ],
                "approved_folder_opened": contract["approved_folder_opened"],
                "approved_file_opened": contract["approved_file_opened"],
                "project_location_opened": contract["project_location_opened"],
                "dashboard_opened": contract["dashboard_opened"],
                "path_accessed": contract["path_accessed"],
                "file_read_performed": contract["file_read_performed"],
                "directory_listing_performed": contract[
                    "directory_listing_performed"
                ],
                "shell_open_dispatched": contract["shell_open_dispatched"],
                "os_open_dispatched": contract["os_open_dispatched"],
                "browser_open_dispatched": contract["browser_open_dispatched"],
                "file_manager_launched": contract["file_manager_launched"],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "file_mutated": contract["file_mutated"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "permission_grant_created": contract["permission_grant_created"],
                "audit_event_written": contract["audit_event_written"],
                "no_safe_local_open_request_creation": contract[
                    "no_safe_local_open_request_creation"
                ],
                "no_safe_local_open_preview_creation": contract[
                    "no_safe_local_open_preview_creation"
                ],
                "no_safe_local_open_dispatch": contract[
                    "no_safe_local_open_dispatch"
                ],
                "no_approved_folder_open": contract["no_approved_folder_open"],
                "no_approved_file_open": contract["no_approved_file_open"],
                "no_project_location_open": contract[
                    "no_project_location_open"
                ],
                "no_dashboard_open": contract["no_dashboard_open"],
                "no_path_access": contract["no_path_access"],
                "no_file_read": contract["no_file_read"],
                "no_directory_listing": contract["no_directory_listing"],
                "no_open_without_preview": contract["no_open_without_preview"],
                "no_open_without_explicit_approval": contract[
                    "no_open_without_explicit_approval"
                ],
                "no_open_without_permission": contract[
                    "no_open_without_permission"
                ],
                "no_open_without_audit_correlation": contract[
                    "no_open_without_audit_correlation"
                ],
                "no_open_non_allowlisted_path": contract[
                    "no_open_non_allowlisted_path"
                ],
                "no_open_arbitrary_path": contract["no_open_arbitrary_path"],
                "no_open_mutating_path": contract["no_open_mutating_path"],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_application_launch": contract["no_application_launch"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "safe_local_open_actions_contract": contract,
                "contract": contract,
                "note": (
                    "Safe Local Open Actions contract is ready for Sprint 215; "
                    "it prepares allowlisted open previews without opening files, "
                    "accessing paths, reading files, launching apps, mutating "
                    "files, or executing local actions."
                ),
            }
        )
        return status

    def _s215_check(self) -> dict[str, Any]:
        s214 = _S214_CHECK(self)
        contract = self.safe_local_open_actions_contract()

        true_keys = (
            "safe_local_open_actions_contract_ready",
            "previous_active_permission_runtime_contract_ready",
            "previous_grant_denial_expiry_lifecycle_contract_ready",
            "previous_runtime_audit_writer_contract_ready",
            "previous_action_proposal_preview_runtime_contract_ready",
            "previous_contract_chain_complete",
            "contract_only",
            "default_deny",
            "preview_before_open_required",
            "explicit_approval_before_open_required",
            "permission_before_open_required",
            "audit_correlation_before_open_required",
            "allowlist_before_open_required",
            "canonical_path_before_open_required",
            "safe_local_scope_before_open_required",
            "single_open_action_required",
            "safe_local_open_request_schema_ready",
            "safe_local_open_target_schema_ready",
            "safe_local_open_preview_schema_ready",
            "safe_local_open_path_policy_schema_ready",
            "safe_local_open_allowlist_schema_ready",
            "safe_local_open_permission_requirement_schema_ready",
            "safe_local_open_audit_correlation_schema_ready",
            "safe_local_open_user_visible_preview_schema_ready",
            "safe_local_open_approval_handoff_schema_ready",
            "safe_local_open_denial_handoff_schema_ready",
            "safe_local_open_execution_blocker_schema_ready",
            "safe_local_open_review_queue_schema_ready",
            "safe_local_open_safety_matrix_schema_ready",
            "safe_local_open_next_allowlisted_app_schema_ready",
            "no_safe_local_open_request_creation",
            "no_safe_local_open_target_resolution",
            "no_safe_local_open_preview_creation",
            "no_safe_local_open_preview_render",
            "no_safe_local_open_approval_handoff",
            "no_safe_local_open_review_queue_enqueue",
            "no_safe_local_open_dispatch",
            "no_approved_folder_open",
            "no_approved_file_open",
            "no_project_location_open",
            "no_dashboard_open",
            "no_path_allowlist_resolution",
            "no_path_canonicalization",
            "no_path_existence_check",
            "no_path_access",
            "no_file_read",
            "no_directory_listing",
            "no_shell_open_dispatch",
            "no_os_open_dispatch",
            "no_browser_open_dispatch",
            "no_file_manager_launch",
            "no_open_without_preview",
            "no_open_without_explicit_approval",
            "no_open_without_permission",
            "no_open_without_audit_correlation",
            "no_open_non_allowlisted_path",
            "no_open_arbitrary_path",
            "no_open_mutating_path",
            "no_open_network_path",
            "no_action_execution_dispatch",
            "no_action_execution",
            "no_command_execution",
            "no_tool_execution",
            "no_file_mutation",
            "no_desktop_action",
            "no_application_launch",
            "no_network_action",
            "no_git_action",
            "no_memory_write",
            "no_external_upload",
            "no_cloud_fallback",
            "no_autonomous_action",
            "no_permission_state_mutation",
            "no_permission_persistence",
            "no_grant_creation",
            "no_grant_persistence",
            "no_audit_event_creation",
            "no_audit_write",
            "no_audit_persistence",
            "all_safety_blockers_inactive",
        )

        false_keys = (
            "safe_local_open_actions_runtime_ready",
            "runtime_ready",
            "runtime_activation_allowed",
            "release_gate_open",
            "default_grant",
            "safe_local_action_handoff_ready",
            "local_open_action_runtime_ready",
            "safe_local_open_request_creation_allowed",
            "safe_local_open_target_resolution_allowed",
            "safe_local_open_preview_creation_allowed",
            "safe_local_open_preview_render_allowed",
            "safe_local_open_approval_handoff_allowed",
            "safe_local_open_review_queue_enqueue_allowed",
            "safe_local_open_dispatch_allowed",
            "approved_folder_open_runtime_ready",
            "approved_file_open_runtime_ready",
            "project_location_open_runtime_ready",
            "dashboard_open_runtime_ready",
            "path_allowlist_resolution_allowed",
            "path_canonicalization_allowed",
            "path_existence_check_allowed",
            "path_access_runtime_ready",
            "file_read_runtime_ready",
            "directory_listing_runtime_ready",
            "shell_open_dispatch_allowed",
            "os_open_dispatch_allowed",
            "browser_open_dispatch_allowed",
            "file_manager_launch_allowed",
            "action_execution_runtime_ready",
            "action_execution_dispatch_allowed",
            "command_execution_allowed",
            "tool_execution_allowed",
            "file_mutation_allowed",
            "desktop_action_allowed",
            "application_launch_allowed",
            "audit_write_allowed",
            "audit_event_packet_creation_allowed",
            "audit_event_write_allowed",
            "audit_log_append_allowed",
            "audit_persistence_allowed",
            "permission_state_mutation_allowed",
            "permission_state_persistence_allowed",
            "grant_packet_creation_allowed",
            "grant_persistence_allowed",
            "safe_local_open_request_created",
            "safe_local_open_target_packet_created",
            "safe_local_open_preview_packet_created",
            "safe_local_open_path_policy_created",
            "safe_local_open_allowlist_packet_created",
            "safe_local_open_permission_requirement_created",
            "safe_local_open_audit_correlation_created",
            "safe_local_open_user_visible_preview_created",
            "safe_local_open_approval_handoff_created",
            "safe_local_open_denial_handoff_created",
            "safe_local_open_execution_blocker_created",
            "safe_local_open_review_queue_item_created",
            "safe_local_open_action_created",
            "safe_local_open_action_enqueued",
            "safe_local_open_action_executed",
            "approved_folder_opened",
            "approved_file_opened",
            "project_location_opened",
            "dashboard_opened",
            "path_allowlist_resolved",
            "path_canonicalized",
            "path_existence_checked",
            "path_accessed",
            "file_read_performed",
            "directory_listing_performed",
            "shell_open_dispatched",
            "os_open_dispatched",
            "browser_open_dispatched",
            "file_manager_launched",
            "action_proposal_created",
            "action_preview_created",
            "action_enqueued",
            "action_executed",
            "command_executed",
            "tool_executed",
            "file_mutated",
            "desktop_action_executed",
            "application_launched",
            "network_action_executed",
            "git_action_executed",
            "memory_written",
            "external_upload_performed",
            "cloud_fallback_used",
            "autonomous_action_performed",
            "permission_state_mutated",
            "permission_grant_created",
            "audit_event_written",
            "audit_event_persisted",
            "audit_log_appended",
            "audit_storage_written",
        )

        assertions: dict[str, bool] = {
            "sprint_214_check_still_clean": s214["failed_assertion_count"] == 0,
            "status_ready": contract["safe_local_open_actions_status"]
            == "safe_local_open_actions_contract_ready",
            "current_sprint_215": contract["permission_action_current_sprint"] == 215,
            "next_sprint_216": contract["permission_action_next_sprint"] == 216,
            "next_boundary_allowlisted_application_launch": contract[
                "permission_action_next_boundary"
            ]
            == "allowlisted_application_launch",
            "allowed_safe_open_target_count_expected": contract[
                "allowed_safe_open_target_count"
            ]
            == len(contract["allowed_safe_open_target_catalog"]),
            "blocked_safe_open_target_count_expected": contract[
                "blocked_safe_open_target_count"
            ]
            == len(contract["blocked_safe_open_target_catalog"]),
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "safe_local_open_actions_contract_only",
        }

        for key in true_keys:
            assertions[f"{key}_true"] = contract[key] is True

        for key in false_keys:
            assertions[f"{key}_false"] = contract[key] is False

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s214_failed = [
            f"sprint_214::{name}" for name in s214.get("failed_assertions", [])
        ]
        all_failed = s214_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s214["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "runtime_audit_writer_contract": contract,
            "action_proposal_preview_runtime_contract": contract,
            "safe_local_open_actions_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 215 "
                "Safe Local Open Actions contract without creating open requests, "
                "previews, approval handoffs, queue items, path access, file "
                "reads, folder/file opens, desktop actions, app launches, "
                "commands, tools, permission mutations, audit writes, or local "
                "action execution."
            ),
        }

    def _s215_plan(self) -> dict[str, Any]:
        contract = self.safe_local_open_actions_contract()
        return {
            "name": self.name,
            "sprint": 215,
            "next_sprint": 216,
            "next_boundary": "allowlisted_application_launch",
            "contract_ready": contract["safe_local_open_actions_contract_ready"],
            "runtime_ready": contract["safe_local_open_actions_runtime_ready"],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "safe_local_open_request": contract[
                    "safe_local_open_request_schema_ready"
                ],
                "safe_local_open_target": contract[
                    "safe_local_open_target_schema_ready"
                ],
                "safe_local_open_preview": contract[
                    "safe_local_open_preview_schema_ready"
                ],
                "safe_local_open_path_policy": contract[
                    "safe_local_open_path_policy_schema_ready"
                ],
                "safe_local_open_allowlist": contract[
                    "safe_local_open_allowlist_schema_ready"
                ],
                "safe_local_open_audit_correlation": contract[
                    "safe_local_open_audit_correlation_schema_ready"
                ],
                "safe_local_open_approval_handoff": contract[
                    "safe_local_open_approval_handoff_schema_ready"
                ],
                "safe_local_open_review_queue": contract[
                    "safe_local_open_review_queue_schema_ready"
                ],
            },
            "blocked_runtime": {
                "open_request_creation": contract[
                    "safe_local_open_request_creation_allowed"
                ],
                "open_preview_creation": contract[
                    "safe_local_open_preview_creation_allowed"
                ],
                "open_dispatch": contract["safe_local_open_dispatch_allowed"],
                "path_access": contract["path_access_runtime_ready"],
                "file_read": contract["file_read_runtime_ready"],
                "folder_open": contract["approved_folder_open_runtime_ready"],
                "file_open": contract["approved_file_open_runtime_ready"],
                "desktop_action": contract["desktop_action_allowed"],
                "application_launch": contract["application_launch_allowed"],
                "file_mutation": contract["file_mutation_allowed"],
            },
        }

    ActivePermissionRuntimePlanner.safe_local_open_actions_contract = (
        _s215_safe_local_open_actions_contract
    )
    ActivePermissionRuntimePlanner.status = _s215_status
    ActivePermissionRuntimePlanner.check = _s215_check
    ActivePermissionRuntimePlanner.plan = _s215_plan
    ActivePermissionRuntimePlanner._s215_extension_installed = True

# Sprint 216 extension: Allowlisted Application Launch.
#
# This remains contract-only. It prepares allowlisted application launch schemas
# and safety visibility for future approved local application launch previews.
# It does not launch applications, resolve executables, dispatch shell/OS
# commands, start processes, open file managers, run tools, mutate files,
# control desktop, write audit events, or execute local actions.
if not getattr(ActivePermissionRuntimePlanner, "_s216_extension_installed", False):
    _S215_STATUS = ActivePermissionRuntimePlanner.status
    _S215_CHECK = ActivePermissionRuntimePlanner.check
    _S215_PLAN = ActivePermissionRuntimePlanner.plan

    def _s216_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.safe_local_open_actions_contract()["safety_blockers"])
        extra = (
            "allowlisted_application_launch_runtime_active",
            "application_launch_request_creation_active",
            "application_launch_target_resolution_active",
            "application_launch_preview_creation_active",
            "application_launch_preview_render_active",
            "application_launch_approval_handoff_active",
            "application_launch_review_queue_enqueue_active",
            "application_launch_dispatch_active",
            "application_allowlist_resolution_active",
            "application_identity_validation_active",
            "application_executable_resolution_active",
            "application_argument_resolution_active",
            "application_environment_resolution_active",
            "application_process_spawn_active",
            "approved_application_launch_runtime_active",
            "approved_project_tool_launch_runtime_active",
            "approved_browser_launch_runtime_active",
            "approved_editor_launch_runtime_active",
            "approved_file_manager_launch_runtime_active",
            "shell_application_launch_dispatch_active",
            "os_application_launch_dispatch_active",
            "desktop_application_launch_dispatch_active",
            "launch_without_preview_active",
            "launch_without_approval_active",
            "launch_without_permission_active",
            "launch_without_audit_correlation_active",
            "launch_non_allowlisted_application_active",
            "launch_arbitrary_executable_active",
            "launch_with_unapproved_arguments_active",
            "launch_privileged_application_active",
            "launch_installer_or_package_manager_active",
            "launch_network_downloader_active",
            "launch_script_or_macro_active",
            "launch_multi_step_chain_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s216_allowlisted_application_launch_contract(self) -> dict[str, Any]:
        s215 = self.safe_local_open_actions_contract()
        blockers = _s216_safety_blockers(self)

        contract: dict[str, Any] = dict(s215)
        contract.update(
            {
                "allowlisted_application_launch_contract_ready": True,
                "allowlisted_application_launch_runtime_ready": False,
                "allowlisted_application_launch_status": "allowlisted_application_launch_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 216,
                "permission_action_next_sprint": 217,
                "permission_action_next_boundary": "controlled_folder_simple_file_creation",
                "previous_active_permission_runtime_contract_ready": s215[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_grant_denial_expiry_lifecycle_contract_ready": s215[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "previous_runtime_audit_writer_contract_ready": s215[
                    "runtime_audit_writer_contract_ready"
                ],
                "previous_action_proposal_preview_runtime_contract_ready": s215[
                    "action_proposal_preview_runtime_contract_ready"
                ],
                "previous_safe_local_open_actions_contract_ready": s215[
                    "safe_local_open_actions_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "preview_before_launch_required": True,
                "explicit_approval_before_launch_required": True,
                "permission_before_launch_required": True,
                "audit_correlation_before_launch_required": True,
                "allowlist_before_launch_required": True,
                "application_identity_before_launch_required": True,
                "safe_arguments_before_launch_required": True,
                "safe_environment_before_launch_required": True,
                "single_application_launch_required": True,
                "application_launch_request_schema_ready": True,
                "application_launch_target_schema_ready": True,
                "application_launch_preview_schema_ready": True,
                "application_launch_allowlist_schema_ready": True,
                "application_launch_permission_requirement_schema_ready": True,
                "application_launch_audit_correlation_schema_ready": True,
                "application_launch_user_visible_preview_schema_ready": True,
                "application_launch_approval_handoff_schema_ready": True,
                "application_launch_denial_handoff_schema_ready": True,
                "application_launch_execution_blocker_schema_ready": True,
                "application_launch_review_queue_schema_ready": True,
                "application_launch_safety_matrix_schema_ready": True,
                "application_launch_next_controlled_file_schema_ready": True,
                "allowed_application_launch_profile_catalog": [
                    "approved_browser_application",
                    "approved_editor_application",
                    "approved_file_manager_application",
                    "approved_creative_tool_application",
                    "approved_project_tool_application",
                ],
                "allowed_application_launch_profile_count": 5,
                "blocked_application_launch_target_catalog": [
                    "arbitrary_executable",
                    "unapproved_application",
                    "installer_or_package_manager",
                    "privileged_admin_application",
                    "shell_command",
                    "script_or_macro",
                    "network_downloader",
                    "credential_or_secret_tool",
                    "system_settings_mutator",
                    "multi_step_automation_chain",
                ],
                "blocked_application_launch_target_count": 10,
                "application_launch_runtime_ready": False,
                "application_launch_request_creation_allowed": False,
                "application_launch_target_resolution_allowed": False,
                "application_launch_preview_creation_allowed": False,
                "application_launch_preview_render_allowed": False,
                "application_launch_approval_handoff_allowed": False,
                "application_launch_review_queue_enqueue_allowed": False,
                "application_launch_dispatch_allowed": False,
                "application_allowlist_resolution_allowed": False,
                "application_identity_validation_allowed": False,
                "application_executable_resolution_allowed": False,
                "application_argument_resolution_allowed": False,
                "application_environment_resolution_allowed": False,
                "application_process_spawn_allowed": False,
                "approved_application_launch_runtime_ready": False,
                "approved_project_tool_launch_runtime_ready": False,
                "approved_browser_launch_runtime_ready": False,
                "approved_editor_launch_runtime_ready": False,
                "approved_file_manager_launch_runtime_ready": False,
                "shell_application_launch_dispatch_allowed": False,
                "os_application_launch_dispatch_allowed": False,
                "desktop_application_launch_dispatch_allowed": False,
                "safe_local_action_handoff_ready": False,
                "local_open_action_runtime_ready": False,
                "action_execution_runtime_ready": False,
                "action_execution_dispatch_allowed": False,
                "command_execution_allowed": False,
                "tool_execution_allowed": False,
                "file_mutation_allowed": False,
                "desktop_action_allowed": False,
                "application_launch_allowed": False,
                "audit_write_allowed": False,
                "audit_event_packet_creation_allowed": False,
                "audit_event_write_allowed": False,
                "audit_log_append_allowed": False,
                "audit_persistence_allowed": False,
                "permission_state_mutation_allowed": False,
                "permission_state_persistence_allowed": False,
                "grant_packet_creation_allowed": False,
                "grant_persistence_allowed": False,
                "application_launch_request_created": False,
                "application_launch_target_packet_created": False,
                "application_launch_preview_packet_created": False,
                "application_launch_allowlist_packet_created": False,
                "application_launch_permission_requirement_created": False,
                "application_launch_audit_correlation_created": False,
                "application_launch_user_visible_preview_created": False,
                "application_launch_approval_handoff_created": False,
                "application_launch_denial_handoff_created": False,
                "application_launch_execution_blocker_created": False,
                "application_launch_review_queue_item_created": False,
                "application_launch_action_created": False,
                "application_launch_action_enqueued": False,
                "application_launch_action_executed": False,
                "application_allowlist_resolved": False,
                "application_identity_validated": False,
                "application_executable_resolved": False,
                "application_arguments_resolved": False,
                "application_environment_resolved": False,
                "application_process_spawned": False,
                "approved_application_launched": False,
                "approved_project_tool_launched": False,
                "approved_browser_launched": False,
                "approved_editor_launched": False,
                "approved_file_manager_launched": False,
                "shell_application_launch_dispatched": False,
                "os_application_launch_dispatched": False,
                "desktop_application_launch_dispatched": False,
                "safe_local_open_action_executed": False,
                "approved_folder_opened": False,
                "approved_file_opened": False,
                "project_location_opened": False,
                "dashboard_opened": False,
                "path_accessed": False,
                "file_read_performed": False,
                "directory_listing_performed": False,
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
                "external_upload_performed": False,
                "cloud_fallback_used": False,
                "autonomous_action_performed": False,
                "permission_state_mutated": False,
                "permission_grant_created": False,
                "audit_event_written": False,
                "audit_event_persisted": False,
                "audit_log_appended": False,
                "audit_storage_written": False,
                "no_application_launch_request_creation": True,
                "no_application_launch_target_resolution": True,
                "no_application_launch_preview_creation": True,
                "no_application_launch_preview_render": True,
                "no_application_launch_approval_handoff": True,
                "no_application_launch_review_queue_enqueue": True,
                "no_application_launch_dispatch": True,
                "no_application_allowlist_resolution": True,
                "no_application_identity_validation": True,
                "no_application_executable_resolution": True,
                "no_application_argument_resolution": True,
                "no_application_environment_resolution": True,
                "no_application_process_spawn": True,
                "no_approved_application_launch": True,
                "no_approved_project_tool_launch": True,
                "no_approved_browser_launch": True,
                "no_approved_editor_launch": True,
                "no_approved_file_manager_launch": True,
                "no_shell_application_launch_dispatch": True,
                "no_os_application_launch_dispatch": True,
                "no_desktop_application_launch_dispatch": True,
                "no_launch_without_preview": True,
                "no_launch_without_explicit_approval": True,
                "no_launch_without_permission": True,
                "no_launch_without_audit_correlation": True,
                "no_launch_non_allowlisted_application": True,
                "no_launch_arbitrary_executable": True,
                "no_launch_with_unapproved_arguments": True,
                "no_launch_privileged_application": True,
                "no_launch_installer_or_package_manager": True,
                "no_launch_network_downloader": True,
                "no_launch_script_or_macro": True,
                "no_launch_multi_step_chain": True,
                "no_safe_local_open_dispatch": True,
                "no_path_access": True,
                "no_file_read": True,
                "no_directory_listing": True,
                "no_action_execution_dispatch": True,
                "no_action_execution": True,
                "no_command_execution": True,
                "no_tool_execution": True,
                "no_file_mutation": True,
                "no_desktop_action": True,
                "no_application_launch": True,
                "no_network_action": True,
                "no_git_action": True,
                "no_memory_write": True,
                "no_external_upload": True,
                "no_cloud_fallback": True,
                "no_autonomous_action": True,
                "no_permission_state_mutation": True,
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_audit_event_creation": True,
                "no_audit_write": True,
                "no_audit_persistence": True,
                "runtime_scope": "allowlisted_application_launch_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s216_status(self) -> dict[str, Any]:
        status = _S215_STATUS(self)
        contract = self.allowlisted_application_launch_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "allowlisted_application_launch_contract_ready": contract[
                    "allowlisted_application_launch_contract_ready"
                ],
                "allowlisted_application_launch_runtime_ready": contract[
                    "allowlisted_application_launch_runtime_ready"
                ],
                "allowlisted_application_launch_status": contract[
                    "allowlisted_application_launch_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "preview_before_launch_required": contract[
                    "preview_before_launch_required"
                ],
                "explicit_approval_before_launch_required": contract[
                    "explicit_approval_before_launch_required"
                ],
                "permission_before_launch_required": contract[
                    "permission_before_launch_required"
                ],
                "audit_correlation_before_launch_required": contract[
                    "audit_correlation_before_launch_required"
                ],
                "allowlist_before_launch_required": contract[
                    "allowlist_before_launch_required"
                ],
                "application_identity_before_launch_required": contract[
                    "application_identity_before_launch_required"
                ],
                "safe_arguments_before_launch_required": contract[
                    "safe_arguments_before_launch_required"
                ],
                "safe_environment_before_launch_required": contract[
                    "safe_environment_before_launch_required"
                ],
                "single_application_launch_required": contract[
                    "single_application_launch_required"
                ],
                "application_launch_request_schema_ready": contract[
                    "application_launch_request_schema_ready"
                ],
                "application_launch_target_schema_ready": contract[
                    "application_launch_target_schema_ready"
                ],
                "application_launch_preview_schema_ready": contract[
                    "application_launch_preview_schema_ready"
                ],
                "application_launch_allowlist_schema_ready": contract[
                    "application_launch_allowlist_schema_ready"
                ],
                "application_launch_permission_requirement_schema_ready": contract[
                    "application_launch_permission_requirement_schema_ready"
                ],
                "application_launch_audit_correlation_schema_ready": contract[
                    "application_launch_audit_correlation_schema_ready"
                ],
                "application_launch_user_visible_preview_schema_ready": contract[
                    "application_launch_user_visible_preview_schema_ready"
                ],
                "application_launch_approval_handoff_schema_ready": contract[
                    "application_launch_approval_handoff_schema_ready"
                ],
                "application_launch_review_queue_schema_ready": contract[
                    "application_launch_review_queue_schema_ready"
                ],
                "allowed_application_launch_profile_count": contract[
                    "allowed_application_launch_profile_count"
                ],
                "blocked_application_launch_target_count": contract[
                    "blocked_application_launch_target_count"
                ],
                "application_launch_runtime_ready": contract[
                    "application_launch_runtime_ready"
                ],
                "application_launch_request_creation_allowed": contract[
                    "application_launch_request_creation_allowed"
                ],
                "application_launch_target_resolution_allowed": contract[
                    "application_launch_target_resolution_allowed"
                ],
                "application_launch_preview_creation_allowed": contract[
                    "application_launch_preview_creation_allowed"
                ],
                "application_launch_preview_render_allowed": contract[
                    "application_launch_preview_render_allowed"
                ],
                "application_launch_approval_handoff_allowed": contract[
                    "application_launch_approval_handoff_allowed"
                ],
                "application_launch_review_queue_enqueue_allowed": contract[
                    "application_launch_review_queue_enqueue_allowed"
                ],
                "application_launch_dispatch_allowed": contract[
                    "application_launch_dispatch_allowed"
                ],
                "application_allowlist_resolution_allowed": contract[
                    "application_allowlist_resolution_allowed"
                ],
                "application_identity_validation_allowed": contract[
                    "application_identity_validation_allowed"
                ],
                "application_executable_resolution_allowed": contract[
                    "application_executable_resolution_allowed"
                ],
                "application_argument_resolution_allowed": contract[
                    "application_argument_resolution_allowed"
                ],
                "application_environment_resolution_allowed": contract[
                    "application_environment_resolution_allowed"
                ],
                "application_process_spawn_allowed": contract[
                    "application_process_spawn_allowed"
                ],
                "approved_application_launch_runtime_ready": contract[
                    "approved_application_launch_runtime_ready"
                ],
                "approved_project_tool_launch_runtime_ready": contract[
                    "approved_project_tool_launch_runtime_ready"
                ],
                "approved_browser_launch_runtime_ready": contract[
                    "approved_browser_launch_runtime_ready"
                ],
                "approved_editor_launch_runtime_ready": contract[
                    "approved_editor_launch_runtime_ready"
                ],
                "approved_file_manager_launch_runtime_ready": contract[
                    "approved_file_manager_launch_runtime_ready"
                ],
                "shell_application_launch_dispatch_allowed": contract[
                    "shell_application_launch_dispatch_allowed"
                ],
                "os_application_launch_dispatch_allowed": contract[
                    "os_application_launch_dispatch_allowed"
                ],
                "desktop_application_launch_dispatch_allowed": contract[
                    "desktop_application_launch_dispatch_allowed"
                ],
                "application_launch_allowed": contract["application_launch_allowed"],
                "desktop_action_allowed": contract["desktop_action_allowed"],
                "file_mutation_allowed": contract["file_mutation_allowed"],
                "application_launch_request_created": contract[
                    "application_launch_request_created"
                ],
                "application_launch_preview_packet_created": contract[
                    "application_launch_preview_packet_created"
                ],
                "application_launch_approval_handoff_created": contract[
                    "application_launch_approval_handoff_created"
                ],
                "application_launch_review_queue_item_created": contract[
                    "application_launch_review_queue_item_created"
                ],
                "application_launch_action_executed": contract[
                    "application_launch_action_executed"
                ],
                "application_allowlist_resolved": contract[
                    "application_allowlist_resolved"
                ],
                "application_identity_validated": contract[
                    "application_identity_validated"
                ],
                "application_executable_resolved": contract[
                    "application_executable_resolved"
                ],
                "application_process_spawned": contract[
                    "application_process_spawned"
                ],
                "approved_application_launched": contract[
                    "approved_application_launched"
                ],
                "approved_project_tool_launched": contract[
                    "approved_project_tool_launched"
                ],
                "approved_browser_launched": contract["approved_browser_launched"],
                "approved_editor_launched": contract["approved_editor_launched"],
                "approved_file_manager_launched": contract[
                    "approved_file_manager_launched"
                ],
                "shell_application_launch_dispatched": contract[
                    "shell_application_launch_dispatched"
                ],
                "os_application_launch_dispatched": contract[
                    "os_application_launch_dispatched"
                ],
                "desktop_application_launch_dispatched": contract[
                    "desktop_application_launch_dispatched"
                ],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "file_mutated": contract["file_mutated"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "permission_grant_created": contract["permission_grant_created"],
                "audit_event_written": contract["audit_event_written"],
                "no_application_launch_request_creation": contract[
                    "no_application_launch_request_creation"
                ],
                "no_application_launch_preview_creation": contract[
                    "no_application_launch_preview_creation"
                ],
                "no_application_launch_dispatch": contract[
                    "no_application_launch_dispatch"
                ],
                "no_application_allowlist_resolution": contract[
                    "no_application_allowlist_resolution"
                ],
                "no_application_identity_validation": contract[
                    "no_application_identity_validation"
                ],
                "no_application_process_spawn": contract[
                    "no_application_process_spawn"
                ],
                "no_approved_application_launch": contract[
                    "no_approved_application_launch"
                ],
                "no_approved_project_tool_launch": contract[
                    "no_approved_project_tool_launch"
                ],
                "no_approved_browser_launch": contract[
                    "no_approved_browser_launch"
                ],
                "no_approved_editor_launch": contract[
                    "no_approved_editor_launch"
                ],
                "no_approved_file_manager_launch": contract[
                    "no_approved_file_manager_launch"
                ],
                "no_launch_without_preview": contract[
                    "no_launch_without_preview"
                ],
                "no_launch_without_explicit_approval": contract[
                    "no_launch_without_explicit_approval"
                ],
                "no_launch_without_permission": contract[
                    "no_launch_without_permission"
                ],
                "no_launch_without_audit_correlation": contract[
                    "no_launch_without_audit_correlation"
                ],
                "no_launch_non_allowlisted_application": contract[
                    "no_launch_non_allowlisted_application"
                ],
                "no_launch_arbitrary_executable": contract[
                    "no_launch_arbitrary_executable"
                ],
                "no_launch_with_unapproved_arguments": contract[
                    "no_launch_with_unapproved_arguments"
                ],
                "no_launch_privileged_application": contract[
                    "no_launch_privileged_application"
                ],
                "no_launch_installer_or_package_manager": contract[
                    "no_launch_installer_or_package_manager"
                ],
                "no_launch_multi_step_chain": contract[
                    "no_launch_multi_step_chain"
                ],
                "no_application_launch": contract["no_application_launch"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_file_mutation": contract["no_file_mutation"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "allowlisted_application_launch_contract": contract,
                "contract": contract,
                "note": (
                    "Allowlisted Application Launch contract is ready for "
                    "Sprint 216; it prepares application launch previews "
                    "without resolving executables, spawning processes, "
                    "dispatching launch commands, launching apps, mutating "
                    "files, or executing local actions."
                ),
            }
        )
        return status

    def _s216_check(self) -> dict[str, Any]:
        s215 = _S215_CHECK(self)
        contract = self.allowlisted_application_launch_contract()

        true_keys = (
            "allowlisted_application_launch_contract_ready",
            "previous_active_permission_runtime_contract_ready",
            "previous_grant_denial_expiry_lifecycle_contract_ready",
            "previous_runtime_audit_writer_contract_ready",
            "previous_action_proposal_preview_runtime_contract_ready",
            "previous_safe_local_open_actions_contract_ready",
            "previous_contract_chain_complete",
            "contract_only",
            "default_deny",
            "preview_before_launch_required",
            "explicit_approval_before_launch_required",
            "permission_before_launch_required",
            "audit_correlation_before_launch_required",
            "allowlist_before_launch_required",
            "application_identity_before_launch_required",
            "safe_arguments_before_launch_required",
            "safe_environment_before_launch_required",
            "single_application_launch_required",
            "application_launch_request_schema_ready",
            "application_launch_target_schema_ready",
            "application_launch_preview_schema_ready",
            "application_launch_allowlist_schema_ready",
            "application_launch_permission_requirement_schema_ready",
            "application_launch_audit_correlation_schema_ready",
            "application_launch_user_visible_preview_schema_ready",
            "application_launch_approval_handoff_schema_ready",
            "application_launch_denial_handoff_schema_ready",
            "application_launch_execution_blocker_schema_ready",
            "application_launch_review_queue_schema_ready",
            "application_launch_safety_matrix_schema_ready",
            "application_launch_next_controlled_file_schema_ready",
            "no_application_launch_request_creation",
            "no_application_launch_target_resolution",
            "no_application_launch_preview_creation",
            "no_application_launch_preview_render",
            "no_application_launch_approval_handoff",
            "no_application_launch_review_queue_enqueue",
            "no_application_launch_dispatch",
            "no_application_allowlist_resolution",
            "no_application_identity_validation",
            "no_application_executable_resolution",
            "no_application_argument_resolution",
            "no_application_environment_resolution",
            "no_application_process_spawn",
            "no_approved_application_launch",
            "no_approved_project_tool_launch",
            "no_approved_browser_launch",
            "no_approved_editor_launch",
            "no_approved_file_manager_launch",
            "no_shell_application_launch_dispatch",
            "no_os_application_launch_dispatch",
            "no_desktop_application_launch_dispatch",
            "no_launch_without_preview",
            "no_launch_without_explicit_approval",
            "no_launch_without_permission",
            "no_launch_without_audit_correlation",
            "no_launch_non_allowlisted_application",
            "no_launch_arbitrary_executable",
            "no_launch_with_unapproved_arguments",
            "no_launch_privileged_application",
            "no_launch_installer_or_package_manager",
            "no_launch_network_downloader",
            "no_launch_script_or_macro",
            "no_launch_multi_step_chain",
            "no_safe_local_open_dispatch",
            "no_path_access",
            "no_file_read",
            "no_directory_listing",
            "no_action_execution_dispatch",
            "no_action_execution",
            "no_command_execution",
            "no_tool_execution",
            "no_file_mutation",
            "no_desktop_action",
            "no_application_launch",
            "no_network_action",
            "no_git_action",
            "no_memory_write",
            "no_external_upload",
            "no_cloud_fallback",
            "no_autonomous_action",
            "no_permission_state_mutation",
            "no_permission_persistence",
            "no_grant_creation",
            "no_grant_persistence",
            "no_audit_event_creation",
            "no_audit_write",
            "no_audit_persistence",
            "all_safety_blockers_inactive",
        )

        false_keys = (
            "allowlisted_application_launch_runtime_ready",
            "runtime_ready",
            "runtime_activation_allowed",
            "release_gate_open",
            "default_grant",
            "application_launch_runtime_ready",
            "application_launch_request_creation_allowed",
            "application_launch_target_resolution_allowed",
            "application_launch_preview_creation_allowed",
            "application_launch_preview_render_allowed",
            "application_launch_approval_handoff_allowed",
            "application_launch_review_queue_enqueue_allowed",
            "application_launch_dispatch_allowed",
            "application_allowlist_resolution_allowed",
            "application_identity_validation_allowed",
            "application_executable_resolution_allowed",
            "application_argument_resolution_allowed",
            "application_environment_resolution_allowed",
            "application_process_spawn_allowed",
            "approved_application_launch_runtime_ready",
            "approved_project_tool_launch_runtime_ready",
            "approved_browser_launch_runtime_ready",
            "approved_editor_launch_runtime_ready",
            "approved_file_manager_launch_runtime_ready",
            "shell_application_launch_dispatch_allowed",
            "os_application_launch_dispatch_allowed",
            "desktop_application_launch_dispatch_allowed",
            "safe_local_action_handoff_ready",
            "local_open_action_runtime_ready",
            "action_execution_runtime_ready",
            "action_execution_dispatch_allowed",
            "command_execution_allowed",
            "tool_execution_allowed",
            "file_mutation_allowed",
            "desktop_action_allowed",
            "application_launch_allowed",
            "audit_write_allowed",
            "audit_event_packet_creation_allowed",
            "audit_event_write_allowed",
            "audit_log_append_allowed",
            "audit_persistence_allowed",
            "permission_state_mutation_allowed",
            "permission_state_persistence_allowed",
            "grant_packet_creation_allowed",
            "grant_persistence_allowed",
            "application_launch_request_created",
            "application_launch_target_packet_created",
            "application_launch_preview_packet_created",
            "application_launch_allowlist_packet_created",
            "application_launch_permission_requirement_created",
            "application_launch_audit_correlation_created",
            "application_launch_user_visible_preview_created",
            "application_launch_approval_handoff_created",
            "application_launch_denial_handoff_created",
            "application_launch_execution_blocker_created",
            "application_launch_review_queue_item_created",
            "application_launch_action_created",
            "application_launch_action_enqueued",
            "application_launch_action_executed",
            "application_allowlist_resolved",
            "application_identity_validated",
            "application_executable_resolved",
            "application_arguments_resolved",
            "application_environment_resolved",
            "application_process_spawned",
            "approved_application_launched",
            "approved_project_tool_launched",
            "approved_browser_launched",
            "approved_editor_launched",
            "approved_file_manager_launched",
            "shell_application_launch_dispatched",
            "os_application_launch_dispatched",
            "desktop_application_launch_dispatched",
            "safe_local_open_action_executed",
            "action_proposal_created",
            "action_preview_created",
            "action_enqueued",
            "action_executed",
            "command_executed",
            "tool_executed",
            "file_mutated",
            "desktop_action_executed",
            "application_launched",
            "network_action_executed",
            "git_action_executed",
            "memory_written",
            "external_upload_performed",
            "cloud_fallback_used",
            "autonomous_action_performed",
            "permission_state_mutated",
            "permission_grant_created",
            "audit_event_written",
            "audit_event_persisted",
            "audit_log_appended",
            "audit_storage_written",
        )

        assertions: dict[str, bool] = {
            "sprint_215_check_still_clean": s215["failed_assertion_count"] == 0,
            "status_ready": contract["allowlisted_application_launch_status"]
            == "allowlisted_application_launch_contract_ready",
            "current_sprint_216": contract["permission_action_current_sprint"] == 216,
            "next_sprint_217": contract["permission_action_next_sprint"] == 217,
            "next_boundary_controlled_folder_simple_file_creation": contract[
                "permission_action_next_boundary"
            ]
            == "controlled_folder_simple_file_creation",
            "allowed_application_launch_profile_count_expected": contract[
                "allowed_application_launch_profile_count"
            ]
            == len(contract["allowed_application_launch_profile_catalog"]),
            "blocked_application_launch_target_count_expected": contract[
                "blocked_application_launch_target_count"
            ]
            == len(contract["blocked_application_launch_target_catalog"]),
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "allowlisted_application_launch_contract_only",
        }

        for key in true_keys:
            assertions[f"{key}_true"] = contract[key] is True

        for key in false_keys:
            assertions[f"{key}_false"] = contract[key] is False

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s215_failed = [
            f"sprint_215::{name}" for name in s215.get("failed_assertions", [])
        ]
        all_failed = s215_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s215["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "runtime_audit_writer_contract": contract,
            "action_proposal_preview_runtime_contract": contract,
            "safe_local_open_actions_contract": contract,
            "allowlisted_application_launch_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 216 "
                "Allowlisted Application Launch contract without creating launch "
                "requests, previews, approval handoffs, review queue items, "
                "allowlist resolutions, executable resolutions, process spawns, "
                "application launches, desktop actions, app launches, commands, "
                "tools, permission mutations, audit writes, or local action "
                "execution."
            ),
        }

    def _s216_plan(self) -> dict[str, Any]:
        contract = self.allowlisted_application_launch_contract()
        return {
            "name": self.name,
            "sprint": 216,
            "next_sprint": 217,
            "next_boundary": "controlled_folder_simple_file_creation",
            "contract_ready": contract[
                "allowlisted_application_launch_contract_ready"
            ],
            "runtime_ready": contract[
                "allowlisted_application_launch_runtime_ready"
            ],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "application_launch_request": contract[
                    "application_launch_request_schema_ready"
                ],
                "application_launch_target": contract[
                    "application_launch_target_schema_ready"
                ],
                "application_launch_preview": contract[
                    "application_launch_preview_schema_ready"
                ],
                "application_launch_allowlist": contract[
                    "application_launch_allowlist_schema_ready"
                ],
                "application_launch_audit_correlation": contract[
                    "application_launch_audit_correlation_schema_ready"
                ],
                "application_launch_approval_handoff": contract[
                    "application_launch_approval_handoff_schema_ready"
                ],
                "application_launch_review_queue": contract[
                    "application_launch_review_queue_schema_ready"
                ],
            },
            "blocked_runtime": {
                "launch_request_creation": contract[
                    "application_launch_request_creation_allowed"
                ],
                "launch_preview_creation": contract[
                    "application_launch_preview_creation_allowed"
                ],
                "launch_dispatch": contract["application_launch_dispatch_allowed"],
                "process_spawn": contract["application_process_spawn_allowed"],
                "application_launch": contract["application_launch_allowed"],
                "desktop_action": contract["desktop_action_allowed"],
                "command_execution": contract["command_execution_allowed"],
                "tool_execution": contract["tool_execution_allowed"],
                "file_mutation": contract["file_mutation_allowed"],
            },
        }

    ActivePermissionRuntimePlanner.allowlisted_application_launch_contract = (
        _s216_allowlisted_application_launch_contract
    )
    ActivePermissionRuntimePlanner.status = _s216_status
    ActivePermissionRuntimePlanner.check = _s216_check
    ActivePermissionRuntimePlanner.plan = _s216_plan
    ActivePermissionRuntimePlanner._s216_extension_installed = True

# Sprint 217 extension: Controlled Folder and Simple File Creation.
#
# This remains contract-only. It prepares controlled folder creation and simple
# file creation schemas and safety visibility for future approved local file
# creation previews.
# It does not create folders, write files, resolve paths, access paths, list
# directories, read files, mutate files, dispatch commands, run tools, launch
# apps, write audit events, mutate permissions, or execute local actions.
if not getattr(ActivePermissionRuntimePlanner, "_s217_extension_installed", False):
    _S216_STATUS = ActivePermissionRuntimePlanner.status
    _S216_CHECK = ActivePermissionRuntimePlanner.check
    _S216_PLAN = ActivePermissionRuntimePlanner.plan

    def _s217_safety_blockers(self) -> tuple[str, ...]:
        base = tuple(self.allowlisted_application_launch_contract()["safety_blockers"])
        extra = (
            "controlled_folder_simple_file_creation_runtime_active",
            "controlled_creation_request_creation_active",
            "controlled_creation_target_resolution_active",
            "controlled_creation_preview_creation_active",
            "controlled_creation_preview_render_active",
            "controlled_creation_approval_handoff_active",
            "controlled_creation_review_queue_enqueue_active",
            "controlled_creation_dispatch_active",
            "folder_creation_runtime_active",
            "simple_file_creation_runtime_active",
            "project_folder_creation_runtime_active",
            "project_simple_file_creation_runtime_active",
            "parent_path_allowlist_resolution_active",
            "target_path_canonicalization_active",
            "target_path_existence_check_active",
            "target_path_access_active",
            "directory_listing_runtime_active",
            "file_read_runtime_active",
            "file_content_template_resolution_active",
            "file_content_preview_creation_active",
            "file_write_runtime_active",
            "folder_mkdir_runtime_active",
            "filesystem_mutation_runtime_active",
            "shell_file_creation_dispatch_active",
            "os_file_creation_dispatch_active",
            "tool_file_creation_dispatch_active",
            "create_without_preview_active",
            "create_without_approval_active",
            "create_without_permission_active",
            "create_without_audit_correlation_active",
            "create_non_allowlisted_path_active",
            "create_arbitrary_path_active",
            "create_hidden_path_active",
            "create_system_path_active",
            "create_credential_path_active",
            "create_executable_file_active",
            "create_binary_file_active",
            "overwrite_existing_path_active",
            "delete_or_replace_path_active",
            "recursive_bulk_creation_active",
            "multi_step_creation_chain_active",
            "network_path_creation_active",
        )
        return tuple(dict.fromkeys(base + extra))

    def _s217_controlled_folder_simple_file_creation_contract(self) -> dict[str, Any]:
        s216 = self.allowlisted_application_launch_contract()
        blockers = _s217_safety_blockers(self)

        contract: dict[str, Any] = dict(s216)
        contract.update(
            {
                "controlled_folder_simple_file_creation_contract_ready": True,
                "controlled_folder_simple_file_creation_runtime_ready": False,
                "controlled_folder_simple_file_creation_status": "controlled_folder_simple_file_creation_contract_ready",
                "permission_action_block_start": 211,
                "permission_action_block_end": 220,
                "permission_action_current_sprint": 217,
                "permission_action_next_sprint": 218,
                "permission_action_next_boundary": "control_center_approval_workflow",
                "previous_active_permission_runtime_contract_ready": s216[
                    "active_permission_runtime_contract_ready"
                ],
                "previous_grant_denial_expiry_lifecycle_contract_ready": s216[
                    "grant_denial_expiry_lifecycle_contract_ready"
                ],
                "previous_runtime_audit_writer_contract_ready": s216[
                    "runtime_audit_writer_contract_ready"
                ],
                "previous_action_proposal_preview_runtime_contract_ready": s216[
                    "action_proposal_preview_runtime_contract_ready"
                ],
                "previous_safe_local_open_actions_contract_ready": s216[
                    "safe_local_open_actions_contract_ready"
                ],
                "previous_allowlisted_application_launch_contract_ready": s216[
                    "allowlisted_application_launch_contract_ready"
                ],
                "previous_contract_chain_complete": True,
                "contract_only": True,
                "runtime_ready": False,
                "runtime_activation_allowed": False,
                "release_gate_open": False,
                "default_deny": True,
                "default_grant": False,
                "preview_before_create_required": True,
                "explicit_approval_before_create_required": True,
                "permission_before_create_required": True,
                "audit_correlation_before_create_required": True,
                "allowlist_before_create_required": True,
                "canonical_path_before_create_required": True,
                "parent_path_before_create_required": True,
                "safe_content_before_file_create_required": True,
                "single_creation_action_required": True,
                "controlled_creation_request_schema_ready": True,
                "controlled_creation_target_schema_ready": True,
                "controlled_creation_preview_schema_ready": True,
                "controlled_creation_path_policy_schema_ready": True,
                "controlled_creation_allowlist_schema_ready": True,
                "controlled_creation_permission_requirement_schema_ready": True,
                "controlled_creation_audit_correlation_schema_ready": True,
                "controlled_creation_user_visible_preview_schema_ready": True,
                "controlled_creation_approval_handoff_schema_ready": True,
                "controlled_creation_denial_handoff_schema_ready": True,
                "controlled_creation_execution_blocker_schema_ready": True,
                "controlled_creation_review_queue_schema_ready": True,
                "controlled_creation_safety_matrix_schema_ready": True,
                "controlled_creation_next_control_center_schema_ready": True,
                "folder_creation_request_schema_ready": True,
                "folder_creation_target_schema_ready": True,
                "folder_creation_preview_schema_ready": True,
                "simple_file_creation_request_schema_ready": True,
                "simple_file_creation_target_schema_ready": True,
                "simple_file_creation_content_preview_schema_ready": True,
                "simple_file_creation_template_schema_ready": True,
                "allowed_controlled_creation_profile_catalog": [
                    "approved_folder_creation",
                    "approved_project_folder_creation",
                    "simple_text_file_creation",
                    "simple_project_note_file_creation",
                ],
                "allowed_controlled_creation_profile_count": 4,
                "blocked_controlled_creation_target_catalog": [
                    "arbitrary_path",
                    "hidden_path",
                    "system_path",
                    "credential_or_secret_path",
                    "executable_file",
                    "binary_file",
                    "existing_path_overwrite",
                    "delete_or_replace_target",
                    "recursive_bulk_creation",
                    "network_location",
                    "shell_command",
                    "multi_step_automation_chain",
                ],
                "blocked_controlled_creation_target_count": 12,
                "controlled_creation_runtime_ready": False,
                "controlled_creation_request_creation_allowed": False,
                "controlled_creation_target_resolution_allowed": False,
                "controlled_creation_preview_creation_allowed": False,
                "controlled_creation_preview_render_allowed": False,
                "controlled_creation_approval_handoff_allowed": False,
                "controlled_creation_review_queue_enqueue_allowed": False,
                "controlled_creation_dispatch_allowed": False,
                "folder_creation_runtime_ready": False,
                "simple_file_creation_runtime_ready": False,
                "project_folder_creation_runtime_ready": False,
                "project_simple_file_creation_runtime_ready": False,
                "parent_path_allowlist_resolution_allowed": False,
                "target_path_canonicalization_allowed": False,
                "target_path_existence_check_allowed": False,
                "target_path_access_allowed": False,
                "directory_listing_runtime_ready": False,
                "file_read_runtime_ready": False,
                "file_content_template_resolution_allowed": False,
                "file_content_preview_creation_allowed": False,
                "file_write_runtime_ready": False,
                "folder_mkdir_runtime_ready": False,
                "filesystem_mutation_runtime_ready": False,
                "shell_file_creation_dispatch_allowed": False,
                "os_file_creation_dispatch_allowed": False,
                "tool_file_creation_dispatch_allowed": False,
                "safe_local_action_handoff_ready": False,
                "local_open_action_runtime_ready": False,
                "application_launch_runtime_ready": False,
                "action_execution_runtime_ready": False,
                "action_execution_dispatch_allowed": False,
                "command_execution_allowed": False,
                "tool_execution_allowed": False,
                "file_mutation_allowed": False,
                "desktop_action_allowed": False,
                "application_launch_allowed": False,
                "audit_write_allowed": False,
                "audit_event_packet_creation_allowed": False,
                "audit_event_write_allowed": False,
                "audit_log_append_allowed": False,
                "audit_persistence_allowed": False,
                "permission_state_mutation_allowed": False,
                "permission_state_persistence_allowed": False,
                "grant_packet_creation_allowed": False,
                "grant_persistence_allowed": False,
                "controlled_creation_request_created": False,
                "controlled_creation_target_packet_created": False,
                "controlled_creation_preview_packet_created": False,
                "controlled_creation_path_policy_created": False,
                "controlled_creation_allowlist_packet_created": False,
                "controlled_creation_permission_requirement_created": False,
                "controlled_creation_audit_correlation_created": False,
                "controlled_creation_user_visible_preview_created": False,
                "controlled_creation_approval_handoff_created": False,
                "controlled_creation_denial_handoff_created": False,
                "controlled_creation_execution_blocker_created": False,
                "controlled_creation_review_queue_item_created": False,
                "controlled_creation_action_created": False,
                "controlled_creation_action_enqueued": False,
                "controlled_creation_action_executed": False,
                "folder_creation_request_created": False,
                "folder_creation_target_created": False,
                "folder_creation_preview_created": False,
                "simple_file_creation_request_created": False,
                "simple_file_creation_target_created": False,
                "simple_file_creation_content_preview_created": False,
                "simple_file_creation_template_created": False,
                "parent_path_allowlist_resolved": False,
                "target_path_canonicalized": False,
                "target_path_existence_checked": False,
                "target_path_accessed": False,
                "directory_listing_performed": False,
                "file_read_performed": False,
                "file_content_template_resolved": False,
                "file_content_preview_created": False,
                "folder_created": False,
                "project_folder_created": False,
                "simple_file_created": False,
                "project_simple_file_created": False,
                "file_written": False,
                "folder_mkdir_performed": False,
                "filesystem_mutated": False,
                "shell_file_creation_dispatched": False,
                "os_file_creation_dispatched": False,
                "tool_file_creation_dispatched": False,
                "safe_local_open_action_executed": False,
                "approved_folder_opened": False,
                "approved_file_opened": False,
                "project_location_opened": False,
                "dashboard_opened": False,
                "path_accessed": False,
                "application_launch_request_created": False,
                "application_launch_preview_packet_created": False,
                "application_launch_action_executed": False,
                "application_process_spawned": False,
                "approved_application_launched": False,
                "approved_project_tool_launched": False,
                "approved_browser_launched": False,
                "approved_editor_launched": False,
                "approved_file_manager_launched": False,
                "application_launched": False,
                "action_proposal_created": False,
                "action_preview_created": False,
                "action_enqueued": False,
                "action_executed": False,
                "command_executed": False,
                "tool_executed": False,
                "file_mutated": False,
                "desktop_action_executed": False,
                "network_action_executed": False,
                "git_action_executed": False,
                "memory_written": False,
                "external_upload_performed": False,
                "cloud_fallback_used": False,
                "autonomous_action_performed": False,
                "permission_state_mutated": False,
                "permission_grant_created": False,
                "audit_event_written": False,
                "audit_event_persisted": False,
                "audit_log_appended": False,
                "audit_storage_written": False,
                "no_controlled_creation_request_creation": True,
                "no_controlled_creation_target_resolution": True,
                "no_controlled_creation_preview_creation": True,
                "no_controlled_creation_preview_render": True,
                "no_controlled_creation_approval_handoff": True,
                "no_controlled_creation_review_queue_enqueue": True,
                "no_controlled_creation_dispatch": True,
                "no_folder_creation_runtime": True,
                "no_simple_file_creation_runtime": True,
                "no_project_folder_creation_runtime": True,
                "no_project_simple_file_creation_runtime": True,
                "no_parent_path_allowlist_resolution": True,
                "no_target_path_canonicalization": True,
                "no_target_path_existence_check": True,
                "no_target_path_access": True,
                "no_directory_listing": True,
                "no_file_read": True,
                "no_file_content_template_resolution": True,
                "no_file_content_preview_creation": True,
                "no_file_write": True,
                "no_folder_mkdir": True,
                "no_filesystem_mutation": True,
                "no_shell_file_creation_dispatch": True,
                "no_os_file_creation_dispatch": True,
                "no_tool_file_creation_dispatch": True,
                "no_create_without_preview": True,
                "no_create_without_explicit_approval": True,
                "no_create_without_permission": True,
                "no_create_without_audit_correlation": True,
                "no_create_non_allowlisted_path": True,
                "no_create_arbitrary_path": True,
                "no_create_hidden_path": True,
                "no_create_system_path": True,
                "no_create_credential_path": True,
                "no_create_executable_file": True,
                "no_create_binary_file": True,
                "no_overwrite_existing_path": True,
                "no_delete_or_replace_path": True,
                "no_recursive_bulk_creation": True,
                "no_multi_step_creation_chain": True,
                "no_network_path_creation": True,
                "no_safe_local_open_dispatch": True,
                "no_application_launch": True,
                "no_desktop_action": True,
                "no_action_execution_dispatch": True,
                "no_action_execution": True,
                "no_command_execution": True,
                "no_tool_execution": True,
                "no_file_mutation": True,
                "no_network_action": True,
                "no_git_action": True,
                "no_memory_write": True,
                "no_external_upload": True,
                "no_cloud_fallback": True,
                "no_autonomous_action": True,
                "no_permission_state_mutation": True,
                "no_permission_persistence": True,
                "no_grant_creation": True,
                "no_grant_persistence": True,
                "no_audit_event_creation": True,
                "no_audit_write": True,
                "no_audit_persistence": True,
                "runtime_scope": "controlled_folder_simple_file_creation_contract_only",
                "safety_blockers": list(blockers),
                "safety_blocker_count": len(blockers),
            }
        )

        for blocker in blockers:
            contract[blocker] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in blockers
        )

        return contract

    def _s217_status(self) -> dict[str, Any]:
        status = _S216_STATUS(self)
        contract = self.controlled_folder_simple_file_creation_contract()

        status.update(
            {
                "name": self.name,
                "version": self.version,
                "status": "planning",
                "planning_ready": True,
                "runtime_ready": False,
                "controlled_folder_simple_file_creation_contract_ready": contract[
                    "controlled_folder_simple_file_creation_contract_ready"
                ],
                "controlled_folder_simple_file_creation_runtime_ready": contract[
                    "controlled_folder_simple_file_creation_runtime_ready"
                ],
                "controlled_folder_simple_file_creation_status": contract[
                    "controlled_folder_simple_file_creation_status"
                ],
                "permission_action_current_sprint": contract[
                    "permission_action_current_sprint"
                ],
                "permission_action_next_sprint": contract[
                    "permission_action_next_sprint"
                ],
                "permission_action_next_boundary": contract[
                    "permission_action_next_boundary"
                ],
                "previous_contract_chain_complete": contract[
                    "previous_contract_chain_complete"
                ],
                "preview_before_create_required": contract[
                    "preview_before_create_required"
                ],
                "explicit_approval_before_create_required": contract[
                    "explicit_approval_before_create_required"
                ],
                "permission_before_create_required": contract[
                    "permission_before_create_required"
                ],
                "audit_correlation_before_create_required": contract[
                    "audit_correlation_before_create_required"
                ],
                "allowlist_before_create_required": contract[
                    "allowlist_before_create_required"
                ],
                "canonical_path_before_create_required": contract[
                    "canonical_path_before_create_required"
                ],
                "parent_path_before_create_required": contract[
                    "parent_path_before_create_required"
                ],
                "safe_content_before_file_create_required": contract[
                    "safe_content_before_file_create_required"
                ],
                "single_creation_action_required": contract[
                    "single_creation_action_required"
                ],
                "controlled_creation_request_schema_ready": contract[
                    "controlled_creation_request_schema_ready"
                ],
                "controlled_creation_target_schema_ready": contract[
                    "controlled_creation_target_schema_ready"
                ],
                "controlled_creation_preview_schema_ready": contract[
                    "controlled_creation_preview_schema_ready"
                ],
                "controlled_creation_path_policy_schema_ready": contract[
                    "controlled_creation_path_policy_schema_ready"
                ],
                "controlled_creation_allowlist_schema_ready": contract[
                    "controlled_creation_allowlist_schema_ready"
                ],
                "controlled_creation_permission_requirement_schema_ready": contract[
                    "controlled_creation_permission_requirement_schema_ready"
                ],
                "controlled_creation_audit_correlation_schema_ready": contract[
                    "controlled_creation_audit_correlation_schema_ready"
                ],
                "controlled_creation_user_visible_preview_schema_ready": contract[
                    "controlled_creation_user_visible_preview_schema_ready"
                ],
                "controlled_creation_approval_handoff_schema_ready": contract[
                    "controlled_creation_approval_handoff_schema_ready"
                ],
                "controlled_creation_review_queue_schema_ready": contract[
                    "controlled_creation_review_queue_schema_ready"
                ],
                "folder_creation_request_schema_ready": contract[
                    "folder_creation_request_schema_ready"
                ],
                "folder_creation_target_schema_ready": contract[
                    "folder_creation_target_schema_ready"
                ],
                "folder_creation_preview_schema_ready": contract[
                    "folder_creation_preview_schema_ready"
                ],
                "simple_file_creation_request_schema_ready": contract[
                    "simple_file_creation_request_schema_ready"
                ],
                "simple_file_creation_target_schema_ready": contract[
                    "simple_file_creation_target_schema_ready"
                ],
                "simple_file_creation_content_preview_schema_ready": contract[
                    "simple_file_creation_content_preview_schema_ready"
                ],
                "allowed_controlled_creation_profile_count": contract[
                    "allowed_controlled_creation_profile_count"
                ],
                "blocked_controlled_creation_target_count": contract[
                    "blocked_controlled_creation_target_count"
                ],
                "controlled_creation_runtime_ready": contract[
                    "controlled_creation_runtime_ready"
                ],
                "controlled_creation_request_creation_allowed": contract[
                    "controlled_creation_request_creation_allowed"
                ],
                "controlled_creation_preview_creation_allowed": contract[
                    "controlled_creation_preview_creation_allowed"
                ],
                "controlled_creation_dispatch_allowed": contract[
                    "controlled_creation_dispatch_allowed"
                ],
                "folder_creation_runtime_ready": contract[
                    "folder_creation_runtime_ready"
                ],
                "simple_file_creation_runtime_ready": contract[
                    "simple_file_creation_runtime_ready"
                ],
                "project_folder_creation_runtime_ready": contract[
                    "project_folder_creation_runtime_ready"
                ],
                "project_simple_file_creation_runtime_ready": contract[
                    "project_simple_file_creation_runtime_ready"
                ],
                "parent_path_allowlist_resolution_allowed": contract[
                    "parent_path_allowlist_resolution_allowed"
                ],
                "target_path_canonicalization_allowed": contract[
                    "target_path_canonicalization_allowed"
                ],
                "target_path_access_allowed": contract[
                    "target_path_access_allowed"
                ],
                "directory_listing_runtime_ready": contract[
                    "directory_listing_runtime_ready"
                ],
                "file_read_runtime_ready": contract["file_read_runtime_ready"],
                "file_write_runtime_ready": contract["file_write_runtime_ready"],
                "folder_mkdir_runtime_ready": contract["folder_mkdir_runtime_ready"],
                "filesystem_mutation_runtime_ready": contract[
                    "filesystem_mutation_runtime_ready"
                ],
                "file_mutation_allowed": contract["file_mutation_allowed"],
                "desktop_action_allowed": contract["desktop_action_allowed"],
                "application_launch_allowed": contract["application_launch_allowed"],
                "controlled_creation_request_created": contract[
                    "controlled_creation_request_created"
                ],
                "controlled_creation_preview_packet_created": contract[
                    "controlled_creation_preview_packet_created"
                ],
                "controlled_creation_approval_handoff_created": contract[
                    "controlled_creation_approval_handoff_created"
                ],
                "controlled_creation_review_queue_item_created": contract[
                    "controlled_creation_review_queue_item_created"
                ],
                "controlled_creation_action_executed": contract[
                    "controlled_creation_action_executed"
                ],
                "folder_creation_request_created": contract[
                    "folder_creation_request_created"
                ],
                "simple_file_creation_request_created": contract[
                    "simple_file_creation_request_created"
                ],
                "parent_path_allowlist_resolved": contract[
                    "parent_path_allowlist_resolved"
                ],
                "target_path_canonicalized": contract["target_path_canonicalized"],
                "target_path_accessed": contract["target_path_accessed"],
                "directory_listing_performed": contract[
                    "directory_listing_performed"
                ],
                "file_read_performed": contract["file_read_performed"],
                "folder_created": contract["folder_created"],
                "project_folder_created": contract["project_folder_created"],
                "simple_file_created": contract["simple_file_created"],
                "project_simple_file_created": contract[
                    "project_simple_file_created"
                ],
                "file_written": contract["file_written"],
                "folder_mkdir_performed": contract["folder_mkdir_performed"],
                "filesystem_mutated": contract["filesystem_mutated"],
                "file_mutated": contract["file_mutated"],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
                "audit_event_written": contract["audit_event_written"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "no_controlled_creation_request_creation": contract[
                    "no_controlled_creation_request_creation"
                ],
                "no_controlled_creation_preview_creation": contract[
                    "no_controlled_creation_preview_creation"
                ],
                "no_controlled_creation_dispatch": contract[
                    "no_controlled_creation_dispatch"
                ],
                "no_folder_creation_runtime": contract[
                    "no_folder_creation_runtime"
                ],
                "no_simple_file_creation_runtime": contract[
                    "no_simple_file_creation_runtime"
                ],
                "no_parent_path_allowlist_resolution": contract[
                    "no_parent_path_allowlist_resolution"
                ],
                "no_target_path_canonicalization": contract[
                    "no_target_path_canonicalization"
                ],
                "no_target_path_access": contract["no_target_path_access"],
                "no_directory_listing": contract["no_directory_listing"],
                "no_file_read": contract["no_file_read"],
                "no_file_write": contract["no_file_write"],
                "no_folder_mkdir": contract["no_folder_mkdir"],
                "no_filesystem_mutation": contract["no_filesystem_mutation"],
                "no_create_without_preview": contract[
                    "no_create_without_preview"
                ],
                "no_create_without_explicit_approval": contract[
                    "no_create_without_explicit_approval"
                ],
                "no_create_without_permission": contract[
                    "no_create_without_permission"
                ],
                "no_create_non_allowlisted_path": contract[
                    "no_create_non_allowlisted_path"
                ],
                "no_create_arbitrary_path": contract["no_create_arbitrary_path"],
                "no_overwrite_existing_path": contract[
                    "no_overwrite_existing_path"
                ],
                "no_recursive_bulk_creation": contract[
                    "no_recursive_bulk_creation"
                ],
                "no_multi_step_creation_chain": contract[
                    "no_multi_step_creation_chain"
                ],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_application_launch": contract["no_application_launch"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "runtime_scope": contract["runtime_scope"],
                "controlled_folder_simple_file_creation_contract": contract,
                "contract": contract,
                "note": (
                    "Controlled Folder and Simple File Creation contract is "
                    "ready for Sprint 217; it prepares folder/file creation "
                    "previews without resolving paths, creating folders, "
                    "writing files, mutating the filesystem, dispatching "
                    "commands, or executing local actions."
                ),
            }
        )
        return status

    def _s217_check(self) -> dict[str, Any]:
        s216 = _S216_CHECK(self)
        contract = self.controlled_folder_simple_file_creation_contract()

        true_keys = (
            "controlled_folder_simple_file_creation_contract_ready",
            "previous_active_permission_runtime_contract_ready",
            "previous_grant_denial_expiry_lifecycle_contract_ready",
            "previous_runtime_audit_writer_contract_ready",
            "previous_action_proposal_preview_runtime_contract_ready",
            "previous_safe_local_open_actions_contract_ready",
            "previous_allowlisted_application_launch_contract_ready",
            "previous_contract_chain_complete",
            "contract_only",
            "default_deny",
            "preview_before_create_required",
            "explicit_approval_before_create_required",
            "permission_before_create_required",
            "audit_correlation_before_create_required",
            "allowlist_before_create_required",
            "canonical_path_before_create_required",
            "parent_path_before_create_required",
            "safe_content_before_file_create_required",
            "single_creation_action_required",
            "controlled_creation_request_schema_ready",
            "controlled_creation_target_schema_ready",
            "controlled_creation_preview_schema_ready",
            "controlled_creation_path_policy_schema_ready",
            "controlled_creation_allowlist_schema_ready",
            "controlled_creation_permission_requirement_schema_ready",
            "controlled_creation_audit_correlation_schema_ready",
            "controlled_creation_user_visible_preview_schema_ready",
            "controlled_creation_approval_handoff_schema_ready",
            "controlled_creation_denial_handoff_schema_ready",
            "controlled_creation_execution_blocker_schema_ready",
            "controlled_creation_review_queue_schema_ready",
            "controlled_creation_safety_matrix_schema_ready",
            "controlled_creation_next_control_center_schema_ready",
            "folder_creation_request_schema_ready",
            "folder_creation_target_schema_ready",
            "folder_creation_preview_schema_ready",
            "simple_file_creation_request_schema_ready",
            "simple_file_creation_target_schema_ready",
            "simple_file_creation_content_preview_schema_ready",
            "simple_file_creation_template_schema_ready",
            "no_controlled_creation_request_creation",
            "no_controlled_creation_target_resolution",
            "no_controlled_creation_preview_creation",
            "no_controlled_creation_preview_render",
            "no_controlled_creation_approval_handoff",
            "no_controlled_creation_review_queue_enqueue",
            "no_controlled_creation_dispatch",
            "no_folder_creation_runtime",
            "no_simple_file_creation_runtime",
            "no_project_folder_creation_runtime",
            "no_project_simple_file_creation_runtime",
            "no_parent_path_allowlist_resolution",
            "no_target_path_canonicalization",
            "no_target_path_existence_check",
            "no_target_path_access",
            "no_directory_listing",
            "no_file_read",
            "no_file_content_template_resolution",
            "no_file_content_preview_creation",
            "no_file_write",
            "no_folder_mkdir",
            "no_filesystem_mutation",
            "no_shell_file_creation_dispatch",
            "no_os_file_creation_dispatch",
            "no_tool_file_creation_dispatch",
            "no_create_without_preview",
            "no_create_without_explicit_approval",
            "no_create_without_permission",
            "no_create_without_audit_correlation",
            "no_create_non_allowlisted_path",
            "no_create_arbitrary_path",
            "no_create_hidden_path",
            "no_create_system_path",
            "no_create_credential_path",
            "no_create_executable_file",
            "no_create_binary_file",
            "no_overwrite_existing_path",
            "no_delete_or_replace_path",
            "no_recursive_bulk_creation",
            "no_multi_step_creation_chain",
            "no_network_path_creation",
            "no_safe_local_open_dispatch",
            "no_application_launch",
            "no_desktop_action",
            "no_action_execution_dispatch",
            "no_action_execution",
            "no_command_execution",
            "no_tool_execution",
            "no_file_mutation",
            "no_network_action",
            "no_git_action",
            "no_memory_write",
            "no_external_upload",
            "no_cloud_fallback",
            "no_autonomous_action",
            "no_permission_state_mutation",
            "no_permission_persistence",
            "no_grant_creation",
            "no_grant_persistence",
            "no_audit_event_creation",
            "no_audit_write",
            "no_audit_persistence",
            "all_safety_blockers_inactive",
        )

        false_keys = (
            "controlled_folder_simple_file_creation_runtime_ready",
            "runtime_ready",
            "runtime_activation_allowed",
            "release_gate_open",
            "default_grant",
            "controlled_creation_runtime_ready",
            "controlled_creation_request_creation_allowed",
            "controlled_creation_target_resolution_allowed",
            "controlled_creation_preview_creation_allowed",
            "controlled_creation_preview_render_allowed",
            "controlled_creation_approval_handoff_allowed",
            "controlled_creation_review_queue_enqueue_allowed",
            "controlled_creation_dispatch_allowed",
            "folder_creation_runtime_ready",
            "simple_file_creation_runtime_ready",
            "project_folder_creation_runtime_ready",
            "project_simple_file_creation_runtime_ready",
            "parent_path_allowlist_resolution_allowed",
            "target_path_canonicalization_allowed",
            "target_path_existence_check_allowed",
            "target_path_access_allowed",
            "directory_listing_runtime_ready",
            "file_read_runtime_ready",
            "file_content_template_resolution_allowed",
            "file_content_preview_creation_allowed",
            "file_write_runtime_ready",
            "folder_mkdir_runtime_ready",
            "filesystem_mutation_runtime_ready",
            "shell_file_creation_dispatch_allowed",
            "os_file_creation_dispatch_allowed",
            "tool_file_creation_dispatch_allowed",
            "safe_local_action_handoff_ready",
            "local_open_action_runtime_ready",
            "application_launch_runtime_ready",
            "action_execution_runtime_ready",
            "action_execution_dispatch_allowed",
            "command_execution_allowed",
            "tool_execution_allowed",
            "file_mutation_allowed",
            "desktop_action_allowed",
            "application_launch_allowed",
            "audit_write_allowed",
            "audit_event_packet_creation_allowed",
            "audit_event_write_allowed",
            "audit_log_append_allowed",
            "audit_persistence_allowed",
            "permission_state_mutation_allowed",
            "permission_state_persistence_allowed",
            "grant_packet_creation_allowed",
            "grant_persistence_allowed",
            "controlled_creation_request_created",
            "controlled_creation_target_packet_created",
            "controlled_creation_preview_packet_created",
            "controlled_creation_path_policy_created",
            "controlled_creation_allowlist_packet_created",
            "controlled_creation_permission_requirement_created",
            "controlled_creation_audit_correlation_created",
            "controlled_creation_user_visible_preview_created",
            "controlled_creation_approval_handoff_created",
            "controlled_creation_denial_handoff_created",
            "controlled_creation_execution_blocker_created",
            "controlled_creation_review_queue_item_created",
            "controlled_creation_action_created",
            "controlled_creation_action_enqueued",
            "controlled_creation_action_executed",
            "folder_creation_request_created",
            "folder_creation_target_created",
            "folder_creation_preview_created",
            "simple_file_creation_request_created",
            "simple_file_creation_target_created",
            "simple_file_creation_content_preview_created",
            "simple_file_creation_template_created",
            "parent_path_allowlist_resolved",
            "target_path_canonicalized",
            "target_path_existence_checked",
            "target_path_accessed",
            "directory_listing_performed",
            "file_read_performed",
            "file_content_template_resolved",
            "file_content_preview_created",
            "folder_created",
            "project_folder_created",
            "simple_file_created",
            "project_simple_file_created",
            "file_written",
            "folder_mkdir_performed",
            "filesystem_mutated",
            "shell_file_creation_dispatched",
            "os_file_creation_dispatched",
            "tool_file_creation_dispatched",
            "safe_local_open_action_executed",
            "approved_folder_opened",
            "approved_file_opened",
            "project_location_opened",
            "dashboard_opened",
            "path_accessed",
            "application_launch_request_created",
            "application_launch_preview_packet_created",
            "application_launch_action_executed",
            "application_process_spawned",
            "approved_application_launched",
            "approved_project_tool_launched",
            "approved_browser_launched",
            "approved_editor_launched",
            "approved_file_manager_launched",
            "application_launched",
            "action_proposal_created",
            "action_preview_created",
            "action_enqueued",
            "action_executed",
            "command_executed",
            "tool_executed",
            "file_mutated",
            "desktop_action_executed",
            "network_action_executed",
            "git_action_executed",
            "memory_written",
            "external_upload_performed",
            "cloud_fallback_used",
            "autonomous_action_performed",
            "permission_state_mutated",
            "permission_grant_created",
            "audit_event_written",
            "audit_event_persisted",
            "audit_log_appended",
            "audit_storage_written",
        )

        assertions: dict[str, bool] = {
            "sprint_216_check_still_clean": s216["failed_assertion_count"] == 0,
            "status_ready": contract["controlled_folder_simple_file_creation_status"]
            == "controlled_folder_simple_file_creation_contract_ready",
            "current_sprint_217": contract["permission_action_current_sprint"] == 217,
            "next_sprint_218": contract["permission_action_next_sprint"] == 218,
            "next_boundary_control_center_approval_workflow": contract[
                "permission_action_next_boundary"
            ]
            == "control_center_approval_workflow",
            "allowed_controlled_creation_profile_count_expected": contract[
                "allowed_controlled_creation_profile_count"
            ]
            == len(contract["allowed_controlled_creation_profile_catalog"]),
            "blocked_controlled_creation_target_count_expected": contract[
                "blocked_controlled_creation_target_count"
            ]
            == len(contract["blocked_controlled_creation_target_catalog"]),
            "safety_blocker_count_expected": contract["safety_blocker_count"]
            == len(contract["safety_blockers"]),
            "runtime_scope_contract_only": contract["runtime_scope"]
            == "controlled_folder_simple_file_creation_contract_only",
        }

        for key in true_keys:
            assertions[f"{key}_true"] = contract[key] is True

        for key in false_keys:
            assertions[f"{key}_false"] = contract[key] is False

        for blocker in contract["safety_blockers"]:
            assertions[f"{blocker}_inactive"] = contract[blocker] is False

        failed_assertions = [name for name, passed in assertions.items() if not passed]
        s216_failed = [
            f"sprint_216::{name}" for name in s216.get("failed_assertions", [])
        ]
        all_failed = s216_failed + failed_assertions

        return {
            "status": "checked",
            "planning_ready": True,
            "runtime_ready": False,
            "assertion_count": int(s216["assertion_count"]) + len(assertions),
            "failed_assertion_count": len(all_failed),
            "failed_assertions": all_failed,
            "permission_action_current_sprint": contract[
                "permission_action_current_sprint"
            ],
            "permission_action_next_sprint": contract[
                "permission_action_next_sprint"
            ],
            "permission_action_next_boundary": contract[
                "permission_action_next_boundary"
            ],
            "active_permission_runtime_contract": contract,
            "grant_denial_expiry_lifecycle_contract": contract,
            "runtime_audit_writer_contract": contract,
            "action_proposal_preview_runtime_contract": contract,
            "safe_local_open_actions_contract": contract,
            "allowlisted_application_launch_contract": contract,
            "controlled_folder_simple_file_creation_contract": contract,
            "note": (
                "Runtime is not enabled yet. This check prepared the Sprint 217 "
                "Controlled Folder and Simple File Creation contract without "
                "creating folders, writing files, resolving paths, accessing "
                "paths, listing directories, reading files, mutating the "
                "filesystem, dispatching commands, running tools, mutating "
                "permissions, writing audit events, or executing local actions."
            ),
        }

    def _s217_plan(self) -> dict[str, Any]:
        contract = self.controlled_folder_simple_file_creation_contract()
        return {
            "name": self.name,
            "sprint": 217,
            "next_sprint": 218,
            "next_boundary": "control_center_approval_workflow",
            "contract_ready": contract[
                "controlled_folder_simple_file_creation_contract_ready"
            ],
            "runtime_ready": contract[
                "controlled_folder_simple_file_creation_runtime_ready"
            ],
            "runtime_scope": contract["runtime_scope"],
            "schemas_ready": {
                "controlled_creation_request": contract[
                    "controlled_creation_request_schema_ready"
                ],
                "controlled_creation_target": contract[
                    "controlled_creation_target_schema_ready"
                ],
                "controlled_creation_preview": contract[
                    "controlled_creation_preview_schema_ready"
                ],
                "controlled_creation_path_policy": contract[
                    "controlled_creation_path_policy_schema_ready"
                ],
                "controlled_creation_allowlist": contract[
                    "controlled_creation_allowlist_schema_ready"
                ],
                "folder_creation_request": contract[
                    "folder_creation_request_schema_ready"
                ],
                "simple_file_creation_request": contract[
                    "simple_file_creation_request_schema_ready"
                ],
            },
            "blocked_runtime": {
                "controlled_creation_request_creation": contract[
                    "controlled_creation_request_creation_allowed"
                ],
                "controlled_creation_preview_creation": contract[
                    "controlled_creation_preview_creation_allowed"
                ],
                "controlled_creation_dispatch": contract[
                    "controlled_creation_dispatch_allowed"
                ],
                "folder_creation_runtime": contract["folder_creation_runtime_ready"],
                "simple_file_creation_runtime": contract[
                    "simple_file_creation_runtime_ready"
                ],
                "file_write_runtime": contract["file_write_runtime_ready"],
                "folder_mkdir_runtime": contract["folder_mkdir_runtime_ready"],
                "filesystem_mutation_runtime": contract[
                    "filesystem_mutation_runtime_ready"
                ],
                "file_mutation": contract["file_mutation_allowed"],
                "command_execution": contract["command_execution_allowed"],
                "tool_execution": contract["tool_execution_allowed"],
            },
        }

    ActivePermissionRuntimePlanner.controlled_folder_simple_file_creation_contract = (
        _s217_controlled_folder_simple_file_creation_contract
    )
    ActivePermissionRuntimePlanner.status = _s217_status
    ActivePermissionRuntimePlanner.check = _s217_check
    ActivePermissionRuntimePlanner.plan = _s217_plan
    ActivePermissionRuntimePlanner._s217_extension_installed = True
