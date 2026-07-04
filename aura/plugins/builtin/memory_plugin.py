from pathlib import Path

from loguru import logger

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.plugins.plugin import Plugin


class MemoryPlugin(Plugin):
    name = "memory"
    version = "0.1.0"
    description = "Simple file-based memory foundation for AURA."

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.store = MemoryStore(project_root=self.project_root)
        self._status = "NOT_READY"

    def start(self) -> None:
        bootstrap_memory = MemoryItem(
            kind="system",
            content="AURA Memory Foundation initialized.",
            metadata={
                "source": "MemoryPlugin",
                "phase": "Genesis",
            },
        )

        self.store.save(bootstrap_memory)
        self._status = "OK"

        logger.info("MemoryPlugin started")

    def stop(self) -> None:
        logger.info("MemoryPlugin stopped")

    def status(self) -> str:
        return self._status

    def recent_memories(self, limit: int = 5) -> list[MemoryItem]:
        return self.store.list_recent(limit=limit)
