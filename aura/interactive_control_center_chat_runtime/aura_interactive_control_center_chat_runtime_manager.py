"""Sprint 188 Interactive Control Center Chat orchestration runtime."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping


class InteractiveControlCenterChatError(RuntimeError):
    """Raised when the bounded interactive chat contract is invalid."""


class AuraInteractiveControlCenterChatRuntimeManager:
    """Compose the Sprint 188 web surface and Sprint 187 model backend."""

    name = "aura_interactive_control_center_chat_runtime"
    component_version = "0.1.0-alpha"
    sprint = 188
    schema_version = "1.0"

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
    ASSET_ROUTES = (
        "/chat",
        "/assets/control-center-chat.css",
        "/assets/control-center-chat.js",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        from aura.browser_chat_session_runtime.aura_browser_chat_web_surface_manager import (
            AuraBrowserChatWebSurfaceManager,
        )

        self.web_surface = AuraBrowserChatWebSurfaceManager(
            project_root=project_root
        )

    def contracts(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ready",
            "asset_routes": list(self.ASSET_ROUTES),
            "asset_route_count": len(self.ASSET_ROUTES),
            "chat_routes": list(self.CHAT_ROUTE_CONTRACTS),
            "chat_route_count": len(self.CHAT_ROUTE_CONTRACTS),
            "model_routes": list(self.MODEL_ROUTE_CONTRACTS),
            "model_route_count": len(self.MODEL_ROUTE_CONTRACTS),
            "total_local_route_count": (
                len(self.ASSET_ROUTES)
                + len(self.CHAT_ROUTE_CONTRACTS)
                + len(self.MODEL_ROUTE_CONTRACTS)
                + 18
            ),
            "save_only_default": True,
            "local_model_mode_explicit": True,
            "model_request_confirmation_per_message": True,
            "model_probe_confirmation_per_request": True,
            "stable_retry_identifiers_in_memory": True,
            "response_kind_visibility": True,
            "placeholder_route_preserved": True,
            "model_provider_enabled_by_default": False,
        }

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "interactive_chat_runtime": True,
            "browser_chat_session_runtime": True,
            "local_model_bridge_runtime": True,
            "model_provider_enabled_by_default": False,
            "model_request_confirmation_required": True,
            "model_probe_confirmation_required": True,
            "save_only_default": True,
            "idempotent_retry_runtime": True,
            "revision_conflict_runtime": True,
            "response_kind_visibility": True,
            "model_download_runtime": False,
            "remote_provider_runtime": False,
            "internet_fallback_runtime": False,
            "streaming_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "arbitrary_file_read_runtime": False,
            "arbitrary_file_write_runtime": False,
            "aura_long_term_memory_write_runtime": False,
            "desktop_control_runtime": False,
            "background_service_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
            "browser_auto_launch": False,
            "local_browser_storage_runtime": False,
            "websocket_runtime": False,
            "eventsource_runtime": False,
            "autonomous_action_runtime": False,
        }

    def status(self) -> dict[str, Any]:
        web = self.web_surface.status()
        contracts = self.contracts()
        safety = self.safety_boundary()

        ready = (
            web["status"] == "ok"
            and web["degraded"] is False
            and web["interactive_chat_runtime"] is True
            and web["model_bridge_connected"] is True
        )
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ready" if ready else "degraded",
            "degraded": not ready,
            "interactive_chat_ready": ready,
            "asset_count": web["asset_count"],
            "chat_route_count": contracts["chat_route_count"],
            "model_route_count": contracts["model_route_count"],
            "total_local_route_count": (
                contracts["total_local_route_count"]
            ),
            "save_only_default": True,
            "local_model_mode_explicit": True,
            "model_provider_enabled_by_default": False,
            "model_request_confirmation_ui": (
                web["model_request_confirmation_ui"]
            ),
            "model_probe_confirmation_ui": (
                web["model_probe_confirmation_ui"]
            ),
            "idempotent_retry_ui": (
                web["idempotent_retry_ui"]
            ),
            "response_kind_visibility": (
                web["response_kind_visibility"]
            ),
            "placeholder_route_available": (
                web["placeholder_route_available"]
            ),
            "provider_network_calls": 0,
            "safety_boundary": safety,
        }

    def self_test(self) -> dict[str, Any]:
        from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
            AuraBrowserChatSessionRuntimeManager,
            BrowserChatSessionConflictError,
        )
        from aura.local_model_bridge_runtime.aura_local_model_bridge_runtime_manager import (
            AuraLocalModelBridgeRuntimeManager,
            LocalModelBridgePermissionError,
            LocalModelBridgeTransportError,
            LocalModelTransportResponse,
        )
        from aura.local_model_bridge_runtime.aura_local_model_browser_chat_runtime_manager import (
            AuraLocalModelBrowserChatRuntimeManager,
        )

        assertions: dict[str, bool] = {}

        status = self.status()
        contracts = self.contracts()
        safety = self.safety_boundary()
        web_test = self.web_surface.self_test()

        assertions["status_ready"] = (
            status["status"] == "ready"
        )
        assertions["status_not_degraded"] = (
            status["degraded"] is False
        )
        assertions["interactive_ready"] = (
            status["interactive_chat_ready"] is True
        )
        assertions["sprint_188"] = (
            status["sprint"] == 188
        )
        assertions["component_version"] = (
            status["component_version"] == "0.1.0-alpha"
        )
        assertions["asset_count_three"] = (
            status["asset_count"] == 3
        )
        assertions["chat_routes_seven"] = (
            status["chat_route_count"] == 7
        )
        assertions["model_routes_two"] = (
            status["model_route_count"] == 2
        )
        assertions["total_routes_thirty"] = (
            status["total_local_route_count"] == 30
        )
        assertions["save_only_default"] = (
            status["save_only_default"] is True
        )
        assertions["model_mode_explicit"] = (
            status["local_model_mode_explicit"] is True
        )
        assertions["provider_default_disabled"] = (
            status["model_provider_enabled_by_default"]
            is False
        )
        assertions["request_confirmation_ui"] = (
            status["model_request_confirmation_ui"] is True
        )
        assertions["probe_confirmation_ui"] = (
            status["model_probe_confirmation_ui"] is True
        )
        assertions["retry_ui"] = (
            status["idempotent_retry_ui"] is True
        )
        assertions["response_kind_ui"] = (
            status["response_kind_visibility"] is True
        )
        assertions["placeholder_ui"] = (
            status["placeholder_route_available"] is True
        )
        assertions["status_network_calls_zero"] = (
            status["provider_network_calls"] == 0
        )

        assertions["contracts_assets_three"] = (
            contracts["asset_route_count"] == 3
        )
        assertions["contracts_chat_seven"] = (
            contracts["chat_route_count"] == 7
        )
        assertions["contracts_model_two"] = (
            contracts["model_route_count"] == 2
        )
        assertions["contracts_total_thirty"] = (
            contracts["total_local_route_count"] == 30
        )
        assertions["contracts_save_default"] = (
            contracts["save_only_default"] is True
        )
        assertions["contracts_model_explicit"] = (
            contracts["local_model_mode_explicit"] is True
        )
        assertions["contracts_message_confirm"] = (
            contracts[
                "model_request_confirmation_per_message"
            ]
            is True
        )
        assertions["contracts_probe_confirm"] = (
            contracts[
                "model_probe_confirmation_per_request"
            ]
            is True
        )
        assertions["contracts_retry_memory"] = (
            contracts[
                "stable_retry_identifiers_in_memory"
            ]
            is True
        )
        assertions["contracts_placeholder"] = (
            contracts["placeholder_route_preserved"] is True
        )
        assertions["contracts_provider_default"] = (
            contracts["model_provider_enabled_by_default"]
            is False
        )

        assertions["web_status_ok"] = (
            web_test["status"] == "ok"
        )
        assertions["web_sprint_188"] = (
            web_test["sprint"] == 188
        )
        assertions["web_assertions_166"] = (
            web_test["assertion_count"] == 166
        )
        assertions["web_failures_zero"] = (
            web_test["failed_assertion_count"] == 0
        )
        assertions["web_interactive"] = (
            web_test["interactive_chat_runtime"] is True
        )
        assertions["web_bridge_connected"] = (
            web_test["model_bridge_connected"] is True
        )
        assertions["web_request_confirm"] = (
            web_test[
                "model_request_confirmation_ui_verified"
            ]
            is True
        )
        assertions["web_probe_confirm"] = (
            web_test[
                "model_probe_confirmation_ui_verified"
            ]
            is True
        )
        assertions["web_retry"] = (
            web_test["idempotent_retry_ui_verified"] is True
        )
        assertions["web_response_kind"] = (
            web_test[
                "response_kind_visibility_verified"
            ]
            is True
        )
        assertions["web_safe_dom"] = (
            web_test["safe_dom_rendering_verified"] is True
        )
        assertions["web_external_zero"] = (
            web_test["external_dependency_count"] == 0
        )

        for key in (
            "model_download_runtime",
            "remote_provider_runtime",
            "internet_fallback_runtime",
            "streaming_runtime",
            "tool_calling_runtime",
            "action_dispatch_runtime",
            "command_execution_runtime",
            "arbitrary_file_read_runtime",
            "arbitrary_file_write_runtime",
            "aura_long_term_memory_write_runtime",
            "desktop_control_runtime",
            "background_service_runtime",
            "public_listener_runtime",
            "lan_listener_runtime",
            "browser_auto_launch",
            "local_browser_storage_runtime",
            "websocket_runtime",
            "eventsource_runtime",
            "autonomous_action_runtime",
        ):
            assertions[f"safety_{key}_false"] = (
                safety[key] is False
            )

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
                payload: dict[str, Any],
            ) -> None:
                self.responses.append(
                    LocalModelTransportResponse(
                        status_code=status_code,
                        headers={
                            "Content-Type": "application/json"
                        },
                        body=json.dumps(payload).encode("utf-8"),
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
                        "Fake provider response queue is empty."
                    )
                return self.responses.pop(0)

        counter = 0

        def identifier() -> str:
            nonlocal counter
            counter += 1
            return f"{counter:032x}"

        with tempfile.TemporaryDirectory(
            prefix="aura-s188-interactive-chat-"
        ) as temporary:
            root = Path(temporary)
            storage = root / "data" / "chat_sessions"
            session_manager = AuraBrowserChatSessionRuntimeManager(
                project_root=root,
                storage_dir=storage,
                id_factory=identifier,
            )

            created = session_manager.create_session(
                title="Interactive contract"
            )
            session_id = created["session"]["session_id"]
            assertions["session_created"] = (
                created["status"] == "created"
            )
            assertions["session_revision_one"] = (
                created["session"]["revision"] == 1
            )
            assertions["session_messages_zero"] = (
                created["session"]["message_count"] == 0
            )

            placeholder = session_manager.submit_message(
                session_id,
                content="Save locally without model",
                client_message_id="client_s188_save_001",
                expected_revision=1,
            )
            assertions["save_only_accepted"] = (
                placeholder["status"] == "accepted"
            )
            assertions["save_only_no_model"] = (
                placeholder["model_bridge_active"] is False
            )
            assertions["save_only_response_kind"] = (
                placeholder["delivered_response"][
                    "response_kind"
                ]
                == "model_bridge_unavailable"
            )
            assertions["save_only_model_false"] = (
                placeholder["delivered_response"][
                    "model_invoked"
                ]
                is False
            )
            assertions["save_only_revision_two"] = (
                placeholder["session"]["revision"] == 2
            )
            assertions["save_only_message_count_two"] = (
                placeholder["session"]["message_count"] == 2
            )

            transport = FakeTransport()
            bridge_manager = AuraLocalModelBridgeRuntimeManager(
                {
                    "provider": "ollama",
                    "base_url": "http://127.0.0.1:11434",
                    "model": "aura-s188-test:latest",
                    "enabled": True,
                    "timeout_seconds": 5,
                    "max_output_tokens": 128,
                    "temperature": 0.1,
                },
                transport=transport,
            )
            integration = AuraLocalModelBrowserChatRuntimeManager(
                session_manager,
                bridge_manager,
            )
            active = integration.status()
            assertions["bridge_active"] = (
                active["active"] is True
            )
            assertions["bridge_provider"] = (
                active["provider"] == "ollama"
            )
            assertions["bridge_model"] = (
                active["model"]
                == "aura-s188-test:latest"
            )
            assertions["bridge_text_only"] = (
                active["model_output_text_only"] is True
            )

            blocked = False
            calls_before = len(transport.calls)
            try:
                integration.submit_model_message(
                    session_id,
                    content="Blocked without confirmation",
                    client_message_id=(
                        "client_s188_model_blocked"
                    ),
                    expected_revision=2,
                    request_id=(
                        "modelreq_s188_blocked"
                    ),
                    confirm_model_request=False,
                )
            except LocalModelBridgePermissionError:
                blocked = True

            assertions["model_confirmation_blocked"] = blocked
            assertions["blocked_no_transport"] = (
                len(transport.calls) == calls_before
            )
            assertions["blocked_no_session_write"] = (
                session_manager.load_session(session_id)[
                    "message_count"
                ]
                == 2
            )

            transport.queue(
                200,
                {
                    "model": "aura-s188-test:latest",
                    "message": {
                        "role": "assistant",
                        "content": (
                            "Interactive local model response."
                        ),
                    },
                    "done": True,
                    "done_reason": "stop",
                    "prompt_eval_count": 12,
                    "eval_count": 7,
                },
            )
            submitted = integration.submit_model_message(
                session_id,
                content="Use the local model",
                client_message_id="client_s188_model_001",
                expected_revision=2,
                request_id="modelreq_s188_model_001",
                confirm_model_request=True,
            )
            assertions["model_submit_accepted"] = (
                submitted["status"] == "accepted"
            )
            assertions["model_invoked_true"] = (
                submitted["model_invoked"] is True
            )
            assertions["model_reinvoked_true"] = (
                submitted["model_reinvoked"] is True
            )
            assertions["model_response_kind"] = (
                submitted["delivered_response"][
                    "response_kind"
                ]
                == "local_model_response"
            )
            assertions["model_response_content"] = (
                submitted["delivered_response"]["content"]
                == "Interactive local model response."
            )
            assertions["model_response_flag"] = (
                submitted["delivered_response"][
                    "model_invoked"
                ]
                is True
            )
            assertions["model_tools_false"] = (
                submitted["tools_invoked"] is False
            )
            assertions["model_actions_false"] = (
                submitted["actions_invoked"] is False
            )
            assertions["model_commands_false"] = (
                submitted["commands_invoked"] is False
            )
            assertions["model_memory_false"] = (
                submitted["aura_memory_written"] is False
            )
            assertions["model_revision_three"] = (
                submitted["session"]["revision"] == 3
            )
            assertions["model_message_count_four"] = (
                submitted["session"]["message_count"] == 4
            )
            assertions["model_transport_once"] = (
                len(transport.calls) == 1
            )

            provider_payload = json.loads(
                transport.calls[0][2].decode("utf-8")
            )
            assertions["provider_stream_false"] = (
                provider_payload["stream"] is False
            )
            assertions["provider_no_tools"] = (
                "tools" not in provider_payload
                and "functions" not in provider_payload
            )
            assertions["provider_system_first"] = (
                provider_payload["messages"][0]["role"]
                == "system"
            )
            assertions["provider_user_last"] = (
                provider_payload["messages"][-1]
                == {
                    "role": "user",
                    "content": "Use the local model",
                }
            )
            assertions["placeholder_assistant_excluded"] = (
                not any(
                    message["role"] == "assistant"
                    and "saved in this local session"
                    in message["content"]
                    for message in provider_payload["messages"]
                )
            )

            calls_before_duplicate = len(transport.calls)
            duplicate = integration.submit_model_message(
                session_id,
                content="Retry content is ignored",
                client_message_id="client_s188_model_001",
                expected_revision=2,
                request_id="modelreq_s188_retry_001",
                confirm_model_request=True,
            )
            assertions["duplicate_status"] = (
                duplicate["status"] == "duplicate"
            )
            assertions["duplicate_replay"] = (
                duplicate["idempotent_replay"] is True
            )
            assertions["duplicate_no_reinvoke"] = (
                duplicate["model_reinvoked"] is False
            )
            assertions["duplicate_transport_unchanged"] = (
                len(transport.calls)
                == calls_before_duplicate
            )
            assertions["duplicate_revision_three"] = (
                duplicate["session"]["revision"] == 3
            )

            conflict = False
            calls_before_conflict = len(transport.calls)
            try:
                integration.submit_model_message(
                    session_id,
                    content="Stale new request",
                    client_message_id="client_s188_model_002",
                    expected_revision=2,
                    request_id="modelreq_s188_stale_001",
                    confirm_model_request=True,
                )
            except BrowserChatSessionConflictError:
                conflict = True

            assertions["stale_conflict"] = conflict
            assertions["stale_no_transport"] = (
                len(transport.calls)
                == calls_before_conflict
            )
            assertions["stale_no_write"] = (
                session_manager.load_session(session_id)[
                    "message_count"
                ]
                == 4
            )

            transport.queue(
                503,
                {"error": "provider_unavailable"},
            )
            provider_failed = False
            calls_before_failure = len(transport.calls)
            try:
                integration.submit_model_message(
                    session_id,
                    content="Provider failure",
                    client_message_id="client_s188_model_003",
                    expected_revision=3,
                    request_id="modelreq_s188_failure_001",
                    confirm_model_request=True,
                )
            except LocalModelBridgeTransportError:
                provider_failed = True

            assertions["provider_failure_visible"] = (
                provider_failed
            )
            assertions["provider_failure_one_call"] = (
                len(transport.calls)
                == calls_before_failure + 1
            )
            assertions["provider_failure_no_write"] = (
                session_manager.load_session(session_id)[
                    "message_count"
                ]
                == 4
            )

            reloaded_manager = AuraBrowserChatSessionRuntimeManager(
                project_root=root,
                storage_dir=storage,
                id_factory=identifier,
            )
            reloaded = reloaded_manager.load_session(
                session_id
            )
            assertions["reload_message_count_four"] = (
                reloaded["message_count"] == 4
            )
            assertions["reload_revision_three"] = (
                reloaded["revision"] == 3
            )
            assertions["reload_placeholder_kind"] = (
                reloaded["messages"][1]["response_kind"]
                == "model_bridge_unavailable"
            )
            assertions["reload_model_kind"] = (
                reloaded["messages"][3]["response_kind"]
                == "local_model_response"
            )
            assertions["reload_model_flag"] = (
                reloaded["messages"][3]["model_invoked"]
                is True
            )
            assertions["reload_integrity_valid"] = (
                reloaded["integrity_sha256"]
                == reloaded_manager._integrity_digest(
                    reloaded
                )
            )

            bad_clear = False
            try:
                reloaded_manager.clear_session(
                    session_id,
                    confirmation="CLEAR wrong_session",
                    expected_revision=3,
                )
            except Exception:
                bad_clear = True

            assertions["bad_clear_blocked"] = bad_clear
            assertions["bad_clear_no_write"] = (
                reloaded_manager.load_session(session_id)[
                    "message_count"
                ]
                == 4
            )

            cleared = reloaded_manager.clear_session(
                session_id,
                confirmation=f"CLEAR {session_id}",
                expected_revision=3,
            )
            assertions["clear_status"] = (
                cleared["status"] == "cleared"
            )
            assertions["clear_revision_four"] = (
                cleared["session"]["revision"] == 4
            )
            assertions["clear_message_count_zero"] = (
                cleared["session"]["message_count"] == 0
            )
            assertions["clear_history_empty"] = (
                reloaded_manager.load_session(session_id)[
                    "messages"
                ]
                == []
            )
            assertions["temporary_json_one"] = (
                len(list(storage.glob("chat_*.json"))) == 1
            )
            assertions["temporary_files_zero"] = (
                list(storage.glob("*.tmp")) == []
                and list(storage.glob(".*.tmp")) == []
            )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise InteractiveControlCenterChatError(
                "Interactive chat runtime self-test failed: "
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
            "interactive_chat_ready": True,
            "web_surface_assertion_count": (
                web_test["assertion_count"]
            ),
            "save_only_flow_verified": True,
            "model_flow_verified": True,
            "model_confirmation_verified": True,
            "idempotent_retry_verified": True,
            "no_duplicate_model_invocation_verified": True,
            "revision_conflict_verified": True,
            "provider_failure_no_write_verified": True,
            "restart_persistence_verified": True,
            "clear_confirmation_verified": True,
            "response_kind_visibility_verified": True,
            "provider_network_calls": 0,
            "model_download_runtime": False,
            "internet_fallback_runtime": False,
            "streaming_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "aura_memory_write_runtime": False,
        }


__all__ = [
    "AuraInteractiveControlCenterChatRuntimeManager",
    "InteractiveControlCenterChatError",
]
