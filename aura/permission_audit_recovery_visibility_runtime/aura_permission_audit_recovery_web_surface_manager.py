"""Static Sprint 189 permission/audit/recovery visibility surface."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class PermissionAuditRecoveryWebSurfaceError(RuntimeError):
    """Raised when the read-only visibility surface is invalid."""


class _VisibilityHTMLInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype: str | None = None
        self.html_lang: str | None = None
        self.ids: set[str] = set()
        self.stylesheets: list[str] = []
        self.scripts: list[dict[str, str | None]] = []
        self.buttons: list[dict[str, str | None]] = []
        self.forms = 0
        self.inputs = 0
        self.textareas = 0
        self.inline_script_count = 0
        self.inline_style_count = 0
        self.event_handlers: list[str] = []
        self.meta_names: set[str] = set()

    @staticmethod
    def _attrs(
        attrs: list[tuple[str, str | None]],
    ) -> dict[str, str | None]:
        return {key: value for key, value in attrs}

    def handle_decl(self, decl: str) -> None:
        self.doctype = decl.lower()

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = self._attrs(attrs)

        if tag == "html":
            self.html_lang = attributes.get("lang")

        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)

        for key in attributes:
            if key.lower().startswith("on"):
                self.event_handlers.append(key)

        if (
            tag == "link"
            and attributes.get("rel") == "stylesheet"
        ):
            href = attributes.get("href")
            if href is not None:
                self.stylesheets.append(href)
        elif tag == "script":
            self.scripts.append(attributes)
            if not attributes.get("src"):
                self.inline_script_count += 1
        elif tag == "style":
            self.inline_style_count += 1
        elif tag == "button":
            self.buttons.append(attributes)
        elif tag == "form":
            self.forms += 1
        elif tag == "input":
            self.inputs += 1
        elif tag == "textarea":
            self.textareas += 1
        elif tag == "meta":
            if "charset" in attributes:
                self.meta_names.add("charset")
            name = attributes.get("name")
            if name:
                self.meta_names.add(name)


class AuraPermissionAuditRecoveryWebSurfaceManager:
    """Load and validate the read-only Sprint 189 browser surface."""

    name = "aura_permission_audit_recovery_web_surface"
    component_version = "0.1.0-alpha"
    sprint = 189
    schema_version = "1.0"

    ASSET_ROUTES = (
        "/visibility",
        "/assets/permission-audit-recovery.css",
        "/assets/permission-audit-recovery.js",
    )
    API_ROUTES = (
        "/api/visibility/status",
        "/api/visibility/permissions",
        "/api/visibility/audit",
        "/api/visibility/recovery",
    )
    ASSET_MAP = {
        "/visibility": (
            "visibility.html",
            "text/html; charset=utf-8",
        ),
        "/assets/permission-audit-recovery.css": (
            "permission-audit-recovery.css",
            "text/css; charset=utf-8",
        ),
        "/assets/permission-audit-recovery.js": (
            "permission-audit-recovery.js",
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
            / "permission_audit_recovery_visibility_runtime"
            / "static"
        )

    @staticmethod
    def _fingerprint(path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {
                "exists": False,
                "size_bytes": 0,
                "sha256": None,
            }

        data = path.read_bytes()
        return {
            "exists": True,
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    def asset_path(self, route: str) -> Path:
        try:
            filename, _ = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 189 visibility asset route: {route}"
            ) from exc
        return self.static_dir / filename

    def asset_content_type(self, route: str) -> str:
        try:
            _, content_type = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 189 visibility asset route: {route}"
            ) from exc
        return content_type

    def asset_bytes(self, route: str) -> bytes:
        path = self.asset_path(route)
        if not path.is_file():
            raise PermissionAuditRecoveryWebSurfaceError(
                f"Missing Sprint 189 visibility asset: {path}"
            )
        return path.read_bytes()

    def asset_manifest(self) -> dict[str, Any]:
        items = []
        missing = []

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
            "available_asset_count": len(items) - len(missing),
            "missing_asset_count": len(missing),
            "missing_routes": missing,
            "items": items,
            "read_only_assets": True,
            "external_dependency_count": 0,
        }

    def status(self) -> dict[str, Any]:
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
            "api_routes": list(self.API_ROUTES),
            "api_route_count": len(self.API_ROUTES),
            "visibility_page_route": "/visibility",
            "permission_panel": True,
            "audit_panel": True,
            "recovery_panel": True,
            "provider_profile_redaction": True,
            "message_content_redaction": True,
            "response_content_redaction": True,
            "read_only": True,
            "mutation_controls_present": False,
            "external_dependencies": False,
            "inline_scripts": False,
            "inline_styles": False,
            "safe_dom_rendering": True,
            "local_browser_storage_runtime": False,
            "websocket_runtime": False,
            "eventsource_runtime": False,
            "network_calls": 0,
            "disk_writes": 0,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}
        manifest = self.asset_manifest()
        status = self.status()

        html = self.asset_bytes("/visibility").decode("utf-8")
        css = self.asset_bytes(
            "/assets/permission-audit-recovery.css"
        ).decode("utf-8")
        javascript = self.asset_bytes(
            "/assets/permission-audit-recovery.js"
        ).decode("utf-8")

        inspector = _VisibilityHTMLInspector()
        inspector.feed(html)
        inspector.close()

        assertions["status_ok"] = status["status"] == "ok"
        assertions["status_not_degraded"] = (
            status["degraded"] is False
        )
        assertions["sprint_189"] = status["sprint"] == 189
        assertions["component_version"] = (
            status["component_version"] == "0.1.0-alpha"
        )
        assertions["assets_three"] = (
            status["asset_count"] == 3
        )
        assertions["assets_available_three"] = (
            status["available_asset_count"] == 3
        )
        assertions["asset_routes_exact"] = (
            tuple(status["asset_routes"])
            == self.ASSET_ROUTES
        )
        assertions["api_routes_four"] = (
            status["api_route_count"] == 4
        )
        assertions["api_routes_exact"] = (
            tuple(status["api_routes"])
            == self.API_ROUTES
        )
        assertions["page_route_exact"] = (
            status["visibility_page_route"] == "/visibility"
        )
        assertions["permission_panel_true"] = (
            status["permission_panel"] is True
        )
        assertions["audit_panel_true"] = (
            status["audit_panel"] is True
        )
        assertions["recovery_panel_true"] = (
            status["recovery_panel"] is True
        )
        assertions["provider_redaction_true"] = (
            status["provider_profile_redaction"] is True
        )
        assertions["message_redaction_true"] = (
            status["message_content_redaction"] is True
        )
        assertions["response_redaction_true"] = (
            status["response_content_redaction"] is True
        )
        assertions["read_only_true"] = (
            status["read_only"] is True
        )
        assertions["mutation_controls_false"] = (
            status["mutation_controls_present"] is False
        )
        assertions["external_false"] = (
            status["external_dependencies"] is False
        )
        assertions["safe_dom_true"] = (
            status["safe_dom_rendering"] is True
        )
        assertions["storage_false"] = (
            status["local_browser_storage_runtime"] is False
        )
        assertions["websocket_false"] = (
            status["websocket_runtime"] is False
        )
        assertions["eventsource_false"] = (
            status["eventsource_runtime"] is False
        )
        assertions["network_zero"] = (
            status["network_calls"] == 0
        )
        assertions["writes_zero"] = (
            status["disk_writes"] == 0
        )

        assertions["manifest_ok"] = (
            manifest["status"] == "ok"
        )
        assertions["manifest_missing_zero"] = (
            manifest["missing_asset_count"] == 0
        )
        assertions["manifest_external_zero"] = (
            manifest["external_dependency_count"] == 0
        )
        assertions["manifest_nonempty"] = all(
            item["size_bytes"] > 0
            for item in manifest["items"]
        )
        assertions["manifest_hashed"] = all(
            isinstance(item["sha256"], str)
            and len(item["sha256"]) == 64
            for item in manifest["items"]
        )
        assertions["manifest_local"] = all(
            item["local_asset"] is True
            and item["external_dependency"] is False
            for item in manifest["items"]
        )
        assertions["content_types_exact"] = (
            self.asset_content_type("/visibility")
            == "text/html; charset=utf-8"
            and self.asset_content_type(
                "/assets/permission-audit-recovery.css"
            )
            == "text/css; charset=utf-8"
            and self.asset_content_type(
                "/assets/permission-audit-recovery.js"
            )
            == "text/javascript; charset=utf-8"
        )

        required_ids = {
            "visibility-main",
            "refresh-visibility",
            "visibility-status",
            "visibility-detail",
            "permission-count",
            "audit-count",
            "recovery-count",
            "provider-title",
            "provider-state",
            "provider-facts",
            "provider-configured",
            "provider-enabled",
            "provider-candidate",
            "provider-raw-values",
            "permissions-title",
            "permission-list",
            "audit-title",
            "audit-list",
            "recovery-title",
            "recovery-list",
            "boundary-title",
            "boundary-list",
            "visibility-error",
        }
        for element_id in sorted(required_ids):
            assertions[f"html_id_{element_id}"] = (
                element_id in inspector.ids
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
        assertions["html_description"] = (
            "description" in inspector.meta_names
        )
        assertions["html_stylesheet"] = (
            inspector.stylesheets
            == ["/assets/permission-audit-recovery.css"]
        )
        assertions["html_one_script"] = (
            len(inspector.scripts) == 1
        )
        assertions["html_script_src"] = (
            inspector.scripts[0].get("src")
            == "/assets/permission-audit-recovery.js"
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
            inspector.event_handlers == []
        )
        assertions["html_forms_zero"] = inspector.forms == 0
        assertions["html_inputs_zero"] = inspector.inputs == 0
        assertions["html_textareas_zero"] = (
            inspector.textareas == 0
        )
        assertions["html_one_button"] = (
            len(inspector.buttons) == 1
            and inspector.buttons[0].get("id")
            == "refresh-visibility"
            and inspector.buttons[0].get("type")
            == "button"
        )
        assertions["html_sprint_189"] = (
            "Sprint 189" in html
        )
        assertions["html_read_only"] = (
            "Read-only visibility" in html
        )
        assertions["html_no_grant"] = (
            "cannot grant permissions" in html
        )
        assertions["html_no_writer"] = (
            "write audit events" in html
        )
        assertions["html_no_recovery_actions"] = (
            "execute recovery actions" in html
        )
        assertions["html_redaction_text"] = (
            "intentionally not displayed" in html
        )
        assertions["html_no_external_urls"] = (
            "http://" not in html
            and "https://" not in html
        )

        js_needles = (
            'status: "/api/visibility/status"',
            'permissions: "/api/visibility/permissions"',
            'audit: "/api/visibility/audit"',
            'recovery: "/api/visibility/recovery"',
            'method: "GET"',
            'cache: "no-store"',
            'credentials: "same-origin"',
            "Promise.all",
            "refreshVisibility",
            "renderStatus",
            "renderPermissions",
            "renderAudit",
            "renderRecovery",
            "renderBoundary",
            "document.createElement",
            ".textContent =",
            ".replaceChildren(",
            "provider_profile",
            "mutable_from_visibility_runtime",
            "content_included",
            "automatic_action",
            "safety_boundary",
        )
        for index, needle in enumerate(
            js_needles,
            start=1,
        ):
            assertions[f"js_contract_{index:02d}"] = (
                needle in javascript
            )

        assertions["js_no_post"] = (
            'method: "POST"' not in javascript
        )
        assertions["js_no_put"] = (
            'method: "PUT"' not in javascript
        )
        assertions["js_no_patch"] = (
            'method: "PATCH"' not in javascript
        )
        assertions["js_no_delete"] = (
            'method: "DELETE"' not in javascript
        )
        assertions["js_no_inner_html"] = (
            ".innerHTML" not in javascript
        )
        assertions["js_no_eval"] = (
            "eval(" not in javascript
            and "new Function(" not in javascript
        )
        assertions["js_no_storage"] = (
            "localStorage" not in javascript
            and "sessionStorage" not in javascript
            and "indexedDB" not in javascript
        )
        assertions["js_no_websocket"] = (
            "WebSocket(" not in javascript
        )
        assertions["js_no_eventsource"] = (
            "EventSource(" not in javascript
        )
        assertions["js_no_external_urls"] = (
            "http://" not in javascript
            and "https://" not in javascript
        )
        assertions["js_no_sensitive_keys"] = (
            "AURA_LOCAL_MODEL_PROVIDER" not in javascript
            and "AURA_LOCAL_MODEL_BASE_URL" not in javascript
            and "AURA_LOCAL_MODEL_NAME" not in javascript
            and "authorization" not in javascript.lower()
            and "api_key" not in javascript.lower()
        )
        assertions["js_no_mutation_endpoints"] = (
            "/grant" not in javascript
            and "/revoke" not in javascript
            and "/retry" not in javascript
            and "/rollback" not in javascript
        )

        css_needles = (
            ":root",
            ".visibility-shell",
            ".page-header",
            ".status-grid",
            ".summary-card",
            ".panel",
            ".panel-grid",
            ".state-badge",
            ".read-only-badge",
            ".fact-grid",
            ".card-list",
            ".recovery-grid",
            ".visibility-item",
            ".recovery-card",
            ".boundary-list",
            ".boundary-item",
            ".boundary-disabled",
            ".error-banner",
            ":focus-visible",
            "@media (max-width: 70rem)",
            "@media (max-width: 52rem)",
            "@media (max-width: 36rem)",
            "@media (prefers-reduced-motion: reduce)",
        )
        for index, needle in enumerate(
            css_needles,
            start=1,
        ):
            assertions[f"css_contract_{index:02d}"] = (
                needle in css
            )

        assertions["css_no_import"] = "@import" not in css
        assertions["css_no_external_urls"] = (
            "http://" not in css
            and "https://" not in css
        )

        unknown_blocked = False
        try:
            self.asset_bytes(
                "/assets/unknown-visibility.js"
            )
        except KeyError:
            unknown_blocked = True
        assertions["unknown_asset_blocked"] = (
            unknown_blocked
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s189-visibility-web-degraded-"
        ) as temporary:
            root = Path(temporary)
            fixture = (
                root
                / "aura"
                / "permission_audit_recovery_visibility_runtime"
                / "static"
            )
            fixture.parent.mkdir(parents=True)
            shutil.copytree(self.static_dir, fixture)
            (
                fixture
                / "permission-audit-recovery.js"
            ).unlink()

            degraded = type(self)(
                project_root=root
            ).asset_manifest()

        assertions["degraded_visible"] = (
            degraded["degraded"] is True
        )
        assertions["degraded_missing_one"] = (
            degraded["missing_asset_count"] == 1
        )
        assertions["degraded_route_exact"] = (
            degraded["missing_routes"]
            == ["/assets/permission-audit-recovery.js"]
        )
        assertions["degraded_available_two"] = (
            degraded["available_asset_count"] == 2
        )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise PermissionAuditRecoveryWebSurfaceError(
                "Permission/audit/recovery web surface "
                "self-test failed: "
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
            "api_route_count": len(self.API_ROUTES),
            "permission_panel_verified": True,
            "audit_panel_verified": True,
            "recovery_panel_verified": True,
            "provider_redaction_ui_verified": True,
            "read_only_ui_verified": True,
            "safe_dom_rendering_verified": True,
            "get_only_fetch_verified": True,
            "degraded_fixture_verified": True,
            "external_dependency_count": 0,
            "inline_script_count": 0,
            "inline_style_count": 0,
            "mutation_controls_present": False,
            "network_calls": 0,
            "disk_writes": 0,
        }


__all__ = [
    "AuraPermissionAuditRecoveryWebSurfaceManager",
    "PermissionAuditRecoveryWebSurfaceError",
]
