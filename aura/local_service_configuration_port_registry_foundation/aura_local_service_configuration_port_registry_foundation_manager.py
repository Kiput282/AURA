"""AURA Service Configuration and Port Registry Foundation.

Sprint 144.

Planner-only, metadata-only, and foundation-only configuration and port registry
foundation for ATLAS local service runtime planning. This defines the future
service configuration scope, read-only config schema, localhost-only binding
policy, port registry schema, reserved port policy, conflict preflight metadata,
environment override boundary, Control Center config card surface, and
permission/audit linkage without reading or writing runtime configuration,
reserving ports, binding ports, opening sockets, starting servers, mutating
environment state, writing files, mutating permissions, writing audit events,
executing tools or commands, connecting ORION, or enabling runtime execution.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class AuraLocalServiceConfigurationPortRegistryFoundationManager:
    """Prepare Sprint 144 service configuration and port registry plans."""

    name = "aura_local_service_configuration_port_registry_foundation"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_service_configuration_port_registry_foundation_status",
        "service_configuration_scope_plan",
        "service_config_schema_plan",
        "service_port_registry_schema_plan",
        "localhost_port_policy_plan",
        "reserved_port_policy_plan",
        "port_conflict_preflight_plan",
        "environment_override_boundary_plan",
        "control_center_config_card_plan",
        "permission_audit_config_link_plan",
        "no_config_port_runtime_activation_plan",
        "local_service_configuration_port_registry_foundation_context",
    ]

    BLUEPRINTS = {
        "service_configuration_scope_items": [
            "service_configuration_purpose_defined",
            "service_configuration_is_future_metadata_contract",
            "service_configuration_safe_idle_default_required",
            "service_configuration_localhost_only_default_required",
            "service_configuration_port_registry_required_before_binding",
            "service_configuration_permission_gate_required",
            "service_configuration_audit_link_required",
            "service_configuration_control_center_visibility_required",
            "service_configuration_manual_activation_review_required",
            "service_configuration_runtime_disabled_now",
        ],
        "service_config_schema_items": [
            "config_schema_service_name_field_defined",
            "config_schema_version_field_defined",
            "config_schema_bind_host_field_defined",
            "config_schema_port_reference_field_defined",
            "config_schema_safe_idle_policy_field_defined",
            "config_schema_health_endpoint_reference_field_defined",
            "config_schema_permission_profile_field_defined",
            "config_schema_audit_profile_field_defined",
            "config_schema_control_center_visibility_field_defined",
            "config_schema_write_runtime_disabled_now",
        ],
        "service_port_registry_schema_items": [
            "port_registry_id_field_defined",
            "port_registry_service_owner_field_defined",
            "port_registry_bind_host_field_defined",
            "port_registry_port_number_field_defined",
            "port_registry_protocol_field_defined",
            "port_registry_status_field_defined",
            "port_registry_risk_classification_field_defined",
            "port_registry_permission_reference_field_defined",
            "port_registry_audit_reference_field_defined",
            "port_registry_persistence_runtime_disabled_now",
        ],
        "localhost_port_policy_items": [
            "localhost_default_bind_host_127_0_0_1_defined",
            "localhost_only_policy_reaffirmed",
            "no_wildcard_bind_allowed",
            "no_lan_bind_allowed_without_future_review",
            "no_public_bind_allowed",
            "no_external_tunnel_allowed_by_default",
            "future_bind_requires_port_registry_entry",
            "future_bind_requires_permission_gate",
            "future_bind_requires_audit_visibility",
            "localhost_policy_runtime_disabled_now",
        ],
        "reserved_port_policy_items": [
            "reserved_port_list_contract_defined",
            "control_center_port_reservation_metadata_defined",
            "health_endpoint_port_reference_metadata_defined",
            "orion_bridge_port_reference_deferred",
            "developer_override_requires_review",
            "privileged_ports_forbidden_by_default",
            "well_known_ports_require_extra_review",
            "port_collision_policy_required",
            "port_release_policy_required_before_runtime",
            "reserved_port_runtime_disabled_now",
        ],
        "port_conflict_preflight_items": [
            "port_conflict_preflight_required_before_binding",
            "preflight_is_future_manual_review_first",
            "preflight_no_network_probe_now",
            "preflight_no_socket_open_now",
            "preflight_no_os_port_scan_now",
            "preflight_conflict_state_schema_defined",
            "preflight_fallback_to_safe_idle_required",
            "preflight_control_center_warning_defined",
            "preflight_audit_reference_required_future",
            "preflight_runtime_disabled_now",
        ],
        "environment_override_boundary_items": [
            "env_override_catalog_defined",
            "env_override_allowed_keys_deferred_until_review",
            "env_override_secret_redaction_required",
            "env_override_no_sensitive_value_echo_required",
            "env_override_no_process_env_mutation_now",
            "env_override_no_dotenv_write_now",
            "env_override_requires_permission_gate_future",
            "env_override_requires_audit_link_future",
            "env_override_control_center_visibility_required",
            "env_override_runtime_disabled_now",
        ],
        "control_center_config_card_items": [
            "control_center_config_card_schema_defined",
            "control_center_bind_host_chip_defined",
            "control_center_port_registry_chip_defined",
            "control_center_port_collision_warning_defined",
            "control_center_safe_idle_config_visibility_defined",
            "control_center_permission_state_visibility_defined",
            "control_center_audit_state_visibility_defined",
            "control_center_config_edit_controls_disabled_now",
            "control_center_port_bind_controls_disabled_now",
            "control_center_card_not_runtime_activation",
        ],
        "permission_audit_config_link_items": [
            "permission_scope_read_project_only_now",
            "config_change_requires_future_permission_request",
            "port_bind_requires_future_permission_request",
            "port_registry_mutation_requires_future_permission_request",
            "audit_reference_for_config_preview_defined",
            "audit_reference_for_port_preview_defined",
            "no_permission_request_created_now",
            "no_permission_grant_applied_now",
            "no_audit_event_written_now",
            "future_config_runtime_requires_permission_audit_review",
        ],
        "no_config_port_runtime_activation_items": [
            "no_config_file_read_runtime",
            "no_config_file_write_runtime",
            "no_port_registry_file_write_runtime",
            "no_port_reserved_runtime",
            "no_port_bound_runtime",
            "no_socket_opened_runtime",
            "no_http_listener_started_runtime",
            "no_service_start_runtime",
            "no_environment_mutation_runtime",
            "no_runtime_execution_feature_enabled_by_config_registry",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_service_configuration_contract_apply",
        "runtime_service_config_read",
        "runtime_service_config_write",
        "runtime_service_config_modify",
        "runtime_port_registry_read",
        "runtime_port_registry_write",
        "runtime_port_registry_modify",
        "runtime_port_reservation_create",
        "runtime_port_reservation_release",
        "runtime_port_conflict_check_execute",
        "runtime_os_port_scan_execute",
        "runtime_socket_open",
        "runtime_port_binding",
        "runtime_network_probe",
        "runtime_http_listener_start",
        "runtime_health_endpoint_server_start",
        "runtime_service_process_start",
        "runtime_service_process_stop",
        "runtime_service_process_restart",
        "runtime_api_server_start",
        "runtime_web_server_start",
        "runtime_dashboard_start",
        "runtime_systemd_unit_create",
        "runtime_systemd_unit_enable",
        "runtime_systemd_unit_start",
        "runtime_environment_read",
        "runtime_environment_write",
        "runtime_environment_mutation",
        "runtime_dotenv_read",
        "runtime_dotenv_write",
        "runtime_secret_read",
        "runtime_permission_request_create",
        "runtime_permission_grant_apply",
        "runtime_permission_mutation",
        "runtime_audit_writer_start",
        "runtime_audit_event_write",
        "runtime_audit_log_append",
        "runtime_action_dispatch",
        "runtime_action_execution",
        "runtime_tool_execution",
        "runtime_command_execution",
        "runtime_file_read",
        "runtime_file_write",
        "runtime_file_modify",
        "runtime_file_delete",
        "runtime_memory_read",
        "runtime_memory_write",
        "runtime_model_request_execute",
        "runtime_orion_handshake",
        "runtime_git_operation",
        "api_server_runtime",
        "web_server_runtime",
        "frontend_runtime",
        "backend_runtime",
        "dashboard_runtime",
        "control_center_runtime",
        "chat_runtime",
        "memory_runtime",
        "permission_runtime",
        "audit_runtime",
        "model_runtime",
        "local_service_runtime",
        "service_runtime",
        "health_endpoint_runtime",
        "port_registry_runtime",
        "configuration_runtime",
        "orion_client_runtime",
        "safe_action_runtime",
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
        "git_commit",
        "git_push",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_service_configuration_plans_applied",
        "runtime_config_files_read",
        "runtime_config_files_written",
        "runtime_config_files_modified",
        "runtime_port_registry_reads",
        "runtime_port_registry_writes",
        "runtime_port_registry_modifications",
        "runtime_ports_reserved",
        "runtime_ports_released",
        "runtime_port_conflict_checks_executed",
        "runtime_os_port_scans_executed",
        "runtime_sockets_opened",
        "runtime_ports_bound",
        "runtime_network_probes",
        "runtime_http_listeners_started",
        "runtime_health_endpoint_servers_started",
        "runtime_services_started",
        "runtime_services_stopped",
        "runtime_services_restarted",
        "runtime_api_servers_started",
        "runtime_web_servers_started",
        "runtime_dashboards_started",
        "runtime_systemd_units_created",
        "runtime_systemd_units_enabled",
        "runtime_systemd_units_started",
        "runtime_environment_reads",
        "runtime_environment_writes",
        "runtime_environment_mutations",
        "runtime_dotenv_reads",
        "runtime_dotenv_writes",
        "runtime_secret_reads",
        "runtime_permission_requests_created",
        "runtime_permission_grants_applied",
        "runtime_permission_mutations",
        "runtime_audit_writers_started",
        "runtime_audit_events_written",
        "runtime_audit_logs_appended",
        "runtime_actions_dispatched",
        "runtime_actions_executed",
        "runtime_tools_executed",
        "runtime_commands_executed",
        "runtime_files_read",
        "runtime_files_written",
        "runtime_files_modified",
        "runtime_files_deleted",
        "runtime_memory_reads",
        "runtime_memory_writes",
        "runtime_model_requests_executed",
        "runtime_orion_handshakes",
        "runtime_git_operations",
        "runtime_execution_features",
    ]

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

    def _items(self, key: str) -> list[dict[str, Any]]:
        return [
            {
                "id": item,
                "configuration_port_registry_foundation_only": True,
                "runtime_enabled": False,
            }
            for item in self.BLUEPRINTS[key]
        ]

    def _runtime_false_flags(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _runtime_zero_counters(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "local_service_configuration_port_registry_foundation_only": True,
            "service_configuration_blueprint_only": True,
            "port_registry_blueprint_only": True,
            "configuration_runtime_disabled": True,
            "port_registry_runtime_disabled": True,
            "port_reservation_runtime_disabled": True,
            "port_conflict_preflight_runtime_disabled": True,
            "environment_override_runtime_disabled": True,
            "service_start_runtime_disabled": True,
            "health_endpoint_runtime_disabled": True,
            "http_listener_runtime_disabled": True,
            "socket_runtime_disabled": True,
            "port_binding_disabled": True,
            "network_probe_disabled": True,
            "systemd_runtime_disabled": True,
            "permission_runtime_disabled": True,
            "audit_runtime_disabled": True,
            "action_dispatch_disabled": True,
            "action_execution_disabled": True,
            "tool_execution_disabled": True,
            "command_execution_disabled": True,
            "file_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "model_runtime_disabled": True,
            "orion_handshake_runtime_disabled": True,
            "git_runtime_disabled": True,
            "localhost_only_policy": True,
            "public_network_exposure_disabled": True,
            "safe_idle_default": True,
            "read_only_metadata_contract": True,
            "review_only": True,
            "release_gate_closed": True,
            "foundation_only": True,
            "planner_only": True,
            "metadata_only": True,
            "manual_approval_required_for_future_configuration_port_runtime": True,
            **self._runtime_false_flags(),
        }

    def summary(self) -> dict[str, Any]:
        counts = {f"{key}_count": len(value) for key, value in self.BLUEPRINTS.items()}
        return {
            "local_service_configuration_port_registry_foundation_ready": True,
            "service_configuration_scope_plan_ready": True,
            "service_config_schema_plan_ready": True,
            "service_port_registry_schema_plan_ready": True,
            "localhost_port_policy_plan_ready": True,
            "reserved_port_policy_plan_ready": True,
            "port_conflict_preflight_plan_ready": True,
            "environment_override_boundary_plan_ready": True,
            "control_center_config_card_plan_ready": True,
            "permission_audit_config_link_plan_ready": True,
            "no_config_port_runtime_activation_plan_ready": True,
            **counts,
            "total_local_service_configuration_port_registry_foundation_blueprint_count": sum(counts.values()),
            **self._runtime_zero_counters(),
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": " ".join(str(target or "AURA service configuration and port registry foundation").split()),
            "principle": "Sprint 144 defines the future service configuration and port registry foundation for AURA on ATLAS. The configuration and port registry contracts are localhost-first, metadata-only, safe-idle-aware, permission/audit-linked, and Control Center visible by design. They must not read or write runtime configuration, reserve or bind ports, open sockets, start servers, mutate environment variables, write files, create permissions, write audit events, dispatch actions, execute tools or commands, perform ORION handshakes, or enable runtime execution features.",
            "plan_types": self.PLAN_TYPES,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def service_configuration_scope_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_configuration_scope_plan", target)
        plan["service_configuration_scope_items"] = self._items("service_configuration_scope_items")
        return plan

    def service_config_schema_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_config_schema_plan", target)
        plan["service_config_schema_items"] = self._items("service_config_schema_items")
        return plan

    def service_port_registry_schema_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("service_port_registry_schema_plan", target)
        plan["service_port_registry_schema_items"] = self._items("service_port_registry_schema_items")
        return plan

    def localhost_port_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("localhost_port_policy_plan", target)
        plan["localhost_port_policy_items"] = self._items("localhost_port_policy_items")
        return plan

    def reserved_port_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("reserved_port_policy_plan", target)
        plan["reserved_port_policy_items"] = self._items("reserved_port_policy_items")
        return plan

    def port_conflict_preflight_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("port_conflict_preflight_plan", target)
        plan["port_conflict_preflight_items"] = self._items("port_conflict_preflight_items")
        return plan

    def environment_override_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("environment_override_boundary_plan", target)
        plan["environment_override_boundary_items"] = self._items("environment_override_boundary_items")
        return plan

    def control_center_config_card_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("control_center_config_card_plan", target)
        plan["control_center_config_card_items"] = self._items("control_center_config_card_items")
        return plan

    def permission_audit_config_link_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_audit_config_link_plan", target)
        plan["permission_audit_config_link_items"] = self._items("permission_audit_config_link_items")
        return plan

    def no_config_port_runtime_activation_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("no_config_port_runtime_activation_plan", target)
        plan["no_config_port_runtime_activation_items"] = self._items("no_config_port_runtime_activation_items")
        return plan

    def context(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "plan_types": self.PLAN_TYPES,
            "blueprints": self.BLUEPRINTS,
            "summary": self.summary(),
            **self.safety_boundary(),
        }

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "context_ready": True,
            "local_service_configuration_port_registry_foundation_data_ready": True,
            "plan_types": self.PLAN_TYPES,
            "plan_type_count": len(self.PLAN_TYPES),
            **self.summary(),
            **self.safety_boundary(),
        }
