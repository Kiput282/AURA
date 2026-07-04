from abc import ABC, abstractmethod
from typing import Any


class ReasoningProvider(ABC):
    """
    Base interface for AURA reasoning providers.
    """

    name: str = "unknown"
    version: str = "0.0.0"

    @abstractmethod
    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        pass

    def health_check(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "status": "OK",
            "message": "Provider is available.",
            "provider": self.name,
            "version": self.version,
        }
