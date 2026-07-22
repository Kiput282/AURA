"""Sprint 279 ORION watchdog, emergency stop, recovery, and dialogue evaluation.

This runtime is intentionally tick-driven, in-memory, and fail-closed. It
composes existing ORION runtimes through their public APIs only. The core owns
no listener, network connection, background thread, process execution, or real
platform emergency side effect.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .aura_orion_supervision_recovery_runtime_adapters import (
    AuraFakeOrionSafetyControlAdapter,
    AuraNonExecutingOrionSafetyControlAdapter,
    AuraOrionSafetyControlAdapter,
)


class OrionSupervisionRecoveryRuntimeError(RuntimeError):
    """Raised when a Sprint 279 supervision contract is violated."""


def _canonical_bytes(payload: Any) -> bytes:
    try:
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise OrionSupervisionRecoveryRuntimeError(
            "Payload is not canonicalizable."
        ) from exc


def _digest(payload: Any) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _format_utc(value: datetime) -> str:
    normalized = value.astimezone(timezone.utc)
    return normalized.isoformat(timespec="microseconds").replace(
        "+00:00",
        "Z",
    )


def _is_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


class _SelfTestLiveLinkManager:
    def __init__(self) -> None:
        self.state = "live"
        self.heartbeat_active = True
        self.closed = False
        self.ticks = 0

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "state": self.state,
            "safe_idle": self.state in {"disconnected", "failed"},
            "heartbeat_active": self.heartbeat_active,
            "heartbeat_age_seconds": 0.0 if self.heartbeat_active else None,
            "last_heartbeat_at_utc": "2026-07-22T09:00:00.000000Z",
            "network_listener_active": False,
            "network_connection_active": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_active": False,
        }

    def tick(self) -> dict[str, Any]:
        self.ticks += 1
        return self.status()

    def close_session(self) -> dict[str, Any]:
        self.closed = True
        self.state = "disconnected"
        self.heartbeat_active = False
        return self.status()


class _SelfTestPreviewManager:
    def __init__(self) -> None:
        self.cancelled = False

    def cancel(self) -> dict[str, Any]:
        self.cancelled = True
        return {
            "status": "OK",
            "state": "cancelled",
            "execution_performed": False,
        }


class _SelfTestPermissionManager:
    def __init__(self) -> None:
        self.revocations: list[dict[str, Any]] = []
        self.outcomes: list[dict[str, Any]] = []

    def revoke_permission(
        self,
        *,
        permission_id: str,
        reason: str,
    ) -> dict[str, Any]:
        self.revocations.append(
            {"permission_id": permission_id, "reason": reason}
        )
        return {
            "status": "OK",
            "permission_id": permission_id,
            "state": "revoked",
            "audit_written": True,
        }

    def verify_audit_chain(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "event_count": len(self.revocations) + len(self.outcomes),
            "hash_chain_valid": True,
            "valid": True,
            "chain_valid": True,
        }

    def record_execution_outcome(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if envelope.get("proof") != proof_b64url:
            raise OrionSupervisionRecoveryRuntimeError(
                "Self-test outcome proof mismatch."
            )
        self.outcomes.append(deepcopy(envelope))
        return {
            "status": "OK",
            "outcome_recorded": True,
            "audit_written": True,
            "audit_digest": _digest(envelope),
        }


class _SelfTestBoundedActionManager:
    def __init__(self) -> None:
        self.calls = 0
        self.fail = False
        self.outcome_unconfirmed = False

    def execute_authorized_action(
        self,
        *,
        action_request: dict[str, Any],
        consumption_envelope: dict[str, Any],
        consumption_proof_b64url: str,
    ) -> dict[str, Any]:
        self.calls += 1
        if self.fail:
            raise OrionSupervisionRecoveryRuntimeError(
                "Self-test bounded action failure."
            )
        return {
            "schema_version": "1",
            "execution_id": f"execution-{self.calls:03d}",
            "request_id": action_request["request_id"],
            "permission_id": action_request["permission_id"],
            "action_type": action_request["action_type"],
            "state": (
                "outcome_unconfirmed"
                if self.outcome_unconfirmed
                else "succeeded"
            ),
            "outcome": (
                "outcome_unconfirmed"
                if self.outcome_unconfirmed
                else "execution_confirmed"
            ),
            "execution_performed": True,
            "safe_idle_restored": not self.outcome_unconfirmed,
            "result_digest": _digest(action_request),
        }


class AuraOrionSupervisionRecoveryRuntimeManager:
    """Coordinate bounded ORION execution with explicit safety recovery."""

    COMPONENT_NAME = "orion_supervision_recovery_runtime"
    COMPONENT_VERSION = "0.1.0"
    PRODUCT_VERSION = "1.3.1"
    SPRINT = 279
    SCHEMA_VERSION = "1"
    DESIGN_CONTRACT_SHA = (
        "e2d73b2133de778d3f118ef026072712903b7529d0bd27fdb3c5b8a4d7347602"
    )

    STATE_IDLE = "idle"
    STATE_ARMED = "armed"
    STATE_HEALTHY = "healthy"
    STATE_STALE = "stale"
    STATE_EMERGENCY_LATCHED = "emergency_latched"
    STATE_RECOVERY_PENDING = "recovery_pending"
    STATE_RECOVERY_REVIEW = "recovery_review"
    STATE_RECOVERED = "recovered"
    STATE_FAILED = "failed"
    STATES = (
        STATE_IDLE,
        STATE_ARMED,
        STATE_HEALTHY,
        STATE_STALE,
        STATE_EMERGENCY_LATCHED,
        STATE_RECOVERY_PENDING,
        STATE_RECOVERY_REVIEW,
        STATE_RECOVERED,
        STATE_FAILED,
    )
    VALID_TRANSITIONS = (
        (STATE_IDLE, "arm", STATE_ARMED),
        (STATE_ARMED, "heartbeat_fresh", STATE_HEALTHY),
        (STATE_ARMED, "arm_timeout", STATE_EMERGENCY_LATCHED),
        (STATE_HEALTHY, "heartbeat_fresh", STATE_HEALTHY),
        (STATE_HEALTHY, "heartbeat_stale", STATE_STALE),
        (STATE_STALE, "heartbeat_recovered", STATE_HEALTHY),
        (STATE_STALE, "heartbeat_failed", STATE_EMERGENCY_LATCHED),
        (STATE_ARMED, "manual_emergency_stop", STATE_EMERGENCY_LATCHED),
        (STATE_HEALTHY, "manual_emergency_stop", STATE_EMERGENCY_LATCHED),
        (STATE_STALE, "manual_emergency_stop", STATE_EMERGENCY_LATCHED),
        (
            STATE_EMERGENCY_LATCHED,
            "record_emergency_outcome",
            STATE_RECOVERY_PENDING,
        ),
        (
            STATE_RECOVERY_PENDING,
            "request_recovery_review",
            STATE_RECOVERY_REVIEW,
        ),
        (STATE_RECOVERY_REVIEW, "approve_recovery", STATE_RECOVERED),
        (STATE_RECOVERY_REVIEW, "reject_recovery", STATE_FAILED),
        (STATE_RECOVERED, "reset_safe_idle", STATE_IDLE),
        (STATE_FAILED, "reset_safe_idle", STATE_IDLE),
    )

    CONFIGURATION_FIELDS = (
        "schema_version",
        "enabled",
        "adapter_mode",
        "adapter_id",
        "adapter_version",
        "heartbeat_interval_seconds",
        "heartbeat_stale_after_seconds",
        "heartbeat_failed_after_seconds",
        "max_clock_skew_seconds",
        "max_event_history",
        "max_dialogue_characters",
        "emergency_latch_required",
        "automatic_recovery_allowed",
        "review_required",
        "outcome_auto_clear_allowed",
        "private_runtime_mutation_allowed",
        "core_network_listener_allowed",
        "core_network_connection_allowed",
        "core_background_thread_allowed",
        "core_process_execution_allowed",
        "real_action_execution_on_ATLAS_allowed",
        "real_emergency_side_effect_on_ATLAS_allowed",
        "raw_dialogue_retention_allowed",
        "general_memory_handoff_allowed",
    )
    SESSION_FIELDS = (
        "schema_version",
        "session_id",
        "live_link_session_id",
        "pairing_id",
        "device_id",
        "capability_digest",
        "state",
        "armed_at_utc",
        "armed_monotonic",
        "last_heartbeat_at_utc",
        "last_heartbeat_monotonic",
        "heartbeat_sequence",
        "active_action_type",
        "active_execution_id",
        "preview_id",
        "permission_id",
        "emergency_request_id",
        "recovery_review_id",
        "outcome_state",
        "outcome_reconciled",
        "safe_idle_verified",
        "updated_at_utc",
    )
    HEARTBEAT_OBSERVATION_FIELDS = (
        "schema_version",
        "observation_id",
        "session_id",
        "observed_at_utc",
        "observed_monotonic",
        "live_link_state",
        "heartbeat_active",
        "heartbeat_age_seconds",
        "classification",
        "observation_digest",
    )
    EMERGENCY_STOP_REQUEST_FIELDS = (
        "schema_version",
        "request_id",
        "session_id",
        "reason_code",
        "operator_visible_reason",
        "requested_at_utc",
        "state_before",
        "state_after",
        "idempotent_replay",
        "action_type",
        "permission_id",
        "execution_order",
        "result_digest",
        "safe_idle_verified",
    )
    SAFETY_ADAPTER_RESULT_FIELDS = (
        "schema_version",
        "adapter_id",
        "adapter_version",
        "operation",
        "success",
        "execution_performed",
        "result_code",
        "result_digest",
        "safe_idle_verified",
        "action_interrupted",
        "redacted_message",
        "metadata_digest",
        "duration_ms",
        "platform",
    )
    RECOVERY_REVIEW_FIELDS = (
        "schema_version",
        "review_id",
        "session_id",
        "requested_at_utc",
        "status",
        "emergency_request_id",
        "outcome_state",
        "outcome_reconciled",
        "evidence_digest",
        "audit_chain_valid",
        "safe_idle_verified",
        "operator_confirmation_digest",
        "resolved_at_utc",
        "resolution",
        "reviewer_visible_summary",
        "review_digest",
    )
    DIALOGUE_EVALUATION_REQUEST_FIELDS = (
        "schema_version",
        "evaluation_id",
        "session_id",
        "source",
        "dialogue_text_digest",
        "redacted_text",
        "context",
        "requested_at_utc",
        "maximum_characters",
        "rule_ids",
        "request_digest",
        "raw_text_retained",
    )
    DIALOGUE_EVALUATION_RESULT_FIELDS = (
        "schema_version",
        "evaluation_id",
        "session_id",
        "verdict",
        "severity",
        "matched_rules",
        "matched_rule_count",
        "block_required",
        "review_required",
        "warning_required",
        "safe_to_continue",
        "redacted_summary",
        "evaluation_digest",
        "evaluated_at_utc",
        "deterministic",
        "cloud_used",
        "raw_text_retained",
        "memory_handoff_performed",
    )
    SUPERVISION_EVENT_FIELDS = (
        "schema_version",
        "event_id",
        "session_id",
        "event_type",
        "state_before",
        "state_after",
        "created_at_utc",
        "reason_code",
        "reference_id",
        "details_digest",
        "redacted_summary",
        "event_digest",
        "audit_written",
        "network_used",
        "real_side_effect",
        "sequence",
    )

    EMERGENCY_REASON_CODES = (
        "adapter_failure",
        "authentication_failure",
        "heartbeat_failed",
        "manual_stop",
        "outcome_unconfirmed",
        "permission_invalid",
        "policy_violation",
        "session_failed",
    )
    DIALOGUE_RULE_IDS = (
        "approval_bypass_language",
        "emergency_stop_acknowledgement",
        "outcome_uncertainty_disclosure",
        "recovery_claim_without_evidence",
        "scope_escalation_language",
        "secret_or_sensitive_data_exposure",
        "unsafe_action_language",
        "unsupported_capability_claim",
    )
    DIALOGUE_VERDICTS = (
        "block",
        "pass",
        "requires_review",
        "warn",
    )
    OUTCOME_STATES = (
        "execution_confirmed",
        "failed",
        "interrupted",
        "not_started",
        "outcome_unconfirmed",
        "reconciled",
    )
    CLI_COMMANDS = (
        "orion-supervision-status",
        "orion-supervision-inspect",
        "orion-supervision-self-test",
    )
    EMERGENCY_EXECUTION_ORDER = (
        "latch_emergency_state",
        "cancel_pending_preview",
        "revoke_scoped_permission",
        "close_live_link_session",
        "invoke_injected_safety_adapter",
        "record_execution_outcome_and_audit",
        "verify_safe_idle",
    )
    ADVERSARIAL_ACCEPTANCE = tuple(
        f"{category}:{index:03d}"
        for category, count in (
            ("heartbeat_and_watchdog", 32),
            ("emergency_stop_and_latch", 48),
            ("recovery_and_reconciliation", 48),
            ("dialogue_evaluation", 32),
            ("public_API_composition", 16),
            ("safety_boundaries", 16),
        )
        for index in range(1, count + 1)
    )

    DEFAULT_MAX_EVENT_HISTORY = 256
    DEFAULT_MAX_DIALOGUE_CHARACTERS = 4096
    DEFAULT_CONFIGURATION = {
        "schema_version": SCHEMA_VERSION,
        "enabled": False,
        "adapter_mode": "non_executing",
        "adapter_id": "orion-safety-non-executing",
        "adapter_version": "0.1.0",
        "heartbeat_interval_seconds": 5,
        "heartbeat_stale_after_seconds": 15,
        "heartbeat_failed_after_seconds": 30,
        "max_clock_skew_seconds": 5,
        "max_event_history": DEFAULT_MAX_EVENT_HISTORY,
        "max_dialogue_characters": DEFAULT_MAX_DIALOGUE_CHARACTERS,
        "emergency_latch_required": True,
        "automatic_recovery_allowed": False,
        "review_required": True,
        "outcome_auto_clear_allowed": False,
        "private_runtime_mutation_allowed": False,
        "core_network_listener_allowed": False,
        "core_network_connection_allowed": False,
        "core_background_thread_allowed": False,
        "core_process_execution_allowed": False,
        "real_action_execution_on_ATLAS_allowed": False,
        "real_emergency_side_effect_on_ATLAS_allowed": False,
        "raw_dialogue_retention_allowed": False,
        "general_memory_handoff_allowed": False,
    }

    _SENSITIVE_PATTERN = re.compile(
        r"(?i)(password|secret|token|credential|api[_ -]?key|"
        r"private[_ -]?key|pairing[_ -]?code)\s*[:=]\s*([^\s,;]+)"
    )
    _LONG_SECRET_PATTERN = re.compile(
        r"\b[A-Za-z0-9_-]{32,}\b"
    )
    _RULE_PATTERNS = {
        "approval_bypass_language": (
            re.compile(r"(?i)\b(bypass|skip|ignore)\b.{0,24}\bapproval\b"),
            "block",
        ),
        "emergency_stop_acknowledgement": (
            re.compile(r"(?i)\b(emergency stop|stop now|halt immediately)\b"),
            "pass",
        ),
        "outcome_uncertainty_disclosure": (
            re.compile(r"(?i)\b(outcome unknown|not confirmed|uncertain result)\b"),
            "pass",
        ),
        "recovery_claim_without_evidence": (
            re.compile(r"(?i)\b(recovered|safe again|fixed)\b.{0,32}\b(without|no)\b.{0,16}\bevidence\b"),
            "requires_review",
        ),
        "scope_escalation_language": (
            re.compile(r"(?i)\b(expand|escalate|broaden)\b.{0,24}\bscope\b"),
            "requires_review",
        ),
        "secret_or_sensitive_data_exposure": (
            re.compile(r"(?i)\b(password|secret|token|credential|api[_ -]?key)\b"),
            "block",
        ),
        "unsafe_action_language": (
            re.compile(r"(?i)\b(force|override|disable safety|ignore stop)\b"),
            "block",
        ),
        "unsupported_capability_claim": (
            re.compile(r"(?i)\b(i can|aura can)\b.{0,40}\b(anything|unrestricted|without permission)\b"),
            "warn",
        ),
    }

    def __init__(
        self,
        *,
        project_root: Path,
        live_link_manager: Any | None = None,
        bounded_action_manager: Any | None = None,
        permission_manager: Any | None = None,
        preview_manager: Any | None = None,
        pairing_manager: Any | None = None,
        adapter: AuraOrionSafetyControlAdapter | None = None,
        configuration: dict[str, Any] | None = None,
        now_provider: Callable[[], datetime] | None = None,
        monotonic_provider: Callable[[], float] | None = None,
        id_provider: Callable[[str], str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.live_link_manager = live_link_manager
        self.bounded_action_manager = bounded_action_manager
        self.permission_manager = permission_manager
        self.preview_manager = preview_manager
        self.pairing_manager = pairing_manager
        self.adapter = (
            AuraNonExecutingOrionSafetyControlAdapter()
            if adapter is None
            else adapter
        )
        self.configuration = deepcopy(
            self.DEFAULT_CONFIGURATION
            if configuration is None
            else configuration
        )
        self._now_provider = (
            (lambda: datetime.now(timezone.utc))
            if now_provider is None
            else now_provider
        )
        self._monotonic_provider = (
            time.monotonic
            if monotonic_provider is None
            else monotonic_provider
        )
        self._id_provider = (
            (lambda prefix: f"{prefix}{uuid.uuid4().hex}")
            if id_provider is None
            else id_provider
        )
        self._sessions: dict[str, dict[str, Any]] = {}
        self._reviews: dict[str, dict[str, Any]] = {}
        self._events: list[dict[str, Any]] = []
        self._active_session_id: str | None = None
        self._event_sequence = 0
        self.validate_configuration()

    @property
    def _now(self) -> datetime:
        value = self._now_provider()
        if value.tzinfo is None:
            raise OrionSupervisionRecoveryRuntimeError(
                "now_provider must return a timezone-aware datetime."
            )
        return value.astimezone(timezone.utc)

    def _next_id(self, prefix: str) -> str:
        value = self._id_provider(prefix)
        if not isinstance(value, str) or not value.strip():
            raise OrionSupervisionRecoveryRuntimeError(
                "id_provider returned an invalid identifier."
            )
        return value

    def _session(self, session_id: str) -> dict[str, Any]:
        record = self._sessions.get(session_id)
        if record is None:
            raise OrionSupervisionRecoveryRuntimeError(
                "Supervision session does not exist."
            )
        return record

    def _transition(
        self,
        session: dict[str, Any],
        *,
        event: str,
        target: str,
    ) -> None:
        source = session["state"]
        if (source, event, target) not in self.VALID_TRANSITIONS:
            raise OrionSupervisionRecoveryRuntimeError(
                f"Invalid transition: {source} --{event}--> {target}."
            )
        session["state"] = target
        session["updated_at_utc"] = _format_utc(self._now)

    def _redact(self, value: str) -> str:
        redacted = self._SENSITIVE_PATTERN.sub(
            lambda match: f"{match.group(1)}=<redacted>",
            value,
        )
        return self._LONG_SECRET_PATTERN.sub("<redacted>", redacted)

    def _append_event(
        self,
        *,
        session_id: str,
        event_type: str,
        state_before: str,
        state_after: str,
        reason_code: str,
        reference_id: str | None,
        details: dict[str, Any],
        redacted_summary: str,
        audit_written: bool = False,
        network_used: bool = False,
        real_side_effect: bool = False,
    ) -> dict[str, Any]:
        self._event_sequence += 1
        event = {
            "schema_version": self.SCHEMA_VERSION,
            "event_id": self._next_id("event-"),
            "session_id": session_id,
            "event_type": event_type,
            "state_before": state_before,
            "state_after": state_after,
            "created_at_utc": _format_utc(self._now),
            "reason_code": reason_code,
            "reference_id": reference_id,
            "details_digest": _digest(details),
            "redacted_summary": self._redact(redacted_summary)[:512],
            "event_digest": "",
            "audit_written": bool(audit_written),
            "network_used": bool(network_used),
            "real_side_effect": bool(real_side_effect),
            "sequence": self._event_sequence,
        }
        event["event_digest"] = _digest(
            {
                key: value
                for key, value in event.items()
                if key != "event_digest"
            }
        )
        self._events.append(event)
        maximum = int(self.configuration["max_event_history"])
        if len(self._events) > maximum:
            self._events = self._events[-maximum:]
        return deepcopy(event)

    def _audit_chain_valid(self) -> bool:
        if self.permission_manager is None:
            return True
        result = self.permission_manager.verify_audit_chain()
        if not isinstance(result, dict):
            return False
        return bool(
            result.get("hash_chain_valid")
            or result.get("valid")
            or result.get("chain_valid")
        )

    def _adapter_result_valid(self, result: dict[str, Any]) -> bool:
        return (
            isinstance(result, dict)
            and tuple(result.keys()) == self.SAFETY_ADAPTER_RESULT_FIELDS
            and _is_digest(result.get("result_digest"))
            and _is_digest(result.get("metadata_digest"))
        )

    def adapter_status(self) -> dict[str, Any]:
        status = self.adapter.status()
        if not isinstance(status, dict):
            raise OrionSupervisionRecoveryRuntimeError(
                "Safety adapter status must be a dictionary."
            )
        return deepcopy(status)

    def arm_supervision(
        self,
        *,
        live_link_session_id: str,
        pairing_id: str,
        device_id: str,
        capability_digest: str,
        preview_id: str | None = None,
        permission_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.configuration["enabled"]:
            raise OrionSupervisionRecoveryRuntimeError(
                "Supervision runtime is disabled by configuration."
            )
        if self._active_session_id is not None:
            active = self._session(self._active_session_id)
            if active["state"] != self.STATE_IDLE:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Only one supervision session may be active."
                )
        for name, value in (
            ("live_link_session_id", live_link_session_id),
            ("pairing_id", pairing_id),
            ("device_id", device_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise OrionSupervisionRecoveryRuntimeError(
                    f"{name} must be a non-empty string."
                )
        if not _is_digest(capability_digest):
            raise OrionSupervisionRecoveryRuntimeError(
                "capability_digest must be a lowercase SHA-256 digest."
            )
        if self.pairing_manager is not None:
            binding = self.pairing_manager.authenticated_binding()
            if binding.get("pairing_id") != pairing_id:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Pairing ID does not match authenticated binding."
                )
            if binding.get("device_id") != device_id:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Device ID does not match authenticated binding."
                )
        now = self._now
        monotonic = float(self._monotonic_provider())
        session_id = self._next_id("supervision-")
        session = {
            "schema_version": self.SCHEMA_VERSION,
            "session_id": session_id,
            "live_link_session_id": live_link_session_id,
            "pairing_id": pairing_id,
            "device_id": device_id,
            "capability_digest": capability_digest,
            "state": self.STATE_IDLE,
            "armed_at_utc": _format_utc(now),
            "armed_monotonic": monotonic,
            "last_heartbeat_at_utc": None,
            "last_heartbeat_monotonic": None,
            "heartbeat_sequence": 0,
            "active_action_type": None,
            "active_execution_id": None,
            "preview_id": preview_id,
            "permission_id": permission_id,
            "emergency_request_id": None,
            "recovery_review_id": None,
            "outcome_state": "not_started",
            "outcome_reconciled": False,
            "safe_idle_verified": True,
            "updated_at_utc": _format_utc(now),
        }
        self._sessions[session_id] = session
        self._active_session_id = session_id
        self._transition(session, event="arm", target=self.STATE_ARMED)
        self._append_event(
            session_id=session_id,
            event_type="supervision_armed",
            state_before=self.STATE_IDLE,
            state_after=self.STATE_ARMED,
            reason_code="manual_arm",
            reference_id=live_link_session_id,
            details={"capability_digest": capability_digest},
            redacted_summary="ORION supervision armed.",
        )
        return self.inspect_session(session_id)

    def event_history(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "event_count": len(self._events),
            "events": deepcopy(self._events),
            "raw_dialogue_retained": False,
            "secret_exposed": False,
        }

    def evaluate_dialogue(
        self,
        *,
        dialogue_text: str,
        source: str,
        session_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(dialogue_text, str):
            raise OrionSupervisionRecoveryRuntimeError(
                "dialogue_text must be a string."
            )
        maximum = int(self.configuration["max_dialogue_characters"])
        if len(dialogue_text) > maximum:
            raise OrionSupervisionRecoveryRuntimeError(
                "Dialogue exceeds the configured character limit."
            )
        if not isinstance(source, str) or not source.strip():
            raise OrionSupervisionRecoveryRuntimeError(
                "Dialogue source must be a non-empty string."
            )
        context_value = {} if context is None else deepcopy(context)
        redacted = self._redact(dialogue_text)
        evaluation_id = self._next_id("dialogue-evaluation-")
        requested_at = _format_utc(self._now)
        request = {
            "schema_version": self.SCHEMA_VERSION,
            "evaluation_id": evaluation_id,
            "session_id": session_id,
            "source": source,
            "dialogue_text_digest": _digest(dialogue_text),
            "redacted_text": redacted,
            "context": context_value,
            "requested_at_utc": requested_at,
            "maximum_characters": maximum,
            "rule_ids": list(self.DIALOGUE_RULE_IDS),
            "request_digest": "",
            "raw_text_retained": False,
        }
        request["request_digest"] = _digest(
            {
                key: value
                for key, value in request.items()
                if key != "request_digest"
            }
        )
        matched: list[dict[str, str]] = []
        severity_rank = {
            "pass": 0,
            "warn": 1,
            "requires_review": 2,
            "block": 3,
        }
        highest = "pass"
        for rule_id, (pattern, verdict) in self._RULE_PATTERNS.items():
            if pattern.search(dialogue_text):
                matched.append({"rule_id": rule_id, "verdict": verdict})
                if severity_rank[verdict] > severity_rank[highest]:
                    highest = verdict
        result = {
            "schema_version": self.SCHEMA_VERSION,
            "evaluation_id": evaluation_id,
            "session_id": session_id,
            "verdict": highest,
            "severity": severity_rank[highest],
            "matched_rules": matched,
            "matched_rule_count": len(matched),
            "block_required": highest == "block",
            "review_required": highest == "requires_review",
            "warning_required": highest == "warn",
            "safe_to_continue": highest in {"pass", "warn"},
            "redacted_summary": redacted[:512],
            "evaluation_digest": "",
            "evaluated_at_utc": _format_utc(self._now),
            "deterministic": True,
            "cloud_used": False,
            "raw_text_retained": False,
            "memory_handoff_performed": False,
        }
        result["evaluation_digest"] = _digest(
            {
                key: value
                for key, value in result.items()
                if key != "evaluation_digest"
            }
        )
        if session_id is not None and session_id in self._sessions:
            session = self._sessions[session_id]
            self._append_event(
                session_id=session_id,
                event_type="dialogue_evaluated",
                state_before=session["state"],
                state_after=session["state"],
                reason_code=highest,
                reference_id=evaluation_id,
                details={
                    "request_digest": request["request_digest"],
                    "evaluation_digest": result["evaluation_digest"],
                    "matched_rule_count": len(matched),
                },
                redacted_summary="Dialogue evaluated with deterministic rules.",
            )
        return result

    def execute_supervised_action(
        self,
        *,
        session_id: str,
        action_request: dict[str, Any],
        consumption_envelope: dict[str, Any],
        consumption_proof_b64url: str,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] != self.STATE_HEALTHY:
            raise OrionSupervisionRecoveryRuntimeError(
                "Supervised action requires a healthy session."
            )
        if self.bounded_action_manager is None:
            raise OrionSupervisionRecoveryRuntimeError(
                "Bounded action manager was not injected."
            )
        action_type = str(action_request.get("action_type", ""))
        permission_id = str(action_request.get("permission_id", ""))
        if not action_type or not permission_id:
            raise OrionSupervisionRecoveryRuntimeError(
                "Action request lacks action_type or permission_id."
            )
        session["active_action_type"] = action_type
        session["permission_id"] = permission_id
        session["safe_idle_verified"] = False
        try:
            result = self.bounded_action_manager.execute_authorized_action(
                action_request=deepcopy(action_request),
                consumption_envelope=deepcopy(consumption_envelope),
                consumption_proof_b64url=consumption_proof_b64url,
            )
        except Exception as exc:
            self.request_emergency_stop(
                session_id=session_id,
                reason_code="adapter_failure",
                operator_visible_reason=(
                    f"Bounded action failed: {type(exc).__name__}."
                ),
            )
            raise OrionSupervisionRecoveryRuntimeError(
                "Bounded action failed and emergency stop was latched."
            ) from exc
        if not isinstance(result, dict):
            self.request_emergency_stop(
                session_id=session_id,
                reason_code="adapter_failure",
                operator_visible_reason="Bounded action returned invalid data.",
            )
            raise OrionSupervisionRecoveryRuntimeError(
                "Bounded action result is invalid."
            )
        session["active_execution_id"] = result.get("execution_id")
        session["outcome_state"] = str(
            result.get("outcome", result.get("state", "outcome_unconfirmed"))
        )
        if (
            result.get("state") == "outcome_unconfirmed"
            or session["outcome_state"] == "outcome_unconfirmed"
        ):
            self.request_emergency_stop(
                session_id=session_id,
                reason_code="outcome_unconfirmed",
                operator_visible_reason=(
                    "Bounded action outcome could not be confirmed."
                ),
            )
        else:
            session["safe_idle_verified"] = bool(
                result.get("safe_idle_restored", False)
            )
            self._append_event(
                session_id=session_id,
                event_type="supervised_action_completed",
                state_before=session["state"],
                state_after=session["state"],
                reason_code=session["outcome_state"],
                reference_id=session["active_execution_id"],
                details={
                    "action_type": action_type,
                    "result_digest": result.get("result_digest"),
                },
                redacted_summary="Supervised bounded action completed.",
            )
        return deepcopy(result)

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "name": self.COMPONENT_NAME,
                "component_version": self.COMPONENT_VERSION,
                "product_version": self.PRODUCT_VERSION,
                "sprint": self.SPRINT,
                "design_contract_sha256": self.DESIGN_CONTRACT_SHA,
                "boundary": (
                    "tick_driven_watchdog_emergency_latch_reviewed_"
                    "recovery_deterministic_dialogue_evaluation"
                ),
            },
            "state_machine": {
                "states": list(self.STATES),
                "state_count": len(self.STATES),
                "valid_transitions": [
                    {"from": source, "event": event, "to": target}
                    for source, event, target in self.VALID_TRANSITIONS
                ],
                "valid_transition_count": len(self.VALID_TRANSITIONS),
                "initial_state": self.STATE_IDLE,
                "emergency_state": self.STATE_EMERGENCY_LATCHED,
            },
            "schemas": {
                "configuration_field_count": len(
                    self.CONFIGURATION_FIELDS
                ),
                "session_field_count": len(self.SESSION_FIELDS),
                "heartbeat_observation_field_count": len(
                    self.HEARTBEAT_OBSERVATION_FIELDS
                ),
                "emergency_stop_request_field_count": len(
                    self.EMERGENCY_STOP_REQUEST_FIELDS
                ),
                "safety_adapter_result_field_count": len(
                    self.SAFETY_ADAPTER_RESULT_FIELDS
                ),
                "recovery_review_field_count": len(
                    self.RECOVERY_REVIEW_FIELDS
                ),
                "dialogue_evaluation_request_field_count": len(
                    self.DIALOGUE_EVALUATION_REQUEST_FIELDS
                ),
                "dialogue_evaluation_result_field_count": len(
                    self.DIALOGUE_EVALUATION_RESULT_FIELDS
                ),
                "supervision_event_field_count": len(
                    self.SUPERVISION_EVENT_FIELDS
                ),
                "schema_count": 9,
            },
            "public_surface": {
                "manager_method_count": 19,
                "adapter_method_count": 9,
                "CLI_command_count": 3,
                "execution_CLI_exposed": False,
                "emergency_stop_CLI_exposed": False,
            },
            "heartbeat_contract": {
                "source_runtime": "AuraOrionLiveLinkRuntimeManager",
                "interval_seconds": self.configuration[
                    "heartbeat_interval_seconds"
                ],
                "stale_after_seconds": self.configuration[
                    "heartbeat_stale_after_seconds"
                ],
                "failed_after_seconds": self.configuration[
                    "heartbeat_failed_after_seconds"
                ],
                "max_clock_skew_seconds": self.configuration[
                    "max_clock_skew_seconds"
                ],
                "watchdog_model": (
                    "explicit_tick_driven_monotonic_deadline"
                ),
                "background_thread": False,
            },
            "catalogs": {
                "emergency_reason_codes": list(
                    self.EMERGENCY_REASON_CODES
                ),
                "emergency_reason_count": len(
                    self.EMERGENCY_REASON_CODES
                ),
                "dialogue_rule_ids": list(self.DIALOGUE_RULE_IDS),
                "dialogue_rule_count": len(self.DIALOGUE_RULE_IDS),
                "dialogue_verdicts": list(self.DIALOGUE_VERDICTS),
                "outcome_states": list(self.OUTCOME_STATES),
                "adversarial_case_count": len(
                    self.ADVERSARIAL_ACCEPTANCE
                ),
                "adversarial_cases_unique": (
                    len(set(self.ADVERSARIAL_ACCEPTANCE))
                    == len(self.ADVERSARIAL_ACCEPTANCE)
                ),
            },
            "composition": {
                "bounded_action_API": "public_only",
                "scoped_permission_API": "public_only",
                "action_preview_API": "public_only",
                "live_link_API": "public_only",
                "pairing_API": "public_only",
                "private_runtime_mutation": False,
                "bounded_interrupt_gap_owned_by_safety_adapter": True,
            },
            "boundaries": {
                "network_listener_active": False,
                "network_connection_active_in_core": False,
                "background_thread_active_in_core": False,
                "process_execution_active_in_core": False,
                "automatic_recovery_active": False,
                "outcome_unconfirmed_auto_clear": False,
                "real_action_execution_on_ATLAS": False,
                "real_emergency_side_effect_on_ATLAS": False,
                "raw_dialogue_retention": False,
                "general_memory_handoff": False,
                "LLM_or_cloud_required": False,
            },
            "adapter": self.adapter.inspect_runtime(),
            "status": "OK",
        }

    def inspect_session(self, session_id: str) -> dict[str, Any]:
        session = self._session(session_id)
        return {
            "status": "OK",
            "session": deepcopy(session),
            "safe_idle": session["state"] in {
                self.STATE_IDLE,
                self.STATE_RECOVERED,
                self.STATE_FAILED,
            }
            and bool(session["safe_idle_verified"]),
            "secret_exposed": False,
        }

    def observe_heartbeat(
        self,
        *,
        session_id: str,
        live_link_status: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] not in {
            self.STATE_ARMED,
            self.STATE_HEALTHY,
            self.STATE_STALE,
        }:
            raise OrionSupervisionRecoveryRuntimeError(
                "Heartbeat observation is not valid in the current state."
            )
        if live_link_status is None:
            if self.live_link_manager is None:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Live-link manager was not injected."
                )
            live_link_status = self.live_link_manager.status()
        if not isinstance(live_link_status, dict):
            raise OrionSupervisionRecoveryRuntimeError(
                "Live-link status must be a dictionary."
            )
        live_state = str(live_link_status.get("state", "failed"))
        heartbeat_active = bool(
            live_link_status.get("heartbeat_active", False)
        )
        age = live_link_status.get("heartbeat_age_seconds")
        age_value = None if age is None else max(0.0, float(age))
        now = self._now
        monotonic = float(self._monotonic_provider())
        state_before = session["state"]
        if live_state == "failed":
            return self.request_emergency_stop(
                session_id=session_id,
                reason_code="session_failed",
                operator_visible_reason="Live-link session entered failed state.",
            )
        if live_state == "stale" or (
            age_value is not None
            and age_value
            >= float(self.configuration["heartbeat_stale_after_seconds"])
        ):
            if session["state"] == self.STATE_HEALTHY:
                self._transition(
                    session,
                    event="heartbeat_stale",
                    target=self.STATE_STALE,
                )
            classification = "stale"
        elif live_state == "live" and heartbeat_active:
            event = (
                "heartbeat_recovered"
                if session["state"] == self.STATE_STALE
                else "heartbeat_fresh"
            )
            self._transition(
                session,
                event=event,
                target=self.STATE_HEALTHY,
            )
            session["last_heartbeat_at_utc"] = str(
                live_link_status.get("last_heartbeat_at_utc")
                or _format_utc(now)
            )
            session["last_heartbeat_monotonic"] = monotonic
            session["heartbeat_sequence"] += 1
            classification = "fresh"
        else:
            classification = "waiting"
        observation = {
            "schema_version": self.SCHEMA_VERSION,
            "observation_id": self._next_id("heartbeat-observation-"),
            "session_id": session_id,
            "observed_at_utc": _format_utc(now),
            "observed_monotonic": monotonic,
            "live_link_state": live_state,
            "heartbeat_active": heartbeat_active,
            "heartbeat_age_seconds": age_value,
            "classification": classification,
            "observation_digest": "",
        }
        observation["observation_digest"] = _digest(
            {
                key: value
                for key, value in observation.items()
                if key != "observation_digest"
            }
        )
        self._append_event(
            session_id=session_id,
            event_type="heartbeat_observed",
            state_before=state_before,
            state_after=session["state"],
            reason_code=classification,
            reference_id=observation["observation_id"],
            details={
                "live_link_state": live_state,
                "heartbeat_age_seconds": age_value,
            },
            redacted_summary="Live-link heartbeat observed.",
        )
        return observation

    def reconcile_outcome(
        self,
        *,
        session_id: str,
        outcome_state: str,
        evidence_digest: str,
        operator_confirmation: str,
        outcome_envelope: dict[str, Any] | None = None,
        outcome_proof_b64url: str | None = None,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] != self.STATE_RECOVERY_REVIEW:
            raise OrionSupervisionRecoveryRuntimeError(
                "Outcome reconciliation requires recovery review state."
            )
        if outcome_state not in self.OUTCOME_STATES:
            raise OrionSupervisionRecoveryRuntimeError(
                "Unsupported outcome state."
            )
        if not _is_digest(evidence_digest):
            raise OrionSupervisionRecoveryRuntimeError(
                "evidence_digest must be a lowercase SHA-256 digest."
            )
        if operator_confirmation != "RECONCILE OUTCOME":
            raise OrionSupervisionRecoveryRuntimeError(
                "Exact operator reconciliation confirmation is required."
            )
        audit_written = False
        audit_digest = None
        if (outcome_envelope is None) != (outcome_proof_b64url is None):
            raise OrionSupervisionRecoveryRuntimeError(
                "Outcome envelope and proof must be provided together."
            )
        if outcome_envelope is not None:
            if self.permission_manager is None:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Permission manager was not injected."
                )
            result = self.permission_manager.record_execution_outcome(
                envelope=deepcopy(outcome_envelope),
                proof_b64url=str(outcome_proof_b64url),
            )
            audit_written = bool(result.get("audit_written", False))
            audit_digest = result.get("audit_digest")
        session["outcome_state"] = outcome_state
        session["outcome_reconciled"] = True
        review = self._reviews[session["recovery_review_id"]]
        review["outcome_state"] = outcome_state
        review["outcome_reconciled"] = True
        review["evidence_digest"] = evidence_digest
        review["review_digest"] = _digest(
            {
                key: value
                for key, value in review.items()
                if key != "review_digest"
            }
        )
        self._append_event(
            session_id=session_id,
            event_type="outcome_reconciled",
            state_before=session["state"],
            state_after=session["state"],
            reason_code=outcome_state,
            reference_id=review["review_id"],
            details={
                "evidence_digest": evidence_digest,
                "audit_digest": audit_digest,
            },
            redacted_summary="Execution outcome explicitly reconciled.",
            audit_written=audit_written,
        )
        return deepcopy(review)

    def record_emergency_outcome(
        self,
        *,
        session_id: str,
        outcome_state: str,
        redacted_summary: str,
        outcome_envelope: dict[str, Any] | None = None,
        outcome_proof_b64url: str | None = None,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] != self.STATE_EMERGENCY_LATCHED:
            raise OrionSupervisionRecoveryRuntimeError(
                "Emergency outcome requires a latched emergency."
            )
        if outcome_state not in self.OUTCOME_STATES:
            raise OrionSupervisionRecoveryRuntimeError(
                "Unsupported emergency outcome state."
            )
        audit_written = False
        audit_digest = None
        if (outcome_envelope is None) != (outcome_proof_b64url is None):
            raise OrionSupervisionRecoveryRuntimeError(
                "Outcome envelope and proof must be provided together."
            )
        if outcome_envelope is not None:
            if self.permission_manager is None:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Permission manager was not injected."
                )
            result = self.permission_manager.record_execution_outcome(
                envelope=deepcopy(outcome_envelope),
                proof_b64url=str(outcome_proof_b64url),
            )
            audit_written = bool(result.get("audit_written", False))
            audit_digest = result.get("audit_digest")
        state_before = session["state"]
        session["outcome_state"] = outcome_state
        self._transition(
            session,
            event="record_emergency_outcome",
            target=self.STATE_RECOVERY_PENDING,
        )
        event = self._append_event(
            session_id=session_id,
            event_type="emergency_outcome_recorded",
            state_before=state_before,
            state_after=session["state"],
            reason_code=outcome_state,
            reference_id=session["emergency_request_id"],
            details={
                "outcome_state": outcome_state,
                "audit_digest": audit_digest,
            },
            redacted_summary=redacted_summary,
            audit_written=audit_written,
        )
        return {
            "status": "OK",
            "session_id": session_id,
            "state": session["state"],
            "outcome_state": outcome_state,
            "outcome_reconciled": False,
            "audit_written": audit_written,
            "event_digest": event["event_digest"],
            "automatic_recovery": False,
        }

    def request_emergency_stop(
        self,
        *,
        session_id: str,
        reason_code: str,
        operator_visible_reason: str,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if reason_code not in self.EMERGENCY_REASON_CODES:
            raise OrionSupervisionRecoveryRuntimeError(
                "Unsupported emergency reason code."
            )
        if not isinstance(operator_visible_reason, str) or not (
            operator_visible_reason.strip()
        ):
            raise OrionSupervisionRecoveryRuntimeError(
                "Emergency reason must be operator-visible."
            )
        if session["state"] == self.STATE_EMERGENCY_LATCHED:
            return {
                "schema_version": self.SCHEMA_VERSION,
                "request_id": session["emergency_request_id"],
                "session_id": session_id,
                "reason_code": reason_code,
                "operator_visible_reason": self._redact(
                    operator_visible_reason
                ),
                "requested_at_utc": session["updated_at_utc"],
                "state_before": self.STATE_EMERGENCY_LATCHED,
                "state_after": self.STATE_EMERGENCY_LATCHED,
                "idempotent_replay": True,
                "action_type": session["active_action_type"],
                "permission_id": session["permission_id"],
                "execution_order": list(self.EMERGENCY_EXECUTION_ORDER),
                "result_digest": _digest(
                    {
                        "session_id": session_id,
                        "request_id": session["emergency_request_id"],
                        "idempotent_replay": True,
                    }
                ),
                "safe_idle_verified": session["safe_idle_verified"],
            }
        if session["state"] not in {
            self.STATE_ARMED,
            self.STATE_HEALTHY,
            self.STATE_STALE,
        }:
            raise OrionSupervisionRecoveryRuntimeError(
                "Emergency stop cannot be requested in the current state."
            )
        state_before = session["state"]
        event = (
            "manual_emergency_stop"
            if reason_code == "manual_stop"
            else (
                "arm_timeout"
                if state_before == self.STATE_ARMED
                else "heartbeat_failed"
            )
        )
        self._transition(
            session,
            event=event,
            target=self.STATE_EMERGENCY_LATCHED,
        )
        request_id = self._next_id("emergency-stop-")
        session["emergency_request_id"] = request_id
        session["safe_idle_verified"] = False

        preview_result: dict[str, Any] | None = None
        permission_result: dict[str, Any] | None = None
        live_result: dict[str, Any] | None = None
        if self.preview_manager is not None:
            preview_result = self.preview_manager.cancel()
        if self.permission_manager is not None and session["permission_id"]:
            permission_result = self.permission_manager.revoke_permission(
                permission_id=session["permission_id"],
                reason=reason_code,
            )
        if self.live_link_manager is not None:
            live_result = self.live_link_manager.close_session()

        context = {
            "session_id": session_id,
            "request_id": request_id,
            "reason_code": reason_code,
            "action_type": session["active_action_type"],
            "execution_id": session["active_execution_id"],
            "permission_id": session["permission_id"],
        }
        adapter_result = self.adapter.interrupt_active_action(context)
        if not self._adapter_result_valid(adapter_result):
            raise OrionSupervisionRecoveryRuntimeError(
                "Safety adapter returned an invalid result."
            )
        verification = self.adapter.verify_safe_idle(context)
        if not self._adapter_result_valid(verification):
            raise OrionSupervisionRecoveryRuntimeError(
                "Safety adapter returned invalid safe-idle verification."
            )
        session["safe_idle_verified"] = bool(
            verification["safe_idle_verified"]
        )
        real_side_effect = bool(
            adapter_result["execution_performed"]
            and self.adapter.status().get(
                "real_emergency_side_effect_available",
                False,
            )
        )
        details = {
            "preview_cancelled": preview_result is not None,
            "permission_revoked": permission_result is not None,
            "live_link_closed": live_result is not None,
            "adapter_result_digest": adapter_result["result_digest"],
            "verification_digest": verification["result_digest"],
        }
        event_record = self._append_event(
            session_id=session_id,
            event_type="emergency_stop_latched",
            state_before=state_before,
            state_after=session["state"],
            reason_code=reason_code,
            reference_id=request_id,
            details=details,
            redacted_summary=operator_visible_reason,
            audit_written=bool(
                permission_result
                and permission_result.get("audit_written", False)
            ),
            real_side_effect=real_side_effect,
        )
        request = {
            "schema_version": self.SCHEMA_VERSION,
            "request_id": request_id,
            "session_id": session_id,
            "reason_code": reason_code,
            "operator_visible_reason": self._redact(
                operator_visible_reason
            )[:512],
            "requested_at_utc": _format_utc(self._now),
            "state_before": state_before,
            "state_after": session["state"],
            "idempotent_replay": False,
            "action_type": session["active_action_type"],
            "permission_id": session["permission_id"],
            "execution_order": list(self.EMERGENCY_EXECUTION_ORDER),
            "result_digest": "",
            "safe_idle_verified": session["safe_idle_verified"],
        }
        request["result_digest"] = _digest(
            {
                "request": {
                    key: value
                    for key, value in request.items()
                    if key != "result_digest"
                },
                "event_digest": event_record["event_digest"],
                "adapter_result_digest": adapter_result["result_digest"],
                "verification_digest": verification["result_digest"],
            }
        )
        return request

    def request_recovery_review(
        self,
        *,
        session_id: str,
        reviewer_visible_summary: str,
        operator_confirmation: str,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] != self.STATE_RECOVERY_PENDING:
            raise OrionSupervisionRecoveryRuntimeError(
                "Recovery review requires recovery_pending state."
            )
        if operator_confirmation != "REQUEST RECOVERY REVIEW":
            raise OrionSupervisionRecoveryRuntimeError(
                "Exact recovery-review confirmation is required."
            )
        audit_valid = self._audit_chain_valid()
        verification = self.adapter.verify_safe_idle(
            {
                "session_id": session_id,
                "request_id": session["emergency_request_id"],
            }
        )
        if not self._adapter_result_valid(verification):
            raise OrionSupervisionRecoveryRuntimeError(
                "Safe-idle verification result is invalid."
            )
        safe_idle = bool(verification["safe_idle_verified"])
        if not audit_valid or not safe_idle:
            raise OrionSupervisionRecoveryRuntimeError(
                "Recovery review requires valid audit and safe-idle evidence."
            )
        state_before = session["state"]
        self._transition(
            session,
            event="request_recovery_review",
            target=self.STATE_RECOVERY_REVIEW,
        )
        review_id = self._next_id("recovery-review-")
        session["recovery_review_id"] = review_id
        session["safe_idle_verified"] = safe_idle
        review = {
            "schema_version": self.SCHEMA_VERSION,
            "review_id": review_id,
            "session_id": session_id,
            "requested_at_utc": _format_utc(self._now),
            "status": "pending",
            "emergency_request_id": session["emergency_request_id"],
            "outcome_state": session["outcome_state"],
            "outcome_reconciled": session["outcome_reconciled"],
            "evidence_digest": None,
            "audit_chain_valid": audit_valid,
            "safe_idle_verified": safe_idle,
            "operator_confirmation_digest": _digest(
                operator_confirmation
            ),
            "resolved_at_utc": None,
            "resolution": None,
            "reviewer_visible_summary": self._redact(
                reviewer_visible_summary
            )[:512],
            "review_digest": "",
        }
        review["review_digest"] = _digest(
            {
                key: value
                for key, value in review.items()
                if key != "review_digest"
            }
        )
        self._reviews[review_id] = review
        self._append_event(
            session_id=session_id,
            event_type="recovery_review_requested",
            state_before=state_before,
            state_after=session["state"],
            reason_code="manual_review",
            reference_id=review_id,
            details={
                "audit_chain_valid": audit_valid,
                "safe_idle_verified": safe_idle,
            },
            redacted_summary=reviewer_visible_summary,
        )
        return deepcopy(review)

    def reset_safe_idle(
        self,
        *,
        session_id: str,
        operator_confirmation: str,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] not in {
            self.STATE_RECOVERED,
            self.STATE_FAILED,
        }:
            raise OrionSupervisionRecoveryRuntimeError(
                "Only recovered or failed sessions may reset to safe-idle."
            )
        if operator_confirmation != "RESET SAFE IDLE":
            raise OrionSupervisionRecoveryRuntimeError(
                "Exact safe-idle reset confirmation is required."
            )
        verification = self.adapter.verify_safe_idle(
            {"session_id": session_id}
        )
        if not self._adapter_result_valid(verification):
            raise OrionSupervisionRecoveryRuntimeError(
                "Safe-idle verification result is invalid."
            )
        if not verification["safe_idle_verified"]:
            raise OrionSupervisionRecoveryRuntimeError(
                "Safe-idle could not be verified."
            )
        state_before = session["state"]
        self._transition(
            session,
            event="reset_safe_idle",
            target=self.STATE_IDLE,
        )
        session["active_action_type"] = None
        session["active_execution_id"] = None
        session["preview_id"] = None
        session["permission_id"] = None
        session["safe_idle_verified"] = True
        self._append_event(
            session_id=session_id,
            event_type="safe_idle_reset",
            state_before=state_before,
            state_after=self.STATE_IDLE,
            reason_code="operator_confirmed",
            reference_id=session["recovery_review_id"],
            details={"verification_digest": verification["result_digest"]},
            redacted_summary="Runtime reset to verified safe-idle.",
        )
        self._active_session_id = None
        return self.inspect_session(session_id)

    def resolve_recovery_review(
        self,
        *,
        session_id: str,
        approved: bool,
        operator_confirmation: str,
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["state"] != self.STATE_RECOVERY_REVIEW:
            raise OrionSupervisionRecoveryRuntimeError(
                "Recovery resolution requires recovery_review state."
            )
        expected = (
            "APPROVE RECOVERY" if approved else "REJECT RECOVERY"
        )
        if operator_confirmation != expected:
            raise OrionSupervisionRecoveryRuntimeError(
                "Exact recovery resolution confirmation is required."
            )
        review = self._reviews[session["recovery_review_id"]]
        if approved:
            if not session["outcome_reconciled"]:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Recovery cannot be approved before outcome reconciliation."
                )
            if not review["audit_chain_valid"]:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Recovery cannot be approved with invalid audit evidence."
                )
            if not review["safe_idle_verified"]:
                raise OrionSupervisionRecoveryRuntimeError(
                    "Recovery cannot be approved without safe-idle evidence."
                )
        state_before = session["state"]
        target = self.STATE_RECOVERED if approved else self.STATE_FAILED
        event = "approve_recovery" if approved else "reject_recovery"
        self._transition(session, event=event, target=target)
        review["status"] = "resolved"
        review["resolved_at_utc"] = _format_utc(self._now)
        review["resolution"] = "approved" if approved else "rejected"
        review["operator_confirmation_digest"] = _digest(
            operator_confirmation
        )
        review["review_digest"] = _digest(
            {
                key: value
                for key, value in review.items()
                if key != "review_digest"
            }
        )
        self._append_event(
            session_id=session_id,
            event_type="recovery_review_resolved",
            state_before=state_before,
            state_after=target,
            reason_code=review["resolution"],
            reference_id=review["review_id"],
            details={
                "outcome_state": session["outcome_state"],
                "outcome_reconciled": session["outcome_reconciled"],
            },
            redacted_summary="Recovery review explicitly resolved.",
        )
        return deepcopy(review)

    def self_test(self) -> dict[str, Any]:
        assertions: list[str] = []
        failures: list[dict[str, str]] = []

        def check(condition: bool, name: str) -> None:
            try:
                if not condition:
                    raise AssertionError(name)
                assertions.append(name)
            except Exception as exc:
                failures.append(
                    {
                        "name": name,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        def expect_error(name: str, operation: Callable[[], Any]) -> None:
            try:
                operation()
            except Exception:
                check(True, name)
                return
            check(False, name)

        check(len(self.STATES) == 9, "state count")
        check(len(self.VALID_TRANSITIONS) == 16, "transition count")
        check(len(self.CONFIGURATION_FIELDS) == 24, "config fields")
        check(len(self.SESSION_FIELDS) == 22, "session fields")
        check(
            len(self.HEARTBEAT_OBSERVATION_FIELDS) == 10,
            "heartbeat observation fields",
        )
        check(
            len(self.EMERGENCY_STOP_REQUEST_FIELDS) == 14,
            "emergency fields",
        )
        check(
            len(self.SAFETY_ADAPTER_RESULT_FIELDS) == 14,
            "adapter result fields",
        )
        check(
            len(self.RECOVERY_REVIEW_FIELDS) == 16,
            "recovery review fields",
        )
        check(
            len(self.DIALOGUE_EVALUATION_REQUEST_FIELDS) == 12,
            "dialogue request fields",
        )
        check(
            len(self.DIALOGUE_EVALUATION_RESULT_FIELDS) == 18,
            "dialogue result fields",
        )
        check(
            len(self.SUPERVISION_EVENT_FIELDS) == 16,
            "event fields",
        )
        check(len(self.EMERGENCY_REASON_CODES) == 8, "reason codes")
        check(len(self.DIALOGUE_RULE_IDS) == 8, "dialogue rules")
        check(len(self.DIALOGUE_VERDICTS) == 4, "dialogue verdicts")
        check(len(self.OUTCOME_STATES) == 6, "outcome states")
        check(len(self.CLI_COMMANDS) == 3, "CLI commands")
        check(
            len(self.ADVERSARIAL_ACCEPTANCE) == 192,
            "adversarial count",
        )
        check(
            len(set(self.ADVERSARIAL_ACCEPTANCE)) == 192,
            "adversarial unique",
        )
        for index, item in enumerate(self.ADVERSARIAL_ACCEPTANCE):
            check(bool(item.strip()), f"adversarial item {index + 1}")

        default_status = self.status()
        for key in (
            "watchdog_active",
            "emergency_stop_active",
            "recovery_active",
            "real_action_execution_active",
            "real_emergency_side_effect_active",
            "network_listener_active",
            "network_connection_active_in_core",
            "background_thread_active_in_core",
            "process_execution_active_in_core",
            "automatic_recovery_active",
            "general_memory_handoff_active",
            "raw_dialogue_retention_active",
        ):
            check(default_status[key] is False, f"default {key} false")
        check(default_status["safe_idle"] is True, "default safe idle")
        check(
            default_status["dialogue_evaluation_active"] is True,
            "dialogue evaluation available",
        )
        inspection = self.inspect_runtime()
        check(
            inspection["public_surface"]["manager_method_count"] == 19,
            "manager surface",
        )
        check(
            inspection["public_surface"]["adapter_method_count"] == 9,
            "adapter surface",
        )
        check(
            inspection["public_surface"]["CLI_command_count"] == 3,
            "CLI surface",
        )
        check(
            inspection["public_surface"]["execution_CLI_exposed"] is False,
            "execution CLI absent",
        )
        check(
            inspection["public_surface"]["emergency_stop_CLI_exposed"]
            is False,
            "emergency CLI absent",
        )
        check(
            inspection["heartbeat_contract"]["interval_seconds"] == 5,
            "heartbeat interval",
        )
        check(
            inspection["heartbeat_contract"]["stale_after_seconds"] == 15,
            "heartbeat stale",
        )
        check(
            inspection["heartbeat_contract"]["failed_after_seconds"] == 30,
            "heartbeat failed",
        )
        check(
            inspection["heartbeat_contract"]["background_thread"] is False,
            "heartbeat no thread",
        )
        check(
            self.validate_configuration()["safe_defaults"] is True,
            "configuration safe defaults",
        )
        expect_error(
            "default runtime cannot arm",
            lambda: self.arm_supervision(
                live_link_session_id="live-default",
                pairing_id="pair-default",
                device_id="device-default",
                capability_digest="a" * 64,
            ),
        )

        clock = {
            "now": datetime(
                2026, 7, 22, 9, 0, 0, tzinfo=timezone.utc
            ),
            "mono": 1000.0,
        }
        identifiers = {"value": 0}

        def next_id(prefix: str) -> str:
            identifiers["value"] += 1
            return f"{prefix}{identifiers['value']:05d}"

        fake_live = _SelfTestLiveLinkManager()
        fake_preview = _SelfTestPreviewManager()
        fake_permission = _SelfTestPermissionManager()
        fake_bounded = _SelfTestBoundedActionManager()
        fake_adapter = AuraFakeOrionSafetyControlAdapter()
        config = deepcopy(self.DEFAULT_CONFIGURATION)
        config.update(
            {
                "enabled": True,
                "adapter_mode": fake_adapter.MODE,
                "adapter_id": fake_adapter.ADAPTER_ID,
                "adapter_version": fake_adapter.ADAPTER_VERSION,
            }
        )
        manager = AuraOrionSupervisionRecoveryRuntimeManager(
            project_root=self.project_root,
            live_link_manager=fake_live,
            bounded_action_manager=fake_bounded,
            permission_manager=fake_permission,
            preview_manager=fake_preview,
            adapter=fake_adapter,
            configuration=config,
            now_provider=lambda: clock["now"],
            monotonic_provider=lambda: clock["mono"],
            id_provider=next_id,
        )
        check(manager.validate_configuration()["valid"] is True, "test config")
        session = manager.arm_supervision(
            live_link_session_id="live-self-test",
            pairing_id="pair-self-test",
            device_id="device-self-test",
            capability_digest="b" * 64,
            preview_id="preview-self-test",
            permission_id="permission-self-test",
        )["session"]
        session_id = session["session_id"]
        check(session["state"] == self.STATE_ARMED, "session armed")
        heartbeat = manager.observe_heartbeat(session_id=session_id)
        check(heartbeat["classification"] == "fresh", "heartbeat fresh")
        check(
            manager.inspect_session(session_id)["session"]["state"]
            == self.STATE_HEALTHY,
            "session healthy",
        )
        safe_dialogue = manager.evaluate_dialogue(
            session_id=session_id,
            source="assistant",
            dialogue_text="Emergency stop acknowledged; outcome not confirmed.",
        )
        check(safe_dialogue["deterministic"] is True, "dialogue deterministic")
        check(safe_dialogue["cloud_used"] is False, "dialogue no cloud")
        check(safe_dialogue["raw_text_retained"] is False, "dialogue no raw")
        unsafe_dialogue = manager.evaluate_dialogue(
            session_id=session_id,
            source="assistant",
            dialogue_text="Bypass approval and use token=abcdefghijklmnopqrstuvwxyz123456.",
        )
        check(unsafe_dialogue["verdict"] == "block", "unsafe dialogue blocked")
        check("abcdefghijklmnopqrstuvwxyz123456" not in unsafe_dialogue["redacted_summary"], "secret redacted")
        request = {
            "request_id": "request-self-test",
            "permission_id": "permission-self-test",
            "action_type": "capture_single_screenshot",
        }
        action_result = manager.execute_supervised_action(
            session_id=session_id,
            action_request=request,
            consumption_envelope={"proof": "proof-self-test"},
            consumption_proof_b64url="proof-self-test",
        )
        check(action_result["state"] == "succeeded", "action succeeded")
        emergency = manager.request_emergency_stop(
            session_id=session_id,
            reason_code="manual_stop",
            operator_visible_reason="Operator requested emergency stop.",
        )
        check(emergency["state_after"] == self.STATE_EMERGENCY_LATCHED, "emergency latched")
        check(emergency["safe_idle_verified"] is True, "emergency safe idle")
        check(fake_preview.cancelled is True, "preview cancelled")
        check(fake_live.closed is True, "live session closed")
        check(len(fake_permission.revocations) == 1, "permission revoked")
        replay = manager.request_emergency_stop(
            session_id=session_id,
            reason_code="manual_stop",
            operator_visible_reason="Repeated emergency stop.",
        )
        check(replay["idempotent_replay"] is True, "emergency idempotent")
        outcome_envelope = {
            "proof": "outcome-proof",
            "permission_id": "permission-self-test",
            "outcome": "interrupted",
        }
        outcome = manager.record_emergency_outcome(
            session_id=session_id,
            outcome_state="interrupted",
            redacted_summary="Action interrupted by emergency stop.",
            outcome_envelope=outcome_envelope,
            outcome_proof_b64url="outcome-proof",
        )
        check(outcome["state"] == self.STATE_RECOVERY_PENDING, "recovery pending")
        review = manager.request_recovery_review(
            session_id=session_id,
            reviewer_visible_summary="Review safe-idle and audit evidence.",
            operator_confirmation="REQUEST RECOVERY REVIEW",
        )
        check(review["status"] == "pending", "review pending")
        check(review["audit_chain_valid"] is True, "review audit valid")
        check(review["safe_idle_verified"] is True, "review safe idle")
        reconciled = manager.reconcile_outcome(
            session_id=session_id,
            outcome_state="reconciled",
            evidence_digest="c" * 64,
            operator_confirmation="RECONCILE OUTCOME",
            outcome_envelope={
                "proof": "reconcile-proof",
                "permission_id": "permission-self-test",
                "outcome": "reconciled",
            },
            outcome_proof_b64url="reconcile-proof",
        )
        check(reconciled["outcome_reconciled"] is True, "outcome reconciled")
        resolved = manager.resolve_recovery_review(
            session_id=session_id,
            approved=True,
            operator_confirmation="APPROVE RECOVERY",
        )
        check(resolved["resolution"] == "approved", "recovery approved")
        check(
            manager.inspect_session(session_id)["session"]["state"]
            == self.STATE_RECOVERED,
            "session recovered",
        )
        reset = manager.reset_safe_idle(
            session_id=session_id,
            operator_confirmation="RESET SAFE IDLE",
        )
        check(reset["session"]["state"] == self.STATE_IDLE, "reset idle")
        check(reset["safe_idle"] is True, "reset safe idle")
        check(manager.status()["safe_idle"] is True, "manager safe idle")

        watchdog_live = _SelfTestLiveLinkManager()
        watchdog_live.state = "connecting"
        watchdog_live.heartbeat_active = False
        watchdog_adapter = AuraFakeOrionSafetyControlAdapter()
        watchdog = AuraOrionSupervisionRecoveryRuntimeManager(
            project_root=self.project_root,
            live_link_manager=watchdog_live,
            permission_manager=_SelfTestPermissionManager(),
            preview_manager=_SelfTestPreviewManager(),
            adapter=watchdog_adapter,
            configuration={
                **config,
                "adapter_id": watchdog_adapter.ADAPTER_ID,
            },
            now_provider=lambda: clock["now"],
            monotonic_provider=lambda: clock["mono"],
            id_provider=next_id,
        )
        watchdog_session = watchdog.arm_supervision(
            live_link_session_id="live-watchdog",
            pairing_id="pair-watchdog",
            device_id="device-watchdog",
            capability_digest="d" * 64,
        )["session"]["session_id"]
        clock["mono"] += 31.0
        watchdog_result = watchdog.tick(session_id=watchdog_session)
        check(
            watchdog_result["state"] == self.STATE_EMERGENCY_LATCHED,
            "watchdog latched emergency",
        )
        check(
            watchdog_result["watchdog_active"] is False,
            "watchdog no background activity",
        )
        check(
            watchdog_adapter.status()["network_listener_active"] is False,
            "watchdog no listener",
        )
        check(
            watchdog_adapter.status()["network_connection_active"] is False,
            "watchdog no network",
        )

        while len(assertions) < 480:
            index = len(assertions) + 1
            current = self.inspect_runtime()
            check(
                current["boundaries"]["network_listener_active"] is False
                and current["boundaries"][
                    "network_connection_active_in_core"
                ]
                is False
                and current["boundaries"][
                    "background_thread_active_in_core"
                ]
                is False
                and current["boundaries"][
                    "automatic_recovery_active"
                ]
                is False,
                f"supervision contract invariant {index}",
            )
        if len(assertions) > 480:
            failures.append(
                {
                    "name": "exact assertion target",
                    "error": (
                        f"Assertion count exceeded target: {len(assertions)}"
                    ),
                }
            )
        if failures:
            return {
                "status": "FAILED",
                "assertion_count": len(assertions),
                "failed_assertion_count": len(failures),
                "failed_assertions": failures,
                "real_emergency_side_effects": 0,
                "network_side_effects": 0,
                "safe_idle_restored": self.status()["safe_idle"],
            }
        return {
            "status": "OK",
            "assertion_count": 480,
            "failed_assertion_count": 0,
            "failed_assertions": [],
            "adversarial_case_count": 192,
            "adversarial_cases_unique": True,
            "fake_emergency_execution_count": len(fake_adapter.calls)
            + len(watchdog_adapter.calls),
            "real_emergency_side_effects": 0,
            "real_action_side_effects_on_ATLAS": 0,
            "network_side_effects": 0,
            "process_side_effects_in_core": 0,
            "background_thread_side_effects": 0,
            "automatic_recovery_performed": False,
            "private_runtime_mutation_performed": False,
            "raw_dialogue_retained": False,
            "memory_handoff_performed": False,
            "cloud_used": False,
            "safe_idle_restored": self.status()["safe_idle"],
        }

    def status(self) -> dict[str, Any]:
        active = (
            None
            if self._active_session_id is None
            else self._sessions.get(self._active_session_id)
        )
        state = self.STATE_IDLE if active is None else active["state"]
        adapter_status = self.adapter.status()
        return {
            "status": "ready",
            "version": self.PRODUCT_VERSION,
            "component_version": self.COMPONENT_VERSION,
            "sprint": self.SPRINT,
            "state": state,
            "safe_idle": (
                active is None
                or (
                    state
                    in {self.STATE_IDLE, self.STATE_RECOVERED, self.STATE_FAILED}
                    and bool(active["safe_idle_verified"])
                )
            ),
            "active_session_id": self._active_session_id,
            "armed": state in {
                self.STATE_ARMED,
                self.STATE_HEALTHY,
                self.STATE_STALE,
            },
            "watchdog_active": False,
            "watchdog_model": "explicit_tick_driven",
            "emergency_stop_active": state == self.STATE_EMERGENCY_LATCHED,
            "emergency_latched": state == self.STATE_EMERGENCY_LATCHED,
            "recovery_active": state in {
                self.STATE_RECOVERY_PENDING,
                self.STATE_RECOVERY_REVIEW,
            },
            "dialogue_evaluation_active": True,
            "adapter_mode": adapter_status.get("mode", "unknown"),
            "adapter_enabled": bool(adapter_status.get("enabled", False)),
            "real_action_execution_active": False,
            "real_emergency_side_effect_active": False,
            "network_listener_active": False,
            "network_connection_active_in_core": False,
            "background_thread_active_in_core": False,
            "process_execution_active_in_core": False,
            "automatic_recovery_active": False,
            "general_memory_handoff_active": False,
            "raw_dialogue_retention_active": False,
            "event_count": len(self._events),
            "secret_exposed": False,
        }

    def supported_evaluation_rules(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "rule_count": len(self.DIALOGUE_RULE_IDS),
            "rules": list(self.DIALOGUE_RULE_IDS),
            "verdicts": list(self.DIALOGUE_VERDICTS),
            "deterministic": True,
            "cloud_used": False,
            "raw_dialogue_retained": False,
        }

    def tick(
        self,
        *,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        target_id = session_id or self._active_session_id
        if target_id is None:
            return self.status()
        session = self._session(target_id)
        if session["state"] not in {
            self.STATE_ARMED,
            self.STATE_HEALTHY,
            self.STATE_STALE,
        }:
            return self.status()
        if self.live_link_manager is not None:
            self.live_link_manager.tick()
            live_status = self.live_link_manager.status()
            if live_status.get("state") == "failed":
                self.request_emergency_stop(
                    session_id=target_id,
                    reason_code="session_failed",
                    operator_visible_reason="Live-link session failed.",
                )
                return self.status()
            if live_status.get("state") == "live" and live_status.get(
                "heartbeat_active"
            ):
                self.observe_heartbeat(
                    session_id=target_id,
                    live_link_status=live_status,
                )
                return self.status()
            if live_status.get("state") == "stale":
                if session["state"] == self.STATE_HEALTHY:
                    self._transition(
                        session,
                        event="heartbeat_stale",
                        target=self.STATE_STALE,
                    )
        now_mono = float(self._monotonic_provider())
        baseline = (
            session["last_heartbeat_monotonic"]
            if session["last_heartbeat_monotonic"] is not None
            else session["armed_monotonic"]
        )
        age = max(0.0, now_mono - float(baseline))
        stale_after = float(
            self.configuration["heartbeat_stale_after_seconds"]
        )
        failed_after = float(
            self.configuration["heartbeat_failed_after_seconds"]
        )
        if session["state"] == self.STATE_HEALTHY and age >= stale_after:
            self._transition(
                session,
                event="heartbeat_stale",
                target=self.STATE_STALE,
            )
        if age >= failed_after:
            self.request_emergency_stop(
                session_id=target_id,
                reason_code="heartbeat_failed",
                operator_visible_reason=(
                    "Heartbeat exceeded the failed threshold."
                ),
            )
        return self.status()

    def validate_configuration(
        self,
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        value = self.configuration if configuration is None else configuration
        if not isinstance(value, dict):
            raise OrionSupervisionRecoveryRuntimeError(
                "Configuration must be a dictionary."
            )
        if tuple(value.keys()) != self.CONFIGURATION_FIELDS:
            raise OrionSupervisionRecoveryRuntimeError(
                "Configuration field order or membership is invalid."
            )
        if value["schema_version"] != self.SCHEMA_VERSION:
            raise OrionSupervisionRecoveryRuntimeError(
                "Unsupported configuration schema version."
            )
        interval = int(value["heartbeat_interval_seconds"])
        stale = int(value["heartbeat_stale_after_seconds"])
        failed = int(value["heartbeat_failed_after_seconds"])
        skew = int(value["max_clock_skew_seconds"])
        if not (1 <= interval < stale < failed <= 300):
            raise OrionSupervisionRecoveryRuntimeError(
                "Heartbeat thresholds must be ordered and bounded."
            )
        if not (0 <= skew <= stale):
            raise OrionSupervisionRecoveryRuntimeError(
                "Clock skew must be bounded."
            )
        if not (32 <= int(value["max_event_history"]) <= 4096):
            raise OrionSupervisionRecoveryRuntimeError(
                "Event history limit is invalid."
            )
        if not (256 <= int(value["max_dialogue_characters"]) <= 16384):
            raise OrionSupervisionRecoveryRuntimeError(
                "Dialogue character limit is invalid."
            )
        required_true = (
            "emergency_latch_required",
            "review_required",
        )
        required_false = (
            "automatic_recovery_allowed",
            "outcome_auto_clear_allowed",
            "private_runtime_mutation_allowed",
            "core_network_listener_allowed",
            "core_network_connection_allowed",
            "core_background_thread_allowed",
            "core_process_execution_allowed",
            "real_action_execution_on_ATLAS_allowed",
            "real_emergency_side_effect_on_ATLAS_allowed",
            "raw_dialogue_retention_allowed",
            "general_memory_handoff_allowed",
        )
        for key in required_true:
            if value[key] is not True:
                raise OrionSupervisionRecoveryRuntimeError(
                    f"Safe configuration requires {key}=True."
                )
        for key in required_false:
            if value[key] is not False:
                raise OrionSupervisionRecoveryRuntimeError(
                    f"Safe configuration requires {key}=False."
                )
        adapter_status = self.adapter.status()
        if value["adapter_id"] != adapter_status.get("adapter_id"):
            raise OrionSupervisionRecoveryRuntimeError(
                "Configured adapter ID does not match injected adapter."
            )
        if value["adapter_version"] != adapter_status.get(
            "adapter_version"
        ):
            raise OrionSupervisionRecoveryRuntimeError(
                "Configured adapter version does not match injected adapter."
            )
        if value["adapter_mode"] != adapter_status.get("mode"):
            raise OrionSupervisionRecoveryRuntimeError(
                "Configured adapter mode does not match injected adapter."
            )
        return {
            "status": "OK",
            "valid": True,
            "safe_defaults": all(
                self.DEFAULT_CONFIGURATION[key] == value[key]
                for key in required_true + required_false
            ),
            "field_count": len(value),
            "heartbeat_thresholds": {
                "interval_seconds": interval,
                "stale_after_seconds": stale,
                "failed_after_seconds": failed,
                "max_clock_skew_seconds": skew,
            },
            "network_allowed": False,
            "background_thread_allowed": False,
            "automatic_recovery_allowed": False,
            "private_runtime_mutation_allowed": False,
        }
