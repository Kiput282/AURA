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


    def listen_state_contract(self) -> dict[str, Any]:
        allowed_states = [
            "idle",
            "listen_requested",
            "permission_required",
            "listen_ready",
            "listening_explicit",
            "listen_stopping",
            "listen_stopped",
            "listen_denied",
            "listen_error",
        ]

        transitions = {
            "idle": ["listen_requested"],
            "listen_requested": ["permission_required", "listen_ready", "listen_denied"],
            "permission_required": ["listen_ready", "listen_denied"],
            "listen_ready": ["listening_explicit", "listen_stopped"],
            "listening_explicit": ["listen_stopping", "listen_error"],
            "listen_stopping": ["listen_stopped", "listen_error"],
            "listen_stopped": ["idle"],
            "listen_denied": ["idle"],
            "listen_error": ["idle"],
        }

        return {
            "sprint": 192,
            "name": "push_to_talk_explicit_listen_state",
            "listen_state_foundation_ready": True,
            "default_state": "idle",
            "current_state": "idle",
            "allowed_states": allowed_states,
            "transition_map": transitions,
            "push_to_talk_required": True,
            "explicit_listen_required": True,
            "explicit_stop_required": True,
            "permission_required_before_listening": True,
            "microphone_permission_action": "microphone_listen",
            "microphone_capture_active": False,
            "audio_buffer_active": False,
            "stt_runtime_active": False,
            "listen_loop_active": False,
            "background_listener_active": False,
            "wake_word_active": False,
            "always_listening_enabled": False,
            "hidden_capture_enabled": False,
            "silent_cloud_fallback_enabled": False,
            "direct_voice_to_action_enabled": False,
            "state_persistence_runtime": False,
            "state_mutation_runtime": False,
            "audio_device_access": False,
            "command_execution_active": False,
            "next_sprint": 193,
            "next_boundary": "local_microphone_capture_boundary",
            "guardrails": [
                "Default listen state is idle.",
                "Listening can only begin from explicit push-to-talk request.",
                "Microphone permission is required before any future live listening.",
                "No microphone capture is performed in Sprint 192.",
                "No audio buffer, STT runtime, wake word, or background listener is active.",
                "No direct voice-to-action execution is allowed.",
            ],
        }


    def microphone_capture_boundary_contract(self) -> dict[str, Any]:
        dependency_check = self.dependency_check()
        sounddevice_available = any(
            package["name"] == "sounddevice" and package["installed"]
            for package in dependency_check["python_packages"]
        )

        return {
            "sprint": 193,
            "name": "local_microphone_capture_boundary",
            "microphone_boundary_ready": True,
            "microphone_capture_runtime_ready": False,
            "microphone_capture_active": False,
            "microphone_permission_action": "microphone_listen",
            "permission_required_before_capture": True,
            "explicit_listen_state_required_before_capture": True,
            "required_listen_state_before_capture": "listening_explicit",
            "push_to_talk_required_before_capture": True,
            "audio_device_access": False,
            "audio_device_discovery_active": False,
            "device_enumeration_performed": False,
            "sounddevice_available": sounddevice_available,
            "sounddevice_runtime_imported": False,
            "recording_enabled": False,
            "recording_active": False,
            "audio_buffer_active": False,
            "audio_file_write_active": False,
            "audio_persistence_enabled": False,
            "audio_transmission_enabled": False,
            "stt_runtime_active": False,
            "transcription_active": False,
            "listen_loop_active": False,
            "background_listener_active": False,
            "wake_word_active": False,
            "always_listening_enabled": False,
            "hidden_capture_enabled": False,
            "silent_cloud_fallback_enabled": False,
            "direct_voice_to_action_enabled": False,
            "command_execution_active": False,
            "speaker_playback_active": False,
            "capture_scope": "boundary_contract_only",
            "retention_policy": "no_audio_retention_in_sprint_193",
            "next_sprint": 194,
            "next_boundary": "speech_to_text_adapter_runtime",
            "guardrails": [
                "No microphone capture is performed in Sprint 193.",
                "No audio device discovery is performed in Sprint 193.",
                "No audio buffer, recording, or audio file write is active.",
                "No STT or transcription runtime is active.",
                "Future capture requires explicit listen state and microphone permission.",
                "No always-listening, hidden capture, wake word, or background listener is active.",
            ],
        }


    def speech_to_text_adapter_runtime_contract(self) -> dict[str, Any]:
        dependency_check = self.dependency_check()
        python_packages = {
            package["name"]: package["installed"]
            for package in dependency_check["python_packages"]
        }
        executables = {
            executable["name"]: executable["found"]
            for executable in dependency_check["executables"]
        }
        candidates = self.stt_candidates()

        return {
            "sprint": 194,
            "name": "speech_to_text_adapter_runtime",
            "stt_adapter_contract_ready": True,
            "stt_adapter_runtime_ready": False,
            "default_adapter": "faster-whisper",
            "candidate_adapters": [candidate["name"] for candidate in candidates],
            "candidate_adapter_count": len(candidates),
            "local_first_required": True,
            "offline_first_required": True,
            "audio_file_input_boundary_ready": True,
            "provided_audio_file_required_for_future_dry_run": True,
            "audio_file_transcription_runtime_ready": False,
            "audio_file_read_active": False,
            "audio_file_write_active": False,
            "microphone_capture_required_for_adapter_contract": False,
            "live_microphone_transcription_active": False,
            "microphone_capture_active": False,
            "audio_device_access": False,
            "audio_device_discovery_active": False,
            "recording_active": False,
            "audio_buffer_active": False,
            "audio_persistence_enabled": False,
            "audio_transmission_enabled": False,
            "stt_runtime_active": False,
            "transcription_active": False,
            "transcript_persistence_enabled": False,
            "transcript_to_chat_handoff_enabled": False,
            "transcript_to_action_enabled": False,
            "command_execution_active": False,
            "model_download_required": False,
            "model_download_performed": False,
            "dependency_install_performed": False,
            "cloud_stt_fallback_enabled": False,
            "silent_cloud_fallback_enabled": False,
            "remote_provider_enabled": False,
            "permission_required_before_transcription": True,
            "microphone_permission_action": "microphone_listen",
            "faster_whisper_available": python_packages.get("faster_whisper", False),
            "vosk_available": python_packages.get("vosk", False),
            "ffmpeg_available": executables.get("ffmpeg", False),
            "runtime_scope": "adapter_contract_only",
            "next_sprint": 195,
            "next_boundary": "voice_intent_and_chat_integration",
            "guardrails": [
                "No STT runtime is executed in Sprint 194.",
                "No audio file is read or written in Sprint 194.",
                "No live microphone transcription is active.",
                "No model download or dependency installation is performed.",
                "No cloud STT or silent fallback is enabled.",
                "Transcripts cannot trigger chat handoff or actions in Sprint 194.",
            ],
        }

    def status(self) -> dict[str, Any]:
        stt_candidates = self.stt_candidates()
        tts_candidates = self.tts_candidates()
        activation = self.activation_contract()
        listen_state = self.listen_state_contract()
        microphone_boundary = self.microphone_capture_boundary_contract()
        stt_adapter = self.speech_to_text_adapter_runtime_contract()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planning",
            "planning_ready": True,
            "activation_foundation_ready": activation["activation_foundation_ready"],
            "listen_state_foundation_ready": listen_state["listen_state_foundation_ready"],
            "default_listen_state": listen_state["default_state"],
            "current_listen_state": listen_state["current_state"],
            "allowed_listen_states": len(listen_state["allowed_states"]),
            "microphone_boundary_ready": microphone_boundary["microphone_boundary_ready"],
            "microphone_capture_runtime_ready": microphone_boundary["microphone_capture_runtime_ready"],
            "microphone_capture_active": microphone_boundary["microphone_capture_active"],
            "audio_device_access": microphone_boundary["audio_device_access"],
            "audio_device_discovery_active": microphone_boundary["audio_device_discovery_active"],
            "recording_active": microphone_boundary["recording_active"],
            "audio_buffer_active": microphone_boundary["audio_buffer_active"],
            "stt_adapter_contract_ready": stt_adapter["stt_adapter_contract_ready"],
            "stt_adapter_runtime_ready": stt_adapter["stt_adapter_runtime_ready"],
            "stt_default_adapter": stt_adapter["default_adapter"],
            "stt_adapter_candidates": stt_adapter["candidate_adapter_count"],
            "audio_file_transcription_runtime_ready": stt_adapter["audio_file_transcription_runtime_ready"],
            "live_microphone_transcription_active": stt_adapter["live_microphone_transcription_active"],
            "transcription_active": stt_adapter["transcription_active"],
            "cloud_stt_fallback_enabled": stt_adapter["cloud_stt_fallback_enabled"],
            "transcript_to_action_enabled": stt_adapter["transcript_to_action_enabled"],
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
            "listen_state_contract": listen_state,
            "microphone_capture_boundary_contract": microphone_boundary,
            "speech_to_text_adapter_runtime_contract": stt_adapter,
            "note": "Voice speech-to-text adapter contract is ready, but real STT execution, audio file transcription, live microphone transcription, cloud fallback, and transcript actions are not enabled yet.",
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
        listen_state = self.listen_state_contract()
        microphone_boundary = self.microphone_capture_boundary_contract()
        stt_adapter = self.speech_to_text_adapter_runtime_contract()

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
            "listen_state_foundation_ready": listen_state["listen_state_foundation_ready"] is True,
            "default_listen_state_idle": listen_state["default_state"] == "idle",
            "current_listen_state_idle": listen_state["current_state"] == "idle",
            "push_to_talk_still_required_for_listen": listen_state["push_to_talk_required"] is True,
            "explicit_listen_still_required": listen_state["explicit_listen_required"] is True,
            "explicit_stop_required": listen_state["explicit_stop_required"] is True,
            "microphone_permission_required_before_listening": listen_state["permission_required_before_listening"] is True,
            "listen_microphone_permission_reuses_existing_action": listen_state["microphone_permission_action"] == "microphone_listen",
            "listen_microphone_capture_inactive": listen_state["microphone_capture_active"] is False,
            "listen_audio_buffer_inactive": listen_state["audio_buffer_active"] is False,
            "listen_stt_runtime_inactive": listen_state["stt_runtime_active"] is False,
            "listen_loop_inactive": listen_state["listen_loop_active"] is False,
            "background_listener_inactive": listen_state["background_listener_active"] is False,
            "wake_word_inactive": listen_state["wake_word_active"] is False,
            "listen_state_persistence_disabled": listen_state["state_persistence_runtime"] is False,
            "listen_state_mutation_runtime_disabled": listen_state["state_mutation_runtime"] is False,
            "audio_device_access_disabled": listen_state["audio_device_access"] is False,
            "microphone_boundary_ready": microphone_boundary["microphone_boundary_ready"] is True,
            "microphone_capture_runtime_not_ready": microphone_boundary["microphone_capture_runtime_ready"] is False,
            "permission_required_before_capture": microphone_boundary["permission_required_before_capture"] is True,
            "explicit_listen_state_required_before_capture": microphone_boundary["explicit_listen_state_required_before_capture"] is True,
            "required_capture_state_is_listening_explicit": microphone_boundary["required_listen_state_before_capture"] == "listening_explicit",
            "push_to_talk_required_before_capture": microphone_boundary["push_to_talk_required_before_capture"] is True,
            "capture_microphone_permission_reuses_existing_action": microphone_boundary["microphone_permission_action"] == "microphone_listen",
            "capture_audio_device_access_disabled": microphone_boundary["audio_device_access"] is False,
            "capture_audio_device_discovery_inactive": microphone_boundary["audio_device_discovery_active"] is False,
            "device_enumeration_not_performed": microphone_boundary["device_enumeration_performed"] is False,
            "microphone_capture_inactive_for_boundary": microphone_boundary["microphone_capture_active"] is False,
            "sounddevice_runtime_not_imported": microphone_boundary["sounddevice_runtime_imported"] is False,
            "recording_disabled_for_boundary": microphone_boundary["recording_enabled"] is False,
            "recording_inactive_for_boundary": microphone_boundary["recording_active"] is False,
            "audio_buffer_inactive_for_capture": microphone_boundary["audio_buffer_active"] is False,
            "audio_file_write_inactive_for_capture": microphone_boundary["audio_file_write_active"] is False,
            "audio_persistence_disabled_for_capture": microphone_boundary["audio_persistence_enabled"] is False,
            "audio_transmission_disabled_for_capture": microphone_boundary["audio_transmission_enabled"] is False,
            "stt_runtime_inactive_for_capture": microphone_boundary["stt_runtime_active"] is False,
            "transcription_inactive_for_capture": microphone_boundary["transcription_active"] is False,
            "listen_loop_inactive_for_capture": microphone_boundary["listen_loop_active"] is False,
            "background_listener_inactive_for_capture": microphone_boundary["background_listener_active"] is False,
            "wake_word_inactive_for_capture": microphone_boundary["wake_word_active"] is False,
            "always_listening_disabled_for_capture": microphone_boundary["always_listening_enabled"] is False,
            "hidden_capture_disabled_for_capture": microphone_boundary["hidden_capture_enabled"] is False,
            "silent_cloud_fallback_disabled_for_capture": microphone_boundary["silent_cloud_fallback_enabled"] is False,
            "direct_voice_to_action_disabled_for_capture": microphone_boundary["direct_voice_to_action_enabled"] is False,
            "command_execution_inactive_for_capture": microphone_boundary["command_execution_active"] is False,
            "stt_adapter_contract_ready": stt_adapter["stt_adapter_contract_ready"] is True,
            "stt_adapter_runtime_not_ready": stt_adapter["stt_adapter_runtime_ready"] is False,
            "stt_default_adapter_is_faster_whisper": stt_adapter["default_adapter"] == "faster-whisper",
            "stt_candidate_adapter_count_matches": stt_adapter["candidate_adapter_count"] == len(self.stt_candidates()),
            "stt_local_first_required": stt_adapter["local_first_required"] is True,
            "stt_offline_first_required": stt_adapter["offline_first_required"] is True,
            "audio_file_input_boundary_ready": stt_adapter["audio_file_input_boundary_ready"] is True,
            "future_audio_file_required_for_stt_dry_run": stt_adapter["provided_audio_file_required_for_future_dry_run"] is True,
            "audio_file_transcription_runtime_not_ready": stt_adapter["audio_file_transcription_runtime_ready"] is False,
            "stt_audio_file_read_inactive": stt_adapter["audio_file_read_active"] is False,
            "stt_audio_file_write_inactive": stt_adapter["audio_file_write_active"] is False,
            "microphone_capture_not_required_for_stt_adapter_contract": stt_adapter["microphone_capture_required_for_adapter_contract"] is False,
            "live_microphone_transcription_inactive": stt_adapter["live_microphone_transcription_active"] is False,
            "stt_microphone_capture_inactive": stt_adapter["microphone_capture_active"] is False,
            "stt_audio_device_access_disabled": stt_adapter["audio_device_access"] is False,
            "stt_audio_device_discovery_inactive": stt_adapter["audio_device_discovery_active"] is False,
            "stt_recording_inactive": stt_adapter["recording_active"] is False,
            "stt_audio_buffer_inactive": stt_adapter["audio_buffer_active"] is False,
            "stt_audio_persistence_disabled": stt_adapter["audio_persistence_enabled"] is False,
            "stt_audio_transmission_disabled": stt_adapter["audio_transmission_enabled"] is False,
            "stt_runtime_inactive_for_adapter": stt_adapter["stt_runtime_active"] is False,
            "transcription_inactive_for_stt_adapter": stt_adapter["transcription_active"] is False,
            "transcript_persistence_disabled": stt_adapter["transcript_persistence_enabled"] is False,
            "transcript_to_chat_handoff_disabled": stt_adapter["transcript_to_chat_handoff_enabled"] is False,
            "transcript_to_action_disabled": stt_adapter["transcript_to_action_enabled"] is False,
            "stt_command_execution_inactive": stt_adapter["command_execution_active"] is False,
            "stt_model_download_not_required": stt_adapter["model_download_required"] is False,
            "stt_model_download_not_performed": stt_adapter["model_download_performed"] is False,
            "stt_dependency_install_not_performed": stt_adapter["dependency_install_performed"] is False,
            "cloud_stt_fallback_disabled": stt_adapter["cloud_stt_fallback_enabled"] is False,
            "silent_cloud_stt_fallback_disabled": stt_adapter["silent_cloud_fallback_enabled"] is False,
            "remote_stt_provider_disabled": stt_adapter["remote_provider_enabled"] is False,
            "permission_required_before_transcription": stt_adapter["permission_required_before_transcription"] is True,
            "stt_microphone_permission_reuses_existing_action": stt_adapter["microphone_permission_action"] == "microphone_listen",
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
            "listen_state_contract": listen_state,
            "microphone_capture_boundary_contract": microphone_boundary,
            "speech_to_text_adapter_runtime_contract": stt_adapter,
            "note": "Runtime is not enabled yet. This check did not access microphone, speaker, audio devices, audio files, STT models, cloud STT, or transcript actions.",
        }
