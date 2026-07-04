import json
from pathlib import Path

from loguru import logger

from aura.memory.conversation_turn import ConversationTurn


class ConversationStore:
    """
    File-based conversation history store for AURA.

    Current format:
    - JSON Lines
    - one conversation turn per line
    - append-only
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.conversation_dir = self.project_root / "data" / "conversations"
        self.conversation_file = self.conversation_dir / "chat_history.jsonl"

        self.conversation_dir.mkdir(parents=True, exist_ok=True)
        self.conversation_file.touch(exist_ok=True)

        logger.info(f"ConversationStore initialized at {self.conversation_file}")

    def save_turn(self, turn: ConversationTurn) -> None:
        with self.conversation_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(turn.to_dict(), ensure_ascii=False) + "\n")

        logger.info(f"Conversation turn saved: {turn.id}")

    def list_all(self) -> list[ConversationTurn]:
        if not self.conversation_file.exists():
            return []

        turns: list[ConversationTurn] = []

        lines = self.conversation_file.read_text(encoding="utf-8").splitlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                turns.append(ConversationTurn.from_dict(data))
            except Exception as error:
                logger.exception(f"Failed to load conversation line: {error}")

        return turns

    def list_recent(self, limit: int = 5) -> list[ConversationTurn]:
        return self.list_all()[-limit:]

    def count(self) -> int:
        return len(self.list_all())
