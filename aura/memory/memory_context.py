import re

from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore


class MemoryContextBuilder:
    """
    Builds memory context for AURA chat.

    Current strategy:
    - keyword relevance
    - lightweight Indonesian/English normalization
    - recent fallback
    """

    STOPWORDS = {
        "a", "an", "and", "are", "as", "at",
        "apa", "atau", "bagaimana", "buat",
        "dan", "di", "do", "does", "for", "from",
        "how", "i", "ini", "is", "itu",
        "kamu", "kita", "me", "my", "of", "on",
        "sedang", "saya", "the", "to", "untuk",
        "what", "who", "yang", "you", "your",
    }

    SYNONYMS = {
        "bangun": {"bangun", "membangun", "dibangun", "build", "building", "built"},
        "membangun": {"bangun", "membangun", "dibangun", "build", "building", "built"},
        "build": {"bangun", "membangun", "dibangun", "build", "building", "built"},
        "building": {"bangun", "membangun", "dibangun", "build", "building", "built"},
        "server": {"server", "atlas"},
        "atlas": {"server", "atlas"},
        "model": {"model", "llama3", "llama3.2", "ollama"},
        "llama3": {"model", "llama3", "llama3.2", "ollama"},
        "ollama": {"model", "llama3", "llama3.2", "ollama"},
        "otak": {"otak", "brain", "model", "ollama", "llama3.2"},
        "brain": {"otak", "brain", "model", "ollama", "llama3.2"},
    }

    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store

    def normalize_token(self, token: str) -> str:
        token = token.lower().strip()

        replacements = {
            "membuatmu": "membuat",
            "menciptakanmu": "menciptakan",
            "membangunnya": "membangun",
            "dibangunnya": "dibangun",
            "llama3_2": "llama3.2",
        }

        return replacements.get(token, token)

    def expand_tokens(self, tokens: set[str]) -> set[str]:
        expanded = set(tokens)

        for token in tokens:
            if token in self.SYNONYMS:
                expanded.update(self.SYNONYMS[token])

        return expanded

    def tokenize(self, text: str) -> set[str]:
        raw_tokens = re.findall(r"[a-zA-Z0-9_.]+", text.lower())

        tokens = {
            self.normalize_token(token)
            for token in raw_tokens
            if len(token) >= 3 and token not in self.STOPWORDS
        }

        return self.expand_tokens(tokens)

    def score_memory(self, query_tokens: set[str], memory: MemoryItem) -> int:
        memory_tokens = self.tokenize(memory.content)

        if not query_tokens or not memory_tokens:
            return 0

        overlap = query_tokens.intersection(memory_tokens)
        score = len(overlap) * 3

        lowered_content = memory.content.lower()

        for token in query_tokens:
            if token in lowered_content:
                score += 1

        return score

    def find_relevant(self, query: str, limit: int = 5) -> list[MemoryItem]:
        memories = self.memory_store.list_all()
        query_tokens = self.tokenize(query)

        scored_memories: list[tuple[int, int, MemoryItem]] = []

        for index, memory in enumerate(memories):
            score = self.score_memory(query_tokens=query_tokens, memory=memory)
            if score > 0:
                scored_memories.append((score, index, memory))

        scored_memories.sort(key=lambda item: (item[0], item[1]), reverse=True)

        return [memory for _, _, memory in scored_memories[:limit]]

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
