"""Guarded ORION adapter contract for Sprint 285."""

from __future__ import annotations

import hashlib
import os
import platform
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .aura_game_input_telemetry_runtime_manager import (
    AuraGameInputTelemetryRuntimeManager,
    GameInputTelemetryRuntimeError,
)


class AuraWindowsGameInputTelemetryAdapter:
    """One bounded foreground-only sample through an injected runner."""

    def __init__(
        self,
        *,
        manager: AuraGameInputTelemetryRuntimeManager,
        telemetry_root: Path | str,
        enabled: bool = False,
        telemetry_runner: (
            Callable[
                [Mapping[str, Any]],
                Sequence[Mapping[str, Any]],
            ]
            | None
        ) = None,
    ) -> None:
        self.manager = manager
        self.telemetry_root = Path(
            telemetry_root
        ).expanduser().resolve()
        self.enabled = bool(enabled)
        self.telemetry_runner = telemetry_runner
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise GameInputTelemetryRuntimeError(message)

    def _output_path(self, request_id: str) -> Path:
        self.telemetry_root.mkdir(parents=True, exist_ok=True)
        self._guard(
            not self.telemetry_root.is_symlink(),
            "Telemetry root must not be a symlink.",
        )
        path = (
            self.telemetry_root / f"{request_id}.jsonl"
        ).resolve()
        try:
            path.relative_to(self.telemetry_root)
        except ValueError as exc:
            raise GameInputTelemetryRuntimeError(
                "Telemetry output escaped root."
            ) from exc
        self._guard(
            not path.exists(),
            "Telemetry output already exists.",
        )
        return path

    def build_powershell_contract(
        self,
        request: Mapping[str, Any],
        output_path: Path | str,
    ) -> str:
        validated = self.manager.validate_input_request(
            request,
            require_permission_unused=False,
        )
        output = Path(output_path).expanduser().resolve()
        escaped = str(output).replace("'", "''")
        return f"""# AURA Sprint 285 foreground-only polling contract
# A separately reviewed helper is required.
# It MUST bind GetForegroundWindow and GetWindowThreadProcessId to PID
# {validated['process_id']} and osu!.exe for every poll.
# It MAY call GetAsyncKeyState only for Z, X, left mouse, and right mouse.
# It MAY call GetCursorPos plus ScreenToClient only to emit normalized
# coordinates inside the bound osu! client area.
# It MUST fail closed on focus loss.
# It MUST NOT enumerate arbitrary keys, log text, read the clipboard,
# install SetWindowsHookEx hooks, call RegisterRawInputDevices,
# call SendInput, or capture background input.
$ErrorActionPreference = 'Stop'
$expectedProcessId = {validated['process_id']}
$expectedExecutable = 'osu!.exe'
$outputPath = '{escaped}'
$durationMilliseconds = 5000
$pollIntervalMilliseconds = 17
$maximumEvents = 512
$maximumBytes = 131072
throw 'foreground_input_telemetry_helper_required_fail_closed'
"""

    def capture_once(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._guard(
            self.enabled,
            "Game-input telemetry adapter is disabled.",
        )
        self._guard(
            not self._active,
            "Game-input telemetry capture is already active.",
        )
        self._guard(
            self.telemetry_runner is not None,
            "Explicit foreground telemetry runner is required.",
        )
        validated = self.manager.validate_input_request(
            request,
            require_permission_unused=False,
        )
        output = self._output_path(validated["request_id"])
        self._active = True
        try:
            events = self.telemetry_runner(validated)
            self._guard(
                not isinstance(events, (str, bytes, bytearray)),
                "Telemetry runner must return sanitized event mappings.",
            )
            encoded = self.manager.serialize_events(events)
            metadata = self.manager.parse_telemetry_metadata(
                encoded
            )
            with output.open("xb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            receipt = self.manager.build_input_receipt(
                request=validated,
                telemetry_sample_succeeded=True,
                artifact_metadata=metadata,
            )
            return {
                "receipt": receipt,
                "local_artifact_path": str(output),
                "backend": {
                    "observation_method": (
                        "foreground_gated_allowlisted_polling"
                    ),
                    "foreground_required_for_every_sample": True,
                    "fail_closed_on_focus_loss": True,
                    "arbitrary_key_capture": False,
                    "text_or_character_logging": False,
                    "background_input_capture": False,
                    "input_hook_installed": False,
                    "raw_input_registered": False,
                    "input_injection_executed": False,
                    "raw_events_exported": False,
                    "local_path_exported_to_atlas": False,
                },
            }
        except Exception:
            if output.exists():
                try:
                    output.unlink()
                except OSError:
                    pass
            raise
        finally:
            self._active = False

    def cleanup_once(
        self,
        *,
        receipt: Mapping[str, Any],
        local_artifact_path: Path | str,
        confirmation: str,
    ) -> dict[str, Any]:
        self._guard(
            confirmation == self.manager.CLEANUP_TEXT,
            "Exact telemetry cleanup confirmation is required.",
        )
        validated = self.manager.validate_input_receipt(
            receipt
        )
        path = Path(local_artifact_path).expanduser().resolve()
        try:
            path.relative_to(self.telemetry_root)
        except ValueError as exc:
            raise GameInputTelemetryRuntimeError(
                "Cleanup path escaped telemetry root."
            ) from exc
        self._guard(
            path.is_file() and not path.is_symlink(),
            "Cleanup target is not a regular telemetry artifact.",
        )
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self._guard(
            digest == validated["artifact"]["sha256"],
            "Cleanup telemetry artifact digest mismatch.",
        )
        path.unlink()
        return self.manager.build_cleanup_receipt(
            request_id=validated["request_id"],
            artifact_id=validated["artifact"]["artifact_id"],
            artifact_sha256=validated["artifact"]["sha256"],
            deleted=not path.exists(),
        )

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsGameInputTelemetryAdapter",
            "enabled": self.enabled,
            "capture_active": self._active,
            "platform": platform.system(),
            "telemetry_root": str(self.telemetry_root),
            "telemetry_runner_injected": (
                self.telemetry_runner is not None
            ),
            "foreground_only": True,
            "semantic_allowlist_only": True,
            "normalized_client_area_coordinates_only": True,
            "arbitrary_key_capture": False,
            "text_or_character_logging": False,
            "background_input_capture": False,
            "input_hook": False,
            "raw_input_registration": False,
            "input_injection": False,
            "controller_read": False,
            "continuous_monitoring": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "foreground_polling_contract": {
                "required_exports": [
                    "GetForegroundWindow",
                    "GetWindowThreadProcessId",
                    "IsWindow",
                    "IsWindowVisible",
                    "GetClientRect",
                    "ScreenToClient",
                    "GetAsyncKeyState",
                    "GetCursorPos",
                ],
                "allowlisted_virtual_keys": [
                    "Z",
                    "X",
                    "VK_LBUTTON",
                    "VK_RBUTTON",
                ],
                "allowlisted_semantic_tokens": list(
                    self.manager.ALLOWED_TOKENS
                ),
                "exact_process_id": True,
                "exact_executable_basename": "osu!.exe",
                "foreground_required_for_every_sample": True,
                "fail_closed_on_focus_loss": True,
                "normalized_client_area_coordinates_only": True,
                "max_duration_seconds": 5,
                "max_relative_milliseconds": 5000,
                "poll_interval_milliseconds": 17,
                "max_events": 512,
                "max_encoded_bytes": 131072,
                "temporary_private_storage": True,
                "missing_helper_behavior": "fail_closed",
                "arbitrary_key_capture": False,
                "text_or_character_logging": False,
                "clipboard_read": False,
                "background_input_capture": False,
                "input_hook": False,
                "raw_input_registration": False,
                "input_injection": False,
            },
        }
