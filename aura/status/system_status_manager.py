from pathlib import Path
from typing import Any

import yaml

from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.avatar.avatar_manager import AvatarManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
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
            "summary": "AURA has a unified early foundation across memory, reflection, daily briefing, partner alpha, context, alpha core loop, model router, tool sandbox, project coding assistant, roles, skills, permissions, plugins, desktop bridge, desktop assistant alpha, voice runtime planning, voice runtime alpha, vision runtime planning, vision runtime alpha, avatar foundation, avatar runtime alpha, and awakening status.",
        }
