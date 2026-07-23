"""Guarded ORION adapter contract for Sprint 284."""

from __future__ import annotations

import hashlib
import os
import platform
from pathlib import Path
from typing import Any, Callable, Mapping

from .aura_game_audio_capture_runtime_manager import (
    AuraGameAudioCaptureRuntimeManager,
    GameAudioCaptureRuntimeError,
)


class AuraWindowsGameAudioCaptureAdapter:
    """One bounded process-loopback sample through an explicit injected runner."""

    def __init__(self, *, manager: AuraGameAudioCaptureRuntimeManager,
                 audio_root: Path | str, enabled: bool = False,
                 capture_runner: Callable[[Mapping[str, Any]], bytes] | None = None) -> None:
        self.manager = manager
        self.audio_root = Path(audio_root).expanduser().resolve()
        self.enabled = bool(enabled)
        self.capture_runner = capture_runner
        self._active = False

    @staticmethod
    def _guard(condition: bool, message: str) -> None:
        if not condition:
            raise GameAudioCaptureRuntimeError(message)

    def _output_path(self, request_id: str) -> Path:
        self.audio_root.mkdir(parents=True, exist_ok=True)
        self._guard(not self.audio_root.is_symlink(), "Audio root must not be a symlink.")
        path = (self.audio_root / f"{request_id}.wav").resolve()
        try:
            path.relative_to(self.audio_root)
        except ValueError as exc:
            raise GameAudioCaptureRuntimeError("Audio output escaped root.") from exc
        self._guard(not path.exists(), "Audio output already exists.")
        return path

    def build_powershell_contract(self, request: Mapping[str, Any],
                                  output_path: Path | str) -> str:
        validated = self.manager.validate_audio_request(
            request, require_permission_unused=False)
        output = Path(output_path).expanduser().resolve()
        return f"""# AURA Sprint 284 process-loopback contract
# This script intentionally requires a separately reviewed process-loopback
# implementation. It MUST use VAD\\Process_Loopback and
# IncludeTargetProcessTree for PID {validated['process_id']}.
# It MUST NOT enumerate microphones or fall back to whole-system loopback.
$ErrorActionPreference = 'Stop'
$expectedProcessId = {validated['process_id']}
$expectedExecutable = 'osu!.exe'
$outputPath = '{str(output).replace("'", "''")}'
$durationMilliseconds = {validated['duration_seconds'] * 1000}
$sampleRate = 48000
$channelCount = 2
$maximumBytes = 1048576
throw 'process_loopback_helper_required_fail_closed'
"""

    def capture_once(self, request: Mapping[str, Any]) -> dict[str, Any]:
        self._guard(self.enabled, "Game-audio adapter is disabled.")
        self._guard(not self._active, "Game-audio capture is already active.")
        self._guard(self.capture_runner is not None,
                    "Explicit process-loopback capture runner is required.")
        validated = self.manager.validate_audio_request(
            request, require_permission_unused=False)
        output = self._output_path(validated["request_id"])
        self._active = True
        try:
            audio = self.capture_runner(validated)
            self._guard(isinstance(audio, bytes), "Capture runner must return WAV bytes.")
            metadata = self.manager.parse_wav_metadata(audio)
            with output.open("xb") as handle:
                handle.write(audio)
                handle.flush()
                os.fsync(handle.fileno())
            receipt = self.manager.build_audio_receipt(
                request=validated, capture_succeeded=True,
                artifact_metadata=metadata)
            return {
                "receipt": receipt,
                "local_artifact_path": str(output),
                "backend": {
                    "capture_source": "process_loopback_include_target_tree",
                    "microphone_read": False,
                    "whole_system_fallback_used": False,
                    "raw_audio_exported": False,
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

    def cleanup_once(self, *, receipt: Mapping[str, Any],
                     local_artifact_path: Path | str,
                     confirmation: str) -> dict[str, Any]:
        self._guard(confirmation == self.manager.CLEANUP_TEXT,
                    "Exact cleanup confirmation is required.")
        validated = self.manager.validate_audio_receipt(receipt)
        path = Path(local_artifact_path).expanduser().resolve()
        try:
            path.relative_to(self.audio_root)
        except ValueError as exc:
            raise GameAudioCaptureRuntimeError("Cleanup path escaped audio root.") from exc
        self._guard(path.is_file() and not path.is_symlink(),
                    "Cleanup target is not a regular artifact.")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self._guard(digest == validated["artifact"]["sha256"],
                    "Cleanup artifact digest mismatch.")
        path.unlink()
        return self.manager.build_cleanup_receipt(
            request_id=validated["request_id"],
            artifact_id=validated["artifact"]["artifact_id"],
            artifact_sha256=validated["artifact"]["sha256"],
            deleted=not path.exists())

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsGameAudioCaptureAdapter",
            "enabled": self.enabled, "capture_active": self._active,
            "platform": platform.system(), "audio_root": str(self.audio_root),
            "capture_runner_injected": self.capture_runner is not None,
            "process_loopback_only": True,
            "include_target_process_tree": True,
            "microphone_capture": False,
            "whole_system_fallback": False,
            "continuous_capture": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "process_loopback_contract": {
                "virtual_device": r"VAD\Process_Loopback",
                "include_target_process_tree": True,
                "exact_process_id": True,
                "exact_executable_basename": "osu!.exe",
                "microphone_enumeration": False,
                "whole_system_fallback": False,
                "output_format": "wav_pcm_s16le",
                "max_duration_seconds": 5,
                "max_encoded_bytes": 1048576,
                "temporary_private_storage": True,
                "missing_helper_behavior": "fail_closed",
            },
        }
