"""Sprint 283 bounded one-shot game-window capture runtime.

ATLAS remains the authority. ORION may capture exactly one already-reviewed
supported-game window only after an explicit preview and single-use permission.
Raw image bytes and local paths never enter ATLAS packets.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
import tempfile
import zlib
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from aura.game_companion_runtime_foundation import (
    AuraGameCompanionRuntimeFoundationManager,
    GameCompanionRuntimeFoundationError,
)
from aura.supported_game_detection_runtime import (
    AuraSupportedGameDetectionRuntimeManager,
)


class GameWindowCaptureRuntimeError(RuntimeError):
    """Raised when a Sprint 283 capture contract fails closed."""


@dataclass(frozen=True, slots=True)
class GameWindowCaptureIdentity:
    component_name: str
    component_version: str
    protocol_version: str
    product_version: str
    sprint: int
    boundary: str
    atlas_role: str
    orion_role: str
    capability_id: str
    reference_game_id: str


class AuraGameWindowCaptureRuntimeManager:
    """Coordinate reviewed, permission-bound, single-frame game capture."""

    COMPONENT_NAME = "game_window_capture_runtime"
    COMPONENT_VERSION = "0.1.0"
    PROTOCOL_VERSION = "aura-game-window-capture-v1"
    PRODUCT_VERSION = "1.4.3"
    SPRINT = 283
    BOUNDARY = "game_window_capture"
    ATLAS_ROLE = "ATLAS_CAPTURE_REVIEW_AUTHORITY"
    ORION_ROLE = "ORION_EXPLICIT_ONE_SHOT_CAPTURE_SOURCE"
    CAPABILITY_ID = "orion.game.capture_window.one_shot"
    REFERENCE_GAME_ID = "osu_offline"
    ACTION_TYPE = "capture_selected_window"

    MAX_ID_LENGTH = 64
    MAX_CLOCK_SKEW_SECONDS = 5
    MAX_PREVIEW_TTL_SECONDS = 60
    MAX_REQUEST_AGE_SECONDS = 15
    MAX_SEQUENCE = 2**63 - 1
    MAX_PROCESS_ID = 2**32 - 1
    MAX_WIDTH = 3840
    MAX_HEIGHT = 2160
    MAX_PIXELS = 3840 * 2160
    MAX_ENCODED_BYTES = 8 * 1024 * 1024
    MAX_ARTIFACT_ID_LENGTH = 96
    MAX_ERROR_CODE_LENGTH = 64
    PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
    APPROVAL_CONFIRMATION = "APPROVE ONE GAME WINDOW CAPTURE"
    CLEANUP_CONFIRMATION = "DELETE TEMPORARY GAME CAPTURE"

    IDENTIFIER_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")
    REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{2,95}$")
    SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
    EXECUTABLE_RE = re.compile(
        r"^[A-Za-z0-9][A-Za-z0-9 !()._+\-]{0,127}\.exe$",
        re.IGNORECASE,
    )

    PREVIEW_FIELDS = frozenset(
        {
            "schema_version",
            "preview_type",
            "protocol_version",
            "capability_id",
            "action_type",
            "request_id",
            "agent_id",
            "device_id",
            "game_id",
            "mode_id",
            "process_id",
            "executable_basename",
            "window_title_sha256",
            "target_binding_digest",
            "max_width",
            "max_height",
            "max_pixels",
            "max_encoded_bytes",
            "frame_limit",
            "output_format",
            "temporary_artifact",
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
            "created_at_utc",
            "expires_at_utc",
            "preview_digest",
        }
    )
    PERMISSION_FIELDS = frozenset(
        {
            "schema_version",
            "permission_type",
            "protocol_version",
            "capability_id",
            "action_type",
            "permission_id",
            "preview_digest",
            "target_binding_digest",
            "agent_id",
            "device_id",
            "game_id",
            "mode_id",
            "process_id",
            "single_use",
            "frame_limit",
            "issued_at_utc",
            "expires_at_utc",
            "permission_digest",
        }
    )
    REQUEST_FIELDS = frozenset(
        {
            "schema_version",
            "request_type",
            "protocol_version",
            "capability_id",
            "action_type",
            "request_id",
            "permission_id",
            "permission_digest",
            "preview_digest",
            "target_binding_digest",
            "agent_id",
            "device_id",
            "game_id",
            "mode_id",
            "process_id",
            "executable_basename",
            "window_title_sha256",
            "sequence",
            "requested_at_utc",
            "max_width",
            "max_height",
            "max_pixels",
            "max_encoded_bytes",
            "frame_limit",
            "output_format",
            "temporary_artifact",
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
            "request_digest",
        }
    )
    ARTIFACT_FIELDS = frozenset(
        {
            "artifact_id",
            "mime_type",
            "sha256",
            "size_bytes",
            "width",
            "height",
            "pixel_count",
            "storage_scope",
            "temporary",
            "raw_bytes_included",
            "local_path_included",
        }
    )
    RECEIPT_FIELDS = frozenset(
        {
            "schema_version",
            "receipt_type",
            "protocol_version",
            "capability_id",
            "action_type",
            "request_id",
            "request_digest",
            "permission_id",
            "target_binding_digest",
            "agent_id",
            "device_id",
            "game_id",
            "process_id",
            "captured_at_utc",
            "frame_count",
            "capture_succeeded",
            "failure_code",
            "artifact",
            "temporary_artifact",
            "cleanup_required",
            "screen_fallback_used",
            "raw_window_title_included",
            "audio_capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "game_input_control_started",
            "receipt_digest",
        }
    )
    CLEANUP_FIELDS = frozenset(
        {
            "schema_version",
            "cleanup_type",
            "protocol_version",
            "request_id",
            "artifact_id",
            "artifact_sha256",
            "deleted",
            "path_exported",
            "cleanup_at_utc",
            "cleanup_digest",
        }
    )

    CLOSED_RUNTIME_FIELDS = (
        "background_capture_active",
        "continuous_capture_active",
        "full_screen_capture_active",
        "audio_capture_active",
        "recording_active",
        "telemetry_active",
        "coaching_active",
        "game_input_control_active",
        "application_launch_active",
        "voice_command_to_action_active",
        "autonomous_gameplay_active",
        "multiplayer_automation_active",
        "raw_image_transport_active",
        "raw_window_title_export_active",
        "artifact_path_export_active",
        "persistent_capture_active",
        "network_listener_active",
    )

    def __init__(
        self,
        project_root: Path,
        *,
        now_provider: Callable[[], datetime] | None = None,
        id_provider: Callable[[str], str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.foundation = AuraGameCompanionRuntimeFoundationManager(
            project_root=self.project_root
        )
        self.detection = AuraSupportedGameDetectionRuntimeManager(
            self.project_root,
            now_provider=now_provider,
        )
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._id_provider = id_provider or (
            lambda prefix: prefix
            + hashlib.sha256(
                f"{prefix}|{self._format_utc(self._now())}".encode("utf-8")
            ).hexdigest()[:20]
        )
        self._permissions: dict[str, dict[str, Any]] = {}
        self._authorized_requests: dict[str, dict[str, Any]] = {}
        self._reviewed_receipts: dict[str, dict[str, Any]] = {}
        self._state = "safe_idle"

    def _now(self) -> datetime:
        return self._now_provider().astimezone(timezone.utc)

    @staticmethod
    def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")

    @classmethod
    def _digest(cls, payload: Mapping[str, Any]) -> str:
        return hashlib.sha256(cls._canonical_bytes(payload)).hexdigest()

    @classmethod
    def _signed_digest(
        cls,
        payload: Mapping[str, Any],
        field: str,
    ) -> str:
        unsigned = dict(payload)
        unsigned.pop(field, None)
        return cls._digest(unsigned)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat(
            timespec="milliseconds"
        ).replace("+00:00", "Z")

    @classmethod
    def _parse_utc(cls, value: Any, *, label: str) -> datetime:
        if not isinstance(value, str) or not 1 <= len(value) <= 40:
            raise GameWindowCaptureRuntimeError(
                f"{label} must be a bounded UTC timestamp."
            )
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise GameWindowCaptureRuntimeError(
                f"{label} is not valid ISO-8601."
            ) from exc
        if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
            raise GameWindowCaptureRuntimeError(
                f"{label} must use UTC."
            )
        return parsed.astimezone(timezone.utc)

    @classmethod
    def _identifier(cls, value: Any, *, label: str) -> str:
        if (
            not isinstance(value, str)
            or len(value) > cls.MAX_ID_LENGTH
            or cls.IDENTIFIER_RE.fullmatch(value) is None
        ):
            raise GameWindowCaptureRuntimeError(
                f"{label} is not a valid bounded identifier."
            )
        return value

    @classmethod
    def _request_id(cls, value: Any, *, label: str) -> str:
        if (
            not isinstance(value, str)
            or len(value) > cls.MAX_ARTIFACT_ID_LENGTH
            or cls.REQUEST_ID_RE.fullmatch(value) is None
        ):
            raise GameWindowCaptureRuntimeError(
                f"{label} is not a valid bounded request identifier."
            )
        return value

    @classmethod
    def _sha(cls, value: Any, *, label: str, nullable: bool = False) -> str | None:
        if nullable and value is None:
            return None
        if not isinstance(value, str) or cls.SHA256_RE.fullmatch(value) is None:
            raise GameWindowCaptureRuntimeError(
                f"{label} must be lowercase SHA-256."
            )
        return value

    @classmethod
    def _positive_int(
        cls,
        value: Any,
        *,
        label: str,
        maximum: int,
    ) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 1 <= value <= maximum
        ):
            raise GameWindowCaptureRuntimeError(
                f"{label} must be a bounded positive integer."
            )
        return value


    def _mode(self, mode_id: Any) -> dict[str, Any]:
        value = self._identifier(mode_id, label="mode_id")
        try:
            return self.foundation.find_mode(value)
        except GameCompanionRuntimeFoundationError as exc:
            raise GameWindowCaptureRuntimeError(
                "Unknown operator-selectable mode."
            ) from exc

    def identity(self) -> dict[str, Any]:
        return asdict(
            GameWindowCaptureIdentity(
                component_name=self.COMPONENT_NAME,
                component_version=self.COMPONENT_VERSION,
                protocol_version=self.PROTOCOL_VERSION,
                product_version=self.PRODUCT_VERSION,
                sprint=self.SPRINT,
                boundary=self.BOUNDARY,
                atlas_role=self.ATLAS_ROLE,
                orion_role=self.ORION_ROLE,
                capability_id=self.CAPABILITY_ID,
                reference_game_id=self.REFERENCE_GAME_ID,
            )
        )

    def capability_declaration(self) -> dict[str, Any]:
        return {
            "capability_id": self.CAPABILITY_ID,
            "version": "1.0",
            "mode": "explicit_one_shot_selected_game_window",
            "source": self.COMPONENT_NAME,
            "constraints": {
                "reference_game_id": self.REFERENCE_GAME_ID,
                "selected_window_only": True,
                "single_use_permission": True,
                "one_frame_per_request": True,
                "temporary_private_artifact": True,
                "max_width": self.MAX_WIDTH,
                "max_height": self.MAX_HEIGHT,
                "max_pixels": self.MAX_PIXELS,
                "max_encoded_bytes": self.MAX_ENCODED_BYTES,
                "full_screen_fallback": False,
                "continuous_capture": False,
                "audio_capture": False,
                "recording": False,
                "telemetry": False,
                "coaching": False,
                "game_input_control": False,
                "raw_image_transport_to_atlas": False,
                "raw_window_title_export": False,
                "artifact_path_export": False,
            },
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "reason": "game_window_capture_ready_explicit_one_shot_only",
            "runtime_ready": True,
            "safe_idle": self._state == "safe_idle",
            "current_state": self._state,
            "game_window_capture_available": True,
            "game_window_capture_active": False,
            "reference_game_id": self.REFERENCE_GAME_ID,
            "capture_host": "ORION",
            "control_authority": "ATLAS",
            "operator_detection_review_required": True,
            "operator_mode_selection_required": True,
            "separate_capture_approval_required": True,
            "scoped_single_use_permission_required": True,
            "temporary_artifact_cleanup_required": True,
            "real_capture_requires_explicit_windows_adapter": True,
            "state_persistence_active": False,
            "next_sprint": 284,
            "next_boundary": "game_audio_capture",
            **{field: False for field in self.CLOSED_RUNTIME_FIELDS},
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "identity": self.identity(),
            "status": self.status(),
            "capability": self.capability_declaration(),
            "flow": [
                "safe_idle",
                "game_detected_pending_review",
                "mode_selected_pending_start",
                "capture_preview_pending_approval",
                "capture_permission_granted",
                "one_shot_capture_requested",
                "capture_artifact_review_pending",
                "safe_idle",
            ],
            "schemas": {
                "preview_fields": sorted(self.PREVIEW_FIELDS),
                "permission_fields": sorted(self.PERMISSION_FIELDS),
                "request_fields": sorted(self.REQUEST_FIELDS),
                "artifact_fields": sorted(self.ARTIFACT_FIELDS),
                "receipt_fields": sorted(self.RECEIPT_FIELDS),
                "cleanup_fields": sorted(self.CLEANUP_FIELDS),
            },
            "limits": {
                "max_preview_ttl_seconds": self.MAX_PREVIEW_TTL_SECONDS,
                "max_request_age_seconds": self.MAX_REQUEST_AGE_SECONDS,
                "max_width": self.MAX_WIDTH,
                "max_height": self.MAX_HEIGHT,
                "max_pixels": self.MAX_PIXELS,
                "max_encoded_bytes": self.MAX_ENCODED_BYTES,
                "frame_limit": 1,
            },
            "host_split": {
                "ATLAS": [
                    "validate the Sprint 282 reviewed game binding",
                    "create the visible capture preview",
                    "grant one exact single-use permission",
                    "authorize one capture request",
                    "validate the redacted artifact receipt",
                    "require temporary artifact cleanup evidence",
                ],
                "ORION": [
                    "revalidate exact process and selected-window binding",
                    "capture one visible game-window frame",
                    "write one bounded temporary PNG",
                    "return metadata and digest without raw bytes or path",
                    "delete the temporary artifact after explicit cleanup",
                ],
            },
            "failure_states": [
                "target_window_missing",
                "target_window_changed",
                "target_process_changed",
                "permission_missing_or_expired",
                "capture_timeout",
                "capture_backend_unavailable",
                "artifact_too_large",
                "artifact_integrity_failed",
                "artifact_cleanup_failed",
                "emergency_stopped",
                "failed_safe",
            ],
            "hard_guards": {
                "automatic_capture": False,
                "continuous_capture": False,
                "full_screen_fallback": False,
                "arbitrary_window_capture": False,
                "capture_on_atlas": False,
                "raw_image_transport": False,
                "raw_window_title_export": False,
                "artifact_path_export": False,
                "audio_capture": False,
                "recording": False,
                "telemetry": False,
                "coaching": False,
                "game_input_control": False,
            },
            "next_boundary": {
                "sprint": 284,
                "boundary": "game_audio_capture",
                "activation_allowed_in_sprint_283": False,
            },
        }

    def _validate_detection_review(
        self,
        review: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(review, Mapping):
            raise GameWindowCaptureRuntimeError(
                "Detection review must be an object."
            )
        if (
            review.get("status") != "game_detected_pending_review"
            or review.get("current_state") != "game_detected_pending_review"
            or review.get("prompt_created") is not True
            or review.get("capture_started") is not False
            or review.get("recording_started") is not False
            or review.get("telemetry_started") is not False
            or review.get("coaching_started") is not False
            or review.get("game_input_control_started") is not False
        ):
            raise GameWindowCaptureRuntimeError(
                "Detection review is not an eligible safe-idle prompt."
            )
        game = review.get("detected_game")
        if not isinstance(game, Mapping):
            raise GameWindowCaptureRuntimeError(
                "Detection review lacks a game binding."
            )
        if game.get("game_id") != self.REFERENCE_GAME_ID:
            raise GameWindowCaptureRuntimeError(
                "Only the active reference game may be captured."
            )
        executable = game.get("executable_basename")
        if (
            not isinstance(executable, str)
            or self.EXECUTABLE_RE.fullmatch(executable) is None
            or executable.casefold() != "osu!.exe"
        ):
            raise GameWindowCaptureRuntimeError(
                "Detection executable binding is invalid."
            )
        process_id = self._positive_int(
            game.get("process_id_ephemeral"),
            label="process_id_ephemeral",
            maximum=self.MAX_PROCESS_ID,
        )
        if game.get("visible_top_level_window") is not True:
            raise GameWindowCaptureRuntimeError(
                "Capture requires a visible top-level game window."
            )
        title_digest = self._sha(
            game.get("window_title_sha256"),
            label="window_title_sha256",
            nullable=True,
        )
        return {
            "game_id": self.REFERENCE_GAME_ID,
            "executable_basename": executable,
            "process_id": process_id,
            "window_title_sha256": title_digest,
        }

    def _target_binding(
        self,
        *,
        agent_id: str,
        device_id: str,
        game_id: str,
        process_id: int,
        executable_basename: str,
        window_title_sha256: str | None,
    ) -> str:
        return self._digest(
            {
                "agent_id": agent_id,
                "device_id": device_id,
                "game_id": game_id,
                "process_id": process_id,
                "executable_basename": executable_basename.casefold(),
                "window_title_sha256": window_title_sha256,
                "selected_window_only": True,
            }
        )

    def build_capture_preview(
        self,
        *,
        detection_review: Mapping[str, Any],
        mode_id: str,
        agent_id: str,
        device_id: str,
        request_id: str,
        ttl_seconds: int = 30,
        max_width: int = 1920,
        max_height: int = 1080,
        max_encoded_bytes: int = 4 * 1024 * 1024,
    ) -> dict[str, Any]:
        target = self._validate_detection_review(detection_review)
        mode = self._mode(mode_id)
        if mode["operator_selectable"] is not True:
            raise GameWindowCaptureRuntimeError(
                "Mode is not operator-selectable."
            )
        agent = self._identifier(agent_id, label="agent_id")
        device = self._identifier(device_id, label="device_id")
        request = self._request_id(request_id, label="request_id")
        ttl = self._positive_int(
            ttl_seconds,
            label="ttl_seconds",
            maximum=self.MAX_PREVIEW_TTL_SECONDS,
        )
        width = self._positive_int(
            max_width,
            label="max_width",
            maximum=self.MAX_WIDTH,
        )
        height = self._positive_int(
            max_height,
            label="max_height",
            maximum=self.MAX_HEIGHT,
        )
        encoded = self._positive_int(
            max_encoded_bytes,
            label="max_encoded_bytes",
            maximum=self.MAX_ENCODED_BYTES,
        )
        pixels = width * height
        if pixels > self.MAX_PIXELS:
            raise GameWindowCaptureRuntimeError(
                "Requested capture dimensions exceed the pixel limit."
            )
        created = self._now()
        expires = created + timedelta(seconds=ttl)
        binding = self._target_binding(
            agent_id=agent,
            device_id=device,
            **target,
        )
        preview: dict[str, Any] = {
            "schema_version": 1,
            "preview_type": "game_window_capture_preview",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "action_type": self.ACTION_TYPE,
            "request_id": request,
            "agent_id": agent,
            "device_id": device,
            "game_id": target["game_id"],
            "mode_id": mode["mode_id"],
            "process_id": target["process_id"],
            "executable_basename": target["executable_basename"],
            "window_title_sha256": target["window_title_sha256"],
            "target_binding_digest": binding,
            "max_width": width,
            "max_height": height,
            "max_pixels": pixels,
            "max_encoded_bytes": encoded,
            "frame_limit": 1,
            "output_format": "PNG",
            "temporary_artifact": True,
            "full_screen_fallback_allowed": False,
            "continuous_capture_allowed": False,
            "audio_capture_allowed": False,
            "recording_allowed": False,
            "telemetry_allowed": False,
            "coaching_allowed": False,
            "game_input_control_allowed": False,
            "created_at_utc": self._format_utc(created),
            "expires_at_utc": self._format_utc(expires),
        }
        preview["preview_digest"] = self._signed_digest(
            preview,
            "preview_digest",
        )
        self._state = "capture_preview_pending_approval"
        return preview

    def validate_capture_preview(
        self,
        preview: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(preview, Mapping) or set(preview) != self.PREVIEW_FIELDS:
            raise GameWindowCaptureRuntimeError(
                "Capture preview fields are not exact."
            )
        if (
            preview["schema_version"] != 1
            or preview["preview_type"] != "game_window_capture_preview"
            or preview["protocol_version"] != self.PROTOCOL_VERSION
            or preview["capability_id"] != self.CAPABILITY_ID
            or preview["action_type"] != self.ACTION_TYPE
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture preview identity mismatch."
            )
        self._request_id(preview["request_id"], label="request_id")
        self._identifier(preview["agent_id"], label="agent_id")
        self._identifier(preview["device_id"], label="device_id")
        if preview["game_id"] != self.REFERENCE_GAME_ID:
            raise GameWindowCaptureRuntimeError(
                "Capture preview game is not active."
            )
        self._mode(preview["mode_id"])
        self._positive_int(
            preview["process_id"],
            label="process_id",
            maximum=self.MAX_PROCESS_ID,
        )
        executable = preview["executable_basename"]
        if (
            not isinstance(executable, str)
            or executable.casefold() != "osu!.exe"
            or self.EXECUTABLE_RE.fullmatch(executable) is None
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture preview executable is invalid."
            )
        self._sha(
            preview["window_title_sha256"],
            label="window_title_sha256",
            nullable=True,
        )
        self._sha(
            preview["target_binding_digest"],
            label="target_binding_digest",
        )
        width = self._positive_int(
            preview["max_width"],
            label="max_width",
            maximum=self.MAX_WIDTH,
        )
        height = self._positive_int(
            preview["max_height"],
            label="max_height",
            maximum=self.MAX_HEIGHT,
        )
        pixels = self._positive_int(
            preview["max_pixels"],
            label="max_pixels",
            maximum=self.MAX_PIXELS,
        )
        if pixels != width * height:
            raise GameWindowCaptureRuntimeError(
                "Capture preview pixel limit is inconsistent."
            )
        self._positive_int(
            preview["max_encoded_bytes"],
            label="max_encoded_bytes",
            maximum=self.MAX_ENCODED_BYTES,
        )
        if preview["frame_limit"] != 1 or preview["output_format"] != "PNG":
            raise GameWindowCaptureRuntimeError(
                "Capture preview must request one PNG frame."
            )
        required_true = ("temporary_artifact",)
        required_false = (
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
        )
        for field in required_true:
            if preview[field] is not True:
                raise GameWindowCaptureRuntimeError(
                    f"{field} must be true."
                )
        for field in required_false:
            if preview[field] is not False:
                raise GameWindowCaptureRuntimeError(
                    f"{field} must remain false."
                )
        created = self._parse_utc(
            preview["created_at_utc"],
            label="created_at_utc",
        )
        expires = self._parse_utc(
            preview["expires_at_utc"],
            label="expires_at_utc",
        )
        ttl = (expires - created).total_seconds()
        if not 0 < ttl <= self.MAX_PREVIEW_TTL_SECONDS:
            raise GameWindowCaptureRuntimeError(
                "Capture preview expiry is invalid."
            )
        now = self._now()
        if now > expires:
            raise GameWindowCaptureRuntimeError(
                "Capture preview has expired."
            )
        if created - now > timedelta(seconds=self.MAX_CLOCK_SKEW_SECONDS):
            raise GameWindowCaptureRuntimeError(
                "Capture preview is too far in the future."
            )
        expected_binding = self._target_binding(
            agent_id=preview["agent_id"],
            device_id=preview["device_id"],
            game_id=preview["game_id"],
            process_id=preview["process_id"],
            executable_basename=preview["executable_basename"],
            window_title_sha256=preview["window_title_sha256"],
        )
        if preview["target_binding_digest"] != expected_binding:
            raise GameWindowCaptureRuntimeError(
                "Capture preview target binding mismatch."
            )
        digest = self._sha(
            preview["preview_digest"],
            label="preview_digest",
        )
        if digest != self._signed_digest(preview, "preview_digest"):
            raise GameWindowCaptureRuntimeError(
                "Capture preview digest mismatch."
            )
        return dict(preview)

    def grant_capture_permission(
        self,
        preview: Mapping[str, Any],
        *,
        confirmation: str,
        permission_id: str | None = None,
    ) -> dict[str, Any]:
        validated = self.validate_capture_preview(preview)
        if confirmation != self.APPROVAL_CONFIRMATION:
            raise GameWindowCaptureRuntimeError(
                "Exact one-shot capture approval is required."
            )
        if validated["request_id"] in self._authorized_requests:
            raise GameWindowCaptureRuntimeError(
                "Capture request was already authorized."
            )
        permission = self._request_id(
            permission_id or self._id_provider("capture-permission-"),
            label="permission_id",
        )
        if permission in self._permissions:
            raise GameWindowCaptureRuntimeError(
                "Capture permission ID already exists."
            )
        issued = self._now()
        preview_expiry = self._parse_utc(
            validated["expires_at_utc"],
            label="expires_at_utc",
        )
        expires = min(
            preview_expiry,
            issued + timedelta(seconds=self.MAX_PREVIEW_TTL_SECONDS),
        )
        record: dict[str, Any] = {
            "schema_version": 1,
            "permission_type": "single_use_game_window_capture",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "action_type": self.ACTION_TYPE,
            "permission_id": permission,
            "preview_digest": validated["preview_digest"],
            "target_binding_digest": validated["target_binding_digest"],
            "agent_id": validated["agent_id"],
            "device_id": validated["device_id"],
            "game_id": validated["game_id"],
            "mode_id": validated["mode_id"],
            "process_id": validated["process_id"],
            "single_use": True,
            "frame_limit": 1,
            "issued_at_utc": self._format_utc(issued),
            "expires_at_utc": self._format_utc(expires),
        }
        record["permission_digest"] = self._signed_digest(
            record,
            "permission_digest",
        )
        self._permissions[permission] = {
            "record": deepcopy(record),
            "preview": deepcopy(validated),
            "consumed": False,
        }
        self._state = "capture_permission_granted"
        return record

    def validate_capture_permission(
        self,
        permission: Mapping[str, Any],
    ) -> dict[str, Any]:
        if (
            not isinstance(permission, Mapping)
            or set(permission) != self.PERMISSION_FIELDS
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture permission fields are not exact."
            )
        if (
            permission["schema_version"] != 1
            or permission["permission_type"]
            != "single_use_game_window_capture"
            or permission["protocol_version"] != self.PROTOCOL_VERSION
            or permission["capability_id"] != self.CAPABILITY_ID
            or permission["action_type"] != self.ACTION_TYPE
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture permission identity mismatch."
            )
        permission_id = self._request_id(
            permission["permission_id"],
            label="permission_id",
        )
        for field in (
            "preview_digest",
            "target_binding_digest",
            "permission_digest",
        ):
            self._sha(permission[field], label=field)
        self._identifier(permission["agent_id"], label="agent_id")
        self._identifier(permission["device_id"], label="device_id")
        if permission["game_id"] != self.REFERENCE_GAME_ID:
            raise GameWindowCaptureRuntimeError(
                "Capture permission game mismatch."
            )
        self._mode(permission["mode_id"])
        self._positive_int(
            permission["process_id"],
            label="process_id",
            maximum=self.MAX_PROCESS_ID,
        )
        if (
            permission["single_use"] is not True
            or permission["frame_limit"] != 1
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture permission must be single-use for one frame."
            )
        issued = self._parse_utc(
            permission["issued_at_utc"],
            label="issued_at_utc",
        )
        expires = self._parse_utc(
            permission["expires_at_utc"],
            label="expires_at_utc",
        )
        if expires <= issued or (
            expires - issued
        ).total_seconds() > self.MAX_PREVIEW_TTL_SECONDS:
            raise GameWindowCaptureRuntimeError(
                "Capture permission expiry is invalid."
            )
        if self._now() > expires:
            raise GameWindowCaptureRuntimeError(
                "Capture permission has expired."
            )
        if permission["permission_digest"] != self._signed_digest(
            permission,
            "permission_digest",
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture permission digest mismatch."
            )
        stored = self._permissions.get(permission_id)
        if stored is None:
            raise GameWindowCaptureRuntimeError(
                "Capture permission is unknown."
            )
        if stored["record"] != dict(permission):
            raise GameWindowCaptureRuntimeError(
                "Capture permission does not match the issued record."
            )
        return dict(permission)

    def build_capture_request(
        self,
        preview: Mapping[str, Any],
        permission: Mapping[str, Any],
        *,
        sequence: int,
        requested_at_utc: str | None = None,
    ) -> dict[str, Any]:
        validated_preview = self.validate_capture_preview(preview)
        validated_permission = self.validate_capture_permission(permission)
        if (
            validated_permission["preview_digest"]
            != validated_preview["preview_digest"]
            or validated_permission["target_binding_digest"]
            != validated_preview["target_binding_digest"]
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture permission is not bound to the preview."
            )
        sequence_value = self._positive_int(
            sequence,
            label="sequence",
            maximum=self.MAX_SEQUENCE,
        )
        requested = (
            self._parse_utc(requested_at_utc, label="requested_at_utc")
            if requested_at_utc is not None
            else self._now()
        )
        request: dict[str, Any] = {
            "schema_version": 1,
            "request_type": "one_shot_game_window_capture",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "action_type": self.ACTION_TYPE,
            "request_id": validated_preview["request_id"],
            "permission_id": validated_permission["permission_id"],
            "permission_digest": validated_permission["permission_digest"],
            "preview_digest": validated_preview["preview_digest"],
            "target_binding_digest": validated_preview[
                "target_binding_digest"
            ],
            "agent_id": validated_preview["agent_id"],
            "device_id": validated_preview["device_id"],
            "game_id": validated_preview["game_id"],
            "mode_id": validated_preview["mode_id"],
            "process_id": validated_preview["process_id"],
            "executable_basename": validated_preview[
                "executable_basename"
            ],
            "window_title_sha256": validated_preview[
                "window_title_sha256"
            ],
            "sequence": sequence_value,
            "requested_at_utc": self._format_utc(requested),
            "max_width": validated_preview["max_width"],
            "max_height": validated_preview["max_height"],
            "max_pixels": validated_preview["max_pixels"],
            "max_encoded_bytes": validated_preview[
                "max_encoded_bytes"
            ],
            "frame_limit": 1,
            "output_format": "PNG",
            "temporary_artifact": True,
            "full_screen_fallback_allowed": False,
            "continuous_capture_allowed": False,
            "audio_capture_allowed": False,
            "recording_allowed": False,
            "telemetry_allowed": False,
            "coaching_allowed": False,
            "game_input_control_allowed": False,
        }
        request["request_digest"] = self._signed_digest(
            request,
            "request_digest",
        )
        return request

    def validate_capture_request(
        self,
        request: Mapping[str, Any],
        *,
        require_issued_permission: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(request, Mapping) or set(request) != self.REQUEST_FIELDS:
            raise GameWindowCaptureRuntimeError(
                "Capture request fields are not exact."
            )
        if (
            request["schema_version"] != 1
            or request["request_type"] != "one_shot_game_window_capture"
            or request["protocol_version"] != self.PROTOCOL_VERSION
            or request["capability_id"] != self.CAPABILITY_ID
            or request["action_type"] != self.ACTION_TYPE
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture request identity mismatch."
            )
        self._request_id(request["request_id"], label="request_id")
        permission_id = self._request_id(
            request["permission_id"],
            label="permission_id",
        )
        for field in (
            "permission_digest",
            "preview_digest",
            "target_binding_digest",
            "request_digest",
        ):
            self._sha(request[field], label=field)
        self._identifier(request["agent_id"], label="agent_id")
        self._identifier(request["device_id"], label="device_id")
        if request["game_id"] != self.REFERENCE_GAME_ID:
            raise GameWindowCaptureRuntimeError(
                "Capture request game mismatch."
            )
        self._mode(request["mode_id"])
        self._positive_int(
            request["process_id"],
            label="process_id",
            maximum=self.MAX_PROCESS_ID,
        )
        executable = request["executable_basename"]
        if (
            not isinstance(executable, str)
            or executable.casefold() != "osu!.exe"
            or self.EXECUTABLE_RE.fullmatch(executable) is None
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture request executable mismatch."
            )
        self._sha(
            request["window_title_sha256"],
            label="window_title_sha256",
            nullable=True,
        )
        self._positive_int(
            request["sequence"],
            label="sequence",
            maximum=self.MAX_SEQUENCE,
        )
        requested = self._parse_utc(
            request["requested_at_utc"],
            label="requested_at_utc",
        )
        age = (self._now() - requested).total_seconds()
        if age > self.MAX_REQUEST_AGE_SECONDS:
            raise GameWindowCaptureRuntimeError(
                "Capture request is stale."
            )
        if age < -self.MAX_CLOCK_SKEW_SECONDS:
            raise GameWindowCaptureRuntimeError(
                "Capture request is too far in the future."
            )
        width = self._positive_int(
            request["max_width"],
            label="max_width",
            maximum=self.MAX_WIDTH,
        )
        height = self._positive_int(
            request["max_height"],
            label="max_height",
            maximum=self.MAX_HEIGHT,
        )
        pixels = self._positive_int(
            request["max_pixels"],
            label="max_pixels",
            maximum=self.MAX_PIXELS,
        )
        if pixels != width * height:
            raise GameWindowCaptureRuntimeError(
                "Capture request pixel limit mismatch."
            )
        self._positive_int(
            request["max_encoded_bytes"],
            label="max_encoded_bytes",
            maximum=self.MAX_ENCODED_BYTES,
        )
        if request["frame_limit"] != 1 or request["output_format"] != "PNG":
            raise GameWindowCaptureRuntimeError(
                "Capture request must be one PNG frame."
            )
        if request["temporary_artifact"] is not True:
            raise GameWindowCaptureRuntimeError(
                "Capture artifact must be temporary."
            )
        for field in (
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
        ):
            if request[field] is not False:
                raise GameWindowCaptureRuntimeError(
                    f"{field} must remain false."
                )
        binding = self._target_binding(
            agent_id=request["agent_id"],
            device_id=request["device_id"],
            game_id=request["game_id"],
            process_id=request["process_id"],
            executable_basename=request["executable_basename"],
            window_title_sha256=request["window_title_sha256"],
        )
        if request["target_binding_digest"] != binding:
            raise GameWindowCaptureRuntimeError(
                "Capture request target binding mismatch."
            )
        if request["request_digest"] != self._signed_digest(
            request,
            "request_digest",
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture request digest mismatch."
            )
        if require_issued_permission:
            stored = self._permissions.get(permission_id)
            if stored is None:
                raise GameWindowCaptureRuntimeError(
                    "Capture request permission is unknown."
                )
            permission = stored["record"]
            if (
                request["permission_digest"]
                != permission["permission_digest"]
                or request["preview_digest"] != permission["preview_digest"]
                or request["target_binding_digest"]
                != permission["target_binding_digest"]
                or request["agent_id"] != permission["agent_id"]
                or request["device_id"] != permission["device_id"]
                or request["game_id"] != permission["game_id"]
                or request["mode_id"] != permission["mode_id"]
                or request["process_id"] != permission["process_id"]
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture request permission binding mismatch."
                )
            if stored["consumed"] is True:
                raise GameWindowCaptureRuntimeError(
                    "Capture permission was already consumed."
                )
            if self._now() > self._parse_utc(
                permission["expires_at_utc"],
                label="expires_at_utc",
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture request permission has expired."
                )
        return dict(request)

    def authorize_capture_request(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated = self.validate_capture_request(request)
        permission_id = validated["permission_id"]
        if validated["request_id"] in self._authorized_requests:
            raise GameWindowCaptureRuntimeError(
                "Capture request replay rejected."
            )
        self._permissions[permission_id]["consumed"] = True
        self._authorized_requests[validated["request_id"]] = deepcopy(
            validated
        )
        self._state = "one_shot_capture_requested"
        return {
            "status": "capture_request_authorized",
            "current_state": self._state,
            "request_id": validated["request_id"],
            "request_digest": validated["request_digest"],
            "permission_id": permission_id,
            "permission_consumed": True,
            "frame_limit": 1,
            "selected_window_only": True,
            "capture_host": "ORION",
            "capture_started_on_atlas": False,
            "raw_image_transport_allowed": False,
            "recording_started": False,
            "audio_capture_started": False,
            "telemetry_started": False,
            "coaching_started": False,
            "game_input_control_started": False,
        }

    @classmethod
    def parse_png_dimensions(cls, data: bytes) -> tuple[int, int]:
        if not isinstance(data, bytes) or len(data) < 24:
            raise GameWindowCaptureRuntimeError(
                "PNG artifact is too short."
            )
        if not data.startswith(cls.PNG_SIGNATURE):
            raise GameWindowCaptureRuntimeError(
                "Artifact is not PNG."
            )
        if data[12:16] != b"IHDR":
            raise GameWindowCaptureRuntimeError(
                "PNG IHDR chunk is missing."
            )
        width, height = struct.unpack(">II", data[16:24])
        if width < 1 or height < 1:
            raise GameWindowCaptureRuntimeError(
                "PNG dimensions are invalid."
            )
        return width, height

    @classmethod
    def minimal_png(cls, width: int = 2, height: int = 2) -> bytes:
        if width < 1 or height < 1:
            raise GameWindowCaptureRuntimeError(
                "Fixture dimensions must be positive."
            )

        def chunk(kind: bytes, payload: bytes) -> bytes:
            body = kind + payload
            return (
                struct.pack(">I", len(payload))
                + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
            )

        row = b"\x00" + (b"\x00\x00\x00\xff" * width)
        raw = row * height
        return (
            cls.PNG_SIGNATURE
            + chunk(
                b"IHDR",
                struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0),
            )
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b"")
        )

    def build_capture_receipt(
        self,
        request: Mapping[str, Any],
        *,
        captured_at_utc: str,
        artifact_id: str | None,
        artifact_sha256: str | None,
        size_bytes: int | None,
        width: int | None,
        height: int | None,
        capture_succeeded: bool,
        failure_code: str | None = None,
    ) -> dict[str, Any]:
        validated = self.validate_capture_request(
            request,
            require_issued_permission=False,
        )
        if validated["request_id"] not in self._authorized_requests:
            raise GameWindowCaptureRuntimeError(
                "Capture receipt has no authorized request."
            )
        captured = self._parse_utc(
            captured_at_utc,
            label="captured_at_utc",
        )
        if captured - self._now() > timedelta(
            seconds=self.MAX_CLOCK_SKEW_SECONDS
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture receipt is too far in the future."
            )
        artifact: dict[str, Any] | None = None
        code: str | None = None
        if capture_succeeded:
            artifact_name = self._request_id(
                artifact_id,
                label="artifact_id",
            )
            digest = self._sha(
                artifact_sha256,
                label="artifact_sha256",
            )
            size = self._positive_int(
                size_bytes,
                label="size_bytes",
                maximum=validated["max_encoded_bytes"],
            )
            width_value = self._positive_int(
                width,
                label="width",
                maximum=validated["max_width"],
            )
            height_value = self._positive_int(
                height,
                label="height",
                maximum=validated["max_height"],
            )
            pixel_count = width_value * height_value
            if pixel_count > validated["max_pixels"]:
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact exceeds the pixel limit."
                )
            if failure_code is not None:
                raise GameWindowCaptureRuntimeError(
                    "Successful capture cannot include a failure code."
                )
            artifact = {
                "artifact_id": artifact_name,
                "mime_type": "image/png",
                "sha256": digest,
                "size_bytes": size,
                "width": width_value,
                "height": height_value,
                "pixel_count": pixel_count,
                "storage_scope": "orion_temporary_private",
                "temporary": True,
                "raw_bytes_included": False,
                "local_path_included": False,
            }
        else:
            if any(
                value is not None
                for value in (
                    artifact_id,
                    artifact_sha256,
                    size_bytes,
                    width,
                    height,
                )
            ):
                raise GameWindowCaptureRuntimeError(
                    "Failed capture cannot include an artifact."
                )
            if (
                not isinstance(failure_code, str)
                or not 1 <= len(failure_code) <= self.MAX_ERROR_CODE_LENGTH
                or self.IDENTIFIER_RE.fullmatch(failure_code) is None
            ):
                raise GameWindowCaptureRuntimeError(
                    "Failed capture requires a bounded failure code."
                )
            code = failure_code
        receipt: dict[str, Any] = {
            "schema_version": 1,
            "receipt_type": "game_window_capture_receipt",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "action_type": self.ACTION_TYPE,
            "request_id": validated["request_id"],
            "request_digest": validated["request_digest"],
            "permission_id": validated["permission_id"],
            "target_binding_digest": validated[
                "target_binding_digest"
            ],
            "agent_id": validated["agent_id"],
            "device_id": validated["device_id"],
            "game_id": validated["game_id"],
            "process_id": validated["process_id"],
            "captured_at_utc": self._format_utc(captured),
            "frame_count": 1 if capture_succeeded else 0,
            "capture_succeeded": bool(capture_succeeded),
            "failure_code": code,
            "artifact": artifact,
            "temporary_artifact": bool(capture_succeeded),
            "cleanup_required": bool(capture_succeeded),
            "screen_fallback_used": False,
            "raw_window_title_included": False,
            "audio_capture_started": False,
            "recording_started": False,
            "telemetry_started": False,
            "coaching_started": False,
            "game_input_control_started": False,
        }
        receipt["receipt_digest"] = self._signed_digest(
            receipt,
            "receipt_digest",
        )
        return receipt

    def validate_capture_receipt(
        self,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(receipt, Mapping) or set(receipt) != self.RECEIPT_FIELDS:
            raise GameWindowCaptureRuntimeError(
                "Capture receipt fields are not exact."
            )
        if (
            receipt["schema_version"] != 1
            or receipt["receipt_type"] != "game_window_capture_receipt"
            or receipt["protocol_version"] != self.PROTOCOL_VERSION
            or receipt["capability_id"] != self.CAPABILITY_ID
            or receipt["action_type"] != self.ACTION_TYPE
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture receipt identity mismatch."
            )
        request_id = self._request_id(
            receipt["request_id"],
            label="request_id",
        )
        request = self._authorized_requests.get(request_id)
        if request is None:
            raise GameWindowCaptureRuntimeError(
                "Capture receipt request is unknown."
            )
        for field in (
            "request_digest",
            "target_binding_digest",
            "receipt_digest",
        ):
            self._sha(receipt[field], label=field)
        self._request_id(receipt["permission_id"], label="permission_id")
        self._identifier(receipt["agent_id"], label="agent_id")
        self._identifier(receipt["device_id"], label="device_id")
        if receipt["game_id"] != self.REFERENCE_GAME_ID:
            raise GameWindowCaptureRuntimeError(
                "Capture receipt game mismatch."
            )
        self._positive_int(
            receipt["process_id"],
            label="process_id",
            maximum=self.MAX_PROCESS_ID,
        )
        self._parse_utc(
            receipt["captured_at_utc"],
            label="captured_at_utc",
        )
        for field in (
            "screen_fallback_used",
            "raw_window_title_included",
            "audio_capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "game_input_control_started",
        ):
            if receipt[field] is not False:
                raise GameWindowCaptureRuntimeError(
                    f"{field} must remain false."
                )
        if (
            receipt["request_digest"] != request["request_digest"]
            or receipt["permission_id"] != request["permission_id"]
            or receipt["target_binding_digest"]
            != request["target_binding_digest"]
            or receipt["agent_id"] != request["agent_id"]
            or receipt["device_id"] != request["device_id"]
            or receipt["game_id"] != request["game_id"]
            or receipt["process_id"] != request["process_id"]
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture receipt request binding mismatch."
            )
        if receipt["capture_succeeded"] is True:
            if (
                receipt["frame_count"] != 1
                or receipt["failure_code"] is not None
                or receipt["temporary_artifact"] is not True
                or receipt["cleanup_required"] is not True
            ):
                raise GameWindowCaptureRuntimeError(
                    "Successful capture receipt lifecycle is invalid."
                )
            artifact = receipt["artifact"]
            if (
                not isinstance(artifact, Mapping)
                or set(artifact) != self.ARTIFACT_FIELDS
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact fields are not exact."
                )
            self._request_id(
                artifact["artifact_id"],
                label="artifact_id",
            )
            if artifact["mime_type"] != "image/png":
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact MIME type must be image/png."
                )
            self._sha(artifact["sha256"], label="artifact.sha256")
            size = self._positive_int(
                artifact["size_bytes"],
                label="artifact.size_bytes",
                maximum=request["max_encoded_bytes"],
            )
            width = self._positive_int(
                artifact["width"],
                label="artifact.width",
                maximum=request["max_width"],
            )
            height = self._positive_int(
                artifact["height"],
                label="artifact.height",
                maximum=request["max_height"],
            )
            if artifact["pixel_count"] != width * height:
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact pixel count mismatch."
                )
            if artifact["pixel_count"] > request["max_pixels"]:
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact pixel count exceeds the limit."
                )
            if (
                artifact["storage_scope"] != "orion_temporary_private"
                or artifact["temporary"] is not True
                or artifact["raw_bytes_included"] is not False
                or artifact["local_path_included"] is not False
                or size < len(self.PNG_SIGNATURE)
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact privacy contract is invalid."
                )
        else:
            if (
                receipt["frame_count"] != 0
                or receipt["artifact"] is not None
                or receipt["temporary_artifact"] is not False
                or receipt["cleanup_required"] is not False
                or not isinstance(receipt["failure_code"], str)
            ):
                raise GameWindowCaptureRuntimeError(
                    "Failed capture receipt shape is invalid."
                )
        if receipt["receipt_digest"] != self._signed_digest(
            receipt,
            "receipt_digest",
        ):
            raise GameWindowCaptureRuntimeError(
                "Capture receipt digest mismatch."
            )
        return dict(receipt)

    def review_capture_receipt(
        self,
        receipt: Mapping[str, Any],
    ) -> dict[str, Any]:
        validated = self.validate_capture_receipt(receipt)
        request_id = validated["request_id"]
        if request_id in self._reviewed_receipts:
            raise GameWindowCaptureRuntimeError(
                "Capture receipt replay rejected."
            )
        self._reviewed_receipts[request_id] = deepcopy(validated)
        if validated["capture_succeeded"] is not True:
            self._state = "failed_safe"
            return {
                "status": "capture_failed_safe",
                "current_state": self._state,
                "request_id": request_id,
                "failure_code": validated["failure_code"],
                "artifact_review_pending": False,
                "safe_idle": False,
                "manual_recovery_required": True,
                "recording_started": False,
                "audio_capture_started": False,
                "telemetry_started": False,
                "coaching_started": False,
                "game_input_control_started": False,
            }
        self._state = "capture_artifact_review_pending"
        artifact = validated["artifact"]
        return {
            "status": "capture_artifact_review_pending",
            "current_state": self._state,
            "request_id": request_id,
            "artifact": deepcopy(artifact),
            "artifact_review_pending": True,
            "raw_image_available_on_atlas": False,
            "local_path_available_on_atlas": False,
            "cleanup_required": True,
            "safe_idle": False,
            "recording_started": False,
            "audio_capture_started": False,
            "telemetry_started": False,
            "coaching_started": False,
            "game_input_control_started": False,
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
        request = self._request_id(request_id, label="request_id")
        reviewed = self._reviewed_receipts.get(request)
        if reviewed is None or reviewed["capture_succeeded"] is not True:
            raise GameWindowCaptureRuntimeError(
                "Cleanup has no reviewed successful capture."
            )
        artifact = reviewed["artifact"]
        if (
            artifact_id != artifact["artifact_id"]
            or artifact_sha256 != artifact["sha256"]
        ):
            raise GameWindowCaptureRuntimeError(
                "Cleanup artifact binding mismatch."
            )
        cleanup_time = (
            self._parse_utc(cleanup_at_utc, label="cleanup_at_utc")
            if cleanup_at_utc is not None
            else self._now()
        )
        receipt: dict[str, Any] = {
            "schema_version": 1,
            "cleanup_type": "temporary_game_capture_cleanup",
            "protocol_version": self.PROTOCOL_VERSION,
            "request_id": request,
            "artifact_id": artifact_id,
            "artifact_sha256": artifact_sha256,
            "deleted": bool(deleted),
            "path_exported": False,
            "cleanup_at_utc": self._format_utc(cleanup_time),
        }
        receipt["cleanup_digest"] = self._signed_digest(
            receipt,
            "cleanup_digest",
        )
        return receipt

    def review_cleanup_receipt(
        self,
        cleanup: Mapping[str, Any],
        *,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != self.CLEANUP_CONFIRMATION:
            raise GameWindowCaptureRuntimeError(
                "Exact temporary-capture cleanup confirmation is required."
            )
        if not isinstance(cleanup, Mapping) or set(cleanup) != self.CLEANUP_FIELDS:
            raise GameWindowCaptureRuntimeError(
                "Cleanup receipt fields are not exact."
            )
        if (
            cleanup["schema_version"] != 1
            or cleanup["cleanup_type"]
            != "temporary_game_capture_cleanup"
            or cleanup["protocol_version"] != self.PROTOCOL_VERSION
            or cleanup["path_exported"] is not False
            or cleanup["deleted"] is not True
        ):
            raise GameWindowCaptureRuntimeError(
                "Cleanup receipt did not prove safe deletion."
            )
        request_id = self._request_id(
            cleanup["request_id"],
            label="request_id",
        )
        reviewed = self._reviewed_receipts.get(request_id)
        if reviewed is None or reviewed["capture_succeeded"] is not True:
            raise GameWindowCaptureRuntimeError(
                "Cleanup receipt request is unknown."
            )
        artifact = reviewed["artifact"]
        if (
            cleanup["artifact_id"] != artifact["artifact_id"]
            or cleanup["artifact_sha256"] != artifact["sha256"]
        ):
            raise GameWindowCaptureRuntimeError(
                "Cleanup receipt artifact binding mismatch."
            )
        self._sha(cleanup["artifact_sha256"], label="artifact_sha256")
        self._parse_utc(cleanup["cleanup_at_utc"], label="cleanup_at_utc")
        if cleanup["cleanup_digest"] != self._signed_digest(
            cleanup,
            "cleanup_digest",
        ):
            raise GameWindowCaptureRuntimeError(
                "Cleanup receipt digest mismatch."
            )
        self._state = "safe_idle"
        return {
            "status": "temporary_capture_deleted_safe_idle",
            "current_state": "safe_idle",
            "request_id": request_id,
            "artifact_deleted": True,
            "artifact_path_exported": False,
            "capture_active": False,
            "recording_active": False,
            "audio_capture_active": False,
            "telemetry_active": False,
            "coaching_active": False,
            "game_input_control_active": False,
        }

    def reset_ephemeral_state(self) -> dict[str, Any]:
        self._permissions.clear()
        self._authorized_requests.clear()
        self._reviewed_receipts.clear()
        self._state = "safe_idle"
        return {
            "status": "ephemeral_capture_state_reset",
            "safe_idle": True,
            "persistent_state_deleted": False,
            "artifact_deleted": False,
            "operator_cleanup_still_required_for_existing_artifacts": True,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: list[tuple[str, bool]] = []

        def check(name: str, condition: bool) -> None:
            assertions.append((name, bool(condition)))

        fixed_now = datetime(2026, 7, 23, 14, 0, tzinfo=timezone.utc)
        counter = {"value": 0}

        def next_id(prefix: str) -> str:
            counter["value"] += 1
            return f"{prefix}{counter['value']:04d}"

        detection = AuraSupportedGameDetectionRuntimeManager(
            self.project_root,
            now_provider=lambda: fixed_now,
        )
        detection_match = {
            "game_id": "osu_offline",
            "profile_version": "1",
            "executable_basename": "osu!.exe",
            "process_id": 4242,
            "visible_top_level_window": True,
            "window_title_sha256": hashlib.sha256(
                b"osu fixture"
            ).hexdigest(),
            "process_name_exact": True,
        }
        detection_packet = detection.build_observation_packet(
            agent_id="orion-agent",
            device_id="orion-device",
            sequence=1,
            observed_at_utc=detection._format_utc(fixed_now),
            monotonic_ms=1000,
            matches=[detection_match],
        )
        detection_review = detection.review_observation(
            detection_packet,
            expected_agent_id="orion-agent",
            expected_device_id="orion-device",
        )

        manager = AuraGameWindowCaptureRuntimeManager(
            self.project_root,
            now_provider=lambda: fixed_now,
            id_provider=next_id,
        )
        identity = manager.identity()
        status = manager.status()
        inspection = manager.inspect_runtime()
        capability = manager.capability_declaration()

        check("identity_version", identity["product_version"] == "1.4.3")
        check("identity_sprint", identity["sprint"] == 283)
        check("identity_boundary", identity["boundary"] == self.BOUNDARY)
        check("identity_capability", identity["capability_id"] == self.CAPABILITY_ID)
        check("status_ready", status["status"] == "ready")
        check("status_runtime_ready", status["runtime_ready"] is True)
        check("status_safe_idle", status["safe_idle"] is True)
        check("status_capture_available", status["game_window_capture_available"] is True)
        check("status_capture_inactive", status["game_window_capture_active"] is False)
        check("status_capture_host", status["capture_host"] == "ORION")
        check("status_authority", status["control_authority"] == "ATLAS")
        check("status_detection_review", status["operator_detection_review_required"] is True)
        check("status_mode_review", status["operator_mode_selection_required"] is True)
        check("status_capture_approval", status["separate_capture_approval_required"] is True)
        check("status_permission", status["scoped_single_use_permission_required"] is True)
        check("status_cleanup", status["temporary_artifact_cleanup_required"] is True)
        check("status_next_sprint", status["next_sprint"] == 284)
        check("status_next_boundary", status["next_boundary"] == "game_audio_capture")
        for field in self.CLOSED_RUNTIME_FIELDS:
            check(f"closed_{field}", status[field] is False)

        check("capability_mode", capability["mode"] == "explicit_one_shot_selected_game_window")
        check("capability_selected_only", capability["constraints"]["selected_window_only"] is True)
        check("capability_single_use", capability["constraints"]["single_use_permission"] is True)
        check("capability_one_frame", capability["constraints"]["one_frame_per_request"] is True)
        check("capability_temp", capability["constraints"]["temporary_private_artifact"] is True)
        for field in (
            "full_screen_fallback",
            "continuous_capture",
            "audio_capture",
            "recording",
            "telemetry",
            "coaching",
            "game_input_control",
            "raw_image_transport_to_atlas",
            "raw_window_title_export",
            "artifact_path_export",
        ):
            check(f"capability_closed_{field}", capability["constraints"][field] is False)

        preview = manager.build_capture_preview(
            detection_review=detection_review,
            mode_id="observer_only",
            agent_id="orion-agent",
            device_id="orion-device",
            request_id="capture-request-0001",
        )
        check("preview_fields", set(preview) == self.PREVIEW_FIELDS)
        check("preview_game", preview["game_id"] == "osu_offline")
        check("preview_mode", preview["mode_id"] == "observer_only")
        check("preview_pid", preview["process_id"] == 4242)
        check("preview_executable", preview["executable_basename"] == "osu!.exe")
        check("preview_frame", preview["frame_limit"] == 1)
        check("preview_png", preview["output_format"] == "PNG")
        check("preview_temp", preview["temporary_artifact"] is True)
        check("preview_digest_shape", self.SHA256_RE.fullmatch(preview["preview_digest"]) is not None)
        check("preview_binding_shape", self.SHA256_RE.fullmatch(preview["target_binding_digest"]) is not None)
        for field in (
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
        ):
            check(f"preview_closed_{field}", preview[field] is False)
        validated_preview = manager.validate_capture_preview(preview)
        check("preview_roundtrip", validated_preview == preview)
        check("preview_state", manager.status()["current_state"] == "capture_preview_pending_approval")

        permission = manager.grant_capture_permission(
            preview,
            confirmation=self.APPROVAL_CONFIRMATION,
            permission_id="capture-permission-0001",
        )
        check("permission_fields", set(permission) == self.PERMISSION_FIELDS)
        check("permission_single_use", permission["single_use"] is True)
        check("permission_frame", permission["frame_limit"] == 1)
        check("permission_preview_binding", permission["preview_digest"] == preview["preview_digest"])
        check("permission_target_binding", permission["target_binding_digest"] == preview["target_binding_digest"])
        check("permission_digest_shape", self.SHA256_RE.fullmatch(permission["permission_digest"]) is not None)
        check("permission_state", manager.status()["current_state"] == "capture_permission_granted")
        check("permission_roundtrip", manager.validate_capture_permission(permission) == permission)

        request = manager.build_capture_request(
            preview,
            permission,
            sequence=1,
        )
        check("request_fields", set(request) == self.REQUEST_FIELDS)
        check("request_frame", request["frame_limit"] == 1)
        check("request_png", request["output_format"] == "PNG")
        check("request_temp", request["temporary_artifact"] is True)
        check("request_digest_shape", self.SHA256_RE.fullmatch(request["request_digest"]) is not None)
        for field in (
            "full_screen_fallback_allowed",
            "continuous_capture_allowed",
            "audio_capture_allowed",
            "recording_allowed",
            "telemetry_allowed",
            "coaching_allowed",
            "game_input_control_allowed",
        ):
            check(f"request_closed_{field}", request[field] is False)
        check("request_roundtrip", manager.validate_capture_request(request) == request)
        authorization = manager.authorize_capture_request(request)
        check("authorization_status", authorization["status"] == "capture_request_authorized")
        check("authorization_consumed", authorization["permission_consumed"] is True)
        check("authorization_frame", authorization["frame_limit"] == 1)
        check("authorization_selected", authorization["selected_window_only"] is True)
        check("authorization_atlas_no_capture", authorization["capture_started_on_atlas"] is False)
        check("authorization_no_raw_transport", authorization["raw_image_transport_allowed"] is False)

        png = self.minimal_png(4, 3)
        width, height = self.parse_png_dimensions(png)
        check("png_width", width == 4)
        check("png_height", height == 3)
        check("png_signature", png.startswith(self.PNG_SIGNATURE))
        check("png_small", len(png) < request["max_encoded_bytes"])

        receipt = manager.build_capture_receipt(
            request,
            captured_at_utc=self._format_utc(fixed_now),
            artifact_id="capture-artifact-0001",
            artifact_sha256=hashlib.sha256(png).hexdigest(),
            size_bytes=len(png),
            width=width,
            height=height,
            capture_succeeded=True,
        )
        check("receipt_fields", set(receipt) == self.RECEIPT_FIELDS)
        check("receipt_success", receipt["capture_succeeded"] is True)
        check("receipt_frame", receipt["frame_count"] == 1)
        check("receipt_cleanup", receipt["cleanup_required"] is True)
        check("receipt_temp", receipt["temporary_artifact"] is True)
        check("receipt_artifact_fields", set(receipt["artifact"]) == self.ARTIFACT_FIELDS)
        check("receipt_mime", receipt["artifact"]["mime_type"] == "image/png")
        check("receipt_storage", receipt["artifact"]["storage_scope"] == "orion_temporary_private")
        check("receipt_raw_false", receipt["artifact"]["raw_bytes_included"] is False)
        check("receipt_path_false", receipt["artifact"]["local_path_included"] is False)
        for field in (
            "screen_fallback_used",
            "raw_window_title_included",
            "audio_capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "game_input_control_started",
        ):
            check(f"receipt_closed_{field}", receipt[field] is False)
        check("receipt_roundtrip", manager.validate_capture_receipt(receipt) == receipt)
        review = manager.review_capture_receipt(receipt)
        check("review_status", review["status"] == "capture_artifact_review_pending")
        check("review_state", review["current_state"] == "capture_artifact_review_pending")
        check("review_pending", review["artifact_review_pending"] is True)
        check("review_no_raw", review["raw_image_available_on_atlas"] is False)
        check("review_no_path", review["local_path_available_on_atlas"] is False)
        check("review_cleanup", review["cleanup_required"] is True)

        cleanup = manager.build_cleanup_receipt(
            request_id=request["request_id"],
            artifact_id=receipt["artifact"]["artifact_id"],
            artifact_sha256=receipt["artifact"]["sha256"],
            deleted=True,
        )
        check("cleanup_fields", set(cleanup) == self.CLEANUP_FIELDS)
        check("cleanup_deleted", cleanup["deleted"] is True)
        check("cleanup_path_false", cleanup["path_exported"] is False)
        cleanup_review = manager.review_cleanup_receipt(
            cleanup,
            confirmation=self.CLEANUP_CONFIRMATION,
        )
        check("cleanup_status", cleanup_review["status"] == "temporary_capture_deleted_safe_idle")
        check("cleanup_safe_idle", cleanup_review["current_state"] == "safe_idle")
        check("cleanup_capture_false", cleanup_review["capture_active"] is False)
        check("cleanup_recording_false", cleanup_review["recording_active"] is False)

        def rejected(name: str, operation: Callable[[], Any]) -> None:
            try:
                operation()
            except GameWindowCaptureRuntimeError:
                check(name, True)
            else:
                check(name, False)

        bad_detection = deepcopy(detection_review)
        bad_detection["capture_started"] = True
        rejected(
            "bad_detection_rejected",
            lambda: AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).build_capture_preview(
                detection_review=bad_detection,
                mode_id="observer_only",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-bad1",
            ),
        )
        bad_game = deepcopy(detection_review)
        bad_game["detected_game"]["game_id"] = "beat_saber"
        rejected(
            "bad_game_rejected",
            lambda: AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).build_capture_preview(
                detection_review=bad_game,
                mode_id="observer_only",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-bad2",
            ),
        )
        rejected(
            "bad_mode_rejected",
            lambda: AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).build_capture_preview(
                detection_review=detection_review,
                mode_id="unknown_mode",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-bad3",
            ),
        )
        rejected(
            "too_wide_rejected",
            lambda: AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).build_capture_preview(
                detection_review=detection_review,
                mode_id="observer_only",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-bad4",
                max_width=self.MAX_WIDTH + 1,
            ),
        )
        rejected(
            "too_many_pixels_rejected",
            lambda: AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).build_capture_preview(
                detection_review=detection_review,
                mode_id="observer_only",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-bad5",
                max_width=3840,
                max_height=2160,
                max_encoded_bytes=self.MAX_ENCODED_BYTES,
            )
            if self.MAX_PIXELS < 3840 * 2160
            else (_ for _ in ()).throw(
                GameWindowCaptureRuntimeError("fixture")
            ),
        )

        negative_manager = AuraGameWindowCaptureRuntimeManager(
            self.project_root,
            now_provider=lambda: fixed_now,
            id_provider=next_id,
        )
        negative_preview = negative_manager.build_capture_preview(
            detection_review=detection_review,
            mode_id="observer_only",
            agent_id="orion-agent",
            device_id="orion-device",
            request_id="capture-request-negative",
        )
        rejected(
            "wrong_approval_rejected",
            lambda: negative_manager.grant_capture_permission(
                negative_preview,
                confirmation="yes",
            ),
        )
        tampered_preview = deepcopy(negative_preview)
        tampered_preview["max_width"] = 1280
        rejected(
            "preview_digest_tamper_rejected",
            lambda: negative_manager.validate_capture_preview(
                tampered_preview
            ),
        )
        full_screen_preview = deepcopy(negative_preview)
        full_screen_preview["full_screen_fallback_allowed"] = True
        full_screen_preview["preview_digest"] = negative_manager._signed_digest(
            full_screen_preview,
            "preview_digest",
        )
        rejected(
            "preview_full_screen_rejected",
            lambda: negative_manager.validate_capture_preview(
                full_screen_preview
            ),
        )
        continuous_preview = deepcopy(negative_preview)
        continuous_preview["continuous_capture_allowed"] = True
        continuous_preview["preview_digest"] = negative_manager._signed_digest(
            continuous_preview,
            "preview_digest",
        )
        rejected(
            "preview_continuous_rejected",
            lambda: negative_manager.validate_capture_preview(
                continuous_preview
            ),
        )
        audio_preview = deepcopy(negative_preview)
        audio_preview["audio_capture_allowed"] = True
        audio_preview["preview_digest"] = negative_manager._signed_digest(
            audio_preview,
            "preview_digest",
        )
        rejected(
            "preview_audio_rejected",
            lambda: negative_manager.validate_capture_preview(audio_preview),
        )
        permission2 = negative_manager.grant_capture_permission(
            negative_preview,
            confirmation=self.APPROVAL_CONFIRMATION,
            permission_id="capture-permission-negative",
        )
        tampered_permission = deepcopy(permission2)
        tampered_permission["process_id"] = 9999
        rejected(
            "permission_tamper_rejected",
            lambda: negative_manager.validate_capture_permission(
                tampered_permission
            ),
        )
        request2 = negative_manager.build_capture_request(
            negative_preview,
            permission2,
            sequence=1,
        )
        tampered_request = deepcopy(request2)
        tampered_request["max_height"] = 720
        rejected(
            "request_digest_tamper_rejected",
            lambda: negative_manager.validate_capture_request(
                tampered_request
            ),
        )
        full_screen_request = deepcopy(request2)
        full_screen_request["full_screen_fallback_allowed"] = True
        full_screen_request["request_digest"] = negative_manager._signed_digest(
            full_screen_request,
            "request_digest",
        )
        rejected(
            "request_full_screen_rejected",
            lambda: negative_manager.validate_capture_request(
                full_screen_request
            ),
        )
        recording_request = deepcopy(request2)
        recording_request["recording_allowed"] = True
        recording_request["request_digest"] = negative_manager._signed_digest(
            recording_request,
            "request_digest",
        )
        rejected(
            "request_recording_rejected",
            lambda: negative_manager.validate_capture_request(
                recording_request
            ),
        )
        negative_manager.authorize_capture_request(request2)
        rejected(
            "request_replay_rejected",
            lambda: negative_manager.authorize_capture_request(request2),
        )
        rejected(
            "permission_reuse_rejected",
            lambda: negative_manager.validate_capture_request(request2),
        )

        receipt2 = negative_manager.build_capture_receipt(
            request2,
            captured_at_utc=self._format_utc(fixed_now),
            artifact_id="capture-artifact-negative",
            artifact_sha256=hashlib.sha256(png).hexdigest(),
            size_bytes=len(png),
            width=4,
            height=3,
            capture_succeeded=True,
        )
        bad_receipt = deepcopy(receipt2)
        bad_receipt["screen_fallback_used"] = True
        bad_receipt["receipt_digest"] = negative_manager._signed_digest(
            bad_receipt,
            "receipt_digest",
        )
        rejected(
            "receipt_screen_fallback_rejected",
            lambda: negative_manager.validate_capture_receipt(bad_receipt),
        )
        raw_receipt = deepcopy(receipt2)
        raw_receipt["artifact"]["raw_bytes_included"] = True
        raw_receipt["receipt_digest"] = negative_manager._signed_digest(
            raw_receipt,
            "receipt_digest",
        )
        rejected(
            "receipt_raw_bytes_rejected",
            lambda: negative_manager.validate_capture_receipt(raw_receipt),
        )
        path_receipt = deepcopy(receipt2)
        path_receipt["artifact"]["local_path_included"] = True
        path_receipt["receipt_digest"] = negative_manager._signed_digest(
            path_receipt,
            "receipt_digest",
        )
        rejected(
            "receipt_path_rejected",
            lambda: negative_manager.validate_capture_receipt(path_receipt),
        )
        oversized_receipt = deepcopy(receipt2)
        oversized_receipt["artifact"]["size_bytes"] = request2["max_encoded_bytes"] + 1
        oversized_receipt["receipt_digest"] = negative_manager._signed_digest(
            oversized_receipt,
            "receipt_digest",
        )
        rejected(
            "receipt_oversized_rejected",
            lambda: negative_manager.validate_capture_receipt(
                oversized_receipt
            ),
        )
        negative_manager.review_capture_receipt(receipt2)
        rejected(
            "receipt_replay_rejected",
            lambda: negative_manager.review_capture_receipt(receipt2),
        )
        cleanup2 = negative_manager.build_cleanup_receipt(
            request_id=request2["request_id"],
            artifact_id=receipt2["artifact"]["artifact_id"],
            artifact_sha256=receipt2["artifact"]["sha256"],
            deleted=True,
        )
        rejected(
            "cleanup_confirmation_rejected",
            lambda: negative_manager.review_cleanup_receipt(
                cleanup2,
                confirmation="delete",
            ),
        )
        bad_cleanup = deepcopy(cleanup2)
        bad_cleanup["deleted"] = False
        bad_cleanup["cleanup_digest"] = negative_manager._signed_digest(
            bad_cleanup,
            "cleanup_digest",
        )
        rejected(
            "cleanup_not_deleted_rejected",
            lambda: negative_manager.review_cleanup_receipt(
                bad_cleanup,
                confirmation=self.CLEANUP_CONFIRMATION,
            ),
        )
        rejected(
            "invalid_png_rejected",
            lambda: self.parse_png_dimensions(b"not png"),
        )

        from .aura_game_window_capture_orion_adapter import (
            AuraWindowsGameWindowCaptureAdapter,
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-sprint-283-self-test-"
        ) as temp_dir:
            capture_root = Path(temp_dir)
            adapter_manager = AuraGameWindowCaptureRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
                id_provider=next_id,
            )
            adapter_preview = adapter_manager.build_capture_preview(
                detection_review=detection_review,
                mode_id="observer_only",
                agent_id="orion-agent",
                device_id="orion-device",
                request_id="capture-request-adapter",
            )
            adapter_permission = adapter_manager.grant_capture_permission(
                adapter_preview,
                confirmation=self.APPROVAL_CONFIRMATION,
                permission_id="capture-permission-adapter",
            )
            adapter_request = adapter_manager.build_capture_request(
                adapter_preview,
                adapter_permission,
                sequence=1,
            )
            adapter_manager.authorize_capture_request(adapter_request)

            def fixture_runner(
                request_value: Mapping[str, Any],
                output_path: Path,
            ) -> Mapping[str, Any]:
                data = self.minimal_png(5, 4)
                output_path.write_bytes(data)
                return {
                    "status": "captured",
                    "process_id": request_value["process_id"],
                    "executable_basename": request_value[
                        "executable_basename"
                    ],
                    "window_handle_nonzero": True,
                    "screen_fallback_used": False,
                    "width": 5,
                    "height": 4,
                }

            adapter = AuraWindowsGameWindowCaptureAdapter(
                manager=adapter_manager,
                capture_root=capture_root,
                enabled=True,
                platform_name="windows",
                runner=fixture_runner,
                now_provider=lambda: fixed_now,
            )
            adapter_result = adapter.capture_once(adapter_request)
            check("adapter_receipt_success", adapter_result["receipt"]["capture_succeeded"] is True)
            check("adapter_local_path_private", "local_artifact_path" in adapter_result)
            check("adapter_path_not_in_receipt", "local_artifact_path" not in json.dumps(adapter_result["receipt"]))
            check("adapter_one_call", adapter.capture_active is False)
            check("adapter_file_exists", Path(adapter_result["local_artifact_path"]).is_file())
            adapter_review = adapter_manager.review_capture_receipt(
                adapter_result["receipt"]
            )
            check("adapter_review_pending", adapter_review["artifact_review_pending"] is True)
            adapter_cleanup = adapter.cleanup_once(
                adapter_result["receipt"],
                local_artifact_path=Path(
                    adapter_result["local_artifact_path"]
                ),
                confirmation=self.CLEANUP_CONFIRMATION,
            )
            check("adapter_cleanup_deleted", adapter_cleanup["deleted"] is True)
            check("adapter_file_deleted", not Path(adapter_result["local_artifact_path"]).exists())
            adapter_cleanup_review = adapter_manager.review_cleanup_receipt(
                adapter_cleanup,
                confirmation=self.CLEANUP_CONFIRMATION,
            )
            check("adapter_safe_idle", adapter_cleanup_review["current_state"] == "safe_idle")
            script = adapter.build_powershell_script(adapter_request)
            check("powershell_get_process", "Get-Process -Id" in script)
            check("powershell_get_window_rect", "GetWindowRect" in script)
            check("powershell_copy_from_screen", "CopyFromScreen" in script)
            check("powershell_system_drawing", "System.Drawing" in script)
            check("powershell_exact_exe", "osu!.exe" in script)
            check("powershell_no_window_title", "MainWindowTitle" not in script)
            check("powershell_no_full_screen", "PrimaryScreen" not in script)
            check("powershell_no_recording", "ffmpeg" not in script.casefold() and "obs" not in script.casefold())

            disabled_adapter = AuraWindowsGameWindowCaptureAdapter(
                manager=adapter_manager,
                capture_root=capture_root,
                enabled=False,
                platform_name="windows",
                runner=fixture_runner,
                now_provider=lambda: fixed_now,
            )
            rejected(
                "disabled_adapter_rejected",
                lambda: disabled_adapter.capture_once(adapter_request),
            )
            non_windows_adapter = AuraWindowsGameWindowCaptureAdapter(
                manager=adapter_manager,
                capture_root=capture_root,
                enabled=True,
                platform_name="linux",
                runner=fixture_runner,
                now_provider=lambda: fixed_now,
            )
            rejected(
                "non_windows_adapter_rejected",
                lambda: non_windows_adapter.capture_once(adapter_request),
            )

        reset = manager.reset_ephemeral_state()
        check("reset_status", reset["status"] == "ephemeral_capture_state_reset")
        check("reset_safe_idle", reset["safe_idle"] is True)
        check("reset_no_persistent_delete", reset["persistent_state_deleted"] is False)
        check("reset_no_artifact_delete", reset["artifact_deleted"] is False)
        check("reset_permission_empty", not manager._permissions)
        check("reset_requests_empty", not manager._authorized_requests)
        check("reset_receipts_empty", not manager._reviewed_receipts)

        for key, value in inspection["hard_guards"].items():
            check(f"hard_guard_{key}", value is False)
        check("flow_start", inspection["flow"][0] == "safe_idle")
        check("flow_review", "capture_artifact_review_pending" in inspection["flow"])
        check("flow_end", inspection["flow"][-1] == "safe_idle")
        check("next_sprint", inspection["next_boundary"]["sprint"] == 284)
        check("next_boundary", inspection["next_boundary"]["boundary"] == "game_audio_capture")
        check("next_activation_closed", inspection["next_boundary"]["activation_allowed_in_sprint_283"] is False)
        check("catalog_preserved", len(self.foundation.game_catalog()) == 8)
        check("modes_preserved", len(self.foundation.mode_catalog()) == 4)

        failed = [name for name, passed in assertions if not passed]
        result = {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": identity,
            "runtime": manager.status(),
        }
        if failed:
            raise GameWindowCaptureRuntimeError(
                "Sprint 283 self-test failed: " + ", ".join(failed)
            )
        return result
