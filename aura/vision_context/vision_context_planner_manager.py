
"""Vision context planner for AURA Genesis.

Planner-only layer. It does not capture the screen, open the camera,
inspect real images, read files, write files, or execute commands.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class VisionContextPlannerManager:
    """Plan safe visual context flows without real vision runtime execution."""

    name = "vision_context_planner"
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
                        or status.get("runtime_ready")
                        or status.get("context_ready")
                        or status.get("vision_ready")
                        or status.get("media_understanding_ready")
                        or status.get("workspace_awareness_ready")
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
            "vision_runtime_alpha_reference": self.safe_import_status([
                ("aura.vision_runtime_alpha.vision_runtime_alpha_manager", "VisionRuntimeAlphaManager"),
                ("aura.vision.vision_runtime_alpha_manager", "VisionRuntimeAlphaManager"),
            ]),
            "media_understanding_reference": self.safe_import_status([
                ("aura.media_understanding.media_understanding_manager", "MediaUnderstandingManager"),
                ("aura.media.media_understanding_manager", "MediaUnderstandingManager"),
            ]),
            "workspace_awareness_reference": self.safe_import_status([
                ("aura.workspace.workspace_awareness_manager", "WorkspaceAwarenessManager"),
                ("aura.workspace_awareness.workspace_awareness_manager", "WorkspaceAwarenessManager"),
            ]),
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "tool_sandbox_reference": self.safe_import_status([
                ("aura.sandbox.tool_sandbox_manager", "ToolSandboxManager"),
                ("aura.tools.tool_sandbox_manager", "ToolSandboxManager"),
            ]),
            "permissions_reference": self.safe_import_status([
                ("aura.permissions.permission_manager", "PermissionManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def vision_plan_types(self) -> list[str]:
        return [
            "vision_context_status",
            "visual_context_plan",
            "screen_context_plan",
            "camera_context_plan",
            "vision_safety_plan",
            "vision_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan visual context needs from metadata only.",
            "Plan screen context questions without screen capture.",
            "Plan camera context questions without camera access.",
            "Plan safe handoff to future vision runtime layers.",
            "Connect vision planning with voice conversation and workspace context.",
            "Keep all outputs planner-only and proposal-only.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "screen_capture",
            "camera_access",
            "image_open",
            "image_read",
            "video_capture",
            "ocr_runtime",
            "visual_recognition_runtime",
            "desktop_action_execution",
            "app_opening",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]

    def infer_context_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "screen": ["screen", "desktop", "window", "monitor", "ui", "workspace"],
            "camera": ["camera", "webcam", "phone", "record", "room"],
            "image": ["image", "picture", "photo", "thumbnail", "texture"],
            "avatar": ["avatar", "character", "model", "blender", "rig"],
            "streaming": ["stream", "live", "obs", "viewer", "chat"],
            "coding": ["code", "repo", "terminal", "sprint", "patch"],
            "safety": ["private", "secret", "sensitive", "permission", "risk"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_visual_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags or "screen" in tags:
            return {
                "mode": "screen_context_metadata_plan",
                "attention": "active_window_and_user_goal",
                "verbosity": "concise",
            }
        if "camera" in tags:
            return {
                "mode": "camera_context_metadata_plan",
                "attention": "scene_intent_and_permission_boundary",
                "verbosity": "confirm_before_runtime_access",
            }
        if "avatar" in tags or "image" in tags:
            return {
                "mode": "asset_context_metadata_plan",
                "attention": "visual_features_and_design_intent",
                "verbosity": "structured",
            }
        return {
            "mode": "general_visual_context_plan",
            "attention": "user_goal_first",
            "verbosity": "balanced",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "screen_capture": False,
            "camera_access": False,
            "image_open": False,
            "image_read": False,
            "video_capture": False,
            "ocr_runtime": False,
            "visual_recognition_runtime": False,
            "desktop_action_execution": False,
            "app_opened": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general vision context"
        tags = self.infer_context_tags(normalized_target)
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
            "visual_mode": self.recommended_visual_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def visual_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_context_plan", target)
        plan["context_steps"] = [
            "Identify what visual context the user needs from metadata.",
            "Classify the request as screen, camera, image, avatar, streaming, coding, safety, or general.",
            "Choose a safe future handoff path without capturing screen or camera.",
            "Return a planned visual context summary without opening images or files.",
        ]
        return plan

    def screen_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("screen_context_plan", target)
        plan["screen_steps"] = [
            "Treat the screen request as metadata-only.",
            "Describe what information would be needed from the active window in a future permitted runtime.",
            "Do not capture the screen, inspect windows, click UI, open apps, or execute desktop actions.",
            "Ask for user-provided context when screen information is needed now.",
        ]
        return plan

    def camera_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("camera_context_plan", target)
        plan["camera_steps"] = [
            "Treat the camera request as metadata-only.",
            "Describe the intended scene context and safety needs.",
            "Do not access camera, webcam, phone stream, or video capture.",
            "Require explicit future permission before any camera runtime is enabled.",
        ]
        return plan

    def vision_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("vision_safety_plan", target)
        plan["safety_steps"] = [
            "Never capture the screen without explicit runtime permission.",
            "Never access camera or webcam in this planner sprint.",
            "Never open or read image/video files automatically.",
            "Never perform OCR or visual recognition runtime automatically.",
            "Never click, open apps, execute commands, write files, or use external tools.",
            "Keep vision planning local-first, permission-first, and proposal-only.",
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
            "vision_plan_types": self.vision_plan_types(),
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
            "visual_context_plan_ready": True,
            "screen_context_plan_ready": True,
            "camera_context_plan_ready": True,
            "vision_safety_plan_ready": True,
            "context_ready": True,
            "vision_plan_types": self.vision_plan_types(),
            "plan_type_count": len(self.vision_plan_types()),
            "vision_runtime_alpha_reference_ready": True,
            "media_understanding_reference_ready": True,
            "workspace_awareness_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "tool_sandbox_reference_ready": True,
            "permissions_reference_ready": True,
            "vision_runtime_alpha_manager_found": integrations["vision_runtime_alpha_reference"]["found"],
            "media_understanding_manager_found": integrations["media_understanding_reference"]["found"],
            "workspace_awareness_manager_found": integrations["workspace_awareness_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "tool_sandbox_manager_found": integrations["tool_sandbox_reference"]["found"],
            "permission_manager_found": integrations["permissions_reference"]["found"],
            **boundary,
        }
