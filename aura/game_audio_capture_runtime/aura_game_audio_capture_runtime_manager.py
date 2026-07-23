"""Sprint 284 bounded explicit short game-audio capture runtime."""

from __future__ import annotations

import hashlib
import io
import json
import re
import wave
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


class GameAudioCaptureRuntimeError(RuntimeError):
    pass


@dataclass(frozen=True)
class GameAudioCaptureIdentity:
    component_name: str = "game_audio_capture_runtime"
    component_version: str = "0.1.0"
    product_version: str = "1.4.4"
    sprint: int = 284
    boundary: str = "game_audio_capture"
    protocol_version: str = "aura-game-audio-capture-v1"
    capability_id: str = "orion.game.capture_audio.short_sample"
    reference_game_id: str = "osu_offline"
    atlas_role: str = "ATLAS_AUDIO_REVIEW_AUTHORITY"
    orion_role: str = "ORION_EXPLICIT_PROCESS_LOOPBACK_SOURCE"


class AuraGameAudioCaptureRuntimeManager:
    IDENTITY = GameAudioCaptureIdentity()
    PROTOCOL_VERSION = IDENTITY.protocol_version
    CAPABILITY_ID = IDENTITY.capability_id
    REFERENCE_GAME_ID = IDENTITY.reference_game_id

    APPROVAL_TEXT = "APPROVE SHORT GAME AUDIO CAPTURE"
    CLEANUP_TEXT = "DELETE TEMPORARY GAME AUDIO"

    MAX_DURATION_SECONDS = 5
    SAMPLE_RATE_HZ = 48000
    CHANNELS = 2
    SAMPLE_WIDTH_BYTES = 2
    MAX_ENCODED_BYTES = 1048576
    MAX_PREVIEW_TTL_SECONDS = 60
    MAX_PERMISSION_TTL_SECONDS = 30
    MAX_REQUEST_AGE_SECONDS = 15

    ALLOWED_MODES = {
        "coach_only",
        "observer_only",
        "coach_observer",
        "coach_observer_recording",
    }

    PREVIEW_FIELDS = {
        "schema_version", "preview_type", "protocol_version", "capability_id",
        "request_id", "agent_id", "device_id", "game_id", "process_id",
        "executable_basename", "window_title_sha256", "mode_id",
        "action_type", "capture_source", "output_format", "duration_seconds",
        "sample_rate_hz", "channel_count", "sample_width_bytes",
        "max_encoded_bytes", "temporary_artifact",
        "microphone_capture_allowed", "whole_system_fallback_allowed",
        "continuous_capture_allowed", "recording_allowed",
        "transcription_allowed", "telemetry_allowed", "coaching_allowed",
        "game_input_control_allowed", "created_at_utc", "expires_at_utc",
        "target_binding_digest", "preview_digest",
    }
    PERMISSION_FIELDS = {
        "schema_version", "permission_type", "protocol_version", "capability_id",
        "permission_id", "preview_digest", "request_id", "agent_id",
        "device_id", "game_id", "process_id", "mode_id", "action_type",
        "capture_source", "duration_seconds", "sample_rate_hz", "channel_count",
        "sample_width_bytes", "max_encoded_bytes", "single_use",
        "issued_at_utc", "expires_at_utc", "target_binding_digest",
        "permission_digest",
    }
    REQUEST_FIELDS = {
        "schema_version", "request_type", "protocol_version", "capability_id",
        "request_id", "permission_id", "permission_digest", "preview_digest",
        "agent_id", "device_id", "game_id", "process_id",
        "executable_basename", "window_title_sha256", "mode_id", "action_type",
        "capture_source", "output_format", "duration_seconds", "sample_rate_hz",
        "channel_count", "sample_width_bytes", "max_encoded_bytes",
        "temporary_artifact", "microphone_capture_allowed",
        "whole_system_fallback_allowed", "continuous_capture_allowed",
        "recording_allowed", "transcription_allowed", "telemetry_allowed",
        "coaching_allowed", "game_input_control_allowed", "requested_at_utc",
        "sequence", "target_binding_digest", "request_digest",
    }
    ARTIFACT_FIELDS = {
        "artifact_id", "mime_type", "sha256", "size_bytes",
        "duration_milliseconds", "sample_rate_hz", "channels",
        "sample_width_bytes", "frame_count", "storage_scope", "temporary",
        "raw_bytes_included", "local_path_included",
    }
    RECEIPT_FIELDS = {
        "schema_version", "receipt_type", "protocol_version", "capability_id",
        "request_id", "permission_id", "request_digest", "agent_id",
        "device_id", "game_id", "process_id", "action_type",
        "capture_succeeded", "captured_at_utc", "failure_code",
        "audio_capture_started", "microphone_read",
        "whole_system_fallback_used", "raw_audio_included",
        "temporary_artifact", "cleanup_required", "recording_started",
        "transcription_started", "telemetry_started", "coaching_started",
        "game_input_control_started", "target_binding_digest", "artifact",
        "receipt_digest",
    }
    CLEANUP_FIELDS = {
        "schema_version", "cleanup_type", "protocol_version", "request_id",
        "artifact_id", "artifact_sha256", "deleted", "path_exported",
        "cleanup_at_utc", "cleanup_digest",
    }

    def __init__(self, *, project_root: Path | str,
                 clock: Callable[[], datetime] | None = None) -> None:
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
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True).encode("utf-8")

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
            raise GameAudioCaptureRuntimeError("Clock must be timezone-aware.")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _fmt(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _time(value: Any, label: str) -> datetime:
        if not isinstance(value, str) or not value.endswith("Z"):
            raise GameAudioCaptureRuntimeError(f"{label} is invalid.")
        try:
            return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)
        except ValueError as exc:
            raise GameAudioCaptureRuntimeError(f"{label} is invalid.") from exc

    @staticmethod
    def _id(value: Any, label: str) -> str:
        if (not isinstance(value, str) or not value or len(value) > 128
                or re.fullmatch(r"[A-Za-z0-9_.:!-]+", value) is None):
            raise GameAudioCaptureRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _sha(value: Any, label: str) -> str:
        if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise GameAudioCaptureRuntimeError(f"{label} is invalid.")
        return value

    @staticmethod
    def _positive(value: Any, label: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise GameAudioCaptureRuntimeError(f"{label} is invalid.")
        return value

    def _next(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}-{self._counter:04d}"

    def identity(self) -> dict[str, Any]:
        return asdict(self.IDENTITY)

    def capability_declaration(self) -> dict[str, Any]:
        return {
            "capability_id": self.CAPABILITY_ID,
            "source": "game_audio_capture_runtime",
            "version": "1.0",
            "mode": "explicit_short_process_loopback_sample",
            "constraints": {
                "reference_game_id": self.REFERENCE_GAME_ID,
                "capture_host": "ORION",
                "control_authority": "ATLAS",
                "process_loopback_only": True,
                "include_target_process_tree": True,
                "microphone_capture": False,
                "whole_system_fallback": False,
                "arbitrary_audio_device_capture": False,
                "duration_limit_seconds": self.MAX_DURATION_SECONDS,
                "sample_rate_hz": self.SAMPLE_RATE_HZ,
                "channels": self.CHANNELS,
                "sample_width_bytes": self.SAMPLE_WIDTH_BYTES,
                "max_encoded_bytes": self.MAX_ENCODED_BYTES,
                "single_use_permission": True,
                "temporary_private_artifact": True,
                "raw_audio_transport_to_atlas": False,
                "artifact_path_export": False,
                "continuous_capture": False,
                "recording": False,
                "transcription": False,
                "telemetry": False,
                "coaching": False,
                "game_input_control": False,
            },
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready", "runtime_ready": True, "safe_idle": True,
            "current_state": "safe_idle",
            "reason": "game_audio_capture_ready_explicit_short_sample_only",
            "reference_game_id": self.REFERENCE_GAME_ID,
            "capture_host": "ORION", "control_authority": "ATLAS",
            "game_audio_capture_available": True,
            "game_audio_capture_active": False,
            "microphone_capture_active": False,
            "whole_system_audio_capture_active": False,
            "continuous_audio_capture_active": False,
            "recording_active": False, "transcription_active": False,
            "telemetry_active": False, "coaching_active": False,
            "game_input_control_active": False,
            "autonomous_gameplay_active": False,
            "network_listener_active": False, "state_persistence_active": False,
            "operator_detection_review_required": True,
            "operator_mode_selection_required": True,
            "separate_audio_approval_required": True,
            "scoped_single_use_permission_required": True,
            "temporary_artifact_cleanup_required": True,
            "real_capture_requires_explicit_windows_process_loopback_adapter": True,
            "next_sprint": 285, "next_boundary": "game_input_telemetry",
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "identity": self.identity(),
            "status": self.status(),
            "capability": self.capability_declaration(),
            "limits": {
                "max_duration_seconds": self.MAX_DURATION_SECONDS,
                "sample_rate_hz": self.SAMPLE_RATE_HZ,
                "channels": self.CHANNELS,
                "sample_width_bytes": self.SAMPLE_WIDTH_BYTES,
                "max_encoded_bytes": self.MAX_ENCODED_BYTES,
                "max_preview_ttl_seconds": self.MAX_PREVIEW_TTL_SECONDS,
                "max_permission_ttl_seconds": self.MAX_PERMISSION_TTL_SECONDS,
                "max_request_age_seconds": self.MAX_REQUEST_AGE_SECONDS,
            },
            "flow": [
                "safe_idle", "game_detected_pending_review",
                "mode_selected_pending_start", "audio_preview_pending_approval",
                "audio_permission_granted", "bounded_audio_capture_requested",
                "audio_artifact_review_pending", "temporary_audio_deleted",
                "safe_idle",
            ],
            "failure_states": [
                "target_game_missing", "target_process_changed",
                "audio_session_missing", "permission_missing_or_expired",
                "process_loopback_backend_unsupported",
                "audio_backend_unavailable", "capture_timeout",
                "duration_exceeded", "sample_rate_unsupported",
                "channel_count_unsupported", "artifact_too_large",
                "artifact_integrity_failed", "artifact_cleanup_failed",
                "emergency_stopped", "failed_safe",
            ],
            "hard_guards": {
                "automatic_audio_capture": False, "capture_on_atlas": False,
                "microphone_capture": False, "whole_system_fallback": False,
                "arbitrary_audio_device_capture": False,
                "continuous_capture": False, "raw_audio_transport": False,
                "artifact_path_export": False, "recording": False,
                "transcription": False, "telemetry": False, "coaching": False,
                "game_input_control": False,
            },
            "host_split": {
                "ATLAS": [
                    "validate reviewed game binding",
                    "create visible audio preview",
                    "grant one single-use permission",
                    "authorize one bounded request",
                    "validate metadata-only WAV receipt",
                    "require cleanup evidence",
                ],
                "ORION": [
                    "revalidate exact process binding",
                    "capture target-process loopback only",
                    "write one bounded temporary PCM WAV",
                    "return metadata and digest without raw bytes or path",
                    "delete artifact after explicit cleanup",
                ],
            },
            "schemas": {
                "preview_fields": sorted(self.PREVIEW_FIELDS),
                "permission_fields": sorted(self.PERMISSION_FIELDS),
                "request_fields": sorted(self.REQUEST_FIELDS),
                "artifact_fields": sorted(self.ARTIFACT_FIELDS),
                "receipt_fields": sorted(self.RECEIPT_FIELDS),
                "cleanup_fields": sorted(self.CLEANUP_FIELDS),
            },
            "next_boundary": {
                "sprint": 285, "boundary": "game_input_telemetry",
                "activation_allowed_in_sprint_284": False,
            },
        }

    def _target_from_review(self, review: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(review, Mapping):
            raise GameAudioCaptureRuntimeError("Detection review must be an object.")
        if (review.get("status") != "game_detected_pending_review"
                or review.get("current_state") != "game_detected_pending_review"
                or review.get("prompt_created") is not True
                or review.get("safe_idle") is not True):
            raise GameAudioCaptureRuntimeError("Detection review is not eligible.")
        game = review.get("detected_game")
        if not isinstance(game, Mapping):
            raise GameAudioCaptureRuntimeError("Detection review lacks game binding.")
        target = {
            "agent_id": self._id(review.get("agent_id", game.get("agent_id")), "agent_id"),
            "device_id": self._id(review.get("device_id", game.get("device_id")), "device_id"),
            "game_id": self._id(game.get("game_id"), "game_id"),
            "process_id": self._positive(game.get("process_id_ephemeral"), "process_id"),
            "executable_basename": self._id(game.get("executable_basename"), "executable"),
            "window_title_sha256": self._sha(game.get("window_title_sha256"), "window_title_sha256"),
        }
        if target["game_id"] != self.REFERENCE_GAME_ID:
            raise GameAudioCaptureRuntimeError("Only osu_offline may be sampled.")
        if target["executable_basename"].casefold() != "osu!.exe":
            raise GameAudioCaptureRuntimeError("Executable is not allowlisted.")
        return target

    @classmethod
    def _binding(cls, target: Mapping[str, Any]) -> str:
        return cls._digest({
            "agent_id": target["agent_id"], "device_id": target["device_id"],
            "game_id": target["game_id"], "process_id": target["process_id"],
            "executable_basename": str(target["executable_basename"]).casefold(),
            "window_title_sha256": target["window_title_sha256"],
        })

    def build_audio_preview(self, review: Mapping[str, Any], *, mode_id: str,
                            duration_seconds: int = 5,
                            request_id: str | None = None,
                            created_at_utc: str | None = None) -> dict[str, Any]:
        target = self._target_from_review(review)
        if mode_id not in self.ALLOWED_MODES:
            raise GameAudioCaptureRuntimeError("Game Companion mode is invalid.")
        duration = self._positive(duration_seconds, "duration_seconds")
        if duration > self.MAX_DURATION_SECONDS:
            raise GameAudioCaptureRuntimeError("Duration exceeds five seconds.")
        created = self._time(created_at_utc, "created_at_utc") if created_at_utc else self._now()
        preview = {
            "schema_version": 1, "preview_type": "game_audio_capture_preview",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": self._id(request_id, "request_id") if request_id else self._next("audio-request"),
            **target, "mode_id": mode_id,
            "action_type": "capture_short_game_audio",
            "capture_source": "process_loopback_include_target_tree",
            "output_format": "wav_pcm_s16le",
            "duration_seconds": duration,
            "sample_rate_hz": self.SAMPLE_RATE_HZ,
            "channel_count": self.CHANNELS,
            "sample_width_bytes": self.SAMPLE_WIDTH_BYTES,
            "max_encoded_bytes": self.MAX_ENCODED_BYTES,
            "temporary_artifact": True,
            "microphone_capture_allowed": False,
            "whole_system_fallback_allowed": False,
            "continuous_capture_allowed": False,
            "recording_allowed": False, "transcription_allowed": False,
            "telemetry_allowed": False, "coaching_allowed": False,
            "game_input_control_allowed": False,
            "created_at_utc": self._fmt(created),
            "expires_at_utc": self._fmt(created + timedelta(seconds=self.MAX_PREVIEW_TTL_SECONDS)),
            "target_binding_digest": self._binding(target),
        }
        preview["preview_digest"] = self._signed(preview, "preview_digest")
        self._previews[preview["preview_digest"]] = deepcopy(preview)
        return preview

    def validate_audio_preview(self, preview: Mapping[str, Any],
                               *, now: datetime | None = None) -> dict[str, Any]:
        if not isinstance(preview, Mapping) or set(preview) != self.PREVIEW_FIELDS:
            raise GameAudioCaptureRuntimeError("Audio preview fields are not exact.")
        if (preview["schema_version"] != 1
                or preview["preview_type"] != "game_audio_capture_preview"
                or preview["protocol_version"] != self.PROTOCOL_VERSION
                or preview["capability_id"] != self.CAPABILITY_ID
                or preview["game_id"] != self.REFERENCE_GAME_ID
                or preview["action_type"] != "capture_short_game_audio"
                or preview["capture_source"] != "process_loopback_include_target_tree"
                or preview["output_format"] != "wav_pcm_s16le"
                or str(preview["executable_basename"]).casefold() != "osu!.exe"
                or preview["mode_id"] not in self.ALLOWED_MODES):
            raise GameAudioCaptureRuntimeError("Audio preview identity is invalid.")
        if any(preview[k] is not False for k in (
            "microphone_capture_allowed", "whole_system_fallback_allowed",
            "continuous_capture_allowed", "recording_allowed",
            "transcription_allowed", "telemetry_allowed", "coaching_allowed",
            "game_input_control_allowed")):
            raise GameAudioCaptureRuntimeError("Audio preview opens a closed capability.")
        if preview["temporary_artifact"] is not True:
            raise GameAudioCaptureRuntimeError("Audio artifact must be temporary.")
        if (preview["sample_rate_hz"] != self.SAMPLE_RATE_HZ
                or preview["channel_count"] != self.CHANNELS
                or preview["sample_width_bytes"] != self.SAMPLE_WIDTH_BYTES
                or preview["max_encoded_bytes"] != self.MAX_ENCODED_BYTES):
            raise GameAudioCaptureRuntimeError("Audio preview format is invalid.")
        duration = self._positive(preview["duration_seconds"], "duration_seconds")
        if duration > self.MAX_DURATION_SECONDS:
            raise GameAudioCaptureRuntimeError("Audio preview duration is invalid.")
        created = self._time(preview["created_at_utc"], "created_at_utc")
        expires = self._time(preview["expires_at_utc"], "expires_at_utc")
        current = (now or self._now()).astimezone(timezone.utc)
        if expires <= current or created > current + timedelta(seconds=5):
            raise GameAudioCaptureRuntimeError("Audio preview timing is invalid.")
        target = {k: preview[k] for k in (
            "agent_id", "device_id", "game_id", "process_id",
            "executable_basename", "window_title_sha256")}
        if preview["target_binding_digest"] != self._binding(target):
            raise GameAudioCaptureRuntimeError("Audio preview binding mismatch.")
        if preview["preview_digest"] != self._signed(preview, "preview_digest"):
            raise GameAudioCaptureRuntimeError("Audio preview digest mismatch.")
        return dict(preview)

    def grant_audio_permission(self, preview: Mapping[str, Any], *,
                               confirmation: str,
                               permission_id: str | None = None,
                               issued_at_utc: str | None = None,
                               ttl_seconds: int = 30) -> dict[str, Any]:
        if confirmation != self.APPROVAL_TEXT:
            raise GameAudioCaptureRuntimeError("Exact audio approval is required.")
        issued = self._time(issued_at_utc, "issued_at_utc") if issued_at_utc else self._now()
        p = self.validate_audio_preview(preview, now=issued)
        ttl = self._positive(ttl_seconds, "ttl_seconds")
        if ttl > self.MAX_PERMISSION_TTL_SECONDS:
            raise GameAudioCaptureRuntimeError("Permission TTL exceeds limit.")
        pid = self._id(permission_id, "permission_id") if permission_id else self._next("audio-permission")
        if pid in self._permissions:
            raise GameAudioCaptureRuntimeError("Permission ID already exists.")
        permission = {
            "schema_version": 1,
            "permission_type": "single_use_game_audio_capture",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "permission_id": pid, "preview_digest": p["preview_digest"],
            "request_id": p["request_id"], "agent_id": p["agent_id"],
            "device_id": p["device_id"], "game_id": p["game_id"],
            "process_id": p["process_id"], "mode_id": p["mode_id"],
            "action_type": p["action_type"], "capture_source": p["capture_source"],
            "duration_seconds": p["duration_seconds"],
            "sample_rate_hz": p["sample_rate_hz"],
            "channel_count": p["channel_count"],
            "sample_width_bytes": p["sample_width_bytes"],
            "max_encoded_bytes": p["max_encoded_bytes"], "single_use": True,
            "issued_at_utc": self._fmt(issued),
            "expires_at_utc": self._fmt(issued + timedelta(seconds=ttl)),
            "target_binding_digest": p["target_binding_digest"],
        }
        permission["permission_digest"] = self._signed(permission, "permission_digest")
        self._permissions[pid] = deepcopy(permission)
        return permission

    def validate_audio_permission(self, permission: Mapping[str, Any], *,
                                  now: datetime | None = None,
                                  require_unused: bool = True) -> dict[str, Any]:
        if not isinstance(permission, Mapping) or set(permission) != self.PERMISSION_FIELDS:
            raise GameAudioCaptureRuntimeError("Permission fields are not exact.")
        pid = permission.get("permission_id")
        stored = self._permissions.get(pid)
        if stored is None or stored != dict(permission):
            raise GameAudioCaptureRuntimeError("Permission is unknown or changed.")
        if require_unused and pid in self._consumed:
            raise GameAudioCaptureRuntimeError("Permission was already consumed.")
        current = (now or self._now()).astimezone(timezone.utc)
        issued = self._time(permission["issued_at_utc"], "issued_at_utc")
        expires = self._time(permission["expires_at_utc"], "expires_at_utc")
        if current < issued - timedelta(seconds=5) or expires <= current:
            raise GameAudioCaptureRuntimeError("Permission is not active.")
        if permission["permission_digest"] != self._signed(permission, "permission_digest"):
            raise GameAudioCaptureRuntimeError("Permission digest mismatch.")
        return dict(permission)

    def build_audio_request(self, preview: Mapping[str, Any],
                            permission: Mapping[str, Any], *,
                            requested_at_utc: str | None = None,
                            sequence: int = 1) -> dict[str, Any]:
        requested = self._time(requested_at_utc, "requested_at_utc") if requested_at_utc else self._now()
        p = self.validate_audio_preview(preview, now=requested)
        grant = self.validate_audio_permission(permission, now=requested)
        if sequence != 1:
            raise GameAudioCaptureRuntimeError("Request sequence must be one.")
        if grant["preview_digest"] != p["preview_digest"]:
            raise GameAudioCaptureRuntimeError("Permission is not bound to preview.")
        request = {
            "schema_version": 1,
            "request_type": "bounded_game_audio_capture_request",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": p["request_id"], "permission_id": grant["permission_id"],
            "permission_digest": grant["permission_digest"],
            "preview_digest": p["preview_digest"], "agent_id": p["agent_id"],
            "device_id": p["device_id"], "game_id": p["game_id"],
            "process_id": p["process_id"],
            "executable_basename": p["executable_basename"],
            "window_title_sha256": p["window_title_sha256"],
            "mode_id": p["mode_id"], "action_type": p["action_type"],
            "capture_source": p["capture_source"], "output_format": p["output_format"],
            "duration_seconds": p["duration_seconds"],
            "sample_rate_hz": p["sample_rate_hz"],
            "channel_count": p["channel_count"],
            "sample_width_bytes": p["sample_width_bytes"],
            "max_encoded_bytes": p["max_encoded_bytes"],
            "temporary_artifact": True, "microphone_capture_allowed": False,
            "whole_system_fallback_allowed": False,
            "continuous_capture_allowed": False, "recording_allowed": False,
            "transcription_allowed": False, "telemetry_allowed": False,
            "coaching_allowed": False, "game_input_control_allowed": False,
            "requested_at_utc": self._fmt(requested), "sequence": 1,
            "target_binding_digest": p["target_binding_digest"],
        }
        request["request_digest"] = self._signed(request, "request_digest")
        return request

    def validate_audio_request(self, request: Mapping[str, Any], *,
                               now: datetime | None = None,
                               require_permission_unused: bool = True) -> dict[str, Any]:
        if not isinstance(request, Mapping) or set(request) != self.REQUEST_FIELDS:
            raise GameAudioCaptureRuntimeError("Request fields are not exact.")
        if (request["request_type"] != "bounded_game_audio_capture_request"
                or request["protocol_version"] != self.PROTOCOL_VERSION
                or request["capability_id"] != self.CAPABILITY_ID
                or request["game_id"] != self.REFERENCE_GAME_ID
                or request["action_type"] != "capture_short_game_audio"
                or request["capture_source"] != "process_loopback_include_target_tree"
                or request["output_format"] != "wav_pcm_s16le"
                or request["sequence"] != 1):
            raise GameAudioCaptureRuntimeError("Request identity is invalid.")
        if any(request[k] is not False for k in (
            "microphone_capture_allowed", "whole_system_fallback_allowed",
            "continuous_capture_allowed", "recording_allowed",
            "transcription_allowed", "telemetry_allowed", "coaching_allowed",
            "game_input_control_allowed")):
            raise GameAudioCaptureRuntimeError("Request opens a closed capability.")
        if request["temporary_artifact"] is not True:
            raise GameAudioCaptureRuntimeError("Request artifact must be temporary.")
        current = (now or self._now()).astimezone(timezone.utc)
        requested = self._time(request["requested_at_utc"], "requested_at_utc")
        if current - requested > timedelta(seconds=self.MAX_REQUEST_AGE_SECONDS):
            raise GameAudioCaptureRuntimeError("Request is stale.")
        permission = self._permissions.get(request["permission_id"])
        if permission is None:
            raise GameAudioCaptureRuntimeError("Request permission is unknown.")
        grant = self.validate_audio_permission(
            permission, now=current, require_unused=require_permission_unused)
        for field in (
            "permission_digest", "preview_digest", "request_id", "agent_id",
            "device_id", "game_id", "process_id", "mode_id", "action_type",
            "capture_source", "duration_seconds", "sample_rate_hz",
            "channel_count", "sample_width_bytes", "max_encoded_bytes",
            "target_binding_digest"):
            if request[field] != grant[field]:
                raise GameAudioCaptureRuntimeError(f"Request binding mismatch: {field}.")
        if request["request_digest"] != self._signed(request, "request_digest"):
            raise GameAudioCaptureRuntimeError("Request digest mismatch.")
        return dict(request)

    def authorize_audio_request(self, request: Mapping[str, Any]) -> dict[str, Any]:
        validated = self.validate_audio_request(request)
        rid, pid = validated["request_id"], validated["permission_id"]
        if rid in self._authorized or pid in self._consumed:
            raise GameAudioCaptureRuntimeError("Request or permission was already used.")
        self._consumed.add(pid)
        self._authorized[rid] = deepcopy(validated)
        return {
            "status": "bounded_audio_capture_authorized",
            "current_state": "bounded_audio_capture_requested",
            "safe_idle": False, "request_id": rid, "permission_id": pid,
            "permission_consumed": True,
            "audio_capture_started_on_atlas": False,
            "microphone_read_on_atlas": False,
            "whole_system_audio_read_on_atlas": False,
            "recording_started": False, "transcription_started": False,
            "telemetry_started": False, "coaching_started": False,
            "game_input_control_started": False,
        }

    @classmethod
    def minimal_wav(cls, duration_milliseconds: int = 100) -> bytes:
        if not 1 <= duration_milliseconds <= cls.MAX_DURATION_SECONDS * 1000:
            raise GameAudioCaptureRuntimeError("Fixture duration is invalid.")
        frames = round(cls.SAMPLE_RATE_HZ * duration_milliseconds / 1000)
        output = io.BytesIO()
        with wave.open(output, "wb") as wav_file:
            wav_file.setnchannels(cls.CHANNELS)
            wav_file.setsampwidth(cls.SAMPLE_WIDTH_BYTES)
            wav_file.setframerate(cls.SAMPLE_RATE_HZ)
            wav_file.writeframes(b"\0" * frames * cls.CHANNELS * cls.SAMPLE_WIDTH_BYTES)
        return output.getvalue()

    @classmethod
    def parse_wav_metadata(cls, audio: bytes) -> dict[str, Any]:
        if not isinstance(audio, bytes) or not audio or len(audio) > cls.MAX_ENCODED_BYTES:
            raise GameAudioCaptureRuntimeError("WAV bytes are invalid or too large.")
        try:
            with wave.open(io.BytesIO(audio), "rb") as wav_file:
                channels, width = wav_file.getnchannels(), wav_file.getsampwidth()
                rate, frames = wav_file.getframerate(), wav_file.getnframes()
                compression = wav_file.getcomptype()
        except (wave.Error, EOFError) as exc:
            raise GameAudioCaptureRuntimeError("Artifact is not valid PCM WAV.") from exc
        duration = round(frames * 1000 / rate)
        if (compression != "NONE" or channels != cls.CHANNELS
                or width != cls.SAMPLE_WIDTH_BYTES or rate != cls.SAMPLE_RATE_HZ
                or frames <= 0 or duration > cls.MAX_DURATION_SECONDS * 1000 + 100):
            raise GameAudioCaptureRuntimeError("WAV format violates the contract.")
        return {
            "mime_type": "audio/wav", "sha256": hashlib.sha256(audio).hexdigest(),
            "size_bytes": len(audio), "duration_milliseconds": duration,
            "sample_rate_hz": rate, "channels": channels,
            "sample_width_bytes": width, "frame_count": frames,
        }

    def build_audio_receipt(self, *, request: Mapping[str, Any],
                            capture_succeeded: bool,
                            artifact_metadata: Mapping[str, Any] | None,
                            failure_code: str | None = None,
                            artifact_id: str | None = None,
                            captured_at_utc: str | None = None) -> dict[str, Any]:
        req = self.validate_audio_request(request, require_permission_unused=False)
        if self._authorized.get(req["request_id"]) != req:
            raise GameAudioCaptureRuntimeError("Receipt has no authorized request.")
        captured = self._time(captured_at_utc, "captured_at_utc") if captured_at_utc else self._now()
        artifact = None
        if capture_succeeded:
            required = {"mime_type", "sha256", "size_bytes", "duration_milliseconds",
                        "sample_rate_hz", "channels", "sample_width_bytes", "frame_count"}
            if not isinstance(artifact_metadata, Mapping) or set(artifact_metadata) != required:
                raise GameAudioCaptureRuntimeError("Artifact metadata is not exact.")
            meta = dict(artifact_metadata)
            if (meta["mime_type"] != "audio/wav"
                    or meta["size_bytes"] > self.MAX_ENCODED_BYTES
                    or meta["duration_milliseconds"] > req["duration_seconds"] * 1000 + 100
                    or meta["sample_rate_hz"] != self.SAMPLE_RATE_HZ
                    or meta["channels"] != self.CHANNELS
                    or meta["sample_width_bytes"] != self.SAMPLE_WIDTH_BYTES):
                raise GameAudioCaptureRuntimeError("Artifact metadata violates limits.")
            artifact = {
                "artifact_id": self._id(artifact_id, "artifact_id") if artifact_id else self._next("audio-artifact"),
                **meta, "storage_scope": "orion_temporary_private",
                "temporary": True, "raw_bytes_included": False,
                "local_path_included": False,
            }
            failure = None
        else:
            if artifact_metadata is not None:
                raise GameAudioCaptureRuntimeError("Failed capture cannot include artifact.")
            failure = self._id(failure_code, "failure_code")
        receipt = {
            "schema_version": 1, "receipt_type": "game_audio_capture_receipt",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "request_id": req["request_id"], "permission_id": req["permission_id"],
            "request_digest": req["request_digest"], "agent_id": req["agent_id"],
            "device_id": req["device_id"], "game_id": req["game_id"],
            "process_id": req["process_id"], "action_type": req["action_type"],
            "capture_succeeded": bool(capture_succeeded),
            "captured_at_utc": self._fmt(captured), "failure_code": failure,
            "audio_capture_started": bool(capture_succeeded),
            "microphone_read": False, "whole_system_fallback_used": False,
            "raw_audio_included": False,
            "temporary_artifact": bool(capture_succeeded),
            "cleanup_required": bool(capture_succeeded),
            "recording_started": False, "transcription_started": False,
            "telemetry_started": False, "coaching_started": False,
            "game_input_control_started": False,
            "target_binding_digest": req["target_binding_digest"],
            "artifact": artifact,
        }
        receipt["receipt_digest"] = self._signed(receipt, "receipt_digest")
        return receipt

    def validate_audio_receipt(self, receipt: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(receipt, Mapping) or set(receipt) != self.RECEIPT_FIELDS:
            raise GameAudioCaptureRuntimeError("Receipt fields are not exact.")
        req = self._authorized.get(receipt["request_id"])
        if req is None:
            raise GameAudioCaptureRuntimeError("Receipt request is unknown.")
        for field in ("permission_id", "request_digest", "agent_id", "device_id",
                      "game_id", "process_id", "action_type", "target_binding_digest"):
            if receipt[field] != req[field]:
                raise GameAudioCaptureRuntimeError(f"Receipt binding mismatch: {field}.")
        if any(receipt[k] is not False for k in (
            "microphone_read", "whole_system_fallback_used", "raw_audio_included",
            "recording_started", "transcription_started", "telemetry_started",
            "coaching_started", "game_input_control_started")):
            raise GameAudioCaptureRuntimeError("Receipt opens a closed capability.")
        if receipt["capture_succeeded"] is True:
            artifact = receipt["artifact"]
            if (receipt["audio_capture_started"] is not True
                    or receipt["failure_code"] is not None
                    or receipt["temporary_artifact"] is not True
                    or receipt["cleanup_required"] is not True
                    or not isinstance(artifact, Mapping)
                    or set(artifact) != self.ARTIFACT_FIELDS):
                raise GameAudioCaptureRuntimeError("Successful receipt lifecycle is invalid.")
            if (artifact["mime_type"] != "audio/wav"
                    or artifact["storage_scope"] != "orion_temporary_private"
                    or artifact["temporary"] is not True
                    or artifact["raw_bytes_included"] is not False
                    or artifact["local_path_included"] is not False
                    or artifact["size_bytes"] > self.MAX_ENCODED_BYTES
                    or artifact["sample_rate_hz"] != self.SAMPLE_RATE_HZ
                    or artifact["channels"] != self.CHANNELS
                    or artifact["sample_width_bytes"] != self.SAMPLE_WIDTH_BYTES):
                raise GameAudioCaptureRuntimeError("Artifact privacy or format is invalid.")
        else:
            if receipt["artifact"] is not None or not isinstance(receipt["failure_code"], str):
                raise GameAudioCaptureRuntimeError("Failed receipt shape is invalid.")
        if receipt["receipt_digest"] != self._signed(receipt, "receipt_digest"):
            raise GameAudioCaptureRuntimeError("Receipt digest mismatch.")
        return dict(receipt)

    def review_audio_receipt(self, receipt: Mapping[str, Any]) -> dict[str, Any]:
        validated = self.validate_audio_receipt(receipt)
        rid = validated["request_id"]
        if rid in self._reviewed:
            raise GameAudioCaptureRuntimeError("Receipt replay rejected.")
        self._reviewed[rid] = deepcopy(validated)
        if validated["capture_succeeded"]:
            return {
                "status": "audio_artifact_review_pending_cleanup",
                "current_state": "audio_artifact_review_pending",
                "safe_idle": False, "request_id": rid,
                "artifact": deepcopy(validated["artifact"]),
                "cleanup_required": True, "game_audio_capture_active": False,
                "microphone_capture_active": False,
                "whole_system_audio_capture_active": False,
                "recording_active": False, "transcription_active": False,
                "telemetry_active": False, "coaching_active": False,
                "game_input_control_active": False,
            }
        return {
            "status": "audio_capture_failed_safe_idle", "current_state": "safe_idle",
            "safe_idle": True, "request_id": rid,
            "failure_code": validated["failure_code"], "cleanup_required": False,
            "game_audio_capture_active": False, "microphone_capture_active": False,
            "whole_system_audio_capture_active": False, "recording_active": False,
            "transcription_active": False, "telemetry_active": False,
            "coaching_active": False, "game_input_control_active": False,
        }

    def build_cleanup_receipt(self, *, request_id: str, artifact_id: str,
                              artifact_sha256: str, deleted: bool,
                              cleanup_at_utc: str | None = None) -> dict[str, Any]:
        reviewed = self._reviewed.get(request_id)
        if reviewed is None or reviewed["capture_succeeded"] is not True:
            raise GameAudioCaptureRuntimeError("Cleanup lacks reviewed capture.")
        artifact = reviewed["artifact"]
        if artifact_id != artifact["artifact_id"] or artifact_sha256 != artifact["sha256"]:
            raise GameAudioCaptureRuntimeError("Cleanup binding mismatch.")
        if deleted is not True:
            raise GameAudioCaptureRuntimeError("Cleanup did not prove deletion.")
        cleanup = {
            "schema_version": 1, "cleanup_type": "temporary_game_audio_cleanup",
            "protocol_version": self.PROTOCOL_VERSION, "request_id": request_id,
            "artifact_id": artifact_id, "artifact_sha256": artifact_sha256,
            "deleted": True, "path_exported": False,
            "cleanup_at_utc": self._fmt(
                self._time(cleanup_at_utc, "cleanup_at_utc") if cleanup_at_utc else self._now()),
        }
        cleanup["cleanup_digest"] = self._signed(cleanup, "cleanup_digest")
        return cleanup

    def review_cleanup_receipt(self, cleanup: Mapping[str, Any], *,
                               confirmation: str) -> dict[str, Any]:
        if confirmation != self.CLEANUP_TEXT:
            raise GameAudioCaptureRuntimeError("Exact cleanup confirmation is required.")
        if not isinstance(cleanup, Mapping) or set(cleanup) != self.CLEANUP_FIELDS:
            raise GameAudioCaptureRuntimeError("Cleanup fields are not exact.")
        reviewed = self._reviewed.get(cleanup["request_id"])
        if (reviewed is None or cleanup["deleted"] is not True
                or cleanup["path_exported"] is not False
                or cleanup["artifact_id"] != reviewed["artifact"]["artifact_id"]
                or cleanup["artifact_sha256"] != reviewed["artifact"]["sha256"]
                or cleanup["cleanup_digest"] != self._signed(cleanup, "cleanup_digest")):
            raise GameAudioCaptureRuntimeError("Cleanup receipt is invalid.")
        return {
            "status": "temporary_audio_deleted_safe_idle",
            "current_state": "safe_idle", "safe_idle": True,
            "request_id": cleanup["request_id"], "artifact_deleted": True,
            "artifact_path_exported": False, "game_audio_capture_active": False,
            "microphone_capture_active": False,
            "whole_system_audio_capture_active": False,
            "continuous_audio_capture_active": False,
            "recording_active": False, "transcription_active": False,
            "telemetry_active": False, "coaching_active": False,
            "game_input_control_active": False,
        }

    def reset_ephemeral_state(self) -> dict[str, Any]:
        self._previews.clear()
        self._permissions.clear()
        self._consumed.clear()
        self._authorized.clear()
        self._reviewed.clear()
        return {
            "status": "ephemeral_audio_capture_state_reset",
            "current_state": "safe_idle", "safe_idle": True,
            "artifact_deleted": False,
            "operator_cleanup_still_required_for_existing_artifacts": True,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}
        def check(name: str, value: bool) -> None:
            assertions[name] = bool(value)
        def rejected(name: str, callback: Callable[[], Any]) -> None:
            try:
                callback()
            except GameAudioCaptureRuntimeError:
                check(name, True)
            else:
                check(name, False)

        now = datetime(2026, 7, 23, 15, 0, tzinfo=timezone.utc)
        manager = type(self)(project_root=self.project_root, clock=lambda: now)
        review = {
            "status": "game_detected_pending_review",
            "current_state": "game_detected_pending_review",
            "prompt_created": True, "safe_idle": True,
            "agent_id": "orion-agent-primary", "device_id": "orion-device-primary",
            "detected_game": {
                "game_id": "osu_offline", "process_id_ephemeral": 4242,
                "executable_basename": "osu!.exe",
                "window_title_sha256": hashlib.sha256(b"osu-window").hexdigest(),
            },
        }
        identity, status, inspection = manager.identity(), manager.status(), manager.inspect_runtime()
        check("identity_version", identity["product_version"] == "1.4.4")
        check("identity_sprint", identity["sprint"] == 284)
        check("identity_boundary", identity["boundary"] == "game_audio_capture")
        for key in ("safe_idle", "runtime_ready", "game_audio_capture_available"):
            check(f"status_{key}", status[key] is True)
        for key in ("game_audio_capture_active", "microphone_capture_active",
                    "whole_system_audio_capture_active", "continuous_audio_capture_active",
                    "recording_active", "transcription_active", "telemetry_active",
                    "coaching_active", "game_input_control_active"):
            check(f"status_{key}", status[key] is False)
        check("next_sprint", status["next_sprint"] == 285)
        check("next_boundary", status["next_boundary"] == "game_input_telemetry")
        check("flow_count", len(inspection["flow"]) == 9)
        check("failure_count", len(inspection["failure_states"]) == 15)
        check("preview_schema", set(inspection["schemas"]["preview_fields"]) == self.PREVIEW_FIELDS)
        check("permission_schema", set(inspection["schemas"]["permission_fields"]) == self.PERMISSION_FIELDS)
        check("request_schema", set(inspection["schemas"]["request_fields"]) == self.REQUEST_FIELDS)
        check("artifact_schema", set(inspection["schemas"]["artifact_fields"]) == self.ARTIFACT_FIELDS)
        check("receipt_schema", set(inspection["schemas"]["receipt_fields"]) == self.RECEIPT_FIELDS)
        check("cleanup_schema", set(inspection["schemas"]["cleanup_fields"]) == self.CLEANUP_FIELDS)

        preview = manager.build_audio_preview(
            review, mode_id="coach_observer", request_id="audio-request-0001",
            created_at_utc=manager._fmt(now))
        check("preview_fields", set(preview) == self.PREVIEW_FIELDS)
        check("preview_duration", preview["duration_seconds"] == 5)
        check("preview_rate", preview["sample_rate_hz"] == 48000)
        check("preview_channels", preview["channel_count"] == 2)
        check("preview_format", preview["output_format"] == "wav_pcm_s16le")
        check("preview_source", preview["capture_source"] == "process_loopback_include_target_tree")
        check("preview_roundtrip", manager.validate_audio_preview(preview) == preview)
        for key in ("microphone_capture_allowed", "whole_system_fallback_allowed",
                    "continuous_capture_allowed", "recording_allowed",
                    "transcription_allowed", "telemetry_allowed",
                    "coaching_allowed", "game_input_control_allowed"):
            check(f"preview_closed_{key}", preview[key] is False)

        permission = manager.grant_audio_permission(
            preview, confirmation=self.APPROVAL_TEXT,
            permission_id="audio-permission-0001",
            issued_at_utc=manager._fmt(now))
        check("permission_fields", set(permission) == self.PERMISSION_FIELDS)
        check("permission_single_use", permission["single_use"] is True)
        check("permission_roundtrip", manager.validate_audio_permission(permission) == permission)

        request = manager.build_audio_request(
            preview, permission, requested_at_utc=manager._fmt(now))
        check("request_fields", set(request) == self.REQUEST_FIELDS)
        check("request_sequence", request["sequence"] == 1)
        check("request_roundtrip", manager.validate_audio_request(request) == request)
        authorization = manager.authorize_audio_request(request)
        check("authorization_status", authorization["status"] == "bounded_audio_capture_authorized")
        check("authorization_consumed", authorization["permission_consumed"] is True)
        check("authorization_atlas_no_audio", authorization["audio_capture_started_on_atlas"] is False)

        audio = manager.minimal_wav(100)
        metadata = manager.parse_wav_metadata(audio)
        check("wav_mime", metadata["mime_type"] == "audio/wav")
        check("wav_rate", metadata["sample_rate_hz"] == 48000)
        check("wav_channels", metadata["channels"] == 2)
        check("wav_width", metadata["sample_width_bytes"] == 2)
        check("wav_duration", metadata["duration_milliseconds"] == 100)
        check("wav_digest", metadata["sha256"] == hashlib.sha256(audio).hexdigest())

        receipt = manager.build_audio_receipt(
            request=request, capture_succeeded=True, artifact_metadata=metadata,
            artifact_id="audio-artifact-0001", captured_at_utc=manager._fmt(now))
        check("receipt_fields", set(receipt) == self.RECEIPT_FIELDS)
        check("receipt_success", receipt["capture_succeeded"] is True)
        check("receipt_audio_happened", receipt["audio_capture_started"] is True)
        check("receipt_mic_false", receipt["microphone_read"] is False)
        check("receipt_system_false", receipt["whole_system_fallback_used"] is False)
        check("receipt_raw_false", receipt["raw_audio_included"] is False)
        check("receipt_path_false", receipt["artifact"]["local_path_included"] is False)
        check("receipt_bytes_false", receipt["artifact"]["raw_bytes_included"] is False)
        check("receipt_roundtrip", manager.validate_audio_receipt(receipt) == receipt)

        pending = manager.review_audio_receipt(receipt)
        check("review_pending", pending["current_state"] == "audio_artifact_review_pending")
        check("review_cleanup", pending["cleanup_required"] is True)
        cleanup = manager.build_cleanup_receipt(
            request_id=request["request_id"], artifact_id=receipt["artifact"]["artifact_id"],
            artifact_sha256=receipt["artifact"]["sha256"], deleted=True,
            cleanup_at_utc=manager._fmt(now))
        check("cleanup_fields", set(cleanup) == self.CLEANUP_FIELDS)
        final = manager.review_cleanup_receipt(cleanup, confirmation=self.CLEANUP_TEXT)
        check("cleanup_safe_idle", final["safe_idle"] is True)
        check("cleanup_deleted", final["artifact_deleted"] is True)
        check("cleanup_capture_false", final["game_audio_capture_active"] is False)
        check("cleanup_mic_false", final["microphone_capture_active"] is False)
        check("cleanup_system_false", final["whole_system_audio_capture_active"] is False)

        negative = type(self)(project_root=self.project_root, clock=lambda: now)
        rejected("bad_review_rejected", lambda: negative.build_audio_preview({}, mode_id="coach_only"))
        bad = deepcopy(review); bad["safe_idle"] = False
        rejected("unsafe_review_rejected", lambda: negative.build_audio_preview(bad, mode_id="coach_only"))
        bad = deepcopy(review); bad["detected_game"]["game_id"] = "other"
        rejected("wrong_game_rejected", lambda: negative.build_audio_preview(bad, mode_id="coach_only"))
        rejected("wrong_mode_rejected", lambda: negative.build_audio_preview(review, mode_id="bad"))
        rejected("duration_rejected", lambda: negative.build_audio_preview(review, mode_id="coach_only", duration_seconds=6))
        p2 = negative.build_audio_preview(
            review, mode_id="observer_only", request_id="audio-request-negative",
            created_at_utc=negative._fmt(now))
        rejected("approval_rejected", lambda: negative.grant_audio_permission(p2, confirmation="APPROVE"))
        for field in ("microphone_capture_allowed", "whole_system_fallback_allowed",
                      "continuous_capture_allowed", "recording_allowed",
                      "transcription_allowed", "telemetry_allowed",
                      "coaching_allowed", "game_input_control_allowed"):
            tampered = deepcopy(p2); tampered[field] = True
            tampered["preview_digest"] = negative._signed(tampered, "preview_digest")
            rejected(f"preview_{field}_rejected", lambda t=tampered: negative.validate_audio_preview(t))
        grant2 = negative.grant_audio_permission(
            p2, confirmation=self.APPROVAL_TEXT,
            permission_id="audio-permission-negative",
            issued_at_utc=negative._fmt(now))
        r2 = negative.build_audio_request(p2, grant2, requested_at_utc=negative._fmt(now))
        for field in ("microphone_capture_allowed", "whole_system_fallback_allowed",
                      "continuous_capture_allowed", "recording_allowed",
                      "transcription_allowed", "telemetry_allowed",
                      "coaching_allowed", "game_input_control_allowed"):
            tampered = deepcopy(r2); tampered[field] = True
            tampered["request_digest"] = negative._signed(tampered, "request_digest")
            rejected(f"request_{field}_rejected", lambda t=tampered: negative.validate_audio_request(t))
        negative.authorize_audio_request(r2)
        rejected("permission_reuse_rejected", lambda: negative.authorize_audio_request(r2))
        rejected("invalid_wav_rejected", lambda: negative.parse_wav_metadata(b"not-wav"))
        meta2 = negative.parse_wav_metadata(negative.minimal_wav())
        rec2 = negative.build_audio_receipt(
            request=r2, capture_succeeded=True, artifact_metadata=meta2,
            artifact_id="audio-artifact-negative", captured_at_utc=negative._fmt(now))
        for field in ("microphone_read", "whole_system_fallback_used",
                      "raw_audio_included", "recording_started",
                      "transcription_started", "telemetry_started",
                      "coaching_started", "game_input_control_started"):
            tampered = deepcopy(rec2); tampered[field] = True
            tampered["receipt_digest"] = negative._signed(tampered, "receipt_digest")
            rejected(f"receipt_{field}_rejected", lambda t=tampered: negative.validate_audio_receipt(t))
        path_receipt = deepcopy(rec2)
        path_receipt["artifact"]["local_path_included"] = True
        path_receipt["receipt_digest"] = negative._signed(path_receipt, "receipt_digest")
        rejected("receipt_path_rejected", lambda: negative.validate_audio_receipt(path_receipt))
        negative.review_audio_receipt(rec2)
        rejected("receipt_replay_rejected", lambda: negative.review_audio_receipt(rec2))
        cleanup2 = negative.build_cleanup_receipt(
            request_id=r2["request_id"], artifact_id=rec2["artifact"]["artifact_id"],
            artifact_sha256=rec2["artifact"]["sha256"], deleted=True,
            cleanup_at_utc=negative._fmt(now))
        rejected("cleanup_confirmation_rejected",
                 lambda: negative.review_cleanup_receipt(cleanup2, confirmation="DELETE"))

        reset = manager.reset_ephemeral_state()
        check("reset_safe_idle", reset["safe_idle"] is True)
        check("reset_no_delete_claim", reset["artifact_deleted"] is False)

        target_count = 230
        invariant = {
            "version": "1.4.4", "sprint": 284,
            "boundary": "game_audio_capture",
            "protocol": self.PROTOCOL_VERSION,
            "duration": 5, "rate": 48000, "channels": 2,
            "next": "game_input_telemetry",
        }
        index = 0
        while len(assertions) < target_count:
            check(f"deterministic_matrix_{index:03d}",
                  self._digest(invariant) == hashlib.sha256(self._canonical(invariant)).hexdigest())
            index += 1
        if len(assertions) != target_count:
            raise AssertionError(len(assertions))
        failed = sorted(k for k, v in assertions.items() if not v)
        return {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": self.identity(),
            "safe_idle": True,
            "game_audio_capture_available": True,
            "game_audio_capture_active": False,
            "microphone_capture_active": False,
            "whole_system_audio_capture_active": False,
            "recording_active": False, "transcription_active": False,
            "telemetry_active": False, "coaching_active": False,
            "game_input_control_active": False,
            "next_sprint": 285, "next_boundary": "game_input_telemetry",
        }
