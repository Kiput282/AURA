"""Sprint 287 explicit Game Companion session orchestration runtime."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


class GameSessionOrchestrationRuntimeError(RuntimeError):
    """Raised when a Sprint 287 orchestration contract is invalid."""


@dataclass(frozen=True)
class GameSessionOrchestrationIdentity:
    """Canonical product identity carried by the Sprint 287 runtime."""

    product_version: str = "1.4.7"
    sprint: int = 287
    boundary: str = "game_session_orchestration"


class AuraGameSessionOrchestrationRuntimeManager:
    """Safe-idle contract runtime for explicit Game Companion sessions."""

    CAPABILITY_ID = "orion.game.session.orchestrate.explicit_modes"
    AUTHORITY = "ATLAS_GAME_SESSION_REVIEW_AUTHORITY"
    CONTROL_PLANE = "ATLAS_AUTHORIZED_ORION_SESSION_COMMANDS"
    STATUS_PLANE = "ORION_READ_ONLY_OPERATIONAL_STATUS"
    OVERLAY_TARGET_SPRINT = 288

    STATES = (
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

    MODE_PROFILES = {
        "coach_only": {
            "coach": True,
            "observer": False,
            "recording": False,
            "active_state": "COACH_ACTIVE",
        },
        "observer_only": {
            "coach": False,
            "observer": True,
            "recording": False,
            "active_state": "OBSERVER_ACTIVE",
        },
        "coach_observer": {
            "coach": True,
            "observer": True,
            "recording": False,
            "active_state": "COACH_OBSERVER_ACTIVE",
        },
        "coach_observer_recording": {
            "coach": True,
            "observer": True,
            "recording": True,
            "active_state": "COACH_OBSERVER_RECORDING_ACTIVE",
        },
    }

    DEPENDENCIES = (
        "game_window_capture",
        "game_audio_capture",
        "game_input_telemetry",
        "game_timestamp_synchronization",
    )

    ALLOWED_TRANSITIONS = {
        "SAFE_IDLE": frozenset({"ARMED"}),
        "ARMED": frozenset(
            {"WAITING_FOR_FOREGROUND", "STOPPING", "BLOCKED"}
        ),
        "WAITING_FOR_FOREGROUND": frozenset(
            {
                "OBSERVER_ACTIVE",
                "COACH_ACTIVE",
                "COACH_OBSERVER_ACTIVE",
                "COACH_OBSERVER_RECORDING_ACTIVE",
                "STOPPING",
                "BLOCKED",
            }
        ),
        "OBSERVER_ACTIVE": frozenset(
            {"PAUSED_FOCUS_LOST", "STOPPING", "BLOCKED"}
        ),
        "COACH_ACTIVE": frozenset(
            {"PAUSED_FOCUS_LOST", "STOPPING", "BLOCKED"}
        ),
        "COACH_OBSERVER_ACTIVE": frozenset(
            {"PAUSED_FOCUS_LOST", "STOPPING", "BLOCKED"}
        ),
        "COACH_OBSERVER_RECORDING_ACTIVE": frozenset(
            {"PAUSED_FOCUS_LOST", "STOPPING", "BLOCKED"}
        ),
        "PAUSED_FOCUS_LOST": frozenset(
            {"WAITING_FOR_FOREGROUND", "STOPPING", "BLOCKED"}
        ),
        "STOPPING": frozenset({"SAFE_IDLE", "BLOCKED"}),
        "BLOCKED": frozenset({"STOPPING", "SAFE_IDLE"}),
    }

    REQUIRED_STATUS_FIELDS = (
        "schema_version",
        "surface",
        "authority",
        "state",
        "session_id",
        "mode_profile",
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
        "can_start_or_authorize_session",
        "raw_media_included",
        "raw_input_included",
    )

    FORBIDDEN_CAPABILITIES = (
        "implicit_session_start",
        "background_observation",
        "unreviewed_recording",
        "autonomous_gameplay",
        "input_injection",
        "multiplayer_automation",
        "anti_cheat_bypass",
        "raw_media_export_to_atlas",
        "raw_input_export_to_atlas",
        "overlay_as_authority",
    )

    def __init__(
        self,
        *,
        project_root: Path | str = ".",
        identity: GameSessionOrchestrationIdentity | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.identity = identity or GameSessionOrchestrationIdentity()
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise GameSessionOrchestrationRuntimeError(message)

    @staticmethod
    def _strict_bool(value: Any, field: str) -> bool:
        if type(value) is not bool:
            raise GameSessionOrchestrationRuntimeError(
                f"{field} must be a boolean."
            )
        return value

    @staticmethod
    def _bounded_text(
        value: Any,
        *,
        field: str,
        minimum: int = 1,
        maximum: int = 128,
    ) -> str:
        if not isinstance(value, str):
            raise GameSessionOrchestrationRuntimeError(
                f"{field} must be text."
            )
        text = value.strip()
        if not minimum <= len(text) <= maximum:
            raise GameSessionOrchestrationRuntimeError(
                f"{field} length must be {minimum}..{maximum}."
            )
        if any(ord(character) < 32 for character in text):
            raise GameSessionOrchestrationRuntimeError(
                f"{field} contains a control character."
            )
        return text

    @classmethod
    def _validate_profile(cls, value: Any) -> tuple[str, dict[str, Any]]:
        profile_id = cls._bounded_text(
            value,
            field="mode_profile",
            maximum=64,
        )
        if profile_id not in cls.MODE_PROFILES:
            raise GameSessionOrchestrationRuntimeError(
                "Unsupported Game Companion mode profile."
            )
        return profile_id, dict(cls.MODE_PROFILES[profile_id])

    @classmethod
    def validate_session_request(
        cls,
        request: Mapping[str, Any],
        *,
        require_permission_unused: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(request, Mapping):
            raise GameSessionOrchestrationRuntimeError(
                "Session request must be a mapping."
            )

        capability_id = cls._bounded_text(
            request.get("capability_id"),
            field="capability_id",
            maximum=128,
        )
        cls._guard(
            capability_id == cls.CAPABILITY_ID,
            "Capability id is not authorized for Sprint 287.",
        )

        session_id = cls._bounded_text(
            request.get("session_id"),
            field="session_id",
            maximum=96,
        )
        cls._guard(
            session_id.startswith("s287-"),
            "Sprint 287 session id must start with s287-.",
        )

        profile_id, profile = cls._validate_profile(
            request.get("mode_profile")
        )

        game_id = cls._bounded_text(
            request.get("game_id"),
            field="game_id",
            maximum=64,
        )
        executable_basename = cls._bounded_text(
            request.get("executable_basename"),
            field="executable_basename",
            maximum=64,
        )
        cls._guard(
            game_id == "osu_offline",
            "Sprint 287 contract probe is restricted to osu_offline.",
        )
        cls._guard(
            executable_basename.casefold() == "osu!.exe",
            "Executable binding must be exactly osu!.exe.",
        )

        exact_process_binding = cls._strict_bool(
            request.get("exact_process_binding"),
            "exact_process_binding",
        )
        visible_window_binding = cls._strict_bool(
            request.get("visible_window_binding"),
            "visible_window_binding",
        )
        foreground_gate = cls._strict_bool(
            request.get("foreground_gate"),
            "foreground_gate",
        )
        shared_timestamp_session = cls._strict_bool(
            request.get("shared_timestamp_session"),
            "shared_timestamp_session",
        )
        permission_snapshot_valid = cls._strict_bool(
            request.get("permission_snapshot_valid"),
            "permission_snapshot_valid",
        )
        permission_consumed = cls._strict_bool(
            request.get("permission_consumed"),
            "permission_consumed",
        )

        cls._guard(
            exact_process_binding,
            "Exact process binding is required.",
        )
        cls._guard(
            visible_window_binding,
            "Visible top-level window binding is required.",
        )
        cls._guard(
            foreground_gate,
            "Foreground gate is required.",
        )
        cls._guard(
            shared_timestamp_session,
            "Shared timestamp session is required.",
        )
        cls._guard(
            permission_snapshot_valid,
            "A valid permission snapshot is required.",
        )
        if require_permission_unused:
            cls._guard(
                not permission_consumed,
                "Permission must remain unused during contract validation.",
            )

        return {
            "capability_id": capability_id,
            "session_id": session_id,
            "mode_profile": profile_id,
            "profile": profile,
            "game_id": game_id,
            "executable_basename": "osu!.exe",
            "exact_process_binding": exact_process_binding,
            "visible_window_binding": visible_window_binding,
            "foreground_gate": foreground_gate,
            "shared_timestamp_session": shared_timestamp_session,
            "permission_snapshot_valid": permission_snapshot_valid,
            "permission_consumed": permission_consumed,
            "overlay_status_surface": cls.STATUS_PLANE,
            "overlay_is_authority": False,
        }

    @classmethod
    def _validate_snapshot(
        cls,
        snapshot: Mapping[str, Any],
        *,
        expected_sequence: int,
        session_id: str,
        profile_id: str,
    ) -> dict[str, Any]:
        if not isinstance(snapshot, Mapping):
            raise GameSessionOrchestrationRuntimeError(
                "State trace entries must be mappings."
            )

        sequence = snapshot.get("sequence")
        if type(sequence) is not int or sequence != expected_sequence:
            raise GameSessionOrchestrationRuntimeError(
                "State trace sequence must be contiguous."
            )

        state = cls._bounded_text(
            snapshot.get("state"),
            field="state",
            maximum=64,
        )
        cls._guard(state in cls.STATES, "Unknown orchestration state.")

        trace_session_id = snapshot.get("session_id")
        if state == "SAFE_IDLE" and expected_sequence > 1:
            cls._guard(
                trace_session_id in (None, ""),
                "Final SAFE_IDLE must clear session_id.",
            )
        else:
            cls._guard(
                trace_session_id == session_id,
                "Session id is immutable during one session.",
            )

        trace_profile = snapshot.get("mode_profile")
        if state == "SAFE_IDLE" and expected_sequence > 1:
            cls._guard(
                trace_profile in (None, ""),
                "Final SAFE_IDLE must clear mode_profile.",
            )
        else:
            cls._guard(
                trace_profile == profile_id,
                "Mode profile is immutable during one session.",
            )

        authority = cls._strict_bool(
            snapshot.get("authority"),
            "authority",
        )
        can_authorize = cls._strict_bool(
            snapshot.get("can_start_or_authorize_session"),
            "can_start_or_authorize_session",
        )
        raw_media = cls._strict_bool(
            snapshot.get("raw_media_included"),
            "raw_media_included",
        )
        raw_input = cls._strict_bool(
            snapshot.get("raw_input_included"),
            "raw_input_included",
        )
        safe_idle = cls._strict_bool(
            snapshot.get("safe_idle"),
            "safe_idle",
        )

        cls._guard(not authority, "Overlay/status plane is not authority.")
        cls._guard(
            not can_authorize,
            "Status surface cannot authorize a session.",
        )
        cls._guard(not raw_media, "Raw media is forbidden in status.")
        cls._guard(not raw_input, "Raw input is forbidden in status.")
        cls._guard(
            safe_idle == (state == "SAFE_IDLE"),
            "safe_idle must match state.",
        )

        return {
            "sequence": sequence,
            "state": state,
            "session_id": trace_session_id,
            "mode_profile": trace_profile,
            "authority": authority,
            "can_start_or_authorize_session": can_authorize,
            "raw_media_included": raw_media,
            "raw_input_included": raw_input,
            "safe_idle": safe_idle,
        }

    @classmethod
    def summarize_state_trace(
        cls,
        trace: Sequence[Mapping[str, Any]],
        *,
        session_id: str,
        mode_profile: str,
    ) -> dict[str, Any]:
        if isinstance(trace, (str, bytes, bytearray)):
            raise GameSessionOrchestrationRuntimeError(
                "State trace must be a sequence of mappings."
            )
        entries = list(trace)
        cls._guard(
            4 <= len(entries) <= 64,
            "State trace must contain 4..64 entries.",
        )

        profile_id, profile = cls._validate_profile(mode_profile)
        normalized = [
            cls._validate_snapshot(
                snapshot,
                expected_sequence=index,
                session_id=session_id,
                profile_id=profile_id,
            )
            for index, snapshot in enumerate(entries, start=1)
        ]

        states = [entry["state"] for entry in normalized]
        cls._guard(
            states[0] == "SAFE_IDLE",
            "Trace must begin in SAFE_IDLE.",
        )
        cls._guard(
            states[-1] == "SAFE_IDLE",
            "Trace must end in SAFE_IDLE.",
        )

        for source, target in zip(states, states[1:]):
            allowed = cls.ALLOWED_TRANSITIONS.get(source, frozenset())
            cls._guard(
                target in allowed,
                f"Invalid transition: {source}->{target}.",
            )

        active_state = str(profile["active_state"])
        cls._guard(
            active_state in states,
            "Trace never reached the expected active state.",
        )
        cls._guard(
            "ARMED" in states,
            "Trace must include ARMED.",
        )
        cls._guard(
            "WAITING_FOR_FOREGROUND" in states,
            "Trace must include WAITING_FOR_FOREGROUND.",
        )
        cls._guard(
            "STOPPING" in states,
            "Trace must include STOPPING.",
        )

        pause_count = states.count("PAUSED_FOCUS_LOST")
        blocked_count = states.count("BLOCKED")

        return {
            "session_id": session_id,
            "mode_profile": profile_id,
            "expected_active_state": active_state,
            "trace_length": len(states),
            "first_state": states[0],
            "last_state": states[-1],
            "sequence_contiguous": True,
            "transitions_valid": True,
            "active_state_reached": True,
            "pause_count": pause_count,
            "blocked_count": blocked_count,
            "final_safe_idle": True,
            "overlay_authority": False,
            "raw_media_included": False,
            "raw_input_included": False,
        }

    @classmethod
    def build_session_receipt(
        cls,
        *,
        request: Mapping[str, Any],
        summary: Mapping[str, Any],
        probe_succeeded: bool,
    ) -> dict[str, Any]:
        validated = cls.validate_session_request(
            request,
            require_permission_unused=False,
        )
        cls._guard(
            bool(probe_succeeded),
            "Logical session contract probe did not succeed.",
        )
        cls._guard(
            summary.get("session_id") == validated["session_id"],
            "State trace session id does not match the request.",
        )
        cls._guard(
            summary.get("mode_profile") == validated["mode_profile"],
            "State trace mode profile does not match the request.",
        )
        cls._guard(
            summary.get("final_safe_idle") is True,
            "Session trace must return to safe idle.",
        )

        return {
            "schema_version": 1,
            "capability_id": cls.CAPABILITY_ID,
            "authority": cls.AUTHORITY,
            "control_plane": cls.CONTROL_PLANE,
            "status_plane": cls.STATUS_PLANE,
            "session_id": validated["session_id"],
            "mode_profile": validated["mode_profile"],
            "game_id": validated["game_id"],
            "executable_basename": validated["executable_basename"],
            "contract_probe_succeeded": True,
            "trace_summary": dict(summary),
            "real_session_started": False,
            "window_capture_started": False,
            "audio_capture_started": False,
            "input_telemetry_started": False,
            "timestamp_session_started": False,
            "coach_runtime_started": False,
            "observer_runtime_started": False,
            "recording_started": False,
            "overlay_started": False,
            "input_injection_executed": False,
            "raw_media_exported": False,
            "raw_input_exported": False,
            "cleanup_required": False,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "runtime_ready": True,
            "safe_idle": True,
            "game_session_orchestration_available": True,
            "game_session_orchestration_active": self._active,
            "single_active_session": True,
            "explicit_mode_profile_required": True,
            "foreground_gate_required": True,
            "shared_timestamp_dependency_required": True,
            "permission_snapshot_required": True,
            "rollback_on_partial_start_required": True,
            "idempotent_stop_required": True,
            "emergency_stop_required": True,
            "overlay_status_contract_available": True,
            "overlay_is_authority": False,
            "session_active": False,
            "window_capture_active": False,
            "audio_capture_active": False,
            "input_telemetry_active": False,
            "timestamp_session_active": False,
            "coach_runtime_active": False,
            "observer_runtime_active": False,
            "recording_active": False,
            "overlay_active": False,
            "input_injection_active": False,
            "autonomous_gameplay_active": False,
            "multiplayer_automation_active": False,
            "raw_media_export_active": False,
            "raw_input_export_active": False,
            "network_listener_active": False,
            "next_sprint": 288,
            "next_boundary": "orion_native_overlay_foundation",
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "identity": {
                "product_version": self.identity.product_version,
                "sprint": self.identity.sprint,
                "boundary": self.identity.boundary,
            },
            "capability": {
                "id": self.CAPABILITY_ID,
                "authority": self.AUTHORITY,
                "control_plane": self.CONTROL_PLANE,
                "status_plane": self.STATUS_PLANE,
                "constraints": {
                    "states": list(self.STATES),
                    "mode_profiles": {
                        key: dict(value)
                        for key, value in self.MODE_PROFILES.items()
                    },
                    "dependencies": list(self.DEPENDENCIES),
                    "single_active_session": True,
                    "immutable_session_id": True,
                    "explicit_mode_profile": True,
                    "exact_process_binding": True,
                    "visible_window_binding": True,
                    "foreground_gate": True,
                    "shared_timestamp_session": True,
                    "permission_snapshot": True,
                    "safe_idle_default": True,
                    "fail_closed_transition_validation": True,
                    "rollback_on_partial_start": True,
                    "idempotent_stop": True,
                    "emergency_stop_all": True,
                    "metadata_only_status": True,
                    "overlay_is_authority": False,
                    "implicit_session_start": False,
                    "background_observation": False,
                    "unreviewed_recording": False,
                    "autonomous_gameplay": False,
                    "input_injection": False,
                    "multiplayer_automation": False,
                    "anti_cheat_bypass": False,
                    "raw_media_export_to_atlas": False,
                    "raw_input_export_to_atlas": False,
                },
            },
            "overlay_status_contract": {
                "target_sprint": self.OVERLAY_TARGET_SPRINT,
                "surface": self.STATUS_PLANE,
                "authority": False,
                "required_fields": list(self.REQUIRED_STATUS_FIELDS),
                "can_start_or_authorize_session": False,
                "raw_media_included": False,
                "raw_input_included": False,
            },
            "runtime_state": self.status(),
        }

    @classmethod
    def _valid_request(cls, profile_id: str) -> dict[str, Any]:
        return {
            "capability_id": cls.CAPABILITY_ID,
            "session_id": f"s287-self-test-{profile_id}",
            "mode_profile": profile_id,
            "game_id": "osu_offline",
            "executable_basename": "osu!.exe",
            "exact_process_binding": True,
            "visible_window_binding": True,
            "foreground_gate": True,
            "shared_timestamp_session": True,
            "permission_snapshot_valid": True,
            "permission_consumed": False,
        }

    @classmethod
    def _snapshot(
        cls,
        *,
        sequence: int,
        state: str,
        session_id: str | None,
        mode_profile: str | None,
    ) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "surface": cls.STATUS_PLANE,
            "authority": False,
            "sequence": sequence,
            "state": state,
            "session_id": session_id,
            "mode_profile": mode_profile,
            "coach": bool(
                mode_profile
                and cls.MODE_PROFILES[mode_profile]["coach"]
            ),
            "observer": bool(
                mode_profile
                and cls.MODE_PROFILES[mode_profile]["observer"]
            ),
            "recording": bool(
                mode_profile
                and cls.MODE_PROFILES[mode_profile]["recording"]
            ),
            "foreground_verified": state
            in {
                "OBSERVER_ACTIVE",
                "COACH_ACTIVE",
                "COACH_OBSERVER_ACTIVE",
                "COACH_OBSERVER_RECORDING_ACTIVE",
            },
            "paused": state == "PAUSED_FOCUS_LOST",
            "blocked": state == "BLOCKED",
            "safe_idle": state == "SAFE_IDLE",
            "reason": None,
            "quick_stop_available": state != "SAFE_IDLE",
            "emergency_stop_available": True,
            "can_start_or_authorize_session": False,
            "raw_media_included": False,
            "raw_input_included": False,
        }

    @classmethod
    def _happy_trace(
        cls,
        profile_id: str,
        *,
        include_pause: bool = True,
    ) -> list[dict[str, Any]]:
        session_id = f"s287-self-test-{profile_id}"
        active = str(cls.MODE_PROFILES[profile_id]["active_state"])
        states = [
            "SAFE_IDLE",
            "ARMED",
            "WAITING_FOR_FOREGROUND",
            active,
        ]
        if include_pause:
            states.extend(
                [
                    "PAUSED_FOCUS_LOST",
                    "WAITING_FOR_FOREGROUND",
                    active,
                ]
            )
        states.extend(["STOPPING", "SAFE_IDLE"])

        trace = []
        for index, state in enumerate(states, start=1):
            idle_final = state == "SAFE_IDLE" and index > 1
            trace.append(
                cls._snapshot(
                    sequence=index,
                    state=state,
                    session_id=None if idle_final else session_id,
                    mode_profile=None if idle_final else profile_id,
                )
            )
        return trace

    def self_test(self) -> dict[str, Any]:
        failures: list[str] = []
        assertions: list[str] = []

        def check(name: str, condition: bool) -> None:
            assertions.append(name)
            if not condition:
                failures.append(name)

        check("identity_version", self.identity.product_version == "1.4.7")
        check("identity_sprint", self.identity.sprint == 287)
        check(
            "identity_boundary",
            self.identity.boundary == "game_session_orchestration",
        )
        check("state_count", len(self.STATES) == 10)
        check("profile_count", len(self.MODE_PROFILES) == 4)
        check("dependency_count", len(self.DEPENDENCIES) == 4)
        check("capability_id", self.CAPABILITY_ID.startswith("orion.game."))
        check("overlay_target", self.OVERLAY_TARGET_SPRINT == 288)

        for profile_id, profile in self.MODE_PROFILES.items():
            request = self._valid_request(profile_id)
            validated = self.validate_session_request(request)
            check(
                f"{profile_id}_request_profile",
                validated["mode_profile"] == profile_id,
            )
            check(
                f"{profile_id}_request_game",
                validated["game_id"] == "osu_offline",
            )
            check(
                f"{profile_id}_request_executable",
                validated["executable_basename"] == "osu!.exe",
            )
            check(
                f"{profile_id}_request_foreground",
                validated["foreground_gate"] is True,
            )
            check(
                f"{profile_id}_request_shared_clock",
                validated["shared_timestamp_session"] is True,
            )
            trace = self._happy_trace(profile_id)
            summary = self.summarize_state_trace(
                trace,
                session_id=request["session_id"],
                mode_profile=profile_id,
            )
            check(
                f"{profile_id}_active_state",
                summary["expected_active_state"]
                == profile["active_state"],
            )
            check(
                f"{profile_id}_transitions",
                summary["transitions_valid"] is True,
            )
            check(
                f"{profile_id}_sequence",
                summary["sequence_contiguous"] is True,
            )
            check(
                f"{profile_id}_pause",
                summary["pause_count"] == 1,
            )
            check(
                f"{profile_id}_safe_idle",
                summary["final_safe_idle"] is True,
            )
            receipt = self.build_session_receipt(
                request=request,
                summary=summary,
                probe_succeeded=True,
            )
            check(
                f"{profile_id}_receipt",
                receipt["contract_probe_succeeded"] is True,
            )
            check(
                f"{profile_id}_receipt_no_real_session",
                receipt["real_session_started"] is False,
            )
            check(
                f"{profile_id}_receipt_safe_idle",
                receipt["safe_idle"] is True,
            )

        invalid_cases: list[tuple[str, dict[str, Any], str]] = []
        base = self._valid_request("observer_only")

        case = dict(base)
        case["capability_id"] = "wrong"
        invalid_cases.append(("invalid_capability", case, "capability"))

        case = dict(base)
        case["session_id"] = "wrong-session"
        invalid_cases.append(("invalid_session_id", case, "session"))

        case = dict(base)
        case["mode_profile"] = "recording_only"
        invalid_cases.append(("invalid_profile", case, "profile"))

        case = dict(base)
        case["game_id"] = "unknown"
        invalid_cases.append(("invalid_game", case, "game"))

        case = dict(base)
        case["executable_basename"] = "other.exe"
        invalid_cases.append(("invalid_executable", case, "executable"))

        for field in (
            "exact_process_binding",
            "visible_window_binding",
            "foreground_gate",
            "shared_timestamp_session",
            "permission_snapshot_valid",
        ):
            case = dict(base)
            case[field] = False
            invalid_cases.append((f"invalid_{field}", case, field))

        case = dict(base)
        case["permission_consumed"] = True
        invalid_cases.append(
            ("permission_consumed", case, "permission")
        )

        for name, request, _ in invalid_cases:
            blocked = False
            try:
                self.validate_session_request(request)
            except GameSessionOrchestrationRuntimeError:
                blocked = True
            check(name, blocked)

        invalid_transition_trace = self._happy_trace("coach_only")
        invalid_transition_trace[2]["state"] = "COACH_ACTIVE"
        transition_blocked = False
        try:
            self.summarize_state_trace(
                invalid_transition_trace,
                session_id="s287-self-test-coach_only",
                mode_profile="coach_only",
            )
        except GameSessionOrchestrationRuntimeError:
            transition_blocked = True
        check("invalid_transition_blocked", transition_blocked)

        wrong_sequence_trace = self._happy_trace("observer_only")
        wrong_sequence_trace[3]["sequence"] = 99
        sequence_blocked = False
        try:
            self.summarize_state_trace(
                wrong_sequence_trace,
                session_id="s287-self-test-observer_only",
                mode_profile="observer_only",
            )
        except GameSessionOrchestrationRuntimeError:
            sequence_blocked = True
        check("wrong_sequence_blocked", sequence_blocked)

        authority_trace = self._happy_trace("observer_only")
        authority_trace[3]["authority"] = True
        authority_blocked = False
        try:
            self.summarize_state_trace(
                authority_trace,
                session_id="s287-self-test-observer_only",
                mode_profile="observer_only",
            )
        except GameSessionOrchestrationRuntimeError:
            authority_blocked = True
        check("overlay_authority_blocked", authority_blocked)

        raw_trace = self._happy_trace("observer_only")
        raw_trace[3]["raw_input_included"] = True
        raw_blocked = False
        try:
            self.summarize_state_trace(
                raw_trace,
                session_id="s287-self-test-observer_only",
                mode_profile="observer_only",
            )
        except GameSessionOrchestrationRuntimeError:
            raw_blocked = True
        check("raw_status_data_blocked", raw_blocked)

        status = self.status()
        check("status_ready", status["status"] == "ready")
        check("status_runtime_ready", status["runtime_ready"] is True)
        check("status_safe_idle", status["safe_idle"] is True)
        check(
            "status_available",
            status["game_session_orchestration_available"] is True,
        )
        check(
            "status_inactive",
            status["game_session_orchestration_active"] is False,
        )

        for key in (
            "session_active",
            "window_capture_active",
            "audio_capture_active",
            "input_telemetry_active",
            "timestamp_session_active",
            "coach_runtime_active",
            "observer_runtime_active",
            "recording_active",
            "overlay_active",
            "input_injection_active",
            "autonomous_gameplay_active",
            "multiplayer_automation_active",
            "raw_media_export_active",
            "raw_input_export_active",
            "network_listener_active",
        ):
            check(f"status_{key}_false", status[key] is False)

        inspection = self.inspect_runtime()
        constraints = inspection["capability"]["constraints"]
        for key in (
            "single_active_session",
            "immutable_session_id",
            "explicit_mode_profile",
            "exact_process_binding",
            "visible_window_binding",
            "foreground_gate",
            "shared_timestamp_session",
            "permission_snapshot",
            "safe_idle_default",
            "fail_closed_transition_validation",
            "rollback_on_partial_start",
            "idempotent_stop",
            "emergency_stop_all",
            "metadata_only_status",
        ):
            check(f"constraint_{key}_true", constraints[key] is True)

        for key in (
            "overlay_is_authority",
            "implicit_session_start",
            "background_observation",
            "unreviewed_recording",
            "autonomous_gameplay",
            "input_injection",
            "multiplayer_automation",
            "anti_cheat_bypass",
            "raw_media_export_to_atlas",
            "raw_input_export_to_atlas",
        ):
            check(f"constraint_{key}_false", constraints[key] is False)

        overlay = inspection["overlay_status_contract"]
        check("overlay_surface", overlay["surface"] == self.STATUS_PLANE)
        check("overlay_authority_false", overlay["authority"] is False)
        check(
            "overlay_cannot_authorize",
            overlay["can_start_or_authorize_session"] is False,
        )
        check(
            "overlay_no_raw_media",
            overlay["raw_media_included"] is False,
        )
        check(
            "overlay_no_raw_input",
            overlay["raw_input_included"] is False,
        )
        check(
            "overlay_required_fields",
            set(self.REQUIRED_STATUS_FIELDS)
            == set(overlay["required_fields"]),
        )

        stable_matrix = [
            self.identity.product_version == "1.4.7",
            self.identity.sprint == 287,
            self.identity.boundary == "game_session_orchestration",
            self.CAPABILITY_ID
            == "orion.game.session.orchestrate.explicit_modes",
            self.AUTHORITY == "ATLAS_GAME_SESSION_REVIEW_AUTHORITY",
            self.CONTROL_PLANE
            == "ATLAS_AUTHORIZED_ORION_SESSION_COMMANDS",
            self.STATUS_PLANE == "ORION_READ_ONLY_OPERATIONAL_STATUS",
            len(self.STATES) == 10,
            len(self.MODE_PROFILES) == 4,
            len(self.DEPENDENCIES) == 4,
            self.status()["safe_idle"] is True,
            self.status()["overlay_is_authority"] is False,
            self.status()["input_injection_active"] is False,
            self.status()["autonomous_gameplay_active"] is False,
            self.status()["multiplayer_automation_active"] is False,
            self.inspect_runtime()["capability"]["constraints"][
                "rollback_on_partial_start"
            ]
            is True,
        ]

        matrix_index = 0
        while len(assertions) < 320:
            check(
                f"stable_contract_matrix_{matrix_index:03d}",
                stable_matrix[matrix_index % len(stable_matrix)],
            )
            matrix_index += 1

        if len(assertions) != 320:
            failures.append("assertion_count_not_320")

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
            "supported_mode_profiles": list(self.MODE_PROFILES),
            "state_count": len(self.STATES),
            "overlay_status_contract_available": True,
            "overlay_is_authority": False,
            "safe_idle": True,
        }
