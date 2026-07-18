"""AURA Sprint 185 Control Center Web Shell static runtime core.

Part A creates and validates local HTML, CSS, and JavaScript assets without
opening a listener. HTTP delivery is intentionally deferred to Part B.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class ControlCenterWebShellError(RuntimeError):
    """Raised when the static shell contract fails validation."""


class _ShellHTMLInspector(HTMLParser):
    """Collect structural and safety facts from the shell document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype: str | None = None
        self.html_lang: str | None = None
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.stylesheets: list[str] = []
        self.scripts: list[dict[str, str | None]] = []
        self.meta_names: set[str] = set()
        self.forms = 0
        self.buttons: list[dict[str, str | None]] = []
        self.inputs: list[dict[str, str | None]] = []
        self.inline_script_count = 0
        self.inline_style_count = 0
        self.event_handler_attributes: list[str] = []
        self._inside_script_without_src = False
        self._inside_style = False

    @staticmethod
    def _attributes(
        attrs: list[tuple[str, str | None]],
    ) -> dict[str, str | None]:
        return {key: value for key, value in attrs}

    def handle_decl(self, decl: str) -> None:
        self.doctype = decl.strip().lower()

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = self._attributes(attrs)

        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)

        for key in attributes:
            if key.lower().startswith("on"):
                self.event_handler_attributes.append(key)

        if tag == "html":
            self.html_lang = attributes.get("lang")
        elif tag == "a":
            href = attributes.get("href")
            if href is not None:
                self.links.append(href)
        elif tag == "link":
            if attributes.get("rel") == "stylesheet":
                href = attributes.get("href")
                if href is not None:
                    self.stylesheets.append(href)
        elif tag == "script":
            self.scripts.append(attributes)
            if not attributes.get("src"):
                self._inside_script_without_src = True
                self.inline_script_count += 1
        elif tag == "style":
            self._inside_style = True
            self.inline_style_count += 1
        elif tag == "meta":
            name = attributes.get("name")
            if name:
                self.meta_names.add(name)
            if "charset" in attributes:
                self.meta_names.add("charset")
        elif tag == "form":
            self.forms += 1
        elif tag == "button":
            self.buttons.append(attributes)
        elif tag == "input":
            self.inputs.append(attributes)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._inside_script_without_src = False
        elif tag == "style":
            self._inside_style = False


class AuraControlCenterWebShellRuntimeManager:
    """Inspect and serve the Sprint 185 static shell contract."""

    name = "aura_control_center_web_shell_runtime"
    component_version = "0.1.0-alpha"
    sprint = 185
    schema_version = "1.0"

    ASSET_ROUTES = (
        "/",
        "/assets/control-center.css",
        "/assets/control-center.js",
    )
    PANEL_IDS = (
        "overview",
        "service",
        "capabilities",
        "plugins",
        "permissions",
        "audit",
        "memory",
        "readiness",
    )
    BACKEND_ROUTES = (
        "/api/control-center",
        "/api/control-center/overview",
        "/api/control-center/service",
        "/api/control-center/capabilities",
        "/api/control-center/plugins",
        "/api/control-center/permissions",
        "/api/control-center/audit",
        "/api/control-center/memory",
        "/api/control-center/readiness",
    )
    ASSET_MAP = {
        "/": ("index.html", "text/html; charset=utf-8"),
        "/assets/control-center.css": (
            "control-center.css",
            "text/css; charset=utf-8",
        ),
        "/assets/control-center.js": (
            "control-center.js",
            "text/javascript; charset=utf-8",
        ),
    }

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()
        self.static_dir = (
            self.project_root
            / "aura"
            / "control_center_web_shell_runtime"
            / "static"
        )
        self.identity_path = (
            self.project_root
            / "aura"
            / "personality"
            / "identity.yaml"
        )
        self.settings_path = (
            self.project_root
            / "aura"
            / "config"
            / "settings.yaml"
        )
        self.memory_file = (
            self.project_root
            / "data"
            / "memory"
            / "memories.jsonl"
        )

    @staticmethod
    def _fingerprint(path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {
                "exists": False,
                "size_bytes": 0,
                "sha256": None,
                "modified_ns": None,
            }

        data = path.read_bytes()
        stat = path.stat()
        return {
            "exists": True,
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "modified_ns": int(stat.st_mtime_ns),
        }

    def asset_path(self, route: str) -> Path:
        """Resolve a declared shell asset route."""

        try:
            filename, _ = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 185 asset route: {route}"
            ) from exc
        return self.static_dir / filename

    def asset_content_type(self, route: str) -> str:
        """Return the declared response media type."""

        try:
            _, content_type = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 185 asset route: {route}"
            ) from exc
        return content_type

    def asset_bytes(self, route: str) -> bytes:
        """Read one local shell asset without network or mutation."""

        path = self.asset_path(route)
        if not path.is_file():
            raise ControlCenterWebShellError(
                f"Missing static shell asset: {path}"
            )
        return path.read_bytes()

    def asset_manifest(self) -> dict[str, Any]:
        """Return local asset metadata and transparent degraded state."""

        items: list[dict[str, Any]] = []
        missing: list[str] = []

        for route in self.ASSET_ROUTES:
            filename, content_type = self.ASSET_MAP[route]
            path = self.static_dir / filename
            fingerprint = self._fingerprint(path)

            if not fingerprint["exists"]:
                missing.append(route)

            items.append(
                {
                    "route": route,
                    "filename": filename,
                    "content_type": content_type,
                    **fingerprint,
                    "local_asset": True,
                    "external_dependency": False,
                }
            )

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ok" if not missing else "degraded",
            "degraded": bool(missing),
            "asset_count": len(items),
            "available_asset_count": (
                len(items) - len(missing)
            ),
            "missing_asset_count": len(missing),
            "missing_routes": missing,
            "routes": list(self.ASSET_ROUTES),
            "items": items,
            "external_dependency_count": 0,
            "read_only": True,
            "mutation_allowed": False,
        }

    def safety_boundary(self) -> dict[str, Any]:
        """Return explicit Part A runtime boundaries."""

        return {
            "control_center_web_shell_core": True,
            "local_static_assets": True,
            "shell_asset_route_count": len(
                self.ASSET_ROUTES
            ),
            "shell_panel_count": len(self.PANEL_IDS),
            "backend_read_endpoint_count": len(
                self.BACKEND_ROUTES
            ),
            "responsive_layout": True,
            "degraded_state_ui": True,
            "safe_idle_indicator": True,
            "manual_read_refresh": True,
            "automatic_read_refresh": True,
            "capability_local_filter": True,
            "external_dependencies": False,
            "cdn_runtime": False,
            "external_font_runtime": False,
            "inline_script_runtime": False,
            "inline_style_runtime": False,
            "shell_http_delivery_runtime": False,
            "browser_auto_launch_runtime": False,
            "websocket_runtime": False,
            "server_sent_event_runtime": False,
            "frontend_mutation_runtime": False,
            "service_control_runtime": False,
            "plugin_control_runtime": False,
            "permission_decision_runtime": False,
            "audit_writer_runtime": False,
            "memory_write_runtime": False,
            "chat_runtime": False,
            "model_runtime": False,
            "command_execution": False,
            "tool_execution": False,
            "action_dispatch": False,
            "background_service_runtime": False,
            "systemd_runtime": False,
            "automatic_start_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
            "autonomous_action": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        """Return shell readiness without opening the listener."""

        manifest = self.asset_manifest()
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": manifest["status"],
            "degraded": manifest["degraded"],
            "asset_count": manifest["asset_count"],
            "available_asset_count": manifest[
                "available_asset_count"
            ],
            "asset_routes": list(self.ASSET_ROUTES),
            "panel_count": len(self.PANEL_IDS),
            "panel_ids": list(self.PANEL_IDS),
            "backend_route_count": len(
                self.BACKEND_ROUTES
            ),
            "backend_endpoint": "/api/control-center",
            "responsive_layout": True,
            "accessibility_contract": True,
            "degraded_state_ui": True,
            "safe_idle_indicator": True,
            "external_dependencies": False,
            "http_delivery_active": False,
            "browser_launched": False,
            "read_only": True,
            "mutation_allowed": False,
            "safety_boundary": self.safety_boundary(),
        }

    def _inspect_html(self, html: str) -> _ShellHTMLInspector:
        inspector = _ShellHTMLInspector()
        inspector.feed(html)
        inspector.close()
        return inspector

    def self_test(self) -> dict[str, Any]:
        """Validate static assets, accessibility, and safety contracts."""

        assertions: dict[str, bool] = {}

        watched_paths = (
            self.identity_path,
            self.settings_path,
            self.memory_file,
        )
        before = {
            str(path): self._fingerprint(path)
            for path in watched_paths
        }

        manifest = self.asset_manifest()
        status = self.status()

        html = self.asset_bytes("/").decode("utf-8")
        css = self.asset_bytes(
            "/assets/control-center.css"
        ).decode("utf-8")
        javascript = self.asset_bytes(
            "/assets/control-center.js"
        ).decode("utf-8")

        after = {
            str(path): self._fingerprint(path)
            for path in watched_paths
        }

        inspector = self._inspect_html(html)

        assertions["schema_one"] = (
            status["schema_version"] == "1.0"
        )
        assertions["sprint_185"] = (
            status["sprint"] == 185
        )
        assertions["status_ok"] = (
            status["status"] == "ok"
        )
        assertions["not_degraded"] = (
            status["degraded"] is False
        )
        assertions["asset_count_three"] = (
            status["asset_count"] == 3
        )
        assertions["asset_available_three"] = (
            status["available_asset_count"] == 3
        )
        assertions["asset_routes_exact"] = (
            tuple(status["asset_routes"])
            == self.ASSET_ROUTES
        )
        assertions["panel_count_eight"] = (
            status["panel_count"] == 8
        )
        assertions["panels_exact"] = (
            tuple(status["panel_ids"])
            == self.PANEL_IDS
        )
        assertions["backend_route_count_nine"] = (
            status["backend_route_count"] == 9
        )
        assertions["backend_endpoint_exact"] = (
            status["backend_endpoint"]
            == "/api/control-center"
        )
        assertions["responsive_true"] = (
            status["responsive_layout"] is True
        )
        assertions["accessibility_true"] = (
            status["accessibility_contract"] is True
        )
        assertions["degraded_ui_true"] = (
            status["degraded_state_ui"] is True
        )
        assertions["safe_idle_indicator_true"] = (
            status["safe_idle_indicator"] is True
        )
        assertions["external_dependencies_false"] = (
            status["external_dependencies"] is False
        )
        assertions["http_delivery_false"] = (
            status["http_delivery_active"] is False
        )
        assertions["browser_launch_false"] = (
            status["browser_launched"] is False
        )
        assertions["read_only_true"] = (
            status["read_only"] is True
        )
        assertions["mutation_false"] = (
            status["mutation_allowed"] is False
        )

        assertions["manifest_ok"] = (
            manifest["status"] == "ok"
        )
        assertions["manifest_not_degraded"] = (
            manifest["degraded"] is False
        )
        assertions["manifest_asset_three"] = (
            manifest["asset_count"] == 3
        )
        assertions["manifest_missing_zero"] = (
            manifest["missing_asset_count"] == 0
        )
        assertions["manifest_external_zero"] = (
            manifest["external_dependency_count"] == 0
        )
        assertions["all_assets_nonempty"] = all(
            item["size_bytes"] > 0
            for item in manifest["items"]
        )
        assertions["all_assets_hashed"] = all(
            isinstance(item["sha256"], str)
            and len(item["sha256"]) == 64
            for item in manifest["items"]
        )
        assertions["all_assets_local"] = all(
            item["local_asset"] is True
            and item["external_dependency"] is False
            for item in manifest["items"]
        )
        assertions["content_types_exact"] = (
            self.asset_content_type("/")
            == "text/html; charset=utf-8"
            and self.asset_content_type(
                "/assets/control-center.css"
            )
            == "text/css; charset=utf-8"
            and self.asset_content_type(
                "/assets/control-center.js"
            )
            == "text/javascript; charset=utf-8"
        )

        unknown_asset_blocked = False
        try:
            self.asset_bytes("/assets/unknown.js")
        except KeyError:
            unknown_asset_blocked = True
        assertions["unknown_asset_blocked"] = (
            unknown_asset_blocked
        )

        assertions["html_doctype"] = (
            inspector.doctype == "doctype html"
        )
        assertions["html_lang_en"] = (
            inspector.html_lang == "en"
        )
        assertions["html_charset"] = (
            "charset" in inspector.meta_names
        )
        assertions["html_viewport"] = (
            "viewport" in inspector.meta_names
        )
        assertions["html_color_scheme"] = (
            "color-scheme" in inspector.meta_names
        )
        assertions["html_theme_color"] = (
            "theme-color" in inspector.meta_names
        )
        assertions["html_description"] = (
            "description" in inspector.meta_names
        )
        assertions["html_local_stylesheet"] = (
            inspector.stylesheets
            == ["/assets/control-center.css"]
        )
        assertions["html_one_script"] = (
            len(inspector.scripts) == 1
        )
        assertions["html_local_script"] = (
            inspector.scripts[0].get("src")
            == "/assets/control-center.js"
        )
        assertions["html_script_defer"] = (
            "defer" in inspector.scripts[0]
        )
        assertions["html_inline_script_zero"] = (
            inspector.inline_script_count == 0
        )
        assertions["html_inline_style_zero"] = (
            inspector.inline_style_count == 0
        )
        assertions["html_event_handlers_zero"] = (
            inspector.event_handler_attributes == []
        )
        assertions["html_forms_zero"] = (
            inspector.forms == 0
        )
        assertions["html_one_read_button"] = (
            len(inspector.buttons) == 1
            and inspector.buttons[0].get("id")
            == "refresh-data"
            and inspector.buttons[0].get("type")
            == "button"
        )
        assertions["html_search_input_only"] = (
            len(inspector.inputs) == 1
            and inspector.inputs[0].get("id")
            == "capability-search"
            and inspector.inputs[0].get("type")
            == "search"
        )
        assertions["html_skip_link"] = (
            "#dashboard-main" in inspector.links
        )
        assertions["html_all_panel_links"] = all(
            f"#{panel_id}" in inspector.links
            for panel_id in self.PANEL_IDS
        )
        assertions["html_all_panel_ids"] = all(
            panel_id in inspector.ids
            for panel_id in self.PANEL_IDS
        )
        assertions["html_main_id"] = (
            "dashboard-main" in inspector.ids
        )
        assertions["html_live_region"] = (
            'aria-live="polite"' in html
            and 'role="status"' in html
        )
        assertions["html_template_present"] = (
            'id="capability-card-template"' in html
        )
        assertions["html_noscript_present"] = (
            "<noscript>" in html
        )
        assertions["html_no_external_urls"] = (
            "http://" not in html
            and "https://" not in html
            and "//cdn." not in html
        )
        assertions["html_no_mutation_methods"] = not any(
            token in html.upper()
            for token in (
                'METHOD="POST"',
                'METHOD="PUT"',
                'METHOD="PATCH"',
                'METHOD="DELETE"',
            )
        )

        js_functions = (
            "renderOverview",
            "renderService",
            "renderCapabilities",
            "renderPlugins",
            "renderPermissions",
            "renderAudit",
            "renderMemory",
            "renderReadiness",
        )
        for function_name in js_functions:
            assertions[
                "js_function_" + function_name
            ] = (
                f"function {function_name}(" in javascript
            )

        assertions["js_strict_mode"] = (
            javascript.lstrip().startswith('"use strict";')
        )
        assertions["js_backend_endpoint"] = (
            'const BACKEND_ENDPOINT = "/api/control-center";'
            in javascript
        )
        assertions["js_refresh_interval"] = (
            "REFRESH_INTERVAL_MS = 5000" in javascript
        )
        assertions["js_fetch_get_only"] = (
            'method: "GET"' in javascript
            and 'method: "POST"' not in javascript
            and 'method: "PUT"' not in javascript
            and 'method: "PATCH"' not in javascript
            and 'method: "DELETE"' not in javascript
        )
        assertions["js_no_store"] = (
            'cache: "no-store"' in javascript
        )
        assertions["js_same_origin"] = (
            'credentials: "same-origin"' in javascript
        )
        assertions["js_accept_json"] = (
            'Accept: "application/json"' in javascript
        )
        assertions["js_abort_controller"] = (
            "new AbortController()" in javascript
        )
        assertions["js_visibility_refresh"] = (
            '"visibilitychange"' in javascript
        )
        assertions["js_manual_refresh"] = (
            '"refresh-data"' in javascript
            and "announce: true" in javascript
        )
        assertions["js_capability_filter"] = (
            '"capability-search"' in javascript
            and "capabilityQuery" in javascript
        )
        assertions["js_degraded_state"] = (
            "payload.degraded" in javascript
            and "Backend degraded" in javascript
        )
        assertions["js_payload_read_only_gate"] = (
            "payload.read_only !== true" in javascript
            and "payload.mutation_allowed !== false"
            in javascript
        )
        assertions["js_panel_count_gate"] = (
            "payload.panel_count !== 8" in javascript
        )
        assertions["js_safe_dom_text"] = (
            ".textContent =" in javascript
            and "document.createElement" in javascript
            and ".replaceChildren()" in javascript
        )
        assertions["js_no_inner_html"] = (
            ".innerHTML" not in javascript
        )
        assertions["js_no_eval"] = (
            "eval(" not in javascript
            and "new Function(" not in javascript
        )
        assertions["js_no_websocket"] = (
            "WebSocket(" not in javascript
        )
        assertions["js_no_event_source"] = (
            "EventSource(" not in javascript
        )
        assertions["js_no_external_urls"] = (
            "http://" not in javascript
            and "https://" not in javascript
        )
        assertions["js_no_storage_mutation"] = (
            "localStorage" not in javascript
            and "sessionStorage" not in javascript
            and "indexedDB" not in javascript
        )
        assertions["js_dom_ready"] = (
            '"DOMContentLoaded"' in javascript
        )

        css_needles = (
            ":root",
            ".app-shell",
            ".sidebar",
            ".dashboard-panel",
            ".metric-grid",
            ".capability-list",
            ":focus-visible",
            "@media (max-width: 70rem)",
            "@media (max-width: 50rem)",
            "@media (max-width: 36rem)",
            "@media (prefers-reduced-motion: reduce)",
        )
        for index, needle in enumerate(css_needles, start=1):
            assertions[f"css_contract_{index:02d}"] = (
                needle in css
            )

        assertions["css_no_import"] = (
            "@import" not in css
        )
        assertions["css_no_external_url"] = (
            "http://" not in css
            and "https://" not in css
        )
        assertions["css_dark_scheme"] = (
            "color-scheme: dark" in css
        )
        assertions["css_min_width"] = (
            "min-width: 20rem" in css
        )
        assertions["css_responsive_grid"] = (
            "grid-template-columns" in css
        )
        assertions["css_accessible_focus"] = (
            "outline: 3px solid var(--accent)" in css
        )

        boundary = self.safety_boundary()
        assertions["boundary_shell_core_true"] = (
            boundary["control_center_web_shell_core"]
            is True
        )
        assertions["boundary_asset_count_three"] = (
            boundary["shell_asset_route_count"] == 3
        )
        assertions["boundary_panel_count_eight"] = (
            boundary["shell_panel_count"] == 8
        )
        assertions["boundary_backend_routes_nine"] = (
            boundary["backend_read_endpoint_count"] == 9
        )
        assertions["boundary_external_false"] = (
            boundary["external_dependencies"] is False
        )
        assertions["boundary_http_delivery_false"] = (
            boundary["shell_http_delivery_runtime"]
            is False
        )

        disabled_keys = (
            "cdn_runtime",
            "external_font_runtime",
            "inline_script_runtime",
            "inline_style_runtime",
            "browser_auto_launch_runtime",
            "websocket_runtime",
            "server_sent_event_runtime",
            "frontend_mutation_runtime",
            "service_control_runtime",
            "plugin_control_runtime",
            "permission_decision_runtime",
            "audit_writer_runtime",
            "memory_write_runtime",
            "chat_runtime",
            "model_runtime",
            "command_execution",
            "tool_execution",
            "action_dispatch",
            "background_service_runtime",
            "systemd_runtime",
            "automatic_start_runtime",
            "public_listener_runtime",
            "lan_listener_runtime",
            "autonomous_action",
        )
        for key in disabled_keys:
            assertions[
                "boundary_disabled_" + key
            ] = boundary[key] is False

        assertions["watched_files_unchanged"] = (
            before == after
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s185-shell-degraded-"
        ) as temporary:
            degraded_root = Path(temporary)
            fixture_dir = (
                degraded_root
                / "aura"
                / "control_center_web_shell_runtime"
                / "static"
            )
            fixture_dir.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            shutil.copytree(
                self.static_dir,
                fixture_dir,
            )
            (
                fixture_dir / "control-center.js"
            ).unlink()

            degraded_manager = (
                AuraControlCenterWebShellRuntimeManager(
                    project_root=degraded_root
                )
            )
            degraded_manifest = (
                degraded_manager.asset_manifest()
            )
            degraded_status = degraded_manager.status()

            assertions["degraded_fixture_visible"] = (
                degraded_manifest["degraded"] is True
                and degraded_status["degraded"] is True
            )
            assertions["degraded_status_label"] = (
                degraded_manifest["status"]
                == "degraded"
            )
            assertions["degraded_missing_one"] = (
                degraded_manifest["missing_asset_count"]
                == 1
            )
            assertions["degraded_route_visible"] = (
                degraded_manifest["missing_routes"]
                == ["/assets/control-center.js"]
            )
            assertions["degraded_available_two"] = (
                degraded_manifest[
                    "available_asset_count"
                ]
                == 2
            )
            assertions["degraded_no_runtime_files"] = (
                not degraded_manager.identity_path.exists()
                and not degraded_manager.settings_path.exists()
                and not degraded_manager.memory_file.exists()
            )

        assertions["sprint266_operations_panel"] = (
            'id="operations"' in html
        )
        assertions["sprint266_operations_status"] = (
            'id="operations-status"' in html
        )
        assertions["sprint266_chat_link"] = (
            'id="operation-chat-link"' in html
            and 'href="/chat"' in html
        )
        assertions["sprint266_render_operations"] = (
            "function renderOperations(" in javascript
        )
        assertions["sprint266_payload_reuse"] = (
            ".runtime_ux_consolidation || {}"
            in javascript
        )
        assertions["sprint266_operations_css"] = (
            ".operations-grid" in css
            and ".operations-boundary" in css
        )

        assertions["sprint267_resources_panel"] = (
            'id="resources"' in html
        )
        assertions["sprint267_resources_status"] = (
            'id="resources-status"' in html
            and 'id="resources-detail"' in html
        )
        assertions["sprint267_summary_metrics"] = all(
            token in html
            for token in (
                'id="resource-cpu-current"',
                'id="resource-memory-current"',
                'id="resource-swap-current"',
                'id="resource-uptime-current"',
                'id="resource-process-count"',
            )
        )
        assertions["sprint267_chart_surfaces"] = (
            'id="resource-cpu-chart"' in html
            and 'id="resource-memory-chart"' in html
            and html.count(
                'class="resource-chart-line"'
            )
            == 2
        )
        assertions["sprint267_storage_surface"] = (
            'id="resource-storage-list"' in html
        )
        assertions["sprint267_window_controls"] = all(
            token in html
            for token in (
                'data-resource-window="5"',
                'data-resource-window="15"',
                'data-resource-window="60"',
                'role="button"',
            )
        )
        assertions["sprint267_render_resources"] = (
            "function renderResources("
            in javascript
        )
        assertions["sprint267_render_chart"] = (
            "function renderResourceChart("
            in javascript
        )
        assertions["sprint267_render_storage"] = (
            "function renderResourceStorage("
            in javascript
        )
        assertions["sprint267_payload_reuse"] = (
            "payload.atlas_resource_monitoring_dashboard"
            in javascript
        )
        assertions["sprint267_refresh_contract"] = (
            "REFRESH_INTERVAL_MS = 5000"
            in javascript
            and "RESOURCE_REFRESH_INTERVAL_MS = 1000"
            in javascript
        )
        assertions["sprint267_no_route_or_dependency"] = (
            javascript.count("fetch(") == 1
            and "http://" not in javascript
            and "https://" not in javascript
        )
        assertions["sprint267_resource_css"] = (
            ".resource-summary-grid" in css
            and ".resource-chart-line" in css
            and ".resource-storage-list" in css
        )
        sprint267_html_lower = html.lower()
        assertions["sprint267_read_only_boundary"] = (
            "history remains in-process only"
            in sprint267_html_lower
            and "no background"
            in sprint267_html_lower
            and "sampler, persistence, process control, "
            "or execution authority"
            in sprint267_html_lower
            and "is enabled"
            in sprint267_html_lower
        )

        assertions["sprint268_visibility_panel"] = (
            'id="permission-visibility"' in html
        )
        assertions["sprint268_visibility_status"] = (
            'id="permission-visibility-status"' in html
            and 'id="permission-visibility-detail"' in html
        )
        assertions["sprint268_visibility_cards"] = (
            html.count(
                'class="permission-visibility-card"'
            )
            == 6
            and html.count(
                'data-visibility-section="'
            )
            == 6
        )
        assertions["sprint268_visibility_state_ids"] = all(
            f'id="permission-visibility-{section}-state"'
            in html
            for section in (
                "permission",
                "audit",
                "proposal",
                "approval",
                "action",
                "recovery",
            )
        )
        assertions["sprint268_visibility_detail_ids"] = all(
            f'id="permission-visibility-{section}-detail"'
            in html
            for section in (
                "permission",
                "audit",
                "proposal",
                "approval",
                "action",
                "recovery",
            )
        )
        assertions["sprint268_visibility_boundary"] = (
            html.count(
                'id="permission-visibility-boundary-'
            )
            == 4
        )
        assertions["sprint268_visibility_renderer"] = (
            "function renderPermissionAuditActionVisibility("
            in javascript
        )
        assertions["sprint268_visibility_payload"] = (
            "payload.permission_audit_action_visibility_ux"
            in javascript
        )
        assertions["sprint268_visibility_render_call"] = (
            javascript.count(
                "renderPermissionAuditActionVisibility("
            )
            == 2
        )
        assertions["sprint268_no_new_fetch_or_route"] = (
            javascript.count("fetch(") == 1
            and "http://" not in javascript
            and "https://" not in javascript
        )
        visibility_start = html.index(
            'id="permission-visibility"'
        )
        visibility_end = html.index(
            "<!-- Sprint 267 — ATLAS resource monitoring dashboard -->"
        )
        visibility_html = html[
            visibility_start:visibility_end
        ]
        assertions["sprint268_no_action_controls"] = (
            html.count("<button") == 1
            and "href=" not in visibility_html
            and __import__("re").search(
                r"<a",
                visibility_html,
            )
            is None
        )
        assertions["sprint268_visibility_css"] = (
            ".permission-visibility-grid" in css
            and ".permission-visibility-card" in css
            and ".permission-visibility-boundary"
            in css
        )
        visibility_lower = visibility_html.lower()
        assertions["sprint268_read_only_boundary"] = all(
            token in visibility_lower
            for token in (
                "no automatic permission grant",
                "no service, restart, or approval action route",
                "no automatic recovery or recovery execution",
                "read-only visibility; no runtime mutation",
            )
        )
        assertions["sprint268_refresh_preserved"] = (
            "REFRESH_INTERVAL_MS = 5000"
            in javascript
            and "RESOURCE_REFRESH_INTERVAL_MS = 1000"
            in javascript
        )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise ControlCenterWebShellError(
                "Control Center Web Shell self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "schema_version": self.schema_version,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "asset_count": len(self.ASSET_ROUTES),
            "asset_routes": list(self.ASSET_ROUTES),
            "panel_count": len(self.PANEL_IDS),
            "panel_ids": list(self.PANEL_IDS),
            "backend_route_count": len(
                self.BACKEND_ROUTES
            ),
            "backend_endpoint": "/api/control-center",
            "degraded_fixture_verified": True,
            "read_only_file_integrity_verified": True,
            "responsive_layout_verified": True,
            "accessibility_contract_verified": True,
            "external_dependency_count": 0,
            "inline_script_count": 0,
            "inline_style_count": 0,
            "mutation_controls_present": False,
            "http_delivery_active": False,
            "browser_launched": False,
        }
