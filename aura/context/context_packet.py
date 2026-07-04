from dataclasses import dataclass, field
from typing import Any

from aura.journal.journal_entry import JournalEntry
from aura.memory.memory_item import MemoryItem


@dataclass
class ContextPacket:
    """
    Represents prepared context for AURA reasoning.

    This packet is a structured bundle of information that can be used by
    chat, roles, model routing, and future tool/action systems.
    """

    user_message: str
    pinned_memories: list[MemoryItem] = field(default_factory=list)
    important_memories: list[MemoryItem] = field(default_factory=list)
    relevant_memories: list[MemoryItem] = field(default_factory=list)
    recent_journal_entries: list[JournalEntry] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def memory_ids(self) -> set[str]:
        ids: set[str] = set()

        for memory in self.pinned_memories:
            ids.add(memory.id)

        for memory in self.important_memories:
            ids.add(memory.id)

        for memory in self.relevant_memories:
            ids.add(memory.id)

        return ids

    def to_text(self) -> str:
        lines: list[str] = []

        lines.append("AURA Context Packet")
        lines.append("===================")
        lines.append(f"User Message: {self.user_message}")
        lines.append("")

        lines.append("Pinned Memories:")
        if self.pinned_memories:
            for memory in self.pinned_memories:
                lines.append(f"- [{memory.kind}] {memory.content}")
        else:
            lines.append("- none")
        lines.append("")

        lines.append("Important Memories:")
        if self.important_memories:
            for memory in self.important_memories:
                importance = memory.metadata.get("importance", 3)
                lines.append(f"- importance={importance} [{memory.kind}] {memory.content}")
        else:
            lines.append("- none")
        lines.append("")

        lines.append("Relevant Memories:")
        if self.relevant_memories:
            for memory in self.relevant_memories:
                lines.append(f"- [{memory.kind}] {memory.content}")
        else:
            lines.append("- none")
        lines.append("")

        lines.append("Recent Project Journal:")
        if self.recent_journal_entries:
            for entry in self.recent_journal_entries:
                lines.append(f"- {entry.title}: {entry.content}")
        else:
            lines.append("- none")

        return "\n".join(lines)
