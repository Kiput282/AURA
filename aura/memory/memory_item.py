from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class MemoryItem:
    """
    Represents one memory record inside AURA.

    For now, memory is simple and file-based.
    Later this can be upgraded to SQLite, vector database, or hybrid memory.
    """

    content: str
    kind: str = "note"
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryItem":
        return cls(
            id=data["id"],
            kind=data.get("kind", "note"),
            content=data["content"],
            metadata=data.get("metadata", {}),
            created_at=data["created_at"],
        )
