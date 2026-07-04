from pathlib import Path
from typing import Any

import yaml
from loguru import logger

from aura.reasoning.local_stub_provider import LocalStubReasoningProvider
from aura.reasoning.ollama_provider import OllamaReasoningProvider
from aura.reasoning.provider import ReasoningProvider
from aura.reasoning.rule_based_provider import RuleBasedReasoningProvider


class ReasoningProviderFactory:
    """
    Creates reasoning providers based on AURA configuration.

    Current supported providers:
    - rule_based
    - local_stub
    - ollama

    Future providers:
    - openai
    - lm_studio
    - local_llm
    """

    @staticmethod
    def from_name(
        provider_name: str,
        config: dict[str, Any] | None = None,
    ) -> ReasoningProvider:
        config = config or {}
        normalized_name = provider_name.strip().lower()

        if normalized_name in {"rule_based", "rules", "genesis"}:
            logger.info("Reasoning provider selected: rule_based")
            return RuleBasedReasoningProvider()

        if normalized_name in {"local_stub", "local", "stub"}:
            logger.info("Reasoning provider selected: local_stub")
            return LocalStubReasoningProvider()

        if normalized_name in {"ollama", "ollama_local"}:
            host = config.get("host", "http://localhost:11434")
            model = config.get("model", "llama3.2")
            timeout = int(config.get("timeout", 60))

            logger.info(
                f"Reasoning provider selected: ollama "
                f"host={host} model={model}"
            )

            return OllamaReasoningProvider(
                host=host,
                model=model,
                timeout=timeout,
            )

        raise ValueError(f"Unsupported reasoning provider: {provider_name}")

    @staticmethod
    def from_settings(project_root: Path) -> ReasoningProvider:
        settings_path = project_root / "aura" / "config" / "settings.yaml"

        if not settings_path.exists():
            logger.warning("settings.yaml not found. Falling back to rule_based provider.")
            return RuleBasedReasoningProvider()

        with settings_path.open("r", encoding="utf-8") as file:
            settings = yaml.safe_load(file) or {}

        reasoning_config = settings.get("reasoning", {})
        provider_name = reasoning_config.get("provider", "rule_based")

        return ReasoningProviderFactory.from_name(
            provider_name=provider_name,
            config=reasoning_config,
        )
