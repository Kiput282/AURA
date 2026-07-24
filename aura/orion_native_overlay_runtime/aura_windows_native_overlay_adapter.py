"""Disabled-by-default ORION adapter for Sprint 288 overlay foundation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .aura_orion_native_overlay_runtime_manager import (
    AuraOrionNativeOverlayRuntimeManager,
    OrionNativeOverlayRuntimeError,
)


class AuraWindowsNativeOverlayAdapter:
    """Build reviewed launch specifications without starting a process."""

    SAFE_IDLE_PREVIEW_APPROVAL = (
        "APPROVE AURA SPRINT 288 SAFE IDLE OVERLAY PREVIEW"
    )

    def __init__(
        self,
        *,
        manager: AuraOrionNativeOverlayRuntimeManager,
        enabled: bool = False,
    ) -> None:
        self.manager = manager
        self.enabled = bool(enabled)
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise OrionNativeOverlayRuntimeError(message)

    def helper_path(self) -> Path:
        return self.manager.helper_path(self.manager.project_root)

    def build_inspect_launch_spec(self) -> dict[str, Any]:
        helper = self.helper_path()
        self._guard(helper.is_file(), "ORION overlay helper is missing.")
        return {
            "executable": "powershell.exe",
            "arguments": [
                "-NoProfile",
                "-STA",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(helper),
                "-Mode",
                "Inspect",
            ],
            "requires_explicit_approval": False,
            "starts_window": False,
            "starts_session": False,
            "reads_input": False,
            "starts_network_listener": False,
        }

    def build_safe_idle_preview_spec(
        self,
        *,
        approval: str,
        view_profile: str = "normal",
        duration_seconds: int = 5,
        screen_index: int = 0,
    ) -> dict[str, Any]:
        self._guard(self.enabled, "Overlay adapter is disabled.")
        self._guard(
            approval == self.SAFE_IDLE_PREVIEW_APPROVAL,
            "Exact safe-idle preview approval is required.",
        )
        self._guard(
            view_profile in self.manager.VIEW_PROFILES,
            "Unknown overlay view profile.",
        )
        self._guard(
            type(duration_seconds) is int
            and 1 <= duration_seconds <= 15,
            "Preview duration must be 1..15 seconds.",
        )
        self._guard(
            type(screen_index) is int and 0 <= screen_index <= 15,
            "Screen index must be 0..15.",
        )

        helper = self.helper_path()
        self._guard(helper.is_file(), "ORION overlay helper is missing.")

        return {
            "executable": "powershell.exe",
            "arguments": [
                "-NoProfile",
                "-STA",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(helper),
                "-Mode",
                "PreviewSafeIdle",
                "-Approval",
                approval,
                "-ViewProfile",
                view_profile,
                "-DurationSeconds",
                str(duration_seconds),
                "-ScreenIndex",
                str(screen_index),
            ],
            "requires_explicit_approval": True,
            "approval": approval,
            "synthetic_safe_idle_only": True,
            "bounded_duration_seconds": duration_seconds,
            "view_profile": view_profile,
            "screen_index": screen_index,
            "live_status_binding": False,
            "overlay_is_authority": False,
            "session_start": False,
            "mode_change": False,
            "quick_stop_execution": False,
            "emergency_stop_execution": False,
            "game_process_enumeration": False,
            "window_capture": False,
            "audio_capture": False,
            "input_telemetry": False,
            "input_read": False,
            "input_hook": False,
            "input_injection": False,
            "raw_media_rendering": False,
            "network_listener": False,
        }

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsNativeOverlayAdapter",
            "enabled": self.enabled,
            "active": self._active,
            "helper_present": self.helper_path().is_file(),
            "safe_idle_preview_available": self.enabled,
            "synthetic_safe_idle_only": True,
            "bounded_preview": True,
            "live_status_binding": False,
            "overlay_is_authority": False,
            "session_start": False,
            "mode_change": False,
            "quick_stop_execution": False,
            "emergency_stop_execution": False,
            "game_process_enumeration": False,
            "capture": False,
            "input_read": False,
            "input_hook": False,
            "input_injection": False,
            "network_listener": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "inspect_launch_spec": self.build_inspect_launch_spec(),
            "preview_contract": {
                "exact_approval": self.SAFE_IDLE_PREVIEW_APPROVAL,
                "view_profiles": list(self.manager.VIEW_PROFILES),
                "minimum_duration_seconds": 1,
                "maximum_duration_seconds": 15,
                "synthetic_safe_idle_only": True,
                "no_live_status_binding": True,
                "no_session_control": True,
                "no_input": True,
                "no_network_listener": True,
            },
        }
