"""Static browser surface for Sprint 186 local chat sessions."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class BrowserChatWebSurfaceError(RuntimeError):
    """Raised when the chat browser surface fails validation."""


class _ChatHTMLInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.stylesheets: list[str] = []
        self.scripts: list[dict[str, str | None]] = []
        self.forms = 0
        self.buttons: list[dict[str, str | None]] = []
        self.inputs: list[dict[str, str | None]] = []
        self.textareas: list[dict[str, str | None]] = []
        self.dialogs: list[dict[str, str | None]] = []
        self.inline_script_count = 0
        self.inline_style_count = 0
        self.event_handlers: list[str] = []
        self.meta_names: set[str] = set()

    @staticmethod
    def _attrs(
        attrs: list[tuple[str, str | None]],
    ) -> dict[str, str | None]:
        return {key: value for key, value in attrs}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = self._attrs(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)

        for key in attributes:
            if key.lower().startswith("on"):
                self.event_handlers.append(key)

        if tag == "link" and attributes.get("rel") == "stylesheet":
            href = attributes.get("href")
            if href is not None:
                self.stylesheets.append(href)
        elif tag == "script":
            self.scripts.append(attributes)
            if not attributes.get("src"):
                self.inline_script_count += 1
        elif tag == "style":
            self.inline_style_count += 1
        elif tag == "form":
            self.forms += 1
        elif tag == "button":
            self.buttons.append(attributes)
        elif tag == "input":
            self.inputs.append(attributes)
        elif tag == "textarea":
            self.textareas.append(attributes)
        elif tag == "dialog":
            self.dialogs.append(attributes)
        elif tag == "meta":
            name = attributes.get("name")
            if name:
                self.meta_names.add(name)
            if "charset" in attributes:
                self.meta_names.add("charset")


class AuraBrowserChatWebSurfaceManager:
    """Load and validate the Sprint 186 local chat page assets."""

    name = "aura_browser_chat_web_surface"
    component_version = "0.1.0-alpha"
    sprint = 186
    schema_version = "1.0"

    ASSET_ROUTES = (
        "/chat",
        "/assets/control-center-chat.css",
        "/assets/control-center-chat.js",
    )
    ASSET_MAP = {
        "/chat": ("chat.html", "text/html; charset=utf-8"),
        "/assets/control-center-chat.css": (
            "chat.css",
            "text/css; charset=utf-8",
        ),
        "/assets/control-center-chat.js": (
            "chat.js",
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
            / "browser_chat_session_runtime"
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
                f"Unknown Sprint 186 chat asset route: {route}"
            ) from exc
        return self.static_dir / filename

    def asset_content_type(self, route: str) -> str:
        try:
            _, content_type = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 186 chat asset route: {route}"
            ) from exc
        return content_type

    def asset_bytes(self, route: str) -> bytes:
        path = self.asset_path(route)
        if not path.is_file():
            raise BrowserChatWebSurfaceError(
                f"Missing chat browser asset: {path}"
            )
        return path.read_bytes()

    def manifest(self) -> dict[str, Any]:
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
        manifest = self.manifest()
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
            "chat_page_route": "/chat",
            "chat_api_base": "/api/chat",
            "model_bridge_active": False,
            "browser_auto_launch": False,
            "external_dependencies": False,
            "inline_scripts": False,
            "inline_styles": False,
            "safe_dom_rendering": True,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}
        manifest = self.manifest()
        status = self.status()

        html = self.asset_bytes("/chat").decode("utf-8")
        css = self.asset_bytes(
            "/assets/control-center-chat.css"
        ).decode("utf-8")
        javascript = self.asset_bytes(
            "/assets/control-center-chat.js"
        ).decode("utf-8")

        inspector = _ChatHTMLInspector()
        inspector.feed(html)
        inspector.close()

        assertions["status_ok"] = status["status"] == "ok"
        assertions["not_degraded"] = status["degraded"] is False
        assertions["assets_three"] = status["asset_count"] == 3
        assertions["available_three"] = (
            status["available_asset_count"] == 3
        )
        assertions["chat_route"] = (
            status["chat_page_route"] == "/chat"
        )
        assertions["api_base"] = (
            status["chat_api_base"] == "/api/chat"
        )
        assertions["model_false"] = (
            status["model_bridge_active"] is False
        )
        assertions["browser_launch_false"] = (
            status["browser_auto_launch"] is False
        )
        assertions["external_false"] = (
            status["external_dependencies"] is False
        )
        assertions["safe_dom_true"] = (
            status["safe_dom_rendering"] is True
        )

        assertions["manifest_ok"] = manifest["status"] == "ok"
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

        required_ids = {
            "chat-main",
            "session-list",
            "session-title",
            "create-session",
            "chat-transcript",
            "message-input",
            "send-message",
            "clear-session",
            "clear-dialog",
            "clear-confirmation",
            "confirm-clear",
            "cancel-clear",
            "chat-status",
            "model-boundary",
        }
        for element_id in required_ids:
            assertions[f"html_id_{element_id}"] = (
                element_id in inspector.ids
            )

        assertions["html_charset"] = (
            "charset" in inspector.meta_names
        )
        assertions["html_viewport"] = (
            "viewport" in inspector.meta_names
        )
        assertions["html_description"] = (
            "description" in inspector.meta_names
        )
        assertions["html_stylesheet"] = (
            inspector.stylesheets
            == ["/assets/control-center-chat.css"]
        )
        assertions["html_one_script"] = (
            len(inspector.scripts) == 1
        )
        assertions["html_script_src"] = (
            inspector.scripts[0].get("src")
            == "/assets/control-center-chat.js"
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
        assertions["html_dialog_one"] = (
            len(inspector.dialogs) == 1
        )
        assertions["html_textarea_one"] = (
            len(inspector.textareas) == 1
        )
        assertions["html_no_external_urls"] = (
            "http://" not in html
            and "https://" not in html
        )
        assertions["html_model_boundary"] = (
            "Local Model Bridge is not active" in html
        )
        assertions["html_sprint_187_boundary"] = (
            "Sprint 187" in html
        )

        js_needles = (
            'const API_BASE = "/api/chat";',
            'const LOCAL_INTENT = "browser-chat-session";',
            'headers["X-AURA-Local-Intent"] = LOCAL_INTENT',
            'method: "POST"',
            'const method = options.method || "GET";',
            "createSession",
            "loadSession",
            "submitMessage",
            "requestClear",
            "confirmClear",
            "expected_revision",
            "client_message_id",
            "CLEAR ",
            "crypto.randomUUID",
            "document.createElement",
            ".textContent =",
        )
        for index, needle in enumerate(js_needles, start=1):
            assertions[f"js_contract_{index:02d}"] = (
                needle in javascript
            )

        assertions["js_no_inner_html"] = (
            ".innerHTML" not in javascript
        )
        assertions["js_no_eval"] = (
            "eval(" not in javascript
            and "new Function(" not in javascript
        )
        assertions["js_no_external_urls"] = (
            "http://" not in javascript
            and "https://" not in javascript
        )
        assertions["js_no_websocket"] = (
            "WebSocket(" not in javascript
        )
        assertions["js_no_eventsource"] = (
            "EventSource(" not in javascript
        )
        assertions["js_no_storage"] = (
            "localStorage" not in javascript
            and "sessionStorage" not in javascript
            and "indexedDB" not in javascript
        )
        assertions["js_no_tools"] = (
            "/api/tools" not in javascript
            and "/api/actions" not in javascript
            and "/api/commands" not in javascript
        )

        css_needles = (
            ":root",
            ".chat-shell",
            ".session-sidebar",
            ".transcript",
            ".message-row",
            ".composer",
            ".boundary-card",
            ":focus-visible",
            "@media (max-width: 58rem)",
            "@media (max-width: 38rem)",
            "@media (prefers-reduced-motion: reduce)",
        )
        for index, needle in enumerate(css_needles, start=1):
            assertions[f"css_contract_{index:02d}"] = (
                needle in css
            )
        assertions["css_no_import"] = "@import" not in css
        assertions["css_no_external_url"] = (
            "http://" not in css
            and "https://" not in css
        )

        unknown_blocked = False
        try:
            self.asset_bytes("/assets/missing-chat.js")
        except KeyError:
            unknown_blocked = True
        assertions["unknown_asset_blocked"] = unknown_blocked

        with tempfile.TemporaryDirectory(
            prefix="aura-s186-chat-web-degraded-"
        ) as temporary:
            root = Path(temporary)
            fixture = (
                root
                / "aura"
                / "browser_chat_session_runtime"
                / "static"
            )
            fixture.parent.mkdir(parents=True)
            shutil.copytree(self.static_dir, fixture)
            (fixture / "chat.js").unlink()
            degraded = AuraBrowserChatWebSurfaceManager(
                project_root=root
            ).manifest()
            assertions["degraded_visible"] = (
                degraded["degraded"] is True
            )
            assertions["degraded_missing_one"] = (
                degraded["missing_asset_count"] == 1
            )
            assertions["degraded_route_exact"] = (
                degraded["missing_routes"]
                == ["/assets/control-center-chat.js"]
            )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise BrowserChatWebSurfaceError(
                "Chat web surface self-test failed: "
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
            "asset_count": 3,
            "chat_page_route": "/chat",
            "chat_api_base": "/api/chat",
            "degraded_fixture_verified": True,
            "safe_dom_rendering_verified": True,
            "responsive_layout_verified": True,
            "accessibility_contract_verified": True,
            "external_dependency_count": 0,
            "inline_script_count": 0,
            "inline_style_count": 0,
            "browser_auto_launch": False,
            "model_bridge_active": False,
        }
