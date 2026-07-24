"""ORION adapter contract for Sprint 286 timestamp synchronization."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .aura_game_timestamp_synchronization_runtime_manager import (
    AuraGameTimestampSynchronizationRuntimeManager,
    GameTimestampSynchronizationRuntimeError,
)


class AuraWindowsGameTimestampSynchronizationAdapter:
    """Disabled-by-default adapter for one bounded logical clock probe."""

    def __init__(
        self,
        *,
        manager: AuraGameTimestampSynchronizationRuntimeManager,
        enabled: bool = False,
        clock_probe_runner: (
            Callable[
                [Mapping[str, Any]],
                Sequence[Mapping[str, Any]],
            ]
            | None
        ) = None,
    ) -> None:
        self.manager = manager
        self.enabled = bool(enabled)
        self.clock_probe_runner = clock_probe_runner
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise GameTimestampSynchronizationRuntimeError(message)

    def build_powershell_contract(
        self,
        request: Mapping[str, Any],
    ) -> str:
        validated = self.manager.validate_clock_request(
            request,
            require_permission_unused=False,
        )
        streams = ",".join(validated["streams"])
        return f"""# AURA Sprint 286 bounded shared-clock contract
# A separately reviewed ORION helper is required.
# It MUST use one [Diagnostics.Stopwatch] monotonic epoch and one explicit
# Stopwatch frequency for all logical stream envelopes.
# UTC is an anchor only and MUST NOT be the sole ordering source.
# It MUST fail closed on monotonic clock discontinuity.
# It MUST NOT call Set-Date, change NTP or Windows Time, capture a window,
# capture audio, read keyboard or mouse input, install hooks, register Raw
# Input, inject input, export raw stream data, or contact ATLAS directly.
$ErrorActionPreference = 'Stop'
$durationMilliseconds = {validated['duration_milliseconds']}
$maximumLogicalSamples = {validated['maximum_logical_samples']}
$streams = '{streams}'
throw 'orion_shared_clock_helper_required_fail_closed'
"""

    def probe_once(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._guard(
            self.enabled,
            "Game timestamp synchronization adapter is disabled.",
        )
        self._guard(
            not self._active,
            "Game timestamp synchronization probe is already active.",
        )
        self._guard(
            self.clock_probe_runner is not None,
            "Explicit bounded clock probe runner is required.",
        )
        validated = self.manager.validate_clock_request(
            request,
            require_permission_unused=False,
        )
        self._active = True
        try:
            envelopes = self.clock_probe_runner(validated)
            self._guard(
                not isinstance(envelopes, (str, bytes, bytearray)),
                "Clock probe runner must return envelope mappings.",
            )
            metadata = self.manager.summarize_envelopes(
                envelopes,
                duration_milliseconds=validated[
                    "duration_milliseconds"
                ],
            )
            receipt = self.manager.build_clock_receipt(
                request=validated,
                metadata=metadata,
                probe_succeeded=True,
            )
            return {
                "receipt": receipt,
                "backend": {
                    "implementation": (
                        "dotnet_stopwatch_shared_session_clock_envelope"
                    ),
                    "shared_session_epoch": True,
                    "explicit_clock_frequency": True,
                    "utc_used_for_anchor_only": True,
                    "atlas_clock_used_for_ordering": False,
                    "clock_discontinuity_fail_closed": True,
                    "raw_monotonic_ticks_exported": False,
                    "raw_stream_exported": False,
                    "window_capture_started": False,
                    "audio_capture_started": False,
                    "input_telemetry_started": False,
                    "keyboard_read": False,
                    "mouse_read": False,
                    "input_hook_installed": False,
                    "raw_input_registered": False,
                    "input_injection_executed": False,
                    "system_clock_changed": False,
                    "ntp_configuration_changed": False,
                    "time_service_changed": False,
                },
            }
        finally:
            self._active = False

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsGameTimestampSynchronizationAdapter",
            "enabled": self.enabled,
            "probe_active": self._active,
            "platform": platform.system(),
            "clock_probe_runner_injected": (
                self.clock_probe_runner is not None
            ),
            "shared_session_epoch": True,
            "explicit_clock_frequency": True,
            "utc_used_for_anchor_only": True,
            "atlas_clock_used_for_ordering": False,
            "system_clock_change": False,
            "ntp_configuration_change": False,
            "time_service_change": False,
            "raw_monotonic_tick_export": False,
            "raw_stream_export": False,
            "window_capture": False,
            "audio_capture": False,
            "input_telemetry": False,
            "keyboard_read": False,
            "mouse_read": False,
            "input_hook": False,
            "raw_input_registration": False,
            "input_injection": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "orion_clock_contract": {
                "required_runtime": ".NET Stopwatch",
                "reference_clock": (
                    "ORION_MONOTONIC_HIGH_RESOLUTION_CLOCK"
                ),
                "utc_anchor_type": (
                    "ORION_UTC_TIMESTAMP_AT_SESSION_EPOCH"
                ),
                "streams": list(self.manager.STREAMS),
                "stream_cadence_milliseconds": dict(
                    self.manager.STREAM_CADENCE_MILLISECONDS
                ),
                "maximum_duration_milliseconds": (
                    self.manager.MAX_DURATION_MILLISECONDS
                ),
                "maximum_logical_samples": (
                    self.manager.MAX_LOGICAL_SAMPLES
                ),
                "clock_discontinuity_behavior": "fail_closed",
                "missing_helper_behavior": "fail_closed",
                "metadata_only_evidence": True,
                "real_capture_started": False,
                "raw_data_read": False,
                "system_clock_change": False,
            },
        }
