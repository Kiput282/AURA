
"""AURA Pre-Runtime Security Audit Foundation.

Planner-only/review-only foundation for pre-runtime security audit.
It prepares audit domains, runtime gate checks, permission boundary checks,
file system safety checks, network surface checks, action execution safety
checks, ORION boundary checks, audit visibility checks, and Sprint 100
stabilization readiness checks without executing security scans, reading
files, probing ports, mutating gates, granting permissions, dispatching
actions, executing commands, invoking tools, or changing runtime behavior.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraPreRuntimeSecurityAuditFoundationManager:
    """Prepare pre-runtime security audit blueprints without runtime execution."""

    name = "aura_pre_runtime_security_audit_foundation"
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

    def security_audit_plan_types(self) -> list[str]:
        return [
            "pre_runtime_security_audit_status",
            "security_audit_domain_plan",
            "runtime_gate_check_plan",
            "permission_boundary_check_plan",
            "file_system_safety_check_plan",
            "network_surface_check_plan",
            "action_execution_safety_check_plan",
            "orion_boundary_check_plan",
            "audit_visibility_check_plan",
            "stabilization_readiness_check_plan",
            "pre_runtime_security_audit_context",
        ]

    def audit_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "audit_name": "AURA Pre-Runtime Security Audit Foundation",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_mode": "pre_runtime_audit_blueprint_only",
            "runtime_mode": "audit_review_only",
            "audit_authority": "ATLAS",
            "audit_scope": "sprint_91_to_98_pre_runtime_foundations",
            "security_scan_runtime_allowed": False,
            "runtime_gate_mutation_allowed": False,
            "permission_change_allowed": False,
            "file_system_access_allowed": False,
            "network_probe_allowed": False,
            "action_dispatch_allowed": False,
            "command_execution_allowed": False,
            "tool_execution_allowed": False,
        }

    def security_audit_domains(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "local_console_static_prototype_domain",
                "purpose": "Audit Local Console Static Prototype Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "local_console_api_schema_domain",
                "purpose": "Audit Local Console API Schema Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "control_center_data_aggregator_domain",
                "purpose": "Audit Control Center Data Aggregator Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "permission_request_review_queue_domain",
                "purpose": "Audit Permission Request Review Queue Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "chat_session_persistence_planner_domain",
                "purpose": "Audit Chat Session Persistence Planner Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "safe_local_web_runtime_gate_domain",
                "purpose": "Audit Safe Local Web Runtime Gate Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "controlled_file_write_approval_draft_domain",
                "purpose": "Audit Controlled File Write Approval Draft Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
            {
                "id": "runtime_action_queue_review_layer_domain",
                "purpose": "Audit Runtime Action Queue Review Layer Foundation boundaries.",
                "runtime_audit_enabled": False,
            },
        ]

    def runtime_gate_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "safe_idle_default_check", "purpose": "Confirm safe_idle remains the default posture.", "runtime_check_enabled": False},
            {"id": "web_runtime_disabled_check", "purpose": "Confirm web runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "api_runtime_disabled_check", "purpose": "Confirm API runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "websocket_runtime_disabled_check", "purpose": "Confirm websocket runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "frontend_backend_runtime_disabled_check", "purpose": "Confirm frontend/backend runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "port_binding_disabled_check", "purpose": "Confirm port binding remains disabled.", "runtime_check_enabled": False},
            {"id": "browser_launch_disabled_check", "purpose": "Confirm browser launch remains disabled.", "runtime_check_enabled": False},
            {"id": "session_runtime_disabled_check", "purpose": "Confirm session runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "service_launcher_runtime_disabled_check", "purpose": "Confirm service/launcher runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "orion_client_runtime_disabled_check", "purpose": "Confirm ORION client runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "screen_recording_runtime_disabled_check", "purpose": "Confirm screen capture and short recording runtime remain disabled.", "runtime_check_enabled": False},
            {"id": "local_action_runtime_disabled_check", "purpose": "Confirm local action runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "plugin_tool_runtime_disabled_check", "purpose": "Confirm plugin/tool runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "git_runtime_disabled_check", "purpose": "Confirm git runtime remains disabled.", "runtime_check_enabled": False},
        ]

    def permission_boundary_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "permission_grant_disabled_check", "purpose": "Confirm runtime permission grant remains disabled.", "runtime_check_enabled": False},
            {"id": "permission_deny_disabled_check", "purpose": "Confirm runtime permission deny remains disabled.", "runtime_check_enabled": False},
            {"id": "permission_resolution_disabled_check", "purpose": "Confirm runtime permission resolution remains disabled.", "runtime_check_enabled": False},
            {"id": "permission_scope_activation_disabled_check", "purpose": "Confirm permission scope activation remains disabled.", "runtime_check_enabled": False},
            {"id": "permission_scope_revocation_disabled_check", "purpose": "Confirm permission scope revocation remains disabled.", "runtime_check_enabled": False},
            {"id": "approval_runtime_disabled_check", "purpose": "Confirm approval runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "denial_runtime_disabled_check", "purpose": "Confirm denial runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "permission_review_queue_blueprint_only_check", "purpose": "Confirm review queue remains blueprint-only.", "runtime_check_enabled": False},
            {"id": "least_privilege_policy_visible_check", "purpose": "Confirm least-privilege planning remains visible.", "runtime_check_enabled": False},
            {"id": "permission_audit_visibility_check", "purpose": "Confirm permission audit visibility is planned.", "runtime_check_enabled": False},
        ]

    def file_system_safety_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "file_read_disabled_check", "purpose": "Confirm file read remains disabled.", "runtime_check_enabled": False},
            {"id": "file_write_disabled_check", "purpose": "Confirm file write remains disabled.", "runtime_check_enabled": False},
            {"id": "file_modify_disabled_check", "purpose": "Confirm file modify remains disabled.", "runtime_check_enabled": False},
            {"id": "file_delete_disabled_check", "purpose": "Confirm file delete remains disabled.", "runtime_check_enabled": False},
            {"id": "file_backup_restore_disabled_check", "purpose": "Confirm backup/restore runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "rollback_runtime_disabled_check", "purpose": "Confirm rollback runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "diff_runtime_disabled_check", "purpose": "Confirm diff runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "path_probe_disabled_check", "purpose": "Confirm path probing remains disabled.", "runtime_check_enabled": False},
            {"id": "overwrite_disabled_check", "purpose": "Confirm overwrite runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "controlled_file_write_review_only_check", "purpose": "Confirm controlled file write remains approval-draft-only.", "runtime_check_enabled": False},
        ]

    def network_surface_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "localhost_gate_blueprint_only_check", "purpose": "Confirm localhost gate remains blueprint-only.", "runtime_check_enabled": False},
            {"id": "public_interface_binding_disabled_check", "purpose": "Confirm public interface binding remains disabled.", "runtime_check_enabled": False},
            {"id": "external_tunnel_disabled_check", "purpose": "Confirm external tunnel runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "network_action_disabled_check", "purpose": "Confirm network action remains disabled.", "runtime_check_enabled": False},
            {"id": "internet_search_runtime_disabled_check", "purpose": "Confirm internet search runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "package_download_disabled_check", "purpose": "Confirm package download remains disabled.", "runtime_check_enabled": False},
            {"id": "dependency_install_disabled_check", "purpose": "Confirm dependency install remains disabled.", "runtime_check_enabled": False},
            {"id": "api_request_handling_disabled_check", "purpose": "Confirm API request handling remains disabled.", "runtime_check_enabled": False},
            {"id": "external_network_exposure_zero_check", "purpose": "Confirm external network exposure counters remain zero.", "runtime_check_enabled": False},
        ]

    def action_execution_safety_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "runtime_action_queue_disabled_check", "purpose": "Confirm runtime action queue runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "queue_item_creation_disabled_check", "purpose": "Confirm queue item creation remains disabled.", "runtime_check_enabled": False},
            {"id": "queue_item_mutation_disabled_check", "purpose": "Confirm queue item mutation remains disabled.", "runtime_check_enabled": False},
            {"id": "queue_item_submission_disabled_check", "purpose": "Confirm queue item submission remains disabled.", "runtime_check_enabled": False},
            {"id": "queue_item_approval_disabled_check", "purpose": "Confirm queue item approval remains disabled.", "runtime_check_enabled": False},
            {"id": "action_dispatch_disabled_check", "purpose": "Confirm action dispatch remains disabled.", "runtime_check_enabled": False},
            {"id": "action_execution_disabled_check", "purpose": "Confirm action execution remains disabled.", "runtime_check_enabled": False},
            {"id": "plugin_action_execution_disabled_check", "purpose": "Confirm plugin action execution remains disabled.", "runtime_check_enabled": False},
            {"id": "tool_execution_disabled_check", "purpose": "Confirm tool execution remains disabled.", "runtime_check_enabled": False},
            {"id": "desktop_control_disabled_check", "purpose": "Confirm desktop control remains disabled.", "runtime_check_enabled": False},
            {"id": "command_execution_disabled_check", "purpose": "Confirm command execution remains disabled.", "runtime_check_enabled": False},
            {"id": "runtime_execution_features_zero_check", "purpose": "Confirm runtime execution features remain zero.", "runtime_check_enabled": False},
        ]

    def orion_boundary_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "orion_client_connection_disabled_check", "purpose": "Confirm ORION client connection remains disabled.", "runtime_check_enabled": False},
            {"id": "orion_pairing_disabled_check", "purpose": "Confirm ORION pairing runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "orion_heartbeat_disabled_check", "purpose": "Confirm ORION heartbeat runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "screen_capture_disabled_check", "purpose": "Confirm screen capture runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "short_recording_disabled_check", "purpose": "Confirm short recording runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "voice_bridge_disabled_check", "purpose": "Confirm voice bridge runtime remains disabled.", "runtime_check_enabled": False},
            {"id": "avatar_game_blender_vscode_disabled_check", "purpose": "Confirm avatar/game/Blender/VS Code bridges remain disabled.", "runtime_check_enabled": False},
            {"id": "emergency_stop_runtime_disabled_check", "purpose": "Confirm emergency stop runtime remains disabled.", "runtime_check_enabled": False},
        ]

    def audit_visibility_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "capability_registry_visibility_check", "purpose": "Confirm capability registry visibility is planned.", "runtime_check_enabled": False},
            {"id": "control_center_visibility_check", "purpose": "Confirm Control Center visibility is planned.", "runtime_check_enabled": False},
            {"id": "permission_audit_visibility_check", "purpose": "Confirm permission decision audit visibility is planned.", "runtime_check_enabled": False},
            {"id": "file_write_audit_visibility_check", "purpose": "Confirm file write audit visibility is planned.", "runtime_check_enabled": False},
            {"id": "web_runtime_audit_visibility_check", "purpose": "Confirm web runtime audit visibility is planned.", "runtime_check_enabled": False},
            {"id": "runtime_action_audit_visibility_check", "purpose": "Confirm runtime action audit visibility is planned.", "runtime_check_enabled": False},
            {"id": "session_persistence_audit_visibility_check", "purpose": "Confirm session persistence audit visibility is planned.", "runtime_check_enabled": False},
            {"id": "security_audit_report_visibility_check", "purpose": "Confirm security audit report visibility is planned.", "runtime_check_enabled": False},
            {"id": "sprint_100_review_visibility_check", "purpose": "Confirm Sprint 100 review visibility is planned.", "runtime_check_enabled": False},
        ]

    def stabilization_readiness_checks(self) -> list[dict[str, Any]]:
        return [
            {"id": "sprint_91_to_98_docs_ready_check", "purpose": "Confirm Sprint 91-98 documentation is ready for review.", "runtime_check_enabled": False},
            {"id": "registry_counts_ready_check", "purpose": "Confirm capability registry counts are ready for Sprint 100.", "runtime_check_enabled": False},
            {"id": "runtime_zero_counters_ready_check", "purpose": "Confirm runtime zero counters are ready for Sprint 100.", "runtime_check_enabled": False},
            {"id": "foundation_only_boundary_ready_check", "purpose": "Confirm foundation-only boundaries are ready for Sprint 100.", "runtime_check_enabled": False},
            {"id": "permission_first_boundary_ready_check", "purpose": "Confirm permission-first boundaries are ready for Sprint 100.", "runtime_check_enabled": False},
            {"id": "safe_idle_first_boundary_ready_check", "purpose": "Confirm safe_idle-first boundaries are ready for Sprint 100.", "runtime_check_enabled": False},
            {"id": "no_runtime_execution_ready_check", "purpose": "Confirm no runtime execution features are active before Sprint 100.", "runtime_check_enabled": False},
            {"id": "checkpoint_review_ready_check", "purpose": "Confirm Sprint 100 review checkpoint can be prepared.", "runtime_check_enabled": False},
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare pre-runtime security audit domain planning.",
            "Prepare runtime gate check planning.",
            "Prepare permission boundary check planning.",
            "Prepare file system safety check planning.",
            "Prepare network surface check planning.",
            "Prepare action execution safety check planning.",
            "Prepare ORION boundary check planning.",
            "Prepare audit visibility check planning.",
            "Prepare Sprint 100 stabilization readiness check planning.",
            "Expose pre-runtime security audit status.",
            "Keep pre-runtime security audit foundation-only, review-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "security_scan_runtime",
            "runtime_security_audit_execution",
            "runtime_check_execution",
            "runtime_gate_mutation",
            "runtime_permission_change",
            "runtime_permission_grant",
            "runtime_permission_deny",
            "runtime_permission_scope_activation",
            "runtime_network_scan",
            "runtime_port_probe",
            "runtime_file_read",
            "runtime_file_write",
            "runtime_command_execution",
            "runtime_action_dispatch",
            "runtime_action_execution",
            "runtime_tool_execution",
            "runtime_memory_write",
            "runtime_git_operation",
            "web_server_runtime",
            "api_server_runtime",
            "websocket_runtime",
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
            "pre_runtime_security_audit_foundation_only": True,
            "security_audit_domain_blueprint_only": True,
            "runtime_gate_check_blueprint_only": True,
            "permission_boundary_check_blueprint_only": True,
            "file_system_safety_check_blueprint_only": True,
            "network_surface_check_blueprint_only": True,
            "action_execution_safety_check_blueprint_only": True,
            "orion_boundary_check_blueprint_only": True,
            "audit_visibility_check_blueprint_only": True,
            "stabilization_readiness_check_blueprint_only": True,
            "pre_runtime_audit_only": True,
            "review_only": True,
            "planner_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "pre_runtime_security_audit_data_ready": True,
            "security_scan_runtime": False,
            "runtime_security_audit_execution": False,
            "runtime_check_execution": False,
            "runtime_gate_mutation": False,
            "runtime_permission_change": False,
            "runtime_permission_grant": False,
            "runtime_permission_deny": False,
            "runtime_permission_scope_activation": False,
            "runtime_network_scan": False,
            "runtime_port_probe": False,
            "runtime_file_read": False,
            "runtime_file_write": False,
            "runtime_command_execution": False,
            "runtime_action_dispatch": False,
            "runtime_action_execution": False,
            "runtime_tool_execution": False,
            "runtime_memory_write": False,
            "runtime_git_operation": False,
            "permission_grant_runtime": False,
            "permission_deny_runtime": False,
            "permission_resolution_runtime": False,
            "permission_scope_activation_runtime": False,
            "permission_scope_revocation_runtime": False,
            "approval_runtime": False,
            "denial_runtime": False,
            "runtime_action_queue_runtime": False,
            "runtime_action_dispatch_runtime": False,
            "local_action_runtime": False,
            "local_action_bridge_runtime": False,
            "plugin_action_execution": False,
            "plugin_runtime": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "desktop_control": False,
            "file_write_runtime": False,
            "controlled_file_write_runtime": False,
            "file_read_runtime": False,
            "file_modify_runtime": False,
            "file_delete_runtime": False,
            "command_execution": False,
            "test_execution": False,
            "code_execution": False,
            "dependency_install": False,
            "package_download": False,
            "internet_search": False,
            "network_action": False,
            "web_server_runtime": False,
            "http_server_start": False,
            "local_web_server_start": False,
            "api_server_runtime": False,
            "api_route_runtime": False,
            "api_request_handling": False,
            "api_response_serving": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "dashboard_render_runtime": False,
            "route_creation_runtime": False,
            "static_file_serving_runtime": False,
            "port_binding": False,
            "public_interface_binding": False,
            "external_tunnel_runtime": False,
            "browser_launch": False,
            "websocket_runtime": False,
            "session_runtime": False,
            "chat_runtime": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "orion_client_runtime": False,
            "client_connection": False,
            "client_pairing_runtime": False,
            "client_heartbeat_runtime": False,
            "screen_capture_runtime": False,
            "short_recording_runtime": False,
            "voice_bridge_runtime": False,
            "avatar_runtime": False,
            "three_d_environment_runtime": False,
            "game_companion_runtime": False,
            "blender_bridge_runtime": False,
            "vscode_project_bridge_runtime": False,
            "emergency_stop_runtime": False,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "memory_write": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
        }

    def audit_summary(self) -> dict[str, Any]:
        domains = self.security_audit_domains()
        runtime_checks = self.runtime_gate_checks()
        permission_checks = self.permission_boundary_checks()
        file_checks = self.file_system_safety_checks()
        network_checks = self.network_surface_checks()
        action_checks = self.action_execution_safety_checks()
        orion_checks = self.orion_boundary_checks()
        audit_checks = self.audit_visibility_checks()
        stabilization_checks = self.stabilization_readiness_checks()
        return {
            "pre_runtime_security_audit_foundation_ready": True,
            "security_audit_domain_plan_ready": True,
            "runtime_gate_check_plan_ready": True,
            "permission_boundary_check_plan_ready": True,
            "file_system_safety_check_plan_ready": True,
            "network_surface_check_plan_ready": True,
            "action_execution_safety_check_plan_ready": True,
            "orion_boundary_check_plan_ready": True,
            "audit_visibility_check_plan_ready": True,
            "stabilization_readiness_check_plan_ready": True,
            "security_audit_domain_count": len(domains),
            "runtime_gate_check_count": len(runtime_checks),
            "permission_boundary_check_count": len(permission_checks),
            "file_system_safety_check_count": len(file_checks),
            "network_surface_check_count": len(network_checks),
            "action_execution_safety_check_count": len(action_checks),
            "orion_boundary_check_count": len(orion_checks),
            "audit_visibility_check_count": len(audit_checks),
            "stabilization_readiness_check_count": len(stabilization_checks),
            "total_security_audit_check_count": (
                len(domains)
                + len(runtime_checks)
                + len(permission_checks)
                + len(file_checks)
                + len(network_checks)
                + len(action_checks)
                + len(orion_checks)
                + len(audit_checks)
                + len(stabilization_checks)
            ),
            "runtime_security_audits_executed": 0,
            "runtime_checks_executed": 0,
            "runtime_gate_changes_applied": 0,
            "runtime_permissions_granted": 0,
            "runtime_permissions_denied": 0,
            "runtime_permission_scopes_activated": 0,
            "runtime_network_scans_executed": 0,
            "runtime_ports_probed": 0,
            "runtime_files_read": 0,
            "runtime_files_written": 0,
            "runtime_commands_executed": 0,
            "runtime_actions_dispatched": 0,
            "runtime_actions_executed": 0,
            "runtime_tools_executed": 0,
            "runtime_memory_writes": 0,
            "runtime_git_operations": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA pre-runtime security audit foundation"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "security_audit_may_prepare_review_blueprints_but_must_not_execute_runtime_checks_or_mutate_runtime_state",
            "audit_identity": self.audit_identity(),
            "security_audit_plan_types": self.security_audit_plan_types(),
            "audit_summary": self.audit_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def security_audit_domain_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("security_audit_domain_plan", target)
        plan["security_audit_domains"] = self.security_audit_domains()
        plan["rule"] = "Security audit domain planning does not execute security scans."
        return plan

    def runtime_gate_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("runtime_gate_check_plan", target)
        plan["runtime_gate_checks"] = self.runtime_gate_checks()
        plan["rule"] = "Runtime gate check planning does not mutate runtime gates."
        return plan

    def permission_boundary_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_boundary_check_plan", target)
        plan["permission_boundary_checks"] = self.permission_boundary_checks()
        plan["rule"] = "Permission boundary check planning does not grant, deny, resolve, activate, or revoke permissions."
        return plan

    def file_system_safety_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("file_system_safety_check_plan", target)
        plan["file_system_safety_checks"] = self.file_system_safety_checks()
        plan["rule"] = "File system safety check planning does not read, write, modify, delete, or probe files."
        return plan

    def network_surface_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("network_surface_check_plan", target)
        plan["network_surface_checks"] = self.network_surface_checks()
        plan["rule"] = "Network surface check planning does not scan networks or probe ports."
        return plan

    def action_execution_safety_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("action_execution_safety_check_plan", target)
        plan["action_execution_safety_checks"] = self.action_execution_safety_checks()
        plan["rule"] = "Action execution safety check planning does not dispatch or execute actions."
        return plan

    def orion_boundary_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_boundary_check_plan", target)
        plan["orion_boundary_checks"] = self.orion_boundary_checks()
        plan["rule"] = "ORION boundary check planning does not connect to ORION or trigger local client actions."
        return plan

    def audit_visibility_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("audit_visibility_check_plan", target)
        plan["audit_visibility_checks"] = self.audit_visibility_checks()
        plan["rule"] = "Audit visibility check planning does not write or fetch audit events."
        return plan

    def stabilization_readiness_check_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("stabilization_readiness_check_plan", target)
        plan["stabilization_readiness_checks"] = self.stabilization_readiness_checks()
        plan["rule"] = "Stabilization readiness planning does not perform runtime changes."
        return plan

    def safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("pre_runtime_security_audit_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Pre-runtime security audit must not execute security scans.",
            "Pre-runtime security audit must not read, write, modify, or delete files.",
            "Pre-runtime security audit must not probe ports or scan networks.",
            "Pre-runtime security audit must not mutate runtime gates.",
            "Pre-runtime security audit must not grant or deny permissions.",
            "Pre-runtime security audit must not activate permission scopes.",
            "Pre-runtime security audit must not dispatch or execute actions.",
            "Pre-runtime security audit must not run plugins, tools, commands, or git operations.",
            "Pre-runtime security audit must not connect to ORION or local clients.",
            "Pre-runtime security audit must remain foundation-only, review-only, metadata-only, and safe_idle-first.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "audit_identity": self.audit_identity(),
            "security_audit_plan_types": self.security_audit_plan_types(),
            "security_audit_domains": self.security_audit_domains(),
            "runtime_gate_checks": self.runtime_gate_checks(),
            "permission_boundary_checks": self.permission_boundary_checks(),
            "file_system_safety_checks": self.file_system_safety_checks(),
            "network_surface_checks": self.network_surface_checks(),
            "action_execution_safety_checks": self.action_execution_safety_checks(),
            "orion_boundary_checks": self.orion_boundary_checks(),
            "audit_visibility_checks": self.audit_visibility_checks(),
            "stabilization_readiness_checks": self.stabilization_readiness_checks(),
            "audit_summary": self.audit_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.audit_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "pre_runtime_security_audit_foundation_ready": True,
            "security_audit_domain_plan_ready": True,
            "runtime_gate_check_plan_ready": True,
            "permission_boundary_check_plan_ready": True,
            "file_system_safety_check_plan_ready": True,
            "network_surface_check_plan_ready": True,
            "action_execution_safety_check_plan_ready": True,
            "orion_boundary_check_plan_ready": True,
            "audit_visibility_check_plan_ready": True,
            "stabilization_readiness_check_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "pre_runtime_security_audit_data_ready": True,
            "security_audit_plan_types": self.security_audit_plan_types(),
            "plan_type_count": len(self.security_audit_plan_types()),
            **summary,
            **boundary,
        }
