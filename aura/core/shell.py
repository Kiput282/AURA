import os
from pathlib import Path

import yaml

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.plugins.builtin.echo_plugin import EchoPlugin
from aura.plugins.builtin.memory_plugin import MemoryPlugin
from aura.plugins.plugin_manager import PluginManager


class AuraShell:
    """
    Interactive shell for AURA Genesis.

    Supported commands:
    - help
    - remember <text>
    - recall
    - recall <limit>
    - status
    - version
    - plugins
    - health
    - clear
    - exit
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.settings_path = self.project_root / "aura" / "config" / "settings.yaml"

        self.memory_store = MemoryStore(project_root=self.project_root)
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
        print("  status               Show shell status")
        print("  version              Show AURA version")
        print("  plugins              Show loaded plugins")
        print("  health               Show shell health summary")
        print("  clear                Clear the terminal screen")
        print("  exit                 Exit AURA shell")

    def load_identity(self) -> dict:
        if not self.identity_path.exists():
            return {}

        with self.identity_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

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

    def status(self) -> None:
        memory_count = self.memory_store.count()

        print("AURA Shell Status")
        print("=================")
        print("Shell   : ONLINE")
        print("Memory  : ONLINE")
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

        config_status = "OK" if self.settings_path.exists() else "ERROR"
        identity_status = "OK" if self.identity_path.exists() else "ERROR"

        print("AURA Shell Health")
        print("=================")
        print("Shell     : OK - Interactive shell online")
        print(f"Config    : {config_status} - settings.yaml")
        print(f"Identity  : {identity_status} - identity.yaml")
        print("Memory    : OK - File-based memory store online")
        print(f"Records   : OK - {memory_count} memory record(s)")
        print(f"Plugins   : OK - {plugin_count} plugin(s) loaded")

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def handle_command(self, raw_command: str) -> None:
        command = raw_command.strip()

        if not command:
            return

        if command == "help":
            self.print_help()
            return

        if command == "exit":
            print("Goodbye, Kiput.")
            self.running = False
            return

        if command == "status":
            self.status()
            return

        if command == "version":
            self.version()
            return

        if command == "plugins":
            self.plugins()
            return

        if command == "health":
            self.health()
            return

        if command == "clear":
            self.clear()
            return

        if command == "recall":
            self.recall()
            return

        if command.startswith("recall "):
            raw_limit = command.removeprefix("recall ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid recall limit. Example: recall 3")
                return

            self.recall(limit=limit)
            return

        if command.startswith("remember "):
            content = command.removeprefix("remember ")
            self.remember(content)
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
