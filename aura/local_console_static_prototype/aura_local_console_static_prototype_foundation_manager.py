
"""AURA Local Console Static Prototype Foundation.

Planner-only foundation for future Local Console / Control Center static
prototype structure. It prepares static page blueprints, asset group
blueprints, panel layout blueprints, route-to-static-page mapping,
data placeholder contracts, theme tokens, accessibility notes, and safety
policy without creating a web server, serving files, binding ports, opening
a browser, running frontend/backend/API runtime, or executing actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class AuraLocalConsoleStaticPrototypeFoundationManager:
    """Prepare Local Console static prototype plans without runtime."""

    name = "aura_local_console_static_prototype_foundation"
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

    def prototype_plan_types(self) -> list[str]:
        return [
            "local_console_static_prototype_status",
            "static_prototype_structure_plan",
            "static_page_blueprint_plan",
            "static_asset_blueprint_plan",
            "panel_layout_blueprint_plan",
            "route_static_mapping_plan",
            "data_placeholder_contract_plan",
            "theme_token_blueprint_plan",
            "accessibility_blueprint_plan",
            "static_prototype_safety_policy_plan",
            "local_console_static_prototype_context",
        ]

    def static_pages(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "dashboard",
                "route": "/",
                "title": "Genesis Dashboard",
                "purpose": "Show AURA identity, boot status, safe_idle state, and high-level health.",
                "runtime_enabled": False,
            },
            {
                "id": "chat",
                "route": "/chat",
                "title": "Chat Console",
                "purpose": "Reserve static layout for future chat runtime and session metadata.",
                "runtime_enabled": False,
            },
            {
                "id": "status",
                "route": "/status",
                "title": "AURA Status",
                "purpose": "Show read-only system status placeholder.",
                "runtime_enabled": False,
            },
            {
                "id": "capabilities",
                "route": "/capabilities",
                "title": "Capability Viewer",
                "purpose": "Show capability registry placeholder cards.",
                "runtime_enabled": False,
            },
            {
                "id": "permissions",
                "route": "/permissions",
                "title": "Permission Center",
                "purpose": "Show permission request visibility placeholder.",
                "runtime_enabled": False,
            },
            {
                "id": "plugins",
                "route": "/plugins",
                "title": "Plugin Dashboard",
                "purpose": "Show plugin and action registry placeholder.",
                "runtime_enabled": False,
            },
            {
                "id": "service",
                "route": "/service",
                "title": "Service Monitor",
                "purpose": "Show runtime service foundation metadata placeholder.",
                "runtime_enabled": False,
            },
            {
                "id": "launcher",
                "route": "/launcher",
                "title": "Launcher Control",
                "purpose": "Show launcher and health monitor placeholder.",
                "runtime_enabled": False,
            },
            {
                "id": "roadmap",
                "route": "/roadmap",
                "title": "Roadmap Viewer",
                "purpose": "Show Genesis and post-Genesis roadmap placeholder.",
                "runtime_enabled": False,
            },
        ]

    def asset_groups(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "html_shells",
                "planned_path": "local_console_static/pages/",
                "purpose": "Static HTML page shells blueprint.",
                "files_created": 0,
            },
            {
                "id": "stylesheets",
                "planned_path": "local_console_static/assets/css/",
                "purpose": "Static CSS token and layout blueprint.",
                "files_created": 0,
            },
            {
                "id": "scripts",
                "planned_path": "local_console_static/assets/js/",
                "purpose": "Static JavaScript placeholder blueprint.",
                "files_created": 0,
            },
            {
                "id": "icons",
                "planned_path": "local_console_static/assets/icons/",
                "purpose": "Icon and status marker blueprint.",
                "files_created": 0,
            },
            {
                "id": "mock_data",
                "planned_path": "local_console_static/mock/",
                "purpose": "Mock dashboard data contract blueprint.",
                "files_created": 0,
            },
            {
                "id": "docs",
                "planned_path": "local_console_static/docs/",
                "purpose": "Static prototype developer notes blueprint.",
                "files_created": 0,
            },
        ]

    def panel_layouts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "identity_header",
                "zone": "top",
                "purpose": "Show AURA name, version, mode, and safe_idle indicator.",
                "interactive": False,
            },
            {
                "id": "navigation_sidebar",
                "zone": "left",
                "purpose": "Show planned console navigation.",
                "interactive": False,
            },
            {
                "id": "chat_panel",
                "zone": "center",
                "purpose": "Reserve future chat panel space.",
                "interactive": False,
            },
            {
                "id": "status_cards",
                "zone": "dashboard",
                "purpose": "Show read-only status card placeholders.",
                "interactive": False,
            },
            {
                "id": "permission_queue",
                "zone": "permissions",
                "purpose": "Show planned permission queue placeholders.",
                "interactive": False,
            },
            {
                "id": "capability_grid",
                "zone": "capabilities",
                "purpose": "Show capability metadata card placeholders.",
                "interactive": False,
            },
            {
                "id": "plugin_action_table",
                "zone": "plugins",
                "purpose": "Show plugin/action table placeholders.",
                "interactive": False,
            },
            {
                "id": "service_health_strip",
                "zone": "service",
                "purpose": "Show service/launcher health placeholder.",
                "interactive": False,
            },
            {
                "id": "roadmap_timeline",
                "zone": "roadmap",
                "purpose": "Show roadmap timeline placeholder.",
                "interactive": False,
            },
        ]

    def route_static_mappings(self) -> list[dict[str, Any]]:
        return [
            {"route": page["route"], "page_id": page["id"], "runtime_route_created": False}
            for page in self.static_pages()
        ]

    def data_placeholder_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "identity_status_packet",
                "source": "identity.yaml and main status",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "capability_registry_packet",
                "source": "Capability Registry",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "permission_workflow_packet",
                "source": "Unified Permission Workflow",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "runtime_service_packet",
                "source": "Runtime Service Foundation",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "launcher_health_packet",
                "source": "Launcher and Health Monitor Foundation",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "chat_bridge_packet",
                "source": "Chat Bridge and Session State Foundation",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "plugin_permission_dashboard_packet",
                "source": "Plugin / Permission Dashboard Foundation",
                "runtime_fetch_enabled": False,
            },
            {
                "id": "roadmap_packet",
                "source": "Roadmap documentation",
                "runtime_fetch_enabled": False,
            },
        ]

    def theme_tokens(self) -> list[dict[str, Any]]:
        return [
            {"id": "aura_identity_accent", "purpose": "Primary AURA accent token blueprint."},
            {"id": "safe_idle_state", "purpose": "Safe idle status visual token blueprint."},
            {"id": "permission_pending_state", "purpose": "Permission pending visual token blueprint."},
            {"id": "runtime_disabled_state", "purpose": "Runtime disabled visual token blueprint."},
            {"id": "local_only_state", "purpose": "Localhost-only visual token blueprint."},
            {"id": "checkpoint_state", "purpose": "Roadmap checkpoint visual token blueprint."},
        ]

    def accessibility_notes(self) -> list[str]:
        return [
            "Static prototype should support keyboard-readable layout.",
            "Status indicators should not rely only on color.",
            "Permission states should use explicit labels.",
            "Safe idle state should be visible on every page.",
            "Runtime disabled states should be visible before any future runtime action.",
            "Navigation labels should match route and panel names.",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Prepare Local Console static prototype structure planning.",
            "Prepare static page blueprint planning.",
            "Prepare static asset group blueprint planning.",
            "Prepare panel layout blueprint planning.",
            "Prepare route-to-static-page mapping planning.",
            "Prepare dashboard data placeholder contract planning.",
            "Prepare theme token blueprint planning.",
            "Prepare accessibility blueprint planning.",
            "Prepare static prototype safety policy planning.",
            "Keep Local Console static prototype planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "web_server_runtime",
            "local_web_server_start",
            "frontend_runtime",
            "backend_runtime",
            "api_runtime",
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
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "static_asset_file_creation_runtime",
            "html_file_generation_runtime",
            "css_file_generation_runtime",
            "js_file_generation_runtime",
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
            "local_console_static_prototype_foundation_only": True,
            "static_prototype_blueprint_only": True,
            "static_page_blueprint_only": True,
            "asset_blueprint_only": True,
            "route_mapping_blueprint_only": True,
            "data_placeholder_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "safe_idle_required": True,
            "local_console_static_prototype_data_ready": True,
            "web_server_runtime": False,
            "local_web_server_start": False,
            "frontend_runtime": False,
            "backend_runtime": False,
            "api_runtime": False,
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
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "static_asset_file_creation_runtime": False,
            "html_file_generation_runtime": False,
            "css_file_generation_runtime": False,
            "js_file_generation_runtime": False,
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

    def prototype_identity(self) -> dict[str, Any]:
        identity = self.load_identity()
        return {
            "prototype_name": "AURA Local Console Static Prototype",
            "console_name": "AURA Control Center",
            "server_name": "ATLAS",
            "project_name": identity.get("name", "AURA"),
            "creator": identity.get("creator", "Kiput"),
            "identity_version": identity.get("version"),
            "default_mode": "safe_idle_required",
            "runtime_mode": "blueprint_only",
            "auto_action_allowed": False,
        }

    def prototype_summary(self) -> dict[str, Any]:
        pages = self.static_pages()
        return {
            "local_console_static_prototype_foundation_ready": True,
            "static_prototype_structure_ready": True,
            "static_page_blueprint_ready": True,
            "static_asset_blueprint_ready": True,
            "panel_layout_blueprint_ready": True,
            "route_static_mapping_ready": True,
            "data_placeholder_contract_ready": True,
            "theme_token_blueprint_ready": True,
            "accessibility_blueprint_ready": True,
            "static_prototype_safety_policy_ready": True,
            "static_page_count": len(pages),
            "asset_group_count": len(self.asset_groups()),
            "panel_layout_count": len(self.panel_layouts()),
            "route_static_mapping_count": len(self.route_static_mappings()),
            "data_placeholder_contract_count": len(self.data_placeholder_contracts()),
            "theme_token_count": len(self.theme_tokens()),
            "accessibility_note_count": len(self.accessibility_notes()),
            "runtime_enabled_pages": sum(1 for item in pages if item["runtime_enabled"]),
            "static_files_created": 0,
            "html_files_created": 0,
            "css_files_created": 0,
            "js_files_created": 0,
            "routes_created": 0,
            "web_servers_started": 0,
            "ports_bound": 0,
            "browser_windows_opened": 0,
            "frontend_apps_started": 0,
            "backend_services_started": 0,
            "api_services_started": 0,
            "runtime_execution_features": 0,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA Local Console static prototype foundation"
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "local_console_static_prototype_may_prepare_static_blueprints_but_must_not_run_web_runtime",
            "prototype_identity": self.prototype_identity(),
            "prototype_plan_types": self.prototype_plan_types(),
            "prototype_summary": self.prototype_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def static_prototype_structure_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("static_prototype_structure_plan", target)
        plan["asset_groups"] = self.asset_groups()
        plan["rule"] = "Structure planning does not create static files or directories beyond development source changes."
        return plan

    def static_page_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("static_page_blueprint_plan", target)
        plan["static_pages"] = self.static_pages()
        plan["rule"] = "Static page blueprint does not render or serve pages."
        return plan

    def static_asset_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("static_asset_blueprint_plan", target)
        plan["asset_groups"] = self.asset_groups()
        plan["rule"] = "Asset blueprint does not generate HTML, CSS, JS, icons, mock data, or static files."
        return plan

    def panel_layout_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("panel_layout_blueprint_plan", target)
        plan["panel_layouts"] = self.panel_layouts()
        plan["rule"] = "Panel layout blueprint does not start UI runtime."
        return plan

    def route_static_mapping_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("route_static_mapping_plan", target)
        plan["route_static_mappings"] = self.route_static_mappings()
        plan["rule"] = "Route mapping blueprint does not create routes or bind ports."
        return plan

    def data_placeholder_contract_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("data_placeholder_contract_plan", target)
        plan["data_placeholder_contracts"] = self.data_placeholder_contracts()
        plan["rule"] = "Data placeholder contract does not fetch runtime data or start APIs."
        return plan

    def theme_token_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("theme_token_blueprint_plan", target)
        plan["theme_tokens"] = self.theme_tokens()
        plan["rule"] = "Theme token blueprint does not create CSS files or frontend runtime."
        return plan

    def accessibility_blueprint_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("accessibility_blueprint_plan", target)
        plan["accessibility_notes"] = self.accessibility_notes()
        plan["rule"] = "Accessibility blueprint records guidance only."
        return plan

    def static_prototype_safety_policy_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("static_prototype_safety_policy_plan", target)
        plan["safety_rules"] = [
            "Static prototype foundation must not start a web server.",
            "Static prototype foundation must not bind ports.",
            "Static prototype foundation must not launch a browser.",
            "Static prototype foundation must not create routes.",
            "Static prototype foundation must not serve files.",
            "Static prototype foundation must not run frontend/backend/API runtime.",
            "Static prototype foundation must not activate chat, plugin, service, launcher, permission, or action runtime.",
            "Static prototype foundation must remain safe_idle-first and metadata-only.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "prototype_identity": self.prototype_identity(),
            "prototype_plan_types": self.prototype_plan_types(),
            "static_pages": self.static_pages(),
            "asset_groups": self.asset_groups(),
            "panel_layouts": self.panel_layouts(),
            "route_static_mappings": self.route_static_mappings(),
            "data_placeholder_contracts": self.data_placeholder_contracts(),
            "theme_tokens": self.theme_tokens(),
            "accessibility_notes": self.accessibility_notes(),
            "prototype_summary": self.prototype_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.prototype_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "local_console_static_prototype_foundation_ready": True,
            "static_prototype_structure_plan_ready": True,
            "static_page_blueprint_plan_ready": True,
            "static_asset_blueprint_plan_ready": True,
            "panel_layout_blueprint_plan_ready": True,
            "route_static_mapping_plan_ready": True,
            "data_placeholder_contract_plan_ready": True,
            "theme_token_blueprint_plan_ready": True,
            "accessibility_blueprint_plan_ready": True,
            "static_prototype_safety_policy_plan_ready": True,
            "planner_ready": True,
            "context_ready": True,
            "local_console_static_prototype_data_ready": True,
            "prototype_plan_types": self.prototype_plan_types(),
            "plan_type_count": len(self.prototype_plan_types()),
            **summary,
            **boundary,
        }
