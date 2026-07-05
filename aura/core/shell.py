import os
from difflib import get_close_matches
from pathlib import Path

import yaml

from aura.core.chat import AuraChat
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.actions.action_request_manager import ActionRequestManager
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.journal.project_journal import ProjectJournal
from aura.context.context_manager import ContextManager
from aura.permissions.permission_manager import PermissionManager
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner
from aura.awakening.awakening_manager import AwakeningManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.status.system_status_manager import SystemStatusManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.plugins.builtin.echo_plugin import EchoPlugin
from aura.plugins.builtin.memory_plugin import MemoryPlugin
from aura.plugins.plugin_manager import PluginManager


class AuraShell:
    """
    Interactive shell for AURA Genesis.
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.settings_path = self.project_root / "aura" / "config" / "settings.yaml"

        self.memory_store = MemoryStore(project_root=self.project_root)
        self.chat_engine = AuraChat(project_root=self.project_root)
        self.plugin_manager = PluginManager()
        self.plugins_loaded = False
        self.running = True

    def known_commands(self) -> list[str]:
        return [
            "help",
            "remember",
            "recall",
            "mem",
            "memory",
            "memory-count",
            "mem-count",
            "memory-list",
            "mem-list",
            "memory-search",
            "mem-search",
            "chat",
            "ask",
            "history",
            "status",
            "version",
            "provider",
            "desktop-status",
            "desktop-capabilities",
            "desktop-action",
            "system-status",
            "status-full",
            "vision-runtime-status",
            "vision-runtime-plan",
            "vision-runtime-check",
            "vision-status",
            "vision-providers",
            "awakening-status",
            "awaken",
            "voice-runtime-status",
            "voice-runtime-plan",
            "voice-runtime-check",
            "voice-status",
            "voice-providers",
            "project-map",
            "project-inspect",
            "project-find",
            "project-summary",
            "project-files",
            "project-read",
            "action-request",
            "action-request-check",
            "plugin-actions",
            "plugin-action",
            "plugin-action-check",
            "skills",
            "skill",
            "skill-check",
            "permissions",
            "permission-check",
            "perm-check",
            "context",
            "context-preview",
            "roles",
            "journal",
            "journal-add",
            "journal-count",
            "reason",
            "provider-check",
            "reason-check",
            "plugins",
            "plugin",
            "health",
            "clear",
            "cls",
            "exit",
            "quit",
            "q",
        ]

    def suggest_command(self, command: str) -> str | None:
        base_command = command.strip().split()[0].lower()

        matches = get_close_matches(
            base_command,
            self.known_commands(),
            n=1,
            cutoff=0.7,
        )

        if not matches:
            return None

        return matches[0]

    def print_banner(self) -> None:
        print("AURA Interactive Shell")
        print("======================")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to leave.")
        print()

    def print_help(self) -> None:
        print("Available commands:")
        print("  help                 Show this help message")
        print("  remember <text>      Save a memory")
        print("  recall               Show recent memories")
        print("  recall <limit>       Show recent memories with limit")
        print("  mem                  Alias for recall")
        print("  memory               Alias for recall")
        print("  memory-count         Show memory record count")
        print("  mem-count            Alias for memory-count")
        print("  memory-list          Show recent memories")
        print("  memory-list <limit>  Show recent memories with limit")
        print("  memory-delete <id>   Delete a memory by ID")
        print("  memory-pin <id>      Pin a memory")
        print("  mem-pin <id>         Alias for memory-pin")
        print("  memory-unpin <id>    Unpin a memory")
        print("  mem-unpin <id>       Alias for memory-unpin")
        print("  memory-importance <id> <1-5>  Set memory importance")
        print("  mem-importance <id> <1-5>     Alias for memory-importance")
        print("  memory-pinned        Show pinned memories")
        print("  mem-pinned           Alias for memory-pinned")
        print("  mem-delete <id>      Alias for memory-delete")
        print("  mem-list             Alias for memory-list")
        print("  chat <text>          Send a message to AURA")
        print("  ask <text>           Alias for chat")
        print("  history              Show recent chat history")
        print("  history <limit>      Show recent chat history with limit")
        print("  memory-search <text> Search relevant memories")
        print("  mem-search <text>    Alias for memory-search")
        print("  status               Show shell status")
        print("  version              Show AURA version")
        print("  journal              Show recent project journal entries")
        print("  journal <limit>      Show recent project journal entries with limit")
        print("  journal-add <text>   Add a project journal entry")
        print("  journal-count        Count project journal entries")
        print("  context <text>       Preview AURA context packet")
        print("  context-preview <text> Alias for context")
        print("  desktop-status       Show desktop bridge status")
        print("  desktop-capabilities Show desktop bridge capabilities")
        print("  desktop-action <a>   Prepare desktop action proposal")
        print("  system-status        Show unified AURA system status")
        print("  status-full          Alias for system-status")
        print("  vision-runtime-status Show vision runtime planning status")
        print("  vision-runtime-plan   Show screen/camera/model runtime plan")
        print("  vision-runtime-check  Run passive vision runtime dependency check")
        print("  vision-status        Show vision foundation status")
        print("  vision-providers     Show vision provider placeholders")
        print("  awakening-status     Show AURA Awakening Alpha status")
        print("  awaken               Alias for awakening-status")
        print("  voice-runtime-status Show voice runtime planning status")
        print("  voice-runtime-plan   Show STT/TTS runtime plan")
        print("  voice-runtime-check  Run passive voice runtime dependency check")
        print("  voice-status         Show voice foundation status")
        print("  voice-providers      Show voice provider placeholders")
        print("  project-map          Show safe project map")
        print("  project-inspect <p>  Inspect safe project path")
        print("  project-find <text>  Search keyword in safe project files")
        print("  project-summary      Show project summary")
        print("  project-files        Show visible project files")
        print("  project-files <n>    Show visible project files with limit")
        print("  project-read <path>  Read safe project file")
        print("  action-request <name>       Prepare safe action request proposal")
        print("  action-request-check <name> Alias for action-request")
        print("  plugin-actions       Show plugin action registry")
        print("  plugin-action <name> Show plugin action detail")
        print("  plugin-action-check <name> Check plugin action permission")
        print("  skills               Show AURA skill registry")
        print("  skill <name>         Show skill detail")
        print("  skill-check <name>   Check skill permission")
        print("  permissions          Show permission policy table")
        print("  permission-check <action>  Check permission for an action")
        print("  perm-check <action>        Alias for permission-check")
        print("  provider             Show reasoning provider")
        print("  roles                Show AURA internal roles")
        print("  reason               Alias for provider")
        print("  provider-check       Check reasoning provider runtime")
        print("  reason-check         Alias for provider-check")
        print("  plugins              Show loaded plugins")
        print("  plugin               Alias for plugins")
        print("  health               Show shell health summary")
        print("  clear                Clear the terminal screen")
        print("  cls                  Alias for clear")
        print("  exit                 Exit AURA shell")
        print("  quit                 Alias for exit")
        print("  q                    Alias for exit")

    def load_identity(self) -> dict:
        if not self.identity_path.exists():
            return {}

        with self.identity_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_settings(self) -> dict:
        if not self.settings_path.exists():
            return {}

        with self.settings_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def configured_provider_name(self) -> str:
        settings = self.load_settings()
        reasoning = settings.get("reasoning", {})
        return reasoning.get("provider", "unknown")

    def ensure_plugins_loaded(self) -> None:
        if self.plugins_loaded:
            return

        self.plugin_manager.register(EchoPlugin())
        self.plugin_manager.register(MemoryPlugin(project_root=self.project_root))
        self.plugin_manager.start_all()

        self.plugins_loaded = True

    def remember(self, content: str) -> None:
        if not content.strip():
            print("Nothing to remember.")
            return

        memory = MemoryItem(
            kind="user_note",
            content=content.strip(),
            metadata={
                "source": "AuraShell",
            },
        )

        self.memory_store.save(memory)

        print("Memory saved.")

    def recall(self, limit: int = 5) -> None:
        memories = self.memory_store.list_recent(limit=limit)

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
        response = self.chat_engine.respond(message, source="AuraShell")
        print(response)

    def history(self, limit: int = 5) -> None:
        turns = self.chat_engine.recent_conversations(limit=limit)

        print("AURA Chat History")
        print("=================")

        if not turns:
            print("No chat history found.")
            return

        for turn in turns:
            print(f"User: {turn.user_message}")
            print(f"AURA: {turn.aura_response}")
            print("---")

    def memory_count(self) -> None:
        count = self.memory_store.count()

        print("AURA Memory Count")
        print("=================")
        print(f"Records: {count}")

    def memory_list(self, limit: int = 5) -> None:
        memories = self.memory_store.list_recent(limit=limit)

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

    def memory_pin(self, memory_id: str) -> None:
        memory = self.memory_store.set_pinned(memory_id=memory_id, pinned=True)

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
        memory = self.memory_store.set_pinned(memory_id=memory_id, pinned=False)

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
        print("AURA Memory Importance")
        print("======================")

        try:
            memory = self.memory_store.set_importance(
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
        memories = self.memory_store.list_pinned()

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

    def memory_delete(self, memory_id: str) -> None:
        memory = self.memory_store.find_by_id(memory_id=memory_id)

        print("AURA Memory Delete")
        print("==================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        if self.memory_store.is_protected(memory):
            print("Cannot delete protected system memory.")
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")
            return

        deleted_memory = self.memory_store.delete_by_id(memory_id=memory_id)

        if deleted_memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Deleted memory:")
        print(f"- ID: {deleted_memory.id}")
        print(f"  Kind: {deleted_memory.kind}")
        print(f"  Content: {deleted_memory.content}")

    def memory_search(self, query: str, limit: int = 5) -> None:
        memories = self.chat_engine.relevant_memories(message=query, limit=limit)

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

    def status(self) -> None:
        memory_count = self.memory_store.count()
        provider = self.chat_engine.provider_info()

        print("AURA Shell Status")
        print("=================")
        print("Shell   : ONLINE")
        print("Memory  : ONLINE")
        print("Chat    : ONLINE")
        print(f"Reason  : {provider['name']} v{provider['version']}")
        print(f"Records : {memory_count}")

    def version(self) -> None:
        identity = self.load_identity()

        name = identity.get("name", "AURA")
        version = identity.get("version", "unknown")
        codename = identity.get("codename", "unknown")
        motto = identity.get("motto", "Grow Together")

        print("AURA Version")
        print("============")
        print(f"Name     : {name}")
        print(f"Version  : {version}")
        print(f"Codename : {codename}")
        print(f"Motto    : {motto}")

    def provider(self) -> None:
        provider = self.chat_engine.provider_info()
        configured_provider = self.configured_provider_name()

        print("AURA Reasoning Provider")
        print("=======================")
        print(f"Name    : {provider['name']}")
        print(f"Version : {provider['version']}")
        print(f"Config  : {configured_provider}")

    def provider_check(self) -> None:
        runtime = self.chat_engine.provider_runtime_check()

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

    def journal(self, limit: int = 5) -> None:
        project_journal = ProjectJournal(project_root=self.project_root)
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
        project_journal = ProjectJournal(project_root=self.project_root)

        title = "Manual Entry"
        if ":" in content:
            title = content.split(":", 1)[0].strip() or "Manual Entry"

        entry = project_journal.add(
            title=title,
            content=content,
            metadata={"source": "shell"},
        )

        print("AURA Project Journal")
        print("====================")
        print("Journal entry saved.")
        print(f"- ID: {entry.id}")
        print(f"  Title: {entry.title}")
        print(f"  Content: {entry.content}")

    def journal_count(self) -> None:
        project_journal = ProjectJournal(project_root=self.project_root)

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

    def context(self, message: str) -> None:
        context_manager = ContextManager(project_root=self.project_root)
        packet = context_manager.build(user_message=message)

        print(packet.to_text())

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
        print(f"Voice Providers     : {status['foundation']['voice_providers']}")
        print(f"Vision Providers    : {status['foundation']['vision_providers']}")
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

    def plugins(self) -> None:
        self.ensure_plugins_loaded()

        plugins = self.plugin_manager.list_plugins()

        print("AURA Plugins")
        print("============")

        if not plugins:
            print("No plugins loaded.")
            return

        for plugin in plugins:
            print(
                f"{plugin['name']:<10}: {plugin['status']} "
                f"v{plugin['version']} - {plugin['description']}"
            )

    def health(self) -> None:
        self.ensure_plugins_loaded()

        plugins = self.plugin_manager.list_plugins()
        plugin_count = len(plugins)
        memory_count = self.memory_store.count()
        provider = self.chat_engine.provider_info()

        config_status = "OK" if self.settings_path.exists() else "ERROR"
        identity_status = "OK" if self.identity_path.exists() else "ERROR"

        print("AURA Shell Health")
        print("=================")
        print("Shell     : OK - Interactive shell online")
        print(f"Config    : {config_status} - settings.yaml")
        print(f"Identity  : {identity_status} - identity.yaml")
        print("Memory    : OK - File-based memory store online")
        print(f"Reasoning : OK - {provider['name']} v{provider['version']}")
        print("Chat      : OK - Chat interface online")
        print(f"Records   : OK - {memory_count} memory record(s)")
        print(f"Plugins   : OK - {plugin_count} plugin(s) loaded")

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def exit_shell(self) -> None:
        print("Goodbye, Kiput.")
        self.running = False

    def handle_command(self, raw_command: str) -> None:
        command = raw_command.strip()
        normalized = command.lower()

        if not command:
            return

        if normalized == "help":
            self.print_help()
            return

        if normalized in {"exit", "quit", "q"}:
            self.exit_shell()
            return

        if normalized.startswith("memory-pin "):
            memory_id = command[len("memory-pin "):].strip()
            self.memory_pin(memory_id=memory_id)
            return

        if normalized.startswith("mem-pin "):
            memory_id = command[len("mem-pin "):].strip()
            self.memory_pin(memory_id=memory_id)
            return

        if normalized.startswith("memory-unpin "):
            memory_id = command[len("memory-unpin "):].strip()
            self.memory_unpin(memory_id=memory_id)
            return

        if normalized.startswith("mem-unpin "):
            memory_id = command[len("mem-unpin "):].strip()
            self.memory_unpin(memory_id=memory_id)
            return

        if normalized.startswith("memory-importance "):
            parts = command.split(maxsplit=2)
            if len(parts) != 3:
                print("Usage: memory-importance <id> <1-5>")
                return

            try:
                importance = int(parts[2])
            except ValueError:
                print("Usage: memory-importance <id> <1-5>")
                return

            self.memory_importance(memory_id=parts[1], importance=importance)
            return

        if normalized.startswith("mem-importance "):
            parts = command.split(maxsplit=2)
            if len(parts) != 3:
                print("Usage: mem-importance <id> <1-5>")
                return

            try:
                importance = int(parts[2])
            except ValueError:
                print("Usage: mem-importance <id> <1-5>")
                return

            self.memory_importance(memory_id=parts[1], importance=importance)
            return

        if normalized in {"memory-pinned", "mem-pinned"}:
            self.memory_pinned()
            return

        if normalized.startswith("memory-delete "):
            memory_id = command[len("memory-delete "):].strip()
            self.memory_delete(memory_id=memory_id)
            return

        if normalized.startswith("mem-delete "):
            memory_id = command[len("mem-delete "):].strip()
            self.memory_delete(memory_id=memory_id)
            return

        if normalized in {"memory-count", "mem-count"}:
            self.memory_count()
            return

        if normalized in {"memory-list", "mem-list"}:
            self.memory_list()
            return

        if normalized.startswith("memory-list "):
            raw_limit = normalized.removeprefix("memory-list ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid memory-list limit. Example: memory-list 10")
                return

            self.memory_list(limit=limit)
            return

        if normalized.startswith("mem-list "):
            raw_limit = normalized.removeprefix("mem-list ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid mem-list limit. Example: mem-list 10")
                return

            self.memory_list(limit=limit)
            return

        if normalized.startswith("memory-search "):
            query = command[len("memory-search "):].strip()
            self.memory_search(query=query)
            return

        if normalized.startswith("mem-search "):
            query = command[len("mem-search "):].strip()
            self.memory_search(query=query)
            return

        if normalized == "status":
            self.status()
            return

        if normalized == "version":
            self.version()
            return

        if normalized == "journal":
            self.journal()
            return

        if normalized.startswith("journal "):
            value = command[len("journal "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: journal <limit>")
                return

            self.journal(limit=limit)
            return

        if normalized.startswith("journal-add "):
            content = command[len("journal-add "):].strip()
            if not content:
                print("Usage: journal-add <text>")
                return

            self.journal_add(content=content)
            return

        if normalized == "journal-count":
            self.journal_count()
            return

        if normalized == "roles":
            self.roles()
            return

        if normalized.startswith("context "):
            message = command[len("context "):].strip()
            if not message:
                print("Usage: context <text>")
                return

            self.context(message=message)
            return

        if normalized.startswith("context-preview "):
            message = command[len("context-preview "):].strip()
            if not message:
                print("Usage: context-preview <text>")
                return

            self.context(message=message)
            return

        if normalized == "desktop-status":
            self.desktop_status()
            return

        if normalized == "desktop-capabilities":
            self.desktop_capabilities()
            return

        if normalized.startswith("desktop-action "):
            action = command[len("desktop-action "):].strip()

            if not action:
                print("Usage: desktop-action <action>")
                return

            self.desktop_action(action=action)
            return

        if normalized in {"system-status", "status-full"}:
            self.system_status()
            return

        if normalized == "vision-runtime-status":
            self.vision_runtime_status()
            return

        if normalized == "vision-runtime-plan":
            self.vision_runtime_plan()
            return

        if normalized == "vision-runtime-check":
            self.vision_runtime_check()
            return

        if normalized == "vision-status":
            self.vision_status()
            return

        if normalized == "vision-providers":
            self.vision_providers()
            return

        if normalized in {"awakening-status", "awaken"}:
            self.awakening_status()
            return

        if normalized == "voice-runtime-status":
            self.voice_runtime_status()
            return

        if normalized == "voice-runtime-plan":
            self.voice_runtime_plan()
            return

        if normalized == "voice-runtime-check":
            self.voice_runtime_check()
            return

        if normalized == "voice-status":
            self.voice_status()
            return

        if normalized == "voice-providers":
            self.voice_providers()
            return

        if normalized == "project-map":
            self.project_map()
            return

        if normalized.startswith("project-map "):
            value = command[len("project-map "):].strip()

            try:
                depth = int(value)
            except ValueError:
                print("Usage: project-map <depth>")
                return

            self.project_map(depth=depth)
            return

        if normalized.startswith("project-inspect "):
            relative_path = command[len("project-inspect "):].strip()

            if not relative_path:
                print("Usage: project-inspect <path>")
                return

            self.project_inspect(relative_path=relative_path)
            return

        if normalized.startswith("project-find "):
            keyword = command[len("project-find "):].strip()

            if not keyword:
                print("Usage: project-find <keyword>")
                return

            self.project_find(keyword=keyword)
            return

        if normalized == "project-summary":
            self.project_summary()
            return

        if normalized == "project-files":
            self.project_files()
            return

        if normalized.startswith("project-files "):
            value = command[len("project-files "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: project-files <limit>")
                return

            self.project_files(limit=limit)
            return

        if normalized.startswith("project-read "):
            relative_path = command[len("project-read "):].strip()
            if not relative_path:
                print("Usage: project-read <path>")
                return

            self.project_read(relative_path=relative_path)
            return

        if normalized.startswith("action-request-check "):
            action = command[len("action-request-check "):].strip()

            if not action:
                print("Usage: action-request-check <name>")
                return

            self.action_request(action=action)
            return

        if normalized.startswith("action-request "):
            action = command[len("action-request "):].strip()

            if not action:
                print("Usage: action-request <name>")
                return

            self.action_request(action=action)
            return

        if normalized == "plugin-actions":
            self.plugin_actions()
            return

        if normalized.startswith("plugin-action-check "):
            name = command[len("plugin-action-check "):].strip()
            if not name:
                print("Usage: plugin-action-check <name>")
                return

            self.plugin_action_check(name=name)
            return

        if normalized.startswith("plugin-action "):
            name = command[len("plugin-action "):].strip()
            if not name:
                print("Usage: plugin-action <name>")
                return

            self.plugin_action_detail(name=name)
            return

        if normalized == "skills":
            self.skills()
            return

        if normalized.startswith("skill-check "):
            name = command[len("skill-check "):].strip()
            if not name:
                print("Usage: skill-check <name>")
                return

            self.skill_check(name=name)
            return

        if normalized.startswith("skill "):
            name = command[len("skill "):].strip()
            if not name:
                print("Usage: skill <name>")
                return

            self.skill_detail(name=name)
            return

        if normalized == "permissions":
            self.permissions()
            return

        if normalized.startswith("permission-check "):
            action = command[len("permission-check "):].strip()
            if not action:
                print("Usage: permission-check <action>")
                return

            self.permission_check(action=action)
            return

        if normalized.startswith("perm-check "):
            action = command[len("perm-check "):].strip()
            if not action:
                print("Usage: perm-check <action>")
                return

            self.permission_check(action=action)
            return

        if normalized in {"provider", "reason"}:
            self.provider()
            return

        if normalized in {"provider-check", "reason-check", "provider check", "reason check"}:
            self.provider_check()
            return

        if normalized in {"plugins", "plugin"}:
            self.plugins()
            return

        if normalized == "health":
            self.health()
            return

        if normalized in {"clear", "cls"}:
            self.clear()
            return

        if normalized in {"recall", "mem", "memory"}:
            self.recall()
            return

        if normalized == "history":
            self.history()
            return

        if normalized.startswith("history "):
            raw_limit = normalized.removeprefix("history ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid history limit. Example: history 3")
                return

            self.history(limit=limit)
            return

        if normalized.startswith("recall "):
            raw_limit = normalized.removeprefix("recall ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid recall limit. Example: recall 3")
                return

            self.recall(limit=limit)
            return

        if normalized.startswith("remember "):
            content = command[len("remember "):]
            self.remember(content)
            return

        if normalized.startswith("chat "):
            message = command[len("chat "):]
            self.chat(message)
            return

        if normalized.startswith("ask "):
            message = command[len("ask "):]
            self.chat(message)
            return

        suggestion = self.suggest_command(command)

        print(f"Unknown command: {command}")

        if suggestion:
            print(f"Did you mean: {suggestion}?")

        print("Type 'help' to see available commands.")

    def run(self) -> None:
        self.print_banner()

        while self.running:
            try:
                raw_command = input("AURA> ")
                self.handle_command(raw_command)
            except KeyboardInterrupt:
                print()
                print("Goodbye, Kiput.")
                break
