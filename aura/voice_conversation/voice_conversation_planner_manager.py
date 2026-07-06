
"""Voice conversation planner for AURA Genesis.

This module is intentionally planner-only. It does not access a microphone,
does not produce real speaker/TTS output, and does not execute commands.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class VoiceConversationPlannerManager:
    """Plan safe voice conversation flows without runtime voice execution."""

    name = "voice_conversation_planner"
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
                        or status.get("ready")
                        or status.get("context_ready")
                        or status.get("runtime_ready")
                        or status.get("tool_sandbox_ready")
                        or status.get("expression_language_ready")
                        or status.get("partner_ready")
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
            "expression_language": self.safe_import_status([
                ("aura.expression.expression_language_manager", "ExpressionLanguageManager"),
                ("aura.expression.expression_language_runtime_manager", "ExpressionLanguageManager"),
            ]),
            "partner_alpha": self.safe_import_status([
                ("aura.partner.partner_alpha_manager", "PartnerAlphaManager"),
                ("aura.partner_alpha.partner_alpha_manager", "PartnerAlphaManager"),
            ]),
            "local_task_planner": self.safe_import_status([
                ("aura.local_task.local_task_planner_alpha_manager", "LocalTaskPlannerAlphaManager"),
            ]),
            "tool_sandbox": self.safe_import_status([
                ("aura.sandbox.tool_sandbox_manager", "ToolSandboxManager"),
                ("aura.tools.tool_sandbox_manager", "ToolSandboxManager"),
            ]),
            "permissions": self.safe_import_status([
                ("aura.permissions.permission_manager", "PermissionManager"),
            ]),
            "voice_runtime_alpha_reference": self.safe_import_status([
                ("aura.voice_runtime_alpha.voice_runtime_alpha_manager", "VoiceRuntimeAlphaManager"),
                ("aura.voice.voice_runtime_alpha_manager", "VoiceRuntimeAlphaManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def voice_plan_types(self) -> list[str]:
        return [
            "voice_conversation_status",
            "voice_intent_plan",
            "voice_response_plan",
            "conversation_turn_plan",
            "voice_safety_plan",
            "voice_conversation_context",
            "safety_boundary",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan voice conversation intent without microphone access.",
            "Plan voice response style without TTS/speaker output.",
            "Plan conversation turn flow for partner interaction.",
            "Plan safety boundaries for voice conversations.",
            "Reference expression language and partner context as metadata.",
            "Stay planner-only and proposal-only.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "microphone_access",
            "speaker_output",
            "tts_runtime_output",
            "audio_recording",
            "wake_word_runtime",
            "voice_command_execution",
            "desktop_action_execution",
            "app_opening",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]

    def infer_voice_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "coding", "sprint", "patch", "repo", "git", "debug"],
            "streaming": ["stream", "live", "chat", "viewer", "obs"],
            "gaming": ["game", "gaming", "match", "boss", "quest"],
            "creative": ["creative", "asset", "avatar", "blender", "design"],
            "learning": ["learn", "study", "explain", "tutorial"],
            "daily": ["daily", "briefing", "reminder", "routine"],
            "safety": ["private", "secret", "unsafe", "risk", "permission"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_voice_style(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "tone": "serious_concise_helpful",
                "pace": "calm_and_structured",
                "verbosity": "short_until_detail_requested",
            }
        if "streaming" in tags:
            return {
                "tone": "friendly_expressive_not_annoying",
                "pace": "responsive",
                "verbosity": "compact_and_contextual",
            }
        if "gaming" in tags:
            return {
                "tone": "playful_supportive",
                "pace": "quick",
                "verbosity": "short_actionable",
            }
        if "learning" in tags:
            return {
                "tone": "patient_clear",
                "pace": "step_by_step",
                "verbosity": "moderate",
            }
        return {
            "tone": "friendly_intelligent_supportive",
            "pace": "natural",
            "verbosity": "balanced",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "microphone_access": False,
            "speaker_output": False,
            "tts_runtime_output": False,
            "audio_recording": False,
            "wake_word_runtime": False,
            "voice_command_execution": False,
            "desktop_action_execution": False,
            "app_opened": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general voice conversation"
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
            "tags": tags,
            "voice_style": self.recommended_voice_style(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def voice_intent_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_intent_plan", target)
        plan["intent_steps"] = [
            "Identify the user's spoken or typed intent from context metadata.",
            "Classify whether the interaction is coding, creative, gaming, streaming, learning, daily, or general.",
            "Select a safe response mode without triggering runtime voice actions.",
            "Ask for clarification when intent is ambiguous or action would need permission.",
        ]
        return plan

    def voice_response_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_response_plan", target)
        plan["response_steps"] = [
            "Prepare a concise natural-language response.",
            "Match tone to AURA personality and current context.",
            "Avoid over-talking during coding or live workflow.",
            "Keep voice output as text/planning metadata only until runtime permissions exist.",
        ]
        return plan

    def conversation_turn_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("conversation_turn_plan", target)
        plan["turn_steps"] = [
            "Receive user message or future voice transcript as metadata.",
            "Summarize intent and context.",
            "Choose whether to answer, ask one clarification, or propose a safe next step.",
            "Return a planned response without microphone, TTS, speaker, command, app, or file action.",
        ]
        return plan

    def voice_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("voice_safety_plan", target)
        plan["safety_steps"] = [
            "Never access microphone without explicit runtime permission.",
            "Never output real TTS/speaker audio in this planner sprint.",
            "Never execute commands from spoken text automatically.",
            "Never open apps, files, browser, desktop actions, or external tools automatically.",
            "Confirm before any future runtime voice action.",
            "Preserve local-first, permission-first, safety-first behavior.",
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
            "voice_plan_types": self.voice_plan_types(),
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
            "voice_intent_plan_ready": True,
            "voice_response_plan_ready": True,
            "conversation_turn_plan_ready": True,
            "voice_safety_plan_ready": True,
            "context_ready": True,
            "voice_plan_types": self.voice_plan_types(),
            "plan_type_count": len(self.voice_plan_types()),
            "expression_language_integration_ready": True,
            "partner_alpha_integration_ready": True,
            "local_task_planner_integration_ready": True,
            "tool_sandbox_integration_ready": True,
            "permissions_integration_ready": True,
            "voice_runtime_alpha_reference_ready": True,
            "expression_language_manager_found": integrations["expression_language"]["found"],
            "partner_alpha_manager_found": integrations["partner_alpha"]["found"],
            "local_task_planner_manager_found": integrations["local_task_planner"]["found"],
            "tool_sandbox_manager_found": integrations["tool_sandbox"]["found"],
            "permission_manager_found": integrations["permissions"]["found"],
            "voice_runtime_alpha_manager_found": integrations["voice_runtime_alpha_reference"]["found"],
            **boundary,
        }
