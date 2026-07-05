from pathlib import Path
from typing import Any

import yaml

from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.partner.partner_alpha_manager import PartnerAlphaManager
from aura.permissions.permission_manager import PermissionManager
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager


class GameCompanionFoundationManager:
    """
    AURA Game Companion Foundation.

    Current phase:
    - prepare safe game session context
    - prepare game session plans
    - prepare strategy plans
    - prepare streaming-safe companion plans
    - prepare coaching/practice plans
    - integrate expression language, voice/avatar hints, vision planning, desktop planning, partner context, and media context
    - never reads game screen automatically
    - never accesses keyboard/mouse automatically
    - never opens games/apps automatically
    - never writes files automatically
    - never executes commands
    """

    name = "game_companion_foundation"
    version = "0.1.0"
    status_name = "foundation"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.expression_language = ExpressionLanguageManager(project_root=self.project_root)
        self.vision_runtime_alpha = VisionRuntimeAlphaManager(project_root=self.project_root)
        self.desktop_assistant_alpha = DesktopAssistantAlphaManager(project_root=self.project_root)
        self.media_understanding = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.partner_alpha = PartnerAlphaManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def game_styles(self) -> list[str]:
        return [
            "calm_focus",
            "cozy_stream",
            "competitive_focus",
            "exploration",
            "creative_building",
            "strategy_support",
            "practice_coaching",
            "streaming_friendly",
        ]

    def game_support_modes(self) -> list[str]:
        return [
            "session_companion",
            "strategy_planner",
            "streaming_commentary_helper",
            "coaching_practice",
            "mood_support",
            "non_invasive_reminder",
        ]

    def safe_boundaries(self) -> list[str]:
        return [
            "no_automatic_game_screen_read",
            "no_automatic_screen_capture",
            "no_automatic_camera_access",
            "no_keyboard_or_mouse_control",
            "no_game_or_app_launch",
            "no_file_write",
            "no_command_execution",
            "no_external_action_execution",
        ]

    def classify_game_context(self, text: str) -> dict[str, Any]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "stream": "streaming",
            "youtube": "streaming",
            "twitch": "streaming",
            "minecraft": "creative_building",
            "survival": "survival",
            "boss": "strategy",
            "fight": "strategy",
            "aim": "practice",
            "practice": "practice",
            "rank": "competitive",
            "competitive": "competitive",
            "cozy": "cozy",
            "friendly": "friendly",
            "focus": "focused",
            "fokus": "focused",
            "tenang": "calm",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["general", "supportive"])

        if "streaming" in tags or "cozy" in tags:
            style = "cozy_stream"
        elif "competitive" in tags or "practice" in tags:
            style = "competitive_focus"
        elif "strategy" in tags or "survival" in tags:
            style = "strategy_support"
        elif "creative_building" in tags:
            style = "creative_building"
        elif "focused" in tags:
            style = "calm_focus"
        else:
            style = "calm_focus"

        return {
            "tags": tags[:6],
            "style": style,
            "streaming_related": "streaming" in tags or "cozy" in tags,
            "competitive_related": "competitive" in tags or "practice" in tags,
            "strategy_related": "strategy" in tags or "survival" in tags,
        }

    def base_plan(self, plan_type: str, target: str, recommended_steps: list[str]) -> dict[str, Any]:
        cleaned_target = " ".join(target.strip().split()) or "<unspecified>"
        context = self.classify_game_context(cleaned_target)
        expression_plan = self.expression_language.expression_plan(
            f"AURA menemani Kiput dalam game: {cleaned_target}"
        )

        read_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        screen_permission = self.permission_manager.check("screen_analyze")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "game_context": context,
            "game_style": context["style"],
            "game_tags": context["tags"],
            "expression_plan": expression_plan,
            "voice_tone_hint": expression_plan["voice_tone_hint"],
            "avatar_expression_hint": expression_plan["avatar_expression_hint"],
            "gesture_hint": expression_plan["gesture_hint"],
            "response_style_hint": expression_plan["response_style_hint"],
            "vision_context_ready": self.vision_runtime_alpha.status()["vision_context_ready"],
            "desktop_context_ready": self.desktop_assistant_alpha.status()["workspace_context_ready"],
            "media_context_ready": self.media_understanding.status()["context_ready"],
            "partner_context_ready": self.partner_alpha.status()["context_ready"],
            "recommended_steps": recommended_steps,
            "permissions": {
                "read_project": read_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "screen_analyze": screen_permission.to_dict(),
                "open_app": open_app_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "game_screen_read": False,
            "screen_capture_performed": False,
            "camera_access_performed": False,
            "keyboard_input_performed": False,
            "mouse_control_performed": False,
            "game_input_control": False,
            "game_app_opened": False,
            "desktop_action_performed": False,
            "voice_output_performed": False,
            "avatar_changed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Game companion plan is proposal-only.",
                "No game screen was read.",
                "No screenshot was captured.",
                "No camera was accessed.",
                "No keyboard or mouse input was performed.",
                "No game or desktop app was opened.",
                "No voice output was played.",
                "No avatar state was changed.",
                "No file was written.",
                "No command was executed.",
                "Future real gameplay assistance must go through explicit permission and confirmation.",
            ],
        }

    def session_plan(self, game_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="game_session",
            target=game_goal,
            recommended_steps=[
                "Clarify the game, mode, goal, and desired vibe for the session.",
                "Prepare a calm companion style that supports focus without interrupting gameplay.",
                "Use expression language hints for tone, avatar expression, and gesture.",
                "Prepare optional reminders for breaks, inventory checks, or stream pacing.",
                "Keep screen reading, game launching, input control, file writing, and commands disabled.",
            ],
        )

    def strategy_plan(self, strategy_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="game_strategy",
            target=strategy_goal,
            recommended_steps=[
                "Break the challenge into preparation, execution, and recovery phases.",
                "Prepare non-invasive strategy notes that can be read before gameplay.",
                "Avoid live screen interpretation until explicit vision runtime approval exists.",
                "Use a focused tone and concise response style for high-pressure gameplay.",
                "Keep all keyboard, mouse, game app, and command actions disabled.",
            ],
        )

    def streaming_plan(self, stream_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="game_streaming",
            target=stream_goal,
            recommended_steps=[
                "Clarify stream tone, audience style, and safe commentary boundaries.",
                "Prepare friendly commentary prompts that are expressive but not annoying.",
                "Suggest pacing notes for intro, gameplay, quiet moments, and outro.",
                "Use expression hints for a streaming-friendly avatar/voice style.",
                "Keep media capture, screen reading, voice output, and external actions disabled.",
            ],
        )

    def coaching_plan(self, coaching_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="game_coaching",
            target=coaching_goal,
            recommended_steps=[
                "Clarify practice objective, current difficulty, and improvement metric.",
                "Prepare a simple drill loop: warm-up, focused reps, review, and rest.",
                "Use supportive feedback style without judgment.",
                "Avoid live input control or screen reading until explicit runtime permission exists.",
                "Keep coaching as text-only planning in this foundation phase.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()

        return {
            "status": self.status_name,
            "context_ready": True,
            "game_status": status,
            "identity": self.load_identity(),
            "expression_context": self.expression_language.context(),
            "vision_context": self.vision_runtime_alpha.context(),
            "desktop_context": self.desktop_assistant_alpha.workspace_context(),
            "media_context": self.media_understanding.context(),
            "partner_context": self.partner_alpha.context(),
            "safe_current_capabilities": [
                "game_companion_status",
                "game_session_plan",
                "game_strategy_plan",
                "game_streaming_plan",
                "game_coaching_plan",
                "game_context",
            ],
            "disabled_capabilities": [
                "automatic_game_screen_read",
                "automatic_screen_capture",
                "automatic_camera_access",
                "automatic_keyboard_input",
                "automatic_mouse_control",
                "automatic_game_app_open",
                "automatic_voice_output",
                "automatic_avatar_change",
                "automatic_file_write",
                "command_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "game_screen_read": False,
            "game_input_control": False,
            "game_app_opened": False,
            "voice_output_performed": False,
            "avatar_changed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Game Companion context is read-only and preparation-only.",
        }

    def status(self) -> dict[str, Any]:
        identity = self.load_identity()
        modes = identity.get("modes", {}) if isinstance(identity, dict) else {}

        screen_permission = self.permission_manager.check("screen_analyze")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        expression_status = self.expression_language.status()
        vision_status = self.vision_runtime_alpha.status()
        desktop_status = self.desktop_assistant_alpha.status()
        media_status = self.media_understanding.status()
        partner_status = self.partner_alpha.status()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "companion_ready": True,
            "session_plan_ready": True,
            "strategy_plan_ready": True,
            "streaming_plan_ready": True,
            "coaching_plan_ready": True,
            "context_ready": True,
            "expression_integration_ready": expression_status["language_ready"],
            "vision_integration_ready": vision_status["alpha_ready"],
            "desktop_integration_ready": desktop_status["alpha_ready"],
            "media_integration_ready": media_status["understanding_ready"],
            "partner_integration_ready": partner_status["alpha_ready"],
            "supported_styles": len(self.game_styles()),
            "support_modes": len(self.game_support_modes()),
            "safety_boundaries": len(self.safe_boundaries()),
            "gaming_mode": modes.get("gaming", "playful and slightly mischievous"),
            "streaming_mode": modes.get("streaming", "expressive but not annoying"),
            "requires_screen_confirmation": screen_permission.requires_confirmation,
            "requires_open_app_confirmation": open_app_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "game_screen_read": False,
            "screen_capture": False,
            "camera_access": False,
            "game_input_control": False,
            "keyboard_input": False,
            "mouse_control": False,
            "game_app_opened": False,
            "desktop_action_execution": False,
            "voice_output": False,
            "avatar_changed": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Game Companion Foundation is online for safe, non-invasive game planning. It does not read game screen, control input, open games/apps, write files, or execute commands automatically.",
        }
