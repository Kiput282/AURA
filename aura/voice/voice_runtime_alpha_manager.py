import shutil
from pathlib import Path
from shlex import quote
from typing import Any

from aura.permissions.permission_manager import PermissionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner


class VoiceRuntimeAlphaManager:
    """
    Voice Runtime Alpha for AURA.

    Current phase:
    - prepare local text-to-speech plans
    - prepare safe speak-test proposals
    - check local dependency availability
    - never access microphone automatically
    - never play speaker output automatically
    - never execute shell commands
    """

    name = "voice_runtime_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.sandbox = ToolSandboxManager(project_root=self.project_root)
        self.planner = VoiceRuntimePlanner(project_root=self.project_root)

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())

        if len(normalized) > 500:
            return normalized[:500].rstrip() + "..."

        return normalized

    def detect_tts_backend(self) -> dict[str, Any]:
        candidates = [
            {
                "name": "piper",
                "type": "neural_tts",
                "priority": 1,
                "requires_voice_model": True,
            },
            {
                "name": "espeak-ng",
                "type": "fallback_tts",
                "priority": 2,
                "requires_voice_model": False,
            },
            {
                "name": "espeak",
                "type": "fallback_tts",
                "priority": 3,
                "requires_voice_model": False,
            },
        ]

        for candidate in candidates:
            path = shutil.which(candidate["name"])

            if path:
                return {
                    **candidate,
                    "found": True,
                    "path": path,
                }

        return {
            "name": "",
            "type": "",
            "priority": 0,
            "requires_voice_model": False,
            "found": False,
            "path": "",
        }

    def status(self) -> dict[str, Any]:
        dependency_check = self.planner.check()
        activation = self.planner.activation_contract()
        listen_state = self.planner.listen_state_contract()
        microphone_boundary = self.planner.microphone_capture_boundary_contract()
        stt_adapter = self.planner.speech_to_text_adapter_runtime_contract()
        voice_intent_chat = self.planner.voice_intent_chat_integration_contract()
        tts_adapter = self.planner.text_to_speech_adapter_runtime_contract()
        voice_permission_audit = self.planner.voice_permission_audit_runtime_contract()
        control_center_voice = self.planner.control_center_voice_controls_contract()
        integration_review = self.planner.voice_runtime_integration_review_contract()
        backend = self.detect_tts_backend()
        speaker_permission = self.permission_manager.check("speaker_speak")
        microphone_permission = self.permission_manager.check("microphone_listen")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "alpha_ready": True,
            "sprint_191_activation_foundation_ready": activation["activation_foundation_ready"],
            "sprint_192_listen_state_foundation_ready": listen_state["listen_state_foundation_ready"],
            "sprint_193_microphone_boundary_ready": microphone_boundary["microphone_boundary_ready"],
            "sprint_194_stt_adapter_contract_ready": stt_adapter["stt_adapter_contract_ready"],
            "sprint_195_voice_intent_chat_contract_ready": voice_intent_chat["voice_intent_chat_contract_ready"],
            "sprint_196_tts_adapter_contract_ready": tts_adapter["tts_adapter_contract_ready"],
            "sprint_197_voice_permission_audit_contract_ready": voice_permission_audit["voice_permission_audit_contract_ready"],
            "sprint_198_control_center_voice_controls_contract_ready": control_center_voice["control_center_voice_controls_contract_ready"],
            "sprint_199_voice_runtime_integration_review_contract_ready": integration_review["voice_runtime_integration_review_contract_ready"],
            "voice_runtime_integration_review_runtime_ready": integration_review["voice_runtime_integration_review_runtime_ready"],
            "voice_runtime_integration_review_status": integration_review["voice_runtime_integration_review_status"],
            "voice_runtime_reviewed_contract_count": integration_review["reviewed_contract_count"],
            "voice_runtime_all_prior_contracts_ready": integration_review["all_prior_contracts_ready"],
            "voice_runtime_all_prior_runtimes_not_ready": integration_review["all_prior_runtimes_not_ready"],
            "voice_runtime_safety_blocker_matrix_ready": integration_review["safety_blocker_matrix_ready"],
            "voice_runtime_activation_allowed": integration_review["runtime_activation_allowed"],
            "control_center_voice_controls_runtime_ready": control_center_voice["control_center_voice_controls_runtime_ready"],
            "control_center_voice_controls_visible": control_center_voice["control_center_voice_controls_visible"],
            "control_center_voice_controls_read_only": control_center_voice["control_center_voice_controls_read_only"],
            "control_center_voice_controls_disabled_by_default": control_center_voice["control_center_voice_controls_disabled_by_default"],
            "control_center_voice_controls_route_contract_ready": control_center_voice["control_center_voice_controls_route_contract_ready"],
            "control_center_voice_controls_panel_contract_ready": control_center_voice["control_center_voice_controls_panel_contract_ready"],
            "control_center_voice_listen_state_display_ready": control_center_voice["listen_state_display_boundary_ready"],
            "control_center_voice_ui_mutation_enabled": control_center_voice["ui_controls_mutation_enabled"],
            "control_center_voice_ui_voice_action_trigger_active": control_center_voice["ui_voice_action_trigger_active"],
            "voice_permission_audit_runtime_ready": voice_permission_audit["voice_permission_audit_runtime_ready"],
            "voice_permission_boundary_ready": voice_permission_audit["permission_boundary_ready"],
            "voice_microphone_permission_action": voice_permission_audit["microphone_permission_action"],
            "voice_speaker_permission_action": voice_permission_audit["speaker_permission_action"],
            "voice_microphone_permission_requires_confirmation": voice_permission_audit["microphone_permission_requires_confirmation"],
            "voice_speaker_permission_requires_confirmation": voice_permission_audit["speaker_permission_requires_confirmation"],
            "voice_audit_event_contract_ready": voice_permission_audit["audit_event_contract_ready"],
            "voice_audit_write_runtime_active": voice_permission_audit["audit_write_runtime_active"],
            "voice_permission_decision_runtime_active": voice_permission_audit["permission_decision_runtime_active"],
            "voice_permission_grant_runtime_active": voice_permission_audit["permission_grant_runtime_active"],
            "voice_permission_mutation_active": voice_permission_audit["permission_mutation_active"],
            "tts_adapter_runtime_ready": tts_adapter["tts_adapter_runtime_ready"],
            "tts_default_adapter": tts_adapter["default_adapter"],
            "tts_adapter_candidates": tts_adapter["candidate_adapter_count"],
            "voice_response_input_boundary_ready": tts_adapter["voice_response_input_boundary_ready"],
            "tts_synthesis_runtime_active": tts_adapter["tts_synthesis_runtime_active"],
            "speaker_playback_active": tts_adapter["speaker_playback_active"],
            "audio_output_file_write_active": tts_adapter["audio_output_file_write_active"],
            "automatic_speak_after_chat_enabled": tts_adapter["automatic_speak_after_chat_enabled"],
            "cloud_tts_fallback_enabled": tts_adapter["cloud_tts_fallback_enabled"],
            "voice_intent_runtime_ready": voice_intent_chat["voice_intent_runtime_ready"],
            "transcript_source": voice_intent_chat["transcript_source"],
            "transcript_to_chat_handoff_ready": voice_intent_chat["transcript_to_chat_handoff_contract_ready"],
            "transcript_to_chat_handoff_active": voice_intent_chat["transcript_to_chat_handoff_active"],
            "chat_session_write_active": voice_intent_chat["chat_session_write_active"],
            "voice_intent_direct_voice_to_action_enabled": voice_intent_chat["direct_voice_to_action_enabled"],
            "voice_intent_command_execution_active": voice_intent_chat["command_execution_active"],
            "stt_adapter_runtime_ready": stt_adapter["stt_adapter_runtime_ready"],
            "stt_default_adapter": stt_adapter["default_adapter"],
            "stt_adapter_candidates": stt_adapter["candidate_adapter_count"],
            "audio_file_transcription_runtime_ready": stt_adapter["audio_file_transcription_runtime_ready"],
            "live_microphone_transcription_active": stt_adapter["live_microphone_transcription_active"],
            "transcription_active": stt_adapter["transcription_active"],
            "cloud_stt_fallback_enabled": stt_adapter["cloud_stt_fallback_enabled"],
            "transcript_to_action_enabled": stt_adapter["transcript_to_action_enabled"],
            "microphone_capture_runtime_ready": microphone_boundary["microphone_capture_runtime_ready"],
            "microphone_capture_active": microphone_boundary["microphone_capture_active"],
            "audio_device_access": microphone_boundary["audio_device_access"],
            "audio_device_discovery_active": microphone_boundary["audio_device_discovery_active"],
            "current_listen_state": listen_state["current_state"],
            "default_listen_state": listen_state["default_state"],
            "speak_plan_ready": True,
            "speak_test_ready": True,
            "voice_context_ready": True,
            "dependency_check_ready": True,
            "tts_backend_found": backend["found"],
            "tts_backend": backend["name"],
            "tts_backend_path": backend["path"],
            "stt_runtime_ready": False,
            "tts_runtime_ready": backend["found"],
            "runtime_ready": False,
            "safe_idle_default": activation["safe_idle_default"],
            "push_to_talk_required": activation["push_to_talk_required"],
            "explicit_listen_required": activation["explicit_listen_required"],
            "always_listening_enabled": activation["always_listening_enabled"],
            "hidden_capture_enabled": activation["hidden_capture_enabled"],
            "background_wake_word_enabled": activation["background_wake_word_enabled"],
            "silent_cloud_fallback_enabled": activation["silent_cloud_fallback_enabled"],
            "direct_voice_to_action_enabled": activation["direct_voice_to_action_enabled"],
            "chat_session_reuse_required": activation["chat_session_reuse_required"],
            "microphone_access": False,
            "speaker_output": False,
            "recording_enabled": False,
            "recording_active": microphone_boundary["recording_active"],
            "audio_buffer_active": microphone_boundary["audio_buffer_active"],
            "audio_file_write_active": microphone_boundary["audio_file_write_active"],
            "playback_enabled": False,
            "command_execution": False,
            "audio_file_write": False,
            "requires_speaker_confirmation": speaker_permission.requires_confirmation,
            "requires_microphone_confirmation": microphone_permission.requires_confirmation,
            "python_packages_installed": dependency_check["python_packages_installed"],
            "python_packages_total": dependency_check["python_packages_total"],
            "executables_found": dependency_check["executables_found"],
            "executables_total": dependency_check["executables_total"],
            "activation_contract": activation,
            "listen_state_contract": listen_state,
            "microphone_capture_boundary_contract": microphone_boundary,
            "speech_to_text_adapter_runtime_contract": stt_adapter,
            "voice_intent_chat_integration_contract": voice_intent_chat,
            "text_to_speech_adapter_runtime_contract": tts_adapter,
            "voice_permission_audit_runtime_contract": voice_permission_audit,
            "control_center_voice_controls_contract": control_center_voice,
            "voice_runtime_integration_review_contract": integration_review,
            "sections": 15,
            "project_root": str(self.project_root),
            "note": "Voice Runtime Alpha is online for Sprint 199 voice runtime integration review. Sprint 191-198 contracts are reviewed without activating microphone capture, STT, TTS, speaker playback, permission mutation, audit writes, handoffs, or voice actions.",
        }

    def build_tts_command(self, text: str) -> dict[str, Any]:
        normalized_text = self.normalize_text(text)
        backend = self.detect_tts_backend()

        if not normalized_text:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No text was provided.",
            }

        if not backend["found"]:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No local TTS executable was found. Install or configure piper, espeak-ng, or espeak before real speech output.",
            }

        if backend["name"] in {"espeak-ng", "espeak"}:
            command = f"{backend['path']} {quote(normalized_text)}"
            reason = "Fallback TTS command prepared. It is not executed by AURA."
        elif backend["name"] == "piper":
            command = f"{backend['path']} --text {quote(normalized_text)}"
            reason = "Piper command proposal prepared. A voice model may still be required."
        else:
            command = ""
            reason = "Unsupported TTS backend."

        return {
            "available": bool(command),
            "backend": backend,
            "command": command,
            "reason": reason,
        }

    def speak_plan(self, text: str) -> dict[str, Any]:
        normalized_text = self.normalize_text(text)
        command_plan = self.build_tts_command(normalized_text)
        speaker_permission = self.permission_manager.check("speaker_speak")

        sandbox_check = (
            self.sandbox.check_command(command_plan["command"])
            if command_plan["command"]
            else None
        )

        return {
            "status": "planned",
            "text": normalized_text,
            "text_length": len(normalized_text),
            "command_available": command_plan["available"],
            "tts_backend": command_plan["backend"],
            "proposed_command": command_plan["command"],
            "command_reason": command_plan["reason"],
            "sandbox_check": sandbox_check,
            "speaker_permission": speaker_permission.to_dict(),
            "speaker_output": False,
            "microphone_access": False,
            "command_execution_performed": False,
            "playback_performed": False,
            "file_write_performed": False,
            "safety_notes": [
                "Speak plan is proposal-only.",
                "No command was executed.",
                "No speaker output was played.",
                "No microphone was accessed.",
                "Speaker output still requires explicit confirmation.",
            ],
        }

    def speak_test(self, text: str) -> dict[str, Any]:
        plan = self.speak_plan(text=text)

        return {
            "status": "prepared",
            "test_ready": True,
            "speak_plan": plan,
            "would_speak": plan["command_available"],
            "speaker_output": False,
            "microphone_access": False,
            "command_execution_performed": False,
            "playback_performed": False,
            "file_write_performed": False,
            "note": "Voice speak test was prepared only. AURA did not play audio or execute a TTS command.",
        }

    def context(self) -> dict[str, Any]:
        status = self.status()
        planner_status = self.planner.status()
        dependency_check = self.planner.check()

        return {
            "status": self.status_name,
            "context_ready": True,
            "alpha_status": status,
            "planner_status": planner_status,
            "dependency_check": dependency_check,
            "safe_current_capabilities": [
                "voice_runtime_alpha_status",
                "voice_speak_plan",
                "voice_speak_test_prepare_only",
                "voice_runtime_context",
            ],
            "disabled_capabilities": [
                "live_microphone_input",
                "automatic_speaker_playback",
                "real_stt_runtime",
                "real_voice_loop",
                "command_execution",
            ],
            "write_performed": False,
            "command_execution_performed": False,
            "microphone_access_performed": False,
            "speaker_output_performed": False,
            "note": "Voice runtime context is read-only and preparation-only.",
        }
