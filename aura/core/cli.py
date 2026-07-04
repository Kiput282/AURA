import argparse
from pathlib import Path

import yaml

from aura.core.chat import AuraChat
from aura.core.shell import AuraShell
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
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
    - reason
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
            print(f"- [{memory.kind}] {memory.content}")

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

        subparsers.add_parser("provider")
        subparsers.add_parser("reason")

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

        if parsed.command in {"provider", "reason"}:
            disable_logging()
            self.provider()
            return True

        if parsed.command == "shell":
            disable_logging()
            self.shell()
            return True

        return False
