
"""Coder project generation planner for AURA Genesis.

Planner-only layer for future code/project generation. It prepares how AURA
should frame project requests, propose directory/file blueprints, plan
dependencies, define validation strategy, and require review gates before
any project/file creation, dependency install, command execution, code
execution, git action, network action, or real tool execution.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class CoderProjectGenerationPlannerManager:
    """Prepare safe planner-only project/code generation plans."""

    name = "coder_project_generation_planner"
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

    def coder_project_plan_types(self) -> list[str]:
        return [
            "coder_project_status",
            "project_request_frame_plan",
            "project_structure_plan",
            "code_file_blueprint_plan",
            "dependency_plan",
            "generation_review_gate_plan",
            "validation_strategy_plan",
            "project_generation_safety_plan",
            "coder_project_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan project generation requirements without creating files.",
            "Plan directory and file blueprints without writing to disk.",
            "Plan code file responsibilities without generating runtime files.",
            "Plan dependencies without installing or downloading packages.",
            "Plan validation strategy without running commands or tests.",
            "Gate future project generation behind explicit review and confirmation.",
            "Keep all outputs planner-only, proposal-only, metadata-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "project_creation_runtime",
            "project_files_written",
            "directory_creation",
            "file_read",
            "file_write",
            "file_delete",
            "file_modify",
            "code_generation_runtime",
            "code_execution",
            "test_execution",
            "command_execution",
            "dependency_install",
            "package_download",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def infer_project_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "web": ["web", "website", "frontend", "backend", "api", "server"],
            "desktop": ["desktop", "gui", "window", "app"],
            "game": ["game", "unity", "godot", "unreal", "pygame"],
            "ai": ["ai", "ml", "model", "agent", "chatbot", "llm"],
            "mobile": ["mobile", "android", "ios", "flutter", "react native"],
            "automation": ["automation", "otomatis", "script", "bot"],
            "data": ["data", "database", "sql", "analytics", "csv"],
            "dependency": ["dependency", "package", "library", "install", "pip", "npm"],
            "execution": ["run", "execute", "jalankan", "test", "build"],
            "git": ["git", "commit", "push", "repo", "github"],
            "unclear": ["maybe", "mungkin", "tidak jelas", "ambigu", "unclear"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_generation_mode(self, tags: list[str]) -> dict[str, str]:
        if "execution" in tags:
            return {
                "mode": "execution_blocked_generation_review",
                "focus": "plan_validation_without_running_commands_or_code",
                "next_gate": "explicit_execution_permission_required_later",
            }
        if "dependency" in tags:
            return {
                "mode": "dependency_review_planning",
                "focus": "list_dependencies_without_installing_or_downloading",
                "next_gate": "dependency_download_permission_required_later",
            }
        if "git" in tags:
            return {
                "mode": "git_action_blocked_planning",
                "focus": "plan_repository_steps_without_git_execution",
                "next_gate": "explicit_git_permission_required_later",
            }
        if "unclear" in tags:
            return {
                "mode": "project_clarification_required",
                "focus": "clarify_project_scope_before_generation",
                "next_gate": "scope_confirmation_required",
            }
        return {
            "mode": "planner_only_project_blueprint",
            "focus": "prepare_project_structure_and_code_blueprint_without_file_write",
            "next_gate": "human_review_required_before_generation",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "generation_ready": False,
            "execution_ready": False,
            "executed": False,
            "project_creation_runtime": False,
            "project_files_written": False,
            "directory_creation": False,
            "file_read": False,
            "file_write": False,
            "file_delete": False,
            "file_modify": False,
            "code_generation_runtime": False,
            "code_execution": False,
            "test_execution": False,
            "command_execution": False,
            "dependency_install": False,
            "package_download": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "internet_search": False,
            "network_action": False,
            "desktop_control": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general coder project generation"
        tags = self.infer_project_tags(normalized_target)
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
            "principle": "plan_review_confirm_before_generation",
            "tags": tags,
            "generation_mode": self.recommended_generation_mode(tags),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def project_request_frame_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("project_request_frame_plan", target)
        plan["request_frame_steps"] = [
            "Clarify project goal, target platform, user workflow, and output format.",
            "Identify required features, optional features, and non-goals.",
            "Identify constraints such as language, framework, runtime, storage, UI, and deployment.",
            "Do not create files, run commands, install dependencies, or generate a project runtime in this sprint.",
        ]
        return plan

    def project_structure_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("project_structure_plan", target)
        plan["structure_steps"] = [
            "Propose top-level directories and their responsibilities.",
            "Separate source code, tests, docs, assets, config, and scripts when needed.",
            "Mark every proposed path as blueprint-only until Kiput approves generation.",
            "Do not create directories or write files in this sprint.",
        ]
        return plan

    def code_file_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("code_file_blueprint_plan", target)
        plan["blueprint_steps"] = [
            "Propose code files and describe each file's responsibility.",
            "Plan interfaces, classes, functions, configuration, and data flow at a high level.",
            "Separate generated-code proposal from actual file writing.",
            "Do not execute, test, or write generated code in this sprint.",
        ]
        return plan

    def dependency_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dependency_plan", target)
        plan["dependency_steps"] = [
            "List possible standard-library options first.",
            "List optional external packages only as proposals.",
            "Explain why each dependency may be needed and what risk it adds.",
            "Require explicit download/install permission before any future package installation.",
        ]
        return plan

    def generation_review_gate_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("generation_review_gate_plan", target)
        plan["review_gate_steps"] = [
            "Present project plan before any generation.",
            "Ask Kiput to approve target directory, files, dependencies, and validation steps.",
            "Require explicit confirmation before future file write, command execution, dependency install, or git action.",
            "Block automatic generation when scope, dependencies, or target path are unclear.",
        ]
        plan["confirmation_template"] = (
            "Kiput, AURA sudah punya blueprint project. "
            "AURA belum akan membuat file atau menjalankan command. Mau review dulu?"
        )
        return plan

    def validation_strategy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("validation_strategy_plan", target)
        plan["validation_steps"] = [
            "Plan static checks such as syntax, lint, import, or config validation.",
            "Plan minimal runtime checks only as future proposals.",
            "Separate validation plan from command execution.",
            "Do not run tests, builds, interpreters, shells, package managers, or external tools in this sprint.",
        ]
        return plan

    def project_generation_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("project_generation_safety_plan", target)
        plan["safety_steps"] = [
            "Never create projects, directories, files, or code runtime in this sprint.",
            "Never read, write, modify, or delete files as part of project generation in this sprint.",
            "Never run commands, tests, generated code, package installs, downloads, tools, network actions, desktop actions, memory writes, or git operations.",
            "Require explicit permission before future file writes, command execution, dependency install, package download, network action, or git action.",
            "Keep all generated project output as reviewable plans and blueprints.",
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
            "coder_project_plan_types": self.coder_project_plan_types(),
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
            "project_request_frame_plan_ready": True,
            "project_structure_plan_ready": True,
            "code_file_blueprint_plan_ready": True,
            "dependency_plan_ready": True,
            "generation_review_gate_plan_ready": True,
            "validation_strategy_plan_ready": True,
            "project_generation_safety_plan_ready": True,
            "context_ready": True,
            "coder_project_plan_types": self.coder_project_plan_types(),
            "plan_type_count": len(self.coder_project_plan_types()),
            **boundary,
        }
