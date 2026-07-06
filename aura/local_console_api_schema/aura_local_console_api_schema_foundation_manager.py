
"""AURA Local Console API Schema Foundation.

Planner-only foundation for future Local Console / Control Center API data
contracts. It prepares schema blueprints, endpoint blueprints, response
envelopes, validation rules, permission boundaries, and versioning notes
without creating API routes, starting servers, binding ports, fetching
runtime data, serving web responses, or executing actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraLocalConsoleAPISchemaFoundationManager:
    """Prepare Local Console API schema plans without runtime."""

    name = "aura_local_console_api_schema_foundation"
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

    def api_schema_plan_types(self) -> list[str]:
        return [
            "local_console_api_schema_status",
            "api_schema_catalog_plan",
            "endpoint_blueprint_plan",
            "response_envelope_plan",
            "request_schema_blueprint_plan",
            "validation_rule_plan",
            "permission_boundary_schema_plan",
            "error_contract_plan",
            "schema_versioning_plan",
            "api_schema_safety_policy_plan",
            "local_console_api_schema_context",
        ]

    def schema_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "identity_status_schema",
                "title": "Identity Status Schema",
                "purpose": "Describe AURA identity, version, mode, safe_idle state, and boot status.",
                "source_system": "identity_status",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "chat_session_schema",
                "title": "Chat Session Schema",
                "purpose": "Describe future chat session metadata, active channel, and message summary.",
                "source_system": "chat_bridge",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "capability_registry_schema",
                "title": "Capability Registry Schema",
                "purpose": "Describe capability registry rows, runtime levels, and visibility flags.",
                "source_system": "capability_registry",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "permission_workflow_schema",
                "title": "Permission Workflow Schema",
                "purpose": "Describe permission request queue fields and approval boundaries.",
                "source_system": "permission_workflow",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "runtime_service_schema",
                "title": "Runtime Service Schema",
                "purpose": "Describe service foundation state and safe disabled runtime indicators.",
                "source_system": "runtime_service",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "launcher_health_schema",
                "title": "Launcher Health Schema",
                "purpose": "Describe launcher status, health monitor fields, and boot mode indicators.",
                "source_system": "launcher_health_monitor",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "plugin_permission_dashboard_schema",
                "title": "Plugin Permission Dashboard Schema",
                "purpose": "Describe plugin dashboard cards, permission cards, and action visibility fields.",
                "source_system": "plugin_permission_dashboard",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "action_queue_schema",
                "title": "Action Queue Schema",
                "purpose": "Describe future review-only action queue entries and safety states.",
                "source_system": "runtime_action_queue_future",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "roadmap_schema",
                "title": "Roadmap Schema",
                "purpose": "Describe Genesis, post-Genesis, sprint, and checkpoint roadmap metadata.",
                "source_system": "roadmap_docs",
                "runtime_fetch_enabled": False,
            },
        ]

    def endpoint_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "get_console_status",
                "method": "GET",
                "path": "/api/local-console/status",
                "schema_packet": "identity_status_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_chat",
                "method": "GET",
                "path": "/api/local-console/chat",
                "schema_packet": "chat_session_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_capabilities",
                "method": "GET",
                "path": "/api/local-console/capabilities",
                "schema_packet": "capability_registry_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_permissions",
                "method": "GET",
                "path": "/api/local-console/permissions",
                "schema_packet": "permission_workflow_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_service",
                "method": "GET",
                "path": "/api/local-console/service",
                "schema_packet": "runtime_service_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_launcher",
                "method": "GET",
                "path": "/api/local-console/launcher",
                "schema_packet": "launcher_health_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_plugins",
                "method": "GET",
                "path": "/api/local-console/plugins",
                "schema_packet": "plugin_permission_dashboard_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_action_queue",
                "method": "GET",
                "path": "/api/local-console/action-queue",
                "schema_packet": "action_queue_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_roadmap",
                "method": "GET",
                "path": "/api/local-console/roadmap",
                "schema_packet": "roadmap_schema",
                "runtime_route_created": False,
            },
            {
                "id": "get_console_health",
                "method": "GET",
                "path": "/api/local-console/health",
                "schema_packet": "identity_status_schema",
                "runtime_route_created": False,
            },
        ]

    def request_schema_blueprints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "read_only_query_schema",
                "purpose": "Describe future read-only query parameters for dashboard views.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
            {
                "id": "pagination_query_schema",
                "purpose": "Describe future pagination query fields for list-like dashboard packets.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
            {
                "id": "filter_query_schema",
                "purpose": "Describe future dashboard filter fields.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
            {
                "id": "permission_preview_query_schema",
                "purpose": "Describe future permission preview lookup fields.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
            {
                "id": "action_preview_query_schema",
                "purpose": "Describe future action preview lookup fields without execution.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
            {
                "id": "roadmap_scope_query_schema",
                "purpose": "Describe future roadmap scope fields.",
                "allows_mutation": False,
                "runtime_validation_enabled": False,
            },
        ]

    def response_envelopes(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "standard_success_envelope",
                "fields": ["ok", "schema_version", "data", "safety"],
                "runtime_serialization_enabled": False,
            },
            {
                "id": "standard_error_envelope",
                "fields": ["ok", "schema_version", "error", "safety"],
                "runtime_serialization_enabled": False,
            },
            {
                "id": "status_envelope",
                "fields": ["ok", "schema_version", "status", "data", "safety"],
                "runtime_serialization_enabled": False,
            },
            {
                "id": "list_envelope",
                "fields": ["ok", "schema_version", "items", "count", "safety"],
                "runtime_serialization_enabled": False,
            },
            {
                "id": "permission_envelope",
                "fields": ["ok", "schema_version", "permission_required", "data", "safety"],
                "runtime_serialization_enabled": False,
            },
            {
                "id": "action_preview_envelope",
                "fields": ["ok", "schema_version", "action_preview", "risk_level", "safety"],
                "runtime_serialization_enabled": False,
            },
        ]

    def validation_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "schema_version_required",
                "rule": "Every future response packet must include schema_version.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "safe_idle_visible",
                "rule": "Every future status-like packet must expose safe_idle state.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "runtime_state_explicit",
                "rule": "Runtime-enabled and runtime-disabled states must be explicit.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "permission_required_visible",
                "rule": "Permission-required fields must be visible before future actions.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "no_secret_payloads",
                "rule": "Schemas must not expose secret values in dashboard packets.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "read_only_default",
                "rule": "All Local Console API schemas default to read-only.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "no_mutation_without_permission",
                "rule": "Mutation schemas must require explicit permission before future runtime.",
                "runtime_validation_enabled": False,
            },
            {
                "id": "audit_metadata_ready",
                "rule": "Future action packets must include audit metadata fields.",
                "runtime_validation_enabled": False,
            },
        ]

    def permission_boundary_rules(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "read_status_allowed",
                "purpose": "Future status packets may be read-only without action execution.",
                "requires_confirmation": False,
                "runtime_permission_enabled": False,
            },
            {
                "id": "read_capabilities_allowed",
                "purpose": "Future capability packets are read-only metadata.",
                "requires_confirmation": False,
                "runtime_permission_enabled": False,
            },
            {
                "id": "read_permissions_preview_only",
                "purpose": "Future permission packets may show preview data but must not resolve requests.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
            {
                "id": "read_action_queue_preview_only",
                "purpose": "Future action queue packets may show planned actions but must not execute them.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
            {
                "id": "write_actions_disabled",
                "purpose": "Write and mutation actions are disabled in this schema foundation.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
            {
                "id": "plugin_actions_disabled",
                "purpose": "Plugin action execution remains disabled.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
            {
                "id": "service_actions_disabled",
                "purpose": "Service start/stop/restart remains disabled.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
            {
                "id": "launcher_actions_disabled",
                "purpose": "Launcher start/stop/restart remains disabled.",
                "requires_confirmation": True,
                "runtime_permission_enabled": False,
            },
        ]

    def error_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "schema_not_available",
                "code": "AURA_SCHEMA_NOT_AVAILABLE",
                "runtime_error_emission_enabled": False,
            },
            {
                "id": "runtime_disabled",
                "code": "AURA_RUNTIME_DISABLED",
                "runtime_error_emission_enabled": False,
            },
            {
                "id": "permission_required",
                "code": "AURA_PERMISSION_REQUIRED",
                "runtime_error_emission_enabled": False,
            },
            {
                "id": "action_not_enabled",
                "code": "AURA_ACTION_NOT_ENABLED",
                "runtime_error_emission_enabled": False,
            },
            {
                "id": "schema_version_mismatch",
                "code": "AURA_SCHEMA_VERSION_MISMATCH",
                "runtime_error_emission_enabled": False,
            },
            {
                "id": "safe_idle_required",
                "code": "AURA_SAFE_IDLE_REQUIRED",
                "runtime_error_emission_enabled": False,
            },
        ]

    def schema_versioning_notes(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "initial_schema_version",
                "value": "0.1.0",
                "purpose": "Initial Local Console API schema foundation version.",
            },
            {
                "id": "genesis_alignment",
                "value": "0.92.0-genesis",
                "purpose": "Schema foundation aligns with Sprint 92.",
            },
            {
                "id": "backward_compatibility",
                "value": "required_after_runtime",
                "purpose": "Future runtime schemas should preserve compatibility once activated.",
            },
            {
                "id": "breaking_changes",
                "value": "must_be_documented",
                "purpose": "Future breaking schema changes must be documented.",
            },
            {
                "id": "runtime_activation",
                "value": "not_enabled",
                "purpose": "Schema versioning does not imply API runtime activation.",
            },
            {
                "id": "safe_default",
                "value": "read_only_schema_blueprint",
                "purpose": "All schemas stay read-only and blueprint-only by default.",
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare Local Console API schema catalog planning.",
            "Prepare endpoint blueprint planning.",
            "Prepare response envelope planning.",
            "Prepare request schema blueprint planning.",
            "Prepare validation rule planning.",
            "Prepare permission boundary schema planning.",
            "Prepare error contract planning.",
            "Prepare schema versioning planning.",
            "Prepare API schema safety policy planning.",
            "Keep Local Console API Schema Foundation planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "api_server_runtime",
            "api_route_runtime",
            "api_request_handling",
            "api_response_serving",
            "http_server_start",
            "web_server_runtime",
            "local_web_server_start",
            "frontend_runtime",
            "backend_runtime",
            "route_creation_runtime",
            "static_file_serving_runtime",
            "port_binding",
            "browser_launch",
            "websocket_runtime",
            "chat_runtime",
            "session_runtime",
            "plugin_runtime",
            "permission_grant_runtime",
            "permission_deny_runtime",
            "runtime_action_activation",
            "runtime_behavior_change",
            "service_runtime",
            "launcher_runtime",
            "runtime_data_fetch",
            "runtime_schema_validation",
            "runtime_serialization",
            "runtime_error_emission",
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
            "local_console_api_schema_foundation_only": True,
            "api_schema_blueprint_only": True,
            "endpoint_blueprint_only": True,
            "response_envelope_blueprint_only": True,
            "request_schema_blueprint_only": True,
            "validation_rule_blueprint_only": True,
            "permission_boundary_blueprint_only": True,
            "error_contract_blueprint_only": True,
            "schema_versioning_blueprint_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "read_only_schema_default": True,
            "safe_idle_required": True,
            "local_console_api_schema_data_ready": True,
            "api_server_runtime": False,
            "api_route_runtime": False,
            "api_request_handling": False,
            "api_response_serving": False,
            "http_server_start": False,
            "web_server_runtime": False,
            "local_web_server_start": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "route_creation_runtime": False,
            "static_file_serving_runtime": False,
            "port_binding": False,
            "browser_launch": False,
            "websocket_runtime": False,
            "chat_runtime": False,
            "session_runtime": False,
            "plugin_runtime": False,
            "permission_grant_runtime": False,
            "permission_deny_runtime": False,
            "runtime_action_activation": False,
            "runtime_behavior_change": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "runtime_data_fetch": False,
            "runtime_schema_validation": False,
            "runtime_serialization": False,
            "runtime_error_emission": False,
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

    def schema_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "schema_foundation_name": "AURA Local Console API Schema Foundation",
            "console_name": "AURA Control Center",
            "server_name": "ATLAS",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "schema_version": "0.1.0",
            "default_mode": "read_only_schema_blueprint",
            "runtime_mode": "blueprint_only",
            "api_runtime_allowed": False,
            "auto_action_allowed": False,
        }

    def schema_summary(self) -> dict[str, Any]:
        endpoints = self.endpoint_blueprints()
        return {
            "local_console_api_schema_foundation_ready": True,
            "api_schema_catalog_ready": True,
            "endpoint_blueprint_ready": True,
            "response_envelope_ready": True,
            "request_schema_blueprint_ready": True,
            "validation_rule_ready": True,
            "permission_boundary_schema_ready": True,
            "error_contract_ready": True,
            "schema_versioning_ready": True,
            "api_schema_safety_policy_ready": True,
            "schema_packet_count": len(self.schema_packets()),
            "endpoint_blueprint_count": len(endpoints),
            "request_schema_blueprint_count": len(self.request_schema_blueprints()),
            "response_envelope_count": len(self.response_envelopes()),
            "validation_rule_count": len(self.validation_rules()),
            "permission_boundary_rule_count": len(self.permission_boundary_rules()),
            "error_contract_count": len(self.error_contracts()),
            "schema_versioning_note_count": len(self.schema_versioning_notes()),
            "runtime_routes_created": sum(1 for item in endpoints if item["runtime_route_created"]),
            "api_servers_started": 0,
            "http_servers_started": 0,
            "ports_bound": 0,
            "requests_handled": 0,
            "responses_served": 0,
            "runtime_data_fetches": 0,
            "runtime_schema_validations": 0,
            "runtime_serializations": 0,
            "runtime_errors_emitted": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA Local Console API schema foundation"
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "local_console_api_schema_may_prepare_data_contracts_but_must_not_run_api_runtime",
            "schema_identity": self.schema_identity(),
            "api_schema_plan_types": self.api_schema_plan_types(),
            "schema_summary": self.schema_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def api_schema_catalog_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("api_schema_catalog_plan", target)
        plan["schema_packets"] = self.schema_packets()
        plan["rule"] = "Schema catalog planning does not fetch runtime data or start API runtime."
        return plan

    def endpoint_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("endpoint_blueprint_plan", target)
        plan["endpoint_blueprints"] = self.endpoint_blueprints()
        plan["rule"] = "Endpoint blueprint planning does not create routes, handle requests, serve responses, or bind ports."
        return plan

    def response_envelope_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("response_envelope_plan", target)
        plan["response_envelopes"] = self.response_envelopes()
        plan["rule"] = "Response envelope planning does not serialize runtime responses."
        return plan

    def request_schema_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("request_schema_blueprint_plan", target)
        plan["request_schema_blueprints"] = self.request_schema_blueprints()
        plan["rule"] = "Request schema blueprint planning does not handle requests."
        return plan

    def validation_rule_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("validation_rule_plan", target)
        plan["validation_rules"] = self.validation_rules()
        plan["rule"] = "Validation rule planning does not run runtime validation."
        return plan

    def permission_boundary_schema_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_boundary_schema_plan", target)
        plan["permission_boundary_rules"] = self.permission_boundary_rules()
        plan["rule"] = "Permission boundary schema planning does not grant, deny, or resolve permissions."
        return plan

    def error_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("error_contract_plan", target)
        plan["error_contracts"] = self.error_contracts()
        plan["rule"] = "Error contract planning does not emit runtime API errors."
        return plan

    def schema_versioning_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("schema_versioning_plan", target)
        plan["schema_versioning_notes"] = self.schema_versioning_notes()
        plan["rule"] = "Schema versioning planning does not activate API runtime."
        return plan

    def api_schema_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("api_schema_safety_policy_plan", target)
        plan["safety_rules"] = [
            "API schema foundation must not start API runtime.",
            "API schema foundation must not create routes.",
            "API schema foundation must not handle requests.",
            "API schema foundation must not serve responses.",
            "API schema foundation must not bind ports.",
            "API schema foundation must not fetch runtime data.",
            "API schema foundation must not run validation, serialization, or error emission runtime.",
            "API schema foundation must remain read-only, safe_idle-first, and metadata-only.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "schema_identity": self.schema_identity(),
            "api_schema_plan_types": self.api_schema_plan_types(),
            "schema_packets": self.schema_packets(),
            "endpoint_blueprints": self.endpoint_blueprints(),
            "request_schema_blueprints": self.request_schema_blueprints(),
            "response_envelopes": self.response_envelopes(),
            "validation_rules": self.validation_rules(),
            "permission_boundary_rules": self.permission_boundary_rules(),
            "error_contracts": self.error_contracts(),
            "schema_versioning_notes": self.schema_versioning_notes(),
            "schema_summary": self.schema_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.schema_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "local_console_api_schema_foundation_ready": True,
            "api_schema_catalog_plan_ready": True,
            "endpoint_blueprint_plan_ready": True,
            "response_envelope_plan_ready": True,
            "request_schema_blueprint_plan_ready": True,
            "validation_rule_plan_ready": True,
            "permission_boundary_schema_plan_ready": True,
            "error_contract_plan_ready": True,
            "schema_versioning_plan_ready": True,
            "api_schema_safety_policy_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "local_console_api_schema_data_ready": True,
            "api_schema_plan_types": self.api_schema_plan_types(),
            "plan_type_count": len(self.api_schema_plan_types()),
            **summary,
            **boundary,
        }
