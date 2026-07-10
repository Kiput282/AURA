"""AURA Sprint 183 read-only health and status aggregation core.

The manager gathers transparent runtime information without starting plugins,
opening a network listener, creating memory files, mutating permissions, or
executing actions.

It prepares payloads for:

- /health
- /api/status
- /api/status/identity
- /api/status/plugins
- /api/status/capabilities
- /api/status/service
- /api/status/memory
- /api/status/safety
- /api/status/errors

HTTP integration is intentionally deferred to Sprint 183 Part B.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)
from aura.service_lifecycle_runtime import (
    AuraServiceLifecycleRuntimeManager,
)


class HealthStatusAggregationError(RuntimeError):
    """Raised when the status aggregation contract cannot be validated."""


class AuraHealthStatusApiRuntimeManager:
    """Build read-only health and status payloads."""

    name = "aura_health_status_api_runtime"
    component_version = "0.1.0-alpha"
    sprint = 183
    schema_version = "1.0"

    ROUTES = (
        "/health",
        "/api/status",
        "/api/status/identity",
        "/api/status/plugins",
        "/api/status/capabilities",
        "/api/status/service",
        "/api/status/memory",
        "/api/status/safety",
        "/api/status/errors",
    )

    EXPECTED_PLUGINS = (
        {
            "name": "echo",
            "module": "aura.plugins.builtin.echo_plugin",
            "class_name": "EchoPlugin",
        },
        {
            "name": "memory",
            "module": "aura.plugins.builtin.memory_plugin",
            "class_name": "MemoryPlugin",
        },
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        lifecycle_manager: (
            AuraServiceLifecycleRuntimeManager | None
        ) = None,
        capability_manager: CapabilityRegistryManager | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()
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
        self.memory_dir = (
            self.project_root
            / "data"
            / "memory"
        )
        self.memory_file = (
            self.memory_dir
            / "memories.jsonl"
        )

        self.lifecycle_manager = (
            lifecycle_manager
            if lifecycle_manager is not None
            else AuraServiceLifecycleRuntimeManager()
        )
        self.capability_manager = (
            capability_manager
            if capability_manager is not None
            else CapabilityRegistryManager()
        )
        self._clock = (
            clock
            if clock is not None
            else lambda: datetime.now(timezone.utc)
        )

    def _now_utc(self) -> str:
        return self._clock().astimezone(timezone.utc).isoformat()

    @staticmethod
    def _error(
        component: str,
        code: str,
        detail: str,
    ) -> dict[str, str]:
        return {
            "component": str(component),
            "code": str(code),
            "detail": str(detail),
        }

    @staticmethod
    def _read_yaml_mapping(path: Path) -> dict[str, Any]:
        if not path.is_file():
            raise FileNotFoundError(
                f"Required YAML file not found: {path}"
            )

        loaded = yaml.safe_load(
            path.read_text(encoding="utf-8")
        ) or {}

        if not isinstance(loaded, dict):
            raise ValueError(
                f"YAML root must be a mapping: {path}"
            )
        return loaded

    @staticmethod
    def _safe_stat(path: Path) -> dict[str, Any]:
        try:
            stat = path.stat()
        except OSError:
            return {
                "exists": False,
                "is_file": False,
                "size_bytes": 0,
                "modified_at_utc": None,
            }

        return {
            "exists": True,
            "is_file": path.is_file(),
            "size_bytes": int(stat.st_size),
            "modified_at_utc": datetime.fromtimestamp(
                stat.st_mtime,
                timezone.utc,
            ).isoformat(),
        }

    @staticmethod
    def _file_fingerprint(path: Path) -> dict[str, Any]:
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

    def identity_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Read identity and version without booting the application."""

        errors: list[dict[str, str]] = []

        try:
            identity = self._read_yaml_mapping(
                self.identity_path
            )
            name = str(identity.get("name", "")).strip()
            version = str(
                identity.get("version", "")
            ).strip()
            codename = str(
                identity.get("codename", "")
            ).strip()
            creator = str(
                identity.get("creator", "")
            ).strip()
            motto = str(
                identity.get("motto", "")
            ).strip()

            missing = [
                key
                for key, value in (
                    ("name", name),
                    ("version", version),
                    ("codename", codename),
                    ("creator", creator),
                )
                if not value
            ]
            if missing:
                raise ValueError(
                    "Missing required identity fields: "
                    + ", ".join(missing)
                )

            payload = {
                "status": "ok",
                "available": True,
                "name": name,
                "version": version,
                "codename": codename,
                "creator": creator,
                "motto": motto,
                "source": str(
                    self.identity_path.relative_to(
                        self.project_root
                    )
                ),
                "probe_mode": "read_only_yaml",
            }
        except Exception as exc:
            errors.append(
                self._error(
                    "identity",
                    "identity_unavailable",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            payload = {
                "status": "error",
                "available": False,
                "name": "AURA",
                "version": "unknown",
                "codename": "unknown",
                "creator": "unknown",
                "motto": "",
                "source": str(self.identity_path),
                "probe_mode": "read_only_yaml",
            }

        return payload, errors

    def core_boot_status(
        self,
        identity: dict[str, Any],
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Validate boot prerequisites without running AuraApp.start()."""

        errors: list[dict[str, str]] = []

        try:
            settings = self._read_yaml_mapping(
                self.settings_path
            )
            app = settings.get("app")
            server = settings.get("server")
            local_web = settings.get(
                "local_web_runtime"
            )

            if not isinstance(app, dict):
                raise ValueError(
                    "settings.app must be a mapping."
                )
            if not isinstance(server, dict):
                raise ValueError(
                    "settings.server must be a mapping."
                )
            if not isinstance(local_web, dict):
                raise ValueError(
                    "settings.local_web_runtime must be a mapping."
                )

            host = str(
                local_web.get("host", "")
            ).strip()
            mode = str(
                local_web.get("mode", "")
            ).strip()
            confirmation = local_web.get(
                "require_explicit_confirmation"
            )

            if host != "127.0.0.1":
                raise ValueError(
                    "Local web host is not 127.0.0.1."
                )
            if mode != "safe_idle":
                raise ValueError(
                    "Local web mode is not safe_idle."
                )
            if confirmation is not True:
                raise ValueError(
                    "Explicit start confirmation is not enabled."
                )
            if identity.get("available") is not True:
                raise ValueError(
                    "Identity is unavailable."
                )

            payload = {
                "status": "ready",
                "ready": True,
                "degraded": False,
                "probe_mode": (
                    "read_only_boot_prerequisite_validation"
                ),
                "boot_executed": False,
                "configuration_loaded": True,
                "identity_loaded": True,
                "event_bus_required": True,
                "configured_environment": str(
                    app.get("environment", "unknown")
                ),
                "server_name": str(
                    server.get("name", "unknown")
                ),
                "server_role": str(
                    server.get("role", "unknown")
                ),
                "local_web_host": host,
                "local_web_mode": mode,
                "explicit_confirmation_required": True,
            }
        except Exception as exc:
            errors.append(
                self._error(
                    "core_boot",
                    "boot_prerequisite_error",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            payload = {
                "status": "degraded",
                "ready": False,
                "degraded": True,
                "probe_mode": (
                    "read_only_boot_prerequisite_validation"
                ),
                "boot_executed": False,
                "configuration_loaded": False,
                "identity_loaded": bool(
                    identity.get("available")
                ),
                "event_bus_required": True,
                "configured_environment": "unknown",
                "server_name": "unknown",
                "server_role": "unknown",
                "local_web_host": None,
                "local_web_mode": None,
                "explicit_confirmation_required": None,
            }

        return payload, errors

    def plugin_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Inspect built-in plugin modules without starting plugins."""

        errors: list[dict[str, str]] = []
        plugins: list[dict[str, Any]] = []

        for specification in self.EXPECTED_PLUGINS:
            name = str(specification["name"])
            module_name = str(specification["module"])
            class_name = str(specification["class_name"])

            try:
                module = importlib.import_module(
                    module_name
                )
                plugin_class = getattr(
                    module,
                    class_name,
                )

                declared_name = str(
                    getattr(plugin_class, "name", name)
                )
                version = str(
                    getattr(
                        plugin_class,
                        "version",
                        "unknown",
                    )
                )
                description = str(
                    getattr(
                        plugin_class,
                        "description",
                        "",
                    )
                )

                plugins.append(
                    {
                        "name": declared_name,
                        "version": version,
                        "description": description,
                        "status": "available",
                        "module_available": True,
                        "runtime_started": False,
                        "probe_mode": (
                            "read_only_module_availability"
                        ),
                    }
                )
            except Exception as exc:
                errors.append(
                    self._error(
                        f"plugin:{name}",
                        "plugin_module_unavailable",
                        f"{type(exc).__name__}: {exc}",
                    )
                )
                plugins.append(
                    {
                        "name": name,
                        "version": "unknown",
                        "description": "",
                        "status": "error",
                        "module_available": False,
                        "runtime_started": False,
                        "probe_mode": (
                            "read_only_module_availability"
                        ),
                    }
                )

        available_count = sum(
            1
            for plugin in plugins
            if plugin["module_available"] is True
        )
        all_available = (
            available_count == len(plugins)
            and bool(plugins)
        )

        return (
            {
                "status": (
                    "ok"
                    if all_available
                    else "degraded"
                ),
                "probe_mode": (
                    "read_only_module_availability"
                ),
                "plugins_started": False,
                "expected_count": len(
                    self.EXPECTED_PLUGINS
                ),
                "available_count": available_count,
                "unavailable_count": (
                    len(plugins) - available_count
                ),
                "all_available": all_available,
                "items": plugins,
            },
            errors,
        )

    def capability_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Return registry summary and boundary without mutation."""

        errors: list[dict[str, str]] = []

        try:
            summary = (
                self.capability_manager.capability_summary()
            )
            boundary = (
                self.capability_manager.safety_boundary()
            )
            payload = {
                "status": "ok",
                "available": True,
                "summary": summary,
                "runtime_ready": bool(
                    boundary.get("runtime_ready", False)
                ),
                "execution_ready": bool(
                    boundary.get(
                        "execution_ready",
                        False,
                    )
                ),
                "runtime_execution_features": int(
                    summary.get(
                        "runtime_execution_features",
                        0,
                    )
                ),
                "probe_mode": "read_only_registry",
            }
        except Exception as exc:
            errors.append(
                self._error(
                    "capabilities",
                    "capability_registry_error",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            payload = {
                "status": "degraded",
                "available": False,
                "summary": {},
                "runtime_ready": False,
                "execution_ready": False,
                "runtime_execution_features": 0,
                "probe_mode": "read_only_registry",
            }

        return payload, errors

    def service_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Return current lifecycle state and uptime."""

        errors: list[dict[str, str]] = []

        try:
            snapshot = self.lifecycle_manager.snapshot()
            state = str(
                snapshot.get("state", "unknown")
            )
            last_error = snapshot.get("last_error")

            payload = {
                "status": (
                    "degraded"
                    if state == "failed"
                    else "ok"
                ),
                "state": state,
                "safe_idle": bool(
                    snapshot.get("safe_idle", False)
                ),
                "listener_active": bool(
                    snapshot.get(
                        "listener_active",
                        False,
                    )
                ),
                "bound_host": snapshot.get(
                    "bound_host"
                ),
                "bound_port": snapshot.get(
                    "bound_port"
                ),
                "uptime_seconds": float(
                    snapshot.get(
                        "uptime_seconds",
                        0.0,
                    )
                ),
                "transition_count": int(
                    snapshot.get(
                        "transition_count",
                        0,
                    )
                ),
                "last_error": last_error,
                "last_failure_phase": snapshot.get(
                    "last_failure_phase"
                ),
                "last_stop_reason": snapshot.get(
                    "last_stop_reason"
                ),
                "process_owner": snapshot.get(
                    "process_owner",
                    {
                        "active": False,
                        "owner_name": None,
                    },
                ),
                "runtime_execution_features": int(
                    snapshot.get(
                        "runtime_execution_features",
                        0,
                    )
                ),
                "probe_mode": (
                    "read_only_lifecycle_snapshot"
                ),
            }

            if state == "failed" or last_error:
                errors.append(
                    self._error(
                        "service",
                        "service_degraded",
                        str(
                            last_error
                            or "Lifecycle state is failed."
                        ),
                    )
                )
        except Exception as exc:
            errors.append(
                self._error(
                    "service",
                    "service_snapshot_error",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            payload = {
                "status": "degraded",
                "state": "unknown",
                "safe_idle": True,
                "listener_active": False,
                "bound_host": None,
                "bound_port": None,
                "uptime_seconds": 0.0,
                "transition_count": 0,
                "last_error": str(exc),
                "last_failure_phase": "status_probe",
                "last_stop_reason": None,
                "process_owner": {
                    "active": False,
                    "owner_name": None,
                },
                "runtime_execution_features": 0,
                "probe_mode": (
                    "read_only_lifecycle_snapshot"
                ),
            }

        return payload, errors

    def memory_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Inspect memory-store availability without creating or writing it."""

        errors: list[dict[str, str]] = []
        stat = self._safe_stat(self.memory_file)

        if not stat["exists"]:
            errors.append(
                self._error(
                    "memory",
                    "memory_store_not_initialized",
                    (
                        "Memory store file is absent; the "
                        "status probe did not create it."
                    ),
                )
            )
            return (
                {
                    "status": "not_initialized",
                    "available": False,
                    "readable": False,
                    "writable_probe_performed": False,
                    "mutation_performed": False,
                    "storage_path": str(
                        self.memory_file.relative_to(
                            self.project_root
                        )
                    ),
                    "record_count": 0,
                    "valid_record_count": 0,
                    "invalid_record_count": 0,
                    "size_bytes": 0,
                    "modified_at_utc": None,
                    "probe_mode": (
                        "read_only_jsonl_availability"
                    ),
                },
                errors,
            )

        try:
            lines = self.memory_file.read_text(
                encoding="utf-8"
            ).splitlines()

            valid_count = 0
            invalid_count = 0
            for line in lines:
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                    if isinstance(value, dict):
                        valid_count += 1
                    else:
                        invalid_count += 1
                except Exception:
                    invalid_count += 1

            if invalid_count:
                errors.append(
                    self._error(
                        "memory",
                        "invalid_memory_records",
                        (
                            f"{invalid_count} memory record(s) "
                            "could not be parsed as JSON objects."
                        ),
                    )
                )

            return (
                {
                    "status": (
                        "ok"
                        if invalid_count == 0
                        else "degraded"
                    ),
                    "available": True,
                    "readable": True,
                    "writable_probe_performed": False,
                    "mutation_performed": False,
                    "storage_path": str(
                        self.memory_file.relative_to(
                            self.project_root
                        )
                    ),
                    "record_count": (
                        valid_count + invalid_count
                    ),
                    "valid_record_count": valid_count,
                    "invalid_record_count": invalid_count,
                    "size_bytes": stat["size_bytes"],
                    "modified_at_utc": (
                        stat["modified_at_utc"]
                    ),
                    "probe_mode": (
                        "read_only_jsonl_availability"
                    ),
                },
                errors,
            )
        except Exception as exc:
            errors.append(
                self._error(
                    "memory",
                    "memory_store_read_error",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            return (
                {
                    "status": "degraded",
                    "available": False,
                    "readable": False,
                    "writable_probe_performed": False,
                    "mutation_performed": False,
                    "storage_path": str(
                        self.memory_file.relative_to(
                            self.project_root
                        )
                    ),
                    "record_count": 0,
                    "valid_record_count": 0,
                    "invalid_record_count": 0,
                    "size_bytes": stat["size_bytes"],
                    "modified_at_utc": (
                        stat["modified_at_utc"]
                    ),
                    "probe_mode": (
                        "read_only_jsonl_availability"
                    ),
                },
                errors,
            )

    def safety_status(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Return consolidated runtime safety boundaries."""

        errors: list[dict[str, str]] = []

        try:
            registry_boundary = (
                self.capability_manager.safety_boundary()
            )
            lifecycle_boundary = (
                self.lifecycle_manager.safety_boundary()
            )

            payload = {
                "status": "safe_idle",
                "safe_idle": True,
                "read_only_status_api_runtime": True,
                "status_probe_side_effect_free": True,
                "mutation_routes_enabled": False,
                "http_methods_allowed": [
                    "GET",
                    "HEAD",
                ],
                "localhost_only": True,
                "runtime_ready": bool(
                    registry_boundary.get(
                        "runtime_ready",
                        False,
                    )
                ),
                "execution_ready": bool(
                    registry_boundary.get(
                        "execution_ready",
                        False,
                    )
                ),
                "background_service_runtime": bool(
                    registry_boundary.get(
                        "background_service_runtime",
                        False,
                    )
                ),
                "automatic_service_start_runtime": bool(
                    registry_boundary.get(
                        "automatic_service_start_runtime",
                        False,
                    )
                ),
                "chat_runtime": bool(
                    registry_boundary.get(
                        "chat_runtime",
                        False,
                    )
                ),
                "command_execution": bool(
                    registry_boundary.get(
                        "command_execution",
                        False,
                    )
                ),
                "tool_execution": bool(
                    registry_boundary.get(
                        "tool_execution",
                        False,
                    )
                ),
                "memory_write": bool(
                    registry_boundary.get(
                        "memory_write",
                        False,
                    )
                ),
                "permission_grant_runtime": bool(
                    registry_boundary.get(
                        "permission_grant_runtime",
                        False,
                    )
                ),
                "lifecycle_background_daemon": bool(
                    lifecycle_boundary.get(
                        "background_daemon",
                        False,
                    )
                ),
                "lifecycle_systemd_runtime": bool(
                    lifecycle_boundary.get(
                        "systemd_runtime",
                        False,
                    )
                ),
                "lifecycle_http_mutation": bool(
                    lifecycle_boundary.get(
                        "http_lifecycle_mutation",
                        False,
                    )
                ),
            }
        except Exception as exc:
            errors.append(
                self._error(
                    "safety",
                    "safety_boundary_error",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            payload = {
                "status": "degraded",
                "safe_idle": True,
                "read_only_status_api_runtime": True,
                "status_probe_side_effect_free": True,
                "mutation_routes_enabled": False,
                "http_methods_allowed": [
                    "GET",
                    "HEAD",
                ],
                "localhost_only": True,
                "runtime_ready": False,
                "execution_ready": False,
                "background_service_runtime": False,
                "automatic_service_start_runtime": False,
                "chat_runtime": False,
                "command_execution": False,
                "tool_execution": False,
                "memory_write": False,
                "permission_grant_runtime": False,
                "lifecycle_background_daemon": False,
                "lifecycle_systemd_runtime": False,
                "lifecycle_http_mutation": False,
            }

        return payload, errors

    def snapshot(self) -> dict[str, Any]:
        """Build one complete status envelope."""

        identity, identity_errors = (
            self.identity_status()
        )
        core_boot, boot_errors = (
            self.core_boot_status(identity)
        )
        plugins, plugin_errors = (
            self.plugin_status()
        )
        capabilities, capability_errors = (
            self.capability_status()
        )
        service, service_errors = (
            self.service_status()
        )
        memory, memory_errors = (
            self.memory_status()
        )
        safety, safety_errors = (
            self.safety_status()
        )

        errors = (
            identity_errors
            + boot_errors
            + plugin_errors
            + capability_errors
            + service_errors
            + memory_errors
            + safety_errors
        )

        component_states = {
            "identity": identity["status"],
            "core_boot": core_boot["status"],
            "plugins": plugins["status"],
            "capabilities": capabilities["status"],
            "service": service["status"],
            "memory": memory["status"],
            "safety": safety["status"],
        }

        degraded_components = sorted(
            name
            for name, state in component_states.items()
            if state not in {
                "ok",
                "ready",
                "safe_idle",
            }
        )
        degraded = bool(
            errors or degraded_components
        )

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "generated_at_utc": self._now_utc(),
            "status": (
                "degraded"
                if degraded
                else "ok"
            ),
            "degraded": degraded,
            "degraded_components": degraded_components,
            "error_count": len(errors),
            "identity": identity,
            "core_boot": core_boot,
            "plugins": plugins,
            "capabilities": capabilities,
            "service": service,
            "memory": memory,
            "safety": safety,
            "errors": errors,
            "routes": list(self.ROUTES),
            "route_count": len(self.ROUTES),
            "read_only": True,
            "mutation_allowed": False,
        }

    def health_payload(
        self,
        snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a compact health response."""

        status = (
            snapshot
            if snapshot is not None
            else self.snapshot()
        )

        identity = status["identity"]
        plugins = status["plugins"]
        service = status["service"]
        memory = status["memory"]
        safety = status["safety"]

        return {
            "schema_version": self.schema_version,
            "status": status["status"],
            "degraded": status["degraded"],
            "timestamp_utc": status["generated_at_utc"],
            "name": identity["name"],
            "version": identity["version"],
            "core_boot_ready": bool(
                status["core_boot"]["ready"]
            ),
            "plugins_available": bool(
                plugins["all_available"]
            ),
            "plugin_available_count": int(
                plugins["available_count"]
            ),
            "service_state": service["state"],
            "listener_active": bool(
                service["listener_active"]
            ),
            "service_uptime_seconds": float(
                service["uptime_seconds"]
            ),
            "memory_available": bool(
                memory["available"]
            ),
            "memory_status": memory["status"],
            "safe_idle": bool(
                safety["safe_idle"]
            ),
            "runtime_ready": bool(
                safety["runtime_ready"]
            ),
            "execution_ready": bool(
                safety["execution_ready"]
            ),
            "error_count": int(
                status["error_count"]
            ),
            "chat_runtime": bool(
                safety["chat_runtime"]
            ),
            "model_runtime": False,
            "command_execution": bool(
                safety["command_execution"]
            ),
            "tool_execution": bool(
                safety["tool_execution"]
            ),
            "memory_write": bool(
                safety["memory_write"]
            ),
            "permission_grant_runtime": bool(
                safety["permission_grant_runtime"]
            ),
            "mutation_allowed": False,
        }

    def payload_for_route(
        self,
        route: str,
        *,
        snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return the read-only payload assigned to one API route."""

        status = (
            snapshot
            if snapshot is not None
            else self.snapshot()
        )

        mapping = {
            "/health": lambda: self.health_payload(
                status
            ),
            "/api/status": lambda: status,
            "/api/status/identity": lambda: (
                status["identity"]
            ),
            "/api/status/plugins": lambda: (
                status["plugins"]
            ),
            "/api/status/capabilities": lambda: (
                status["capabilities"]
            ),
            "/api/status/service": lambda: (
                status["service"]
            ),
            "/api/status/memory": lambda: (
                status["memory"]
            ),
            "/api/status/safety": lambda: (
                status["safety"]
            ),
            "/api/status/errors": lambda: {
                "status": (
                    "degraded"
                    if status["errors"]
                    else "ok"
                ),
                "error_count": status["error_count"],
                "degraded_components": status[
                    "degraded_components"
                ],
                "items": status["errors"],
                "generated_at_utc": status[
                    "generated_at_utc"
                ],
            },
        }

        try:
            factory = mapping[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 183 status route: {route}"
            ) from exc

        return factory()

    def self_test(self) -> dict[str, Any]:
        """Validate healthy, degraded, and side-effect-free behavior."""

        assertions: dict[str, bool] = {}

        watched_paths = (
            self.identity_path,
            self.settings_path,
            self.memory_file,
        )
        before = {
            str(path): self._file_fingerprint(path)
            for path in watched_paths
        }

        snapshot = self.snapshot()
        health = self.health_payload(snapshot)

        after = {
            str(path): self._file_fingerprint(path)
            for path in watched_paths
        }

        assertions["schema_version_one"] = (
            snapshot["schema_version"] == "1.0"
        )
        assertions["sprint_183"] = (
            snapshot["sprint"] == 183
        )
        assertions["route_count_nine"] = (
            snapshot["route_count"] == 9
        )
        assertions["all_routes_declared"] = (
            tuple(snapshot["routes"]) == self.ROUTES
        )
        assertions["snapshot_read_only"] = (
            snapshot["read_only"] is True
        )
        assertions["mutation_disallowed"] = (
            snapshot["mutation_allowed"] is False
        )
        assertions["identity_available"] = (
            snapshot["identity"]["available"] is True
        )
        assertions['identity_version_185'] = (
            snapshot["identity"]["version"]
            == '0.185.0-genesis'
        )
        assertions["boot_probe_did_not_execute_boot"] = (
            snapshot["core_boot"]["boot_executed"]
            is False
        )
        assertions["boot_prerequisites_ready"] = (
            snapshot["core_boot"]["ready"] is True
        )
        assertions["plugins_not_started"] = (
            snapshot["plugins"]["plugins_started"]
            is False
        )
        assertions["two_plugins_expected"] = (
            snapshot["plugins"]["expected_count"] == 2
        )
        assertions["two_plugins_available"] = (
            snapshot["plugins"]["available_count"] == 2
        )
        assertions["capability_registry_available"] = (
            snapshot["capabilities"]["available"]
            is True
        )
        assertions['capability_total_116'] = (
            snapshot["capabilities"]["summary"][
                "total_capabilities"
            ]
            == 116
        )
        assertions['capability_online_114'] = (
            snapshot["capabilities"]["summary"][
                "online_capabilities"
            ]
            == 114
        )
        assertions['permission_gated_eight'] = (
            snapshot["capabilities"]["summary"][
                "permission_gated_count"
            ]
            == 8
        )
        assertions["runtime_feature_count_one"] = (
            snapshot["capabilities"][
                "runtime_execution_features"
            ]
            == 1
        )
        assertions["service_snapshot_present"] = (
            snapshot["service"]["state"]
            in {
                "stopped",
                "starting",
                "running",
                "stopping",
                "failed",
            }
        )
        assertions["service_status_probe_read_only"] = (
            snapshot["service"]["probe_mode"]
            == "read_only_lifecycle_snapshot"
        )
        assertions["service_uptime_numeric"] = (
            isinstance(
                snapshot["service"][
                    "uptime_seconds"
                ],
                float,
            )
        )
        assertions["memory_probe_no_write_test"] = (
            snapshot["memory"][
                "writable_probe_performed"
            ]
            is False
        )
        assertions["memory_probe_no_mutation"] = (
            snapshot["memory"][
                "mutation_performed"
            ]
            is False
        )
        assertions["safety_safe_idle"] = (
            snapshot["safety"]["safe_idle"] is True
        )
        assertions["status_api_read_only"] = (
            snapshot["safety"][
                "read_only_status_api_runtime"
            ]
            is True
        )
        assertions["probe_side_effect_free"] = (
            snapshot["safety"][
                "status_probe_side_effect_free"
            ]
            is True
        )
        assertions["mutation_routes_disabled"] = (
            snapshot["safety"][
                "mutation_routes_enabled"
            ]
            is False
        )
        assertions["runtime_ready_false"] = (
            snapshot["safety"]["runtime_ready"]
            is False
        )
        assertions["execution_ready_false"] = (
            snapshot["safety"]["execution_ready"]
            is False
        )
        assertions["background_service_false"] = (
            snapshot["safety"][
                "background_service_runtime"
            ]
            is False
        )
        assertions["auto_start_false"] = (
            snapshot["safety"][
                "automatic_service_start_runtime"
            ]
            is False
        )
        assertions["chat_false"] = (
            snapshot["safety"]["chat_runtime"]
            is False
        )
        assertions["command_false"] = (
            snapshot["safety"][
                "command_execution"
            ]
            is False
        )
        assertions["tool_false"] = (
            snapshot["safety"]["tool_execution"]
            is False
        )
        assertions["memory_write_false"] = (
            snapshot["safety"]["memory_write"]
            is False
        )
        assertions["permission_grant_false"] = (
            snapshot["safety"][
                "permission_grant_runtime"
            ]
            is False
        )
        assertions["health_identity_matches"] = (
            health["version"]
            == snapshot["identity"]["version"]
        )
        assertions["health_service_state_matches"] = (
            health["service_state"]
            == snapshot["service"]["state"]
        )
        assertions["health_mutation_disallowed"] = (
            health["mutation_allowed"] is False
        )
        assertions["watched_files_unchanged"] = (
            before == after
        )

        for route in self.ROUTES:
            payload = self.payload_for_route(
                route,
                snapshot=snapshot,
            )
            assertions[
                "route_payload_mapping_"
                + route.replace("/", "_").strip("_")
            ] = isinstance(payload, dict)

        unknown_route_blocked = False
        try:
            self.payload_for_route(
                "/api/status/unknown",
                snapshot=snapshot,
            )
        except KeyError:
            unknown_route_blocked = True
        assertions["unknown_route_blocked"] = (
            unknown_route_blocked
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s183-degraded-"
        ) as temporary:
            degraded_root = Path(temporary)
            (
                degraded_root
                / "aura"
                / "personality"
            ).mkdir(parents=True)
            (
                degraded_root
                / "aura"
                / "personality"
                / "identity.yaml"
            ).write_text(
                "name: AURA\n",
                encoding="utf-8",
            )

            degraded_manager = (
                AuraHealthStatusApiRuntimeManager(
                    project_root=degraded_root,
                    lifecycle_manager=(
                        AuraServiceLifecycleRuntimeManager()
                    ),
                    capability_manager=(
                        self.capability_manager
                    ),
                    clock=self._clock,
                )
            )
            degraded = degraded_manager.snapshot()

            assertions["degraded_fixture_detected"] = (
                degraded["degraded"] is True
            )
            assertions["degraded_status_visible"] = (
                degraded["status"] == "degraded"
            )
            assertions["degraded_has_errors"] = (
                degraded["error_count"] >= 2
            )
            assertions["identity_degraded_visible"] = (
                degraded["identity"]["available"]
                is False
            )
            assertions["boot_degraded_visible"] = (
                degraded["core_boot"]["ready"]
                is False
            )
            assertions["memory_missing_visible"] = (
                degraded["memory"]["status"]
                == "not_initialized"
            )
            assertions["degraded_probe_created_no_memory"] = (
                not degraded_manager.memory_file.exists()
            )
            assertions["degraded_probe_created_no_settings"] = (
                not degraded_manager.settings_path.exists()
            )
            assertions["degraded_errors_route_visible"] = (
                degraded_manager.payload_for_route(
                    "/api/status/errors",
                    snapshot=degraded,
                )["error_count"]
                == degraded["error_count"]
            )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise HealthStatusAggregationError(
                "Health/status self-test failed: "
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
            "route_count": len(self.ROUTES),
            "routes": list(self.ROUTES),
            "healthy_snapshot_status": snapshot[
                "status"
            ],
            "healthy_snapshot_error_count": snapshot[
                "error_count"
            ],
            "degraded_fixture_verified": True,
            "read_only_file_integrity_verified": True,
            "plugins_started_by_probe": False,
            "memory_mutation_performed": False,
            "listener_started_by_probe": False,
        }
