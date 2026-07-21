"""Authenticated ORION heartbeat, capability, and grounding runtime.

Sprint 275 provides a transport-agnostic, in-memory live-link runtime.
Every accepted envelope is bound to the Sprint 274 paired identity and
verified through the pairing runtime's public HMAC API.

This module does not bind a listener, open a connection, write audit or
memory records, preview or approve actions, execute actions, or activate
watchdog/recovery behavior.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from aura.orion_pairing_identity_runtime import (
    AuraOrionPairingIdentityRuntimeManager,
    OrionPairingIdentityRuntimeError,
)


class OrionLiveLinkRuntimeError(RuntimeError):
    """Raised when Sprint 275 live-link validation fails closed."""


@dataclass(frozen=True, slots=True)
class OrionLiveLinkCapability:
    capability_id: str
    version: str
    mode: str
    constraints: dict[str, Any]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class OrionLiveGroundingSnapshot:
    source: str
    subject: str
    summary: str
    confidence: float
    provenance: dict[str, Any]
    redaction_applied: bool
    observed_at_utc: str
    received_at_utc: str
    freshness: str
    capability_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AuraOrionLiveLinkRuntimeManager:
    """Manage authenticated Sprint 275 live-link envelopes in memory."""

    COMPONENT_VERSION = "0.1.0"
    PROTOCOL_VERSION = "aura-orion-live-link-v1"

    STATE_DISCONNECTED = "disconnected"
    STATE_CONNECTING = "connecting"
    STATE_LIVE = "live"
    STATE_STALE = "stale"
    STATE_FAILED = "failed"
    STATES = (
        STATE_DISCONNECTED,
        STATE_CONNECTING,
        STATE_LIVE,
        STATE_STALE,
        STATE_FAILED,
    )

    HEARTBEAT_INTERVAL_SECONDS = 5
    HEARTBEAT_STALE_AFTER_SECONDS = 15
    HEARTBEAT_FAILED_AFTER_SECONDS = 30
    MAX_CLOCK_SKEW_SECONDS = 5

    GROUNDING_FRESH_AFTER_SECONDS = 5
    GROUNDING_STALE_AFTER_SECONDS = 15
    GROUNDING_EXPIRED_AFTER_SECONDS = 30

    MAX_SEQUENCE = 2**63 - 1
    MAX_CAPABILITIES = 64
    MAX_CAPABILITY_ID_LENGTH = 128
    MAX_VERSION_LENGTH = 32
    MAX_MODE_LENGTH = 32
    MAX_CONSTRAINT_BYTES = 16_384
    MAX_GROUNDING_SUMMARY_LENGTH = 4_096
    MAX_PROVENANCE_BYTES = 16_384

    DOMAIN_HEARTBEAT = "orion-live-link.heartbeat"
    DOMAIN_CAPABILITY = "orion-live-link.capability-negotiation"
    DOMAIN_GROUNDING = "orion-live-link.grounding"

    VALID_TRANSITIONS = (
        ("disconnected", "open_authenticated_session", "connecting"),
        ("connecting", "accept_first_heartbeat", "live"),
        ("live", "accept_heartbeat", "live"),
        ("live", "heartbeat_timeout", "stale"),
        ("stale", "accept_fresh_heartbeat", "live"),
        ("stale", "failure_timeout", "failed"),
        ("connecting", "authentication_failure", "failed"),
        ("connecting", "handshake_timeout", "failed"),
        ("live", "close_session", "disconnected"),
        ("stale", "close_session", "disconnected"),
        ("failed", "reset_session", "disconnected"),
    )

    DEFERRED_FALSE_FIELDS = (
        "network_listener_active",
        "network_connection_active",
        "action_preview_active",
        "approval_active",
        "permission_active",
        "audit_write_active",
        "real_action_execution_active",
        "watchdog_active",
        "emergency_stop_active",
        "recovery_active",
    )

    def __init__(
        self,
        project_root: Path,
        *,
        pairing_manager: AuraOrionPairingIdentityRuntimeManager | None = None,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.pairing_manager = pairing_manager or (
            AuraOrionPairingIdentityRuntimeManager(
                project_root=self.project_root
            )
        )
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._state = self.STATE_DISCONNECTED
        self._failure_reason: str | None = None
        self._session_id: str | None = None
        self._binding: dict[str, Any] | None = None
        self._opened_at: datetime | None = None
        self._last_heartbeat_at: datetime | None = None
        self._last_sequence = 0
        self._capability_digest: str | None = None
        self._agreed_capabilities: tuple[
            OrionLiveLinkCapability, ...
        ] = ()
        self._rejected_capabilities: tuple[dict[str, Any], ...] = ()
        self._latest_grounding: OrionLiveGroundingSnapshot | None = None

    def _now(self) -> datetime:
        value = self._now_provider()
        if value.tzinfo is None:
            raise OrionLiveLinkRuntimeError(
                "Live-link clock must be timezone-aware."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        if value.tzinfo is None:
            raise OrionLiveLinkRuntimeError(
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
            raise OrionLiveLinkRuntimeError(
                f"{label} must be a UTC timestamp string."
            )
        normalized = value
        if value.endswith("Z"):
            normalized = value[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise OrionLiveLinkRuntimeError(
                f"{label} is invalid."
            ) from exc
        if parsed.tzinfo is None:
            raise OrionLiveLinkRuntimeError(
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
            raise OrionLiveLinkRuntimeError(
                "Payload is not deterministically canonicalizable."
            ) from exc

    @staticmethod
    def _validate_ascii_token(
        value: Any,
        *,
        label: str,
        max_length: int,
        allowed_extra: str = "._:-",
    ) -> str:
        if not isinstance(value, str):
            raise OrionLiveLinkRuntimeError(
                f"{label} must be a string."
            )
        candidate = value.strip()
        if not candidate or len(candidate) > max_length:
            raise OrionLiveLinkRuntimeError(
                f"{label} has an invalid length."
            )
        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            + allowed_extra
        )
        if any(char not in allowed for char in candidate):
            raise OrionLiveLinkRuntimeError(
                f"{label} contains unsupported characters."
            )
        return candidate

    def _validate_sequence(self, value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise OrionLiveLinkRuntimeError(
                "Envelope sequence must be an integer."
            )
        if value < 1 or value > self.MAX_SEQUENCE:
            raise OrionLiveLinkRuntimeError(
                "Envelope sequence is outside the supported range."
            )
        if value <= self._last_sequence:
            raise OrionLiveLinkRuntimeError(
                "Duplicate or out-of-order envelope sequence rejected."
            )
        return value

    @staticmethod
    def _validate_hex_digest(value: Any, *, label: str) -> str:
        if not isinstance(value, str) or len(value) != 64:
            raise OrionLiveLinkRuntimeError(
                f"{label} must be a SHA-256 hex digest."
            )
        lowered = value.lower()
        if any(char not in "0123456789abcdef" for char in lowered):
            raise OrionLiveLinkRuntimeError(
                f"{label} must be a SHA-256 hex digest."
            )
        return lowered

    def _require_session(self) -> None:
        if (
            self._state == self.STATE_DISCONNECTED
            or self._session_id is None
            or self._binding is None
        ):
            raise OrionLiveLinkRuntimeError(
                "An authenticated live-link session is required."
            )

    def _require_live(self) -> None:
        self._require_session()
        if self._state != self.STATE_LIVE:
            raise OrionLiveLinkRuntimeError(
                "Operation requires a live heartbeat state."
            )

    def _validate_common_envelope(
        self,
        envelope: dict[str, Any],
        *,
        message_type: str,
        proof_b64url: str,
        domain: str,
        require_live: bool,
    ) -> tuple[int, datetime]:
        if not isinstance(envelope, dict):
            raise OrionLiveLinkRuntimeError(
                "Live-link envelope must be an object."
            )
        if require_live:
            self._require_live()
        else:
            self._require_session()

        if envelope.get("protocol_version") != self.PROTOCOL_VERSION:
            raise OrionLiveLinkRuntimeError(
                "Unsupported live-link protocol version."
            )
        if envelope.get("message_type") != message_type:
            raise OrionLiveLinkRuntimeError(
                "Live-link message type is invalid."
            )
        if envelope.get("session_id") != self._session_id:
            raise OrionLiveLinkRuntimeError(
                "Live-link session ID does not match."
            )
        assert self._binding is not None
        if envelope.get("pairing_id") != self._binding["pairing_id"]:
            raise OrionLiveLinkRuntimeError(
                "Live-link pairing ID does not match."
            )
        if envelope.get("device_id") != self._binding["device_id"]:
            raise OrionLiveLinkRuntimeError(
                "Live-link device ID does not match."
            )

        sequence = self._validate_sequence(envelope.get("sequence"))
        sent_at = self._parse_utc(
            envelope.get("sent_at_utc"),
            label="sent_at_utc",
        )
        now = self._now()
        if (
            sent_at - now
        ).total_seconds() > self.MAX_CLOCK_SKEW_SECONDS:
            raise OrionLiveLinkRuntimeError(
                "Future live-link timestamp rejected."
            )

        try:
            verification = (
                self.pairing_manager.verify_authenticated_envelope(
                    domain=domain,
                    payload=envelope,
                    proof_b64url=proof_b64url,
                )
            )
        except OrionPairingIdentityRuntimeError as exc:
            if self._state == self.STATE_CONNECTING:
                self._state = self.STATE_FAILED
                self._failure_reason = "authentication_failure"
            raise OrionLiveLinkRuntimeError(
                "Authenticated live-link envelope verification failed."
            ) from exc
        if verification.get("verified") is not True:
            raise OrionLiveLinkRuntimeError(
                "Authenticated live-link envelope was not verified."
            )
        return sequence, sent_at

    @classmethod
    def _atlas_capabilities(
        cls,
    ) -> tuple[OrionLiveLinkCapability, ...]:
        return (
            OrionLiveLinkCapability(
                capability_id="orion.heartbeat",
                version="1",
                mode="read_only",
                constraints={
                    "interval_seconds": cls.HEARTBEAT_INTERVAL_SECONDS,
                    "stale_after_seconds": (
                        cls.HEARTBEAT_STALE_AFTER_SECONDS
                    ),
                    "failed_after_seconds": (
                        cls.HEARTBEAT_FAILED_AFTER_SECONDS
                    ),
                },
                source="ATLAS",
            ),
            OrionLiveLinkCapability(
                capability_id="orion.capability_negotiation",
                version="1",
                mode="read_only",
                constraints={
                    "unknown_required_capabilities": "reject",
                    "real_actions": False,
                },
                source="ATLAS",
            ),
            OrionLiveLinkCapability(
                capability_id="orion.live_grounding",
                version="1",
                mode="read_only",
                constraints={
                    "fresh_after_seconds": (
                        cls.GROUNDING_FRESH_AFTER_SECONDS
                    ),
                    "stale_after_seconds": (
                        cls.GROUNDING_STALE_AFTER_SECONDS
                    ),
                    "expired_after_seconds": (
                        cls.GROUNDING_EXPIRED_AFTER_SECONDS
                    ),
                    "redaction_required": True,
                },
                source="ATLAS",
            ),
        )

    def _normalize_capability(
        self,
        payload: Any,
    ) -> tuple[OrionLiveLinkCapability, bool]:
        if not isinstance(payload, dict):
            raise OrionLiveLinkRuntimeError(
                "Capability entry must be an object."
            )
        capability_id = self._validate_ascii_token(
            payload.get("capability_id"),
            label="capability ID",
            max_length=self.MAX_CAPABILITY_ID_LENGTH,
            allowed_extra="._-",
        )
        version = self._validate_ascii_token(
            payload.get("version"),
            label="capability version",
            max_length=self.MAX_VERSION_LENGTH,
            allowed_extra="._-",
        )
        mode = self._validate_ascii_token(
            payload.get("mode"),
            label="capability mode",
            max_length=self.MAX_MODE_LENGTH,
            allowed_extra="._-",
        )
        source = self._validate_ascii_token(
            payload.get("source"),
            label="capability source",
            max_length=32,
            allowed_extra="._-",
        )
        if source != "ORION":
            raise OrionLiveLinkRuntimeError(
                "Advertised capabilities must originate from ORION."
            )
        constraints = payload.get("constraints")
        if not isinstance(constraints, dict):
            raise OrionLiveLinkRuntimeError(
                "Capability constraints must be an object."
            )
        if len(self._canonical_json(constraints)) > self.MAX_CONSTRAINT_BYTES:
            raise OrionLiveLinkRuntimeError(
                "Capability constraints exceed the size limit."
            )
        required = constraints.get("required", False)
        if not isinstance(required, bool):
            raise OrionLiveLinkRuntimeError(
                "Capability required constraint must be boolean."
            )
        normalized_constraints = dict(constraints)
        normalized_constraints.pop("required", None)
        return (
            OrionLiveLinkCapability(
                capability_id=capability_id,
                version=version,
                mode=mode,
                constraints=normalized_constraints,
                source=source,
            ),
            required,
        )

    @classmethod
    def _compute_capability_digest(
        cls,
        capabilities: tuple[OrionLiveLinkCapability, ...],
    ) -> str:
        ordered = sorted(
            (item.to_dict() for item in capabilities),
            key=lambda item: (
                item["capability_id"],
                item["version"],
                item["mode"],
                item["source"],
            ),
        )
        return hashlib.sha256(cls._canonical_json(ordered)).hexdigest()

    def _grounding_freshness(
        self,
        *,
        observed_at: datetime,
        received_at: datetime,
    ) -> str:
        age = (received_at - observed_at).total_seconds()
        if age < -self.MAX_CLOCK_SKEW_SECONDS:
            return "future_rejected"
        if age <= self.GROUNDING_FRESH_AFTER_SECONDS:
            return "fresh"
        if age <= self.GROUNDING_STALE_AFTER_SECONDS:
            return "stale"
        return "expired"

    def open_authenticated_session(self) -> dict[str, Any]:
        if self._state != self.STATE_DISCONNECTED:
            raise OrionLiveLinkRuntimeError(
                "Live-link session can only open from disconnected state."
            )
        try:
            binding = self.pairing_manager.authenticated_binding()
        except OrionPairingIdentityRuntimeError as exc:
            raise OrionLiveLinkRuntimeError(
                "A paired ORION identity is required."
            ) from exc

        self._state = self.STATE_CONNECTING
        self._failure_reason = None
        self._session_id = "live-" + uuid.uuid4().hex
        self._binding = dict(binding)
        self._opened_at = self._now()
        self._last_heartbeat_at = None
        self._last_sequence = 0
        self._capability_digest = None
        self._agreed_capabilities = ()
        self._rejected_capabilities = ()
        self._latest_grounding = None
        return self.status()

    def receive_heartbeat(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if self._state not in (
            self.STATE_CONNECTING,
            self.STATE_LIVE,
            self.STATE_STALE,
        ):
            raise OrionLiveLinkRuntimeError(
                "Heartbeat is not accepted in the current state."
            )
        sequence, sent_at = self._validate_common_envelope(
            envelope,
            message_type="heartbeat",
            proof_b64url=proof_b64url,
            domain=self.DOMAIN_HEARTBEAT,
            require_live=False,
        )
        age = (self._now() - sent_at).total_seconds()
        if age > self.HEARTBEAT_FAILED_AFTER_SECONDS:
            raise OrionLiveLinkRuntimeError(
                "Expired heartbeat rejected."
            )

        digest = self._validate_hex_digest(
            envelope.get("capability_digest"),
            label="capability digest",
        )
        if (
            self._capability_digest is not None
            and digest != self._capability_digest
        ):
            raise OrionLiveLinkRuntimeError(
                "Heartbeat capability digest does not match agreement."
            )
        device_state = self._validate_ascii_token(
            envelope.get("device_state"),
            label="device state",
            max_length=64,
            allowed_extra="._-",
        )

        self._last_sequence = sequence
        self._last_heartbeat_at = self._now()
        self._state = self.STATE_LIVE
        self._failure_reason = None
        return {
            "status": "OK",
            "accepted": True,
            "state": self._state,
            "session_id": self._session_id,
            "sequence": sequence,
            "device_state": device_state,
            "received_at_utc": self._format_utc(
                self._last_heartbeat_at
            ),
            "capability_digest": digest,
            "network_used": False,
        }

    def negotiate_capabilities(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        sequence, _ = self._validate_common_envelope(
            envelope,
            message_type="capability_negotiation",
            proof_b64url=proof_b64url,
            domain=self.DOMAIN_CAPABILITY,
            require_live=True,
        )
        advertised_payload = envelope.get("advertised_capabilities")
        if (
            not isinstance(advertised_payload, list)
            or not advertised_payload
            or len(advertised_payload) > self.MAX_CAPABILITIES
        ):
            raise OrionLiveLinkRuntimeError(
                "Advertised capability list is invalid."
            )

        normalized = [
            self._normalize_capability(item)
            for item in advertised_payload
        ]
        keys = [
            (
                item.capability_id,
                item.version,
            )
            for item, _ in normalized
        ]
        if len(set(keys)) != len(keys):
            raise OrionLiveLinkRuntimeError(
                "Advertised capability list contains duplicates."
            )

        atlas_by_key = {
            (item.capability_id, item.version): item
            for item in self._atlas_capabilities()
        }
        agreed: list[OrionLiveLinkCapability] = []
        rejected: list[dict[str, Any]] = []

        for item, required in normalized:
            key = (item.capability_id, item.version)
            atlas_item = atlas_by_key.get(key)
            if atlas_item is None:
                if required:
                    raise OrionLiveLinkRuntimeError(
                        "Unknown required capability rejected."
                    )
                rejected.append(
                    {
                        "capability_id": item.capability_id,
                        "version": item.version,
                        "reason": "unsupported",
                    }
                )
                continue
            if item.mode != atlas_item.mode:
                if required:
                    raise OrionLiveLinkRuntimeError(
                        "Required capability mode mismatch rejected."
                    )
                rejected.append(
                    {
                        "capability_id": item.capability_id,
                        "version": item.version,
                        "reason": "mode_mismatch",
                    }
                )
                continue
            agreed.append(atlas_item)

        agreed_tuple = tuple(
            sorted(
                agreed,
                key=lambda item: (
                    item.capability_id,
                    item.version,
                ),
            )
        )
        rejected_tuple = tuple(
            sorted(
                rejected,
                key=lambda item: (
                    item["capability_id"],
                    item["version"],
                ),
            )
        )
        digest = self._compute_capability_digest(agreed_tuple)

        self._last_sequence = sequence
        self._agreed_capabilities = agreed_tuple
        self._rejected_capabilities = rejected_tuple
        self._capability_digest = digest
        return {
            "status": "OK",
            "sequence": sequence,
            "accepted_capabilities": [
                item.to_dict() for item in agreed_tuple
            ],
            "rejected_capabilities": list(rejected_tuple),
            "agreed_capabilities": [
                item.to_dict() for item in agreed_tuple
            ],
            "capability_digest": digest,
            "real_actions_enabled": False,
            "network_used": False,
        }

    def receive_grounding(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        sequence, _ = self._validate_common_envelope(
            envelope,
            message_type="grounding",
            proof_b64url=proof_b64url,
            domain=self.DOMAIN_GROUNDING,
            require_live=True,
        )
        if self._capability_digest is None:
            raise OrionLiveLinkRuntimeError(
                "Capability negotiation is required before grounding."
            )
        if envelope.get("capability_digest") != self._capability_digest:
            raise OrionLiveLinkRuntimeError(
                "Grounding capability digest does not match agreement."
            )
        agreed_ids = {
            item.capability_id
            for item in self._agreed_capabilities
        }
        if "orion.live_grounding" not in agreed_ids:
            raise OrionLiveLinkRuntimeError(
                "Live-grounding capability was not negotiated."
            )

        observed_at = self._parse_utc(
            envelope.get("observed_at_utc"),
            label="observed_at_utc",
        )
        received_at = self._now()
        freshness = self._grounding_freshness(
            observed_at=observed_at,
            received_at=received_at,
        )
        if freshness == "future_rejected":
            raise OrionLiveLinkRuntimeError(
                "Future grounding timestamp rejected."
            )
        if freshness == "expired":
            raise OrionLiveLinkRuntimeError(
                "Expired grounding snapshot rejected."
            )

        source = self._validate_ascii_token(
            envelope.get("source"),
            label="grounding source",
            max_length=64,
            allowed_extra="._-",
        )
        if source != "ORION":
            raise OrionLiveLinkRuntimeError(
                "Grounding source must be ORION."
            )
        subject = self._validate_ascii_token(
            envelope.get("subject"),
            label="grounding subject",
            max_length=128,
            allowed_extra="._-",
        )
        summary = envelope.get("summary")
        if (
            not isinstance(summary, str)
            or not summary.strip()
            or len(summary) > self.MAX_GROUNDING_SUMMARY_LENGTH
        ):
            raise OrionLiveLinkRuntimeError(
                "Grounding summary is invalid."
            )
        confidence = envelope.get("confidence")
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not math.isfinite(float(confidence))
            or float(confidence) < 0.0
            or float(confidence) > 1.0
        ):
            raise OrionLiveLinkRuntimeError(
                "Grounding confidence must be between 0 and 1."
            )
        provenance = envelope.get("provenance")
        if not isinstance(provenance, dict):
            raise OrionLiveLinkRuntimeError(
                "Grounding provenance must be an object."
            )
        if len(self._canonical_json(provenance)) > self.MAX_PROVENANCE_BYTES:
            raise OrionLiveLinkRuntimeError(
                "Grounding provenance exceeds the size limit."
            )
        if envelope.get("redaction_applied") is not True:
            raise OrionLiveLinkRuntimeError(
                "Grounding must be redacted before acceptance."
            )

        snapshot = OrionLiveGroundingSnapshot(
            source=source,
            subject=subject,
            summary=summary.strip(),
            confidence=float(confidence),
            provenance=dict(provenance),
            redaction_applied=True,
            observed_at_utc=self._format_utc(observed_at),
            received_at_utc=self._format_utc(received_at),
            freshness=freshness,
            capability_digest=self._capability_digest,
        )
        self._last_sequence = sequence
        self._latest_grounding = snapshot
        return {
            "status": "OK",
            "accepted": True,
            "sequence": sequence,
            "freshness": freshness,
            "usable_for_actions": False,
            "snapshot": snapshot.to_dict(),
            "persisted": False,
            "network_used": False,
        }

    def tick(self) -> dict[str, Any]:
        now = self._now()
        if (
            self._state == self.STATE_CONNECTING
            and self._opened_at is not None
            and (
                now - self._opened_at
            ).total_seconds() >= self.HEARTBEAT_FAILED_AFTER_SECONDS
        ):
            self._state = self.STATE_FAILED
            self._failure_reason = "handshake_timeout"
        elif (
            self._state in (
                self.STATE_LIVE,
                self.STATE_STALE,
            )
            and self._last_heartbeat_at is not None
        ):
            age = (
                now - self._last_heartbeat_at
            ).total_seconds()
            if age >= self.HEARTBEAT_FAILED_AFTER_SECONDS:
                self._state = self.STATE_FAILED
                self._failure_reason = "heartbeat_failed"
            elif age >= self.HEARTBEAT_STALE_AFTER_SECONDS:
                self._state = self.STATE_STALE
                self._failure_reason = "heartbeat_stale"
        return self.status()

    def close_session(self) -> dict[str, Any]:
        if self._state not in (
            self.STATE_LIVE,
            self.STATE_STALE,
        ):
            raise OrionLiveLinkRuntimeError(
                "Only a live or stale session can close normally."
            )
        self._clear_session()
        return self.status()

    def reset_session(self) -> dict[str, Any]:
        if self._state != self.STATE_FAILED:
            raise OrionLiveLinkRuntimeError(
                "Only a failed session can be reset."
            )
        self._clear_session()
        return self.status()

    def _clear_session(self) -> None:
        self._state = self.STATE_DISCONNECTED
        self._failure_reason = None
        self._session_id = None
        self._binding = None
        self._opened_at = None
        self._last_heartbeat_at = None
        self._last_sequence = 0
        self._capability_digest = None
        self._agreed_capabilities = ()
        self._rejected_capabilities = ()
        self._latest_grounding = None

    def status(self) -> dict[str, Any]:
        pairing_status = self.pairing_manager.status()
        now = self._now()
        heartbeat_age = (
            None
            if self._last_heartbeat_at is None
            else max(
                0.0,
                (now - self._last_heartbeat_at).total_seconds(),
            )
        )
        latest_grounding = (
            None
            if self._latest_grounding is None
            else {
                "source": self._latest_grounding.source,
                "subject": self._latest_grounding.subject,
                "confidence": self._latest_grounding.confidence,
                "observed_at_utc": (
                    self._latest_grounding.observed_at_utc
                ),
                "received_at_utc": (
                    self._latest_grounding.received_at_utc
                ),
                "freshness": self._latest_grounding.freshness,
                "redaction_applied": True,
                "payload_persisted": False,
            }
        )
        payload = {
            "status": "ready",
            "reason": "orion_live_link_runtime_ready",
            "state": self._state,
            "failure_reason": self._failure_reason,
            "session_id": self._session_id,
            "paired_identity_available": (
                pairing_status["authenticated"] is True
                and pairing_status["device_identity_bound"] is True
            ),
            "binding": (
                None
                if self._binding is None
                else dict(self._binding)
            ),
            "last_sequence": self._last_sequence,
            "opened_at_utc": (
                None
                if self._opened_at is None
                else self._format_utc(self._opened_at)
            ),
            "last_heartbeat_at_utc": (
                None
                if self._last_heartbeat_at is None
                else self._format_utc(self._last_heartbeat_at)
            ),
            "heartbeat_age_seconds": heartbeat_age,
            "heartbeat_active": self._state in (
                self.STATE_LIVE,
                self.STATE_STALE,
            ),
            "capability_negotiation_active": (
                self._capability_digest is not None
                and self._state in (
                    self.STATE_LIVE,
                    self.STATE_STALE,
                )
            ),
            "live_grounding_active": (
                self._latest_grounding is not None
                and self._latest_grounding.freshness == "fresh"
                and self._state == self.STATE_LIVE
            ),
            "capability_digest": self._capability_digest,
            "agreed_capabilities": [
                item.to_dict()
                for item in self._agreed_capabilities
            ],
            "rejected_capabilities": list(
                self._rejected_capabilities
            ),
            "latest_grounding": latest_grounding,
            "network_listener_active": False,
            "network_connection_active": False,
            "action_preview_active": False,
            "approval_active": False,
            "permission_active": False,
            "audit_write_active": False,
            "real_action_execution_active": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_active": False,
            "runtime_persistence_active": False,
            "heartbeat_history_persisted": False,
            "grounding_payload_persisted": False,
            "secret_exposed": False,
            "safe_idle": self._state == self.STATE_DISCONNECTED,
        }
        for field in self.DEFERRED_FALSE_FIELDS:
            if payload[field] is not False:
                raise OrionLiveLinkRuntimeError(
                    f"Deferred field '{field}' became active."
                )
        return payload

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "component": {
                "name": "aura_orion_live_link_runtime",
                "component_version": self.COMPONENT_VERSION,
                "sprint": 275,
                "boundary": (
                    "heartbeat_capability_negotiation_live_grounding"
                ),
            },
            "protocol": {
                "version": self.PROTOCOL_VERSION,
                "proof_algorithm": "HMAC-SHA256",
                "proof_verification": "hmac.compare_digest",
                "pairing_binding_required": True,
                "secret_exposed": False,
                "domains": {
                    "heartbeat": self.DOMAIN_HEARTBEAT,
                    "capability_negotiation": self.DOMAIN_CAPABILITY,
                    "grounding": self.DOMAIN_GROUNDING,
                },
                "strictly_monotonic_sequence": True,
                "sequence_start": 1,
                "sequence_max": self.MAX_SEQUENCE,
            },
            "state_machine": {
                "states": list(self.STATES),
                "valid_transitions": [
                    {
                        "from": source,
                        "event": event,
                        "to": target,
                    }
                    for source, event, target in self.VALID_TRANSITIONS
                ],
                "default_state": self.STATE_DISCONNECTED,
            },
            "heartbeat": {
                "interval_seconds": self.HEARTBEAT_INTERVAL_SECONDS,
                "stale_after_seconds": (
                    self.HEARTBEAT_STALE_AFTER_SECONDS
                ),
                "failed_after_seconds": (
                    self.HEARTBEAT_FAILED_AFTER_SECONDS
                ),
                "max_clock_skew_seconds": (
                    self.MAX_CLOCK_SKEW_SECONDS
                ),
            },
            "capability_negotiation": {
                "atlas_capabilities": [
                    item.to_dict()
                    for item in self._atlas_capabilities()
                ],
                "canonicalization": (
                    "JSON UTF-8 sort_keys compact separators allow_nan=False"
                ),
                "digest": "SHA-256",
                "unknown_required_capabilities": "reject",
                "deferred_action_capabilities": "reject",
            },
            "live_grounding": {
                "fresh_after_seconds": (
                    self.GROUNDING_FRESH_AFTER_SECONDS
                ),
                "stale_after_seconds": (
                    self.GROUNDING_STALE_AFTER_SECONDS
                ),
                "expired_after_seconds": (
                    self.GROUNDING_EXPIRED_AFTER_SECONDS
                ),
                "future_timestamps": "reject",
                "redaction_required": True,
                "expired_for_actions": False,
            },
            "transport": {
                "mode": (
                    "transport_agnostic_authenticated_envelope_runtime"
                ),
                "network_listener_active": False,
                "network_connection_active": False,
                "direct_send_receive": False,
            },
            "persistence": {
                "runtime_state": "in_memory_only",
                "heartbeat_history_persisted": False,
                "grounding_payload_persisted": False,
                "audit_write_active": False,
                "memory_write_active": False,
            },
            "deferred_boundaries": {
                "sprint_276": [
                    "action_preview",
                    "explicit_approval",
                ],
                "sprint_277": [
                    "scoped_permission",
                    "permission_expiry",
                    "audit_write",
                    "reviewed_memory",
                ],
                "sprint_278": [
                    "capture_actions",
                    "app_actions",
                    "file_actions",
                    "obs_actions",
                ],
                "sprint_279": [
                    "watchdog",
                    "emergency_stop_runtime",
                    "recovery",
                    "dialogue_evaluation",
                ],
            },
        }

    def self_test(self) -> dict[str, Any]:
        assertions: list[tuple[str, bool]] = []

        def check(name: str, condition: bool) -> None:
            assertions.append((name, bool(condition)))

        def expect_error(
            name: str,
            operation: Callable[[], Any],
            contains: str | None = None,
        ) -> None:
            try:
                operation()
            except (
                OrionLiveLinkRuntimeError,
                OrionPairingIdentityRuntimeError,
                ValueError,
            ) as exc:
                check(
                    name,
                    contains is None
                    or contains.lower() in str(exc).lower(),
                )
            else:
                check(name, False)

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

        with tempfile.TemporaryDirectory(
            prefix="aura-sprint-275-self-test-"
        ) as temporary:
            state_root = Path(temporary) / "pairing"
            pairing = AuraOrionPairingIdentityRuntimeManager(
                project_root=self.project_root,
                state_root=state_root,
                now_provider=lambda: clock["now"],
            )
            unpaired_live = AuraOrionLiveLinkRuntimeManager(
                project_root=self.project_root,
                pairing_manager=pairing,
                now_provider=lambda: clock["now"],
            )
            expect_error(
                "unpaired_open_rejected",
                unpaired_live.open_authenticated_session,
                "paired",
            )

            enrollment = pairing.begin_pairing(
                display_name="ORION Sprint 275 Test",
                platform="windows",
            )
            secret_text = enrollment["credential"][
                "shared_secret_b64url"
            ]
            secret = base64.urlsafe_b64decode(
                secret_text + "=" * (-len(secret_text) % 4)
            )
            challenge = enrollment["challenge"]
            message = "\n".join(
                [
                    "1",
                    enrollment["pairing_id"],
                    enrollment["device"]["device_id"],
                    challenge["challenge_id"],
                    challenge["challenge_b64url"],
                    challenge["issued_at_utc"],
                    challenge["expires_at_utc"],
                ]
            ).encode("utf-8")
            pairing_proof = base64.urlsafe_b64encode(
                hmac.new(
                    secret,
                    message,
                    hashlib.sha256,
                ).digest()
            ).decode("ascii").rstrip("=")
            pairing.complete_pairing(
                pairing_id=enrollment["pairing_id"],
                device_id=enrollment["device"]["device_id"],
                challenge_id=challenge["challenge_id"],
                proof_b64url=pairing_proof,
            )

            binding = pairing.authenticated_binding()
            check("binding_pairing_id", binding["pairing_id"].startswith("pair-"))
            check("binding_device_id", binding["device_id"].startswith("orion-"))
            check("binding_credential_id", binding["credential_id"].startswith("cred-"))
            check("binding_fingerprint", len(binding["credential_fingerprint"]) == 32)
            check("binding_identity_version", binding["identity_version"] == "orion-device-identity-v1")
            check("binding_role", binding["device_role"] == "ORION_AGENT")
            check("binding_platform", binding["platform"] == "windows")
            check("binding_secret_redacted", binding["secret_exposed"] is False)
            check("binding_no_secret_key", "shared_secret_b64url" not in binding)

            live = AuraOrionLiveLinkRuntimeManager(
                project_root=self.project_root,
                pairing_manager=pairing,
                now_provider=lambda: clock["now"],
            )
            initial = live.status()
            check("initial_state", initial["state"] == self.STATE_DISCONNECTED)
            check("initial_safe_idle", initial["safe_idle"] is True)
            check("initial_pairing_available", initial["paired_identity_available"] is True)
            check("initial_no_session", initial["session_id"] is None)
            check("initial_sequence_zero", initial["last_sequence"] == 0)
            check("initial_no_capability_digest", initial["capability_digest"] is None)
            check("initial_no_grounding", initial["latest_grounding"] is None)
            check("initial_network_listener_false", initial["network_listener_active"] is False)
            check("initial_network_connection_false", initial["network_connection_active"] is False)
            for field in self.DEFERRED_FALSE_FIELDS:
                check(f"initial_{field}", initial[field] is False)

            opened = live.open_authenticated_session()
            session_id = opened["session_id"]
            check("opened_state", opened["state"] == self.STATE_CONNECTING)
            check("opened_session_id", isinstance(session_id, str) and session_id.startswith("live-"))
            check("opened_binding", opened["binding"]["pairing_id"] == binding["pairing_id"])
            check("opened_not_safe_idle", opened["safe_idle"] is False)
            check("opened_no_network", opened["network_listener_active"] is False and opened["network_connection_active"] is False)
            expect_error(
                "second_open_rejected",
                live.open_authenticated_session,
                "disconnected",
            )

            empty_digest = hashlib.sha256(
                self._canonical_json([])
            ).hexdigest()
            heartbeat = {
                "protocol_version": self.PROTOCOL_VERSION,
                "message_type": "heartbeat",
                "session_id": session_id,
                "pairing_id": binding["pairing_id"],
                "device_id": binding["device_id"],
                "sequence": 1,
                "sent_at_utc": self._format_utc(clock["now"]),
                "device_state": "ready",
                "capability_digest": empty_digest,
            }
            signed_heartbeat = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_HEARTBEAT,
                payload=heartbeat,
            )
            check("heartbeat_sign_status", signed_heartbeat["status"] == "OK")
            check("heartbeat_sign_algorithm", signed_heartbeat["algorithm"] == "HMAC-SHA256")
            check("heartbeat_sign_verification", signed_heartbeat["verification"] == "hmac.compare_digest")
            check("heartbeat_sign_domain", signed_heartbeat["domain"] == self.DOMAIN_HEARTBEAT)
            check("heartbeat_sign_secret_redacted", signed_heartbeat["secret_exposed"] is False)
            accepted = live.receive_heartbeat(
                envelope=heartbeat,
                proof_b64url=signed_heartbeat["proof_b64url"],
            )
            check("heartbeat_accepted", accepted["accepted"] is True)
            check("heartbeat_live", accepted["state"] == self.STATE_LIVE)
            check("heartbeat_sequence", accepted["sequence"] == 1)
            check("heartbeat_device_state", accepted["device_state"] == "ready")
            check("heartbeat_network_zero", accepted["network_used"] is False)

            duplicate = dict(heartbeat)
            duplicate_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_HEARTBEAT,
                payload=duplicate,
            )
            expect_error(
                "duplicate_sequence_rejected",
                lambda: live.receive_heartbeat(
                    envelope=duplicate,
                    proof_b64url=duplicate_signed["proof_b64url"],
                ),
                "duplicate",
            )
            out_of_order = dict(heartbeat)
            out_of_order["sequence"] = 0
            expect_error(
                "zero_sequence_rejected",
                lambda: live.receive_heartbeat(
                    envelope=out_of_order,
                    proof_b64url=signed_heartbeat["proof_b64url"],
                ),
                "range",
            )
            wrong_session = dict(heartbeat)
            wrong_session["sequence"] = 2
            wrong_session["session_id"] = "live-" + uuid.uuid4().hex
            wrong_session_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_HEARTBEAT,
                payload=wrong_session,
            )
            expect_error(
                "wrong_session_rejected",
                lambda: live.receive_heartbeat(
                    envelope=wrong_session,
                    proof_b64url=wrong_session_signed["proof_b64url"],
                ),
                "session",
            )
            tampered = dict(heartbeat)
            tampered["sequence"] = 2
            expect_error(
                "tampered_payload_rejected",
                lambda: live.receive_heartbeat(
                    envelope=tampered,
                    proof_b64url=signed_heartbeat["proof_b64url"],
                ),
                "verification",
            )
            cross_domain = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_GROUNDING,
                payload=tampered,
            )
            expect_error(
                "cross_domain_reuse_rejected",
                lambda: live.receive_heartbeat(
                    envelope=tampered,
                    proof_b64url=cross_domain["proof_b64url"],
                ),
                "verification",
            )

            advertised = [
                {
                    "capability_id": "orion.live_grounding",
                    "version": "1",
                    "mode": "read_only",
                    "constraints": {},
                    "source": "ORION",
                },
                {
                    "capability_id": "orion.heartbeat",
                    "version": "1",
                    "mode": "read_only",
                    "constraints": {},
                    "source": "ORION",
                },
                {
                    "capability_id": "orion.capability_negotiation",
                    "version": "1",
                    "mode": "read_only",
                    "constraints": {},
                    "source": "ORION",
                },
                {
                    "capability_id": "orion.capture_action",
                    "version": "1",
                    "mode": "execute",
                    "constraints": {},
                    "source": "ORION",
                },
            ]
            capability_envelope = {
                "protocol_version": self.PROTOCOL_VERSION,
                "message_type": "capability_negotiation",
                "session_id": session_id,
                "pairing_id": binding["pairing_id"],
                "device_id": binding["device_id"],
                "sequence": 2,
                "sent_at_utc": self._format_utc(clock["now"]),
                "advertised_capabilities": advertised,
            }
            capability_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_CAPABILITY,
                payload=capability_envelope,
            )
            agreement = live.negotiate_capabilities(
                envelope=capability_envelope,
                proof_b64url=capability_signed["proof_b64url"],
            )
            check("agreement_sequence", agreement["sequence"] == 2)
            check("agreement_accepted_count", len(agreement["accepted_capabilities"]) == 3)
            check("agreement_rejected_count", len(agreement["rejected_capabilities"]) == 1)
            check("agreement_capture_rejected", agreement["rejected_capabilities"][0]["capability_id"] == "orion.capture_action")
            check("agreement_capture_reason", agreement["rejected_capabilities"][0]["reason"] == "unsupported")
            check("agreement_digest_length", len(agreement["capability_digest"]) == 64)
            check("agreement_real_actions_false", agreement["real_actions_enabled"] is False)
            check("agreement_network_zero", agreement["network_used"] is False)
            check("agreement_sorted", [item["capability_id"] for item in agreement["agreed_capabilities"]] == sorted(item["capability_id"] for item in agreement["agreed_capabilities"]))

            required_unknown = {
                "protocol_version": self.PROTOCOL_VERSION,
                "message_type": "capability_negotiation",
                "session_id": session_id,
                "pairing_id": binding["pairing_id"],
                "device_id": binding["device_id"],
                "sequence": 3,
                "sent_at_utc": self._format_utc(clock["now"]),
                "advertised_capabilities": [
                    {
                        "capability_id": "orion.unknown_required",
                        "version": "1",
                        "mode": "read_only",
                        "constraints": {"required": True},
                        "source": "ORION",
                    }
                ],
            }
            required_unknown_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_CAPABILITY,
                payload=required_unknown,
            )
            expect_error(
                "unknown_required_rejected",
                lambda: live.negotiate_capabilities(
                    envelope=required_unknown,
                    proof_b64url=required_unknown_signed["proof_b64url"],
                ),
                "required",
            )
            check("failed_negotiation_no_sequence_mutation", live.status()["last_sequence"] == 2)

            grounding = {
                "protocol_version": self.PROTOCOL_VERSION,
                "message_type": "grounding",
                "session_id": session_id,
                "pairing_id": binding["pairing_id"],
                "device_id": binding["device_id"],
                "sequence": 3,
                "observed_at_utc": self._format_utc(clock["now"]),
                "sent_at_utc": self._format_utc(clock["now"]),
                "source": "ORION",
                "subject": "desktop_state",
                "summary": "redacted metadata-only workspace summary",
                "confidence": 0.95,
                "provenance": {
                    "adapter": "orion_agent",
                    "capture": "metadata_only",
                },
                "redaction_applied": True,
                "capability_digest": agreement["capability_digest"],
            }
            grounding_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_GROUNDING,
                payload=grounding,
            )
            grounded = live.receive_grounding(
                envelope=grounding,
                proof_b64url=grounding_signed["proof_b64url"],
            )
            check("grounding_accepted", grounded["accepted"] is True)
            check("grounding_sequence", grounded["sequence"] == 3)
            check("grounding_fresh", grounded["freshness"] == "fresh")
            check("grounding_actions_false", grounded["usable_for_actions"] is False)
            check("grounding_not_persisted", grounded["persisted"] is False)
            check("grounding_network_zero", grounded["network_used"] is False)
            check("grounding_redacted", grounded["snapshot"]["redaction_applied"] is True)
            check("grounding_confidence", grounded["snapshot"]["confidence"] == 0.95)
            status_after_grounding = live.status()
            check("status_heartbeat_active", status_after_grounding["heartbeat_active"] is True)
            check("status_capability_active", status_after_grounding["capability_negotiation_active"] is True)
            check("status_grounding_active", status_after_grounding["live_grounding_active"] is True)
            check("status_no_raw_summary", "summary" not in status_after_grounding["latest_grounding"])
            check("status_grounding_not_persisted", status_after_grounding["latest_grounding"]["payload_persisted"] is False)

            unredacted = dict(grounding)
            unredacted["sequence"] = 4
            unredacted["redaction_applied"] = False
            unredacted_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_GROUNDING,
                payload=unredacted,
            )
            expect_error(
                "unredacted_grounding_rejected",
                lambda: live.receive_grounding(
                    envelope=unredacted,
                    proof_b64url=unredacted_signed["proof_b64url"],
                ),
                "redacted",
            )
            check("unredacted_no_sequence_mutation", live.status()["last_sequence"] == 3)

            future_grounding = dict(grounding)
            future_grounding["sequence"] = 4
            future_grounding["observed_at_utc"] = self._format_utc(
                clock["now"] + timedelta(seconds=10)
            )
            future_grounding["sent_at_utc"] = self._format_utc(
                clock["now"]
            )
            future_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_GROUNDING,
                payload=future_grounding,
            )
            expect_error(
                "future_grounding_rejected",
                lambda: live.receive_grounding(
                    envelope=future_grounding,
                    proof_b64url=future_signed["proof_b64url"],
                ),
                "future",
            )

            expired_grounding = dict(grounding)
            expired_grounding["sequence"] = 4
            expired_grounding["observed_at_utc"] = self._format_utc(
                clock["now"] - timedelta(seconds=20)
            )
            expired_grounding["sent_at_utc"] = self._format_utc(
                clock["now"]
            )
            expired_signed = pairing.sign_authenticated_envelope(
                domain=self.DOMAIN_GROUNDING,
                payload=expired_grounding,
            )
            expect_error(
                "expired_grounding_rejected",
                lambda: live.receive_grounding(
                    envelope=expired_grounding,
                    proof_b64url=expired_signed["proof_b64url"],
                ),
                "expired",
            )

            clock["now"] += timedelta(
                seconds=self.HEARTBEAT_STALE_AFTER_SECONDS
            )
            stale = live.tick()
            check("tick_stale_state", stale["state"] == self.STATE_STALE)
            check("tick_stale_reason", stale["failure_reason"] == "heartbeat_stale")
            check("tick_stale_heartbeat_active", stale["heartbeat_active"] is True)
            check("tick_stale_grounding_inactive", stale["live_grounding_active"] is False)
            clock["now"] += timedelta(
                seconds=(
                    self.HEARTBEAT_FAILED_AFTER_SECONDS
                    - self.HEARTBEAT_STALE_AFTER_SECONDS
                )
            )
            failed = live.tick()
            check("tick_failed_state", failed["state"] == self.STATE_FAILED)
            check("tick_failed_reason", failed["failure_reason"] == "heartbeat_failed")
            check("tick_failed_heartbeat_inactive", failed["heartbeat_active"] is False)
            check("tick_failed_capability_inactive", failed["capability_negotiation_active"] is False)
            reset = live.reset_session()
            check("reset_disconnected", reset["state"] == self.STATE_DISCONNECTED)
            check("reset_safe_idle", reset["safe_idle"] is True)
            check("reset_session_none", reset["session_id"] is None)
            check("reset_sequence_zero", reset["last_sequence"] == 0)
            check("reset_digest_none", reset["capability_digest"] is None)
            check("reset_grounding_none", reset["latest_grounding"] is None)

            inspect = live.inspect_runtime()
            check("inspect_sprint", inspect["component"]["sprint"] == 275)
            check("inspect_component_version", inspect["component"]["component_version"] == "0.1.0")
            check("inspect_boundary", inspect["component"]["boundary"] == "heartbeat_capability_negotiation_live_grounding")
            check("inspect_protocol", inspect["protocol"]["version"] == self.PROTOCOL_VERSION)
            check("inspect_hmac", inspect["protocol"]["proof_algorithm"] == "HMAC-SHA256")
            check("inspect_compare_digest", inspect["protocol"]["proof_verification"] == "hmac.compare_digest")
            check("inspect_binding_required", inspect["protocol"]["pairing_binding_required"] is True)
            check("inspect_secret_redacted", inspect["protocol"]["secret_exposed"] is False)
            check("inspect_states", len(inspect["state_machine"]["states"]) == 5)
            check("inspect_transitions", len(inspect["state_machine"]["valid_transitions"]) == 11)
            check("inspect_interval", inspect["heartbeat"]["interval_seconds"] == 5)
            check("inspect_stale", inspect["heartbeat"]["stale_after_seconds"] == 15)
            check("inspect_failed", inspect["heartbeat"]["failed_after_seconds"] == 30)
            check("inspect_atlas_caps", len(inspect["capability_negotiation"]["atlas_capabilities"]) == 3)
            check("inspect_unknown_reject", inspect["capability_negotiation"]["unknown_required_capabilities"] == "reject")
            check("inspect_redaction_required", inspect["live_grounding"]["redaction_required"] is True)
            check("inspect_network_listener_false", inspect["transport"]["network_listener_active"] is False)
            check("inspect_network_connection_false", inspect["transport"]["network_connection_active"] is False)
            check("inspect_in_memory", inspect["persistence"]["runtime_state"] == "in_memory_only")
            check("inspect_heartbeat_not_persisted", inspect["persistence"]["heartbeat_history_persisted"] is False)
            check("inspect_grounding_not_persisted", inspect["persistence"]["grounding_payload_persisted"] is False)
            check("inspect_audit_false", inspect["persistence"]["audit_write_active"] is False)
            check("inspect_memory_false", inspect["persistence"]["memory_write_active"] is False)

        failed_assertions = [
            name for name, passed in assertions if not passed
        ]
        return {
            "status": (
                "OK" if not failed_assertions else "FAILED"
            ),
            "component": {
                "name": "aura_orion_live_link_runtime",
                "component_version": self.COMPONENT_VERSION,
                "sprint": 275,
                "boundary": (
                    "heartbeat_capability_negotiation_live_grounding"
                ),
            },
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed_assertions),
            "failed_assertions": failed_assertions,
            "contract": {
                "states": list(self.STATES),
                "valid_transitions": len(self.VALID_TRANSITIONS),
                "heartbeat_interval_seconds": (
                    self.HEARTBEAT_INTERVAL_SECONDS
                ),
                "heartbeat_stale_after_seconds": (
                    self.HEARTBEAT_STALE_AFTER_SECONDS
                ),
                "heartbeat_failed_after_seconds": (
                    self.HEARTBEAT_FAILED_AFTER_SECONDS
                ),
                "proof_algorithm": "HMAC-SHA256",
                "proof_verification": "hmac.compare_digest",
                "pairing_binding_required": True,
                "atlas_capabilities": len(
                    self._atlas_capabilities()
                ),
                "runtime_persistence": "in_memory_only",
                "network_listener_active": False,
                "network_connection_active": False,
                "real_action_execution_active": False,
            },
        }
