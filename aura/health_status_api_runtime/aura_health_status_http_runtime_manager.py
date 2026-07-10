"""HTTP integration for the Sprint 183 read-only status API."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Type
from urllib.parse import urlsplit

from aura.local_web_runtime_alpha import AuraLocalWebRuntimeAlphaManager
from aura.service_lifecycle_runtime import AuraServiceLifecycleRuntimeManager

from .aura_health_status_api_runtime_manager import (
    AuraHealthStatusApiRuntimeManager,
)


class AuraHealthStatusHttpRuntimeManager(AuraLocalWebRuntimeAlphaManager):
    """Serve Sprint 183 status payloads on the safe local listener."""

    name = "aura_health_status_http_runtime"
    component_version = "0.1.0-alpha"
    sprint = 183
    ROUTES = ("/", *AuraHealthStatusApiRuntimeManager.ROUTES)

    def __init__(self, project_root: str | Path | None = None) -> None:
        super().__init__(project_root=project_root)
        self._status_manager: AuraHealthStatusApiRuntimeManager | None = None

    def attach_status_manager(
        self,
        manager: AuraHealthStatusApiRuntimeManager,
    ) -> None:
        if self._status_manager is not None:
            raise RuntimeError("Sprint 183 status manager is already attached.")
        if not isinstance(manager, AuraHealthStatusApiRuntimeManager):
            raise TypeError(
                "manager must be AuraHealthStatusApiRuntimeManager."
            )
        self._status_manager = manager

    def _require_status_manager(self) -> AuraHealthStatusApiRuntimeManager:
        if self._status_manager is None:
            raise RuntimeError("Sprint 183 status manager is not attached.")
        return self._status_manager

    def safety_boundary(self) -> dict[str, Any]:
        return {
            **super().safety_boundary(),
            "health_status_api_runtime": True,
            "read_only_status_routes": True,
            "status_schema_version": "1.0",
            "status_route_count": len(
                AuraHealthStatusApiRuntimeManager.ROUTES
            ),
            "mutation_routes_enabled": False,
            "degraded_status_visible": True,
            "plugin_start_from_status_probe": False,
            "memory_mutation_from_status_probe": False,
            "listener_start_from_status_probe": False,
        }

    def _health_payload(self, bound_port: int) -> dict[str, Any]:
        status_manager = self._require_status_manager()
        snapshot = status_manager.snapshot()
        payload = status_manager.health_payload(snapshot)
        payload.update(
            {
                "service": "AURA Health and Status API Runtime",
                "component_version": self.component_version,
                "sprint": self.sprint,
                "bind_host": self.DEFAULT_HOST,
                "bound_port": int(bound_port),
                "listener_active": True,
                "runtime_execution_features": 1,
            }
        )
        return payload

    def _status_payload(self, bound_port: int) -> dict[str, Any]:
        del bound_port
        return self._require_status_manager().snapshot()

    def _control_center_html(self, bound_port: int) -> str:
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AURA Health and Status API Runtime</title>
  <style>
    body {{ background:#111; color:#eee; font-family:system-ui,sans-serif;
      margin:0; padding:2rem; }}
    main {{ margin:0 auto; max-width:52rem; }}
    code {{ background:#222; border-radius:.25rem; padding:.15rem .35rem; }}
    .safe {{ font-weight:700; letter-spacing:.08em; }}
  </style>
</head>
<body>
  <main>
    <h1>AURA</h1>
    <h2>Health and Status API Runtime</h2>
    <p class="safe">SAFE IDLE · READ ONLY</p>
    <p>Sprint 183 Part B</p>
    <p>Binding: <code>127.0.0.1:{bound_port}</code></p>
    <p>Lifecycle: foreground, manual, explicit confirmation.</p>
    <p>Status payloads: 9 read-only routes.</p>
    <p>Chat, models, memory writes, permission mutation, commands, tools,
    actions, background service, systemd, auto-start, public/LAN binding,
    and autonomy remain disabled.</p>
  </main>
</body>
</html>
"""

    def _handler_class(
        self,
        bound_port_getter: Any,
    ) -> Type[BaseHTTPRequestHandler]:
        manager = self

        class HealthStatusHandler(BaseHTTPRequestHandler):
            server_version = "AURA-Health-Status-Alpha/0.1"
            sys_version = ""

            def _security_headers(self) -> None:
                self.send_header("Cache-Control", "no-store")
                self.send_header("Pragma", "no-cache")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Referrer-Policy", "no-referrer")
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'none'; style-src 'unsafe-inline'; "
                    "base-uri 'none'; frame-ancestors 'none'; "
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
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
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

            def _dispatch_read(self, *, send_body: bool) -> None:
                if not manager._host_header_allowed(
                    self.headers.get("Host", "")
                ):
                    self._send_json(
                        403,
                        {
                            "status": "blocked",
                            "reason": "host_header_not_allowlisted",
                        },
                        send_body=send_body,
                    )
                    return

                path = urlsplit(self.path).path
                bound_port = int(bound_port_getter())

                if path == "/":
                    self._send(
                        200,
                        manager._control_center_html(bound_port).encode(
                            "utf-8"
                        ),
                        "text/html; charset=utf-8",
                        send_body=send_body,
                    )
                    return

                if path not in AuraHealthStatusApiRuntimeManager.ROUTES:
                    self._send_json(
                        404,
                        {"status": "not_found", "path": path},
                        send_body=send_body,
                    )
                    return

                try:
                    if path == "/health":
                        payload = manager._health_payload(bound_port)
                    elif path == "/api/status":
                        payload = manager._status_payload(bound_port)
                    else:
                        status_manager = manager._require_status_manager()
                        snapshot = status_manager.snapshot()
                        payload = status_manager.payload_for_route(
                            path,
                            snapshot=snapshot,
                        )
                    self._send_json(200, payload, send_body=send_body)
                except Exception as exc:
                    self._send_json(
                        503,
                        {
                            "status": "degraded",
                            "degraded": True,
                            "error_count": 1,
                            "errors": [
                                {
                                    "component": "health_status_http",
                                    "code": "status_payload_error",
                                    "detail": f"{type(exc).__name__}: {exc}",
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
                    {"status": "blocked", "reason": "read_only_runtime"},
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

            def log_message(self, format_string: str, *args: Any) -> None:
                timestamp = datetime.now(timezone.utc).isoformat()
                print(
                    f"{timestamp} AURA_STATUS_API "
                    f"{self.client_address[0]} {format_string % args}",
                    file=sys.stderr,
                )

        return HealthStatusHandler


@dataclass(frozen=True)
class HealthStatusRuntimeBundle:
    web_runtime: AuraHealthStatusHttpRuntimeManager
    lifecycle_manager: AuraServiceLifecycleRuntimeManager
    status_manager: AuraHealthStatusApiRuntimeManager


def build_health_status_runtime_bundle(
    project_root: str | Path | None = None,
) -> HealthStatusRuntimeBundle:
    web_runtime = AuraHealthStatusHttpRuntimeManager(
        project_root=project_root
    )
    lifecycle_manager = AuraServiceLifecycleRuntimeManager(
        web_runtime=web_runtime
    )
    status_manager = AuraHealthStatusApiRuntimeManager(
        project_root=project_root,
        lifecycle_manager=lifecycle_manager,
    )
    web_runtime.attach_status_manager(status_manager)
    return HealthStatusRuntimeBundle(
        web_runtime=web_runtime,
        lifecycle_manager=lifecycle_manager,
        status_manager=status_manager,
    )


def build_health_status_lifecycle_manager(
    project_root: str | Path | None = None,
) -> AuraServiceLifecycleRuntimeManager:
    return build_health_status_runtime_bundle(
        project_root=project_root
    ).lifecycle_manager
