from typing import Any

from aura.reasoning.provider import ReasoningProvider


class LocalStubReasoningProvider(ReasoningProvider):
    """
    Local model stub provider for AURA Genesis.

    This does not run a real local LLM yet.
    It exists to prove that AURA can switch reasoning providers through config.
    """

    name = "local_stub"
    version = "0.1.0"

    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        context = context or {}
        normalized = message.strip().lower()

        if not normalized:
            return "[local_stub] I received silence, but I am online."

        if normalized in {"hello", "hi", "hey", "halo"}:
            return "[local_stub] Hello, Kiput. Local reasoning stub is online."

        if "who are you" in normalized or "siapa kamu" in normalized:
            return "[local_stub] I am AURA running through the local_stub provider."

        if "what do you remember" in normalized or "apa yang kamu ingat" in normalized:
            memories = context.get("recent_memories", [])

            if not memories:
                return "[local_stub] I do not have memory records yet."

            lines = ["[local_stub] I can access these recent memories:"]
            for memory in memories:
                lines.append(f"- {memory.content}")

            return "\n".join(lines)

        if "status" in normalized:
            return (
                "[local_stub] AURA Genesis is online. "
                "Provider switching works through settings.yaml."
            )

        return (
            "[local_stub] I am not a real LLM yet, but I received your message: "
            f"\"{message}\""
        )
