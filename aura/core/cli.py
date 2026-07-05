import argparse
from pathlib import Path
from typing import Any

import yaml

from aura.core.chat import AuraChat
from aura.core_loop.core_loop_manager import CoreLoopManager
from aura.model_router.model_router import ModelRouter
from aura.partner.partner_alpha_manager import PartnerAlphaManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.actions.action_request_manager import ActionRequestManager
from aura.avatar.avatar_manager import AvatarManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
from aura.blender.blender_bridge_foundation_manager import BlenderBridgeFoundationManager
from aura.core.shell import AuraShell
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.journal.project_journal import ProjectJournal
from aura.context.context_manager import ContextManager
from aura.permissions.permission_manager import PermissionManager
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
from aura.status.system_status_manager import SystemStatusManager
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

    def action_request(self, action: str) -> None:
        manager = ActionRequestManager()
        request = manager.build(action_name=action)

        print("AURA Action Request")
        print("===================")
        print(f"Requested Action   : {request.requested_action}")
        print(f"Resolved Action    : {request.resolved_action}")
        print(f"Request State      : {request.request_state}")
        print(f"Plugin Action Found: {request.plugin_action_found}")
        print(f"Plugin             : {request.plugin or '-'}")
        print(f"Skill              : {request.skill or '-'}")
        print(f"Plugin Status      : {request.plugin_action_status}")
        print(f"Permission Action  : {request.permission_action}")
        print(f"Permission Level   : {request.permission_level} - {request.permission_level_label}")
        print(f"Allowed            : {request.allowed}")
        print(f"Confirmation       : {request.requires_confirmation}")
        print(f"Description        : {request.description}")
        print(f"Reason             : {request.reason}")
        print(f"Note               : {request.note}")

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

    def project_map(self, depth: int = 2, limit: int = 80) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        project_map = plugin.project_map(depth=depth, limit=limit)

        print("AURA Project Map")
        print("================")
        print(f"Project Root: {project_map['project_root']}")
        print(f"Depth       : {project_map['depth']}")
        print(f"Limit       : {project_map['limit']}")
        print(f"Directories : {project_map['directories']}")
        print(f"Files       : {project_map['files']}")
        print()
        print("Entries:")

        for entry in project_map["entries"]:
            marker = "[D]" if entry["type"] == "directory" else "[F]"
            print(f"- {marker} {entry['path']}")

    def project_inspect(self, relative_path: str) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        try:
            info = plugin.inspect_path(relative_path=relative_path)
        except Exception as error:
            print(f"Error: {error}")
            return

        print("AURA Project Inspect")
        print("====================")
        print(f"Path: {info['path']}")
        print(f"Type: {info['type']}")

        if info["type"] == "directory":
            print(f"Children Shown: {info['children_shown']}/{info['child_limit']}")
            print()
            print("Children:")

            for child in info["children"]:
                marker = "[D]" if child["type"] == "directory" else "[F]"
                print(f"- {marker} {child['path']}")

            return

        if info["type"] == "file":
            print(f"Suffix      : {info['suffix']}")
            print(f"Size Bytes  : {info['size_bytes']}")
            print(f"Safe To Read: {info['safe_to_read']}")
            print(f"Preview     : {info['preview_line_count']} line(s)")
            print()

            if info["preview_lines"]:
                print("Preview:")
                for index, line in enumerate(info["preview_lines"], start=1):
                    print(f"{index:03}: {line}")

            return

    def project_find(self, keyword: str, limit: int = 30) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        try:
            result = plugin.find_text(keyword=keyword, limit=limit)
        except Exception as error:
            print(f"Error: {error}")
            return

        print("AURA Project Find")
        print("=================")
        print(f"Keyword: {result['keyword']}")
        print(f"Limit  : {result['limit']}")
        print(f"Matches: {result['match_count']}")
        print()

        if not result["matches"]:
            print("No matches found.")
            return

        for match in result["matches"]:
            print(f"- {match['file']}:{match['line']}")
            print(f"  {match['text']}")

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

    def voice_runtime_status(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        status = planner.status()

        print("AURA Voice Runtime Status")
        print("=========================")
        print(f"Name              : {status['name']}")
        print(f"Version           : {status['version']}")
        print(f"Status            : {status['status']}")
        print(f"Planning Ready    : {status['planning_ready']}")
        print(f"Runtime Ready     : {status['runtime_ready']}")
        print(f"Microphone Access : {status['microphone_access']}")
        print(f"Speaker Output    : {status['speaker_output']}")
        print(f"STT Runtime Ready : {status['stt_runtime_ready']}")
        print(f"TTS Runtime Ready : {status['tts_runtime_ready']}")
        print(f"STT Candidates    : {status['stt_candidates']}")
        print(f"TTS Candidates    : {status['tts_candidates']}")
        print(f"Candidate Count   : {status['candidate_count']}")
        print(f"Note              : {status['note']}")

    def voice_runtime_plan(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        plan = planner.plan()
        recommended = plan["recommended_path"]

        print("AURA Voice Runtime Plan")
        print("=======================")
        print("Recommended Path")
        print("----------------")
        print(f"STT         : {recommended['stt']}")
        print(f"TTS         : {recommended['tts']}")
        print(f"Fallback TTS: {recommended['fallback_tts']}")
        print(f"Audio I/O   : {recommended['audio_io']}")
        print(f"Description : {recommended['description']}")
        print()
        print("Phases")
        print("------")

        for phase in plan["phases"]:
            print(f"- Phase {phase['phase']}: {phase['name']}")
            print(f"  Status     : {phase['status']}")
            print(f"  Description: {phase['description']}")

        print()
        print("STT Candidates")
        print("--------------")
        for candidate in plan["stt_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("TTS Candidates")
        print("--------------")
        for candidate in plan["tts_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Safety Rules")
        print("------------")
        for rule in plan["safety_rules"]:
            print(f"- {rule}")

    def voice_runtime_check(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        result = planner.check()
        dependencies = result["dependencies"]

        print("AURA Voice Runtime Check")
        print("========================")
        print(f"Status                 : {result['status']}")
        print(f"Planning Ready         : {result['planning_ready']}")
        print(f"Runtime Ready          : {result['runtime_ready']}")
        print(f"Python Packages        : {result['python_packages_installed']}/{result['python_packages_total']}")
        print(f"Executables            : {result['executables_found']}/{result['executables_total']}")
        print()
        print("Python Packages")
        print("---------------")
        for package in dependencies["python_packages"]:
            print(f"- {package['name']}: {package['installed']} ({package['purpose']})")

        print()
        print("Executables")
        print("-----------")
        for executable in dependencies["executables"]:
            print(f"- {executable['name']}: {executable['found']} ({executable['purpose']})")

        print()
        print("Environment")
        print("-----------")
        environment = dependencies["environment"]
        print(f"OS             : {environment['os']}")
        print(f"OS Release     : {environment['os_release']}")
        print(f"Machine        : {environment['machine']}")
        print(f"Pulse Server   : {environment['pulse_server'] or '-'}")
        print(f"PipeWire Runtime: {environment['pipewire_runtime'] or '-'}")
        print(f"XDG Runtime    : {environment['xdg_runtime'] or '-'}")
        print()
        print(f"Note: {result['note']}")

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
        print(f"- Vision Providers: {status['vision_providers']}")
        print(f"- Memory Records : {status['memory_records']}")
        print(f"- Journal Entries: {status['journal_entries']}")
        print(f"- Roles          : {status['roles']}")
        print(f"- Skills         : {status['skills']}")
        print(f"- Plugin Actions : {status['plugin_actions']}")
        print()
        print(f"Summary: {status['summary']}")

    def vision_runtime_status(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        status = planner.status()

        print("AURA Vision Runtime Status")
        print("==========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Planning Ready       : {status['planning_ready']}")
        print(f"Runtime Ready        : {status['runtime_ready']}")
        print(f"Screen Access        : {status['screen_access']}")
        print(f"Camera Access        : {status['camera_access']}")
        print(f"Screen Runtime Ready : {status['screen_runtime_ready']}")
        print(f"Camera Runtime Ready : {status['camera_runtime_ready']}")
        print(f"Vision Model Ready   : {status['vision_model_ready']}")
        print(f"Screen Candidates    : {status['screen_candidates']}")
        print(f"Camera Candidates    : {status['camera_candidates']}")
        print(f"Model Candidates     : {status['model_candidates']}")
        print(f"Candidate Count      : {status['candidate_count']}")
        print(f"Note                 : {status['note']}")

    def vision_runtime_plan(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        plan = planner.plan()
        recommended = plan["recommended_path"]

        print("AURA Vision Runtime Plan")
        print("========================")
        print("Recommended Path")
        print("----------------")
        print(f"Screen Capture  : {recommended['screen_capture']}")
        print(f"Camera Capture  : {recommended['camera_capture']}")
        print(f"Vision Model    : {recommended['vision_model']}")
        print(f"Image Processing: {recommended['image_processing']}")
        print(f"Description     : {recommended['description']}")
        print()
        print("Phases")
        print("------")

        for phase in plan["phases"]:
            print(f"- Phase {phase['phase']}: {phase['name']}")
            print(f"  Status     : {phase['status']}")
            print(f"  Description: {phase['description']}")

        print()
        print("Screen Capture Candidates")
        print("-------------------------")
        for candidate in plan["screen_capture_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Camera Capture Candidates")
        print("-------------------------")
        for candidate in plan["camera_capture_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Vision Model Candidates")
        print("-----------------------")
        for candidate in plan["vision_model_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Safety Rules")
        print("------------")
        for rule in plan["safety_rules"]:
            print(f"- {rule}")

    def vision_runtime_check(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        result = planner.check()
        dependencies = result["dependencies"]

        print("AURA Vision Runtime Check")
        print("=========================")
        print(f"Status                 : {result['status']}")
        print(f"Planning Ready         : {result['planning_ready']}")
        print(f"Runtime Ready          : {result['runtime_ready']}")
        print(f"Python Packages        : {result['python_packages_installed']}/{result['python_packages_total']}")
        print(f"Executables            : {result['executables_found']}/{result['executables_total']}")
        print()
        print("Python Packages")
        print("---------------")
        for package in dependencies["python_packages"]:
            print(f"- {package['name']}: {package['installed']} ({package['purpose']})")

        print()
        print("Executables")
        print("-----------")
        for executable in dependencies["executables"]:
            print(f"- {executable['name']}: {executable['found']} ({executable['purpose']})")

        print()
        print("Environment")
        print("-----------")
        environment = dependencies["environment"]
        print(f"OS                 : {environment['os']}")
        print(f"OS Release         : {environment['os_release']}")
        print(f"Machine            : {environment['machine']}")
        print(f"Desktop Environment: {environment['desktop_environment']}")
        print(f"Display            : {environment['display'] or '-'}")
        print(f"Wayland Display    : {environment['wayland_display'] or '-'}")
        print(f"XDG Runtime        : {environment['xdg_runtime'] or '-'}")
        print()
        print(f"Note: {result['note']}")

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

    def tool_sandbox_status(self) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        status = sandbox.status()

        print("AURA Tool Sandbox Status")
        print("========================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Sandbox Ready                : {status['sandbox_ready']}")
        print(f"Policy Ready                 : {status['policy_ready']}")
        print(f"Dry Run Ready                : {status['dry_run_ready']}")
        print(f"Real Execution Ready         : {status['real_execution_ready']}")
        print(f"Requires Confirmation        : {status['requires_confirmation_for_execution']}")
        print(f"Allowed Commands             : {status['allowed_command_count']}")
        print(f"Blocked Commands             : {status['blocked_command_count']}")
        print(f"Blocked Patterns             : {status['blocked_pattern_count']}")
        print(f"Project Root                 : {status['project_root']}")
        print()
        print(f"Note: {status['note']}")

    def tool_sandbox_policy(self) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        policy = sandbox.policy_dict()

        print("AURA Tool Sandbox Policy")
        print("========================")
        print(f"Name                         : {policy['name']}")
        print(f"Status                       : {policy['status']}")
        print(f"Dry Run Supported            : {policy['dry_run_supported']}")
        print(f"Real Execution Supported     : {policy['real_execution_supported']}")
        print(f"Requires Confirmation        : {policy['requires_confirmation_for_execution']}")
        print(f"Description                  : {policy['description']}")
        print()

        print("Allowed Commands")
        print("----------------")
        for command in policy["allowed_commands"]:
            print(f"- {command}")

        print()
        print("Blocked Commands")
        print("----------------")
        for command in policy["blocked_commands"]:
            print(f"- {command}")

        print()
        print("Blocked Patterns")
        print("----------------")
        for pattern in policy["blocked_patterns"]:
            print(f"- {pattern}")

    def tool_sandbox_check(self, command: str) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        result = sandbox.check_command(command)

        print("AURA Tool Sandbox Check")
        print("=======================")
        print(f"Command              : {result['command']}")
        print(f"Normalized Command   : {result['normalized_command']}")
        print(f"Base Command         : {result['base_command']}")
        print(f"State                : {result['state']}")
        print(f"Allowed              : {result['allowed']}")
        print(f"Dry Run Supported    : {result['dry_run_supported']}")
        print(f"Real Execution       : {result['real_execution_supported']}")
        print(f"Confirmation Required: {result['requires_confirmation_for_execution']}")
        print(f"Executed             : {result['executed']}")
        print(f"Reason               : {result['reason']}")

        if result["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in result["blocked_patterns_found"]:
                print(f"- {pattern}")

        print()
        print(f"Note: {result['note']}")

    def tool_sandbox_dry_run(self, command: str) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        result = sandbox.dry_run(command)
        check = result["check"]

        print("AURA Tool Sandbox Dry Run")
        print("=========================")
        print(f"Command       : {result['command']}")
        print(f"Dry Run Ready : {result['dry_run_ready']}")
        print(f"Would Execute : {result['would_execute']}")
        print(f"Executed      : {result['executed']}")
        print(f"Check State   : {check['state']}")
        print(f"Allowed       : {check['allowed']}")
        print(f"Reason        : {check['reason']}")

        if check["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in check["blocked_patterns_found"]:
                print(f"- {pattern}")

        if result["plan"]:
            print()
            print("Plan")
            print("----")
            for step in result["plan"]:
                print(f"- {step}")

        print()
        print(f"Note: {result['note']}")

    def model_router_status(self) -> None:
        router = ModelRouter(project_root=self.project_root)
        status = router.status()

        print("AURA Model Router Status")
        print("========================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Router Ready           : {status['router_ready']}")
        print(f"Route Selection Ready  : {status['route_selection_ready']}")
        print(f"Runtime Switching Ready: {status['runtime_switching_ready']}")
        print(f"Model Download Ready   : {status['model_download_ready']}")
        print(f"Active Provider        : {status['active_provider']}")
        print(f"Active Model           : {status['active_model']}")
        print(f"Active Host            : {status['active_host']}")
        print(f"Routes                 : {status['routes']}")
        print()
        print("Route Status Counts")
        print("-------------------")
        for name, value in status["route_status_counts"].items():
            print(f"{name:<12}: {value}")
        print()
        print(f"Note: {status['note']}")

    def model_router_routes(self) -> None:
        router = ModelRouter(project_root=self.project_root)

        print("AURA Model Router Routes")
        print("========================")

        for route in router.list_routes():
            print(f"- {route.name}")
            print(f"  Role       : {route.role}")
            print(f"  Provider   : {route.provider}")
            print(f"  Model      : {route.model}")
            print(f"  Status     : {route.status}")
            print(f"  Description: {route.description}")

            if route.use_cases:
                print(f"  Use Cases  : {', '.join(route.use_cases)}")

            if route.candidate_models:
                print(f"  Candidates : {', '.join(route.candidate_models)}")

            if route.safety_notes:
                print("  Safety:")
                for note in route.safety_notes:
                    print(f"  - {note}")

            print()

    def model_router_select(self, target: str) -> None:
        router = ModelRouter(project_root=self.project_root)
        result = router.select(target)
        route = result["route"]

        print("AURA Model Router Selection")
        print("===========================")
        print(f"Target                     : {result['target']}")
        print(f"Normalized Target          : {result['normalized_target']}")
        print(f"Found                      : {result['found']}")
        print(f"Fallback Used              : {result['fallback_used']}")
        print(f"Runtime Switching Performed: {result['runtime_switching_performed']}")
        print()

        if route:
            print("Selected Route")
            print("--------------")
            print(f"Name       : {route['name']}")
            print(f"Role       : {route['role']}")
            print(f"Provider   : {route['provider']}")
            print(f"Model      : {route['model']}")
            print(f"Status     : {route['status']}")
            print(f"Description: {route['description']}")

            if route["use_cases"]:
                print(f"Use Cases  : {', '.join(route['use_cases'])}")

            if route["candidate_models"]:
                print(f"Candidates : {', '.join(route['candidate_models'])}")

            if route["safety_notes"]:
                print("Safety:")
                for note in route["safety_notes"]:
                    print(f"- {note}")

        print()
        print(f"Note: {result['note']}")

    def core_loop_status(self) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Alpha Core Loop Status")
        print("===========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Loop Ready           : {status['loop_ready']}")
        print(f"Execution Ready      : {status['execution_ready']}")
        print(f"Safe Action Execution: {status['safe_action_execution']}")
        print(f"Steps                : {status['steps']}")
        print(f"Flow                 : {status['flow']}")
        print()
        print("Systems")
        print("-------")
        for name, value in status["systems"].items():
            print(f"{name:<16}: {value}")
        print()
        print("Runtime")
        print("-------")
        for name, value in status["runtime"].items():
            print(f"{name:<22}: {value}")
        print()
        print(f"Note: {status['note']}")

    def core_loop_run(self, message: str) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        result = manager.run(message=message)

        print("AURA Alpha Core Loop Run")
        print("========================")
        print(f"Input     : {result['input']['message']}")
        print(f"Action    : {result['plan']['inferred_action']}")
        print(f"Mode      : {result['plan']['mode']}")
        print(f"Executed  : {result['execution']['executed']}")
        print()
        print("Context")
        print("-------")
        context = result["context"]
        print(f"Pinned Memories       : {context['pinned_memories']}")
        print(f"Important Memories    : {context['important_memories']}")
        print(f"Relevant Memories     : {context['relevant_memories']}")
        print(f"Recent Journal Entries: {context['recent_journal_entries']}")
        if context["latest_journal"]:
            print(f"Latest Journal        : {context['latest_journal']}")
        print()
        print("Safety")
        print("------")
        safety = result["safety"]
        print(f"Resolved Action : {safety['resolved_action']}")
        print(f"Request State   : {safety['request_state']}")
        print(f"Allowed         : {safety['allowed']}")
        print(f"Confirmation    : {safety['requires_confirmation']}")
        print(f"Permission      : {safety['permission_action']}")
        print(f"Reason          : {safety['reason']}")
        print()
        print("AURA Response")
        print("-------------")
        print(result["response"]["text"])
        print()
        print("Journal")
        print("-------")
        print(f"Mode           : {result['journal']['mode']}")
        print(f"Write Performed: {result['journal']['write_performed']}")
        print(f"Note           : {result['journal']['note']}")

    def core_loop_trace(self, message: str) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        result = manager.trace(message=message)

        print("AURA Alpha Core Loop Trace")
        print("==========================")
        print(f"Loop      : {result['loop']['name']} v{result['loop']['version']}")
        print(f"Status    : {result['loop']['status']}")
        print(f"Input     : {result['input']['message']}")
        print()
        print("Steps")
        print("-----")
        for step in result["loop"]["steps"]:
            print(f"{step['index']}. {step['name']}")
            print(f"   Status     : {step['status']}")
            print(f"   Component  : {step['component']}")
            print(f"   Description: {step['description']}")
        print()
        print("Trace Summary")
        print("-------------")
        print(f"Inferred Action: {result['plan']['inferred_action']}")
        print(f"Safety State   : {result['safety']['request_state']}")
        print(f"Allowed        : {result['safety']['allowed']}")
        print(f"Executed       : {result['execution']['executed']}")
        print()
        print("Response Preview")
        print("----------------")
        print(result["response"]["text"])

    def avatar_status(self) -> None:
        manager = AvatarManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Avatar Status")
        print("==================")
        print(f"Name                    : {status['name']}")
        print(f"Version                 : {status['version']}")
        print(f"Status                  : {status['status']}")
        print(f"Foundation Ready        : {status['foundation_ready']}")
        print(f"Runtime Ready           : {status['runtime_ready']}")
        print(f"Avatar Loaded           : {status['avatar_loaded']}")
        print(f"Expression Runtime Ready: {status['expression_runtime_ready']}")
        print(f"Gesture Runtime Ready   : {status['gesture_runtime_ready']}")
        print(f"Motion Runtime Ready    : {status['motion_runtime_ready']}")
        print(f"Providers               : {status['providers']}")
        print(f"Expressions             : {status['expressions']}")
        print(f"Gestures                : {status['gestures']}")
        print(f"Note                    : {status['note']}")

    def avatar_providers(self) -> None:
        manager = AvatarManager(project_root=self.project_root)

        print("AURA Avatar Providers")
        print("=====================")

        for provider in manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type                : {provider.provider_type}")
            print(f"  Status              : {provider.status}")
            print(f"  State Supported     : {provider.state_supported}")
            print(f"  Expression Supported: {provider.expression_supported}")
            print(f"  Gesture Supported   : {provider.gesture_supported}")
            print(f"  Runtime Supported   : {provider.runtime_supported}")
            print(f"  Description         : {provider.description}")
            print()

    def avatar_state(self) -> None:
        manager = AvatarManager(project_root=self.project_root)
        state = manager.state()

        print("AURA Avatar State")
        print("=================")
        print(f"Avatar Name       : {state['avatar_name']}")
        print(f"Avatar Format     : {state['avatar_format']}")
        print(f"Runtime           : {state['runtime']}")
        print(f"Body State        : {state['body_state']}")
        print(f"Pose              : {state['pose']}")
        print(f"Expression        : {state['expression']}")
        print(f"Gesture           : {state['gesture']}")
        print(f"Model Loaded      : {state['model_loaded']}")
        print(f"Tracking Connected: {state['tracking_connected']}")
        print(f"Voice Link Ready  : {state['voice_link_ready']}")
        print(f"Vision Link Ready : {state['vision_link_ready']}")
        print(f"Motion Link Ready : {state['motion_link_ready']}")
        print()
        print("Supported Expressions:")
        for expression in state["supported_expressions"]:
            print(f"- {expression}")
        print()
        print("Supported Gestures:")
        for gesture in state["supported_gestures"]:
            print(f"- {gesture}")
        print()
        print("Planning:")
        planning = state["planning"]
        print(f"Preferred Format   : {planning['preferred_format']}")
        print(f"Authoring Tools    : {', '.join(planning['authoring_tools'])}")
        print(f"Runtime Candidates : {', '.join(planning['runtime_candidates'])}")
        print(f"Future Links       : {', '.join(planning['future_links'])}")
        print()
        print(f"Note: {state['note']}")

    def avatar_expression(self, expression: str) -> None:
        manager = AvatarManager(project_root=self.project_root)
        result = manager.expression_request(expression=expression)
        permission = result["permission"]

        print("AURA Avatar Expression Proposal")
        print("===============================")
        print(f"Requested Expression: {result['requested_expression']}")
        print(f"Supported           : {result['supported']}")
        print(f"Request State       : {result['request_state']}")
        print(f"Runtime Ready       : {result['runtime_ready']}")
        print(f"Executed            : {result['executed']}")
        print()
        print("Permission")
        print("----------")
        print(f"Action      : {permission['action']}")
        print(f"Level       : {permission['level']} - {permission['level_label']}")
        print(f"Allowed     : {permission['allowed']}")
        print(f"Confirmation: {permission['requires_confirmation']}")
        print(f"Reason      : {permission['reason']}")
        print()
        print(f"Note: {result['note']}")

    def avatar_gesture(self, gesture: str) -> None:
        manager = AvatarManager(project_root=self.project_root)
        result = manager.gesture_request(gesture=gesture)
        permission = result["permission"]

        print("AURA Avatar Gesture Proposal")
        print("============================")
        print(f"Requested Gesture: {result['requested_gesture']}")
        print(f"Supported        : {result['supported']}")
        print(f"Request State    : {result['request_state']}")
        print(f"Runtime Ready    : {result['runtime_ready']}")
        print(f"Executed         : {result['executed']}")
        print()
        print("Permission")
        print("----------")
        print(f"Action      : {permission['action']}")
        print(f"Level       : {permission['level']} - {permission['level_label']}")
        print(f"Allowed     : {permission['allowed']}")
        print(f"Confirmation: {permission['requires_confirmation']}")
        print(f"Reason      : {permission['reason']}")
        print()
        print(f"Note: {result['note']}")

    def desktop_status(self) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        status = manager.status()
        environment = status["environment"]

        print("AURA Desktop Bridge Status")
        print("==========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Bridge Ready         : {status['bridge_ready']}")
        print(f"Execution Ready      : {status['execution_ready']}")
        print(f"Safe Action Execution: {status['safe_action_execution']}")
        print(f"Capability Count     : {status['capability_count']}")
        print()
        print("Environment")
        print("-----------")
        print(f"OS                  : {environment['os']}")
        print(f"OS Release          : {environment['os_release']}")
        print(f"Machine             : {environment['machine']}")
        print(f"Desktop Environment: {environment['desktop_environment']}")
        print(f"Display             : {environment['display'] or '-'}")
        print(f"Wayland Display     : {environment['wayland_display'] or '-'}")
        print()
        print(f"Note: {status['note']}")

    def desktop_capabilities(self) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        capabilities = manager.capabilities()

        print("AURA Desktop Capabilities")
        print("=========================")
        print(f"Total: {len(capabilities)}")
        print()

        for capability in capabilities:
            print(f"- {capability['name']}")
            print(f"  Status       : {capability['status']}")
            print(f"  Permission   : {capability['permission_action']}")
            print(f"  Confirmation : {capability['requires_confirmation']}")
            print(f"  Execution    : {capability['execution_ready']}")
            print(f"  Description  : {capability['description']}")
            print()

    def desktop_action(self, action: str) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        proposal = manager.action_request(action_name=action)
        request = proposal["action_request"]

        print("AURA Desktop Action Proposal")
        print("============================")
        print(f"Requested Action        : {proposal['requested_action']}")
        print(f"Desktop Capability Found: {proposal['desktop_capability_found']}")
        print(f"Desktop State           : {proposal['desktop_state']}")
        print(f"Execution Ready         : {proposal['execution_ready']}")
        print(f"Executed                : {proposal['executed']}")
        print()
        print("Action Request")
        print("--------------")
        print(f"Resolved Action   : {request.resolved_action}")
        print(f"Request State     : {request.request_state}")
        print(f"Plugin Found      : {request.plugin_action_found}")
        print(f"Plugin            : {request.plugin or '-'}")
        print(f"Skill             : {request.skill or '-'}")
        print(f"Plugin Status     : {request.plugin_action_status}")
        print(f"Permission Action : {request.permission_action}")
        print(f"Permission Level  : {request.permission_level} - {request.permission_level_label}")
        print(f"Allowed           : {request.allowed}")
        print(f"Confirmation      : {request.requires_confirmation}")
        print(f"Reason            : {request.reason}")
        print(f"Note              : {proposal['note']}")

    def system_status(self) -> None:
        status_manager = SystemStatusManager(project_root=self.project_root)
        status = status_manager.build_status()

        print("AURA Unified System Status")
        print("==========================")
        print(f"Name       : {status['identity']['name']}")
        print(f"Version    : {status['identity']['version']}")
        print(f"Codename   : {status['identity']['codename']}")
        print(f"Creator    : {status['identity']['creator']}")
        print(f"Motto      : {status['identity']['motto']}")
        print(f"Project    : {status['project_root']}")
        print()
        print("Reasoning")
        print("---------")
        print(f"Provider   : {status['reasoning']['provider']}")
        print(f"Model      : {status['reasoning']['model']}")
        print(f"Host       : {status['reasoning']['host']}")
        print()
        print("Foundation Counts")
        print("-----------------")
        print(f"Memory Records      : {status['foundation']['memory_records']}")
        print(f"Journal Entries     : {status['foundation']['journal_entries']}")
        print(f"Roles               : {status['foundation']['roles']}")
        print(f"Skills              : {status['foundation']['skills']}")
        print(f"Plugin Actions      : {status['foundation']['plugin_actions']}")
        print(f"Core Loop Steps     : {status['foundation']['core_loop_steps']}")
        print(f"Model Routes        : {status['foundation']['model_routes']}")
        print(f"Sandbox Allowed     : {status['foundation']['sandbox_allowed_commands']}")
        print(f"Sandbox Blocked     : {status['foundation']['sandbox_blocked_commands']}")
        print(f"Sandbox Patterns    : {status['foundation']['sandbox_blocked_patterns']}")
        print(f"Project Python Files: {status['foundation']['project_python_files']}")
        print(f"Reflection Milestones: {status['foundation']['reflection_milestones']}")
        print(f"Voice Providers     : {status['foundation']['voice_providers']}")
        print(f"Voice Runtime Alpha : {status['foundation']['voice_runtime_alpha_sections']}")
        print(f"Vision Providers    : {status['foundation']['vision_providers']}")
        print(f"Vision Runtime Alpha: {status['foundation']['vision_runtime_alpha_sections']}")
        print(f"Avatar Providers    : {status['foundation']['avatar_providers']}")
        print(f"Avatar Runtime Alpha: {status['foundation']['avatar_runtime_alpha_sections']}")
        print(f"Awakening Readiness : {status['foundation']['awakening_readiness']}")
        print()
        print("Systems")
        print("-------")
        for name, value in status["systems"].items():
            print(f"{name:16}: {value}")
        print()
        print("Runtime")
        print("-------")
        for name, value in status["runtime"].items():
            print(f"{name:22}: {value}")
        print()
        print(f"Summary: {status['summary']}")

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

        history_parser.add_argument("limit", type=int, nargs="?", default=5)
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

        subparsers.add_parser("tool-sandbox-status")
        subparsers.add_parser("tool-sandbox-policy")

        tool_sandbox_check_parser = subparsers.add_parser("tool-sandbox-check")
        tool_sandbox_check_parser.add_argument("command_text", type=str)

        tool_sandbox_dry_run_parser = subparsers.add_parser("tool-sandbox-dry-run")
        tool_sandbox_dry_run_parser.add_argument("command_text", type=str)

        subparsers.add_parser("model-router-status")
        subparsers.add_parser("model-router-routes")

        model_router_select_parser = subparsers.add_parser("model-router-select")
        model_router_select_parser.add_argument("target", type=str)

        subparsers.add_parser("core-loop-status")

        core_loop_run_parser = subparsers.add_parser("core-loop-run")
        core_loop_run_parser.add_argument("message", type=str)

        core_loop_trace_parser = subparsers.add_parser("core-loop-trace")
        core_loop_trace_parser.add_argument("message", type=str)

        subparsers.add_parser("avatar-runtime-alpha-status")

        avatar_expression_plan_parser = subparsers.add_parser("avatar-expression-plan")
        avatar_expression_plan_parser.add_argument("expression")

        avatar_gesture_plan_parser = subparsers.add_parser("avatar-gesture-plan")
        avatar_gesture_plan_parser.add_argument("gesture")

        subparsers.add_parser("avatar-runtime-context")

        subparsers.add_parser("avatar-status")
        subparsers.add_parser("avatar-providers")
        subparsers.add_parser("avatar-state")

        avatar_expression_parser = subparsers.add_parser("avatar-expression")
        avatar_expression_parser.add_argument("expression", type=str)

        avatar_gesture_parser = subparsers.add_parser("avatar-gesture")
        avatar_gesture_parser.add_argument("gesture", type=str)

        subparsers.add_parser("desktop-alpha-status")

        desktop_action_plan_parser = subparsers.add_parser("desktop-action-plan")
        desktop_action_plan_parser.add_argument("action_type")
        desktop_action_plan_parser.add_argument("target", nargs="+")

        desktop_open_app_plan_parser = subparsers.add_parser("desktop-open-app-plan")
        desktop_open_app_plan_parser.add_argument("app_name", nargs="+")

        desktop_open_browser_plan_parser = subparsers.add_parser("desktop-open-browser-plan")
        desktop_open_browser_plan_parser.add_argument("url", nargs="+")

        desktop_open_file_plan_parser = subparsers.add_parser("desktop-open-file-plan")
        desktop_open_file_plan_parser.add_argument("file_path", nargs="+")

        subparsers.add_parser("desktop-workspace-context")

        subparsers.add_parser("desktop-status")
        subparsers.add_parser("desktop-capabilities")

        desktop_action_parser = subparsers.add_parser("desktop-action")
        desktop_action_parser.add_argument("action", type=str)

        subparsers.add_parser("system-status")
        subparsers.add_parser("status-full")

        subparsers.add_parser("vision-runtime-alpha-status")
        subparsers.add_parser("vision-screen-plan")
        subparsers.add_parser("vision-camera-plan")
        subparsers.add_parser("vision-runtime-context")

        subparsers.add_parser("vision-runtime-status")
        subparsers.add_parser("vision-runtime-plan")
        subparsers.add_parser("vision-runtime-check")

        subparsers.add_parser("vision-status")
        subparsers.add_parser("vision-providers")

        subparsers.add_parser("blender-bridge-status")

        blender_scene_plan_parser = subparsers.add_parser("blender-scene-plan")
        blender_scene_plan_parser.add_argument("goal", nargs="+")

        blender_asset_plan_parser = subparsers.add_parser("blender-asset-plan")
        blender_asset_plan_parser.add_argument("goal", nargs="+")

        blender_texture_plan_parser = subparsers.add_parser("blender-texture-plan")
        blender_texture_plan_parser.add_argument("goal", nargs="+")

        blender_rigging_plan_parser = subparsers.add_parser("blender-rigging-plan")
        blender_rigging_plan_parser.add_argument("goal", nargs="+")

        blender_animation_plan_parser = subparsers.add_parser("blender-animation-plan")
        blender_animation_plan_parser.add_argument("goal", nargs="+")

        subparsers.add_parser("blender-context")

        subparsers.add_parser("workspace-awareness-status")
        subparsers.add_parser("workspace-map")
        subparsers.add_parser("workspace-context")
        subparsers.add_parser("workspace-current-state")
        subparsers.add_parser("workspace-important-files")

        subparsers.add_parser("partner-alpha-status")
        subparsers.add_parser("partner-context")
        subparsers.add_parser("partner-readiness")
        subparsers.add_parser("partner-next-step")

        subparsers.add_parser("awakening-status")
        subparsers.add_parser("awaken")

        subparsers.add_parser("voice-runtime-alpha-status")

        voice_speak_plan_parser = subparsers.add_parser("voice-speak-plan")
        voice_speak_plan_parser.add_argument("text", nargs="+")

        voice_speak_test_parser = subparsers.add_parser("voice-speak-test")
        voice_speak_test_parser.add_argument("text", nargs="+")

        subparsers.add_parser("voice-runtime-context")

        subparsers.add_parser("voice-runtime-status")
        subparsers.add_parser("voice-runtime-plan")
        subparsers.add_parser("voice-runtime-check")

        subparsers.add_parser("voice-status")
        subparsers.add_parser("voice-providers")

        subparsers.add_parser("project-code-status")

        project_code_map_parser = subparsers.add_parser("project-code-map")
        project_code_map_parser.add_argument("--limit", type=int, default=30)

        project_code_inspect_parser = subparsers.add_parser("project-code-inspect")
        project_code_inspect_parser.add_argument("path", type=str)

        project_code_plan_parser = subparsers.add_parser("project-code-plan")
        project_code_plan_parser.add_argument("request", type=str)

        project_code_safety_parser = subparsers.add_parser("project-code-safety")
        project_code_safety_parser.add_argument("command_text", type=str)

        project_map_parser = subparsers.add_parser("project-map")
        project_map_parser.add_argument("--depth", type=int, default=2)
        project_map_parser.add_argument("--limit", type=int, default=80)

        project_inspect_parser = subparsers.add_parser("project-inspect")
        project_inspect_parser.add_argument("relative_path", type=str)

        project_find_parser = subparsers.add_parser("project-find")
        project_find_parser.add_argument("keyword", type=str)
        project_find_parser.add_argument("--limit", type=int, default=30)

        subparsers.add_parser("project-summary")

        project_files_parser = subparsers.add_parser("project-files")
        project_files_parser.add_argument("--limit", type=int, default=50)

        project_read_parser = subparsers.add_parser("project-read")
        project_read_parser.add_argument("relative_path", type=str)

        action_request_parser = subparsers.add_parser("action-request")
        action_request_parser.add_argument("action", type=str)

        action_request_check_parser = subparsers.add_parser("action-request-check")
        action_request_check_parser.add_argument("action", type=str)

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

        subparsers.add_parser("daily-briefing-status")

        daily_briefing_parser = subparsers.add_parser("daily-briefing")
        daily_briefing_parser.add_argument("--limit", type=int, default=6)

        daily_briefing_compact_parser = subparsers.add_parser("daily-briefing-compact")
        daily_briefing_compact_parser.add_argument("--limit", type=int, default=4)

        daily_briefing_context_parser = subparsers.add_parser("daily-briefing-context")
        daily_briefing_context_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("memory-reflection-status")

        memory_reflect_parser = subparsers.add_parser("memory-reflect")
        memory_reflect_parser.add_argument("--limit", type=int, default=8)

        memory_insights_parser = subparsers.add_parser("memory-insights")
        memory_insights_parser.add_argument("--limit", type=int, default=8)

        memory_reflection_context_parser = subparsers.add_parser("memory-reflection-context")
        memory_reflection_context_parser.add_argument("--limit", type=int, default=5)

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

        if parsed.command == "tool-sandbox-status":
            disable_logging()
            self.tool_sandbox_status()
            return True

        if parsed.command == "tool-sandbox-policy":
            disable_logging()
            self.tool_sandbox_policy()
            return True

        if parsed.command == "tool-sandbox-check":
            disable_logging()
            self.tool_sandbox_check(command=parsed.command_text)
            return True

        if parsed.command == "tool-sandbox-dry-run":
            disable_logging()
            self.tool_sandbox_dry_run(command=parsed.command_text)
            return True

        if parsed.command == "model-router-status":
            disable_logging()
            self.model_router_status()
            return True

        if parsed.command == "model-router-routes":
            disable_logging()
            self.model_router_routes()
            return True

        if parsed.command == "model-router-select":
            disable_logging()
            self.model_router_select(target=parsed.target)
            return True

        if parsed.command == "core-loop-status":
            disable_logging()
            self.core_loop_status()
            return True

        if parsed.command == "core-loop-run":
            disable_logging()
            self.core_loop_run(message=parsed.message)
            return True

        if parsed.command == "core-loop-trace":
            disable_logging()
            self.core_loop_trace(message=parsed.message)
            return True

        if parsed.command == "avatar-runtime-alpha-status":
            disable_logging()
            self.avatar_runtime_alpha_status()
            return True

        if parsed.command == "avatar-expression-plan":
            disable_logging()
            self.avatar_expression_plan(expression=parsed.expression)
            return True

        if parsed.command == "avatar-gesture-plan":
            disable_logging()
            self.avatar_gesture_plan(gesture=parsed.gesture)
            return True

        if parsed.command == "avatar-runtime-context":
            disable_logging()
            self.avatar_runtime_context()
            return True

        if parsed.command == "avatar-status":
            disable_logging()
            self.avatar_status()
            return True

        if parsed.command == "avatar-providers":
            disable_logging()
            self.avatar_providers()
            return True

        if parsed.command == "avatar-state":
            disable_logging()
            self.avatar_state()
            return True

        if parsed.command == "avatar-expression":
            disable_logging()
            self.avatar_expression(expression=parsed.expression)
            return True

        if parsed.command == "avatar-gesture":
            disable_logging()
            self.avatar_gesture(gesture=parsed.gesture)
            return True

        if parsed.command == "desktop-alpha-status":
            disable_logging()
            self.desktop_alpha_status()
            return True

        if parsed.command == "desktop-action-plan":
            disable_logging()
            self.desktop_action_plan(
                action_type=parsed.action_type,
                target=" ".join(parsed.target),
            )
            return True

        if parsed.command == "desktop-open-app-plan":
            disable_logging()
            self.desktop_open_app_plan(app_name=" ".join(parsed.app_name))
            return True

        if parsed.command == "desktop-open-browser-plan":
            disable_logging()
            self.desktop_open_browser_plan(url=" ".join(parsed.url))
            return True

        if parsed.command == "desktop-open-file-plan":
            disable_logging()
            self.desktop_open_file_plan(file_path=" ".join(parsed.file_path))
            return True

        if parsed.command == "desktop-workspace-context":
            disable_logging()
            self.desktop_workspace_context()
            return True

        if parsed.command == "desktop-status":
            disable_logging()
            self.desktop_status()
            return True

        if parsed.command == "desktop-capabilities":
            disable_logging()
            self.desktop_capabilities()
            return True

        if parsed.command == "desktop-action":
            disable_logging()
            self.desktop_action(action=parsed.action)
            return True

        if parsed.command in {"system-status", "status-full"}:
            disable_logging()
            self.system_status()
            return True

        if parsed.command == "vision-runtime-alpha-status":
            disable_logging()
            self.vision_runtime_alpha_status()
            return True

        if parsed.command == "vision-screen-plan":
            disable_logging()
            self.vision_screen_plan()
            return True

        if parsed.command == "vision-camera-plan":
            disable_logging()
            self.vision_camera_plan()
            return True

        if parsed.command == "vision-runtime-context":
            disable_logging()
            self.vision_runtime_context()
            return True

        if parsed.command == "vision-runtime-status":
            disable_logging()
            self.vision_runtime_status()
            return True

        if parsed.command == "vision-runtime-plan":
            disable_logging()
            self.vision_runtime_plan()
            return True

        if parsed.command == "vision-runtime-check":
            disable_logging()
            self.vision_runtime_check()
            return True

        if parsed.command == "vision-status":
            disable_logging()
            self.vision_status()
            return True

        if parsed.command == "vision-providers":
            disable_logging()
            self.vision_providers()
            return True

        if parsed.command == "blender-bridge-status":
            disable_logging()
            self.blender_bridge_status()
            return True

        if parsed.command == "blender-scene-plan":
            disable_logging()
            self.blender_scene_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-asset-plan":
            disable_logging()
            self.blender_asset_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-texture-plan":
            disable_logging()
            self.blender_texture_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-rigging-plan":
            disable_logging()
            self.blender_rigging_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-animation-plan":
            disable_logging()
            self.blender_animation_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-context":
            disable_logging()
            self.blender_context()
            return True

        if parsed.command == "workspace-awareness-status":
            disable_logging()
            self.workspace_awareness_status()
            return True

        if parsed.command == "workspace-map":
            disable_logging()
            self.workspace_map()
            return True

        if parsed.command == "workspace-context":
            disable_logging()
            self.workspace_context()
            return True

        if parsed.command == "workspace-current-state":
            disable_logging()
            self.workspace_current_state()
            return True

        if parsed.command == "workspace-important-files":
            disable_logging()
            self.workspace_important_files()
            return True

        if parsed.command == "partner-alpha-status":
            disable_logging()
            self.partner_alpha_status()
            return True

        if parsed.command == "partner-context":
            disable_logging()
            self.partner_context()
            return True

        if parsed.command == "partner-readiness":
            disable_logging()
            self.partner_readiness()
            return True

        if parsed.command == "partner-next-step":
            disable_logging()
            self.partner_next_step()
            return True

        if parsed.command in {"awakening-status", "awaken"}:
            disable_logging()
            self.awakening_status()
            return True

        if parsed.command == "voice-runtime-alpha-status":
            disable_logging()
            self.voice_runtime_alpha_status()
            return True

        if parsed.command == "voice-speak-plan":
            disable_logging()
            self.voice_speak_plan(text=" ".join(parsed.text))
            return True

        if parsed.command == "voice-speak-test":
            disable_logging()
            self.voice_speak_test(text=" ".join(parsed.text))
            return True

        if parsed.command == "voice-runtime-context":
            disable_logging()
            self.voice_runtime_context()
            return True

        if parsed.command == "voice-runtime-status":
            disable_logging()
            self.voice_runtime_status()
            return True

        if parsed.command == "voice-runtime-plan":
            disable_logging()
            self.voice_runtime_plan()
            return True

        if parsed.command == "voice-runtime-check":
            disable_logging()
            self.voice_runtime_check()
            return True

        if parsed.command == "voice-status":
            disable_logging()
            self.voice_status()
            return True

        if parsed.command == "voice-providers":
            disable_logging()
            self.voice_providers()
            return True

        if parsed.command == "project-code-status":
            disable_logging()
            self.project_code_status()
            return True

        if parsed.command == "project-code-map":
            disable_logging()
            self.project_code_map(limit=parsed.limit)
            return True

        if parsed.command == "project-code-inspect":
            disable_logging()
            self.project_code_inspect(relative_path=parsed.path)
            return True

        if parsed.command == "project-code-plan":
            disable_logging()
            self.project_code_plan(request=parsed.request)
            return True

        if parsed.command == "project-code-safety":
            disable_logging()
            self.project_code_safety(command=parsed.command_text)
            return True

        if parsed.command == "project-map":
            disable_logging()
            self.project_map(depth=parsed.depth, limit=parsed.limit)
            return True

        if parsed.command == "project-inspect":
            disable_logging()
            self.project_inspect(relative_path=parsed.relative_path)
            return True

        if parsed.command == "project-find":
            disable_logging()
            self.project_find(keyword=parsed.keyword, limit=parsed.limit)
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

        if parsed.command in {"action-request", "action-request-check"}:
            disable_logging()
            self.action_request(action=parsed.action)
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

        if parsed.command == "daily-briefing-status":
            disable_logging()
            self.daily_briefing_status()
            return True

        if parsed.command == "daily-briefing":
            disable_logging()
            self.daily_briefing(limit=parsed.limit)
            return True

        if parsed.command == "daily-briefing-compact":
            disable_logging()
            self.daily_briefing_compact(limit=parsed.limit)
            return True

        if parsed.command == "daily-briefing-context":
            disable_logging()
            self.daily_briefing_context(limit=parsed.limit)
            return True

        if parsed.command == "memory-reflection-status":
            disable_logging()
            self.memory_reflection_status()
            return True

        if parsed.command == "memory-reflect":
            disable_logging()
            self.memory_reflect(limit=parsed.limit)
            return True

        if parsed.command == "memory-insights":
            disable_logging()
            self.memory_insights(limit=parsed.limit)
            return True

        if parsed.command == "memory-reflection-context":
            disable_logging()
            self.memory_reflection_context(limit=parsed.limit)
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


    def project_code_status(self) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        status = manager.status()
        route = status["coding_route"]

        print("AURA Project Coding Assistant v2")
        print("================================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Analysis Ready         : {status['analysis_ready']}")
        print(f"AST Inspection Ready   : {status['ast_inspection_ready']}")
        print(f"Patch Planning Ready   : {status['patch_planning_ready']}")
        print(f"File Write Ready       : {status['file_write_ready']}")
        print(f"Command Execution Ready: {status['command_execution_ready']}")
        print(f"Sandbox Check Ready    : {status['sandbox_check_ready']}")
        print(f"Real Tool Execution    : {status['real_tool_execution']}")
        print(f"Python Files           : {status['python_files']}")
        print()
        print("Coding Route")
        print("------------")
        print(f"Route   : {route['name']}")
        print(f"Provider: {route['provider']}")
        print(f"Model   : {route['model']}")
        print(f"Status  : {route['status']}")
        print()
        print(f"Note: {status['note']}")

    def project_code_map(self, limit: int = 30) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        result = manager.code_map(limit=limit)
        totals = result["totals"]

        print("AURA Project Code Map")
        print("=====================")
        print(f"Files    : {totals['files']}")
        print(f"Classes  : {totals['classes']}")
        print(f"Functions: {totals['functions']}")
        print(f"Methods  : {totals['methods']}")
        print()

        for item in result["files"]:
            print(f"- {item['path']}")
            print(f"  Parse OK : {item.get('parse_ok', False)}")
            print(f"  Lines    : {item.get('line_count', 0)}")
            print(f"  Classes  : {item.get('class_count', 0)}")
            print(f"  Functions: {item.get('function_count', 0)}")
            print(f"  Methods  : {item.get('method_count', 0)}")

            classes = item.get("classes", [])
            functions = item.get("functions", [])
            methods = item.get("methods", [])

            if classes:
                print(f"  Class List   : {', '.join(classes[:8])}")
            if functions:
                print(f"  Function List: {', '.join(functions[:8])}")
            if methods:
                print(f"  Method List  : {', '.join(methods[:8])}")

            if item.get("parse_error"):
                print(f"  Error: {item['parse_error']}")

            print()

        print(f"Note: {result['note']}")

    def project_code_inspect(self, relative_path: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        summary = manager.summarize_file(relative_path)

        print("AURA Project Code Inspect")
        print("=========================")
        print(f"Path     : {summary['path']}")
        print(f"Language : {summary['language']}")
        print(f"Size     : {summary['size_bytes']} bytes")
        print(f"Lines    : {summary['line_count']}")
        print(f"Parse OK : {summary['parse_ok']}")
        print(f"Imports  : {summary['import_count']}")
        print(f"Classes  : {summary['class_count']}")
        print(f"Functions: {summary['function_count']}")
        print(f"Methods  : {summary['method_count']}")

        if summary["parse_error"]:
            print(f"Parse Error: {summary['parse_error']}")

        if summary["imports"]:
            print()
            print("Imports")
            print("-------")
            for item in summary["imports"][:40]:
                print(f"- {item}")

        if summary["classes"]:
            print()
            print("Classes")
            print("-------")
            for item in summary["classes"]:
                print(f"- {item}")

        if summary["functions"]:
            print()
            print("Functions")
            print("---------")
            for item in summary["functions"][:60]:
                print(f"- {item}")

        if summary["methods"]:
            print()
            print("Methods")
            print("-------")
            for item in summary["methods"][:80]:
                print(f"- {item}")

        if summary["safety_notes"]:
            print()
            print("Safety Notes")
            print("------------")
            for note in summary["safety_notes"]:
                print(f"- {note}")

    def project_code_plan(self, request: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        plan = manager.patch_plan(request)
        route = plan["coding_route"]

        print("AURA Project Code Patch Plan")
        print("============================")
        print(f"Request                    : {plan['request']}")
        print(f"Mode                       : {plan['mode']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print(f"Command Execution Performed: {plan['command_execution_performed']}")
        print()

        print("Coding Route")
        print("------------")
        print(f"Route   : {route['name']}")
        print(f"Provider: {route['provider']}")
        print(f"Model   : {route['model']}")
        print(f"Status  : {route['status']}")
        print()

        print("Related Files")
        print("-------------")
        for file in plan["related_files"]:
            print(f"- {file}")

        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")

        print()
        print("Sandbox Checks")
        print("--------------")
        for check in plan["sandbox_checks"]:
            print(f"- {check['command']} -> state={check['state']} allowed={check['allowed']} executed={check['executed']}")

        print()
        print("Safety")
        print("------")
        safety = plan["safety"]
        print(f"Writes Without Confirmation: {safety['writes_allowed_without_confirmation']}")
        print(f"Real Tool Execution        : {safety['real_tool_execution']}")
        print(f"Dangerous Commands Blocked : {safety['dangerous_commands_blocked']}")
        print(f"Note                       : {safety['note']}")

    def project_code_safety(self, command: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        result = manager.command_safety(command)
        check = result["check"]
        dry_run = result["dry_run"]

        print("AURA Project Code Command Safety")
        print("================================")
        print(f"Command      : {result['command']}")
        print(f"State        : {check['state']}")
        print(f"Allowed      : {check['allowed']}")
        print(f"Dry Run Ready: {dry_run['dry_run_ready']}")
        print(f"Would Execute: {dry_run['would_execute']}")
        print(f"Executed     : {dry_run['executed']}")
        print(f"Reason       : {check['reason']}")

        if check["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in check["blocked_patterns_found"]:
                print(f"- {pattern}")

        print()
        print(f"Note: {result['project_coding_note']}")


    def memory_reflection_status(self) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Memory Reflection System")
        print("=============================")
        print(f"Name                    : {status['name']}")
        print(f"Version                 : {status['version']}")
        print(f"Status                  : {status['status']}")
        print(f"Reflection Ready        : {status['reflection_ready']}")
        print(f"Memory Read Ready       : {status['memory_read_ready']}")
        print(f"Journal Read Ready      : {status['journal_read_ready']}")
        print(f"Insight Generation Ready: {status['insight_generation_ready']}")
        print(f"Automatic Memory Write  : {status['automatic_memory_write']}")
        print(f"Automatic Memory Delete : {status['automatic_memory_delete']}")
        print(f"Automatic Memory Merge  : {status['automatic_memory_merge']}")
        print(f"Memory Count            : {status['memory_count']}")
        print(f"Journal Count           : {status['journal_count']}")
        print(f"Pinned Memory Count     : {status['pinned_memory_count']}")
        print(f"Important Memory Count  : {status['important_memory_count']}")
        print(f"Milestone Count         : {status['milestone_count']}")
        print()
        print(f"Note: {status['note']}")

    def memory_reflect(self, limit: int = 8) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        reflection = manager.reflect(limit=limit)

        print("AURA Memory Reflection")
        print("======================")
        print(f"Title          : {reflection['title']}")
        print(f"Status         : {reflection['status']}")
        print(f"Memory Count   : {reflection['memory_count']}")
        print(f"Journal Count  : {reflection['journal_count']}")
        print(f"Milestone Count: {reflection['milestone_count']}")
        print(f"Limit          : {reflection['metadata']['limit']}")
        print()

        print("Recent Milestones")
        print("-----------------")
        for item in reflection["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in reflection["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in reflection["project_insights"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in reflection["safety_notes"]:
            print(f"- {item}")

    def memory_insights(self, limit: int = 8) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        result = manager.insights(limit=limit)

        print("AURA Memory Insights")
        print("====================")
        print(f"Status         : {result['status']}")
        print(f"Insight Count  : {result['insight_count']}")
        print(f"Write Performed: {result['write_performed']}")
        print(f"Delete Performed: {result['delete_performed']}")
        print(f"Merge Performed : {result['merge_performed']}")
        print()

        print("Insights")
        print("--------")
        for item in result["insights"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in result["safety_notes"]:
            print(f"- {item}")

    def memory_reflection_context(self, limit: int = 5) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        context = manager.reflection_context(limit=limit)

        print("AURA Memory Reflection Context")
        print("==============================")
        print(f"Status          : {context['status']}")
        print(f"Context Ready   : {context['context_ready']}")
        print(f"Memory Count    : {context['memory_count']}")
        print(f"Journal Count   : {context['journal_count']}")
        print(f"Milestones      : {len(context['milestones'])}")
        print(f"Memory Highlights: {len(context['memory_highlights'])}")
        print(f"Write Performed : {context['write_performed']}")
        print()
        print("Milestones")
        print("----------")
        for milestone in context["milestones"]:
            print(f"- {milestone['title']}: {milestone['content']}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for memory in context["memory_highlights"]:
            print(f"- {memory['content']}")

        print()
        print(f"Note: {context['note']}")


    def daily_briefing_status(self) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Daily Project Briefing Status")
        print("==================================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Briefing Ready         : {status['briefing_ready']}")
        print(f"Compact Ready          : {status['compact_ready']}")
        print(f"Context Ready          : {status['context_ready']}")
        print(f"Journal Read Ready     : {status['journal_read_ready']}")
        print(f"Reflection Read Ready  : {status['reflection_read_ready']}")
        print(f"System Summary Ready   : {status['system_summary_ready']}")
        print(f"Automatic File Write   : {status['automatic_file_write']}")
        print(f"Automatic Memory Write : {status['automatic_memory_write']}")
        print(f"Automatic Journal Write: {status['automatic_journal_write']}")
        print(f"Command Execution      : {status['command_execution']}")
        print(f"AURA Version           : {status['aura_version']}")
        print(f"Memory Count           : {status['memory_count']}")
        print(f"Journal Count          : {status['journal_count']}")
        print(f"Milestone Count        : {status['milestone_count']}")
        print(f"Latest Milestone       : {status['latest_milestone']}")
        print(f"Briefing Sections      : {status['briefing_sections']}")
        print()
        print(f"Note: {status['note']}")

    def daily_briefing(self, limit: int = 6) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        briefing = manager.build(limit=limit)

        print("AURA Daily Project Briefing")
        print("===========================")
        print(f"Title   : {briefing['title']}")
        print(f"Status  : {briefing['status']}")
        print(f"Version : {briefing['version']}")
        print(f"Limit   : {briefing['metadata']['limit']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
        print()

        latest = briefing["latest_milestone"]
        print("Latest Milestone")
        print("----------------")
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Recent Milestones")
        print("-----------------")
        for item in briefing["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in briefing["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in briefing["project_insights"]:
            print(f"- {item}")

        print()
        print("Safety State")
        print("------------")
        for key, value in briefing["safety_state"].items():
            print(f"{key}: {value}")

        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in briefing["recommended_next_steps"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in briefing["safety_notes"]:
            print(f"- {item}")

    def daily_briefing_compact(self, limit: int = 4) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        briefing = manager.compact(limit=limit)

        print("AURA Daily Project Briefing Compact")
        print("===================================")
        print(f"Title                    : {briefing['title']}")
        print(f"Status                   : {briefing['status']}")
        print(f"Version                  : {briefing['version']}")
        print(f"Write Performed          : {briefing['write_performed']}")
        print(f"Command Execution        : {briefing['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
        print()

        print("Latest Milestone")
        print("----------------")
        latest = briefing["latest_milestone"]
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Top Insights")
        print("------------")
        for item in briefing["top_insights"]:
            print(f"- {item}")

        print()
        print("Next Steps")
        print("----------")
        for item in briefing["next_steps"]:
            print(f"- {item}")

        print()
        print("Safety State")
        print("------------")
        for key, value in briefing["safety_state"].items():
            print(f"{key}: {value}")

    def daily_briefing_context(self, limit: int = 5) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        context = manager.context(limit=limit)

        print("AURA Daily Project Briefing Context")
        print("===================================")
        print(f"Status             : {context['status']}")
        print(f"Context Ready      : {context['context_ready']}")
        print(f"Write Performed    : {context['write_performed']}")
        print(f"Command Execution  : {context['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(context["project_summary"])
        print()

        latest = context["latest_milestone"]
        print("Latest Milestone")
        print("----------------")
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Recent Milestones")
        print("-----------------")
        for item in context["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in context["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in context["project_insights"]:
            print(f"- {item}")

        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in context["recommended_next_steps"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def voice_runtime_alpha_status(self) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Voice Runtime Alpha Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Speak Plan Ready             : {status['speak_plan_ready']}")
        print(f"Speak Test Ready             : {status['speak_test_ready']}")
        print(f"Voice Context Ready          : {status['voice_context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"TTS Backend Found            : {status['tts_backend_found']}")
        print(f"TTS Backend                  : {status['tts_backend'] or '-'}")
        print(f"TTS Backend Path             : {status['tts_backend_path'] or '-'}")
        print(f"STT Runtime Ready            : {status['stt_runtime_ready']}")
        print(f"TTS Runtime Ready            : {status['tts_runtime_ready']}")
        print(f"Microphone Access            : {status['microphone_access']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"Recording Enabled            : {status['recording_enabled']}")
        print(f"Playback Enabled             : {status['playback_enabled']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Audio File Write             : {status['audio_file_write']}")
        print(f"Requires Speaker Confirmation: {status['requires_speaker_confirmation']}")
        print(f"Requires Mic Confirmation    : {status['requires_microphone_confirmation']}")
        print(f"Python Packages              : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                  : {status['executables_found']}/{status['executables_total']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def voice_speak_plan(self, text: str) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.speak_plan(text=text)

        print("AURA Voice Speak Plan")
        print("=====================")
        print(f"Status                    : {plan['status']}")
        print(f"Text                      : {plan['text']}")
        print(f"Text Length               : {plan['text_length']}")
        print(f"Command Available         : {plan['command_available']}")
        print(f"TTS Backend               : {plan['tts_backend']['name'] or '-'}")
        print(f"TTS Backend Found         : {plan['tts_backend']['found']}")
        print(f"Proposed Command          : {plan['proposed_command'] or '-'}")
        print(f"Command Reason            : {plan['command_reason']}")
        print(f"Speaker Output            : {plan['speaker_output']}")
        print(f"Microphone Access         : {plan['microphone_access']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Playback Performed        : {plan['playback_performed']}")
        print(f"File Write Performed      : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Speaker Permission")
        print("------------------")
        permission = plan["speaker_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def voice_speak_test(self, text: str) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        result = manager.speak_test(text=text)
        plan = result["speak_plan"]

        print("AURA Voice Speak Test")
        print("=====================")
        print(f"Status               : {result['status']}")
        print(f"Test Ready           : {result['test_ready']}")
        print(f"Would Speak          : {result['would_speak']}")
        print(f"Speaker Output       : {result['speaker_output']}")
        print(f"Microphone Access    : {result['microphone_access']}")
        print(f"Command Execution    : {result['command_execution_performed']}")
        print(f"Playback Performed   : {result['playback_performed']}")
        print(f"File Write Performed : {result['file_write_performed']}")
        print()
        print("Prepared Speak Plan")
        print("-------------------")
        print(f"Text              : {plan['text']}")
        print(f"Command Available : {plan['command_available']}")
        print(f"TTS Backend       : {plan['tts_backend']['name'] or '-'}")
        print(f"Proposed Command  : {plan['proposed_command'] or '-'}")
        print(f"Command Reason    : {plan['command_reason']}")
        print()
        print(f"Note: {result['note']}")

    def voice_runtime_context(self) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]

        print("AURA Voice Runtime Alpha Context")
        print("================================")
        print(f"Status                      : {context['status']}")
        print(f"Context Ready               : {context['context_ready']}")
        print(f"Write Performed             : {context['write_performed']}")
        print(f"Command Execution Performed : {context['command_execution_performed']}")
        print(f"Microphone Access Performed : {context['microphone_access_performed']}")
        print(f"Speaker Output Performed    : {context['speaker_output_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready       : {alpha['alpha_ready']}")
        print(f"Speak Plan Ready  : {alpha['speak_plan_ready']}")
        print(f"Speak Test Ready  : {alpha['speak_test_ready']}")
        print(f"TTS Backend Found : {alpha['tts_backend_found']}")
        print(f"TTS Backend       : {alpha['tts_backend'] or '-'}")
        print(f"Microphone Access : {alpha['microphone_access']}")
        print(f"Speaker Output    : {alpha['speaker_output']}")
        print(f"Command Execution : {alpha['command_execution']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def vision_runtime_alpha_status(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Vision Runtime Alpha Status")
        print("================================")
        print(f"Name                        : {status['name']}")
        print(f"Version                     : {status['version']}")
        print(f"Status                      : {status['status']}")
        print(f"Alpha Ready                 : {status['alpha_ready']}")
        print(f"Screen Plan Ready           : {status['screen_plan_ready']}")
        print(f"Camera Plan Ready           : {status['camera_plan_ready']}")
        print(f"Vision Context Ready        : {status['vision_context_ready']}")
        print(f"Dependency Check Ready      : {status['dependency_check_ready']}")
        print(f"Screen Backend Found        : {status['screen_backend_found']}")
        print(f"Screen Backend              : {status['screen_backend'] or '-'}")
        print(f"Screen Backend Path         : {status['screen_backend_path'] or '-'}")
        print(f"Camera Backend Found        : {status['camera_backend_found']}")
        print(f"Camera Backend              : {status['camera_backend'] or '-'}")
        print(f"Camera Backend Path         : {status['camera_backend_path'] or '-'}")
        print(f"Screen Capture Ready        : {status['screen_capture_ready']}")
        print(f"Camera Capture Ready        : {status['camera_capture_ready']}")
        print(f"Vision Model Ready          : {status['vision_model_ready']}")
        print(f"Screen Access               : {status['screen_access']}")
        print(f"Camera Access               : {status['camera_access']}")
        print(f"Screenshot Capture          : {status['screenshot_capture']}")
        print(f"Camera Frame Capture        : {status['camera_frame_capture']}")
        print(f"Command Execution           : {status['command_execution']}")
        print(f"Image File Write            : {status['image_file_write']}")
        print(f"Requires Screen Confirmation: {status['requires_screen_confirmation']}")
        print(f"Requires Camera Confirmation: {status['requires_camera_confirmation']}")
        print(f"Python Packages             : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                 : {status['executables_found']}/{status['executables_total']}")
        print(f"Sections                    : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def vision_screen_plan(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.screen_plan()

        print("AURA Vision Screen Plan")
        print("=======================")
        print(f"Status                     : {plan['status']}")
        print(f"Command Available          : {plan['command_available']}")
        print(f"Screen Backend             : {plan['screen_backend']['name'] or '-'}")
        print(f"Screen Backend Found       : {plan['screen_backend']['found']}")
        print(f"Proposed Command           : {plan['proposed_command'] or '-'}")
        print(f"Command Reason             : {plan['command_reason']}")
        print(f"Screen Access              : {plan['screen_access']}")
        print(f"Camera Access              : {plan['camera_access']}")
        print(f"Screenshot Capture         : {plan['screenshot_capture_performed']}")
        print(f"Command Execution          : {plan['command_execution_performed']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Screen Permission")
        print("-----------------")
        permission = plan["screen_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def vision_camera_plan(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.camera_plan()

        print("AURA Vision Camera Plan")
        print("=======================")
        print(f"Status                     : {plan['status']}")
        print(f"Command Available          : {plan['command_available']}")
        print(f"Camera Backend             : {plan['camera_backend']['name'] or '-'}")
        print(f"Camera Backend Found       : {plan['camera_backend']['found']}")
        print(f"Proposed Command           : {plan['proposed_command'] or '-'}")
        print(f"Command Reason             : {plan['command_reason']}")
        print(f"Screen Access              : {plan['screen_access']}")
        print(f"Camera Access              : {plan['camera_access']}")
        print(f"Camera Frame Capture       : {plan['camera_frame_capture_performed']}")
        print(f"Command Execution          : {plan['command_execution_performed']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Camera Permission")
        print("-----------------")
        permission = plan["camera_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def vision_runtime_context(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]

        print("AURA Vision Runtime Alpha Context")
        print("=================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"Screen Access Performed      : {context['screen_access_performed']}")
        print(f"Camera Access Performed      : {context['camera_access_performed']}")
        print(f"Screenshot Capture Performed : {context['screenshot_capture_performed']}")
        print(f"Camera Frame Capture         : {context['camera_frame_capture_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready          : {alpha['alpha_ready']}")
        print(f"Screen Plan Ready    : {alpha['screen_plan_ready']}")
        print(f"Camera Plan Ready    : {alpha['camera_plan_ready']}")
        print(f"Screen Backend Found : {alpha['screen_backend_found']}")
        print(f"Screen Backend       : {alpha['screen_backend'] or '-'}")
        print(f"Camera Backend Found : {alpha['camera_backend_found']}")
        print(f"Camera Backend       : {alpha['camera_backend'] or '-'}")
        print(f"Screen Access        : {alpha['screen_access']}")
        print(f"Camera Access        : {alpha['camera_access']}")
        print(f"Command Execution    : {alpha['command_execution']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def avatar_runtime_alpha_status(self) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Avatar Runtime Alpha Status")
        print("================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Expression Plan Ready        : {status['expression_plan_ready']}")
        print(f"Gesture Plan Ready           : {status['gesture_plan_ready']}")
        print(f"Avatar Context Ready         : {status['avatar_context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Foundation Ready             : {status['foundation_ready']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Avatar Loaded                : {status['avatar_loaded']}")
        print(f"Model Loaded                 : {status['model_loaded']}")
        print(f"Tracking Connected           : {status['tracking_connected']}")
        print(f"Voice Link Ready             : {status['voice_link_ready']}")
        print(f"Vision Link Ready            : {status['vision_link_ready']}")
        print(f"Motion Link Ready            : {status['motion_link_ready']}")
        print(f"Render Backend Found         : {status['render_backend_found']}")
        print(f"Render Backend               : {status['render_backend'] or '-'}")
        print(f"Render Backend Path          : {status['render_backend_path'] or '-'}")
        print(f"Media Backend Found          : {status['media_backend_found']}")
        print(f"Media Backend                : {status['media_backend'] or '-'}")
        print(f"Media Backend Path           : {status['media_backend_path'] or '-'}")
        print(f"Expression Runtime Ready     : {status['expression_runtime_ready']}")
        print(f"Gesture Runtime Ready        : {status['gesture_runtime_ready']}")
        print(f"Motion Runtime Ready         : {status['motion_runtime_ready']}")
        print(f"Render Runtime Ready         : {status['render_runtime_ready']}")
        print(f"Render Performed             : {status['render_performed']}")
        print(f"Expression Changed           : {status['expression_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"External App Opened          : {status['external_app_opened']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Image File Write             : {status['image_file_write']}")
        print(f"Animation File Write         : {status['animation_file_write']}")
        print(f"Requires Prepare Confirmation: {status['requires_prepare_confirmation']}")
        print(f"Requires Write Confirmation  : {status['requires_write_confirmation']}")
        print(f"Requires Command Confirmation: {status['requires_command_confirmation']}")
        print(f"Python Packages              : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                  : {status['executables_found']}/{status['executables_total']}")
        print(f"Supported Expressions        : {status['supported_expressions']}")
        print(f"Supported Gestures           : {status['supported_gestures']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def avatar_expression_plan(self, expression: str) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.expression_plan(expression=expression)

        print("AURA Avatar Expression Plan")
        print("===========================")
        print(f"Status                    : {plan['status']}")
        print(f"Requested Expression      : {plan['requested_expression']}")
        print(f"Supported                 : {plan['supported']}")
        print(f"Request State             : {plan['request_state']}")
        print(f"Render Command Available  : {plan['render_command_available']}")
        print(f"Render Backend            : {plan['render_backend']['name'] or '-'}")
        print(f"Render Backend Found      : {plan['render_backend']['found']}")
        print(f"Proposed Render Command   : {plan['proposed_render_command'] or '-'}")
        print(f"Render Command Reason     : {plan['render_command_reason']}")
        print(f"Runtime Ready             : {plan['runtime_ready']}")
        print(f"Avatar Loaded             : {plan['avatar_loaded']}")
        print(f"Expression Changed        : {plan['expression_changed']}")
        print(f"Gesture Changed           : {plan['gesture_changed']}")
        print(f"Render Performed          : {plan['render_performed']}")
        print(f"External App Opened       : {plan['external_app_opened']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Image File Write          : {plan['image_file_write_performed']}")
        print(f"Animation File Write      : {plan['animation_file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def avatar_gesture_plan(self, gesture: str) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.gesture_plan(gesture=gesture)

        print("AURA Avatar Gesture Plan")
        print("========================")
        print(f"Status                    : {plan['status']}")
        print(f"Requested Gesture         : {plan['requested_gesture']}")
        print(f"Supported                 : {plan['supported']}")
        print(f"Request State             : {plan['request_state']}")
        print(f"Render Command Available  : {plan['render_command_available']}")
        print(f"Render Backend            : {plan['render_backend']['name'] or '-'}")
        print(f"Render Backend Found      : {plan['render_backend']['found']}")
        print(f"Proposed Render Command   : {plan['proposed_render_command'] or '-'}")
        print(f"Render Command Reason     : {plan['render_command_reason']}")
        print(f"Runtime Ready             : {plan['runtime_ready']}")
        print(f"Avatar Loaded             : {plan['avatar_loaded']}")
        print(f"Expression Changed        : {plan['expression_changed']}")
        print(f"Gesture Changed           : {plan['gesture_changed']}")
        print(f"Render Performed          : {plan['render_performed']}")
        print(f"External App Opened       : {plan['external_app_opened']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Image File Write          : {plan['image_file_write_performed']}")
        print(f"Animation File Write      : {plan['animation_file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def avatar_runtime_context(self) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]
        state = context["avatar_state"]

        print("AURA Avatar Runtime Alpha Context")
        print("=================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"Render Performed             : {context['render_performed']}")
        print(f"External App Opened          : {context['external_app_opened']}")
        print(f"Expression Changed           : {context['expression_changed']}")
        print(f"Gesture Changed              : {context['gesture_changed']}")
        print(f"Image File Write             : {context['image_file_write_performed']}")
        print(f"Animation File Write         : {context['animation_file_write_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready           : {alpha['alpha_ready']}")
        print(f"Expression Plan Ready : {alpha['expression_plan_ready']}")
        print(f"Gesture Plan Ready    : {alpha['gesture_plan_ready']}")
        print(f"Render Backend Found  : {alpha['render_backend_found']}")
        print(f"Render Backend        : {alpha['render_backend'] or '-'}")
        print(f"Media Backend Found   : {alpha['media_backend_found']}")
        print(f"Media Backend         : {alpha['media_backend'] or '-'}")
        print(f"Avatar Loaded         : {alpha['avatar_loaded']}")
        print(f"Render Performed      : {alpha['render_performed']}")
        print(f"Command Execution     : {alpha['command_execution']}")
        print()
        print("Avatar State")
        print("------------")
        print(f"Avatar Name       : {state['avatar_name']}")
        print(f"Avatar Format     : {state['avatar_format']}")
        print(f"Runtime           : {state['runtime']}")
        print(f"Body State        : {state['body_state']}")
        print(f"Pose              : {state['pose']}")
        print(f"Expression        : {state['expression']}")
        print(f"Gesture           : {state['gesture']}")
        print(f"Model Loaded      : {state['model_loaded']}")
        print(f"Tracking Connected: {state['tracking_connected']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def desktop_alpha_status(self) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Desktop Assistant Alpha Status")
        print("===================================")
        print(f"Name                          : {status['name']}")
        print(f"Version                       : {status['version']}")
        print(f"Status                        : {status['status']}")
        print(f"Alpha Ready                   : {status['alpha_ready']}")
        print(f"Action Plan Ready             : {status['action_plan_ready']}")
        print(f"Open App Plan Ready           : {status['open_app_plan_ready']}")
        print(f"Open Browser Plan Ready       : {status['open_browser_plan_ready']}")
        print(f"Open File Plan Ready          : {status['open_file_plan_ready']}")
        print(f"Workspace Context Ready       : {status['workspace_context_ready']}")
        print(f"Dependency Check Ready        : {status['dependency_check_ready']}")
        print(f"Bridge Ready                  : {status['bridge_ready']}")
        print(f"Execution Ready               : {status['execution_ready']}")
        print(f"Safe Action Execution         : {status['safe_action_execution']}")
        print(f"App Opened                    : {status['app_opened']}")
        print(f"Browser Opened                : {status['browser_opened']}")
        print(f"File Opened                   : {status['file_opened']}")
        print(f"Click Performed               : {status['click_performed']}")
        print(f"Keyboard Input Performed      : {status['keyboard_input_performed']}")
        print(f"Mouse Control                 : {status['mouse_control']}")
        print(f"Command Execution             : {status['command_execution']}")
        print(f"File Write                    : {status['file_write']}")
        print(f"External App Opened           : {status['external_app_opened']}")
        print(f"Open App Confirmation         : {status['requires_open_app_confirmation']}")
        print(f"Open Browser Confirmation     : {status['requires_open_browser_confirmation']}")
        print(f"Open File Confirmation        : {status['requires_open_file_confirmation']}")
        print(f"Run Command Confirmation      : {status['requires_run_command_confirmation']}")
        print(f"Write File Confirmation       : {status['requires_write_file_confirmation']}")
        print(f"Capability Count              : {status['capability_count']}")
        print(f"Supported Action Types        : {status['supported_action_type_count']}")
        print(f"Sandbox Ready                 : {status['sandbox_ready']}")
        print(f"Sandbox Dry Run Ready         : {status['sandbox_dry_run_ready']}")
        print(f"Real Tool Execution           : {status['real_tool_execution']}")
        print(f"Sections                      : {status['sections']}")
        print()
        print("Environment")
        print("-----------")
        env = status["environment"]
        print(f"OS                  : {env['os']}")
        print(f"OS Release          : {env['os_release']}")
        print(f"Machine             : {env['machine']}")
        print(f"Desktop Environment : {env['desktop_environment']}")
        print(f"Display             : {env['display'] or '-'}")
        print(f"Wayland Display     : {env['wayland_display'] or '-'}")
        print()
        print("Supported Action Types")
        print("----------------------")
        for item in status["supported_action_types"]:
            print(f"- {item}")
        print()
        print(f"Note: {status['note']}")

    def desktop_action_plan(self, action_type: str, target: str) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        plan = manager.action_plan(action_type=action_type, target=target)

        print("AURA Desktop Action Plan")
        print("========================")
        print(f"Status                  : {plan['status']}")
        print(f"Action Type             : {plan['action_type']}")
        print(f"Target                  : {plan['target'] or '-'}")
        print(f"Plan State              : {plan['plan_state']}")
        print(f"Supported               : {plan['supported']}")
        print(f"Description             : {plan['description']}")
        print(f"Plugin Action           : {plan['plugin_action']}")
        print(f"Command Available       : {plan['command_available']}")
        print(f"Proposed Command        : {plan['proposed_command'] or '-'}")
        print(f"Command Reason          : {plan['command_reason']}")
        print(f"Execution Ready         : {plan['execution_ready']}")
        print(f"Executed                : {plan['executed']}")
        print(f"App Opened              : {plan['app_opened']}")
        print(f"Browser Opened          : {plan['browser_opened']}")
        print(f"File Opened             : {plan['file_opened']}")
        print(f"Click Performed         : {plan['click_performed']}")
        print(f"Keyboard Input          : {plan['keyboard_input_performed']}")
        print(f"Mouse Control           : {plan['mouse_control_performed']}")
        print(f"External App Opened     : {plan['external_app_opened']}")
        print(f"Command Execution       : {plan['command_execution_performed']}")
        print(f"File Write              : {plan['file_write_performed']}")
        print()

        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")
        print()

        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def desktop_open_app_plan(self, app_name: str) -> None:
        self.desktop_action_plan(action_type="open_app", target=app_name)

    def desktop_open_browser_plan(self, url: str) -> None:
        self.desktop_action_plan(action_type="open_browser", target=url)

    def desktop_open_file_plan(self, file_path: str) -> None:
        self.desktop_action_plan(action_type="open_file", target=file_path)

    def desktop_workspace_context(self) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        context = manager.workspace_context()
        alpha = context["alpha_status"]
        env = context["environment"]

        print("AURA Desktop Workspace Context")
        print("==============================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"App Opened                   : {context['app_opened']}")
        print(f"Browser Opened               : {context['browser_opened']}")
        print(f"File Opened                  : {context['file_opened']}")
        print(f"Click Performed              : {context['click_performed']}")
        print(f"Keyboard Input Performed     : {context['keyboard_input_performed']}")
        print(f"Mouse Control Performed      : {context['mouse_control_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready              : {alpha['alpha_ready']}")
        print(f"Action Plan Ready        : {alpha['action_plan_ready']}")
        print(f"Open App Plan Ready      : {alpha['open_app_plan_ready']}")
        print(f"Open Browser Plan Ready  : {alpha['open_browser_plan_ready']}")
        print(f"Open File Plan Ready     : {alpha['open_file_plan_ready']}")
        print(f"Workspace Context Ready  : {alpha['workspace_context_ready']}")
        print(f"Safe Action Execution    : {alpha['safe_action_execution']}")
        print(f"Command Execution        : {alpha['command_execution']}")
        print(f"File Write               : {alpha['file_write']}")
        print()
        print("Environment")
        print("-----------")
        print(f"OS                  : {env['os']}")
        print(f"OS Release          : {env['os_release']}")
        print(f"Machine             : {env['machine']}")
        print(f"Desktop Environment : {env['desktop_environment']}")
        print(f"Display             : {env['display'] or '-'}")
        print(f"Wayland Display     : {env['wayland_display'] or '-'}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def partner_alpha_status(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Partner Alpha Status")
        print("=========================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Partner Ready                : {status['partner_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Readiness Report Ready       : {status['readiness_report_ready']}")
        print(f"Next Step Ready              : {status['next_step_ready']}")
        print(f"Action Safety Ready          : {status['action_safety_ready']}")
        print(f"Component Readiness          : {status['component_readiness']}")
        print(f"Awakening Readiness          : {status['awakening_readiness']}")
        print(f"Memory Count                 : {status['memory_count']}")
        print(f"Journal Count                : {status['journal_count']}")
        print(f"Roles                        : {status['roles']}")
        print(f"Skills                       : {status['skills']}")
        print(f"Plugin Actions               : {status['plugin_actions']}")
        print(f"Voice Runtime Alpha Ready    : {status['voice_runtime_alpha_ready']}")
        print(f"Vision Runtime Alpha Ready   : {status['vision_runtime_alpha_ready']}")
        print(f"Avatar Runtime Alpha Ready   : {status['avatar_runtime_alpha_ready']}")
        print(f"Desktop Assistant Alpha Ready: {status['desktop_assistant_alpha_ready']}")
        print(f"Actions Checked              : {status['actions_checked']}")
        print(f"Actions Need Confirmation    : {status['actions_requiring_confirmation']}")
        print(f"Actions Restricted           : {status['actions_restricted']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Safe Action Execution        : {status['safe_action_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Microphone Access            : {status['microphone_access']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"Screen Access                : {status['screen_access']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Avatar Rendering             : {status['avatar_rendering']}")
        print(f"Avatar Expression Changed    : {status['avatar_expression_changed']}")
        print(f"Avatar Gesture Changed       : {status['avatar_gesture_changed']}")
        print(f"Desktop App Opened           : {status['desktop_app_opened']}")
        print(f"Desktop Browser Opened       : {status['desktop_browser_opened']}")
        print(f"Desktop File Opened          : {status['desktop_file_opened']}")
        print(f"Desktop Click Performed      : {status['desktop_click_performed']}")
        print(f"Desktop Keyboard Input       : {status['desktop_keyboard_input_performed']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print()
        print(f"Note: {status['note']}")

    def partner_context(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Partner Alpha Context")
        print("==========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Project")
        print("-------")
        print(f"Project Summary : {context['project_summary']}")
        print(f"Latest Milestone: {context['latest_milestone'] or '-'}")
        print()
        print("Readiness")
        print("---------")
        readiness = context["readiness"]
        print(f"Readiness Ready : {readiness['readiness_ready']}")
        print(f"Readiness       : {readiness['readiness']}")
        print(f"Partner Ready   : {readiness['partner_ready']}")
        print(f"Write Performed : {readiness['write_performed']}")
        print(f"Command Executed: {readiness['command_execution_performed']}")
        print()
        print("Action Safety")
        print("-------------")
        safety = context["action_safety"]
        print(f"Status                    : {safety['status']}")
        print(f"Actions Checked           : {safety['actions_checked']}")
        print(f"Ready Count               : {safety['ready_count']}")
        print(f"Requires Confirmation     : {safety['requires_confirmation_count']}")
        print(f"Restricted Count          : {safety['restricted_count']}")
        print(f"Executed                  : {safety['executed']}")
        print()
        print("Project Insights")
        print("----------------")
        for item in context["project_insights"][:6]:
            print(f"- {item}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in context["recommended_next_steps"][:6]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")

    def partner_readiness(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        readiness = manager.readiness_report()

        print("AURA Partner Alpha Readiness")
        print("============================")
        print(f"Status                       : {readiness['status']}")
        print(f"Readiness Ready              : {readiness['readiness_ready']}")
        print(f"Readiness                    : {readiness['readiness']}")
        print(f"Partner Ready                : {readiness['partner_ready']}")
        print(f"Ready Count                  : {readiness['ready_count']}")
        print(f"Total Components             : {readiness['total_components']}")
        print(f"Write Performed              : {readiness['write_performed']}")
        print(f"Command Execution Performed  : {readiness['command_execution_performed']}")
        print()
        print("Components")
        print("----------")
        for component in readiness["components"]:
            print(f"- {component['name']}")
            print(f"  Status : {component['status']}")
            print(f"  Ready  : {component['ready']}")
            print(f"  Summary: {component['summary']}")
        print()
        print("Blocked Real-World Access")
        print("-------------------------")
        for item in readiness["blocked_real_world_access"]:
            print(f"- {item}")
        print()
        print("Safety State")
        print("------------")
        safety = readiness["safety_state"]
        print(f"Real Tool Execution : {safety['real_tool_execution']}")
        print(f"Safe Action Execution: {safety['safe_action_execution']}")
        print(f"Memory Write        : {safety['memory_write']}")
        print(f"Journal Write       : {safety['journal_write']}")
        print(f"File Write          : {safety['file_write']}")
        print(f"Command Execution   : {safety['command_execution']}")
        print()
        print(f"Note: {readiness['note']}")

    def partner_next_step(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        recommendation = manager.next_step_recommendation()

        print("AURA Partner Alpha Next Step")
        print("============================")
        print(f"Status                       : {recommendation['status']}")
        print(f"Recommendation Ready         : {recommendation['recommendation_ready']}")
        print(f"Latest Milestone             : {recommendation['latest_milestone'] or '-'}")
        print(f"Write Performed              : {recommendation['write_performed']}")
        print(f"Memory Write Performed       : {recommendation['memory_write_performed']}")
        print(f"Journal Write Performed      : {recommendation['journal_write_performed']}")
        print(f"Command Execution Performed  : {recommendation['command_execution_performed']}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in recommendation["recommended_next_steps"]:
            print(f"- {item}")
        print()
        print("Safety Notes")
        print("------------")
        for item in recommendation["safety_notes"]:
            print(f"- {item}")


    def workspace_awareness_status(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Workspace Awareness Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Awareness Ready              : {status['awareness_ready']}")
        print(f"Workspace Map Ready          : {status['workspace_map_ready']}")
        print(f"Workspace Context Ready      : {status['workspace_context_ready']}")
        print(f"Current State Ready          : {status['current_state_ready']}")
        print(f"Important Files Ready        : {status['important_files_ready']}")
        print(f"Project Root Detected        : {status['project_root_detected']}")
        print(f"Git Repository Detected      : {status['git_repository_detected']}")
        print(f"Git Branch                   : {status['git_branch']}")
        print(f"Latest Commit Hint           : {status['latest_commit_hint'] or '-'}")
        print(f"AURA Version                 : {status['aura_version']}")
        print(f"Current Sprint               : {status['current_sprint'] or '-'}")
        print(f"Top-Level Directories        : {status['top_level_directories']}")
        print(f"Top-Level Files              : {status['top_level_files']}")
        print(f"Workspace Directories        : {status['workspace_directories']}")
        print(f"Workspace Files              : {status['workspace_files']}")
        print(f"Important Files              : {status['existing_important_file_count']}/{status['important_file_count']}")
        print(f"Ignored Directories          : {status['ignored_dir_count']}")
        print(f"Python Files                 : {status['python_files']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def workspace_map(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        workspace_map = manager.workspace_map(depth=2, limit=120)

        print("AURA Workspace Map")
        print("==================")
        print(f"Status                       : {workspace_map['status']}")
        print(f"Workspace Map Ready          : {workspace_map['workspace_map_ready']}")
        print(f"Project Root                 : {workspace_map['project_root']}")
        print(f"Depth                        : {workspace_map['depth']}")
        print(f"Limit                        : {workspace_map['limit']}")
        print(f"Directories                  : {workspace_map['directories']}")
        print(f"Files                        : {workspace_map['files']}")
        print(f"Read Only                    : {workspace_map['read_only']}")
        print(f"Write Performed              : {workspace_map['write_performed']}")
        print(f"Command Execution Performed  : {workspace_map['command_execution_performed']}")
        print()
        print("Ignored/Runtime Directories")
        print("---------------------------")
        for item in workspace_map["ignored_dirs"]:
            print(f"- {item}")
        print()
        print("Entries")
        print("-------")
        for item in workspace_map["entries"]:
            marker = "D" if item["type"] == "directory" else "F"
            print(f"- [{marker}] {item['path']}")
        print()
        print(f"Note: {workspace_map['note']}")

    def workspace_context(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Workspace Context")
        print("======================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Summary")
        print("-------")
        print(context["workspace_summary"])
        print()
        print("Current State")
        print("-------------")
        state = context["current_state"]
        print(f"Version             : {state['version']}")
        print(f"Codename            : {state['codename']}")
        print(f"Creator             : {state['creator']}")
        print(f"Motto               : {state['motto']}")
        print(f"Current Sprint      : {state['current_sprint'] or '-'}")
        print(f"Git Repository      : {state['git_repository_detected']}")
        print(f"Git Branch          : {state['git_branch']}")
        print(f"Git Status Checked  : {state['git_status_checked']}")
        print(f"Python Files        : {state['python_files']}")
        print(f"Memory Records      : {state['memory_records']}")
        print(f"Journal Entries     : {state['journal_entries']}")
        print()
        print("Top-Level Directories")
        print("---------------------")
        for item in context["top_level_directories"]:
            print(f"- {item}")
        print()
        print("Top-Level Files")
        print("---------------")
        for item in context["top_level_files"]:
            print(f"- {item}")
        print()
        print("Important Files")
        print("---------------")
        for item in context["important_files"]:
            state_text = "exists" if item["exists"] else "missing"
            print(f"- {item['path']} [{state_text}]")
            print(f"  Reason: {item['reason']}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")

    def workspace_current_state(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        state = manager.current_state()

        print("AURA Workspace Current State")
        print("============================")
        print(f"Status                       : {state['status']}")
        print(f"Current State Ready          : {state['current_state_ready']}")
        print(f"Project Root                 : {state['project_root']}")
        print(f"Version                      : {state['version']}")
        print(f"Codename                     : {state['codename']}")
        print(f"Creator                      : {state['creator']}")
        print(f"Motto                        : {state['motto']}")
        print(f"Current Sprint               : {state['current_sprint'] or '-'}")
        print(f"Git Repository Detected      : {state['git_repository_detected']}")
        print(f"Git Branch                   : {state['git_branch']}")
        print(f"Latest Commit Hint           : {state['latest_commit_hint'] or '-'}")
        print(f"Git Status Checked           : {state['git_status_checked']}")
        print(f"Git Status Note              : {state['git_status_note']}")
        print(f"Python Files                 : {state['python_files']}")
        print(f"Memory Records               : {state['memory_records']}")
        print(f"Journal Entries              : {state['journal_entries']}")
        print(f"Read Only                    : {state['read_only']}")
        print(f"Write Performed              : {state['write_performed']}")
        print(f"Command Execution Performed  : {state['command_execution_performed']}")

    def workspace_important_files(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        files = manager.important_files()

        print("AURA Workspace Important Files")
        print("==============================")
        print(f"Important File Candidates: {len(files)}")
        print()
        for item in files:
            state_text = "exists" if item["exists"] else "missing"
            print(f"- {item['path']}")
            print(f"  State : {state_text}")
            print(f"  Type  : {item['type']}")
            print(f"  Size  : {item['size_bytes']} bytes")
            print(f"  Reason: {item['reason']}")
        print()
        print("Safety")
        print("------")
        print("Read Only                 : True")
        print("Write Performed           : False")
        print("Command Execution Performed: False")


    def blender_bridge_status(self) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Blender Bridge Foundation Status")
        print("=====================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Bridge Ready                 : {status['bridge_ready']}")
        print(f"Scene Plan Ready             : {status['scene_plan_ready']}")
        print(f"Asset Plan Ready             : {status['asset_plan_ready']}")
        print(f"Texture Plan Ready           : {status['texture_plan_ready']}")
        print(f"Material Plan Ready          : {status['material_plan_ready']}")
        print(f"Rigging Plan Ready           : {status['rigging_plan_ready']}")
        print(f"Animation Plan Ready         : {status['animation_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Asset Awareness Ready        : {status['asset_awareness_ready']}")
        print(f"Backend Found                : {status['backend_found']}")
        print(f"Backend Name                 : {status['backend_name'] or '-'}")
        print(f"Backend Path                 : {status['backend_path'] or '-'}")
        print(f"bpy Found                    : {status['bpy_found']}")
        print(f"Blender Executable Found     : {status['blender_executable_found']}")
        print(f"Blender Executable Path      : {status['blender_executable_path'] or '-'}")
        print(f"FFmpeg Found                 : {status['ffmpeg_found']}")
        print(f"Asset Candidates             : {status['asset_candidate_count']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Blender App Opened           : {status['blender_app_opened']}")
        print(f"Blender Script Executed      : {status['blender_script_executed']}")
        print(f"Scene Modified               : {status['scene_modified']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Blend File Write             : {status['blend_file_write']}")
        print(f"Texture File Write           : {status['texture_file_write']}")
        print(f"Script File Write            : {status['script_file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_blender_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Blender App Opened           : {plan['blender_app_opened']}")
        print(f"Blender Script Executed      : {plan['blender_script_executed']}")
        print(f"Scene Modified               : {plan['scene_modified']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Command Plan")
        print("------------")
        command_plan = plan["command_plan"]
        print(f"Available: {command_plan['available']}")
        print(f"Backend  : {command_plan['backend']['name'] or '-'}")
        print(f"Command  : {command_plan['command'] or '-'}")
        print(f"Reason   : {command_plan['reason']}")
        print()
        print("Asset Summary")
        print("-------------")
        asset_summary = plan["asset_summary"]
        print(f"Candidate Count: {asset_summary['candidate_count']}")
        print(f"Read Only      : {asset_summary['read_only']}")
        print(f"File Write     : {asset_summary['file_write_performed']}")
        print(f"Command Exec   : {asset_summary['command_execution_performed']}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def blender_scene_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.scene_plan(goal)
        self.print_blender_plan("AURA Blender Scene Plan", plan)

    def blender_asset_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.asset_plan(goal)
        self.print_blender_plan("AURA Blender Asset Plan", plan)

    def blender_texture_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.texture_plan(goal)
        self.print_blender_plan("AURA Blender Texture/Material Plan", plan)

    def blender_rigging_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.rigging_plan(goal)
        self.print_blender_plan("AURA Blender Rigging Plan", plan)

    def blender_animation_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.animation_plan(goal)
        self.print_blender_plan("AURA Blender Animation Plan", plan)

    def blender_context(self) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Blender Bridge Context")
        print("===========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print(f"Blender App Opened           : {context['blender_app_opened']}")
        print(f"Blender Script Executed      : {context['blender_script_executed']}")
        print()
        print("Bridge Status")
        print("-------------")
        status = context["bridge_status"]
        print(f"Bridge Ready       : {status['bridge_ready']}")
        print(f"Backend Found      : {status['backend_found']}")
        print(f"Backend Name       : {status['backend_name'] or '-'}")
        print(f"Asset Candidates   : {status['asset_candidate_count']}")
        print(f"Runtime Ready      : {status['runtime_ready']}")
        print(f"File Write         : {status['file_write']}")
        print(f"Command Execution  : {status['command_execution']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(context["workspace_context"]["workspace_summary"])
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print("Asset Summary")
        print("-------------")
        asset_summary = context["asset_summary"]
        print(f"Candidate Count: {asset_summary['candidate_count']}")
        print(f"Read Only      : {asset_summary['read_only']}")
        print(f"File Write     : {asset_summary['file_write_performed']}")
        print(f"Command Exec   : {asset_summary['command_execution_performed']}")
        print()
        print(f"Note: {context['note']}")

