
"""Unified Permission Workflow Manager for AURA.

Planner-only permission workflow foundation for unifying how AURA prepares
permission requests, approval/deny states, risk reviews, confirmation
prompts, audit trails, and future Control Center Permission Center views.

This module does not grant permission, execute actions, write files, run
commands, install dependencies, access devices, start services, open UI,
access networks, control the desktop, run git, or perform external actions.
"""
from __future__ import annotations

from typing import Any


class UnifiedPermissionWorkflowManager:
    """Prepare unified permission workflow plans without granting permission."""

    name = "unified_permission_workflow"
    version = "0.1.0"
    status_name = "online"

    def workflow_plan_types(self) -> list[str]:
        return [
            "permission_workflow_status",
            "permission_request_plan",
            "permission_state_transition_plan",
            "permission_risk_review_plan",
            "confirmation_prompt_plan",
            "permission_audit_trail_plan",
            "control_center_permission_view_plan",
            "permission_policy_gap_review_plan",
            "permission_workflow_context",
        ]

    def permission_request_states(self) -> list[str]:
        return [
            "draft",
            "pending_review",
            "approved_once_planned",
            "denied_planned",
            "expired_planned",
            "cancelled_planned",
            "audit_only",
        ]

    def approval_modes(self) -> list[str]:
        return [
            "none",
            "approve_once",
            "deny",
            "review_details",
            "request_clarification",
        ]

    def permission_categories(self) -> list[str]:
        return [
            "read_project",
            "user_confirmation",
            "microphone_permission",
            "camera_permission",
            "screen_permission",
            "file_write_permission",
            "command_execution_permission",
            "dependency_download_permission",
            "internet_search_permission",
            "desktop_control_permission",
            "git_operation_permission",
            "service_control_permission",
            "plugin_install_permission",
        ]

    def risk_levels(self) -> list[str]:
        return [
            "low",
            "medium",
            "high",
            "critical",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare permission request plans without granting permission.",
            "Prepare approval and denial state transition plans.",
            "Classify permission requests by category and risk level.",
            "Prepare human-readable confirmation prompts.",
            "Prepare audit trail metadata for future review.",
            "Prepare Permission Center data for future AURA Control Center.",
            "Keep all permission decisions explicit, reviewable, and user-confirmed.",
            "Keep the workflow planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "permission_grant_runtime",
            "automatic_approval",
            "always_approve_mode",
            "background_approval",
            "runtime_action_activation",
            "runtime_behavior_change",
            "file_operation_runtime",
            "command_execution_runtime",
            "dependency_install_runtime",
            "download_runtime",
            "microphone_runtime",
            "camera_runtime",
            "screen_capture_runtime",
            "internet_runtime",
            "desktop_control_runtime",
            "git_operation_runtime",
            "plugin_install_runtime",
            "service_control_runtime",
            "ui_runtime",
            "web_server_runtime",
            "chat_runtime",
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
            "permission_workflow_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "control_center_permission_data_ready": True,
            "permission_grant_runtime": False,
            "automatic_approval": False,
            "always_approve_mode": False,
            "background_approval": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "file_operation_runtime": False,
            "command_execution_runtime": False,
            "dependency_install_runtime": False,
            "download_runtime": False,
            "microphone_runtime": False,
            "camera_runtime": False,
            "screen_capture_runtime": False,
            "internet_runtime": False,
            "desktop_control_runtime": False,
            "git_operation_runtime": False,
            "plugin_install_runtime": False,
            "service_control_runtime": False,
            "ui_runtime": False,
            "web_server_runtime": False,
            "chat_runtime": False,
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

    def permission_templates(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "read_project",
                "title": "Read Project Metadata",
                "category": "read_project",
                "risk_level": "low",
                "default_state": "audit_only",
                "requires_explicit_user_confirmation": False,
                "allowed_approval_modes": ["none", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "internet_search",
                "title": "Internet Search Request",
                "category": "internet_search_permission",
                "risk_level": "medium",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
            {
                "id": "dependency_download",
                "title": "Dependency or Package Download Request",
                "category": "dependency_download_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
            {
                "id": "file_write",
                "title": "File Write Request",
                "category": "file_write_permission",
                "risk_level": "critical",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
            {
                "id": "command_execution",
                "title": "Command Execution Request",
                "category": "command_execution_permission",
                "risk_level": "critical",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
            {
                "id": "microphone_access",
                "title": "Microphone Access Request",
                "category": "microphone_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "camera_access",
                "title": "Camera Access Request",
                "category": "camera_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "screen_access",
                "title": "Screen or Screenshot Access Request",
                "category": "screen_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "desktop_control",
                "title": "Desktop Control Request",
                "category": "desktop_control_permission",
                "risk_level": "critical",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
            {
                "id": "git_operation",
                "title": "Git Operation Request",
                "category": "git_operation_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "service_control",
                "title": "AURA Service Control Request",
                "category": "service_control_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details"],
                "runtime_enabled": False,
            },
            {
                "id": "plugin_install",
                "title": "Plugin Install Request",
                "category": "plugin_install_permission",
                "risk_level": "high",
                "default_state": "pending_review",
                "requires_explicit_user_confirmation": True,
                "allowed_approval_modes": ["approve_once", "deny", "review_details", "request_clarification"],
                "runtime_enabled": False,
            },
        ]

    def workflow_summary(self) -> dict[str, Any]:
        templates = self.permission_templates()
        risk_counts: dict[str, int] = {}
        category_counts: dict[str, int] = {}
        explicit_confirmation_count = 0

        for item in templates:
            risk_counts[item["risk_level"]] = risk_counts.get(item["risk_level"], 0) + 1
            category_counts[item["category"]] = category_counts.get(item["category"], 0) + 1
            if item["requires_explicit_user_confirmation"]:
                explicit_confirmation_count += 1

        return {
            "permission_template_count": len(templates),
            "permission_category_count": len(self.permission_categories()),
            "request_state_count": len(self.permission_request_states()),
            "approval_mode_count": len(self.approval_modes()),
            "risk_level_count": len(self.risk_levels()),
            "explicit_confirmation_required_count": explicit_confirmation_count,
            "runtime_enabled_template_count": sum(1 for item in templates if item["runtime_enabled"]),
            "always_approve_template_count": 0,
            "runtime_execution_features": 0,
            "risk_counts": risk_counts,
            "category_counts": category_counts,
        }

    def normalize_text(self, text: Any) -> str:
        return " ".join(str(text or "").strip().split())

    def infer_permission_category(self, request_text: str) -> str:
        text = self.normalize_text(request_text).lower()

        if any(token in text for token in ["mic", "microphone", "audio", "voice record"]):
            return "microphone_permission"
        if any(token in text for token in ["camera", "webcam"]):
            return "camera_permission"
        if any(token in text for token in ["screen", "screenshot", "ocr", "visual"]):
            return "screen_permission"
        if any(token in text for token in ["write file", "create file", "modify file", "delete file", "project generation"]):
            return "file_write_permission"
        if any(token in text for token in ["command", "shell", "execute", "terminal"]):
            return "command_execution_permission"
        if any(token in text for token in ["install", "download", "package", "dependency", "pip", "npm", "apt"]):
            return "dependency_download_permission"
        if any(token in text for token in ["internet", "search web", "network", "online"]):
            return "internet_search_permission"
        if any(token in text for token in ["desktop", "mouse", "keyboard", "window control"]):
            return "desktop_control_permission"
        if any(token in text for token in ["git", "commit", "push", "branch"]):
            return "git_operation_permission"
        if any(token in text for token in ["service", "systemd", "launcher", "start aura", "restart aura"]):
            return "service_control_permission"
        if any(token in text for token in ["plugin", "extension"]):
            return "plugin_install_permission"

        return "user_confirmation"

    def infer_risk_level(self, permission_category: str) -> str:
        critical = {
            "file_write_permission",
            "command_execution_permission",
            "desktop_control_permission",
        }
        high = {
            "microphone_permission",
            "camera_permission",
            "screen_permission",
            "dependency_download_permission",
            "git_operation_permission",
            "service_control_permission",
            "plugin_install_permission",
        }
        medium = {
            "internet_search_permission",
            "user_confirmation",
        }

        if permission_category in critical:
            return "critical"
        if permission_category in high:
            return "high"
        if permission_category in medium:
            return "medium"
        return "low"

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA permission workflow"
        category = self.infer_permission_category(normalized_target)
        risk = self.infer_risk_level(category)
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "permission_category": category,
            "risk_level": risk,
            "requires_explicit_user_confirmation": category != "read_project",
            "allowed_approval_modes": self.approval_modes(),
            "workflow_plan_types": self.workflow_plan_types(),
            "workflow_summary": self.workflow_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def permission_request_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_request_plan", target)
        plan["request_steps"] = [
            "Describe the requested action in human-readable language.",
            "Classify permission category and risk level.",
            "Explain why permission is needed.",
            "Show what will not happen unless approved.",
            "Require explicit user confirmation for risky categories.",
            "Keep the request as a plan only; do not grant permission.",
        ]
        return plan

    def permission_state_transition_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_state_transition_plan", target)
        plan["state_transitions"] = [
            "draft -> pending_review",
            "pending_review -> approved_once_planned",
            "pending_review -> denied_planned",
            "pending_review -> request_clarification",
            "pending_review -> expired_planned",
            "pending_review -> cancelled_planned",
        ]
        plan["state_rule"] = "State transition planning does not execute the requested action."
        return plan

    def permission_risk_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_risk_review_plan", target)
        plan["risk_review_steps"] = [
            "Identify possible impact of the requested action.",
            "Identify files, commands, devices, network, desktop, git, service, or plugin areas affected.",
            "Recommend approve_once, deny, review_details, or request_clarification.",
            "Treat critical runtime actions as deferred unless a future runtime layer exists.",
        ]
        return plan

    def confirmation_prompt_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("confirmation_prompt_plan", target)
        plan["prompt_template"] = {
            "title": "Permission required",
            "question": "Do you approve this action once?",
            "approve_label": "Approve Once",
            "deny_label": "Deny",
            "details_label": "Review Details",
            "clarify_label": "Request Clarification",
        }
        plan["prompt_rule"] = "No always-approve option is available in Genesis phase."
        return plan

    def permission_audit_trail_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_audit_trail_plan", target)
        plan["audit_fields"] = [
            "request_id",
            "timestamp",
            "target",
            "permission_category",
            "risk_level",
            "requested_by",
            "decision",
            "decision_reason",
            "runtime_enabled",
            "executed",
        ]
        plan["audit_rule"] = "Audit trail planning is metadata-only and does not write logs by itself."
        return plan

    def control_center_permission_view_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("control_center_permission_view_plan", target)
        plan["permission_center_cards"] = [
            "Pending permission requests",
            "Risk level",
            "Requested action",
            "Target resource",
            "Approve Once button",
            "Deny button",
            "Review Details button",
            "Request Clarification button",
            "Audit metadata",
        ]
        plan["control_center_rule"] = "Permission Center may display and route permission decisions only after a future runtime workflow exists."
        return plan

    def permission_policy_gap_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_policy_gap_review_plan", target)
        plan["gap_review_steps"] = [
            "Identify capabilities that still need permission policies.",
            "Keep file write, command execution, desktop control, dependency install, and service control locked.",
            "Ensure Control Center UI cannot bypass permission workflow.",
            "Defer real approval persistence until an explicit runtime permission store exists.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "workflow_plan_types": self.workflow_plan_types(),
            "permission_request_states": self.permission_request_states(),
            "approval_modes": self.approval_modes(),
            "permission_categories": self.permission_categories(),
            "risk_levels": self.risk_levels(),
            "permission_templates": self.permission_templates(),
            "workflow_summary": self.workflow_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.workflow_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "permission_workflow_ready": True,
            "planner_ready": True,
            "control_center_permission_data_ready": True,
            "permission_request_plan_ready": True,
            "permission_state_transition_plan_ready": True,
            "permission_risk_review_plan_ready": True,
            "confirmation_prompt_plan_ready": True,
            "permission_audit_trail_plan_ready": True,
            "control_center_permission_view_plan_ready": True,
            "permission_policy_gap_review_plan_ready": True,
            "context_ready": True,
            "workflow_plan_types": self.workflow_plan_types(),
            "plan_type_count": len(self.workflow_plan_types()),
            **summary,
            **boundary,
        }
