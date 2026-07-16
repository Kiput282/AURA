from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
import json

from aura.local_model_bridge_runtime.aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeConfigurationError,
    LocalModelBridgePermissionError,
    LocalModelTransportResponse,
)
from aura.local_model_service_discovery_health.local_model_service_discovery_health_contract import (
    LocalModelServiceDiscoveryHealthContract,
)
from aura.model_router.model_router import ModelRouter


BridgeTransport = Callable[
    [str, str, bytes | None, Mapping[str, str], float],
    LocalModelTransportResponse,
]


class LocalModelRouterActivationError(RuntimeError):
    """Base error for Sprint 258 route activation."""


class LocalModelRouterPermissionError(
    LocalModelRouterActivationError
):
    """Raised when explicit route or model permission is absent."""


class LocalModelRouterHealthError(
    LocalModelRouterActivationError
):
    """Raised when provider health has not been verified."""


class LocalModelRouterRouteError(
    LocalModelRouterActivationError
):
    """Raised when a route cannot be activated safely."""


class LocalModelRouterActivationContract:
    VERSION = "1.1.8"
    SPRINT = 258
    CONFIRMATION_TOKEN = "ROUTE_LOCAL_MODEL_REQUEST"
    DEFAULT_TARGET = "companion"
    MAX_ROUTED_MESSAGES = 16
    MAX_ROUTED_INPUT_CHARS = 32768

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.router = ModelRouter(
            project_root=self.project_root
        )
        self.health = (
            LocalModelServiceDiscoveryHealthContract(
                project_root=self.project_root
            )
        )

    def profile_mapping(self) -> dict[str, Any]:
        reasoning = self.router.reasoning_settings()
        timeout = reasoning.get(
            "timeout",
            60,
        )

        if (
            isinstance(timeout, bool)
            or not isinstance(
                timeout,
                (int, float),
            )
        ):
            raise LocalModelBridgeConfigurationError(
                "reasoning.timeout must be numeric."
            )

        raw = {
            "provider": self.router.current_provider(),
            "base_url": self.router.current_host(),
            "model": self.router.current_model(),
            "enabled": True,
            "timeout_seconds": float(timeout),
            "max_output_tokens": 512,
            "temperature": 0.2,
        }
        manager = (
            AuraLocalModelBridgeRuntimeManager(
                raw
            )
        )
        status = manager.status()

        return {
            "provider": status["provider"],
            "base_url": status["base_url"],
            "model": status["model"],
            "enabled": status["enabled"],
            "timeout_seconds": status[
                "timeout_seconds"
            ],
            "max_output_tokens": status[
                "max_output_tokens"
            ],
            "temperature": status[
                "temperature"
            ],
            "persistent_configuration_write": False,
            "credentials_read": False,
            "source": "aura/config/settings.yaml:reasoning",
        }

    def profile_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        preview = self.route_preview(target)
        profile = self.profile_mapping()

        return {
            "target": target,
            "normalized_target": preview[
                "normalized_target"
            ],
            "route_found": preview["route_found"],
            "route_status": preview[
                "route_status"
            ],
            "provider": profile["provider"],
            "base_url": profile["base_url"],
            "model": profile["model"],
            "timeout_seconds": profile[
                "timeout_seconds"
            ],
            "profile_enabled": profile["enabled"],
            "profile_source": profile["source"],
            "persistent_configuration_write": False,
            "credentials_read": False,
            "health_probe_performed": False,
            "model_request_performed": False,
        }

    def route_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        if not isinstance(target, str):
            raise LocalModelRouterRouteError(
                "target must be a string."
            )

        normalized_input = target.strip()

        if not normalized_input:
            raise LocalModelRouterRouteError(
                "target must not be empty."
            )

        selection = self.router.select(
            normalized_input
        )
        route = selection.get("route")
        route_found = bool(
            selection.get("found")
        )
        fallback_used = bool(
            selection.get("fallback_used")
        )
        profile = self.profile_mapping()
        host = self.health.host_posture()

        route_provider = (
            route.get("provider")
            if isinstance(route, dict)
            else None
        )
        route_model = (
            route.get("model")
            if isinstance(route, dict)
            else None
        )
        route_status = (
            route.get("status")
            if isinstance(route, dict)
            else None
        )

        reasons = []

        if not route_found:
            reasons.append(
                "exact_route_required"
            )

        if fallback_used:
            reasons.append(
                "fallback_not_executable"
            )

        if route_status != "online":
            reasons.append(
                "route_not_online"
            )

        if route_provider != profile["provider"]:
            reasons.append(
                "route_provider_mismatch"
            )

        if route_model != profile["model"]:
            reasons.append(
                "route_model_mismatch"
            )

        if profile["provider"] not in (
            AuraLocalModelBridgeRuntimeManager
            .SUPPORTED_PROVIDERS
        ):
            reasons.append(
                "unsupported_provider"
            )

        if host["state"] not in {
            "available_unprobed",
            "degraded_unprobed",
        }:
            reasons.append(
                "provider_unavailable"
            )

        eligible_for_confirmation = (
            not reasons
        )

        return {
            "target": normalized_input,
            "normalized_target": selection[
                "normalized_target"
            ],
            "route_found": route_found,
            "fallback_used": fallback_used,
            "route": route,
            "route_status": route_status,
            "provider": route_provider,
            "model": route_model,
            "configured_base_url": profile[
                "base_url"
            ],
            "provider_state": host["state"],
            "eligible_for_confirmation": (
                eligible_for_confirmation
            ),
            "execution_ready": False,
            "health_verified": False,
            "permission_verified": False,
            "denial_reasons": reasons,
            "route_selection_mutated": False,
            "route_decision_persisted": False,
            "runtime_switching_performed": False,
            "health_probe_performed": False,
            "model_request_performed": False,
        }

    def request_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        route = self.route_preview(target)

        return {
            **route,
            "confirmation_required": True,
            "confirmation_token": (
                self.CONFIRMATION_TOKEN
            ),
            "provider_health_required": True,
            "model_request_permission_required": True,
            "request_schema": {
                "target": "exact route target",
                "messages": (
                    "1-16 bridge-compatible message objects"
                ),
                "request_id": (
                    "modelreq_<safe identifier>"
                ),
                "provider_health_verified": True,
                "confirm_router_request": True,
            },
            "live_inference_default": False,
            "live_inference_performed": False,
        }

    @classmethod
    def _validate_routed_messages(
        cls,
        messages: Sequence[
            Mapping[str, Any]
        ],
    ) -> list[dict[str, Any]]:
        if (
            isinstance(messages, (str, bytes))
            or not isinstance(
                messages,
                Sequence,
            )
        ):
            raise LocalModelRouterRouteError(
                "messages must be a sequence."
            )

        if not messages:
            raise LocalModelRouterRouteError(
                "messages must not be empty."
            )

        if len(messages) > cls.MAX_ROUTED_MESSAGES:
            raise LocalModelRouterRouteError(
                "routed message count exceeds limit."
            )

        copied = []
        total_chars = 0

        for item in messages:
            if not isinstance(item, Mapping):
                raise LocalModelRouterRouteError(
                    "each routed message must be an object."
                )

            if set(item) != {
                "role",
                "content",
            }:
                raise LocalModelRouterRouteError(
                    "routed messages contain only role and content."
                )

            role = item["role"]
            content = item["content"]

            if not isinstance(role, str):
                raise LocalModelRouterRouteError(
                    "message role must be a string."
                )

            if not isinstance(content, str):
                raise LocalModelRouterRouteError(
                    "message content must be a string."
                )

            normalized_content = content.strip()

            if not normalized_content:
                raise LocalModelRouterRouteError(
                    "message content must not be empty."
                )

            total_chars += len(
                normalized_content
            )

            if (
                total_chars
                > cls.MAX_ROUTED_INPUT_CHARS
            ):
                raise LocalModelRouterRouteError(
                    "routed input exceeds limit."
                )

            copied.append(
                {
                    "role": role,
                    "content": normalized_content,
                }
            )

        return copied

    def execute(
        self,
        *,
        target: str,
        messages: Sequence[
            Mapping[str, Any]
        ],
        request_id: str,
        provider_health_verified: bool,
        confirm_router_request: bool,
        confirmation_token: str,
        transport: BridgeTransport | None = None,
    ) -> dict[str, Any]:
        if (
            confirm_router_request is not True
            or confirmation_token
            != self.CONFIRMATION_TOKEN
        ):
            raise LocalModelRouterPermissionError(
                "Router execution requires exact explicit confirmation."
            )

        if provider_health_verified is not True:
            raise LocalModelRouterHealthError(
                "Provider health must be explicitly verified."
            )

        preview = self.route_preview(target)

        if not preview[
            "eligible_for_confirmation"
        ]:
            raise LocalModelRouterRouteError(
                "Route is not eligible: "
                + ", ".join(
                    preview["denial_reasons"]
                )
            )

        normalized_messages = (
            self._validate_routed_messages(
                messages
            )
        )
        profile = self.profile_mapping()
        bridge_profile = {
            "provider": profile["provider"],
            "base_url": profile["base_url"],
            "model": profile["model"],
            "enabled": profile["enabled"],
            "timeout_seconds": profile["timeout_seconds"],
            "max_output_tokens": profile["max_output_tokens"],
            "temperature": profile["temperature"],
        }
        bridge = (
            AuraLocalModelBridgeRuntimeManager(
                bridge_profile,
                transport=transport,
            )
        )
        generated = bridge.generate(
            messages=normalized_messages,
            request_id=request_id,
            confirm_model_request=True,
        )

        return {
            "status": "completed",
            "version": self.VERSION,
            "sprint": self.SPRINT,
            "target": preview[
                "normalized_target"
            ],
            "route": preview["route"],
            "route_selection_performed": True,
            "route_selection_mutated": False,
            "route_decision_persisted": False,
            "runtime_switching_performed": False,
            "provider_health_verified": True,
            "model_request_permission_verified": True,
            "bridge_handoff_performed": True,
            "bridge_result": generated,
            "service_started": False,
            "service_stopped": False,
            "model_downloaded": False,
            "model_loaded": False,
            "queue_activated": False,
            "resource_budget_mutated": False,
            "non_loopback_network": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        class FakeTransport:
            def __init__(self) -> None:
                self.calls: list[
                    dict[str, Any]
                ] = []

            def __call__(
                self,
                method: str,
                url: str,
                body: bytes | None,
                headers: Mapping[str, str],
                timeout_seconds: float,
            ) -> LocalModelTransportResponse:
                request_payload = (
                    json.loads(
                        body.decode("utf-8")
                    )
                    if body is not None
                    else None
                )
                self.calls.append(
                    {
                        "method": method,
                        "url": url,
                        "payload": request_payload,
                        "headers": dict(headers),
                        "timeout_seconds": (
                            timeout_seconds
                        ),
                    }
                )
                return LocalModelTransportResponse(
                    status_code=200,
                    headers={
                        "Content-Type": (
                            "application/json"
                        )
                    },
                    body=json.dumps(
                        {
                            "model": (
                                self_outer.router
                                .current_model()
                            ),
                            "message": {
                                "role": "assistant",
                                "content": (
                                    "fixture router response"
                                ),
                            },
                            "done": True,
                            "done_reason": "stop",
                            "prompt_eval_count": 4,
                            "eval_count": 3,
                        }
                    ).encode("utf-8"),
                )

        self_outer = self
        fake = FakeTransport()
        denied_without_permission = False
        denied_without_health = False
        unknown_route_denied = False
        foundation_route_denied = False

        try:
            self.execute(
                target="companion",
                messages=[
                    {
                        "role": "user",
                        "content": "fixture",
                    }
                ],
                request_id=(
                    "modelreq_router_no_permission"
                ),
                provider_health_verified=True,
                confirm_router_request=False,
                confirmation_token="",
                transport=fake,
            )
        except LocalModelRouterPermissionError:
            denied_without_permission = True

        try:
            self.execute(
                target="companion",
                messages=[
                    {
                        "role": "user",
                        "content": "fixture",
                    }
                ],
                request_id=(
                    "modelreq_router_no_health"
                ),
                provider_health_verified=False,
                confirm_router_request=True,
                confirmation_token=(
                    self.CONFIRMATION_TOKEN
                ),
                transport=fake,
            )
        except LocalModelRouterHealthError:
            denied_without_health = True

        try:
            self.execute(
                target="unknown-route",
                messages=[
                    {
                        "role": "user",
                        "content": "fixture",
                    }
                ],
                request_id=(
                    "modelreq_router_unknown"
                ),
                provider_health_verified=True,
                confirm_router_request=True,
                confirmation_token=(
                    self.CONFIRMATION_TOKEN
                ),
                transport=fake,
            )
        except LocalModelRouterRouteError:
            unknown_route_denied = True

        try:
            self.execute(
                target="coding",
                messages=[
                    {
                        "role": "user",
                        "content": "fixture",
                    }
                ],
                request_id=(
                    "modelreq_router_foundation"
                ),
                provider_health_verified=True,
                confirm_router_request=True,
                confirmation_token=(
                    self.CONFIRMATION_TOKEN
                ),
                transport=fake,
            )
        except LocalModelRouterRouteError:
            foundation_route_denied = True

        result = self.execute(
            target="chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an isolated fixture."
                    ),
                },
                {
                    "role": "user",
                    "content": "Reply safely.",
                },
            ],
            request_id=(
                "modelreq_router_fixture"
            ),
            provider_health_verified=True,
            confirm_router_request=True,
            confirmation_token=(
                self.CONFIRMATION_TOKEN
            ),
            transport=fake,
        )

        call = (
            fake.calls[0]
            if fake.calls
            else {}
        )
        bridge_result = result[
            "bridge_result"
        ]

        return {
            "denied_without_permission": (
                denied_without_permission
            ),
            "denied_without_health": (
                denied_without_health
            ),
            "unknown_route_denied": (
                unknown_route_denied
            ),
            "foundation_route_denied": (
                foundation_route_denied
            ),
            "selected_target": result[
                "target"
            ],
            "selected_route_found": (
                result["route"]["name"]
                == "companion"
            ),
            "route_selection_performed": (
                result[
                    "route_selection_performed"
                ]
            ),
            "route_selection_mutated": (
                result[
                    "route_selection_mutated"
                ]
            ),
            "route_decision_persisted": (
                result[
                    "route_decision_persisted"
                ]
            ),
            "runtime_switching_performed": (
                result[
                    "runtime_switching_performed"
                ]
            ),
            "provider_health_verified": (
                result[
                    "provider_health_verified"
                ]
            ),
            "model_request_permission_verified": (
                result[
                    "model_request_permission_verified"
                ]
            ),
            "bridge_handoff_performed": (
                result[
                    "bridge_handoff_performed"
                ]
            ),
            "transport_call_count": len(
                fake.calls
            ),
            "transport_method": call.get(
                "method"
            ),
            "transport_url_loopback": (
                call.get("url", "").startswith(
                    (
                        "http://127.0.0.1:",
                        "http://localhost:",
                    )
                )
            ),
            "transport_path": (
                call.get("url", "").split(
                    ":11434",
                    1,
                )[-1]
            ),
            "payload_model_matches": (
                call.get(
                    "payload",
                    {},
                ).get("model")
                == self.router.current_model()
            ),
            "payload_stream_false": (
                call.get(
                    "payload",
                    {},
                ).get("stream")
                is False
            ),
            "bridge_result_is_object": (
                isinstance(
                    bridge_result,
                    dict,
                )
            ),
            "canonical_network_opened": False,
            "service_mutated": False,
            "model_downloaded": False,
            "model_loaded": False,
            "queue_activated": False,
            "resource_budget_mutated": False,
            "chat_session_mutated": False,
            "memory_mutated": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }
