"""Bounded Sprint 272 voice auto-conversation context foundation.

This module prepares a server-grounded context packet for a future explicit
Auto Conversation turn. It does not send a chat message, invoke a model,
synthesize speech, dispatch an action, or mutate a session.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Callable, Mapping

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)


class VoiceAutoConversationRuntimeError(RuntimeError):
    """Base error for the Sprint 272 context foundation."""


class VoiceAutoConversationValidationError(
    VoiceAutoConversationRuntimeError
):
    """Raised when an explicit prepare request is invalid."""


@dataclass(frozen=True)
class VoiceAutoConversationIdentity:
    name: str
    version: str
    codename: str
    creator: str
    motto: str

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "codename": self.codename,
            "creator": self.creator,
            "motto": self.motto,
        }


class AuraVoiceAutoConversationRuntimeManager:
    """Prepare an honest, bounded context packet without executing a turn."""

    COMPONENT_VERSION = "0.1.0-alpha"
    SPRINT = 272
    SESSION_ID_RE = re.compile(r"^chat_[0-9a-f]{32}$")
    REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
    MAX_TRANSCRIPT_CHARACTERS = 8192
    MAX_RUNTIME_CAPABILITIES = 16

    def __init__(
        self,
        *,
        project_root: Path,
        capability_registry_manager: (
            CapabilityRegistryManager | None
        ) = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.identity_path = (
            self.project_root
            / "aura"
            / "personality"
            / "identity.yaml"
        )
        self.capability_registry_manager = (
            capability_registry_manager
            or CapabilityRegistryManager()
        )

    @staticmethod
    def _scalar(
        text: str,
        key: str,
        fallback: str,
    ) -> str:
        match = re.search(
            rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$",
            text,
        )
        if not match:
            return fallback
        value = match.group(1).strip().strip("\"'")
        return value or fallback

    def identity(self) -> VoiceAutoConversationIdentity:
        if not self.identity_path.is_file():
            raise VoiceAutoConversationRuntimeError(
                "AURA identity file is unavailable."
            )
        text = self.identity_path.read_text(
            encoding="utf-8",
            errors="strict",
        )
        return VoiceAutoConversationIdentity(
            name=self._scalar(text, "name", "AURA"),
            version=self._scalar(text, "version", "unknown"),
            codename=self._scalar(text, "codename", "unknown"),
            creator=self._scalar(text, "creator", "Kiput"),
            motto=self._scalar(
                text,
                "motto",
                "Grow Together",
            ),
        )

    def _runtime_capability_ids(self) -> list[str]:
        catalog = self.capability_registry_manager.capability_catalog()
        selected: list[str] = []
        for capability in catalog:
            if capability.get("state") != "online":
                continue
            runtime_level = str(
                capability.get("runtime_level") or ""
            )
            if runtime_level in {
                "foundation_only",
                "planner_only",
                "review_only",
                "planned_future",
                "disabled_runtime",
            }:
                continue
            capability_id = str(capability.get("id") or "").strip()
            if capability_id:
                selected.append(capability_id)
            if len(selected) >= self.MAX_RUNTIME_CAPABILITIES:
                break
        return selected

    @staticmethod
    def _validate_voice_status(
        voice_status: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        payload = dict(voice_status or {})
        if payload.get("ready") is not True:
            raise VoiceAutoConversationValidationError(
                "Voice runtime is not ready."
            )
        required_false = (
            "always_listening",
            "wake_word",
            "cloud_fallback",
            "direct_voice_to_action",
            "raw_audio_retention",
        )
        for field in required_false:
            if payload.get(field) is not False:
                raise VoiceAutoConversationValidationError(
                    f"Unsafe voice boundary: {field} must remain false."
                )
        return payload

    @classmethod
    def _validate_session_id(cls, session_id: Any) -> str:
        value = str(session_id or "").strip()
        if not cls.SESSION_ID_RE.fullmatch(value):
            raise VoiceAutoConversationValidationError(
                "A valid active chat session ID is required."
            )
        return value

    @classmethod
    def _validate_request_id(cls, request_id: Any) -> str:
        value = str(request_id or "").strip()
        if not cls.REQUEST_ID_RE.fullmatch(value):
            raise VoiceAutoConversationValidationError(
                "A bounded request ID is required."
            )
        return value

    @classmethod
    def _validate_transcript(cls, transcript: Any) -> str:
        if not isinstance(transcript, str):
            raise VoiceAutoConversationValidationError(
                "Transcript must be text."
            )
        value = transcript.strip()
        if not value:
            raise VoiceAutoConversationValidationError(
                "Transcript cannot be empty."
            )
        if len(value) > cls.MAX_TRANSCRIPT_CHARACTERS:
            raise VoiceAutoConversationValidationError(
                "Transcript exceeds the bounded character limit."
            )
        return value

    def status(self) -> dict[str, Any]:
        identity = self.identity()
        summary = self.capability_registry_manager.capability_summary()
        return {
            "name": "aura_voice_auto_conversation_runtime",
            "component_version": self.COMPONENT_VERSION,
            "sprint": self.SPRINT,
            "status": "ready",
            "ready": True,
            "default_mode": "manual_review",
            "auto_conversation_enabled_by_default": False,
            "explicit_enable_required": True,
            "audio_unlock_required": True,
            "active_session_required": True,
            "server_session_validation_required": True,
            "single_turn_per_ptt_release": True,
            "visible_response_before_tts": True,
            "client_stale_turn_suppression_required": True,
            "model_invocation_enabled": True,
            "automatic_chat_send_enabled": True,
            "tts_autoplay_enabled": True,
            "direct_voice_to_action": False,
            "automatic_sensitive_approval": False,
            "always_listening": False,
            "wake_word": False,
            "cloud_fallback": False,
            "raw_audio_retention": False,
            "new_listener": False,
            "public_binding": False,
            "runtime_mutated": False,
            "identity": identity.as_dict(),
            "capability_summary": {
                "total_capabilities": summary[
                    "total_capabilities"
                ],
                "online_capabilities": summary[
                    "online_capabilities"
                ],
                "permission_gated_count": summary[
                    "permission_gated_count"
                ],
                "runtime_execution_features": summary[
                    "runtime_execution_features"
                ],
            },
        }

    def prepare_turn(
        self,
        *,
        session_id: Any,
        transcript: Any,
        confirm_auto_conversation: Any,
        request_id: Any,
        voice_status: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if confirm_auto_conversation is not True:
            raise VoiceAutoConversationValidationError(
                "Explicit Auto Conversation confirmation is required."
            )
        valid_session_id = self._validate_session_id(session_id)
        valid_transcript = self._validate_transcript(transcript)
        valid_request_id = self._validate_request_id(request_id)
        safe_voice_status = self._validate_voice_status(voice_status)

        identity = self.identity()
        summary = self.capability_registry_manager.capability_summary()
        runtime_capabilities = self._runtime_capability_ids()

        context_packet = {
            "schema": "aura_voice_companion_context_v1",
            "identity": identity.as_dict(),
            "speaking_style": {
                "tone": "warm, direct, collaborative",
                "language_preference": "follow the user language",
                "avoid_generic_chatbot_framing": True,
            },
            "capability_summary": {
                "total_capabilities": summary[
                    "total_capabilities"
                ],
                "online_capabilities": summary[
                    "online_capabilities"
                ],
                "permission_gated_count": summary[
                    "permission_gated_count"
                ],
                "runtime_execution_features": summary[
                    "runtime_execution_features"
                ],
                "selected_online_runtime_capabilities": (
                    runtime_capabilities
                ),
            },
            "voice_runtime": {
                "status": safe_voice_status.get("status"),
                "inference_host": safe_voice_status.get(
                    "inference_host"
                ),
                "capture_host": safe_voice_status.get(
                    "audio_capture_host"
                ),
                "playback_host": safe_voice_status.get(
                    "audio_playback_host"
                ),
                "stt_backend": safe_voice_status.get(
                    "stt_backend"
                ),
                "tts_backend": safe_voice_status.get(
                    "tts_backend"
                ),
            },
            "active_session": {
                "session_id": valid_session_id,
                "server_validation_required_before_send": True,
                "history_included": False,
                "history_reason": (
                    "Deferred to the server-owned active-session "
                    "integration patch."
                ),
            },
            "reviewed_memory": {
                "included": False,
                "reason": (
                    "Only server-verified reviewed memory may be "
                    "added by the integration patch."
                ),
            },
            "project_context": {
                "included": False,
                "reason": (
                    "Only an already available bounded workspace "
                    "context may be added by the integration patch."
                ),
            },
            "honesty_boundary": {
                "invent_capabilities": False,
                "claim_unknown_runtime_state": False,
                "state_uncertainty_explicitly": True,
                "sensitive_actions_require_preview_and_approval": True,
            },
        }

        model_context_text = (
            f"You are {identity.name} v{identity.version}, "
            f"codename {identity.codename}, created by "
            f"{identity.creator}. Speak warmly, directly, and as a "
            "collaborative local partner rather than a generic chatbot. "
            f"Current capability registry: "
            f"{summary['online_capabilities']} online of "
            f"{summary['total_capabilities']} total, "
            f"{summary['permission_gated_count']} permission-gated, "
            f"{summary['runtime_execution_features']} runtime execution "
            "features. Never invent a capability or runtime state. "
            "State uncertainty explicitly. Sensitive actions always "
            "require a visible preview and explicit approval."
        )

        return {
            "status": "prepared",
            "ready_for_integration": True,
            "sprint": self.SPRINT,
            "request_id": valid_request_id,
            "session_id": valid_session_id,
            "transcript": valid_transcript,
            "context_packet": context_packet,
            "model_context_text": model_context_text,
            "next_step": (
                "server_validate_session_then_submit_one_model_turn"
            ),
            "automatic_chat_send_performed": False,
            "model_invoked": False,
            "tts_requested": False,
            "autoplay_attempted": False,
            "action_dispatched": False,
            "permission_granted": False,
            "runtime_mutated": False,
        }


    @staticmethod
    def assistant_text_from_result(
        result: Mapping[str, Any],
    ) -> str:
        # Extract the persisted assistant response without guessing facts.
        direct_keys = (
            "assistant_text",
            "response_text",
            "reply_text",
            "text",
        )
        for key in direct_keys:
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        object_keys = (
            "assistant_message",
            "model_message",
            "delivered_response",
            "response",
            "reply",
        )
        for key in object_keys:
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, Mapping):
                for text_key in ("content", "text", "reply", "response"):
                    text = value.get(text_key)
                    if isinstance(text, str) and text.strip():
                        return text.strip()

        session_candidates = (
            result,
            result.get("session"),
            result.get("updated_session"),
            result.get("chat_session"),
        )
        for session in session_candidates:
            if not isinstance(session, Mapping):
                continue
            messages = session.get("messages")
            if not isinstance(messages, list):
                continue
            for message in reversed(messages):
                if not isinstance(message, Mapping):
                    continue
                if message.get("role") not in {"assistant", "model"}:
                    continue
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()

        raise VoiceAutoConversationRuntimeError(
            "The local model turn did not expose a persisted "
            "assistant response."
        )

    def execute_turn(
        self,
        *,
        session_id: Any,
        transcript: Any,
        expected_revision: Any,
        client_message_id: Any,
        request_id: Any,
        confirm_auto_conversation: Any,
        confirm_model_request: Any,
        voice_status: Mapping[str, Any] | None,
        submit_model_message: Callable[..., Mapping[str, Any]],
    ) -> dict[str, Any]:
        # Execute exactly one server-owned model turn.
        prepared = self.prepare_turn(
            session_id=session_id,
            transcript=transcript,
            confirm_auto_conversation=confirm_auto_conversation,
            request_id=request_id,
            voice_status=voice_status,
        )
        if confirm_model_request is not True:
            raise VoiceAutoConversationValidationError(
                "Explicit local-model confirmation is required."
            )
        if not isinstance(expected_revision, int) or expected_revision < 0:
            raise VoiceAutoConversationValidationError(
                "A non-negative expected session revision is required."
            )
        valid_client_message_id = self._validate_request_id(
            client_message_id
        )

        model_result = dict(
            submit_model_message(
                prepared["session_id"],
                content=prepared["transcript"],
                client_message_id=valid_client_message_id,
                expected_revision=expected_revision,
                request_id=prepared["request_id"],
                confirm_model_request=True,
                system_prompt=prepared["model_context_text"],
            )
        )
        assistant_text = self.assistant_text_from_result(model_result)

        return {
            "status": "completed",
            "sprint": self.SPRINT,
            "request_id": prepared["request_id"],
            "session_id": prepared["session_id"],
            "assistant_text": assistant_text,
            "context_packet": prepared["context_packet"],
            "model_result": model_result,
            "automatic_chat_send_performed": True,
            "model_invoked": True,
            "visible_response_required_before_tts": True,
            "tts_client_handoff_ready": True,
            "tts_requested": False,
            "autoplay_attempted": False,
            "action_dispatched": False,
            "permission_granted": False,
            "runtime_mutated": True,
        }


def run_voice_auto_conversation_foundation_self_test(
    *,
    project_root: Path,
    voice_status: Mapping[str, Any],
) -> dict[str, Any]:
    manager = AuraVoiceAutoConversationRuntimeManager(
        project_root=project_root
    )
    status = manager.status()
    prepared = manager.prepare_turn(
        session_id="chat_" + ("a" * 32),
        transcript="Halo AURA, jelaskan status kemampuanmu.",
        confirm_auto_conversation=True,
        request_id="sprint-272-foundation-self-test",
        voice_status=voice_status,
    )

    assertions = {
        "status_ready": status["ready"] is True,
        "manual_review_default": (
            status["default_mode"] == "manual_review"
        ),
        "auto_disabled_default": (
            status["auto_conversation_enabled_by_default"]
            is False
        ),
        "explicit_enable_required": (
            status["explicit_enable_required"] is True
        ),
        "model_enabled_integration": (
            status["model_invocation_enabled"] is True
        ),
        "automatic_send_enabled_integration": (
            status["automatic_chat_send_enabled"] is True
        ),
        "autoplay_enabled_integration": (
            status["tts_autoplay_enabled"] is True
        ),
        "always_listening_false": (
            status["always_listening"] is False
        ),
        "wake_word_false": status["wake_word"] is False,
        "cloud_fallback_false": (
            status["cloud_fallback"] is False
        ),
        "direct_action_false": (
            status["direct_voice_to_action"] is False
        ),
        "raw_retention_false": (
            status["raw_audio_retention"] is False
        ),
        "prepared": prepared["status"] == "prepared",
        "identity_grounded": (
            prepared["context_packet"]["identity"]["name"]
            == "AURA"
        ),
        "capability_grounded": (
            prepared["context_packet"]["capability_summary"][
                "total_capabilities"
            ]
            > 0
        ),
        "honesty_grounded": (
            prepared["context_packet"]["honesty_boundary"][
                "invent_capabilities"
            ]
            is False
        ),
        "no_send": (
            prepared["automatic_chat_send_performed"] is False
        ),
        "no_model": prepared["model_invoked"] is False,
        "no_tts": prepared["tts_requested"] is False,
        "no_action": prepared["action_dispatched"] is False,
        "no_mutation": prepared["runtime_mutated"] is False,
    }
    failed = sorted(
        name for name, passed in assertions.items() if not passed
    )
    return {
        "status": "OK" if not failed else "FAILED",
        "assertion_count": len(assertions),
        "failed_assertion_count": len(failed),
        "failed_assertions": failed,
        "assertions": assertions,
        "runtime_status": status,
        "prepared_turn": prepared,
    }
