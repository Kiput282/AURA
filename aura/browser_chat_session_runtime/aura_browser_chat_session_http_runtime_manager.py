"""HTTP integration for Sprint 186 local browser chat sessions."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Type
from urllib.parse import parse_qs, urlsplit
from http.server import BaseHTTPRequestHandler

from aura.control_center_web_shell_runtime import (
    AuraControlCenterWebShellHttpRuntimeManager,
    AuraControlCenterWebShellRuntimeManager,
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
from aura.local_model_router_activation.local_model_router_activation_contract import (
    LocalModelRouterActivationContract,
)
from aura.local_model_bridge_runtime.aura_local_model_browser_chat_runtime_manager import (
    AuraLocalModelBrowserChatRuntimeManager,
)
from aura.permission_audit_recovery_visibility_runtime import (
    AuraPermissionAuditRecoveryVisibilityRuntimeManager,
    AuraPermissionAuditRecoveryWebSurfaceManager,
)


from aura.review_first_memory_integration import (
    ReviewFirstMemoryConflictError,
    ReviewFirstMemoryIntegrationRuntimeManager,
    ReviewFirstMemoryNotFoundError,
    ReviewFirstMemoryValidationError,
)
from aura.voice.voice_daily_use_runtime_manager import (
    AuraVoiceDailyUseRuntimeManager,
    VoiceDailyUseBackendError,
    VoiceDailyUseBusyError,
    VoiceDailyUseConfigurationError,
    VoiceDailyUseRuntimeError,
    VoiceDailyUseValidationError,
)


class AuraBrowserChatSessionHttpRuntimeManager(
    AuraControlCenterWebShellHttpRuntimeManager
):
    """Serve bounded chat routes on the existing localhost listener."""

    name = "aura_browser_chat_session_http_runtime"
    component_version = "0.1.0-alpha"
    sprint = 189
    PRIMARY_MODEL_ROUTE = "companion"
    OPERATIONAL_MODEL_ENDPOINT = (
        "/api/chat/sessions/{session_id}/model-messages"
    )

    CHAT_ASSET_ROUTES = (
        AuraBrowserChatWebSurfaceManager.ASSET_ROUTES
    )
    CHAT_FIXED_GET_ROUTES = (
        '/api/chat/status',
        '/api/chat/sessions',
        '/api/chat/recovery',
        '/api/chat/memory-review',
    )
    CHAT_ROUTE_CONTRACTS = (
        'GET /api/chat/status',
        'GET /api/chat/sessions',
        'GET /api/chat/recovery',
        'GET /api/chat/memory-review',
        'POST /api/chat/memory-review/candidates',
        'POST /api/chat/memory-review/candidates/{candidate_id}/edit',
        'POST /api/chat/memory-review/candidates/{candidate_id}/approve-preview',
        'POST /api/chat/memory-review/candidates/{candidate_id}/reject',
        'POST /api/chat/sessions',
        'GET /api/chat/sessions/{session_id}',
        'POST /api/chat/sessions/{session_id}/resume',
        'POST /api/chat/sessions/{session_id}/rename',
        'POST /api/chat/sessions/{session_id}/archive',
        'POST /api/chat/sessions/{session_id}/restore',
        'POST /api/chat/sessions/{session_id}/messages',
        'POST /api/chat/sessions/{session_id}/model-messages',
        'POST /api/chat/sessions/{session_id}/clear',
    )
    MODEL_ROUTE_CONTRACTS = (
        "GET /api/model/status",
        "POST /api/model/probe",
    )
    VOICE_ROUTE_CONTRACTS = (
        "GET /api/voice/status",
        "POST /api/voice/transcribe",
        "POST /api/voice/synthesize",
    )
    VISIBILITY_ASSET_ROUTES = (
        AuraPermissionAuditRecoveryWebSurfaceManager.ASSET_ROUTES
    )
    VISIBILITY_API_ROUTES = (
        AuraPermissionAuditRecoveryWebSurfaceManager.API_ROUTES
    )
    VISIBILITY_ROUTE_CONTRACTS = (
        "GET /api/visibility/status",
        "GET /api/visibility/permissions",
        "GET /api/visibility/audit",
        "GET /api/visibility/recovery",
    )
    VISIBILITY_TOTAL_ROUTE_COUNT = (
        len(VISIBILITY_ASSET_ROUTES)
        + len(VISIBILITY_ROUTE_CONTRACTS)
    )
    TOTAL_ROUTE_CONTRACT_COUNT = 50
    MAX_REQUEST_BODY_BYTES = 65536
    MAX_VOICE_AUDIO_BYTES = (
        AuraVoiceDailyUseRuntimeManager.MAX_AUDIO_BYTES
    )
    LOCAL_INTENT_HEADER = "X-AURA-Local-Intent"
    LOCAL_INTENT_VALUE = "browser-chat-session"
    VOICE_CONFIRM_HEADER = "X-AURA-Voice-Confirm"
    VOICE_MICROPHONE_CONFIRM_VALUE = "microphone-listen"
    VOICE_REQUEST_ID_HEADER = "X-AURA-Request-ID"

    _SESSION_DETAIL_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})$"
    )
    _SESSION_RESUME_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/resume$"
    )
    _SESSION_RENAME_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/rename$"
    )
    _SESSION_ARCHIVE_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/archive$"
    )
    _SESSION_RESTORE_RE = re.compile(
        r"^/api/chat/sessions/(chat_[0-9a-f]{32})/restore$"
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

    _MEMORY_CANDIDATE_EDIT_RE = re.compile(
        r"^/api/chat/memory-review/candidates/"
        r"(memory_candidate_[0-9a-f]{24})/edit$"
    )
    _MEMORY_CANDIDATE_APPROVE_RE = re.compile(
        r"^/api/chat/memory-review/candidates/"
        r"(memory_candidate_[0-9a-f]{24})/"
        r"approve-preview$"
    )
    _MEMORY_CANDIDATE_REJECT_RE = re.compile(
        r"^/api/chat/memory-review/candidates/"
        r"(memory_candidate_[0-9a-f]{24})/reject$"
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
        self.memory_review_manager = (
            ReviewFirstMemoryIntegrationRuntimeManager(
                project_root=project_root
            )
        )

        try:
            local_model_profile = (
                AuraLocalModelBridgeProfileResolver
                .resolve(os.environ)
            )
            if local_model_profile is None:
                settings_profile = (
                    LocalModelRouterActivationContract(
                        project_root=self.project_root
                    )
                    .profile_mapping()
                )
                local_model_profile = {
                    key: settings_profile[key]
                    for key in (
                        "provider",
                        "base_url",
                        "model",
                        "enabled",
                        "timeout_seconds",
                        "max_output_tokens",
                        "temperature",
                    )
                }
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
        self.permission_audit_recovery_manager = (
            AuraPermissionAuditRecoveryVisibilityRuntimeManager(
                os.environ
            )
        )
        self.permission_audit_recovery_web_manager = (
            AuraPermissionAuditRecoveryWebSurfaceManager(
                project_root=project_root
            )
        )
        self.voice_daily_use_manager = (
            AuraVoiceDailyUseRuntimeManager(
                project_root=project_root
            )
        )

    def operational_model_handoff_status(
        self,
    ) -> dict[str, Any]:
        return {
            "operational_browser_chat_model_handoff": True,
            "browser_chat_connected": True,
            "model_message_route_available": True,
            "primary_model_route": self.PRIMARY_MODEL_ROUTE,
            "operational_model_endpoint": (
                self.OPERATIONAL_MODEL_ENDPOINT
            ),
            "explicit_model_confirmation_required": True,
            "save_only_fallback_available": True,
            "model_output_text_only": True,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "aura_memory_write_runtime": False,
            "network_fallback_runtime": False,
            "runtime_mutated": False,
        }

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
            "permission_audit_recovery_visibility_runtime": True,
            "permission_audit_recovery_http_routes": True,
            "permission_audit_recovery_api_route_count": len(
                self.VISIBILITY_ROUTE_CONTRACTS
            ),
            "permission_audit_recovery_asset_route_count": len(
                self.VISIBILITY_ASSET_ROUTES
            ),
            "permission_audit_recovery_total_route_count": (
                self.VISIBILITY_TOTAL_ROUTE_COUNT
            ),
            "permission_audit_recovery_read_only": True,
            "permission_mutation_runtime": False,
            "audit_writer_runtime": False,
            "automatic_recovery_runtime": False,
            "browser_chat_model_bridge_runtime": True,
            "explicit_model_request_confirmation": True,
            "explicit_model_probe_confirmation": True,
            "bounded_session_mutation": True,
            "session_list_filter_runtime": True,
            "session_resume_runtime": True,
            "session_rename_runtime": True,
            "session_archive_runtime": True,
            "session_restore_runtime": True,
            "chat_history_recovery_diagnostic": True,
            "chat_history_recovery_read_only": True,
            "chat_history_recovery_route": (
                "/api/chat/recovery"
            ),
            "automatic_history_repair": False,
            "corrupt_session_overwrite": False,
            "session_quarantine_runtime": False,
            "session_permanent_delete_runtime": False,
            "cross_session_history_merge": False,
            "session_id_immutable": True,
            "json_content_type_required": True,
            "local_intent_header_required": True,
            "same_origin_required": True,
            "request_body_limit_bytes": (
                self.MAX_REQUEST_BODY_BYTES
            ),
            "model_bridge_runtime": False,
            "model_inference_runtime": False,
            "network_fallback_runtime": False,
            "review_first_memory_integration_runtime": True,
            "memory_candidate_in_process_queue": True,
            "memory_candidate_edit_runtime": True,
            "memory_candidate_reject_runtime": True,
            "memory_write_preview_runtime": True,
            "memory_candidate_persistence": False,
            "memory_review_queue_persistence": False,
            "memory_permission_grant_apply": False,
            "memory_store_constructed": False,
            "memory_store_mutation": False,
            "automatic_memory_write": False,
            "automatic_memory_merge": False,
            "automatic_memory_delete": False,
            "aura_long_term_memory_write": False,
            "voice_daily_use_runtime": True,
            "voice_route_contract_count": len(
                self.VOICE_ROUTE_CONTRACTS
            ),
            "voice_status_route": "/api/voice/status",
            "voice_transcribe_route": "/api/voice/transcribe",
            "voice_synthesize_route": "/api/voice/synthesize",
            "voice_inference_host": "ATLAS",
            "voice_capture_host": "ORION browser",
            "voice_playback_host": "ORION browser",
            "voice_audio_content_type": "audio/wav",
            "voice_audio_limit_bytes": (
                self.MAX_VOICE_AUDIO_BYTES
            ),
            "voice_single_flight": True,
            "voice_explicit_confirmation_required": True,
            "voice_raw_audio_retention": False,
            "voice_always_listening": False,
            "voice_wake_word": False,
            "voice_cloud_fallback": False,
            "voice_direct_action_dispatch": False,
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
            ReviewFirstMemoryNotFoundError,
        ):
            return 404, {
                "status": "not_found",
                "error": "memory_candidate_not_found",
                "detail": str(exc),
                "memory_store_mutated": False,
            }
        if isinstance(
            exc,
            ReviewFirstMemoryConflictError,
        ):
            return 409, {
                "status": "conflict",
                "error": "memory_candidate_conflict",
                "detail": str(exc),
                "memory_store_mutated": False,
            }
        if isinstance(
            exc,
            ReviewFirstMemoryValidationError,
        ):
            return 400, {
                "status": "invalid_request",
                "error": "memory_candidate_validation_error",
                "detail": str(exc),
                "memory_store_mutated": False,
            }
        if isinstance(
            exc,
            BrowserChatSessionNotFoundError,
        ):
            return 404, {
                "status": "not_found",
                "error": "chat_session_not_found",
                "detail": str(exc),
                "recovery": {
                    "kind": "missing_session",
                    "action": "refresh_session_list",
                    "target_state": "neutral_no_session",
                    "retryable": False,
                    "preserve_unsent_draft_in_memory": True,
                },
            }
        if isinstance(
            exc,
            BrowserChatSessionConflictError,
        ):
            detail = str(exc)
            archived = "archived" in detail.lower()
            return 409, {
                "status": "conflict",
                "error": (
                    "chat_session_archived"
                    if archived
                    else "chat_session_revision_conflict"
                ),
                "detail": detail,
                "recovery": {
                    "kind": (
                        "archived_session"
                        if archived
                        else "stale_revision"
                    ),
                    "action": (
                        "restore_session"
                        if archived
                        else "reload_current_session"
                    ),
                    "retryable": not archived,
                    "preserve_unsent_draft_in_memory": True,
                    "explicit_user_action_required": archived,
                },
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
                "recovery": {
                    "kind": "session_corruption",
                    "action": "review_recovery_status",
                    "endpoint": "/api/chat/recovery",
                    "retryable": False,
                    "original_file_preserved": True,
                    "repair_performed": False,
                    "quarantine_performed": False,
                },
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

    def _voice_error_payload(
        self,
        exc: Exception,
    ) -> tuple[int, dict[str, Any]]:
        if isinstance(exc, VoiceDailyUseBusyError):
            return 409, {
                "status": "busy",
                "error": "voice_inference_busy",
                "detail": str(exc),
                "retryable": True,
            }
        if isinstance(exc, VoiceDailyUseValidationError):
            return 400, {
                "status": "invalid_request",
                "error": "voice_validation_error",
                "detail": str(exc),
                "retryable": False,
            }
        if isinstance(exc, VoiceDailyUseConfigurationError):
            return 503, {
                "status": "degraded",
                "error": "voice_configuration_error",
                "detail": str(exc),
                "retryable": False,
            }
        if isinstance(exc, VoiceDailyUseBackendError):
            return 502, {
                "status": "backend_error",
                "error": "voice_backend_error",
                "detail": str(exc),
                "retryable": True,
            }
        if isinstance(exc, VoiceDailyUseRuntimeError):
            return 500, {
                "status": "error",
                "error": "voice_runtime_error",
                "detail": str(exc),
                "retryable": False,
            }
        return 500, {
            "status": "error",
            "error": "unexpected_voice_runtime_error",
            "detail": f"{type(exc).__name__}: {exc}",
            "retryable": False,
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
                if path == "/api/voice/status":
                    return 200, (
                        manager.voice_daily_use_manager
                        .status()
                    )

                if path == "/api/model/status":
                    return 200, (
                        manager.local_model_chat_manager
                        .status()
                    )

                if path == "/api/chat/memory-review":
                    return 200, (
                        manager.memory_review_manager
                        .list_candidates()
                    )

                if path == "/api/chat/recovery":
                    recovery = (
                        manager.chat_session_manager
                        .recovery_status()
                    )
                    return 200, {
                        **recovery,
                        "route": "/api/chat/recovery",
                        "read_only": True,
                        "mutation_allowed": False,
                    }

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
                    query = parse_qs(
                        urlsplit(self.path).query,
                        keep_blank_values=True,
                    )
                    unknown = set(query) - {"state"}
                    if unknown:
                        raise BrowserChatValidationError(
                            "Unknown session-list query field."
                        )
                    state_values = query.get("state", ["active"])
                    if len(state_values) != 1:
                        raise BrowserChatValidationError(
                            "Session-list state must appear once."
                        )
                    session_state = state_values[0] or "active"
                    sessions = (
                        manager.chat_session_manager
                        .list_sessions(state=session_state)
                    )
                    return 200, {
                        "status": "ok",
                        "state": session_state,
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

            def _visibility_read_payload(
                self,
                path: str,
            ) -> tuple[int, dict[str, Any]] | None:
                visibility = (
                    manager.permission_audit_recovery_manager
                )
                if path == "/api/visibility/status":
                    return 200, visibility.status()
                if path == "/api/visibility/permissions":
                    return 200, visibility.permission_snapshot()
                if path == "/api/visibility/audit":
                    return 200, visibility.audit_snapshot()
                if path == "/api/visibility/recovery":
                    return 200, visibility.recovery_snapshot()
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

                if path in manager.VISIBILITY_ASSET_ROUTES:
                    try:
                        body = (
                            manager.permission_audit_recovery_web_manager
                            .asset_bytes(path)
                        )
                        content_type = (
                            manager.permission_audit_recovery_web_manager
                            .asset_content_type(path)
                        )
                    except Exception as exc:
                        self._send_json(
                            503,
                            {
                                "status": "degraded",
                                "error": (
                                    "permission_audit_recovery_"
                                    "asset_unavailable"
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
                                "AURA Permission, Audit, and "
                                "Recovery Visibility Runtime"
                            ),
                            "sprint": 189,
                            "control_center_backend": True,
                            "control_center_backend_routes": 9,
                            "control_center_panels": 8,
                            "control_center_web_shell": True,
                            "control_center_shell_assets": 3,
                            "browser_chat_session_runtime": True,
                            "browser_chat_http_routes": 17,
                            "voice_daily_use_runtime": True,
                            "voice_http_routes": 3,
                            "voice_backend_ready": (
                                manager.voice_daily_use_manager
                                .status()["ready"]
                            ),
                            "voice_inference_host": "ATLAS",
                            "voice_capture_host": "ORION browser",
                            "voice_playback_host": "ORION browser",
                            "browser_chat_assets": 3,
                            "local_model_bridge_http_routes": 2,
                            "permission_audit_recovery_visibility": True,
                            "permission_audit_recovery_http_routes": 4,
                            "permission_audit_recovery_assets": 3,
                            "permission_audit_recovery_total_routes": 7,
                            "permission_audit_recovery_read_only": True,
                            "permission_mutation_runtime": False,
                            "audit_writer_runtime": False,
                            "automatic_recovery_runtime": False,
                            "total_route_contracts": 50,
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
                    visibility_payload = (
                        self._visibility_read_payload(path)
                    )
                except Exception as exc:
                    self._send_json(
                        503,
                        {
                            "status": "degraded",
                            "degraded": True,
                            "error": (
                                "permission_audit_recovery_"
                                "visibility_error"
                            ),
                            "detail": (
                                f"{type(exc).__name__}: "
                                f"{exc}"
                            ),
                            "mutation_allowed": False,
                        },
                        send_body=send_body,
                    )
                    return

                if visibility_payload is not None:
                    status, payload = visibility_payload
                    self._send_json(
                        status,
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

            def _read_voice_audio_body(
                self,
            ) -> bytes | None:
                content_type = self.headers.get(
                    "Content-Type",
                    "",
                )
                if (
                    content_type.split(";", 1)[0].strip().lower()
                    != "audio/wav"
                ):
                    self._send_json(
                        415,
                        {
                            "status": "blocked",
                            "reason": "audio_wav_required",
                        },
                        send_body=True,
                    )
                    return None

                if self.headers.get("Transfer-Encoding", ""):
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
                    content_length = int(content_length_text)
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

                if content_length <= 0:
                    self._send_json(
                        400,
                        {
                            "status": "blocked",
                            "reason": "empty_voice_audio",
                        },
                        send_body=True,
                    )
                    return None
                if content_length > manager.MAX_VOICE_AUDIO_BYTES:
                    self._send_json(
                        413,
                        {
                            "status": "blocked",
                            "reason": "voice_audio_too_large",
                            "max_bytes": (
                                manager.MAX_VOICE_AUDIO_BYTES
                            ),
                        },
                        send_body=True,
                    )
                    return None
                return self.rfile.read(content_length)

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

                voice_transcribe_route = (
                    path == "/api/voice/transcribe"
                )
                voice_synthesize_route = (
                    path == "/api/voice/synthesize"
                )
                if (
                    voice_transcribe_route
                    or voice_synthesize_route
                ):
                    if not self._chat_mutation_guard():
                        return
                    request_id = self.headers.get(
                        manager.VOICE_REQUEST_ID_HEADER
                    )
                    try:
                        if voice_transcribe_route:
                            if (
                                self.headers.get(
                                    manager.VOICE_CONFIRM_HEADER
                                )
                                != manager.VOICE_MICROPHONE_CONFIRM_VALUE
                            ):
                                self._send_json(
                                    403,
                                    {
                                        "status": "blocked",
                                        "reason": (
                                            "microphone_confirmation_"
                                            "required"
                                        ),
                                    },
                                    send_body=True,
                                )
                                return
                            audio = self._read_voice_audio_body()
                            if audio is None:
                                return
                            result = (
                                manager.voice_daily_use_manager
                                .transcribe_wav_bytes(
                                    audio,
                                    request_id=request_id,
                                )
                            )
                            self._send_json(
                                200,
                                result,
                                send_body=True,
                            )
                            return

                        payload = self._read_json_body()
                        if payload is None:
                            return
                        if set(payload) != {
                            "text",
                            "confirm_speak",
                        }:
                            raise VoiceDailyUseValidationError(
                                "TTS fields must be text and "
                                "confirm_speak."
                            )
                        if payload["confirm_speak"] is not True:
                            raise VoiceDailyUseValidationError(
                                "TTS playback requires explicit "
                                "speaker confirmation."
                            )
                        audio, _metadata = (
                            manager.voice_daily_use_manager
                            .synthesize_wav(
                                payload["text"],
                                request_id=request_id,
                            )
                        )
                        self._send(
                            200,
                            audio,
                            "audio/wav",
                            send_body=True,
                        )
                        return
                    except Exception as exc:
                        status, error_payload = (
                            manager._voice_error_payload(exc)
                        )
                        self._send_json(
                            status,
                            error_payload,
                            send_body=True,
                        )
                        return

                create_route = (
                    path == "/api/chat/sessions"
                )
                resume_match = (
                    manager._SESSION_RESUME_RE.fullmatch(
                        path
                    )
                )
                rename_match = (
                    manager._SESSION_RENAME_RE.fullmatch(
                        path
                    )
                )
                archive_match = (
                    manager._SESSION_ARCHIVE_RE.fullmatch(
                        path
                    )
                )
                restore_match = (
                    manager._SESSION_RESTORE_RE.fullmatch(
                        path
                    )
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
                memory_candidate_create_route = (
                    path
                    == "/api/chat/memory-review/candidates"
                )
                memory_candidate_edit_match = (
                    manager._MEMORY_CANDIDATE_EDIT_RE
                    .fullmatch(path)
                )
                memory_candidate_approve_match = (
                    manager._MEMORY_CANDIDATE_APPROVE_RE
                    .fullmatch(path)
                )
                memory_candidate_reject_match = (
                    manager._MEMORY_CANDIDATE_REJECT_RE
                    .fullmatch(path)
                )

                if not (
                    create_route
                    or resume_match is not None
                    or rename_match is not None
                    or archive_match is not None
                    or restore_match is not None
                    or message_match is not None
                    or clear_match is not None
                    or model_message_match is not None
                    or model_probe_route
                    or memory_candidate_create_route
                    or memory_candidate_edit_match is not None
                    or memory_candidate_approve_match is not None
                    or memory_candidate_reject_match is not None
                ):
                    self._reject_mutation()
                    return

                if not self._chat_mutation_guard():
                    return

                payload = self._read_json_body()
                if payload is None:
                    return

                try:
                    if memory_candidate_create_route:
                        allowed = {
                            "session_id",
                            "message_id",
                            "confirm_memory_candidate",
                        }
                        if set(payload) != allowed:
                            raise ReviewFirstMemoryValidationError(
                                "Memory candidate creation fields must be "
                                "session_id, message_id, and "
                                "confirm_memory_candidate."
                            )
                        if (
                            payload["confirm_memory_candidate"]
                            is not True
                        ):
                            raise ReviewFirstMemoryValidationError(
                                "Memory candidate creation requires "
                                "explicit confirmation."
                            )
                        session = (
                            manager.chat_session_manager
                            .load_session(payload["session_id"])
                        )
                        message_matches = [
                            item
                            for item in session["messages"]
                            if item["message_id"]
                            == payload["message_id"]
                        ]
                        if len(message_matches) != 1:
                            raise ReviewFirstMemoryNotFoundError(
                                "Source user message was not found."
                            )
                        source_message = message_matches[0]
                        if source_message["role"] != "user":
                            raise ReviewFirstMemoryValidationError(
                                "Only a user message can become a "
                                "memory candidate."
                            )
                        result = (
                            manager.memory_review_manager
                            .create_candidate(
                                content=source_message["content"],
                                source_session_id=session[
                                    "session_id"
                                ],
                                source_message_id=source_message[
                                    "message_id"
                                ],
                                source_sequence=source_message[
                                    "sequence"
                                ],
                            )
                        )
                        status = 201
                    elif memory_candidate_edit_match is not None:
                        allowed = {
                            "content",
                            "category",
                            "importance",
                            "pinned",
                            "expected_revision",
                            "confirm_review_edit",
                        }
                        if set(payload) != allowed:
                            raise ReviewFirstMemoryValidationError(
                                "Memory candidate edit fields are invalid."
                            )
                        if payload["confirm_review_edit"] is not True:
                            raise ReviewFirstMemoryValidationError(
                                "Memory candidate edit requires "
                                "explicit confirmation."
                            )
                        result = (
                            manager.memory_review_manager
                            .edit_candidate(
                                memory_candidate_edit_match.group(1),
                                content=payload["content"],
                                category=payload["category"],
                                importance=payload["importance"],
                                pinned=payload["pinned"],
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif memory_candidate_approve_match is not None:
                        if set(payload) != {
                            "expected_revision",
                            "confirm_review_approval",
                        }:
                            raise ReviewFirstMemoryValidationError(
                                "Memory approval-preview fields are invalid."
                            )
                        if (
                            payload["confirm_review_approval"]
                            is not True
                        ):
                            raise ReviewFirstMemoryValidationError(
                                "Approval preview requires explicit "
                                "review confirmation."
                            )
                        result = (
                            manager.memory_review_manager
                            .approve_write_preview(
                                memory_candidate_approve_match
                                .group(1),
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif memory_candidate_reject_match is not None:
                        if set(payload) != {
                            "expected_revision",
                            "confirm_reject",
                        }:
                            raise ReviewFirstMemoryValidationError(
                                "Memory rejection fields are invalid."
                            )
                        if payload["confirm_reject"] is not True:
                            raise ReviewFirstMemoryValidationError(
                                "Memory rejection requires explicit "
                                "confirmation."
                            )
                        result = (
                            manager.memory_review_manager
                            .reject_candidate(
                                memory_candidate_reject_match
                                .group(1),
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif create_route:
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
                    elif resume_match is not None:
                        if set(payload) != {"expected_revision"}:
                            raise BrowserChatValidationError(
                                "Resume-session requires only "
                                "expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .resume_session(
                                resume_match.group(1),
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif rename_match is not None:
                        if set(payload) != {
                            "title",
                            "expected_revision",
                        }:
                            raise BrowserChatValidationError(
                                "Rename-session fields must be title "
                                "and expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .rename_session(
                                rename_match.group(1),
                                title=payload["title"],
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif archive_match is not None:
                        if set(payload) != {"expected_revision"}:
                            raise BrowserChatValidationError(
                                "Archive-session requires only "
                                "expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .archive_session(
                                archive_match.group(1),
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
                    elif restore_match is not None:
                        if set(payload) != {"expected_revision"}:
                            raise BrowserChatValidationError(
                                "Restore-session requires only "
                                "expected_revision."
                            )
                        result = (
                            manager.chat_session_manager
                            .restore_session(
                                restore_match.group(1),
                                expected_revision=payload[
                                    "expected_revision"
                                ],
                            )
                        )
                        status = 200
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
    shell_manager = AuraControlCenterWebShellRuntimeManager(
        project_root=project_root
    )

    web_runtime.attach_status_manager(status_manager)
    web_runtime.attach_backend_manager(backend_manager)
    web_runtime.attach_shell_manager(shell_manager)

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
