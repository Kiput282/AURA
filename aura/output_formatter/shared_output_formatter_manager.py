
"""Shared output formatter foundation for AURA.

This module provides planner-safe, renderer-only formatting helpers for
CLI, shell, future service monitor output, and the future AURA Control
Center. It does not execute commands, read/write project files at runtime,
call tools, install dependencies, access the network, or perform external
actions.
"""
from __future__ import annotations

from typing import Any


class SharedOutputFormatterManager:
    """Render consistent AURA text packets without runtime side effects."""

    name = "shared_output_formatter"
    version = "0.1.0"
    status_name = "online"

    def formatter_plan_types(self) -> list[str]:
        return [
            "shared_output_formatter_status",
            "packet_render_plan",
            "safety_boundary_render_plan",
            "cli_output_format_plan",
            "shell_output_format_plan",
            "console_output_format_plan",
            "ui_output_contract_plan",
            "formatter_migration_plan",
            "shared_output_formatter_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Render consistent key-value packet output.",
            "Render consistent title/header output.",
            "Render compact summaries for list and dictionary values.",
            "Render safety boundary sections in a predictable order.",
            "Provide shared output contracts for CLI, shell, service monitor, and future Control Center UI.",
            "Prepare formatter migration plans without changing existing runtime behavior automatically.",
            "Keep formatting renderer-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "runtime_behavior_change",
            "automatic_cli_refactor",
            "automatic_shell_refactor",
            "ui_runtime",
            "web_server_runtime",
            "chat_runtime",
            "service_runtime",
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

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "foundation_only": True,
            "formatter_ready": True,
            "renderer_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "runtime_behavior_change": False,
            "automatic_cli_refactor": False,
            "automatic_shell_refactor": False,
            "ui_runtime": False,
            "web_server_runtime": False,
            "chat_runtime": False,
            "service_runtime": False,
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

    def normalize_text(self, text: Any) -> str:
        return " ".join(str(text or "").strip().split())

    def label_for_key(self, key: str) -> str:
        normalized = self.normalize_text(str(key).replace("_", " "))
        return normalized.title() if normalized else "Unknown"

    def is_scalar(self, value: Any) -> bool:
        return isinstance(value, (str, int, float, bool)) or value is None

    def summarize_value(self, value: Any) -> str:
        if self.is_scalar(value):
            return str(value)
        if isinstance(value, list):
            return f"{len(value)} item(s)"
        if isinstance(value, tuple):
            return f"{len(value)} item(s)"
        if isinstance(value, set):
            return f"{len(value)} item(s)"
        if isinstance(value, dict):
            return f"{len(value)} field(s)"
        return type(value).__name__

    def render_title_lines(self, title: str) -> list[str]:
        clean_title = self.normalize_text(title) or "AURA Output"
        return [clean_title, "=" * len(clean_title)]

    def render_key_value_lines(self, packet: dict[str, Any], label_width: int = 56) -> list[str]:
        lines: list[str] = []
        for key, value in packet.items():
            label = self.label_for_key(key)
            summary = self.summarize_value(value)
            lines.append(f"{label:<{label_width}}: {summary}")
        return lines

    def default_safety_keys(self) -> list[str]:
        return [
            "foundation_only",
            "formatter_ready",
            "renderer_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "runtime_behavior_change",
            "automatic_cli_refactor",
            "automatic_shell_refactor",
            "ui_runtime",
            "web_server_runtime",
            "chat_runtime",
            "service_runtime",
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

    def render_safety_boundary_lines(
        self,
        packet: dict[str, Any],
        title: str = "AURA Safety Boundary",
        label_width: int = 56,
        safety_keys: list[str] | None = None,
    ) -> list[str]:
        keys = safety_keys or self.default_safety_keys()
        lines = ["", title, "-" * len(title)]
        for key in keys:
            if key in packet:
                label = self.label_for_key(key)
                lines.append(f"{label:<{label_width}}: {packet[key]}")
        return lines

    def render_packet_lines(
        self,
        title: str,
        packet: dict[str, Any],
        include_safety_boundary: bool = True,
        safety_title: str = "AURA Safety Boundary",
    ) -> list[str]:
        lines = []
        lines.extend(self.render_title_lines(title))
        lines.extend(self.render_key_value_lines(packet))
        if include_safety_boundary:
            lines.extend(self.render_safety_boundary_lines(packet, title=safety_title))
        return lines

    def render_packet_text(
        self,
        title: str,
        packet: dict[str, Any],
        include_safety_boundary: bool = True,
        safety_title: str = "AURA Safety Boundary",
    ) -> str:
        return "\n".join(
            self.render_packet_lines(
                title=title,
                packet=packet,
                include_safety_boundary=include_safety_boundary,
                safety_title=safety_title,
            )
        )

    def sample_packet(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "target": "CLI / shell / service monitor / future Control Center output",
            "formatter_ready": True,
            "renderer_only": True,
            "example_items": ["status", "capabilities", "safety_boundary"],
            "example_summary": {
                "cli": "supported",
                "shell": "supported",
                "control_center": "planned",
            },
            **boundary,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "shared AURA output formatting"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "format_once_reuse_across_cli_shell_service_console",
            "formatter_plan_types": self.formatter_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def packet_render_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("packet_render_plan", target)
        plan["render_steps"] = [
            "Normalize packet keys into human-readable labels.",
            "Render scalar values directly.",
            "Render list, tuple, set, and dictionary values as compact summaries.",
            "Append a safety boundary section when requested.",
            "Return plain text lines suitable for CLI, shell, service monitor, and future UI bridges.",
        ]
        return plan

    def safety_boundary_render_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("safety_boundary_render_plan", target)
        plan["render_steps"] = [
            "Use a stable safety-key order across modules.",
            "Show positive foundation/planner/metadata states first.",
            "Show disabled runtime, execution, file, command, network, tool, desktop, and git states after.",
            "Avoid hiding risky fields when they are present in a packet.",
        ]
        return plan

    def cli_output_format_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("cli_output_format_plan", target)
        plan["migration_steps"] = [
            "Keep existing CLI commands stable.",
            "Introduce shared formatter usage gradually for new commands first.",
            "Migrate repeated print_packet helpers only after validation.",
            "Avoid changing command semantics during formatter migration.",
        ]
        return plan

    def shell_output_format_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("shell_output_format_plan", target)
        plan["migration_steps"] = [
            "Keep existing shell command behavior stable.",
            "Use shared formatter for new shell packet rendering.",
            "Migrate repeated shell output helpers after CLI behavior is stable.",
            "Keep output readable in terminal and local console contexts.",
        ]
        return plan

    def console_output_format_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("console_output_format_plan", target)
        plan["console_targets"] = [
            "AURA Control Center dashboard cards.",
            "Chat console status blocks.",
            "Permission center request details.",
            "Plugin manager capability summaries.",
            "Service monitor health output.",
            "Action log detail views.",
        ]
        return plan

    def ui_output_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("ui_output_contract_plan", target)
        plan["contract_fields"] = [
            "title",
            "status",
            "version",
            "mode",
            "summary",
            "capabilities",
            "safety_boundary",
            "actions",
            "logs",
        ]
        plan["ui_rule"] = "UI may display formatter output, but must not convert display rendering into permission approval or runtime action."
        return plan

    def formatter_migration_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("formatter_migration_plan", target)
        plan["migration_order"] = [
            "New Sprint 81 formatter commands.",
            "Checkpoint and permission-style packet printers.",
            "Repeated CLI packet helpers.",
            "Repeated shell packet helpers.",
            "Future service monitor output.",
            "Future AURA Control Center data bridge.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "formatter_plan_types": self.formatter_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "sample_packet": self.sample_packet(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "formatter_ready": True,
            "renderer_only": True,
            "planner_ready": True,
            "packet_render_plan_ready": True,
            "safety_boundary_render_plan_ready": True,
            "cli_output_format_plan_ready": True,
            "shell_output_format_plan_ready": True,
            "console_output_format_plan_ready": True,
            "ui_output_contract_plan_ready": True,
            "formatter_migration_plan_ready": True,
            "context_ready": True,
            "formatter_plan_types": self.formatter_plan_types(),
            "plan_type_count": len(self.formatter_plan_types()),
            "runtime_execution_features": 0,
            **boundary,
        }
