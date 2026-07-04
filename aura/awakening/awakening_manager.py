from pathlib import Path

from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.voice.voice_manager import VoiceManager


class AwakeningManager:
    """
    AURA Awakening Alpha status manager.

    Awakening Alpha means AURA has a coherent foundation for:
    - Speak
    - See
    - Think
    - Learn

    This does not mean all runtime abilities are fully active yet.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_store = MemoryStore(project_root=project_root)
        self.project_journal = ProjectJournal(project_root=project_root)
        self.voice_manager = VoiceManager()
        self.role_registry = build_builtin_role_registry()
        self.skill_registry = build_builtin_skill_registry()
        self.plugin_action_registry = build_builtin_plugin_action_registry()

    def build_status(self) -> dict:
        voice_status = self.voice_manager.status()

        speak_state = {
            "name": "Speak",
            "status": "foundation",
            "ready": True,
            "description": "Voice foundation is online with STT/TTS placeholder providers.",
            "note": "Real microphone and speaker runtime are not connected yet.",
        }

        see_state = {
            "name": "See",
            "status": "planned",
            "ready": False,
            "description": "Vision, screen analyzer, and camera analyzer are planned.",
            "note": "Screen/camera runtime is not connected yet.",
        }

        think_state = {
            "name": "Think",
            "status": "online",
            "ready": True,
            "description": "Reasoning provider, role system, skill registry, and plugin action interface are online.",
            "note": "Local Ollama reasoning is active through the provider system.",
        }

        learn_state = {
            "name": "Learn",
            "status": "online",
            "ready": True,
            "description": "Memory, project journal, and context systems are online.",
            "note": "AURA can preserve project progress and build context packets.",
        }

        pillars = [
            speak_state,
            see_state,
            think_state,
            learn_state,
        ]

        ready_count = sum(1 for pillar in pillars if pillar["ready"])

        return {
            "milestone": "AURA AWAKENING ALPHA",
            "status": "alpha",
            "phase": "Genesis",
            "ready_count": ready_count,
            "total_pillars": len(pillars),
            "pillars": pillars,
            "voice_providers": voice_status["providers"],
            "memory_records": self.memory_store.count(),
            "journal_entries": self.project_journal.count(),
            "roles": self.role_registry.count(),
            "skills": self.skill_registry.count(),
            "plugin_actions": self.plugin_action_registry.count(),
            "summary": "AURA has a coherent early mind foundation, but vision and real voice runtime are not fully connected yet.",
        }
