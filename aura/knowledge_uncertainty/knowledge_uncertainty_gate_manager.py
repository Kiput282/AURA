
"""Knowledge uncertainty and internet search gate for AURA Genesis.

Planner-only knowledge honesty layer. It marks uncertainty, plans when to ask,
when to request internet search permission, when downloads may be required,
and how to explain confidence without performing real search, download,
network, file, command, or tool execution.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class KnowledgeUncertaintyGateManager:
    """Plan honest uncertainty handling and internet/search/download gates."""

    name = "knowledge_uncertainty_gate"
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
                        or status.get("reasoning_context_plan_ready")
                        or status.get("thought_cycle_plan_ready")
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
            "reasoning_context_reference": self.safe_import_status([
                ("aura.reasoning_context.reasoning_context_manager", "ReasoningContextManager"),
            ]),
            "thought_loop_reference": self.safe_import_status([
                ("aura.thought_loop.thought_loop_planner_manager", "ThoughtLoopPlannerManager"),
            ]),
            "partner_runtime_reference": self.safe_import_status([
                ("aura.partner_runtime.partner_runtime_planning_manager", "PartnerRuntimePlanningManager"),
            ]),
            "workspace_memory_reference": self.safe_import_status([
                ("aura.workspace_memory.workspace_memory_link_manager", "WorkspaceMemoryLinkManager"),
                ("aura.memory.workspace_memory_link_manager", "WorkspaceMemoryLinkManager"),
            ]),
            "safe_file_operation_reference": self.safe_import_status([
                ("aura.file_ops.safe_file_operation_planner_manager", "SafeFileOperationPlannerManager"),
            ]),
            "codebase_validation_reference": self.safe_import_status([
                ("aura.codebase_validation.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
                ("aura.codebase_validation_gate.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def knowledge_plan_types(self) -> list[str]:
        return [
            "knowledge_uncertainty_status",
            "knowledge_gap_plan",
            "uncertainty_review_plan",
            "internet_search_gate_plan",
            "source_requirement_plan",
            "download_requirement_plan",
            "answer_confidence_plan",
            "knowledge_safety_plan",
            "knowledge_uncertainty_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Mark what AURA knows, does not know, and only assumes.",
            "Plan when AURA should ask Kiput instead of guessing.",
            "Plan when internet search permission should be requested.",
            "Plan source requirements before future search.",
            "Plan download requirement notices before future project downloads.",
            "Plan confidence labels for answers.",
            "Keep all outputs planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "internet_search",
            "web_request",
            "source_fetch",
            "browser_opening",
            "network_action",
            "download_execution",
            "file_download",
            "dependency_install",
            "package_install",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "memory_write",
            "background_monitoring",
            "autonomous_search",
            "fabricated_answer",
            "fabricated_source",
        ]

    def infer_knowledge_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "project", "repo", "dependency", "package", "library", "install"],
            "download": ["download", "asset", "model", "file", "gb", "mb", "unduh"],
            "internet": ["internet", "search", "web", "source", "reference", "cari"],
            "uncertainty": ["tidak tahu", "belum tahu", "not sure", "uncertain", "kurang yakin"],
            "current_info": ["latest", "terbaru", "harga", "jadwal", "versi", "update"],
            "safety": ["permission", "izin", "risk", "safe", "private", "sensitive"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_knowledge_mode(self, tags: list[str]) -> dict[str, str]:
        if "download" in tags or "coding" in tags:
            return {
                "mode": "project_dependency_permission_gate",
                "focus": "explain_required_dependency_or_download_before_action",
                "next_gate": "explicit_download_or_install_permission",
            }
        if "internet" in tags or "current_info" in tags:
            return {
                "mode": "internet_search_permission_gate",
                "focus": "request_search_permission_before_using_current_web_info",
                "next_gate": "search_permission_required",
            }
        if "uncertainty" in tags:
            return {
                "mode": "honest_uncertainty_response",
                "focus": "admit_unknowns_and_ask_or_request_search",
                "next_gate": "ask_kiput_or_search_gate",
            }
        return {
            "mode": "general_knowledge_honesty_gate",
            "focus": "separate_known_unknown_assumed_before_answer",
            "next_gate": "confidence_review",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "internet_search": False,
            "web_request": False,
            "source_fetch": False,
            "browser_opening": False,
            "network_action": False,
            "download_execution": False,
            "file_download": False,
            "dependency_install": False,
            "package_install": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "memory_write": False,
            "background_monitoring": False,
            "autonomous_search": False,
            "fabricated_answer": False,
            "fabricated_source": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general knowledge uncertainty gate"
        tags = self.infer_knowledge_tags(normalized_target)
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
            "knowledge_mode": self.recommended_knowledge_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def knowledge_gap_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("knowledge_gap_plan", target)
        plan["gap_steps"] = [
            "Separate known facts, assumptions, and unknowns.",
            "Mark which unknowns are critical before answering.",
            "Choose ask-Kiput, answer-with-caveat, or future search-permission path.",
            "Never fill missing facts with fabrication.",
        ]
        return plan

    def uncertainty_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("uncertainty_review_plan", target)
        plan["uncertainty_steps"] = [
            "Identify confidence level: high, medium, low, or unknown.",
            "Explain why the answer may be uncertain.",
            "Decide whether to ask a clarification question or request search permission.",
            "Use honest wording when knowledge is incomplete.",
        ]
        return plan

    def internet_search_gate_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("internet_search_gate_plan", target)
        plan["search_gate_steps"] = [
            "Identify whether current or external information is needed.",
            "Explain what AURA would search for in a future runtime.",
            "Ask Kiput for permission before any internet search.",
            "Do not search, open browser, fetch sources, or use network in this sprint.",
        ]
        plan["permission_prompt_template"] = (
            "Kiput, AURA belum yakin dan perlu referensi terbaru. "
            "AURA bisa cari di internet tentang: <topik>. Mau AURA cari sekarang?"
        )
        return plan

    def source_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("source_requirement_plan", target)
        plan["source_steps"] = [
            "Identify what source type would be appropriate: official docs, release notes, vendor page, paper, or trusted article.",
            "Prefer primary/official sources when accuracy matters.",
            "Plan to cite sources after future search.",
            "Do not invent citations or source claims.",
        ]
        return plan

    def download_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("download_requirement_plan", target)
        plan["download_steps"] = [
            "Identify whether a project dependency, model, asset, SDK, library, or dataset may be required.",
            "Prepare a notice with name, source, estimated size, purpose, and risk.",
            "Ask Kiput before any download or install.",
            "Do not download, install, write files, or execute commands in this sprint.",
        ]
        plan["download_notice_template"] = (
            "Ada file/dependency yang harus kita download dulu nih Kiput. "
            "Nama: <nama>. Sumber: <sumber>. Ukuran kira-kira: <ukuran>. "
            "Fungsi: <fungsi>. Risiko: <risiko>. Mau AURA download/install nanti?"
        )
        return plan

    def answer_confidence_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("answer_confidence_plan", target)
        plan["confidence_steps"] = [
            "Choose a confidence label before answering.",
            "State assumptions when confidence is not high.",
            "Say when AURA does not know enough.",
            "Recommend search or clarification only when needed.",
        ]
        return plan

    def knowledge_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("knowledge_safety_plan", target)
        plan["safety_steps"] = [
            "Never pretend to know when evidence is missing.",
            "Never fabricate sources, versions, prices, schedules, or file contents.",
            "Never search internet, fetch sources, download files, install dependencies, execute tools, write memory, read/write files, or run commands in this sprint.",
            "Ask permission before future internet search, download, install, or external action.",
            "Keep knowledge behavior honest, local-first, permission-first, and proposal-only.",
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
            "knowledge_plan_types": self.knowledge_plan_types(),
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
            "knowledge_gap_plan_ready": True,
            "uncertainty_review_plan_ready": True,
            "internet_search_gate_plan_ready": True,
            "source_requirement_plan_ready": True,
            "download_requirement_plan_ready": True,
            "answer_confidence_plan_ready": True,
            "knowledge_safety_plan_ready": True,
            "context_ready": True,
            "knowledge_plan_types": self.knowledge_plan_types(),
            "plan_type_count": len(self.knowledge_plan_types()),
            "reasoning_context_reference_ready": True,
            "thought_loop_reference_ready": True,
            "partner_runtime_reference_ready": True,
            "workspace_memory_reference_ready": True,
            "safe_file_operation_reference_ready": True,
            "codebase_validation_reference_ready": True,
            "reasoning_context_manager_found": integrations["reasoning_context_reference"]["found"],
            "thought_loop_manager_found": integrations["thought_loop_reference"]["found"],
            "partner_runtime_manager_found": integrations["partner_runtime_reference"]["found"],
            "workspace_memory_manager_found": integrations["workspace_memory_reference"]["found"],
            "safe_file_operation_manager_found": integrations["safe_file_operation_reference"]["found"],
            "codebase_validation_manager_found": integrations["codebase_validation_reference"]["found"],
            **boundary,
        }
