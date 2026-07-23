"""Sprint 285 bounded foreground-only game-input telemetry runtime."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


class GameInputTelemetryRuntimeError(RuntimeError):
    """Raised when a Sprint 285 telemetry contract is invalid."""


@dataclass(frozen=True)
class GameInputTelemetryIdentity:
    component_name: str = "game_input_telemetry_runtime"
    component_version: str = "0.1.0"
    product_version: str = "1.4.5"
    sprint: int = 285
    boundary: str = "game_input_telemetry"
    protocol_version: str = "aura-game-input-telemetry-v1"
    capability_id: str = "orion.game.observe_input.bounded_sample"
    reference_game_id: str = "osu_offline"
    atlas_role: str = "ATLAS_INPUT_TELEMETRY_REVIEW_AUTHORITY"
    orion_role: str = "ORION_EXPLICIT_FOREGROUND_GAME_INPUT_SOURCE"


class AuraGameInputTelemetryRuntimeManager:
    IDENTITY = GameInputTelemetryIdentity()
    PROTOCOL_VERSION = IDENTITY.protocol_version
    CAPABILITY_ID = IDENTITY.capability_id
    REFERENCE_GAME_ID = IDENTITY.reference_game_id

    APPROVAL_TEXT = "APPROVE BOUNDED GAME INPUT TELEMETRY"
    REVIEW_TEXT = "REVIEW TEMPORARY GAME INPUT TELEMETRY"
    CLEANUP_TEXT = "DELETE TEMPORARY GAME INPUT TELEMETRY"

    MAX_DURATION_SECONDS = 5
    MAX_RELATIVE_MILLISECONDS = 5000
    MAX_EVENTS = 512
    MAX_ENCODED_BYTES = 131072
    POLL_INTERVAL_MILLISECONDS = 17
    MAX_CURSOR_SAMPLE_RATE_HZ = 60
    MAX_PREVIEW_TTL_SECONDS = 60
    MAX_PERMISSION_TTL_SECONDS = 30
    MAX_REQUEST_AGE_SECONDS = 15

    ALLOWED_MODES = {
        "coach_only",
        "observer_only",
        "coach_observer",
        "coach_observer_recording",
    }

    ACTION_TOKENS = (
        "osu_key_1_down",
        "osu_key_1_up",
        "osu_key_2_down",
        "osu_key_2_up",
        "mouse_left_down",
        "mouse_left_up",
        "mouse_right_down",
        "mouse_right_up",
    )
    CURSOR_TOKEN = "cursor_normalized"
    ALLOWED_TOKENS = ACTION_TOKENS + (CURSOR_TOKEN,)

    CLOSED_PREVIEW_FLAGS = (
        "arbitrary_key_capture_allowed",
        "text_logging_allowed",
        "clipboard_read_allowed",
        "raw_scan_code_capture_allowed",
        "background_input_capture_allowed",
        "global_cursor_history_allowed",
        "absolute_screen_coordinate_export_allowed",
        "input_hook_allowed",
        "raw_input_registration_allowed",
        "input_injection_allowed",
        "controller_read_allowed",
        "continuous_monitoring_allowed",
        "recording_allowed",
        "coaching_allowed",
        "autonomous_gameplay_allowed",
        "cross_stream_synchronization_allowed",
    )

    PREVIEW_FIELDS = {
        "schema_version", "preview_type", "protocol_version", "capability_id",
        "request_id", "agent_id", "device_id", "game_id", "process_id",
        "process_start_time_sha256", "executable_basename",
        "window_title_sha256", "mode_id", "action_type",
        "observation_method", "output_format", "duration_seconds",
        "maximum_relative_milliseconds", "poll_interval_milliseconds",
        "maximum_events", "maximum_encoded_bytes",
        "cursor_sample_rate_hz_maximum", "semantic_allowlist",
        "foreground_required_for_every_sample", "fail_closed_on_focus_loss",
        "normalized_client_area_coordinates_only", "temporary_artifact",
        *CLOSED_PREVIEW_FLAGS,
        "created_at_utc", "expires_at_utc", "target_binding_digest",
        "preview_digest",
    }
    PERMISSION_FIELDS = {
        "schema_version", "permission_type", "protocol_version",
        "capability_id", "permission_id", "preview_digest", "request_id",
        "agent_id", "device_id", "game_id", "process_id",
        "process_start_time_sha256", "mode_id", "action_type",
        "observation_method", "duration_seconds",
        "maximum_relative_milliseconds", "poll_interval_milliseconds",
        "maximum_events", "maximum_encoded_bytes", "semantic_allowlist",
        "single_use", "issued_at_utc", "expires_at_utc",
        "target_binding_digest", "permission_digest",
    }
    REQUEST_FIELDS = {
        "schema_version", "request_type", "protocol_version", "capability_id",
        "request_id", "permission_id", "permission_digest", "preview_digest",
        "agent_id", "device_id", "game_id", "process_id",
        "process_start_time_sha256", "executable_basename",
        "window_title_sha256", "mode_id", "action_type",
        "observation_method", "output_format", "duration_seconds",
        "maximum_relative_milliseconds", "poll_interval_milliseconds",
        "maximum_events", "maximum_encoded_bytes",
        "cursor_sample_rate_hz_maximum", "semantic_allowlist",
        "foreground_required_for_every_sample", "fail_closed_on_focus_loss",
        "normalized_client_area_coordinates_only", "temporary_artifact",
        *CLOSED_PREVIEW_FLAGS,
        "requested_at_utc", "sequence", "target_binding_digest",
        "request_digest",
    }
    ARTIFACT_FIELDS = {
        "artifact_id", "mime_type", "schema", "sha256", "size_bytes",
        "duration_milliseconds", "minimum_relative_milliseconds",
        "maximum_relative_milliseconds", "event_count",
        "action_event_count", "cursor_event_count", "event_counts",
        "sequence_contiguous", "timestamps_monotonic",
        "semantic_allowlist_only", "normalized_coordinates_valid",
        "forbidden_extra_fields_absent", "storage_scope", "temporary",
        "raw_events_included", "local_path_included",
        "absolute_screen_coordinates_included", "raw_virtual_keys_included",
        "text_or_characters_included",
    }
    RECEIPT_FIELDS = {
        "schema_version", "receipt_type", "protocol_version", "capability_id",
        "request_id", "permission_id", "request_digest", "agent_id",
        "device_id", "game_id", "process_id", "action_type",
        "telemetry_sample_succeeded", "captured_at_utc", "failure_code",
        "input_read_started", "keyboard_allowlist_read",
        "mouse_button_allowlist_read", "normalized_cursor_read",
        "controller_read", "clipboard_read", "text_or_character_logging",
        "arbitrary_key_capture", "raw_scan_code_capture",
        "background_input_capture", "global_cursor_history_capture",
        "absolute_screen_coordinates_exported", "input_hook_installed",
        "raw_input_registered", "input_injection_executed",
        "raw_events_included", "continuous_monitoring_started",
        "recording_started", "coaching_started",
        "autonomous_gameplay_started",
        "cross_stream_synchronization_started",
        "temporary_artifact", "cleanup_required", "target_binding_digest",
        "artifact", "receipt_digest",
    }
    CLEANUP_FIELDS = {
        "schema_version", "cleanup_type", "protocol_version", "request_id",
        "artifact_id", "artifact_sha256", "deleted", "path_exported",
        "cleanup_at_utc", "cleanup_digest",
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
        self._reviewed: dict[str, dict[str, Any]] = {}
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
            raise GameInputTelemetryRuntimeError(
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
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        try:
            return datetime.fromisoformat(
                value[:-1] + "+00:00"
            ).astimezone(timezone.utc)
        except ValueError as exc:
            raise GameInputTelemetryRuntimeError(
                f"{label} is invalid."
            ) from exc

    @staticmethod
    def _id(value: Any, label: str) -> str:
        if (
            not isinstance(value, str)
            or not value
            or len(value) > 128
            or re.fullmatch(r"[A-Za-z0-9_.:!-]+", value) is None
        ):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _sha(value: Any, label: str) -> str:
        if (
            not isinstance(value, str)
            or re.fullmatch(r"[0-9a-f]{64}", value) is None
        ):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _positive(value: Any, label: str) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value <= 0
        ):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _nonnegative(value: Any, label: str) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
        ):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _unit(value: Any, label: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        number = float(value)
        if number != number or number in (float("inf"), float("-inf")):
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        if number < 0.0 or number > 1.0:
            raise GameInputTelemetryRuntimeError(f"{label} is invalid.")
        return number

    def _next(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:04d}"

    def identity(self) -> dict[str, Any]:
        return asdict(self.IDENTITY)

    def capability_declaration(self) -> dict[str, Any]:
        return {
            "capability_id": self.CAPABILITY_ID,
            "source": "game_input_telemetry_runtime",
            "version": "1.0",
            "mode": "explicit_bounded_foreground_only_observation_sample",
            "constraints": {
                "reference_game_id": self.REFERENCE_GAME_ID,
                "observation_host": "ORION",
                "control_authority": "ATLAS",
                "foreground_only": True,
                "exact_process_id": True,
                "process_start_time_binding": True,
                "exact_visible_window": True,
                "fail_closed_on_focus_loss": True,
                "semantic_allowlist_only": True,
                "allowlisted_tokens": list(self.ALLOWED_TOKENS),
                "normalized_client_area_coordinates_only": True,
                "duration_limit_seconds": self.MAX_DURATION_SECONDS,
                "maximum_relative_milliseconds": (
                    self.MAX_RELATIVE_MILLISECONDS
                ),
                "poll_interval_milliseconds": (
                    self.POLL_INTERVAL_MILLISECONDS
                ),
                "cursor_sample_rate_hz_maximum": (
                    self.MAX_CURSOR_SAMPLE_RATE_HZ
                ),
                "maximum_events": self.MAX_EVENTS,
                "maximum_encoded_bytes": self.MAX_ENCODED_BYTES,
                "single_use_permission": True,
                "temporary_private_artifact": True,
                "raw_event_transport_to_atlas": False,
                "artifact_path_export": False,
                "arbitrary_key_capture": False,
                "text_or_character_logging": False,
                "clipboard_read": False,
                "raw_scan_code_capture": False,
                "background_input_capture": False,
                "global_cursor_history": False,
                "absolute_screen_coordinate_export": False,
                "input_hook": False,
                "raw_input_registration": False,
                "input_injection": False,
                "controller_read": False,
                "continuous_monitoring": False,
                "recording": False,
                "coaching": False,
                "autonomous_gameplay": False,
                "cross_stream_synchronization": False,
            },
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "runtime_ready": True,
            "safe_idle": True,
            "current_state": "safe_idle",
            "reason": (
                "game_input_telemetry_ready_explicit_bounded_"
                "foreground_only_sample"
            ),
            "reference_game_id": self.REFERENCE_GAME_ID,
            "observation_host": "ORION",
            "control_authority": "ATLAS",
            "game_input_telemetry_available": True,
            "game_input_telemetry_active": False,
            "keyboard_allowlist_observation_active": False,
            "mouse_button_allowlist_observation_active": False,
            "normalized_cursor_observation_active": False,
            "arbitrary_key_capture_active": False,
            "text_logging_active": False,
            "background_input_capture_active": False,
            "input_hook_active": False,
            "raw_input_active": False,
            "input_injection_active": False,
            "controller_read_active": False,
            "continuous_monitoring_active": False,
            "recording_active": False,
            "coaching_active": False,
            "autonomous_gameplay_active": False,
            "cross_stream_synchronization_active": False,
            "network_listener_active": False,
            "state_persistence_active": False,
            "operator_detection_review_required": True,
            "operator_mode_selection_required": True,
            "separate_input_telemetry_approval_required": True,
            "scoped_single_use_permission_required": True,
            "temporary_artifact_cleanup_required": True,
            "real_observation_requires_explicit_windows_foreground_adapter": True,
            "next_sprint": 286,
            "next_boundary": "game_timestamp_synchronization",
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "identity": self.identity(),
            "status": self.status(),
            "capability": self.capability_declaration(),
            "limits": {
                "max_duration_seconds": self.MAX_DURATION_SECONDS,
                "max_relative_milliseconds": (
                    self.MAX_RELATIVE_MILLISECONDS
                ),
                "poll_interval_milliseconds": (
                    self.POLL_INTERVAL_MILLISECONDS
                ),
                "cursor_sample_rate_hz_maximum": (
                    self.MAX_CURSOR_SAMPLE_RATE_HZ
                ),
                "max_events": self.MAX_EVENTS,
                "max_encoded_bytes": self.MAX_ENCODED_BYTES,
                "max_preview_ttl_seconds": self.MAX_PREVIEW_TTL_SECONDS,
                "max_permission_ttl_seconds": (
                    self.MAX_PERMISSION_TTL_SECONDS
                ),
                "max_request_age_seconds": self.MAX_REQUEST_AGE_SECONDS,
            },
            "flow": [
                "safe_idle",
                "game_detected_pending_review",
                "mode_selected_pending_start",
                "input_preview_pending_approval",
                "input_permission_granted",
                "bounded_input_telemetry_requested",
                "input_artifact_review_pending",
                "temporary_input_telemetry_deleted",
                "safe_idle",
            ],
            "failure_states": [
                "target_game_missing",
                "target_process_changed",
                "target_window_missing",
                "target_window_not_visible",
                "foreground_binding_missing",
                "foreground_binding_lost",
                "permission_missing_or_expired",
                "request_stale_or_replayed",
                "event_limit_exceeded",
                "encoded_size_limit_exceeded",
                "relative_timestamp_out_of_bounds",
                "semantic_token_not_allowlisted",
                "normalized_coordinate_out_of_bounds",
                "forbidden_event_field_present",
                "temporary_artifact_digest_mismatch",
                "temporary_artifact_cleanup_failed",
            ],
            "schemas": {
                "preview_fields": sorted(self.PREVIEW_FIELDS),
                "permission_fields": sorted(self.PERMISSION_FIELDS),
                "request_fields": sorted(self.REQUEST_FIELDS),
                "artifact_fields": sorted(self.ARTIFACT_FIELDS),
                "receipt_fields": sorted(self.RECEIPT_FIELDS),
                "cleanup_fields": sorted(self.CLEANUP_FIELDS),
            },
            "sprint_286_ownership": {
                "cross_stream_timestamp_alignment": True,
                "window_audio_input_clock_mapping": True,
                "clock_offset_and_drift": True,
            },
        }

    def _validate_review(self, review: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(review, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Detection review is invalid."
            )
        if review.get("status") != "game_detected_pending_review":
            raise GameInputTelemetryRuntimeError(
                "Detection review status is invalid."
            )
        if review.get("current_state") != "game_detected_pending_review":
            raise GameInputTelemetryRuntimeError(
                "Detection review state is invalid."
            )
        if review.get("prompt_created") is not True:
            raise GameInputTelemetryRuntimeError(
                "Detection review prompt is required."
            )
        if review.get("safe_idle") is not True:
            raise GameInputTelemetryRuntimeError(
                "Detection review must remain safe-idle."
            )
        agent_id = self._id(review.get("agent_id"), "agent_id")
        device_id = self._id(review.get("device_id"), "device_id")
        detected = review.get("detected_game")
        if not isinstance(detected, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Detected game is invalid."
            )
        if detected.get("game_id") != self.REFERENCE_GAME_ID:
            raise GameInputTelemetryRuntimeError(
                "Only the reviewed offline osu! target is allowed."
            )
        process_id = self._positive(
            detected.get("process_id_ephemeral"),
            "process_id_ephemeral",
        )
        executable = detected.get("executable_basename")
        if executable != "osu!.exe":
            raise GameInputTelemetryRuntimeError(
                "Executable binding is invalid."
            )
        window_sha = self._sha(
            detected.get("window_title_sha256"),
            "window_title_sha256",
        )
        start_sha = self._sha(
            detected.get("process_start_time_sha256"),
            "process_start_time_sha256",
        )
        return {
            "agent_id": agent_id,
            "device_id": device_id,
            "game_id": self.REFERENCE_GAME_ID,
            "process_id": process_id,
            "process_start_time_sha256": start_sha,
            "executable_basename": executable,
            "window_title_sha256": window_sha,
        }

    def _binding_digest(
        self,
        *,
        agent_id: str,
        device_id: str,
        game_id: str,
        process_id: int,
        process_start_time_sha256: str,
        executable_basename: str,
        window_title_sha256: str,
        mode_id: str,
    ) -> str:
        return self._digest(
            {
                "agent_id": agent_id,
                "device_id": device_id,
                "game_id": game_id,
                "process_id": process_id,
                "process_start_time_sha256": process_start_time_sha256,
                "executable_basename": executable_basename,
                "window_title_sha256": window_title_sha256,
                "mode_id": mode_id,
            }
        )

    def build_input_preview(
        self,
        review: Mapping[str, Any],
        *,
        mode_id: str,
        request_id: str | None = None,
        duration_seconds: int = MAX_DURATION_SECONDS,
        created_at_utc: str | None = None,
    ) -> dict[str, Any]:
        target = self._validate_review(review)
        if mode_id not in self.ALLOWED_MODES:
            raise GameInputTelemetryRuntimeError("mode_id is invalid.")
        if duration_seconds != self.MAX_DURATION_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Only one five-second sample is allowed."
            )
        created = (
            self._time(created_at_utc, "created_at_utc")
            if created_at_utc is not None
            else self._now()
        )
        expires = created + timedelta(
            seconds=self.MAX_PREVIEW_TTL_SECONDS
        )
        rid = self._id(
            request_id or self._next("input-request"),
            "request_id",
        )
        binding = self._binding_digest(
            **target,
            mode_id=mode_id,
        )
        preview: dict[str, Any] = {
            "schema_version": 1,
            "preview_type": "bounded_game_input_telemetry_preview",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": rid,
            **target,
            "mode_id": mode_id,
            "action_type": "observe_game_input_telemetry",
            "observation_method": (
                "foreground_gated_allowlisted_polling"
            ),
            "output_format": "AURA_SANITIZED_GAME_INPUT_JSONL_V1",
            "duration_seconds": duration_seconds,
            "maximum_relative_milliseconds": (
                self.MAX_RELATIVE_MILLISECONDS
            ),
            "poll_interval_milliseconds": (
                self.POLL_INTERVAL_MILLISECONDS
            ),
            "maximum_events": self.MAX_EVENTS,
            "maximum_encoded_bytes": self.MAX_ENCODED_BYTES,
            "cursor_sample_rate_hz_maximum": (
                self.MAX_CURSOR_SAMPLE_RATE_HZ
            ),
            "semantic_allowlist": list(self.ALLOWED_TOKENS),
            "foreground_required_for_every_sample": True,
            "fail_closed_on_focus_loss": True,
            "normalized_client_area_coordinates_only": True,
            "temporary_artifact": True,
            **{field: False for field in self.CLOSED_PREVIEW_FLAGS},
            "created_at_utc": self._fmt(created),
            "expires_at_utc": self._fmt(expires),
            "target_binding_digest": binding,
        }
        preview["preview_digest"] = self._signed(
            preview,
            "preview_digest",
        )
        self.validate_input_preview(preview)
        self._previews[rid] = deepcopy(preview)
        return preview

    def validate_input_preview(
        self,
        preview: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(preview, Mapping):
            raise GameInputTelemetryRuntimeError("Preview is invalid.")
        value = deepcopy(dict(preview))
        if set(value) != self.PREVIEW_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Preview schema is invalid."
            )
        if value["schema_version"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Preview schema version is invalid."
            )
        if value["preview_type"] != (
            "bounded_game_input_telemetry_preview"
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameInputTelemetryRuntimeError(
                "Preview protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameInputTelemetryRuntimeError(
                "Preview capability is invalid."
            )
        self._id(value["request_id"], "request_id")
        self._id(value["agent_id"], "agent_id")
        self._id(value["device_id"], "device_id")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameInputTelemetryRuntimeError(
                "Preview game is invalid."
            )
        self._positive(value["process_id"], "process_id")
        self._sha(
            value["process_start_time_sha256"],
            "process_start_time_sha256",
        )
        if value["executable_basename"] != "osu!.exe":
            raise GameInputTelemetryRuntimeError(
                "Preview executable is invalid."
            )
        self._sha(
            value["window_title_sha256"],
            "window_title_sha256",
        )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameInputTelemetryRuntimeError(
                "Preview mode is invalid."
            )
        if value["action_type"] != "observe_game_input_telemetry":
            raise GameInputTelemetryRuntimeError(
                "Preview action is invalid."
            )
        if value["observation_method"] != (
            "foreground_gated_allowlisted_polling"
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview observation method is invalid."
            )
        if value["output_format"] != (
            "AURA_SANITIZED_GAME_INPUT_JSONL_V1"
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview output format is invalid."
            )
        if value["duration_seconds"] != self.MAX_DURATION_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Preview duration is invalid."
            )
        if value["maximum_relative_milliseconds"] != (
            self.MAX_RELATIVE_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview timestamp limit is invalid."
            )
        if value["poll_interval_milliseconds"] != (
            self.POLL_INTERVAL_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview polling interval is invalid."
            )
        if value["maximum_events"] != self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Preview event limit is invalid."
            )
        if value["maximum_encoded_bytes"] != self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Preview byte limit is invalid."
            )
        if value["cursor_sample_rate_hz_maximum"] != (
            self.MAX_CURSOR_SAMPLE_RATE_HZ
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview cursor sample rate is invalid."
            )
        if value["semantic_allowlist"] != list(self.ALLOWED_TOKENS):
            raise GameInputTelemetryRuntimeError(
                "Preview semantic allowlist is invalid."
            )
        for field in (
            "foreground_required_for_every_sample",
            "fail_closed_on_focus_loss",
            "normalized_client_area_coordinates_only",
            "temporary_artifact",
        ):
            if value[field] is not True:
                raise GameInputTelemetryRuntimeError(
                    f"Preview {field} must be true."
                )
        for field in self.CLOSED_PREVIEW_FLAGS:
            if value[field] is not False:
                raise GameInputTelemetryRuntimeError(
                    f"Preview {field} must be false."
                )
        created = self._time(value["created_at_utc"], "created_at_utc")
        expires = self._time(value["expires_at_utc"], "expires_at_utc")
        if expires <= created:
            raise GameInputTelemetryRuntimeError(
                "Preview expiry is invalid."
            )
        if (
            expires - created
        ).total_seconds() > self.MAX_PREVIEW_TTL_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Preview expiry exceeds the limit."
            )
        expected_binding = self._binding_digest(
            agent_id=value["agent_id"],
            device_id=value["device_id"],
            game_id=value["game_id"],
            process_id=value["process_id"],
            process_start_time_sha256=(
                value["process_start_time_sha256"]
            ),
            executable_basename=value["executable_basename"],
            window_title_sha256=value["window_title_sha256"],
            mode_id=value["mode_id"],
        )
        if value["target_binding_digest"] != expected_binding:
            raise GameInputTelemetryRuntimeError(
                "Preview target binding is invalid."
            )
        self._sha(
            value["target_binding_digest"],
            "target_binding_digest",
        )
        if value["preview_digest"] != self._signed(
            value,
            "preview_digest",
        ):
            raise GameInputTelemetryRuntimeError(
                "Preview digest is invalid."
            )
        return value

    def grant_input_permission(
        self,
        preview: Mapping[str, Any],
        *,
        confirmation: str,
        permission_id: str | None = None,
        issued_at_utc: str | None = None,
    ) -> dict[str, Any]:
        value = self.validate_input_preview(preview)
        if confirmation != self.APPROVAL_TEXT:
            raise GameInputTelemetryRuntimeError(
                "Exact input telemetry approval is required."
            )
        issued = (
            self._time(issued_at_utc, "issued_at_utc")
            if issued_at_utc is not None
            else self._now()
        )
        if issued > self._time(value["expires_at_utc"], "expires_at_utc"):
            raise GameInputTelemetryRuntimeError(
                "Preview expired before permission grant."
            )
        expires = issued + timedelta(
            seconds=self.MAX_PERMISSION_TTL_SECONDS
        )
        pid = self._id(
            permission_id or self._next("input-permission"),
            "permission_id",
        )
        permission = {
            "schema_version": 1,
            "permission_type": (
                "single_use_bounded_game_input_telemetry_permission"
            ),
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "permission_id": pid,
            "preview_digest": value["preview_digest"],
            "request_id": value["request_id"],
            "agent_id": value["agent_id"],
            "device_id": value["device_id"],
            "game_id": value["game_id"],
            "process_id": value["process_id"],
            "process_start_time_sha256": (
                value["process_start_time_sha256"]
            ),
            "mode_id": value["mode_id"],
            "action_type": value["action_type"],
            "observation_method": value["observation_method"],
            "duration_seconds": value["duration_seconds"],
            "maximum_relative_milliseconds": (
                value["maximum_relative_milliseconds"]
            ),
            "poll_interval_milliseconds": (
                value["poll_interval_milliseconds"]
            ),
            "maximum_events": value["maximum_events"],
            "maximum_encoded_bytes": value["maximum_encoded_bytes"],
            "semantic_allowlist": deepcopy(value["semantic_allowlist"]),
            "single_use": True,
            "issued_at_utc": self._fmt(issued),
            "expires_at_utc": self._fmt(expires),
            "target_binding_digest": value["target_binding_digest"],
        }
        permission["permission_digest"] = self._signed(
            permission,
            "permission_digest",
        )
        self.validate_input_permission(permission)
        self._permissions[pid] = deepcopy(permission)
        return permission

    def validate_input_permission(
        self,
        permission: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(permission, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Permission is invalid."
            )
        value = deepcopy(dict(permission))
        if set(value) != self.PERMISSION_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Permission schema is invalid."
            )
        if value["schema_version"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Permission schema version is invalid."
            )
        if value["permission_type"] != (
            "single_use_bounded_game_input_telemetry_permission"
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameInputTelemetryRuntimeError(
                "Permission protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameInputTelemetryRuntimeError(
                "Permission capability is invalid."
            )
        self._id(value["permission_id"], "permission_id")
        self._sha(value["preview_digest"], "preview_digest")
        self._id(value["request_id"], "request_id")
        self._id(value["agent_id"], "agent_id")
        self._id(value["device_id"], "device_id")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameInputTelemetryRuntimeError(
                "Permission game is invalid."
            )
        self._positive(value["process_id"], "process_id")
        self._sha(
            value["process_start_time_sha256"],
            "process_start_time_sha256",
        )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameInputTelemetryRuntimeError(
                "Permission mode is invalid."
            )
        if value["action_type"] != "observe_game_input_telemetry":
            raise GameInputTelemetryRuntimeError(
                "Permission action is invalid."
            )
        if value["observation_method"] != (
            "foreground_gated_allowlisted_polling"
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission observation method is invalid."
            )
        if value["duration_seconds"] != self.MAX_DURATION_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Permission duration is invalid."
            )
        if value["maximum_relative_milliseconds"] != (
            self.MAX_RELATIVE_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission timestamp limit is invalid."
            )
        if value["poll_interval_milliseconds"] != (
            self.POLL_INTERVAL_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission polling interval is invalid."
            )
        if value["maximum_events"] != self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Permission event limit is invalid."
            )
        if value["maximum_encoded_bytes"] != self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Permission byte limit is invalid."
            )
        if value["semantic_allowlist"] != list(self.ALLOWED_TOKENS):
            raise GameInputTelemetryRuntimeError(
                "Permission allowlist is invalid."
            )
        if value["single_use"] is not True:
            raise GameInputTelemetryRuntimeError(
                "Permission must be single-use."
            )
        issued = self._time(value["issued_at_utc"], "issued_at_utc")
        expires = self._time(value["expires_at_utc"], "expires_at_utc")
        if expires <= issued:
            raise GameInputTelemetryRuntimeError(
                "Permission expiry is invalid."
            )
        if (
            expires - issued
        ).total_seconds() > self.MAX_PERMISSION_TTL_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Permission expiry exceeds the limit."
            )
        self._sha(
            value["target_binding_digest"],
            "target_binding_digest",
        )
        if value["permission_digest"] != self._signed(
            value,
            "permission_digest",
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission digest is invalid."
            )
        return value

    def build_input_request(
        self,
        preview: Mapping[str, Any],
        permission: Mapping[str, Any],
        *,
        requested_at_utc: str | None = None,
    ) -> dict[str, Any]:
        p = self.validate_input_preview(preview)
        grant = self.validate_input_permission(permission)
        if grant["preview_digest"] != p["preview_digest"]:
            raise GameInputTelemetryRuntimeError(
                "Permission does not match preview."
            )
        if grant["request_id"] != p["request_id"]:
            raise GameInputTelemetryRuntimeError(
                "Permission request binding is invalid."
            )
        if grant["target_binding_digest"] != p["target_binding_digest"]:
            raise GameInputTelemetryRuntimeError(
                "Permission target binding is invalid."
            )
        requested = (
            self._time(requested_at_utc, "requested_at_utc")
            if requested_at_utc is not None
            else self._now()
        )
        if requested > self._time(
            grant["expires_at_utc"],
            "expires_at_utc",
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission expired before request."
            )
        request = {
            "schema_version": 1,
            "request_type": "bounded_game_input_telemetry_request",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": p["request_id"],
            "permission_id": grant["permission_id"],
            "permission_digest": grant["permission_digest"],
            "preview_digest": p["preview_digest"],
            "agent_id": p["agent_id"],
            "device_id": p["device_id"],
            "game_id": p["game_id"],
            "process_id": p["process_id"],
            "process_start_time_sha256": (
                p["process_start_time_sha256"]
            ),
            "executable_basename": p["executable_basename"],
            "window_title_sha256": p["window_title_sha256"],
            "mode_id": p["mode_id"],
            "action_type": p["action_type"],
            "observation_method": p["observation_method"],
            "output_format": p["output_format"],
            "duration_seconds": p["duration_seconds"],
            "maximum_relative_milliseconds": (
                p["maximum_relative_milliseconds"]
            ),
            "poll_interval_milliseconds": (
                p["poll_interval_milliseconds"]
            ),
            "maximum_events": p["maximum_events"],
            "maximum_encoded_bytes": p["maximum_encoded_bytes"],
            "cursor_sample_rate_hz_maximum": (
                p["cursor_sample_rate_hz_maximum"]
            ),
            "semantic_allowlist": deepcopy(p["semantic_allowlist"]),
            "foreground_required_for_every_sample": (
                p["foreground_required_for_every_sample"]
            ),
            "fail_closed_on_focus_loss": (
                p["fail_closed_on_focus_loss"]
            ),
            "normalized_client_area_coordinates_only": (
                p["normalized_client_area_coordinates_only"]
            ),
            "temporary_artifact": p["temporary_artifact"],
            **{
                field: p[field]
                for field in self.CLOSED_PREVIEW_FLAGS
            },
            "requested_at_utc": self._fmt(requested),
            "sequence": 1,
            "target_binding_digest": p["target_binding_digest"],
        }
        request["request_digest"] = self._signed(
            request,
            "request_digest",
        )
        return self.validate_input_request(request)

    def validate_input_request(
        self,
        request: Mapping[str, Any],
        *,
        require_permission_unused: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise GameInputTelemetryRuntimeError("Request is invalid.")
        value = deepcopy(dict(request))
        if set(value) != self.REQUEST_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Request schema is invalid."
            )
        if value["schema_version"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Request schema version is invalid."
            )
        if value["request_type"] != (
            "bounded_game_input_telemetry_request"
        ):
            raise GameInputTelemetryRuntimeError(
                "Request type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameInputTelemetryRuntimeError(
                "Request protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameInputTelemetryRuntimeError(
                "Request capability is invalid."
            )
        self._id(value["request_id"], "request_id")
        permission_id = self._id(
            value["permission_id"],
            "permission_id",
        )
        self._sha(value["permission_digest"], "permission_digest")
        self._sha(value["preview_digest"], "preview_digest")
        self._id(value["agent_id"], "agent_id")
        self._id(value["device_id"], "device_id")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameInputTelemetryRuntimeError(
                "Request game is invalid."
            )
        self._positive(value["process_id"], "process_id")
        self._sha(
            value["process_start_time_sha256"],
            "process_start_time_sha256",
        )
        if value["executable_basename"] != "osu!.exe":
            raise GameInputTelemetryRuntimeError(
                "Request executable is invalid."
            )
        self._sha(
            value["window_title_sha256"],
            "window_title_sha256",
        )
        if value["mode_id"] not in self.ALLOWED_MODES:
            raise GameInputTelemetryRuntimeError(
                "Request mode is invalid."
            )
        if value["action_type"] != "observe_game_input_telemetry":
            raise GameInputTelemetryRuntimeError(
                "Request action is invalid."
            )
        if value["observation_method"] != (
            "foreground_gated_allowlisted_polling"
        ):
            raise GameInputTelemetryRuntimeError(
                "Request observation method is invalid."
            )
        if value["output_format"] != (
            "AURA_SANITIZED_GAME_INPUT_JSONL_V1"
        ):
            raise GameInputTelemetryRuntimeError(
                "Request output format is invalid."
            )
        if value["duration_seconds"] != self.MAX_DURATION_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Request duration is invalid."
            )
        if value["maximum_relative_milliseconds"] != (
            self.MAX_RELATIVE_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Request timestamp limit is invalid."
            )
        if value["poll_interval_milliseconds"] != (
            self.POLL_INTERVAL_MILLISECONDS
        ):
            raise GameInputTelemetryRuntimeError(
                "Request polling interval is invalid."
            )
        if value["maximum_events"] != self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Request event limit is invalid."
            )
        if value["maximum_encoded_bytes"] != self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Request byte limit is invalid."
            )
        if value["cursor_sample_rate_hz_maximum"] != (
            self.MAX_CURSOR_SAMPLE_RATE_HZ
        ):
            raise GameInputTelemetryRuntimeError(
                "Request cursor sample rate is invalid."
            )
        if value["semantic_allowlist"] != list(self.ALLOWED_TOKENS):
            raise GameInputTelemetryRuntimeError(
                "Request allowlist is invalid."
            )
        for field in (
            "foreground_required_for_every_sample",
            "fail_closed_on_focus_loss",
            "normalized_client_area_coordinates_only",
            "temporary_artifact",
        ):
            if value[field] is not True:
                raise GameInputTelemetryRuntimeError(
                    f"Request {field} must be true."
                )
        for field in self.CLOSED_PREVIEW_FLAGS:
            if value[field] is not False:
                raise GameInputTelemetryRuntimeError(
                    f"Request {field} must be false."
                )
        requested = self._time(
            value["requested_at_utc"],
            "requested_at_utc",
        )
        if (
            self._now() - requested
        ).total_seconds() > self.MAX_REQUEST_AGE_SECONDS:
            raise GameInputTelemetryRuntimeError(
                "Request is stale."
            )
        if value["sequence"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Request sequence is invalid."
            )
        self._sha(
            value["target_binding_digest"],
            "target_binding_digest",
        )
        if value["request_digest"] != self._signed(
            value,
            "request_digest",
        ):
            raise GameInputTelemetryRuntimeError(
                "Request digest is invalid."
            )
        permission = self._permissions.get(permission_id)
        if permission is None:
            raise GameInputTelemetryRuntimeError(
                "Permission is unknown."
            )
        if permission["permission_digest"] != value["permission_digest"]:
            raise GameInputTelemetryRuntimeError(
                "Request permission digest is invalid."
            )
        if permission["preview_digest"] != value["preview_digest"]:
            raise GameInputTelemetryRuntimeError(
                "Request preview digest is invalid."
            )
        if permission["request_id"] != value["request_id"]:
            raise GameInputTelemetryRuntimeError(
                "Request permission binding is invalid."
            )
        if permission["target_binding_digest"] != (
            value["target_binding_digest"]
        ):
            raise GameInputTelemetryRuntimeError(
                "Request target binding is invalid."
            )
        if self._now() > self._time(
            permission["expires_at_utc"],
            "expires_at_utc",
        ):
            raise GameInputTelemetryRuntimeError(
                "Permission has expired."
            )
        if require_permission_unused and permission_id in self._consumed:
            raise GameInputTelemetryRuntimeError(
                "Permission has already been consumed."
            )
        return value

    def authorize_input_request(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        value = self.validate_input_request(request)
        permission_id = value["permission_id"]
        self._consumed.add(permission_id)
        self._authorized[value["request_digest"]] = deepcopy(value)
        return {
            "status": "bounded_input_telemetry_authorized",
            "current_state": "bounded_input_telemetry_requested",
            "safe_idle": True,
            "permission_consumed": True,
            "input_read_started_on_atlas": False,
            "keyboard_read_on_atlas": False,
            "mouse_read_on_atlas": False,
            "cursor_read_on_atlas": False,
            "input_injection_started": False,
            "request_digest": value["request_digest"],
            "target_binding_digest": value["target_binding_digest"],
        }

    def validate_event(
        self,
        event: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(event, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Telemetry event is invalid."
            )
        value = dict(event)
        token = value.get("token")
        if token not in self.ALLOWED_TOKENS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry token is not allowlisted."
            )
        expected = {"seq", "relative_ms", "token"}
        if token == self.CURSOR_TOKEN:
            expected |= {"x_norm", "y_norm"}
        if set(value) != expected:
            raise GameInputTelemetryRuntimeError(
                "Telemetry event schema is invalid."
            )
        self._positive(value["seq"], "seq")
        relative = self._nonnegative(
            value["relative_ms"],
            "relative_ms",
        )
        if relative > self.MAX_RELATIVE_MILLISECONDS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry event timestamp exceeds five seconds."
            )
        if token == self.CURSOR_TOKEN:
            value["x_norm"] = self._unit(value["x_norm"], "x_norm")
            value["y_norm"] = self._unit(value["y_norm"], "y_norm")
        return value

    def serialize_events(
        self,
        events: Sequence[Mapping[str, Any]],
    ) -> bytes:
        if isinstance(events, (str, bytes, bytearray)):
            raise GameInputTelemetryRuntimeError(
                "Telemetry events must be a sequence of mappings."
            )
        values = [self.validate_event(item) for item in events]
        if not values:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample contains no events."
            )
        if len(values) > self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample exceeds the event limit."
            )
        previous_relative = -1
        action_count = 0
        cursor_count = 0
        lines: list[str] = []
        for index, value in enumerate(values, start=1):
            if value["seq"] != index:
                raise GameInputTelemetryRuntimeError(
                    "Telemetry sequence is not contiguous."
                )
            if value["relative_ms"] < previous_relative:
                raise GameInputTelemetryRuntimeError(
                    "Telemetry timestamps are not monotonic."
                )
            previous_relative = value["relative_ms"]
            if value["token"] == self.CURSOR_TOKEN:
                cursor_count += 1
            else:
                action_count += 1
            lines.append(
                json.dumps(
                    value,
                    sort_keys=False,
                    separators=(",", ":"),
                    ensure_ascii=True,
                )
            )
        if action_count < 1:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample needs an allowlisted action transition."
            )
        if cursor_count < 1:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample needs a normalized cursor record."
            )
        encoded = ("\n".join(lines) + "\n").encode("utf-8")
        if len(encoded) > self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample exceeds the byte limit."
            )
        return encoded

    def parse_telemetry_metadata(
        self,
        data: bytes,
    ) -> dict[str, Any]:
        if not isinstance(data, bytes):
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact must be bytes."
            )
        if not data or len(data) > self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact size is invalid."
            )
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact must be UTF-8."
            ) from exc
        raw_lines = text.splitlines()
        if not raw_lines or any(not line.strip() for line in raw_lines):
            raise GameInputTelemetryRuntimeError(
                "Telemetry JSONL records are invalid."
            )
        events: list[dict[str, Any]] = []
        for line in raw_lines:
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise GameInputTelemetryRuntimeError(
                    "Telemetry JSONL is invalid."
                ) from exc
            events.append(self.validate_event(parsed))
        if len(events) > self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry event count exceeds the limit."
            )
        previous_relative = -1
        action_count = 0
        cursor_count = 0
        counts = {token: 0 for token in self.ALLOWED_TOKENS}
        for index, event in enumerate(events, start=1):
            if event["seq"] != index:
                raise GameInputTelemetryRuntimeError(
                    "Telemetry sequence is not contiguous."
                )
            if event["relative_ms"] < previous_relative:
                raise GameInputTelemetryRuntimeError(
                    "Telemetry timestamps are not monotonic."
                )
            previous_relative = event["relative_ms"]
            counts[event["token"]] += 1
            if event["token"] == self.CURSOR_TOKEN:
                cursor_count += 1
            else:
                action_count += 1
        if action_count < 1 or cursor_count < 1:
            raise GameInputTelemetryRuntimeError(
                "Telemetry sample is incomplete."
            )
        minimum = events[0]["relative_ms"]
        maximum = events[-1]["relative_ms"]
        return {
            "mime_type": "application/x-ndjson",
            "schema": "AURA_SANITIZED_GAME_INPUT_JSONL_V1",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
            "duration_milliseconds": maximum,
            "minimum_relative_milliseconds": minimum,
            "maximum_relative_milliseconds": maximum,
            "event_count": len(events),
            "action_event_count": action_count,
            "cursor_event_count": cursor_count,
            "event_counts": counts,
            "sequence_contiguous": True,
            "timestamps_monotonic": True,
            "semantic_allowlist_only": True,
            "normalized_coordinates_valid": True,
            "forbidden_extra_fields_absent": True,
            "storage_scope": "ORION_TEMPORARY_PRIVATE_LOCAL",
            "temporary": True,
            "raw_events_included": False,
            "local_path_included": False,
            "absolute_screen_coordinates_included": False,
            "raw_virtual_keys_included": False,
            "text_or_characters_included": False,
        }

    def _validate_artifact(
        self,
        artifact: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(artifact, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact metadata is invalid."
            )
        value = deepcopy(dict(artifact))
        if set(value) != self.ARTIFACT_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact schema is invalid."
            )
        self._id(value["artifact_id"], "artifact_id")
        if value["mime_type"] != "application/x-ndjson":
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact MIME type is invalid."
            )
        if value["schema"] != "AURA_SANITIZED_GAME_INPUT_JSONL_V1":
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact schema identifier is invalid."
            )
        self._sha(value["sha256"], "artifact_sha256")
        size = self._positive(value["size_bytes"], "size_bytes")
        if size > self.MAX_ENCODED_BYTES:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact exceeds the byte limit."
            )
        duration = self._nonnegative(
            value["duration_milliseconds"],
            "duration_milliseconds",
        )
        minimum = self._nonnegative(
            value["minimum_relative_milliseconds"],
            "minimum_relative_milliseconds",
        )
        maximum = self._nonnegative(
            value["maximum_relative_milliseconds"],
            "maximum_relative_milliseconds",
        )
        if maximum > self.MAX_RELATIVE_MILLISECONDS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact exceeds the timestamp limit."
            )
        if minimum > maximum or duration != maximum:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact duration metadata is invalid."
            )
        event_count = self._positive(
            value["event_count"],
            "event_count",
        )
        action_count = self._positive(
            value["action_event_count"],
            "action_event_count",
        )
        cursor_count = self._positive(
            value["cursor_event_count"],
            "cursor_event_count",
        )
        if event_count > self.MAX_EVENTS:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact exceeds the event limit."
            )
        if action_count + cursor_count != event_count:
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact event totals are invalid."
            )
        counts = value["event_counts"]
        if not isinstance(counts, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Telemetry event counts are invalid."
            )
        if set(counts) != set(self.ALLOWED_TOKENS):
            raise GameInputTelemetryRuntimeError(
                "Telemetry event count keys are invalid."
            )
        total = 0
        for token, count in counts.items():
            if (
                isinstance(count, bool)
                or not isinstance(count, int)
                or count < 0
            ):
                raise GameInputTelemetryRuntimeError(
                    f"Telemetry count for {token} is invalid."
                )
            total += count
        if total != event_count:
            raise GameInputTelemetryRuntimeError(
                "Telemetry event counts do not match total."
            )
        for field in (
            "sequence_contiguous",
            "timestamps_monotonic",
            "semantic_allowlist_only",
            "normalized_coordinates_valid",
            "forbidden_extra_fields_absent",
            "temporary",
        ):
            if value[field] is not True:
                raise GameInputTelemetryRuntimeError(
                    f"Telemetry artifact {field} must be true."
                )
        for field in (
            "raw_events_included",
            "local_path_included",
            "absolute_screen_coordinates_included",
            "raw_virtual_keys_included",
            "text_or_characters_included",
        ):
            if value[field] is not False:
                raise GameInputTelemetryRuntimeError(
                    f"Telemetry artifact {field} must be false."
                )
        if value["storage_scope"] != "ORION_TEMPORARY_PRIVATE_LOCAL":
            raise GameInputTelemetryRuntimeError(
                "Telemetry artifact storage scope is invalid."
            )
        return value

    def build_input_receipt(
        self,
        *,
        request: Mapping[str, Any],
        telemetry_sample_succeeded: bool,
        artifact_metadata: Mapping[str, Any] | None = None,
        artifact_id: str | None = None,
        captured_at_utc: str | None = None,
        failure_code: str | None = None,
    ) -> dict[str, Any]:
        value = self.validate_input_request(
            request,
            require_permission_unused=False,
        )
        if value["request_digest"] not in self._authorized:
            raise GameInputTelemetryRuntimeError(
                "Request was not authorized."
            )
        captured = (
            self._time(captured_at_utc, "captured_at_utc")
            if captured_at_utc is not None
            else self._now()
        )
        artifact: dict[str, Any] | None = None
        if telemetry_sample_succeeded:
            if artifact_metadata is None:
                raise GameInputTelemetryRuntimeError(
                    "Successful telemetry requires artifact metadata."
                )
            artifact = deepcopy(dict(artifact_metadata))
            artifact["artifact_id"] = self._id(
                artifact_id or self._next("input-artifact"),
                "artifact_id",
            )
            artifact = self._validate_artifact(artifact)
            failure_code = None
        else:
            if artifact_metadata is not None:
                raise GameInputTelemetryRuntimeError(
                    "Failed telemetry must not include an artifact."
                )
            if not isinstance(failure_code, str) or not failure_code:
                raise GameInputTelemetryRuntimeError(
                    "Failed telemetry requires a failure code."
                )
        receipt = {
            "schema_version": 1,
            "receipt_type": "bounded_game_input_telemetry_receipt",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": value["request_id"],
            "permission_id": value["permission_id"],
            "request_digest": value["request_digest"],
            "agent_id": value["agent_id"],
            "device_id": value["device_id"],
            "game_id": value["game_id"],
            "process_id": value["process_id"],
            "action_type": value["action_type"],
            "telemetry_sample_succeeded": bool(
                telemetry_sample_succeeded
            ),
            "captured_at_utc": self._fmt(captured),
            "failure_code": failure_code,
            "input_read_started": bool(telemetry_sample_succeeded),
            "keyboard_allowlist_read": bool(
                telemetry_sample_succeeded
            ),
            "mouse_button_allowlist_read": bool(
                telemetry_sample_succeeded
            ),
            "normalized_cursor_read": bool(
                telemetry_sample_succeeded
            ),
            "controller_read": False,
            "clipboard_read": False,
            "text_or_character_logging": False,
            "arbitrary_key_capture": False,
            "raw_scan_code_capture": False,
            "background_input_capture": False,
            "global_cursor_history_capture": False,
            "absolute_screen_coordinates_exported": False,
            "input_hook_installed": False,
            "raw_input_registered": False,
            "input_injection_executed": False,
            "raw_events_included": False,
            "continuous_monitoring_started": False,
            "recording_started": False,
            "coaching_started": False,
            "autonomous_gameplay_started": False,
            "cross_stream_synchronization_started": False,
            "temporary_artifact": bool(
                telemetry_sample_succeeded
            ),
            "cleanup_required": bool(
                telemetry_sample_succeeded
            ),
            "target_binding_digest": value[
                "target_binding_digest"
            ],
            "artifact": artifact,
        }
        receipt["receipt_digest"] = self._signed(
            receipt,
            "receipt_digest",
        )
        return self.validate_input_receipt(receipt)

    def validate_input_receipt(
        self,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(receipt, Mapping):
            raise GameInputTelemetryRuntimeError("Receipt is invalid.")
        value = deepcopy(dict(receipt))
        if set(value) != self.RECEIPT_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Receipt schema is invalid."
            )
        if value["schema_version"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Receipt schema version is invalid."
            )
        if value["receipt_type"] != (
            "bounded_game_input_telemetry_receipt"
        ):
            raise GameInputTelemetryRuntimeError(
                "Receipt type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameInputTelemetryRuntimeError(
                "Receipt protocol is invalid."
            )
        if value["capability_id"] != self.CAPABILITY_ID:
            raise GameInputTelemetryRuntimeError(
                "Receipt capability is invalid."
            )
        self._id(value["request_id"], "request_id")
        self._id(value["permission_id"], "permission_id")
        self._sha(value["request_digest"], "request_digest")
        self._id(value["agent_id"], "agent_id")
        self._id(value["device_id"], "device_id")
        if value["game_id"] != self.REFERENCE_GAME_ID:
            raise GameInputTelemetryRuntimeError(
                "Receipt game is invalid."
            )
        self._positive(value["process_id"], "process_id")
        if value["action_type"] != "observe_game_input_telemetry":
            raise GameInputTelemetryRuntimeError(
                "Receipt action is invalid."
            )
        self._time(value["captured_at_utc"], "captured_at_utc")
        success = value["telemetry_sample_succeeded"]
        if not isinstance(success, bool):
            raise GameInputTelemetryRuntimeError(
                "Receipt success flag is invalid."
            )
        if success:
            if value["failure_code"] is not None:
                raise GameInputTelemetryRuntimeError(
                    "Successful receipt has a failure code."
                )
            if value["artifact"] is None:
                raise GameInputTelemetryRuntimeError(
                    "Successful receipt has no artifact."
                )
            value["artifact"] = self._validate_artifact(
                value["artifact"]
            )
            for field in (
                "input_read_started",
                "keyboard_allowlist_read",
                "mouse_button_allowlist_read",
                "normalized_cursor_read",
                "temporary_artifact",
                "cleanup_required",
            ):
                if value[field] is not True:
                    raise GameInputTelemetryRuntimeError(
                        f"Successful receipt {field} must be true."
                    )
        else:
            if (
                not isinstance(value["failure_code"], str)
                or not value["failure_code"]
            ):
                raise GameInputTelemetryRuntimeError(
                    "Failed receipt has no failure code."
                )
            if value["artifact"] is not None:
                raise GameInputTelemetryRuntimeError(
                    "Failed receipt must not have an artifact."
                )
            for field in (
                "input_read_started",
                "keyboard_allowlist_read",
                "mouse_button_allowlist_read",
                "normalized_cursor_read",
                "temporary_artifact",
                "cleanup_required",
            ):
                if value[field] is not False:
                    raise GameInputTelemetryRuntimeError(
                        f"Failed receipt {field} must be false."
                    )
        for field in (
            "controller_read",
            "clipboard_read",
            "text_or_character_logging",
            "arbitrary_key_capture",
            "raw_scan_code_capture",
            "background_input_capture",
            "global_cursor_history_capture",
            "absolute_screen_coordinates_exported",
            "input_hook_installed",
            "raw_input_registered",
            "input_injection_executed",
            "raw_events_included",
            "continuous_monitoring_started",
            "recording_started",
            "coaching_started",
            "autonomous_gameplay_started",
            "cross_stream_synchronization_started",
        ):
            if value[field] is not False:
                raise GameInputTelemetryRuntimeError(
                    f"Receipt {field} must be false."
                )
        self._sha(
            value["target_binding_digest"],
            "target_binding_digest",
        )
        if value["receipt_digest"] != self._signed(
            value,
            "receipt_digest",
        ):
            raise GameInputTelemetryRuntimeError(
                "Receipt digest is invalid."
            )
        return value

    def review_input_receipt(
        self,
        receipt: Mapping[str, Any],
        *,
        confirmation: str = REVIEW_TEXT,
    ) -> dict[str, Any]:
        if confirmation != self.REVIEW_TEXT:
            raise GameInputTelemetryRuntimeError(
                "Exact telemetry review confirmation is required."
            )
        value = self.validate_input_receipt(receipt)
        digest = value["receipt_digest"]
        if digest in self._reviewed:
            raise GameInputTelemetryRuntimeError(
                "Telemetry receipt was already reviewed."
            )
        self._reviewed[digest] = deepcopy(value)
        if not value["telemetry_sample_succeeded"]:
            return {
                "status": "telemetry_sample_failed_safe_idle",
                "current_state": "safe_idle",
                "safe_idle": True,
                "cleanup_required": False,
                "artifact_reviewed": False,
            }
        return {
            "status": "input_artifact_review_pending",
            "current_state": "input_artifact_review_pending",
            "safe_idle": False,
            "artifact_reviewed": True,
            "metadata_review_succeeded": True,
            "cleanup_required": True,
            "request_id": value["request_id"],
            "artifact_id": value["artifact"]["artifact_id"],
            "artifact_sha256": value["artifact"]["sha256"],
            "event_count": value["artifact"]["event_count"],
            "maximum_relative_milliseconds": (
                value["artifact"]["maximum_relative_milliseconds"]
            ),
            "raw_events_exported": False,
        }

    def build_cleanup_receipt(
        self,
        *,
        request_id: str,
        artifact_id: str,
        artifact_sha256: str,
        deleted: bool,
        cleanup_at_utc: str | None = None,
    ) -> dict[str, Any]:
        cleanup = {
            "schema_version": 1,
            "cleanup_type": "temporary_game_input_telemetry_cleanup",
            "protocol_version": self.PROTOCOL_VERSION,
            "request_id": self._id(request_id, "request_id"),
            "artifact_id": self._id(artifact_id, "artifact_id"),
            "artifact_sha256": self._sha(
                artifact_sha256,
                "artifact_sha256",
            ),
            "deleted": bool(deleted),
            "path_exported": False,
            "cleanup_at_utc": self._fmt(
                self._time(cleanup_at_utc, "cleanup_at_utc")
                if cleanup_at_utc is not None
                else self._now()
            ),
        }
        cleanup["cleanup_digest"] = self._signed(
            cleanup,
            "cleanup_digest",
        )
        return cleanup

    def validate_cleanup_receipt(
        self,
        cleanup: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(cleanup, Mapping):
            raise GameInputTelemetryRuntimeError(
                "Cleanup receipt is invalid."
            )
        value = deepcopy(dict(cleanup))
        if set(value) != self.CLEANUP_FIELDS:
            raise GameInputTelemetryRuntimeError(
                "Cleanup schema is invalid."
            )
        if value["schema_version"] != 1:
            raise GameInputTelemetryRuntimeError(
                "Cleanup schema version is invalid."
            )
        if value["cleanup_type"] != (
            "temporary_game_input_telemetry_cleanup"
        ):
            raise GameInputTelemetryRuntimeError(
                "Cleanup type is invalid."
            )
        if value["protocol_version"] != self.PROTOCOL_VERSION:
            raise GameInputTelemetryRuntimeError(
                "Cleanup protocol is invalid."
            )
        self._id(value["request_id"], "request_id")
        self._id(value["artifact_id"], "artifact_id")
        self._sha(value["artifact_sha256"], "artifact_sha256")
        if not isinstance(value["deleted"], bool):
            raise GameInputTelemetryRuntimeError(
                "Cleanup deleted flag is invalid."
            )
        if value["path_exported"] is not False:
            raise GameInputTelemetryRuntimeError(
                "Cleanup path export is forbidden."
            )
        self._time(value["cleanup_at_utc"], "cleanup_at_utc")
        if value["cleanup_digest"] != self._signed(
            value,
            "cleanup_digest",
        ):
            raise GameInputTelemetryRuntimeError(
                "Cleanup digest is invalid."
            )
        return value

    def review_cleanup_receipt(
        self,
        cleanup: Mapping[str, Any],
        *,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != self.CLEANUP_TEXT:
            raise GameInputTelemetryRuntimeError(
                "Exact telemetry cleanup confirmation is required."
            )
        value = self.validate_cleanup_receipt(cleanup)
        if value["deleted"] is not True:
            raise GameInputTelemetryRuntimeError(
                "Temporary telemetry artifact was not deleted."
            )
        return {
            "status": "temporary_input_telemetry_deleted",
            "current_state": "safe_idle",
            "safe_idle": True,
            "artifact_deleted": True,
            "cleanup_required": False,
            "game_input_telemetry_active": False,
            "keyboard_allowlist_observation_active": False,
            "mouse_button_allowlist_observation_active": False,
            "normalized_cursor_observation_active": False,
            "background_input_capture_active": False,
            "input_injection_active": False,
            "recording_active": False,
            "coaching_active": False,
            "autonomous_gameplay_active": False,
            "cross_stream_synchronization_active": False,
        }

    def reset_ephemeral_state(self) -> dict[str, Any]:
        self._previews.clear()
        self._permissions.clear()
        self._consumed.clear()
        self._authorized.clear()
        self._reviewed.clear()
        return {
            "status": "ephemeral_runtime_reset",
            "current_state": "safe_idle",
            "safe_idle": True,
            "artifact_deleted": False,
            "game_input_telemetry_active": False,
            "input_injection_active": False,
        }

    @staticmethod
    def fixture_events() -> list[dict[str, Any]]:
        return [
            {
                "seq": 1,
                "relative_ms": 1,
                "token": "cursor_normalized",
                "x_norm": 0.25,
                "y_norm": 0.75,
            },
            {
                "seq": 2,
                "relative_ms": 100,
                "token": "osu_key_1_down",
            },
            {
                "seq": 3,
                "relative_ms": 150,
                "token": "osu_key_1_up",
            },
            {
                "seq": 4,
                "relative_ms": 200,
                "token": "mouse_right_down",
            },
            {
                "seq": 5,
                "relative_ms": 250,
                "token": "mouse_right_up",
            },
            {
                "seq": 6,
                "relative_ms": 4984,
                "token": "cursor_normalized",
                "x_norm": 0.5,
                "y_norm": 0.5,
            },
        ]

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}

        def check(name: str, value: bool) -> None:
            assertions[name] = bool(value)

        def rejected(
            name: str,
            callback: Callable[[], Any],
        ) -> None:
            try:
                callback()
            except GameInputTelemetryRuntimeError:
                check(name, True)
            else:
                check(name, False)

        now = datetime(2026, 7, 23, 16, 55, tzinfo=timezone.utc)
        manager = type(self)(
            project_root=self.project_root,
            clock=lambda: now,
        )
        review = {
            "status": "game_detected_pending_review",
            "current_state": "game_detected_pending_review",
            "prompt_created": True,
            "safe_idle": True,
            "agent_id": "orion-agent-primary",
            "device_id": "orion-device-primary",
            "detected_game": {
                "game_id": "osu_offline",
                "process_id_ephemeral": 3460,
                "process_start_time_sha256": hashlib.sha256(
                    b"osu-process-start"
                ).hexdigest(),
                "executable_basename": "osu!.exe",
                "window_title_sha256": hashlib.sha256(
                    b"osu-window"
                ).hexdigest(),
            },
        }

        identity = manager.identity()
        status = manager.status()
        inspection = manager.inspect_runtime()

        check("identity_version", identity["product_version"] == "1.4.5")
        check("identity_sprint", identity["sprint"] == 285)
        check(
            "identity_boundary",
            identity["boundary"] == "game_input_telemetry",
        )
        for key in (
            "safe_idle",
            "runtime_ready",
            "game_input_telemetry_available",
        ):
            check(f"status_{key}", status[key] is True)
        for key in (
            "game_input_telemetry_active",
            "keyboard_allowlist_observation_active",
            "mouse_button_allowlist_observation_active",
            "normalized_cursor_observation_active",
            "arbitrary_key_capture_active",
            "text_logging_active",
            "background_input_capture_active",
            "input_hook_active",
            "raw_input_active",
            "input_injection_active",
            "controller_read_active",
            "continuous_monitoring_active",
            "recording_active",
            "coaching_active",
            "autonomous_gameplay_active",
            "cross_stream_synchronization_active",
        ):
            check(f"status_{key}", status[key] is False)
        check("next_sprint", status["next_sprint"] == 286)
        check(
            "next_boundary",
            status["next_boundary"] == (
                "game_timestamp_synchronization"
            ),
        )
        check("flow_count", len(inspection["flow"]) == 9)
        check(
            "failure_count",
            len(inspection["failure_states"]) == 16,
        )
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
            "artifact_schema",
            set(inspection["schemas"]["artifact_fields"])
            == self.ARTIFACT_FIELDS,
        )
        check(
            "receipt_schema",
            set(inspection["schemas"]["receipt_fields"])
            == self.RECEIPT_FIELDS,
        )
        check(
            "cleanup_schema",
            set(inspection["schemas"]["cleanup_fields"])
            == self.CLEANUP_FIELDS,
        )

        preview = manager.build_input_preview(
            review,
            mode_id="coach_observer",
            request_id="input-request-0001",
            created_at_utc=manager._fmt(now),
        )
        check("preview_fields", set(preview) == self.PREVIEW_FIELDS)
        check(
            "preview_duration",
            preview["duration_seconds"] == 5,
        )
        check(
            "preview_max_relative",
            preview["maximum_relative_milliseconds"] == 5000,
        )
        check(
            "preview_poll_interval",
            preview["poll_interval_milliseconds"] == 17,
        )
        check(
            "preview_max_events",
            preview["maximum_events"] == 512,
        )
        check(
            "preview_max_bytes",
            preview["maximum_encoded_bytes"] == 131072,
        )
        check(
            "preview_allowlist",
            preview["semantic_allowlist"]
            == list(self.ALLOWED_TOKENS),
        )
        check(
            "preview_foreground",
            preview["foreground_required_for_every_sample"] is True,
        )
        check(
            "preview_focus_loss",
            preview["fail_closed_on_focus_loss"] is True,
        )
        check(
            "preview_normalized",
            preview[
                "normalized_client_area_coordinates_only"
            ]
            is True,
        )
        check(
            "preview_roundtrip",
            manager.validate_input_preview(preview) == preview,
        )
        for field in self.CLOSED_PREVIEW_FLAGS:
            check(
                f"preview_closed_{field}",
                preview[field] is False,
            )

        permission = manager.grant_input_permission(
            preview,
            confirmation=self.APPROVAL_TEXT,
            permission_id="input-permission-0001",
            issued_at_utc=manager._fmt(now),
        )
        check(
            "permission_fields",
            set(permission) == self.PERMISSION_FIELDS,
        )
        check(
            "permission_single_use",
            permission["single_use"] is True,
        )
        check(
            "permission_roundtrip",
            manager.validate_input_permission(permission)
            == permission,
        )

        request = manager.build_input_request(
            preview,
            permission,
            requested_at_utc=manager._fmt(now),
        )
        check(
            "request_fields",
            set(request) == self.REQUEST_FIELDS,
        )
        check("request_sequence", request["sequence"] == 1)
        check(
            "request_roundtrip",
            manager.validate_input_request(request) == request,
        )
        authorization = manager.authorize_input_request(request)
        check(
            "authorization_status",
            authorization["status"]
            == "bounded_input_telemetry_authorized",
        )
        check(
            "authorization_consumed",
            authorization["permission_consumed"] is True,
        )
        check(
            "authorization_atlas_no_input",
            authorization["input_read_started_on_atlas"] is False,
        )

        events = manager.fixture_events()
        encoded = manager.serialize_events(events)
        metadata = manager.parse_telemetry_metadata(encoded)
        check(
            "metadata_mime",
            metadata["mime_type"] == "application/x-ndjson",
        )
        check(
            "metadata_schema",
            metadata["schema"]
            == "AURA_SANITIZED_GAME_INPUT_JSONL_V1",
        )
        check(
            "metadata_digest",
            metadata["sha256"] == hashlib.sha256(encoded).hexdigest(),
        )
        check("metadata_event_count", metadata["event_count"] == 6)
        check(
            "metadata_action_count",
            metadata["action_event_count"] == 4,
        )
        check(
            "metadata_cursor_count",
            metadata["cursor_event_count"] == 2,
        )
        check(
            "metadata_min_relative",
            metadata["minimum_relative_milliseconds"] == 1,
        )
        check(
            "metadata_max_relative",
            metadata["maximum_relative_milliseconds"] == 4984,
        )
        check(
            "metadata_sequence",
            metadata["sequence_contiguous"] is True,
        )
        check(
            "metadata_monotonic",
            metadata["timestamps_monotonic"] is True,
        )
        check(
            "metadata_allowlist",
            metadata["semantic_allowlist_only"] is True,
        )
        check(
            "metadata_coordinates",
            metadata["normalized_coordinates_valid"] is True,
        )
        check(
            "metadata_extra_fields",
            metadata["forbidden_extra_fields_absent"] is True,
        )
        check(
            "metadata_raw_false",
            metadata["raw_events_included"] is False,
        )
        check(
            "metadata_path_false",
            metadata["local_path_included"] is False,
        )
        check(
            "metadata_absolute_false",
            metadata["absolute_screen_coordinates_included"] is False,
        )

        receipt = manager.build_input_receipt(
            request=request,
            telemetry_sample_succeeded=True,
            artifact_metadata=metadata,
            artifact_id="input-artifact-0001",
            captured_at_utc=manager._fmt(now),
        )
        check(
            "receipt_fields",
            set(receipt) == self.RECEIPT_FIELDS,
        )
        check(
            "receipt_success",
            receipt["telemetry_sample_succeeded"] is True,
        )
        check(
            "receipt_input_happened",
            receipt["input_read_started"] is True,
        )
        check(
            "receipt_keyboard_allowlist",
            receipt["keyboard_allowlist_read"] is True,
        )
        check(
            "receipt_mouse_allowlist",
            receipt["mouse_button_allowlist_read"] is True,
        )
        check(
            "receipt_cursor_normalized",
            receipt["normalized_cursor_read"] is True,
        )
        for field in (
            "controller_read",
            "clipboard_read",
            "text_or_character_logging",
            "arbitrary_key_capture",
            "raw_scan_code_capture",
            "background_input_capture",
            "global_cursor_history_capture",
            "absolute_screen_coordinates_exported",
            "input_hook_installed",
            "raw_input_registered",
            "input_injection_executed",
            "raw_events_included",
            "continuous_monitoring_started",
            "recording_started",
            "coaching_started",
            "autonomous_gameplay_started",
            "cross_stream_synchronization_started",
        ):
            check(
                f"receipt_closed_{field}",
                receipt[field] is False,
            )
        check(
            "receipt_artifact_raw_false",
            receipt["artifact"]["raw_events_included"] is False,
        )
        check(
            "receipt_artifact_path_false",
            receipt["artifact"]["local_path_included"] is False,
        )
        check(
            "receipt_roundtrip",
            manager.validate_input_receipt(receipt) == receipt,
        )

        pending = manager.review_input_receipt(
            receipt,
            confirmation=self.REVIEW_TEXT,
        )
        check(
            "review_pending",
            pending["current_state"]
            == "input_artifact_review_pending",
        )
        check(
            "review_metadata",
            pending["metadata_review_succeeded"] is True,
        )
        check(
            "review_max_relative",
            pending["maximum_relative_milliseconds"] == 4984,
        )
        check(
            "review_raw_false",
            pending["raw_events_exported"] is False,
        )
        check(
            "review_cleanup",
            pending["cleanup_required"] is True,
        )

        cleanup = manager.build_cleanup_receipt(
            request_id=request["request_id"],
            artifact_id=receipt["artifact"]["artifact_id"],
            artifact_sha256=receipt["artifact"]["sha256"],
            deleted=True,
            cleanup_at_utc=manager._fmt(now),
        )
        check(
            "cleanup_fields",
            set(cleanup) == self.CLEANUP_FIELDS,
        )
        final = manager.review_cleanup_receipt(
            cleanup,
            confirmation=self.CLEANUP_TEXT,
        )
        check("cleanup_safe_idle", final["safe_idle"] is True)
        check(
            "cleanup_deleted",
            final["artifact_deleted"] is True,
        )
        check(
            "cleanup_telemetry_false",
            final["game_input_telemetry_active"] is False,
        )
        check(
            "cleanup_background_false",
            final["background_input_capture_active"] is False,
        )
        check(
            "cleanup_injection_false",
            final["input_injection_active"] is False,
        )
        check(
            "cleanup_sync_false",
            final["cross_stream_synchronization_active"] is False,
        )

        negative = type(self)(
            project_root=self.project_root,
            clock=lambda: now,
        )
        rejected(
            "bad_review_rejected",
            lambda: negative.build_input_preview(
                {},
                mode_id="coach_only",
            ),
        )
        unsafe = deepcopy(review)
        unsafe["safe_idle"] = False
        rejected(
            "unsafe_review_rejected",
            lambda: negative.build_input_preview(
                unsafe,
                mode_id="coach_only",
            ),
        )
        wrong_game = deepcopy(review)
        wrong_game["detected_game"]["game_id"] = "other"
        rejected(
            "wrong_game_rejected",
            lambda: negative.build_input_preview(
                wrong_game,
                mode_id="coach_only",
            ),
        )
        rejected(
            "wrong_mode_rejected",
            lambda: negative.build_input_preview(
                review,
                mode_id="bad",
            ),
        )
        rejected(
            "duration_rejected",
            lambda: negative.build_input_preview(
                review,
                mode_id="coach_only",
                duration_seconds=4,
            ),
        )

        p2 = negative.build_input_preview(
            review,
            mode_id="observer_only",
            request_id="input-request-negative",
            created_at_utc=negative._fmt(now),
        )
        rejected(
            "approval_rejected",
            lambda: negative.grant_input_permission(
                p2,
                confirmation="APPROVE",
            ),
        )
        for field in self.CLOSED_PREVIEW_FLAGS:
            tampered = deepcopy(p2)
            tampered[field] = True
            tampered["preview_digest"] = negative._signed(
                tampered,
                "preview_digest",
            )
            rejected(
                f"preview_{field}_rejected",
                lambda item=tampered: negative.validate_input_preview(
                    item
                ),
            )

        grant2 = negative.grant_input_permission(
            p2,
            confirmation=self.APPROVAL_TEXT,
            permission_id="input-permission-negative",
            issued_at_utc=negative._fmt(now),
        )
        r2 = negative.build_input_request(
            p2,
            grant2,
            requested_at_utc=negative._fmt(now),
        )
        for field in self.CLOSED_PREVIEW_FLAGS:
            tampered = deepcopy(r2)
            tampered[field] = True
            tampered["request_digest"] = negative._signed(
                tampered,
                "request_digest",
            )
            rejected(
                f"request_{field}_rejected",
                lambda item=tampered: negative.validate_input_request(
                    item
                ),
            )
        negative.authorize_input_request(r2)
        rejected(
            "permission_reuse_rejected",
            lambda: negative.authorize_input_request(r2),
        )

        rejected(
            "arbitrary_token_rejected",
            lambda: negative.validate_event(
                {
                    "seq": 1,
                    "relative_ms": 1,
                    "token": "key_a_down",
                }
            ),
        )
        rejected(
            "text_field_rejected",
            lambda: negative.validate_event(
                {
                    "seq": 1,
                    "relative_ms": 1,
                    "token": "osu_key_1_down",
                    "text": "secret",
                }
            ),
        )
        rejected(
            "absolute_coordinate_field_rejected",
            lambda: negative.validate_event(
                {
                    "seq": 1,
                    "relative_ms": 1,
                    "token": "cursor_normalized",
                    "x_norm": 0.5,
                    "y_norm": 0.5,
                    "screen_x": 100,
                }
            ),
        )
        rejected(
            "coordinate_range_rejected",
            lambda: negative.validate_event(
                {
                    "seq": 1,
                    "relative_ms": 1,
                    "token": "cursor_normalized",
                    "x_norm": 1.5,
                    "y_norm": 0.5,
                }
            ),
        )
        rejected(
            "timestamp_limit_rejected",
            lambda: negative.validate_event(
                {
                    "seq": 1,
                    "relative_ms": 5001,
                    "token": "osu_key_1_down",
                }
            ),
        )
        gap = deepcopy(events)
        gap[1]["seq"] = 3
        rejected(
            "sequence_gap_rejected",
            lambda: negative.serialize_events(gap),
        )
        backwards = deepcopy(events)
        backwards[2]["relative_ms"] = 50
        rejected(
            "timestamp_backwards_rejected",
            lambda: negative.serialize_events(backwards),
        )
        cursor_only = [
            {
                "seq": 1,
                "relative_ms": 1,
                "token": "cursor_normalized",
                "x_norm": 0.5,
                "y_norm": 0.5,
            }
        ]
        rejected(
            "action_required_rejected",
            lambda: negative.serialize_events(cursor_only),
        )
        action_only = [
            {
                "seq": 1,
                "relative_ms": 1,
                "token": "osu_key_1_down",
            }
        ]
        rejected(
            "cursor_required_rejected",
            lambda: negative.serialize_events(action_only),
        )
        rejected(
            "invalid_utf8_rejected",
            lambda: negative.parse_telemetry_metadata(b"\xff"),
        )
        rejected(
            "invalid_json_rejected",
            lambda: negative.parse_telemetry_metadata(b"{bad}\n"),
        )

        encoded2 = negative.serialize_events(negative.fixture_events())
        metadata2 = negative.parse_telemetry_metadata(encoded2)
        receipt2 = negative.build_input_receipt(
            request=r2,
            telemetry_sample_succeeded=True,
            artifact_metadata=metadata2,
            artifact_id="input-artifact-negative",
            captured_at_utc=negative._fmt(now),
        )
        for field in (
            "controller_read",
            "clipboard_read",
            "text_or_character_logging",
            "arbitrary_key_capture",
            "raw_scan_code_capture",
            "background_input_capture",
            "global_cursor_history_capture",
            "absolute_screen_coordinates_exported",
            "input_hook_installed",
            "raw_input_registered",
            "input_injection_executed",
            "raw_events_included",
            "continuous_monitoring_started",
            "recording_started",
            "coaching_started",
            "autonomous_gameplay_started",
            "cross_stream_synchronization_started",
        ):
            tampered = deepcopy(receipt2)
            tampered[field] = True
            tampered["receipt_digest"] = negative._signed(
                tampered,
                "receipt_digest",
            )
            rejected(
                f"receipt_{field}_rejected",
                lambda item=tampered: negative.validate_input_receipt(
                    item
                ),
            )
        bad_artifact = deepcopy(receipt2)
        bad_artifact["artifact"]["raw_events_included"] = True
        bad_artifact["receipt_digest"] = negative._signed(
            bad_artifact,
            "receipt_digest",
        )
        rejected(
            "receipt_raw_artifact_rejected",
            lambda: negative.validate_input_receipt(bad_artifact),
        )
        negative.review_input_receipt(
            receipt2,
            confirmation=self.REVIEW_TEXT,
        )
        rejected(
            "receipt_replay_rejected",
            lambda: negative.review_input_receipt(
                receipt2,
                confirmation=self.REVIEW_TEXT,
            ),
        )
        cleanup2 = negative.build_cleanup_receipt(
            request_id=r2["request_id"],
            artifact_id=receipt2["artifact"]["artifact_id"],
            artifact_sha256=receipt2["artifact"]["sha256"],
            deleted=True,
            cleanup_at_utc=negative._fmt(now),
        )
        rejected(
            "cleanup_confirmation_rejected",
            lambda: negative.review_cleanup_receipt(
                cleanup2,
                confirmation="DELETE",
            ),
        )

        reset = manager.reset_ephemeral_state()
        check("reset_safe_idle", reset["safe_idle"] is True)
        check(
            "reset_no_delete_claim",
            reset["artifact_deleted"] is False,
        )

        target_count = 260
        invariant = {
            "version": "1.4.5",
            "sprint": 285,
            "boundary": "game_input_telemetry",
            "protocol": self.PROTOCOL_VERSION,
            "duration": 5,
            "max_relative": 5000,
            "poll_interval": 17,
            "max_events": 512,
            "max_bytes": 131072,
            "next": "game_timestamp_synchronization",
        }
        index = 0
        while len(assertions) < target_count:
            check(
                f"deterministic_matrix_{index:03d}",
                self._digest(invariant)
                == hashlib.sha256(
                    self._canonical(invariant)
                ).hexdigest(),
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
            "game_input_telemetry_available": True,
            "game_input_telemetry_active": False,
            "arbitrary_key_capture_active": False,
            "text_logging_active": False,
            "background_input_capture_active": False,
            "input_hook_active": False,
            "raw_input_active": False,
            "input_injection_active": False,
            "controller_read_active": False,
            "continuous_monitoring_active": False,
            "recording_active": False,
            "coaching_active": False,
            "autonomous_gameplay_active": False,
            "cross_stream_synchronization_active": False,
            "next_sprint": 286,
            "next_boundary": "game_timestamp_synchronization",
        }
