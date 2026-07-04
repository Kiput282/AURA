import re
from pathlib import Path

from aura.context.context_packet import ContextPacket
from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore


class ContextManager:
    """
    Context Manager v1 for AURA.

    Responsibilities:
    - collect pinned memories
    - collect important memories
    - collect relevant memories
    - collect recent project journal entries
    - return a structured ContextPacket
    """

    STOPWORDS = {
        "a", "an", "the", "is", "are", "am", "to", "of", "and", "or",
        "apa", "yang", "di", "ke", "dari", "ini", "itu", "kita", "saya",
        "aku", "sebuah", "sebagai", "dengan", "untuk", "sedang",
        "aura", "gunakan", "digunakan", "pakai", "memakai", "use", "used",

        # Generic/noisy memory-management terms.
        "memory", "memori", "remember", "recall", "delete", "deleted",
        "hapus", "test", "testing", "uji", "coba", "temp", "temporary",
        "sementara",
    }

    SYNONYMS = {
        "bangun": {"membangun", "build", "building", "project"},
        "membangun": {"bangun", "build", "building", "project"},
        "build": {"bangun", "membangun", "building", "project"},
        "building": {"bangun", "membangun", "build", "project"},
        "project": {"proyek", "membangun", "build", "building"},
        "proyek": {"project", "membangun", "build", "building"},

        "otak": {"model", "reasoning", "ollama", "llama3.2"},
        "lokal": {"local", "ollama", "llama3.2"},
        "local": {"lokal", "ollama", "llama3.2"},
        "model": {"otak", "reasoning", "ollama", "llama3.2"},
        "ollama": {"model", "otak", "lokal", "local", "llama3.2"},
        "llama3.2": {"model", "otak", "ollama", "lokal", "local"},
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_store = MemoryStore(project_root=project_root)
        self.project_journal = ProjectJournal(project_root=project_root)

    def build(
        self,
        user_message: str,
        relevant_limit: int = 5,
        important_limit: int = 5,
        journal_limit: int = 3,
    ) -> ContextPacket:
        pinned_memories = self.memory_store.list_pinned()
        pinned_ids = {
            memory.id
            for memory in pinned_memories
        }

        important_memories = self.remove_duplicate_memories(
            memories=self.list_important_memories(limit=important_limit),
            existing_ids=pinned_ids,
        )
        important_ids = {
            memory.id
            for memory in important_memories
        }

        relevant_memories = self.list_relevant_memories(
            query=user_message,
            limit=relevant_limit,
        )
        recent_journal_entries = self.project_journal.list_recent(limit=journal_limit)

        relevant_memories = self.remove_duplicate_memories(
            memories=relevant_memories,
            existing_ids=pinned_ids | important_ids,
        )

        return ContextPacket(
            user_message=user_message,
            pinned_memories=pinned_memories,
            important_memories=important_memories,
            relevant_memories=relevant_memories,
            recent_journal_entries=recent_journal_entries,
            metadata={
                "relevant_limit": relevant_limit,
                "important_limit": important_limit,
                "journal_limit": journal_limit,
            },
        )

    def tokenize(self, text: str) -> set[str]:
        tokens = set(re.findall(r"[a-zA-Z0-9_.]+", text.lower()))
        return {
            token
            for token in tokens
            if token and token not in self.STOPWORDS
        }

    def expand_tokens(self, tokens: set[str]) -> set[str]:
        expanded_tokens = set(tokens)

        for token in tokens:
            expanded_tokens.update(self.SYNONYMS.get(token, set()))

        return expanded_tokens

    def score_memory(self, query_tokens: set[str], memory: MemoryItem) -> int:
        content_tokens = self.tokenize(memory.content)
        metadata_tokens = self.tokenize(" ".join(str(value) for value in memory.metadata.values()))

        memory_tokens = content_tokens | metadata_tokens
        matched_tokens = query_tokens & memory_tokens

        score = len(matched_tokens)

        content_lower = memory.content.lower()
        for token in query_tokens:
            if token in content_lower:
                score += 1

        return score

    def list_relevant_memories(self, query: str, limit: int = 5) -> list[MemoryItem]:
        query_tokens = self.expand_tokens(self.tokenize(query))

        if not query_tokens:
            return []

        scored_memories: list[tuple[int, int, MemoryItem]] = []

        for index, memory in enumerate(self.memory_store.list_all()):
            if memory.kind == "system" and int(memory.metadata.get("importance", 3)) < 4:
                continue

            score = self.score_memory(query_tokens=query_tokens, memory=memory)

            if score >= 2:
                scored_memories.append((score, index, memory))

        scored_memories.sort(
            key=lambda item: (
                item[0],
                int(item[2].metadata.get("importance", 3)),
                item[1],
            ),
            reverse=True,
        )

        return [
            memory
            for _, _, memory in scored_memories[:limit]
        ]

    def list_important_memories(self, limit: int = 5) -> list[MemoryItem]:
        memories = self.memory_store.list_all()

        important_memories = [
            memory
            for memory in memories
            if int(memory.metadata.get("importance", 3)) >= 4
        ]

        important_memories.sort(
            key=lambda memory: int(memory.metadata.get("importance", 3)),
            reverse=True,
        )

        return important_memories[:limit]

    def remove_duplicate_memories(
        self,
        memories: list[MemoryItem],
        existing_ids: set[str],
    ) -> list[MemoryItem]:
        unique_memories: list[MemoryItem] = []

        for memory in memories:
            if memory.id in existing_ids:
                continue

            unique_memories.append(memory)

        return unique_memories
