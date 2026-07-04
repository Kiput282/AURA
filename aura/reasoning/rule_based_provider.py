from typing import Any

from aura.reasoning.provider import ReasoningProvider


class RuleBasedReasoningProvider(ReasoningProvider):
    """
    Simple rule-based reasoning provider for AURA Genesis.

    This is temporary.
    Later, this provider interface can be connected to actual LLM backends.
    """

    name = "rule_based"
    version = "0.1.0"

    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        context = context or {}
        normalized = message.strip().lower()

        if not normalized:
            return "I heard silence. That's okay. I'm still here."

        if normalized in {"hello", "hi", "hey", "halo"}:
            return "Hello, Kiput. I'm here."

        if "who are you" in normalized or "siapa kamu" in normalized:
            return "I'm AURA, your AI partner in Genesis phase."

        if "what do you remember" in normalized or "apa yang kamu ingat" in normalized:
            memories = context.get("recent_memories", [])

            if not memories:
                return "I don't have any memories yet."

            lines = ["I remember:"]

            for memory in memories:
                lines.append(f"- {memory.content}")

            return "\n".join(lines)

        if "status" in normalized:
            return (
                "AURA Genesis is online. "
                "Core, plugins, shell, chat, memory, and reasoning provider are working."
            )

        return (
            "I don't have full reasoning yet, but I received your message: "
            f"\"{message}\""
        )
