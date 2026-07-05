from pathlib import Path
from typing import Any

import yaml

from aura.actions.action_request_manager import ActionRequestManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.model_router.model_router import ModelRouter
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager


class PartnerAlphaManager:
    """
    AURA Partner Alpha.

    Current phase:
    - unify memory, reflection, briefing, awakening, model routing, safety, and runtime alpha layers
    - expose partner status
    - expose partner context
    - expose partner readiness report
    - recommend next safe development steps
    - never access microphone automatically
    - never access camera/screen automatically
    - never speak automatically
    - never render avatar automatically
    - never open desktop apps/browser/files automatically
    - never write files/memory/journal automatically
    - never execute commands
    """

    name = "aura_partner_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

        self.memory_store = MemoryStore(project_root=self.project_root)
        self.project_journal = ProjectJournal(project_root=self.project_root)
        self.memory_reflection = MemoryReflectionManager(project_root=self.project_root)
        self.daily_briefing = DailyBriefingManager(project_root=self.project_root)
        self.awakening = AwakeningManager(project_root=self.project_root)

        self.voice_runtime_alpha = VoiceRuntimeAlphaManager(project_root=self.project_root)
        self.vision_runtime_alpha = VisionRuntimeAlphaManager(project_root=self.project_root)
        self.avatar_runtime_alpha = AvatarRuntimeAlphaManager(project_root=self.project_root)
        self.desktop_assistant_alpha = DesktopAssistantAlphaManager(project_root=self.project_root)

        self.model_router = ModelRouter(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)
        self.project_coding = ProjectCodingManager(project_root=self.project_root)
        self.action_request_manager = ActionRequestManager()

        self.role_registry = build_builtin_role_registry()
        self.skill_registry = build_builtin_skill_registry()
        self.plugin_action_registry = build_builtin_plugin_action_registry()

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def collect_statuses(self) -> dict[str, Any]:
        return {
            "identity": self.load_identity(),
            "awakening": self.awakening.build_status(),
            "reflection": self.memory_reflection.status(),
            "briefing": self.daily_briefing.status(),
            "voice": self.voice_runtime_alpha.status(),
            "vision": self.vision_runtime_alpha.status(),
            "avatar": self.avatar_runtime_alpha.status(),
            "desktop": self.desktop_assistant_alpha.status(),
            "model_router": self.model_router.status(),
            "tool_sandbox": self.tool_sandbox.status(),
            "project_coding": self.project_coding.status(),
        }

    def action_safety_summary(self) -> dict[str, Any]:
        action_names = [
            "voice.speak_test",
            "vision.screen_plan",
            "vision.camera_plan",
            "avatar.expression_plan",
            "avatar.gesture_plan",
            "desktop.open_app_plan",
            "desktop.open_browser_plan",
            "desktop.open_file_plan",
            "write_file",
            "run_command",
            "wipe_data",
        ]

        requests = [
            self.action_request_manager.build(action_name=name).to_dict()
            for name in action_names
        ]

        return {
            "status": "checked",
            "actions_checked": len(requests),
            "ready_count": sum(1 for item in requests if item["request_state"] == "ready"),
            "requires_confirmation_count": sum(
                1 for item in requests
                if item["request_state"] == "requires_confirmation"
            ),
            "restricted_count": sum(
                1 for item in requests
                if item["request_state"] == "restricted"
            ),
            "requests": requests,
            "executed": False,
            "note": "Partner Alpha checked action safety metadata only. No action was executed.",
        }

    def component_states(self, statuses: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "name": "identity",
                "status": "online",
                "ready": bool(statuses["identity"].get("name", "AURA")),
                "summary": "AURA identity, creator, codename, and motto are available.",
            },
            {
                "name": "think",
                "status": statuses["model_router"]["status"],
                "ready": statuses["model_router"]["route_selection_ready"],
                "summary": "Model router and reasoning route metadata are available.",
            },
            {
                "name": "learn",
                "status": statuses["reflection"]["status"],
                "ready": (
                    statuses["reflection"]["reflection_ready"]
                    and statuses["briefing"]["briefing_ready"]
                ),
                "summary": "Memory, journal, reflection, and daily briefing are available as read-only context.",
            },
            {
                "name": "speak",
                "status": statuses["voice"]["status"],
                "ready": statuses["voice"]["alpha_ready"],
                "summary": "Voice Runtime Alpha can prepare speak plans without microphone access or speaker output.",
            },
            {
                "name": "see",
                "status": statuses["vision"]["status"],
                "ready": statuses["vision"]["alpha_ready"],
                "summary": "Vision Runtime Alpha can prepare screen/camera plans without real screen or camera access.",
            },
            {
                "name": "embody",
                "status": statuses["avatar"]["status"],
                "ready": statuses["avatar"]["alpha_ready"],
                "summary": "Avatar Runtime Alpha can prepare expression and gesture plans without rendering or avatar control.",
            },
            {
                "name": "act",
                "status": statuses["desktop"]["status"],
                "ready": statuses["desktop"]["alpha_ready"],
                "summary": "Desktop Assistant Alpha can prepare desktop action plans without opening apps, files, or browser.",
            },
            {
                "name": "safety",
                "status": statuses["tool_sandbox"]["status"],
                "ready": (
                    statuses["tool_sandbox"]["sandbox_ready"]
                    and not statuses["tool_sandbox"]["real_execution_ready"]
                ),
                "summary": "Tool sandbox, permissions, and action requests are active while real execution remains disabled.",
            },
            {
                "name": "project",
                "status": statuses["project_coding"]["status"],
                "ready": statuses["project_coding"]["analysis_ready"],
                "summary": "Project coding assistant can inspect and plan code changes without automatic file writes.",
            },
            {
                "name": "awakening",
                "status": statuses["awakening"]["status"],
                "ready": statuses["awakening"]["ready_count"] == statuses["awakening"]["total_pillars"],
                "summary": "AURA Awakening Alpha pillars are coherent across Speak, See, Think, and Learn.",
            },
        ]

    def readiness_report(self) -> dict[str, Any]:
        statuses = self.collect_statuses()
        components = self.component_states(statuses=statuses)
        ready_count = sum(1 for item in components if item["ready"])
        total_components = len(components)

        return {
            "status": self.status_name,
            "readiness_ready": True,
            "ready_count": ready_count,
            "total_components": total_components,
            "readiness": f"{ready_count}/{total_components}",
            "partner_ready": ready_count == total_components,
            "components": components,
            "blocked_real_world_access": [
                "microphone_access",
                "speaker_output",
                "screen_access",
                "camera_access",
                "avatar_rendering",
                "desktop_action_execution",
                "file_write",
                "memory_write",
                "journal_write",
                "command_execution",
            ],
            "safety_state": {
                "real_tool_execution": statuses["tool_sandbox"]["real_execution_ready"],
                "safe_action_execution": False,
                "memory_write": False,
                "journal_write": False,
                "file_write": False,
                "command_execution": False,
            },
            "write_performed": False,
            "command_execution_performed": False,
            "note": "Partner readiness is based on safe alpha/foundation availability, not real-world autonomous execution.",
        }

    def next_step_recommendation(self) -> dict[str, Any]:
        statuses = self.collect_statuses()
        latest = statuses["briefing"]["latest_milestone"]

        steps = [
            "Complete Sprint 50.0 validation across CLI, shell, system-status, boot, journal, git commit, and remote sync.",
            "After Sprint 50.0 is committed, pause for a Sprint 41-50 review and changelog.",
            "Confirm the safety boundary before moving into v0.51+.",
            "Start v0.51 Workspace Awareness Foundation after the review.",
            "Keep real microphone, screen, camera, desktop action, file write, and command execution disabled until explicit enablement design is complete.",
        ]

        if latest:
            steps.insert(
                0,
                f"Use the latest milestone as context before finalizing Partner Alpha: {latest}.",
            )

        return {
            "status": self.status_name,
            "recommendation_ready": True,
            "latest_milestone": latest,
            "recommended_next_steps": steps,
            "safety_notes": [
                "Recommendations are text-only.",
                "No file was written.",
                "No memory was written.",
                "No journal entry was written.",
                "No command was executed.",
                "No external action was executed.",
            ],
            "write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
        }

    def status(self) -> dict[str, Any]:
        statuses = self.collect_statuses()
        readiness = self.readiness_report()
        action_safety = self.action_safety_summary()

        voice = statuses["voice"]
        vision = statuses["vision"]
        avatar = statuses["avatar"]
        desktop = statuses["desktop"]

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "alpha_ready": True,
            "partner_ready": readiness["partner_ready"],
            "context_ready": True,
            "readiness_report_ready": readiness["readiness_ready"],
            "next_step_ready": True,
            "action_safety_ready": True,
            "component_ready_count": readiness["ready_count"],
            "component_total": readiness["total_components"],
            "component_readiness": readiness["readiness"],
            "memory_count": self.memory_store.count(),
            "journal_count": self.project_journal.count(),
            "roles": self.role_registry.count(),
            "skills": self.skill_registry.count(),
            "plugin_actions": self.plugin_action_registry.count(),
            "awakening_readiness": f"{statuses['awakening']['ready_count']}/{statuses['awakening']['total_pillars']}",
            "voice_runtime_alpha_ready": voice["alpha_ready"],
            "vision_runtime_alpha_ready": vision["alpha_ready"],
            "avatar_runtime_alpha_ready": avatar["alpha_ready"],
            "desktop_assistant_alpha_ready": desktop["alpha_ready"],
            "safe_action_execution": False,
            "external_action_execution": False,
            "microphone_access": False,
            "speaker_output": False,
            "screen_access": False,
            "camera_access": False,
            "avatar_rendering": False,
            "avatar_expression_changed": False,
            "avatar_gesture_changed": False,
            "desktop_app_opened": False,
            "desktop_browser_opened": False,
            "desktop_file_opened": False,
            "desktop_click_performed": False,
            "desktop_keyboard_input_performed": False,
            "memory_write": False,
            "journal_write": False,
            "file_write": False,
            "command_execution": False,
            "actions_checked": action_safety["actions_checked"],
            "actions_requiring_confirmation": action_safety["requires_confirmation_count"],
            "actions_restricted": action_safety["restricted_count"],
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "AURA Partner Alpha is online as a unified safe partner layer. It reads context and prepares recommendations only; it does not perform real-world or destructive actions automatically.",
        }

    def context(self) -> dict[str, Any]:
        statuses = self.collect_statuses()
        reflection_context = self.memory_reflection.reflection_context(limit=8)
        briefing_context = self.daily_briefing.context(limit=5)
        readiness = self.readiness_report()
        action_safety = self.action_safety_summary()

        return {
            "status": self.status_name,
            "context_ready": True,
            "identity": statuses["identity"],
            "project_summary": briefing_context["project_summary"],
            "latest_milestone": briefing_context["latest_milestone"],
            "memory_highlights": reflection_context["memory_highlights"],
            "project_insights": briefing_context["project_insights"],
            "recommended_next_steps": briefing_context["recommended_next_steps"],
            "readiness": readiness,
            "action_safety": action_safety,
            "runtime_alpha": {
                "voice": statuses["voice"],
                "vision": statuses["vision"],
                "avatar": statuses["avatar"],
                "desktop": statuses["desktop"],
            },
            "disabled_capabilities": [
                "automatic_microphone_access",
                "automatic_speaker_output",
                "automatic_screen_access",
                "automatic_camera_access",
                "automatic_avatar_rendering",
                "automatic_desktop_action_execution",
                "automatic_memory_write",
                "automatic_journal_write",
                "automatic_file_write",
                "command_execution",
            ],
            "write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Partner context is read-only and preparation-only.",
        }
