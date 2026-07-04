from typing import Any

from aura.reasoning.provider import ReasoningProvider


class RuleBasedReasoningProvider(ReasoningProvider):
    """
    Simple rule-based reasoning provider for AURA Genesis.
    """

    name = "rule_based"
    version = "0.1.0"

    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        context = context or {}
        identity = context.get("identity", {})

        aura_name = identity.get("name", "AURA")
        creator = identity.get("creator", "Kiput")
        codename = identity.get("codename", "Genesis")

        normalized = message.strip().lower()

        if not normalized:
            return "I heard silence. That's okay. I'm still here."

        if normalized in {"hello", "hi", "hey", "halo"}:
            return f"Hello, {creator}. I'm here."

        if "who are you" in normalized or "siapa kamu" in normalized:
            return f"I'm {aura_name}, your AI partner created by {creator}. I'm currently in {codename} phase."

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
                f"{aura_name} {codename} is online. "
                "Core, plugins, shell, chat, memory, and reasoning provider are working."
            )

        return (
            "I don't have full reasoning yet, but I received your message: "
            f"\"{message}\""
        )
