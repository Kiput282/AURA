"""ORION adapter contract for Sprint 287 session orchestration."""

from __future__ import annotations

import platform
from typing import Any, Callable, Mapping, Sequence

from .aura_game_session_orchestration_runtime_manager import (
    AuraGameSessionOrchestrationRuntimeManager,
    GameSessionOrchestrationRuntimeError,
)


class AuraWindowsGameSessionOrchestrationAdapter:
    """Disabled-by-default adapter for one logical state-machine probe."""

    def __init__(
        self,
        *,
        manager: AuraGameSessionOrchestrationRuntimeManager,
        enabled: bool = False,
        state_trace_runner: (
            Callable[
                [Mapping[str, Any]],
                Sequence[Mapping[str, Any]],
            ]
            | None
        ) = None,
    ) -> None:
        self.manager = manager
        self.enabled = bool(enabled)
        self.state_trace_runner = state_trace_runner
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise GameSessionOrchestrationRuntimeError(message)

    def build_powershell_contract(
        self,
        request: Mapping[str, Any],
    ) -> str:
        validated = self.manager.validate_session_request(
            request,
            require_permission_unused=False,
        )
        return f"""# AURA Sprint 287 logical session-orchestration contract
# A separately reviewed ORION helper is required.
# Session: {validated['session_id']}
# Profile: {validated['mode_profile']}
# Game: {validated['game_id']} / {validated['executable_basename']}
# ATLAS remains authority. ORION status/overlay is read-only.
# A real session MUST require exact process and visible-window binding,
# foreground verification, an approved permission snapshot, and one shared
# timestamp session. Partial starts MUST roll back. Stop and emergency-stop
# MUST be idempotent. The helper MUST NOT start capture, coaching, recording,
# input injection, autonomous gameplay, multiplayer automation, or raw export.
$ErrorActionPreference = 'Stop'
throw 'orion_session_orchestration_helper_required_fail_closed'
"""

    def probe_once(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._guard(
            self.enabled,
            "Game session orchestration adapter is disabled.",
        )
        self._guard(
            not self._active,
            "A logical session contract probe is already active.",
        )
        self._guard(
            self.state_trace_runner is not None,
            "Explicit logical state-trace runner is required.",
        )

        validated = self.manager.validate_session_request(
            request,
            require_permission_unused=False,
        )

        self._active = True
        try:
            trace = self.state_trace_runner(validated)
            self._guard(
                not isinstance(trace, (str, bytes, bytearray)),
                "State trace runner must return mapping entries.",
            )
            summary = self.manager.summarize_state_trace(
                trace,
                session_id=validated["session_id"],
                mode_profile=validated["mode_profile"],
            )
            receipt = self.manager.build_session_receipt(
                request=validated,
                summary=summary,
                probe_succeeded=True,
            )
            return {
                "receipt": receipt,
                "backend": {
                    "implementation": (
                        "atlas_authorized_orion_game_session_state_machine"
                    ),
                    "logical_contract_probe_only": True,
                    "single_active_session": True,
                    "foreground_gate": True,
                    "rollback_on_partial_start": True,
                    "idempotent_stop": True,
                    "emergency_stop_all": True,
                    "overlay_status_contract": True,
                    "overlay_is_authority": False,
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
                },
            }
        finally:
            self._active = False

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsGameSessionOrchestrationAdapter",
            "enabled": self.enabled,
            "probe_active": self._active,
            "platform": platform.system(),
            "state_trace_runner_injected": (
                self.state_trace_runner is not None
            ),
            "logical_contract_probe_only": True,
            "single_active_session": True,
            "foreground_gate": True,
            "rollback_on_partial_start": True,
            "idempotent_stop": True,
            "emergency_stop_all": True,
            "overlay_status_contract": True,
            "overlay_is_authority": False,
            "real_session": False,
            "window_capture": False,
            "audio_capture": False,
            "input_telemetry": False,
            "timestamp_session": False,
            "coach_runtime": False,
            "observer_runtime": False,
            "recording": False,
            "overlay": False,
            "input_injection": False,
            "raw_media_export": False,
            "raw_input_export": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "orion_session_contract": {
                "authority": self.manager.AUTHORITY,
                "control_plane": self.manager.CONTROL_PLANE,
                "status_plane": self.manager.STATUS_PLANE,
                "states": list(self.manager.STATES),
                "mode_profiles": list(self.manager.MODE_PROFILES),
                "dependencies": list(self.manager.DEPENDENCIES),
                "foreground_loss_behavior": "pause_or_stop_fail_closed",
                "partial_start_behavior": "rollback_to_safe_idle",
                "normal_stop_behavior": "idempotent",
                "emergency_stop_behavior": "idempotent_stop_all",
                "missing_helper_behavior": "fail_closed",
                "overlay_target_sprint": 288,
                "overlay_is_authority": False,
                "metadata_only_status": True,
                "real_session_started": False,
            },
        }
