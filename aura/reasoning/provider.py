from abc import ABC, abstractmethod
from typing import Any


class ReasoningProvider(ABC):
    """
    Base interface for AURA reasoning providers.

    Future providers can include:
    - rule-based
    - local LLM
    - Ollama
    - OpenAI
    - LM Studio
    - custom model adapters
    """

    name: str = "unknown"
    version: str = "0.0.0"

    @abstractmethod
    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        pass
