import json
from pathlib import Path

from loguru import logger

from aura.memory.memory_item import MemoryItem


class MemoryStore:
    """
    Simple file-based memory store for AURA.

    Current format:
    - JSON Lines
    - one memory per line
    - append-only

    This is intentionally simple for Genesis.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_dir = self.project_root / "data" / "memory"
        self.memory_file = self.memory_dir / "memories.jsonl"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file.touch(exist_ok=True)

        logger.info(f"MemoryStore initialized at {self.memory_file}")

    def save(self, item: MemoryItem) -> None:
        with self.memory_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")

        logger.info(f"Memory saved: {item.id}")

    def list_recent(self, limit: int = 5) -> list[MemoryItem]:
        if not self.memory_file.exists():
            return []

        lines = self.memory_file.read_text(encoding="utf-8").splitlines()
        recent_lines = lines[-limit:]

        memories: list[MemoryItem] = []

        for line in recent_lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                memories.append(MemoryItem.from_dict(data))
            except Exception as error:
                logger.exception(f"Failed to load memory line: {error}")

        return memories
