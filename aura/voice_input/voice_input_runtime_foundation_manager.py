
"""Voice input runtime foundation for AURA Genesis.

Foundation-only voice input layer. It prepares metadata-only plans for future
microphone permission, voice capture boundaries, speech-to-text adapter choice,
voice intent gating, and voice command confirmation without accessing the
microphone, recording audio, transcribing speech, executing commands, or
controlling devices.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class VoiceInputRuntimeFoundationManager:
    """Prepare safe voice input runtime foundation plans."""

    name = "voice_input_runtime_foundation"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}
        with self.identity_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def safe_import_status(self, candidates: list[tuple[str, str]]) -> dict[str, Any]:
        for module_name, class_name in candidates:
            try:
                module = importlib.import_module(module_name)
                manager_class = getattr(module, class_name)
                manager = manager_class(project_root=self.project_root)
                status = manager.status() if hasattr(manager, "status") else {}
                return {
                    "found": True,
                    "module": module_name,
                    "class": class_name,
                    "status": status.get("status", "available"),
                    "ready": bool(
                        status.get("planner_ready")
                        or status.get("context_ready")
                        or status.get("voice_intent_plan_ready")
                        or status.get("reasoning_context_plan_ready")
                        or status.get("knowledge_gap_plan_ready")
                    ),
                }
            except Exception:
                continue

        return {
            "found": False,
            "module": None,
            "class": None,
            "status": "not_found",
            "ready": False,
        }

    def integration_context(self) -> dict[str, Any]:
        return {
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "thought_loop_reference": self.safe_import_status([
                ("aura.thought_loop.thought_loop_planner_manager", "ThoughtLoopPlannerManager"),
            ]),
            "reasoning_context_reference": self.safe_import_status([
                ("aura.reasoning_context.reasoning_context_manager", "ReasoningContextManager"),
            ]),
            "knowledge_uncertainty_reference": self.safe_import_status([
                ("aura.knowledge_uncertainty.knowledge_uncertainty_gate_manager", "KnowledgeUncertaintyGateManager"),
            ]),
            "partner_runtime_reference": self.safe_import_status([
                ("aura.partner_runtime.partner_runtime_planning_manager", "PartnerRuntimePlanningManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def voice_input_plan_types(self) -> list[str]:
        return [
            "voice_input_status",
            "voice_input_permission_plan",
            "voice_capture_boundary_plan",
            "speech_to_text_adapter_plan",
            "voice_intent_gate_plan",
            "voice_command_confirmation_plan",
            "voice_session_plan",
            "voice_input_safety_plan",
            "voice_input_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan future microphone permission flow.",
            "Plan safe voice capture boundaries without recording audio.",
            "Plan speech-to-text adapter selection without running STT.",
            "Plan voice intent gates before any command handling.",
            "Plan voice command confirmation before future execution.",
            "Connect voice input planning with thought, reasoning, knowledge, and partner runtime layers.",
            "Keep all outputs foundation-only, planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "microphone_access",
            "audio_recording",
            "audio_capture",
            "speech_to_text_runtime",
            "speech_transcription",
            "wake_word_detection",
            "always_listening",
            "background_listening",
            "voice_command_execution",
            "voice_tool_execution",
            "speaker_output",
            "tts_runtime",
            "network_stt",
            "cloud_stt",
            "file_read",
            "file_write",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]

    def infer_voice_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "permission": ["permission", "izin", "allow", "grant"],
            "microphone": ["microphone", "mic", "audio", "suara", "dengar"],
            "stt": ["speech", "transcribe", "stt", "whisper", "recognition"],
            "command": ["command", "perintah", "execute", "run", "jalankan"],
            "session": ["session", "conversation", "chat", "dialog"],
            "safety": ["safe", "risk", "private", "sensitive", "privacy"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_voice_mode(self, tags: list[str]) -> dict[str, str]:
        if "command" in tags:
            return {
                "mode": "voice_command_permission_gate",
                "focus": "confirm_voice_command_before_future_action",
                "next_gate": "explicit_confirmation_required",
            }
        if "stt" in tags:
            return {
                "mode": "speech_to_text_adapter_planning",
                "focus": "choose_local_or_permission_based_stt_adapter_later",
                "next_gate": "microphone_and_stt_permission_required",
            }
        if "microphone" in tags or "permission" in tags:
            return {
                "mode": "microphone_permission_planning",
                "focus": "request_and_scope_microphone_access_before_runtime",
                "next_gate": "mic_permission_required",
            }
        return {
            "mode": "general_voice_input_foundation",
            "focus": "prepare_hearing_foundation_without_device_access",
            "next_gate": "voice_input_permission_review",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "microphone_access": False,
            "audio_recording": False,
            "audio_capture": False,
            "speech_to_text_runtime": False,
            "speech_transcription": False,
            "wake_word_detection": False,
            "always_listening": False,
            "background_listening": False,
            "voice_command_execution": False,
            "voice_tool_execution": False,
            "speaker_output": False,
            "tts_runtime": False,
            "network_stt": False,
            "cloud_stt": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "internet_search": False,
            "network_action": False,
            "desktop_control": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general voice input foundation"
        tags = self.infer_voice_tags(normalized_target)
        identity = self.load_identity()
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "creator": identity.get("creator", "Kiput"),
            "aura_name": identity.get("name", "AURA"),
            "motto": identity.get("motto", "Grow Together"),
            "essence": "AURA hidup ketika ia bisa berpikir, mendengar, dan melihat",
            "principle": "permission_first_voice_input",
            "tags": tags,
            "voice_mode": self.recommended_voice_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def voice_input_permission_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_input_permission_plan", target)
        plan["permission_steps"] = [
            "Explain why microphone access may be needed in a future runtime.",
            "Ask Kiput before enabling microphone access.",
            "Limit voice input to explicit session scope.",
            "Keep microphone disabled until a future permission gate is implemented.",
        ]
        plan["permission_prompt_template"] = (
            "Kiput, agar AURA bisa mendengar lewat suara, AURA perlu izin akses mikrofon. "
            "Akses ini hanya untuk sesi yang kamu izinkan. Mau aktifkan nanti?"
        )
        return plan

    def voice_capture_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_capture_boundary_plan", target)
        plan["capture_boundary_steps"] = [
            "Define when listening may start and stop in a future runtime.",
            "Avoid always-listening behavior by default.",
            "Avoid background listening without explicit permission.",
            "Do not record, capture, store, or transmit audio in this sprint.",
        ]
        return plan

    def speech_to_text_adapter_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("speech_to_text_adapter_plan", target)
        plan["adapter_steps"] = [
            "Compare future local STT, offline STT, and permission-based cloud STT options.",
            "Prefer local/offline STT for privacy when practical.",
            "Require download/install notice for any STT model or dependency.",
            "Do not run transcription or download models in this sprint.",
        ]
        return plan

    def voice_intent_gate_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_intent_gate_plan", target)
        plan["intent_gate_steps"] = [
            "Separate normal conversation from action commands.",
            "Send unclear voice input to clarification instead of execution.",
            "Require confirmation before future voice command execution.",
            "Block direct tool, file, command, desktop, git, internet, or external action execution.",
        ]
        return plan

    def voice_command_confirmation_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_command_confirmation_plan", target)
        plan["confirmation_steps"] = [
            "Repeat the interpreted command back to Kiput.",
            "List planned effects before action.",
            "Ask for explicit confirmation.",
            "Do not execute anything in this sprint.",
        ]
        plan["confirmation_prompt_template"] = (
            "Kiput, AURA menangkap perintah suara: <perintah>. "
            "AURA akan melakukan: <rencana>. Lanjutkan?"
        )
        return plan

    def voice_session_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_session_plan", target)
        plan["session_steps"] = [
            "Plan voice session start, active, paused, and stopped states.",
            "Keep voice input session explicit and visible.",
            "Prepare future push-to-talk or session-only listening mode.",
            "Do not enable live listening in this sprint.",
        ]
        return plan

    def voice_input_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_input_safety_plan", target)
        plan["safety_steps"] = [
            "Never access microphone in this sprint.",
            "Never record, capture, transcribe, store, or transmit audio.",
            "Never run always-listening or background listening.",
            "Never execute voice commands, tools, files, commands, desktop actions, internet search, network actions, memory writes, or git operations.",
            "Require explicit permission before future microphone, STT, download, install, or voice command execution.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        identity = self.load_identity()
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "identity_version": identity.get("version"),
            "voice_input_plan_types": self.voice_input_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "integration_context": self.integration_context(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        integrations = self.integration_context()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "voice_input_permission_plan_ready": True,
            "voice_capture_boundary_plan_ready": True,
            "speech_to_text_adapter_plan_ready": True,
            "voice_intent_gate_plan_ready": True,
            "voice_command_confirmation_plan_ready": True,
            "voice_session_plan_ready": True,
            "voice_input_safety_plan_ready": True,
            "context_ready": True,
            "voice_input_plan_types": self.voice_input_plan_types(),
            "plan_type_count": len(self.voice_input_plan_types()),
            "voice_conversation_reference_ready": True,
            "thought_loop_reference_ready": True,
            "reasoning_context_reference_ready": True,
            "knowledge_uncertainty_reference_ready": True,
            "partner_runtime_reference_ready": True,
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "thought_loop_manager_found": integrations["thought_loop_reference"]["found"],
            "reasoning_context_manager_found": integrations["reasoning_context_reference"]["found"],
            "knowledge_uncertainty_manager_found": integrations["knowledge_uncertainty_reference"]["found"],
            "partner_runtime_manager_found": integrations["partner_runtime_reference"]["found"],
            **boundary,
        }
