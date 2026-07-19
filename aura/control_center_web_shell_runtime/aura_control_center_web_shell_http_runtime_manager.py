"""HTTP delivery for the Sprint 185 local Control Center Web Shell.

The adapter serves three local static assets and preserves all Sprint 183
status and Sprint 184 backend routes on the same foreground localhost
listener. It exposes no mutation endpoints and never launches a browser.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Type
from urllib.parse import urlsplit

from aura.control_center_backend_runtime import (
    AuraControlCenterBackendRuntimeManager,
    AuraControlCenterBackendHttpRuntimeManager,
)
from aura.health_status_api_runtime import (
    AuraHealthStatusApiRuntimeManager,
)
from aura.service_lifecycle_runtime import (
    AuraServiceLifecycleRuntimeManager,
)

from .aura_control_center_web_shell_runtime_manager import (
    AuraControlCenterWebShellRuntimeManager,
)


class AuraControlCenterWebShellHttpRuntimeManager(
    AuraControlCenterBackendHttpRuntimeManager
):
    """Serve the web shell and inherited read-only JSON routes."""

    name = "aura_control_center_web_shell_http_runtime"
    component_version = "0.1.0-alpha"
    sprint = 185

    SHELL_ROUTES = (
        AuraControlCenterWebShellRuntimeManager.ASSET_ROUTES
    )
    JSON_ROUTES = (
        AuraControlCenterBackendHttpRuntimeManager.JSON_ROUTES
    )
    ROUTES = (
        *SHELL_ROUTES,
        *JSON_ROUTES,
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        super().__init__(project_root=project_root)
        self._shell_manager: (
            AuraControlCenterWebShellRuntimeManager | None
        ) = None

    def attach_shell_manager(
        self,
        manager: AuraControlCenterWebShellRuntimeManager,
    ) -> None:
        """Attach the local static shell manager."""

        if self._shell_manager is not None:
            raise RuntimeError(
                "Sprint 185 shell manager is already attached."
            )
        if not isinstance(
            manager,
            AuraControlCenterWebShellRuntimeManager,
        ):
            raise TypeError(
                "manager must be "
                "AuraControlCenterWebShellRuntimeManager."
            )
        self._shell_manager = manager

    def _require_shell_manager(
        self,
    ) -> AuraControlCenterWebShellRuntimeManager:
        manager = self._shell_manager
        if manager is None:
            raise RuntimeError(
                "Sprint 185 shell manager is not attached."
            )
        return manager

    def safety_boundary(self) -> dict[str, Any]:
        """Return inherited safety and Sprint 185 shell limits."""

        return {
            **super().safety_boundary(),
            "control_center_web_shell_runtime": True,
            "local_static_asset_delivery": True,
            "shell_asset_route_count": len(
                self.SHELL_ROUTES
            ),
            "shell_panel_count": len(
                AuraControlCenterWebShellRuntimeManager.PANEL_IDS
            ),
            "total_route_count": len(self.ROUTES),
            "external_dependency_runtime": False,
            "cdn_runtime": False,
            "external_font_runtime": False,
            "browser_auto_launch_runtime": False,
            "websocket_runtime": False,
            "server_sent_event_runtime": False,
            "frontend_mutation_runtime": False,
            "service_control_runtime": False,
            "plugin_control_runtime": False,
            "permission_decision_runtime": False,
            "audit_writer_runtime": False,
            "memory_write_runtime": False,
        }

    def _handler_class(
        self,
        bound_port_getter: Any,
    ) -> Type[BaseHTTPRequestHandler]:
        manager = self

        class ControlCenterWebShellHandler(
            BaseHTTPRequestHandler
        ):
            server_version = (
                "AURA-Control-Center-Web-Shell-Alpha/0.1"
            )
            sys_version = ""

            def _security_headers(
                self,
                *,
                content_type: str,
            ) -> None:
                self.send_header("Cache-Control", "no-store")
                self.send_header("Pragma", "no-cache")
                self.send_header(
                    "X-Content-Type-Options",
                    "nosniff",
                )
                self.send_header(
                    "X-Frame-Options",
                    "DENY",
                )
                self.send_header(
                    "Referrer-Policy",
                    "no-referrer",
                )
                self.send_header(
                    "Permissions-Policy",
                    "camera=(), microphone=(self), "
                    "geolocation=(), payment=(), usb=()",
                )

                if content_type.startswith("text/html"):
                    policy = (
                        "default-src 'none'; "
                        "style-src 'self'; "
                        "script-src 'self'; "
                        "connect-src 'self'; "
                        "img-src 'self' data:; "
                        "font-src 'none'; "
                        "media-src 'self' blob:; "
                        "object-src 'none'; "
                        "worker-src 'none'; "
                        "manifest-src 'none'; "
                        "base-uri 'none'; "
                        "frame-ancestors 'none'; "
                        "form-action 'none'"
                    )
                else:
                    policy = (
                        "default-src 'none'; "
                        "base-uri 'none'; "
                        "frame-ancestors 'none'; "
                        "form-action 'none'"
                    )

                self.send_header(
                    "Content-Security-Policy",
                    policy,
                )

            def _send(
                self,
                status: int,
                body: bytes,
                content_type: str,
                *,
                send_body: bool,
                allow: str | None = None,
            ) -> None:
                self.send_response(status)
                self.send_header(
                    "Content-Type",
                    content_type,
                )
                self.send_header(
                    "Content-Length",
                    str(len(body)),
                )
                if allow is not None:
                    self.send_header("Allow", allow)
                self._security_headers(
                    content_type=content_type
                )
                self.end_headers()
                if send_body:
                    self.wfile.write(body)

            def _send_json(
                self,
                status: int,
                payload: dict[str, Any],
                *,
                send_body: bool,
                allow: str | None = None,
            ) -> None:
                body = json.dumps(
                    payload,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                self._send(
                    status,
                    body,
                    "application/json; charset=utf-8",
                    send_body=send_body,
                    allow=allow,
                )

            def _dispatch_read(
                self,
                *,
                send_body: bool,
            ) -> None:
                if not manager._host_header_allowed(
                    self.headers.get("Host", "")
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": (
                                "host_header_not_allowlisted"
                            ),
                        },
                        send_body=send_body,
                    )
                    return

                path = urlsplit(self.path).path
                bound_port = int(bound_port_getter())

                if path in manager.SHELL_ROUTES:
                    try:
                        shell_manager = (
                            manager._require_shell_manager()
                        )
                        body = shell_manager.asset_bytes(path)
                        content_type = (
                            shell_manager.asset_content_type(
                                path
                            )
                        )
                    except Exception as exc:
                        self._send_json(
                            503,
                            {
                                "status": "degraded",
                                "degraded": True,
                                "error_count": 1,
                                "errors": [
                                    {
                                        "component": (
                                            "control_center_web_shell"
                                        ),
                                        "code": (
                                            "shell_asset_unavailable"
                                        ),
                                        "detail": (
                                            f"{type(exc).__name__}: "
                                            f"{exc}"
                                        ),
                                    }
                                ],
                                "mutation_allowed": False,
                            },
                            send_body=send_body,
                        )
                        return

                    self._send(
                        200,
                        body,
                        content_type,
                        send_body=send_body,
                    )
                    return

                if path not in manager.JSON_ROUTES:
                    self._send_json(
                        404,
                        {
                            "status": "not_found",
                            "path": path,
                        },
                        send_body=send_body,
                    )
                    return

                try:
                    if path == "/health":
                        payload = manager._health_payload(
                            bound_port
                        )
                        payload.update(
                            {
                                "service": (
                                    "AURA Control Center "
                                    "Web Shell Runtime"
                                ),
                                "sprint": 185,
                                "control_center_backend": True,
                                "control_center_backend_routes": 9,
                                "control_center_panels": 8,
                                "control_center_web_shell": True,
                                "control_center_shell_assets": 3,
                                "browser_auto_launch": False,
                            }
                        )
                    elif path == "/api/status":
                        payload = manager._status_payload(
                            bound_port
                        )
                    elif path in manager.STATUS_ROUTES:
                        status_manager = (
                            manager._require_status_manager()
                        )
                        snapshot = status_manager.snapshot()
                        payload = (
                            status_manager.payload_for_route(
                                path,
                                snapshot=snapshot,
                            )
                        )
                    else:
                        payload = manager._backend_payload(path)

                    self._send_json(
                        200,
                        payload,
                        send_body=send_body,
                    )
                except Exception as exc:
                    self._send_json(
                        503,
                        {
                            "status": "degraded",
                            "degraded": True,
                            "error_count": 1,
                            "errors": [
                                {
                                    "component": (
                                        "control_center_web_shell_http"
                                    ),
                                    "code": (
                                        "runtime_payload_error"
                                    ),
                                    "detail": (
                                        f"{type(exc).__name__}: "
                                        f"{exc}"
                                    ),
                                }
                            ],
                            "mutation_allowed": False,
                        },
                        send_body=send_body,
                    )

            def do_GET(self) -> None:
                self._dispatch_read(send_body=True)

            def do_HEAD(self) -> None:
                self._dispatch_read(send_body=False)

            def _reject_mutation(self) -> None:
                self._send_json(
                    405,
                    {
                        "status": "blocked",
                        "reason": "read_only_runtime",
                    },
                    send_body=True,
                    allow="GET, HEAD",
                )

            do_POST = _reject_mutation
            do_PUT = _reject_mutation
            do_PATCH = _reject_mutation
            do_DELETE = _reject_mutation
            do_OPTIONS = _reject_mutation
            do_CONNECT = _reject_mutation
            do_TRACE = _reject_mutation

            def log_message(
                self,
                format_string: str,
                *args: Any,
            ) -> None:
                timestamp = datetime.now(
                    timezone.utc
                ).isoformat()
                message = format_string % args
                print(
                    f"{timestamp} "
                    "AURA_CONTROL_CENTER_WEB_SHELL "
                    f"{self.client_address[0]} "
                    f"{message}",
                    file=sys.stderr,
                )

        return ControlCenterWebShellHandler


@dataclass(frozen=True)
class ControlCenterWebShellRuntimeBundle:
    """Connected Sprint 185 runtime objects."""

    web_runtime: AuraControlCenterWebShellHttpRuntimeManager
    lifecycle_manager: AuraServiceLifecycleRuntimeManager
    status_manager: AuraHealthStatusApiRuntimeManager
    backend_manager: AuraControlCenterBackendRuntimeManager
    shell_manager: AuraControlCenterWebShellRuntimeManager


def build_control_center_web_shell_runtime_bundle(
    project_root: str | Path | None = None,
) -> ControlCenterWebShellRuntimeBundle:
    """Build one shared shell/backend/status/lifecycle object graph."""

    web_runtime = (
        AuraControlCenterWebShellHttpRuntimeManager(
            project_root=project_root
        )
    )
    lifecycle_manager = AuraServiceLifecycleRuntimeManager(
        web_runtime=web_runtime
    )
    status_manager = AuraHealthStatusApiRuntimeManager(
        project_root=project_root,
        lifecycle_manager=lifecycle_manager,
    )
    backend_manager = AuraControlCenterBackendRuntimeManager(
        project_root=project_root,
        status_manager=status_manager,
    )
    shell_manager = AuraControlCenterWebShellRuntimeManager(
        project_root=project_root
    )

    web_runtime.attach_status_manager(status_manager)
    web_runtime.attach_backend_manager(backend_manager)
    web_runtime.attach_shell_manager(shell_manager)

    return ControlCenterWebShellRuntimeBundle(
        web_runtime=web_runtime,
        lifecycle_manager=lifecycle_manager,
        status_manager=status_manager,
        backend_manager=backend_manager,
        shell_manager=shell_manager,
    )


def build_control_center_web_shell_lifecycle_manager(
    project_root: str | Path | None = None,
) -> AuraServiceLifecycleRuntimeManager:
    """Return the connected lifecycle manager used by the main CLI."""

    return build_control_center_web_shell_runtime_bundle(
        project_root=project_root
    ).lifecycle_manager
