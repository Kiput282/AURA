"""HTTP integration for Sprint 186 local browser chat sessions."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Type
from urllib.parse import urlsplit
from http.server import BaseHTTPRequestHandler

from aura.control_center_web_shell_runtime import (
    AuraControlCenterWebShellHttpRuntimeManager,
)
from aura.service_lifecycle_runtime import (
    AuraServiceLifecycleRuntimeManager,
)

from .aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
    BrowserChatClearConfirmationError,
    BrowserChatSessionConflictError,
    BrowserChatSessionCorruptionError,
    BrowserChatSessionError,
    BrowserChatSessionNotFoundError,
    BrowserChatValidationError,
)
from .aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
)

from aura.local_model_bridge_runtime.aura_local_model_bridge_profile_resolver import (
    AuraLocalModelBridgeProfileResolver,
)
from aura.local_model_bridge_runtime.aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeConfigurationError,
    LocalModelBridgeError,
    LocalModelBridgePermissionError,
    LocalModelBridgeResponseError,
    LocalModelBridgeTransportError,
    LocalModelBridgeValidationError,
)
from aura.local_model_bridge_runtime.aura_local_model_browser_chat_runtime_manager import (
    AuraLocalModelBrowserChatRuntimeManager,
)


class AuraBrowserChatSessionHttpRuntimeManager(
    AuraControlCenterWebShellHttpRuntimeManager
):
    """Serve bounded chat routes on the existing localhost listener."""

    name = "aura_browser_chat_session_http_runtime"
    component_version = "0.1.0-alpha"
    sprint = 188

    CHAT_ASSET_ROUTES = (
        AuraBrowserChatWebSurfaceManager.ASSET_ROUTES
    )
    CHAT_FIXED_GET_ROUTES = (
        "/api/chat/status",
        "/api/chat/sessions",
    )
    CHAT_ROUTE_CONTRACTS = (
        "GET /api/chat/status",
        "GET /api/chat/sessions",
        "POST /api/chat/sessions",
        "GET /api/chat/sessions/{session_id}",
        "POST /api/chat/sessions/{session_id}/messages",
        "POST /api/chat/sessions/{session_id}/model-messages",
        "POST /api/chat/sessions/{session_id}/clear",
    )
    MODEL_ROUTE_CONTRACTS = (
        "GET /api/model/status",
        "POST /api/model/probe",
    )
    TOTAL_ROUTE_CONTRACT_COUNT = 30
    MAX_REQUEST_BODY_BYTES = 65536
    LOCAL_INTENT_HEADER = "X-AURA-Local-Intent"
    LOCAL_INTENT_VALUE = "browser-chat-session"

    _SESSION_DETAIL_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})$"
    )
    _SESSION_MESSAGE_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/messages$"
    )
    _SESSION_CLEAR_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/clear$"
    )
    _SESSION_MODEL_MESSAGE_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/model-messages$"
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        chat_storage_dir: str | Path | None = None,
    ) -> None:
        super().__init__(project_root=project_root)
        if chat_storage_dir is None:
            configured = os.environ.get(
                "AURA_CHAT_SESSION_STORAGE_DIR"
            )
            chat_storage_dir = configured or None

        self.chat_session_manager = (
            AuraBrowserChatSessionRuntimeManager(
                project_root=project_root,
                storage_dir=chat_storage_dir,
            )
        )
        self.chat_web_manager = (
            AuraBrowserChatWebSurfaceManager(
                project_root=project_root
            )
        )

        try:
            local_model_profile = (
                AuraLocalModelBridgeProfileResolver
                .resolve(os.environ)
            )
            local_model_configuration_error = None
        except LocalModelBridgeConfigurationError as exc:
            local_model_profile = None
            local_model_configuration_error = str(exc)

        self.local_model_bridge_manager = (
            AuraLocalModelBridgeRuntimeManager(
                local_model_profile
            )
        )
        self.local_model_chat_manager = (
            AuraLocalModelBrowserChatRuntimeManager(
                self.chat_session_manager,
                self.local_model_bridge_manager,
                configuration_error=(
                    local_model_configuration_error
                ),
            )
        )

    def safety_boundary(self) -> dict[str, Any]:
        return {
            **super().safety_boundary(),
            "browser_chat_session_runtime": True,
            "browser_chat_http_routes": True,
            "control_center_chat_ui": True,
            "chat_route_contract_count": len(
                self.CHAT_ROUTE_CONTRACTS
            ),
            "model_route_contract_count": len(
                self.MODEL_ROUTE_CONTRACTS
            ),
            "chat_asset_route_count": len(
                self.CHAT_ASSET_ROUTES
            ),
            "total_route_contract_count": (
                self.TOTAL_ROUTE_CONTRACT_COUNT
            ),
            "browser_chat_model_bridge_runtime": True,
            "explicit_model_request_confirmation": True,
            "explicit_model_probe_confirmation": True,
            "bounded_session_mutation": True,
            "json_content_type_required": True,
            "local_intent_header_required": True,
            "same_origin_required": True,
            "request_body_limit_bytes": (
                self.MAX_REQUEST_BODY_BYTES
            ),
            "model_bridge_runtime": False,
            "model_inference_runtime": False,
            "network_fallback_runtime": False,
            "aura_long_term_memory_write": False,
            "tool_execution": False,
            "action_dispatch": False,
            "command_execution": False,
            "browser_auto_launch_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
        }

    @staticmethod
    def _request_origin_allowed(
        origin: str | None,
    ) -> bool:
        return origin in {
            "http://127.0.0.1:8765",
            "http://localhost:8765",
        }

    def _chat_error_payload(
        self,
        exc: Exception,
    ) -> tuple[int, dict[str, Any]]:
        if isinstance(
            exc,
            LocalModelBridgePermissionError,
        ):
            return 403, {
                "status": "blocked",
                "error": "local_model_permission_required",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            LocalModelBridgeConfigurationError,
        ):
            return 503, {
                "status": "degraded",
                "error": "local_model_configuration_error",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            LocalModelBridgeValidationError,
        ):
            return 400, {
                "status": "invalid_request",
                "error": "local_model_validation_error",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            (
                LocalModelBridgeTransportError,
                LocalModelBridgeResponseError,
            ),
        ):
            return 502, {
                "status": "provider_error",
                "error": "local_model_provider_error",
                "detail": str(exc),
            }
        if isinstance(exc, LocalModelBridgeError):
            return 500, {
                "status": "error",
                "error": "local_model_bridge_error",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            BrowserChatSessionNotFoundError,
        ):
            return 404, {
                "status": "not_found",
                "error": "chat_session_not_found",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            BrowserChatSessionConflictError,
        ):
            return 409, {
                "status": "conflict",
                "error": "chat_session_revision_conflict",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            BrowserChatClearConfirmationError,
        ):
            return 400, {
                "status": "invalid_request",
                "error": "clear_confirmation_required",
                "detail": str(exc),
            }
        if isinstance(exc, BrowserChatValidationError):
            return 400, {
                "status": "invalid_request",
                "error": "chat_validation_error",
                "detail": str(exc),
            }
        if isinstance(
            exc,
            BrowserChatSessionCorruptionError,
        ):
            return 503, {
                "status": "degraded",
                "error": "chat_session_corruption",
                "detail": str(exc),
            }
        if isinstance(exc, BrowserChatSessionError):
            return 500, {
                "status": "error",
                "error": "chat_session_runtime_error",
                "detail": str(exc),
            }
        return 500, {
            "status": "error",
            "error": "unexpected_chat_runtime_error",
            "detail": f"{type(exc).__name__}: {exc}",
        }

    def _handler_class(
        self,
        bound_port_getter: Any,
    ) -> Type[BaseHTTPRequestHandler]:
        parent_handler = super()._handler_class(
            bound_port_getter
        )
        manager = self

        class BrowserChatSessionHandler(parent_handler):
            server_version = (
                "AURA-Browser-Chat-Session-Alpha/0.1"
            )

            def _chat_read_payload(
                self,
                path: str,
            ) -> tuple[int, dict[str, Any]] | None:
                if path == "/api/model/status":
                    return 200, (
                        manager.local_model_chat_manager
                        .status()
                    )

                if path == "/api/chat/status":
                    status = manager.chat_session_manager.status()
                    return 200, {
                        **status,
                        "chat_page_route": "/chat",
                        "route_contract_count": len(
                            manager.CHAT_ROUTE_CONTRACTS
                        ),
                        "model_bridge_active": False,
                    }

                if path == "/api/chat/sessions":
                    sessions = (
                        manager.chat_session_manager
                        .list_sessions()
                    )
                    return 200, {
                        "status": "ok",
                        "session_count": len(sessions),
                        "sessions": sessions,
                        "model_bridge_active": False,
                    }

                match = manager._SESSION_DETAIL_RE.fullmatch(
                    path
                )
                if match is not None:
                    session = (
                        manager.chat_session_manager
                        .load_session(match.group(1))
                    )
                    return 200, {
                        "status": "ok",
                        "session": session,
                        "clear_confirmation": (
                            manager.chat_session_manager
                            .clear_confirmation_phrase(
                                match.group(1)
                            )
                        ),
                        "model_bridge_active": False,
                    }

                return None

            def _dispatch_read(
                self,
                *,
                send_body: bool,
            ) -> None:
                if not manager._host_header_allowed(
                    self.headers.get("Host", "")
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": (
                                "host_header_not_allowlisted"
                            ),
                        },
                        send_body=send_body,
                    )
                    return

                path = urlsplit(self.path).path

                if path in manager.CHAT_ASSET_ROUTES:
                    try:
                        body = manager.chat_web_manager.asset_bytes(
                            path
                        )
                        content_type = (
                            manager.chat_web_manager
                            .asset_content_type(path)
                        )
                    except Exception as exc:
                        self._send_json(
                            503,
                            {
                                "status": "degraded",
                                "error": (
                                    "chat_asset_unavailable"
                                ),
                                "detail": (
                                    f"{type(exc).__name__}: "
                                    f"{exc}"
                                ),
                            },
                            send_body=send_body,
                        )
                        return

                    self._send(
                        200,
                        body,
                        content_type,
                        send_body=send_body,
                    )
                    return

                if path == "/health":
                    payload = manager._health_payload(
                        int(bound_port_getter())
                    )
                    payload.update(
                        {
                            "service": (
                                "AURA Interactive Control Center "
                                "Chat Runtime"
                            ),
                            "sprint": 188,
                            "control_center_backend": True,
                            "control_center_backend_routes": 9,
                            "control_center_panels": 8,
                            "control_center_web_shell": True,
                            "control_center_shell_assets": 3,
                            "browser_chat_session_runtime": True,
                            "browser_chat_http_routes": 7,
                            "browser_chat_assets": 3,
                            "local_model_bridge_http_routes": 2,
                            "total_route_contracts": 30,
                            "model_bridge_configured": (
                                manager.local_model_chat_manager
                                .status()["configured"]
                            ),
                            "model_bridge_enabled": (
                                manager.local_model_chat_manager
                                .status()["enabled"]
                            ),
                            "model_bridge_active": (
                                manager.local_model_chat_manager
                                .status()["active"]
                            ),
                            "model_bridge_provider": (
                                manager.local_model_chat_manager
                                .status()["provider"]
                            ),
                            "model_bridge_model": (
                                manager.local_model_chat_manager
                                .status()["model"]
                            ),
                            "browser_chat_model_connected": True,
                            "browser_auto_launch": False,
                            "bounded_session_mutation": True,
                        }
                    )
                    self._send_json(
                        200,
                        payload,
                        send_body=send_body,
                    )
                    return

                try:
                    chat_payload = self._chat_read_payload(path)
                except Exception as exc:
                    status, payload = manager._chat_error_payload(
                        exc
                    )
                    self._send_json(
                        status,
                        payload,
                        send_body=send_body,
                    )
                    return

                if chat_payload is not None:
                    status, payload = chat_payload
                    self._send_json(
                        status,
                        payload,
                        send_body=send_body,
                    )
                    return

                super()._dispatch_read(
                    send_body=send_body
                )

            def _read_json_body(
                self,
            ) -> dict[str, Any] | None:
                content_type = self.headers.get(
                    "Content-Type",
                    "",
                )
                if (
                    content_type.split(";", 1)[0].strip().lower()
                    != "application/json"
                ):
                    self._send_json(
                        415,
                        {
                            "status": "blocked",
                            "reason": (
                                "application_json_required"
                            ),
                        },
                        send_body=True,
                    )
                    return None

                transfer_encoding = self.headers.get(
                    "Transfer-Encoding",
                    "",
                )
                if transfer_encoding:
                    self._send_json(
                        400,
                        {
                            "status": "blocked",
                            "reason": (
                                "transfer_encoding_not_supported"
                            ),
                        },
                        send_body=True,
                    )
                    return None

                content_length_text = self.headers.get(
                    "Content-Length"
                )
                if content_length_text is None:
                    self._send_json(
                        411,
                        {
                            "status": "blocked",
                            "reason": "content_length_required",
                        },
                        send_body=True,
                    )
                    return None
                try:
                    content_length = int(
                        content_length_text
                    )
                except ValueError:
                    self._send_json(
                        400,
                        {
                            "status": "blocked",
                            "reason": "invalid_content_length",
                        },
                        send_body=True,
                    )
                    return None

                if content_length < 0:
                    self._send_json(
                        400,
                        {
                            "status": "blocked",
                            "reason": "invalid_content_length",
                        },
                        send_body=True,
                    )
                    return None
                if (
                    content_length
                    > manager.MAX_REQUEST_BODY_BYTES
                ):
                    self._send_json(
                        413,
                        {
                            "status": "blocked",
                            "reason": "request_body_too_large",
                            "max_bytes": (
                                manager.MAX_REQUEST_BODY_BYTES
                            ),
                        },
                        send_body=True,
                    )
                    return None

                body = self.rfile.read(content_length)
                try:
                    payload = json.loads(
                        body.decode("utf-8")
                    )
                except (
                    UnicodeDecodeError,
                    json.JSONDecodeError,
                ):
                    self._send_json(
                        400,
                        {
                            "status": "invalid_request",
                            "reason": "invalid_json",
                        },
                        send_body=True,
                    )
                    return None

                if not isinstance(payload, dict):
                    self._send_json(
                        400,
                        {
                            "status": "invalid_request",
                            "reason": "json_object_required",
                        },
                        send_body=True,
                    )
                    return None
                return payload

            def _chat_mutation_guard(self) -> bool:
                if not manager._host_header_allowed(
                    self.headers.get("Host", "")
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": (
                                "host_header_not_allowlisted"
                            ),
                        },
                        send_body=True,
                    )
                    return False

                if (
                    self.headers.get(
                        manager.LOCAL_INTENT_HEADER
                    )
                    != manager.LOCAL_INTENT_VALUE
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": (
                                "local_intent_header_required"
                            ),
                        },
                        send_body=True,
                    )
                    return False

                if not manager._request_origin_allowed(
                    self.headers.get("Origin")
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": (
                                "same_origin_required"
                            ),
                        },
                        send_body=True,
                    )
                    return False

                return True

            def do_POST(self) -> None:
                path = urlsplit(self.path).path

                create_route = (
                    path == "/api/chat/sessions"
                )
                message_match = (
                    manager._SESSION_MESSAGE_RE.fullmatch(
                        path
                    )
                )
                clear_match = (
                    manager._SESSION_CLEAR_RE.fullmatch(
                        path
                    )
                )
                model_message_match = (
                    manager._SESSION_MODEL_MESSAGE_RE
                    .fullmatch(path)
                )
                model_probe_route = (
                    path == "/api/model/probe"
                )

                if not (
                    create_route
                    or message_match is not None
                    or clear_match is not None
                    or model_message_match is not None
                    or model_probe_route
                ):
                    self._reject_mutation()
                    return

                if not self._chat_mutation_guard():
                    return

                payload = self._read_json_body()
                if payload is None:
                    return

                try:
                    if create_route:
                        allowed = {"title"}
                        if not set(payload).issubset(allowed):
                            raise BrowserChatValidationError(
                                "Unknown create-session field."
                            )
                        result = (
                            manager.chat_session_manager
                            .create_session(
                                title=payload.get("title")
                            )
                        )
                        status = 201
                    elif model_probe_route:
                        if set(payload) != {
                            "confirm_local_connection"
                        }:
                            raise LocalModelBridgeValidationError(
                                "Model probe requires only "
                                "confirm_local_connection."
                            )
                        result = (
                            manager.local_model_chat_manager
                            .probe(
                                confirm_local_connection=(
                                    payload[
                                        "confirm_local_connection"
                                    ]
                                )
                            )
                        )
                        status = 200
                    elif model_message_match is not None:
                        allowed = {
                            "content",
                            "client_message_id",
                            "expected_revision",
                            "request_id",
                            "confirm_model_request",
                        }
                        if set(payload) != allowed:
                            raise LocalModelBridgeValidationError(
                                "Model-message fields must be "
                                "content, client_message_id, "
                                "expected_revision, request_id, "
                                "and confirm_model_request."
                            )
                        result = (
                            manager.local_model_chat_manager
                            .submit_model_message(
                                model_message_match.group(1),
                                content=payload["content"],
                                client_message_id=payload[
                                    "client_message_id"
                                ],
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                                request_id=payload[
                                    "request_id"
                                ],
                                confirm_model_request=payload[
                                    "confirm_model_request"
                                ],
                            )
                        )
                        status = 200
                    elif message_match is not None:
                        allowed = {
                            "content",
                            "client_message_id",
                            "expected_revision",
                        }
                        if set(payload) != allowed:
                            raise BrowserChatValidationError(
                                "Submit-message fields must be "
                                "content, client_message_id, and "
                                "expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .submit_message(
                                message_match.group(1),
                                content=payload["content"],
                                client_message_id=payload[
                                    "client_message_id"
                                ],
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    else:
                        assert clear_match is not None
                        allowed = {
                            "confirmation",
                            "expected_revision",
                        }
                        if set(payload) != allowed:
                            raise BrowserChatValidationError(
                                "Clear-session fields must be "
                                "confirmation and "
                                "expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .clear_session(
                                clear_match.group(1),
                                confirmation=payload[
                                    "confirmation"
                                ],
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200

                    self._send_json(
                        status,
                        result,
                        send_body=True,
                    )
                except Exception as exc:
                    status, error_payload = (
                        manager._chat_error_payload(exc)
                    )
                    self._send_json(
                        status,
                        error_payload,
                        send_body=True,
                    )

        return BrowserChatSessionHandler


@dataclass(frozen=True)
class BrowserChatSessionRuntimeBundle:
    """Connected Sprint 186 runtime objects."""

    web_runtime: AuraBrowserChatSessionHttpRuntimeManager
    lifecycle_manager: AuraServiceLifecycleRuntimeManager


def build_browser_chat_session_runtime_bundle(
    project_root: str | Path | None = None,
    *,
    chat_storage_dir: str | Path | None = None,
) -> BrowserChatSessionRuntimeBundle:
    """Build one shared Sprint 186 lifecycle/listener object graph."""

    web_runtime = AuraBrowserChatSessionHttpRuntimeManager(
        project_root=project_root,
        chat_storage_dir=chat_storage_dir,
    )
    lifecycle_manager = AuraServiceLifecycleRuntimeManager(
        web_runtime=web_runtime
    )

    from aura.health_status_api_runtime import (
        AuraHealthStatusApiRuntimeManager,
    )
    from aura.control_center_backend_runtime import (
        AuraControlCenterBackendRuntimeManager,
    )

    status_manager = AuraHealthStatusApiRuntimeManager(
        project_root=project_root,
        lifecycle_manager=lifecycle_manager,
    )
    backend_manager = AuraControlCenterBackendRuntimeManager(
        project_root=project_root,
        status_manager=status_manager,
    )

    web_runtime.attach_status_manager(status_manager)
    web_runtime.attach_backend_manager(backend_manager)

    return BrowserChatSessionRuntimeBundle(
        web_runtime=web_runtime,
        lifecycle_manager=lifecycle_manager,
    )


def build_browser_chat_session_lifecycle_manager(
    project_root: str | Path | None = None,
) -> AuraServiceLifecycleRuntimeManager:
    """Return the connected lifecycle manager used by the main CLI."""

    return build_browser_chat_session_runtime_bundle(
        project_root=project_root
    ).lifecycle_manager
