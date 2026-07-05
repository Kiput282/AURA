from pathlib import Path
from typing import Any

import yaml

from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.game.game_companion_foundation_manager import GameCompanionFoundationManager
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.permissions.permission_manager import PermissionManager
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager


class StreamingSafetyFoundationManager:
    """
    AURA Streaming Safety Foundation.

    Current phase:
    - prepare safe streaming context plans
    - prepare chat safety plans
    - prepare content boundary plans
    - prepare privacy reminder plans
    - prepare moderation note plans
    - integrate game companion, expression language, media, vision, and desktop planning context
    - never reads live chat automatically
    - never captures screen automatically
    - never sends chat messages automatically
    - never performs moderation actions automatically
    - never opens browser/apps automatically
    - never writes files automatically
    - never executes commands
    """

    name = "streaming_safety_foundation"
    version = "0.1.0"
    status_name = "foundation"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.expression_language = ExpressionLanguageManager(project_root=self.project_root)
        self.game_companion = GameCompanionFoundationManager(project_root=self.project_root)
        self.media_understanding = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.vision_runtime_alpha = VisionRuntimeAlphaManager(project_root=self.project_root)
        self.desktop_assistant_alpha = DesktopAssistantAlphaManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def safety_categories(self) -> list[str]:
        return [
            "privacy",
            "chat_safety",
            "content_boundaries",
            "community_rules",
            "platform_safe_language",
            "non_invasive_assistance",
            "creator_focus",
            "technical_safety",
        ]

    def stream_modes(self) -> list[str]:
        return [
            "cozy_gaming",
            "educational",
            "creative_workflow",
            "avatar_companion",
            "quiet_focus",
            "collab_friendly",
            "community_chat",
        ]

    def disabled_runtime_actions(self) -> list[str]:
        return [
            "automatic_live_chat_read",
            "automatic_chat_message_send",
            "automatic_moderation_action",
            "automatic_screen_capture",
            "automatic_camera_access",
            "automatic_browser_open",
            "automatic_app_open",
            "automatic_file_write",
            "command_execution",
            "external_action_execution",
        ]

    def classify_stream_context(self, text: str) -> dict[str, Any]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "game": "gaming",
            "gaming": "gaming",
            "minecraft": "gaming",
            "stream": "streaming",
            "youtube": "platform_youtube",
            "twitch": "platform_twitch",
            "cozy": "cozy",
            "friendly": "friendly",
            "avatar": "avatar",
            "desktop": "desktop",
            "chat": "chat",
            "live chat": "chat",
            "moderation": "moderation",
            "rules": "moderation",
            "privacy": "privacy",
            "private": "privacy",
            "safe": "safety",
            "aman": "safety",
            "commentary": "commentary",
            "komentar": "commentary",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["streaming", "safety"])

        if "privacy" in tags or "desktop" in tags:
            priority = "privacy_first"
        elif "moderation" in tags or "chat" in tags:
            priority = "community_safety"
        elif "gaming" in tags or "cozy" in tags:
            priority = "cozy_game_safety"
        elif "avatar" in tags or "commentary" in tags:
            priority = "presentation_safety"
        else:
            priority = "general_stream_safety"

        return {
            "tags": tags[:7],
            "priority": priority,
            "chat_related": "chat" in tags or "moderation" in tags,
            "privacy_related": "privacy" in tags or "desktop" in tags,
            "game_related": "gaming" in tags,
            "avatar_related": "avatar" in tags or "commentary" in tags,
        }

    def base_plan(self, plan_type: str, target: str, recommended_steps: list[str]) -> dict[str, Any]:
        cleaned_target = " ".join(target.strip().split()) or "<unspecified>"
        stream_context = self.classify_stream_context(cleaned_target)

        expression_plan = self.expression_language.expression_plan(
            f"AURA menjaga stream tetap aman dan nyaman: {cleaned_target}"
        )
        game_streaming_plan = self.game_companion.streaming_plan(cleaned_target)

        read_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        screen_permission = self.permission_manager.check("screen_analyze")
        open_browser_permission = self.permission_manager.check("open_browser")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "stream_context": stream_context,
            "stream_priority": stream_context["priority"],
            "stream_tags": stream_context["tags"],
            "expression_plan": expression_plan,
            "game_streaming_plan": game_streaming_plan,
            "voice_tone_hint": expression_plan["voice_tone_hint"],
            "avatar_expression_hint": expression_plan["avatar_expression_hint"],
            "gesture_hint": expression_plan["gesture_hint"],
            "response_style_hint": expression_plan["response_style_hint"],
            "game_context_ready": self.game_companion.status()["context_ready"],
            "expression_context_ready": self.expression_language.status()["context_ready"],
            "media_context_ready": self.media_understanding.status()["context_ready"],
            "vision_context_ready": self.vision_runtime_alpha.status()["vision_context_ready"],
            "desktop_context_ready": self.desktop_assistant_alpha.status()["workspace_context_ready"],
            "recommended_steps": recommended_steps,
            "permissions": {
                "read_project": read_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "screen_analyze": screen_permission.to_dict(),
                "open_browser": open_browser_permission.to_dict(),
                "open_app": open_app_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "live_chat_read": False,
            "chat_message_sent": False,
            "moderation_action_performed": False,
            "screen_capture_performed": False,
            "camera_access_performed": False,
            "browser_opened": False,
            "app_opened": False,
            "voice_output_performed": False,
            "avatar_changed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Streaming safety plan is proposal-only.",
                "No live chat was read.",
                "No chat message was sent.",
                "No moderation action was performed.",
                "No screen was captured.",
                "No camera was accessed.",
                "No browser or app was opened.",
                "No voice output was played.",
                "No avatar state was changed.",
                "No file was written.",
                "No command was executed.",
                "Future live streaming actions must go through explicit permission and confirmation.",
            ],
        }

    def context_plan(self, stream_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="streaming_context",
            target=stream_goal,
            recommended_steps=[
                "Clarify stream platform, theme, audience, and intended tone.",
                "Prepare safety categories before stream starts: privacy, chat, content boundaries, and moderation notes.",
                "Use expression hints for a friendly but not annoying stream presence.",
                "Use game companion context only as non-invasive planning support.",
                "Keep live chat reading, screen capture, browser/app opening, file writing, and commands disabled.",
            ],
        )

    def chat_safety_plan(self, chat_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="streaming_chat_safety",
            target=chat_goal,
            recommended_steps=[
                "Define friendly chat expectations before the stream starts.",
                "Prepare reminder language for respectful discussion and no spam.",
                "Plan how to respond calmly to off-topic or unsafe messages.",
                "Keep chat review as text-only planning until live chat access is explicitly approved.",
                "Do not send messages or moderate chat automatically.",
            ],
        )

    def content_boundary_plan(self, content_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="streaming_content_boundary",
            target=content_goal,
            recommended_steps=[
                "Clarify what content is allowed, avoided, or paused during stream.",
                "Prepare boundaries for gameplay, avatar commentary, jokes, and sensitive topics.",
                "Keep AURA's style expressive but not annoying.",
                "Prepare fallback responses for uncertain or unsafe topics.",
                "Do not perform live content detection, screen capture, or external actions automatically.",
            ],
        )

    def privacy_plan(self, privacy_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="streaming_privacy",
            target=privacy_goal,
            recommended_steps=[
                "Prepare a privacy checklist before going live.",
                "Check for desktop notifications, private files, browser tabs, personal accounts, and sensitive windows.",
                "Plan safe screen regions and scenes without capturing the screen automatically.",
                "Prepare reminders to use stream overlays and avoid showing personal information.",
                "Keep screen capture, browser opening, app opening, file writing, and commands disabled.",
            ],
        )

    def moderation_plan(self, moderation_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="streaming_moderation",
            target=moderation_goal,
            recommended_steps=[
                "Prepare community rules in a friendly and clear tone.",
                "Plan escalation levels: gentle reminder, warning, timeout suggestion, and manual review.",
                "Keep moderation notes as suggestions only.",
                "Do not delete messages, timeout users, ban users, or send chat messages automatically.",
                "Keep all moderation actions behind explicit human confirmation.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()

        return {
            "status": self.status_name,
            "context_ready": True,
            "streaming_status": status,
            "identity": self.load_identity(),
            "game_context": self.game_companion.context(),
            "expression_context": self.expression_language.context(),
            "media_context": self.media_understanding.context(),
            "vision_context": self.vision_runtime_alpha.context(),
            "desktop_context": self.desktop_assistant_alpha.workspace_context(),
            "safe_current_capabilities": [
                "streaming_safety_status",
                "streaming_context_plan",
                "streaming_chat_safety_plan",
                "streaming_content_boundary_plan",
                "streaming_privacy_plan",
                "streaming_moderation_plan",
                "streaming_safety_context",
            ],
            "disabled_capabilities": self.disabled_runtime_actions(),
            "read_only": True,
            "write_performed": False,
            "live_chat_read": False,
            "message_sent": False,
            "moderation_action": False,
            "screen_capture": False,
            "camera_access": False,
            "browser_opened": False,
            "app_opened": False,
            "voice_output_performed": False,
            "avatar_changed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Streaming Safety context is read-only and preparation-only.",
        }

    def status(self) -> dict[str, Any]:
        identity = self.load_identity()
        modes = identity.get("modes", {}) if isinstance(identity, dict) else {}

        screen_permission = self.permission_manager.check("screen_analyze")
        open_browser_permission = self.permission_manager.check("open_browser")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        game_status = self.game_companion.status()
        expression_status = self.expression_language.status()
        media_status = self.media_understanding.status()
        vision_status = self.vision_runtime_alpha.status()
        desktop_status = self.desktop_assistant_alpha.status()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "safety_ready": True,
            "context_plan_ready": True,
            "chat_safety_ready": True,
            "content_boundary_ready": True,
            "privacy_plan_ready": True,
            "moderation_plan_ready": True,
            "context_ready": True,
            "game_integration_ready": game_status["companion_ready"],
            "expression_integration_ready": expression_status["language_ready"],
            "media_integration_ready": media_status["understanding_ready"],
            "vision_integration_ready": vision_status["alpha_ready"],
            "desktop_integration_ready": desktop_status["alpha_ready"],
            "safety_categories": len(self.safety_categories()),
            "stream_modes": len(self.stream_modes()),
            "disabled_runtime_actions": len(self.disabled_runtime_actions()),
            "streaming_mode": modes.get("streaming", "expressive but not annoying"),
            "requires_screen_confirmation": screen_permission.requires_confirmation,
            "requires_open_browser_confirmation": open_browser_permission.requires_confirmation,
            "requires_open_app_confirmation": open_app_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "live_chat_read": False,
            "message_sent": False,
            "moderation_action": False,
            "screen_capture": False,
            "camera_access": False,
            "browser_opened": False,
            "app_opened": False,
            "voice_output": False,
            "avatar_changed": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Streaming Safety Foundation is online for safe stream planning. It does not read live chat, send messages, moderate, capture screen, open apps/browser, write files, or execute commands automatically.",
        }
