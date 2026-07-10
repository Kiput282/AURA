"""AURA Sprint 181 Local Web Runtime Alpha.

This is AURA's first deliberately narrow runtime listener. It provides a
foreground-only, manually confirmed, localhost-only HTTP service with three
read-only routes:

- GET /
- GET /health
- GET /api/status

The runtime does not activate chat, model calls, memory writes, permission
mutation, audit writes, commands, tools, desktop control, arbitrary file
access, background service installation, or public/LAN binding.
"""

from __future__ import annotations

import json
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Type
from urllib.parse import urlsplit

import yaml


@dataclass(frozen=True)
class LocalWebRuntimeConfig:
    """Validated runtime configuration."""

    host: str = "127.0.0.1"
    port: int = 8765
    mode: str = "safe_idle"
    require_explicit_confirmation: bool = True


class LocalOnlyThreadingHTTPServer(ThreadingHTTPServer):
    """IPv4 localhost server with short-lived daemon request threads."""

    daemon_threads = True
    allow_reuse_address = True


class AuraLocalWebRuntimeAlphaManager:
    """Manage the Sprint 181 localhost-only foreground runtime."""

    name = "aura_local_web_runtime_alpha"
    component_version = "0.1.0-alpha"
    sprint = 181

    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8765
    ALLOWED_MODE = "safe_idle"
    ROUTES = ("/", "/health", "/api/status")

    def __init__(self, project_root: str | Path | None = None) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        self.project_root = Path(project_root).resolve()
        self.settings_path = (
            self.project_root / "aura" / "config" / "settings.yaml"
        )

    def load_config(self) -> LocalWebRuntimeConfig:
        """Load and fail-closed validate the local web runtime section."""

        if not self.settings_path.is_file():
            raise RuntimeError(
                f"Missing settings file: {self.settings_path}"
            )

        loaded = yaml.safe_load(
            self.settings_path.read_text(encoding="utf-8")
        ) or {}

        if not isinstance(loaded, dict):
            raise RuntimeError("settings.yaml must contain a mapping.")

        raw = loaded.get("local_web_runtime")
        if not isinstance(raw, dict):
            raise RuntimeError(
                "Missing local_web_runtime configuration section."
            )

        host = str(raw.get("host", "")).strip()
        mode = str(raw.get("mode", "")).strip()

        try:
            port = int(raw.get("port"))
        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                "local_web_runtime.port must be an integer."
            ) from exc

        require_confirmation = raw.get(
            "require_explicit_confirmation",
            True,
        )
        if not isinstance(require_confirmation, bool):
            raise RuntimeError(
                "local_web_runtime.require_explicit_confirmation "
                "must be true or false."
            )

        self._validate_host(host)
        self._validate_port(port)
        self._validate_mode(mode)

        if not require_confirmation:
            raise RuntimeError(
                "Sprint 181 requires explicit start confirmation."
            )

        return LocalWebRuntimeConfig(
            host=host,
            port=port,
            mode=mode,
            require_explicit_confirmation=require_confirmation,
        )

    @classmethod
    def _validate_host(cls, host: str) -> None:
        if host != cls.DEFAULT_HOST:
            raise RuntimeError(
                "Sprint 181 permits only host 127.0.0.1. "
                "Wildcard, IPv6 wildcard, LAN, and public binds are blocked."
            )

    @staticmethod
    def _validate_port(port: int) -> None:
        if not 1024 <= port <= 65535:
            raise RuntimeError(
                "local_web_runtime.port must be between 1024 and 65535."
            )

    @classmethod
    def _validate_mode(cls, mode: str) -> None:
        if mode != cls.ALLOWED_MODE:
            raise RuntimeError(
                "Sprint 181 permits only mode safe_idle."
            )

    @staticmethod
    def _host_header_allowed(value: str) -> bool:
        host = (value or "").strip().lower()
        if not host:
            return False

        return (
            host == "127.0.0.1"
            or host.startswith("127.0.0.1:")
            or host == "localhost"
            or host.startswith("localhost:")
        )

    def safety_boundary(self) -> dict[str, Any]:
        """Return the explicit Sprint 181 runtime boundary."""

        return {
            "localhost_only": True,
            "foreground_only": True,
            "manual_start_only": True,
            "explicit_confirmation_required": True,
            "safe_idle_default": True,
            "read_only_http_runtime": True,
            "public_interface_binding": False,
            "lan_interface_binding": False,
            "wildcard_binding": False,
            "ipv6_wildcard_binding": False,
            "cors_runtime": False,
            "websocket_runtime": False,
            "background_daemon": False,
            "systemd_runtime": False,
            "browser_auto_launch": False,
            "chat_runtime": False,
            "model_runtime": False,
            "memory_write_runtime": False,
            "permission_mutation_runtime": False,
            "audit_write_runtime": False,
            "command_execution": False,
            "tool_execution": False,
            "action_dispatch": False,
            "arbitrary_file_read": False,
            "arbitrary_file_write": False,
            "desktop_control": False,
            "voice_runtime": False,
            "vision_runtime": False,
            "autonomous_action": False,
        }

    def status(
        self,
        *,
        listener_active: bool = False,
        bound_port: int | None = None,
    ) -> dict[str, Any]:
        """Return read-only component status without starting a listener."""

        config = self.load_config()
        return {
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ready" if listener_active else "stopped",
            "runtime_level": "permission_gated_alpha",
            "service_mode": config.mode,
            "configured_host": config.host,
            "configured_port": config.port,
            "bound_port": bound_port if listener_active else None,
            "listener_active": listener_active,
            "runtime_routes": list(self.ROUTES),
            "runtime_route_count": len(self.ROUTES),
            "runtime_execution_features": 1 if listener_active else 0,
            **self.safety_boundary(),
        }

    def _health_payload(self, bound_port: int) -> dict[str, Any]:
        config = self.load_config()
        return {
            "status": "ok",
            "service": "AURA Local Web Runtime Alpha",
            "component_version": self.component_version,
            "sprint": self.sprint,
            "service_state": "ready",
            "mode": config.mode,
            "bind_host": config.host,
            "bound_port": bound_port,
            "safe_idle": True,
            "listener_active": True,
            "runtime_execution_features": 1,
            "chat_runtime": False,
            "model_runtime": False,
            "command_execution": False,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }

    def _status_payload(self, bound_port: int) -> dict[str, Any]:
        return self.status(
            listener_active=True,
            bound_port=bound_port,
        )

    def _control_center_html(self, bound_port: int) -> str:
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AURA Control Center — Runtime Alpha</title>
<style>
:root {{
  color-scheme: dark;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  background: #090d18;
  color: #edf2ff;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at 20% 0%, #24345f 0, transparent 42%),
    radial-gradient(circle at 100% 30%, #362453 0, transparent 35%),
    #090d18;
}}
main {{
  width: min(920px, calc(100% - 32px));
  border: 1px solid #334168;
  border-radius: 24px;
  padding: 30px;
  background: rgba(14, 20, 38, .94);
  box-shadow: 0 28px 90px rgba(0, 0, 0, .48);
}}
header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}}
h1 {{
  margin: 0;
  font-size: clamp(2.4rem, 8vw, 5rem);
  letter-spacing: .12em;
}}
.subtitle {{ color: #aebbe0; }}
.badge {{
  border: 1px solid #56d69b;
  border-radius: 999px;
  padding: 9px 14px;
  color: #8cf0bd;
  white-space: nowrap;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
  margin-top: 28px;
}}
.card {{
  border: 1px solid #293655;
  border-radius: 17px;
  padding: 18px;
  background: #11182b;
}}
.card h2 {{
  margin: 0 0 10px;
  color: #9fb0dc;
  font-size: .78rem;
  letter-spacing: .13em;
  text-transform: uppercase;
}}
.value {{ font-size: 1.16rem; font-weight: 750; }}
.notice {{
  margin-top: 24px;
  color: #9ca9cc;
  line-height: 1.65;
}}
code {{ color: #c0d9ff; }}
</style>
</head>
<body>
<main>
<header>
  <div>
    <h1>AURA</h1>
    <div class="subtitle">Control Center Runtime Alpha</div>
  </div>
  <div class="badge">SAFE IDLE</div>
</header>
<section class="grid">
  <article class="card">
    <h2>Sprint</h2>
    <div class="value">181 Part A</div>
  </article>
  <article class="card">
    <h2>Binding</h2>
    <div class="value">127.0.0.1:{bound_port}</div>
  </article>
  <article class="card">
    <h2>Service</h2>
    <div class="value">Foreground / Manual</div>
  </article>
  <article class="card">
    <h2>Chat</h2>
    <div class="value">Not activated yet</div>
  </article>
</section>
<p class="notice">
This alpha exposes only <code>/</code>, <code>/health</code>, and
<code>/api/status</code>. Mutating HTTP methods, model calls, memory writes,
permission changes, commands, tools, desktop actions, public/LAN binding,
background service installation, and autonomous behavior remain blocked.
</p>
</main>
</body>
</html>"""

    def _handler_class(
        self,
        bound_port_getter: Any,
    ) -> Type[BaseHTTPRequestHandler]:
        manager = self

        class LocalWebHandler(BaseHTTPRequestHandler):
            server_version = "AURA-Local-Web-Alpha/0.1"
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

                if path == "/health":
                    self._send_json(
                        200,
                        manager._health_payload(bound_port),
                        send_body=send_body,
                    )
                    return

                if path == "/api/status":
                    self._send_json(
                        200,
                        manager._status_payload(bound_port),
                        send_body=send_body,
                    )
                    return

                self._send_json(
                    404,
                    {
                        "status": "not_found",
                        "path": path,
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
                timestamp = datetime.now(timezone.utc).isoformat()
                message = format_string % args
                print(
                    f"{timestamp} "
                    f"AURA_LOCAL_WEB "
                    f"{self.client_address[0]} "
                    f"{message}",
                    file=sys.stderr,
                )

        return LocalWebHandler

    def create_server(
        self,
        *,
        port_override: int | None = None,
    ) -> LocalOnlyThreadingHTTPServer:
        """Create and bind the server after all fail-closed checks pass."""

        config = self.load_config()
        port = config.port if port_override is None else int(port_override)

        if port != 0:
            self._validate_port(port)

        server_holder: dict[str, LocalOnlyThreadingHTTPServer] = {}

        def bound_port_getter() -> int:
            server = server_holder["server"]
            return int(server.server_address[1])

        handler_class = self._handler_class(bound_port_getter)

        try:
            server = LocalOnlyThreadingHTTPServer(
                (config.host, port),
                handler_class,
            )
        except OSError as exc:
            raise RuntimeError(
                f"Unable to bind {config.host}:{port}: {exc}"
            ) from exc

        server_holder["server"] = server

        bound_host, bound_port = server.server_address[:2]
        if bound_host != self.DEFAULT_HOST:
            server.server_close()
            raise RuntimeError(
                f"Unsafe bind detected: {bound_host}:{bound_port}"
            )

        return server

    def serve_forever(self, *, confirmed: bool) -> None:
        """Run in the foreground until Ctrl+C."""

        config = self.load_config()

        if config.require_explicit_confirmation and not confirmed:
            raise RuntimeError(
                "Explicit confirmation is required. "
                "Use --confirm-localhost to start."
            )

        server = self.create_server()
        bound_host, bound_port = server.server_address[:2]

        print("AURA Local Web Runtime Alpha")
        print("============================")
        print(f"Mode       : {config.mode}")
        print(f"Bind       : http://{bound_host}:{bound_port}")
        print("Scope      : localhost-only, foreground-only, read-only")
        print("Routes     : /, /health, /api/status")
        print("Chat       : DISABLED")
        print("Model      : DISABLED")
        print("Commands   : DISABLED")
        print("Stop       : Ctrl+C")

        try:
            server.serve_forever(poll_interval=0.25)
        except KeyboardInterrupt:
            print()
            print("Shutdown requested.")
        finally:
            server.server_close()
            print("AURA Local Web Runtime Alpha stopped.")

    @staticmethod
    def _request(
        url: str,
        *,
        method: str = "GET",
    ) -> tuple[int, bytes, dict[str, str]]:
        request = urllib.request.Request(url=url, method=method)
        try:
            with urllib.request.urlopen(
                request,
                timeout=3.0,
            ) as response:
                return (
                    int(response.status),
                    response.read(),
                    dict(response.headers.items()),
                )
        except urllib.error.HTTPError as exc:
            return (
                int(exc.code),
                exc.read(),
                dict(exc.headers.items()),
            )

    def self_test(self, *, configured_port: bool = True) -> dict[str, Any]:
        """Bind, exercise, and cleanly close the real HTTP runtime."""

        server = self.create_server(
            port_override=None if configured_port else 0
        )
        host, port = server.server_address[:2]

        thread = threading.Thread(
            target=server.serve_forever,
            kwargs={"poll_interval": 0.05},
            name="aura-local-web-runtime-self-test",
            daemon=True,
        )
        thread.start()

        base_url = f"http://{host}:{port}"
        try:
            deadline = time.monotonic() + 3.0
            while True:
                try:
                    status, _, _ = self._request(
                        f"{base_url}/health"
                    )
                    if status == 200:
                        break
                except OSError:
                    pass

                if time.monotonic() >= deadline:
                    raise RuntimeError(
                        "Runtime self-test listener did not become ready."
                    )
                time.sleep(0.05)

            root_status, root_body, root_headers = self._request(
                f"{base_url}/"
            )
            health_status, health_body, health_headers = self._request(
                f"{base_url}/health"
            )
            api_status, api_body, api_headers = self._request(
                f"{base_url}/api/status"
            )
            missing_status, _, _ = self._request(
                f"{base_url}/missing"
            )
            post_status, post_body, post_headers = self._request(
                f"{base_url}/api/status",
                method="POST",
            )

            health_payload = json.loads(
                health_body.decode("utf-8")
            )
            api_payload = json.loads(
                api_body.decode("utf-8")
            )
            post_payload = json.loads(
                post_body.decode("utf-8")
            )

            assertions = {
                "bound_to_ipv4_localhost": host == self.DEFAULT_HOST,
                "root_ok": root_status == 200,
                "root_is_html": "text/html" in root_headers.get(
                    "Content-Type",
                    "",
                ),
                "root_contains_aura": b"AURA" in root_body,
                "health_ok": health_status == 200,
                "health_json": "application/json" in health_headers.get(
                    "Content-Type",
                    "",
                ),
                "health_safe_idle": (
                    health_payload.get("safe_idle") is True
                ),
                "health_command_execution_blocked": (
                    health_payload.get("command_execution") is False
                ),
                "status_ok": api_status == 200,
                "status_listener_active": (
                    api_payload.get("listener_active") is True
                ),
                "status_runtime_feature_count_one": (
                    api_payload.get("runtime_execution_features") == 1
                ),
                "status_public_binding_blocked": (
                    api_payload.get("public_interface_binding") is False
                ),
                "missing_route_404": missing_status == 404,
                "post_blocked_405": post_status == 405,
                "post_read_only_reason": (
                    post_payload.get("reason") == "read_only_runtime"
                ),
                "allow_header_read_only": (
                    post_headers.get("Allow") == "GET, HEAD"
                ),
                "security_header_nosniff": (
                    api_headers.get("X-Content-Type-Options")
                    == "nosniff"
                ),
                "chat_runtime_disabled": (
                    api_payload.get("chat_runtime") is False
                ),
                "model_runtime_disabled": (
                    api_payload.get("model_runtime") is False
                ),
                "memory_write_runtime_disabled": (
                    api_payload.get("memory_write_runtime") is False
                ),
                "permission_mutation_disabled": (
                    api_payload.get("permission_mutation_runtime")
                    is False
                ),
            }

            failed = [
                key
                for key, passed in assertions.items()
                if not passed
            ]
            if failed:
                raise RuntimeError(
                    "Runtime self-test failed: "
                    + ", ".join(failed)
                )

            return {
                "status": "ok",
                "host": host,
                "port": int(port),
                "configured_port_tested": configured_port,
                "assertion_count": len(assertions),
                "failed_assertion_count": 0,
                "routes_tested": list(self.ROUTES),
                "mutation_method_blocked": "POST",
            }
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3.0)
            if thread.is_alive():
                raise RuntimeError(
                    "Runtime self-test server did not shut down cleanly."
                )
