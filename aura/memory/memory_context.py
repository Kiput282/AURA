import re

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore


class MemoryContextBuilder:
    """
    Builds memory context for AURA chat.

    Current strategy:
    - simple keyword relevance
    - recent fallback

    Future strategy:
    - embeddings
    - vector search
    - semantic memory graph
    """

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "apa",
        "atau",
        "bagaimana",
        "buat",
        "dan",
        "di",
        "do",
        "does",
        "for",
        "from",
        "how",
        "i",
        "ini",
        "is",
        "itu",
        "kamu",
        "kita",
        "me",
        "membuat",
        "membangun",
        "my",
        "of",
        "on",
        "sedang",
        "saya",
        "the",
        "to",
        "untuk",
        "what",
        "who",
        "yang",
        "you",
        "your",
    }

    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store

    def tokenize(self, text: str) -> set[str]:
        tokens = re.findall(r"[a-zA-Z0-9_]+", text.lower())
        return {
            token
            for token in tokens
            if len(token) >= 3 and token not in self.STOPWORDS
        }

    def score_memory(self, query_tokens: set[str], memory: MemoryItem) -> int:
        memory_tokens = self.tokenize(memory.content)

        if not query_tokens or not memory_tokens:
            return 0

        overlap = query_tokens.intersection(memory_tokens)
        score = len(overlap)

        lowered_content = memory.content.lower()

        for token in query_tokens:
            if token in lowered_content:
                score += 1

        return score

    def find_relevant(self, query: str, limit: int = 5) -> list[MemoryItem]:
        memories = self.memory_store.list_all()
        query_tokens = self.tokenize(query)

        scored_memories: list[tuple[int, MemoryItem]] = []

        for memory in memories:
            score = self.score_memory(query_tokens=query_tokens, memory=memory)
            if score > 0:
                scored_memories.append((score, memory))

        scored_memories.sort(key=lambda item: item[0], reverse=True)

        return [memory for _, memory in scored_memories[:limit]]

    def build_context(
        self,
        query: str,
        relevant_limit: int = 5,
        recent_limit: int = 5,
    ) -> dict:
        relevant_memories = self.find_relevant(query=query, limit=relevant_limit)
        recent_memories = self.memory_store.list_recent(limit=recent_limit)

        return {
            "relevant_memories": relevant_memories,
            "recent_memories": recent_memories,
            "relevant_count": len(relevant_memories),
            "recent_count": len(recent_memories),
        }
