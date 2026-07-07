
"""AURA Controlled File Write Approval Draft Foundation.

Planner-only/draft-only foundation for future controlled file write approval.
It prepares file write proposal drafts, target path policies, diff preview
contracts, overwrite rules, backup requirements, approval checklists,
rollback notes, audit visibility fields, and safety policy without reading,
writing, modifying, deleting, backing up, overwriting, or rolling back files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraControlledFileWriteApprovalDraftFoundationManager:
    """Prepare controlled file write approval drafts without file runtime."""

    name = "aura_controlled_file_write_approval_draft_foundation"
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

    def approval_draft_plan_types(self) -> list[str]:
        return [
            "controlled_file_write_approval_draft_status",
            "file_write_proposal_draft_plan",
            "target_path_policy_plan",
            "diff_preview_contract_plan",
            "overwrite_rule_plan",
            "backup_requirement_plan",
            "approval_checklist_plan",
            "rollback_note_plan",
            "file_write_audit_visibility_plan",
            "file_write_safety_policy_plan",
            "controlled_file_write_approval_draft_context",
        ]

    def approval_draft_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "draft_name": "AURA Controlled File Write Approval Draft Foundation",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_mode": "approval_draft_only",
            "runtime_mode": "pre_file_write_runtime",
            "file_write_authority": "ATLAS",
            "future_write_scope": "explicit_user_approval_required",
            "file_write_allowed": False,
            "file_read_allowed": False,
            "file_modify_allowed": False,
            "file_delete_allowed": False,
            "overwrite_allowed": False,
            "backup_creation_allowed": False,
            "rollback_execution_allowed": False,
            "command_execution_allowed": False,
        }

    def file_write_proposal_drafts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "create_new_file_proposal",
                "purpose": "Future proposal for creating a new file after explicit approval.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "append_file_proposal",
                "purpose": "Future proposal for appending content to an approved file.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "replace_file_proposal",
                "purpose": "Future proposal for replacing an approved file with preview and approval.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "patch_file_proposal",
                "purpose": "Future proposal for applying a controlled patch.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "template_file_proposal",
                "purpose": "Future proposal for creating a file from an approved template.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "config_file_proposal",
                "purpose": "Future proposal for editing explicit safe configuration files.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "documentation_file_proposal",
                "purpose": "Future proposal for writing docs after preview.",
                "runtime_file_write_enabled": False,
            },
            {
                "id": "generated_asset_manifest_proposal",
                "purpose": "Future proposal for writing generated asset manifests.",
                "runtime_file_write_enabled": False,
            },
        ]

    def target_path_policies(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "project_root_scope_policy",
                "purpose": "Future file writes must be constrained to approved project/workspace paths.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "explicit_target_path_required",
                "purpose": "Future writes must require an explicit target path.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "path_traversal_denied",
                "purpose": "Future writes must deny path traversal outside approved scope.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "home_directory_denied_by_default",
                "purpose": "Future writes must not target the user's home directory by default.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "system_directory_denied",
                "purpose": "Future writes must deny system directories.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "secret_path_denied",
                "purpose": "Future writes must deny env, key, token, credential, and secret paths.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "binary_path_requires_extra_review",
                "purpose": "Future binary writes must require separate review.",
                "runtime_path_check_enabled": False,
            },
            {
                "id": "path_policy_audit_visibility",
                "purpose": "Future path policy decisions must be visible in audit.",
                "runtime_path_check_enabled": False,
            },
        ]

    def diff_preview_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "before_after_preview",
                "purpose": "Future write proposal should show before/after preview where applicable.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "unified_diff_preview",
                "purpose": "Future write proposal should show unified diff for text changes.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "new_file_preview",
                "purpose": "Future new file proposal should show full content preview.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "append_preview",
                "purpose": "Future append proposal should show appended section clearly.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "line_count_summary",
                "purpose": "Future diff preview should show changed line counts.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "risk_summary_preview",
                "purpose": "Future preview should summarize file write risk.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "target_path_preview",
                "purpose": "Future preview should show target path and write mode.",
                "runtime_diff_enabled": False,
            },
            {
                "id": "approval_prompt_preview",
                "purpose": "Future preview should show exact approval prompt before write.",
                "runtime_diff_enabled": False,
            },
        ]

    def overwrite_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "no_overwrite_by_default",
                "purpose": "Future writes must not overwrite existing files by default.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "explicit_overwrite_approval_required",
                "purpose": "Future overwrite requires explicit user approval.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "overwrite_preview_required",
                "purpose": "Future overwrite requires diff/preview.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "overwrite_backup_required",
                "purpose": "Future overwrite requires backup plan.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "protected_file_overwrite_denied",
                "purpose": "Future overwrite of protected files is denied by default.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "multi_file_overwrite_requires_batch_review",
                "purpose": "Future multi-file overwrite requires batch review.",
                "runtime_overwrite_enabled": False,
            },
            {
                "id": "overwrite_audit_visibility",
                "purpose": "Future overwrite intent must be visible in audit.",
                "runtime_overwrite_enabled": False,
            },
        ]

    def backup_requirements(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "backup_before_replace",
                "purpose": "Future replace/overwrite should require backup before write.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_location_policy",
                "purpose": "Future backup path must stay within approved backup boundary.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_manifest_note",
                "purpose": "Future backup should include manifest metadata.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_retention_note",
                "purpose": "Future backup retention must be clear before write.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_failure_blocks_write",
                "purpose": "Future write must stop if required backup fails.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_restore_reference",
                "purpose": "Future backup should link to rollback notes.",
                "runtime_backup_enabled": False,
            },
            {
                "id": "backup_audit_visibility",
                "purpose": "Future backup decision must be visible in audit.",
                "runtime_backup_enabled": False,
            },
        ]

    def approval_checklist_items(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "target_path_confirmed",
                "purpose": "User confirms the exact target path.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "write_mode_confirmed",
                "purpose": "User confirms create/append/replace/patch mode.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "diff_preview_reviewed",
                "purpose": "User reviews preview/diff before write.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "overwrite_risk_reviewed",
                "purpose": "User reviews overwrite risk when applicable.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "backup_requirement_reviewed",
                "purpose": "User reviews backup requirement before write.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "rollback_note_reviewed",
                "purpose": "User reviews rollback notes before write.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "permission_reference_attached",
                "purpose": "Future write links to permission review queue reference.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "single_action_scope_confirmed",
                "purpose": "User confirms the write is one scoped action.",
                "runtime_approval_enabled": False,
            },
            {
                "id": "final_user_approval_required",
                "purpose": "Final explicit approval is required before runtime write.",
                "runtime_approval_enabled": False,
            },
        ]

    def rollback_notes(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "rollback_not_executed_by_default",
                "purpose": "Future rollback is never automatic by default.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_source_reference",
                "purpose": "Future rollback notes should reference backup/source.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_preview_required",
                "purpose": "Future rollback should show preview before execution.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_user_approval_required",
                "purpose": "Future rollback requires explicit approval.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_scope_single_file_by_default",
                "purpose": "Future rollback is single-file by default.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_failure_note",
                "purpose": "Future rollback failure must be explained and auditable.",
                "runtime_rollback_enabled": False,
            },
            {
                "id": "rollback_audit_visibility",
                "purpose": "Future rollback intent/result must be visible in audit.",
                "runtime_rollback_enabled": False,
            },
        ]

    def audit_visibility_fields(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "file_write_event_id",
                "purpose": "Future file write approval audit event identifier.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "requested_write_mode",
                "purpose": "Future create/append/replace/patch mode visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "target_path",
                "purpose": "Future target path visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "path_policy_result",
                "purpose": "Future path policy result visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "diff_preview_reference",
                "purpose": "Future diff preview reference visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "overwrite_decision",
                "purpose": "Future overwrite decision visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "backup_requirement",
                "purpose": "Future backup requirement visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "rollback_reference",
                "purpose": "Future rollback note/reference visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "permission_reference",
                "purpose": "Future permission review queue reference visibility.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "approval_state",
                "purpose": "Future approval state visibility.",
                "runtime_audit_enabled": False,
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare file write proposal draft planning.",
            "Prepare target path policy planning.",
            "Prepare diff preview contract planning.",
            "Prepare overwrite rule planning.",
            "Prepare backup requirement planning.",
            "Prepare approval checklist planning.",
            "Prepare rollback note planning.",
            "Prepare file write audit visibility planning.",
            "Prepare file write safety policy planning.",
            "Expose controlled file write approval draft status.",
            "Keep controlled file write approval foundation draft-only, pre-runtime, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "file_write_runtime",
            "controlled_file_write_runtime",
            "file_create_runtime",
            "file_append_runtime",
            "file_replace_runtime",
            "file_patch_runtime",
            "file_overwrite_runtime",
            "file_read_runtime",
            "file_modify_runtime",
            "file_delete_runtime",
            "file_move_runtime",
            "file_copy_runtime",
            "file_backup_runtime",
            "file_restore_runtime",
            "rollback_runtime",
            "diff_runtime",
            "path_probe_runtime",
            "path_traversal_runtime",
            "approval_runtime",
            "permission_grant_runtime",
            "permission_deny_runtime",
            "permission_resolution_runtime",
            "permission_scope_activation_runtime",
            "permission_scope_revocation_runtime",
            "runtime_action_activation",
            "runtime_behavior_change",
            "session_runtime",
            "chat_runtime",
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
            "plugin_runtime",
            "service_runtime",
            "launcher_runtime",
            "orion_client_runtime",
            "client_connection",
            "screen_capture_runtime",
            "short_recording_runtime",
            "voice_bridge_runtime",
            "avatar_runtime",
            "three_d_environment_runtime",
            "game_companion_runtime",
            "blender_bridge_runtime",
            "vscode_project_bridge_runtime",
            "local_action_bridge_runtime",
            "emergency_stop_runtime",
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
            "controlled_file_write_approval_draft_foundation_only": True,
            "file_write_proposal_draft_only": True,
            "target_path_policy_blueprint_only": True,
            "diff_preview_contract_blueprint_only": True,
            "overwrite_rule_blueprint_only": True,
            "backup_requirement_blueprint_only": True,
            "approval_checklist_blueprint_only": True,
            "rollback_note_blueprint_only": True,
            "audit_visibility_blueprint_only": True,
            "pre_file_write_runtime_only": True,
            "draft_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "controlled_file_write_approval_draft_data_ready": True,
            "file_write_runtime": False,
            "controlled_file_write_runtime": False,
            "file_create_runtime": False,
            "file_append_runtime": False,
            "file_replace_runtime": False,
            "file_patch_runtime": False,
            "file_overwrite_runtime": False,
            "file_read_runtime": False,
            "file_modify_runtime": False,
            "file_delete_runtime": False,
            "file_move_runtime": False,
            "file_copy_runtime": False,
            "file_backup_runtime": False,
            "file_restore_runtime": False,
            "rollback_runtime": False,
            "diff_runtime": False,
            "path_probe_runtime": False,
            "path_traversal_runtime": False,
            "approval_runtime": False,
            "permission_grant_runtime": False,
            "permission_deny_runtime": False,
            "permission_resolution_runtime": False,
            "permission_scope_activation_runtime": False,
            "permission_scope_revocation_runtime": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "session_runtime": False,
            "chat_runtime": False,
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
            "plugin_runtime": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "orion_client_runtime": False,
            "client_connection": False,
            "screen_capture_runtime": False,
            "short_recording_runtime": False,
            "voice_bridge_runtime": False,
            "avatar_runtime": False,
            "three_d_environment_runtime": False,
            "game_companion_runtime": False,
            "blender_bridge_runtime": False,
            "vscode_project_bridge_runtime": False,
            "local_action_bridge_runtime": False,
            "emergency_stop_runtime": False,
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

    def approval_draft_summary(self) -> dict[str, Any]:
        proposal_drafts = self.file_write_proposal_drafts()
        path_policies = self.target_path_policies()
        diff_contracts = self.diff_preview_contracts()
        overwrite_rules = self.overwrite_rules()
        backup_requirements = self.backup_requirements()
        checklist_items = self.approval_checklist_items()
        rollback_notes = self.rollback_notes()
        audit_fields = self.audit_visibility_fields()
        return {
            "controlled_file_write_approval_draft_foundation_ready": True,
            "file_write_proposal_draft_plan_ready": True,
            "target_path_policy_plan_ready": True,
            "diff_preview_contract_plan_ready": True,
            "overwrite_rule_plan_ready": True,
            "backup_requirement_plan_ready": True,
            "approval_checklist_plan_ready": True,
            "rollback_note_plan_ready": True,
            "file_write_audit_visibility_plan_ready": True,
            "file_write_safety_policy_plan_ready": True,
            "file_write_proposal_draft_count": len(proposal_drafts),
            "target_path_policy_count": len(path_policies),
            "diff_preview_contract_count": len(diff_contracts),
            "overwrite_rule_count": len(overwrite_rules),
            "backup_requirement_count": len(backup_requirements),
            "approval_checklist_item_count": len(checklist_items),
            "rollback_note_count": len(rollback_notes),
            "audit_visibility_field_count": len(audit_fields),
            "total_approval_draft_blueprint_count": (
                len(proposal_drafts)
                + len(path_policies)
                + len(diff_contracts)
                + len(overwrite_rules)
                + len(backup_requirements)
                + len(checklist_items)
                + len(rollback_notes)
                + len(audit_fields)
            ),
            "runtime_files_created": 0,
            "runtime_files_appended": 0,
            "runtime_files_replaced": 0,
            "runtime_files_patched": 0,
            "runtime_files_overwritten": 0,
            "runtime_files_read": 0,
            "runtime_files_modified": 0,
            "runtime_files_deleted": 0,
            "runtime_files_moved": 0,
            "runtime_files_copied": 0,
            "runtime_backups_created": 0,
            "runtime_restores_performed": 0,
            "runtime_rollbacks_executed": 0,
            "runtime_diffs_generated": 0,
            "runtime_paths_probed": 0,
            "runtime_approvals_granted": 0,
            "runtime_approvals_denied": 0,
            "runtime_permission_scopes_activated": 0,
            "runtime_actions_triggered": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA controlled file write approval draft foundation"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "file_write_may_be_drafted_but_must_not_execute_without_future_explicit_user_approval",
            "approval_draft_identity": self.approval_draft_identity(),
            "approval_draft_plan_types": self.approval_draft_plan_types(),
            "approval_draft_summary": self.approval_draft_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def file_write_proposal_draft_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("file_write_proposal_draft_plan", target)
        plan["file_write_proposal_drafts"] = self.file_write_proposal_drafts()
        plan["rule"] = "File write proposal drafts do not write, read, modify, delete, or overwrite files."
        return plan

    def target_path_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("target_path_policy_plan", target)
        plan["target_path_policies"] = self.target_path_policies()
        plan["rule"] = "Target path policy planning does not probe paths or access the file system."
        return plan

    def diff_preview_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("diff_preview_contract_plan", target)
        plan["diff_preview_contracts"] = self.diff_preview_contracts()
        plan["rule"] = "Diff preview contract planning does not read files or generate runtime diffs."
        return plan

    def overwrite_rule_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("overwrite_rule_plan", target)
        plan["overwrite_rules"] = self.overwrite_rules()
        plan["rule"] = "Overwrite rule planning does not overwrite files."
        return plan

    def backup_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("backup_requirement_plan", target)
        plan["backup_requirements"] = self.backup_requirements()
        plan["rule"] = "Backup requirement planning does not create backups or restore files."
        return plan

    def approval_checklist_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("approval_checklist_plan", target)
        plan["approval_checklist_items"] = self.approval_checklist_items()
        plan["rule"] = "Approval checklist planning does not grant approval or execute writes."
        return plan

    def rollback_note_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("rollback_note_plan", target)
        plan["rollback_notes"] = self.rollback_notes()
        plan["rule"] = "Rollback note planning does not execute rollback."
        return plan

    def file_write_audit_visibility_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("file_write_audit_visibility_plan", target)
        plan["audit_visibility_fields"] = self.audit_visibility_fields()
        plan["rule"] = "Audit visibility planning does not write or fetch audit events."
        return plan

    def file_write_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("file_write_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Controlled file write approval draft must not write files.",
            "Controlled file write approval draft must not read files.",
            "Controlled file write approval draft must not modify files.",
            "Controlled file write approval draft must not delete files.",
            "Controlled file write approval draft must not overwrite files.",
            "Controlled file write approval draft must not create backups.",
            "Controlled file write approval draft must not execute rollback.",
            "Controlled file write approval draft must not grant runtime approval.",
            "Controlled file write approval draft must not trigger actions.",
            "Controlled file write approval draft must remain draft-only, planner-only, metadata-only, and safe_idle-first.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "approval_draft_identity": self.approval_draft_identity(),
            "approval_draft_plan_types": self.approval_draft_plan_types(),
            "file_write_proposal_drafts": self.file_write_proposal_drafts(),
            "target_path_policies": self.target_path_policies(),
            "diff_preview_contracts": self.diff_preview_contracts(),
            "overwrite_rules": self.overwrite_rules(),
            "backup_requirements": self.backup_requirements(),
            "approval_checklist_items": self.approval_checklist_items(),
            "rollback_notes": self.rollback_notes(),
            "audit_visibility_fields": self.audit_visibility_fields(),
            "approval_draft_summary": self.approval_draft_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.approval_draft_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "controlled_file_write_approval_draft_foundation_ready": True,
            "file_write_proposal_draft_plan_ready": True,
            "target_path_policy_plan_ready": True,
            "diff_preview_contract_plan_ready": True,
            "overwrite_rule_plan_ready": True,
            "backup_requirement_plan_ready": True,
            "approval_checklist_plan_ready": True,
            "rollback_note_plan_ready": True,
            "file_write_audit_visibility_plan_ready": True,
            "file_write_safety_policy_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "controlled_file_write_approval_draft_data_ready": True,
            "approval_draft_plan_types": self.approval_draft_plan_types(),
            "plan_type_count": len(self.approval_draft_plan_types()),
            **summary,
            **boundary,
        }
