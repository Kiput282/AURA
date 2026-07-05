from pathlib import Path
from typing import Any

import yaml

from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.avatar.avatar_manager import AvatarManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
from aura.blender.blender_bridge_foundation_manager import BlenderBridgeFoundationManager
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.game.game_companion_foundation_manager import GameCompanionFoundationManager
from aura.streaming.streaming_safety_foundation_manager import StreamingSafetyFoundationManager
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.model_router.model_router import ModelRouter
from aura.partner.partner_alpha_manager import PartnerAlphaManager
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager


class SystemStatusManager:
    """
    Unified System Status for AURA.

    This manager creates one high-level dashboard for AURA's current foundation.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.identity_path = project_root / "aura" / "personality" / "identity.yaml"
        self.settings_path = project_root / "aura" / "config" / "settings.yaml"

        self.memory_store = MemoryStore(project_root=project_root)
        self.project_journal = ProjectJournal(project_root=project_root)
        self.role_registry = build_builtin_role_registry()
        self.skill_registry = build_builtin_skill_registry()
        self.plugin_action_registry = build_builtin_plugin_action_registry()
        self.voice_manager = VoiceManager()
        self.voice_runtime_planner = VoiceRuntimePlanner(project_root=project_root)
        self.voice_runtime_alpha_manager = VoiceRuntimeAlphaManager(project_root=project_root)
        self.vision_manager = VisionManager()
        self.vision_runtime_planner = VisionRuntimePlanner(project_root=project_root)
        self.vision_runtime_alpha_manager = VisionRuntimeAlphaManager(project_root=project_root)
        self.awakening_manager = AwakeningManager(project_root=project_root)
        self.desktop_manager = DesktopBridgeManager(project_root=project_root)
        self.desktop_assistant_alpha_manager = DesktopAssistantAlphaManager(project_root=project_root)
        self.avatar_manager = AvatarManager(project_root=project_root)
        self.avatar_runtime_alpha_manager = AvatarRuntimeAlphaManager(project_root=project_root)
        self.model_router = ModelRouter(project_root=project_root)
        self.tool_sandbox_manager = ToolSandboxManager(project_root=project_root)
        self.project_coding_manager = ProjectCodingManager(project_root=project_root)
        self.memory_reflection_manager = MemoryReflectionManager(project_root=project_root)
        self.daily_briefing_manager = DailyBriefingManager(project_root=project_root)
        self.partner_alpha_manager = PartnerAlphaManager(project_root=project_root)
        self.workspace_awareness_manager = WorkspaceAwarenessManager(project_root=project_root)
        self.blender_bridge_manager = BlenderBridgeFoundationManager(project_root=project_root)
        self.media_understanding_manager = MediaUnderstandingFoundationManager(project_root=project_root)
        self.expression_language_manager = ExpressionLanguageManager(project_root=project_root)
        self.game_companion_manager = GameCompanionFoundationManager(project_root=project_root)
        self.streaming_safety_manager = StreamingSafetyFoundationManager(project_root=project_root)

    def load_yaml(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}

        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def build_status(self) -> dict[str, Any]:
        identity = self.load_yaml(self.identity_path)
        settings = self.load_yaml(self.settings_path)

        app_settings = settings.get("app", {})
        reasoning_settings = settings.get("reasoning", {})

        voice_status = self.voice_manager.status()
        voice_runtime_status = self.voice_runtime_planner.status()
        voice_runtime_alpha_status = self.voice_runtime_alpha_manager.status()
        vision_status = self.vision_manager.status()
        vision_runtime_status = self.vision_runtime_planner.status()
        vision_runtime_alpha_status = self.vision_runtime_alpha_manager.status()
        awakening_status = self.awakening_manager.build_status()
        desktop_status = self.desktop_manager.status()
        desktop_alpha_status = self.desktop_assistant_alpha_manager.status()
        avatar_status = self.avatar_manager.status()
        avatar_runtime_alpha_status = self.avatar_runtime_alpha_manager.status()
        model_router_status = self.model_router.status()
        tool_sandbox_status = self.tool_sandbox_manager.status()
        project_coding_status = self.project_coding_manager.status()
        memory_reflection_status = self.memory_reflection_manager.status()
        daily_briefing_status = self.daily_briefing_manager.status()
        partner_alpha_status = self.partner_alpha_manager.status()
        workspace_awareness_status = self.workspace_awareness_manager.status()
        blender_bridge_status = self.blender_bridge_manager.status()
        media_understanding_status = self.media_understanding_manager.status()
        expression_language_status = self.expression_language_manager.status()
        game_companion_status = self.game_companion_manager.status()
        streaming_safety_status = self.streaming_safety_manager.status()

        return {
            "project_root": str(self.project_root),
            "identity": {
                "name": identity.get("name", "AURA"),
                "version": identity.get("version", "unknown"),
                "codename": identity.get("codename", "Genesis"),
                "creator": identity.get("creator", "Kiput"),
                "motto": identity.get("motto", "Grow Together"),
            },
            "app": {
                "name": app_settings.get("name", "AURA"),
                "environment": app_settings.get("environment", "development"),
                "debug": app_settings.get("debug", False),
            },
            "reasoning": {
                "provider": reasoning_settings.get("provider", "unknown"),
                "model": reasoning_settings.get("model", "unknown"),
                "host": reasoning_settings.get("host", "unknown"),
            },
            "foundation": {
                "memory_records": self.memory_store.count(),
                "journal_entries": self.project_journal.count(),
                "roles": self.role_registry.count(),
                "skills": self.skill_registry.count(),
                "plugin_actions": self.plugin_action_registry.count(),
                "core_loop_steps": 7,
                "model_routes": model_router_status["routes"],
                "sandbox_allowed_commands": tool_sandbox_status["allowed_command_count"],
                "sandbox_blocked_commands": tool_sandbox_status["blocked_command_count"],
                "sandbox_blocked_patterns": tool_sandbox_status["blocked_pattern_count"],
                "project_python_files": project_coding_status["python_files"],
                "reflection_milestones": memory_reflection_status["milestone_count"],
                "briefing_sections": daily_briefing_status["briefing_sections"],
                "partner_alpha_sections": partner_alpha_status["sections"],
                "workspace_awareness_sections": workspace_awareness_status["sections"],
                "workspace_important_files": workspace_awareness_status["existing_important_file_count"],
                "blender_bridge_sections": blender_bridge_status["sections"],
                "blender_asset_candidates": blender_bridge_status["asset_candidate_count"],
                "media_understanding_sections": media_understanding_status["sections"],
                "media_asset_candidates": media_understanding_status["candidate_count"],
                "expression_language_sections": expression_language_status["sections"],
                "expression_emotion_tags": expression_language_status["emotion_tags"],
                "game_companion_sections": game_companion_status["sections"],
                "game_support_modes": game_companion_status["support_modes"],
                "streaming_safety_sections": streaming_safety_status["sections"],
                "streaming_safety_categories": streaming_safety_status["safety_categories"],
                "desktop_alpha_sections": desktop_alpha_status["sections"],
                "voice_providers": voice_status["providers"],
                "voice_runtime_candidates": voice_runtime_status["candidate_count"],
                "voice_runtime_alpha_sections": voice_runtime_alpha_status["sections"],
                "vision_providers": vision_status["providers"],
                "vision_runtime_candidates": vision_runtime_status["candidate_count"],
                "vision_runtime_alpha_sections": vision_runtime_alpha_status["sections"],
                "avatar_providers": avatar_status["providers"],
                "avatar_runtime_alpha_sections": avatar_runtime_alpha_status["sections"],
                "awakening_readiness": f"{awakening_status['ready_count']}/{awakening_status['total_pillars']}",
            },
            "systems": {
                "memory": "online",
                "journal": "online",
                "memory_reflection": memory_reflection_status["status"],
                "daily_briefing": daily_briefing_status["status"],
                "partner_alpha": partner_alpha_status["status"],
                "workspace_awareness": workspace_awareness_status["status"],
                "blender_bridge": blender_bridge_status["status"],
                "media_understanding": media_understanding_status["status"],
                "expression_language": expression_language_status["status"],
                "game_companion": game_companion_status["status"],
                "streaming_safety": streaming_safety_status["status"],
                "context": "online",
                "core_loop": "alpha",
                "model_router": model_router_status["status"],
                "tool_sandbox": tool_sandbox_status["status"],
                "permissions": "online",
                "skills": "online",
                "plugin_actions": "online",
                "project_plugin": "online",
                "project_coding": project_coding_status["status"],
                "desktop_bridge": desktop_status["status"],
                "desktop_assistant_alpha": desktop_alpha_status["status"],
                "voice": voice_status["status"],
                "voice_runtime": voice_runtime_status["status"],
                "voice_runtime_alpha": voice_runtime_alpha_status["status"],
                "vision": vision_status["status"],
                "vision_runtime": vision_runtime_status["status"],
                "vision_runtime_alpha": vision_runtime_alpha_status["status"],
                "avatar": avatar_status["status"],
                "avatar_runtime_alpha": avatar_runtime_alpha_status["status"],
                "awakening": awakening_status["status"],
            },
            "runtime": {
                "real_voice_runtime": voice_runtime_status["runtime_ready"],
                "voice_runtime_planning": voice_runtime_status["planning_ready"],
                "voice_runtime_alpha_ready": voice_runtime_alpha_status["alpha_ready"],
                "voice_speak_plan_ready": voice_runtime_alpha_status["speak_plan_ready"],
                "voice_speak_test_ready": voice_runtime_alpha_status["speak_test_ready"],
                "voice_tts_backend_found": voice_runtime_alpha_status["tts_backend_found"],
                "voice_speaker_output": voice_runtime_alpha_status["speaker_output"],
                "voice_microphone_access": voice_runtime_alpha_status["microphone_access"],
                "voice_command_execution": voice_runtime_alpha_status["command_execution"],
                "real_vision_runtime": vision_runtime_status["runtime_ready"],
                "vision_runtime_planning": vision_runtime_status["planning_ready"],
                "vision_runtime_alpha_ready": vision_runtime_alpha_status["alpha_ready"],
                "vision_screen_plan_ready": vision_runtime_alpha_status["screen_plan_ready"],
                "vision_camera_plan_ready": vision_runtime_alpha_status["camera_plan_ready"],
                "vision_screen_backend_found": vision_runtime_alpha_status["screen_backend_found"],
                "vision_camera_backend_found": vision_runtime_alpha_status["camera_backend_found"],
                "vision_screen_access": vision_runtime_alpha_status["screen_access"],
                "vision_camera_access": vision_runtime_alpha_status["camera_access"],
                "vision_command_execution": vision_runtime_alpha_status["command_execution"],
                "avatar_runtime": avatar_status["runtime_ready"],
                "avatar_foundation": avatar_status["foundation_ready"],
                "avatar_runtime_alpha_ready": avatar_runtime_alpha_status["alpha_ready"],
                "avatar_expression_plan_ready": avatar_runtime_alpha_status["expression_plan_ready"],
                "avatar_gesture_plan_ready": avatar_runtime_alpha_status["gesture_plan_ready"],
                "avatar_render_backend_found": avatar_runtime_alpha_status["render_backend_found"],
                "avatar_media_backend_found": avatar_runtime_alpha_status["media_backend_found"],
                "avatar_loaded": avatar_runtime_alpha_status["avatar_loaded"],
                "avatar_render_performed": avatar_runtime_alpha_status["render_performed"],
                "avatar_command_execution": avatar_runtime_alpha_status["command_execution"],
                "avatar_image_file_write": avatar_runtime_alpha_status["image_file_write"],
                "avatar_animation_file_write": avatar_runtime_alpha_status["animation_file_write"],
                "alpha_core_loop": True,
                "model_routing": model_router_status["route_selection_ready"],
                "real_model_switching": model_router_status["runtime_switching_ready"],
                "tool_sandbox_ready": tool_sandbox_status["sandbox_ready"],
                "tool_sandbox_dry_run": tool_sandbox_status["dry_run_ready"],
                "real_tool_execution": tool_sandbox_status["real_execution_ready"],
                "project_coding_v2": project_coding_status["analysis_ready"],
                "project_patch_planning": project_coding_status["patch_planning_ready"],
                "project_file_write": project_coding_status["file_write_ready"],
                "memory_reflection_ready": memory_reflection_status["reflection_ready"],
                "memory_reflection_write": memory_reflection_status["automatic_memory_write"],
                "memory_reflection_delete": memory_reflection_status["automatic_memory_delete"],
                "daily_briefing_ready": daily_briefing_status["briefing_ready"],
                "daily_briefing_write": daily_briefing_status["automatic_file_write"],
                "daily_briefing_command_execution": daily_briefing_status["command_execution"],
                "partner_alpha_ready": partner_alpha_status["alpha_ready"],
                "partner_ready": partner_alpha_status["partner_ready"],
                "partner_context_ready": partner_alpha_status["context_ready"],
                "partner_readiness_report_ready": partner_alpha_status["readiness_report_ready"],
                "partner_next_step_ready": partner_alpha_status["next_step_ready"],
                "partner_microphone_access": partner_alpha_status["microphone_access"],
                "partner_speaker_output": partner_alpha_status["speaker_output"],
                "partner_screen_access": partner_alpha_status["screen_access"],
                "partner_camera_access": partner_alpha_status["camera_access"],
                "partner_desktop_action_execution": partner_alpha_status["external_action_execution"],
                "partner_memory_write": partner_alpha_status["memory_write"],
                "partner_journal_write": partner_alpha_status["journal_write"],
                "partner_file_write": partner_alpha_status["file_write"],
                "partner_command_execution": partner_alpha_status["command_execution"],
                "workspace_awareness_ready": workspace_awareness_status["awareness_ready"],
                "workspace_map_ready": workspace_awareness_status["workspace_map_ready"],
                "workspace_context_ready": workspace_awareness_status["workspace_context_ready"],
                "workspace_current_state_ready": workspace_awareness_status["current_state_ready"],
                "workspace_important_files_ready": workspace_awareness_status["important_files_ready"],
                "workspace_file_write": workspace_awareness_status["file_write"],
                "workspace_memory_write": workspace_awareness_status["memory_write"],
                "workspace_journal_write": workspace_awareness_status["journal_write"],
                "workspace_command_execution": workspace_awareness_status["command_execution"],
                "workspace_external_action_execution": workspace_awareness_status["external_action_execution"],
                "blender_bridge_ready": blender_bridge_status["bridge_ready"],
                "blender_scene_plan_ready": blender_bridge_status["scene_plan_ready"],
                "blender_asset_plan_ready": blender_bridge_status["asset_plan_ready"],
                "blender_texture_plan_ready": blender_bridge_status["texture_plan_ready"],
                "blender_material_plan_ready": blender_bridge_status["material_plan_ready"],
                "blender_rigging_plan_ready": blender_bridge_status["rigging_plan_ready"],
                "blender_animation_plan_ready": blender_bridge_status["animation_plan_ready"],
                "blender_context_ready": blender_bridge_status["context_ready"],
                "blender_backend_found": blender_bridge_status["backend_found"],
                "blender_bpy_found": blender_bridge_status["bpy_found"],
                "blender_executable_found": blender_bridge_status["blender_executable_found"],
                "blender_app_opened": blender_bridge_status["blender_app_opened"],
                "blender_script_executed": blender_bridge_status["blender_script_executed"],
                "blender_file_write": blender_bridge_status["file_write"],
                "blender_command_execution": blender_bridge_status["command_execution"],
                "blender_external_action_execution": blender_bridge_status["external_action_execution"],
                "media_understanding_ready": media_understanding_status["understanding_ready"],
                "media_asset_summary_ready": media_understanding_status["asset_summary_ready"],
                "media_image_plan_ready": media_understanding_status["image_plan_ready"],
                "media_texture_reference_ready": media_understanding_status["texture_reference_ready"],
                "media_thumbnail_review_ready": media_understanding_status["thumbnail_review_ready"],
                "media_video_plan_ready": media_understanding_status["video_plan_ready"],
                "media_context_ready": media_understanding_status["context_ready"],
                "media_metadata_inspection_ready": media_understanding_status["metadata_inspection_ready"],
                "media_file_opened": media_understanding_status["media_file_opened"],
                "media_pixel_read": media_understanding_status["media_pixel_read"],
                "media_file_write": media_understanding_status["file_write"],
                "media_command_execution": media_understanding_status["command_execution"],
                "media_external_action_execution": media_understanding_status["external_action_execution"],
                "expression_language_ready": expression_language_status["language_ready"],
                "expression_state_ready": expression_language_status["state_ready"],
                "expression_plan_ready": expression_language_status["plan_ready"],
                "expression_voice_hint_ready": expression_language_status["voice_hint_ready"],
                "expression_avatar_hint_ready": expression_language_status["avatar_hint_ready"],
                "expression_gesture_hint_ready": expression_language_status["gesture_hint_ready"],
                "expression_context_ready": expression_language_status["context_ready"],
                "expression_avatar_changed": expression_language_status["avatar_changed"],
                "expression_gesture_changed": expression_language_status["gesture_changed"],
                "expression_voice_output": expression_language_status["voice_output"],
                "expression_file_write": expression_language_status["file_write"],
                "expression_command_execution": expression_language_status["command_execution"],
                "expression_external_action_execution": expression_language_status["external_action_execution"],
                "game_companion_ready": game_companion_status["companion_ready"],
                "game_session_plan_ready": game_companion_status["session_plan_ready"],
                "game_strategy_plan_ready": game_companion_status["strategy_plan_ready"],
                "game_streaming_plan_ready": game_companion_status["streaming_plan_ready"],
                "game_coaching_plan_ready": game_companion_status["coaching_plan_ready"],
                "game_context_ready": game_companion_status["context_ready"],
                "game_expression_integration_ready": game_companion_status["expression_integration_ready"],
                "game_vision_integration_ready": game_companion_status["vision_integration_ready"],
                "game_desktop_integration_ready": game_companion_status["desktop_integration_ready"],
                "game_partner_integration_ready": game_companion_status["partner_integration_ready"],
                "game_screen_read": game_companion_status["game_screen_read"],
                "game_input_control": game_companion_status["game_input_control"],
                "game_app_opened": game_companion_status["game_app_opened"],
                "game_file_write": game_companion_status["file_write"],
                "game_command_execution": game_companion_status["command_execution"],
                "game_external_action_execution": game_companion_status["external_action_execution"],
                "streaming_safety_ready": streaming_safety_status["safety_ready"],
                "streaming_context_plan_ready": streaming_safety_status["context_plan_ready"],
                "streaming_chat_safety_ready": streaming_safety_status["chat_safety_ready"],
                "streaming_content_boundary_ready": streaming_safety_status["content_boundary_ready"],
                "streaming_privacy_plan_ready": streaming_safety_status["privacy_plan_ready"],
                "streaming_moderation_plan_ready": streaming_safety_status["moderation_plan_ready"],
                "streaming_safety_context_ready": streaming_safety_status["context_ready"],
                "streaming_game_integration_ready": streaming_safety_status["game_integration_ready"],
                "streaming_expression_integration_ready": streaming_safety_status["expression_integration_ready"],
                "streaming_media_integration_ready": streaming_safety_status["media_integration_ready"],
                "streaming_vision_integration_ready": streaming_safety_status["vision_integration_ready"],
                "streaming_desktop_integration_ready": streaming_safety_status["desktop_integration_ready"],
                "streaming_live_chat_read": streaming_safety_status["live_chat_read"],
                "streaming_message_sent": streaming_safety_status["message_sent"],
                "streaming_moderation_action": streaming_safety_status["moderation_action"],
                "streaming_screen_capture": streaming_safety_status["screen_capture"],
                "streaming_browser_opened": streaming_safety_status["browser_opened"],
                "streaming_app_opened": streaming_safety_status["app_opened"],
                "streaming_file_write": streaming_safety_status["file_write"],
                "streaming_command_execution": streaming_safety_status["command_execution"],
                "streaming_external_action_execution": streaming_safety_status["external_action_execution"],
                "desktop_bridge": desktop_status["bridge_ready"],
                "safe_action_execution": desktop_status["safe_action_execution"],
                "desktop_assistant_alpha_ready": desktop_alpha_status["alpha_ready"],
                "desktop_action_plan_ready": desktop_alpha_status["action_plan_ready"],
                "desktop_open_app_plan_ready": desktop_alpha_status["open_app_plan_ready"],
                "desktop_open_browser_plan_ready": desktop_alpha_status["open_browser_plan_ready"],
                "desktop_open_file_plan_ready": desktop_alpha_status["open_file_plan_ready"],
                "desktop_workspace_context_ready": desktop_alpha_status["workspace_context_ready"],
                "desktop_app_opened": desktop_alpha_status["app_opened"],
                "desktop_browser_opened": desktop_alpha_status["browser_opened"],
                "desktop_file_opened": desktop_alpha_status["file_opened"],
                "desktop_click_performed": desktop_alpha_status["click_performed"],
                "desktop_keyboard_input_performed": desktop_alpha_status["keyboard_input_performed"],
                "desktop_file_write": desktop_alpha_status["file_write"],
                "desktop_command_execution": desktop_alpha_status["command_execution"],
            },
            "summary": "AURA has a unified early foundation across memory, reflection, daily briefing, partner alpha, workspace awareness, blender bridge, media understanding, expression language, game companion, streaming safety, context, alpha core loop, model router, tool sandbox, project coding assistant, roles, skills, permissions, plugins, desktop bridge, desktop assistant alpha, voice runtime planning, voice runtime alpha, vision runtime planning, vision runtime alpha, avatar foundation, avatar runtime alpha, and awakening status.",
        }
