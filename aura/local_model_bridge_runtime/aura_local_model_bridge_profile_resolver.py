"""Environment-only profile resolution for Sprint 187."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeConfigurationError,
)


class AuraLocalModelBridgeProfileResolver:
    """Resolve a strict non-persistent local provider profile."""

    ENV_PREFIX = "AURA_LOCAL_MODEL_"
    ENV_KEYS = {
        "AURA_LOCAL_MODEL_PROVIDER",
        "AURA_LOCAL_MODEL_BASE_URL",
        "AURA_LOCAL_MODEL_NAME",
        "AURA_LOCAL_MODEL_ENABLED",
        "AURA_LOCAL_MODEL_TIMEOUT_SECONDS",
        "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS",
        "AURA_LOCAL_MODEL_TEMPERATURE",
    }

    @staticmethod
    def _parse_boolean(value: str, *, key: str) -> bool:
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
        raise LocalModelBridgeConfigurationError(
            f"{key} must be exactly true or false."
        )

    @classmethod
    def resolve(
        cls,
        environ: Mapping[str, str],
    ) -> dict[str, Any] | None:
        present = {
            key: value
            for key, value in environ.items()
            if key.startswith(cls.ENV_PREFIX)
        }
        if not present:
            return None

        unknown = set(present) - cls.ENV_KEYS
        if unknown:
            raise LocalModelBridgeConfigurationError(
                "Unknown local model environment keys: "
                + ", ".join(sorted(unknown))
            )

        provider = present.get("AURA_LOCAL_MODEL_PROVIDER")
        model = present.get("AURA_LOCAL_MODEL_NAME")
        if provider is None or not provider.strip():
            raise LocalModelBridgeConfigurationError(
                "AURA_LOCAL_MODEL_PROVIDER is required when local model "
                "configuration is present."
            )
        if model is None or not model.strip():
            raise LocalModelBridgeConfigurationError(
                "AURA_LOCAL_MODEL_NAME is required when local model "
                "configuration is present."
            )

        raw: dict[str, Any] = {
            "provider": provider,
            "model": model,
            "enabled": cls._parse_boolean(
                present.get(
                    "AURA_LOCAL_MODEL_ENABLED",
                    "false",
                ),
                key="AURA_LOCAL_MODEL_ENABLED",
            ),
        }

        if "AURA_LOCAL_MODEL_BASE_URL" in present:
            raw["base_url"] = present[
                "AURA_LOCAL_MODEL_BASE_URL"
            ]

        if "AURA_LOCAL_MODEL_TIMEOUT_SECONDS" in present:
            try:
                raw["timeout_seconds"] = float(
                    present[
                        "AURA_LOCAL_MODEL_TIMEOUT_SECONDS"
                    ]
                )
            except ValueError as exc:
                raise LocalModelBridgeConfigurationError(
                    "AURA_LOCAL_MODEL_TIMEOUT_SECONDS must be numeric."
                ) from exc

        if "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS" in present:
            try:
                raw["max_output_tokens"] = int(
                    present[
                        "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS"
                    ]
                )
            except ValueError as exc:
                raise LocalModelBridgeConfigurationError(
                    "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS must be an integer."
                ) from exc

        if "AURA_LOCAL_MODEL_TEMPERATURE" in present:
            try:
                raw["temperature"] = float(
                    present[
                        "AURA_LOCAL_MODEL_TEMPERATURE"
                    ]
                )
            except ValueError as exc:
                raise LocalModelBridgeConfigurationError(
                    "AURA_LOCAL_MODEL_TEMPERATURE must be numeric."
                ) from exc

        manager = AuraLocalModelBridgeRuntimeManager(raw)
        profile = manager._require_profile()
        return {
            "provider": profile.provider,
            "base_url": profile.base_url,
            "model": profile.model,
            "enabled": profile.enabled,
            "timeout_seconds": profile.timeout_seconds,
            "max_output_tokens": profile.max_output_tokens,
            "temperature": profile.temperature,
        }

    @classmethod
    def status(
        cls,
        environ: Mapping[str, str],
    ) -> dict[str, Any]:
        profile = cls.resolve(environ)
        return {
            "status": (
                "unconfigured"
                if profile is None
                else "configured"
            ),
            "configuration_source": "environment",
            "configured": profile is not None,
            "enabled": bool(
                profile is not None
                and profile["enabled"] is True
            ),
            "profile": profile,
            "persistent_configuration_write": False,
            "credential_configuration_supported": False,
        }

    @classmethod
    def self_test(cls) -> dict[str, Any]:
        assertions: dict[str, bool] = {}

        assertions["empty_resolves_none"] = (
            cls.resolve({}) is None
        )
        empty_status = cls.status({})
        assertions["empty_status_unconfigured"] = (
            empty_status["status"] == "unconfigured"
        )
        assertions["empty_status_source_env"] = (
            empty_status["configuration_source"]
            == "environment"
        )
        assertions["empty_no_persistence"] = (
            empty_status["persistent_configuration_write"]
            is False
        )
        assertions["empty_no_credentials"] = (
            empty_status["credential_configuration_supported"]
            is False
        )

        ollama = cls.resolve(
            {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "qwen2.5:3b",
                "AURA_LOCAL_MODEL_ENABLED": "true",
            }
        )
        assert ollama is not None
        assertions["ollama_provider"] = (
            ollama["provider"] == "ollama"
        )
        assertions["ollama_default_url"] = (
            ollama["base_url"]
            == "http://127.0.0.1:11434"
        )
        assertions["ollama_model"] = (
            ollama["model"] == "qwen2.5:3b"
        )
        assertions["ollama_enabled"] = (
            ollama["enabled"] is True
        )
        assertions["ollama_default_timeout"] = (
            ollama["timeout_seconds"] == 30.0
        )
        assertions["ollama_default_tokens"] = (
            ollama["max_output_tokens"] == 512
        )
        assertions["ollama_default_temperature"] = (
            ollama["temperature"] == 0.2
        )

        openai = cls.resolve(
            {
                "AURA_LOCAL_MODEL_PROVIDER": (
                    "openai_compatible"
                ),
                "AURA_LOCAL_MODEL_BASE_URL": (
                    "http://localhost:8080"
                ),
                "AURA_LOCAL_MODEL_NAME": "local-instruct",
                "AURA_LOCAL_MODEL_ENABLED": "false",
                "AURA_LOCAL_MODEL_TIMEOUT_SECONDS": "20",
                "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS": "700",
                "AURA_LOCAL_MODEL_TEMPERATURE": "0.45",
            }
        )
        assert openai is not None
        assertions["openai_provider"] = (
            openai["provider"] == "openai_compatible"
        )
        assertions["openai_url"] = (
            openai["base_url"]
            == "http://localhost:8080"
        )
        assertions["openai_disabled"] = (
            openai["enabled"] is False
        )
        assertions["openai_timeout"] = (
            openai["timeout_seconds"] == 20.0
        )
        assertions["openai_tokens"] = (
            openai["max_output_tokens"] == 700
        )
        assertions["openai_temperature"] = (
            openai["temperature"] == 0.45
        )

        invalid_cases = {
            "unknown_key": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_API_KEY": "secret",
            },
            "missing_provider": {
                "AURA_LOCAL_MODEL_NAME": "model",
            },
            "missing_model": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
            },
            "bad_enabled": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_ENABLED": "yes",
            },
            "bad_timeout": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_TIMEOUT_SECONDS": "abc",
            },
            "bad_tokens": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS": "1.5",
            },
            "bad_temperature": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_TEMPERATURE": "abc",
            },
            "remote_url": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_BASE_URL": (
                    "http://192.168.1.10:11434"
                ),
            },
            "https_url": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_BASE_URL": (
                    "https://127.0.0.1:11434"
                ),
            },
            "credential_url": {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_NAME": "model",
                "AURA_LOCAL_MODEL_BASE_URL": (
                    "http://user:pass@127.0.0.1:11434"
                ),
            },
        }
        for label, environ in invalid_cases.items():
            caught = False
            try:
                cls.resolve(environ)
            except LocalModelBridgeConfigurationError:
                caught = True
            assertions[f"invalid_{label}_blocked"] = caught

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise LocalModelBridgeConfigurationError(
                "Local model profile resolver self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": "aura_local_model_bridge_profile_resolver",
            "sprint": 187,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "environment_resolution_verified": True,
            "default_values_verified": True,
            "strict_boolean_verified": True,
            "numeric_parsing_verified": True,
            "unknown_keys_blocked": True,
            "credential_keys_blocked": True,
            "remote_urls_blocked": True,
            "persistent_configuration_write": False,
        }
