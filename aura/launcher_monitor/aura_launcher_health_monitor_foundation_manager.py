
"""AURA Launcher & Health Monitor Foundation.

Planner-only launcher and health monitor foundation for preparing safe_idle
launch planning, start/stop/restart/status/logs planning, health monitor
planning, and future AURA Control Center service monitor data.

This module does not start processes, stop processes, restart processes,
execute commands, run systemctl, create services, read log files, bind ports,
open UI, run a web server, launch chat runtime, or perform external actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraLauncherHealthMonitorFoundationManager:
    """Prepare launcher and health monitor plans without controlling runtime."""

    name = "aura_launcher_health_monitor_foundation"
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

    def normalize_text(self, text: Any) -> str:
        return " ".join(str(text or "").strip().split())

    def launcher_plan_types(self) -> list[str]:
        return [
            "launcher_health_status",
            "launcher_start_plan",
            "launcher_stop_plan",
            "launcher_restart_plan",
            "launcher_status_plan",
            "launcher_log_view_plan",
            "health_monitor_plan",
            "control_center_service_monitor_plan",
            "launcher_safety_policy_plan",
            "launcher_health_context",
        ]

    def launcher_modes(self) -> list[str]:
        return [
            "safe_idle",
            "manual_start_planned",
            "monitor_only",
            "disabled",
        ]

    def launcher_actions(self) -> list[str]:
        return [
            "start_planned",
            "stop_planned",
            "restart_planned",
            "status_planned",
            "logs_planned",
            "health_check_planned",
        ]

    def health_states(self) -> list[str]:
        return [
            "healthy_planned",
            "degraded_planned",
            "unhealthy_planned",
            "unknown_planned",
            "offline_planned",
        ]

    def monitor_fields(self) -> list[str]:
        return [
            "service_status",
            "boot_mode",
            "launch_mode",
            "identity_version",
            "server_name",
            "safe_idle_required",
            "runtime_actions_locked",
            "permission_workflow_ready",
            "capability_registry_ready",
            "runtime_service_foundation_ready",
            "last_health_check_planned",
            "last_log_line_planned",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare launcher start planning without starting a process.",
            "Prepare launcher stop planning without stopping a process.",
            "Prepare launcher restart planning without restarting a process.",
            "Prepare status view planning without querying a real service.",
            "Prepare log view planning without reading log files.",
            "Prepare health monitor fields for future service visibility.",
            "Prepare Control Center service monitor data.",
            "Keep launch policy safe_idle-only and never auto-action.",
            "Keep the launcher foundation planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "launcher_runtime",
            "health_monitor_runtime",
            "service_runtime",
            "process_start",
            "process_stop",
            "process_restart",
            "background_process_start",
            "systemctl_execution",
            "systemd_enable",
            "systemd_start",
            "systemd_stop",
            "systemd_restart",
            "service_control_runtime",
            "log_file_read",
            "log_file_write",
            "auto_boot_runtime",
            "port_binding",
            "web_server_runtime",
            "ui_runtime",
            "chat_runtime",
            "permission_grant_runtime",
            "runtime_action_activation",
            "runtime_behavior_change",
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
            "launcher_foundation_only": True,
            "health_monitor_foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "launcher_monitor_data_ready": True,
            "launcher_runtime": False,
            "health_monitor_runtime": False,
            "service_runtime": False,
            "process_start": False,
            "process_stop": False,
            "process_restart": False,
            "background_process_start": False,
            "systemctl_execution": False,
            "systemd_enable": False,
            "systemd_start": False,
            "systemd_stop": False,
            "systemd_restart": False,
            "service_control_runtime": False,
            "log_file_read": False,
            "log_file_write": False,
            "auto_boot_runtime": False,
            "port_binding": False,
            "web_server_runtime": False,
            "ui_runtime": False,
            "chat_runtime": False,
            "permission_grant_runtime": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
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

    def launcher_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "launcher_name": "aura-launcher",
            "display_name": "AURA Launcher & Health Monitor",
            "server_name": "ATLAS",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_launch_mode": "safe_idle",
            "default_monitor_mode": "metadata_only",
            "service_name": "aura.service",
            "auto_action_allowed": False,
        }

    def launcher_summary(self) -> dict[str, Any]:
        return {
            "launcher_foundation_ready": True,
            "health_monitor_foundation_ready": True,
            "launcher_identity_ready": True,
            "safe_idle_launch_policy_ready": True,
            "start_plan_ready": True,
            "stop_plan_ready": True,
            "restart_plan_ready": True,
            "status_plan_ready": True,
            "log_view_plan_ready": True,
            "health_monitor_plan_ready": True,
            "control_center_service_monitor_plan_ready": True,
            "launcher_safety_policy_plan_ready": True,
            "launcher_mode_count": len(self.launcher_modes()),
            "launcher_action_count": len(self.launcher_actions()),
            "health_state_count": len(self.health_states()),
            "monitor_field_count": len(self.monitor_fields()),
            "runtime_enabled_launchers": 0,
            "processes_started": 0,
            "processes_stopped": 0,
            "processes_restarted": 0,
            "systemctl_commands_executed": 0,
            "log_files_read": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA launcher and health monitor foundation"
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "launcher_may_prepare_safe_idle_visibility_but_must_not_control_runtime",
            "launcher_identity": self.launcher_identity(),
            "launcher_plan_types": self.launcher_plan_types(),
            "launcher_summary": self.launcher_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def launcher_start_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_start_plan", target)
        plan["start_steps"] = [
            "Verify requested launch mode is safe_idle.",
            "Prepare identity/version visibility.",
            "Prepare capability registry visibility.",
            "Prepare permission workflow visibility.",
            "Prepare runtime service foundation visibility.",
            "Keep all runtime actions locked.",
            "Do not start a process, systemd unit, web server, UI, chat runtime, or launcher runtime.",
        ]
        return plan

    def launcher_stop_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_stop_plan", target)
        plan["stop_steps"] = [
            "Prepare stop request metadata.",
            "Mark stop operation as planned only.",
            "Do not stop a process.",
            "Do not run systemctl stop.",
            "Do not modify service state.",
        ]
        return plan

    def launcher_restart_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_restart_plan", target)
        plan["restart_steps"] = [
            "Prepare restart request metadata.",
            "Require future explicit confirmation before any runtime restart.",
            "Keep pending runtime actions cancelled or requiring new confirmation.",
            "Do not restart a process.",
            "Do not run systemctl restart.",
        ]
        return plan

    def launcher_status_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_status_plan", target)
        plan["status_fields"] = [
            "launcher status",
            "service status",
            "safe_idle mode",
            "runtime lock status",
            "identity version",
            "permission workflow readiness",
            "capability registry readiness",
            "runtime service foundation readiness",
        ]
        plan["status_rule"] = "Status planning does not query a real service or process."
        return plan

    def launcher_log_view_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_log_view_plan", target)
        plan["log_view_fields"] = [
            "planned log source",
            "planned severity",
            "planned timestamp",
            "planned message",
            "planned service name",
            "planned safe_idle state",
        ]
        plan["log_rule"] = "Log view planning does not read, write, tail, or rotate real log files."
        return plan

    def health_monitor_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("health_monitor_plan", target)
        plan["health_states"] = self.health_states()
        plan["monitor_fields"] = self.monitor_fields()
        plan["health_rule"] = "Health monitor planning does not run a background monitor."
        return plan

    def control_center_service_monitor_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("control_center_service_monitor_plan", target)
        plan["control_center_cards"] = [
            "Launcher status",
            "Service status",
            "Safe idle mode",
            "Runtime locks",
            "Health state",
            "Last health check planned",
            "Start plan button",
            "Stop plan button",
            "Restart plan button",
            "Logs plan button",
        ]
        plan["control_center_rule"] = "Control Center may display launcher data only; it must not bypass permission workflow or control runtime."
        return plan

    def launcher_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("launcher_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Launcher must default to safe_idle.",
            "Launcher must not grant permission.",
            "Launcher must not execute queued runtime actions.",
            "Launcher must not run systemctl by itself.",
            "Launcher must not start microphone, camera, screen, web, UI, chat, desktop, git, file, command, network, or plugin runtime.",
            "Runtime control must remain deferred until explicit permission and runtime layers exist.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "launcher_identity": self.launcher_identity(),
            "launcher_plan_types": self.launcher_plan_types(),
            "launcher_modes": self.launcher_modes(),
            "launcher_actions": self.launcher_actions(),
            "health_states": self.health_states(),
            "monitor_fields": self.monitor_fields(),
            "launcher_summary": self.launcher_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.launcher_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "launcher_foundation_ready": True,
            "health_monitor_foundation_ready": True,
            "planner_ready": True,
            "launcher_monitor_data_ready": True,
            "launcher_start_plan_ready": True,
            "launcher_stop_plan_ready": True,
            "launcher_restart_plan_ready": True,
            "launcher_status_plan_ready": True,
            "launcher_log_view_plan_ready": True,
            "health_monitor_plan_ready": True,
            "control_center_service_monitor_plan_ready": True,
            "launcher_safety_policy_plan_ready": True,
            "context_ready": True,
            "launcher_plan_types": self.launcher_plan_types(),
            "plan_type_count": len(self.launcher_plan_types()),
            **summary,
            **boundary,
        }
