"""AURA Sprint 187 Local Model Bridge Runtime core.

The bridge supports bounded localhost-only model requests for Ollama and
OpenAI-compatible local servers. It never downloads models, falls back to the
internet, executes tools, dispatches actions, runs commands, reads arbitrary
files, or writes AURA long-term memory.
"""

from __future__ import annotations

import ipaddress
import json
import re
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit


class LocalModelBridgeError(RuntimeError):
    """Base error for the local model bridge runtime."""


class LocalModelBridgeConfigurationError(LocalModelBridgeError):
    """Raised when a provider profile violates the local safety contract."""


class LocalModelBridgePermissionError(LocalModelBridgeError):
    """Raised when explicit local model permission is absent."""


class LocalModelBridgeValidationError(LocalModelBridgeError):
    """Raised when a model request violates schema or size limits."""


class LocalModelBridgeTransportError(LocalModelBridgeError):
    """Raised when a local provider cannot be reached safely."""


class LocalModelBridgeResponseError(LocalModelBridgeError):
    """Raised when a provider returns an invalid or unsafe response envelope."""


@dataclass(frozen=True)
class LocalModelProviderProfile:
    """Validated local model provider configuration."""

    provider: str
    base_url: str
    model: str
    enabled: bool = False
    timeout_seconds: float = 30.0
    max_output_tokens: int = 512
    temperature: float = 0.2


@dataclass(frozen=True)
class LocalModelTransportResponse:
    """Raw response returned by the HTTP transport boundary."""

    status_code: int
    headers: Mapping[str, str]
    body: bytes


TransportCallable = Callable[
    [str, str, bytes | None, Mapping[str, str], float],
    LocalModelTransportResponse,
]


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject every provider redirect instead of following it."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Mapping[str, str],
        newurl: str,
    ) -> None:
        return None


class LocalhostHTTPTransport:
    """Minimal stdlib HTTP transport used only after URL validation."""

    user_agent = "AURA-Local-Model-Bridge/0.1"

    @staticmethod
    def _enforce_resolved_loopback(url: str) -> None:
        parsed = urlsplit(url)
        hostname = parsed.hostname
        try:
            port = parsed.port
        except ValueError as exc:
            raise LocalModelBridgeTransportError(
                "The local provider URL contains an invalid port."
            ) from exc

        if hostname is None or port is None:
            raise LocalModelBridgeTransportError(
                "The local provider URL is missing host or port."
            )

        try:
            addresses = socket.getaddrinfo(
                hostname,
                port,
                type=socket.SOCK_STREAM,
            )
        except socket.gaierror as exc:
            raise LocalModelBridgeTransportError(
                "The local provider hostname could not be resolved."
            ) from exc

        if not addresses:
            raise LocalModelBridgeTransportError(
                "The local provider hostname resolved to no addresses."
            )

        for result in addresses:
            raw_address = str(result[4][0]).split("%", 1)[0]
            try:
                address = ipaddress.ip_address(raw_address)
            except ValueError as exc:
                raise LocalModelBridgeTransportError(
                    "The local provider resolved to an invalid IP address."
                ) from exc
            if not address.is_loopback:
                raise LocalModelBridgeTransportError(
                    "The local provider resolved outside the loopback interface."
                )

    def __call__(
        self,
        method: str,
        url: str,
        body: bytes | None,
        headers: Mapping[str, str],
        timeout_seconds: float,
    ) -> LocalModelTransportResponse:
        self._enforce_resolved_loopback(url)

        request_headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
            **dict(headers),
        }
        request = urllib.request.Request(
            url,
            method=method,
            data=body,
            headers=request_headers,
        )
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            _NoRedirectHandler(),
        )
        try:
            with opener.open(
                request,
                timeout=timeout_seconds,
            ) as response:
                return LocalModelTransportResponse(
                    status_code=int(response.status),
                    headers=dict(response.headers.items()),
                    body=response.read(),
                )
        except urllib.error.HTTPError as exc:
            return LocalModelTransportResponse(
                status_code=int(exc.code),
                headers=dict(exc.headers.items()),
                body=exc.read(),
            )
        except (
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
            OSError,
        ) as exc:
            raise LocalModelBridgeTransportError(
                "The configured local model provider could not be reached: "
                f"{type(exc).__name__}."
            ) from exc


class AuraLocalModelBridgeRuntimeManager:
    """Validate, probe, and invoke one explicitly configured local model."""

    name = "aura_local_model_bridge_runtime"
    component_version = "0.1.0-alpha"
    sprint = 187
    schema_version = "1.0"

    SUPPORTED_PROVIDERS = (
        "ollama",
        "openai_compatible",
    )
    DEFAULT_BASE_URLS = {
        "ollama": "http://127.0.0.1:11434",
        "openai_compatible": "http://127.0.0.1:8080",
    }
    PROBE_PATHS = {
        "ollama": "/api/tags",
        "openai_compatible": "/v1/models",
    }
    GENERATE_PATHS = {
        "ollama": "/api/chat",
        "openai_compatible": "/v1/chat/completions",
    }

    MAX_MESSAGES = 64
    MAX_MESSAGE_CHARS = 8192
    MAX_TOTAL_INPUT_CHARS = 131072
    MAX_REQUEST_BODY_BYTES = 262144
    MAX_RESPONSE_BODY_BYTES = 1048576
    MAX_OUTPUT_CHARS = 32768
    MIN_TIMEOUT_SECONDS = 1.0
    MAX_TIMEOUT_SECONDS = 120.0
    MIN_OUTPUT_TOKENS = 1
    MAX_OUTPUT_TOKENS = 8192
    MIN_TEMPERATURE = 0.0
    MAX_TEMPERATURE = 2.0

    _MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}$")
    _REQUEST_ID_RE = re.compile(r"^modelreq_[A-Za-z0-9_-]{1,96}$")
    _ALLOWED_ROLES = {"system", "user", "assistant"}
    _LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}

    def __init__(
        self,
        profile: LocalModelProviderProfile | Mapping[str, Any] | None = None,
        *,
        transport: TransportCallable | None = None,
        monotonic_factory: Callable[[], float] | None = None,
    ) -> None:
        self._transport = transport or LocalhostHTTPTransport()
        self._monotonic = monotonic_factory or time.monotonic
        self._profile = (
            self._coerce_profile(profile)
            if profile is not None
            else None
        )

    @classmethod
    def _validate_base_url(cls, base_url: Any) -> str:
        if not isinstance(base_url, str):
            raise LocalModelBridgeConfigurationError(
                "base_url must be a string."
            )

        candidate = base_url.strip()
        if not candidate:
            raise LocalModelBridgeConfigurationError(
                "base_url must not be empty."
            )

        parsed = urlsplit(candidate)
        if parsed.scheme.lower() != "http":
            raise LocalModelBridgeConfigurationError(
                "Only plain HTTP is allowed for loopback-local providers."
            )
        if parsed.username is not None or parsed.password is not None:
            raise LocalModelBridgeConfigurationError(
                "Provider URLs must not contain credentials."
            )
        if parsed.query or parsed.fragment:
            raise LocalModelBridgeConfigurationError(
                "Provider base URLs must not contain query or fragment data."
            )
        if parsed.path not in ("", "/"):
            raise LocalModelBridgeConfigurationError(
                "Provider base URLs must not contain an application path."
            )

        hostname = parsed.hostname
        if hostname is None or hostname.lower() not in cls._LOCAL_HOSTS:
            raise LocalModelBridgeConfigurationError(
                "Provider hostname must be localhost, 127.0.0.1, or ::1."
            )

        try:
            port = parsed.port
        except ValueError as exc:
            raise LocalModelBridgeConfigurationError(
                "Provider port is invalid."
            ) from exc

        if port is None or not (1 <= port <= 65535):
            raise LocalModelBridgeConfigurationError(
                "Provider base URL must include a valid explicit port."
            )

        host_text = (
            f"[{hostname}]"
            if ":" in hostname
            else hostname.lower()
        )
        return urlunsplit(
            (
                "http",
                f"{host_text}:{port}",
                "",
                "",
                "",
            )
        )

    @classmethod
    def _validate_model(cls, model: Any) -> str:
        if not isinstance(model, str):
            raise LocalModelBridgeConfigurationError(
                "model must be a string."
            )
        normalized = model.strip()
        if not cls._MODEL_RE.fullmatch(normalized):
            raise LocalModelBridgeConfigurationError(
                "model must be 1-128 safe provider identifier characters."
            )
        return normalized

    @classmethod
    def _coerce_profile(
        cls,
        profile: LocalModelProviderProfile | Mapping[str, Any],
    ) -> LocalModelProviderProfile:
        if isinstance(profile, LocalModelProviderProfile):
            raw = {
                "provider": profile.provider,
                "base_url": profile.base_url,
                "model": profile.model,
                "enabled": profile.enabled,
                "timeout_seconds": profile.timeout_seconds,
                "max_output_tokens": profile.max_output_tokens,
                "temperature": profile.temperature,
            }
        elif isinstance(profile, Mapping):
            raw = dict(profile)
        else:
            raise LocalModelBridgeConfigurationError(
                "profile must be a LocalModelProviderProfile or mapping."
            )

        allowed = {
            "provider",
            "base_url",
            "model",
            "enabled",
            "timeout_seconds",
            "max_output_tokens",
            "temperature",
        }
        unknown = set(raw) - allowed
        if unknown:
            raise LocalModelBridgeConfigurationError(
                "Unknown provider profile fields: "
                + ", ".join(sorted(unknown))
            )

        provider = raw.get("provider")
        if not isinstance(provider, str):
            raise LocalModelBridgeConfigurationError(
                "provider must be a string."
            )
        provider = provider.strip().lower()
        if provider not in cls.SUPPORTED_PROVIDERS:
            raise LocalModelBridgeConfigurationError(
                "provider must be ollama or openai_compatible."
            )

        base_url = raw.get(
            "base_url",
            cls.DEFAULT_BASE_URLS[provider],
        )
        model = cls._validate_model(raw.get("model"))

        enabled = raw.get("enabled", False)
        if not isinstance(enabled, bool):
            raise LocalModelBridgeConfigurationError(
                "enabled must be boolean."
            )

        timeout = raw.get("timeout_seconds", 30.0)
        if isinstance(timeout, bool) or not isinstance(
            timeout,
            (int, float),
        ):
            raise LocalModelBridgeConfigurationError(
                "timeout_seconds must be numeric."
            )
        timeout = float(timeout)
        if not (
            cls.MIN_TIMEOUT_SECONDS
            <= timeout
            <= cls.MAX_TIMEOUT_SECONDS
        ):
            raise LocalModelBridgeConfigurationError(
                "timeout_seconds is outside the allowed range."
            )

        max_tokens = raw.get("max_output_tokens", 512)
        if isinstance(max_tokens, bool) or not isinstance(
            max_tokens,
            int,
        ):
            raise LocalModelBridgeConfigurationError(
                "max_output_tokens must be an integer."
            )
        if not (
            cls.MIN_OUTPUT_TOKENS
            <= max_tokens
            <= cls.MAX_OUTPUT_TOKENS
        ):
            raise LocalModelBridgeConfigurationError(
                "max_output_tokens is outside the allowed range."
            )

        temperature = raw.get("temperature", 0.2)
        if isinstance(temperature, bool) or not isinstance(
            temperature,
            (int, float),
        ):
            raise LocalModelBridgeConfigurationError(
                "temperature must be numeric."
            )
        temperature = float(temperature)
        if not (
            cls.MIN_TEMPERATURE
            <= temperature
            <= cls.MAX_TEMPERATURE
        ):
            raise LocalModelBridgeConfigurationError(
                "temperature is outside the allowed range."
            )

        return LocalModelProviderProfile(
            provider=provider,
            base_url=cls._validate_base_url(base_url),
            model=model,
            enabled=enabled,
            timeout_seconds=timeout,
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

    @staticmethod
    def _decode_json(
        response: LocalModelTransportResponse,
        *,
        context: str,
    ) -> dict[str, Any]:
        if len(response.body) > (
            AuraLocalModelBridgeRuntimeManager.MAX_RESPONSE_BODY_BYTES
        ):
            raise LocalModelBridgeResponseError(
                f"{context} response exceeds the body limit."
            )
        try:
            payload = json.loads(response.body.decode("utf-8"))
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise LocalModelBridgeResponseError(
                f"{context} response is not valid UTF-8 JSON."
            ) from exc
        if not isinstance(payload, dict):
            raise LocalModelBridgeResponseError(
                f"{context} response must be a JSON object."
            )
        return payload

    @staticmethod
    def _normalize_message_content(content: Any) -> str:
        if not isinstance(content, str):
            raise LocalModelBridgeValidationError(
                "message content must be a string."
            )
        normalized = content.strip()
        if not normalized:
            raise LocalModelBridgeValidationError(
                "message content must not be empty."
            )
        if len(normalized) > (
            AuraLocalModelBridgeRuntimeManager.MAX_MESSAGE_CHARS
        ):
            raise LocalModelBridgeValidationError(
                "message content exceeds the per-message character limit."
            )
        invalid_controls = [
            character
            for character in normalized
            if ord(character) < 32
            and character not in ("\n", "\t")
        ]
        if invalid_controls:
            raise LocalModelBridgeValidationError(
                "message content contains a disallowed control character."
            )
        return normalized

    @classmethod
    def _validate_messages(
        cls,
        messages: Any,
    ) -> list[dict[str, str]]:
        if isinstance(messages, (str, bytes)) or not isinstance(
            messages,
            Sequence,
        ):
            raise LocalModelBridgeValidationError(
                "messages must be a sequence of message objects."
            )
        if not messages:
            raise LocalModelBridgeValidationError(
                "messages must not be empty."
            )
        if len(messages) > cls.MAX_MESSAGES:
            raise LocalModelBridgeValidationError(
                "message count exceeds the bridge limit."
            )

        normalized: list[dict[str, str]] = []
        total_chars = 0
        system_count = 0
        user_count = 0

        for index, message in enumerate(messages):
            if not isinstance(message, Mapping):
                raise LocalModelBridgeValidationError(
                    "each message must be an object."
                )
            if set(message) != {"role", "content"}:
                raise LocalModelBridgeValidationError(
                    "each message must contain only role and content."
                )

            role = message["role"]
            if not isinstance(role, str):
                raise LocalModelBridgeValidationError(
                    "message role must be a string."
                )
            role = role.strip().lower()
            if role not in cls._ALLOWED_ROLES:
                raise LocalModelBridgeValidationError(
                    "message role must be system, user, or assistant."
                )
            if role == "system":
                system_count += 1
                if index != 0 or system_count > 1:
                    raise LocalModelBridgeValidationError(
                        "at most one system message is allowed and it must be first."
                    )
            if role == "user":
                user_count += 1

            content = cls._normalize_message_content(
                message["content"]
            )
            total_chars += len(content)
            if total_chars > cls.MAX_TOTAL_INPUT_CHARS:
                raise LocalModelBridgeValidationError(
                    "total message content exceeds the bridge limit."
                )
            normalized.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        if user_count == 0:
            raise LocalModelBridgeValidationError(
                "at least one user message is required."
            )
        return normalized

    @classmethod
    def _validate_request_id(cls, request_id: Any) -> str:
        if not isinstance(request_id, str):
            raise LocalModelBridgeValidationError(
                "request_id must be a string."
            )
        normalized = request_id.strip()
        if not cls._REQUEST_ID_RE.fullmatch(normalized):
            raise LocalModelBridgeValidationError(
                "request_id must match modelreq_<safe identifier>."
            )
        return normalized

    def _require_profile(self) -> LocalModelProviderProfile:
        if self._profile is None:
            raise LocalModelBridgeConfigurationError(
                "No local model provider profile is configured."
            )
        return self._profile

    def _require_enabled_profile(self) -> LocalModelProviderProfile:
        profile = self._require_profile()
        if not profile.enabled:
            raise LocalModelBridgePermissionError(
                "The local model provider profile is disabled."
            )
        return profile

    @classmethod
    def _endpoint(
        cls,
        profile: LocalModelProviderProfile,
        *,
        operation: str,
    ) -> str:
        if operation == "probe":
            path = cls.PROBE_PATHS[profile.provider]
        elif operation == "generate":
            path = cls.GENERATE_PATHS[profile.provider]
        else:
            raise LocalModelBridgeConfigurationError(
                "Unknown bridge operation."
            )
        return profile.base_url + path

    @classmethod
    def provider_contracts(cls) -> dict[str, Any]:
        return {
            "schema_version": cls.schema_version,
            "providers": {
                "ollama": {
                    "default_base_url": cls.DEFAULT_BASE_URLS["ollama"],
                    "probe_path": cls.PROBE_PATHS["ollama"],
                    "generate_path": cls.GENERATE_PATHS["ollama"],
                    "streaming": False,
                    "tool_calling": False,
                },
                "openai_compatible": {
                    "default_base_url": cls.DEFAULT_BASE_URLS[
                        "openai_compatible"
                    ],
                    "probe_path": cls.PROBE_PATHS[
                        "openai_compatible"
                    ],
                    "generate_path": cls.GENERATE_PATHS[
                        "openai_compatible"
                    ],
                    "streaming": False,
                    "tool_calling": False,
                },
            },
            "local_hosts": sorted(cls._LOCAL_HOSTS),
            "http_only": True,
            "explicit_port_required": True,
            "resolved_loopback_enforcement": True,
            "redirect_following": False,
            "network_fallback": False,
            "model_download": False,
        }

    def status(self) -> dict[str, Any]:
        profile = self._profile
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": (
                "ready_disabled"
                if profile is None or not profile.enabled
                else "ready_local_profile"
            ),
            "configured": profile is not None,
            "enabled": bool(
                profile is not None and profile.enabled
            ),
            "provider": (
                profile.provider
                if profile is not None
                else None
            ),
            "base_url": (
                profile.base_url
                if profile is not None
                else None
            ),
            "model": (
                profile.model
                if profile is not None
                else None
            ),
            "timeout_seconds": (
                profile.timeout_seconds
                if profile is not None
                else None
            ),
            "max_output_tokens": (
                profile.max_output_tokens
                if profile is not None
                else None
            ),
            "temperature": (
                profile.temperature
                if profile is not None
                else None
            ),
            "network_probe_performed": False,
            "model_request_performed": False,
            "http_listener_active": False,
            "browser_chat_connected": False,
            "safety_boundary": self.safety_boundary(),
        }

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "local_model_bridge_core": True,
            "ollama_provider_contract": True,
            "openai_compatible_provider_contract": True,
            "loopback_endpoint_enforcement": True,
            "resolved_loopback_enforcement": True,
            "explicit_port_required": True,
            "explicit_probe_confirmation": True,
            "explicit_model_request_confirmation": True,
            "bounded_request_schema": True,
            "bounded_response_schema": True,
            "non_streaming_only": True,
            "model_output_text_only": True,
            "model_download_runtime": False,
            "internet_fallback_runtime": False,
            "remote_provider_runtime": False,
            "redirect_following_runtime": False,
            "provider_credentials_runtime": False,
            "tool_schema_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "arbitrary_file_read_runtime": False,
            "arbitrary_file_write_runtime": False,
            "aura_long_term_memory_write_runtime": False,
            "desktop_control_runtime": False,
            "browser_chat_integration_runtime": False,
            "http_listener_runtime": False,
            "background_service_runtime": False,
            "systemd_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
            "autonomous_action_runtime": False,
            "safe_idle": True,
        }

    def probe(
        self,
        *,
        confirm_local_connection: bool,
    ) -> dict[str, Any]:
        if confirm_local_connection is not True:
            raise LocalModelBridgePermissionError(
                "Local provider probe requires explicit confirmation."
            )
        profile = self._require_enabled_profile()
        url = self._endpoint(profile, operation="probe")

        started = self._monotonic()
        response = self._transport(
            "GET",
            url,
            None,
            {"Accept": "application/json"},
            profile.timeout_seconds,
        )
        elapsed_ms = max(
            0,
            int((self._monotonic() - started) * 1000),
        )

        if response.status_code != 200:
            raise LocalModelBridgeTransportError(
                "Local provider probe returned HTTP "
                f"{response.status_code}."
            )
        payload = self._decode_json(
            response,
            context="provider probe",
        )

        if profile.provider == "ollama":
            models = payload.get("models")
            if not isinstance(models, list):
                raise LocalModelBridgeResponseError(
                    "Ollama probe response must contain a models list."
                )
            model_ids = [
                item.get("name")
                for item in models
                if isinstance(item, Mapping)
                and isinstance(item.get("name"), str)
            ]
        else:
            data = payload.get("data")
            if not isinstance(data, list):
                raise LocalModelBridgeResponseError(
                    "OpenAI-compatible probe response must contain a data list."
                )
            model_ids = [
                item.get("id")
                for item in data
                if isinstance(item, Mapping)
                and isinstance(item.get("id"), str)
            ]

        return {
            "status": "available",
            "provider": profile.provider,
            "base_url": profile.base_url,
            "configured_model": profile.model,
            "configured_model_visible": (
                profile.model in model_ids
            ),
            "available_model_count": len(model_ids),
            "available_models": model_ids,
            "elapsed_ms": elapsed_ms,
            "local_connection_confirmed": True,
            "model_request_performed": False,
            "network_fallback_used": False,
        }

    @classmethod
    def _request_payload(
        cls,
        profile: LocalModelProviderProfile,
        messages: list[dict[str, str]],
    ) -> dict[str, Any]:
        if profile.provider == "ollama":
            return {
                "model": profile.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": profile.temperature,
                    "num_predict": profile.max_output_tokens,
                },
            }
        return {
            "model": profile.model,
            "messages": messages,
            "stream": False,
            "temperature": profile.temperature,
            "max_tokens": profile.max_output_tokens,
        }

    @classmethod
    def _parse_generated_content(
        cls,
        profile: LocalModelProviderProfile,
        payload: dict[str, Any],
    ) -> tuple[str, str | None, dict[str, Any]]:
        if profile.provider == "ollama":
            message = payload.get("message")
            if not isinstance(message, Mapping):
                raise LocalModelBridgeResponseError(
                    "Ollama response must contain a message object."
                )
            if message.get("role") not in (None, "assistant"):
                raise LocalModelBridgeResponseError(
                    "Ollama response role must be assistant."
                )
            content = message.get("content")
            response_model = payload.get("model")
            metadata = {
                "done": payload.get("done"),
                "done_reason": payload.get("done_reason"),
                "prompt_eval_count": payload.get(
                    "prompt_eval_count"
                ),
                "eval_count": payload.get("eval_count"),
            }
        else:
            choices = payload.get("choices")
            if not isinstance(choices, list) or not choices:
                raise LocalModelBridgeResponseError(
                    "OpenAI-compatible response must contain choices."
                )
            first = choices[0]
            if not isinstance(first, Mapping):
                raise LocalModelBridgeResponseError(
                    "OpenAI-compatible first choice must be an object."
                )
            message = first.get("message")
            if not isinstance(message, Mapping):
                raise LocalModelBridgeResponseError(
                    "OpenAI-compatible choice must contain a message object."
                )
            if message.get("role") not in (None, "assistant"):
                raise LocalModelBridgeResponseError(
                    "OpenAI-compatible response role must be assistant."
                )
            content = message.get("content")
            response_model = payload.get("model")
            metadata = {
                "finish_reason": first.get("finish_reason"),
                "usage": payload.get("usage"),
            }

        if not isinstance(content, str):
            raise LocalModelBridgeResponseError(
                "Model response content must be a string."
            )
        content = content.strip()
        if not content:
            raise LocalModelBridgeResponseError(
                "Model response content must not be empty."
            )
        if len(content) > cls.MAX_OUTPUT_CHARS:
            raise LocalModelBridgeResponseError(
                "Model response content exceeds the output limit."
            )
        invalid_controls = [
            character
            for character in content
            if ord(character) < 32
            and character not in ("\n", "\t")
        ]
        if invalid_controls:
            raise LocalModelBridgeResponseError(
                "Model response contains a disallowed control character."
            )

        if response_model is not None and not isinstance(
            response_model,
            str,
        ):
            raise LocalModelBridgeResponseError(
                "Provider response model identifier must be a string or null."
            )

        return content, response_model, metadata

    def generate(
        self,
        *,
        messages: Sequence[Mapping[str, Any]],
        request_id: str,
        confirm_model_request: bool,
    ) -> dict[str, Any]:
        if confirm_model_request is not True:
            raise LocalModelBridgePermissionError(
                "Model inference requires explicit confirmation."
            )

        profile = self._require_enabled_profile()
        validated_request_id = self._validate_request_id(
            request_id
        )
        normalized_messages = self._validate_messages(
            messages
        )
        payload = self._request_payload(
            profile,
            normalized_messages,
        )
        body = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        if len(body) > self.MAX_REQUEST_BODY_BYTES:
            raise LocalModelBridgeValidationError(
                "Serialized model request exceeds the body limit."
            )

        url = self._endpoint(profile, operation="generate")
        started = self._monotonic()
        response = self._transport(
            "POST",
            url,
            body,
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-AURA-Request-ID": validated_request_id,
            },
            profile.timeout_seconds,
        )
        elapsed_ms = max(
            0,
            int((self._monotonic() - started) * 1000),
        )

        if response.status_code != 200:
            raise LocalModelBridgeTransportError(
                "Local model request returned HTTP "
                f"{response.status_code}."
            )

        response_payload = self._decode_json(
            response,
            context="model inference",
        )
        content, response_model, metadata = (
            self._parse_generated_content(
                profile,
                response_payload,
            )
        )

        return {
            "status": "completed",
            "request_id": validated_request_id,
            "provider": profile.provider,
            "base_url": profile.base_url,
            "configured_model": profile.model,
            "response_model": response_model,
            "content": content,
            "elapsed_ms": elapsed_ms,
            "input_message_count": len(normalized_messages),
            "input_character_count": sum(
                len(item["content"])
                for item in normalized_messages
            ),
            "model_request_confirmed": True,
            "model_invoked": True,
            "network_fallback_used": False,
            "streaming_used": False,
            "tool_schema_sent": False,
            "tool_calls_accepted": False,
            "tools_invoked": False,
            "actions_invoked": False,
            "commands_invoked": False,
            "aura_memory_written": False,
            "provider_metadata": metadata,
        }

    def self_test(self) -> dict[str, Any]:
        """Validate configuration, permission, transport, and parsing gates."""

        assertions: dict[str, bool] = {}

        class FakeTransport:
            def __init__(self) -> None:
                self.calls: list[
                    tuple[
                        str,
                        str,
                        bytes | None,
                        dict[str, str],
                        float,
                    ]
                ] = []
                self.responses: list[
                    LocalModelTransportResponse
                ] = []

            def queue(
                self,
                status_code: int,
                payload: Any,
            ) -> None:
                body = (
                    payload
                    if isinstance(payload, bytes)
                    else json.dumps(payload).encode("utf-8")
                )
                self.responses.append(
                    LocalModelTransportResponse(
                        status_code=status_code,
                        headers={
                            "Content-Type": "application/json"
                        },
                        body=body,
                    )
                )

            def __call__(
                self,
                method: str,
                url: str,
                body: bytes | None,
                headers: Mapping[str, str],
                timeout_seconds: float,
            ) -> LocalModelTransportResponse:
                self.calls.append(
                    (
                        method,
                        url,
                        body,
                        dict(headers),
                        timeout_seconds,
                    )
                )
                if not self.responses:
                    raise AssertionError(
                        "Fake transport response queue is empty."
                    )
                return self.responses.pop(0)

        times = iter(
            [
                1.0,
                1.025,
                2.0,
                2.125,
                3.0,
                3.01,
                4.0,
                4.2,
            ]
        )

        default = AuraLocalModelBridgeRuntimeManager()
        default_status = default.status()
        assertions["default_status_ready_disabled"] = (
            default_status["status"] == "ready_disabled"
        )
        assertions["default_unconfigured"] = (
            default_status["configured"] is False
        )
        assertions["default_disabled"] = (
            default_status["enabled"] is False
        )
        assertions["default_provider_none"] = (
            default_status["provider"] is None
        )
        assertions["default_probe_false"] = (
            default_status["network_probe_performed"] is False
        )
        assertions["default_request_false"] = (
            default_status["model_request_performed"] is False
        )
        assertions["default_listener_false"] = (
            default_status["http_listener_active"] is False
        )
        assertions["default_chat_false"] = (
            default_status["browser_chat_connected"] is False
        )

        contracts = default.provider_contracts()
        assertions["contracts_two_providers"] = (
            set(contracts["providers"])
            == {"ollama", "openai_compatible"}
        )
        assertions["contracts_ollama_probe"] = (
            contracts["providers"]["ollama"]["probe_path"]
            == "/api/tags"
        )
        assertions["contracts_ollama_generate"] = (
            contracts["providers"]["ollama"]["generate_path"]
            == "/api/chat"
        )
        assertions["contracts_openai_probe"] = (
            contracts["providers"]["openai_compatible"][
                "probe_path"
            ]
            == "/v1/models"
        )
        assertions["contracts_openai_generate"] = (
            contracts["providers"]["openai_compatible"][
                "generate_path"
            ]
            == "/v1/chat/completions"
        )
        assertions["contracts_http_only"] = (
            contracts["http_only"] is True
        )
        assertions["contracts_port_required"] = (
            contracts["explicit_port_required"] is True
        )
        assertions["contracts_resolved_loopback"] = (
            contracts["resolved_loopback_enforcement"] is True
        )
        assertions["contracts_redirect_false"] = (
            contracts["redirect_following"] is False
        )
        assertions["contracts_no_fallback"] = (
            contracts["network_fallback"] is False
        )
        assertions["contracts_no_download"] = (
            contracts["model_download"] is False
        )

        valid_urls = {
            "ipv4": (
                "http://127.0.0.1:11434",
                "http://127.0.0.1:11434",
            ),
            "localhost": (
                "http://LOCALHOST:8080/",
                "http://localhost:8080",
            ),
            "ipv6": (
                "http://[::1]:9000",
                "http://[::1]:9000",
            ),
        }
        for label, (value, expected) in valid_urls.items():
            assertions[f"url_valid_{label}"] = (
                self._validate_base_url(value) == expected
            )

        invalid_urls = {
            "remote_ip": "http://192.168.1.10:11434",
            "remote_name": "http://example.com:11434",
            "https": "https://127.0.0.1:11434",
            "missing_port": "http://127.0.0.1",
            "credentials": "http://user:pass@127.0.0.1:11434",
            "query": "http://127.0.0.1:11434?x=1",
            "fragment": "http://127.0.0.1:11434#x",
            "path": "http://127.0.0.1:11434/api",
            "bad_port": "http://127.0.0.1:99999",
            "file_scheme": "file:///tmp/model",
        }
        for label, value in invalid_urls.items():
            caught = False
            try:
                self._validate_base_url(value)
            except LocalModelBridgeConfigurationError:
                caught = True
            assertions[f"url_invalid_{label}"] = caught

        invalid_profiles = {
            "provider": {
                "provider": "remote",
                "model": "model",
            },
            "model_empty": {
                "provider": "ollama",
                "model": "",
            },
            "model_space": {
                "provider": "ollama",
                "model": "bad model",
            },
            "enabled_type": {
                "provider": "ollama",
                "model": "model",
                "enabled": "yes",
            },
            "timeout_low": {
                "provider": "ollama",
                "model": "model",
                "timeout_seconds": 0.5,
            },
            "timeout_high": {
                "provider": "ollama",
                "model": "model",
                "timeout_seconds": 121,
            },
            "tokens_low": {
                "provider": "ollama",
                "model": "model",
                "max_output_tokens": 0,
            },
            "tokens_high": {
                "provider": "ollama",
                "model": "model",
                "max_output_tokens": 8193,
            },
            "temperature_low": {
                "provider": "ollama",
                "model": "model",
                "temperature": -0.1,
            },
            "temperature_high": {
                "provider": "ollama",
                "model": "model",
                "temperature": 2.1,
            },
            "unknown_field": {
                "provider": "ollama",
                "model": "model",
                "unknown": True,
            },
        }
        for label, raw in invalid_profiles.items():
            caught = False
            try:
                AuraLocalModelBridgeRuntimeManager(raw)
            except LocalModelBridgeConfigurationError:
                caught = True
            assertions[f"profile_invalid_{label}"] = caught

        disabled_transport = FakeTransport()
        disabled = AuraLocalModelBridgeRuntimeManager(
            {
                "provider": "ollama",
                "model": "qwen2.5:3b",
                "enabled": False,
            },
            transport=disabled_transport,
        )
        assertions["disabled_status_configured"] = (
            disabled.status()["configured"] is True
        )
        assertions["disabled_status_enabled_false"] = (
            disabled.status()["enabled"] is False
        )

        disabled_probe = False
        try:
            disabled.probe(confirm_local_connection=True)
        except LocalModelBridgePermissionError:
            disabled_probe = True
        assertions["disabled_probe_blocked"] = disabled_probe
        assertions["disabled_probe_no_transport"] = (
            disabled_transport.calls == []
        )

        no_confirm_probe = False
        try:
            disabled.probe(confirm_local_connection=False)
        except LocalModelBridgePermissionError:
            no_confirm_probe = True
        assertions["probe_confirmation_required"] = no_confirm_probe

        no_profile_generate = False
        try:
            default.generate(
                messages=[
                    {"role": "user", "content": "hello"}
                ],
                request_id="modelreq_default",
                confirm_model_request=True,
            )
        except LocalModelBridgeConfigurationError:
            no_profile_generate = True
        assertions["generate_profile_required"] = (
            no_profile_generate
        )

        validation_cases = {
            "messages_string": "hello",
            "messages_empty": [],
            "message_not_object": ["hello"],
            "extra_field": [
                {
                    "role": "user",
                    "content": "hello",
                    "extra": True,
                }
            ],
            "bad_role": [
                {"role": "tool", "content": "hello"}
            ],
            "system_not_first": [
                {"role": "user", "content": "hello"},
                {"role": "system", "content": "rules"},
            ],
            "two_system": [
                {"role": "system", "content": "one"},
                {"role": "system", "content": "two"},
                {"role": "user", "content": "hello"},
            ],
            "no_user": [
                {"role": "assistant", "content": "hello"}
            ],
            "empty_content": [
                {"role": "user", "content": " "}
            ],
            "control_content": [
                {"role": "user", "content": "bad\x00"}
            ],
            "too_long": [
                {
                    "role": "user",
                    "content": "x"
                    * (self.MAX_MESSAGE_CHARS + 1),
                }
            ],
            "too_many": [
                {"role": "user", "content": "x"}
                for _ in range(self.MAX_MESSAGES + 1)
            ],
        }
        for label, messages in validation_cases.items():
            caught = False
            try:
                self._validate_messages(messages)
            except LocalModelBridgeValidationError:
                caught = True
            assertions[f"messages_invalid_{label}"] = caught

        request_id_cases = {
            "missing_prefix": "abc",
            "space": "modelreq_bad id",
            "empty": "",
            "too_long": "modelreq_" + "a" * 97,
        }
        for label, request_id in request_id_cases.items():
            caught = False
            try:
                self._validate_request_id(request_id)
            except LocalModelBridgeValidationError:
                caught = True
            assertions[f"request_id_invalid_{label}"] = caught

        ollama_transport = FakeTransport()
        ollama = AuraLocalModelBridgeRuntimeManager(
            {
                "provider": "ollama",
                "model": "qwen2.5:3b",
                "enabled": True,
                "timeout_seconds": 10,
                "max_output_tokens": 256,
                "temperature": 0.1,
            },
            transport=ollama_transport,
            monotonic_factory=lambda: next(times),
        )
        ollama_status = ollama.status()
        assertions["ollama_status_ready"] = (
            ollama_status["status"]
            == "ready_local_profile"
        )
        assertions["ollama_status_provider"] = (
            ollama_status["provider"] == "ollama"
        )
        assertions["ollama_status_base"] = (
            ollama_status["base_url"]
            == "http://127.0.0.1:11434"
        )
        assertions["ollama_status_model"] = (
            ollama_status["model"] == "qwen2.5:3b"
        )

        ollama_transport.queue(
            200,
            {
                "models": [
                    {"name": "qwen2.5:3b"},
                    {"name": "gemma3:4b"},
                ]
            },
        )
        probe = ollama.probe(
            confirm_local_connection=True
        )
        assertions["ollama_probe_available"] = (
            probe["status"] == "available"
        )
        assertions["ollama_probe_model_visible"] = (
            probe["configured_model_visible"] is True
        )
        assertions["ollama_probe_count_two"] = (
            probe["available_model_count"] == 2
        )
        assertions["ollama_probe_elapsed_25"] = (
            probe["elapsed_ms"] == 24
            or probe["elapsed_ms"] == 25
        )
        assertions["ollama_probe_no_request"] = (
            probe["model_request_performed"] is False
        )
        assertions["ollama_probe_no_fallback"] = (
            probe["network_fallback_used"] is False
        )
        probe_call = ollama_transport.calls[-1]
        assertions["ollama_probe_method_get"] = (
            probe_call[0] == "GET"
        )
        assertions["ollama_probe_url_fixed"] = (
            probe_call[1]
            == "http://127.0.0.1:11434/api/tags"
        )
        assertions["ollama_probe_body_none"] = (
            probe_call[2] is None
        )

        no_confirm_generate = False
        calls_before = len(ollama_transport.calls)
        try:
            ollama.generate(
                messages=[
                    {"role": "user", "content": "hello"}
                ],
                request_id="modelreq_no_confirm",
                confirm_model_request=False,
            )
        except LocalModelBridgePermissionError:
            no_confirm_generate = True
        assertions["generate_confirmation_required"] = (
            no_confirm_generate
        )
        assertions["generate_no_confirm_no_transport"] = (
            len(ollama_transport.calls) == calls_before
        )

        ollama_transport.queue(
            200,
            {
                "model": "qwen2.5:3b",
                "message": {
                    "role": "assistant",
                    "content": "  Hello from local Ollama.  ",
                },
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 12,
                "eval_count": 8,
            },
        )
        generated = ollama.generate(
            messages=[
                {
                    "role": "system",
                    "content": "You are AURA.",
                },
                {
                    "role": "user",
                    "content": "  Hello  ",
                },
            ],
            request_id="modelreq_ollama_001",
            confirm_model_request=True,
        )
        assertions["ollama_generate_completed"] = (
            generated["status"] == "completed"
        )
        assertions["ollama_generate_request_id"] = (
            generated["request_id"]
            == "modelreq_ollama_001"
        )
        assertions["ollama_generate_content_trimmed"] = (
            generated["content"]
            == "Hello from local Ollama."
        )
        assertions["ollama_generate_model_invoked"] = (
            generated["model_invoked"] is True
        )
        assertions["ollama_generate_messages_two"] = (
            generated["input_message_count"] == 2
        )
        assertions["ollama_generate_no_fallback"] = (
            generated["network_fallback_used"] is False
        )
        assertions["ollama_generate_no_stream"] = (
            generated["streaming_used"] is False
        )
        assertions["ollama_generate_no_tools"] = (
            generated["tools_invoked"] is False
            and generated["tool_schema_sent"] is False
            and generated["tool_calls_accepted"] is False
        )
        assertions["ollama_generate_no_actions"] = (
            generated["actions_invoked"] is False
        )
        assertions["ollama_generate_no_commands"] = (
            generated["commands_invoked"] is False
        )
        assertions["ollama_generate_no_memory"] = (
            generated["aura_memory_written"] is False
        )
        ollama_call = ollama_transport.calls[-1]
        assertions["ollama_generate_method_post"] = (
            ollama_call[0] == "POST"
        )
        assertions["ollama_generate_url_fixed"] = (
            ollama_call[1]
            == "http://127.0.0.1:11434/api/chat"
        )
        assertions["ollama_generate_json_header"] = (
            ollama_call[3]["Content-Type"]
            == "application/json"
        )
        assertions["ollama_generate_request_header"] = (
            ollama_call[3]["X-AURA-Request-ID"]
            == "modelreq_ollama_001"
        )
        ollama_body = json.loads(
            ollama_call[2].decode("utf-8")
        )
        assertions["ollama_body_stream_false"] = (
            ollama_body["stream"] is False
        )
        assertions["ollama_body_no_tools"] = (
            "tools" not in ollama_body
            and "functions" not in ollama_body
        )
        assertions["ollama_body_temperature"] = (
            ollama_body["options"]["temperature"] == 0.1
        )
        assertions["ollama_body_tokens"] = (
            ollama_body["options"]["num_predict"] == 256
        )
        assertions["ollama_body_trimmed_user"] = (
            ollama_body["messages"][1]["content"] == "Hello"
        )

        openai_transport = FakeTransport()
        openai = AuraLocalModelBridgeRuntimeManager(
            {
                "provider": "openai_compatible",
                "base_url": "http://localhost:8080",
                "model": "local-instruct",
                "enabled": True,
                "timeout_seconds": 20,
                "max_output_tokens": 300,
                "temperature": 0.3,
            },
            transport=openai_transport,
            monotonic_factory=lambda: next(times),
        )
        openai_transport.queue(
            200,
            {
                "object": "list",
                "data": [
                    {"id": "local-instruct"},
                ],
            },
        )
        openai_probe = openai.probe(
            confirm_local_connection=True
        )
        assertions["openai_probe_available"] = (
            openai_probe["status"] == "available"
        )
        assertions["openai_probe_visible"] = (
            openai_probe["configured_model_visible"] is True
        )
        assertions["openai_probe_url_fixed"] = (
            openai_transport.calls[-1][1]
            == "http://localhost:8080/v1/models"
        )

        openai_transport.queue(
            200,
            {
                "id": "chatcmpl-local",
                "model": "local-instruct",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Local OpenAI-compatible reply.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 4,
                    "completion_tokens": 5,
                    "total_tokens": 9,
                },
            },
        )
        openai_generated = openai.generate(
            messages=[
                {
                    "role": "user",
                    "content": "Hello local model",
                }
            ],
            request_id="modelreq_openai_001",
            confirm_model_request=True,
        )
        assertions["openai_generate_completed"] = (
            openai_generated["status"] == "completed"
        )
        assertions["openai_generate_content"] = (
            openai_generated["content"]
            == "Local OpenAI-compatible reply."
        )
        assertions["openai_generate_response_model"] = (
            openai_generated["response_model"]
            == "local-instruct"
        )
        assertions["openai_generate_finish_reason"] = (
            openai_generated["provider_metadata"][
                "finish_reason"
            ]
            == "stop"
        )
        openai_call = openai_transport.calls[-1]
        assertions["openai_generate_url_fixed"] = (
            openai_call[1]
            == "http://localhost:8080/v1/chat/completions"
        )
        openai_body = json.loads(
            openai_call[2].decode("utf-8")
        )
        assertions["openai_body_stream_false"] = (
            openai_body["stream"] is False
        )
        assertions["openai_body_tokens"] = (
            openai_body["max_tokens"] == 300
        )
        assertions["openai_body_temperature"] = (
            openai_body["temperature"] == 0.3
        )
        assertions["openai_body_no_tools"] = (
            "tools" not in openai_body
            and "functions" not in openai_body
        )

        malformed_cases = [
            (
                "invalid_json",
                LocalModelTransportResponse(
                    200,
                    {},
                    b"not-json",
                ),
            ),
            (
                "empty_ollama_content",
                LocalModelTransportResponse(
                    200,
                    {},
                    json.dumps(
                        {
                            "message": {
                                "role": "assistant",
                                "content": " ",
                            }
                        }
                    ).encode("utf-8"),
                ),
            ),
            (
                "wrong_ollama_role",
                LocalModelTransportResponse(
                    200,
                    {},
                    json.dumps(
                        {
                            "message": {
                                "role": "tool",
                                "content": "x",
                            }
                        }
                    ).encode("utf-8"),
                ),
            ),
            (
                "oversized_content",
                LocalModelTransportResponse(
                    200,
                    {},
                    json.dumps(
                        {
                            "message": {
                                "role": "assistant",
                                "content": "x"
                                * (self.MAX_OUTPUT_CHARS + 1),
                            }
                        }
                    ).encode("utf-8"),
                ),
            ),
        ]
        for label, queued in malformed_cases:
            transport = FakeTransport()
            transport.responses.append(queued)
            manager = AuraLocalModelBridgeRuntimeManager(
                {
                    "provider": "ollama",
                    "model": "model",
                    "enabled": True,
                },
                transport=transport,
            )
            caught = False
            try:
                manager.generate(
                    messages=[
                        {
                            "role": "user",
                            "content": "hello",
                        }
                    ],
                    request_id=f"modelreq_{label}",
                    confirm_model_request=True,
                )
            except LocalModelBridgeResponseError:
                caught = True
            assertions[f"response_invalid_{label}"] = caught

        http_error_transport = FakeTransport()
        http_error_transport.queue(
            503,
            {"error": "unavailable"},
        )
        http_error_manager = AuraLocalModelBridgeRuntimeManager(
            {
                "provider": "ollama",
                "model": "model",
                "enabled": True,
            },
            transport=http_error_transport,
        )
        http_error_seen = False
        try:
            http_error_manager.generate(
                messages=[
                    {"role": "user", "content": "hello"}
                ],
                request_id="modelreq_http_error",
                confirm_model_request=True,
            )
        except LocalModelBridgeTransportError as exc:
            http_error_seen = "503" in str(exc)
        assertions["transport_http_error_visible"] = (
            http_error_seen
        )

        boundary = default.safety_boundary()
        enabled_keys = (
            "local_model_bridge_core",
            "ollama_provider_contract",
            "openai_compatible_provider_contract",
            "loopback_endpoint_enforcement",
            "resolved_loopback_enforcement",
            "explicit_port_required",
            "explicit_probe_confirmation",
            "explicit_model_request_confirmation",
            "bounded_request_schema",
            "bounded_response_schema",
            "non_streaming_only",
            "model_output_text_only",
            "safe_idle",
        )
        for key in enabled_keys:
            assertions[f"boundary_enabled_{key}"] = (
                boundary[key] is True
            )

        disabled_keys = (
            "model_download_runtime",
            "internet_fallback_runtime",
            "remote_provider_runtime",
            "redirect_following_runtime",
            "provider_credentials_runtime",
            "tool_schema_runtime",
            "tool_calling_runtime",
            "action_dispatch_runtime",
            "command_execution_runtime",
            "arbitrary_file_read_runtime",
            "arbitrary_file_write_runtime",
            "aura_long_term_memory_write_runtime",
            "desktop_control_runtime",
            "browser_chat_integration_runtime",
            "http_listener_runtime",
            "background_service_runtime",
            "systemd_runtime",
            "public_listener_runtime",
            "lan_listener_runtime",
            "autonomous_action_runtime",
        )
        for key in disabled_keys:
            assertions[f"boundary_disabled_{key}"] = (
                boundary[key] is False
            )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise LocalModelBridgeError(
                "Local Model Bridge self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "schema_version": self.schema_version,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "provider_contracts_verified": True,
            "loopback_enforcement_verified": True,
            "profile_validation_verified": True,
            "probe_permission_verified": True,
            "model_request_permission_verified": True,
            "ollama_probe_verified": True,
            "ollama_generation_verified": True,
            "openai_compatible_probe_verified": True,
            "openai_compatible_generation_verified": True,
            "message_schema_verified": True,
            "request_limits_verified": True,
            "response_limits_verified": True,
            "transport_errors_verified": True,
            "model_download_runtime": False,
            "internet_fallback_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "aura_memory_write_runtime": False,
            "browser_chat_integration_runtime": False,
            "http_listener_runtime": False,
        }
