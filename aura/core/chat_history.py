import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from loguru import logger


@dataclass
class ChatTurn:
    """
    Represents one chat exchange between the user and AURA.
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
    def from_dict(cls, data: dict[str, Any]) -> "ChatTurn":
        return cls(
            id=data["id"],
            source=data.get("source", "AuraChat"),
            user_message=data["user_message"],
            aura_response=data["aura_response"],
            metadata=data.get("metadata", {}),
            created_at=data["created_at"],
        )


class ChatHistoryStore:
    """
    Simple file-based chat history store for AURA Genesis.

    Current format:
    - JSON Lines
    - one chat turn per line
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.history_dir = self.project_root / "data" / "chat"
        self.history_file = self.history_dir / "history.jsonl"

        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.history_file.touch(exist_ok=True)

        logger.info(f"ChatHistoryStore initialized at {self.history_file}")

    def save_turn(self, turn: ChatTurn) -> None:
        with self.history_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(turn.to_dict(), ensure_ascii=False) + "\n")

        logger.info(f"Chat turn saved: {turn.id}")

    def list_all(self) -> list[ChatTurn]:
        if not self.history_file.exists():
            return []

        turns: list[ChatTurn] = []

        lines = self.history_file.read_text(encoding="utf-8").splitlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                turns.append(ChatTurn.from_dict(data))
            except Exception as error:
                logger.exception(f"Failed to load chat history line: {error}")

        return turns

    def list_recent(self, limit: int = 5) -> list[ChatTurn]:
        return self.list_all()[-limit:]

    def count(self) -> int:
        return len(self.list_all())
