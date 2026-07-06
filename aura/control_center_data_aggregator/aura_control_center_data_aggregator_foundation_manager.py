
"""AURA Control Center Data Aggregator Foundation.

Planner-only foundation for future Control Center dashboard data
aggregation. It prepares aggregation packet blueprints for ATLAS core
status, ORION client status, bridge status, permission scope status,
health snapshots, dashboard views, and audit event visibility without
fetching runtime data, connecting to clients, starting API/web runtime,
or executing actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraControlCenterDataAggregatorFoundationManager:
    """Prepare Control Center data aggregator plans without runtime."""

    name = "aura_control_center_data_aggregator_foundation"
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

    def aggregator_plan_types(self) -> list[str]:
        return [
            "control_center_data_aggregator_status",
            "aggregator_packet_catalog_plan",
            "atlas_core_packet_plan",
            "orion_client_packet_plan",
            "client_bridge_packet_plan",
            "dashboard_view_packet_plan",
            "permission_scope_packet_plan",
            "health_snapshot_packet_plan",
            "audit_event_visibility_packet_plan",
            "data_aggregator_safety_policy_plan",
            "control_center_data_aggregator_context",
        ]

    def aggregator_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "aggregator_name": "AURA Control Center Data Aggregator Foundation",
            "console_name": "AURA Control Center",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "atlas_role": "brain_core_server",
            "orion_role": "client_body_senses_executor",
            "default_mode": "metadata_blueprint_only",
            "runtime_mode": "blueprint_only",
            "runtime_fetch_allowed": False,
            "client_connection_allowed": False,
            "auto_action_allowed": False,
        }

    def atlas_core_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "atlas_identity_status_packet",
                "title": "ATLAS Identity Status Packet",
                "purpose": "Expose AURA identity, version, boot status, and safe_idle status for future dashboard.",
                "source_system": "identity_status",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "atlas_capability_registry_packet",
                "title": "ATLAS Capability Registry Packet",
                "purpose": "Expose capability registry summary and visible capability cards.",
                "source_system": "capability_registry",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "atlas_permission_workflow_packet",
                "title": "ATLAS Permission Workflow Packet",
                "purpose": "Expose permission workflow summary and pending request visibility.",
                "source_system": "unified_permission_workflow",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "atlas_runtime_service_packet",
                "title": "ATLAS Runtime Service Packet",
                "purpose": "Expose runtime service foundation status and disabled runtime boundaries.",
                "source_system": "runtime_service_foundation",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "atlas_launcher_health_packet",
                "title": "ATLAS Launcher Health Packet",
                "purpose": "Expose launcher and health monitor foundation metadata.",
                "source_system": "launcher_health_monitor",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "atlas_roadmap_packet",
                "title": "ATLAS Roadmap Packet",
                "purpose": "Expose Genesis and post-Genesis roadmap status for future dashboard.",
                "source_system": "roadmap_docs",
                "runtime_fetch_enabled": False,
            },
        ]

    def orion_client_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "orion_client_identity_packet",
                "title": "ORION Client Identity Packet",
                "purpose": "Reserve future ORION Client Agent identity and pairing state.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_voice_bridge_packet",
                "title": "ORION Voice Bridge Packet",
                "purpose": "Reserve future microphone, speaker, push-to-talk, and voice playback status.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_screen_bridge_packet",
                "title": "ORION Screen Bridge Packet",
                "purpose": "Reserve future screenshot, short recording, frame sampling, and capture permission status.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_avatar_environment_packet",
                "title": "ORION Avatar and 3D Environment Packet",
                "purpose": "Reserve future avatar runtime, 3D environment, expression, lip sync, and visual state.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_local_action_bridge_packet",
                "title": "ORION Local Action Bridge Packet",
                "purpose": "Reserve future local file/folder/software action bridge status.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_blender_bridge_packet",
                "title": "ORION Blender Bridge Packet",
                "purpose": "Reserve future Blender scene/object/material/texture workflow bridge status.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_vscode_project_bridge_packet",
                "title": "ORION VS Code Project Bridge Packet",
                "purpose": "Reserve future local project/file/editor/test bridge status.",
                "client_runtime_fetch_enabled": False,
            },
            {
                "id": "orion_streaming_game_bridge_packet",
                "title": "ORION Streaming and Game Bridge Packet",
                "purpose": "Reserve future OBS, streaming presence, game companion, and game window observation status.",
                "client_runtime_fetch_enabled": False,
            },
        ]

    def client_bridge_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "pairing_status_packet",
                "title": "Pairing Status Packet",
                "purpose": "Reserve trusted ATLAS-ORION pairing status.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_heartbeat_packet",
                "title": "Client Heartbeat Packet",
                "purpose": "Reserve future ORION heartbeat and last-seen metadata.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_latency_packet",
                "title": "Client Latency Packet",
                "purpose": "Reserve future local network latency and round-trip timing metadata.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_permission_scope_packet",
                "title": "Client Permission Scope Packet",
                "purpose": "Reserve future active client permission scope metadata.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_emergency_stop_packet",
                "title": "Client Emergency Stop Packet",
                "purpose": "Reserve future emergency stop state visibility.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_audit_forwarding_packet",
                "title": "Client Audit Forwarding Packet",
                "purpose": "Reserve future local client audit event forwarding metadata.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_plugin_health_packet",
                "title": "Client Plugin Health Packet",
                "purpose": "Reserve future ORION plugin health summary.",
                "runtime_connection_enabled": False,
            },
            {
                "id": "client_runtime_boundary_packet",
                "title": "Client Runtime Boundary Packet",
                "purpose": "Reserve future runtime-disabled/runtime-enabled client boundary visibility.",
                "runtime_connection_enabled": False,
            },
        ]

    def dashboard_view_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "genesis_dashboard_view",
                "title": "Genesis Dashboard View",
                "purpose": "Aggregate future identity, status, safe_idle, and health cards.",
                "runtime_render_enabled": False,
            },
            {
                "id": "chat_console_view",
                "title": "Chat Console View",
                "purpose": "Aggregate future chat/session visibility without chat runtime activation.",
                "runtime_render_enabled": False,
            },
            {
                "id": "permission_center_view",
                "title": "Permission Center View",
                "purpose": "Aggregate future permission request and scope visibility without resolving permissions.",
                "runtime_render_enabled": False,
            },
            {
                "id": "capability_viewer_view",
                "title": "Capability Viewer View",
                "purpose": "Aggregate future capability registry cards.",
                "runtime_render_enabled": False,
            },
            {
                "id": "plugin_dashboard_view",
                "title": "Plugin Dashboard View",
                "purpose": "Aggregate future plugin and action metadata visibility.",
                "runtime_render_enabled": False,
            },
            {
                "id": "service_launcher_view",
                "title": "Service and Launcher View",
                "purpose": "Aggregate future service and launcher status without service/launcher runtime.",
                "runtime_render_enabled": False,
            },
            {
                "id": "orion_client_view",
                "title": "ORION Client View",
                "purpose": "Aggregate future ORION client/bridge/device status.",
                "runtime_render_enabled": False,
            },
            {
                "id": "work_mode_view",
                "title": "Work Mode View",
                "purpose": "Aggregate future project, VS Code, Blender, and action queue visibility.",
                "runtime_render_enabled": False,
            },
            {
                "id": "roadmap_view",
                "title": "Roadmap View",
                "purpose": "Aggregate future roadmap and checkpoint metadata.",
                "runtime_render_enabled": False,
            },
        ]

    def permission_scope_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "one_time_permission_scope",
                "purpose": "Represent future one-time action approvals.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "session_permission_scope",
                "purpose": "Represent future temporary session approvals.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "workspace_permission_scope",
                "purpose": "Represent future workspace root permissions.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "app_permission_scope",
                "purpose": "Represent future app/window permissions.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "mode_permission_scope",
                "purpose": "Represent future mode-based permissions.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "plugin_permission_scope",
                "purpose": "Represent future plugin-specific permissions.",
                "runtime_permission_enabled": False,
            },
            {
                "id": "emergency_stop_scope",
                "purpose": "Represent future emergency stop visibility and revocation state.",
                "runtime_permission_enabled": False,
            },
        ]

    def health_snapshot_packets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "atlas_core_health",
                "purpose": "Future ATLAS core health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "atlas_memory_health",
                "purpose": "Future memory/journal/log health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "atlas_permission_health",
                "purpose": "Future permission manager health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "atlas_api_schema_health",
                "purpose": "Future API schema foundation health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_client_health",
                "purpose": "Future ORION Client Agent health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_voice_health",
                "purpose": "Future ORION voice bridge health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_screen_health",
                "purpose": "Future ORION screen bridge health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_avatar_health",
                "purpose": "Future ORION avatar and 3D environment health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_app_bridge_health",
                "purpose": "Future ORION app/workflow bridge health summary.",
                "runtime_health_fetch_enabled": False,
            },
            {
                "id": "orion_emergency_stop_health",
                "purpose": "Future ORION emergency stop visibility summary.",
                "runtime_health_fetch_enabled": False,
            },
        ]

    def audit_event_visibility_fields(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "event_id",
                "purpose": "Future unique audit event identifier.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "source_device",
                "purpose": "Future ATLAS or ORION event source.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "action_type",
                "purpose": "Future action or observation type.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "target",
                "purpose": "Future target path, app, window, plugin, or bridge.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "permission_scope",
                "purpose": "Future permission scope attached to the event.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "risk_level",
                "purpose": "Future risk level visibility.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "result",
                "purpose": "Future action result, denial, stop, or failure state.",
                "runtime_audit_fetch_enabled": False,
            },
            {
                "id": "timestamp",
                "purpose": "Future event timestamp.",
                "runtime_audit_fetch_enabled": False,
            },
        ]

    def aggregation_packet_catalog(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "atlas_core_group",
                "title": "ATLAS Core Packet Group",
                "packet_count": len(self.atlas_core_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "orion_client_group",
                "title": "ORION Client Packet Group",
                "packet_count": len(self.orion_client_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "client_bridge_group",
                "title": "Client Bridge Packet Group",
                "packet_count": len(self.client_bridge_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "dashboard_view_group",
                "title": "Dashboard View Packet Group",
                "packet_count": len(self.dashboard_view_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "permission_scope_group",
                "title": "Permission Scope Packet Group",
                "packet_count": len(self.permission_scope_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "health_snapshot_group",
                "title": "Health Snapshot Packet Group",
                "packet_count": len(self.health_snapshot_packets()),
                "runtime_fetch_enabled": False,
            },
            {
                "id": "audit_event_visibility_group",
                "title": "Audit Event Visibility Field Group",
                "packet_count": len(self.audit_event_visibility_fields()),
                "runtime_fetch_enabled": False,
            },
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare Control Center aggregation packet catalog planning.",
            "Prepare ATLAS core packet planning.",
            "Prepare ORION client packet planning.",
            "Prepare client bridge packet planning.",
            "Prepare dashboard view packet planning.",
            "Prepare permission scope packet planning.",
            "Prepare health snapshot packet planning.",
            "Prepare audit event visibility packet planning.",
            "Prepare Control Center data aggregator safety policy planning.",
            "Keep Control Center Data Aggregator planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "data_aggregator_runtime",
            "runtime_data_fetch",
            "client_connection",
            "client_pairing_runtime",
            "client_heartbeat_runtime",
            "client_audit_fetch_runtime",
            "client_audit_forwarding_runtime",
            "dashboard_render_runtime",
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
            "orion_client_runtime",
            "voice_bridge_runtime",
            "screen_capture_runtime",
            "short_recording_runtime",
            "avatar_runtime",
            "three_d_environment_runtime",
            "obs_bridge_runtime",
            "game_companion_runtime",
            "blender_bridge_runtime",
            "vscode_project_bridge_runtime",
            "local_action_bridge_runtime",
            "emergency_stop_runtime",
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
            "control_center_data_aggregator_foundation_only": True,
            "aggregation_packet_blueprint_only": True,
            "atlas_packet_blueprint_only": True,
            "orion_packet_blueprint_only": True,
            "client_bridge_packet_blueprint_only": True,
            "dashboard_view_packet_blueprint_only": True,
            "permission_scope_packet_blueprint_only": True,
            "health_snapshot_packet_blueprint_only": True,
            "audit_event_visibility_blueprint_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "control_center_data_aggregator_data_ready": True,
            "data_aggregator_runtime": False,
            "runtime_data_fetch": False,
            "client_connection": False,
            "client_pairing_runtime": False,
            "client_heartbeat_runtime": False,
            "client_audit_fetch_runtime": False,
            "client_audit_forwarding_runtime": False,
            "dashboard_render_runtime": False,
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
            "orion_client_runtime": False,
            "voice_bridge_runtime": False,
            "screen_capture_runtime": False,
            "short_recording_runtime": False,
            "avatar_runtime": False,
            "three_d_environment_runtime": False,
            "obs_bridge_runtime": False,
            "game_companion_runtime": False,
            "blender_bridge_runtime": False,
            "vscode_project_bridge_runtime": False,
            "local_action_bridge_runtime": False,
            "emergency_stop_runtime": False,
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

    def aggregator_summary(self) -> dict[str, Any]:
        catalog = self.aggregation_packet_catalog()
        atlas_packets = self.atlas_core_packets()
        orion_packets = self.orion_client_packets()
        bridge_packets = self.client_bridge_packets()
        dashboard_packets = self.dashboard_view_packets()
        permission_packets = self.permission_scope_packets()
        health_packets = self.health_snapshot_packets()
        audit_fields = self.audit_event_visibility_fields()
        return {
            "control_center_data_aggregator_foundation_ready": True,
            "aggregator_packet_catalog_ready": True,
            "atlas_core_packet_plan_ready": True,
            "orion_client_packet_plan_ready": True,
            "client_bridge_packet_plan_ready": True,
            "dashboard_view_packet_plan_ready": True,
            "permission_scope_packet_plan_ready": True,
            "health_snapshot_packet_plan_ready": True,
            "audit_event_visibility_packet_plan_ready": True,
            "data_aggregator_safety_policy_ready": True,
            "aggregation_packet_group_count": len(catalog),
            "atlas_core_packet_count": len(atlas_packets),
            "orion_client_packet_count": len(orion_packets),
            "client_bridge_packet_count": len(bridge_packets),
            "dashboard_view_packet_count": len(dashboard_packets),
            "permission_scope_packet_count": len(permission_packets),
            "health_snapshot_packet_count": len(health_packets),
            "audit_event_visibility_field_count": len(audit_fields),
            "total_blueprint_packet_count": (
                len(atlas_packets)
                + len(orion_packets)
                + len(bridge_packets)
                + len(dashboard_packets)
                + len(permission_packets)
                + len(health_packets)
                + len(audit_fields)
            ),
            "runtime_packets_collected": 0,
            "runtime_data_fetches": 0,
            "client_connections_opened": 0,
            "client_pairings_created": 0,
            "client_heartbeats_sent": 0,
            "client_heartbeats_received": 0,
            "dashboard_views_rendered": 0,
            "api_requests_handled": 0,
            "api_responses_served": 0,
            "audit_events_fetched": 0,
            "audit_events_forwarded": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA Control Center data aggregator foundation"
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "control_center_data_aggregator_may_prepare_dashboard_packet_blueprints_but_must_not_fetch_runtime_data",
            "aggregator_identity": self.aggregator_identity(),
            "aggregator_plan_types": self.aggregator_plan_types(),
            "aggregator_summary": self.aggregator_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def aggregator_packet_catalog_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("aggregator_packet_catalog_plan", target)
        plan["aggregation_packet_catalog"] = self.aggregation_packet_catalog()
        plan["rule"] = "Packet catalog planning does not collect runtime packets."
        return plan

    def atlas_core_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("atlas_core_packet_plan", target)
        plan["atlas_core_packets"] = self.atlas_core_packets()
        plan["rule"] = "ATLAS core packet planning does not fetch runtime ATLAS data."
        return plan

    def orion_client_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("orion_client_packet_plan", target)
        plan["orion_client_packets"] = self.orion_client_packets()
        plan["rule"] = "ORION client packet planning does not connect to ORION or start client runtime."
        return plan

    def client_bridge_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("client_bridge_packet_plan", target)
        plan["client_bridge_packets"] = self.client_bridge_packets()
        plan["rule"] = "Client bridge packet planning does not pair, heartbeat, connect, or forward audit events."
        return plan

    def dashboard_view_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("dashboard_view_packet_plan", target)
        plan["dashboard_view_packets"] = self.dashboard_view_packets()
        plan["rule"] = "Dashboard view packet planning does not render dashboard views."
        return plan

    def permission_scope_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_scope_packet_plan", target)
        plan["permission_scope_packets"] = self.permission_scope_packets()
        plan["rule"] = "Permission scope packet planning does not grant, deny, resolve, or activate permissions."
        return plan

    def health_snapshot_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("health_snapshot_packet_plan", target)
        plan["health_snapshot_packets"] = self.health_snapshot_packets()
        plan["rule"] = "Health snapshot packet planning does not fetch runtime health data."
        return plan

    def audit_event_visibility_packet_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("audit_event_visibility_packet_plan", target)
        plan["audit_event_visibility_fields"] = self.audit_event_visibility_fields()
        plan["rule"] = "Audit event visibility planning does not fetch or forward audit events."
        return plan

    def data_aggregator_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("data_aggregator_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Data aggregator foundation must not fetch runtime data.",
            "Data aggregator foundation must not connect to ORION.",
            "Data aggregator foundation must not create client pairings.",
            "Data aggregator foundation must not send or receive heartbeats.",
            "Data aggregator foundation must not fetch or forward audit events.",
            "Data aggregator foundation must not render dashboard views.",
            "Data aggregator foundation must not start API/web/client runtime.",
            "Data aggregator foundation must remain safe_idle-first and metadata-only.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "aggregator_identity": self.aggregator_identity(),
            "aggregator_plan_types": self.aggregator_plan_types(),
            "aggregation_packet_catalog": self.aggregation_packet_catalog(),
            "atlas_core_packets": self.atlas_core_packets(),
            "orion_client_packets": self.orion_client_packets(),
            "client_bridge_packets": self.client_bridge_packets(),
            "dashboard_view_packets": self.dashboard_view_packets(),
            "permission_scope_packets": self.permission_scope_packets(),
            "health_snapshot_packets": self.health_snapshot_packets(),
            "audit_event_visibility_fields": self.audit_event_visibility_fields(),
            "aggregator_summary": self.aggregator_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.aggregator_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "control_center_data_aggregator_foundation_ready": True,
            "aggregator_packet_catalog_plan_ready": True,
            "atlas_core_packet_plan_ready": True,
            "orion_client_packet_plan_ready": True,
            "client_bridge_packet_plan_ready": True,
            "dashboard_view_packet_plan_ready": True,
            "permission_scope_packet_plan_ready": True,
            "health_snapshot_packet_plan_ready": True,
            "audit_event_visibility_packet_plan_ready": True,
            "data_aggregator_safety_policy_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "control_center_data_aggregator_data_ready": True,
            "aggregator_plan_types": self.aggregator_plan_types(),
            "plan_type_count": len(self.aggregator_plan_types()),
            **summary,
            **boundary,
        }
