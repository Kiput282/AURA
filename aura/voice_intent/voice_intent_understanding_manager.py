
"""Voice intent understanding layer for AURA Genesis.

Planner-only layer for future voice intent understanding. It prepares how AURA
should normalize transcribed voice text, classify intent, extract entities,
ask clarification, gate action-like commands, and keep voice understanding
safe without microphone access, speech-to-text runtime, audio recording,
command execution, tool execution, or external actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class VoiceIntentUnderstandingManager:
    """Prepare safe planner-only voice intent understanding."""

    name = "voice_intent_understanding"
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

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def voice_intent_plan_types(self) -> list[str]:
        return [
            "voice_intent_status",
            "voice_transcript_normalization_plan",
            "voice_intent_classification_plan",
            "voice_entity_slot_plan",
            "voice_clarification_plan",
            "voice_action_gate_plan",
            "voice_response_plan",
            "voice_intent_safety_plan",
            "voice_intent_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan how future transcribed voice text should be normalized.",
            "Plan how voice intent should be classified.",
            "Plan entity and slot extraction from voice text.",
            "Plan clarification when voice meaning is ambiguous.",
            "Plan action gates for command-like voice requests.",
            "Plan safe response strategy for voice conversations.",
            "Keep all voice intent outputs planner-only and human-reviewable.",
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
            "action_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]

    def infer_intent_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "conversation": ["chat", "bicara", "ngobrol", "tanya", "jawab", "conversation"],
            "action": ["jalankan", "buka", "buat", "hapus", "ubah", "kirim", "run", "execute"],
            "coding": ["code", "repo", "project", "commit", "bug", "patch", "validasi"],
            "file": ["file", "folder", "dokumen", "readme", "roadmap"],
            "internet": ["internet", "search", "cari", "web", "download"],
            "unclear": ["mungkin", "kayaknya", "kurang jelas", "tidak jelas", "ambigu"],
            "safety": ["izin", "permission", "bahaya", "private", "sensitive", "aman"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_intent_mode(self, tags: list[str]) -> dict[str, str]:
        if "action" in tags or "coding" in tags or "file" in tags:
            return {
                "mode": "voice_action_gate",
                "focus": "classify_as_possible_action_and_require_confirmation",
                "next_gate": "explicit_confirmation_required",
            }
        if "internet" in tags:
            return {
                "mode": "voice_external_request_gate",
                "focus": "request_permission_before_future_search_or_download",
                "next_gate": "internet_or_download_permission_required",
            }
        if "unclear" in tags:
            return {
                "mode": "voice_clarification",
                "focus": "ask_clarification_before_answer_or_action",
                "next_gate": "clarification_required",
            }
        if "conversation" in tags:
            return {
                "mode": "voice_conversation_intent",
                "focus": "respond_conversationally_without_action_execution",
                "next_gate": "response_strategy_review",
            }
        return {
            "mode": "general_voice_intent_understanding",
            "focus": "classify_voice_text_without_execution",
            "next_gate": "intent_review",
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
            "action_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "memory_write": False,
            "internet_search": False,
            "network_action": False,
            "desktop_control": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general voice intent understanding"
        tags = self.infer_intent_tags(normalized_target)
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
            "principle": "understand_voice_before_action",
            "tags": tags,
            "intent_mode": self.recommended_intent_mode(tags),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def voice_transcript_normalization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_transcript_normalization_plan", target)
        plan["normalization_steps"] = [
            "Treat input as future transcribed text, not live audio.",
            "Normalize spacing, casing hints, filler words, and incomplete phrases.",
            "Keep original meaning visible for review.",
            "Do not record, transcribe, or capture audio in this sprint.",
        ]
        return plan

    def voice_intent_classification_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_intent_classification_plan", target)
        plan["classification_steps"] = [
            "Classify voice text as conversation, question, instruction, command-like request, correction, or unclear.",
            "Mark uncertainty when intent is ambiguous.",
            "Prefer clarification over guessing.",
            "Never execute action-like voice intent directly.",
        ]
        return plan

    def voice_entity_slot_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_entity_slot_plan", target)
        plan["entity_slot_steps"] = [
            "Identify possible target object, action verb, time, location, file/project, and constraints.",
            "Mark missing required slots.",
            "Ask for missing slots before action planning.",
            "Do not read files or inspect external state in this sprint.",
        ]
        return plan

    def voice_clarification_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_clarification_plan", target)
        plan["clarification_steps"] = [
            "Detect unclear, conflicting, or incomplete voice meaning.",
            "Ask one short clarification question.",
            "Avoid pretending the command was understood.",
            "Do not proceed to action planning until meaning is clear.",
        ]
        return plan

    def voice_action_gate_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_action_gate_plan", target)
        plan["action_gate_steps"] = [
            "Detect whether voice text requests an action.",
            "Separate harmless conversation from actionable command.",
            "Require explicit confirmation before any future action.",
            "Block tool, command, file, desktop, internet, network, memory, git, and external execution in this sprint.",
        ]
        plan["confirmation_template"] = (
            "Kiput, AURA memahami ini sebagai kemungkinan perintah: <intent>. "
            "AURA belum akan menjalankan apa pun. Mau AURA lanjutkan ke rencana aksi?"
        )
        return plan

    def voice_response_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_response_plan", target)
        plan["response_steps"] = [
            "Choose concise response for voice-friendly interaction.",
            "State uncertainty when needed.",
            "Ask clarification before long explanations when voice context is unclear.",
            "Keep response non-executing and reviewable.",
        ]
        return plan

    def voice_intent_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_intent_safety_plan", target)
        plan["safety_steps"] = [
            "Never access microphone, record audio, capture audio, or run STT in this sprint.",
            "Never execute voice commands, tools, files, commands, desktop actions, internet search, network actions, memory writes, or git operations.",
            "Never assume unclear voice intent is correct.",
            "Require clarification or explicit confirmation before future action.",
            "Keep voice intent understanding planner-only, proposal-only, and metadata-only.",
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
            "voice_intent_plan_types": self.voice_intent_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "voice_transcript_normalization_plan_ready": True,
            "voice_intent_classification_plan_ready": True,
            "voice_entity_slot_plan_ready": True,
            "voice_clarification_plan_ready": True,
            "voice_action_gate_plan_ready": True,
            "voice_response_plan_ready": True,
            "voice_intent_safety_plan_ready": True,
            "context_ready": True,
            "voice_intent_plan_types": self.voice_intent_plan_types(),
            "plan_type_count": len(self.voice_intent_plan_types()),
            **boundary,
        }
