from pathlib import Path
from typing import Any

from aura.memory.conversation_store import ConversationStore
from aura.memory.conversation_turn import ConversationTurn
from aura.memory.memory_store import MemoryStore
from aura.reasoning.factory import ReasoningProviderFactory
from aura.reasoning.provider import ReasoningProvider


class AuraChat:
    """
    Chat interface for AURA Genesis.

    AuraChat delegates reasoning to a ReasoningProvider.
    """

    def __init__(
        self,
        project_root: Path,
        reasoning_provider: ReasoningProvider | None = None,
    ):
        self.project_root = project_root
        self.memory_store = MemoryStore(project_root=self.project_root)
        self.conversation_store = ConversationStore(project_root=self.project_root)
        self.reasoning_provider = (
            reasoning_provider
            or ReasoningProviderFactory.from_settings(project_root=self.project_root)
        )

    def build_context(self) -> dict:
        return {
            "recent_memories": self.memory_store.list_recent(limit=5),
            "recent_conversations": self.conversation_store.list_recent(limit=5),
            "provider": {
                "name": self.reasoning_provider.name,
                "version": self.reasoning_provider.version,
            },
        }

    def generate_response(self, message: str) -> str:
        context = self.build_context()
        return self.reasoning_provider.respond(message, context=context)

    def respond(self, message: str, *, source: str = "AuraChat") -> str:
        response = self.generate_response(message)

        turn = ConversationTurn(
            user_message=message,
            aura_response=response,
            source=source,
            metadata={
                "phase": "Genesis",
                "engine": self.reasoning_provider.name,
                "provider_version": self.reasoning_provider.version,
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
