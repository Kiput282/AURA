from pathlib import Path
from typing import Any

import yaml

from aura.context.context_manager import ContextManager
from aura.memory.conversation_store import ConversationStore
from aura.memory.conversation_turn import ConversationTurn
from aura.memory.memory_context import MemoryContextBuilder
from aura.memory.memory_store import MemoryStore
from aura.reasoning.factory import ReasoningProviderFactory
from aura.reasoning.provider import ReasoningProvider


class AuraChat:
    """
    Chat interface for AURA Genesis.

    AuraChat delegates reasoning to a ReasoningProvider.
    It also builds context for the provider, including:
    - identity
    - relevant memories
    - recent memories
    - recent conversations
    """

    def __init__(
        self,
        project_root: Path,
        reasoning_provider: ReasoningProvider | None = None,
    ):
        self.project_root = project_root
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

        self.memory_store = MemoryStore(project_root=self.project_root)
        self.context_manager = ContextManager(project_root=self.project_root)
        self.memory_context_builder = MemoryContextBuilder(memory_store=self.memory_store)
        self.conversation_store = ConversationStore(project_root=self.project_root)
        self.reasoning_provider = (
            reasoning_provider
            or ReasoningProviderFactory.from_settings(project_root=self.project_root)
        )

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        with self.identity_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def build_context(self, message: str = "") -> dict[str, Any]:
        context_packet = self.context_manager.build(user_message=message)
        legacy_memory_context = self.memory_context_builder.build_context(query=message)

        context_memories = self.merge_memories(
            context_packet.pinned_memories,
            context_packet.important_memories,
            context_packet.relevant_memories,
        )

        return {
            "identity": self.load_identity(),
            "context_packet": context_packet,
            "context_packet_text": context_packet.to_text(),
            "pinned_memories": context_packet.pinned_memories,
            "important_memories": context_packet.important_memories,
            "raw_relevant_memories": context_packet.relevant_memories,
            "relevant_memories": context_memories,
            "recent_memories": legacy_memory_context["recent_memories"],
            "recent_project_journal": context_packet.recent_journal_entries,
            "memory_context": {
                "pinned_count": len(context_packet.pinned_memories),
                "important_count": len(context_packet.important_memories),
                "relevant_count": len(context_packet.relevant_memories),
                "context_memory_count": len(context_memories),
                "recent_count": legacy_memory_context["recent_count"],
                "journal_count": len(context_packet.recent_journal_entries),
            },
            "recent_conversations": self.conversation_store.list_recent(limit=5),
            "provider": {
                "name": self.reasoning_provider.name,
                "version": self.reasoning_provider.version,
            },
        }

    def merge_memories(self, *memory_groups):
        merged = []
        seen_ids = set()

        for memories in memory_groups:
            for memory in memories:
                if memory.id in seen_ids:
                    continue

                seen_ids.add(memory.id)
                merged.append(memory)

        return merged

    def detect_language(self, message: str) -> str:
        normalized = message.strip().lower()

        english_markers = {
            "what",
            "who",
            "when",
            "where",
            "why",
            "how",
            "last",
            "latest",
            "recent",
            "briefly",
        }

        indonesian_markers = {
            "apa",
            "siapa",
            "kapan",
            "dimana",
            "di mana",
            "kenapa",
            "bagaimana",
            "terakhir",
            "barusan",
            "singkat",
        }

        tokens = {
            token.strip(".,!?;:'\"()[]{}")
            for token in normalized.replace("/", " ").split()
        }

        english_score = len(tokens.intersection(english_markers))
        indonesian_score = len(tokens.intersection(indonesian_markers))

        if english_score > indonesian_score:
            return "en"

        if indonesian_score > english_score:
            return "id"

        return "unknown"

    def try_context_guardrail(self, message: str, context: dict[str, Any]) -> str | None:
        normalized = message.strip().lower()
        recent_journal = context.get("recent_project_journal", [])

        asks_latest_work = any(
            phrase in normalized
            for phrase in {
                "apa yang terakhir kita kerjakan",
                "apa terakhir yang kita kerjakan",
                "terakhir kita kerjakan",
                "terakhir kita mengerjakan",
                "terakhir kita buat",
                "apa sprint terakhir",
                "sprint terakhir",
                "what did we work on last",
                "what was the latest sprint",
                "latest sprint",
                "last sprint",
            }
        )

        if asks_latest_work and recent_journal:
            latest_entry = recent_journal[-1]
            content = latest_entry.content

            if self.detect_language(message) == "en":
                return f"The latest work was {content}"

            return f"Terakhir kita mengerjakan {content}"

        return None

    def generate_response(self, message: str) -> str:
        context = self.build_context(message=message)
        guardrail_response = self.try_context_guardrail(message=message, context=context)

        if guardrail_response:
            return guardrail_response

        return self.reasoning_provider.respond(message, context=context)

    def respond(self, message: str, *, source: str = "AuraChat") -> str:
        response = self.generate_response(message)

        context = self.build_context(message=message)

        turn = ConversationTurn(
            user_message=message,
            aura_response=response,
            source=source,
            metadata={
                "phase": "Genesis",
                "engine": self.reasoning_provider.name,
                "provider_version": self.reasoning_provider.version,
                "relevant_memory_count": context["memory_context"]["relevant_count"],
                "pinned_memory_count": context["memory_context"]["pinned_count"],
                "important_memory_count": context["memory_context"]["important_count"],
                "journal_context_count": context["memory_context"]["journal_count"],
                "context_aware": True,
            },
        )

        self.conversation_store.save_turn(turn)

        return response

    def recent_conversations(self, limit: int = 5) -> list[ConversationTurn]:
        return self.conversation_store.list_recent(limit=limit)

    def provider_info(self) -> dict[str, str]:
        return {
            "name": self.reasoning_provider.name,
            "version": self.reasoning_provider.version,
        }

    def provider_runtime_check(self) -> dict[str, Any]:
        context = self.build_context()
        return self.reasoning_provider.health_check(context=context)

    def relevant_memories(self, message: str, limit: int = 5):
        return self.memory_context_builder.find_relevant(query=message, limit=limit)
