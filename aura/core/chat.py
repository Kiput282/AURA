from pathlib import Path

from aura.memory.memory_store import MemoryStore


class AuraChat:
    """
    Early chat foundation for AURA Genesis.

    This is not an LLM yet.
    It provides a stable interface that can later be connected to:
    - local LLM
    - remote LLM
    - memory-aware reasoning
    - tool/plugin calling
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.memory_store = MemoryStore(project_root=self.project_root)

    def respond(self, message: str) -> str:
        normalized = message.strip().lower()

        if not normalized:
            return "I heard silence. That's okay. I'm still here."

        if normalized in {"hello", "hi", "hey", "halo"}:
            return "Hello, Kiput. I'm here."

        if "who are you" in normalized or "siapa kamu" in normalized:
            return "I'm AURA, your AI partner in Genesis phase."

        if "what do you remember" in normalized or "apa yang kamu ingat" in normalized:
            memories = self.memory_store.list_recent(limit=5)

            if not memories:
                return "I don't have any memories yet."

            lines = ["I remember:"]
            for memory in memories:
                lines.append(f"- {memory.content}")

            return "\n".join(lines)

        if "status" in normalized:
            return "AURA Genesis is online. Core, plugins, shell, and memory are working."

        return (
            "I don't have full reasoning yet, but I received your message: "
            f"\"{message}\""
        )
