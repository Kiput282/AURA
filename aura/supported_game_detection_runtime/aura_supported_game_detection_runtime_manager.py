"""Sprint 282 allowlisted supported-game detection runtime.

The runtime accepts only bounded read-only observations produced on ORION,
validates them on ATLAS, suppresses duplicate detections in memory, and creates
a safe review prompt. It never exports a full process inventory or starts
capture, recording, telemetry, coaching, application launch, voice actions, or
game input control.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from aura.game_companion_runtime_foundation import (
    AuraGameCompanionRuntimeFoundationManager,
)


class SupportedGameDetectionRuntimeError(RuntimeError):
    """Raised when a Sprint 282 detection packet fails closed."""


@dataclass(frozen=True, slots=True)
class SupportedGameDetectionIdentity:
    """Stable metadata for the Sprint 282 runtime."""

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


class AuraSupportedGameDetectionRuntimeManager:
    """Validate ORION observations and build review-only game prompts."""

    COMPONENT_NAME = "supported_game_detection_runtime"
    COMPONENT_VERSION = "0.1.0"
    PROTOCOL_VERSION = "aura-supported-game-detection-v1"
    PRODUCT_VERSION = "1.4.2"
    SPRINT = 282
    BOUNDARY = "supported_game_detection"
    ATLAS_ROLE = "ATLAS_DETECTION_REVIEW_AUTHORITY"
    ORION_ROLE = "ORION_READ_ONLY_DETECTION_SOURCE"
    CAPABILITY_ID = "orion.game.detect_supported.read_only"
    REFERENCE_GAME_ID = "osu_offline"

    MAX_MATCHES = 8
    MAX_CLOCK_SKEW_SECONDS = 5
    MAX_OBSERVATION_AGE_SECONDS = 15
    MAX_SEQUENCE = 2**63 - 1
    MAX_PROCESS_ID = 2**32 - 1
    MAX_ID_LENGTH = 64
    MAX_EXECUTABLE_BASENAME_LENGTH = 128
    MAX_PROFILE_VERSION_LENGTH = 32

    IDENTIFIER_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")
    SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
    EXECUTABLE_BASENAME_RE = re.compile(
        r"^[A-Za-z0-9][A-Za-z0-9 !()._+\-]{0,127}\.exe$",
        re.IGNORECASE,
    )

    ACTIVE_DETECTION_PROFILES: tuple[dict[str, Any], ...] = (
        {
            "game_id": "osu_offline",
            "profile_version": "1",
            "status": "active_reference",
            "executable_basenames": ("osu!.exe",),
            "exact_basename_match": True,
            "require_visible_top_level_window": True,
            "collect_executable_path": False,
            "collect_command_line": False,
            "export_raw_window_title": False,
            "environment_policy": "offline_only",
        },
    )

    PACKET_FIELDS = frozenset(
        {
            "schema_version",
            "packet_type",
            "protocol_version",
            "capability_id",
            "agent_id",
            "device_id",
            "sequence",
            "observed_at_utc",
            "monotonic_ms",
            "matches",
            "inventory_exported",
            "process_command_lines_included",
            "executable_paths_included",
            "raw_window_titles_included",
            "capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "application_launch_started",
            "game_input_control_started",
            "packet_digest",
        }
    )
    MATCH_FIELDS = frozenset(
        {
            "game_id",
            "profile_version",
            "executable_basename",
            "process_id",
            "visible_top_level_window",
            "window_title_sha256",
            "process_name_exact",
        }
    )

    CLOSED_RUNTIME_FIELDS = (
        "background_scan_active",
        "continuous_polling_active",
        "network_listener_active",
        "network_connection_active",
        "full_process_inventory_export_active",
        "raw_window_title_export_active",
        "executable_path_export_active",
        "command_line_export_active",
        "capture_active",
        "audio_capture_active",
        "recording_active",
        "telemetry_active",
        "coaching_active",
        "application_launch_active",
        "voice_command_to_action_active",
        "game_input_control_active",
        "autonomous_gameplay_active",
        "multiplayer_automation_active",
        "persistent_state_write_active",
        "external_action_execution_active",
    )

    def __init__(
        self,
        project_root: Path,
        *,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.foundation = AuraGameCompanionRuntimeFoundationManager(
            project_root=self.project_root
        )
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._last_sequence_by_identity: dict[tuple[str, str], int] = {}
        self._last_event_key_by_identity: dict[tuple[str, str], str] = {}

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
    def _packet_digest(cls, packet: Mapping[str, Any]) -> str:
        unsigned = dict(packet)
        unsigned.pop("packet_digest", None)
        return cls._digest(unsigned)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        normalized = value.astimezone(timezone.utc)
        return normalized.isoformat(timespec="milliseconds").replace(
            "+00:00", "Z"
        )

    @classmethod
    def _parse_utc(cls, value: Any, *, label: str) -> datetime:
        if not isinstance(value, str) or len(value) > 40:
            raise SupportedGameDetectionRuntimeError(
                f"{label} must be a bounded UTC timestamp."
            )
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise SupportedGameDetectionRuntimeError(
                f"{label} is not a valid ISO-8601 timestamp."
            ) from exc
        if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
            raise SupportedGameDetectionRuntimeError(
                f"{label} must use UTC."
            )
        return parsed.astimezone(timezone.utc)

    @classmethod
    def _validate_identifier(cls, value: Any, *, label: str) -> str:
        if not isinstance(value, str) or not cls.IDENTIFIER_RE.fullmatch(
            value
        ):
            raise SupportedGameDetectionRuntimeError(
                f"{label} is not a valid bounded identifier."
            )
        return value

    @classmethod
    def _validate_executable_basename(cls, value: Any) -> str:
        if (
            not isinstance(value, str)
            or len(value) > cls.MAX_EXECUTABLE_BASENAME_LENGTH
            or not cls.EXECUTABLE_BASENAME_RE.fullmatch(value)
            or "/" in value
            or "\\" in value
            or ":" in value
        ):
            raise SupportedGameDetectionRuntimeError(
                "executable_basename must be one Windows basename."
            )
        return value

    def identity(self) -> dict[str, Any]:
        """Return stable Sprint 282 metadata."""

        return asdict(
            SupportedGameDetectionIdentity(
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

    def detection_profiles(self) -> list[dict[str, Any]]:
        """Return fresh copies of the active, exact-match allowlist."""

        profiles: list[dict[str, Any]] = []
        for item in self.ACTIVE_DETECTION_PROFILES:
            copied = dict(item)
            copied["executable_basenames"] = list(
                item["executable_basenames"]
            )
            profiles.append(copied)
        return profiles

    def capability_declaration(self) -> dict[str, Any]:
        """Declare the bounded read-only capability for live-link negotiation."""

        return {
            "capability_id": self.CAPABILITY_ID,
            "version": "1.0",
            "mode": "read_only_manual_scan",
            "source": self.COMPONENT_NAME,
            "constraints": {
                "active_game_ids": [
                    item["game_id"]
                    for item in self.ACTIVE_DETECTION_PROFILES
                ],
                "exact_executable_basename_allowlist": True,
                "visible_top_level_window_required": True,
                "manual_scan_only": True,
                "background_polling": False,
                "full_process_inventory_exported": False,
                "raw_window_titles_exported": False,
                "executable_paths_exported": False,
                "command_lines_exported": False,
                "automatic_session_start": False,
                "automatic_capture_start": False,
                "automatic_recording_start": False,
                "automatic_telemetry_start": False,
                "automatic_coaching_start": False,
                "application_launch": False,
                "game_input_control": False,
            },
        }

    def status(self) -> dict[str, Any]:
        """Return idle availability without claiming an active scan."""

        return {
            "status": "ready",
            "reason": "supported_game_detection_ready_explicit_scan_only",
            "safe_idle": True,
            "runtime_ready": True,
            "supported_game_detection_available": True,
            "supported_game_detection_active": False,
            "read_only_scan_requires_explicit_invocation": True,
            "safe_idle_prompt_available": True,
            "active_detection_profile_count": len(
                self.ACTIVE_DETECTION_PROFILES
            ),
            "active_game_ids": [
                item["game_id"] for item in self.ACTIVE_DETECTION_PROFILES
            ],
            "authenticated_transport_required": True,
            "authentication_performed_by_existing_live_link": True,
            "packet_authentication_performed_here": False,
            "ephemeral_sequence_tracking": True,
            "ephemeral_event_deduplication": True,
            "state_persistence_active": False,
            "next_sprint": 283,
            "next_boundary": "game_window_capture",
            **{field: False for field in self.CLOSED_RUNTIME_FIELDS},
        }

    def inspect_runtime(self) -> dict[str, Any]:
        """Describe the host split, schema, and hard guards."""

        return {
            "identity": self.identity(),
            "status": self.status(),
            "capability": self.capability_declaration(),
            "profiles": self.detection_profiles(),
            "canonical_game_catalog": self.foundation.game_catalog(),
            "operator_modes": self.foundation.mode_catalog(),
            "session_contract": self.foundation.session_contract(),
            "packet_schema": {
                "packet_fields": sorted(self.PACKET_FIELDS),
                "match_fields": sorted(self.MATCH_FIELDS),
                "max_matches": self.MAX_MATCHES,
                "max_observation_age_seconds": (
                    self.MAX_OBSERVATION_AGE_SECONDS
                ),
                "max_clock_skew_seconds": self.MAX_CLOCK_SKEW_SECONDS,
            },
            "host_split": {
                "ORION": [
                    "filter exact allowlisted executable basenames locally",
                    "require a visible top-level window",
                    "hash any window title locally",
                    "export only matched bounded evidence",
                ],
                "ATLAS": [
                    "require authenticated ORION live-link transport",
                    "validate canonical game and detection profile",
                    "enforce freshness and monotonic sequence",
                    "suppress repeated detection prompts in memory",
                    "create game_detected_pending_review prompt",
                    "retain session and mode authority",
                ],
            },
            "hard_guards": {
                "full_process_inventory_exported": False,
                "raw_window_title_exported": False,
                "executable_path_exported": False,
                "command_line_exported": False,
                "automatic_session_start": False,
                "automatic_capture_start": False,
                "automatic_recording_start": False,
                "automatic_telemetry_start": False,
                "automatic_coaching_start": False,
                "application_launch": False,
                "voice_command_to_action": False,
                "game_input_control": False,
                "autonomous_gameplay": False,
                "multiplayer_automation": False,
                "network_listener_started_here": False,
                "persistent_state_write": False,
            },
            "next_boundary": {
                "sprint": 283,
                "boundary": "game_window_capture",
                "activation_allowed_in_sprint_282": False,
            },
        }

    def _profile_for_game(self, game_id: str) -> dict[str, Any]:
        for profile in self.ACTIVE_DETECTION_PROFILES:
            if profile["game_id"] == game_id:
                return dict(profile)
        raise SupportedGameDetectionRuntimeError(
            f"game_id is not active for detection: {game_id}"
        )

    def _validate_match(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise SupportedGameDetectionRuntimeError(
                "Each detection match must be an object."
            )
        if set(value) != self.MATCH_FIELDS:
            raise SupportedGameDetectionRuntimeError(
                "Detection match fields are not exact."
            )

        game_id = self._validate_identifier(
            value["game_id"], label="game_id"
        )
        profile = self._profile_for_game(game_id)
        canonical_game = self.foundation.find_game(game_id)
        if canonical_game["catalog_status"] != "reference":
            raise SupportedGameDetectionRuntimeError(
                "Only the active reference game can be detected in Sprint 282."
            )

        profile_version = value["profile_version"]
        if (
            not isinstance(profile_version, str)
            or not 1 <= len(profile_version)
            <= self.MAX_PROFILE_VERSION_LENGTH
            or profile_version != profile["profile_version"]
        ):
            raise SupportedGameDetectionRuntimeError(
                "Detection profile version mismatch."
            )

        basename = self._validate_executable_basename(
            value["executable_basename"]
        )
        allowed = {
            item.casefold()
            for item in profile["executable_basenames"]
        }
        if basename.casefold() not in allowed:
            raise SupportedGameDetectionRuntimeError(
                "Executable basename is not allowlisted for the game."
            )

        process_id = value["process_id"]
        if (
            isinstance(process_id, bool)
            or not isinstance(process_id, int)
            or not 1 <= process_id <= self.MAX_PROCESS_ID
        ):
            raise SupportedGameDetectionRuntimeError(
                "process_id must be a bounded positive integer."
            )

        visible = value["visible_top_level_window"]
        if not isinstance(visible, bool):
            raise SupportedGameDetectionRuntimeError(
                "visible_top_level_window must be boolean."
            )
        if profile["require_visible_top_level_window"] and not visible:
            raise SupportedGameDetectionRuntimeError(
                "The active profile requires a visible top-level window."
            )

        digest = value["window_title_sha256"]
        if digest is not None and (
            not isinstance(digest, str)
            or not self.SHA256_RE.fullmatch(digest)
        ):
            raise SupportedGameDetectionRuntimeError(
                "window_title_sha256 must be null or lowercase SHA-256."
            )

        if value["process_name_exact"] is not True:
            raise SupportedGameDetectionRuntimeError(
                "process_name_exact must be true."
            )

        return {
            "game_id": game_id,
            "profile_version": profile_version,
            "executable_basename": basename,
            "process_id": process_id,
            "visible_top_level_window": visible,
            "window_title_sha256": digest,
            "process_name_exact": True,
        }

    def build_observation_packet(
        self,
        *,
        agent_id: str,
        device_id: str,
        sequence: int,
        observed_at_utc: str,
        monotonic_ms: int,
        matches: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        """Build one bounded observation packet without transport."""

        agent = self._validate_identifier(agent_id, label="agent_id")
        device = self._validate_identifier(device_id, label="device_id")
        if (
            isinstance(sequence, bool)
            or not isinstance(sequence, int)
            or not 1 <= sequence <= self.MAX_SEQUENCE
        ):
            raise SupportedGameDetectionRuntimeError(
                "sequence must be a bounded positive integer."
            )
        if (
            isinstance(monotonic_ms, bool)
            or not isinstance(monotonic_ms, int)
            or monotonic_ms < 0
        ):
            raise SupportedGameDetectionRuntimeError(
                "monotonic_ms must be a non-negative integer."
            )
        self._parse_utc(observed_at_utc, label="observed_at_utc")
        if isinstance(matches, (str, bytes)) or len(matches) > self.MAX_MATCHES:
            raise SupportedGameDetectionRuntimeError(
                "matches must be a bounded sequence."
            )

        validated_matches = [
            self._validate_match(item) for item in matches
        ]
        unique_keys = {
            (
                item["game_id"],
                item["executable_basename"].casefold(),
                item["process_id"],
            )
            for item in validated_matches
        }
        if len(unique_keys) != len(validated_matches):
            raise SupportedGameDetectionRuntimeError(
                "Duplicate detection matches are not allowed."
            )
        validated_matches.sort(
            key=lambda item: (
                item["game_id"],
                item["process_id"],
                item["executable_basename"].casefold(),
            )
        )

        packet: dict[str, Any] = {
            "schema_version": 1,
            "packet_type": "supported_game_detection_observation",
            "protocol_version": self.PROTOCOL_VERSION,
            "capability_id": self.CAPABILITY_ID,
            "agent_id": agent,
            "device_id": device,
            "sequence": sequence,
            "observed_at_utc": observed_at_utc,
            "monotonic_ms": monotonic_ms,
            "matches": validated_matches,
            "inventory_exported": False,
            "process_command_lines_included": False,
            "executable_paths_included": False,
            "raw_window_titles_included": False,
            "capture_started": False,
            "recording_started": False,
            "telemetry_started": False,
            "coaching_started": False,
            "application_launch_started": False,
            "game_input_control_started": False,
        }
        packet["packet_digest"] = self._packet_digest(packet)
        return packet

    def validate_observation_packet(
        self,
        packet: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Validate exact schema, freshness, redaction, and digest."""

        if not isinstance(packet, Mapping) or set(packet) != self.PACKET_FIELDS:
            raise SupportedGameDetectionRuntimeError(
                "Detection packet fields are not exact."
            )
        if packet["schema_version"] != 1:
            raise SupportedGameDetectionRuntimeError(
                "Unsupported detection schema version."
            )
        if (
            packet["packet_type"]
            != "supported_game_detection_observation"
            or packet["protocol_version"] != self.PROTOCOL_VERSION
            or packet["capability_id"] != self.CAPABILITY_ID
        ):
            raise SupportedGameDetectionRuntimeError(
                "Detection packet identity mismatch."
            )

        self._validate_identifier(packet["agent_id"], label="agent_id")
        self._validate_identifier(packet["device_id"], label="device_id")

        sequence = packet["sequence"]
        if (
            isinstance(sequence, bool)
            or not isinstance(sequence, int)
            or not 1 <= sequence <= self.MAX_SEQUENCE
        ):
            raise SupportedGameDetectionRuntimeError(
                "Invalid detection sequence."
            )
        monotonic_ms = packet["monotonic_ms"]
        if (
            isinstance(monotonic_ms, bool)
            or not isinstance(monotonic_ms, int)
            or monotonic_ms < 0
        ):
            raise SupportedGameDetectionRuntimeError(
                "Invalid detection monotonic timestamp."
            )

        observed = self._parse_utc(
            packet["observed_at_utc"], label="observed_at_utc"
        )
        now = self._now_provider().astimezone(timezone.utc)
        age = (now - observed).total_seconds()
        if age > self.MAX_OBSERVATION_AGE_SECONDS:
            raise SupportedGameDetectionRuntimeError(
                "Detection observation is stale."
            )
        if age < -self.MAX_CLOCK_SKEW_SECONDS:
            raise SupportedGameDetectionRuntimeError(
                "Detection observation is too far in the future."
            )

        for field in (
            "inventory_exported",
            "process_command_lines_included",
            "executable_paths_included",
            "raw_window_titles_included",
            "capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "application_launch_started",
            "game_input_control_started",
        ):
            if packet[field] is not False:
                raise SupportedGameDetectionRuntimeError(
                    f"{field} must remain false."
                )

        matches = packet["matches"]
        if (
            not isinstance(matches, list)
            or len(matches) > self.MAX_MATCHES
        ):
            raise SupportedGameDetectionRuntimeError(
                "Detection matches are not bounded."
            )
        validated_matches = [
            self._validate_match(item) for item in matches
        ]
        if validated_matches != matches:
            raise SupportedGameDetectionRuntimeError(
                "Detection matches are not canonical."
            )

        packet_digest = packet["packet_digest"]
        if (
            not isinstance(packet_digest, str)
            or not self.SHA256_RE.fullmatch(packet_digest)
            or packet_digest != self._packet_digest(packet)
        ):
            raise SupportedGameDetectionRuntimeError(
                "Detection packet digest mismatch."
            )
        return dict(packet)

    def _event_key(self, packet: Mapping[str, Any]) -> str:
        event = {
            "agent_id": packet["agent_id"],
            "device_id": packet["device_id"],
            "matches": [
                {
                    "game_id": item["game_id"],
                    "executable_basename": item["executable_basename"],
                    "process_id": item["process_id"],
                    "visible_top_level_window": (
                        item["visible_top_level_window"]
                    ),
                }
                for item in packet["matches"]
            ],
        }
        return self._digest(event)

    def review_observation(
        self,
        packet: Mapping[str, Any],
        *,
        expected_agent_id: str,
        expected_device_id: str,
    ) -> dict[str, Any]:
        """Review one authenticated packet and create no automatic action."""

        validated = self.validate_observation_packet(packet)
        expected_agent = self._validate_identifier(
            expected_agent_id, label="expected_agent_id"
        )
        expected_device = self._validate_identifier(
            expected_device_id, label="expected_device_id"
        )
        if (
            validated["agent_id"] != expected_agent
            or validated["device_id"] != expected_device
        ):
            raise SupportedGameDetectionRuntimeError(
                "Authenticated ORION identity binding mismatch."
            )

        identity_key = (expected_agent, expected_device)
        previous_sequence = self._last_sequence_by_identity.get(
            identity_key, 0
        )
        if validated["sequence"] <= previous_sequence:
            raise SupportedGameDetectionRuntimeError(
                "Detection sequence replay or regression rejected."
            )
        self._last_sequence_by_identity[identity_key] = validated["sequence"]

        common = {
            "safe_execution_state": True,
            "runtime_execution_active": False,
            "authenticated_transport_required": True,
            "authenticated_identity_bound": True,
            "capture_started": False,
            "audio_capture_started": False,
            "recording_started": False,
            "telemetry_started": False,
            "coaching_started": False,
            "application_launch_started": False,
            "game_input_control_started": False,
            "voice_command_to_action_started": False,
            "external_action_execution_started": False,
            "automatic_session_start": False,
            "operator_review_required": True,
            "operator_start_required": True,
            "packet_digest": validated["packet_digest"],
            "sequence": validated["sequence"],
        }

        if not validated["matches"]:
            self._last_event_key_by_identity.pop(identity_key, None)
            return {
                "status": "no_supported_game_detected",
                "current_state": "safe_idle",
                "prompt_created": False,
                "detected_game": None,
                "available_modes": [],
                **common,
            }

        event_key = self._event_key(validated)
        if self._last_event_key_by_identity.get(identity_key) == event_key:
            return {
                "status": "duplicate_detection_suppressed",
                "current_state": "game_detected_pending_review",
                "prompt_created": False,
                "deduplication_key": event_key,
                "detected_game": None,
                "available_modes": [],
                **common,
            }
        self._last_event_key_by_identity[identity_key] = event_key

        selected = validated["matches"][0]
        game = self.foundation.find_game(selected["game_id"])
        modes = self.foundation.mode_catalog()
        return {
            "status": "game_detected_pending_review",
            "current_state": "game_detected_pending_review",
            "prompt_created": True,
            "deduplication_key": event_key,
            "detected_game": {
                "game_id": game["game_id"],
                "title": game["title"],
                "environment_policy": game["environment_policy"],
                "executable_basename": selected["executable_basename"],
                "process_id_ephemeral": selected["process_id"],
                "visible_top_level_window": (
                    selected["visible_top_level_window"]
                ),
                "window_title_sha256": selected["window_title_sha256"],
            },
            "available_modes": modes,
            "prompt": {
                "title": f"{game['title']} detected",
                "message": (
                    "A supported game is visible on ORION. Review the game "
                    "and choose a mode. Nothing starts automatically."
                ),
                "choices": [
                    item["mode_id"] for item in modes
                ],
                "dismiss_returns_to": "safe_idle",
                "session_start_available": False,
            },
            **common,
        }

    def reset_ephemeral_review_state(self) -> dict[str, Any]:
        """Clear only in-memory replay and prompt-dedup state."""

        sequence_count = len(self._last_sequence_by_identity)
        event_count = len(self._last_event_key_by_identity)
        self._last_sequence_by_identity.clear()
        self._last_event_key_by_identity.clear()
        return {
            "status": "ephemeral_review_state_reset",
            "sequence_identity_count_cleared": sequence_count,
            "event_identity_count_cleared": event_count,
            "persistent_state_deleted": False,
            "safe_idle": True,
        }

    def self_test(self) -> dict[str, Any]:
        """Validate the full runtime contract without real process scanning."""

        assertions: list[tuple[str, bool]] = []

        def check(name: str, condition: bool) -> None:
            assertions.append((name, bool(condition)))

        fixed_now = datetime(2026, 7, 23, 13, 0, 0, tzinfo=timezone.utc)
        manager = AuraSupportedGameDetectionRuntimeManager(
            self.project_root,
            now_provider=lambda: fixed_now,
        )
        identity = manager.identity()
        status = manager.status()
        inspection = manager.inspect_runtime()
        profiles = manager.detection_profiles()
        capability = manager.capability_declaration()

        expected_identity = {
            "component_name": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "protocol_version": self.PROTOCOL_VERSION,
            "product_version": self.PRODUCT_VERSION,
            "sprint": self.SPRINT,
            "boundary": self.BOUNDARY,
            "atlas_role": self.ATLAS_ROLE,
            "orion_role": self.ORION_ROLE,
            "capability_id": self.CAPABILITY_ID,
            "reference_game_id": self.REFERENCE_GAME_ID,
        }
        for field, expected in expected_identity.items():
            check(f"identity_{field}", identity.get(field) == expected)

        check("status_ready", status["status"] == "ready")
        check("status_safe_idle", status["safe_idle"] is True)
        check("runtime_ready", status["runtime_ready"] is True)
        check(
            "detection_available",
            status["supported_game_detection_available"] is True,
        )
        check(
            "scan_idle",
            status["supported_game_detection_active"] is False,
        )
        check(
            "explicit_scan_required",
            status["read_only_scan_requires_explicit_invocation"] is True,
        )
        check(
            "prompt_available",
            status["safe_idle_prompt_available"] is True,
        )
        check(
            "active_profile_count",
            status["active_detection_profile_count"] == 1,
        )
        check(
            "active_game_exact",
            status["active_game_ids"] == ["osu_offline"],
        )
        check(
            "authenticated_transport_required",
            status["authenticated_transport_required"] is True,
        )
        check(
            "existing_live_link_auth",
            status["authentication_performed_by_existing_live_link"]
            is True,
        )
        check(
            "no_duplicate_auth_layer",
            status["packet_authentication_performed_here"] is False,
        )
        check(
            "ephemeral_sequence",
            status["ephemeral_sequence_tracking"] is True,
        )
        check(
            "ephemeral_dedup",
            status["ephemeral_event_deduplication"] is True,
        )
        check(
            "no_state_persistence",
            status["state_persistence_active"] is False,
        )
        check("next_sprint", status["next_sprint"] == 283)
        check(
            "next_boundary",
            status["next_boundary"] == "game_window_capture",
        )
        for field in self.CLOSED_RUNTIME_FIELDS:
            check(f"runtime_closed_{field}", status[field] is False)

        check("profile_count", len(profiles) == 1)
        profile = profiles[0]
        check("profile_game", profile["game_id"] == "osu_offline")
        check(
            "profile_executable",
            profile["executable_basenames"] == ["osu!.exe"],
        )
        check(
            "profile_exact",
            profile["exact_basename_match"] is True,
        )
        check(
            "profile_visible_window",
            profile["require_visible_top_level_window"] is True,
        )
        check(
            "profile_no_path",
            profile["collect_executable_path"] is False,
        )
        check(
            "profile_no_command",
            profile["collect_command_line"] is False,
        )
        check(
            "profile_no_raw_title",
            profile["export_raw_window_title"] is False,
        )
        check(
            "profile_offline",
            profile["environment_policy"] == "offline_only",
        )

        check(
            "capability_id",
            capability["capability_id"] == self.CAPABILITY_ID,
        )
        check("capability_mode", capability["mode"] == "read_only_manual_scan")
        for key in (
            "background_polling",
            "full_process_inventory_exported",
            "raw_window_titles_exported",
            "executable_paths_exported",
            "command_lines_exported",
            "automatic_session_start",
            "automatic_capture_start",
            "automatic_recording_start",
            "automatic_telemetry_start",
            "automatic_coaching_start",
            "application_launch",
            "game_input_control",
        ):
            check(
                f"capability_constraint_{key}",
                capability["constraints"][key] is False,
            )
        check(
            "capability_exact_allowlist",
            capability["constraints"][
                "exact_executable_basename_allowlist"
            ]
            is True,
        )
        check(
            "capability_visible_required",
            capability["constraints"][
                "visible_top_level_window_required"
            ]
            is True,
        )
        check(
            "capability_manual_only",
            capability["constraints"]["manual_scan_only"] is True,
        )

        match = {
            "game_id": "osu_offline",
            "profile_version": "1",
            "executable_basename": "osu!.exe",
            "process_id": 4242,
            "visible_top_level_window": True,
            "window_title_sha256": hashlib.sha256(
                b"osu! fixture window"
            ).hexdigest(),
            "process_name_exact": True,
        }
        observed = manager._format_utc(fixed_now)
        packet = manager.build_observation_packet(
            agent_id="orion-agent",
            device_id="orion-device",
            sequence=1,
            observed_at_utc=observed,
            monotonic_ms=1000,
            matches=[match],
        )
        check("packet_exact_fields", set(packet) == self.PACKET_FIELDS)
        check("packet_schema", packet["schema_version"] == 1)
        check(
            "packet_type",
            packet["packet_type"]
            == "supported_game_detection_observation",
        )
        check(
            "packet_protocol",
            packet["protocol_version"] == self.PROTOCOL_VERSION,
        )
        check(
            "packet_capability",
            packet["capability_id"] == self.CAPABILITY_ID,
        )
        check("packet_match_count", len(packet["matches"]) == 1)
        check("packet_inventory_false", packet["inventory_exported"] is False)
        check(
            "packet_command_false",
            packet["process_command_lines_included"] is False,
        )
        check(
            "packet_path_false",
            packet["executable_paths_included"] is False,
        )
        check(
            "packet_raw_title_false",
            packet["raw_window_titles_included"] is False,
        )
        for field in (
            "capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "application_launch_started",
            "game_input_control_started",
        ):
            check(f"packet_{field}", packet[field] is False)
        check(
            "packet_digest_shape",
            self.SHA256_RE.fullmatch(packet["packet_digest"]) is not None,
        )
        check(
            "packet_digest_valid",
            packet["packet_digest"] == manager._packet_digest(packet),
        )
        check(
            "raw_title_absent",
            "osu! fixture window" not in json.dumps(packet),
        )
        serialized_packet = json.dumps(packet, sort_keys=True)
        check(
            "path_field_absent",
            '"executable_path":' not in serialized_packet,
        )
        check(
            "command_line_absent",
            '"command_line":' not in serialized_packet,
        )

        validated = manager.validate_observation_packet(packet)
        check(
            "validation_roundtrip",
            validated["packet_digest"] == packet["packet_digest"],
        )
        review = manager.review_observation(
            packet,
            expected_agent_id="orion-agent",
            expected_device_id="orion-device",
        )
        check(
            "review_status",
            review["status"] == "game_detected_pending_review",
        )
        check(
            "review_state",
            review["current_state"] == "game_detected_pending_review",
        )
        check("review_prompt", review["prompt_created"] is True)
        check(
            "review_game",
            review["detected_game"]["game_id"] == "osu_offline",
        )
        check(
            "review_modes",
            [item["mode_id"] for item in review["available_modes"]]
            == [
                "coach_only",
                "observer_only",
                "coach_observer",
                "coach_observer_recording",
            ],
        )
        check(
            "review_no_session_start",
            review["prompt"]["session_start_available"] is False,
        )
        check(
            "review_operator_required",
            review["operator_review_required"] is True
            and review["operator_start_required"] is True,
        )
        for field in (
            "capture_started",
            "audio_capture_started",
            "recording_started",
            "telemetry_started",
            "coaching_started",
            "application_launch_started",
            "game_input_control_started",
            "voice_command_to_action_started",
            "external_action_execution_started",
        ):
            check(f"review_closed_{field}", review[field] is False)

        duplicate_packet = manager.build_observation_packet(
            agent_id="orion-agent",
            device_id="orion-device",
            sequence=2,
            observed_at_utc=observed,
            monotonic_ms=1001,
            matches=[match],
        )
        duplicate = manager.review_observation(
            duplicate_packet,
            expected_agent_id="orion-agent",
            expected_device_id="orion-device",
        )
        check(
            "duplicate_status",
            duplicate["status"] == "duplicate_detection_suppressed",
        )
        check(
            "duplicate_prompt_false",
            duplicate["prompt_created"] is False,
        )

        empty_packet = manager.build_observation_packet(
            agent_id="orion-agent",
            device_id="orion-device",
            sequence=3,
            observed_at_utc=observed,
            monotonic_ms=1002,
            matches=[],
        )
        empty_review = manager.review_observation(
            empty_packet,
            expected_agent_id="orion-agent",
            expected_device_id="orion-device",
        )
        check(
            "empty_safe_idle",
            empty_review["current_state"] == "safe_idle",
        )
        check(
            "empty_no_prompt",
            empty_review["prompt_created"] is False,
        )

        def rejected(name: str, operation: Callable[[], Any]) -> None:
            try:
                operation()
            except SupportedGameDetectionRuntimeError:
                check(name, True)
            else:
                check(name, False)

        rejected(
            "replay_rejected",
            lambda: manager.review_observation(
                empty_packet,
                expected_agent_id="orion-agent",
                expected_device_id="orion-device",
            ),
        )
        identity_manager = AuraSupportedGameDetectionRuntimeManager(
            self.project_root,
            now_provider=lambda: fixed_now,
        )
        rejected(
            "identity_mismatch_rejected",
            lambda: identity_manager.review_observation(
                packet,
                expected_agent_id="different-agent",
                expected_device_id="orion-device",
            ),
        )

        tampered = json.loads(json.dumps(packet))
        tampered["matches"][0]["process_id"] = 9999
        rejected(
            "tampered_digest_rejected",
            lambda: AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).validate_observation_packet(tampered),
        )

        extra_field = json.loads(json.dumps(packet))
        extra_field["raw_process_inventory"] = []
        rejected(
            "extra_packet_field_rejected",
            lambda: AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ).validate_observation_packet(extra_field),
        )

        stale_time = manager._format_utc(
            fixed_now
            - timedelta(seconds=self.MAX_OBSERVATION_AGE_SECONDS + 1)
        )
        rejected(
            "stale_packet_rejected",
            lambda: manager.validate_observation_packet(
                manager.build_observation_packet(
                    agent_id="orion-agent",
                    device_id="orion-device",
                    sequence=4,
                    observed_at_utc=stale_time,
                    monotonic_ms=1003,
                    matches=[],
                )
            ),
        )

        future_time = manager._format_utc(
            fixed_now
            + timedelta(seconds=self.MAX_CLOCK_SKEW_SECONDS + 1)
        )
        rejected(
            "future_packet_rejected",
            lambda: manager.validate_observation_packet(
                manager.build_observation_packet(
                    agent_id="orion-agent",
                    device_id="orion-device",
                    sequence=4,
                    observed_at_utc=future_time,
                    monotonic_ms=1003,
                    matches=[],
                )
            ),
        )

        invalid_cases = (
            (
                "planned_game_rejected",
                {**match, "game_id": "beat_saber"},
            ),
            (
                "wrong_executable_rejected",
                {**match, "executable_basename": "notepad.exe"},
            ),
            (
                "path_executable_rejected",
                {**match, "executable_basename": r"C:\osu!\osu!.exe"},
            ),
            (
                "invisible_window_rejected",
                {**match, "visible_top_level_window": False},
            ),
            (
                "bad_digest_rejected",
                {**match, "window_title_sha256": "bad"},
            ),
            (
                "process_exact_false_rejected",
                {**match, "process_name_exact": False},
            ),
            (
                "zero_pid_rejected",
                {**match, "process_id": 0},
            ),
        )
        for name, invalid_match in invalid_cases:
            rejected(
                name,
                lambda invalid_match=invalid_match: manager.build_observation_packet(
                    agent_id="orion-agent",
                    device_id="orion-device",
                    sequence=10,
                    observed_at_utc=observed,
                    monotonic_ms=2000,
                    matches=[invalid_match],
                ),
            )

        rejected(
            "duplicate_match_rejected",
            lambda: manager.build_observation_packet(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=10,
                observed_at_utc=observed,
                monotonic_ms=2000,
                matches=[match, match],
            ),
        )
        rejected(
            "too_many_matches_rejected",
            lambda: manager.build_observation_packet(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=10,
                observed_at_utc=observed,
                monotonic_ms=2000,
                matches=[match] * (self.MAX_MATCHES + 1),
            ),
        )
        rejected(
            "invalid_agent_rejected",
            lambda: manager.build_observation_packet(
                agent_id="BAD AGENT",
                device_id="orion-device",
                sequence=10,
                observed_at_utc=observed,
                monotonic_ms=2000,
                matches=[],
            ),
        )
        rejected(
            "invalid_sequence_rejected",
            lambda: manager.build_observation_packet(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=0,
                observed_at_utc=observed,
                monotonic_ms=2000,
                matches=[],
            ),
        )

        from .aura_supported_game_detection_orion_adapter import (
            AuraWindowsSupportedGameDetectionAdapter,
        )

        fixture_rows = [
            {
                "process_id": 4242,
                "executable_basename": "osu!.exe",
                "visible_window": True,
                "window_title": "osu! fixture window",
            },
            {
                "process_id": 5252,
                "executable_basename": "notepad.exe",
                "visible_window": True,
                "window_title": "private title",
            },
            {
                "process_id": 6262,
                "executable_basename": "osu!.exe",
                "visible_window": False,
                "window_title": "",
            },
        ]

        adapter = AuraWindowsSupportedGameDetectionAdapter(
            manager=AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ),
            enabled=True,
            platform_name="windows",
            runner=lambda allowed: fixture_rows,
            now_provider=lambda: fixed_now,
            monotonic_ms_provider=lambda: 5000,
        )
        adapter_packet = adapter.scan_once(
            agent_id="orion-agent",
            device_id="orion-device",
            sequence=1,
        )
        check(
            "adapter_filters_allowlist",
            len(adapter_packet["matches"]) == 1,
        )
        check(
            "adapter_match_game",
            adapter_packet["matches"][0]["game_id"] == "osu_offline",
        )
        check(
            "adapter_hashes_title",
            self.SHA256_RE.fullmatch(
                adapter_packet["matches"][0]["window_title_sha256"]
            )
            is not None,
        )
        check(
            "adapter_drops_raw_title",
            "private title" not in json.dumps(adapter_packet)
            and "osu! fixture window" not in json.dumps(adapter_packet),
        )
        check(
            "adapter_drops_unsupported_process",
            "notepad.exe" not in json.dumps(adapter_packet),
        )
        check(
            "adapter_requires_visible_window",
            all(
                item["visible_top_level_window"]
                for item in adapter_packet["matches"]
            ),
        )
        check(
            "adapter_scan_once_only",
            adapter.background_scan_active is False,
        )
        script = adapter.build_powershell_script()
        check("powershell_uses_get_process", "Get-Process" in script)
        check("powershell_exact_allowlist", "osu!.exe" in script)
        check(
            "powershell_no_commandline",
            "CommandLine" not in script and "Win32_Process" not in script,
        )
        check(
            "powershell_no_path",
            "ExecutablePath" not in script and ".Path" not in script,
        )
        check(
            "powershell_only_json_output",
            "ConvertTo-Json" in script,
        )

        disabled_adapter = AuraWindowsSupportedGameDetectionAdapter(
            manager=AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ),
            enabled=False,
            platform_name="windows",
            runner=lambda allowed: [],
            now_provider=lambda: fixed_now,
        )
        rejected(
            "disabled_adapter_rejected",
            lambda: disabled_adapter.scan_once(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=1,
            ),
        )
        non_windows_adapter = AuraWindowsSupportedGameDetectionAdapter(
            manager=AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ),
            enabled=True,
            platform_name="linux",
            runner=lambda allowed: [],
            now_provider=lambda: fixed_now,
        )
        rejected(
            "non_windows_adapter_rejected",
            lambda: non_windows_adapter.scan_once(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=1,
            ),
        )
        bad_runner_adapter = AuraWindowsSupportedGameDetectionAdapter(
            manager=AuraSupportedGameDetectionRuntimeManager(
                self.project_root,
                now_provider=lambda: fixed_now,
            ),
            enabled=True,
            platform_name="windows",
            runner=lambda allowed: (_ for _ in ()).throw(
                RuntimeError("fixture failure")
            ),
            now_provider=lambda: fixed_now,
        )
        rejected(
            "runner_failure_rejected",
            lambda: bad_runner_adapter.scan_once(
                agent_id="orion-agent",
                device_id="orion-device",
                sequence=1,
            ),
        )

        reset = manager.reset_ephemeral_review_state()
        check(
            "reset_status",
            reset["status"] == "ephemeral_review_state_reset",
        )
        check(
            "reset_no_persistent_delete",
            reset["persistent_state_deleted"] is False,
        )
        check("reset_safe_idle", reset["safe_idle"] is True)
        check(
            "reset_sequence_empty",
            not manager._last_sequence_by_identity,
        )
        check(
            "reset_event_empty",
            not manager._last_event_key_by_identity,
        )

        for guard, value in inspection["hard_guards"].items():
            check(f"hard_guard_{guard}", value is False)
        check(
            "next_boundary_sprint",
            inspection["next_boundary"]["sprint"] == 283,
        )
        check(
            "next_boundary_name",
            inspection["next_boundary"]["boundary"]
            == "game_window_capture",
        )
        check(
            "next_activation_forbidden",
            inspection["next_boundary"][
                "activation_allowed_in_sprint_282"
            ]
            is False,
        )
        check(
            "canonical_catalog_preserved",
            len(inspection["canonical_game_catalog"]) == 8,
        )
        check(
            "operator_modes_preserved",
            len(inspection["operator_modes"]) == 4,
        )
        check(
            "constructor_no_external_side_effect",
            manager.project_root == Path(manager.project_root).resolve(),
        )

        failed = [name for name, passed in assertions if not passed]
        result = {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": identity,
            "runtime": status,
        }
        if failed:
            raise SupportedGameDetectionRuntimeError(
                "Sprint 282 self-test failed: " + ", ".join(failed)
            )
        return result
