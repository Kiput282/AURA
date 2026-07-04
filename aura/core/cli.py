import argparse
from pathlib import Path
from typing import Any

import yaml

from aura.core.chat import AuraChat
from aura.core.shell import AuraShell
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.journal.project_journal import ProjectJournal
from aura.context.context_manager import ContextManager
from aura.permissions.permission_manager import PermissionManager
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.voice.voice_manager import VoiceManager
from aura.awakening.awakening_manager import AwakeningManager
from aura.vision.vision_manager import VisionManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.utils.logger import disable_logging


class AuraCLI:
    """
    Simple command-line interface for AURA.

    Supported commands:
    - remember
    - recall
    - chat
    - history
    - provider
    - provider-check
    - reason
    - reason-check
    - shell
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.settings_path = self.project_root / "aura" / "config" / "settings.yaml"

    def get_memory_store(self) -> MemoryStore:
        return MemoryStore(project_root=self.project_root)

    def load_settings(self) -> dict:
        if not self.settings_path.exists():
            return {}

        with self.settings_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def configured_provider_name(self) -> str:
        settings = self.load_settings()
        reasoning = settings.get("reasoning", {})
        return reasoning.get("provider", "unknown")

    def print_provider_runtime_check(self, runtime: dict[str, Any]) -> None:
        print("AURA Provider Runtime Check")
        print("===========================")
        print(f"Provider : {runtime.get('provider', 'unknown')} v{runtime.get('version', 'unknown')}")
        print(f"Config   : {self.configured_provider_name()}")
        print(f"Status   : {runtime.get('status', 'UNKNOWN')}")
        print(f"Message  : {runtime.get('message', '-')}")

        if "host" in runtime:
            print(f"Host     : {runtime.get('host')}")

        if "model" in runtime:
            print(f"Model    : {runtime.get('model')}")

        available_models = runtime.get("available_models", [])
        if available_models:
            print("Models   :")
            for model in available_models:
                print(f"- {model}")
        elif "available_models" in runtime:
            print("Models   : none")

    def remember(self, content: str) -> None:
        memory_store = self.get_memory_store()

        memory = MemoryItem(
            kind="user_note",
            content=content,
            metadata={
                "source": "AuraCLI",
            },
        )

        memory_store.save(memory)

        print("Memory saved.")
        print(f"Content: {content}")

    def recall(self, limit: int = 5) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_recent(limit=limit)

        print("AURA Memory Recall")
        print("==================")

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def chat(self, message: str) -> None:
        chat = AuraChat(project_root=self.project_root)
        response = chat.respond(message, source="AuraCLI")
        print(response)

    def history(self, limit: int = 5) -> None:
        chat = AuraChat(project_root=self.project_root)
        turns = chat.recent_conversations(limit=limit)

        print("AURA Chat History")
        print("=================")

        if not turns:
            print("No chat history found.")
            return

        for turn in turns:
            print(f"User: {turn.user_message}")
            print(f"AURA: {turn.aura_response}")
            print("---")

    def provider(self) -> None:
        chat = AuraChat(project_root=self.project_root)
        provider = chat.provider_info()
        configured_provider = self.configured_provider_name()

        print("AURA Reasoning Provider")
        print("=======================")
        print(f"Name    : {provider['name']}")
        print(f"Version : {provider['version']}")
        print(f"Config  : {configured_provider}")

    def provider_check(self) -> None:
        chat = AuraChat(project_root=self.project_root)
        runtime = chat.provider_runtime_check()
        self.print_provider_runtime_check(runtime)

    def memory_count(self) -> None:
        memory_store = self.get_memory_store()
        count = memory_store.count()

        print("AURA Memory Count")
        print("=================")
        print(f"Records: {count}")

    def memory_list(self, limit: int = 5) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_recent(limit=limit)

        print("AURA Memory List")
        print("================")
        print(f"Limit: {limit}")
        print()

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def memory_delete(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.find_by_id(memory_id=memory_id)

        print("AURA Memory Delete")
        print("==================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        if memory_store.is_protected(memory):
            print("Cannot delete protected system memory.")
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")
            return

        deleted_memory = memory_store.delete_by_id(memory_id=memory_id)

        if deleted_memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Deleted memory:")
        print(f"- ID: {deleted_memory.id}")
        print(f"  Kind: {deleted_memory.kind}")
        print(f"  Content: {deleted_memory.content}")

    def memory_search(self, query: str, limit: int = 5) -> None:
        chat = AuraChat(project_root=self.project_root)
        memories = chat.relevant_memories(message=query, limit=limit)

        print("AURA Relevant Memories")
        print("======================")
        print(f"Query: {query}")
        print()

        if not memories:
            print("No relevant memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def get_project_journal(self) -> ProjectJournal:
        return ProjectJournal(project_root=self.project_root)

    def journal(self, limit: int = 5) -> None:
        project_journal = self.get_project_journal()
        entries = project_journal.list_recent(limit=limit)

        print("AURA Project Journal")
        print("====================")
        print(f"Limit: {limit}")
        print()

        if not entries:
            print("No journal entries found.")
            return

        for entry in entries:
            print(f"- ID: {entry.id}")
            print(f"  Title: {entry.title}")
            print(f"  Content: {entry.content}")
            print(f"  Created At: {entry.created_at}")

    def journal_add(self, content: str) -> None:
        project_journal = self.get_project_journal()

        title = "Manual Entry"
        if ":" in content:
            title = content.split(":", 1)[0].strip() or "Manual Entry"

        entry = project_journal.add(
            title=title,
            content=content,
            metadata={"source": "cli"},
        )

        print("AURA Project Journal")
        print("====================")
        print("Journal entry saved.")
        print(f"- ID: {entry.id}")
        print(f"  Title: {entry.title}")
        print(f"  Content: {entry.content}")

    def journal_count(self) -> None:
        project_journal = self.get_project_journal()

        print("AURA Project Journal Count")
        print("==========================")
        print(f"Entries: {project_journal.count()}")

    def roles(self) -> None:
        registry = build_builtin_role_registry()
        roles = registry.list_roles()

        print("AURA Roles")
        print("==========")
        print(f"Total: {registry.count()}")
        print()

        for role in roles:
            print(f"- {role.name}")
            print(f"  Status      : {role.status}")
            print(f"  Provider    : {role.provider}")
            print(f"  Model       : {role.model}")
            print(f"  Description : {role.description}")

            if role.capabilities:
                print("  Capabilities:")
                for capability in role.capabilities:
                    print(f"  - {capability}")

            print()

    def memory_pin(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.set_pinned(memory_id=memory_id, pinned=True)

        print("AURA Memory Pin")
        print("===============")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory pinned.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_unpin(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.set_pinned(memory_id=memory_id, pinned=False)

        print("AURA Memory Unpin")
        print("=================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory unpinned.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_importance(self, memory_id: str, importance: int) -> None:
        memory_store = self.get_memory_store()

        print("AURA Memory Importance")
        print("======================")

        try:
            memory = memory_store.set_importance(
                memory_id=memory_id,
                importance=importance,
            )
        except ValueError as error:
            print(str(error))
            return

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory importance updated.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_pinned(self) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_pinned()

        print("AURA Pinned Memories")
        print("====================")

        if not memories:
            print("No pinned memories found.")
            return

        for memory in memories:
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
            print(f"  Importance: {memory.metadata.get('importance', 3)}")
            print(f"  Content: {memory.content}")

    def context(self, message: str) -> None:
        context_manager = ContextManager(project_root=self.project_root)
        packet = context_manager.build(user_message=message)

        print(packet.to_text())

    def permissions(self) -> None:
        permission_manager = PermissionManager()

        print("AURA Permissions")
        print("================")

        for result in permission_manager.list_permissions():
            print(f"- {result.action}")
            print(f"  Level       : {int(result.level)} - {result.level.label}")
            print(f"  Allowed     : {result.allowed}")
            print(f"  Confirmation: {result.requires_confirmation}")
            print(f"  Description : {result.description}")
            print(f"  Reason      : {result.reason}")
            print()

    def permission_check(self, action: str) -> None:
        permission_manager = PermissionManager()
        result = permission_manager.check(action=action)

        print("AURA Permission Check")
        print("=====================")
        print(f"Action      : {result.action}")
        print(f"Level       : {int(result.level)} - {result.level.label}")
        print(f"Allowed     : {result.allowed}")
        print(f"Confirmation: {result.requires_confirmation}")
        print(f"Description : {result.description}")
        print(f"Reason      : {result.reason}")

    def skills(self) -> None:
        registry = build_builtin_skill_registry()

        print("AURA Skills")
        print("===========")
        print(f"Total: {registry.count()}")
        print()

        for skill in registry.list_skills():
            permission = registry.check_permission(skill)

            print(f"- {skill.name}")
            print(f"  Status      : {skill.status}")
            print(f"  Role        : {skill.role}")
            print(f"  Permission  : {skill.permission_action}")
            print(f"  Allowed     : {permission.allowed}")
            print(f"  Confirmation: {permission.requires_confirmation}")
            print(f"  Description : {skill.description}")

            if skill.capabilities:
                print("  Capabilities:")
                for capability in skill.capabilities:
                    print(f"  - {capability}")

            print()

    def skill_detail(self, name: str) -> None:
        registry = build_builtin_skill_registry()
        skill = registry.get(name=name)

        print("AURA Skill")
        print("==========")

        if skill is None:
            print(f"Skill not found: {name}")
            return

        permission = registry.check_permission(skill)

        print(f"Name        : {skill.name}")
        print(f"Status      : {skill.status}")
        print(f"Role        : {skill.role}")
        print(f"Permission  : {skill.permission_action}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Description : {skill.description}")

        if skill.capabilities:
            print("Capabilities:")
            for capability in skill.capabilities:
                print(f"- {capability}")

    def skill_check(self, name: str) -> None:
        registry = build_builtin_skill_registry()
        skill = registry.get(name=name)

        print("AURA Skill Check")
        print("================")

        if skill is None:
            print(f"Skill not found: {name}")
            return

        permission = registry.check_permission(skill)

        print(f"Skill       : {skill.name}")
        print(f"Status      : {skill.status}")
        print(f"Role        : {skill.role}")
        print(f"Permission  : {skill.permission_action}")
        print(f"Level       : {int(permission.level)} - {permission.level.label}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Reason      : {permission.reason}")

    def plugin_actions(self) -> None:
        registry = build_builtin_plugin_action_registry()

        print("AURA Plugin Actions")
        print("===================")
        print(f"Total: {registry.count()}")
        print()

        for action in registry.list_actions():
            permission = registry.check_permission(action)

            print(f"- {action.name}")
            print(f"  Plugin      : {action.plugin}")
            print(f"  Status      : {action.status}")
            print(f"  Skill       : {action.skill}")
            print(f"  Permission  : {action.permission_action}")
            print(f"  Allowed     : {permission.allowed}")
            print(f"  Confirmation: {permission.requires_confirmation}")
            print(f"  Description : {action.description}")
            print()

    def plugin_action_detail(self, name: str) -> None:
        registry = build_builtin_plugin_action_registry()
        action = registry.get(name=name)

        print("AURA Plugin Action")
        print("==================")

        if action is None:
            print(f"Plugin action not found: {name}")
            return

        permission = registry.check_permission(action)

        print(f"Name        : {action.name}")
        print(f"Plugin      : {action.plugin}")
        print(f"Status      : {action.status}")
        print(f"Skill       : {action.skill}")
        print(f"Permission  : {action.permission_action}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Description : {action.description}")

    def plugin_action_check(self, name: str) -> None:
        registry = build_builtin_plugin_action_registry()
        action = registry.get(name=name)

        print("AURA Plugin Action Check")
        print("========================")

        if action is None:
            print(f"Plugin action not found: {name}")
            return

        permission = registry.check_permission(action)

        print(f"Action      : {action.name}")
        print(f"Plugin      : {action.plugin}")
        print(f"Status      : {action.status}")
        print(f"Skill       : {action.skill}")
        print(f"Permission  : {action.permission_action}")
        print(f"Level       : {int(permission.level)} - {permission.level.label}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Reason      : {permission.reason}")

    def project_summary(self) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        summary = plugin.summary()

        print("AURA Project Summary")
        print("====================")
        print(f"Project Root  : {summary['project_root']}")
        print(f"Visible Files : {summary['visible_files']}")
        print(f"Python Files  : {summary['python_files']}")
        print(f"Markdown Files: {summary['markdown_files']}")
        print(f"YAML Files    : {summary['yaml_files']}")
        print()
        print("Top Files:")
        for file in summary["top_files"]:
            print(f"- {file}")

    def project_files(self, limit: int = 50) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        files = plugin.list_files(limit=limit)

        print("AURA Project Files")
        print("==================")
        print(f"Limit: {limit}")
        print()

        if not files:
            print("No visible project files found.")
            return

        for file in files:
            print(f"- {file}")

    def project_read(self, relative_path: str) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        print("AURA Project Read")
        print("=================")
        print(f"File: {relative_path}")
        print()

        try:
            content = plugin.read_file(relative_path=relative_path)
        except Exception as error:
            print(f"Error: {error}")
            return

        print(content)

    def voice_status(self) -> None:
        voice_manager = VoiceManager()
        status = voice_manager.status()

        print("AURA Voice Status")
        print("=================")
        print(f"Status           : {status['status']}")
        print(f"Microphone Access: {status['microphone_access']}")
        print(f"Speaker Output   : {status['speaker_output']}")
        print(f"STT Ready        : {status['stt_ready']}")
        print(f"TTS Ready        : {status['tts_ready']}")
        print(f"Providers        : {status['providers']}")
        print(f"Note             : {status['note']}")

    def voice_providers(self) -> None:
        voice_manager = VoiceManager()

        print("AURA Voice Providers")
        print("====================")

        for provider in voice_manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type            : {provider.provider_type}")
            print(f"  Status          : {provider.status}")
            print(f"  Input Supported : {provider.input_supported}")
            print(f"  Output Supported: {provider.output_supported}")
            print(f"  Description     : {provider.description}")
            print()

    def awakening_status(self) -> None:
        awakening_manager = AwakeningManager(project_root=self.project_root)
        status = awakening_manager.build_status()

        print("AURA Awakening Status")
        print("=====================")
        print(f"Milestone     : {status['milestone']}")
        print(f"Phase         : {status['phase']}")
        print(f"Status        : {status['status']}")
        print(f"Readiness     : {status['ready_count']}/{status['total_pillars']} pillars")
        print()
        print("Pillars:")
        for pillar in status["pillars"]:
            print(f"- {pillar['name']}")
            print(f"  Status     : {pillar['status']}")
            print(f"  Ready      : {pillar['ready']}")
            print(f"  Description: {pillar['description']}")
            print(f"  Note       : {pillar['note']}")
        print()
        print("Foundation Counts:")
        print(f"- Voice Providers: {status['voice_providers']}")
        print(f"- Memory Records : {status['memory_records']}")
        print(f"- Journal Entries: {status['journal_entries']}")
        print(f"- Roles          : {status['roles']}")
        print(f"- Skills         : {status['skills']}")
        print(f"- Plugin Actions : {status['plugin_actions']}")
        print()
        print(f"Summary: {status['summary']}")

    def vision_status(self) -> None:
        vision_manager = VisionManager()
        status = vision_manager.status()

        print("AURA Vision Status")
        print("==================")
        print(f"Status       : {status['status']}")
        print(f"Screen Access: {status['screen_access']}")
        print(f"Camera Access: {status['camera_access']}")
        print(f"Screen Ready : {status['screen_ready']}")
        print(f"Camera Ready : {status['camera_ready']}")
        print(f"Providers    : {status['providers']}")
        print(f"Note         : {status['note']}")

    def vision_providers(self) -> None:
        vision_manager = VisionManager()

        print("AURA Vision Providers")
        print("=====================")

        for provider in vision_manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type            : {provider.provider_type}")
            print(f"  Status          : {provider.status}")
            print(f"  Screen Supported: {provider.screen_supported}")
            print(f"  Camera Supported: {provider.camera_supported}")
            print(f"  Description     : {provider.description}")
            print()

    def shell(self) -> None:
        shell = AuraShell()
        shell.run()

    def parse(self, args: list[str] | None = None):
        parser = argparse.ArgumentParser(
            prog="aura",
            description="AURA Genesis command-line interface",
        )

        subparsers = parser.add_subparsers(dest="command")

        remember_parser = subparsers.add_parser("remember")
        remember_parser.add_argument("content", type=str)

        recall_parser = subparsers.add_parser("recall")
        recall_parser.add_argument("--limit", type=int, default=5)

        chat_parser = subparsers.add_parser("chat")
        chat_parser.add_argument("message", type=str)

        history_parser = subparsers.add_parser("history")
        history_parser.add_argument("--limit", type=int, default=5)

        journal_parser = subparsers.add_parser("journal")
        journal_parser.add_argument("--limit", type=int, default=5)

        journal_latest_parser = subparsers.add_parser("journal-latest")
        journal_latest_parser.add_argument("--limit", type=int, default=5)

        journal_add_parser = subparsers.add_parser("journal-add")
        journal_add_parser.add_argument("content", type=str)

        subparsers.add_parser("journal-count")

        context_parser = subparsers.add_parser("context")
        context_parser.add_argument("message", type=str)

        context_preview_parser = subparsers.add_parser("context-preview")
        context_preview_parser.add_argument("message", type=str)

        subparsers.add_parser("vision-status")
        subparsers.add_parser("vision-providers")

        subparsers.add_parser("awakening-status")
        subparsers.add_parser("awaken")

        subparsers.add_parser("voice-status")
        subparsers.add_parser("voice-providers")

        subparsers.add_parser("project-summary")

        project_files_parser = subparsers.add_parser("project-files")
        project_files_parser.add_argument("--limit", type=int, default=50)

        project_read_parser = subparsers.add_parser("project-read")
        project_read_parser.add_argument("relative_path", type=str)

        subparsers.add_parser("plugin-actions")

        plugin_action_parser = subparsers.add_parser("plugin-action")
        plugin_action_parser.add_argument("name", type=str)

        plugin_action_check_parser = subparsers.add_parser("plugin-action-check")
        plugin_action_check_parser.add_argument("name", type=str)

        subparsers.add_parser("skills")

        skill_parser = subparsers.add_parser("skill")
        skill_parser.add_argument("name", type=str)

        skill_check_parser = subparsers.add_parser("skill-check")
        skill_check_parser.add_argument("name", type=str)

        subparsers.add_parser("permissions")

        permission_check_parser = subparsers.add_parser("permission-check")
        permission_check_parser.add_argument("action", type=str)

        perm_check_parser = subparsers.add_parser("perm-check")
        perm_check_parser.add_argument("action", type=str)

        subparsers.add_parser("provider")
        subparsers.add_parser("roles")
        subparsers.add_parser("reason")

        memory_delete_parser = subparsers.add_parser("memory-delete")
        memory_delete_parser.add_argument("memory_id", type=str)

        mem_delete_parser = subparsers.add_parser("mem-delete")
        mem_delete_parser.add_argument("memory_id", type=str)

        memory_pin_parser = subparsers.add_parser("memory-pin")
        memory_pin_parser.add_argument("memory_id", type=str)

        mem_pin_parser = subparsers.add_parser("mem-pin")
        mem_pin_parser.add_argument("memory_id", type=str)

        memory_unpin_parser = subparsers.add_parser("memory-unpin")
        memory_unpin_parser.add_argument("memory_id", type=str)

        mem_unpin_parser = subparsers.add_parser("mem-unpin")
        mem_unpin_parser.add_argument("memory_id", type=str)

        memory_importance_parser = subparsers.add_parser("memory-importance")
        memory_importance_parser.add_argument("memory_id", type=str)
        memory_importance_parser.add_argument("importance", type=int)

        mem_importance_parser = subparsers.add_parser("mem-importance")
        mem_importance_parser.add_argument("memory_id", type=str)
        mem_importance_parser.add_argument("importance", type=int)

        subparsers.add_parser("memory-pinned")
        subparsers.add_parser("mem-pinned")

        subparsers.add_parser("memory-count")
        subparsers.add_parser("mem-count")

        memory_list_parser = subparsers.add_parser("memory-list")
        memory_list_parser.add_argument("--limit", type=int, default=5)

        mem_list_parser = subparsers.add_parser("mem-list")
        mem_list_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("provider-check")
        subparsers.add_parser("reason-check")

        memory_search_parser = subparsers.add_parser("memory-search")
        memory_search_parser.add_argument("query", type=str)
        memory_search_parser.add_argument("--limit", type=int, default=5)

        mem_search_parser = subparsers.add_parser("mem-search")
        mem_search_parser.add_argument("query", type=str)
        mem_search_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("shell")

        return parser.parse_args(args)

    def run(self, args: list[str] | None = None) -> bool:
        parsed = self.parse(args)

        if parsed.command == "remember":
            disable_logging()
            self.remember(parsed.content)
            return True

        if parsed.command == "recall":
            disable_logging()
            self.recall(limit=parsed.limit)
            return True

        if parsed.command == "chat":
            disable_logging()
            self.chat(parsed.message)
            return True

        if parsed.command == "history":
            disable_logging()
            self.history(limit=parsed.limit)
            return True

        if parsed.command in {"journal", "journal-latest"}:
            disable_logging()
            self.journal(limit=parsed.limit)
            return True

        if parsed.command == "journal-add":
            disable_logging()
            self.journal_add(content=parsed.content)
            return True

        if parsed.command == "journal-count":
            disable_logging()
            self.journal_count()
            return True

        if parsed.command == "roles":
            disable_logging()
            self.roles()
            return True

        if parsed.command in {"context", "context-preview"}:
            disable_logging()
            self.context(message=parsed.message)
            return True

        if parsed.command == "vision-status":
            disable_logging()
            self.vision_status()
            return True

        if parsed.command == "vision-providers":
            disable_logging()
            self.vision_providers()
            return True

        if parsed.command in {"awakening-status", "awaken"}:
            disable_logging()
            self.awakening_status()
            return True

        if parsed.command == "voice-status":
            disable_logging()
            self.voice_status()
            return True

        if parsed.command == "voice-providers":
            disable_logging()
            self.voice_providers()
            return True

        if parsed.command == "project-summary":
            disable_logging()
            self.project_summary()
            return True

        if parsed.command == "project-files":
            disable_logging()
            self.project_files(limit=parsed.limit)
            return True

        if parsed.command == "project-read":
            disable_logging()
            self.project_read(relative_path=parsed.relative_path)
            return True

        if parsed.command == "plugin-actions":
            disable_logging()
            self.plugin_actions()
            return True

        if parsed.command == "plugin-action":
            disable_logging()
            self.plugin_action_detail(name=parsed.name)
            return True

        if parsed.command == "plugin-action-check":
            disable_logging()
            self.plugin_action_check(name=parsed.name)
            return True

        if parsed.command == "skills":
            disable_logging()
            self.skills()
            return True

        if parsed.command == "skill":
            disable_logging()
            self.skill_detail(name=parsed.name)
            return True

        if parsed.command == "skill-check":
            disable_logging()
            self.skill_check(name=parsed.name)
            return True

        if parsed.command == "permissions":
            disable_logging()
            self.permissions()
            return True

        if parsed.command in {"permission-check", "perm-check"}:
            disable_logging()
            self.permission_check(action=parsed.action)
            return True

        if parsed.command in {"provider", "reason"}:
            disable_logging()
            self.provider()
            return True

        if parsed.command in {"provider-check", "reason-check"}:
            disable_logging()
            self.provider_check()
            return True

        if parsed.command in {"memory-delete", "mem-delete"}:
            disable_logging()
            self.memory_delete(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-pin", "mem-pin"}:
            disable_logging()
            self.memory_pin(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-unpin", "mem-unpin"}:
            disable_logging()
            self.memory_unpin(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-importance", "mem-importance"}:
            disable_logging()
            self.memory_importance(
                memory_id=parsed.memory_id,
                importance=parsed.importance,
            )
            return True

        if parsed.command in {"memory-pinned", "mem-pinned"}:
            disable_logging()
            self.memory_pinned()
            return True

        if parsed.command in {"memory-count", "mem-count"}:
            disable_logging()
            self.memory_count()
            return True

        if parsed.command in {"memory-list", "mem-list"}:
            disable_logging()
            self.memory_list(limit=parsed.limit)
            return True

        if parsed.command in {"memory-search", "mem-search"}:
            disable_logging()
            self.memory_search(query=parsed.query, limit=parsed.limit)
            return True

        if parsed.command == "shell":
            disable_logging()
            self.shell()
            return True

        return False
