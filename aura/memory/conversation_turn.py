from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class ConversationTurn:
    """
    Represents one user-AURA conversation turn.
    """

    user_message: str
    aura_response: str
    source: str = "AuraChat"
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "user_message": self.user_message,
            "aura_response": self.aura_response,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConversationTurn":
        return cls(
            id=data["id"],
            source=data.get("source", "AuraChat"),
            user_message=data["user_message"],
            aura_response=data["aura_response"],
            metadata=data.get("metadata", {}),
            created_at=data["created_at"],
        )
