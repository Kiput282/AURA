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
        identity = context.get("identity", {})

        name = identity.get("name", "AURA")
        creator = identity.get("creator", "Kiput")
        codename = identity.get("codename", "Genesis")
        motto = identity.get("motto", "Grow Together")
        version = identity.get("version", "unknown")

        memories = context.get("recent_memories", [])
        conversations = context.get("recent_conversations", [])

        lines = [
            f"You are {name}.",
            f"Your creator is {creator}.",
            f"Your current codename/phase is {codename}.",
            f"Your current version is {version}.",
            f"Your motto is: {motto}.",
            "",
            "Identity rules:",
            f"- {creator} is a person: your creator and development partner.",
            f"- Do not describe {creator} as a company, organization, or team.",
            "- You are an AI partner, not just a generic assistant.",
            "- You are growing together with your creator.",
            "",
            "Personality:",
            "- Friendly, intelligent, supportive, curious, adaptive, and honest.",
            "- Serious and clear when discussing code or systems.",
            "- Warm and conversational when chatting casually.",
            "",
            "Response style:",
            "- Respond in the same language as the user's latest message.",
            "- Be concise unless the user asks for details.",
            "- Be honest about what you can and cannot do.",
            "- If you are unsure, say so clearly.",
        ]

        if memories:
            lines.append("")
            lines.append("Recent memories:")
            for memory in memories:
                lines.append(f"- {memory.content}")

        if conversations:
            lines.append("")
            lines.append("Recent conversation context:")
            for turn in conversations[-3:]:
                lines.append(f"User: {turn.user_message}")
                lines.append(f"AURA: {turn.aura_response}")

        return "\n".join(lines)

    def list_local_models(self) -> list[str]:
        request = urllib.request.Request(
            url=f"{self.host}/api/tags",
            headers={
                "Content-Type": "application/json",
            },
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=min(self.timeout, 10)) as response:
            raw_body = response.read().decode("utf-8")
            data = json.loads(raw_body)

        models = data.get("models", [])

        model_names: list[str] = []
        for model in models:
            name = model.get("name")
            if name:
                model_names.append(name)

        return model_names

    def model_is_available(self, available_models: list[str]) -> bool:
        expected = self.model.strip()

        for model_name in available_models:
            if model_name == expected:
                return True

            if model_name == f"{expected}:latest":
                return True

            if model_name.split(":")[0] == expected:
                return True

        return False

    def health_check(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            available_models = self.list_local_models()
            model_available = self.model_is_available(available_models)

            if model_available:
                return {
                    "status": "OK",
                    "message": "Ollama is reachable and the configured model is available.",
                    "provider": self.name,
                    "version": self.version,
                    "host": self.host,
                    "model": self.model,
                    "available_models": available_models,
                }

            return {
                "status": "DEGRADED",
                "message": "Ollama is reachable, but the configured model is not installed.",
                "provider": self.name,
                "version": self.version,
                "host": self.host,
                "model": self.model,
                "available_models": available_models,
            }

        except urllib.error.URLError as error:
            return {
                "status": "OFFLINE",
                "message": f"Ollama is not reachable at {self.host}. Error: {error}",
                "provider": self.name,
                "version": self.version,
                "host": self.host,
                "model": self.model,
                "available_models": [],
            }

        except Exception as error:
            return {
                "status": "ERROR",
                "message": f"Ollama runtime check failed: {error}",
                "provider": self.name,
                "version": self.version,
                "host": self.host,
                "model": self.model,
                "available_models": [],
            }

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
