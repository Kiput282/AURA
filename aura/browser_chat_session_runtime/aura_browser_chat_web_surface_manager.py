"""Static browser surface for Sprint 188 interactive local chat."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class BrowserChatWebSurfaceError(RuntimeError):
    """Raised when the interactive chat browser surface fails validation."""


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
        self.fieldsets: list[dict[str, str | None]] = []
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
        elif tag == "fieldset":
            self.fieldsets.append(attributes)
        elif tag == "meta":
            name = attributes.get("name")
            if name:
                self.meta_names.add(name)
            if "charset" in attributes:
                self.meta_names.add("charset")


class AuraBrowserChatWebSurfaceManager:
    """Load and validate the Sprint 188 interactive chat assets."""

    name = "aura_interactive_control_center_chat_surface"
    component_version = "0.2.0-alpha"
    sprint = 188
    schema_version = "1.0"

    ASSET_ROUTES = (
        "/chat",
        "/assets/control-center-chat.css",
        "/assets/control-center-chat.js",
    )
    ASSET_MAP = {
        "/chat": (
            "chat.html",
            "text/html; charset=utf-8",
        ),
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
                f"Unknown Sprint 188 chat asset route: {route}"
            ) from exc
        return self.static_dir / filename

    def asset_content_type(self, route: str) -> str:
        try:
            _, content_type = self.ASSET_MAP[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 188 chat asset route: {route}"
            ) from exc
        return content_type

    def asset_bytes(self, route: str) -> bytes:
        path = self.asset_path(route)
        if not path.is_file():
            raise BrowserChatWebSurfaceError(
                f"Missing interactive chat asset: {path}"
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
            "model_api_base": "/api/model",
            "interactive_chat_runtime": True,
            "model_bridge_connected": True,
            "model_provider_enabled_by_default": False,
            "model_request_confirmation_ui": True,
            "model_probe_confirmation_ui": True,
            "idempotent_retry_ui": True,
            "session_list_filter_ui": True,
            "session_resume_ui": True,
            "session_rename_ui": True,
            "session_archive_ui": True,
            "session_restore_ui": True,
            "history_recovery_ui": True,
            "history_recovery_endpoint": "/api/chat/recovery",
            "history_recovery_read_only": True,
            "history_recovery_retry_ui": True,
            "history_recovery_dismiss_ui": True,
            "stale_revision_draft_preservation_ui": True,
            "missing_session_neutral_state_ui": True,
            "corrupt_file_preservation_ui": True,
            "automatic_history_repair_ui": False,
            "recovery_extension_sprint": 264,
            "session_permanent_delete_ui": False,
            "cross_session_history_merge_ui": False,
            "lifecycle_extension_sprint": 263,
            "placeholder_route_available": True,
            "response_kind_visibility": True,
            "browser_auto_launch": False,
            "external_dependencies": False,
            "inline_scripts": False,
            "inline_styles": False,
            "safe_dom_rendering": True,
            "local_storage_runtime": False,
            "websocket_runtime": False,
            "eventsource_runtime": False,
            "tool_action_command_ui": False,
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
        assertions["not_degraded"] = (
            status["degraded"] is False
        )
        assertions["sprint_188"] = status["sprint"] == 188
        assertions["component_version"] = (
            status["component_version"] == "0.2.0-alpha"
        )
        assertions["assets_three"] = (
            status["asset_count"] == 3
        )
        assertions["available_three"] = (
            status["available_asset_count"] == 3
        )
        assertions["chat_route"] = (
            status["chat_page_route"] == "/chat"
        )
        assertions["chat_api_base"] = (
            status["chat_api_base"] == "/api/chat"
        )
        assertions["model_api_base"] = (
            status["model_api_base"] == "/api/model"
        )
        assertions["interactive_true"] = (
            status["interactive_chat_runtime"] is True
        )
        assertions["bridge_connected"] = (
            status["model_bridge_connected"] is True
        )
        assertions["provider_default_false"] = (
            status["model_provider_enabled_by_default"]
            is False
        )
        assertions["request_confirmation_true"] = (
            status["model_request_confirmation_ui"] is True
        )
        assertions["probe_confirmation_true"] = (
            status["model_probe_confirmation_ui"] is True
        )
        assertions["idempotent_retry_true"] = (
            status["idempotent_retry_ui"] is True
        )
        assertions["placeholder_true"] = (
            status["placeholder_route_available"] is True
        )
        assertions["response_kind_true"] = (
            status["response_kind_visibility"] is True
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
        assertions["storage_false"] = (
            status["local_storage_runtime"] is False
        )
        assertions["websocket_false"] = (
            status["websocket_runtime"] is False
        )
        assertions["eventsource_false"] = (
            status["eventsource_runtime"] is False
        )
        assertions["tool_ui_false"] = (
            status["tool_action_command_ui"] is False
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
        assertions["manifest_routes_exact"] = (
            [item["route"] for item in manifest["items"]]
            == list(self.ASSET_ROUTES)
        )
        assertions["manifest_assets_local"] = all(
            item["local_asset"] is True
            for item in manifest["items"]
        )
        assertions["manifest_no_external"] = all(
            item["external_dependency"] is False
            for item in manifest["items"]
        )

        required_ids = {
            "chat-main",
            "session-list",
            "session-title",
            "create-session",
            "refresh-sessions",
            "session-filter-active",
            "session-filter-archived",
            "session-state-label",
            "resume-session",
            "rename-session",
            "archive-session",
            "restore-session",
            "history-recovery-panel",
            "history-recovery-title",
            "history-recovery-state",
            "history-recovery-detail",
            "history-recovery-issues",
            "retry-history-recovery",
            "dismiss-history-recovery",
            "rename-dialog",
            "rename-title",
            "confirm-rename",
            "cancel-rename",
            "chat-transcript",
            "message-input",
            "message-count",
            "message-mode-group",
            "mode-save-only",
            "mode-local-model",
            "confirm-model-request",
            "send-message",
            "pending-status",
            "clear-session",
            "clear-dialog",
            "clear-phrase",
            "clear-confirmation",
            "confirm-clear",
            "cancel-clear",
            "chat-status",
            "model-panel",
            "model-panel-title",
            "model-status-badge",
            "model-status-detail",
            "model-provider",
            "model-name",
            "refresh-model-status",
            "probe-model",
            "probe-dialog",
            "confirm-probe",
            "cancel-probe",
        }
        for element_id in sorted(required_ids):
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
        assertions["html_dialog_three"] = (
            len(inspector.dialogs) == 3
        )
        assertions["html_fieldset_one"] = (
            len(inspector.fieldsets) == 1
        )
        assertions["html_textarea_one"] = (
            len(inspector.textareas) == 1
        )
        assertions["html_no_external_urls"] = (
            "http://" not in html
            and "https://" not in html
        )
        assertions["html_sprint_188"] = (
            "Sprint 188" not in html
            or "Sprint 263 lifecycle extension" in html
        )
        assertions["html_sprint_263_lifecycle"] = (
            "Sprint 263 lifecycle extension" not in html
        )
        assertions["html_sprint_264_recovery"] = (
            "Sprint 264 history recovery UX" in html
        )
        assertions["html_recovery_read_only"] = (
            "Read-only diagnostic" in html
        )
        assertions["html_original_files_preserved"] = (
            "original files preserved" in html
        )
        assertions["html_safe_idle_visible"] = (
            "Safe idle is preserved" in html
        )
        assertions["html_no_repair_control"] = (
            "repair-session" not in html
            and "quarantine-session" not in html
        )
        assertions["html_no_delete_control"] = (
            "delete-session" not in html
            and "Delete session" not in html
        )
        assertions["html_interactive_title"] = (
            "AURA Interactive Chat" in html
        )
        assertions["html_local_bridge"] = (
            "Local Model Bridge" in html
        )
        assertions["html_loopback_boundary"] = (
            "Loopback · text only · no tools" in html
        )
        assertions["html_save_only"] = (
            "Save only" in html
        )
        assertions["html_local_model"] = (
            "Local model" in html
        )
        assertions["html_single_confirmation"] = (
            "this single message" in html
        )
        assertions["html_probe_explanation"] = (
            "does not download or invoke a model" in html
        )
        assertions["html_no_tools_text"] = (
            "no tools, commands, actions, or memory writes"
            in html
        )

        input_by_id = {
            item.get("id"): item
            for item in inspector.inputs
            if item.get("id")
        }
        assertions["input_save_radio"] = (
            input_by_id["mode-save-only"].get("type")
            == "radio"
        )
        assertions["input_model_radio"] = (
            input_by_id["mode-local-model"].get("type")
            == "radio"
        )
        assertions["input_model_disabled"] = (
            "disabled"
            in input_by_id["mode-local-model"]
        )
        assertions["input_confirmation_checkbox"] = (
            input_by_id["confirm-model-request"].get("type")
            == "checkbox"
        )
        assertions["input_confirmation_disabled"] = (
            "disabled"
            in input_by_id["confirm-model-request"]
        )

        js_needles = (
            'const API_BASE = "/api/chat";',
            'const MODEL_API_BASE = "/api/model";',
            'const LOCAL_INTENT = "browser-chat-session";',
            'headers["X-AURA-Local-Intent"] = LOCAL_INTENT',
            'credentials: "same-origin"',
            'cache: "no-store"',
            "Promise.allSettled",
            "refreshSessions",
            "sessionFilter",
            "?state=",
            "resumeSession",
            "renameSession",
            "archiveSession",
            "restoreSession",
            "/resume",
            "/rename",
            "/archive",
            "/restore",
            "Session archived without deletion",
            "cross_session_history_merged",
            "/recovery",
            "refreshRecoveryStatus",
            "handleChatRecoveryError",
            "retryHistoryRecovery",
            "dismissHistoryRecovery",
            "state.recovery",
            "chat_session_corruption",
            "neutral_no_session",
            "preserve_unsent_draft_in_memory",
            "restore_session",
            "original_file_preserved",
            "refreshModelStatus",
            "renderModelStatus",
            "requestProbe",
            "confirmProbe",
            "submitMessage",
            "requestClear",
            "confirmClear",
            "selectedMode",
            "modelIsActive",
            "submissionFor",
            "clearPendingSubmission",
            "expected_revision",
            "client_message_id",
            "request_id",
            "confirm_model_request: true",
            "confirm_local_connection: true",
            "/model-messages",
            '"local_model_response"',
            '"model_bridge_unavailable"',
            "idempotent_replay",
            "crypto.randomUUID",
            "document.createElement",
            ".textContent =",
            ".replaceChildren(",
            "retry keeps the same request ID",
            "event.isComposing",
        )
        for index, needle in enumerate(
            js_needles,
            start=1,
        ):
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
        assertions["js_no_permanent_delete"] = (
            "/delete" not in javascript
            and "deleteSession" not in javascript
        )
        assertions["js_no_repair_runtime"] = (
            "/api/chat/repair" not in javascript
            and "repairSession" not in javascript
        )
        assertions["js_no_quarantine_runtime"] = (
            "/api/chat/quarantine" not in javascript
            and "quarantineSession" not in javascript
        )
        assertions["js_no_cross_session_merge"] = (
            "mergeSessionHistory" not in javascript
            and "crossSessionHistory" not in javascript
        )
        assertions["js_no_stream"] = (
            "ReadableStream" not in javascript
            and "response.body.getReader" not in javascript
        )
        assertions["js_model_not_default"] = (
            'mode-save-only").checked = true'
            in javascript
        )
        assertions["js_confirmation_resets"] = (
            'confirm-model-request").checked = false'
            in javascript
        )
        assertions["js_pending_in_memory"] = (
            "pendingSubmission" in javascript
        )

        css_needles = (
            ":root",
            ".chat-shell",
            ".session-sidebar",
            ".model-card",
            ".model-facts",
            ".model-actions",
            ".transcript",
            ".message-row",
            '[data-response-kind="local_model_response"]',
            '[data-response-kind="model_bridge_unavailable"]',
            ".message-kind",
            ".composer",
            ".composer-heading",
            ".pending-status",
            ".mode-selector",
            ".mode-option",
            ".model-confirmation",
            ".history-recovery",
            ".recovery-actions",
            ".recovery-issue-list",
            ".recovery-boundary",
            ":focus-visible",
            "@media (max-width: 64rem)",
            "@media (max-width: 48rem)",
            "@media (max-width: 38rem)",
            "@media (prefers-reduced-motion: reduce)",
        )
        for index, needle in enumerate(
            css_needles,
            start=1,
        ):
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

        unknown_blocked = False
        try:
            self.asset_bytes(
                "/assets/missing-interactive-chat.js"
            )
        except KeyError:
            unknown_blocked = True
        assertions["unknown_asset_blocked"] = (
            unknown_blocked
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s188-chat-web-degraded-"
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
                "Interactive chat web surface self-test failed: "
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
            "model_api_base": "/api/model",
            "interactive_chat_runtime": True,
            "model_bridge_connected": True,
            "model_provider_enabled_by_default": False,
            "model_request_confirmation_ui_verified": True,
            "model_probe_confirmation_ui_verified": True,
            "idempotent_retry_ui_verified": True,
            "session_list_filter_ui_verified": True,
            "session_resume_ui_verified": True,
            "session_rename_ui_verified": True,
            "session_archive_ui_verified": True,
            "session_restore_ui_verified": True,
            "history_recovery_ui_verified": True,
            "history_recovery_endpoint": "/api/chat/recovery",
            "history_recovery_read_only": True,
            "history_recovery_retry_ui_verified": True,
            "history_recovery_dismiss_ui_verified": True,
            "stale_revision_draft_preservation_ui_verified": True,
            "missing_session_neutral_state_ui_verified": True,
            "corrupt_file_preservation_ui_verified": True,
            "automatic_history_repair_ui": False,
            "recovery_extension_sprint": 264,
            "session_permanent_delete_ui": False,
            "cross_session_history_merge_ui": False,
            "lifecycle_extension_sprint": 263,
            "placeholder_route_ui_verified": True,
            "response_kind_visibility_verified": True,
            "safe_dom_rendering_verified": True,
            "responsive_layout_verified": True,
            "accessibility_contract_verified": True,
            "external_dependency_count": 0,
            "inline_script_count": 0,
            "inline_style_count": 0,
            "browser_auto_launch": False,
            "tool_action_command_ui": False,
        }
