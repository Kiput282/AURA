
"""Desktop workflow planner for AURA Genesis.

Planner-only layer. It does not open apps, control windows, capture
screenshots, send mouse/keyboard input, read/write files, or execute commands.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class DesktopWorkflowPlannerManager:
    """Plan safe desktop workflows without desktop runtime execution."""

    name = "desktop_workflow_planner"
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

    def safe_import_status(self, candidates: list[tuple[str, str]]) -> dict[str, Any]:
        for module_name, class_name in candidates:
            try:
                module = importlib.import_module(module_name)
                manager_class = getattr(module, class_name)
                manager = manager_class(project_root=self.project_root)
                status = manager.status() if hasattr(manager, "status") else {}
                return {
                    "found": True,
                    "module": module_name,
                    "class": class_name,
                    "status": status.get("status", "available"),
                    "ready": bool(
                        status.get("planner_ready")
                        or status.get("context_ready")
                        or status.get("workflow_ready")
                        or status.get("workspace_awareness_ready")
                        or status.get("safe_file_operation_ready")
                    ),
                }
            except Exception:
                continue

        return {
            "found": False,
            "module": None,
            "class": None,
            "status": "not_found",
            "ready": False,
        }

    def integration_context(self) -> dict[str, Any]:
        return {
            "local_task_reference": self.safe_import_status([
                ("aura.task_planner.local_task_planner_manager", "LocalTaskPlannerManager"),
                ("aura.local_task.local_task_planner_manager", "LocalTaskPlannerManager"),
            ]),
            "safe_file_operation_reference": self.safe_import_status([
                ("aura.file_ops.safe_file_operation_planner_manager", "SafeFileOperationPlannerManager"),
            ]),
            "workspace_awareness_reference": self.safe_import_status([
                ("aura.workspace.workspace_awareness_manager", "WorkspaceAwarenessManager"),
                ("aura.workspace_awareness.workspace_awareness_manager", "WorkspaceAwarenessManager"),
            ]),
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "vision_context_reference": self.safe_import_status([
                ("aura.vision_context.vision_context_planner_manager", "VisionContextPlannerManager"),
            ]),
            "avatar_interaction_reference": self.safe_import_status([
                ("aura.avatar_interaction.avatar_interaction_planner_manager", "AvatarInteractionPlannerManager"),
            ]),
            "codebase_validation_reference": self.safe_import_status([
                ("aura.codebase_validation.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
                ("aura.codebase_validation_gate.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def desktop_plan_types(self) -> list[str]:
        return [
            "desktop_workflow_status",
            "desktop_workflow_plan",
            "desktop_app_context_plan",
            "desktop_window_flow_plan",
            "desktop_task_sequence_plan",
            "desktop_safety_plan",
            "desktop_workflow_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan desktop workflow steps from metadata only.",
            "Plan app context without opening applications.",
            "Plan window flow without window inspection or control.",
            "Plan task sequences without file or command execution.",
            "Connect desktop workflow planning with voice, vision, avatar, and workspace context.",
            "Keep all outputs planner-only and proposal-only.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "desktop_control",
            "app_opening",
            "window_inspection",
            "window_control",
            "mouse_control",
            "keyboard_control",
            "screen_capture",
            "clipboard_access",
            "notification_access",
            "process_inspection",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]

    def infer_desktop_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "coding", "repo", "terminal", "sprint", "patch", "commit"],
            "creative": ["blender", "avatar", "texture", "image", "video", "design"],
            "streaming": ["stream", "obs", "live", "viewer", "chat"],
            "files": ["file", "folder", "document", "rename", "move", "copy", "delete"],
            "browser": ["browser", "web", "tab", "website", "search"],
            "office": ["spreadsheet", "doc", "slide", "pdf", "report"],
            "safety": ["private", "secret", "sensitive", "permission", "risk"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_workflow_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "mode": "developer_workflow_plan",
                "attention": "terminal_repo_and_validation_sequence",
                "interaction": "confirm_before_execution",
            }
        if "creative" in tags:
            return {
                "mode": "creative_workspace_plan",
                "attention": "asset_context_and_app_boundary",
                "interaction": "metadata_only_review",
            }
        if "streaming" in tags:
            return {
                "mode": "streaming_workspace_plan",
                "attention": "OBS_scene_and_chat_context_without_control",
                "interaction": "do_not_interrupt_stream",
            }
        if "files" in tags:
            return {
                "mode": "safe_file_workflow_plan",
                "attention": "risk_review_before_file_operations",
                "interaction": "proposal_only",
            }
        return {
            "mode": "general_desktop_workflow_plan",
            "attention": "user_goal_and_safe_sequence",
            "interaction": "ask_before_runtime_action",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "desktop_control": False,
            "app_opening": False,
            "window_inspection": False,
            "window_control": False,
            "mouse_control": False,
            "keyboard_control": False,
            "screen_capture": False,
            "clipboard_access": False,
            "notification_access": False,
            "process_inspection": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general desktop workflow"
        tags = self.infer_desktop_tags(normalized_target)
        identity = self.load_identity()
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "creator": identity.get("creator", "Kiput"),
            "aura_name": identity.get("name", "AURA"),
            "tags": tags,
            "workflow_mode": self.recommended_workflow_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def desktop_workflow_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("desktop_workflow_plan", target)
        plan["workflow_steps"] = [
            "Identify the user goal from metadata.",
            "Break the desktop task into safe proposed steps.",
            "Mark steps that would require future explicit permission.",
            "Do not open apps, inspect windows, use mouse/keyboard, access clipboard, read files, write files, or execute commands.",
        ]
        return plan

    def desktop_app_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("desktop_app_context_plan", target)
        plan["app_context_steps"] = [
            "Identify which app context would be relevant from the request.",
            "Describe the needed app state as metadata only.",
            "Do not open, focus, inspect, or control any application.",
            "Ask the user to provide app context manually when needed now.",
        ]
        return plan

    def desktop_window_flow_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("desktop_window_flow_plan", target)
        plan["window_flow_steps"] = [
            "Plan the ideal window/task flow as a proposal.",
            "Avoid reading active windows or capturing the screen.",
            "Avoid moving, resizing, focusing, or controlling windows.",
            "Keep all window references as future-permission placeholders.",
        ]
        return plan

    def desktop_task_sequence_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("desktop_task_sequence_plan", target)
        plan["task_sequence_steps"] = [
            "Convert the user goal into a safe task sequence.",
            "Separate informational planning from actions requiring runtime permission.",
            "Flag any file, command, browser, app, or desktop action as disabled in this sprint.",
            "Return only a human-reviewable sequence.",
        ]
        return plan

    def desktop_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("desktop_safety_plan", target)
        plan["safety_steps"] = [
            "Never open or control desktop apps in this planner sprint.",
            "Never inspect windows, capture the screen, access clipboard, or inspect processes.",
            "Never send mouse or keyboard input.",
            "Never read files, write files, execute commands, or call external tools.",
            "Require explicit future permission before any desktop runtime execution.",
            "Keep desktop workflow planning local-first, permission-first, and proposal-only.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        identity = self.load_identity()
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "identity_version": identity.get("version"),
            "desktop_plan_types": self.desktop_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "integration_context": self.integration_context(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        integrations = self.integration_context()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "desktop_workflow_plan_ready": True,
            "desktop_app_context_plan_ready": True,
            "desktop_window_flow_plan_ready": True,
            "desktop_task_sequence_plan_ready": True,
            "desktop_safety_plan_ready": True,
            "context_ready": True,
            "desktop_plan_types": self.desktop_plan_types(),
            "plan_type_count": len(self.desktop_plan_types()),
            "local_task_reference_ready": True,
            "safe_file_operation_reference_ready": True,
            "workspace_awareness_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "vision_context_reference_ready": True,
            "avatar_interaction_reference_ready": True,
            "codebase_validation_reference_ready": True,
            "local_task_manager_found": integrations["local_task_reference"]["found"],
            "safe_file_operation_manager_found": integrations["safe_file_operation_reference"]["found"],
            "workspace_awareness_manager_found": integrations["workspace_awareness_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "vision_context_manager_found": integrations["vision_context_reference"]["found"],
            "avatar_interaction_manager_found": integrations["avatar_interaction_reference"]["found"],
            "codebase_validation_manager_found": integrations["codebase_validation_reference"]["found"],
            **boundary,
        }
