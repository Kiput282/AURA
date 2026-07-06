
"""AURA Runtime Service Foundation.

Planner-only service foundation for preparing AURA safe_idle boot mode,
service lifecycle planning, health check planning, startup policy planning,
systemd unit planning, and future service monitor data.

This module does not create a systemd service, start a background process,
auto-start AURA, execute commands, write service files, control services,
open network ports, run a web server, launch UI, or perform external actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraRuntimeServiceFoundationManager:
    """Prepare AURA runtime service plans without starting a service."""

    name = "aura_runtime_service_foundation"
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

    def service_plan_types(self) -> list[str]:
        return [
            "runtime_service_status",
            "safe_idle_boot_plan",
            "service_lifecycle_plan",
            "service_health_check_plan",
            "systemd_unit_blueprint_plan",
            "service_recovery_plan",
            "service_monitor_view_plan",
            "auto_boot_policy_plan",
            "runtime_service_context",
        ]

    def boot_modes(self) -> list[str]:
        return [
            "safe_idle",
            "manual_only",
            "maintenance",
            "disabled",
        ]

    def lifecycle_states(self) -> list[str]:
        return [
            "not_installed",
            "planned",
            "stopped_planned",
            "starting_planned",
            "safe_idle_planned",
            "restarting_planned",
            "stopping_planned",
            "failed_planned",
            "disabled_planned",
        ]

    def health_check_fields(self) -> list[str]:
        return [
            "identity_loaded",
            "version_detected",
            "core_boot_ready",
            "safe_idle_mode",
            "permission_workflow_ready",
            "capability_registry_ready",
            "output_formatter_ready",
            "runtime_actions_locked",
            "service_process_running",
            "systemd_unit_installed",
            "auto_boot_enabled",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan AURA safe_idle service boot behavior.",
            "Plan service lifecycle states without controlling a real service.",
            "Plan health check fields for a future launcher and monitor.",
            "Plan systemd unit blueprint metadata without writing service files.",
            "Plan recovery behavior after ATLAS reboot or power loss.",
            "Prepare service monitor data for future AURA Control Center.",
            "Keep auto-boot as safe_idle only and never auto-action.",
            "Keep the service foundation planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "service_runtime",
            "systemd_unit_creation",
            "systemd_enable",
            "systemd_start",
            "systemd_stop",
            "systemd_restart",
            "background_process_start",
            "auto_boot_runtime",
            "port_binding",
            "web_server_runtime",
            "ui_runtime",
            "chat_runtime",
            "launcher_runtime",
            "service_control_runtime",
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
            "service_foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "runtime_service_data_ready": True,
            "service_runtime": False,
            "systemd_unit_creation": False,
            "systemd_enable": False,
            "systemd_start": False,
            "systemd_stop": False,
            "systemd_restart": False,
            "background_process_start": False,
            "auto_boot_runtime": False,
            "port_binding": False,
            "web_server_runtime": False,
            "ui_runtime": False,
            "chat_runtime": False,
            "launcher_runtime": False,
            "service_control_runtime": False,
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

    def service_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "service_name": "aura.service",
            "display_name": "AURA Runtime Service",
            "server_name": "ATLAS",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "motto": identity.get("motto", "Grow Together"),
            "identity_version": identity.get("version"),
            "default_boot_mode": "safe_idle",
            "default_runtime_mode": "locked",
            "auto_action_allowed": False,
        }

    def service_summary(self) -> dict[str, Any]:
        return {
            "service_foundation_ready": True,
            "service_identity_ready": True,
            "safe_idle_boot_ready": True,
            "lifecycle_plan_ready": True,
            "health_check_plan_ready": True,
            "systemd_blueprint_plan_ready": True,
            "recovery_plan_ready": True,
            "service_monitor_view_ready": True,
            "auto_boot_policy_ready": True,
            "boot_mode_count": len(self.boot_modes()),
            "lifecycle_state_count": len(self.lifecycle_states()),
            "health_check_field_count": len(self.health_check_fields()),
            "runtime_enabled_services": 0,
            "systemd_units_created": 0,
            "background_processes_started": 0,
            "auto_boot_runtime_enabled": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA runtime service foundation"
        identity = self.service_identity()
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "aura_may_wake_automatically_but_must_not_act_automatically",
            "service_identity": identity,
            "service_plan_types": self.service_plan_types(),
            "service_summary": self.service_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def safe_idle_boot_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("safe_idle_boot_plan", target)
        plan["boot_steps"] = [
            "Load AURA identity and version metadata.",
            "Load capability registry metadata.",
            "Load permission workflow metadata.",
            "Load output formatter metadata.",
            "Enter safe_idle mode.",
            "Keep all runtime actions locked.",
            "Expose future status data for launcher and Control Center.",
            "Do not execute commands, write files, bind ports, or start runtime adapters.",
        ]
        return plan

    def service_lifecycle_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_lifecycle_plan", target)
        plan["lifecycle_states"] = self.lifecycle_states()
        plan["lifecycle_rule"] = "Lifecycle planning does not start, stop, restart, enable, or disable a real service."
        return plan

    def service_health_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_health_check_plan", target)
        plan["health_check_fields"] = self.health_check_fields()
        plan["health_rule"] = "Health checks are planned metadata until a future launcher/service monitor exists."
        return plan

    def systemd_unit_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("systemd_unit_blueprint_plan", target)
        plan["systemd_blueprint"] = {
            "unit_name": "aura.service",
            "description": "AURA Runtime Service",
            "working_directory": "/home/kiput/Projects/AURA",
            "boot_mode": "safe_idle",
            "restart_policy": "on-failure planned",
            "auto_start": "planned, not enabled",
        }
        plan["systemd_rule"] = "This is a blueprint only. No service file is written and no systemctl command is executed."
        return plan

    def service_recovery_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_recovery_plan", target)
        plan["recovery_steps"] = [
            "After ATLAS reboot, future service should start only in safe_idle.",
            "Verify identity, version, capability registry, and permission workflow.",
            "Keep pending runtime actions cancelled or requiring new confirmation.",
            "Do not resume file, command, download, device, desktop, git, or plugin actions automatically.",
        ]
        return plan

    def service_monitor_view_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_monitor_view_plan", target)
        plan["monitor_cards"] = [
            "Service status",
            "Boot mode",
            "Runtime mode",
            "Version",
            "Server",
            "Uptime planned",
            "Health fields",
            "Runtime locks",
            "Permission workflow status",
            "Capability registry status",
        ]
        return plan

    def auto_boot_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("auto_boot_policy_plan", target)
        plan["auto_boot_rules"] = [
            "Auto-boot may be enabled only for safe_idle.",
            "Auto-boot must not grant permission.",
            "Auto-boot must not execute queued actions.",
            "Auto-boot must not open microphone, camera, screen, network, desktop, git, file, or command runtime.",
            "Manual launcher and monitor must be available before enabling real auto-start.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "service_identity": self.service_identity(),
            "service_plan_types": self.service_plan_types(),
            "boot_modes": self.boot_modes(),
            "lifecycle_states": self.lifecycle_states(),
            "health_check_fields": self.health_check_fields(),
            "service_summary": self.service_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.service_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "service_foundation_ready": True,
            "planner_ready": True,
            "runtime_service_data_ready": True,
            "safe_idle_boot_plan_ready": True,
            "service_lifecycle_plan_ready": True,
            "service_health_check_plan_ready": True,
            "systemd_unit_blueprint_plan_ready": True,
            "service_recovery_plan_ready": True,
            "service_monitor_view_plan_ready": True,
            "auto_boot_policy_plan_ready": True,
            "context_ready": True,
            "service_plan_types": self.service_plan_types(),
            "plan_type_count": len(self.service_plan_types()),
            **summary,
            **boundary,
        }
