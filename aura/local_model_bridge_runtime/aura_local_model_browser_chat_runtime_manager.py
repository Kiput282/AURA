"""Safe browser-chat integration for the Sprint 187 local model bridge."""

from __future__ import annotations

from typing import Any, Mapping


class AuraLocalModelBrowserChatRuntimeManager:
    """Connect bounded local chat sessions to one local text-only model."""

    name = "aura_local_model_browser_chat_runtime"
    component_version = "0.1.0-alpha"
    sprint = 187
    schema_version = "1.0"

    SYSTEM_PROMPT = (
        "You are AURA, a local AI assistant. Reply with helpful text only. "
        "Do not claim tools, commands, actions, file operations, memory writes, "
        "internet access, desktop control, or external effects. Those "
        "capabilities are not connected to this local model bridge."
    )

    def __init__(
        self,
        session_manager: Any,
        bridge_manager: Any,
        *,
        configuration_error: str | None = None,
    ) -> None:
        self.session_manager = session_manager
        self.bridge_manager = bridge_manager
        self.configuration_error = configuration_error

    def _require_configuration(self) -> None:
        if self.configuration_error is None:
            return

        from .aura_local_model_bridge_runtime_manager import (
            LocalModelBridgeConfigurationError,
        )

        raise LocalModelBridgeConfigurationError(
            self.configuration_error
        )

    def status(self) -> dict[str, Any]:
        bridge = self.bridge_manager.status()
        configured = bool(bridge["configured"])
        enabled = bool(bridge["enabled"])
        degraded = self.configuration_error is not None
        active = configured and enabled and not degraded

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": (
                "degraded"
                if degraded
                else "active"
                if active
                else "disabled"
            ),
            "degraded": degraded,
            "configuration_error": self.configuration_error,
            "browser_chat_connected": True,
            "configured": configured,
            "enabled": enabled,
            "active": active,
            "provider": bridge["provider"],
            "base_url": bridge["base_url"],
            "model": bridge["model"],
            "model_output_text_only": True,
            "explicit_model_confirmation_required": True,
            "explicit_probe_confirmation_required": True,
            "placeholder_route_available": True,
            "model_message_route_available": True,
            "model_download_runtime": False,
            "internet_fallback_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "aura_memory_write_runtime": False,
        }

    def probe(
        self,
        *,
        confirm_local_connection: bool,
    ) -> dict[str, Any]:
        self._require_configuration()
        result = self.bridge_manager.probe(
            confirm_local_connection=confirm_local_connection
        )
        return {
            **result,
            "browser_chat_connected": True,
        }

    def submit_model_message(
        self,
        session_id: str,
        *,
        content: str,
        client_message_id: str,
        expected_revision: int,
        request_id: str,
        confirm_model_request: bool,
    ) -> dict[str, Any]:
        self._require_configuration()

        def response_factory(
            messages: list[dict[str, str]],
        ) -> Mapping[str, Any]:
            return self.bridge_manager.generate(
                messages=messages,
                request_id=request_id,
                confirm_model_request=confirm_model_request,
            )

        result = self.session_manager.submit_local_model_message(
            session_id,
            content=content,
            client_message_id=client_message_id,
            expected_revision=expected_revision,
            system_prompt=self.SYSTEM_PROMPT,
            response_factory=response_factory,
        )
        return {
            **result,
            "browser_chat_model_bridge": True,
        }
