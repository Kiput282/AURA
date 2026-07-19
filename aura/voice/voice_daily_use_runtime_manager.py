"""Bounded local STT/TTS runtime for Sprint 271 voice daily use."""

from __future__ import annotations

import io
import json
import os
import re
import subprocess
import tempfile
import threading
import uuid
import wave
from pathlib import Path
from typing import Any


class VoiceDailyUseRuntimeError(RuntimeError):
    """Base error for bounded daily-use voice runtime failures."""


class VoiceDailyUseConfigurationError(VoiceDailyUseRuntimeError):
    """Raised when the isolated voice backend is unavailable."""


class VoiceDailyUseValidationError(VoiceDailyUseRuntimeError):
    """Raised when a bounded voice request is invalid."""


class VoiceDailyUseBusyError(VoiceDailyUseRuntimeError):
    """Raised when another local voice inference is already running."""


class VoiceDailyUseBackendError(VoiceDailyUseRuntimeError):
    """Raised when the isolated STT/TTS worker fails."""


class AuraVoiceDailyUseRuntimeManager:
    """Run explicit local STT/TTS through the isolated ATLAS backend."""

    name = "aura_voice_daily_use_runtime"
    component_version = "0.1.0-alpha"
    sprint = 271

    DEFAULT_VOICE_ROOT = Path("/mnt/aura-data/AURA/voice")
    MAX_AUDIO_BYTES = 2 * 1024 * 1024
    MAX_AUDIO_SECONDS = 15.0
    MAX_TTS_TEXT_CHARACTERS = 600
    MAX_TTS_AUDIO_BYTES = 4 * 1024 * 1024
    MAX_TTS_AUDIO_SECONDS = 45.0
    STT_TIMEOUT_SECONDS = 45.0
    TTS_TIMEOUT_SECONDS = 30.0
    REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,96}$")

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        voice_root: str | Path | None = None,
        worker_path: str | Path | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        self.project_root = Path(project_root).resolve()
        configured_root = voice_root or os.environ.get("AURA_VOICE_ROOT")
        self.voice_root = Path(
            configured_root or self.DEFAULT_VOICE_ROOT
        ).expanduser().resolve()
        self.current_link = self.voice_root / "current"
        self.runtime_root = self.voice_root / "runtime"
        self.worker_path = Path(
            worker_path
            or self.project_root / "aura/voice/voice_backend_worker.py"
        ).resolve()
        self._inference_lock = threading.Lock()

    @staticmethod
    def _safe_request_id(request_id: str | None) -> str:
        value = request_id or f"voice-{uuid.uuid4().hex}"
        if not isinstance(value, str) or not value:
            raise VoiceDailyUseValidationError(
                "Voice request_id must be a non-empty string."
            )
        if not AuraVoiceDailyUseRuntimeManager.REQUEST_ID_RE.fullmatch(value):
            raise VoiceDailyUseValidationError(
                "Voice request_id contains unsupported characters."
            )
        return value

    def _backend_paths(self) -> dict[str, Path]:
        try:
            release = self.current_link.resolve(strict=True)
        except (FileNotFoundError, RuntimeError) as exc:
            raise VoiceDailyUseConfigurationError(
                "The active isolated voice release is unavailable."
            ) from exc

        paths = {
            "release": release,
            "manifest": release / "manifest.json",
            "python": release / "venv/bin/python",
            "stt_model": (
                release / "models/stt/faster-whisper-small"
            ),
            "tts_model": (
                release
                / "models/tts/piper-id_ID-news_tts-medium"
                / "id_ID-news_tts-medium.onnx"
            ),
            "tts_config": (
                release
                / "models/tts/piper-id_ID-news_tts-medium"
                / "id_ID-news_tts-medium.onnx.json"
            ),
            "worker": self.worker_path,
        }
        missing = [
            name for name, path in paths.items()
            if name != "release" and not path.exists()
        ]
        if missing:
            raise VoiceDailyUseConfigurationError(
                "Voice backend artifacts are missing: "
                + ", ".join(sorted(missing))
            )
        if not paths["python"].is_file():
            raise VoiceDailyUseConfigurationError(
                "Voice backend Python executable is invalid."
            )
        try:
            manifest = json.loads(
                paths["manifest"].read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise VoiceDailyUseConfigurationError(
                "Voice backend manifest is invalid."
            ) from exc
        if manifest.get("status") != "ACTIVE_TESTED_RELEASE":
            raise VoiceDailyUseConfigurationError(
                "Voice backend release is not an activated tested release."
            )
        return paths

    def status(self) -> dict[str, Any]:
        try:
            paths = self._backend_paths()
            manifest = json.loads(
                paths["manifest"].read_text(encoding="utf-8")
            )
            ready = True
            reason = "ready"
        except (
            VoiceDailyUseConfigurationError,
            OSError,
            json.JSONDecodeError,
        ) as exc:
            paths = {}
            manifest = {}
            ready = False
            reason = str(exc)

        return {
            "status": "ready" if ready else "degraded",
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "ready": ready,
            "reason": reason,
            "voice_root": str(self.voice_root),
            "active_release": str(paths.get("release", "")),
            "release_id": manifest.get("release_id"),
            "stt_backend": "faster-whisper-small-cpu-int8",
            "tts_backend": "piper-id_ID-news_tts-medium",
            "audio_capture_host": "ORION browser",
            "audio_playback_host": "ORION browser",
            "inference_host": "ATLAS",
            "accepted_audio_content_type": "audio/wav",
            "max_audio_bytes": self.MAX_AUDIO_BYTES,
            "max_audio_seconds": self.MAX_AUDIO_SECONDS,
            "max_tts_text_characters": self.MAX_TTS_TEXT_CHARACTERS,
            "single_flight": True,
            "always_listening": False,
            "wake_word": False,
            "cloud_fallback": False,
            "raw_audio_retention": False,
            "direct_voice_to_action": False,
            "runtime_mutated": False,
        }

    @staticmethod
    def _validate_wav_bytes(audio: bytes) -> dict[str, Any]:
        if not isinstance(audio, bytes) or not audio:
            raise VoiceDailyUseValidationError(
                "Voice audio must be non-empty WAV bytes."
            )
        if len(audio) > AuraVoiceDailyUseRuntimeManager.MAX_AUDIO_BYTES:
            raise VoiceDailyUseValidationError(
                "Voice audio exceeds the bounded request size."
            )
        try:
            with wave.open(io.BytesIO(audio), "rb") as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                frames = wav_file.getnframes()
        except (wave.Error, EOFError) as exc:
            raise VoiceDailyUseValidationError(
                "Voice audio must be a valid PCM WAV file."
            ) from exc

        if channels not in {1, 2}:
            raise VoiceDailyUseValidationError(
                "Voice WAV must contain one or two channels."
            )
        if sample_width != 2:
            raise VoiceDailyUseValidationError(
                "Voice WAV must use signed 16-bit PCM samples."
            )
        if sample_rate < 8000 or sample_rate > 48000:
            raise VoiceDailyUseValidationError(
                "Voice WAV sample rate must be between 8 kHz and 48 kHz."
            )
        if frames <= 0:
            raise VoiceDailyUseValidationError(
                "Voice WAV must contain at least one frame."
            )
        duration = frames / sample_rate
        if duration > AuraVoiceDailyUseRuntimeManager.MAX_AUDIO_SECONDS:
            raise VoiceDailyUseValidationError(
                "Voice WAV exceeds the 15-second push-to-talk limit."
            )
        return {
            "channels": channels,
            "sample_width": sample_width,
            "sample_rate": sample_rate,
            "frames": frames,
            "duration_seconds": round(duration, 6),
            "size_bytes": len(audio),
        }

    def _run_worker(
        self,
        command: list[str],
        *,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        paths = self._backend_paths()
        environment = {
            **os.environ,
            "PYTHONNOUSERSITE": "1",
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "NO_PROXY": "*",
            "no_proxy": "*",
        }
        try:
            result = subprocess.run(
                [
                    str(paths["python"]),
                    str(paths["worker"]),
                    *command,
                ],
                cwd=self.project_root,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise VoiceDailyUseBackendError(
                "Voice backend inference timed out."
            ) from exc
        except OSError as exc:
            raise VoiceDailyUseBackendError(
                "Voice backend worker could not be started."
            ) from exc

        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise VoiceDailyUseBackendError(
                "Voice backend worker failed: " + detail[-1000:]
            )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise VoiceDailyUseBackendError(
                "Voice backend returned an invalid response."
            ) from exc
        if not isinstance(payload, dict) or payload.get("status") != "ok":
            raise VoiceDailyUseBackendError(
                "Voice backend returned a non-success response."
            )
        return payload

    def transcribe_wav_bytes(
        self,
        audio: bytes,
        *,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        request_id = self._safe_request_id(request_id)
        wav_metadata = self._validate_wav_bytes(audio)
        if not self._inference_lock.acquire(blocking=False):
            raise VoiceDailyUseBusyError(
                "Another local voice inference is already running."
            )
        try:
            self.runtime_root.mkdir(parents=True, exist_ok=True, mode=0o700)
            os.chmod(self.runtime_root, 0o700)
            with tempfile.TemporaryDirectory(
                prefix="stt-",
                dir=self.runtime_root,
            ) as temporary_dir:
                input_path = Path(temporary_dir) / "input.wav"
                input_path.write_bytes(audio)
                paths = self._backend_paths()
                result = self._run_worker(
                    [
                        "transcribe",
                        "--input",
                        str(input_path),
                        "--model-dir",
                        str(paths["stt_model"]),
                        "--language",
                        "id",
                        "--cpu-threads",
                        "6",
                    ],
                    timeout_seconds=self.STT_TIMEOUT_SECONDS,
                )
            transcript = str(result.get("transcript", "")).strip()
            if not transcript:
                raise VoiceDailyUseValidationError(
                    "No speech transcript was detected."
                )
            return {
                "status": "ok",
                "request_id": request_id,
                "transcript": transcript,
                "language": result.get("language", "id"),
                "language_probability": result.get(
                    "language_probability"
                ),
                "segment_count": result.get("segment_count", 0),
                "elapsed_seconds": result.get("elapsed_seconds"),
                "input_wav": wav_metadata,
                "raw_audio_retained": False,
                "chat_handoff_performed": False,
                "direct_action_dispatch": False,
            }
        finally:
            self._inference_lock.release()

    def synthesize_wav(
        self,
        text: str,
        *,
        request_id: str | None = None,
    ) -> tuple[bytes, dict[str, Any]]:
        request_id = self._safe_request_id(request_id)
        if not isinstance(text, str):
            raise VoiceDailyUseValidationError(
                "TTS text must be a string."
            )
        normalized = " ".join(text.split())
        if not normalized:
            raise VoiceDailyUseValidationError(
                "TTS text must not be empty."
            )
        if len(normalized) > self.MAX_TTS_TEXT_CHARACTERS:
            raise VoiceDailyUseValidationError(
                "TTS text exceeds the bounded character limit."
            )
        if not self._inference_lock.acquire(blocking=False):
            raise VoiceDailyUseBusyError(
                "Another local voice inference is already running."
            )
        try:
            self.runtime_root.mkdir(parents=True, exist_ok=True, mode=0o700)
            os.chmod(self.runtime_root, 0o700)
            with tempfile.TemporaryDirectory(
                prefix="tts-",
                dir=self.runtime_root,
            ) as temporary_dir:
                temporary = Path(temporary_dir)
                text_path = temporary / "input.txt"
                output_path = temporary / "output.wav"
                text_path.write_text(normalized, encoding="utf-8")
                paths = self._backend_paths()
                result = self._run_worker(
                    [
                        "synthesize",
                        "--text-file",
                        str(text_path),
                        "--output",
                        str(output_path),
                        "--model",
                        str(paths["tts_model"]),
                        "--config",
                        str(paths["tts_config"]),
                    ],
                    timeout_seconds=self.TTS_TIMEOUT_SECONDS,
                )
                audio = output_path.read_bytes()
                metadata = self._validate_synthesized_wav(audio)
            return audio, {
                "status": "ok",
                "request_id": request_id,
                "elapsed_seconds": result.get("elapsed_seconds"),
                "wav": metadata,
                "audio_retained": False,
                "speaker_playback_performed": False,
                "direct_action_dispatch": False,
            }
        finally:
            self._inference_lock.release()

    @classmethod
    def _validate_synthesized_wav(cls, audio: bytes) -> dict[str, Any]:
        if not audio or len(audio) > cls.MAX_TTS_AUDIO_BYTES:
            raise VoiceDailyUseBackendError(
                "TTS backend returned an invalid bounded WAV size."
            )
        try:
            with wave.open(io.BytesIO(audio), "rb") as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                frames = wav_file.getnframes()
        except (wave.Error, EOFError) as exc:
            raise VoiceDailyUseBackendError(
                "TTS backend returned an invalid WAV file."
            ) from exc
        duration = frames / sample_rate if sample_rate else 0.0
        if frames <= 0 or duration > cls.MAX_TTS_AUDIO_SECONDS:
            raise VoiceDailyUseBackendError(
                "TTS backend returned an invalid audio duration."
            )
        return {
            "channels": channels,
            "sample_width": sample_width,
            "sample_rate": sample_rate,
            "frames": frames,
            "duration_seconds": round(duration, 6),
            "size_bytes": len(audio),
        }
