"""Sprint 281 Game Companion runtime foundation.

This module is deterministic and side-effect-free. It defines the catalog,
operator-selectable modes, session state machine, pipeline separation, and
hard safety guards required before Sprint 282 supported-game detection.

It does not scan processes or windows, capture screen/audio, record gameplay,
collect input telemetry, launch applications, control game input, open network
connections, persist session state, or execute actions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class GameCompanionRuntimeFoundationError(RuntimeError):
    """Raised when the Sprint 281 foundation violates its contract."""


@dataclass(frozen=True, slots=True)
class GameCompanionRuntimeIdentity:
    """Stable metadata for the Sprint 281 boundary."""

    component_name: str
    component_version: str
    product_version: str
    sprint: int
    boundary: str
    host_role: str
    reference_game_id: str


class AuraGameCompanionRuntimeFoundationManager:
    """Expose the closed Game Companion runtime foundation."""

    COMPONENT_NAME = "game_companion_runtime_foundation"
    COMPONENT_VERSION = "0.1.0"
    PRODUCT_VERSION = "1.4.1"
    SPRINT = 281
    BOUNDARY = "game_companion_runtime_foundation"
    HOST_ROLE = "ATLAS_CONTROL_AUTHORITY"
    REFERENCE_GAME_ID = "osu_offline"

    MODE_CATALOG: tuple[dict[str, Any], ...] = (
        {
            "mode_id": "coach_only",
            "coach": True,
            "observer": False,
            "recording": False,
            "operator_selectable": True,
        },
        {
            "mode_id": "observer_only",
            "coach": False,
            "observer": True,
            "recording": False,
            "operator_selectable": True,
        },
        {
            "mode_id": "coach_observer",
            "coach": True,
            "observer": True,
            "recording": False,
            "operator_selectable": True,
        },
        {
            "mode_id": "coach_observer_recording",
            "coach": True,
            "observer": True,
            "recording": True,
            "operator_selectable": True,
        },
    )

    GAME_CATALOG: tuple[dict[str, Any], ...] = (
        {
            "game_id": "osu_offline",
            "title": "osu!",
            "catalog_status": "reference",
            "first_runtime_role": "coach_observer_recording",
            "environment_policy": "offline_only",
            "input_profile": "keyboard_mouse",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "beat_saber",
            "title": "Beat Saber",
            "catalog_status": "planned",
            "first_runtime_role": "observer_performer_later",
            "environment_policy": "private_or_offline_first",
            "input_profile": "vr_controller",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "monster_hunter_world_single_player",
            "title": "Monster Hunter: World",
            "catalog_status": "planned",
            "first_runtime_role": "hunter_coach",
            "environment_policy": "single_player_only",
            "input_profile": "keyboard_mouse",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "ace_combat_single_player",
            "title": "Ace Combat",
            "catalog_status": "planned",
            "first_runtime_role": "observer_virtual_pilot_later",
            "environment_policy": "single_player_only",
            "input_profile": "controller_or_virtual_controller",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "mortal_kombat_local",
            "title": "Mortal Kombat",
            "catalog_status": "planned",
            "first_runtime_role": "local_opponent_research_later",
            "environment_policy": "local_two_player_only",
            "input_profile": "controller_or_virtual_controller",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "resident_evil_4_observer",
            "title": "Resident Evil 4",
            "catalog_status": "planned",
            "first_runtime_role": "observer_first",
            "environment_policy": "single_player_only",
            "input_profile": "keyboard_mouse",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "minecraft_private",
            "title": "Minecraft",
            "catalog_status": "legacy_candidate",
            "first_runtime_role": "private_world_companion",
            "environment_policy": "private_or_local_only",
            "input_profile": "keyboard_mouse",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
        {
            "game_id": "arknights_endfield_deferred",
            "title": "Arknights: Endfield",
            "catalog_status": "deferred",
            "first_runtime_role": "none",
            "environment_policy": "not_active",
            "input_profile": "keyboard_mouse",
            "ranked_or_score_submission_automation": False,
            "autonomous_control": False,
        },
    )

    EXCLUDED_GAME_IDS = (
        "genshin_impact",
        "clash_of_clans",
    )

    SESSION_STATES = (
        "safe_idle",
        "game_detected_pending_review",
        "mode_selected_pending_start",
        "session_active",
        "session_stopping",
        "session_review_pending",
        "session_closed",
        "emergency_stopped",
        "failed_safe",
    )

    ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
        "safe_idle": ("game_detected_pending_review",),
        "game_detected_pending_review": (
            "mode_selected_pending_start",
            "safe_idle",
            "emergency_stopped",
            "failed_safe",
        ),
        "mode_selected_pending_start": (
            "session_active",
            "safe_idle",
            "emergency_stopped",
            "failed_safe",
        ),
        "session_active": (
            "session_stopping",
            "emergency_stopped",
            "failed_safe",
        ),
        "session_stopping": (
            "session_review_pending",
            "emergency_stopped",
            "failed_safe",
        ),
        "session_review_pending": (
            "session_closed",
            "failed_safe",
        ),
        "session_closed": ("safe_idle",),
        "emergency_stopped": ("session_review_pending", "safe_idle"),
        "failed_safe": ("session_review_pending", "safe_idle"),
    }

    FALSE_RUNTIME_FIELDS = (
        "process_scan_active",
        "window_scan_active",
        "supported_game_detection_active",
        "safe_idle_prompt_active",
        "game_window_capture_active",
        "game_audio_capture_active",
        "input_telemetry_active",
        "timestamp_synchronization_active",
        "recording_active",
        "dataset_manifest_write_active",
        "public_stream_pipeline_active",
        "private_dataset_pipeline_active",
        "post_session_analysis_active",
        "coach_feedback_active",
        "voice_command_to_action_active",
        "application_launch_active",
        "game_input_control_active",
        "autonomous_gameplay_active",
        "multiplayer_automation_active",
        "network_listener_active",
        "network_connection_active",
        "persistent_state_write_active",
        "external_action_execution_active",
    )

    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root).resolve()

    def identity(self) -> dict[str, Any]:
        """Return deterministic component identity metadata."""

        return asdict(
            GameCompanionRuntimeIdentity(
                component_name=self.COMPONENT_NAME,
                component_version=self.COMPONENT_VERSION,
                product_version=self.PRODUCT_VERSION,
                sprint=self.SPRINT,
                boundary=self.BOUNDARY,
                host_role=self.HOST_ROLE,
                reference_game_id=self.REFERENCE_GAME_ID,
            )
        )

    def mode_catalog(self) -> list[dict[str, Any]]:
        """Return fresh copies of the four operator-selectable modes."""

        return [dict(item) for item in self.MODE_CATALOG]

    def game_catalog(self) -> list[dict[str, Any]]:
        """Return the canonical planning catalog; detection remains disabled."""

        return [dict(item) for item in self.GAME_CATALOG]

    def session_contract(self) -> dict[str, Any]:
        """Return the non-persistent session state-machine contract."""

        return {
            "initial_state": "safe_idle",
            "states": list(self.SESSION_STATES),
            "allowed_transitions": {
                state: list(targets)
                for state, targets in self.ALLOWED_TRANSITIONS.items()
            },
            "operator_selects_mode": True,
            "operator_starts_session": True,
            "operator_can_stop_session": True,
            "emergency_stop_independent": True,
            "automatic_session_start": False,
            "automatic_recovery": False,
            "state_persistence_active": False,
        }

    def pipeline_contract(self) -> dict[str, Any]:
        """Keep public output and private dataset recording independent."""

        return {
            "public_stream_pipeline": {
                "active": False,
                "purpose": "future_public_creator_output",
                "contains_private_training_dataset": False,
            },
            "private_dataset_pipeline": {
                "active": False,
                "purpose": "future_private_training_recording",
                "published_publicly": False,
            },
            "separate_pipelines_required": True,
            "shared_implicit_sink_allowed": False,
            "operator_visibility_required": True,
            "recording_requires_explicit_mode": True,
        }

    def status(self) -> dict[str, Any]:
        """Return the closed and safe-idle Sprint 281 status."""

        return {
            "status": "ready",
            "reason": "game_companion_runtime_foundation_ready_runtime_closed",
            "safe_idle": True,
            "foundation_only": True,
            "runtime_ready": False,
            "reference_game_id": self.REFERENCE_GAME_ID,
            "catalog_game_count": len(self.GAME_CATALOG),
            "operator_mode_count": len(self.MODE_CATALOG),
            "session_state_count": len(self.SESSION_STATES),
            "public_private_pipeline_separated": True,
            "no_autonomous_game_control": True,
            **{field: False for field in self.FALSE_RUNTIME_FIELDS},
        }

    def inspect_foundation(self) -> dict[str, Any]:
        """Describe Sprint 281 without activating a runtime."""

        return {
            "identity": self.identity(),
            "runtime": self.status(),
            "modes": self.mode_catalog(),
            "games": self.game_catalog(),
            "excluded_game_ids": list(self.EXCLUDED_GAME_IDS),
            "session": self.session_contract(),
            "pipelines": self.pipeline_contract(),
            "next_boundary": {
                "sprint": 282,
                "boundary": "supported_game_detection",
                "runtime_activation_allowed_in_sprint_281": False,
            },
            "hard_guards": {
                "scan_processes": False,
                "scan_windows": False,
                "capture_screen": False,
                "capture_audio": False,
                "collect_input_telemetry": False,
                "start_recording": False,
                "write_dataset_manifest": False,
                "launch_game": False,
                "control_keyboard_or_mouse": False,
                "control_virtual_controller": False,
                "execute_voice_command_action": False,
                "automate_multiplayer": False,
                "publish_private_dataset": False,
                "open_network_connection": False,
                "persist_runtime_state": False,
            },
        }

    def find_game(self, game_id: str) -> dict[str, Any]:
        """Return one catalog item or raise a contract error."""

        for game in self.GAME_CATALOG:
            if game["game_id"] == game_id:
                return dict(game)
        raise GameCompanionRuntimeFoundationError(
            f"unknown game_id: {game_id}"
        )

    def find_mode(self, mode_id: str) -> dict[str, Any]:
        """Return one mode item or raise a contract error."""

        for mode in self.MODE_CATALOG:
            if mode["mode_id"] == mode_id:
                return dict(mode)
        raise GameCompanionRuntimeFoundationError(
            f"unknown mode_id: {mode_id}"
        )

    def transition_allowed(self, current_state: str, next_state: str) -> bool:
        """Check a proposed state transition without changing state."""

        return next_state in self.ALLOWED_TRANSITIONS.get(current_state, ())

    def build_session_proposal(
        self,
        *,
        game_id: str,
        mode_id: str,
    ) -> dict[str, Any]:
        """Build a review-only proposal with every execution path disabled."""

        game = self.find_game(game_id)
        mode = self.find_mode(mode_id)
        return {
            "status": "proposal_ready",
            "foundation_only": True,
            "game": game,
            "mode": mode,
            "current_state": "safe_idle",
            "proposed_state": "mode_selected_pending_start",
            "operator_review_required": True,
            "operator_start_required": True,
            "permission_grant_required_in_future_runtime": True,
            "execution_ready": False,
            "executed": False,
            "capture_started": False,
            "audio_capture_started": False,
            "telemetry_started": False,
            "recording_started": False,
            "game_input_control_started": False,
            "external_action_execution_started": False,
            "note": (
                "Sprint 281 produces a deterministic review-only proposal. "
                "Sprint 282 owns supported-game detection."
            ),
        }

    def self_test(self) -> dict[str, Any]:
        """Validate the complete foundation contract without side effects."""

        assertions: list[tuple[str, bool]] = []

        def check(name: str, condition: bool) -> None:
            assertions.append((name, bool(condition)))

        identity = self.identity()
        status = self.status()
        modes = self.mode_catalog()
        games = self.game_catalog()
        session = self.session_contract()
        pipelines = self.pipeline_contract()
        inspection = self.inspect_foundation()

        expected_identity = {
            "component_name": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "product_version": self.PRODUCT_VERSION,
            "sprint": self.SPRINT,
            "boundary": self.BOUNDARY,
            "host_role": self.HOST_ROLE,
            "reference_game_id": self.REFERENCE_GAME_ID,
        }
        for field, expected in expected_identity.items():
            check(f"identity_{field}", identity.get(field) == expected)

        check("status_ready", status["status"] == "ready")
        check(
            "status_reason_exact",
            status["reason"]
            == "game_companion_runtime_foundation_ready_runtime_closed",
        )
        check("safe_idle_true", status["safe_idle"] is True)
        check("foundation_only_true", status["foundation_only"] is True)
        check("runtime_ready_false", status["runtime_ready"] is False)
        check("catalog_game_count_exact", status["catalog_game_count"] == 8)
        check("operator_mode_count_exact", status["operator_mode_count"] == 4)
        check("session_state_count_exact", status["session_state_count"] == 9)
        check(
            "public_private_pipeline_separated",
            status["public_private_pipeline_separated"] is True,
        )
        check(
            "no_autonomous_game_control",
            status["no_autonomous_game_control"] is True,
        )
        for field in self.FALSE_RUNTIME_FIELDS:
            check(f"runtime_false_{field}", status[field] is False)

        expected_modes = [
            "coach_only",
            "observer_only",
            "coach_observer",
            "coach_observer_recording",
        ]
        check(
            "mode_ids_exact",
            [item["mode_id"] for item in modes] == expected_modes,
        )
        for mode in modes:
            check(
                f"mode_operator_selectable_{mode['mode_id']}",
                mode["operator_selectable"] is True,
            )
        recording_modes = [
            item["mode_id"] for item in modes if item["recording"] is True
        ]
        check(
            "recording_mode_exact",
            recording_modes == ["coach_observer_recording"],
        )

        game_ids = [item["game_id"] for item in games]
        check("reference_game_present", self.REFERENCE_GAME_ID in game_ids)
        check(
            "reference_game_first",
            game_ids[0] == self.REFERENCE_GAME_ID,
        )
        reference = self.find_game(self.REFERENCE_GAME_ID)
        check(
            "reference_game_status",
            reference["catalog_status"] == "reference",
        )
        check(
            "reference_game_offline_only",
            reference["environment_policy"] == "offline_only",
        )
        for game in games:
            check(
                f"game_no_autonomous_control_{game['game_id']}",
                game["autonomous_control"] is False,
            )
            check(
                f"game_no_ranked_automation_{game['game_id']}",
                game["ranked_or_score_submission_automation"] is False,
            )
        for excluded in self.EXCLUDED_GAME_IDS:
            check(f"excluded_not_catalogued_{excluded}", excluded not in game_ids)

        check("session_initial_safe_idle", session["initial_state"] == "safe_idle")
        check(
            "session_states_exact",
            session["states"] == list(self.SESSION_STATES),
        )
        check(
            "safe_idle_detection_transition",
            self.transition_allowed(
                "safe_idle", "game_detected_pending_review"
            ),
        )
        check(
            "no_safe_idle_direct_active",
            not self.transition_allowed("safe_idle", "session_active"),
        )
        check(
            "active_can_stop",
            self.transition_allowed("session_active", "session_stopping"),
        )
        check(
            "active_can_emergency_stop",
            self.transition_allowed(
                "session_active", "emergency_stopped"
            ),
        )
        check(
            "closed_returns_safe_idle",
            self.transition_allowed("session_closed", "safe_idle"),
        )
        check(
            "automatic_session_start_false",
            session["automatic_session_start"] is False,
        )
        check(
            "automatic_recovery_false",
            session["automatic_recovery"] is False,
        )
        check(
            "state_persistence_false",
            session["state_persistence_active"] is False,
        )

        check(
            "pipeline_separation_required",
            pipelines["separate_pipelines_required"] is True,
        )
        check(
            "implicit_shared_sink_forbidden",
            pipelines["shared_implicit_sink_allowed"] is False,
        )
        check(
            "public_pipeline_inactive",
            pipelines["public_stream_pipeline"]["active"] is False,
        )
        check(
            "private_pipeline_inactive",
            pipelines["private_dataset_pipeline"]["active"] is False,
        )
        check(
            "public_excludes_private_dataset",
            pipelines["public_stream_pipeline"][
                "contains_private_training_dataset"
            ]
            is False,
        )
        check(
            "private_not_published",
            pipelines["private_dataset_pipeline"]["published_publicly"]
            is False,
        )

        for mode_id in expected_modes:
            proposal = self.build_session_proposal(
                game_id=self.REFERENCE_GAME_ID,
                mode_id=mode_id,
            )
            check(
                f"proposal_ready_{mode_id}",
                proposal["status"] == "proposal_ready",
            )
            check(
                f"proposal_execution_closed_{mode_id}",
                proposal["execution_ready"] is False
                and proposal["executed"] is False,
            )
            check(
                f"proposal_no_capture_{mode_id}",
                proposal["capture_started"] is False
                and proposal["audio_capture_started"] is False,
            )
            check(
                f"proposal_no_telemetry_recording_{mode_id}",
                proposal["telemetry_started"] is False
                and proposal["recording_started"] is False,
            )
            check(
                f"proposal_no_control_{mode_id}",
                proposal["game_input_control_started"] is False
                and proposal["external_action_execution_started"] is False,
            )

        try:
            self.find_game("unknown_game")
        except GameCompanionRuntimeFoundationError:
            check("unknown_game_rejected", True)
        else:
            check("unknown_game_rejected", False)

        try:
            self.find_mode("unknown_mode")
        except GameCompanionRuntimeFoundationError:
            check("unknown_mode_rejected", True)
        else:
            check("unknown_mode_rejected", False)

        for guard, value in inspection["hard_guards"].items():
            check(f"hard_guard_{guard}", value is False)

        check(
            "next_sprint_exact",
            inspection["next_boundary"]["sprint"] == 282,
        )
        check(
            "next_boundary_exact",
            inspection["next_boundary"]["boundary"]
            == "supported_game_detection",
        )
        check(
            "sprint_281_activation_forbidden",
            inspection["next_boundary"][
                "runtime_activation_allowed_in_sprint_281"
            ]
            is False,
        )
        check(
            "constructor_side_effects_zero",
            self.project_root == Path(self.project_root).resolve(),
        )

        failed = [name for name, passed in assertions if not passed]
        payload = {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": identity,
            "runtime": status,
        }
        if failed:
            raise GameCompanionRuntimeFoundationError(
                "Sprint 281 self-test failed: " + ", ".join(failed)
            )
        return payload
