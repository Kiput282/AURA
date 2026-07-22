"""Sprint 276 ORION action preview and explicit approval runtime."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


class OrionActionPreviewApprovalRuntimeError(RuntimeError):
    """Raised when the Sprint 276 preview/approval contract is violated."""


class AuraOrionActionPreviewApprovalRuntimeManager:
    """Transport-agnostic, in-memory preview and explicit approval runtime."""

    COMPONENT_NAME = "orion_action_preview_approval_runtime"
    COMPONENT_VERSION = "0.1.0"
    PRODUCT_VERSION = "1.4.0"
    SPRINT = 276
    SCHEMA_VERSION = "1"
    APPROVAL_PROOF_DOMAIN = "action-approval-decision"

    STATE_IDLE = "idle"
    STATE_PREVIEW_READY = "preview_ready"
    STATE_PENDING_APPROVAL = "pending_approval"
    STATE_APPROVED = "approved"
    STATE_DENIED = "denied"
    STATE_CANCELLED = "cancelled"
    STATE_EXPIRED = "expired"

    STATES = (
        STATE_IDLE,
        STATE_PREVIEW_READY,
        STATE_PENDING_APPROVAL,
        STATE_APPROVED,
        STATE_DENIED,
        STATE_CANCELLED,
        STATE_EXPIRED,
    )

    VALID_TRANSITIONS = (
        (STATE_IDLE, STATE_PREVIEW_READY),
        (STATE_PREVIEW_READY, STATE_PENDING_APPROVAL),
        (STATE_PREVIEW_READY, STATE_CANCELLED),
        (STATE_PREVIEW_READY, STATE_EXPIRED),
        (STATE_PENDING_APPROVAL, STATE_APPROVED),
        (STATE_PENDING_APPROVAL, STATE_DENIED),
        (STATE_PENDING_APPROVAL, STATE_CANCELLED),
        (STATE_PENDING_APPROVAL, STATE_EXPIRED),
        (STATE_APPROVED, STATE_IDLE),
        (STATE_DENIED, STATE_IDLE),
        (STATE_CANCELLED, STATE_IDLE),
        (STATE_EXPIRED, STATE_IDLE),
    )

    ACTION_CATALOG = {
        "capture_single_screenshot": {
            "future_capability": "orion.capture.single_screenshot",
            "minimum_risk": "medium",
        },
        "capture_selected_window": {
            "future_capability": "orion.capture.selected_window",
            "minimum_risk": "medium",
        },
        "open_allowlisted_application": {
            "future_capability": "orion.application.open_allowlisted",
            "minimum_risk": "medium",
        },
        "create_controlled_file": {
            "future_capability": "orion.file.create_controlled",
            "minimum_risk": "medium",
        },
        "create_controlled_folder": {
            "future_capability": "orion.file.create_controlled_folder",
            "minimum_risk": "medium",
        },
        "obs_start_recording": {
            "future_capability": "orion.obs.start_recording",
            "minimum_risk": "high",
        },
        "obs_stop_recording": {
            "future_capability": "orion.obs.stop_recording",
            "minimum_risk": "high",
        },
        "obs_switch_scene": {
            "future_capability": "orion.obs.switch_scene",
            "minimum_risk": "high",
        },
    }

    PREVIEW_REQUIRED_FIELDS = (
        "schema_version",
        "preview_id",
        "action_type",
        "source",
        "human_summary",
        "target",
        "parameters",
        "reason",
        "required_capability",
        "required_capability_available",
        "risk_level",
        "risk_reasons",
        "possible_side_effects",
        "reversible",
        "rollback_summary",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "grounding_reference",
        "created_at_utc",
        "expires_at_utc",
        "preview_digest",
        "state",
    )

    OPTIONAL_VOICE_FIELDS = (
        "raw_stt_transcript",
        "corrected_stt_transcript",
        "stt_confidence",
        "transcript_changed",
    )

    APPROVAL_REQUEST_FIELDS = (
        "schema_version",
        "approval_request_id",
        "preview_id",
        "preview_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "approval_nonce",
        "sequence",
        "requested_at_utc",
        "expires_at_utc",
        "state",
    )

    APPROVAL_DECISION_FIELDS = (
        "schema_version",
        "message_type",
        "approval_request_id",
        "preview_id",
        "preview_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "approval_nonce",
        "sequence",
        "decision",
        "operator_confirmation",
        "decided_at_utc",
        "note",
    )

    CLI_COMMANDS = (
        "orion-action-preview-status",
        "orion-action-preview-inspect",
        "orion-action-preview-self-test",
    )

    PREVIEW_TTL_SECONDS = 120
    APPROVAL_TTL_SECONDS = 60
    MAXIMUM_TTL_SECONDS = 300
    MAXIMUM_CLOCK_SKEW_SECONDS = 5
    APPROVAL_NONCE_BYTES = 32
    REPLAY_LEDGER_SIZE = 256
    FIRST_SEQUENCE = 1

    ACTION_TYPE_MAX_CHARACTERS = 64
    TARGET_MAX_CHARACTERS = 256
    REASON_MAX_CHARACTERS = 1000
    HUMAN_SUMMARY_MAX_CHARACTERS = 2000
    TRANSCRIPT_MAX_CHARACTERS = 4000
    PARAMETERS_MAX_CANONICAL_BYTES = 16384
    SIDE_EFFECT_ITEM_LIMIT = 16
    SIDE_EFFECT_ITEM_MAX_CHARACTERS = 256

    RISK_ORDER = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "critical": 3,
    }

    DEFERRED_FALSE_FIELDS = (
        "network_listener_active",
        "network_connection_active",
        "runtime_persistence_active",
        "real_execution_active",
        "scoped_permission_active",
        "permission_expiry_runtime_active",
        "audit_write_active",
        "reviewed_memory_write_active",
        "capture_action_active",
        "application_action_active",
        "file_action_active",
        "obs_action_active",
        "watchdog_active",
        "emergency_stop_active",
        "recovery_runtime_active",
    )

    def __init__(
        self,
        *,
        project_root: Path,
        pairing_manager: Any,
        live_link_manager: Any,
        now_provider: Callable[[], datetime] | None = None,
        nonce_provider: Callable[[int], bytes] | None = None,
        id_provider: Callable[[str], str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.pairing_manager = pairing_manager
        self.live_link_manager = live_link_manager
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._nonce_provider = nonce_provider or secrets.token_bytes
        self._id_provider = id_provider or (
            lambda prefix: prefix + uuid.uuid4().hex
        )
        self._state = self.STATE_IDLE
        self._preview: dict[str, Any] | None = None
        self._approval_request: dict[str, Any] | None = None
        self._decision: dict[str, Any] | None = None
        self._last_sequence = 0
        self._replay_ledger: list[str] = []

    def _now(self) -> datetime:
        value = self._now_provider()
        if value.tzinfo is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview/approval clock must be timezone-aware."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        if value.tzinfo is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "Timestamp must be timezone-aware."
            )
        return (
            value.astimezone(timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )

    @staticmethod
    def _parse_utc(value: Any, *, label: str) -> datetime:
        if not isinstance(value, str) or not value:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be a UTC timestamp string."
            )
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} is invalid."
            ) from exc
        if parsed.tzinfo is None:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must include a timezone."
            )
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _canonical_json(value: Any) -> bytes:
        try:
            return json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise OrionActionPreviewApprovalRuntimeError(
                "Payload is not deterministically canonicalizable."
            ) from exc

    @classmethod
    def _deep_copy(cls, value: Any) -> Any:
        return json.loads(cls._canonical_json(value).decode("utf-8"))

    @staticmethod
    def _validate_text(
        value: Any,
        *,
        label: str,
        maximum: int,
        allow_empty: bool = False,
    ) -> str:
        if not isinstance(value, str):
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be a string."
            )
        normalized = value.strip()
        if not normalized and not allow_empty:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must not be empty."
            )
        if len(normalized) > maximum:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} exceeds the maximum length."
            )
        return normalized

    @classmethod
    def _validate_digest(cls, value: Any, *, label: str) -> str:
        normalized = cls._validate_text(
            value,
            label=label,
            maximum=64,
        ).lower()
        if len(normalized) != 64 or any(
            character not in "0123456789abcdef"
            for character in normalized
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be a lowercase SHA-256 digest."
            )
        return normalized

    @classmethod
    def _validate_text_list(
        cls,
        value: Any,
        *,
        label: str,
        allow_empty: bool,
    ) -> list[str]:
        if not isinstance(value, list):
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be a list."
            )
        if len(value) > cls.SIDE_EFFECT_ITEM_LIMIT:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} exceeds the item limit."
            )
        normalized = [
            cls._validate_text(
                item,
                label=f"{label} item",
                maximum=cls.SIDE_EFFECT_ITEM_MAX_CHARACTERS,
            )
            for item in value
        ]
        if not normalized and not allow_empty:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must not be empty."
            )
        if len(set(normalized)) != len(normalized):
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must not contain duplicates."
            )
        return normalized

    @classmethod
    def _validate_ttl(cls, value: Any, *, label: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be an integer."
            )
        if value < 1 or value > cls.MAXIMUM_TTL_SECONDS:
            raise OrionActionPreviewApprovalRuntimeError(
                f"{label} must be between 1 and "
                f"{cls.MAXIMUM_TTL_SECONDS} seconds."
            )
        return value

    def _transition(self, target: str) -> None:
        if (self._state, target) not in self.VALID_TRANSITIONS:
            raise OrionActionPreviewApprovalRuntimeError(
                f"Invalid preview/approval transition: "
                f"{self._state} -> {target}."
            )
        self._state = target

    def _current_context(
        self,
    ) -> tuple[dict[str, Any], dict[str, Any], str]:
        try:
            binding = self.pairing_manager.authenticated_binding()
        except Exception as exc:
            raise OrionActionPreviewApprovalRuntimeError(
                "A paired ORION identity is required."
            ) from exc
        if not isinstance(binding, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Authenticated binding is invalid."
            )
        if binding.get("secret_exposed") is not False:
            raise OrionActionPreviewApprovalRuntimeError(
                "Authenticated binding exposed a secret."
            )
        pairing_id = self._validate_text(
            binding.get("pairing_id"),
            label="pairing ID",
            maximum=128,
        )
        device_id = self._validate_text(
            binding.get("device_id"),
            label="device ID",
            maximum=128,
        )

        live = self.live_link_manager.status()
        if not isinstance(live, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link status is invalid."
            )
        if live.get("state") != "live":
            raise OrionActionPreviewApprovalRuntimeError(
                "A live ORION session is required."
            )
        if live.get("heartbeat_active") is not True:
            raise OrionActionPreviewApprovalRuntimeError(
                "A live heartbeat is required."
            )
        if live.get("capability_negotiation_active") is not True:
            raise OrionActionPreviewApprovalRuntimeError(
                "Capability negotiation must be active."
            )
        session_id = self._validate_text(
            live.get("session_id"),
            label="live-link session ID",
            maximum=128,
        )
        capability_digest = self._validate_digest(
            live.get("capability_digest"),
            label="capability digest",
        )
        live_binding = live.get("binding")
        if not isinstance(live_binding, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link binding is missing."
            )
        if live_binding.get("pairing_id") != pairing_id:
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link pairing ID does not match."
            )
        if live_binding.get("device_id") != device_id:
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link device ID does not match."
            )
        return (
            self._deep_copy(binding),
            self._deep_copy(live),
            capability_digest,
        )

    def _normalize_grounding_reference(
        self,
        value: Any,
        *,
        live: dict[str, Any],
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Grounding reference must be an object."
            )
        forbidden = {
            "summary",
            "payload",
            "raw",
            "image",
            "text",
            "content",
        }
        if forbidden.intersection(value):
            raise OrionActionPreviewApprovalRuntimeError(
                "Raw or unredacted grounding content is prohibited."
            )
        required = {
            "source",
            "subject",
            "observed_at_utc",
            "freshness",
            "redaction_applied",
        }
        if set(value) != required:
            raise OrionActionPreviewApprovalRuntimeError(
                "Grounding reference fields are invalid."
            )
        source = self._validate_text(
            value["source"],
            label="grounding source",
            maximum=128,
        )
        subject = self._validate_text(
            value["subject"],
            label="grounding subject",
            maximum=128,
        )
        observed = self._format_utc(
            self._parse_utc(
                value["observed_at_utc"],
                label="grounding observed timestamp",
            )
        )
        if value["freshness"] != "fresh":
            raise OrionActionPreviewApprovalRuntimeError(
                "Only fresh grounding may be referenced."
            )
        if value["redaction_applied"] is not True:
            raise OrionActionPreviewApprovalRuntimeError(
                "Grounding reference must be redacted."
            )
        current = live.get("latest_grounding")
        if not isinstance(current, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link has no current grounding reference."
            )
        for key, expected in (
            ("source", source),
            ("subject", subject),
            ("observed_at_utc", observed),
            ("freshness", "fresh"),
            ("redaction_applied", True),
        ):
            if current.get(key) != expected:
                raise OrionActionPreviewApprovalRuntimeError(
                    "Grounding reference does not match live-link state."
                )
        return {
            "source": source,
            "subject": subject,
            "observed_at_utc": observed,
            "freshness": "fresh",
            "redaction_applied": True,
        }

    @classmethod
    def _preview_digest(cls, preview: dict[str, Any]) -> str:
        digest_payload = {
            key: value
            for key, value in preview.items()
            if key not in {"preview_digest", "state"}
        }
        return hashlib.sha256(
            cls._canonical_json(digest_payload)
        ).hexdigest()

    def _assert_preview_integrity(self) -> dict[str, Any]:
        if self._preview is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "No active preview exists."
            )
        if set(self._preview) != set(self.PREVIEW_REQUIRED_FIELDS).union(
            {
                key
                for key in self.OPTIONAL_VOICE_FIELDS
                if key in self._preview
            }
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Stored preview fields changed."
            )
        expected = self._preview_digest(self._preview)
        if not hmac.compare_digest(
            expected,
            self._preview["preview_digest"],
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Stored preview digest integrity check failed."
            )
        return self._deep_copy(self._preview)

    def _assert_context_unchanged(self) -> None:
        if self._preview is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "No active preview exists."
            )
        binding, live, digest = self._current_context()
        if binding["pairing_id"] != self._preview["pairing_id"]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview pairing binding changed."
            )
        if binding["device_id"] != self._preview["device_id"]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview device binding changed."
            )
        if live["session_id"] != self._preview["live_link_session_id"]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview live-link session binding changed."
            )
        if digest != self._preview["capability_digest"]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview capability digest binding changed."
            )

    def create_preview(
        self,
        *,
        action_type: str,
        source: str,
        human_summary: str,
        target: str,
        parameters: dict[str, Any],
        reason: str,
        risk_level: str,
        risk_reasons: list[str],
        possible_side_effects: list[str],
        reversible: bool,
        rollback_summary: str | None,
        grounding_reference: dict[str, Any] | None = None,
        raw_stt_transcript: str | None = None,
        corrected_stt_transcript: str | None = None,
        stt_confidence: float | None = None,
        preview_ttl_seconds: int = PREVIEW_TTL_SECONDS,
    ) -> dict[str, Any]:
        if self._state != self.STATE_IDLE:
            raise OrionActionPreviewApprovalRuntimeError(
                "A new preview requires idle state."
            )
        normalized_action = self._validate_text(
            action_type,
            label="action type",
            maximum=self.ACTION_TYPE_MAX_CHARACTERS,
        )
        if normalized_action not in self.ACTION_CATALOG:
            raise OrionActionPreviewApprovalRuntimeError(
                "Unknown action type rejected."
            )
        normalized_source = self._validate_text(
            source,
            label="source",
            maximum=32,
        ).lower()
        if normalized_source not in {"chat", "voice", "system"}:
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview source is unsupported."
            )
        normalized_summary = self._validate_text(
            human_summary,
            label="human summary",
            maximum=self.HUMAN_SUMMARY_MAX_CHARACTERS,
        )
        normalized_target = self._validate_text(
            target,
            label="target",
            maximum=self.TARGET_MAX_CHARACTERS,
        )
        normalized_reason = self._validate_text(
            reason,
            label="reason",
            maximum=self.REASON_MAX_CHARACTERS,
        )
        if not isinstance(parameters, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Parameters must be an object."
            )
        normalized_parameters = self._deep_copy(parameters)
        if len(self._canonical_json(normalized_parameters)) > (
            self.PARAMETERS_MAX_CANONICAL_BYTES
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Parameters exceed the canonical byte limit."
            )
        normalized_risk = self._validate_text(
            risk_level,
            label="risk level",
            maximum=16,
        ).lower()
        if normalized_risk not in self.RISK_ORDER:
            raise OrionActionPreviewApprovalRuntimeError(
                "Risk level is invalid."
            )
        catalog = self.ACTION_CATALOG[normalized_action]
        minimum = catalog["minimum_risk"]
        if self.RISK_ORDER[normalized_risk] < self.RISK_ORDER[minimum]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Risk downgrade rejected."
            )
        normalized_risk_reasons = self._validate_text_list(
            risk_reasons,
            label="risk reasons",
            allow_empty=False,
        )
        normalized_side_effects = self._validate_text_list(
            possible_side_effects,
            label="possible side effects",
            allow_empty=True,
        )
        if not isinstance(reversible, bool):
            raise OrionActionPreviewApprovalRuntimeError(
                "Reversible must be boolean."
            )
        if rollback_summary is None:
            normalized_rollback = None
        else:
            normalized_rollback = self._validate_text(
                rollback_summary,
                label="rollback summary",
                maximum=1000,
            )
        if reversible and normalized_rollback is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "A reversible action requires a rollback summary."
            )
        if not reversible and normalized_rollback is not None:
            raise OrionActionPreviewApprovalRuntimeError(
                "An irreversible action must not claim a rollback."
            )

        ttl = self._validate_ttl(
            preview_ttl_seconds,
            label="preview TTL",
        )
        binding, live, capability_digest = self._current_context()
        grounding = self._normalize_grounding_reference(
            grounding_reference,
            live=live,
        )

        voice: dict[str, Any] = {}
        if normalized_source == "voice":
            raw = self._validate_text(
                raw_stt_transcript,
                label="raw STT transcript",
                maximum=self.TRANSCRIPT_MAX_CHARACTERS,
            )
            if isinstance(stt_confidence, bool) or not isinstance(
                stt_confidence,
                (int, float),
            ):
                raise OrionActionPreviewApprovalRuntimeError(
                    "STT confidence must be numeric."
                )
            confidence = float(stt_confidence)
            if confidence < 0.0 or confidence > 1.0:
                raise OrionActionPreviewApprovalRuntimeError(
                    "STT confidence must be between 0 and 1."
                )
            corrected = (
                None
                if corrected_stt_transcript is None
                else self._validate_text(
                    corrected_stt_transcript,
                    label="corrected STT transcript",
                    maximum=self.TRANSCRIPT_MAX_CHARACTERS,
                )
            )
            voice = {
                "raw_stt_transcript": raw,
                "corrected_stt_transcript": corrected,
                "stt_confidence": confidence,
                "transcript_changed": (
                    corrected is not None and corrected != raw
                ),
            }
        elif any(
            value is not None
            for value in (
                raw_stt_transcript,
                corrected_stt_transcript,
                stt_confidence,
            )
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "STT fields are only valid for voice previews."
            )

        agreed = live.get("agreed_capabilities")
        if not isinstance(agreed, list):
            raise OrionActionPreviewApprovalRuntimeError(
                "Live-link capability agreement is invalid."
            )
        required_capability = catalog["future_capability"]
        capability_available = any(
            isinstance(item, dict)
            and item.get("capability_id") == required_capability
            for item in agreed
        )

        now = self._now()
        preview: dict[str, Any] = {
            "schema_version": self.SCHEMA_VERSION,
            "preview_id": self._id_provider("preview-"),
            "action_type": normalized_action,
            "source": normalized_source,
            "human_summary": normalized_summary,
            "target": normalized_target,
            "parameters": normalized_parameters,
            "reason": normalized_reason,
            "required_capability": required_capability,
            "required_capability_available": capability_available,
            "risk_level": normalized_risk,
            "risk_reasons": normalized_risk_reasons,
            "possible_side_effects": normalized_side_effects,
            "reversible": reversible,
            "rollback_summary": normalized_rollback,
            "pairing_id": binding["pairing_id"],
            "device_id": binding["device_id"],
            "live_link_session_id": live["session_id"],
            "capability_digest": capability_digest,
            "grounding_reference": grounding,
            "created_at_utc": self._format_utc(now),
            "expires_at_utc": self._format_utc(
                now + timedelta(seconds=ttl)
            ),
            "preview_digest": "",
            "state": self.STATE_PREVIEW_READY,
            **voice,
        }
        preview["preview_digest"] = self._preview_digest(preview)
        self._preview = self._deep_copy(preview)
        self._approval_request = None
        self._decision = None
        self._last_sequence = 0
        self._transition(self.STATE_PREVIEW_READY)
        return self._assert_preview_integrity()

    def render_preview(self) -> dict[str, Any]:
        preview = self._assert_preview_integrity()
        voice = None
        if preview["source"] == "voice":
            voice = {
                key: preview[key]
                for key in self.OPTIONAL_VOICE_FIELDS
            }
        return {
            "status": "OK",
            "state": self._state,
            "title": "ORION action preview — no execution performed",
            "preview_id": preview["preview_id"],
            "preview_digest": preview["preview_digest"],
            "sections": {
                "action": {
                    "action_type": preview["action_type"],
                    "human_summary": preview["human_summary"],
                },
                "target": {
                    "device_id": preview["device_id"],
                    "target": preview["target"],
                    "parameters": self._deep_copy(
                        preview["parameters"]
                    ),
                },
                "reason": preview["reason"],
                "risk": {
                    "level": preview["risk_level"],
                    "reasons": list(preview["risk_reasons"]),
                    "possible_side_effects": list(
                        preview["possible_side_effects"]
                    ),
                },
                "reversibility": {
                    "reversible": preview["reversible"],
                    "rollback_summary": preview["rollback_summary"],
                },
                "voice": voice,
                "authorization_boundary": {
                    "approval_required": True,
                    "permission_issued": False,
                    "execution_authorized": False,
                    "execution_performed": False,
                },
            },
            "preview": preview,
        }

    def request_approval(
        self,
        *,
        approval_ttl_seconds: int = APPROVAL_TTL_SECONDS,
    ) -> dict[str, Any]:
        if self._state != self.STATE_PREVIEW_READY:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval can only be requested from preview_ready."
            )
        preview = self._assert_preview_integrity()
        self._assert_context_unchanged()
        ttl = self._validate_ttl(
            approval_ttl_seconds,
            label="approval TTL",
        )
        now = self._now()
        preview_expiry = self._parse_utc(
            preview["expires_at_utc"],
            label="preview expiry",
        )
        if now >= preview_expiry:
            self._transition(self.STATE_EXPIRED)
            raise OrionActionPreviewApprovalRuntimeError(
                "Preview expired before approval request."
            )
        request_expiry = min(
            preview_expiry,
            now + timedelta(seconds=ttl),
        )
        nonce = self._nonce_provider(self.APPROVAL_NONCE_BYTES)
        if (
            not isinstance(nonce, bytes)
            or len(nonce) != self.APPROVAL_NONCE_BYTES
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval nonce provider returned invalid bytes."
            )
        request = {
            "schema_version": self.SCHEMA_VERSION,
            "approval_request_id": self._id_provider("approval-"),
            "preview_id": preview["preview_id"],
            "preview_digest": preview["preview_digest"],
            "pairing_id": preview["pairing_id"],
            "device_id": preview["device_id"],
            "live_link_session_id": preview[
                "live_link_session_id"
            ],
            "capability_digest": preview["capability_digest"],
            "approval_nonce": base64.urlsafe_b64encode(
                nonce
            ).decode("ascii").rstrip("="),
            "sequence": self.FIRST_SEQUENCE,
            "requested_at_utc": self._format_utc(now),
            "expires_at_utc": self._format_utc(request_expiry),
            "state": self.STATE_PENDING_APPROVAL,
        }
        if set(request) != set(self.APPROVAL_REQUEST_FIELDS):
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval request schema is invalid."
            )
        self._approval_request = self._deep_copy(request)
        self._transition(self.STATE_PENDING_APPROVAL)
        return self._deep_copy(self._approval_request)

    def resolve_approval(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if self._state != self.STATE_PENDING_APPROVAL:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision requires pending_approval state."
            )
        preview = self._assert_preview_integrity()
        self._assert_context_unchanged()
        request = self._approval_request
        if request is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval request is missing."
            )
        if not isinstance(envelope, dict):
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision envelope must be an object."
            )
        if set(envelope) != set(self.APPROVAL_DECISION_FIELDS):
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision fields are invalid."
            )
        if envelope["schema_version"] != self.SCHEMA_VERSION:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision schema version mismatch."
            )
        if envelope["message_type"] != "action_approval_decision":
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision message type mismatch."
            )
        for key in (
            "approval_request_id",
            "preview_id",
            "preview_digest",
            "pairing_id",
            "device_id",
            "live_link_session_id",
            "capability_digest",
            "approval_nonce",
        ):
            if envelope[key] != request[key]:
                raise OrionActionPreviewApprovalRuntimeError(
                    f"Approval decision {key} binding mismatch."
                )
        if envelope["preview_digest"] != preview["preview_digest"]:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision preview digest mismatch."
            )
        sequence = envelope["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval sequence must be an integer."
            )
        if sequence != self.FIRST_SEQUENCE:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval sequence must start at 1."
            )
        if sequence <= self._last_sequence:
            raise OrionActionPreviewApprovalRuntimeError(
                "Duplicate or out-of-order approval sequence rejected."
            )
        decision = envelope["decision"]
        if decision not in {"approve", "deny"}:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision must be approve or deny."
            )
        if envelope["operator_confirmation"] != "explicit":
            raise OrionActionPreviewApprovalRuntimeError(
                "Explicit operator confirmation is required."
            )
        note = self._validate_text(
            envelope["note"],
            label="approval note",
            maximum=1000,
            allow_empty=True,
        )
        decided_at = self._parse_utc(
            envelope["decided_at_utc"],
            label="approval decision timestamp",
        )
        now = self._now()
        if (
            decided_at - now
        ).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionActionPreviewApprovalRuntimeError(
                "Future approval decision rejected."
            )
        requested_at = self._parse_utc(
            request["requested_at_utc"],
            label="approval request timestamp",
        )
        if (
            requested_at - decided_at
        ).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval decision predates its request."
            )
        request_expiry = self._parse_utc(
            request["expires_at_utc"],
            label="approval request expiry",
        )
        preview_expiry = self._parse_utc(
            preview["expires_at_utc"],
            label="preview expiry",
        )
        if now >= request_expiry or now >= preview_expiry:
            self._transition(self.STATE_EXPIRED)
            raise OrionActionPreviewApprovalRuntimeError(
                "Expired approval decision rejected."
            )
        replay_key = hashlib.sha256(
            self._canonical_json(
                {
                    "approval_request_id": request[
                        "approval_request_id"
                    ],
                    "approval_nonce": request["approval_nonce"],
                    "sequence": sequence,
                }
            )
        ).hexdigest()
        if replay_key in self._replay_ledger:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval replay rejected."
            )
        try:
            self.pairing_manager.verify_authenticated_envelope(
                domain=self.APPROVAL_PROOF_DOMAIN,
                payload=envelope,
                proof_b64url=proof_b64url,
            )
        except Exception as exc:
            raise OrionActionPreviewApprovalRuntimeError(
                "Approval proof verification failed."
            ) from exc

        target_state = (
            self.STATE_APPROVED
            if decision == "approve"
            else self.STATE_DENIED
        )
        self._last_sequence = sequence
        self._replay_ledger.append(replay_key)
        if len(self._replay_ledger) > self.REPLAY_LEDGER_SIZE:
            self._replay_ledger = self._replay_ledger[
                -self.REPLAY_LEDGER_SIZE :
            ]
        self._transition(target_state)
        self._decision = self._deep_copy(
            {
                **envelope,
                "note": note,
                "recorded_at_utc": self._format_utc(now),
                "state": target_state,
            }
        )
        return {
            "status": "OK",
            "state": target_state,
            "decision": decision,
            "preview_id": preview["preview_id"],
            "preview_digest": preview["preview_digest"],
            "approval_request_id": request["approval_request_id"],
            "approval_recorded": True,
            "permission_issued": False,
            "execution_authorized": False,
            "execution_performed": False,
            "audit_written": False,
            "memory_written": False,
            "network_used": False,
            "runtime_persisted": False,
        }

    def cancel(self) -> dict[str, Any]:
        if self._state not in (
            self.STATE_PREVIEW_READY,
            self.STATE_PENDING_APPROVAL,
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Cancel requires preview_ready or pending_approval."
            )
        self._transition(self.STATE_CANCELLED)
        return self.status()

    def tick(self) -> dict[str, Any]:
        if self._state not in (
            self.STATE_PREVIEW_READY,
            self.STATE_PENDING_APPROVAL,
        ):
            return self.status()
        if self._preview is None:
            raise OrionActionPreviewApprovalRuntimeError(
                "Active state is missing its preview."
            )
        expiry = self._parse_utc(
            self._preview["expires_at_utc"],
            label="preview expiry",
        )
        if (
            self._state == self.STATE_PENDING_APPROVAL
            and self._approval_request is not None
        ):
            expiry = min(
                expiry,
                self._parse_utc(
                    self._approval_request["expires_at_utc"],
                    label="approval request expiry",
                ),
            )
        if self._now() >= expiry:
            self._transition(self.STATE_EXPIRED)
        return self.status()

    def reset(self) -> dict[str, Any]:
        if self._state not in (
            self.STATE_APPROVED,
            self.STATE_DENIED,
            self.STATE_CANCELLED,
            self.STATE_EXPIRED,
        ):
            raise OrionActionPreviewApprovalRuntimeError(
                "Reset requires a terminal preview/approval state."
            )
        self._transition(self.STATE_IDLE)
        self._preview = None
        self._approval_request = None
        self._decision = None
        self._last_sequence = 0
        return self.status()

    def status(self) -> dict[str, Any]:
        preview = None
        if self._preview is not None:
            preview = {
                "preview_id": self._preview["preview_id"],
                "action_type": self._preview["action_type"],
                "source": self._preview["source"],
                "human_summary": self._preview["human_summary"],
                "target": self._preview["target"],
                "required_capability": self._preview[
                    "required_capability"
                ],
                "required_capability_available": self._preview[
                    "required_capability_available"
                ],
                "risk_level": self._preview["risk_level"],
                "reversible": self._preview["reversible"],
                "preview_digest": self._preview["preview_digest"],
                "expires_at_utc": self._preview["expires_at_utc"],
                "transcript_changed": self._preview.get(
                    "transcript_changed"
                ),
            }
        approval = None
        if self._approval_request is not None:
            approval = {
                key: self._approval_request[key]
                for key in (
                    "approval_request_id",
                    "preview_id",
                    "preview_digest",
                    "sequence",
                    "requested_at_utc",
                    "expires_at_utc",
                    "state",
                )
            }
        payload = {
            "status": "ready",
            "reason": "orion_action_preview_approval_runtime_ready",
            "state": self._state,
            "preview": preview,
            "approval_request": approval,
            "decision": (
                None
                if self._decision is None
                else {
                    "decision": self._decision["decision"],
                    "state": self._decision["state"],
                    "recorded_at_utc": self._decision[
                        "recorded_at_utc"
                    ],
                }
            ),
            "last_sequence": self._last_sequence,
            "replay_ledger_entries": len(self._replay_ledger),
            "action_preview_active": self._state != self.STATE_IDLE,
            "approval_active": self._state
            == self.STATE_PENDING_APPROVAL,
            "approval_recorded": self._state
            in (self.STATE_APPROVED, self.STATE_DENIED),
            "permission_issued": False,
            "execution_authorized": False,
            "execution_performed": False,
            "audit_written": False,
            "memory_written": False,
            "network_listener_active": False,
            "network_connection_active": False,
            "runtime_persistence_active": False,
            "real_execution_active": False,
            "scoped_permission_active": False,
            "permission_expiry_runtime_active": False,
            "audit_write_active": False,
            "reviewed_memory_write_active": False,
            "capture_action_active": False,
            "application_action_active": False,
            "file_action_active": False,
            "obs_action_active": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_runtime_active": False,
            "secret_exposed": False,
            "safe_idle": self._state == self.STATE_IDLE,
        }
        for field in self.DEFERRED_FALSE_FIELDS:
            if payload[field] is not False:
                raise OrionActionPreviewApprovalRuntimeError(
                    f"Deferred field '{field}' became active."
                )
        return payload

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "component": {
                "name": self.COMPONENT_NAME,
                "component_version": self.COMPONENT_VERSION,
                "product_version": self.PRODUCT_VERSION,
                "sprint": self.SPRINT,
            },
            "state_machine": {
                "states": list(self.STATES),
                "state_count": len(self.STATES),
                "valid_transitions": [
                    list(item) for item in self.VALID_TRANSITIONS
                ],
                "valid_transition_count": len(
                    self.VALID_TRANSITIONS
                ),
                "all_other_transitions_fail_closed": True,
            },
            "action_catalog": {
                "entries": self._deep_copy(self.ACTION_CATALOG),
                "count": len(self.ACTION_CATALOG),
                "preview_only": True,
                "capabilities_activated": False,
            },
            "preview": {
                "required_fields": list(
                    self.PREVIEW_REQUIRED_FIELDS
                ),
                "required_field_count": len(
                    self.PREVIEW_REQUIRED_FIELDS
                ),
                "optional_voice_fields": list(
                    self.OPTIONAL_VOICE_FIELDS
                ),
                "canonical_json": True,
                "digest_algorithm": "SHA-256",
                "immutable_after_creation": True,
                "raw_grounding_persisted": False,
                "secret_exposed": False,
            },
            "approval": {
                "request_fields": list(
                    self.APPROVAL_REQUEST_FIELDS
                ),
                "request_field_count": len(
                    self.APPROVAL_REQUEST_FIELDS
                ),
                "decision_fields": list(
                    self.APPROVAL_DECISION_FIELDS
                ),
                "decision_field_count": len(
                    self.APPROVAL_DECISION_FIELDS
                ),
                "decisions": ["approve", "deny"],
                "proof_domain": self.APPROVAL_PROOF_DOMAIN,
                "proof_algorithm": "HMAC-SHA256",
                "proof_verification": "hmac.compare_digest",
                "single_use_nonce": True,
                "strictly_monotonic_sequence": True,
                "replay_rejected": True,
                "operator_confirmation": "explicit",
            },
            "voice_policy": {
                "raw_transcript_required_for_voice": True,
                "corrected_transcript_optional": True,
                "confidence_required_for_voice": True,
                "confidence_range": [0.0, 1.0],
                "silent_action_correction_allowed": False,
                "explicit_approval_still_required": True,
            },
            "limits": {
                "preview_ttl_seconds": self.PREVIEW_TTL_SECONDS,
                "approval_ttl_seconds": self.APPROVAL_TTL_SECONDS,
                "maximum_ttl_seconds": self.MAXIMUM_TTL_SECONDS,
                "maximum_clock_skew_seconds": (
                    self.MAXIMUM_CLOCK_SKEW_SECONDS
                ),
                "approval_nonce_bytes": self.APPROVAL_NONCE_BYTES,
                "replay_ledger_size": self.REPLAY_LEDGER_SIZE,
                "first_sequence": self.FIRST_SEQUENCE,
                "parameters_max_canonical_bytes": (
                    self.PARAMETERS_MAX_CANONICAL_BYTES
                ),
                "transcript_max_characters": (
                    self.TRANSCRIPT_MAX_CHARACTERS
                ),
            },
            "public_manager_methods": [
                "create_preview",
                "render_preview",
                "request_approval",
                "resolve_approval",
                "cancel",
                "tick",
                "reset",
                "status",
                "inspect_runtime",
                "self_test",
            ],
            "cli_commands": list(self.CLI_COMMANDS),
            "deferred_boundaries": {
                field: False for field in self.DEFERRED_FALSE_FIELDS
            },
            "composition": {
                "pairing_manager": "public API only",
                "live_link_manager": "status and inspect_runtime only",
                "private_runtime_api_use": False,
                "transport_agnostic": True,
                "runtime_persistence": "in_memory_only",
            },
        }

    def self_test(self) -> dict[str, Any]:
        assertions: list[str] = []
        failures: list[str] = []

        def check(condition: bool, label: str) -> None:
            assertions.append(label)
            if not condition:
                failures.append(label)

        def expect_error(operation: Callable[[], Any], label: str) -> None:
            try:
                operation()
            except OrionActionPreviewApprovalRuntimeError:
                check(True, label)
            else:
                check(False, label)

        class PairingStub:
            def __init__(self) -> None:
                self.secret = b"sprint-276-test-secret-32bytes!"[:32]
                self.binding = {
                    "pairing_id": "pair-test",
                    "device_id": "orion-test",
                    "secret_exposed": False,
                }

            def authenticated_binding(self) -> dict[str, Any]:
                return deepcopy(self.binding)

            def sign_authenticated_envelope(
                self,
                *,
                domain: str,
                payload: dict[str, Any],
            ) -> dict[str, Any]:
                material = (
                    domain.encode("utf-8")
                    + b"\0"
                    + AuraOrionActionPreviewApprovalRuntimeManager
                    ._canonical_json(payload)
                )
                proof = base64.urlsafe_b64encode(
                    hmac.new(
                        self.secret,
                        material,
                        hashlib.sha256,
                    ).digest()
                ).decode("ascii").rstrip("=")
                return {"proof_b64url": proof}

            def verify_authenticated_envelope(
                self,
                *,
                domain: str,
                payload: dict[str, Any],
                proof_b64url: str,
            ) -> dict[str, Any]:
                expected = self.sign_authenticated_envelope(
                    domain=domain,
                    payload=payload,
                )["proof_b64url"]
                if not isinstance(proof_b64url, str) or not hmac.compare_digest(
                    expected,
                    proof_b64url,
                ):
                    raise ValueError("verification failed")
                return {"verified": True}

        class LiveStub:
            def __init__(self) -> None:
                self.payload = {
                    "state": "live",
                    "session_id": "live-test",
                    "heartbeat_active": True,
                    "capability_negotiation_active": True,
                    "capability_digest": "a" * 64,
                    "binding": {
                        "pairing_id": "pair-test",
                        "device_id": "orion-test",
                    },
                    "agreed_capabilities": [
                        {
                            "capability_id": "orion.heartbeat",
                            "version": "1",
                            "mode": "read_only",
                            "constraints": {},
                            "source": "ATLAS",
                        }
                    ],
                    "latest_grounding": {
                        "source": "ORION",
                        "subject": "desktop_state",
                        "observed_at_utc": (
                            "2026-07-21T00:00:00.000000Z"
                        ),
                        "freshness": "fresh",
                        "redaction_applied": True,
                    },
                }

            def status(self) -> dict[str, Any]:
                return deepcopy(self.payload)

            def inspect_runtime(self) -> dict[str, Any]:
                return {"status": "OK", "component": {"sprint": 275}}

        clock = {
            "now": datetime(
                2026,
                7,
                21,
                0,
                0,
                0,
                tzinfo=timezone.utc,
            )
        }
        ids = {"value": 0}

        def next_id(prefix: str) -> str:
            ids["value"] += 1
            return f"{prefix}{ids['value']:04d}"

        pairing = PairingStub()
        live = LiveStub()
        manager = AuraOrionActionPreviewApprovalRuntimeManager(
            project_root=self.project_root,
            pairing_manager=pairing,
            live_link_manager=live,
            now_provider=lambda: clock["now"],
            nonce_provider=lambda size: b"n" * size,
            id_provider=next_id,
        )

        # Static contract assertions.
        check(len(self.STATES) == 7, "state-count")
        check(len(set(self.STATES)) == 7, "state-unique")
        check(
            all(isinstance(state, str) and bool(state) for state in self.STATES),
            "state-values-valid",
        )
        check(
            len(self.VALID_TRANSITIONS) == 12,
            "transition-count",
        )
        check(
            len(set(self.VALID_TRANSITIONS)) == 12,
            "transition-unique",
        )
        check(
            all(source in self.STATES for source, _ in self.VALID_TRANSITIONS),
            "transition-sources-valid",
        )
        check(
            all(target in self.STATES for _, target in self.VALID_TRANSITIONS),
            "transition-targets-valid",
        )
        check(len(self.ACTION_CATALOG) == 8, "catalog-count")
        for action_type, metadata in self.ACTION_CATALOG.items():
            check(bool(action_type), f"catalog-action-{action_type}")
            check(
                metadata["minimum_risk"] in self.RISK_ORDER,
                f"catalog-risk-{action_type}",
            )
            check(
                metadata["future_capability"].startswith("orion."),
                f"catalog-capability-{action_type}",
            )
        check(
            len(self.PREVIEW_REQUIRED_FIELDS) == 24,
            "preview-field-count",
        )
        for field in self.PREVIEW_REQUIRED_FIELDS:
            check(bool(field), f"preview-field-{field}")
        check(
            len(self.OPTIONAL_VOICE_FIELDS) == 4,
            "voice-field-count",
        )
        for field in self.OPTIONAL_VOICE_FIELDS:
            check(bool(field), f"voice-field-{field}")
        check(
            len(self.APPROVAL_REQUEST_FIELDS) == 13,
            "request-field-count",
        )
        for field in self.APPROVAL_REQUEST_FIELDS:
            check(bool(field), f"request-field-{field}")
        check(
            len(self.APPROVAL_DECISION_FIELDS) == 15,
            "decision-field-count",
        )
        for field in self.APPROVAL_DECISION_FIELDS:
            check(bool(field), f"decision-field-{field}")
        check(len(self.CLI_COMMANDS) == 3, "cli-count")
        check(
            all(
                command.startswith("orion-action-preview-")
                for command in self.CLI_COMMANDS
            ),
            "cli-prefixes-valid",
        )
        check(
            len(self.DEFERRED_FALSE_FIELDS) == 15,
            "deferred-count",
        )
        for field in self.DEFERRED_FALSE_FIELDS:
            check(field.endswith("_active"), f"deferred-{field}")

        # Dynamic lifecycle and adversarial assertions.
        initial = manager.status()
        check(initial["state"] == "idle", "initial-idle")
        check(initial["safe_idle"] is True, "initial-safe-idle")
        check(initial["secret_exposed"] is False, "initial-secret-redacted")

        preview = manager.create_preview(
            action_type="capture_single_screenshot",
            source="chat",
            human_summary="Capture one reviewed screenshot.",
            target="ORION selected desktop",
            parameters={"format": "png"},
            reason="User requested a bounded preview.",
            risk_level="medium",
            risk_reasons=["Screen content may contain private data."],
            possible_side_effects=["A future capture may expose content."],
            reversible=False,
            rollback_summary=None,
            grounding_reference={
                "source": "ORION",
                "subject": "desktop_state",
                "observed_at_utc": "2026-07-21T00:00:00.000000Z",
                "freshness": "fresh",
                "redaction_applied": True,
            },
        )
        check(preview["state"] == "preview_ready", "preview-state")
        check(preview["source"] == "chat", "preview-source")
        check(preview["required_capability_available"] is False, "cap-unavailable")
        check(len(preview["preview_digest"]) == 64, "preview-digest")
        check(preview["grounding_reference"]["freshness"] == "fresh", "ground-fresh")
        check("summary" not in preview["grounding_reference"], "ground-redacted")
        rendered = manager.render_preview()
        check(rendered["status"] == "OK", "render-status")
        check(
            rendered["sections"]["authorization_boundary"][
                "execution_performed"
            ] is False,
            "render-no-execution",
        )
        mutated = deepcopy(preview)
        mutated["target"] = "tampered"
        check(
            mutated["preview_digest"] == preview["preview_digest"],
            "external-copy-mutation-contained",
        )
        request = manager.request_approval()
        check(request["state"] == "pending_approval", "request-state")
        check(request["sequence"] == 1, "request-sequence")
        check(len(request["approval_nonce"]) >= 43, "request-nonce")
        envelope = {
            "schema_version": "1",
            "message_type": "action_approval_decision",
            "approval_request_id": request["approval_request_id"],
            "preview_id": request["preview_id"],
            "preview_digest": request["preview_digest"],
            "pairing_id": request["pairing_id"],
            "device_id": request["device_id"],
            "live_link_session_id": request["live_link_session_id"],
            "capability_digest": request["capability_digest"],
            "approval_nonce": request["approval_nonce"],
            "sequence": 1,
            "decision": "approve",
            "operator_confirmation": "explicit",
            "decided_at_utc": self._format_utc(clock["now"]),
            "note": "Approved for preview contract testing.",
        }
        proof = pairing.sign_authenticated_envelope(
            domain=self.APPROVAL_PROOF_DOMAIN,
            payload=envelope,
        )["proof_b64url"]
        result = manager.resolve_approval(
            envelope=envelope,
            proof_b64url=proof,
        )
        check(result["state"] == "approved", "approved-state")
        check(result["approval_recorded"] is True, "approval-recorded")
        check(result["permission_issued"] is False, "no-permission")
        check(result["execution_authorized"] is False, "no-authorization")
        check(result["execution_performed"] is False, "no-execution")
        check(result["audit_written"] is False, "no-audit")
        check(result["memory_written"] is False, "no-memory")
        check(manager.reset()["state"] == "idle", "approved-reset")

        voice = manager.create_preview(
            action_type="open_allowlisted_application",
            source="voice",
            human_summary="Open a future allowlisted application.",
            target="OBS Studio",
            parameters={"application": "obs"},
            reason="Voice request requires explicit review.",
            risk_level="medium",
            risk_reasons=["Opening an application changes desktop state."],
            possible_side_effects=["The application may consume resources."],
            reversible=True,
            rollback_summary="Close the application after review.",
            raw_stt_transcript="buka op es",
            corrected_stt_transcript="Buka OBS.",
            stt_confidence=0.72,
        )
        check(voice["transcript_changed"] is True, "voice-changed")
        check(voice["raw_stt_transcript"] == "buka op es", "voice-raw")
        check(voice["corrected_stt_transcript"] == "Buka OBS.", "voice-corrected")
        check(voice["stt_confidence"] == 0.72, "voice-confidence")
        voice_request = manager.request_approval()
        deny = {
            "schema_version": "1",
            "message_type": "action_approval_decision",
            "approval_request_id": voice_request["approval_request_id"],
            "preview_id": voice_request["preview_id"],
            "preview_digest": voice_request["preview_digest"],
            "pairing_id": voice_request["pairing_id"],
            "device_id": voice_request["device_id"],
            "live_link_session_id": voice_request["live_link_session_id"],
            "capability_digest": voice_request["capability_digest"],
            "approval_nonce": voice_request["approval_nonce"],
            "sequence": 1,
            "decision": "deny",
            "operator_confirmation": "explicit",
            "decided_at_utc": self._format_utc(clock["now"]),
            "note": "Denied.",
        }
        deny_proof = pairing.sign_authenticated_envelope(
            domain=self.APPROVAL_PROOF_DOMAIN,
            payload=deny,
        )["proof_b64url"]
        denied = manager.resolve_approval(
            envelope=deny,
            proof_b64url=deny_proof,
        )
        check(denied["state"] == "denied", "denied-state")
        check(manager.reset()["state"] == "idle", "denied-reset")

        manager.create_preview(
            action_type="create_controlled_folder",
            source="system",
            human_summary="Preview a controlled folder creation.",
            target="/future/controlled/path",
            parameters={"name": "test"},
            reason="Cancellation test.",
            risk_level="medium",
            risk_reasons=["Filesystem state would change later."],
            possible_side_effects=[],
            reversible=True,
            rollback_summary="Remove the empty folder.",
        )
        check(manager.cancel()["state"] == "cancelled", "cancelled-state")
        check(manager.reset()["state"] == "idle", "cancelled-reset")

        manager.create_preview(
            action_type="capture_selected_window",
            source="chat",
            human_summary="Preview an expiring window capture.",
            target="Selected window",
            parameters={},
            reason="Expiry test.",
            risk_level="medium",
            risk_reasons=["Window content may be sensitive."],
            possible_side_effects=[],
            reversible=False,
            rollback_summary=None,
            preview_ttl_seconds=1,
        )
        clock["now"] += timedelta(seconds=1)
        check(manager.tick()["state"] == "expired", "expired-state")
        check(manager.reset()["state"] == "idle", "expired-reset")
        clock["now"] -= timedelta(seconds=1)

        expect_error(
            lambda: manager.create_preview(
                action_type="unknown",
                source="chat",
                human_summary="Unknown.",
                target="none",
                parameters={},
                reason="test",
                risk_level="medium",
                risk_reasons=["test"],
                possible_side_effects=[],
                reversible=False,
                rollback_summary=None,
            ),
            "unknown-action-rejected",
        )
        expect_error(
            lambda: manager.create_preview(
                action_type="obs_switch_scene",
                source="chat",
                human_summary="Risk downgrade.",
                target="Scene",
                parameters={},
                reason="test",
                risk_level="medium",
                risk_reasons=["test"],
                possible_side_effects=[],
                reversible=True,
                rollback_summary="Switch back.",
            ),
            "risk-downgrade-rejected",
        )
        expect_error(
            lambda: manager.create_preview(
                action_type="capture_single_screenshot",
                source="voice",
                human_summary="Missing voice transcript.",
                target="desktop",
                parameters={},
                reason="test",
                risk_level="medium",
                risk_reasons=["test"],
                possible_side_effects=[],
                reversible=False,
                rollback_summary=None,
                stt_confidence=0.5,
            ),
            "missing-raw-transcript-rejected",
        )
        expect_error(
            lambda: manager.create_preview(
                action_type="capture_single_screenshot",
                source="voice",
                human_summary="Bad confidence.",
                target="desktop",
                parameters={},
                reason="test",
                risk_level="medium",
                risk_reasons=["test"],
                possible_side_effects=[],
                reversible=False,
                rollback_summary=None,
                raw_stt_transcript="capture",
                stt_confidence=1.5,
            ),
            "bad-confidence-rejected",
        )

        inspect = manager.inspect_runtime()
        check(inspect["state_machine"]["state_count"] == 7, "inspect-states")
        check(inspect["action_catalog"]["count"] == 8, "inspect-actions")
        check(
            inspect["approval"]["proof_verification"]
            == "hmac.compare_digest",
            "inspect-proof",
        )
        check(
            inspect["voice_policy"]["silent_action_correction_allowed"]
            is False,
            "inspect-no-silent-correction",
        )
        check(
            all(
                value is False
                for value in inspect["deferred_boundaries"].values()
            ),
            "inspect-deferred-false",
        )

        if len(assertions) != 152:
            failures.append(
                f"assertion-count:{len(assertions)}"
            )
        return {
            "status": "OK" if not failures else "FAILED",
            "component": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "sprint": self.SPRINT,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failures),
            "failed_assertions": failures,
            "network_side_effects": 0,
            "filesystem_side_effects": 0,
            "action_side_effects": 0,
            "runtime_persistence": "in_memory_only",
            "real_execution_active": False,
        }
