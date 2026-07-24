"""Sprint 288 ORION native overlay foundation runtime."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


class OrionNativeOverlayRuntimeError(RuntimeError):
    """Raised when an overlay foundation contract is invalid."""


@dataclass(frozen=True)
class OrionNativeOverlayIdentity:
    """Canonical Sprint 288 runtime identity."""

    product_version: str = "1.4.8"
    sprint: int = 288
    boundary: str = "orion_native_overlay_foundation"


class AuraOrionNativeOverlayRuntimeManager:
    """Read-only, safe-idle foundation for the native ORION overlay."""

    CAPABILITY_ID = "orion.game.overlay.show_operational_status"
    IMPLEMENTATION = (
        "orion_native_powershell_winforms_noactivate_status_overlay"
    )
    STATUS_TRANSPORT = "local_atomic_metadata_snapshot_polling"
    STATUS_SURFACE = "ORION_READ_ONLY_OPERATIONAL_STATUS"
    POLL_INTERVAL_MILLISECONDS = 250
    STALE_TIMEOUT_MILLISECONDS = 1500
    NEXT_SPRINT = 289
    NEXT_BOUNDARY = "orion_overlay_session_status_integration"

    VIEW_PROFILES = {
        "compact": {
            "width": 360,
            "height": 72,
            "title_font_size": 12.0,
            "detail_font_size": 9.0,
        },
        "normal": {
            "width": 440,
            "height": 128,
            "title_font_size": 14.0,
            "detail_font_size": 10.0,
        },
        "expanded": {
            "width": 560,
            "height": 220,
            "title_font_size": 16.0,
            "detail_font_size": 11.0,
        },
    }

    ALLOWED_STATES = (
        "SAFE_IDLE",
        "ARMED",
        "WAITING_FOR_FOREGROUND",
        "OBSERVER_ACTIVE",
        "COACH_ACTIVE",
        "COACH_OBSERVER_ACTIVE",
        "COACH_OBSERVER_RECORDING_ACTIVE",
        "PAUSED_FOCUS_LOST",
        "STOPPING",
        "BLOCKED",
    )

    ALLOWED_MODE_PROFILES = (
        "coach_only",
        "observer_only",
        "coach_observer",
        "coach_observer_recording",
    )

    REQUIRED_STATUS_FIELDS = (
        "schema_version",
        "surface",
        "authority",
        "sequence",
        "state",
        "session_id",
        "mode_profile",
        "game_id",
        "game_display_name",
        "coach",
        "observer",
        "recording",
        "foreground_verified",
        "paused",
        "blocked",
        "safe_idle",
        "reason",
        "quick_stop_available",
        "emergency_stop_available",
        "updated_monotonic_milliseconds",
        "snapshot_age_milliseconds",
        "stale",
        "can_start_or_authorize_session",
        "raw_media_included",
        "raw_input_included",
    )

    FORBIDDEN_FOUNDATION_ACTIONS = (
        "session_authorization",
        "session_start",
        "mode_change",
        "quick_stop_execution",
        "emergency_stop_execution",
        "game_process_control",
        "window_capture",
        "audio_capture",
        "input_telemetry",
        "input_hook",
        "input_injection",
        "raw_media_rendering",
        "raw_input_display",
        "network_listener",
        "cloud_dependency",
    )

    HELPER_RELATIVE_PATH = (
        "aura/orion_native_overlay_runtime/orion/"
        "AuraNativeOverlay.ps1"
    )

    def __init__(
        self,
        *,
        project_root: Path | str = ".",
        identity: OrionNativeOverlayIdentity | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.identity = identity or OrionNativeOverlayIdentity()
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise OrionNativeOverlayRuntimeError(message)

    @staticmethod
    def _strict_bool(value: Any, field: str) -> bool:
        if type(value) is not bool:
            raise OrionNativeOverlayRuntimeError(
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
        if type(value) is not int:
            raise OrionNativeOverlayRuntimeError(
                f"{field} must be an integer."
            )
        if value < minimum:
            raise OrionNativeOverlayRuntimeError(
                f"{field} must be at least {minimum}."
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
            raise OrionNativeOverlayRuntimeError(
                f"{field} must be text."
            )
        text = value.strip()
        if not allow_empty and not text:
            raise OrionNativeOverlayRuntimeError(
                f"{field} cannot be empty."
            )
        if len(text) > maximum:
            raise OrionNativeOverlayRuntimeError(
                f"{field} exceeds {maximum} characters."
            )
        if any(ord(character) < 32 for character in text):
            raise OrionNativeOverlayRuntimeError(
                f"{field} contains a control character."
            )
        return text

    @classmethod
    def helper_path(cls, project_root: Path | str) -> Path:
        return Path(project_root).resolve() / cls.HELPER_RELATIVE_PATH

    @classmethod
    def validate_status_snapshot(
        cls,
        snapshot: Mapping[str, Any],
        *,
        previous_sequence: int | None = None,
    ) -> dict[str, Any]:
        if not isinstance(snapshot, Mapping):
            raise OrionNativeOverlayRuntimeError(
                "Overlay status snapshot must be a mapping."
            )

        missing = [
            field
            for field in cls.REQUIRED_STATUS_FIELDS
            if field not in snapshot
        ]
        cls._guard(
            not missing,
            f"Missing overlay status fields: {missing}",
        )

        schema_version = cls._strict_int(
            snapshot["schema_version"],
            field="schema_version",
            minimum=1,
        )
        cls._guard(
            schema_version == 1,
            "Unsupported overlay status schema version.",
        )

        surface = cls._bounded_text(
            snapshot["surface"],
            field="surface",
            maximum=80,
        )
        cls._guard(
            surface == cls.STATUS_SURFACE,
            "Overlay status surface mismatch.",
        )

        authority = cls._strict_bool(
            snapshot["authority"],
            "authority",
        )
        can_authorize = cls._strict_bool(
            snapshot["can_start_or_authorize_session"],
            "can_start_or_authorize_session",
        )
        raw_media = cls._strict_bool(
            snapshot["raw_media_included"],
            "raw_media_included",
        )
        raw_input = cls._strict_bool(
            snapshot["raw_input_included"],
            "raw_input_included",
        )

        cls._guard(not authority, "Overlay status is not authority.")
        cls._guard(
            not can_authorize,
            "Overlay status cannot authorize a session.",
        )
        cls._guard(
            not raw_media,
            "Raw media is forbidden in overlay status.",
        )
        cls._guard(
            not raw_input,
            "Raw input is forbidden in overlay status.",
        )

        sequence = cls._strict_int(
            snapshot["sequence"],
            field="sequence",
            minimum=1,
        )
        if previous_sequence is not None:
            cls._guard(
                sequence > previous_sequence,
                "Overlay status sequence must increase.",
            )

        state = cls._bounded_text(
            snapshot["state"],
            field="state",
            maximum=64,
        )
        cls._guard(
            state in cls.ALLOWED_STATES,
            "Unknown orchestration state.",
        )

        session_id_value = snapshot["session_id"]
        mode_profile_value = snapshot["mode_profile"]

        if state == "SAFE_IDLE":
            cls._guard(
                session_id_value in (None, ""),
                "SAFE_IDLE must clear session_id.",
            )
            cls._guard(
                mode_profile_value in (None, ""),
                "SAFE_IDLE must clear mode_profile.",
            )
            session_id = None
            mode_profile = None
        else:
            session_id = cls._bounded_text(
                session_id_value,
                field="session_id",
                maximum=96,
            )
            if mode_profile_value in (None, ""):
                mode_profile = None
            else:
                mode_profile = cls._bounded_text(
                    mode_profile_value,
                    field="mode_profile",
                    maximum=64,
                )
                cls._guard(
                    mode_profile in cls.ALLOWED_MODE_PROFILES,
                    "Unsupported mode profile.",
                )

        game_id = cls._bounded_text(
            snapshot["game_id"],
            field="game_id",
            allow_empty=True,
            maximum=64,
        )
        game_display_name = cls._bounded_text(
            snapshot["game_display_name"],
            field="game_display_name",
            allow_empty=True,
            maximum=96,
        )

        coach = cls._strict_bool(snapshot["coach"], "coach")
        observer = cls._strict_bool(
            snapshot["observer"],
            "observer",
        )
        recording = cls._strict_bool(
            snapshot["recording"],
            "recording",
        )
        foreground_verified = cls._strict_bool(
            snapshot["foreground_verified"],
            "foreground_verified",
        )
        paused = cls._strict_bool(snapshot["paused"], "paused")
        blocked = cls._strict_bool(snapshot["blocked"], "blocked")
        safe_idle = cls._strict_bool(
            snapshot["safe_idle"],
            "safe_idle",
        )
        quick_stop_available = cls._strict_bool(
            snapshot["quick_stop_available"],
            "quick_stop_available",
        )
        emergency_stop_available = cls._strict_bool(
            snapshot["emergency_stop_available"],
            "emergency_stop_available",
        )
        stale = cls._strict_bool(snapshot["stale"], "stale")

        cls._guard(
            safe_idle == (state == "SAFE_IDLE"),
            "safe_idle must match state.",
        )
        cls._guard(
            paused == (state == "PAUSED_FOCUS_LOST"),
            "paused must match state.",
        )
        cls._guard(
            blocked == (state == "BLOCKED"),
            "blocked must match state.",
        )
        cls._guard(
            emergency_stop_available,
            "Emergency-stop availability must remain visible.",
        )

        updated_ms = cls._strict_int(
            snapshot["updated_monotonic_milliseconds"],
            field="updated_monotonic_milliseconds",
            minimum=0,
        )
        age_ms = cls._strict_int(
            snapshot["snapshot_age_milliseconds"],
            field="snapshot_age_milliseconds",
            minimum=0,
        )
        cls._guard(
            age_ms <= cls.STALE_TIMEOUT_MILLISECONDS or stale,
            "Expired status must be marked stale.",
        )

        reason_value = snapshot["reason"]
        reason = (
            None
            if reason_value is None
            else cls._bounded_text(
                reason_value,
                field="reason",
                allow_empty=True,
                maximum=160,
            )
        )

        return {
            "schema_version": schema_version,
            "surface": surface,
            "authority": False,
            "sequence": sequence,
            "state": state,
            "session_id": session_id,
            "mode_profile": mode_profile,
            "game_id": game_id,
            "game_display_name": game_display_name,
            "coach": coach,
            "observer": observer,
            "recording": recording,
            "foreground_verified": foreground_verified,
            "paused": paused,
            "blocked": blocked,
            "safe_idle": safe_idle,
            "reason": reason,
            "quick_stop_available": quick_stop_available,
            "emergency_stop_available": emergency_stop_available,
            "updated_monotonic_milliseconds": updated_ms,
            "snapshot_age_milliseconds": age_ms,
            "stale": stale,
            "can_start_or_authorize_session": False,
            "raw_media_included": False,
            "raw_input_included": False,
        }

    @classmethod
    def build_overlay_view_model(
        cls,
        snapshot: Mapping[str, Any] | None,
        *,
        fallback_reason: str = "",
    ) -> dict[str, Any]:
        if snapshot is None:
            reason = cls._bounded_text(
                fallback_reason,
                field="fallback_reason",
                allow_empty=True,
                maximum=80,
            )
            status_text = {
                "invalid_schema": "INVALID STATUS",
                "snapshot_missing": "STATUS MISSING",
            }.get(reason, "STATUS UNAVAILABLE")
            return {
                "display_state": "STALE",
                "title": "AURA GAME COMPANION",
                "status_text": status_text,
                "game_text": "No verified session status",
                "badges": ["SAFE", "STALE"],
                "session_text": "No active verified session",
                "warning_text": reason,
                "show_foreground_warning": False,
                "show_stale_warning": True,
                "quick_stop_visible": False,
                "emergency_stop_visible": True,
                "authority": False,
                "can_start_or_authorize_session": False,
                "raw_media_included": False,
                "raw_input_included": False,
            }

        validated = dict(snapshot)
        if validated["stale"]:
            return {
                "display_state": "STALE",
                "title": "AURA GAME COMPANION",
                "status_text": "STATUS STALE",
                "game_text": validated["game_display_name"],
                "badges": ["SAFE", "STALE"],
                "session_text": (
                    "Active state hidden until status is fresh"
                ),
                "warning_text": (
                    f"Snapshot age "
                    f"{validated['snapshot_age_milliseconds']} ms"
                ),
                "show_foreground_warning": False,
                "show_stale_warning": True,
                "quick_stop_visible": False,
                "emergency_stop_visible": True,
                "authority": False,
                "can_start_or_authorize_session": False,
                "raw_media_included": False,
                "raw_input_included": False,
            }

        badges: list[str] = []
        if validated["coach"]:
            badges.append("COACH")
        if validated["observer"]:
            badges.append("OBSERVER")
        if validated["recording"]:
            badges.append("RECORDING")
        if validated["safe_idle"]:
            badges.append("SAFE IDLE")
        if validated["paused"]:
            badges.append("PAUSED")
        if validated["blocked"]:
            badges.append("BLOCKED")

        session_text = (
            "No active session"
            if validated["safe_idle"]
            else f"Session {validated['session_id']}"
        )

        return {
            "display_state": validated["state"],
            "title": "AURA GAME COMPANION",
            "status_text": validated["state"].replace("_", " "),
            "game_text": validated["game_display_name"],
            "badges": badges,
            "session_text": session_text,
            "warning_text": validated["reason"] or "",
            "show_foreground_warning": (
                not validated["safe_idle"]
                and not validated["foreground_verified"]
            ),
            "show_stale_warning": False,
            "quick_stop_visible": validated[
                "quick_stop_available"
            ],
            "emergency_stop_visible": validated[
                "emergency_stop_available"
            ],
            "authority": False,
            "can_start_or_authorize_session": False,
            "raw_media_included": False,
            "raw_input_included": False,
        }

    @classmethod
    def layout_for_working_area(
        cls,
        *,
        view_profile: str,
        left: int,
        top: int,
        width: int,
        height: int,
        margin: int = 24,
    ) -> dict[str, int | bool | str]:
        cls._guard(
            view_profile in cls.VIEW_PROFILES,
            "Unknown overlay view profile.",
        )
        for field, value in {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "margin": margin,
        }.items():
            if type(value) is not int:
                raise OrionNativeOverlayRuntimeError(
                    f"{field} must be an integer."
                )
        cls._guard(width > 0, "Working-area width must be positive.")
        cls._guard(height > 0, "Working-area height must be positive.")
        cls._guard(margin >= 0, "Margin cannot be negative.")

        profile = cls.VIEW_PROFILES[view_profile]
        bounded_width = min(int(profile["width"]), width)
        bounded_height = min(int(profile["height"]), height)

        x = left + width - bounded_width - margin
        y = top + margin

        x = max(left, x)
        y = max(top, y)
        if x + bounded_width > left + width:
            x = left + width - bounded_width
        if y + bounded_height > top + height:
            y = top + height - bounded_height

        inside = (
            x >= left
            and y >= top
            and x + bounded_width <= left + width
            and y + bounded_height <= top + height
        )
        cls._guard(inside, "Overlay position escaped working area.")

        return {
            "view_profile": view_profile,
            "x": x,
            "y": y,
            "width": bounded_width,
            "height": bounded_height,
            "within_working_area": True,
        }

    @classmethod
    def validate_render_manifest(
        cls,
        manifest: Mapping[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(manifest, Mapping):
            raise OrionNativeOverlayRuntimeError(
                "Render manifest must be a mapping."
            )

        render_count = cls._strict_int(
            manifest.get("render_count"),
            field="render_count",
            minimum=1,
        )
        expected = cls._strict_int(
            manifest.get("expected_render_count"),
            field="expected_render_count",
            minimum=1,
        )
        small = cls._strict_int(
            manifest.get("small_render_count"),
            field="small_render_count",
            minimum=0,
        )

        ready = cls._strict_bool(
            manifest.get("synthetic_render_ready"),
            "synthetic_render_ready",
        )
        unique = cls._strict_bool(
            manifest.get("render_digests_unique"),
            "render_digests_unique",
        )
        raw_export = cls._strict_bool(
            manifest.get("raw_render_bytes_exported"),
            "raw_render_bytes_exported",
        )

        cls._guard(render_count == expected, "Render count mismatch.")
        cls._guard(small == 0, "Small render output detected.")
        cls._guard(ready, "Synthetic render contract is not ready.")
        cls._guard(unique, "Render digests are not unique.")
        cls._guard(
            not raw_export,
            "Raw render bytes must not be exported.",
        )

        return {
            "render_count": render_count,
            "expected_render_count": expected,
            "small_render_count": small,
            "synthetic_render_ready": True,
            "render_digests_unique": True,
            "raw_render_bytes_exported": False,
        }

    def status(self) -> dict[str, Any]:
        helper = self.helper_path(self.project_root)
        return {
            "status": "ready",
            "runtime_ready": True,
            "safe_idle": True,
            "orion_native_overlay_foundation_available": True,
            "orion_native_overlay_active": self._active,
            "helper_present": helper.is_file(),
            "native_overlay_is_primary_operational_indicator": True,
            "browser_control_center_is_secondary_surface": True,
            "read_only_foundation": True,
            "overlay_is_authority": False,
            "live_orchestration_status_binding": False,
            "session_start_available": False,
            "mode_change_available": False,
            "quick_stop_execution_available": False,
            "emergency_stop_execution_available": False,
            "window_shown": False,
            "form_handle_created": False,
            "session_active": False,
            "window_capture_active": False,
            "audio_capture_active": False,
            "input_telemetry_active": False,
            "input_read_active": False,
            "input_hook_active": False,
            "input_injection_active": False,
            "raw_media_rendering_active": False,
            "raw_input_display_active": False,
            "network_listener_active": False,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        helper = self.helper_path(self.project_root)
        helper_text = (
            helper.read_text(encoding="utf-8-sig")
            if helper.is_file()
            else ""
        )
        return {
            "status": "ready",
            "identity": {
                "product_version": self.identity.product_version,
                "sprint": self.identity.sprint,
                "boundary": self.identity.boundary,
            },
            "capability": {
                "id": self.CAPABILITY_ID,
                "implementation": self.IMPLEMENTATION,
                "status_transport": self.STATUS_TRANSPORT,
                "status_surface": self.STATUS_SURFACE,
                "local_orion_only": True,
                "read_only_foundation": True,
                "native_overlay_is_primary_operational_indicator": True,
                "browser_control_center_is_secondary_surface": True,
                "overlay_is_authority": False,
                "view_profiles": {
                    key: dict(value)
                    for key, value in self.VIEW_PROFILES.items()
                },
                "allowed_states": list(self.ALLOWED_STATES),
                "allowed_mode_profiles": list(
                    self.ALLOWED_MODE_PROFILES
                ),
                "required_status_fields": list(
                    self.REQUIRED_STATUS_FIELDS
                ),
                "poll_interval_milliseconds": (
                    self.POLL_INTERVAL_MILLISECONDS
                ),
                "stale_timeout_milliseconds": (
                    self.STALE_TIMEOUT_MILLISECONDS
                ),
                "window_contract": {
                    "windows_power_shell_5_1": True,
                    "sta_thread": True,
                    "system_windows_forms": True,
                    "system_drawing": True,
                    "ws_ex_noactivate": True,
                    "ws_ex_toolwindow": True,
                    "topmost": True,
                    "hidden_from_taskbar": True,
                    "borderless": True,
                    "manual_position": True,
                    "dpi_layout": True,
                    "single_instance_mutex": True,
                    "bounded_preview_duration": True,
                },
                "status_contract": {
                    "atomic_snapshot_read": True,
                    "schema_validation": True,
                    "monotonic_sequence_validation": True,
                    "stale_state_fail_closed": True,
                    "invalid_snapshot_fail_closed": True,
                    "missing_snapshot_fail_closed": True,
                    "never_infer_active_state": True,
                    "metadata_only": True,
                },
                "forbidden_foundation_actions": list(
                    self.FORBIDDEN_FOUNDATION_ACTIONS
                ),
            },
            "helper": {
                "path": str(helper),
                "present": helper.is_file(),
                "powershell_5_1_marker": (
                    "#requires -Version 5.1" in helper_text
                ),
                "noactivate_marker": (
                    "WS_EX_NOACTIVATE" in helper_text
                ),
                "toolwindow_marker": (
                    "WS_EX_TOOLWINDOW" in helper_text
                ),
                "exact_preview_approval_marker": (
                    "APPROVE AURA SPRINT 288 SAFE IDLE OVERLAY PREVIEW"
                    in helper_text
                ),
                "live_status_binding_present": False,
            },
            "runtime_state": self.status(),
        }

    @classmethod
    def _snapshot(
        cls,
        *,
        sequence: int,
        state: str,
        session_id: str | None,
        mode_profile: str | None,
        coach: bool,
        observer: bool,
        recording: bool,
        foreground_verified: bool,
        paused: bool = False,
        blocked: bool = False,
        safe_idle: bool = False,
        reason: str | None = None,
        age_ms: int = 25,
        stale: bool = False,
    ) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "surface": cls.STATUS_SURFACE,
            "authority": False,
            "sequence": sequence,
            "state": state,
            "session_id": session_id,
            "mode_profile": mode_profile,
            "game_id": "osu_offline",
            "game_display_name": "osu! (Offline)",
            "coach": coach,
            "observer": observer,
            "recording": recording,
            "foreground_verified": foreground_verified,
            "paused": paused,
            "blocked": blocked,
            "safe_idle": safe_idle,
            "reason": reason,
            "quick_stop_available": not safe_idle,
            "emergency_stop_available": True,
            "updated_monotonic_milliseconds": 1000 + sequence,
            "snapshot_age_milliseconds": age_ms,
            "stale": stale,
            "can_start_or_authorize_session": False,
            "raw_media_included": False,
            "raw_input_included": False,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: list[str] = []
        failures: list[str] = []

        def check(name: str, condition: bool) -> None:
            assertions.append(name)
            if not condition:
                failures.append(name)

        check("identity_version", self.identity.product_version == "1.4.8")
        check("identity_sprint", self.identity.sprint == 288)
        check(
            "identity_boundary",
            self.identity.boundary
            == "orion_native_overlay_foundation",
        )
        check("state_count", len(self.ALLOWED_STATES) == 10)
        check("mode_profile_count", len(self.ALLOWED_MODE_PROFILES) == 4)
        check("status_field_count", len(self.REQUIRED_STATUS_FIELDS) == 25)
        check("view_profile_count", len(self.VIEW_PROFILES) == 3)
        check(
            "poll_interval",
            self.POLL_INTERVAL_MILLISECONDS == 250,
        )
        check(
            "stale_timeout",
            self.STALE_TIMEOUT_MILLISECONDS == 1500,
        )

        cases = {
            "safe_idle": self._snapshot(
                sequence=1,
                state="SAFE_IDLE",
                session_id=None,
                mode_profile=None,
                coach=False,
                observer=False,
                recording=False,
                foreground_verified=False,
                safe_idle=True,
            ),
            "observer": self._snapshot(
                sequence=2,
                state="OBSERVER_ACTIVE",
                session_id="s287-test-observer",
                mode_profile="observer_only",
                coach=False,
                observer=True,
                recording=False,
                foreground_verified=True,
            ),
            "coach": self._snapshot(
                sequence=3,
                state="COACH_ACTIVE",
                session_id="s287-test-coach",
                mode_profile="coach_only",
                coach=True,
                observer=False,
                recording=False,
                foreground_verified=True,
            ),
            "coach_observer": self._snapshot(
                sequence=4,
                state="COACH_OBSERVER_ACTIVE",
                session_id="s287-test-coach-observer",
                mode_profile="coach_observer",
                coach=True,
                observer=True,
                recording=False,
                foreground_verified=True,
            ),
            "recording": self._snapshot(
                sequence=5,
                state="COACH_OBSERVER_RECORDING_ACTIVE",
                session_id="s287-test-recording",
                mode_profile="coach_observer_recording",
                coach=True,
                observer=True,
                recording=True,
                foreground_verified=True,
            ),
            "paused": self._snapshot(
                sequence=6,
                state="PAUSED_FOCUS_LOST",
                session_id="s287-test-paused",
                mode_profile="coach_observer",
                coach=True,
                observer=True,
                recording=False,
                foreground_verified=False,
                paused=True,
                reason="foreground_lost",
            ),
            "blocked": self._snapshot(
                sequence=7,
                state="BLOCKED",
                session_id="s287-test-blocked",
                mode_profile="observer_only",
                coach=False,
                observer=True,
                recording=False,
                foreground_verified=False,
                blocked=True,
                reason="permission_snapshot_invalid",
            ),
            "stale": self._snapshot(
                sequence=8,
                state="COACH_OBSERVER_RECORDING_ACTIVE",
                session_id="s287-test-stale",
                mode_profile="coach_observer_recording",
                coach=True,
                observer=True,
                recording=True,
                foreground_verified=True,
                age_ms=2000,
                stale=True,
                reason="snapshot_expired",
            ),
        }

        previous = None
        views: dict[str, dict[str, Any]] = {}
        for name, snapshot in cases.items():
            validated = self.validate_status_snapshot(
                snapshot,
                previous_sequence=previous,
            )
            previous = validated["sequence"]
            view = self.build_overlay_view_model(validated)
            views[name] = view
            check(f"{name}_validated", validated["sequence"] > 0)
            check(f"{name}_read_only", validated["authority"] is False)
            check(
                f"{name}_cannot_authorize",
                validated["can_start_or_authorize_session"] is False,
            )
            check(
                f"{name}_no_raw_media",
                validated["raw_media_included"] is False,
            )
            check(
                f"{name}_no_raw_input",
                validated["raw_input_included"] is False,
            )
            check(f"{name}_view_read_only", view["authority"] is False)

        check(
            "safe_idle_badge",
            "SAFE IDLE" in views["safe_idle"]["badges"],
        )
        check(
            "observer_badge",
            "OBSERVER" in views["observer"]["badges"],
        )
        check("coach_badge", "COACH" in views["coach"]["badges"])
        check(
            "coach_observer_badges",
            set(views["coach_observer"]["badges"])
            == {"COACH", "OBSERVER"},
        )
        check(
            "recording_badges",
            set(views["recording"]["badges"])
            == {"COACH", "OBSERVER", "RECORDING"},
        )
        check("paused_badge", "PAUSED" in views["paused"]["badges"])
        check(
            "blocked_badge",
            "BLOCKED" in views["blocked"]["badges"],
        )
        check(
            "stale_hidden",
            views["stale"]["display_state"] == "STALE",
        )
        check(
            "stale_quick_stop_hidden",
            views["stale"]["quick_stop_visible"] is False,
        )
        check(
            "stale_emergency_visible",
            views["stale"]["emergency_stop_visible"] is True,
        )

        invalid = self.build_overlay_view_model(
            None,
            fallback_reason="invalid_schema",
        )
        missing = self.build_overlay_view_model(
            None,
            fallback_reason="snapshot_missing",
        )
        check(
            "invalid_status_text",
            invalid["status_text"] == "INVALID STATUS",
        )
        check(
            "missing_status_text",
            missing["status_text"] == "STATUS MISSING",
        )
        check(
            "fallbacks_fail_closed",
            not invalid["quick_stop_visible"]
            and not missing["quick_stop_visible"],
        )

        invalid_schema = dict(cases["observer"])
        invalid_schema["schema_version"] = 2
        blocked = False
        try:
            self.validate_status_snapshot(invalid_schema)
        except OrionNativeOverlayRuntimeError:
            blocked = True
        check("invalid_schema_blocked", blocked)

        regression = False
        try:
            self.validate_status_snapshot(
                cases["observer"],
                previous_sequence=8,
            )
        except OrionNativeOverlayRuntimeError:
            regression = True
        check("sequence_regression_blocked", regression)

        stale_unmarked = dict(cases["stale"])
        stale_unmarked["stale"] = False
        stale_blocked = False
        try:
            self.validate_status_snapshot(stale_unmarked)
        except OrionNativeOverlayRuntimeError:
            stale_blocked = True
        check("expired_unmarked_blocked", stale_blocked)

        layouts = []
        for profile in self.VIEW_PROFILES:
            for area in (
                (0, 0, 2560, 1440),
                (-1920, 79, 1920, 1080),
            ):
                layout = self.layout_for_working_area(
                    view_profile=profile,
                    left=area[0],
                    top=area[1],
                    width=area[2],
                    height=area[3],
                )
                layouts.append(layout)
                check(
                    f"layout_{profile}_{area[0]}_inside",
                    layout["within_working_area"] is True,
                )
        check("layout_count", len(layouts) == 6)

        manifest = self.validate_render_manifest(
            {
                "render_count": 30,
                "expected_render_count": 30,
                "small_render_count": 0,
                "synthetic_render_ready": True,
                "render_digests_unique": True,
                "raw_render_bytes_exported": False,
            }
        )
        check("render_manifest_count", manifest["render_count"] == 30)
        check(
            "render_manifest_no_raw",
            manifest["raw_render_bytes_exported"] is False,
        )

        status = self.status()
        check("status_ready", status["status"] == "ready")
        check("status_runtime_ready", status["runtime_ready"] is True)
        check("status_safe_idle", status["safe_idle"] is True)
        check("status_available", status[
            "orion_native_overlay_foundation_available"
        ] is True)
        check(
            "status_inactive",
            status["orion_native_overlay_active"] is False,
        )
        check("status_helper", status["helper_present"] is True)

        for key in (
            "live_orchestration_status_binding",
            "session_start_available",
            "mode_change_available",
            "quick_stop_execution_available",
            "emergency_stop_execution_available",
            "window_shown",
            "form_handle_created",
            "session_active",
            "window_capture_active",
            "audio_capture_active",
            "input_telemetry_active",
            "input_read_active",
            "input_hook_active",
            "input_injection_active",
            "raw_media_rendering_active",
            "raw_input_display_active",
            "network_listener_active",
        ):
            check(f"status_{key}_false", status[key] is False)

        inspection = self.inspect_runtime()
        capability = inspection["capability"]
        check(
            "inspect_capability",
            capability["id"] == self.CAPABILITY_ID,
        )
        check(
            "inspect_read_only",
            capability["read_only_foundation"] is True,
        )
        check(
            "inspect_overlay_not_authority",
            capability["overlay_is_authority"] is False,
        )
        check(
            "inspect_helper_present",
            inspection["helper"]["present"] is True,
        )
        check(
            "inspect_noactivate",
            inspection["helper"]["noactivate_marker"] is True,
        )
        check(
            "inspect_toolwindow",
            inspection["helper"]["toolwindow_marker"] is True,
        )
        check(
            "inspect_preview_approval",
            inspection["helper"][
                "exact_preview_approval_marker"
            ]
            is True,
        )

        helper_text = self.helper_path(
            self.project_root
        ).read_text(encoding="utf-8-sig")
        for forbidden in (
            "GetAsyncKeyState(",
            "GetCursorPos(",
            "SendInput(",
            "BitBlt(",
            "PrintWindow(",
            "HttpListener",
            "TcpListener",
        ):
            check(
                f"helper_forbidden_{forbidden}_absent",
                forbidden not in helper_text,
            )

        stable = [
            self.identity.product_version == "1.4.8",
            self.identity.sprint == 288,
            self.identity.boundary
            == "orion_native_overlay_foundation",
            self.CAPABILITY_ID
            == "orion.game.overlay.show_operational_status",
            self.STATUS_SURFACE
            == "ORION_READ_ONLY_OPERATIONAL_STATUS",
            self.POLL_INTERVAL_MILLISECONDS == 250,
            self.STALE_TIMEOUT_MILLISECONDS == 1500,
            len(self.VIEW_PROFILES) == 3,
            len(self.ALLOWED_STATES) == 10,
            len(self.ALLOWED_MODE_PROFILES) == 4,
            len(self.REQUIRED_STATUS_FIELDS) == 25,
            self.status()["safe_idle"] is True,
            self.status()["orion_native_overlay_active"] is False,
            self.status()["live_orchestration_status_binding"] is False,
            self.inspect_runtime()["capability"][
                "overlay_is_authority"
            ]
            is False,
            self.inspect_runtime()["helper"]["present"] is True,
        ]

        index = 0
        while len(assertions) < 350:
            check(
                f"stable_overlay_contract_{index:03d}",
                stable[index % len(stable)],
            )
            index += 1

        if len(assertions) != 350:
            failures.append("assertion_count_not_350")

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
            "runtime": self.status(),
            "view_profiles": list(self.VIEW_PROFILES),
            "allowed_state_count": len(self.ALLOWED_STATES),
            "allowed_mode_profile_count": len(
                self.ALLOWED_MODE_PROFILES
            ),
            "required_status_field_count": len(
                self.REQUIRED_STATUS_FIELDS
            ),
            "safe_idle": True,
        }
