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
    - append-friendly for save
    - rewrite-based for update/delete
    """

    PROTECTED_KINDS = {"system"}

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

    def write_all(self, memories: list[MemoryItem]) -> None:
        with self.memory_file.open("w", encoding="utf-8") as file:
            for memory in memories:
                file.write(json.dumps(memory.to_dict(), ensure_ascii=False) + "\n")

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

    def is_protected(self, memory: MemoryItem) -> bool:
        return memory.kind in self.PROTECTED_KINDS

    def update_by_id(self, memory_id: str, metadata_updates: dict) -> MemoryItem | None:
        target_id = memory_id.strip()
        memories = self.list_all()

        updated_memory: MemoryItem | None = None

        for memory in memories:
            if memory.id != target_id:
                continue

            memory.metadata.update(metadata_updates)
            updated_memory = memory
            break

        if updated_memory is None:
            return None

        self.write_all(memories)
        logger.info(f"Memory updated: {updated_memory.id}")

        return updated_memory

    def set_pinned(self, memory_id: str, pinned: bool) -> MemoryItem | None:
        return self.update_by_id(
            memory_id=memory_id,
            metadata_updates={"pinned": pinned},
        )

    def set_importance(self, memory_id: str, importance: int) -> MemoryItem | None:
        if importance < 1 or importance > 5:
            raise ValueError("importance must be between 1 and 5")

        return self.update_by_id(
            memory_id=memory_id,
            metadata_updates={"importance": importance},
        )

    def list_pinned(self) -> list[MemoryItem]:
        return [
            memory
            for memory in self.list_all()
            if bool(memory.metadata.get("pinned", False))
        ]

    def delete_by_id(self, memory_id: str) -> MemoryItem | None:
        target_id = memory_id.strip()
        memories = self.list_all()

        deleted_memory: MemoryItem | None = None
        remaining_memories: list[MemoryItem] = []

        for memory in memories:
            if memory.id == target_id:
                if self.is_protected(memory):
                    logger.warning(f"Blocked deletion of protected memory: {memory.id}")
                    return None

                deleted_memory = memory
                continue

            remaining_memories.append(memory)

        if deleted_memory is None:
            return None

        self.write_all(remaining_memories)

        logger.info(f"Memory deleted: {deleted_memory.id}")

        return deleted_memory

    def count(self) -> int:
        return len(self.list_all())
