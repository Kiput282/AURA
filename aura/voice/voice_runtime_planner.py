import importlib.util
import os
import platform
import shutil
from pathlib import Path
from typing import Any

from aura.permissions.permission_manager import PermissionManager


class VoiceRuntimePlanner:
    """
    Voice Runtime Planning for AURA.

    Current phase:
    - plan STT/TTS runtime candidates
    - check passive dependency availability
    - map permissions and confirmation requirements
    - never access microphone or speaker
    """

    name = "voice_runtime_planning"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.permission_manager = PermissionManager()

    def stt_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "faster-whisper",
                "type": "speech_to_text",
                "status": "candidate",
                "local_first": True,
                "offline_capable": True,
                "description": "Local Whisper-based speech recognition using CPU or GPU.",
                "notes": "Good default candidate for local STT on ATLAS.",
            },
            {
                "name": "whisper.cpp",
                "type": "speech_to_text",
                "status": "candidate",
                "local_first": True,
                "offline_capable": True,
                "description": "Lightweight native Whisper runtime.",
                "notes": "Good for efficient local inference and small models.",
            },
            {
                "name": "vosk",
                "type": "speech_to_text",
                "status": "candidate",
                "local_first": True,
                "offline_capable": True,
                "description": "Offline lightweight speech recognition.",
                "notes": "Useful fallback for low-resource STT.",
            },
        ]

    def tts_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "piper",
                "type": "text_to_speech",
                "status": "candidate",
                "local_first": True,
                "offline_capable": True,
                "description": "Fast local neural text-to-speech.",
                "notes": "Good default candidate for local TTS.",
            },
            {
                "name": "coqui-tts",
                "type": "text_to_speech",
                "status": "candidate",
                "local_first": True,
                "offline_capable": True,
                "description": "Neural local TTS framework.",
                "notes": "Flexible but heavier than Piper.",
            },
            {
                "name": "espeak-ng",
                "type": "text_to_speech",
                "status": "fallback",
                "local_first": True,
                "offline_capable": True,
                "description": "Lightweight classic TTS engine.",
                "notes": "Good fallback for simple voice output testing.",
            },
        ]

    def dependency_check(self) -> dict[str, Any]:
        python_packages = [
            {
                "name": "sounddevice",
                "purpose": "microphone input and speaker output bridge",
                "installed": importlib.util.find_spec("sounddevice") is not None,
            },
            {
                "name": "numpy",
                "purpose": "audio buffer processing",
                "installed": importlib.util.find_spec("numpy") is not None,
            },
            {
                "name": "faster_whisper",
                "purpose": "candidate local STT runtime",
                "installed": importlib.util.find_spec("faster_whisper") is not None,
            },
            {
                "name": "vosk",
                "purpose": "candidate offline STT runtime",
                "installed": importlib.util.find_spec("vosk") is not None,
            },
        ]

        executables = [
            {
                "name": "ffmpeg",
                "purpose": "audio conversion and media handling",
                "found": shutil.which("ffmpeg") is not None,
            },
            {
                "name": "piper",
                "purpose": "candidate local TTS runtime",
                "found": shutil.which("piper") is not None,
            },
            {
                "name": "espeak-ng",
                "purpose": "fallback local TTS runtime",
                "found": shutil.which("espeak-ng") is not None,
            },
            {
                "name": "espeak",
                "purpose": "fallback local TTS runtime",
                "found": shutil.which("espeak") is not None,
            },
        ]

        return {
            "python_packages": python_packages,
            "executables": executables,
            "environment": {
                "os": platform.system() or "unknown",
                "os_release": platform.release() or "unknown",
                "machine": platform.machine() or "unknown",
                "pulse_server": os.environ.get("PULSE_SERVER") or "",
                "pipewire_runtime": os.environ.get("PIPEWIRE_RUNTIME_DIR") or "",
                "xdg_runtime": os.environ.get("XDG_RUNTIME_DIR") or "",
            },
            "note": "This is a passive check only. No microphone or speaker was accessed.",
        }

    def permission_map(self) -> dict[str, Any]:
        microphone = self.permission_manager.check("microphone_listen")
        speaker = self.permission_manager.check("speaker_speak")

        return {
            "microphone_listen": microphone.to_dict(),
            "speaker_speak": speaker.to_dict(),
        }


    def activation_contract(self) -> dict[str, Any]:
        return {
            "sprint": 191,
            "name": "voice_runtime_activation_foundation",
            "activation_foundation_ready": True,
            "runtime_ready": False,
            "safe_idle_default": True,
            "push_to_talk_required": True,
            "explicit_listen_required": True,
            "always_listening_enabled": False,
            "hidden_capture_enabled": False,
            "background_wake_word_enabled": False,
            "silent_cloud_fallback_enabled": False,
            "direct_voice_to_action_enabled": False,
            "microphone_capture_active": False,
            "speaker_playback_active": False,
            "stt_runtime_active": False,
            "tts_runtime_active": False,
            "audio_file_write_active": False,
            "command_execution_active": False,
            "microphone_permission_action": "microphone_listen",
            "speaker_permission_action": "speaker_speak",
            "chat_session_reuse_required": True,
            "control_center_voice_controls_deferred": True,
            "next_sprint": 192,
            "next_boundary": "push_to_talk_and_explicit_listen_state",
            "guardrails": [
                "No always-listening mode.",
                "No hidden microphone capture.",
                "No background wake word.",
                "No direct voice-to-action execution.",
                "No silent cloud STT or TTS fallback.",
                "Reuse the stable chat/session interaction path.",
            ],
        }

    def status(self) -> dict[str, Any]:
        stt_candidates = self.stt_candidates()
        tts_candidates = self.tts_candidates()
        activation = self.activation_contract()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planning",
            "planning_ready": True,
            "activation_foundation_ready": activation["activation_foundation_ready"],
            "runtime_ready": False,
            "safe_idle_default": activation["safe_idle_default"],
            "push_to_talk_required": activation["push_to_talk_required"],
            "always_listening_enabled": activation["always_listening_enabled"],
            "hidden_capture_enabled": activation["hidden_capture_enabled"],
            "background_wake_word_enabled": activation["background_wake_word_enabled"],
            "silent_cloud_fallback_enabled": activation["silent_cloud_fallback_enabled"],
            "direct_voice_to_action_enabled": activation["direct_voice_to_action_enabled"],
            "chat_session_reuse_required": activation["chat_session_reuse_required"],
            "microphone_access": False,
            "speaker_output": False,
            "stt_runtime_ready": False,
            "tts_runtime_ready": False,
            "stt_candidates": len(stt_candidates),
            "tts_candidates": len(tts_candidates),
            "candidate_count": len(stt_candidates) + len(tts_candidates),
            "permissions": self.permission_map(),
            "activation_contract": activation,
            "note": "Voice runtime activation foundation is ready for explicit push-to-talk planning, but real microphone/STT/TTS/speaker runtime is not enabled yet.",
        }

    def plan(self) -> dict[str, Any]:
        return {
            "recommended_path": {
                "stt": "faster-whisper",
                "tts": "piper",
                "fallback_tts": "espeak-ng",
                "audio_io": "sounddevice",
                "description": "Use local offline STT/TTS first, then connect microphone/speaker only after explicit confirmation.",
            },
            "phases": [
                {
                    "phase": 1,
                    "name": "Runtime package planning",
                    "status": "ready_to_plan",
                    "description": "Choose STT/TTS providers and document dependency requirements.",
                },
                {
                    "phase": 2,
                    "name": "Passive dependency check",
                    "status": "ready",
                    "description": "Check installed packages and executables without accessing audio devices.",
                },
                {
                    "phase": 3,
                    "name": "Audio device discovery",
                    "status": "future",
                    "description": "List microphone/speaker devices only after user approval.",
                },
                {
                    "phase": 4,
                    "name": "STT dry run",
                    "status": "future",
                    "description": "Test speech-to-text with a provided audio file before live microphone input.",
                },
                {
                    "phase": 5,
                    "name": "TTS dry run",
                    "status": "future",
                    "description": "Generate TTS output to a file before speaker playback.",
                },
                {
                    "phase": 6,
                    "name": "Voice loop alpha",
                    "status": "future",
                    "description": "Connect listen-think-speak loop with confirmation and runtime safety flags.",
                },
            ],
            "stt_candidates": self.stt_candidates(),
            "tts_candidates": self.tts_candidates(),
            "permissions": self.permission_map(),
            "safety_rules": [
                "Do not access microphone without explicit user confirmation.",
                "Do not play speaker output without explicit user confirmation.",
                "Prefer dry-run audio files before live audio devices.",
                "Keep all voice runtime actions local-first when possible.",
                "Keep runtime flags false until real STT/TTS is connected and tested.",
            ],
        }

    def check(self) -> dict[str, Any]:
        dependencies = self.dependency_check()
        activation = self.activation_contract()

        installed_python = sum(
            1
            for package in dependencies["python_packages"]
            if package["installed"]
        )

        found_executables = sum(
            1
            for executable in dependencies["executables"]
            if executable["found"]
        )

        assertions = {
            "activation_foundation_ready": activation["activation_foundation_ready"] is True,
            "runtime_not_enabled": activation["runtime_ready"] is False,
            "safe_idle_default": activation["safe_idle_default"] is True,
            "push_to_talk_required": activation["push_to_talk_required"] is True,
            "explicit_listen_required": activation["explicit_listen_required"] is True,
            "always_listening_disabled": activation["always_listening_enabled"] is False,
            "hidden_capture_disabled": activation["hidden_capture_enabled"] is False,
            "background_wake_word_disabled": activation["background_wake_word_enabled"] is False,
            "silent_cloud_fallback_disabled": activation["silent_cloud_fallback_enabled"] is False,
            "direct_voice_to_action_disabled": activation["direct_voice_to_action_enabled"] is False,
            "microphone_capture_inactive": activation["microphone_capture_active"] is False,
            "speaker_playback_inactive": activation["speaker_playback_active"] is False,
            "stt_runtime_inactive": activation["stt_runtime_active"] is False,
            "tts_runtime_inactive": activation["tts_runtime_active"] is False,
            "audio_file_write_inactive": activation["audio_file_write_active"] is False,
            "command_execution_inactive": activation["command_execution_active"] is False,
            "microphone_permission_reuses_existing_action": activation["microphone_permission_action"] == "microphone_listen",
            "speaker_permission_reuses_existing_action": activation["speaker_permission_action"] == "speaker_speak",
            "chat_session_reuse_required": activation["chat_session_reuse_required"] is True,
        }

        failed_assertions = [
            name
            for name, passed in assertions.items()
            if not passed
        ]

        return {
            "status": "checked" if not failed_assertions else "failed",
            "runtime_ready": False,
            "planning_ready": True,
            "activation_foundation_ready": activation["activation_foundation_ready"],
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed_assertions),
            "failed_assertions": failed_assertions,
            "assertions": assertions,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "dependencies": dependencies,
            "activation_contract": activation,
            "note": "Runtime is not enabled yet. This check did not access microphone or speaker.",
        }
