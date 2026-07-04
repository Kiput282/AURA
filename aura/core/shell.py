from pathlib import Path

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore


class AuraShell:
    """
    Interactive shell for AURA Genesis.

    Supported commands:
    - help
    - remember <text>
    - recall
    - recall <limit>
    - status
    - exit
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.memory_store = MemoryStore(project_root=self.project_root)
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
        print("  exit                 Exit AURA shell")

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
