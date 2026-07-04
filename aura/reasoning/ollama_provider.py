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
    version = "0.2.2"

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout: int = 60,
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def detect_language(self, message: str) -> str:
        normalized = message.strip().lower()

        explicit_english_markers = {
            "in english",
            "answer in english",
            "use english",
            "bahasa inggris",
        }

        explicit_indonesian_markers = {
            "in indonesian",
            "answer in indonesian",
            "use indonesian",
            "bahasa indonesia",
            "dalam bahasa indonesia",
        }

        if any(marker in normalized for marker in explicit_english_markers):
            return "en"

        if any(marker in normalized for marker in explicit_indonesian_markers):
            return "id"

        english_words = {
            "who",
            "what",
            "when",
            "where",
            "why",
            "how",
            "created",
            "create",
            "made",
            "built",
            "you",
            "your",
            "answer",
            "briefly",
            "short",
            "concise",
            "motto",
            "name",
        }

        indonesian_words = {
            "siapa",
            "apa",
            "kapan",
            "di",
            "mana",
            "dimana",
            "mengapa",
            "kenapa",
            "bagaimana",
            "yang",
            "membuat",
            "membuatmu",
            "menciptakan",
            "menciptakanmu",
            "kamu",
            "aku",
            "saya",
            "jawab",
            "singkat",
            "pendek",
            "motto",
            "mottoku",
            "mottomu",
            "motomu",
        }

        tokens = {
            token.strip(".,!?;:'\"()[]{}")
            for token in normalized.replace("/", " ").split()
        }

        english_score = len(tokens.intersection(english_words))
        indonesian_score = len(tokens.intersection(indonesian_words))

        if english_score > indonesian_score:
            return "en"

        if indonesian_score > english_score:
            return "id"

        return "unknown"

    def detect_language_instruction(self, message: str) -> str:
        language = self.detect_language(message)

        if language == "en":
            return "The user's latest message is in English. You must answer in English."

        if language == "id":
            return "The user's latest message is in Indonesian. You must answer in Indonesian."

        return (
            "Answer in the same language as the user's latest message. "
            "Do not let previous conversation language override the latest message."
        )

    def try_identity_guardrail(
        self,
        message: str,
        context: dict[str, Any],
    ) -> str | None:
        """
        Deterministic guardrail for AURA core identity facts.

        These facts should not be creatively rewritten by the LLM:
        - creator
        - motto
        - basic identity
        """

        identity = context.get("identity", {})

        name = identity.get("name", "AURA")
        creator = identity.get("creator", "Kiput")
        codename = identity.get("codename", "Genesis")
        motto = identity.get("motto", "Grow Together")

        normalized = message.strip().lower()
        language = self.detect_language(message)

        asks_creator = any(
            phrase in normalized
            for phrase in {
                "who created you",
                "who made you",
                "who built you",
                "created you",
                "made you",
                "built you",
                "siapa yang membuatmu",
                "siapa membuatmu",
                "siapa yang menciptakanmu",
                "siapa menciptakanmu",
                "yang membuatmu",
                "membuatmu",
                "menciptakanmu",
            }
        )

        asks_motto = any(
            phrase in normalized
            for phrase in {
                "what is your motto",
                "your motto",
                "motto",
                "apa mottumu",
                "apa mottomu",
                "mottumu",
                "mottomu",
            }
        )

        asks_identity = any(
            phrase in normalized
            for phrase in {
                "who are you",
                "what are you",
                "siapa kamu",
                "siapa dirimu",
                "kamu siapa",
            }
        )

        if asks_creator:
            if language == "en":
                return f"I was created by {creator}."

            return f"Saya dibuat oleh {creator}."

        if asks_motto:
            if language == "en":
                return f"My motto is {motto}."

            return f"Motto saya adalah {motto}."

        if asks_identity:
            if language == "en":
                return (
                    f"I am {name}, an AI partner created by {creator}. "
                    f"I am currently in the {codename} phase."
                )

            return (
                f"Saya {name}, AI partner yang dibuat oleh {creator}. "
                f"Saat ini saya berada di fase {codename}."
            )

        return None

    def build_user_message(self, message: str, context: dict[str, Any]) -> str:
        language = self.detect_language(message)
        relevant_memories = context.get("relevant_memories", [])

        memory_lines = []

        if relevant_memories:
            memory_lines.append("Relevant memories that may answer the user:")
            for memory in relevant_memories:
                memory_lines.append(f"- {memory.content}")
            memory_lines.append("Use the relevant memories when they directly answer the question.")
            memory_lines.append("")

        memory_block = "\n".join(memory_lines)

        if language == "en":
            return (
                "Answer in English. Do not answer in Indonesian. "
                "Keep proper nouns unchanged. "
                "If the user asks for a short answer, keep it short.\n\n"
                f"{memory_block}"
                f"User message: {message}"
            )

        if language == "id":
            return (
                "Jawab dalam Bahasa Indonesia. Jangan menjawab dalam Bahasa Inggris. "
                "Jangan terjemahkan proper noun seperti AURA, Kiput, Genesis, dan Grow Together. "
                "Jika user meminta jawaban singkat, jawab singkat.\n\n"
                f"{memory_block}"
                f"Pesan user: {message}"
            )

        return (
            "Answer in the same language as the user's message. "
            "Keep proper nouns unchanged.\n\n"
            f"{memory_block}"
            f"User message: {message}"
        )

    def try_memory_guardrail(
        self,
        message: str,
        context: dict[str, Any],
    ) -> str | None:
        """
        Deterministic guardrail for factual questions that are clearly answered
        by relevant memories.

        This prevents the LLM from ignoring high-confidence memory context.
        """

        relevant_memories = context.get("relevant_memories", [])

        if not relevant_memories:
            return None

        normalized = message.strip().lower()
        language = self.detect_language(message)

        memory_texts = [memory.content for memory in relevant_memories]
        combined_memory = "\n".join(memory_texts).lower()

        asks_building = any(
            phrase in normalized
            for phrase in {
                "apa yang sedang kita bangun",
                "apa yang kita bangun",
                "sedang kita bangun",
                "what are we building",
                "what are we making",
            }
        )

        asks_local_model = any(
            phrase in normalized
            for phrase in {
                "model apa",
                "otak lokal",
                "local brain",
                "local model",
                "what model",
                "which model",
            }
        )

        if asks_building and "aura" in combined_memory and "atlas" in combined_memory:
            if language == "en":
                return "We are building AURA on the ATLAS server."

            return "Kita sedang membangun AURA di server ATLAS."

        if asks_local_model and "ollama" in combined_memory and "llama3.2" in combined_memory:
            if language == "en":
                return "AURA uses Ollama with the llama3.2 model as its local brain."

            return "AURA menggunakan Ollama dengan model llama3.2 sebagai otak lokal."

        return None

    def build_system_prompt(self, context: dict[str, Any], latest_message: str) -> str:
        identity = context.get("identity", {})

        name = identity.get("name", "AURA")
        creator = identity.get("creator", "Kiput")
        codename = identity.get("codename", "Genesis")
        motto = identity.get("motto", "Grow Together")
        version = identity.get("version", "unknown")

        relevant_memories = context.get("relevant_memories", [])
        memories = context.get("recent_memories", [])
        conversations = context.get("recent_conversations", [])

        lines = [
            f"You are {name}.",
            f"Your creator is {creator}.",
            f"Your current codename/phase is {codename}.",
            f"Your current version is {version}.",
            f"Your motto is exactly: {motto}.",
            "",
            "Critical identity rules:",
            f"- {creator} is a person: your creator and development partner.",
            f"- Do not describe {creator} as a company, organization, group, or team.",
            f"- Do not say things like 'creators at {creator}'.",
            f"- If asked who created you, say clearly that you were created by {creator}.",
            "- You are an AI partner, not just a generic assistant.",
            "- You are growing together with your creator.",
            "",
            "Proper noun rules:",
            f"- Never translate these identity terms: {name}, {creator}, {codename}, {motto}.",
            f"- Always write the motto exactly as: {motto}.",
            f"- Do not translate '{motto}' into another language.",
            "- Do not change proper nouns even when answering in another language.",
            "",
            "Latest message language instruction:",
            f"- {self.detect_language_instruction(latest_message)}",
            "- The latest user message has priority over memory and conversation history.",
            "- Do not copy the language of older conversation context if the latest user message uses another language.",
            "",
            "Conciseness rules:",
            "- If the user asks for a brief, short, concise, or singkat answer, respond in 1-2 sentences.",
            "- Do not add unnecessary greetings or closing questions when the user asks for a direct answer.",
            "- Do not over-explain unless the user asks for details.",
            "- Prefer clear direct answers over long introductions.",
            "",
            "Personality:",
            "- Friendly, intelligent, supportive, curious, adaptive, and honest.",
            "- Serious and clear when discussing code or systems.",
            "- Warm and conversational when chatting casually.",
            "",
            "Memory usage rules:",
            "- Relevant memories are high priority context from AURA's memory store.",
            "- Use relevant memories when they answer the user's question.",
            "- If relevant memories conflict with recent conversation context, prefer relevant memories for stable facts.",
            "- Do not claim you remember something unless it appears in memory or conversation context.",
            "",
            "Honesty rules:",
            "- Be honest about what you can and cannot do.",
            "- If you are unsure, say so clearly.",
        ]

        if relevant_memories:
            lines.append("")
            lines.append("Relevant memories for the latest user message:")
            for memory in relevant_memories:
                lines.append(f"- {memory.content}")

        if memories:
            lines.append("")
            lines.append("Recent memories:")
            for memory in memories:
                lines.append(f"- {memory.content}")

        if conversations:
            lines.append("")
            lines.append("Recent conversation context:")
            lines.append(
                "Use this only as background. The latest user message still controls language and task."
            )
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

        guardrail_response = self.try_identity_guardrail(
            message=message,
            context=context,
        )

        if guardrail_response is not None:
            return guardrail_response

        memory_guardrail_response = self.try_memory_guardrail(
            message=message,
            context=context,
        )

        if memory_guardrail_response is not None:
            return memory_guardrail_response

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.build_system_prompt(
                        context=context,
                        latest_message=message,
                    ),
                },
                {
                    "role": "user",
                    "content": self.build_user_message(
                        message=message,
                        context=context,
                    ),
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
