
"""Review and stabilization checkpoint for Sprint 71-80.

Planner-only checkpoint layer for reviewing the Sprint 71-80 development
block. It summarizes completed features, active/foundation/planner-only
status, safety boundaries, stabilization needs, roadmap gaps, and the next
planning block without performing file operations, command execution,
network action, git action, tool execution, or external actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ReviewStabilization7180Manager:
    """Prepare Sprint 71-80 checkpoint review and stabilization plans."""

    name = "review_stabilization_71_80"
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

    def checkpoint_plan_types(self) -> list[str]:
        return [
            "checkpoint_71_80_status",
            "completed_feature_review_plan",
            "active_foundation_review_plan",
            "safety_boundary_review_plan",
            "stabilization_validation_plan",
            "technical_debt_review_plan",
            "roadmap_gap_review_plan",
            "next_block_planning_plan",
            "checkpoint_71_80_context",
        ]

    def sprint_block(self) -> list[dict[str, str]]:
        return [
            {
                "sprint": "71.0",
                "version": "0.71.0-genesis",
                "feature": "Thought Loop Planner",
                "status": "online",
                "category": "thinking",
                "runtime_level": "planner_only",
            },
            {
                "sprint": "72.0",
                "version": "0.72.0-genesis",
                "feature": "Reasoning Context Manager",
                "status": "online",
                "category": "reasoning",
                "runtime_level": "planner_only",
            },
            {
                "sprint": "73.0",
                "version": "0.73.0-genesis",
                "feature": "Knowledge Uncertainty & Internet Search Gate",
                "status": "online",
                "category": "knowledge_safety",
                "runtime_level": "permission_gate_planner",
            },
            {
                "sprint": "74.0",
                "version": "0.74.0-genesis",
                "feature": "Voice Input Runtime Foundation",
                "status": "online",
                "category": "hearing_foundation",
                "runtime_level": "foundation_only",
            },
            {
                "sprint": "75.0",
                "version": "0.75.0-genesis",
                "feature": "Voice Intent Understanding Layer",
                "status": "online",
                "category": "hearing_understanding",
                "runtime_level": "planner_only",
            },
            {
                "sprint": "76.0",
                "version": "0.76.0-genesis",
                "feature": "Vision Input Runtime Foundation",
                "status": "online",
                "category": "seeing_foundation",
                "runtime_level": "foundation_only",
            },
            {
                "sprint": "77.0",
                "version": "0.77.0-genesis",
                "feature": "Visual Context Understanding Layer",
                "status": "online",
                "category": "seeing_understanding",
                "runtime_level": "planner_only",
            },
            {
                "sprint": "78.0",
                "version": "0.78.0-genesis",
                "feature": "Coder Project Generation Planner",
                "status": "online",
                "category": "coding_planner",
                "runtime_level": "planner_only",
            },
            {
                "sprint": "79.0",
                "version": "0.79.0-genesis",
                "feature": "Dependency & Download Permission Gate",
                "status": "online",
                "category": "dependency_safety",
                "runtime_level": "permission_gate_planner",
            },
            {
                "sprint": "80.0",
                "version": "0.80.0-genesis",
                "feature": "Review & Stabilization 71-80",
                "status": "planned",
                "category": "checkpoint",
                "runtime_level": "review_only",
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Review Sprint 71-80 completed features without changing runtime behavior.",
            "Summarize active, foundation-only, planner-only, and permission-gated modules.",
            "Review safety boundaries for hearing, seeing, coding, dependency, reasoning, and knowledge gates.",
            "Plan compact validation strategy without running commands from inside the manager.",
            "Identify technical debt and roadmap gaps for the next sprint block.",
            "Prepare Sprint 81-90 planning direction as review-only metadata.",
            "Keep checkpoint output planner-only, review-only, metadata-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "runtime_behavior_change",
            "automatic_stabilization",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "command_execution",
            "test_execution",
            "code_execution",
            "dependency_install",
            "package_download",
            "internet_search",
            "network_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def feature_status_summary(self) -> dict[str, Any]:
        block = self.sprint_block()
        completed = [item for item in block if item["status"] == "online"]
        foundation_only = [item for item in completed if item["runtime_level"] == "foundation_only"]
        planner_only = [item for item in completed if item["runtime_level"] == "planner_only"]
        permission_gated = [item for item in completed if "permission_gate" in item["runtime_level"]]
        review_only = [item for item in block if item["runtime_level"] == "review_only"]

        return {
            "block": "71-80",
            "planned_sprints": len(block),
            "completed_online": len(completed),
            "foundation_only": len(foundation_only),
            "planner_only": len(planner_only),
            "permission_gated": len(permission_gated),
            "review_only": len(review_only),
            "runtime_execution_features": 0,
            "all_completed_features": [item["feature"] for item in completed],
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "checkpoint_only": True,
            "review_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "runtime_behavior_change": False,
            "automatic_stabilization": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "command_execution": False,
            "test_execution": False,
            "code_execution": False,
            "dependency_install": False,
            "package_download": False,
            "internet_search": False,
            "network_action": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "desktop_control": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "Sprint 71-80 checkpoint review"
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
            "identity_version": identity.get("version"),
            "checkpoint_block": "71-80",
            "principle": "review_stabilize_plan_before_next_block",
            "feature_status_summary": self.feature_status_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def completed_feature_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("completed_feature_review_plan", target)
        plan["review_steps"] = [
            "Confirm Sprint 71-79 features are present in the roadmap and documented.",
            "Confirm each feature has an online status or explicit foundation/planner-only boundary.",
            "Confirm checkpoint Sprint 80 summarizes the block instead of adding runtime behavior.",
            "Prepare a human-readable summary for what exists, what is not runtime-active, and what should come next.",
        ]
        plan["completed_features"] = self.feature_status_summary()["all_completed_features"]
        return plan

    def active_foundation_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("active_foundation_review_plan", target)
        plan["review_steps"] = [
            "Separate active planner systems from foundation-only runtime foundations.",
            "Mark voice and vision foundations as online but runtime-disabled.",
            "Mark reasoning, knowledge, voice intent, visual context, coder project, and dependency gates as planner-only.",
            "Keep all action-like systems behind review, permission, and confirmation gates.",
        ]
        return plan

    def safety_boundary_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("safety_boundary_review_plan", target)
        plan["review_steps"] = [
            "Review that no sprint in 71-79 introduced real microphone, camera, OCR, vision, download, install, command, file, network, desktop, or git execution.",
            "Confirm voice, vision, coder, and dependency features remain permission-gated.",
            "Confirm internet search remains a gate and not automatic behavior.",
            "Confirm Sprint 80 itself is review-only and does not change runtime behavior.",
        ]
        return plan

    def stabilization_validation_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("stabilization_validation_plan", target)
        plan["validation_steps"] = [
            "Run targeted py_compile for checkpoint and touched integration files.",
            "Run direct manager status checks instead of expensive full status loops when possible.",
            "Run one final boot check with timeout.",
            "Avoid oversized validation blocks and avoid repeating long main.py integrations unnecessarily.",
        ]
        return plan

    def technical_debt_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("technical_debt_review_plan", target)
        plan["debt_review_steps"] = [
            "Review repeated CLI/shell packet printers for possible future shared formatter.",
            "Review repeated system_status wiring pattern for possible helper registration.",
            "Review long README/roadmap append-only growth for future changelog indexing.",
            "Defer refactor until after checkpoint unless it is necessary for stability.",
        ]
        return plan

    def roadmap_gap_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("roadmap_gap_review_plan", target)
        plan["gap_review_steps"] = [
            "Identify unbuilt runtime capabilities: actual microphone input, camera input, OCR, visual model runtime, project file generation, dependency install, and internet execution.",
            "Keep unbuilt capabilities as future milestones requiring explicit permission gates.",
            "Prioritize core AURA capabilities: think, hear, see, code safely, and ask permission.",
            "Prepare the next 10-sprint block without losing safety consistency.",
        ]
        return plan

    def next_block_planning_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("next_block_planning_plan", target)
        plan["next_block_direction"] = [
            "Sprint 81-90 should continue from planner-only foundations into controlled, permission-gated execution design.",
            "Possible focus: shared formatter/refactor, capability registry cleanup, permission workflow consolidation, prototype runtime adapters, and stronger validation tooling.",
            "Any real microphone/camera/download/file/code execution should remain behind explicit user approval and separate validation gates.",
            "Keep checkpoint reviews every 10 sprints.",
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
            "checkpoint_block": "71-80",
            "checkpoint_plan_types": self.checkpoint_plan_types(),
            "sprint_block": self.sprint_block(),
            "feature_status_summary": self.feature_status_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.feature_status_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "checkpoint_ready": True,
            "completed_feature_review_plan_ready": True,
            "active_foundation_review_plan_ready": True,
            "safety_boundary_review_plan_ready": True,
            "stabilization_validation_plan_ready": True,
            "technical_debt_review_plan_ready": True,
            "roadmap_gap_review_plan_ready": True,
            "next_block_planning_plan_ready": True,
            "context_ready": True,
            "checkpoint_plan_types": self.checkpoint_plan_types(),
            "plan_type_count": len(self.checkpoint_plan_types()),
            "completed_online": summary["completed_online"],
            "foundation_only_count": summary["foundation_only"],
            "planner_only_count": summary["planner_only"],
            "permission_gated_count": summary["permission_gated"],
            "runtime_execution_features": summary["runtime_execution_features"],
            **boundary,
        }
