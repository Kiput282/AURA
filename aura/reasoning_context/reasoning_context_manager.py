
"""Reasoning context manager for AURA Genesis.

Planner-only reasoning context layer. It organizes visible reasoning context,
facts, assumptions, unknowns, evidence boundaries, and decision frames without
exposing hidden chain-of-thought or executing tools/actions.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class ReasoningContextManager:
    """Prepare safe visible reasoning context without runtime execution."""

    name = "reasoning_context_manager"
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
                        or status.get("thought_cycle_plan_ready")
                        or status.get("intent_frame_plan_ready")
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
            "thought_loop_reference": self.safe_import_status([
                ("aura.thought_loop.thought_loop_planner_manager", "ThoughtLoopPlannerManager"),
            ]),
            "partner_runtime_reference": self.safe_import_status([
                ("aura.partner_runtime.partner_runtime_planning_manager", "PartnerRuntimePlanningManager"),
            ]),
            "project_intent_reference": self.safe_import_status([
                ("aura.project_intent.project_intent_planner_manager", "ProjectIntentPlannerManager"),
                ("aura.intent.project_intent_planner_manager", "ProjectIntentPlannerManager"),
            ]),
            "local_task_reference": self.safe_import_status([
                ("aura.task_planner.local_task_planner_manager", "LocalTaskPlannerManager"),
                ("aura.local_task.local_task_planner_manager", "LocalTaskPlannerManager"),
            ]),
            "workspace_memory_reference": self.safe_import_status([
                ("aura.workspace_memory.workspace_memory_link_manager", "WorkspaceMemoryLinkManager"),
                ("aura.memory.workspace_memory_link_manager", "WorkspaceMemoryLinkManager"),
            ]),
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "vision_context_reference": self.safe_import_status([
                ("aura.vision_context.vision_context_planner_manager", "VisionContextPlannerManager"),
            ]),
            "codebase_validation_reference": self.safe_import_status([
                ("aura.codebase_validation.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
                ("aura.codebase_validation_gate.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def reasoning_plan_types(self) -> list[str]:
        return [
            "reasoning_context_status",
            "reasoning_context_plan",
            "fact_assumption_plan",
            "unknowns_review_plan",
            "evidence_boundary_plan",
            "decision_frame_plan",
            "response_strategy_plan",
            "reasoning_safety_plan",
            "reasoning_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare visible reasoning context without exposing hidden chain-of-thought.",
            "Separate facts, assumptions, unknowns, constraints, and user goals.",
            "Review evidence boundaries before answering.",
            "Frame safe decisions before action.",
            "Prepare response strategy that is honest when uncertain.",
            "Connect reasoning context with thought loop, voice, vision, memory, and project planners.",
            "Keep all outputs planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "hidden_chain_of_thought_exposure",
            "private_reasoning_disclosure",
            "autonomous_reasoning_loop",
            "background_reasoning_loop",
            "self_triggered_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "file_read",
            "file_write",
            "command_execution",
            "desktop_control",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "git_commit",
            "git_push",
        ]

    def infer_reasoning_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "project", "repo", "patch", "commit", "debug", "error"],
            "knowledge": ["know", "internet", "search", "reference", "tidak tahu", "belum tahu"],
            "voice": ["voice", "hear", "listen", "suara", "dengar"],
            "vision": ["vision", "see", "lihat", "screen", "camera", "gambar"],
            "memory": ["memory", "remember", "learn", "grow", "ingat", "belajar"],
            "decision": ["decide", "choose", "pilih", "keputusan", "rekomendasi"],
            "safety": ["safe", "risk", "permission", "izin", "private", "sensitive"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_reasoning_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "mode": "developer_reasoning_context",
                "focus": "separate_project_facts_assumptions_unknowns_and_validation_needs",
                "handoff": "thought_loop_or_codebase_validation",
            }
        if "knowledge" in tags:
            return {
                "mode": "honest_knowledge_context",
                "focus": "mark_uncertainty_before_answering_or_searching_later",
                "handoff": "future_internet_search_gate",
            }
        if "decision" in tags:
            return {
                "mode": "decision_frame_context",
                "focus": "compare_options_constraints_risks_and_recommendation_basis",
                "handoff": "partner_runtime_or_action_readiness",
            }
        if "voice" in tags or "vision" in tags:
            return {
                "mode": "multimodal_reasoning_context",
                "focus": "structure_heard_or_seen_context_before_response",
                "handoff": "voice_or_vision_runtime_future",
            }
        return {
            "mode": "general_reasoning_context",
            "focus": "organize_visible_context_before_answering",
            "handoff": "thought_loop_planner",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "hidden_chain_of_thought_exposed": False,
            "private_reasoning_disclosed": False,
            "autonomous_reasoning_loop": False,
            "background_reasoning_loop": False,
            "self_triggered_action": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "internet_search": False,
            "network_action": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "desktop_control": False,
            "screen_capture": False,
            "camera_access": False,
            "microphone_access": False,
            "speaker_output": False,
            "avatar_rendering": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general reasoning context"
        tags = self.infer_reasoning_tags(normalized_target)
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
            "principle": "cerdas_tetapi_tidak_sok_tahu",
            "tags": tags,
            "reasoning_mode": self.recommended_reasoning_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def reasoning_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("reasoning_context_plan", target)
        plan["context_steps"] = [
            "Identify user goal and available context.",
            "Separate facts, assumptions, unknowns, constraints, and desired outcome.",
            "Select the safest reasoning mode.",
            "Prepare a visible summary without exposing hidden chain-of-thought.",
        ]
        return plan

    def fact_assumption_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("fact_assumption_plan", target)
        plan["fact_assumption_steps"] = [
            "List facts provided by the user or current context.",
            "List assumptions that are not yet verified.",
            "Mark which assumptions need user confirmation or future search.",
            "Avoid treating assumptions as facts.",
        ]
        return plan

    def unknowns_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("unknowns_review_plan", target)
        plan["unknowns_steps"] = [
            "Identify what AURA does not know yet.",
            "Classify each unknown as ask-user, check-memory-later, search-internet-later, or validate-project-later.",
            "Avoid confident answers when critical unknowns remain.",
            "Prepare a concise clarification or permission request when needed.",
        ]
        return plan

    def evidence_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("evidence_boundary_plan", target)
        plan["evidence_steps"] = [
            "Identify what evidence is available.",
            "Identify what evidence is missing.",
            "Mark whether current answer should be high, medium, or low confidence.",
            "Do not fabricate sources, file contents, internet facts, or runtime observations.",
        ]
        return plan

    def decision_frame_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("decision_frame_plan", target)
        plan["decision_steps"] = [
            "Define the decision to be made.",
            "List options, constraints, risks, and tradeoffs.",
            "Mark which option is safest or most aligned with AURA's roadmap.",
            "Ask for confirmation before action.",
        ]
        return plan

    def response_strategy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("response_strategy_plan", target)
        plan["response_steps"] = [
            "Choose whether to answer directly, ask a question, propose a plan, or request permission.",
            "Prefer concise visible reasoning summaries.",
            "Be honest about uncertainty.",
            "Preserve AURA's supportive and non-arrogant personality.",
        ]
        return plan

    def reasoning_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("reasoning_safety_plan", target)
        plan["safety_steps"] = [
            "Do not expose hidden chain-of-thought or private reasoning traces.",
            "Do not run autonomous or background reasoning loops.",
            "Do not execute tools, commands, files, memory writes, internet searches, device access, desktop actions, network actions, or git operations.",
            "Do not pretend to know when evidence is missing.",
            "Return visible reasoning summaries, assumptions, confidence, and next-step proposals only.",
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
            "reasoning_plan_types": self.reasoning_plan_types(),
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
            "reasoning_context_plan_ready": True,
            "fact_assumption_plan_ready": True,
            "unknowns_review_plan_ready": True,
            "evidence_boundary_plan_ready": True,
            "decision_frame_plan_ready": True,
            "response_strategy_plan_ready": True,
            "reasoning_safety_plan_ready": True,
            "context_ready": True,
            "reasoning_plan_types": self.reasoning_plan_types(),
            "plan_type_count": len(self.reasoning_plan_types()),
            "thought_loop_reference_ready": True,
            "partner_runtime_reference_ready": True,
            "project_intent_reference_ready": True,
            "local_task_reference_ready": True,
            "workspace_memory_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "vision_context_reference_ready": True,
            "codebase_validation_reference_ready": True,
            "thought_loop_manager_found": integrations["thought_loop_reference"]["found"],
            "partner_runtime_manager_found": integrations["partner_runtime_reference"]["found"],
            "project_intent_manager_found": integrations["project_intent_reference"]["found"],
            "local_task_manager_found": integrations["local_task_reference"]["found"],
            "workspace_memory_manager_found": integrations["workspace_memory_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "vision_context_manager_found": integrations["vision_context_reference"]["found"],
            "codebase_validation_manager_found": integrations["codebase_validation_reference"]["found"],
            **boundary,
        }
