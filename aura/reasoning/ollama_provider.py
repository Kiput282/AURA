import json
import urllib.error
import urllib.request
from typing import Any

from aura.reasoning.provider import ReasoningProvider


class OllamaReasoningProvider(ReasoningProvider):
    """
    Ollama reasoning provider for AURA.

    This provider talks to a local Ollama server through HTTP.

    Default endpoint:
    - http://localhost:11434/api/chat
    """

    name = "ollama"
    version = "0.1.0"

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout: int = 60,
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def build_system_prompt(self, context: dict[str, Any]) -> str:
        memories = context.get("recent_memories", [])

        lines = [
            "You are AURA, an AI partner created by Kiput.",
            "Your motto is Grow Together.",
            "You are currently in Genesis phase.",
            "Be helpful, honest, supportive, and concise.",
        ]

        if memories:
            lines.append("")
            lines.append("Recent memories:")
            for memory in memories:
                lines.append(f"- {memory.content}")

        return "\n".join(lines)

    def respond(self, message: str, context: dict[str, Any] | None = None) -> str:
        context = context or {}

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.build_system_prompt(context),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            "stream": False,
        }

        request = urllib.request.Request(
            url=f"{self.host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw_body = response.read().decode("utf-8")
                data = json.loads(raw_body)

            assistant_message = data.get("message", {})
            content = assistant_message.get("content", "").strip()

            if not content:
                return "[ollama] I received an empty response from the local model."

            return content

        except urllib.error.URLError as error:
            return (
                "[ollama] Ollama is not available yet. "
                f"Make sure Ollama is running at {self.host} "
                f"and model '{self.model}' is installed. "
                f"Error: {error}"
            )

        except Exception as error:
            return f"[ollama] Failed to generate response: {error}"
