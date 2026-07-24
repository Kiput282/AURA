"""Disabled-by-default ORION adapter for Sprint 289 integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_orion_overlay_session_status_integration_manager import (
    AuraOrionOverlaySessionStatusIntegrationManager,
    OrionOverlaySessionStatusIntegrationError,
)


class AuraOrionOverlaySessionStatusAdapter:
    """Build reviewed helper launch specs without starting a process."""

    LIVE_STATUS_APPROVAL = (
        "APPROVE AURA SPRINT 289 LIVE STATUS OVERLAY"
    )

    def __init__(
        self,
        *,
        manager: AuraOrionOverlaySessionStatusIntegrationManager,
        enabled: bool = False,
    ) -> None:
        self.manager = manager
        self.enabled = bool(enabled)
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise OrionOverlaySessionStatusIntegrationError(message)

    def helper_path(self) -> Path:
        return (
            self.manager.project_root
            / "aura/orion_native_overlay_runtime/orion/"
            "AuraNativeOverlay.ps1"
        )

    def build_live_status_launch_spec(
        self,
        *,
        approval: str,
        status_path: Path | str,
        request_directory: Path | str,
        acknowledgement_directory: Path | str,
        permission_snapshot_sha256: str,
        view_profile: str = "normal",
        screen_index: int = 0,
        duration_seconds: int = 0,
    ) -> dict[str, Any]:
        self._guard(self.enabled, "Integration adapter is disabled.")
        self._guard(
            approval == self.LIVE_STATUS_APPROVAL,
            "Exact live-status approval is required.",
        )
        self._guard(
            view_profile in ("compact", "normal", "expanded"),
            "Unknown view profile.",
        )
        self._guard(
            type(screen_index) is int and 0 <= screen_index <= 15,
            "Screen index must be 0..15.",
        )
        self._guard(
            type(duration_seconds) is int
            and 0 <= duration_seconds <= 3600,
            "Duration must be 0..3600 seconds.",
        )

        permission_digest = self.manager._sha256_hex(
            permission_snapshot_sha256,
            "permission_snapshot_sha256",
        )
        helper = self.helper_path()
        self._guard(helper.is_file(), "Overlay helper is missing.")

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
                "LiveStatus",
                "-Approval",
                approval,
                "-StatusPath",
                str(Path(status_path)),
                "-RequestDirectory",
                str(Path(request_directory)),
                "-AcknowledgementDirectory",
                str(Path(acknowledgement_directory)),
                "-PermissionSnapshotSha256",
                permission_digest,
                "-ViewProfile",
                view_profile,
                "-ScreenIndex",
                str(screen_index),
                "-DurationSeconds",
                str(duration_seconds),
            ],
            "requires_explicit_approval": True,
            "live_status_binding": True,
            "reviewed_quick_stop": True,
            "reviewed_emergency_stop_all": True,
            "overlay_is_authority": False,
            "direct_stop_execution": False,
            "session_start": False,
            "mode_change": False,
            "raw_media_display": False,
            "raw_input_display": False,
            "input_hook": False,
            "input_injection": False,
            "network_listener": False,
        }

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraOrionOverlaySessionStatusAdapter",
            "enabled": self.enabled,
            "active": self._active,
            "helper_present": self.helper_path().is_file(),
            "live_status_binding_available": self.enabled,
            "reviewed_quick_stop_available": self.enabled,
            "reviewed_emergency_stop_all_available": self.enabled,
            "overlay_is_authority": False,
            "direct_stop_execution": False,
            "session_start": False,
            "mode_change": False,
            "raw_media_display": False,
            "raw_input_display": False,
            "input_hook": False,
            "input_injection": False,
            "network_listener": False,
            "safe_idle": True,
        }
