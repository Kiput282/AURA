
"""Thought loop planner for AURA Genesis.

Planner-only thinking layer. It does not run autonomous loops,
execute tools, write memory, search the internet, access devices,
read/write project files, or execute commands.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class ThoughtLoopPlannerManager:
    """Plan safe thinking cycles without autonomous runtime execution."""

    name = "thought_loop_planner"
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
                        or status.get("runtime_ready")
                        or status.get("intent_ready")
                        or status.get("memory_ready")
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
            "partner_runtime_reference": self.safe_import_status([
                ("aura.partner_runtime.partner_runtime_planning_manager", "PartnerRuntimePlanningManager"),
            ]),
            "local_task_reference": self.safe_import_status([
                ("aura.task_planner.local_task_planner_manager", "LocalTaskPlannerManager"),
                ("aura.local_task.local_task_planner_manager", "LocalTaskPlannerManager"),
            ]),
            "project_intent_reference": self.safe_import_status([
                ("aura.project_intent.project_intent_planner_manager", "ProjectIntentPlannerManager"),
                ("aura.intent.project_intent_planner_manager", "ProjectIntentPlannerManager"),
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
            "desktop_workflow_reference": self.safe_import_status([
                ("aura.desktop_workflow.desktop_workflow_planner_manager", "DesktopWorkflowPlannerManager"),
            ]),
            "codebase_validation_reference": self.safe_import_status([
                ("aura.codebase_validation.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
                ("aura.codebase_validation_gate.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def thought_plan_types(self) -> list[str]:
        return [
            "thought_loop_status",
            "thought_cycle_plan",
            "intent_frame_plan",
            "reasoning_summary_plan",
            "uncertainty_review_plan",
            "action_readiness_review",
            "growth_memory_review",
            "thought_safety_plan",
            "thought_loop_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan a safe thought cycle before action.",
            "Frame user intent before choosing a planner.",
            "Prepare high-level reasoning summaries without exposing hidden chain-of-thought.",
            "Review uncertainty and decide whether to ask, search later, or proceed.",
            "Review action readiness and permission gates.",
            "Review what may be useful for future memory without writing memory automatically.",
            "Keep all outputs planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "autonomous_thought_loop",
            "background_loop",
            "continuous_self_prompting",
            "self_triggered_action",
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
            "app_opening",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "git_commit",
            "git_push",
        ]

    def infer_thought_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "repo", "project", "sprint", "patch", "commit", "validation"],
            "voice": ["voice", "hear", "listen", "speech", "suara", "dengar"],
            "vision": ["vision", "see", "screen", "camera", "lihat", "gambar"],
            "knowledge": ["know", "internet", "search", "tidak tahu", "belum tahu", "reference"],
            "memory": ["memory", "remember", "learn", "grow", "belajar", "ingat"],
            "safety": ["permission", "safe", "risk", "private", "sensitive", "izin"],
            "planning": ["plan", "roadmap", "next", "workflow", "task"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_thought_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "mode": "developer_reasoning_planner",
                "focus": "understand_project_goal_before_patch",
                "next_gate": "validation_and_permission_review",
            }
        if "knowledge" in tags:
            return {
                "mode": "honest_knowledge_planner",
                "focus": "admit_uncertainty_before_answering",
                "next_gate": "internet_search_gate_future",
            }
        if "voice" in tags or "vision" in tags:
            return {
                "mode": "multimodal_context_planner",
                "focus": "connect_hearing_or_seeing_context_to_reasoning",
                "next_gate": "runtime_input_permission",
            }
        if "memory" in tags:
            return {
                "mode": "growth_memory_planner",
                "focus": "decide_what_may_help_future_growth",
                "next_gate": "memory_write_permission",
            }
        return {
            "mode": "general_thought_planner",
            "focus": "think_before_act",
            "next_gate": "ask_when_uncertain",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "autonomous_thought_loop": False,
            "background_loop": False,
            "continuous_self_prompting": False,
            "self_triggered_action": False,
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
            "app_opening": False,
            "screen_capture": False,
            "camera_access": False,
            "microphone_access": False,
            "speaker_output": False,
            "avatar_rendering": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general thought loop planning"
        tags = self.infer_thought_tags(normalized_target)
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
            "thought_mode": self.recommended_thought_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def thought_cycle_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("thought_cycle_plan", target)
        plan["thought_cycle_steps"] = [
            "Observe the user goal from provided metadata.",
            "Frame the intent before choosing an answer or planner.",
            "Check uncertainty and avoid pretending to know.",
            "Choose whether to answer, ask, plan, or request permission for future action.",
            "Return a concise human-reviewable thinking summary.",
        ]
        return plan

    def intent_frame_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("intent_frame_plan", target)
        plan["intent_frame_steps"] = [
            "Identify the user's main goal.",
            "Identify the context needed to answer or act safely.",
            "Separate facts, assumptions, unknowns, and required permissions.",
            "Choose the safest next planning layer.",
        ]
        return plan

    def reasoning_summary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("reasoning_summary_plan", target)
        plan["reasoning_summary_steps"] = [
            "Prepare a short visible reasoning summary.",
            "Do not expose private hidden chain-of-thought.",
            "Show key assumptions, confidence level, and next action proposal.",
            "Keep reasoning output useful, honest, and concise.",
        ]
        return plan

    def uncertainty_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("uncertainty_review_plan", target)
        plan["uncertainty_steps"] = [
            "Identify what AURA knows from current context.",
            "Identify what AURA does not know.",
            "Decide whether to ask Kiput, use memory later, or request internet search permission in a future sprint.",
            "Never fabricate an answer when uncertain.",
        ]
        return plan

    def action_readiness_review(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("action_readiness_review", target)
        plan["readiness_steps"] = [
            "Identify whether the request is only informational or requires action.",
            "Identify required permission gates before action.",
            "Block any tool, file, command, desktop, internet, device, or git action in this sprint.",
            "Return only a readiness review.",
        ]
        return plan

    def growth_memory_review(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("growth_memory_review", target)
        plan["growth_memory_steps"] = [
            "Identify whether the interaction contains durable growth information.",
            "Suggest what may be useful for future AURA behavior.",
            "Do not write memory automatically from this planner.",
            "Require explicit memory permission or a separate safe memory gate.",
        ]
        return plan

    def thought_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("thought_safety_plan", target)
        plan["safety_steps"] = [
            "Never run autonomous or background thought loops in this sprint.",
            "Never self-trigger actions.",
            "Never execute tools, files, commands, desktop actions, internet search, device access, memory write, network action, or git operations.",
            "Never pretend to know when uncertain.",
            "Require explicit permission before any future runtime action.",
            "Keep AURA's thinking local-first, honest, permission-first, and proposal-only.",
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
            "thought_plan_types": self.thought_plan_types(),
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
            "thought_cycle_plan_ready": True,
            "intent_frame_plan_ready": True,
            "reasoning_summary_plan_ready": True,
            "uncertainty_review_plan_ready": True,
            "action_readiness_review_ready": True,
            "growth_memory_review_ready": True,
            "thought_safety_plan_ready": True,
            "context_ready": True,
            "thought_plan_types": self.thought_plan_types(),
            "plan_type_count": len(self.thought_plan_types()),
            "partner_runtime_reference_ready": True,
            "local_task_reference_ready": True,
            "project_intent_reference_ready": True,
            "workspace_memory_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "vision_context_reference_ready": True,
            "desktop_workflow_reference_ready": True,
            "codebase_validation_reference_ready": True,
            "partner_runtime_manager_found": integrations["partner_runtime_reference"]["found"],
            "local_task_manager_found": integrations["local_task_reference"]["found"],
            "project_intent_manager_found": integrations["project_intent_reference"]["found"],
            "workspace_memory_manager_found": integrations["workspace_memory_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "vision_context_manager_found": integrations["vision_context_reference"]["found"],
            "desktop_workflow_manager_found": integrations["desktop_workflow_reference"]["found"],
            "codebase_validation_manager_found": integrations["codebase_validation_reference"]["found"],
            **boundary,
        }
