
"""Dependency and download permission gate for AURA Genesis.

Planner-only layer for future dependency, package, installer, model, asset,
and external download decisions. It prepares how AURA should review package
requests, source trust, install commands, risk, offline alternatives, and
permission gates before any download, install, command execution, network
action, file write, tool execution, or external action.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class DependencyDownloadPermissionGateManager:
    """Prepare safe planner-only dependency/download permission gates."""

    name = "dependency_download_permission_gate"
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

    def dependency_permission_plan_types(self) -> list[str]:
        return [
            "dependency_permission_status",
            "dependency_request_review_plan",
            "package_source_review_plan",
            "download_permission_plan",
            "install_command_review_plan",
            "dependency_risk_plan",
            "offline_alternative_plan",
            "dependency_permission_safety_plan",
            "dependency_permission_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan dependency requests without installing packages.",
            "Plan package/source trust review without network access.",
            "Plan download permission prompts without downloading anything.",
            "Plan install command review without running commands.",
            "Plan dependency risk review before future approval.",
            "Plan offline or standard-library alternatives first.",
            "Keep all outputs planner-only, proposal-only, metadata-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "dependency_install",
            "package_download",
            "model_download",
            "asset_download",
            "installer_download",
            "binary_download",
            "network_action",
            "internet_search",
            "package_manager_runtime",
            "dependency_resolution_runtime",
            "download_runtime",
            "install_runtime",
            "pip_execution",
            "npm_execution",
            "apt_execution",
            "uv_execution",
            "poetry_execution",
            "shell_execution",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "external_binary_execution",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "memory_write",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def infer_dependency_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "python": ["python", "pip", "venv", "uv", "poetry", "requirements"],
            "node": ["node", "npm", "pnpm", "yarn", "package.json"],
            "system": ["apt", "sudo", "system package", "driver", "binary"],
            "model": ["model", "weights", "checkpoint", "onnx", "gguf", "safetensors"],
            "asset": ["asset", "image", "texture", "audio", "video", "dataset"],
            "download": ["download", "unduh", "curl", "wget", "fetch"],
            "install": ["install", "pasang", "setup", "installer"],
            "security": ["malware", "unsafe", "risk", "vulnerability", "supply chain"],
            "network": ["url", "http", "https", "github", "internet", "network"],
            "command": ["run", "execute", "command", "shell", "terminal", "jalankan"],
            "unclear": ["maybe", "mungkin", "tidak jelas", "ambigu", "unclear"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_permission_mode(self, tags: list[str]) -> dict[str, str]:
        if "command" in tags or "install" in tags:
            return {
                "mode": "install_command_permission_gate",
                "focus": "review_install_command_without_execution",
                "next_gate": "explicit_install_and_command_permission_required",
            }
        if "download" in tags or "network" in tags or "model" in tags or "asset" in tags:
            return {
                "mode": "download_permission_gate",
                "focus": "review_source_size_license_and_risk_without_download",
                "next_gate": "explicit_download_permission_required",
            }
        if "security" in tags:
            return {
                "mode": "dependency_risk_review",
                "focus": "review_supply_chain_security_and_safety_before_approval",
                "next_gate": "risk_acceptance_required",
            }
        if "unclear" in tags:
            return {
                "mode": "dependency_clarification_required",
                "focus": "clarify_dependency_need_source_and_scope_before_permission",
                "next_gate": "scope_confirmation_required",
            }
        return {
            "mode": "planner_only_dependency_review",
            "focus": "prepare_dependency_review_without_install_download_or_network",
            "next_gate": "human_review_required",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "permission_ready": False,
            "execution_ready": False,
            "executed": False,
            "dependency_install": False,
            "package_download": False,
            "model_download": False,
            "asset_download": False,
            "installer_download": False,
            "binary_download": False,
            "network_action": False,
            "internet_search": False,
            "package_manager_runtime": False,
            "dependency_resolution_runtime": False,
            "download_runtime": False,
            "install_runtime": False,
            "pip_execution": False,
            "npm_execution": False,
            "apt_execution": False,
            "uv_execution": False,
            "poetry_execution": False,
            "shell_execution": False,
            "command_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "external_binary_execution": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "memory_write": False,
            "desktop_control": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general dependency download permission"
        tags = self.infer_dependency_tags(normalized_target)
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
            "principle": "review_source_risk_permission_before_download_or_install",
            "tags": tags,
            "permission_mode": self.recommended_permission_mode(tags),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def dependency_request_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dependency_request_review_plan", target)
        plan["request_review_steps"] = [
            "Clarify why the dependency, model, asset, binary, or package is needed.",
            "Check whether the standard library or existing project dependencies are enough.",
            "Separate required dependencies from optional conveniences.",
            "Do not install, download, search internet, write files, or run commands in this sprint.",
        ]
        return plan

    def package_source_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("package_source_review_plan", target)
        plan["source_review_steps"] = [
            "Plan source review for official registry, publisher, repository, license, popularity, and maintenance.",
            "Flag unknown URLs, unofficial mirrors, binary installers, and unpinned versions for manual review.",
            "Require source trust review before any future network/download action.",
            "Do not access network, fetch URLs, or inspect remote packages in this sprint.",
        ]
        return plan

    def download_permission_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("download_permission_plan", target)
        plan["download_permission_steps"] = [
            "Explain what would be downloaded, from where, why it is needed, and expected risk.",
            "Ask Kiput for explicit permission before any future download.",
            "Separate package download, model download, asset download, installer download, and binary download.",
            "Keep all downloads disabled in this sprint.",
        ]
        plan["permission_prompt_template"] = (
            "Kiput, AURA perlu izin sebelum download/install: <item>. "
            "Sumber: <source>. Alasan: <reason>. Mau lanjut nanti?"
        )
        return plan

    def install_command_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("install_command_review_plan", target)
        plan["install_review_steps"] = [
            "Plan review of install commands before future execution.",
            "Identify package manager, command scope, target environment, and possible system impact.",
            "Require explicit permission before pip, npm, apt, uv, poetry, shell, or any command execution.",
            "Do not run installers, package managers, shells, tests, builds, or commands in this sprint.",
        ]
        return plan

    def dependency_risk_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dependency_risk_plan", target)
        plan["risk_steps"] = [
            "Plan review for license risk, supply-chain risk, malware risk, abandoned packages, and excessive permissions.",
            "Prefer pinned versions and minimal dependency surface in future proposals.",
            "Mark risky or unknown packages as requiring manual approval.",
            "Do not trust package names, URLs, binaries, or install commands until reviewed.",
        ]
        return plan

    def offline_alternative_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("offline_alternative_plan", target)
        plan["offline_steps"] = [
            "Check whether existing code, standard library, or already-installed tools can solve the task.",
            "Prefer no-download implementation paths when practical.",
            "List tradeoffs between external dependency and offline/simple implementation.",
            "Do not search internet, inspect installed packages, or read project files in this sprint.",
        ]
        return plan

    def dependency_permission_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dependency_permission_safety_plan", target)
        plan["safety_steps"] = [
            "Never install dependencies, download packages, download models/assets/binaries/installers, or run package managers in this sprint.",
            "Never execute commands, shells, tests, builds, tools, network actions, desktop actions, memory writes, git actions, or external actions.",
            "Never read, write, modify, or delete files as part of dependency permission planning in this sprint.",
            "Require explicit permission before future dependency install, package download, model/asset download, command execution, network action, or git action.",
            "Keep all dependency and download decisions as reviewable plans.",
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
            "dependency_permission_plan_types": self.dependency_permission_plan_types(),
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
            "dependency_request_review_plan_ready": True,
            "package_source_review_plan_ready": True,
            "download_permission_plan_ready": True,
            "install_command_review_plan_ready": True,
            "dependency_risk_plan_ready": True,
            "offline_alternative_plan_ready": True,
            "dependency_permission_safety_plan_ready": True,
            "context_ready": True,
            "dependency_permission_plan_types": self.dependency_permission_plan_types(),
            "plan_type_count": len(self.dependency_permission_plan_types()),
            **boundary,
        }
