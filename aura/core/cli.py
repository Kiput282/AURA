import argparse
from pathlib import Path

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore


class AuraCLI:
    """
    Simple command-line interface for AURA.

    Supported commands:
    - boot
    - remember
    - recall
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.memory_store = MemoryStore(project_root=self.project_root)

    def remember(self, content: str) -> None:
        memory = MemoryItem(
            kind="user_note",
            content=content,
            metadata={
                "source": "AuraCLI",
            },
        )

        self.memory_store.save(memory)

        print("Memory saved.")
        print(f"Content: {content}")

    def recall(self, limit: int = 5) -> None:
        memories = self.memory_store.list_recent(limit=limit)

        print("AURA Memory Recall")
        print("==================")

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            print(f"- [{memory.kind}] {memory.content}")

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

        return parser.parse_args(args)

    def run(self, args: list[str] | None = None) -> bool:
        parsed = self.parse(args)

        if parsed.command == "remember":
            self.remember(parsed.content)
            return True

        if parsed.command == "recall":
            self.recall(limit=parsed.limit)
            return True

        return False
