from pathlib import Path
from typing import Any

import yaml

from aura.awakening.awakening_manager import AwakeningManager
from aura.avatar.avatar_manager import AvatarManager
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.model_router.model_router import ModelRouter
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner


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
        self.vision_manager = VisionManager()
        self.vision_runtime_planner = VisionRuntimePlanner(project_root=project_root)
        self.awakening_manager = AwakeningManager(project_root=project_root)
        self.desktop_manager = DesktopBridgeManager(project_root=project_root)
        self.avatar_manager = AvatarManager(project_root=project_root)
        self.model_router = ModelRouter(project_root=project_root)
        self.tool_sandbox_manager = ToolSandboxManager(project_root=project_root)
        self.project_coding_manager = ProjectCodingManager(project_root=project_root)

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
        vision_status = self.vision_manager.status()
        vision_runtime_status = self.vision_runtime_planner.status()
        awakening_status = self.awakening_manager.build_status()
        desktop_status = self.desktop_manager.status()
        avatar_status = self.avatar_manager.status()
        model_router_status = self.model_router.status()
        tool_sandbox_status = self.tool_sandbox_manager.status()
        project_coding_status = self.project_coding_manager.status()

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
                "voice_providers": voice_status["providers"],
                "voice_runtime_candidates": voice_runtime_status["candidate_count"],
                "vision_providers": vision_status["providers"],
                "vision_runtime_candidates": vision_runtime_status["candidate_count"],
                "avatar_providers": avatar_status["providers"],
                "awakening_readiness": f"{awakening_status['ready_count']}/{awakening_status['total_pillars']}",
            },
            "systems": {
                "memory": "online",
                "journal": "online",
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
                "voice": voice_status["status"],
                "voice_runtime": voice_runtime_status["status"],
                "vision": vision_status["status"],
                "vision_runtime": vision_runtime_status["status"],
                "avatar": avatar_status["status"],
                "awakening": awakening_status["status"],
            },
            "runtime": {
                "real_voice_runtime": voice_runtime_status["runtime_ready"],
                "voice_runtime_planning": voice_runtime_status["planning_ready"],
                "real_vision_runtime": vision_runtime_status["runtime_ready"],
                "vision_runtime_planning": vision_runtime_status["planning_ready"],
                "avatar_runtime": avatar_status["runtime_ready"],
                "avatar_foundation": avatar_status["foundation_ready"],
                "alpha_core_loop": True,
                "model_routing": model_router_status["route_selection_ready"],
                "real_model_switching": model_router_status["runtime_switching_ready"],
                "tool_sandbox_ready": tool_sandbox_status["sandbox_ready"],
                "tool_sandbox_dry_run": tool_sandbox_status["dry_run_ready"],
                "real_tool_execution": tool_sandbox_status["real_execution_ready"],
                "project_coding_v2": project_coding_status["analysis_ready"],
                "project_patch_planning": project_coding_status["patch_planning_ready"],
                "project_file_write": project_coding_status["file_write_ready"],
                "desktop_bridge": desktop_status["bridge_ready"],
                "safe_action_execution": desktop_status["safe_action_execution"],
            },
            "summary": "AURA has a unified early foundation across memory, context, alpha core loop, model router, tool sandbox, project coding assistant, roles, skills, permissions, plugins, desktop bridge, voice runtime planning, vision runtime planning, avatar foundation, and awakening status.",
        }
