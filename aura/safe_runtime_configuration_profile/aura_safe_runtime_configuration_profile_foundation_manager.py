
"""AURA Safe Runtime Configuration Profile Foundation.

Planner-only/configuration-blueprint-only foundation for Sprint 102.
It prepares safe runtime configuration profile blueprints without writing
config files, applying runtime profiles, starting services, binding ports,
changing permissions, activating dry-run, dispatching actions, executing
tools/commands, connecting ORION, writing memory, or performing git runtime.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraSafeRuntimeConfigurationProfileFoundationManager:
    """Prepare safe runtime configuration profiles without applying runtime config."""

    name = "aura_safe_runtime_configuration_profile_foundation"
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

    def configuration_plan_types(self) -> list[str]:
        return [
            "safe_runtime_configuration_profile_status",
            "configuration_profile_type_plan",
            "runtime_mode_policy_plan",
            "service_configuration_boundary_plan",
            "permission_configuration_boundary_plan",
            "file_system_configuration_boundary_plan",
            "network_configuration_boundary_plan",
            "dry_run_configuration_requirement_plan",
            "rollout_configuration_guard_plan",
            "configuration_audit_visibility_plan",
            "safe_runtime_configuration_profile_context",
        ]

    def profile_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "profile_name": "AURA Safe Runtime Configuration Profile Foundation",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "profile_scope": "sprint_102_safe_runtime_configuration_profile",
            "source_baseline": "sprint_101_genesis_runtime_readiness_baseline",
            "default_mode": "safe_runtime_configuration_blueprint_only",
            "runtime_mode": "configuration_planning_only",
            "configuration_authority": "ATLAS",
            "future_executor": "ATLAS_or_ORION_only_after_future_explicit_approval",
            "runtime_config_write_allowed": False,
            "runtime_config_apply_allowed": False,
            "runtime_profile_activation_allowed": False,
            "service_start_allowed": False,
            "port_binding_allowed": False,
            "permission_change_allowed": False,
            "file_system_runtime_allowed": False,
            "network_probe_allowed": False,
            "dry_run_activation_allowed": False,
            "action_dispatch_allowed": False,
            "tool_execution_allowed": False,
            "git_runtime_allowed": False,
        }

    def configuration_profile_types(self) -> list[dict[str, Any]]:
        return [
            {"id": "safe_idle_profile", "purpose": "Default non-runtime posture.", "runtime_enabled": False},
            {"id": "metadata_only_profile", "purpose": "Status and metadata visibility only.", "runtime_enabled": False},
            {"id": "review_only_profile", "purpose": "Review packet and checklist planning only.", "runtime_enabled": False},
            {"id": "dry_run_preview_profile", "purpose": "Future preview-only dry-run profile.", "runtime_enabled": False},
            {"id": "mock_runtime_contract_profile", "purpose": "Future mock contract profile.", "runtime_enabled": False},
            {"id": "local_service_proposal_profile", "purpose": "Future proposal-only local service profile.", "runtime_enabled": False},
            {"id": "limited_controlled_runtime_profile", "purpose": "Future controlled runtime candidate profile.", "runtime_enabled": False},
            {"id": "high_risk_runtime_deferred_profile", "purpose": "Explicitly deferred high-risk profile.", "runtime_enabled": False},
        ]

    def runtime_mode_policies(self) -> list[dict[str, Any]]:
        return [
            {"id": "safe_idle_default", "required": True, "runtime_mutation": False},
            {"id": "explicit_mode_selection_required", "required": True, "runtime_mutation": False},
            {"id": "no_implicit_runtime_escalation", "required": True, "runtime_mutation": False},
            {"id": "dry_run_before_runtime", "required": True, "runtime_mutation": False},
            {"id": "permission_before_side_effect", "required": True, "runtime_mutation": False},
            {"id": "audit_visibility_before_runtime", "required": True, "runtime_mutation": False},
            {"id": "rollback_path_before_runtime", "required": True, "runtime_mutation": False},
            {"id": "kill_switch_before_runtime", "required": True, "runtime_mutation": False},
            {"id": "manual_user_review_before_runtime", "required": True, "runtime_mutation": False},
        ]

    def service_configuration_boundaries(self) -> list[dict[str, Any]]:
        return [
            {"id": "service_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "launcher_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "web_server_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "api_server_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "websocket_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "orion_client_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "background_worker_start_disabled_by_default", "enforced": True, "service_started": False},
            {"id": "service_profile_requires_future_approval", "enforced": True, "service_started": False},
        ]

    def permission_configuration_boundaries(self) -> list[dict[str, Any]]:
        return [
            {"id": "read_project_only_for_profile_view", "runtime_permission_changed": False},
            {"id": "no_permission_grant_from_profile", "runtime_permission_changed": False},
            {"id": "no_permission_deny_from_profile", "runtime_permission_changed": False},
            {"id": "no_permission_scope_activation_from_profile", "runtime_permission_changed": False},
            {"id": "no_permission_scope_revocation_from_profile", "runtime_permission_changed": False},
            {"id": "future_runtime_profile_requires_explicit_approval", "runtime_permission_changed": False},
            {"id": "permission_decision_dry_run_only_until_approved", "runtime_permission_changed": False},
            {"id": "high_risk_permission_profile_deferred", "runtime_permission_changed": False},
        ]

    def file_system_configuration_boundaries(self) -> list[dict[str, Any]]:
        return [
            {"id": "config_file_read_disabled", "runtime_file_access": False},
            {"id": "config_file_write_disabled", "runtime_file_access": False},
            {"id": "profile_file_write_disabled", "runtime_file_access": False},
            {"id": "runtime_state_file_write_disabled", "runtime_file_access": False},
            {"id": "file_operation_runtime_disabled", "runtime_file_access": False},
            {"id": "controlled_file_write_dry_run_only", "runtime_file_access": False},
            {"id": "path_probe_disabled", "runtime_file_access": False},
            {"id": "overwrite_disabled", "runtime_file_access": False},
        ]

    def network_configuration_boundaries(self) -> list[dict[str, Any]]:
        return [
            {"id": "port_binding_disabled", "runtime_network_access": False},
            {"id": "localhost_server_disabled", "runtime_network_access": False},
            {"id": "public_interface_binding_disabled", "runtime_network_access": False},
            {"id": "external_tunnel_disabled", "runtime_network_access": False},
            {"id": "network_probe_disabled", "runtime_network_access": False},
            {"id": "internet_search_runtime_disabled", "runtime_network_access": False},
            {"id": "package_download_disabled", "runtime_network_access": False},
            {"id": "api_request_handling_disabled", "runtime_network_access": False},
            {"id": "websocket_runtime_disabled", "runtime_network_access": False},
        ]

    def dry_run_configuration_requirements(self) -> list[dict[str, Any]]:
        return [
            {"id": "dry_run_flag_required", "satisfied_by_default": False},
            {"id": "side_effect_free_output_required", "satisfied_by_default": False},
            {"id": "preview_packet_required", "satisfied_by_default": False},
            {"id": "permission_reference_required", "satisfied_by_default": False},
            {"id": "capability_registry_reference_required", "satisfied_by_default": False},
            {"id": "audit_event_blueprint_required", "satisfied_by_default": False},
            {"id": "cancel_path_required", "satisfied_by_default": False},
            {"id": "user_review_required", "satisfied_by_default": False},
        ]

    def rollout_configuration_guards(self) -> list[dict[str, Any]]:
        return [
            {"id": "phase_0_metadata_only_guard", "active_runtime": False},
            {"id": "phase_1_dry_run_preview_guard", "active_runtime": False},
            {"id": "phase_2_mock_contract_guard", "active_runtime": False},
            {"id": "phase_3_permission_dry_run_guard", "active_runtime": False},
            {"id": "phase_4_service_proposal_guard", "active_runtime": False},
            {"id": "phase_5_limited_runtime_guard", "active_runtime": False},
            {"id": "phase_6_high_risk_deferred_guard", "active_runtime": False},
        ]

    def configuration_audit_visibility_items(self) -> list[dict[str, Any]]:
        return [
            {"id": "profile_name_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "profile_mode_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "profile_risk_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "permission_boundary_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "service_boundary_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "file_boundary_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "network_boundary_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
            {"id": "rollout_guard_visibility", "audit_ready": True, "runtime_audit_stream_started": False},
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare safe runtime configuration profile type planning.",
            "Prepare runtime mode policy planning.",
            "Prepare service configuration boundary planning.",
            "Prepare permission configuration boundary planning.",
            "Prepare file system configuration boundary planning.",
            "Prepare network configuration boundary planning.",
            "Prepare dry-run configuration requirement planning.",
            "Prepare rollout configuration guard planning.",
            "Prepare configuration audit visibility planning.",
            "Expose safe runtime configuration profile status.",
            "Keep configuration profiles blueprint-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "runtime_config_read",
            "runtime_config_write",
            "runtime_config_apply",
            "runtime_profile_activation",
            "runtime_environment_mutation",
            "runtime_service_start",
            "runtime_launcher_start",
            "runtime_web_server_start",
            "runtime_api_server_start",
            "runtime_websocket_start",
            "runtime_orion_client_start",
            "runtime_permission_change",
            "runtime_permission_grant",
            "runtime_permission_deny",
            "runtime_permission_scope_activation",
            "dry_run_activation_runtime",
            "runtime_file_read",
            "runtime_file_write",
            "runtime_network_probe",
            "runtime_port_binding",
            "runtime_action_dispatch",
            "runtime_action_execution",
            "runtime_tool_execution",
            "runtime_command_execution",
            "runtime_audit_stream_start",
            "runtime_memory_write",
            "runtime_git_operation",
            "web_server_runtime",
            "api_server_runtime",
            "frontend_runtime",
            "backend_runtime",
            "orion_client_runtime",
            "desktop_control",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "safe_runtime_configuration_profile_foundation_only": True,
            "configuration_profile_blueprint_only": True,
            "configuration_profile_type_blueprint_only": True,
            "runtime_mode_policy_blueprint_only": True,
            "service_configuration_boundary_blueprint_only": True,
            "permission_configuration_boundary_blueprint_only": True,
            "file_system_configuration_boundary_blueprint_only": True,
            "network_configuration_boundary_blueprint_only": True,
            "dry_run_configuration_requirement_blueprint_only": True,
            "rollout_configuration_guard_blueprint_only": True,
            "configuration_audit_visibility_blueprint_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "safe_runtime_configuration_profile_data_ready": True,
            "runtime_config_read": False,
            "runtime_config_write": False,
            "runtime_config_apply": False,
            "runtime_profile_activation": False,
            "runtime_environment_mutation": False,
            "runtime_service_start": False,
            "runtime_launcher_start": False,
            "runtime_web_server_start": False,
            "runtime_api_server_start": False,
            "runtime_websocket_start": False,
            "runtime_orion_client_start": False,
            "runtime_permission_change": False,
            "runtime_permission_grant": False,
            "runtime_permission_deny": False,
            "runtime_permission_scope_activation": False,
            "dry_run_activation_runtime": False,
            "runtime_file_read": False,
            "runtime_file_write": False,
            "runtime_network_probe": False,
            "runtime_port_binding": False,
            "runtime_action_dispatch": False,
            "runtime_action_execution": False,
            "runtime_tool_execution": False,
            "runtime_command_execution": False,
            "runtime_audit_stream_start": False,
            "runtime_memory_write": False,
            "runtime_git_operation": False,
            "web_server_runtime": False,
            "api_server_runtime": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "orion_client_runtime": False,
            "desktop_control": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "command_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def profile_summary(self) -> dict[str, Any]:
        profile_types = self.configuration_profile_types()
        mode_policies = self.runtime_mode_policies()
        service_boundaries = self.service_configuration_boundaries()
        permission_boundaries = self.permission_configuration_boundaries()
        file_boundaries = self.file_system_configuration_boundaries()
        network_boundaries = self.network_configuration_boundaries()
        dry_run_requirements = self.dry_run_configuration_requirements()
        rollout_guards = self.rollout_configuration_guards()
        audit_items = self.configuration_audit_visibility_items()
        return {
            "safe_runtime_configuration_profile_foundation_ready": True,
            "configuration_profile_type_plan_ready": True,
            "runtime_mode_policy_plan_ready": True,
            "service_configuration_boundary_plan_ready": True,
            "permission_configuration_boundary_plan_ready": True,
            "file_system_configuration_boundary_plan_ready": True,
            "network_configuration_boundary_plan_ready": True,
            "dry_run_configuration_requirement_plan_ready": True,
            "rollout_configuration_guard_plan_ready": True,
            "configuration_audit_visibility_plan_ready": True,
            "configuration_profile_type_count": len(profile_types),
            "runtime_mode_policy_count": len(mode_policies),
            "service_configuration_boundary_count": len(service_boundaries),
            "permission_configuration_boundary_count": len(permission_boundaries),
            "file_system_configuration_boundary_count": len(file_boundaries),
            "network_configuration_boundary_count": len(network_boundaries),
            "dry_run_configuration_requirement_count": len(dry_run_requirements),
            "rollout_configuration_guard_count": len(rollout_guards),
            "configuration_audit_visibility_count": len(audit_items),
            "total_safe_runtime_configuration_blueprint_count": (
                len(profile_types)
                + len(mode_policies)
                + len(service_boundaries)
                + len(permission_boundaries)
                + len(file_boundaries)
                + len(network_boundaries)
                + len(dry_run_requirements)
                + len(rollout_guards)
                + len(audit_items)
            ),
            "runtime_config_profiles_read": 0,
            "runtime_config_profiles_written": 0,
            "runtime_config_profiles_applied": 0,
            "runtime_profile_activations": 0,
            "runtime_environment_mutations": 0,
            "runtime_services_started": 0,
            "runtime_launchers_started": 0,
            "runtime_web_servers_started": 0,
            "runtime_api_servers_started": 0,
            "runtime_websockets_started": 0,
            "runtime_orion_clients_started": 0,
            "runtime_permissions_changed": 0,
            "runtime_permissions_granted": 0,
            "runtime_permissions_denied": 0,
            "runtime_permission_scopes_activated": 0,
            "dry_run_modes_activated": 0,
            "runtime_files_read": 0,
            "runtime_files_written": 0,
            "runtime_network_probes": 0,
            "runtime_ports_bound": 0,
            "runtime_actions_dispatched": 0,
            "runtime_actions_executed": 0,
            "runtime_tools_executed": 0,
            "runtime_commands_executed": 0,
            "runtime_audit_streams_started": 0,
            "runtime_memory_writes": 0,
            "runtime_git_operations": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA safe runtime configuration profile foundation"
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "Safe runtime configuration profiles may define future modes but must not read, write, apply, or activate runtime configuration.",
            "profile_identity": self.profile_identity(),
            "configuration_plan_types": self.configuration_plan_types(),
            "profile_summary": self.profile_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **self.safety_boundary(),
        }

    def configuration_profile_type_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("configuration_profile_type_plan", target)
        plan["configuration_profile_types"] = self.configuration_profile_types()
        return plan

    def runtime_mode_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("runtime_mode_policy_plan", target)
        plan["runtime_mode_policies"] = self.runtime_mode_policies()
        return plan

    def service_configuration_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_configuration_boundary_plan", target)
        plan["service_configuration_boundaries"] = self.service_configuration_boundaries()
        return plan

    def permission_configuration_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_configuration_boundary_plan", target)
        plan["permission_configuration_boundaries"] = self.permission_configuration_boundaries()
        return plan

    def file_system_configuration_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("file_system_configuration_boundary_plan", target)
        plan["file_system_configuration_boundaries"] = self.file_system_configuration_boundaries()
        return plan

    def network_configuration_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("network_configuration_boundary_plan", target)
        plan["network_configuration_boundaries"] = self.network_configuration_boundaries()
        return plan

    def dry_run_configuration_requirement_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dry_run_configuration_requirement_plan", target)
        plan["dry_run_configuration_requirements"] = self.dry_run_configuration_requirements()
        return plan

    def rollout_configuration_guard_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("rollout_configuration_guard_plan", target)
        plan["rollout_configuration_guards"] = self.rollout_configuration_guards()
        return plan

    def configuration_audit_visibility_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("configuration_audit_visibility_plan", target)
        plan["configuration_audit_visibility_items"] = self.configuration_audit_visibility_items()
        return plan

    def safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("safe_runtime_configuration_profile_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Safe runtime configuration profiles must not be read from runtime config files.",
            "Safe runtime configuration profiles must not write runtime config files.",
            "Safe runtime configuration profiles must not apply or activate runtime profiles.",
            "Safe runtime configuration profiles must not start local services, web servers, API servers, websockets, launchers, or ORION clients.",
            "Safe runtime configuration profiles must not change permissions or activate permission scopes.",
            "Safe runtime configuration profiles must not activate dry-run runtime.",
            "Safe runtime configuration profiles must not read/write runtime files, probe networks, bind ports, dispatch actions, run tools/commands, write memory, or perform git operations.",
            "Safe runtime configuration profiles must preserve safe_idle-first and explicit future approval.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "profile_identity": self.profile_identity(),
            "configuration_plan_types": self.configuration_plan_types(),
            "configuration_profile_types": self.configuration_profile_types(),
            "runtime_mode_policies": self.runtime_mode_policies(),
            "service_configuration_boundaries": self.service_configuration_boundaries(),
            "permission_configuration_boundaries": self.permission_configuration_boundaries(),
            "file_system_configuration_boundaries": self.file_system_configuration_boundaries(),
            "network_configuration_boundaries": self.network_configuration_boundaries(),
            "dry_run_configuration_requirements": self.dry_run_configuration_requirements(),
            "rollout_configuration_guards": self.rollout_configuration_guards(),
            "configuration_audit_visibility_items": self.configuration_audit_visibility_items(),
            "profile_summary": self.profile_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **self.safety_boundary(),
        }

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "safe_runtime_configuration_profile_foundation_ready": True,
            "configuration_profile_type_plan_ready": True,
            "runtime_mode_policy_plan_ready": True,
            "service_configuration_boundary_plan_ready": True,
            "permission_configuration_boundary_plan_ready": True,
            "file_system_configuration_boundary_plan_ready": True,
            "network_configuration_boundary_plan_ready": True,
            "dry_run_configuration_requirement_plan_ready": True,
            "rollout_configuration_guard_plan_ready": True,
            "configuration_audit_visibility_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "safe_runtime_configuration_profile_data_ready": True,
            "configuration_plan_types": self.configuration_plan_types(),
            "plan_type_count": len(self.configuration_plan_types()),
            **self.profile_summary(),
            **self.safety_boundary(),
        }
