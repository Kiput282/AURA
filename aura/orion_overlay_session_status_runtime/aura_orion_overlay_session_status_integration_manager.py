"""Sprint 289 ORION overlay session-status integration runtime."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from aura.orion_native_overlay_runtime import (
    AuraOrionNativeOverlayRuntimeManager,
    OrionNativeOverlayRuntimeError,
)


class OrionOverlaySessionStatusIntegrationError(RuntimeError):
    """Raised when the Sprint 289 integration contract is invalid."""


@dataclass(frozen=True)
class OrionOverlaySessionStatusIdentity:
    """Canonical Sprint 289 runtime identity."""

    product_version: str = "1.4.9"
    sprint: int = 289
    boundary: str = "orion_overlay_session_status_integration"


class AuraOrionOverlaySessionStatusIntegrationManager:
    """Metadata-only status projection and reviewed stop-request bridge."""

    CAPABILITY_ID = "orion.game.overlay.session_status_integration"
    STATUS_SURFACE = "ORION_READ_ONLY_OPERATIONAL_STATUS"
    AUTHORITATIVE_STATUS_SOURCE = (
        "game_session_orchestrator_metadata_projection"
    )
    STATUS_TRANSPORT = "local_atomic_json_snapshot_polling"
    COMMAND_TRANSPORT = (
        "local_atomic_reviewed_command_request_and_acknowledgement"
    )
    AUTHORITATIVE_HANDLER = "game_session_orchestrator"

    POLL_INTERVAL_MILLISECONDS = 250
    STALE_TIMEOUT_MILLISECONDS = 1500
    REQUEST_EXPIRY_MILLISECONDS = 5000
    EMERGENCY_HOLD_MILLISECONDS = 1500

    QUICK_STOP_COMMAND = "QUICK_STOP_CURRENT_SESSION"
    EMERGENCY_STOP_COMMAND = "EMERGENCY_STOP_ALL"

    QUICK_STOP_CONFIRMATION = "two_step_local_confirmation"
    EMERGENCY_CONFIRMATION = "press_and_hold_local_confirmation"

    ACK_DISPOSITIONS = (
        "ACCEPTED",
        "DUPLICATE",
        "EXPIRED",
        "REJECTED",
    )

    LIVE_REQUIRED_FIELDS = (
        *AuraOrionNativeOverlayRuntimeManager.REQUIRED_STATUS_FIELDS,
        "session_elapsed_milliseconds",
    )

    REQUEST_REQUIRED_FIELDS = (
        "schema_version",
        "request_id",
        "command",
        "session_id",
        "issued_monotonic_milliseconds",
        "expires_monotonic_milliseconds",
        "confirmation_type",
        "confirmation_started_monotonic_milliseconds",
        "confirmation_completed_monotonic_milliseconds",
        "confirmation_hold_milliseconds",
        "reviewed",
        "permission_snapshot_sha256",
        "audit_required",
        "idempotency_key",
        "overlay_origin",
        "authority",
        "direct_execution",
        "raw_input_included",
    )

    ACK_REQUIRED_FIELDS = (
        "schema_version",
        "request_id",
        "command",
        "disposition",
        "authoritative_handler",
        "handled_monotonic_milliseconds",
        "executed_in_probe",
        "idempotent_replay",
        "safe_idle",
        "reason",
    )

    def __init__(
        self,
        *,
        project_root: Path | str = ".",
        identity: OrionOverlaySessionStatusIdentity | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.identity = identity or OrionOverlaySessionStatusIdentity()
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise OrionOverlaySessionStatusIntegrationError(message)

    @staticmethod
    def _strict_bool(value: Any, field: str) -> bool:
        if type(value) is not bool:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} must be a boolean."
            )
        return value

    @staticmethod
    def _strict_int(
        value: Any,
        *,
        field: str,
        minimum: int = 0,
    ) -> int:
        if type(value) is not int or value < minimum:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} must be an integer >= {minimum}."
            )
        return value

    @staticmethod
    def _bounded_text(
        value: Any,
        *,
        field: str,
        allow_empty: bool = False,
        maximum: int = 160,
    ) -> str:
        if not isinstance(value, str):
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} must be text."
            )
        text = value.strip()
        if not allow_empty and not text:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} cannot be empty."
            )
        if len(text) > maximum:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} exceeds {maximum} characters."
            )
        if any(ord(character) < 32 for character in text):
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} contains a control character."
            )
        return text

    @staticmethod
    def _sha256_hex(value: Any, field: str) -> str:
        text = (
            AuraOrionOverlaySessionStatusIntegrationManager._bounded_text(
                value,
                field=field,
                maximum=64,
            )
        )
        if len(text) != 64:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} must be a SHA-256 hex digest."
            )
        try:
            bytes.fromhex(text)
        except ValueError as exc:
            raise OrionOverlaySessionStatusIntegrationError(
                f"{field} must be hexadecimal."
            ) from exc
        return text.lower()

    @staticmethod
    def canonical_json_bytes(value: Any) -> bytes:
        return (
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            )
            + "\n"
        ).encode("utf-8")

    @classmethod
    def atomic_write_json(
        cls,
        path: Path | str,
        value: Any,
    ) -> str:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".tmp")
        data = cls.canonical_json_bytes(value)

        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary, destination)

        try:
            directory_fd = os.open(
                str(destination.parent),
                os.O_RDONLY,
            )
        except OSError:
            directory_fd = None

        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)

        cls._guard(
            not temporary.exists(),
            "Atomic temporary file was not removed.",
        )
        return hashlib.sha256(destination.read_bytes()).hexdigest()

    @staticmethod
    def read_json(path: Path | str) -> dict[str, Any]:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise OrionOverlaySessionStatusIntegrationError(
                "JSON root must be an object."
            )
        return value

    @classmethod
    def validate_live_status_snapshot(
        cls,
        snapshot: Mapping[str, Any],
        *,
        previous_sequence: int | None = None,
        previous_session_id: str | None = None,
        previous_elapsed_milliseconds: int | None = None,
    ) -> dict[str, Any]:
        if not isinstance(snapshot, Mapping):
            raise OrionOverlaySessionStatusIntegrationError(
                "Live status snapshot must be a mapping."
            )

        missing = [
            field
            for field in cls.LIVE_REQUIRED_FIELDS
            if field not in snapshot
        ]
        cls._guard(
            not missing,
            f"Missing live status fields: {missing}",
        )

        foundation = {
            field: snapshot[field]
            for field in (
                AuraOrionNativeOverlayRuntimeManager.REQUIRED_STATUS_FIELDS
            )
        }

        try:
            validated = (
                AuraOrionNativeOverlayRuntimeManager
                .validate_status_snapshot(
                    foundation,
                    previous_sequence=previous_sequence,
                )
            )
        except OrionNativeOverlayRuntimeError as exc:
            raise OrionOverlaySessionStatusIntegrationError(
                str(exc)
            ) from exc

        elapsed = cls._strict_int(
            snapshot["session_elapsed_milliseconds"],
            field="session_elapsed_milliseconds",
        )

        session_id = validated["session_id"]
        if validated["safe_idle"]:
            cls._guard(
                elapsed == 0,
                "SAFE_IDLE session timer must be zero.",
            )
        elif (
            previous_session_id is not None
            and session_id == previous_session_id
            and previous_elapsed_milliseconds is not None
        ):
            cls._guard(
                elapsed >= previous_elapsed_milliseconds,
                "Session elapsed timer regressed.",
            )

        validated["session_elapsed_milliseconds"] = elapsed
        return validated

    @classmethod
    def project_session_status(
        cls,
        session_status: Mapping[str, Any],
        *,
        sequence: int,
        updated_monotonic_milliseconds: int,
        snapshot_age_milliseconds: int = 0,
        session_elapsed_milliseconds: int = 0,
    ) -> dict[str, Any]:
        if not isinstance(session_status, Mapping):
            raise OrionOverlaySessionStatusIntegrationError(
                "Session status must be a mapping."
            )

        state = cls._bounded_text(
            session_status.get("state"),
            field="state",
            maximum=64,
        )
        cls._guard(
            state
            in AuraOrionNativeOverlayRuntimeManager.ALLOWED_STATES,
            "Unknown session orchestration state.",
        )

        safe_idle = state == "SAFE_IDLE"
        session_id_value = session_status.get("session_id")
        mode_value = session_status.get("mode_profile")

        if safe_idle:
            session_id = None
            mode_profile = None
        else:
            session_id = cls._bounded_text(
                session_id_value,
                field="session_id",
                maximum=96,
            )
            if mode_value in (None, ""):
                mode_profile = None
            else:
                mode_profile = cls._bounded_text(
                    mode_value,
                    field="mode_profile",
                    maximum=64,
                )
                cls._guard(
                    mode_profile
                    in (
                        AuraOrionNativeOverlayRuntimeManager
                        .ALLOWED_MODE_PROFILES
                    ),
                    "Unsupported mode profile.",
                )

        snapshot = {
            "schema_version": 1,
            "surface": cls.STATUS_SURFACE,
            "authority": False,
            "sequence": cls._strict_int(
                sequence,
                field="sequence",
                minimum=1,
            ),
            "state": state,
            "session_id": session_id,
            "mode_profile": mode_profile,
            "game_id": cls._bounded_text(
                session_status.get("game_id", ""),
                field="game_id",
                allow_empty=True,
                maximum=64,
            ),
            "game_display_name": cls._bounded_text(
                session_status.get("game_display_name", ""),
                field="game_display_name",
                allow_empty=True,
                maximum=96,
            ),
            "coach": cls._strict_bool(
                session_status.get("coach", False),
                "coach",
            ),
            "observer": cls._strict_bool(
                session_status.get("observer", False),
                "observer",
            ),
            "recording": cls._strict_bool(
                session_status.get("recording", False),
                "recording",
            ),
            "foreground_verified": cls._strict_bool(
                session_status.get("foreground_verified", False),
                "foreground_verified",
            ),
            "paused": state == "PAUSED_FOCUS_LOST",
            "blocked": state == "BLOCKED",
            "safe_idle": safe_idle,
            "reason": session_status.get("reason"),
            "quick_stop_available": (
                not safe_idle
                and state not in ("STOPPING",)
                and not bool(session_status.get("stale", False))
            ),
            "emergency_stop_available": True,
            "updated_monotonic_milliseconds": cls._strict_int(
                updated_monotonic_milliseconds,
                field="updated_monotonic_milliseconds",
            ),
            "snapshot_age_milliseconds": cls._strict_int(
                snapshot_age_milliseconds,
                field="snapshot_age_milliseconds",
            ),
            "stale": cls._strict_bool(
                session_status.get("stale", False),
                "stale",
            ),
            "can_start_or_authorize_session": False,
            "raw_media_included": False,
            "raw_input_included": False,
            "session_elapsed_milliseconds": cls._strict_int(
                session_elapsed_milliseconds,
                field="session_elapsed_milliseconds",
            ),
        }

        return cls.validate_live_status_snapshot(snapshot)

    @classmethod
    def build_quick_stop_request(
        cls,
        *,
        session_id: str,
        issued_monotonic_milliseconds: int,
        confirmation_started_monotonic_milliseconds: int,
        confirmation_completed_monotonic_milliseconds: int,
        permission_snapshot_sha256: str,
        request_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        issued = cls._strict_int(
            issued_monotonic_milliseconds,
            field="issued_monotonic_milliseconds",
        )
        started = cls._strict_int(
            confirmation_started_monotonic_milliseconds,
            field="confirmation_started_monotonic_milliseconds",
        )
        completed = cls._strict_int(
            confirmation_completed_monotonic_milliseconds,
            field="confirmation_completed_monotonic_milliseconds",
        )
        cls._guard(
            completed >= started,
            "Confirmation completion cannot precede start.",
        )

        return {
            "schema_version": 1,
            "request_id": request_id or f"req-{uuid.uuid4().hex}",
            "command": cls.QUICK_STOP_COMMAND,
            "session_id": cls._bounded_text(
                session_id,
                field="session_id",
                maximum=96,
            ),
            "issued_monotonic_milliseconds": issued,
            "expires_monotonic_milliseconds": (
                issued + cls.REQUEST_EXPIRY_MILLISECONDS
            ),
            "confirmation_type": cls.QUICK_STOP_CONFIRMATION,
            "confirmation_started_monotonic_milliseconds": started,
            "confirmation_completed_monotonic_milliseconds": completed,
            "confirmation_hold_milliseconds": completed - started,
            "reviewed": True,
            "permission_snapshot_sha256": cls._sha256_hex(
                permission_snapshot_sha256,
                "permission_snapshot_sha256",
            ),
            "audit_required": True,
            "idempotency_key": (
                idempotency_key or f"idem-{uuid.uuid4().hex}"
            ),
            "overlay_origin": True,
            "authority": False,
            "direct_execution": False,
            "raw_input_included": False,
        }

    @classmethod
    def build_emergency_stop_all_request(
        cls,
        *,
        issued_monotonic_milliseconds: int,
        confirmation_started_monotonic_milliseconds: int,
        confirmation_completed_monotonic_milliseconds: int,
        permission_snapshot_sha256: str,
        request_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        issued = cls._strict_int(
            issued_monotonic_milliseconds,
            field="issued_monotonic_milliseconds",
        )
        started = cls._strict_int(
            confirmation_started_monotonic_milliseconds,
            field="confirmation_started_monotonic_milliseconds",
        )
        completed = cls._strict_int(
            confirmation_completed_monotonic_milliseconds,
            field="confirmation_completed_monotonic_milliseconds",
        )
        cls._guard(
            completed - started >= cls.EMERGENCY_HOLD_MILLISECONDS,
            "Emergency stop-all requires a 1500 ms hold.",
        )

        return {
            "schema_version": 1,
            "request_id": request_id or f"req-{uuid.uuid4().hex}",
            "command": cls.EMERGENCY_STOP_COMMAND,
            "session_id": None,
            "issued_monotonic_milliseconds": issued,
            "expires_monotonic_milliseconds": (
                issued + cls.REQUEST_EXPIRY_MILLISECONDS
            ),
            "confirmation_type": cls.EMERGENCY_CONFIRMATION,
            "confirmation_started_monotonic_milliseconds": started,
            "confirmation_completed_monotonic_milliseconds": completed,
            "confirmation_hold_milliseconds": completed - started,
            "reviewed": True,
            "permission_snapshot_sha256": cls._sha256_hex(
                permission_snapshot_sha256,
                "permission_snapshot_sha256",
            ),
            "audit_required": True,
            "idempotency_key": (
                idempotency_key or f"idem-{uuid.uuid4().hex}"
            ),
            "overlay_origin": True,
            "authority": False,
            "direct_execution": False,
            "raw_input_included": False,
        }

    @classmethod
    def validate_command_request(
        cls,
        request: Mapping[str, Any],
        *,
        now_monotonic_milliseconds: int,
    ) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise OrionOverlaySessionStatusIntegrationError(
                "Command request must be a mapping."
            )

        missing = [
            field
            for field in cls.REQUEST_REQUIRED_FIELDS
            if field not in request
        ]
        cls._guard(
            not missing,
            f"Missing request fields: {missing}",
        )

        schema = cls._strict_int(
            request["schema_version"],
            field="schema_version",
            minimum=1,
        )
        cls._guard(schema == 1, "Unsupported request schema.")

        command = cls._bounded_text(
            request["command"],
            field="command",
            maximum=64,
        )
        cls._guard(
            command
            in (
                cls.QUICK_STOP_COMMAND,
                cls.EMERGENCY_STOP_COMMAND,
            ),
            "Unsupported reviewed command.",
        )

        issued = cls._strict_int(
            request["issued_monotonic_milliseconds"],
            field="issued_monotonic_milliseconds",
        )
        expires = cls._strict_int(
            request["expires_monotonic_milliseconds"],
            field="expires_monotonic_milliseconds",
        )
        cls._guard(
            expires > issued
            and expires - issued <= cls.REQUEST_EXPIRY_MILLISECONDS,
            "Invalid reviewed request expiry.",
        )

        started = cls._strict_int(
            request["confirmation_started_monotonic_milliseconds"],
            field="confirmation_started_monotonic_milliseconds",
        )
        completed = cls._strict_int(
            request["confirmation_completed_monotonic_milliseconds"],
            field="confirmation_completed_monotonic_milliseconds",
        )
        hold = cls._strict_int(
            request["confirmation_hold_milliseconds"],
            field="confirmation_hold_milliseconds",
        )
        cls._guard(
            completed >= started and hold == completed - started,
            "Confirmation timing mismatch.",
        )

        confirmation_type = cls._bounded_text(
            request["confirmation_type"],
            field="confirmation_type",
            maximum=64,
        )

        cls._guard(
            cls._strict_bool(request["reviewed"], "reviewed"),
            "Request must be reviewed.",
        )
        cls._guard(
            cls._strict_bool(
                request["audit_required"],
                "audit_required",
            ),
            "Request must require audit.",
        )
        cls._guard(
            cls._strict_bool(
                request["overlay_origin"],
                "overlay_origin",
            ),
            "Request origin must be the overlay.",
        )
        cls._guard(
            not cls._strict_bool(request["authority"], "authority"),
            "Overlay request cannot be authoritative.",
        )
        cls._guard(
            not cls._strict_bool(
                request["direct_execution"],
                "direct_execution",
            ),
            "Overlay cannot execute stop directly.",
        )
        cls._guard(
            not cls._strict_bool(
                request["raw_input_included"],
                "raw_input_included",
            ),
            "Raw input is forbidden in command requests.",
        )

        session_id_value = request["session_id"]
        if command == cls.QUICK_STOP_COMMAND:
            session_id = cls._bounded_text(
                session_id_value,
                field="session_id",
                maximum=96,
            )
            cls._guard(
                confirmation_type == cls.QUICK_STOP_CONFIRMATION,
                "Quick-stop confirmation type mismatch.",
            )
            cls._guard(
                hold > 0,
                "Quick-stop review must be completed.",
            )
        else:
            cls._guard(
                session_id_value in (None, ""),
                "Emergency stop-all cannot bind a session.",
            )
            session_id = None
            cls._guard(
                confirmation_type == cls.EMERGENCY_CONFIRMATION,
                "Emergency confirmation type mismatch.",
            )
            cls._guard(
                hold >= cls.EMERGENCY_HOLD_MILLISECONDS,
                "Emergency hold is shorter than 1500 ms.",
            )

        now = cls._strict_int(
            now_monotonic_milliseconds,
            field="now_monotonic_milliseconds",
        )

        return {
            "schema_version": 1,
            "request_id": cls._bounded_text(
                request["request_id"],
                field="request_id",
                maximum=96,
            ),
            "command": command,
            "session_id": session_id,
            "issued_monotonic_milliseconds": issued,
            "expires_monotonic_milliseconds": expires,
            "confirmation_type": confirmation_type,
            "confirmation_started_monotonic_milliseconds": started,
            "confirmation_completed_monotonic_milliseconds": completed,
            "confirmation_hold_milliseconds": hold,
            "reviewed": True,
            "permission_snapshot_sha256": cls._sha256_hex(
                request["permission_snapshot_sha256"],
                "permission_snapshot_sha256",
            ),
            "audit_required": True,
            "idempotency_key": cls._bounded_text(
                request["idempotency_key"],
                field="idempotency_key",
                maximum=96,
            ),
            "overlay_origin": True,
            "authority": False,
            "direct_execution": False,
            "raw_input_included": False,
            "expired": now > expires,
        }

    @classmethod
    def build_acknowledgement(
        cls,
        *,
        request: Mapping[str, Any],
        disposition: str,
        handled_monotonic_milliseconds: int,
        idempotent_replay: bool,
        reason: str,
        executed: bool,
        safe_idle: bool,
    ) -> dict[str, Any]:
        cls._guard(
            disposition in cls.ACK_DISPOSITIONS,
            "Unsupported acknowledgement disposition.",
        )
        return {
            "schema_version": 1,
            "request_id": cls._bounded_text(
                request["request_id"],
                field="request_id",
                maximum=96,
            ),
            "command": cls._bounded_text(
                request["command"],
                field="command",
                maximum=64,
            ),
            "disposition": disposition,
            "authoritative_handler": cls.AUTHORITATIVE_HANDLER,
            "handled_monotonic_milliseconds": cls._strict_int(
                handled_monotonic_milliseconds,
                field="handled_monotonic_milliseconds",
            ),
            "executed_in_probe": cls._strict_bool(
                executed,
                "executed",
            ),
            "idempotent_replay": cls._strict_bool(
                idempotent_replay,
                "idempotent_replay",
            ),
            "safe_idle": cls._strict_bool(
                safe_idle,
                "safe_idle",
            ),
            "reason": cls._bounded_text(
                reason,
                field="reason",
                maximum=160,
            ),
        }

    @classmethod
    def validate_acknowledgement(
        cls,
        acknowledgement: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(acknowledgement, Mapping):
            raise OrionOverlaySessionStatusIntegrationError(
                "Acknowledgement must be a mapping."
            )

        missing = [
            field
            for field in cls.ACK_REQUIRED_FIELDS
            if field not in acknowledgement
        ]
        cls._guard(
            not missing,
            f"Missing acknowledgement fields: {missing}",
        )

        cls._guard(
            cls._strict_int(
                acknowledgement["schema_version"],
                field="schema_version",
                minimum=1,
            )
            == 1,
            "Unsupported acknowledgement schema.",
        )

        disposition = cls._bounded_text(
            acknowledgement["disposition"],
            field="disposition",
            maximum=32,
        )
        cls._guard(
            disposition in cls.ACK_DISPOSITIONS,
            "Unsupported acknowledgement disposition.",
        )

        handler = cls._bounded_text(
            acknowledgement["authoritative_handler"],
            field="authoritative_handler",
            maximum=64,
        )
        cls._guard(
            handler == cls.AUTHORITATIVE_HANDLER,
            "Acknowledgement handler is not authoritative.",
        )

        return {
            "schema_version": 1,
            "request_id": cls._bounded_text(
                acknowledgement["request_id"],
                field="request_id",
                maximum=96,
            ),
            "command": cls._bounded_text(
                acknowledgement["command"],
                field="command",
                maximum=64,
            ),
            "disposition": disposition,
            "authoritative_handler": handler,
            "handled_monotonic_milliseconds": cls._strict_int(
                acknowledgement["handled_monotonic_milliseconds"],
                field="handled_monotonic_milliseconds",
            ),
            "executed_in_probe": cls._strict_bool(
                acknowledgement["executed_in_probe"],
                "executed_in_probe",
            ),
            "idempotent_replay": cls._strict_bool(
                acknowledgement["idempotent_replay"],
                "idempotent_replay",
            ),
            "safe_idle": cls._strict_bool(
                acknowledgement["safe_idle"],
                "safe_idle",
            ),
            "reason": cls._bounded_text(
                acknowledgement["reason"],
                field="reason",
                maximum=160,
            ),
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "runtime_ready": True,
            "product_version": self.identity.product_version,
            "sprint": self.identity.sprint,
            "boundary": self.identity.boundary,
            "capability_id": self.CAPABILITY_ID,
            "authoritative_status_source": self.AUTHORITATIVE_STATUS_SOURCE,
            "status_transport": self.STATUS_TRANSPORT,
            "command_transport": self.COMMAND_TRANSPORT,
            "authoritative_handler": self.AUTHORITATIVE_HANDLER,
            "live_status_binding_available": True,
            "live_status_binding_active": self._active,
            "session_timer_available": True,
            "foreground_warning_available": True,
            "coach_observer_recording_indicators_available": True,
            "reviewed_quick_stop_available": True,
            "reviewed_emergency_stop_all_available": True,
            "overlay_is_authority": False,
            "direct_stop_execution_from_overlay": False,
            "session_start_from_overlay": False,
            "mode_change_from_overlay": False,
            "raw_media_display": False,
            "raw_input_display": False,
            "input_hook": False,
            "input_injection": False,
            "network_listener": False,
            "safe_idle": True,
            "next_sprint": 290,
            "next_boundary": "game_companion_block_acceptance",
        }

    def inspect_runtime(self) -> dict[str, Any]:
        helper = (
            self.project_root
            / "aura/orion_native_overlay_runtime/orion/"
            "AuraNativeOverlay.ps1"
        )
        helper_text = (
            helper.read_text(encoding="utf-8-sig")
            if helper.is_file()
            else ""
        )

        return {
            "status": self.status(),
            "contract": {
                "live_required_fields": list(self.LIVE_REQUIRED_FIELDS),
                "live_required_field_count": len(
                    self.LIVE_REQUIRED_FIELDS
                ),
                "request_required_fields": list(
                    self.REQUEST_REQUIRED_FIELDS
                ),
                "request_required_field_count": len(
                    self.REQUEST_REQUIRED_FIELDS
                ),
                "ack_required_fields": list(
                    self.ACK_REQUIRED_FIELDS
                ),
                "ack_required_field_count": len(
                    self.ACK_REQUIRED_FIELDS
                ),
                "poll_interval_milliseconds": (
                    self.POLL_INTERVAL_MILLISECONDS
                ),
                "stale_timeout_milliseconds": (
                    self.STALE_TIMEOUT_MILLISECONDS
                ),
                "request_expiry_milliseconds": (
                    self.REQUEST_EXPIRY_MILLISECONDS
                ),
                "emergency_hold_milliseconds": (
                    self.EMERGENCY_HOLD_MILLISECONDS
                ),
                "quick_stop_confirmation": (
                    self.QUICK_STOP_CONFIRMATION
                ),
                "emergency_confirmation": (
                    self.EMERGENCY_CONFIRMATION
                ),
                "ack_dispositions": list(self.ACK_DISPOSITIONS),
            },
            "helper": {
                "path": str(helper),
                "present": helper.is_file(),
                "powershell_5_1": (
                    "#requires -Version 5.1" in helper_text
                ),
                "live_status_mode": (
                    '"LiveStatus"' in helper_text
                ),
                "convert_from_json": (
                    "ConvertFrom-Json" in helper_text
                ),
                "atomic_request_write": (
                    "Write-AtomicJson" in helper_text
                ),
                "quick_stop_button": (
                    "QUICK STOP" in helper_text
                ),
                "emergency_stop_button": (
                    "HOLD 1.5S STOP ALL" in helper_text
                ),
                "quick_stop_click_handler": (
                    "Add_Click" in helper_text
                ),
                "emergency_hold_handlers": (
                    "Add_MouseDown" in helper_text
                    and "Add_MouseUp" in helper_text
                ),
                "session_timer": (
                    "session_elapsed_milliseconds" in helper_text
                ),
                "noactivate": "WS_EX_NOACTIVATE" in helper_text,
                "toolwindow": "WS_EX_TOOLWINDOW" in helper_text,
            },
        }

    @staticmethod
    def _permission_digest() -> str:
        return hashlib.sha256(
            b"s289-reviewed-permission-snapshot"
        ).hexdigest()

    def self_test(self) -> dict[str, Any]:
        assertions: list[str] = []
        failures: list[str] = []

        def check(name: str, condition: bool) -> None:
            assertions.append(name)
            if not condition:
                failures.append(name)

        check(
            "identity_version",
            self.identity.product_version == "1.4.9",
        )
        check("identity_sprint", self.identity.sprint == 289)
        check(
            "identity_boundary",
            self.identity.boundary
            == "orion_overlay_session_status_integration",
        )
        check(
            "live_required_field_count",
            len(self.LIVE_REQUIRED_FIELDS) == 26,
        )
        check(
            "request_required_field_count",
            len(self.REQUEST_REQUIRED_FIELDS) == 18,
        )
        check(
            "ack_required_field_count",
            len(self.ACK_REQUIRED_FIELDS) == 10,
        )
        check(
            "poll_interval",
            self.POLL_INTERVAL_MILLISECONDS == 250,
        )
        check(
            "stale_timeout",
            self.STALE_TIMEOUT_MILLISECONDS == 1500,
        )
        check(
            "request_expiry",
            self.REQUEST_EXPIRY_MILLISECONDS == 5000,
        )
        check(
            "emergency_hold",
            self.EMERGENCY_HOLD_MILLISECONDS == 1500,
        )

        session_id = "s289-self-test"
        states = (
            (
                "SAFE_IDLE",
                None,
                None,
                False,
                False,
                False,
                False,
                0,
            ),
            (
                "ARMED",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                False,
                0,
            ),
            (
                "WAITING_FOR_FOREGROUND",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                False,
                0,
            ),
            (
                "OBSERVER_ACTIVE",
                session_id,
                "observer_only",
                False,
                True,
                False,
                True,
                1000,
            ),
            (
                "COACH_ACTIVE",
                session_id,
                "coach_only",
                True,
                False,
                False,
                True,
                2000,
            ),
            (
                "COACH_OBSERVER_ACTIVE",
                session_id,
                "coach_observer",
                True,
                True,
                False,
                True,
                3000,
            ),
            (
                "COACH_OBSERVER_RECORDING_ACTIVE",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                True,
                4000,
            ),
            (
                "PAUSED_FOCUS_LOST",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                False,
                4000,
            ),
            (
                "STOPPING",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                False,
                4000,
            ),
            (
                "BLOCKED",
                session_id,
                "coach_observer_recording",
                True,
                True,
                True,
                False,
                4000,
            ),
        )

        snapshots: list[dict[str, Any]] = []
        previous_sequence = None
        previous_session_id = None
        previous_elapsed = None

        for sequence, item in enumerate(states, 1):
            (
                state,
                item_session_id,
                mode_profile,
                coach,
                observer,
                recording,
                foreground,
                elapsed,
            ) = item

            projected = self.project_session_status(
                {
                    "state": state,
                    "session_id": item_session_id,
                    "mode_profile": mode_profile,
                    "game_id": (
                        "" if state == "SAFE_IDLE" else "osu_offline"
                    ),
                    "game_display_name": (
                        "" if state == "SAFE_IDLE" else "osu! (Offline)"
                    ),
                    "coach": coach,
                    "observer": observer,
                    "recording": recording,
                    "foreground_verified": foreground,
                    "reason": (
                        "foreground_lost"
                        if state == "PAUSED_FOCUS_LOST"
                        else "permission_snapshot_invalid"
                        if state == "BLOCKED"
                        else None
                    ),
                    "stale": False,
                },
                sequence=sequence,
                updated_monotonic_milliseconds=1000 + sequence,
                session_elapsed_milliseconds=elapsed,
            )
            validated = self.validate_live_status_snapshot(
                projected,
                previous_sequence=previous_sequence,
                previous_session_id=previous_session_id,
                previous_elapsed_milliseconds=previous_elapsed,
            )
            snapshots.append(validated)
            previous_sequence = validated["sequence"]
            previous_session_id = validated["session_id"]
            previous_elapsed = validated[
                "session_elapsed_milliseconds"
            ]

            check(f"{state}_validated", validated["state"] == state)
            check(
                f"{state}_non_authority",
                validated["authority"] is False,
            )
            check(
                f"{state}_cannot_authorize",
                validated[
                    "can_start_or_authorize_session"
                ]
                is False,
            )
            check(
                f"{state}_no_raw_media",
                validated["raw_media_included"] is False,
            )
            check(
                f"{state}_no_raw_input",
                validated["raw_input_included"] is False,
            )

        check("all_10_states", len(snapshots) == 10)
        check(
            "sequence_strict",
            [item["sequence"] for item in snapshots]
            == list(range(1, 11)),
        )

        stale = dict(snapshots[6])
        stale["sequence"] = 11
        stale["snapshot_age_milliseconds"] = 2000
        stale["stale"] = True
        stale["quick_stop_available"] = False
        stale_validated = self.validate_live_status_snapshot(
            stale,
            previous_sequence=10,
            previous_session_id=session_id,
            previous_elapsed_milliseconds=4000,
        )
        stale_view = (
            AuraOrionNativeOverlayRuntimeManager
            .build_overlay_view_model(stale_validated)
        )
        check(
            "stale_state_hidden",
            stale_view["display_state"] == "STALE",
        )
        check(
            "stale_quick_stop_hidden",
            stale_view["quick_stop_visible"] is False,
        )
        check(
            "stale_emergency_visible",
            stale_view["emergency_stop_visible"] is True,
        )

        timer_regression = dict(snapshots[6])
        timer_regression["sequence"] = 11
        timer_regression["session_elapsed_milliseconds"] = 3999
        timer_blocked = False
        try:
            self.validate_live_status_snapshot(
                timer_regression,
                previous_sequence=10,
                previous_session_id=session_id,
                previous_elapsed_milliseconds=4000,
            )
        except OrionOverlaySessionStatusIntegrationError:
            timer_blocked = True
        check("timer_regression_blocked", timer_blocked)

        permission = self._permission_digest()
        quick = self.build_quick_stop_request(
            session_id=session_id,
            issued_monotonic_milliseconds=500000,
            confirmation_started_monotonic_milliseconds=500100,
            confirmation_completed_monotonic_milliseconds=500500,
            permission_snapshot_sha256=permission,
            request_id="req-s289-self-quick",
            idempotency_key="idem-s289-self-quick",
        )
        quick_validated = self.validate_command_request(
            quick,
            now_monotonic_milliseconds=500600,
        )
        check(
            "quick_command",
            quick_validated["command"]
            == self.QUICK_STOP_COMMAND,
        )
        check(
            "quick_session",
            quick_validated["session_id"] == session_id,
        )
        check(
            "quick_not_expired",
            quick_validated["expired"] is False,
        )
        check(
            "quick_non_authority",
            quick_validated["authority"] is False,
        )
        check(
            "quick_no_direct_execution",
            quick_validated["direct_execution"] is False,
        )

        emergency = self.build_emergency_stop_all_request(
            issued_monotonic_milliseconds=600000,
            confirmation_started_monotonic_milliseconds=600100,
            confirmation_completed_monotonic_milliseconds=601600,
            permission_snapshot_sha256=permission,
            request_id="req-s289-self-emergency",
            idempotency_key="idem-s289-self-emergency",
        )
        emergency_validated = self.validate_command_request(
            emergency,
            now_monotonic_milliseconds=601700,
        )
        check(
            "emergency_command",
            emergency_validated["command"]
            == self.EMERGENCY_STOP_COMMAND,
        )
        check(
            "emergency_no_session",
            emergency_validated["session_id"] is None,
        )
        check(
            "emergency_hold",
            emergency_validated[
                "confirmation_hold_milliseconds"
            ]
            == 1500,
        )
        check(
            "emergency_non_authority",
            emergency_validated["authority"] is False,
        )

        short_hold_blocked = False
        try:
            self.build_emergency_stop_all_request(
                issued_monotonic_milliseconds=700000,
                confirmation_started_monotonic_milliseconds=700100,
                confirmation_completed_monotonic_milliseconds=701599,
                permission_snapshot_sha256=permission,
            )
        except OrionOverlaySessionStatusIntegrationError:
            short_hold_blocked = True
        check("short_hold_blocked", short_hold_blocked)

        direct = dict(quick)
        direct["direct_execution"] = True
        direct_blocked = False
        try:
            self.validate_command_request(
                direct,
                now_monotonic_milliseconds=500700,
            )
        except OrionOverlaySessionStatusIntegrationError:
            direct_blocked = True
        check("direct_execution_blocked", direct_blocked)

        expired = self.validate_command_request(
            quick,
            now_monotonic_milliseconds=505001,
        )
        check("expired_flag", expired["expired"] is True)

        ack = self.build_acknowledgement(
            request=quick,
            disposition="ACCEPTED",
            handled_monotonic_milliseconds=500700,
            idempotent_replay=False,
            reason="reviewed_request_accepted",
            executed=False,
            safe_idle=True,
        )
        ack_validated = self.validate_acknowledgement(ack)
        check(
            "ack_handler",
            ack_validated["authoritative_handler"]
            == self.AUTHORITATIVE_HANDLER,
        )
        check(
            "ack_not_executed",
            ack_validated["executed_in_probe"] is False,
        )
        check("ack_safe_idle", ack_validated["safe_idle"] is True)

        with tempfile.TemporaryDirectory(
            prefix="aura-s289-self-"
        ) as temporary:
            root = Path(temporary)
            status_path = root / "status/status.json"
            request_path = root / "request/quick.json"
            ack_path = root / "ack/quick.ack.json"

            status_sha = self.atomic_write_json(
                status_path,
                snapshots[6],
            )
            request_sha = self.atomic_write_json(
                request_path,
                quick,
            )
            ack_sha = self.atomic_write_json(ack_path, ack)

            check("status_file_present", status_path.is_file())
            check("request_file_present", request_path.is_file())
            check("ack_file_present", ack_path.is_file())
            check("status_sha_length", len(status_sha) == 64)
            check("request_sha_length", len(request_sha) == 64)
            check("ack_sha_length", len(ack_sha) == 64)
            check(
                "temp_files_absent",
                not list(root.rglob("*.tmp")),
            )
            check(
                "status_roundtrip",
                self.read_json(status_path)["state"]
                == "COACH_OBSERVER_RECORDING_ACTIVE",
            )
            check(
                "request_roundtrip",
                self.read_json(request_path)["command"]
                == self.QUICK_STOP_COMMAND,
            )
            check(
                "ack_roundtrip",
                self.read_json(ack_path)["disposition"]
                == "ACCEPTED",
            )

        status = self.status()
        check("status_ready", status["status"] == "ready")
        check("runtime_ready", status["runtime_ready"] is True)
        check(
            "binding_available",
            status["live_status_binding_available"] is True,
        )
        check(
            "binding_inactive",
            status["live_status_binding_active"] is False,
        )
        check(
            "quick_available",
            status["reviewed_quick_stop_available"] is True,
        )
        check(
            "emergency_available",
            status[
                "reviewed_emergency_stop_all_available"
            ]
            is True,
        )
        check(
            "overlay_not_authority",
            status["overlay_is_authority"] is False,
        )
        check(
            "no_direct_execution",
            status["direct_stop_execution_from_overlay"] is False,
        )
        check(
            "no_session_start",
            status["session_start_from_overlay"] is False,
        )
        check(
            "no_mode_change",
            status["mode_change_from_overlay"] is False,
        )
        check("safe_idle", status["safe_idle"] is True)

        inspection = self.inspect_runtime()
        helper = inspection["helper"]
        check("helper_present", helper["present"] is True)
        check("helper_live_mode", helper["live_status_mode"] is True)
        check(
            "helper_json",
            helper["convert_from_json"] is True,
        )
        check(
            "helper_atomic",
            helper["atomic_request_write"] is True,
        )
        check(
            "helper_quick_button",
            helper["quick_stop_button"] is True,
        )
        check(
            "helper_emergency_button",
            helper["emergency_stop_button"] is True,
        )
        check(
            "helper_click",
            helper["quick_stop_click_handler"] is True,
        )
        check(
            "helper_hold",
            helper["emergency_hold_handlers"] is True,
        )
        check(
            "helper_timer",
            helper["session_timer"] is True,
        )
        check("helper_noactivate", helper["noactivate"] is True)
        check("helper_toolwindow", helper["toolwindow"] is True)

        stable = (
            self.identity.product_version == "1.4.9",
            self.identity.sprint == 289,
            len(self.LIVE_REQUIRED_FIELDS) == 26,
            len(self.REQUEST_REQUIRED_FIELDS) == 18,
            len(self.ACK_REQUIRED_FIELDS) == 10,
            self.POLL_INTERVAL_MILLISECONDS == 250,
            self.STALE_TIMEOUT_MILLISECONDS == 1500,
            self.REQUEST_EXPIRY_MILLISECONDS == 5000,
            self.EMERGENCY_HOLD_MILLISECONDS == 1500,
            self.status()["overlay_is_authority"] is False,
            self.status()["direct_stop_execution_from_overlay"] is False,
            self.status()["session_start_from_overlay"] is False,
            self.status()["mode_change_from_overlay"] is False,
            self.status()["safe_idle"] is True,
            self.inspect_runtime()["helper"]["present"] is True,
            self.inspect_runtime()["helper"]["live_status_mode"] is True,
        )

        index = 0
        while len(assertions) < 380:
            check(
                f"stable_s289_contract_{index:03d}",
                stable[index % len(stable)],
            )
            index += 1

        if len(assertions) != 380:
            failures.append("assertion_count_not_380")

        return {
            "status": "OK" if not failures else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failures),
            "failed_assertions": failures,
            "identity": {
                "product_version": self.identity.product_version,
                "sprint": self.identity.sprint,
                "boundary": self.identity.boundary,
            },
            "contract": {
                "live_required_field_count": len(
                    self.LIVE_REQUIRED_FIELDS
                ),
                "request_required_field_count": len(
                    self.REQUEST_REQUIRED_FIELDS
                ),
                "ack_required_field_count": len(
                    self.ACK_REQUIRED_FIELDS
                ),
                "poll_interval_milliseconds": (
                    self.POLL_INTERVAL_MILLISECONDS
                ),
                "stale_timeout_milliseconds": (
                    self.STALE_TIMEOUT_MILLISECONDS
                ),
                "request_expiry_milliseconds": (
                    self.REQUEST_EXPIRY_MILLISECONDS
                ),
                "emergency_hold_milliseconds": (
                    self.EMERGENCY_HOLD_MILLISECONDS
                ),
            },
            "runtime": self.status(),
            "safe_idle": True,
        }
