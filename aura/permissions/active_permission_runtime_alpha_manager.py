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

# Sprint 212 extension: alpha visibility for Grant, Denial, and Expiry Lifecycle.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s212_extension_installed", False):
    _S211_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s212_alpha_status(self) -> dict[str, Any]:
        status = _S211_ALPHA_STATUS(self)
        contract = self.planner.grant_denial_expiry_lifecycle_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_212_grant_denial_expiry_lifecycle_contract_ready": contract[
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
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 2,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 212 "
                    "grant, denial, and expiry lifecycle visibility without "
                    "creating grants, mutating permission state, writing audit "
                    "events, or executing local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s212_alpha_status
    ActivePermissionRuntimeAlphaManager._s212_extension_installed = True

# Sprint 213 extension: alpha visibility for Runtime Audit Writer.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s213_extension_installed", False):
    _S212_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s213_alpha_status(self) -> dict[str, Any]:
        status = _S212_ALPHA_STATUS(self)
        contract = self.planner.runtime_audit_writer_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_213_runtime_audit_writer_contract_ready": contract[
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
                "audit_permission_lifecycle_link_schema_ready": contract[
                    "audit_permission_lifecycle_link_schema_ready"
                ],
                "audit_review_queue_packet_schema_ready": contract[
                    "audit_review_queue_packet_schema_ready"
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
                "audit_review_queue_enqueue_allowed": contract[
                    "audit_review_queue_enqueue_allowed"
                ],
                "audit_event_packet_created": contract[
                    "audit_event_packet_created"
                ],
                "audit_write_request_created": contract["audit_write_request_created"],
                "audit_write_decision_created": contract[
                    "audit_write_decision_created"
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
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 3,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 213 "
                    "Runtime Audit Writer visibility without creating audit "
                    "packets, writing audit events, appending audit logs, "
                    "persisting audit data, mutating permissions, or executing "
                    "local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s213_alpha_status
    ActivePermissionRuntimeAlphaManager._s213_extension_installed = True

# Sprint 214 extension: alpha visibility for Action Proposal and Preview Runtime.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s214_extension_installed", False):
    _S213_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s214_alpha_status(self) -> dict[str, Any]:
        status = _S213_ALPHA_STATUS(self)
        contract = self.planner.action_proposal_preview_runtime_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_214_action_proposal_preview_contract_ready": contract[
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
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_application_launch": contract["no_application_launch"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 4,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 214 "
                    "Action Proposal and Preview visibility without creating "
                    "proposals, previews, approval handoffs, queue items, "
                    "mutating files, launching apps, or executing local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s214_alpha_status
    ActivePermissionRuntimeAlphaManager._s214_extension_installed = True

# Sprint 215 extension: alpha visibility for Safe Local Open Actions.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s215_extension_installed", False):
    _S214_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s215_alpha_status(self) -> dict[str, Any]:
        status = _S214_ALPHA_STATUS(self)
        contract = self.planner.safe_local_open_actions_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_215_safe_local_open_actions_contract_ready": contract[
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
                "safe_local_open_preview_creation_allowed": contract[
                    "safe_local_open_preview_creation_allowed"
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
                "path_access_runtime_ready": contract["path_access_runtime_ready"],
                "file_read_runtime_ready": contract["file_read_runtime_ready"],
                "directory_listing_runtime_ready": contract[
                    "directory_listing_runtime_ready"
                ],
                "shell_open_dispatch_allowed": contract[
                    "shell_open_dispatch_allowed"
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
                "safe_local_open_preview_packet_created": contract[
                    "safe_local_open_preview_packet_created"
                ],
                "safe_local_open_approval_handoff_created": contract[
                    "safe_local_open_approval_handoff_created"
                ],
                "safe_local_open_review_queue_item_created": contract[
                    "safe_local_open_review_queue_item_created"
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
                "file_manager_launched": contract["file_manager_launched"],
                "action_executed": contract["action_executed"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "file_mutated": contract["file_mutated"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "application_launched": contract["application_launched"],
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
                "no_open_non_allowlisted_path": contract[
                    "no_open_non_allowlisted_path"
                ],
                "no_open_arbitrary_path": contract["no_open_arbitrary_path"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 5,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 215 "
                    "Safe Local Open Actions visibility without opening files, "
                    "accessing paths, reading files, launching apps, mutating "
                    "files, or executing local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s215_alpha_status
    ActivePermissionRuntimeAlphaManager._s215_extension_installed = True

# Sprint 216 extension: alpha visibility for Allowlisted Application Launch.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s216_extension_installed", False):
    _S215_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s216_alpha_status(self) -> dict[str, Any]:
        status = _S215_ALPHA_STATUS(self)
        contract = self.planner.allowlisted_application_launch_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_216_allowlisted_application_launch_contract_ready": contract[
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
                "application_launch_preview_creation_allowed": contract[
                    "application_launch_preview_creation_allowed"
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
                "application_launched": contract["application_launched"],
                "desktop_action_executed": contract["desktop_action_executed"],
                "file_mutated": contract["file_mutated"],
                "command_executed": contract["command_executed"],
                "tool_executed": contract["tool_executed"],
                "audit_event_written": contract["audit_event_written"],
                "permission_state_mutated": contract["permission_state_mutated"],
                "no_application_launch_request_creation": contract[
                    "no_application_launch_request_creation"
                ],
                "no_application_launch_preview_creation": contract[
                    "no_application_launch_preview_creation"
                ],
                "no_application_launch_dispatch": contract[
                    "no_application_launch_dispatch"
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
                "no_launch_non_allowlisted_application": contract[
                    "no_launch_non_allowlisted_application"
                ],
                "no_launch_arbitrary_executable": contract[
                    "no_launch_arbitrary_executable"
                ],
                "no_application_launch": contract["no_application_launch"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_file_mutation": contract["no_file_mutation"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 6,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 216 "
                    "Allowlisted Application Launch visibility without resolving "
                    "executables, spawning processes, dispatching launches, "
                    "launching apps, mutating files, or executing local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s216_alpha_status
    ActivePermissionRuntimeAlphaManager._s216_extension_installed = True

# Sprint 217 extension: alpha visibility for Controlled Folder and Simple File Creation.
if not getattr(ActivePermissionRuntimeAlphaManager, "_s217_extension_installed", False):
    _S216_ALPHA_STATUS = ActivePermissionRuntimeAlphaManager.status

    def _s217_alpha_status(self) -> dict[str, Any]:
        status = _S216_ALPHA_STATUS(self)
        contract = self.planner.controlled_folder_simple_file_creation_contract()
        check = self.planner.check()

        status.update(
            {
                "sprint_217_controlled_folder_simple_file_creation_contract_ready": contract[
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
                "simple_file_creation_request_schema_ready": contract[
                    "simple_file_creation_request_schema_ready"
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
                "no_file_write": contract["no_file_write"],
                "no_folder_mkdir": contract["no_folder_mkdir"],
                "no_filesystem_mutation": contract["no_filesystem_mutation"],
                "no_create_without_preview": contract[
                    "no_create_without_preview"
                ],
                "no_create_without_explicit_approval": contract[
                    "no_create_without_explicit_approval"
                ],
                "no_create_arbitrary_path": contract["no_create_arbitrary_path"],
                "no_overwrite_existing_path": contract[
                    "no_overwrite_existing_path"
                ],
                "no_recursive_bulk_creation": contract[
                    "no_recursive_bulk_creation"
                ],
                "no_file_mutation": contract["no_file_mutation"],
                "no_desktop_action": contract["no_desktop_action"],
                "no_application_launch": contract["no_application_launch"],
                "safety_blocker_count": contract["safety_blocker_count"],
                "all_safety_blockers_inactive": contract[
                    "all_safety_blockers_inactive"
                ],
                "assertion_count": check["assertion_count"],
                "failed_assertion_count": check["failed_assertion_count"],
                "failed_assertions": check["failed_assertions"],
                "runtime_scope": contract["runtime_scope"],
                "sections": 7,
                "note": (
                    "Active Permission Runtime Alpha now exposes Sprint 217 "
                    "Controlled Folder and Simple File Creation visibility "
                    "without resolving paths, creating folders, writing files, "
                    "mutating the filesystem, dispatching commands, or executing "
                    "local actions."
                ),
            }
        )
        return status

    ActivePermissionRuntimeAlphaManager.status = _s217_alpha_status
    ActivePermissionRuntimeAlphaManager._s217_extension_installed = True
