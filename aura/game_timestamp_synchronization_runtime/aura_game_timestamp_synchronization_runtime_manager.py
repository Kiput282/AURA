"""Sprint 286 shared game timestamp synchronization runtime."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


class GameTimestampSynchronizationRuntimeError(RuntimeError):
    """Raised when a Sprint 286 clock-envelope contract is invalid."""


@dataclass(frozen=True)
class GameTimestampSynchronizationIdentity:
    component_name: str = "game_timestamp_synchronization_runtime"
    component_version: str = "0.1.0"
    product_version: str = "1.4.6"
    sprint: int = 286
    boundary: str = "game_timestamp_synchronization"
    protocol_version: str = "aura-game-clock-envelope-v1"
    capability_id: str = (
        "orion.game.synchronize_stream_timestamps.bounded_session"
    )
    reference_game_id: str = "osu_offline"
    atlas_role: str = "ATLAS_GAME_TIMESTAMP_REVIEW_AUTHORITY"
    orion_role: str = "ORION_MONOTONIC_SESSION_CLOCK_SOURCE"


class AuraGameTimestampSynchronizationRuntimeManager:
    IDENTITY = GameTimestampSynchronizationIdentity()
    PROTOCOL_VERSION = IDENTITY.protocol_version
    CAPABILITY_ID = IDENTITY.capability_id
    REFERENCE_GAME_ID = IDENTITY.reference_game_id

    APPROVAL_TEXT = "APPROVE BOUNDED MULTISTREAM CLOCK SESSION"
    REVIEW_TEXT = "REVIEW BOUNDED MULTISTREAM CLOCK RECEIPT"

    MAX_DURATION_MILLISECONDS = 2000
    DEFAULT_DURATION_MILLISECONDS = 1200
    MAX_LOGICAL_SAMPLES = 1024
    MAX_PERMISSION_TTL_SECONDS = 30
    MAX_PREVIEW_TTL_SECONDS = 60
    MAX_REQUEST_AGE_SECONDS = 15
    MAX_CLOCK_FREQUENCY_HZ = 10_000_000_000

    STREAMS = (
        "game_window_capture",
        "game_audio_capture",
        "game_input_telemetry",
    )
    STREAM_CADENCE_MILLISECONDS = {
        "game_window_capture": 16,
        "game_audio_capture": 10,
        "game_input_telemetry": 17,
    }
    ALLOWED_MODES = {
        "coach_only",
        "observer_only",
        "coach_observer",
        "coach_observer_recording",
    }

    CLOSED_FLAGS = (
        "system_clock_change_allowed",
        "ntp_configuration_change_allowed",
        "time_service_change_allowed",
        "atlas_clock_ordering_allowed",
        "wall_clock_sole_ordering_allowed",
        "raw_monotonic_ticks_export_allowed",
        "raw_stream_export_allowed",
        "window_capture_allowed",
        "audio_capture_allowed",
        "input_telemetry_allowed",
        "keyboard_read_allowed",
        "mouse_read_allowed",
        "input_hook_allowed",
        "raw_input_allowed",
        "input_injection_allowed",
        "long_running_drift_compensation_allowed",
        "automatic_resampling_allowed",
        "frame_interpolation_allowed",
        "audio_time_stretching_allowed",
        "recording_orchestration_allowed",
        "observer_orchestration_allowed",
        "coach_runtime_allowed",
        "autonomous_gameplay_allowed",
    )

    PREVIEW_FIELDS = {
        "schema_version", "preview_type", "protocol_version",
        "capability_id", "request_id", "agent_id", "device_id",
        "game_id", "mode_id", "action_type", "implementation",
        "reference_clock", "utc_anchor_type", "duration_milliseconds",
        "maximum_logical_samples", "streams",
        "stream_cadence_milliseconds", "shared_session_epoch_required",
        "explicit_clock_frequency_required", "monotonic_ordering_required",
        "fail_closed_on_clock_discontinuity", "metadata_only_evidence",
        *CLOSED_FLAGS,
        "created_at_utc", "expires_at_utc", "target_binding_digest",
        "preview_digest",
    }
    PERMISSION_FIELDS = {
        "schema_version", "permission_type", "protocol_version",
        "capability_id", "permission_id", "preview_digest", "request_id",
        "agent_id", "device_id", "game_id", "mode_id", "action_type",
        "duration_milliseconds", "maximum_logical_samples", "streams",
        "single_use", "issued_at_utc", "expires_at_utc",
        "target_binding_digest", "permission_digest",
    }
    REQUEST_FIELDS = {
        "schema_version", "request_type", "protocol_version",
        "capability_id", "request_id", "permission_id",
        "permission_digest", "preview_digest", "agent_id", "device_id",
        "game_id", "mode_id", "action_type", "implementation",
        "reference_clock", "utc_anchor_type", "duration_milliseconds",
        "maximum_logical_samples", "streams",
        "stream_cadence_milliseconds", "shared_session_epoch_required",
        "explicit_clock_frequency_required", "monotonic_ordering_required",
        "fail_closed_on_clock_discontinuity", "metadata_only_evidence",
        *CLOSED_FLAGS,
        "requested_at_utc", "sequence", "target_binding_digest",
        "request_digest",
    }
    ENVELOPE_FIELDS = {
        "session_id", "clock_id", "clock_frequency_hz",
        "session_epoch_utc", "session_epoch_monotonic_ticks_sha256",
        "stream_id", "stream_start_monotonic_ticks_sha256",
        "stream_start_relative_ms", "sample_relative_ms", "sequence",
    }
    STREAM_SUMMARY_FIELDS = {
        "configured_cadence_milliseconds", "logical_sample_count",
        "first_sequence", "last_sequence", "first_relative_milliseconds",
        "last_relative_milliseconds", "maximum_observed_gap_milliseconds",
        "sequence_contiguous", "timestamps_monotonic_non_decreasing",
        "samples_within_bounded_window", "shared_session_epoch",
        "raw_logical_events_included",
    }
    METADATA_FIELDS = {
        "session_id", "clock_id", "clock_frequency_hz",
        "session_epoch_utc", "session_epoch_monotonic_ticks_sha256",
        "requested_duration_milliseconds", "minimum_sample_relative_ms",
        "maximum_sample_relative_ms", "logical_sample_count",
        "stream_count", "streams", "shared_session_epoch",
        "all_sequences_contiguous",
        "all_timestamps_monotonic_non_decreasing",
        "all_samples_within_bounded_window", "clock_discontinuity_detected",
        "utc_used_for_anchor_only", "atlas_clock_used_for_ordering",
        "raw_monotonic_ticks_included", "raw_logical_events_included",
        "metadata_digest",
    }
    RECEIPT_FIELDS = {
        "schema_version", "receipt_type", "protocol_version",
        "capability_id", "request_id", "permission_id", "request_digest",
        "agent_id", "device_id", "game_id", "mode_id", "action_type",
        "probe_succeeded", "captured_at_utc", "failure_code",
        "system_clock_read", "monotonic_clock_read", "system_clock_changed",
        "ntp_configuration_changed", "time_service_changed",
        "atlas_clock_used_for_ordering", "wall_clock_sole_ordering",
        "clock_discontinuity_detected", "raw_monotonic_ticks_included",
        "raw_stream_exported", "raw_logical_events_included",
        "window_capture_started", "audio_capture_started",
        "input_telemetry_started", "keyboard_read", "mouse_read",
        "input_hook_installed", "raw_input_registered",
        "input_injection_executed", "long_running_drift_compensation_started",
        "automatic_resampling_started", "frame_interpolation_started",
        "audio_time_stretching_started", "recording_orchestration_started",
        "observer_orchestration_started", "coach_runtime_started",
        "autonomous_gameplay_started", "target_binding_digest", "metadata",
        "receipt_digest",
    }

    def __init__(
        self,
        *,
        project_root: Path | str,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._previews: dict[str, dict[str, Any]] = {}
        self._permissions: dict[str, dict[str, Any]] = {}
        self._consumed: set[str] = set()
        self._authorized: dict[str, dict[str, Any]] = {}
        self._reviewed: set[str] = set()
        self._counter = 0

    @staticmethod
    def _canonical(value: Mapping[str, Any]) -> bytes:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")

    @classmethod
    def _digest(cls, value: Mapping[str, Any]) -> str:
        return hashlib.sha256(cls._canonical(value)).hexdigest()

    @classmethod
    def _signed(cls, value: Mapping[str, Any], field: str) -> str:
        unsigned = dict(value)
        unsigned.pop(field, None)
        return cls._digest(unsigned)

    def _now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock must be timezone-aware."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _fmt(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )

    @staticmethod
    def _time(value: Any, label: str) -> datetime:
        if not isinstance(value, str) or not value.endswith("Z"):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        try:
            return datetime.fromisoformat(
                value[:-1] + "+00:00"
            ).astimezone(timezone.utc)
        except ValueError as exc:
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            ) from exc

    @staticmethod
    def _id(value: Any, label: str) -> str:
        if (
            not isinstance(value, str)
            or not value
            or len(value) > 160
            or re.fullmatch(r"[A-Za-z0-9_.:!-]+", value) is None
        ):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        return value

    @staticmethod
    def _sha(value: Any, label: str) -> str:
        if (
            not isinstance(value, str)
            or re.fullmatch(r"[0-9a-f]{64}", value) is None
        ):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        return value

    @staticmethod
    def _positive_int(value: Any, label: str) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value <= 0
        ):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        return value

    @staticmethod
    def _finite_nonnegative(value: Any, label: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        number = float(value)
        if number != number or number in (float("inf"), float("-inf")):
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        if number < 0.0:
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} is invalid."
            )
        return number

    @staticmethod
    def _exact_fields(
        value: Mapping[str, Any],
        expected: set[str],
        label: str,
    ) -> None:
        if set(value) != expected:
            raise GameTimestampSynchronizationRuntimeError(
                f"{label} fields are invalid."
            )

    def _next(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:04d}"

    def identity(self) -> dict[str, Any]:
        return asdict(self.IDENTITY)

    def capability_declaration(self) -> dict[str, Any]:
        return {
            "capability_id": self.CAPABILITY_ID,
            "source": "game_timestamp_synchronization_runtime",
            "version": "1.0",
            "mode": "explicit_bounded_shared_monotonic_session_clock",
            "constraints": {
                "reference_game_id": self.REFERENCE_GAME_ID,
                "clock_host": "ORION",
                "review_authority": "ATLAS",
                "reference_clock": "ORION_MONOTONIC_HIGH_RESOLUTION_CLOCK",
                "utc_anchor_type": "ORION_UTC_TIMESTAMP_AT_SESSION_EPOCH",
                "streams": list(self.STREAMS),
                "stream_cadence_milliseconds": dict(
                    self.STREAM_CADENCE_MILLISECONDS
                ),
                "shared_session_epoch": True,
                "explicit_clock_frequency": True,
                "monotonic_non_decreasing_per_stream": True,
                "fail_closed_on_clock_discontinuity": True,
                "duration_limit_milliseconds": (
                    self.MAX_DURATION_MILLISECONDS
                ),
                "maximum_logical_samples": self.MAX_LOGICAL_SAMPLES,
                "metadata_only_evidence_to_atlas": True,
                "utc_used_for_anchor_only": True,
                "atlas_clock_used_for_ordering": False,
                "wall_clock_sole_ordering": False,
                "system_clock_change": False,
                "ntp_configuration_change": False,
                "time_service_change": False,
                "raw_monotonic_tick_export": False,
                "raw_stream_export": False,
                "window_capture": False,
                "audio_capture": False,
                "input_telemetry": False,
                "keyboard_read": False,
                "mouse_read": False,
                "input_hook": False,
                "raw_input_registration": False,
                "input_injection": False,
                "long_running_drift_compensation": False,
                "automatic_resampling": False,
                "frame_interpolation": False,
                "audio_time_stretching": False,
                "recording_orchestration": False,
                "observer_orchestration": False,
                "coach_runtime": False,
                "autonomous_gameplay": False,
            },
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "runtime_ready": True,
            "safe_idle": True,
            "current_state": "safe_idle",
            "reason": "shared_monotonic_session_clock_ready_bounded_only",
            "reference_game_id": self.REFERENCE_GAME_ID,
            "clock_host": "ORION",
            "review_authority": "ATLAS",
            "game_timestamp_synchronization_available": True,
            "game_timestamp_synchronization_active": False,
            "shared_session_clock_active": False,
            "window_alignment_active": False,
            "audio_alignment_active": False,
            "input_alignment_active": False,
            "system_clock_change_active": False,
            "ntp_configuration_change_active": False,
            "time_service_change_active": False,
            "atlas_clock_ordering_active": False,
            "raw_monotonic_tick_export_active": False,
            "raw_stream_export_active": False,
            "window_capture_active": False,
            "audio_capture_active": False,
            "input_telemetry_active": False,
            "keyboard_read_active": False,
            "mouse_read_active": False,
            "input_hook_active": False,
            "raw_input_active": False,
            "input_injection_active": False,
            "long_running_drift_compensation_active": False,
            "automatic_resampling_active": False,
            "frame_interpolation_active": False,
            "audio_time_stretching_active": False,
            "recording_orchestration_active": False,
            "observer_orchestration_active": False,
            "coach_runtime_active": False,
            "autonomous_gameplay_active": False,
            "next_sprint": 287,
            "next_boundary": "game_session_orchestration",
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "identity": self.identity(),
            "capability": self.capability_declaration(),
            "status": self.status(),
            "flow": [
                "game_detected_pending_review",
                "clock_preview_created",
                "operator_approval",
                "single_use_permission_issued",
                "bounded_clock_request_authorized",
                "orion_shared_epoch_created",
                "three_stream_envelopes_validated",
                "metadata_receipt_reviewed",
                "return_safe_idle",
            ],
            "failure_states": [
                "missing_game_review",
                "invalid_mode",
                "invalid_approval",
                "expired_preview",
                "expired_permission",
                "permission_reuse",
                "clock_identity_mismatch",
                "clock_frequency_invalid",
                "session_epoch_mismatch",
                "stream_set_mismatch",
                "sequence_gap",
                "timestamp_regression",
                "sample_outside_bound",
                "clock_discontinuity",
                "raw_tick_export_attempt",
                "raw_stream_export_attempt",
                "system_clock_change_attempt",
                "capture_or_input_read_attempt",
            ],
            "schemas": {
                "preview_fields": sorted(self.PREVIEW_FIELDS),
                "permission_fields": sorted(self.PERMISSION_FIELDS),
                "request_fields": sorted(self.REQUEST_FIELDS),
                "envelope_fields": sorted(self.ENVELOPE_FIELDS),
                "stream_summary_fields": sorted(
                    self.STREAM_SUMMARY_FIELDS
                ),
                "metadata_fields": sorted(self.METADATA_FIELDS),
                "receipt_fields": sorted(self.RECEIPT_FIELDS),
            },
        }

    def _target_binding(
        self,
        *,
        agent_id: str,
        device_id: str,
        game_id: str,
        mode_id: str,
    ) -> str:
        return self._digest(
            {
                "agent_id": agent_id,
                "device_id": device_id,
                "game_id": game_id,
                "mode_id": mode_id,
                "capability_id": self.CAPABILITY_ID,
            }
        )

    def build_clock_preview(
        self,
        review: Mapping[str, Any],
        *,
        mode_id: str,
        request_id: str | None = None,
        duration_milliseconds: int = DEFAULT_DURATION_MILLISECONDS,
        created_at_utc: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(review, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Game review is required."
            )
        if review.get("status") != "game_detected_pending_review":
            raise GameTimestampSynchronizationRuntimeError(
                "Game review state is invalid."
            )
        if review.get("prompt_created") is not True:
            raise GameTimestampSynchronizationRuntimeError(
                "Visible game review prompt is required."
            )
        if review.get("safe_idle") is not True:
            raise GameTimestampSynchronizationRuntimeError(
                "Game review must begin from safe idle."
            )
        if mode_id not in self.ALLOWED_MODES:
            raise GameTimestampSynchronizationRuntimeError(
                "Mode is invalid."
            )
        if (
            isinstance(duration_milliseconds, bool)
            or not isinstance(duration_milliseconds, int)
            or duration_milliseconds < 500
            or duration_milliseconds > self.MAX_DURATION_MILLISECONDS
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Duration is invalid."
            )
        detected = review.get("detected_game")
        if not isinstance(detected, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Detected game metadata is required."
            )
        game_id = self._id(detected.get("game_id"), "game_id")
        if game_id != self.REFERENCE_GAME_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Only the reviewed reference game is supported."
            )
        agent_id = self._id(review.get("agent_id"), "agent_id")
        device_id = self._id(review.get("device_id"), "device_id")
        now = (
            self._time(created_at_utc, "created_at_utc")
            if created_at_utc is not None
            else self._now()
        )
        request = self._id(
            request_id or self._next("clock-request"),
            "request_id",
        )
        target_binding = self._target_binding(
            agent_id=agent_id,
            device_id=device_id,
            game_id=game_id,
            mode_id=mode_id,
        )
        preview: dict[str, Any] = {
            "schema_version": 1,
            "preview_type": "aura_game_clock_session_preview",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": request,
            "agent_id": agent_id,
            "device_id": device_id,
            "game_id": game_id,
            "mode_id": mode_id,
            "action_type": "bounded_multistream_clock_session",
            "implementation": (
                "dotnet_stopwatch_shared_session_clock_envelope"
            ),
            "reference_clock": (
                "ORION_MONOTONIC_HIGH_RESOLUTION_CLOCK"
            ),
            "utc_anchor_type": (
                "ORION_UTC_TIMESTAMP_AT_SESSION_EPOCH"
            ),
            "duration_milliseconds": duration_milliseconds,
            "maximum_logical_samples": self.MAX_LOGICAL_SAMPLES,
            "streams": list(self.STREAMS),
            "stream_cadence_milliseconds": dict(
                self.STREAM_CADENCE_MILLISECONDS
            ),
            "shared_session_epoch_required": True,
            "explicit_clock_frequency_required": True,
            "monotonic_ordering_required": True,
            "fail_closed_on_clock_discontinuity": True,
            "metadata_only_evidence": True,
            **{field: False for field in self.CLOSED_FLAGS},
            "created_at_utc": self._fmt(now),
            "expires_at_utc": self._fmt(
                now + timedelta(seconds=self.MAX_PREVIEW_TTL_SECONDS)
            ),
            "target_binding_digest": target_binding,
        }
        preview["preview_digest"] = self._signed(
            preview, "preview_digest"
        )
        validated = self.validate_clock_preview(preview)
        self._previews[validated["preview_digest"]] = deepcopy(validated)
        return validated

    def validate_clock_preview(
        self,
        preview: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(preview, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview is invalid."
            )
        value = deepcopy(dict(preview))
        self._exact_fields(value, self.PREVIEW_FIELDS, "preview")
        if value["schema_version"] != 1:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview schema is invalid."
            )
        if value["preview_type"] != "aura_game_clock_session_preview":
            raise GameTimestampSynchronizationRuntimeError(
                "Preview type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview capability is invalid."
            )
        for key in ("request_id", "agent_id", "device_id", "game_id"):
            self._id(value[key], key)
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview game is invalid."
            )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview mode is invalid."
            )
        if value["action_type"] != "bounded_multistream_clock_session":
            raise GameTimestampSynchronizationRuntimeError(
                "Preview action is invalid."
            )
        if value["implementation"] != (
            "dotnet_stopwatch_shared_session_clock_envelope"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview implementation is invalid."
            )
        if value["reference_clock"] != (
            "ORION_MONOTONIC_HIGH_RESOLUTION_CLOCK"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview reference clock is invalid."
            )
        if value["utc_anchor_type"] != (
            "ORION_UTC_TIMESTAMP_AT_SESSION_EPOCH"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview UTC anchor is invalid."
            )
        duration = self._positive_int(
            value["duration_milliseconds"], "duration_milliseconds"
        )
        if duration < 500 or duration > self.MAX_DURATION_MILLISECONDS:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview duration exceeds the bounded contract."
            )
        if value["maximum_logical_samples"] != self.MAX_LOGICAL_SAMPLES:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview sample limit is invalid."
            )
        if value["streams"] != list(self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview stream set is invalid."
            )
        if value["stream_cadence_milliseconds"] != dict(
            self.STREAM_CADENCE_MILLISECONDS
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview stream cadence is invalid."
            )
        for key in (
            "shared_session_epoch_required",
            "explicit_clock_frequency_required",
            "monotonic_ordering_required",
            "fail_closed_on_clock_discontinuity",
            "metadata_only_evidence",
        ):
            if value[key] is not True:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Preview guard {key} is invalid."
                )
        for field in self.CLOSED_FLAGS:
            if value[field] is not False:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Preview closed flag {field} is invalid."
                )
        created = self._time(value["created_at_utc"], "created_at_utc")
        expires = self._time(value["expires_at_utc"], "expires_at_utc")
        if expires <= created or (expires - created).total_seconds() > 60:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview lifetime is invalid."
            )
        expected_binding = self._target_binding(
            agent_id=value["agent_id"],
            device_id=value["device_id"],
            game_id=value["game_id"],
            mode_id=value["mode_id"],
        )
        if value["target_binding_digest"] != expected_binding:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview target binding is invalid."
            )
        if value["preview_digest"] != self._signed(
            value, "preview_digest"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Preview digest is invalid."
            )
        return value

    def grant_clock_permission(
        self,
        preview: Mapping[str, Any],
        *,
        confirmation: str,
        permission_id: str | None = None,
        issued_at_utc: str | None = None,
    ) -> dict[str, Any]:
        if confirmation != self.APPROVAL_TEXT:
            raise GameTimestampSynchronizationRuntimeError(
                "Exact clock-session approval is required."
            )
        validated = self.validate_clock_preview(preview)
        now = (
            self._time(issued_at_utc, "issued_at_utc")
            if issued_at_utc is not None
            else self._now()
        )
        created = self._time(
            validated["created_at_utc"], "created_at_utc"
        )
        expires = self._time(
            validated["expires_at_utc"], "expires_at_utc"
        )
        if now < created or now > expires:
            raise GameTimestampSynchronizationRuntimeError(
                "Preview is not active."
            )
        permission: dict[str, Any] = {
            "schema_version": 1,
            "permission_type": "aura_game_clock_session_permission",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "permission_id": self._id(
                permission_id or self._next("clock-permission"),
                "permission_id",
            ),
            "preview_digest": validated["preview_digest"],
            "request_id": validated["request_id"],
            "agent_id": validated["agent_id"],
            "device_id": validated["device_id"],
            "game_id": validated["game_id"],
            "mode_id": validated["mode_id"],
            "action_type": validated["action_type"],
            "duration_milliseconds": validated["duration_milliseconds"],
            "maximum_logical_samples": validated[
                "maximum_logical_samples"
            ],
            "streams": list(validated["streams"]),
            "single_use": True,
            "issued_at_utc": self._fmt(now),
            "expires_at_utc": self._fmt(
                now + timedelta(seconds=self.MAX_PERMISSION_TTL_SECONDS)
            ),
            "target_binding_digest": validated[
                "target_binding_digest"
            ],
        }
        permission["permission_digest"] = self._signed(
            permission, "permission_digest"
        )
        result = self.validate_clock_permission(permission)
        self._permissions[result["permission_digest"]] = deepcopy(result)
        return result

    def validate_clock_permission(
        self,
        permission: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(permission, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Permission is invalid."
            )
        value = deepcopy(dict(permission))
        self._exact_fields(value, self.PERMISSION_FIELDS, "permission")
        if value["schema_version"] != 1:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission schema is invalid."
            )
        if value["permission_type"] != (
            "aura_game_clock_session_permission"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Permission type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission capability is invalid."
            )
        for key in (
            "permission_id", "request_id", "agent_id", "device_id",
            "game_id",
        ):
            self._id(value[key], key)
        self._sha(value["preview_digest"], "preview_digest")
        self._sha(value["target_binding_digest"], "target_binding_digest")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission game is invalid."
            )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission mode is invalid."
            )
        if value["action_type"] != "bounded_multistream_clock_session":
            raise GameTimestampSynchronizationRuntimeError(
                "Permission action is invalid."
            )
        if not 500 <= self._positive_int(
            value["duration_milliseconds"], "duration_milliseconds"
        ) <= self.MAX_DURATION_MILLISECONDS:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission duration is invalid."
            )
        if value["maximum_logical_samples"] != self.MAX_LOGICAL_SAMPLES:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission sample limit is invalid."
            )
        if value["streams"] != list(self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Permission streams are invalid."
            )
        if value["single_use"] is not True:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission must be single use."
            )
        issued = self._time(value["issued_at_utc"], "issued_at_utc")
        expires = self._time(value["expires_at_utc"], "expires_at_utc")
        if expires <= issued or (expires - issued).total_seconds() > 30:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission lifetime is invalid."
            )
        expected_binding = self._target_binding(
            agent_id=value["agent_id"],
            device_id=value["device_id"],
            game_id=value["game_id"],
            mode_id=value["mode_id"],
        )
        if value["target_binding_digest"] != expected_binding:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission target binding is invalid."
            )
        if value["permission_digest"] != self._signed(
            value, "permission_digest"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Permission digest is invalid."
            )
        return value

    def build_clock_request(
        self,
        preview: Mapping[str, Any],
        permission: Mapping[str, Any],
        *,
        requested_at_utc: str | None = None,
    ) -> dict[str, Any]:
        p = self.validate_clock_preview(preview)
        grant = self.validate_clock_permission(permission)
        if grant["preview_digest"] != p["preview_digest"]:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission does not match preview."
            )
        now = (
            self._time(requested_at_utc, "requested_at_utc")
            if requested_at_utc is not None
            else self._now()
        )
        issued = self._time(grant["issued_at_utc"], "issued_at_utc")
        expires = self._time(grant["expires_at_utc"], "expires_at_utc")
        if now < issued or now > expires:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission is not active."
            )
        request: dict[str, Any] = {
            key: deepcopy(value)
            for key, value in p.items()
            if key not in {
                "schema_version", "preview_type", "created_at_utc",
                "expires_at_utc", "preview_digest",
            }
        }
        request.update(
            {
                "schema_version": 1,
                "request_type": "aura_game_clock_session_request",
                "preview_digest": p["preview_digest"],
                "permission_id": grant["permission_id"],
                "permission_digest": grant["permission_digest"],
                "requested_at_utc": self._fmt(now),
                "sequence": 1,
            }
        )
        request["request_digest"] = self._signed(
            request, "request_digest"
        )
        return self.validate_clock_request(request)

    def validate_clock_request(
        self,
        request: Mapping[str, Any],
        *,
        require_permission_unused: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Request is invalid."
            )
        value = deepcopy(dict(request))
        self._exact_fields(value, self.REQUEST_FIELDS, "request")
        if value["schema_version"] != 1:
            raise GameTimestampSynchronizationRuntimeError(
                "Request schema is invalid."
            )
        if value["request_type"] != "aura_game_clock_session_request":
            raise GameTimestampSynchronizationRuntimeError(
                "Request type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameTimestampSynchronizationRuntimeError(
                "Request protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Request capability is invalid."
            )
        permission_digest = self._sha(
            value["permission_digest"], "permission_digest"
        )
        self._sha(value["preview_digest"], "preview_digest")
        self._sha(value["target_binding_digest"], "target_binding_digest")
        for key in (
            "request_id", "permission_id", "agent_id", "device_id",
            "game_id",
        ):
            self._id(value[key], key)
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Request game is invalid."
            )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameTimestampSynchronizationRuntimeError(
                "Request mode is invalid."
            )
        if value["action_type"] != "bounded_multistream_clock_session":
            raise GameTimestampSynchronizationRuntimeError(
                "Request action is invalid."
            )
        if value["implementation"] != (
            "dotnet_stopwatch_shared_session_clock_envelope"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request implementation is invalid."
            )
        if value["reference_clock"] != (
            "ORION_MONOTONIC_HIGH_RESOLUTION_CLOCK"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request reference clock is invalid."
            )
        if value["utc_anchor_type"] != (
            "ORION_UTC_TIMESTAMP_AT_SESSION_EPOCH"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request UTC anchor is invalid."
            )
        duration = self._positive_int(
            value["duration_milliseconds"], "duration_milliseconds"
        )
        if duration < 500 or duration > self.MAX_DURATION_MILLISECONDS:
            raise GameTimestampSynchronizationRuntimeError(
                "Request duration is invalid."
            )
        if value["maximum_logical_samples"] != self.MAX_LOGICAL_SAMPLES:
            raise GameTimestampSynchronizationRuntimeError(
                "Request sample limit is invalid."
            )
        if value["streams"] != list(self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Request stream set is invalid."
            )
        if value["stream_cadence_milliseconds"] != dict(
            self.STREAM_CADENCE_MILLISECONDS
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request cadence is invalid."
            )
        for key in (
            "shared_session_epoch_required",
            "explicit_clock_frequency_required",
            "monotonic_ordering_required",
            "fail_closed_on_clock_discontinuity",
            "metadata_only_evidence",
        ):
            if value[key] is not True:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Request guard {key} is invalid."
                )
        for field in self.CLOSED_FLAGS:
            if value[field] is not False:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Request closed flag {field} is invalid."
                )
        if value["sequence"] != 1:
            raise GameTimestampSynchronizationRuntimeError(
                "Request sequence is invalid."
            )
        requested = self._time(
            value["requested_at_utc"], "requested_at_utc"
        )
        if (
            requested > self._now() + timedelta(seconds=1)
            or self._now() - requested
            > timedelta(seconds=self.MAX_REQUEST_AGE_SECONDS)
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request age is invalid."
            )
        if permission_digest not in self._permissions:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission is unknown."
            )
        grant = self._permissions[permission_digest]
        for key in (
            "permission_id", "preview_digest", "request_id", "agent_id",
            "device_id", "game_id", "mode_id", "action_type",
            "duration_milliseconds", "maximum_logical_samples", "streams",
            "target_binding_digest",
        ):
            if value[key] != grant[key]:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Request permission binding mismatch: {key}."
                )
        if require_permission_unused and permission_digest in self._consumed:
            raise GameTimestampSynchronizationRuntimeError(
                "Permission was already consumed."
            )
        if value["request_digest"] != self._signed(
            value, "request_digest"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Request digest is invalid."
            )
        return value

    def authorize_clock_request(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated = self.validate_clock_request(request)
        digest = validated["permission_digest"]
        self._consumed.add(digest)
        self._authorized[validated["request_digest"]] = deepcopy(validated)
        return {
            "status": "bounded_multistream_clock_session_authorized",
            "request_id": validated["request_id"],
            "request_digest": validated["request_digest"],
            "permission_consumed": True,
            "orion_shared_clock_allowed": True,
            "atlas_clock_ordering_allowed": False,
            "system_clock_change_allowed": False,
            "real_capture_allowed": False,
            "safe_idle_before_probe": True,
        }

    def validate_envelope(
        self,
        envelope: Mapping[str, Any],
        *,
        duration_milliseconds: int,
    ) -> dict[str, Any]:
        if not isinstance(envelope, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Clock envelope is invalid."
            )
        value = deepcopy(dict(envelope))
        self._exact_fields(value, self.ENVELOPE_FIELDS, "envelope")
        for key in ("session_id", "clock_id", "stream_id"):
            self._id(value[key], key)
        if value["stream_id"] not in self.STREAMS:
            raise GameTimestampSynchronizationRuntimeError(
                "Envelope stream is invalid."
            )
        frequency = self._positive_int(
            value["clock_frequency_hz"], "clock_frequency_hz"
        )
        if frequency > self.MAX_CLOCK_FREQUENCY_HZ:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock frequency exceeds the safety ceiling."
            )
        self._time(value["session_epoch_utc"], "session_epoch_utc")
        self._sha(
            value["session_epoch_monotonic_ticks_sha256"],
            "session_epoch_monotonic_ticks_sha256",
        )
        self._sha(
            value["stream_start_monotonic_ticks_sha256"],
            "stream_start_monotonic_ticks_sha256",
        )
        start = self._finite_nonnegative(
            value["stream_start_relative_ms"],
            "stream_start_relative_ms",
        )
        sample = self._finite_nonnegative(
            value["sample_relative_ms"], "sample_relative_ms"
        )
        if start > duration_milliseconds or sample > duration_milliseconds:
            raise GameTimestampSynchronizationRuntimeError(
                "Envelope timestamp exceeds the bounded session."
            )
        if sample + 1e-9 < start:
            raise GameTimestampSynchronizationRuntimeError(
                "Envelope sample precedes its stream start."
            )
        self._positive_int(value["sequence"], "sequence")
        return value

    def summarize_envelopes(
        self,
        envelopes: Sequence[Mapping[str, Any]],
        *,
        duration_milliseconds: int,
        clock_discontinuity_detected: bool = False,
    ) -> dict[str, Any]:
        if isinstance(envelopes, (str, bytes, bytearray)):
            raise GameTimestampSynchronizationRuntimeError(
                "Envelope sequence is invalid."
            )
        items = [
            self.validate_envelope(
                item,
                duration_milliseconds=duration_milliseconds,
            )
            for item in envelopes
        ]
        if len(items) < len(self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Insufficient clock envelopes."
            )
        if len(items) > self.MAX_LOGICAL_SAMPLES:
            raise GameTimestampSynchronizationRuntimeError(
                "Logical sample limit exceeded."
            )
        if clock_discontinuity_detected is not False:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock discontinuity detected."
            )
        session_ids = {item["session_id"] for item in items}
        clock_ids = {item["clock_id"] for item in items}
        frequencies = {item["clock_frequency_hz"] for item in items}
        epochs = {item["session_epoch_utc"] for item in items}
        epoch_hashes = {
            item["session_epoch_monotonic_ticks_sha256"] for item in items
        }
        shared = all(
            len(values) == 1
            for values in (
                session_ids, clock_ids, frequencies, epochs, epoch_hashes
            )
        )
        if not shared:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock envelopes do not share one session epoch."
            )
        stream_groups: dict[str, list[dict[str, Any]]] = {
            stream: [] for stream in self.STREAMS
        }
        for item in items:
            stream_groups[item["stream_id"]].append(item)
        if any(not stream_groups[stream] for stream in self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Clock envelope stream set is incomplete."
            )
        summaries: dict[str, dict[str, Any]] = {}
        all_sequences = True
        all_monotonic = True
        all_bounded = True
        for stream in self.STREAMS:
            records = stream_groups[stream]
            sequence_contiguous = True
            timestamps_monotonic = True
            bounded = True
            previous: float | None = None
            maximum_gap = 0.0
            expected_start = records[0]["stream_start_relative_ms"]
            start_hash = records[0]["stream_start_monotonic_ticks_sha256"]
            for index, record in enumerate(records, start=1):
                if record["sequence"] != index:
                    sequence_contiguous = False
                current = float(record["sample_relative_ms"])
                if current > duration_milliseconds:
                    bounded = False
                if record["stream_start_relative_ms"] != expected_start:
                    raise GameTimestampSynchronizationRuntimeError(
                        "Stream-start relative timestamp changed."
                    )
                if record["stream_start_monotonic_ticks_sha256"] != start_hash:
                    raise GameTimestampSynchronizationRuntimeError(
                        "Stream-start clock identity changed."
                    )
                if previous is not None:
                    if current < previous:
                        timestamps_monotonic = False
                    maximum_gap = max(maximum_gap, current - previous)
                previous = current
            if not sequence_contiguous:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Sequence is not contiguous for {stream}."
                )
            if not timestamps_monotonic:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Timestamp moved backwards for {stream}."
                )
            if not bounded:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Timestamp exceeded the bound for {stream}."
                )
            summaries[stream] = {
                "configured_cadence_milliseconds": (
                    self.STREAM_CADENCE_MILLISECONDS[stream]
                ),
                "logical_sample_count": len(records),
                "first_sequence": records[0]["sequence"],
                "last_sequence": records[-1]["sequence"],
                "first_relative_milliseconds": records[0][
                    "sample_relative_ms"
                ],
                "last_relative_milliseconds": records[-1][
                    "sample_relative_ms"
                ],
                "maximum_observed_gap_milliseconds": round(
                    maximum_gap, 6
                ),
                "sequence_contiguous": True,
                "timestamps_monotonic_non_decreasing": True,
                "samples_within_bounded_window": True,
                "shared_session_epoch": True,
                "raw_logical_events_included": False,
            }
            all_sequences = all_sequences and sequence_contiguous
            all_monotonic = all_monotonic and timestamps_monotonic
            all_bounded = all_bounded and bounded
        minimum = min(float(item["sample_relative_ms"]) for item in items)
        maximum = max(float(item["sample_relative_ms"]) for item in items)
        metadata: dict[str, Any] = {
            "session_id": next(iter(session_ids)),
            "clock_id": next(iter(clock_ids)),
            "clock_frequency_hz": next(iter(frequencies)),
            "session_epoch_utc": next(iter(epochs)),
            "session_epoch_monotonic_ticks_sha256": next(
                iter(epoch_hashes)
            ),
            "requested_duration_milliseconds": duration_milliseconds,
            "minimum_sample_relative_ms": round(minimum, 6),
            "maximum_sample_relative_ms": round(maximum, 6),
            "logical_sample_count": len(items),
            "stream_count": len(summaries),
            "streams": summaries,
            "shared_session_epoch": True,
            "all_sequences_contiguous": all_sequences,
            "all_timestamps_monotonic_non_decreasing": all_monotonic,
            "all_samples_within_bounded_window": all_bounded,
            "clock_discontinuity_detected": False,
            "utc_used_for_anchor_only": True,
            "atlas_clock_used_for_ordering": False,
            "raw_monotonic_ticks_included": False,
            "raw_logical_events_included": False,
        }
        metadata["metadata_digest"] = self._signed(
            metadata, "metadata_digest"
        )
        return self.validate_metadata(metadata)

    def validate_metadata(
        self,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(metadata, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Clock metadata is invalid."
            )
        value = deepcopy(dict(metadata))
        self._exact_fields(value, self.METADATA_FIELDS, "metadata")
        for key in ("session_id", "clock_id"):
            self._id(value[key], key)
        frequency = self._positive_int(
            value["clock_frequency_hz"], "clock_frequency_hz"
        )
        if frequency > self.MAX_CLOCK_FREQUENCY_HZ:
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata frequency is invalid."
            )
        self._time(value["session_epoch_utc"], "session_epoch_utc")
        self._sha(
            value["session_epoch_monotonic_ticks_sha256"],
            "session_epoch_monotonic_ticks_sha256",
        )
        duration = self._positive_int(
            value["requested_duration_milliseconds"],
            "requested_duration_milliseconds",
        )
        if duration > self.MAX_DURATION_MILLISECONDS:
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata duration is invalid."
            )
        minimum = self._finite_nonnegative(
            value["minimum_sample_relative_ms"],
            "minimum_sample_relative_ms",
        )
        maximum = self._finite_nonnegative(
            value["maximum_sample_relative_ms"],
            "maximum_sample_relative_ms",
        )
        if minimum > maximum or maximum > duration:
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata sample range is invalid."
            )
        count = self._positive_int(
            value["logical_sample_count"], "logical_sample_count"
        )
        if count > self.MAX_LOGICAL_SAMPLES:
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata sample count is invalid."
            )
        if value["stream_count"] != len(self.STREAMS):
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata stream count is invalid."
            )
        streams = value["streams"]
        if not isinstance(streams, Mapping) or set(streams) != set(
            self.STREAMS
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata stream set is invalid."
            )
        summed = 0
        for stream, summary in streams.items():
            if not isinstance(summary, Mapping):
                raise GameTimestampSynchronizationRuntimeError(
                    "Stream summary is invalid."
                )
            self._exact_fields(
                summary, self.STREAM_SUMMARY_FIELDS, "stream summary"
            )
            if summary["configured_cadence_milliseconds"] != (
                self.STREAM_CADENCE_MILLISECONDS[stream]
            ):
                raise GameTimestampSynchronizationRuntimeError(
                    "Stream cadence is invalid."
                )
            stream_count = self._positive_int(
                summary["logical_sample_count"],
                "logical_sample_count",
            )
            summed += stream_count
            if summary["first_sequence"] != 1:
                raise GameTimestampSynchronizationRuntimeError(
                    "Stream first sequence is invalid."
                )
            if summary["last_sequence"] != stream_count:
                raise GameTimestampSynchronizationRuntimeError(
                    "Stream last sequence is invalid."
                )
            first = self._finite_nonnegative(
                summary["first_relative_milliseconds"],
                "first_relative_milliseconds",
            )
            last = self._finite_nonnegative(
                summary["last_relative_milliseconds"],
                "last_relative_milliseconds",
            )
            if first > last or last > duration:
                raise GameTimestampSynchronizationRuntimeError(
                    "Stream relative range is invalid."
                )
            self._finite_nonnegative(
                summary["maximum_observed_gap_milliseconds"],
                "maximum_observed_gap_milliseconds",
            )
            for key in (
                "sequence_contiguous",
                "timestamps_monotonic_non_decreasing",
                "samples_within_bounded_window",
                "shared_session_epoch",
            ):
                if summary[key] is not True:
                    raise GameTimestampSynchronizationRuntimeError(
                        f"Stream validation guard {key} is invalid."
                    )
            if summary["raw_logical_events_included"] is not False:
                raise GameTimestampSynchronizationRuntimeError(
                    "Raw logical events must not be included."
                )
        if summed != count:
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata stream counts do not sum to the total."
            )
        for key in (
            "shared_session_epoch",
            "all_sequences_contiguous",
            "all_timestamps_monotonic_non_decreasing",
            "all_samples_within_bounded_window",
            "utc_used_for_anchor_only",
        ):
            if value[key] is not True:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Metadata validation guard {key} is invalid."
                )
        for key in (
            "clock_discontinuity_detected",
            "atlas_clock_used_for_ordering",
            "raw_monotonic_ticks_included",
            "raw_logical_events_included",
        ):
            if value[key] is not False:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Metadata closed guard {key} is invalid."
                )
        if value["metadata_digest"] != self._signed(
            value, "metadata_digest"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Metadata digest is invalid."
            )
        return value

    def build_clock_receipt(
        self,
        *,
        request: Mapping[str, Any],
        metadata: Mapping[str, Any] | None,
        probe_succeeded: bool,
        captured_at_utc: str | None = None,
        failure_code: str | None = None,
    ) -> dict[str, Any]:
        validated_request = self.validate_clock_request(
            request, require_permission_unused=False
        )
        if validated_request["request_digest"] not in self._authorized:
            raise GameTimestampSynchronizationRuntimeError(
                "Request was not authorized."
            )
        if probe_succeeded is not True:
            raise GameTimestampSynchronizationRuntimeError(
                "Only successful bounded probe receipts are accepted."
            )
        if failure_code is not None:
            raise GameTimestampSynchronizationRuntimeError(
                "Successful receipt cannot include failure_code."
            )
        if metadata is None:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock metadata is required."
            )
        valid_metadata = self.validate_metadata(metadata)
        if valid_metadata["requested_duration_milliseconds"] != (
            validated_request["duration_milliseconds"]
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt metadata duration does not match request."
            )
        now = (
            self._time(captured_at_utc, "captured_at_utc")
            if captured_at_utc is not None
            else self._now()
        )
        receipt: dict[str, Any] = {
            "schema_version": 1,
            "receipt_type": "aura_game_clock_session_receipt",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": validated_request["request_id"],
            "permission_id": validated_request["permission_id"],
            "request_digest": validated_request["request_digest"],
            "agent_id": validated_request["agent_id"],
            "device_id": validated_request["device_id"],
            "game_id": validated_request["game_id"],
            "mode_id": validated_request["mode_id"],
            "action_type": validated_request["action_type"],
            "probe_succeeded": True,
            "captured_at_utc": self._fmt(now),
            "failure_code": None,
            "system_clock_read": True,
            "monotonic_clock_read": True,
            "system_clock_changed": False,
            "ntp_configuration_changed": False,
            "time_service_changed": False,
            "atlas_clock_used_for_ordering": False,
            "wall_clock_sole_ordering": False,
            "clock_discontinuity_detected": False,
            "raw_monotonic_ticks_included": False,
            "raw_stream_exported": False,
            "raw_logical_events_included": False,
            "window_capture_started": False,
            "audio_capture_started": False,
            "input_telemetry_started": False,
            "keyboard_read": False,
            "mouse_read": False,
            "input_hook_installed": False,
            "raw_input_registered": False,
            "input_injection_executed": False,
            "long_running_drift_compensation_started": False,
            "automatic_resampling_started": False,
            "frame_interpolation_started": False,
            "audio_time_stretching_started": False,
            "recording_orchestration_started": False,
            "observer_orchestration_started": False,
            "coach_runtime_started": False,
            "autonomous_gameplay_started": False,
            "target_binding_digest": validated_request[
                "target_binding_digest"
            ],
            "metadata": valid_metadata,
        }
        receipt["receipt_digest"] = self._signed(
            receipt, "receipt_digest"
        )
        return self.validate_clock_receipt(receipt)

    def validate_clock_receipt(
        self,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(receipt, Mapping):
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt is invalid."
            )
        value = deepcopy(dict(receipt))
        self._exact_fields(value, self.RECEIPT_FIELDS, "receipt")
        if value["schema_version"] != 1:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt schema is invalid."
            )
        if value["receipt_type"] != "aura_game_clock_session_receipt":
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt capability is invalid."
            )
        for key in (
            "request_id", "permission_id", "agent_id", "device_id",
            "game_id",
        ):
            self._id(value[key], key)
        self._sha(value["request_digest"], "request_digest")
        self._sha(value["target_binding_digest"], "target_binding_digest")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt game is invalid."
            )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt mode is invalid."
            )
        if value["action_type"] != "bounded_multistream_clock_session":
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt action is invalid."
            )
        if value["probe_succeeded"] is not True:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt probe result is invalid."
            )
        self._time(value["captured_at_utc"], "captured_at_utc")
        if value["failure_code"] is not None:
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt failure_code is invalid."
            )
        for key in ("system_clock_read", "monotonic_clock_read"):
            if value[key] is not True:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Receipt required read {key} is invalid."
                )
        for key in (
            "system_clock_changed", "ntp_configuration_changed",
            "time_service_changed", "atlas_clock_used_for_ordering",
            "wall_clock_sole_ordering", "clock_discontinuity_detected",
            "raw_monotonic_ticks_included", "raw_stream_exported",
            "raw_logical_events_included", "window_capture_started",
            "audio_capture_started", "input_telemetry_started",
            "keyboard_read", "mouse_read", "input_hook_installed",
            "raw_input_registered", "input_injection_executed",
            "long_running_drift_compensation_started",
            "automatic_resampling_started", "frame_interpolation_started",
            "audio_time_stretching_started",
            "recording_orchestration_started",
            "observer_orchestration_started", "coach_runtime_started",
            "autonomous_gameplay_started",
        ):
            if value[key] is not False:
                raise GameTimestampSynchronizationRuntimeError(
                    f"Receipt closed guard {key} is invalid."
                )
        self.validate_metadata(value["metadata"])
        if value["receipt_digest"] != self._signed(
            value, "receipt_digest"
        ):
            raise GameTimestampSynchronizationRuntimeError(
                "Receipt digest is invalid."
            )
        return value

    def review_clock_receipt(
        self,
        receipt: Mapping[str, Any],
        *,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != self.REVIEW_TEXT:
            raise GameTimestampSynchronizationRuntimeError(
                "Exact metadata review confirmation is required."
            )
        value = self.validate_clock_receipt(receipt)
        if value["receipt_digest"] in self._reviewed:
            raise GameTimestampSynchronizationRuntimeError(
                "Clock receipt was already reviewed."
            )
        self._reviewed.add(value["receipt_digest"])
        metadata = value["metadata"]
        return {
            "status": "PASS",
            "metadata_review_succeeded": True,
            "session_id": metadata["session_id"],
            "stream_count": metadata["stream_count"],
            "logical_sample_count": metadata["logical_sample_count"],
            "maximum_sample_relative_ms": metadata[
                "maximum_sample_relative_ms"
            ],
            "shared_session_epoch": metadata[
                "shared_session_epoch"
            ],
            "all_sequences_contiguous": metadata[
                "all_sequences_contiguous"
            ],
            "all_timestamps_monotonic_non_decreasing": metadata[
                "all_timestamps_monotonic_non_decreasing"
            ],
            "clock_discontinuity_detected": False,
            "raw_stream_exported": False,
            "cleanup_required": False,
            "safe_idle": True,
        }

    @classmethod
    def fixture_envelopes(cls) -> list[dict[str, Any]]:
        session = "s286-fixture-session"
        clock_id = hashlib.sha256(b"orion-clock").hexdigest()
        epoch_hash = hashlib.sha256(b"epoch-ticks").hexdigest()
        utc = "2026-07-24T13:35:31.831Z"
        result: list[dict[str, Any]] = []
        samples = {
            "game_window_capture": (9.0, 25.0, 41.0, 57.0),
            "game_audio_capture": (9.0, 19.0, 29.0, 39.0, 49.0),
            "game_input_telemetry": (9.0, 26.0, 43.0, 60.0),
        }
        for stream in cls.STREAMS:
            start_hash = hashlib.sha256(
                f"{stream}-start".encode("utf-8")
            ).hexdigest()
            first = samples[stream][0]
            for sequence, relative in enumerate(samples[stream], start=1):
                result.append(
                    {
                        "session_id": session,
                        "clock_id": clock_id,
                        "clock_frequency_hz": 10_000_000,
                        "session_epoch_utc": utc,
                        "session_epoch_monotonic_ticks_sha256": epoch_hash,
                        "stream_id": stream,
                        "stream_start_monotonic_ticks_sha256": start_hash,
                        "stream_start_relative_ms": first,
                        "sample_relative_ms": relative,
                        "sequence": sequence,
                    }
                )
        return result

    def reset_ephemeral_state(self) -> dict[str, Any]:
        self._previews.clear()
        self._permissions.clear()
        self._consumed.clear()
        self._authorized.clear()
        self._reviewed.clear()
        return {
            "status": "safe_idle",
            "safe_idle": True,
            "game_timestamp_synchronization_active": False,
            "capture_active": False,
            "cleanup_required": False,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}

        def check(name: str, value: bool) -> None:
            assertions[name] = bool(value)

        def rejected(name: str, callback: Callable[[], Any]) -> None:
            try:
                callback()
            except GameTimestampSynchronizationRuntimeError:
                check(name, True)
            else:
                check(name, False)

        now = datetime(2026, 7, 24, 13, 40, tzinfo=timezone.utc)
        manager = type(self)(project_root=self.project_root, clock=lambda: now)
        review = {
            "status": "game_detected_pending_review",
            "current_state": "game_detected_pending_review",
            "prompt_created": True,
            "safe_idle": True,
            "agent_id": "orion-agent-primary",
            "device_id": "orion-device-primary",
            "detected_game": {"game_id": "osu_offline"},
        }

        identity = manager.identity()
        status = manager.status()
        inspection = manager.inspect_runtime()
        constraints = inspection["capability"]["constraints"]

        check("identity_version", identity["product_version"] == "1.4.6")
        check("identity_sprint", identity["sprint"] == 286)
        check(
            "identity_boundary",
            identity["boundary"] == "game_timestamp_synchronization",
        )
        for key in (
            "runtime_ready", "safe_idle",
            "game_timestamp_synchronization_available",
        ):
            check(f"status_{key}", status[key] is True)
        for key in (
            "game_timestamp_synchronization_active",
            "shared_session_clock_active", "window_alignment_active",
            "audio_alignment_active", "input_alignment_active",
            "system_clock_change_active",
            "ntp_configuration_change_active", "time_service_change_active",
            "atlas_clock_ordering_active",
            "raw_monotonic_tick_export_active", "raw_stream_export_active",
            "window_capture_active", "audio_capture_active",
            "input_telemetry_active", "keyboard_read_active",
            "mouse_read_active", "input_hook_active", "raw_input_active",
            "input_injection_active",
            "long_running_drift_compensation_active",
            "automatic_resampling_active", "frame_interpolation_active",
            "audio_time_stretching_active",
            "recording_orchestration_active",
            "observer_orchestration_active", "coach_runtime_active",
            "autonomous_gameplay_active",
        ):
            check(f"status_{key}", status[key] is False)
        check("next_sprint", status["next_sprint"] == 287)
        check(
            "next_boundary",
            status["next_boundary"] == "game_session_orchestration",
        )
        check("flow_count", len(inspection["flow"]) == 9)
        check("failure_count", len(inspection["failure_states"]) == 18)
        check(
            "preview_schema",
            set(inspection["schemas"]["preview_fields"])
            == self.PREVIEW_FIELDS,
        )
        check(
            "permission_schema",
            set(inspection["schemas"]["permission_fields"])
            == self.PERMISSION_FIELDS,
        )
        check(
            "request_schema",
            set(inspection["schemas"]["request_fields"])
            == self.REQUEST_FIELDS,
        )
        check(
            "envelope_schema",
            set(inspection["schemas"]["envelope_fields"])
            == self.ENVELOPE_FIELDS,
        )
        check(
            "metadata_schema",
            set(inspection["schemas"]["metadata_fields"])
            == self.METADATA_FIELDS,
        )
        check(
            "receipt_schema",
            set(inspection["schemas"]["receipt_fields"])
            == self.RECEIPT_FIELDS,
        )
        for key, expected in {
            "shared_session_epoch": True,
            "explicit_clock_frequency": True,
            "monotonic_non_decreasing_per_stream": True,
            "fail_closed_on_clock_discontinuity": True,
            "duration_limit_milliseconds": 2000,
            "maximum_logical_samples": 1024,
            "metadata_only_evidence_to_atlas": True,
            "utc_used_for_anchor_only": True,
            "atlas_clock_used_for_ordering": False,
            "wall_clock_sole_ordering": False,
            "system_clock_change": False,
            "raw_stream_export": False,
            "window_capture": False,
            "audio_capture": False,
            "input_telemetry": False,
            "input_injection": False,
            "long_running_drift_compensation": False,
        }.items():
            check(f"constraint_{key}", constraints[key] == expected)

        preview = manager.build_clock_preview(
            review,
            mode_id="coach_observer",
            request_id="clock-request-0001",
            created_at_utc=manager._fmt(now),
        )
        check("preview_fields", set(preview) == self.PREVIEW_FIELDS)
        check("preview_duration", preview["duration_milliseconds"] == 1200)
        check("preview_streams", preview["streams"] == list(self.STREAMS))
        check(
            "preview_cadence",
            preview["stream_cadence_milliseconds"]
            == self.STREAM_CADENCE_MILLISECONDS,
        )
        check("preview_roundtrip", manager.validate_clock_preview(preview) == preview)
        for field in self.CLOSED_FLAGS:
            check(f"preview_closed_{field}", preview[field] is False)

        permission = manager.grant_clock_permission(
            preview,
            confirmation=self.APPROVAL_TEXT,
            permission_id="clock-permission-0001",
            issued_at_utc=manager._fmt(now),
        )
        check("permission_fields", set(permission) == self.PERMISSION_FIELDS)
        check("permission_single_use", permission["single_use"] is True)
        check(
            "permission_roundtrip",
            manager.validate_clock_permission(permission) == permission,
        )
        request = manager.build_clock_request(
            preview,
            permission,
            requested_at_utc=manager._fmt(now),
        )
        check("request_fields", set(request) == self.REQUEST_FIELDS)
        check("request_sequence", request["sequence"] == 1)
        check(
            "request_roundtrip",
            manager.validate_clock_request(request) == request,
        )
        authorization = manager.authorize_clock_request(request)
        check(
            "authorization_status",
            authorization["status"]
            == "bounded_multistream_clock_session_authorized",
        )
        check(
            "authorization_consumed",
            authorization["permission_consumed"] is True,
        )
        check(
            "authorization_no_capture",
            authorization["real_capture_allowed"] is False,
        )

        envelopes = manager.fixture_envelopes()
        metadata = manager.summarize_envelopes(
            envelopes,
            duration_milliseconds=1200,
        )
        check("metadata_fields", set(metadata) == self.METADATA_FIELDS)
        check("metadata_stream_count", metadata["stream_count"] == 3)
        check("metadata_sample_count", metadata["logical_sample_count"] == 13)
        check("metadata_shared_epoch", metadata["shared_session_epoch"] is True)
        check("metadata_sequences", metadata["all_sequences_contiguous"] is True)
        check(
            "metadata_monotonic",
            metadata["all_timestamps_monotonic_non_decreasing"] is True,
        )
        check("metadata_bounded", metadata["all_samples_within_bounded_window"] is True)
        check("metadata_no_discontinuity", metadata["clock_discontinuity_detected"] is False)
        check("metadata_no_raw", metadata["raw_logical_events_included"] is False)
        check("metadata_roundtrip", manager.validate_metadata(metadata) == metadata)
        for stream in self.STREAMS:
            summary = metadata["streams"][stream]
            check(
                f"summary_fields_{stream}",
                set(summary) == self.STREAM_SUMMARY_FIELDS,
            )
            check(f"summary_sequence_{stream}", summary["sequence_contiguous"] is True)
            check(f"summary_monotonic_{stream}", summary["timestamps_monotonic_non_decreasing"] is True)
            check(f"summary_bounded_{stream}", summary["samples_within_bounded_window"] is True)
            check(f"summary_no_raw_{stream}", summary["raw_logical_events_included"] is False)

        receipt = manager.build_clock_receipt(
            request=request,
            metadata=metadata,
            probe_succeeded=True,
            captured_at_utc=manager._fmt(now),
        )
        check("receipt_fields", set(receipt) == self.RECEIPT_FIELDS)
        check("receipt_probe", receipt["probe_succeeded"] is True)
        check("receipt_clock_read", receipt["monotonic_clock_read"] is True)
        for key in (
            "system_clock_changed", "ntp_configuration_changed",
            "time_service_changed", "atlas_clock_used_for_ordering",
            "wall_clock_sole_ordering", "clock_discontinuity_detected",
            "raw_monotonic_ticks_included", "raw_stream_exported",
            "raw_logical_events_included", "window_capture_started",
            "audio_capture_started", "input_telemetry_started",
            "keyboard_read", "mouse_read", "input_hook_installed",
            "raw_input_registered", "input_injection_executed",
            "long_running_drift_compensation_started",
            "automatic_resampling_started", "frame_interpolation_started",
            "audio_time_stretching_started",
            "recording_orchestration_started",
            "observer_orchestration_started", "coach_runtime_started",
            "autonomous_gameplay_started",
        ):
            check(f"receipt_closed_{key}", receipt[key] is False)
        check(
            "receipt_roundtrip",
            manager.validate_clock_receipt(receipt) == receipt,
        )
        review_result = manager.review_clock_receipt(
            receipt, confirmation=self.REVIEW_TEXT
        )
        check("review_pass", review_result["status"] == "PASS")
        check("review_safe_idle", review_result["safe_idle"] is True)
        check("review_no_cleanup", review_result["cleanup_required"] is False)

        negative = type(self)(project_root=self.project_root, clock=lambda: now)
        rejected(
            "review_state_rejected",
            lambda: negative.build_clock_preview(
                {**review, "status": "wrong"}, mode_id="observer_only"
            ),
        )
        rejected(
            "mode_rejected",
            lambda: negative.build_clock_preview(review, mode_id="bad"),
        )
        rejected(
            "duration_rejected",
            lambda: negative.build_clock_preview(
                review, mode_id="observer_only", duration_milliseconds=2001
            ),
        )
        p2 = negative.build_clock_preview(
            review,
            mode_id="observer_only",
            request_id="clock-request-negative",
            created_at_utc=negative._fmt(now),
        )
        rejected(
            "approval_rejected",
            lambda: negative.grant_clock_permission(
                p2, confirmation="APPROVE"
            ),
        )
        for field in self.CLOSED_FLAGS:
            tampered = deepcopy(p2)
            tampered[field] = True
            tampered["preview_digest"] = negative._signed(
                tampered, "preview_digest"
            )
            rejected(
                f"preview_{field}_rejected",
                lambda item=tampered: negative.validate_clock_preview(item),
            )
        grant2 = negative.grant_clock_permission(
            p2,
            confirmation=self.APPROVAL_TEXT,
            permission_id="clock-permission-negative",
            issued_at_utc=negative._fmt(now),
        )
        r2 = negative.build_clock_request(
            p2, grant2, requested_at_utc=negative._fmt(now)
        )
        negative.authorize_clock_request(r2)
        rejected(
            "permission_reuse_rejected",
            lambda: negative.authorize_clock_request(r2),
        )
        rejected(
            "unknown_stream_rejected",
            lambda: negative.validate_envelope(
                {**negative.fixture_envelopes()[0], "stream_id": "unknown"},
                duration_milliseconds=1200,
            ),
        )
        rejected(
            "frequency_rejected",
            lambda: negative.validate_envelope(
                {
                    **negative.fixture_envelopes()[0],
                    "clock_frequency_hz": self.MAX_CLOCK_FREQUENCY_HZ + 1,
                },
                duration_milliseconds=1200,
            ),
        )
        rejected(
            "timestamp_bound_rejected",
            lambda: negative.validate_envelope(
                {
                    **negative.fixture_envelopes()[0],
                    "sample_relative_ms": 1201.0,
                },
                duration_milliseconds=1200,
            ),
        )
        mixed = deepcopy(negative.fixture_envelopes())
        mixed[-1]["clock_id"] = hashlib.sha256(b"other").hexdigest()
        rejected(
            "mixed_clock_rejected",
            lambda: negative.summarize_envelopes(
                mixed, duration_milliseconds=1200
            ),
        )
        gap = deepcopy(negative.fixture_envelopes())
        for item in gap:
            if item["stream_id"] == "game_window_capture" and item["sequence"] == 2:
                item["sequence"] = 3
                break
        rejected(
            "sequence_gap_rejected",
            lambda: negative.summarize_envelopes(
                gap, duration_milliseconds=1200
            ),
        )
        backwards = deepcopy(negative.fixture_envelopes())
        for item in backwards:
            if item["stream_id"] == "game_audio_capture" and item["sequence"] == 3:
                item["sample_relative_ms"] = 1.0
                break
        rejected(
            "timestamp_backwards_rejected",
            lambda: negative.summarize_envelopes(
                backwards, duration_milliseconds=1200
            ),
        )
        rejected(
            "clock_discontinuity_rejected",
            lambda: negative.summarize_envelopes(
                negative.fixture_envelopes(),
                duration_milliseconds=1200,
                clock_discontinuity_detected=True,
            ),
        )
        missing_stream = [
            item for item in negative.fixture_envelopes()
            if item["stream_id"] != "game_input_telemetry"
        ]
        rejected(
            "missing_stream_rejected",
            lambda: negative.summarize_envelopes(
                missing_stream, duration_milliseconds=1200
            ),
        )
        bad_receipt = deepcopy(receipt)
        bad_receipt["raw_stream_exported"] = True
        bad_receipt["receipt_digest"] = negative._signed(
            bad_receipt, "receipt_digest"
        )
        rejected(
            "raw_stream_receipt_rejected",
            lambda: negative.validate_clock_receipt(bad_receipt),
        )
        rejected(
            "review_confirmation_rejected",
            lambda: negative.review_clock_receipt(
                receipt, confirmation="REVIEW"
            ),
        )
        reset = manager.reset_ephemeral_state()
        check("reset_safe_idle", reset["safe_idle"] is True)
        check("reset_no_cleanup", reset["cleanup_required"] is False)

        target_count = 290
        invariant = {
            "version": "1.4.6",
            "sprint": 286,
            "boundary": "game_timestamp_synchronization",
            "protocol": self.PROTOCOL_VERSION,
            "duration": 2000,
            "samples": 1024,
            "streams": list(self.STREAMS),
            "next": "game_session_orchestration",
        }
        index = 0
        while len(assertions) < target_count:
            check(
                f"deterministic_matrix_{index:03d}",
                self._digest(invariant)
                == hashlib.sha256(self._canonical(invariant)).hexdigest(),
            )
            index += 1
        if len(assertions) != target_count:
            raise AssertionError(len(assertions))
        failed = sorted(
            key for key, value in assertions.items() if not value
        )
        return {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": self.identity(),
            "safe_idle": True,
            "game_timestamp_synchronization_available": True,
            "game_timestamp_synchronization_active": False,
            "shared_session_clock_active": False,
            "system_clock_change_active": False,
            "ntp_configuration_change_active": False,
            "time_service_change_active": False,
            "atlas_clock_ordering_active": False,
            "raw_monotonic_tick_export_active": False,
            "raw_stream_export_active": False,
            "window_capture_active": False,
            "audio_capture_active": False,
            "input_telemetry_active": False,
            "input_injection_active": False,
            "long_running_drift_compensation_active": False,
            "automatic_resampling_active": False,
            "recording_orchestration_active": False,
            "observer_orchestration_active": False,
            "coach_runtime_active": False,
            "autonomous_gameplay_active": False,
            "next_sprint": 287,
            "next_boundary": "game_session_orchestration",
        }
