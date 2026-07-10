"""HTTP integration for the Sprint 184 read-only Control Center backend.

The adapter preserves the Sprint 183 status API and adds nine Control Center
backend payload routes. It does not deliver the Sprint 185 browser web shell.
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

from aura.health_status_api_runtime import (
    AuraHealthStatusApiRuntimeManager,
    AuraHealthStatusHttpRuntimeManager,
)
from aura.service_lifecycle_runtime import (
    AuraServiceLifecycleRuntimeManager,
)

from .aura_control_center_backend_runtime_manager import (
    AuraControlCenterBackendRuntimeManager,
)


class AuraControlCenterBackendHttpRuntimeManager(
    AuraHealthStatusHttpRuntimeManager
):
    """Serve Sprint 183 status and Sprint 184 backend payloads."""

    name = "aura_control_center_backend_http_runtime"
    component_version = "0.1.0-alpha"
    sprint = 184

    STATUS_ROUTES = AuraHealthStatusApiRuntimeManager.ROUTES
    BACKEND_ROUTES = (
        AuraControlCenterBackendRuntimeManager.ROUTES
    )
    JSON_ROUTES = (
        *STATUS_ROUTES,
        *BACKEND_ROUTES,
    )
    ROUTES = (
        "/",
        *JSON_ROUTES,
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        super().__init__(project_root=project_root)
        self._backend_manager: (
            AuraControlCenterBackendRuntimeManager | None
        ) = None

    def attach_backend_manager(
        self,
        manager: AuraControlCenterBackendRuntimeManager,
    ) -> None:
        """Attach the backend manager sharing this listener lifecycle."""

        if self._backend_manager is not None:
            raise RuntimeError(
                "Sprint 184 backend manager is already attached."
            )
        if not isinstance(
            manager,
            AuraControlCenterBackendRuntimeManager,
        ):
            raise TypeError(
                "manager must be "
                "AuraControlCenterBackendRuntimeManager."
            )
        self._backend_manager = manager

    def _require_backend_manager(
        self,
    ) -> AuraControlCenterBackendRuntimeManager:
        manager = self._backend_manager
        if manager is None:
            raise RuntimeError(
                "Sprint 184 backend manager is not attached."
            )
        return manager

    def safety_boundary(self) -> dict[str, Any]:
        """Return inherited safety plus Sprint 184 backend limits."""

        return {
            **super().safety_boundary(),
            "control_center_backend_runtime": True,
            "read_only_backend_routes": True,
            "backend_schema_version": "1.0",
            "backend_route_count": len(
                self.BACKEND_ROUTES
            ),
            "backend_panel_count": len(
                AuraControlCenterBackendRuntimeManager.PANEL_IDS
            ),
            "total_json_route_count": len(
                self.JSON_ROUTES
            ),
            "control_center_web_shell_runtime": False,
            "frontend_asset_serving_runtime": False,
            "browser_launch_runtime": False,
            "backend_mutation_runtime": False,
            "service_control_runtime": False,
            "plugin_control_runtime": False,
            "permission_decision_runtime": False,
            "audit_writer_runtime": False,
            "memory_write_runtime": False,
        }

    def _control_center_html(
        self,
        bound_port: int,
    ) -> str:
        """Return an informational root page, not the Sprint 185 shell."""

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1"
  >
  <title>AURA Control Center Backend Runtime</title>
  <style>
    body {{
      background: #111;
      color: #eee;
      font-family: system-ui, sans-serif;
      margin: 0;
      padding: 2rem;
    }}
    main {{
      margin: 0 auto;
      max-width: 54rem;
    }}
    code {{
      background: #222;
      border-radius: .25rem;
      padding: .15rem .35rem;
    }}
    .safe {{
      font-weight: 700;
      letter-spacing: .08em;
    }}
  </style>
</head>
<body>
  <main>
    <h1>AURA</h1>
    <h2>Control Center Backend Runtime</h2>
    <p class="safe">SAFE IDLE · READ ONLY · BACKEND ONLY</p>
    <dl>
      <dt>Sprint</dt>
      <dd>184 Part B</dd>
      <dt>Binding</dt>
      <dd><code>127.0.0.1:{bound_port}</code></dd>
      <dt>Status API</dt>
      <dd>9 read-only JSON routes</dd>
      <dt>Control Center backend</dt>
      <dd>9 read-only JSON routes / 8 panel view models</dd>
      <dt>Browser web shell</dt>
      <dd>Not enabled until Sprint 185</dd>
    </dl>
    <p>
      Service controls, plugin controls, permission decisions, audit
      persistence, memory writes, chat, models, commands, tools, actions,
      background service, systemd, auto-start, public/LAN binding, and
      autonomy remain disabled.
    </p>
  </main>
</body>
</html>
"""

    def _backend_payload(
        self,
        route: str,
    ) -> dict[str, Any]:
        backend_manager = self._require_backend_manager()
        snapshot = backend_manager.snapshot()
        return backend_manager.payload_for_route(
            route,
            snapshot=snapshot,
        )

    def _handler_class(
        self,
        bound_port_getter: Any,
    ) -> Type[BaseHTTPRequestHandler]:
        manager = self

        class ControlCenterBackendHandler(
            BaseHTTPRequestHandler
        ):
            server_version = (
                "AURA-Control-Center-Backend-Alpha/0.1"
            )
            sys_version = ""

            def _security_headers(self) -> None:
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
                    "Content-Security-Policy",
                    "default-src 'none'; "
                    "style-src 'unsafe-inline'; "
                    "base-uri 'none'; "
                    "frame-ancestors 'none'; "
                    "form-action 'none'",
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
                self._security_headers()
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

                if path == "/":
                    body = manager._control_center_html(
                        bound_port
                    ).encode("utf-8")
                    self._send(
                        200,
                        body,
                        "text/html; charset=utf-8",
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
                                    "Backend Runtime"
                                ),
                                "sprint": 184,
                                "control_center_backend": True,
                                "control_center_backend_routes": 9,
                                "control_center_panels": 8,
                                "control_center_web_shell": False,
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
                                        "control_center_backend_http"
                                    ),
                                    "code": (
                                        "backend_payload_error"
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
                    "AURA_CONTROL_CENTER_BACKEND "
                    f"{self.client_address[0]} "
                    f"{message}",
                    file=sys.stderr,
                )

        return ControlCenterBackendHandler


@dataclass(frozen=True)
class ControlCenterBackendRuntimeBundle:
    """Connected Sprint 184 runtime objects."""

    web_runtime: AuraControlCenterBackendHttpRuntimeManager
    lifecycle_manager: AuraServiceLifecycleRuntimeManager
    status_manager: AuraHealthStatusApiRuntimeManager
    backend_manager: AuraControlCenterBackendRuntimeManager


def build_control_center_backend_runtime_bundle(
    project_root: str | Path | None = None,
) -> ControlCenterBackendRuntimeBundle:
    """Build one shared web/lifecycle/status/backend object graph."""

    web_runtime = (
        AuraControlCenterBackendHttpRuntimeManager(
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
    backend_manager = (
        AuraControlCenterBackendRuntimeManager(
            project_root=project_root,
            status_manager=status_manager,
        )
    )

    web_runtime.attach_status_manager(status_manager)
    web_runtime.attach_backend_manager(backend_manager)

    return ControlCenterBackendRuntimeBundle(
        web_runtime=web_runtime,
        lifecycle_manager=lifecycle_manager,
        status_manager=status_manager,
        backend_manager=backend_manager,
    )


def build_control_center_lifecycle_manager(
    project_root: str | Path | None = None,
) -> AuraServiceLifecycleRuntimeManager:
    """Return the connected lifecycle manager used by the main CLI."""

    return build_control_center_backend_runtime_bundle(
        project_root=project_root
    ).lifecycle_manager
