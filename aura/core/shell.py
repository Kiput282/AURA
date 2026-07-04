import os
from pathlib import Path

import yaml

from aura.core.chat import AuraChat
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
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
        print("  chat <text>          Send a message to AURA")
        print("  ask <text>           Alias for chat")
        print("  history              Show recent chat history")
        print("  history <limit>      Show recent chat history with limit")
        print("  status               Show shell status")
        print("  version              Show AURA version")
        print("  provider             Show reasoning provider")
        print("  reason               Alias for provider")
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
            print(f"- [{memory.kind}] {memory.content}")

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

        if normalized == "status":
            self.status()
            return

        if normalized == "version":
            self.version()
            return

        if normalized in {"provider", "reason"}:
            self.provider()
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

        print(f"Unknown command: {command}")
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
