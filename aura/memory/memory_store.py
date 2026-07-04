import json
from pathlib import Path

from loguru import logger

from aura.memory.memory_item import MemoryItem


class MemoryStore:
    """
    Simple file-based memory store for AURA.

    Current format:
    - JSON Lines
    - one memory item per line
    - append-friendly
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

    def list_all(self) -> list[MemoryItem]:
        if not self.memory_file.exists():
            return []

        memories: list[MemoryItem] = []

        lines = self.memory_file.read_text(encoding="utf-8").splitlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                memories.append(MemoryItem.from_dict(data))
            except Exception as error:
                logger.exception(f"Failed to load memory line: {error}")

        return memories

    def list_recent(self, limit: int = 5) -> list[MemoryItem]:
        return self.list_all()[-limit:]

    def exists(self, kind: str, content: str) -> bool:
        for memory in self.list_all():
            if memory.kind == kind and memory.content == content:
                return True

        return False

    def find_by_id(self, memory_id: str) -> MemoryItem | None:
        target_id = memory_id.strip()

        for memory in self.list_all():
            if memory.id == target_id:
                return memory

        return None

    def delete_by_id(self, memory_id: str) -> MemoryItem | None:
        target_id = memory_id.strip()
        memories = self.list_all()

        deleted_memory: MemoryItem | None = None
        remaining_memories: list[MemoryItem] = []

        for memory in memories:
            if memory.id == target_id:
                deleted_memory = memory
                continue

            remaining_memories.append(memory)

        if deleted_memory is None:
            return None

        with self.memory_file.open("w", encoding="utf-8") as file:
            for memory in remaining_memories:
                file.write(json.dumps(memory.to_dict(), ensure_ascii=False) + "\n")

        logger.info(f"Memory deleted: {deleted_memory.id}")

        return deleted_memory

    def count(self) -> int:
        return len(self.list_all())
