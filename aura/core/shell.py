import os
from difflib import get_close_matches
from pathlib import Path

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
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.game.game_companion_foundation_manager import GameCompanionFoundationManager
from aura.streaming.streaming_safety_foundation_manager import StreamingSafetyFoundationManager
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.journal.project_journal import ProjectJournal
from aura.context.context_manager import ContextManager
from aura.permissions.permission_manager import PermissionManager
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.creative.creative_assistant_foundation_manager import CreativeAssistantFoundationManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager
from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
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
            "daily-briefing-status",
            "daily-briefing",
            "daily-briefing-compact",
            "daily-briefing-context",
            "memory-reflection-status",
            "memory-reflect",
            "memory-insights",
            "memory-reflection-context",
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
            "tool-sandbox-status",
            "tool-sandbox-policy",
            "tool-sandbox-check",
            "tool-sandbox-dry-run",
            "model-router-status",
            "model-router-routes",
            "model-router-select",
            "core-loop-status",
            "core-loop-run",
            "core-loop-trace",
            "avatar-runtime-alpha-status",
            "avatar-expression-plan",
            "avatar-gesture-plan",
            "avatar-runtime-context",
            "avatar-status",
            "avatar-providers",
            "avatar-state",
            "avatar-expression",
            "avatar-gesture",
            "desktop-alpha-status",
            "desktop-action-plan",
            "desktop-open-app-plan",
            "desktop-open-browser-plan",
            "desktop-open-file-plan",
            "desktop-workspace-context",
            "desktop-status",
            "desktop-capabilities",
            "desktop-action",
            "system-status",
            "status-full",
            "vision-runtime-alpha-status",
            "vision-screen-plan",
            "vision-camera-plan",
            "vision-runtime-context",
            "vision-runtime-status",
            "vision-runtime-plan",
            "vision-runtime-check",
            "vision-status",
            "vision-providers",
            "creative-assistant-status",
            "creative-brief-plan",
            "creative-character-concept-plan",
            "creative-visual-asset-plan",
            "creative-content-idea-plan",
            "creative-review-plan",
            "creative-context",
            "project-intent-status",
            "project-intent-summary",
            "project-goal-plan",
            "sprint-intent-plan",
            "project-next-action-candidates",
            "project-intent-context",
            "workspace-memory-link-status",
            "workspace-memory-summary",
            "workspace-memory-candidates",
            "workspace-file-memory-candidates",
            "workspace-milestone-memory-candidates",
            "workspace-memory-link-context",
            "streaming-safety-status",
            "streaming-context-plan",
            "streaming-chat-safety-plan",
            "streaming-content-boundary-plan",
            "streaming-privacy-plan",
            "streaming-moderation-plan",
            "streaming-safety-context",
            "game-companion-status",
            "game-session-plan",
            "game-strategy-plan",
            "game-streaming-plan",
            "game-coaching-plan",
            "game-context",
            "expression-language-status",
            "expression-state",
            "expression-plan",
            "expression-voice-hint",
            "expression-avatar-hint",
            "expression-gesture-hint",
            "expression-context",
            "media-understanding-status",
            "media-asset-summary",
            "media-image-plan",
            "media-texture-reference-plan",
            "media-thumbnail-review-plan",
            "media-video-plan",
            "media-context",
            "blender-bridge-status",
            "blender-scene-plan",
            "blender-asset-plan",
            "blender-texture-plan",
            "blender-rigging-plan",
            "blender-animation-plan",
            "blender-context",
            "workspace-awareness-status",
            "workspace-map",
            "workspace-context",
            "workspace-current-state",
            "workspace-important-files",
            "partner-alpha-status",
            "partner-context",
            "partner-readiness",
            "partner-next-step",
            "awakening-status",
            "awaken",
            "voice-runtime-alpha-status",
            "voice-speak-plan",
            "voice-speak-test",
            "voice-runtime-context",
            "voice-runtime-status",
            "voice-runtime-plan",
            "voice-runtime-check",
            "voice-status",
            "voice-providers",
            "project-code-status",
            "project-code-map",
            "project-code-inspect",
            "project-code-plan",
            "project-code-safety",
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
        print("  daily-briefing-status Show Daily Project Briefing status")
        print("  daily-briefing       Show daily project briefing")
        print("  daily-briefing <n>   Show daily project briefing with limit")
        print("  daily-briefing-compact Show compact daily briefing")
        print("  daily-briefing-compact <n> Show compact daily briefing with limit")
        print("  daily-briefing-context Show daily briefing context")
        print("  daily-briefing-context <n> Show daily briefing context with limit")
        print("  memory-reflection-status Show Memory Reflection System status")
        print("  memory-reflect       Reflect on memory and journal")
        print("  memory-reflect <n>   Reflect with milestone limit")
        print("  memory-insights      Show reflection insights")
        print("  memory-insights <n>  Show reflection insights with limit")
        print("  memory-reflection-context Show reflection context")
        print("  memory-reflection-context <n> Show reflection context with limit")
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
        print("  tool-sandbox-status  Show tool sandbox foundation status")
        print("  tool-sandbox-policy  Show tool sandbox policy")
        print("  tool-sandbox-check <cmd> Check command safety")
        print("  tool-sandbox-dry-run <cmd> Prepare dry-run plan")
        print("  model-router-status  Show model router foundation status")
        print("  model-router-routes  List model routes")
        print("  model-router-select <target> Select model route metadata")
        print("  core-loop-status     Show AURA alpha core loop status")
        print("  core-loop-run <text> Run alpha core loop safely")
        print("  core-loop-trace <text> Trace alpha core loop safely")
        print("  avatar-runtime-alpha-status Show Avatar Runtime Alpha status")
        print("  avatar-expression-plan <e> Prepare safe avatar expression plan")
        print("  avatar-gesture-plan <g>   Prepare safe avatar gesture plan")
        print("  avatar-runtime-context Show Avatar Runtime Alpha context")
        print("  avatar-status        Show avatar foundation status")
        print("  avatar-providers     Show avatar placeholder providers")
        print("  avatar-state         Show placeholder avatar state")
        print("  avatar-expression <e> Prepare expression proposal")
        print("  avatar-gesture <g>   Prepare gesture proposal")
        print("  desktop-alpha-status Show Desktop Assistant Alpha status")
        print("  desktop-action-plan <type> <target> Prepare safe desktop action plan")
        print("  desktop-open-app-plan <app> Prepare safe open app plan")
        print("  desktop-open-browser-plan <url> Prepare safe open browser plan")
        print("  desktop-open-file-plan <path> Prepare safe open file plan")
        print("  desktop-workspace-context Show desktop workspace context")
        print("  desktop-status       Show desktop bridge status")
        print("  desktop-capabilities Show desktop bridge capabilities")
        print("  desktop-action <a>   Prepare desktop action proposal")
        print("  system-status        Show unified AURA system status")
        print("  status-full          Alias for system-status")
        print("  vision-runtime-alpha-status Show Vision Runtime Alpha status")
        print("  vision-screen-plan   Prepare safe screen analysis plan")
        print("  vision-camera-plan   Prepare safe camera analysis plan")
        print("  vision-runtime-context Show Vision Runtime Alpha context")
        print("  vision-runtime-status Show vision runtime planning status")
        print("  vision-runtime-plan   Show screen/camera/model runtime plan")
        print("  vision-runtime-check  Run passive vision runtime dependency check")
        print("  vision-status        Show vision foundation status")
        print("  vision-providers     Show vision provider placeholders")
        print("  creative-assistant-status Show AURA Creative Assistant Foundation status")
        print("  creative-brief-plan <target> Prepare safe creative brief plan")
        print("  creative-character-concept-plan <target> Prepare character concept plan")
        print("  creative-visual-asset-plan <target> Prepare visual asset plan")
        print("  creative-content-idea-plan <target> Prepare content idea plan")
        print("  creative-review-plan <target> Prepare creative review plan")
        print("  creative-context Show creative assistant context")
        print("  project-intent-status Show AURA Project Intent Planner status")
        print("  project-intent-summary <topic> Show read-only project intent summary")
        print("  project-goal-plan <goal> Prepare safety-aware project goal plan")
        print("  sprint-intent-plan <goal> Prepare sprint intent plan")
        print("  project-next-action-candidates <topic> Prepare next action candidates")
        print("  project-intent-context Show project intent planner context")
        print("  workspace-memory-link-status Show AURA Workspace Memory Link status")
        print("  workspace-memory-summary Show read-only workspace memory summary")
        print("  workspace-memory-candidates <target> Prepare project memory candidates")
        print("  workspace-file-memory-candidates <target> Prepare important file memory candidates")
        print("  workspace-milestone-memory-candidates <target> Prepare milestone memory candidates")
        print("  workspace-memory-link-context Show workspace memory link context")
        print("  streaming-safety-status Show AURA Streaming Safety Foundation status")
        print("  streaming-context-plan <target> Prepare safe streaming context plan")
        print("  streaming-chat-safety-plan <target> Prepare safe chat safety plan")
        print("  streaming-content-boundary-plan <target> Prepare safe content boundary plan")
        print("  streaming-privacy-plan <target> Prepare safe privacy plan")
        print("  streaming-moderation-plan <target> Prepare safe moderation note plan")
        print("  streaming-safety-context Show streaming safety context")
        print("  game-companion-status Show AURA Game Companion Foundation status")
        print("  game-session-plan <target> Prepare safe game session plan")
        print("  game-strategy-plan <target> Prepare safe game strategy plan")
        print("  game-streaming-plan <target> Prepare streaming-safe game plan")
        print("  game-coaching-plan <target> Prepare safe game coaching plan")
        print("  game-context Show game companion context")
        print("  expression-language-status Show AURA Expression Language status")
        print("  expression-state Show AURA internal expression state")
        print("  expression-plan <text> Prepare safe expression plan")
        print("  expression-voice-hint <target> Prepare safe voice tone hint")
        print("  expression-avatar-hint <target> Prepare safe avatar expression hint")
        print("  expression-gesture-hint <target> Prepare safe gesture hint")
        print("  expression-context Show expression language context")
        print("  media-understanding-status Show AURA Media Understanding status")
        print("  media-asset-summary Show metadata-only media asset summary")
        print("  media-image-plan <goal> Prepare safe image description plan")
        print("  media-texture-reference-plan <goal> Prepare safe texture reference plan")
        print("  media-thumbnail-review-plan <goal> Prepare safe thumbnail/banner review plan")
        print("  media-video-plan <goal> Prepare safe video/audio plan")
        print("  media-context Show media understanding context")
        print("  blender-bridge-status Show AURA Blender Bridge Foundation status")
        print("  blender-scene-plan <goal> Prepare safe Blender scene plan")
        print("  blender-asset-plan <goal> Prepare safe Blender asset plan")
        print("  blender-texture-plan <goal> Prepare safe Blender texture/material plan")
        print("  blender-rigging-plan <goal> Prepare safe Blender rigging plan")
        print("  blender-animation-plan <goal> Prepare safe Blender animation plan")
        print("  blender-context     Show Blender bridge context")
        print("  workspace-awareness-status Show AURA Workspace Awareness status")
        print("  workspace-map        Show read-only AURA workspace map")
        print("  workspace-context    Show read-only AURA workspace context")
        print("  workspace-current-state Show current AURA workspace state")
        print("  workspace-important-files Show important AURA project files")
        print("  partner-alpha-status Show AURA Partner Alpha status")
        print("  partner-context      Show AURA Partner Alpha context")
        print("  partner-readiness    Show AURA Partner Alpha readiness")
        print("  partner-next-step    Show AURA Partner Alpha next step")
        print("  awakening-status     Show AURA Awakening Alpha status")
        print("  awaken               Alias for awakening-status")
        print("  voice-runtime-alpha-status Show Voice Runtime Alpha status")
        print("  voice-speak-plan <text> Prepare safe TTS speak plan")
        print("  voice-speak-test <text> Prepare speak test without playback")
        print("  voice-runtime-context Show Voice Runtime Alpha context")
        print("  voice-runtime-status Show voice runtime planning status")
        print("  voice-runtime-plan   Show STT/TTS runtime plan")
        print("  voice-runtime-check  Run passive voice runtime dependency check")
        print("  voice-status         Show voice foundation status")
        print("  voice-providers      Show voice provider placeholders")
        print("  project-code-status  Show Project Coding Assistant v2 status")
        print("  project-code-map     Show AST-based project code map")
        print("  project-code-inspect <path> Inspect code file")
        print("  project-code-plan <request> Prepare safe patch plan")
        print("  project-code-safety <cmd> Check command safety")
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
        print(f"Creative Assistant  : {status['foundation']['creative_assistant_sections']}")
        print(f"Creative Plan Types : {status['foundation']['creative_plan_types']}")
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

        if normalized == "daily-briefing-status":
            self.daily_briefing_status()
            return

        if normalized == "daily-briefing":
            self.daily_briefing()
            return

        if normalized.startswith("daily-briefing "):
            value = command[len("daily-briefing "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing <limit>")
                return
            self.daily_briefing(limit=limit)
            return

        if normalized == "daily-briefing-compact":
            self.daily_briefing_compact()
            return

        if normalized.startswith("daily-briefing-compact "):
            value = command[len("daily-briefing-compact "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing-compact <limit>")
                return
            self.daily_briefing_compact(limit=limit)
            return

        if normalized == "daily-briefing-context":
            self.daily_briefing_context()
            return

        if normalized.startswith("daily-briefing-context "):
            value = command[len("daily-briefing-context "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing-context <limit>")
                return
            self.daily_briefing_context(limit=limit)
            return

        if normalized == "memory-reflection-status":
            self.memory_reflection_status()
            return

        if normalized == "memory-reflect":
            self.memory_reflect()
            return

        if normalized.startswith("memory-reflect "):
            value = command[len("memory-reflect "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-reflect <limit>")
                return
            self.memory_reflect(limit=limit)
            return

        if normalized == "memory-insights":
            self.memory_insights()
            return

        if normalized.startswith("memory-insights "):
            value = command[len("memory-insights "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-insights <limit>")
                return
            self.memory_insights(limit=limit)
            return

        if normalized == "memory-reflection-context":
            self.memory_reflection_context()
            return

        if normalized.startswith("memory-reflection-context "):
            value = command[len("memory-reflection-context "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-reflection-context <limit>")
                return
            self.memory_reflection_context(limit=limit)
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

        if normalized == "tool-sandbox-status":
            self.tool_sandbox_status()
            return

        if normalized == "tool-sandbox-policy":
            self.tool_sandbox_policy()
            return

        if normalized.startswith("tool-sandbox-check "):
            command_text = command[len("tool-sandbox-check "):].strip()

            if not command_text:
                print("Usage: tool-sandbox-check <command>")
                return

            self.tool_sandbox_check(command=command_text)
            return

        if normalized.startswith("tool-sandbox-dry-run "):
            command_text = command[len("tool-sandbox-dry-run "):].strip()

            if not command_text:
                print("Usage: tool-sandbox-dry-run <command>")
                return

            self.tool_sandbox_dry_run(command=command_text)
            return

        if normalized == "model-router-status":
            self.model_router_status()
            return

        if normalized == "model-router-routes":
            self.model_router_routes()
            return

        if normalized.startswith("model-router-select "):
            target = command[len("model-router-select "):].strip()

            if not target:
                print("Usage: model-router-select <target>")
                return

            self.model_router_select(target=target)
            return

        if normalized == "core-loop-status":
            self.core_loop_status()
            return

        if normalized.startswith("core-loop-run "):
            message = command[len("core-loop-run "):].strip()

            if not message:
                print("Usage: core-loop-run <text>")
                return

            self.core_loop_run(message=message)
            return

        if normalized.startswith("core-loop-trace "):
            message = command[len("core-loop-trace "):].strip()

            if not message:
                print("Usage: core-loop-trace <text>")
                return

            self.core_loop_trace(message=message)
            return

        if normalized == "avatar-runtime-alpha-status":
            self.avatar_runtime_alpha_status()
            return

        if normalized.startswith("avatar-expression-plan "):
            expression = command[len("avatar-expression-plan "):].strip()
            if not expression:
                print("Usage: avatar-expression-plan <expression>")
                return
            self.avatar_expression_plan(expression=expression)
            return

        if normalized == "avatar-expression-plan":
            print("Usage: avatar-expression-plan <expression>")
            return

        if normalized.startswith("avatar-gesture-plan "):
            gesture = command[len("avatar-gesture-plan "):].strip()
            if not gesture:
                print("Usage: avatar-gesture-plan <gesture>")
                return
            self.avatar_gesture_plan(gesture=gesture)
            return

        if normalized == "avatar-gesture-plan":
            print("Usage: avatar-gesture-plan <gesture>")
            return

        if normalized == "avatar-runtime-context":
            self.avatar_runtime_context()
            return

        if normalized == "avatar-status":
            self.avatar_status()
            return

        if normalized == "avatar-providers":
            self.avatar_providers()
            return

        if normalized == "avatar-state":
            self.avatar_state()
            return

        if normalized.startswith("avatar-expression "):
            expression = command[len("avatar-expression "):].strip()

            if not expression:
                print("Usage: avatar-expression <expression>")
                return

            self.avatar_expression(expression=expression)
            return

        if normalized.startswith("avatar-gesture "):
            gesture = command[len("avatar-gesture "):].strip()

            if not gesture:
                print("Usage: avatar-gesture <gesture>")
                return

            self.avatar_gesture(gesture=gesture)
            return

        if normalized == "desktop-alpha-status":
            self.desktop_alpha_status()
            return

        if normalized.startswith("desktop-action-plan "):
            rest = command[len("desktop-action-plan "):].strip()
            parts = rest.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: desktop-action-plan <action_type> <target>")
                return
            self.desktop_action_plan(action_type=parts[0], target=parts[1])
            return

        if normalized == "desktop-action-plan":
            print("Usage: desktop-action-plan <action_type> <target>")
            return

        if normalized.startswith("desktop-open-app-plan "):
            app_name = command[len("desktop-open-app-plan "):].strip()
            if not app_name:
                print("Usage: desktop-open-app-plan <app>")
                return
            self.desktop_open_app_plan(app_name=app_name)
            return

        if normalized == "desktop-open-app-plan":
            print("Usage: desktop-open-app-plan <app>")
            return

        if normalized.startswith("desktop-open-browser-plan "):
            url = command[len("desktop-open-browser-plan "):].strip()
            if not url:
                print("Usage: desktop-open-browser-plan <url>")
                return
            self.desktop_open_browser_plan(url=url)
            return

        if normalized == "desktop-open-browser-plan":
            print("Usage: desktop-open-browser-plan <url>")
            return

        if normalized.startswith("desktop-open-file-plan "):
            file_path = command[len("desktop-open-file-plan "):].strip()
            if not file_path:
                print("Usage: desktop-open-file-plan <path>")
                return
            self.desktop_open_file_plan(file_path=file_path)
            return

        if normalized == "desktop-open-file-plan":
            print("Usage: desktop-open-file-plan <path>")
            return

        if normalized == "desktop-workspace-context":
            self.desktop_workspace_context()
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

        if normalized == "vision-runtime-alpha-status":
            self.vision_runtime_alpha_status()
            return

        if normalized == "vision-screen-plan":
            self.vision_screen_plan()
            return

        if normalized == "vision-camera-plan":
            self.vision_camera_plan()
            return

        if normalized == "vision-runtime-context":
            self.vision_runtime_context()
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

        if normalized == "creative-assistant-status":
            self.creative_assistant_status()
            return

        if normalized.startswith("creative-brief-plan "):
            target = command[len("creative-brief-plan "):].strip()
            if not target:
                print("Usage: creative-brief-plan <target>")
                return
            self.creative_brief_plan(target)
            return

        if normalized.startswith("creative-character-concept-plan "):
            target = command[len("creative-character-concept-plan "):].strip()
            if not target:
                print("Usage: creative-character-concept-plan <target>")
                return
            self.creative_character_concept_plan(target)
            return

        if normalized.startswith("creative-visual-asset-plan "):
            target = command[len("creative-visual-asset-plan "):].strip()
            if not target:
                print("Usage: creative-visual-asset-plan <target>")
                return
            self.creative_visual_asset_plan(target)
            return

        if normalized.startswith("creative-content-idea-plan "):
            target = command[len("creative-content-idea-plan "):].strip()
            if not target:
                print("Usage: creative-content-idea-plan <target>")
                return
            self.creative_content_idea_plan(target)
            return

        if normalized.startswith("creative-review-plan "):
            target = command[len("creative-review-plan "):].strip()
            if not target:
                print("Usage: creative-review-plan <target>")
                return
            self.creative_review_plan(target)
            return

        if normalized == "creative-context":
            self.creative_context()
            return

        if normalized == "project-intent-status":
            self.project_intent_status()
            return

        if normalized.startswith("project-intent-summary "):
            topic = command[len("project-intent-summary "):].strip()
            if not topic:
                print("Usage: project-intent-summary <topic>")
                return
            self.project_intent_summary(topic)
            return

        if normalized.startswith("project-goal-plan "):
            goal = command[len("project-goal-plan "):].strip()
            if not goal:
                print("Usage: project-goal-plan <goal>")
                return
            self.project_goal_plan(goal)
            return

        if normalized.startswith("sprint-intent-plan "):
            goal = command[len("sprint-intent-plan "):].strip()
            if not goal:
                print("Usage: sprint-intent-plan <goal>")
                return
            self.sprint_intent_plan(goal)
            return

        if normalized.startswith("project-next-action-candidates "):
            topic = command[len("project-next-action-candidates "):].strip()
            if not topic:
                print("Usage: project-next-action-candidates <topic>")
                return
            self.project_next_action_candidates(topic)
            return

        if normalized == "project-intent-context":
            self.project_intent_context()
            return

        if normalized == "workspace-memory-link-status":
            self.workspace_memory_link_status()
            return

        if normalized == "workspace-memory-summary":
            self.workspace_memory_summary()
            return

        if normalized.startswith("workspace-memory-candidates "):
            target = command[len("workspace-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-memory-candidates <target>")
                return
            self.workspace_memory_candidates(target)
            return

        if normalized.startswith("workspace-file-memory-candidates "):
            target = command[len("workspace-file-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-file-memory-candidates <target>")
                return
            self.workspace_file_memory_candidates(target)
            return

        if normalized.startswith("workspace-milestone-memory-candidates "):
            target = command[len("workspace-milestone-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-milestone-memory-candidates <target>")
                return
            self.workspace_milestone_memory_candidates(target)
            return

        if normalized == "workspace-memory-link-context":
            self.workspace_memory_link_context()
            return

        if normalized == "streaming-safety-status":
            self.streaming_safety_status()
            return

        if normalized.startswith("streaming-context-plan "):
            target = command[len("streaming-context-plan "):].strip()
            if not target:
                print("Usage: streaming-context-plan <target>")
                return
            self.streaming_context_plan(target)
            return

        if normalized.startswith("streaming-chat-safety-plan "):
            target = command[len("streaming-chat-safety-plan "):].strip()
            if not target:
                print("Usage: streaming-chat-safety-plan <target>")
                return
            self.streaming_chat_safety_plan(target)
            return

        if normalized.startswith("streaming-content-boundary-plan "):
            target = command[len("streaming-content-boundary-plan "):].strip()
            if not target:
                print("Usage: streaming-content-boundary-plan <target>")
                return
            self.streaming_content_boundary_plan(target)
            return

        if normalized.startswith("streaming-privacy-plan "):
            target = command[len("streaming-privacy-plan "):].strip()
            if not target:
                print("Usage: streaming-privacy-plan <target>")
                return
            self.streaming_privacy_plan(target)
            return

        if normalized.startswith("streaming-moderation-plan "):
            target = command[len("streaming-moderation-plan "):].strip()
            if not target:
                print("Usage: streaming-moderation-plan <target>")
                return
            self.streaming_moderation_plan(target)
            return

        if normalized == "streaming-safety-context":
            self.streaming_safety_context()
            return

        if normalized == "game-companion-status":
            self.game_companion_status()
            return

        if normalized.startswith("game-session-plan "):
            target = command[len("game-session-plan "):].strip()
            if not target:
                print("Usage: game-session-plan <target>")
                return
            self.game_session_plan(target)
            return

        if normalized.startswith("game-strategy-plan "):
            target = command[len("game-strategy-plan "):].strip()
            if not target:
                print("Usage: game-strategy-plan <target>")
                return
            self.game_strategy_plan(target)
            return

        if normalized.startswith("game-streaming-plan "):
            target = command[len("game-streaming-plan "):].strip()
            if not target:
                print("Usage: game-streaming-plan <target>")
                return
            self.game_streaming_plan(target)
            return

        if normalized.startswith("game-coaching-plan "):
            target = command[len("game-coaching-plan "):].strip()
            if not target:
                print("Usage: game-coaching-plan <target>")
                return
            self.game_coaching_plan(target)
            return

        if normalized == "game-context":
            self.game_context()
            return

        if normalized == "expression-language-status":
            self.expression_language_status()
            return

        if normalized == "expression-state":
            self.expression_state()
            return

        if normalized.startswith("expression-plan "):
            target = command[len("expression-plan "):].strip()
            if not target:
                print("Usage: expression-plan <text>")
                return
            self.expression_plan(target)
            return

        if normalized.startswith("expression-voice-hint "):
            target = command[len("expression-voice-hint "):].strip()
            if not target:
                print("Usage: expression-voice-hint <target>")
                return
            self.expression_voice_hint(target)
            return

        if normalized.startswith("expression-avatar-hint "):
            target = command[len("expression-avatar-hint "):].strip()
            if not target:
                print("Usage: expression-avatar-hint <target>")
                return
            self.expression_avatar_hint(target)
            return

        if normalized.startswith("expression-gesture-hint "):
            target = command[len("expression-gesture-hint "):].strip()
            if not target:
                print("Usage: expression-gesture-hint <target>")
                return
            self.expression_gesture_hint(target)
            return

        if normalized == "expression-context":
            self.expression_context()
            return

        if normalized == "media-understanding-status":
            self.media_understanding_status()
            return

        if normalized == "media-asset-summary":
            self.media_asset_summary()
            return

        if normalized.startswith("media-image-plan "):
            goal = command[len("media-image-plan "):].strip()
            if not goal:
                print("Usage: media-image-plan <goal>")
                return
            self.media_image_plan(goal)
            return

        if normalized.startswith("media-texture-reference-plan "):
            goal = command[len("media-texture-reference-plan "):].strip()
            if not goal:
                print("Usage: media-texture-reference-plan <goal>")
                return
            self.media_texture_reference_plan(goal)
            return

        if normalized.startswith("media-thumbnail-review-plan "):
            goal = command[len("media-thumbnail-review-plan "):].strip()
            if not goal:
                print("Usage: media-thumbnail-review-plan <goal>")
                return
            self.media_thumbnail_review_plan(goal)
            return

        if normalized.startswith("media-video-plan "):
            goal = command[len("media-video-plan "):].strip()
            if not goal:
                print("Usage: media-video-plan <goal>")
                return
            self.media_video_plan(goal)
            return

        if normalized == "media-context":
            self.media_context()
            return

        if normalized == "blender-bridge-status":
            self.blender_bridge_status()
            return

        if normalized.startswith("blender-scene-plan "):
            goal = command[len("blender-scene-plan "):].strip()
            if not goal:
                print("Usage: blender-scene-plan <goal>")
                return
            self.blender_scene_plan(goal)
            return

        if normalized.startswith("blender-asset-plan "):
            goal = command[len("blender-asset-plan "):].strip()
            if not goal:
                print("Usage: blender-asset-plan <goal>")
                return
            self.blender_asset_plan(goal)
            return

        if normalized.startswith("blender-texture-plan "):
            goal = command[len("blender-texture-plan "):].strip()
            if not goal:
                print("Usage: blender-texture-plan <goal>")
                return
            self.blender_texture_plan(goal)
            return

        if normalized.startswith("blender-rigging-plan "):
            goal = command[len("blender-rigging-plan "):].strip()
            if not goal:
                print("Usage: blender-rigging-plan <goal>")
                return
            self.blender_rigging_plan(goal)
            return

        if normalized.startswith("blender-animation-plan "):
            goal = command[len("blender-animation-plan "):].strip()
            if not goal:
                print("Usage: blender-animation-plan <goal>")
                return
            self.blender_animation_plan(goal)
            return

        if normalized == "blender-context":
            self.blender_context()
            return

        if normalized == "workspace-awareness-status":
            self.workspace_awareness_status()
            return

        if normalized == "workspace-map":
            self.workspace_map()
            return

        if normalized == "workspace-context":
            self.workspace_context()
            return

        if normalized == "workspace-current-state":
            self.workspace_current_state()
            return

        if normalized == "workspace-important-files":
            self.workspace_important_files()
            return

        if normalized == "partner-alpha-status":
            self.partner_alpha_status()
            return

        if normalized == "partner-context":
            self.partner_context()
            return

        if normalized == "partner-readiness":
            self.partner_readiness()
            return

        if normalized == "partner-next-step":
            self.partner_next_step()
            return

        if normalized in {"awakening-status", "awaken"}:
            self.awakening_status()
            return

        if normalized == "voice-runtime-alpha-status":
            self.voice_runtime_alpha_status()
            return

        if normalized.startswith("voice-speak-plan "):
            value = command[len("voice-speak-plan "):].strip()
            if not value:
                print("Usage: voice-speak-plan <text>")
                return
            self.voice_speak_plan(text=value)
            return

        if normalized == "voice-speak-plan":
            print("Usage: voice-speak-plan <text>")
            return

        if normalized.startswith("voice-speak-test "):
            value = command[len("voice-speak-test "):].strip()
            if not value:
                print("Usage: voice-speak-test <text>")
                return
            self.voice_speak_test(text=value)
            return

        if normalized == "voice-speak-test":
            print("Usage: voice-speak-test <text>")
            return

        if normalized == "voice-runtime-context":
            self.voice_runtime_context()
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

        if normalized == "project-code-status":
            self.project_code_status()
            return

        if normalized == "project-code-map":
            self.project_code_map()
            return

        if normalized.startswith("project-code-map "):
            value = command[len("project-code-map "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: project-code-map <limit>")
                return
            self.project_code_map(limit=limit)
            return

        if normalized.startswith("project-code-inspect "):
            relative_path = command[len("project-code-inspect "):].strip()
            if not relative_path:
                print("Usage: project-code-inspect <path>")
                return
            self.project_code_inspect(relative_path=relative_path)
            return

        if normalized.startswith("project-code-plan "):
            request = command[len("project-code-plan "):].strip()
            if not request:
                print("Usage: project-code-plan <request>")
                return
            self.project_code_plan(request=request)
            return

        if normalized.startswith("project-code-safety "):
            command_text = command[len("project-code-safety "):].strip()
            if not command_text:
                print("Usage: project-code-safety <command>")
                return
            self.project_code_safety(command=command_text)
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

    def project_code_map(self, limit: int = 20) -> None:
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
            for item in summary["functions"][:40]:
                print(f"- {item}")

        if summary["methods"]:
            print()
            print("Methods")
            print("-------")
            for item in summary["methods"][:50]:
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
        print(f"Status          : {result['status']}")
        print(f"Insight Count   : {result['insight_count']}")
        print(f"Write Performed : {result['write_performed']}")
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
        print(f"Status           : {context['status']}")
        print(f"Context Ready    : {context['context_ready']}")
        print(f"Memory Count     : {context['memory_count']}")
        print(f"Journal Count    : {context['journal_count']}")
        print(f"Milestones       : {len(context['milestones'])}")
        print(f"Memory Highlights: {len(context['memory_highlights'])}")
        print(f"Write Performed  : {context['write_performed']}")
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

        print("Latest Milestone")
        print("----------------")
        latest = briefing["latest_milestone"]
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

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
        print(f"Title             : {briefing['title']}")
        print(f"Status            : {briefing['status']}")
        print(f"Version           : {briefing['version']}")
        print(f"Write Performed   : {briefing['write_performed']}")
        print(f"Command Execution : {briefing['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
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

    def daily_briefing_context(self, limit: int = 5) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        context = manager.context(limit=limit)

        print("AURA Daily Project Briefing Context")
        print("===================================")
        print(f"Status           : {context['status']}")
        print(f"Context Ready    : {context['context_ready']}")
        print(f"Write Performed  : {context['write_performed']}")
        print(f"Command Execution: {context['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(context["project_summary"])
        print()
        print("Recent Milestones")
        print("-----------------")
        for item in context["recent_milestones"]:
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
        print(f"Status               : {plan['status']}")
        print(f"Text                 : {plan['text']}")
        print(f"Text Length          : {plan['text_length']}")
        print(f"Command Available    : {plan['command_available']}")
        print(f"TTS Backend          : {plan['tts_backend']['name'] or '-'}")
        print(f"TTS Backend Found    : {plan['tts_backend']['found']}")
        print(f"Proposed Command     : {plan['proposed_command'] or '-'}")
        print(f"Command Reason       : {plan['command_reason']}")
        print(f"Speaker Output       : {plan['speaker_output']}")
        print(f"Microphone Access    : {plan['microphone_access']}")
        print(f"Command Execution    : {plan['command_execution_performed']}")
        print(f"Playback Performed   : {plan['playback_performed']}")
        print(f"File Write Performed : {plan['file_write_performed']}")
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
        print(f"Render Backend Found         : {status['render_backend_found']}")
        print(f"Render Backend               : {status['render_backend'] or '-'}")
        print(f"Media Backend Found          : {status['media_backend_found']}")
        print(f"Media Backend                : {status['media_backend'] or '-'}")
        print(f"Render Performed             : {status['render_performed']}")
        print(f"Expression Changed           : {status['expression_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"External App Opened          : {status['external_app_opened']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Image File Write             : {status['image_file_write']}")
        print(f"Animation File Write         : {status['animation_file_write']}")
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
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def blender_scene_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Scene Plan", manager.scene_plan(goal))

    def blender_asset_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Asset Plan", manager.asset_plan(goal))

    def blender_texture_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Texture/Material Plan", manager.texture_plan(goal))

    def blender_rigging_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Rigging Plan", manager.rigging_plan(goal))

    def blender_animation_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Animation Plan", manager.animation_plan(goal))

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
        print(f"Note: {context['note']}")


    def media_understanding_status(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Media Understanding Foundation Status")
        print("==========================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Understanding Ready          : {status['understanding_ready']}")
        print(f"Asset Summary Ready          : {status['asset_summary_ready']}")
        print(f"Image Plan Ready             : {status['image_plan_ready']}")
        print(f"Texture Reference Ready      : {status['texture_reference_ready']}")
        print(f"Thumbnail Review Ready       : {status['thumbnail_review_ready']}")
        print(f"Video Plan Ready             : {status['video_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Metadata Inspection Ready    : {status['metadata_inspection_ready']}")
        print(f"Candidate Count              : {status['candidate_count']}")
        print(f"Image Count                  : {status['image_count']}")
        print(f"Texture Reference Count      : {status['texture_reference_count']}")
        print(f"Video Count                  : {status['video_count']}")
        print(f"Audio Count                  : {status['audio_count']}")
        print(f"3D Count                     : {status['three_d_count']}")
        print(f"Design Source Count          : {status['design_source_count']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Metadata Only                : {status['metadata_only']}")
        print(f"Media File Opened            : {status['media_file_opened']}")
        print(f"Media Pixel Read             : {status['media_pixel_read']}")
        print(f"Image Pixel Read             : {status['image_pixel_read']}")
        print(f"Video Frame Read             : {status['video_frame_read']}")
        print(f"Audio Stream Read            : {status['audio_stream_read']}")
        print(f"Thumbnail Generated          : {status['thumbnail_generated']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def media_asset_summary(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        summary = manager.asset_summary()

        print("AURA Media Asset Summary")
        print("========================")
        print(f"Status                       : {summary['status']}")
        print(f"Asset Summary Ready          : {summary['asset_summary_ready']}")
        print(f"Candidate Count              : {summary['candidate_count']}")
        print(f"Image Count                  : {summary['image_count']}")
        print(f"Texture Reference Count      : {summary['texture_reference_count']}")
        print(f"Video Count                  : {summary['video_count']}")
        print(f"Audio Count                  : {summary['audio_count']}")
        print(f"3D Count                     : {summary['three_d_count']}")
        print(f"Design Source Count          : {summary['design_source_count']}")
        print(f"Metadata Only                : {summary['metadata_only']}")
        print(f"File Opened                  : {summary['file_opened']}")
        print(f"Pixel Read                   : {summary['pixel_read']}")
        print(f"File Write Performed         : {summary['file_write_performed']}")
        print(f"Command Execution Performed  : {summary['command_execution_performed']}")
        print()
        print("By Category")
        print("-----------")
        if summary["by_category"]:
            for key, value in sorted(summary["by_category"].items()):
                print(f"- {key}: {value}")
        else:
            print("- none")
        print()
        print("Assets")
        print("------")
        if summary["assets"]:
            for item in summary["assets"]:
                print(f"- {item['path']} [{item['category']}, {item['suffix']}, {item['size_bytes']} bytes]")
        else:
            print("- no visible media assets found in safe project files")
        print()
        print(f"Note: {summary['note']}")

    def print_media_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Metadata Only                : {plan['metadata_only']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Media File Opened            : {plan['media_file_opened']}")
        print(f"Pixel Read                   : {plan['pixel_read']}")
        print(f"Image Pixel Read             : {plan['image_pixel_read']}")
        print(f"Video Frame Read             : {plan['video_frame_read']}")
        print(f"Audio Stream Read            : {plan['audio_stream_read']}")
        print(f"Thumbnail Generated          : {plan['thumbnail_generated']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Blender Context Ready        : {plan['blender_context_ready']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Asset Summary")
        print("-------------")
        summary = plan["asset_summary"]
        print(f"Candidate Count: {summary['candidate_count']}")
        print(f"Images         : {summary['image_count']}")
        print(f"Videos         : {summary['video_count']}")
        print(f"Audio          : {summary['audio_count']}")
        print(f"3D Assets      : {summary['three_d_count']}")
        print(f"Metadata Only  : {summary['metadata_only']}")
        print(f"File Opened    : {summary['file_opened']}")
        print(f"Pixel Read     : {summary['pixel_read']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def media_image_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Image Description Plan", manager.image_description_plan(goal))

    def media_texture_reference_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Texture Reference Plan", manager.texture_reference_plan(goal))

    def media_thumbnail_review_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Thumbnail/Banner Review Plan", manager.thumbnail_review_plan(goal))

    def media_video_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Video/Audio Plan", manager.video_plan(goal))

    def media_context(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Media Understanding Context")
        print("================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Metadata Only                : {context['metadata_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Media File Opened            : {context['media_file_opened']}")
        print(f"Pixel Read                   : {context['pixel_read']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Media Status")
        print("------------")
        status = context["media_status"]
        print(f"Understanding Ready : {status['understanding_ready']}")
        print(f"Candidate Count     : {status['candidate_count']}")
        print(f"Image Count         : {status['image_count']}")
        print(f"Video Count         : {status['video_count']}")
        print(f"Audio Count         : {status['audio_count']}")
        print(f"3D Count            : {status['three_d_count']}")
        print(f"Runtime Ready       : {status['runtime_ready']}")
        print(f"File Write          : {status['file_write']}")
        print(f"Command Execution   : {status['command_execution']}")
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
        summary = context["asset_summary"]
        print(f"Candidate Count: {summary['candidate_count']}")
        print(f"Metadata Only  : {summary['metadata_only']}")
        print(f"File Opened    : {summary['file_opened']}")
        print(f"Pixel Read     : {summary['pixel_read']}")
        print(f"File Write     : {summary['file_write_performed']}")
        print(f"Command Exec   : {summary['command_execution_performed']}")
        print()
        print(f"Note: {context['note']}")


    def expression_language_status(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Expression Language Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Language Ready               : {status['language_ready']}")
        print(f"State Ready                  : {status['state_ready']}")
        print(f"Plan Ready                   : {status['plan_ready']}")
        print(f"Voice Hint Ready             : {status['voice_hint_ready']}")
        print(f"Avatar Hint Ready            : {status['avatar_hint_ready']}")
        print(f"Gesture Hint Ready           : {status['gesture_hint_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Mood States                  : {status['mood_states']}")
        print(f"Emotion Tags                 : {status['emotion_tags']}")
        print(f"Voice Tones                  : {status['voice_tones']}")
        print(f"Avatar Expressions           : {status['avatar_expressions']}")
        print(f"Gestures                     : {status['gestures']}")
        print(f"Response Styles              : {status['response_styles']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def expression_state(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        state = manager.expression_state()

        print("AURA Expression State")
        print("=====================")
        print(f"Status                       : {state['status']}")
        print(f"State Ready                  : {state['state_ready']}")
        print(f"AURA Name                    : {state['aura_name']}")
        print(f"AURA Version                 : {state['aura_version']}")
        print(f"Codename                     : {state['codename']}")
        print(f"Creator                      : {state['creator']}")
        print(f"Base Mood                    : {state['base_mood']}")
        print(f"Base Emotion Tags            : {', '.join(state['base_emotion_tags'])}")
        print(f"Default Voice Tone           : {state['default_voice_tone']}")
        print(f"Default Avatar Expression    : {state['default_avatar_expression']}")
        print(f"Default Gesture              : {state['default_gesture']}")
        print()
        print("Supported Moods")
        print("---------------")
        for item in state["supported_moods"]:
            print(f"- {item}")
        print()
        print("Supported Voice Tones")
        print("---------------------")
        for item in state["supported_voice_tones"]:
            print(f"- {item}")
        print()
        print("Supported Avatar Expressions")
        print("----------------------------")
        for item in state["supported_avatar_expressions"]:
            print(f"- {item}")
        print()
        print("Supported Gestures")
        print("------------------")
        for item in state["supported_gestures"]:
            print(f"- {item}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {state['read_only']}")
        print(f"Write Performed              : {state['write_performed']}")
        print(f"Avatar Changed               : {state['avatar_changed']}")
        print(f"Voice Output Performed       : {state['voice_output_performed']}")
        print(f"Command Execution Performed  : {state['command_execution_performed']}")
        print()
        print(f"Note: {state['note']}")

    def print_expression_hint(self, title: str, hint: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {hint['status']}")
        print(f"Hint Type                    : {hint['hint_type']}")
        print(f"Target                       : {hint['target']}")
        print(f"Hint State                   : {hint['hint_state']}")
        print(f"Mood                         : {hint['mood']}")
        print(f"Emotion Tags                 : {', '.join(hint['emotion_tags'])}")
        print(f"Voice Tone Hint              : {hint['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {hint['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {hint['gesture_hint']}")
        print(f"Response Style Hint          : {hint['response_style_hint']}")
        print(f"Execution Ready              : {hint['execution_ready']}")
        print(f"Executed                     : {hint['executed']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Avatar Changed               : {hint['avatar_changed']}")
        print(f"Gesture Changed              : {hint['gesture_changed']}")
        print(f"Voice Output Performed       : {hint['voice_output_performed']}")
        print(f"File Write Performed         : {hint['file_write_performed']}")
        print(f"Command Execution Performed  : {hint['command_execution_performed']}")
        print(f"External Action Performed    : {hint['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in hint["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in hint["safety_notes"]:
            print(f"- {note}")

    def expression_plan(self, text: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        plan = manager.expression_plan(text)

        print("AURA Expression Plan")
        print("====================")
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Text                         : {plan['text']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Mood                         : {plan['mood']}")
        print(f"Emotion Tags                 : {', '.join(plan['emotion_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Voice Runtime Alpha Ready    : {plan['voice_runtime_alpha_ready']}")
        print(f"Avatar Runtime Alpha Ready   : {plan['avatar_runtime_alpha_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"Gesture Changed              : {plan['gesture_changed']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Speaker Output               : {plan['speaker_output']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def expression_voice_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Voice Hint", manager.voice_hint(target))

    def expression_avatar_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Avatar Hint", manager.avatar_hint(target))

    def expression_gesture_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Gesture Hint", manager.gesture_hint(target))

    def expression_context(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Expression Language Context")
        print("================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"Gesture Changed              : {context['gesture_changed']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Expression Status")
        print("-----------------")
        status = context["expression_status"]
        print(f"Language Ready      : {status['language_ready']}")
        print(f"State Ready         : {status['state_ready']}")
        print(f"Plan Ready          : {status['plan_ready']}")
        print(f"Voice Hint Ready    : {status['voice_hint_ready']}")
        print(f"Avatar Hint Ready   : {status['avatar_hint_ready']}")
        print(f"Gesture Hint Ready  : {status['gesture_hint_ready']}")
        print(f"Context Ready       : {status['context_ready']}")
        print(f"Runtime Ready       : {status['runtime_ready']}")
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


    def game_companion_status(self) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Game Companion Foundation Status")
        print("=====================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Companion Ready              : {status['companion_ready']}")
        print(f"Session Plan Ready           : {status['session_plan_ready']}")
        print(f"Strategy Plan Ready          : {status['strategy_plan_ready']}")
        print(f"Streaming Plan Ready         : {status['streaming_plan_ready']}")
        print(f"Coaching Plan Ready          : {status['coaching_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Expression Integration Ready : {status['expression_integration_ready']}")
        print(f"Vision Integration Ready     : {status['vision_integration_ready']}")
        print(f"Desktop Integration Ready    : {status['desktop_integration_ready']}")
        print(f"Media Integration Ready      : {status['media_integration_ready']}")
        print(f"Partner Integration Ready    : {status['partner_integration_ready']}")
        print(f"Supported Styles             : {status['supported_styles']}")
        print(f"Support Modes                : {status['support_modes']}")
        print(f"Safety Boundaries            : {status['safety_boundaries']}")
        print(f"Gaming Mode                  : {status['gaming_mode']}")
        print(f"Streaming Mode               : {status['streaming_mode']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Game Screen Read             : {status['game_screen_read']}")
        print(f"Screen Capture               : {status['screen_capture']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Game Input Control           : {status['game_input_control']}")
        print(f"Keyboard Input               : {status['keyboard_input']}")
        print(f"Mouse Control                : {status['mouse_control']}")
        print(f"Game App Opened              : {status['game_app_opened']}")
        print(f"Desktop Action Execution     : {status['desktop_action_execution']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_game_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Game Style                   : {plan['game_style']}")
        print(f"Game Tags                    : {', '.join(plan['game_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Desktop Context Ready        : {plan['desktop_context_ready']}")
        print(f"Media Context Ready          : {plan['media_context_ready']}")
        print(f"Partner Context Ready        : {plan['partner_context_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Game Context")
        print("------------")
        context = plan["game_context"]
        print(f"Style               : {context['style']}")
        print(f"Tags                : {', '.join(context['tags'])}")
        print(f"Streaming Related   : {context['streaming_related']}")
        print(f"Competitive Related : {context['competitive_related']}")
        print(f"Strategy Related    : {context['strategy_related']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Game Screen Read             : {plan['game_screen_read']}")
        print(f"Screen Capture Performed     : {plan['screen_capture_performed']}")
        print(f"Camera Access Performed      : {plan['camera_access_performed']}")
        print(f"Keyboard Input Performed     : {plan['keyboard_input_performed']}")
        print(f"Mouse Control Performed      : {plan['mouse_control_performed']}")
        print(f"Game Input Control           : {plan['game_input_control']}")
        print(f"Game App Opened              : {plan['game_app_opened']}")
        print(f"Desktop Action Performed     : {plan['desktop_action_performed']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def game_session_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Session Plan", manager.session_plan(target))

    def game_strategy_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Strategy Plan", manager.strategy_plan(target))

    def game_streaming_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Streaming Plan", manager.streaming_plan(target))

    def game_coaching_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Coaching Plan", manager.coaching_plan(target))

    def game_context(self) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Game Companion Context")
        print("===========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Game Screen Read             : {context['game_screen_read']}")
        print(f"Game Input Control           : {context['game_input_control']}")
        print(f"Game App Opened              : {context['game_app_opened']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Game Status")
        print("-----------")
        status = context["game_status"]
        print(f"Companion Ready      : {status['companion_ready']}")
        print(f"Session Plan Ready   : {status['session_plan_ready']}")
        print(f"Strategy Plan Ready  : {status['strategy_plan_ready']}")
        print(f"Streaming Plan Ready : {status['streaming_plan_ready']}")
        print(f"Coaching Plan Ready  : {status['coaching_plan_ready']}")
        print(f"Context Ready        : {status['context_ready']}")
        print(f"Runtime Ready        : {status['runtime_ready']}")
        print()
        print("Integrations")
        print("------------")
        print(f"Expression : {status['expression_integration_ready']}")
        print(f"Vision     : {status['vision_integration_ready']}")
        print(f"Desktop    : {status['desktop_integration_ready']}")
        print(f"Media      : {status['media_integration_ready']}")
        print(f"Partner    : {status['partner_integration_ready']}")
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


    def streaming_safety_status(self) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Streaming Safety Foundation Status")
        print("=======================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Safety Ready                 : {status['safety_ready']}")
        print(f"Context Plan Ready           : {status['context_plan_ready']}")
        print(f"Chat Safety Ready            : {status['chat_safety_ready']}")
        print(f"Content Boundary Ready       : {status['content_boundary_ready']}")
        print(f"Privacy Plan Ready           : {status['privacy_plan_ready']}")
        print(f"Moderation Plan Ready        : {status['moderation_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Game Integration Ready       : {status['game_integration_ready']}")
        print(f"Expression Integration Ready : {status['expression_integration_ready']}")
        print(f"Media Integration Ready      : {status['media_integration_ready']}")
        print(f"Vision Integration Ready     : {status['vision_integration_ready']}")
        print(f"Desktop Integration Ready    : {status['desktop_integration_ready']}")
        print(f"Safety Categories            : {status['safety_categories']}")
        print(f"Stream Modes                 : {status['stream_modes']}")
        print(f"Disabled Runtime Actions     : {status['disabled_runtime_actions']}")
        print(f"Streaming Mode               : {status['streaming_mode']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Live Chat Read               : {status['live_chat_read']}")
        print(f"Message Sent                 : {status['message_sent']}")
        print(f"Moderation Action            : {status['moderation_action']}")
        print(f"Screen Capture               : {status['screen_capture']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Browser Opened               : {status['browser_opened']}")
        print(f"App Opened                   : {status['app_opened']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_streaming_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Stream Priority              : {plan['stream_priority']}")
        print(f"Stream Tags                  : {', '.join(plan['stream_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Game Context Ready           : {plan['game_context_ready']}")
        print(f"Expression Context Ready     : {plan['expression_context_ready']}")
        print(f"Media Context Ready          : {plan['media_context_ready']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Desktop Context Ready        : {plan['desktop_context_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Stream Context")
        print("--------------")
        context = plan["stream_context"]
        print(f"Priority        : {context['priority']}")
        print(f"Tags            : {', '.join(context['tags'])}")
        print(f"Chat Related    : {context['chat_related']}")
        print(f"Privacy Related : {context['privacy_related']}")
        print(f"Game Related    : {context['game_related']}")
        print(f"Avatar Related  : {context['avatar_related']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Live Chat Read               : {plan['live_chat_read']}")
        print(f"Chat Message Sent            : {plan['chat_message_sent']}")
        print(f"Moderation Action Performed  : {plan['moderation_action_performed']}")
        print(f"Screen Capture Performed     : {plan['screen_capture_performed']}")
        print(f"Camera Access Performed      : {plan['camera_access_performed']}")
        print(f"Browser Opened               : {plan['browser_opened']}")
        print(f"App Opened                   : {plan['app_opened']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def streaming_context_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Context Plan", manager.context_plan(target))

    def streaming_chat_safety_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Chat Safety Plan", manager.chat_safety_plan(target))

    def streaming_content_boundary_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Content Boundary Plan", manager.content_boundary_plan(target))

    def streaming_privacy_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Privacy Plan", manager.privacy_plan(target))

    def streaming_moderation_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Moderation Plan", manager.moderation_plan(target))

    def streaming_safety_context(self) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Streaming Safety Context")
        print("=============================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Live Chat Read               : {context['live_chat_read']}")
        print(f"Message Sent                 : {context['message_sent']}")
        print(f"Moderation Action            : {context['moderation_action']}")
        print(f"Screen Capture               : {context['screen_capture']}")
        print(f"Camera Access                : {context['camera_access']}")
        print(f"Browser Opened               : {context['browser_opened']}")
        print(f"App Opened                   : {context['app_opened']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Streaming Status")
        print("----------------")
        status = context["streaming_status"]
        print(f"Safety Ready           : {status['safety_ready']}")
        print(f"Context Plan Ready     : {status['context_plan_ready']}")
        print(f"Chat Safety Ready      : {status['chat_safety_ready']}")
        print(f"Content Boundary Ready : {status['content_boundary_ready']}")
        print(f"Privacy Plan Ready     : {status['privacy_plan_ready']}")
        print(f"Moderation Plan Ready  : {status['moderation_plan_ready']}")
        print(f"Context Ready          : {status['context_ready']}")
        print(f"Runtime Ready          : {status['runtime_ready']}")
        print()
        print("Integrations")
        print("------------")
        print(f"Game       : {status['game_integration_ready']}")
        print(f"Expression : {status['expression_integration_ready']}")
        print(f"Media      : {status['media_integration_ready']}")
        print(f"Vision     : {status['vision_integration_ready']}")
        print(f"Desktop    : {status['desktop_integration_ready']}")
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


    def workspace_memory_link_status(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Workspace Memory Link Status")
        print("=================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Link Ready                   : {status['link_ready']}")
        print(f"Summary Ready                : {status['summary_ready']}")
        print(f"Memory Candidates Ready      : {status['memory_candidates_ready']}")
        print(f"File Memory Candidates Ready : {status['file_memory_candidates_ready']}")
        print(f"Milestone Candidates Ready   : {status['milestone_candidates_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Workspace Integration Ready  : {status['workspace_integration_ready']}")
        print(f"Memory Store Ready           : {status['memory_store_ready']}")
        print(f"Journal Integration Ready    : {status['journal_integration_ready']}")
        print(f"Reflection Integration Ready : {status['reflection_integration_ready']}")
        print(f"Memory Count                 : {status['memory_count']}")
        print(f"Journal Count                : {status['journal_count']}")
        print(f"Milestone Count              : {status['milestone_count']}")
        print(f"Important File Count         : {status['important_file_count']}")
        print(f"Candidate Types              : {status['candidate_types']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Candidate Only               : {status['candidate_only']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Memory Delete                : {status['memory_delete']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def workspace_memory_summary(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        summary = manager.summary()

        print("AURA Workspace Memory Summary")
        print("=============================")
        print(f"Status                       : {summary['status']}")
        print(f"Summary Ready                : {summary['summary_ready']}")
        print(f"Memory Count                 : {summary['memory_count']}")
        print(f"Journal Count                : {summary['journal_count']}")
        print(f"Milestone Count              : {summary['milestone_count']}")
        print(f"Read Only                    : {summary['read_only']}")
        print(f"Write Performed              : {summary['write_performed']}")
        print(f"Memory Write Performed       : {summary['memory_write_performed']}")
        print(f"Memory Delete Performed      : {summary['memory_delete_performed']}")
        print(f"Journal Write Performed      : {summary['journal_write_performed']}")
        print(f"File Write Performed         : {summary['file_write_performed']}")
        print(f"Command Execution Performed  : {summary['command_execution_performed']}")
        print(f"External Action Performed    : {summary['external_action_execution_performed']}")
        print()
        print("Summary")
        print("-------")
        print(summary["summary"])
        print()
        print("Workspace Summary")
        print("-----------------")
        print(summary["workspace_summary"])
        latest = summary.get("latest_milestone")
        if latest:
            print()
            print("Latest Milestone")
            print("----------------")
            print(f"Title      : {latest['title']}")
            print(f"Created At : {latest['created_at']}")
        print()
        print(f"Note: {summary['note']}")

    def print_workspace_memory_candidates(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Candidate Count              : {plan['candidate_count']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Read Only                    : {plan['read_only']}")
        print(f"Memory Write Performed       : {plan['memory_write_performed']}")
        print(f"Memory Delete Performed      : {plan['memory_delete_performed']}")
        print(f"Journal Write Performed      : {plan['journal_write_performed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Candidates")
        print("----------")
        for index, candidate in enumerate(plan["candidates"], start=1):
            metadata = candidate["metadata"]
            print(f"{index}. Type       : {candidate['candidate_type']}")
            print(f"   Kind       : {candidate['kind']}")
            print(f"   Importance : {metadata['suggested_importance']}")
            print(f"   Pinned     : {metadata['suggested_pinned']}")
            print(f"   Write Ready: {candidate['write_ready']}")
            print(f"   Written    : {candidate['written']}")
            print(f"   Reason     : {candidate['reason']}")
            print(f"   Content    : {candidate['content']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def workspace_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace Memory Candidates",
            manager.project_memory_candidates(target),
        )

    def workspace_file_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace File Memory Candidates",
            manager.file_memory_candidates(target),
        )

    def workspace_milestone_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace Milestone Memory Candidates",
            manager.milestone_memory_candidates(target),
        )

    def workspace_memory_link_context(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Workspace Memory Link Context")
        print("==================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Memory Delete Performed      : {context['memory_delete_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Link Status")
        print("-----------")
        status = context["link_status"]
        print(f"Link Ready              : {status['link_ready']}")
        print(f"Summary Ready           : {status['summary_ready']}")
        print(f"Memory Candidates Ready : {status['memory_candidates_ready']}")
        print(f"File Candidates Ready   : {status['file_memory_candidates_ready']}")
        print(f"Milestone Ready         : {status['milestone_candidates_ready']}")
        print(f"Context Ready           : {status['context_ready']}")
        print(f"Candidate Only          : {status['candidate_only']}")
        print(f"Runtime Ready           : {status['runtime_ready']}")
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


    def project_intent_status(self) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Project Intent Planner Status")
        print("==================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Intent Ready                          : {status['intent_ready']}")
        print(f"Summary Ready                         : {status['summary_ready']}")
        print(f"Goal Plan Ready                       : {status['goal_plan_ready']}")
        print(f"Sprint Intent Plan Ready              : {status['sprint_intent_plan_ready']}")
        print(f"Next Action Candidates Ready          : {status['next_action_candidates_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Workspace Awareness Integration       : {status['workspace_awareness_integration_ready']}")
        print(f"Project Coding Integration            : {status['project_coding_integration_ready']}")
        print(f"Daily Briefing Integration            : {status['daily_briefing_integration_ready']}")
        print(f"Memory Reflection Integration         : {status['memory_reflection_integration_ready']}")
        print(f"Intent Categories                     : {status['intent_categories']}")
        print(f"Project Python Files                  : {status['project_python_files']}")
        print(f"Memory Count                          : {status['memory_count']}")
        print(f"Journal Count                         : {status['journal_count']}")
        print(f"Milestone Count                       : {status['milestone_count']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"Memory Write                          : {status['memory_write']}")
        print(f"Journal Write                         : {status['journal_write']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def project_intent_summary(self, topic: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        summary = manager.summary(topic)

        print("AURA Project Intent Summary")
        print("===========================")
        print(f"Status                                : {summary['status']}")
        print(f"Summary Ready                         : {summary['summary_ready']}")
        print(f"Topic                                 : {summary['topic']}")
        print(f"Read Only                             : {summary['read_only']}")
        print(f"Write Performed                       : {summary['write_performed']}")
        print(f"File Write Performed                  : {summary['file_write_performed']}")
        print(f"Memory Write Performed                : {summary['memory_write_performed']}")
        print(f"Journal Write Performed               : {summary['journal_write_performed']}")
        print(f"Command Execution Performed           : {summary['command_execution_performed']}")
        print(f"External Action Performed             : {summary['external_action_execution_performed']}")
        print()
        print("Intent")
        print("------")
        intent = summary["intent"]
        print(f"Priority       : {intent['priority']}")
        print(f"Tags           : {', '.join(intent['tags'])}")
        print(f"Safety Related : {intent['safety_related']}")
        print(f"Sprint Related : {intent['sprint_related']}")
        print(f"Implementation : {intent['implementation_related']}")
        print(f"Memory Related : {intent['memory_related']}")
        print()
        print("Summary")
        print("-------")
        print(summary["summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(summary["workspace_memory_summary"])
        print()
        print("Daily Project Summary")
        print("---------------------")
        print(summary["daily_project_summary"])
        print()
        print("Top Insights")
        print("------------")
        for item in summary["top_insights"]:
            print(f"- {item}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in summary["recommended_next_steps"]:
            print(f"- {item}")
        print()
        print(f"Note: {summary['note']}")

    def print_project_intent_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Intent Priority                       : {plan['intent_priority']}")
        print(f"Intent Tags                           : {', '.join(plan['intent_tags'])}")
        print(f"Project Coding Route                  : {plan['project_coding_route']}")
        print(f"Project Python Files                  : {plan['project_python_files']}")
        print(f"Action Candidate Count                : {plan['action_candidate_count']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"Memory Write Performed                : {plan['memory_write_performed']}")
        print(f"Journal Write Performed               : {plan['journal_write_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print()
        print("Intent")
        print("------")
        intent = plan["intent"]
        print(f"Priority                 : {intent['priority']}")
        print(f"Tags                     : {', '.join(intent['tags'])}")
        print(f"Safety Related           : {intent['safety_related']}")
        print(f"Sprint Related           : {intent['sprint_related']}")
        print(f"Implementation Related   : {intent['implementation_related']}")
        print(f"Memory Related           : {intent['memory_related']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Daily Project Summary")
        print("---------------------")
        print(plan["daily_project_summary"])
        print()
        print("Patch Plan")
        print("----------")
        patch_plan = plan["patch_plan"]
        print(f"Mode                     : {patch_plan['mode']}")
        print(f"File Write Performed     : {patch_plan['file_write_performed']}")
        print(f"Command Execution        : {patch_plan['command_execution_performed']}")
        print(f"Coding Route             : {patch_plan['coding_route']}")
        print("Related Files:")
        for file in patch_plan["related_files"]:
            print(f"- {file}")
        print()
        print("Action Candidates")
        print("-----------------")
        for index, candidate in enumerate(plan["action_candidates"], start=1):
            print(f"{index}. {candidate['name']}")
            print(f"   Importance : {candidate['importance']}")
            print(f"   Candidate  : {candidate['candidate_only']}")
            print(f"   Executed   : {candidate['executed']}")
            print(f"   Reason     : {candidate['reason']}")
            print(f"   Detail     : {candidate['description']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def project_goal_plan(self, goal: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Project Goal Plan",
            manager.goal_plan(goal),
        )

    def sprint_intent_plan(self, goal: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Sprint Intent Plan",
            manager.sprint_intent_plan(goal),
        )

    def project_next_action_candidates(self, topic: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Project Next Action Candidates",
            manager.next_action_candidates(topic),
        )

    def project_intent_context(self) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Project Intent Context")
        print("===========================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"Memory Write Performed                : {context['memory_write_performed']}")
        print(f"Journal Write Performed               : {context['journal_write_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print()
        print("Planner Status")
        print("--------------")
        status = context["planner_status"]
        print(f"Intent Ready                 : {status['intent_ready']}")
        print(f"Summary Ready                : {status['summary_ready']}")
        print(f"Goal Plan Ready              : {status['goal_plan_ready']}")
        print(f"Sprint Intent Plan Ready     : {status['sprint_intent_plan_ready']}")
        print(f"Next Action Candidates Ready : {status['next_action_candidates_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Proposal Only                : {status['proposal_only']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print()
        print("Project Coding Status")
        print("---------------------")
        coding = context["project_coding_status"]
        print(f"Status              : {coding['status']}")
        print(f"Analysis Ready      : {coding['analysis_ready']}")
        print(f"Patch Planning Ready: {coding['patch_planning_ready']}")
        print(f"Python Files        : {coding['python_files']}")
        print(f"Coding Route        : {coding['coding_route']}")
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


    def creative_assistant_status(self) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Creative Assistant Foundation Status")
        print("========================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Assistant Ready                       : {status['assistant_ready']}")
        print(f"Brief Plan Ready                      : {status['brief_plan_ready']}")
        print(f"Character Concept Ready               : {status['character_concept_ready']}")
        print(f"Visual Asset Plan Ready               : {status['visual_asset_plan_ready']}")
        print(f"Content Idea Plan Ready               : {status['content_idea_plan_ready']}")
        print(f"Review Plan Ready                     : {status['review_plan_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Project Intent Integration            : {status['project_intent_integration_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Media Understanding Integration       : {status['media_understanding_integration_ready']}")
        print(f"Expression Language Integration       : {status['expression_language_integration_ready']}")
        print(f"Blender Bridge Integration            : {status['blender_bridge_integration_ready']}")
        print(f"Creative Plan Types                   : {status['creative_plan_types']}")
        print(f"Media Candidate Count                 : {status['media_candidate_count']}")
        print(f"Blender Asset Candidate Count         : {status['blender_asset_candidate_count']}")
        print(f"Expression Mood States                : {status['expression_mood_states']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"Image Generation                      : {status['image_generation']}")
        print(f"Media File Opened                     : {status['media_file_opened']}")
        print(f"Pixel Read                            : {status['pixel_read']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_creative_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Creative Focus                        : {plan['creative_direction']['focus']}")
        print(f"Creative Tags                         : {', '.join(plan['creative_direction']['tags'])}")
        print(f"Brand Anchor                          : {plan['creative_direction']['brand_anchor']}")
        print(f"Safety Priority                       : {plan['creative_direction']['safety_priority']}")
        print(f"Creative Output Count                 : {plan['creative_output_count']}")
        print(f"Media Candidate Count                 : {plan['media_candidate_count']}")
        print(f"Media Metadata Only                   : {plan['media_metadata_only']}")
        print(f"Expression Mood                       : {plan['expression_mood']}")
        print(f"Expression Tags                       : {', '.join(plan['expression_tags'])}")
        print(f"Blender Asset Candidate Count         : {plan['blender_asset_candidate_count']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"Proposal Only                         : {plan['proposal_only']}")
        print(f"Image Generation Performed            : {plan['image_generation_performed']}")
        print(f"Media File Opened                     : {plan['media_file_opened']}")
        print(f"Pixel Read                            : {plan['pixel_read']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print()
        print("Creative Outputs")
        print("----------------")
        for item in plan["creative_outputs"]:
            print(f"- {item}")
        print()
        print("Project Intent Summary")
        print("----------------------")
        print(plan["project_intent_summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Expression Plan")
        print("---------------")
        expression = plan["expression_plan"]
        print(f"Mood              : {expression['mood']}")
        print(f"Voice Tone Hint   : {expression['voice_tone_hint']}")
        print(f"Avatar Expression : {expression['avatar_expression_hint']}")
        print(f"Gesture Hint      : {expression['gesture_hint']}")
        print(f"Response Style    : {expression['response_style_hint']}")
        print(f"Avatar Changed    : {expression['avatar_changed']}")
        print(f"Voice Output      : {expression['voice_output_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def creative_brief_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Brief Plan",
            manager.brief_plan(target),
        )

    def creative_character_concept_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Character Concept Plan",
            manager.character_concept_plan(target),
        )

    def creative_visual_asset_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Visual Asset Plan",
            manager.visual_asset_plan(target),
        )

    def creative_content_idea_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Content Idea Plan",
            manager.content_idea_plan(target),
        )

    def creative_review_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Review Plan",
            manager.review_plan(target),
        )

    def creative_context(self) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Creative Assistant Context")
        print("===============================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Proposal Only                         : {context['proposal_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"Image Generation Performed            : {context['image_generation_performed']}")
        print(f"Media File Opened                     : {context['media_file_opened']}")
        print(f"Pixel Read                            : {context['pixel_read']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print()
        print("Creative Status")
        print("---------------")
        status = context["creative_status"]
        print(f"Assistant Ready              : {status['assistant_ready']}")
        print(f"Brief Plan Ready             : {status['brief_plan_ready']}")
        print(f"Character Concept Ready      : {status['character_concept_ready']}")
        print(f"Visual Asset Plan Ready      : {status['visual_asset_plan_ready']}")
        print(f"Content Idea Plan Ready      : {status['content_idea_plan_ready']}")
        print(f"Review Plan Ready            : {status['review_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Proposal Only                : {status['proposal_only']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print()
        print("Integration Summary")
        print("-------------------")
        integration = context["integration_summary"]
        print(f"Project Intent Ready         : {integration['project_intent_ready']}")
        print(f"Workspace Memory Ready       : {integration['workspace_memory_ready']}")
        print(f"Media Understanding Ready    : {integration['media_understanding_ready']}")
        print(f"Expression Language Ready    : {integration['expression_language_ready']}")
        print(f"Blender Bridge Ready         : {integration['blender_bridge_ready']}")
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

