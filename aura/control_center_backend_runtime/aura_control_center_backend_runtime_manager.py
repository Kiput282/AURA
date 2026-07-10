"""AURA Sprint 184 read-only Control Center backend core.

This module converts the Sprint 183 health/status snapshot and older
Control Center foundation contracts into stable browser-facing view models.

Part A does not attach routes to HTTP, render a frontend, start plugins,
resolve permissions, write audit events, mutate memory, or execute actions.
"""

from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)
from aura.health_status_api_runtime.aura_health_status_api_runtime_manager import (
    AuraHealthStatusApiRuntimeManager,
)


class ControlCenterBackendError(RuntimeError):
    """Raised when the backend view-model contract fails validation."""


class AuraControlCenterBackendRuntimeManager:
    """Build stable read-only Control Center backend payloads."""

    name = "aura_control_center_backend_runtime"
    component_version = "0.1.0-alpha"
    sprint = 184
    schema_version = "1.0"

    ROUTES = (
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

    FOUNDATION_MODULES = (
        {
            "id": "data_aggregator",
            "module": (
                "aura.control_center_data_aggregator."
                "aura_control_center_data_aggregator_foundation_manager"
            ),
        },
        {
            "id": "api_contract",
            "module": (
                "aura.dashboard_api_contract_consolidation."
                "aura_dashboard_api_contract_consolidation_foundation_manager"
            ),
        },
        {
            "id": "runtime_readiness",
            "module": (
                "aura.dashboard_runtime_readiness_view_model."
                "aura_dashboard_runtime_readiness_view_model_foundation_manager"
            ),
        },
        {
            "id": "service_monitor",
            "module": (
                "aura.control_center_service_monitor_panel_foundation."
                "aura_control_center_service_monitor_panel_foundation_manager"
            ),
        },
        {
            "id": "capability_viewer",
            "module": (
                "aura.control_center_capability_viewer_foundation."
                "aura_control_center_capability_viewer_foundation_manager"
            ),
        },
        {
            "id": "plugin_viewer",
            "module": (
                "aura.control_center_plugin_panel_foundation."
                "aura_control_center_plugin_panel_foundation_manager"
            ),
        },
        {
            "id": "permission_panel",
            "module": (
                "aura.control_center_permission_panel_foundation."
                "aura_control_center_permission_panel_foundation_manager"
            ),
        },
        {
            "id": "audit_panel",
            "module": (
                "aura.control_center_audit_panel_foundation."
                "aura_control_center_audit_panel_foundation_manager"
            ),
        },
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        status_manager: AuraHealthStatusApiRuntimeManager | None = None,
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
        self.memory_file = (
            self.project_root
            / "data"
            / "memory"
            / "memories.jsonl"
        )

        self.capability_manager = (
            capability_manager
            if capability_manager is not None
            else CapabilityRegistryManager()
        )
        self.status_manager = (
            status_manager
            if status_manager is not None
            else AuraHealthStatusApiRuntimeManager(
                project_root=self.project_root,
                capability_manager=self.capability_manager,
            )
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

    @staticmethod
    def _manager_class(module: Any) -> type:
        candidates: list[type] = []

        for _, candidate in inspect.getmembers(
            module,
            inspect.isclass,
        ):
            if candidate.__module__ != module.__name__:
                continue
            if not candidate.__name__.startswith("Aura"):
                continue
            if not candidate.__name__.endswith("Manager"):
                continue
            if not hasattr(candidate, "status"):
                continue
            candidates.append(candidate)

        if len(candidates) != 1:
            raise LookupError(
                "Expected exactly one Aura*Manager with status(); "
                f"found {len(candidates)} in {module.__name__}."
            )
        return candidates[0]

    def foundation_contracts(
        self,
    ) -> tuple[dict[str, Any], list[dict[str, str]]]:
        """Read foundation status contracts without activating runtime."""

        errors: list[dict[str, str]] = []
        items: list[dict[str, Any]] = []

        for specification in self.FOUNDATION_MODULES:
            contract_id = str(specification["id"])
            module_name = str(specification["module"])

            try:
                module = importlib.import_module(module_name)
                manager_class = self._manager_class(module)
                manager = manager_class(self.project_root)
                status = manager.status()

                if not isinstance(status, dict):
                    raise TypeError(
                        "Foundation status() did not return a mapping."
                    )

                items.append(
                    {
                        "id": contract_id,
                        "status": "available",
                        "available": True,
                        "module": module_name,
                        "manager_class": manager_class.__name__,
                        "foundation_name": str(
                            status.get(
                                "name",
                                contract_id,
                            )
                        ),
                        "foundation_version": str(
                            status.get(
                                "version",
                                "unknown",
                            )
                        ),
                        "foundation_status": str(
                            status.get(
                                "status",
                                "unknown",
                            )
                        ),
                        "runtime_activated": False,
                        "probe_mode": (
                            "read_only_foundation_status"
                        ),
                    }
                )
            except Exception as exc:
                errors.append(
                    self._error(
                        f"foundation:{contract_id}",
                        "foundation_contract_unavailable",
                        f"{type(exc).__name__}: {exc}",
                    )
                )
                items.append(
                    {
                        "id": contract_id,
                        "status": "unavailable",
                        "available": False,
                        "module": module_name,
                        "manager_class": None,
                        "foundation_name": contract_id,
                        "foundation_version": "unknown",
                        "foundation_status": "unknown",
                        "runtime_activated": False,
                        "probe_mode": (
                            "read_only_foundation_status"
                        ),
                    }
                )

        available_count = sum(
            1
            for item in items
            if item["available"] is True
        )

        return (
            {
                "status": (
                    "ok"
                    if available_count == len(items)
                    else "degraded"
                ),
                "expected_count": len(
                    self.FOUNDATION_MODULES
                ),
                "available_count": available_count,
                "unavailable_count": (
                    len(items) - available_count
                ),
                "all_available": (
                    available_count == len(items)
                ),
                "runtime_activated": False,
                "probe_mode": (
                    "read_only_foundation_status"
                ),
                "items": items,
            },
            errors,
        )

    def capability_cards(
        self,
    ) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        """Convert the registry catalog into read-only viewer cards."""

        errors: list[dict[str, str]] = []

        try:
            catalog = self.capability_manager.capability_catalog()
            cards = [
                {
                    "id": str(item.get("id", "")),
                    "name": str(item.get("name", "")),
                    "state": str(
                        item.get("state", "unknown")
                    ),
                    "runtime_level": str(
                        item.get(
                            "runtime_level",
                            "unknown",
                        )
                    ),
                    "risk_level": str(
                        item.get(
                            "risk_level",
                            "unknown",
                        )
                    ),
                    "permission_required": str(
                        item.get(
                            "permission_required",
                            "unknown",
                        )
                    ),
                    "category": str(
                        item.get(
                            "category",
                            "unknown",
                        )
                    ),
                    "introduced_in": str(
                        item.get(
                            "introduced_in",
                            "unknown",
                        )
                    ),
                    "control_center_visible": bool(
                        item.get(
                            "control_center_visible",
                            False,
                        )
                    ),
                    "description": str(
                        item.get("description", "")
                    ),
                    "actions_allowed": False,
                }
                for item in catalog
            ]
            cards.sort(
                key=lambda item: (
                    item["category"],
                    item["id"],
                )
            )
            return cards, errors
        except Exception as exc:
            errors.append(
                self._error(
                    "capability_viewer",
                    "capability_cards_unavailable",
                    f"{type(exc).__name__}: {exc}",
                )
            )
            return [], errors

    def overview_panel(
        self,
        status: dict[str, Any],
        foundations: dict[str, Any],
    ) -> dict[str, Any]:
        summary = status["capabilities"]["summary"]
        service = status["service"]

        return {
            "panel_id": "overview",
            "title": "Genesis Dashboard Overview",
            "status": status["status"],
            "degraded": status["degraded"],
            "identity": {
                "name": status["identity"]["name"],
                "version": status["identity"]["version"],
                "codename": status["identity"]["codename"],
                "creator": status["identity"]["creator"],
            },
            "core_boot_ready": bool(
                status["core_boot"]["ready"]
            ),
            "safe_idle": bool(
                status["safety"]["safe_idle"]
            ),
            "service_state": service["state"],
            "listener_active": bool(
                service["listener_active"]
            ),
            "uptime_seconds": float(
                service["uptime_seconds"]
            ),
            "capability_total": int(
                summary["total_capabilities"]
            ),
            "online_capabilities": int(
                summary["online_capabilities"]
            ),
            "permission_gated_capabilities": int(
                summary["permission_gated_count"]
            ),
            "runtime_execution_features": int(
                summary["runtime_execution_features"]
            ),
            "plugin_available_count": int(
                status["plugins"]["available_count"]
            ),
            "plugin_expected_count": int(
                status["plugins"]["expected_count"]
            ),
            "memory_status": status["memory"]["status"],
            "memory_available": bool(
                status["memory"]["available"]
            ),
            "error_count": int(status["error_count"]),
            "foundation_contracts_available": int(
                foundations["available_count"]
            ),
            "foundation_contracts_expected": int(
                foundations["expected_count"]
            ),
            "read_only": True,
            "actions_allowed": False,
        }

    def service_panel(
        self,
        status: dict[str, Any],
    ) -> dict[str, Any]:
        service = status["service"]

        return {
            "panel_id": "service",
            "title": "Service Monitor",
            "status": service["status"],
            "state": service["state"],
            "safe_idle": bool(service["safe_idle"]),
            "listener_active": bool(
                service["listener_active"]
            ),
            "bound_host": service["bound_host"],
            "bound_port": service["bound_port"],
            "uptime_seconds": float(
                service["uptime_seconds"]
            ),
            "transition_count": int(
                service["transition_count"]
            ),
            "last_error": service["last_error"],
            "last_failure_phase": service[
                "last_failure_phase"
            ],
            "last_stop_reason": service[
                "last_stop_reason"
            ],
            "process_owner": service["process_owner"],
            "start_control_enabled": False,
            "stop_control_enabled": False,
            "restart_control_enabled": False,
            "systemd_control_enabled": False,
            "auto_start_control_enabled": False,
            "read_only": True,
            "actions_allowed": False,
        }

    def capabilities_panel(
        self,
        status: dict[str, Any],
        cards: list[dict[str, Any]],
    ) -> dict[str, Any]:
        summary = status["capabilities"]["summary"]

        return {
            "panel_id": "capabilities",
            "title": "Capability Viewer",
            "status": (
                "ok"
                if cards
                else "degraded"
            ),
            "summary": summary,
            "card_count": len(cards),
            "cards": cards,
            "filter_fields": [
                "state",
                "runtime_level",
                "risk_level",
                "permission_required",
                "category",
            ],
            "mutation_enabled": False,
            "read_only": True,
            "actions_allowed": False,
        }

    def plugins_panel(
        self,
        status: dict[str, Any],
    ) -> dict[str, Any]:
        plugins = status["plugins"]

        return {
            "panel_id": "plugins",
            "title": "Plugin Viewer",
            "status": plugins["status"],
            "expected_count": int(
                plugins["expected_count"]
            ),
            "available_count": int(
                plugins["available_count"]
            ),
            "unavailable_count": int(
                plugins["unavailable_count"]
            ),
            "all_available": bool(
                plugins["all_available"]
            ),
            "plugins_started": bool(
                plugins["plugins_started"]
            ),
            "items": plugins["items"],
            "install_enabled": False,
            "enable_enabled": False,
            "disable_enabled": False,
            "reload_enabled": False,
            "read_only": True,
            "actions_allowed": False,
        }

    def permissions_panel(
        self,
        status: dict[str, Any],
        foundations: dict[str, Any],
    ) -> dict[str, Any]:
        summary = status["capabilities"]["summary"]
        safety = status["safety"]
        permission_contract = next(
            (
                item
                for item in foundations["items"]
                if item["id"] == "permission_panel"
            ),
            {
                "available": False,
                "foundation_status": "unknown",
            },
        )

        return {
            "panel_id": "permissions",
            "title": "Permission State",
            "status": (
                "ok"
                if permission_contract["available"]
                else "degraded"
            ),
            "visibility_mode": (
                "declared_requirements_read_only"
            ),
            "foundation_available": bool(
                permission_contract["available"]
            ),
            "foundation_status": permission_contract[
                "foundation_status"
            ],
            "permission_gated_capability_count": int(
                summary["permission_gated_count"]
            ),
            "declared_permission_counts": summary[
                "permission_counts"
            ],
            "pending_request_runtime_active": False,
            "pending_request_count": None,
            "decision_runtime_active": False,
            "grant_runtime_active": bool(
                safety["permission_grant_runtime"]
            ),
            "deny_runtime_active": False,
            "scope_mutation_enabled": False,
            "read_only": True,
            "actions_allowed": False,
        }

    def audit_panel(
        self,
        foundations: dict[str, Any],
    ) -> dict[str, Any]:
        audit_contract = next(
            (
                item
                for item in foundations["items"]
                if item["id"] == "audit_panel"
            ),
            {
                "available": False,
                "foundation_status": "unknown",
            },
        )

        return {
            "panel_id": "audit",
            "title": "Audit State",
            "status": (
                "not_activated"
                if audit_contract["available"]
                else "degraded"
            ),
            "foundation_available": bool(
                audit_contract["available"]
            ),
            "foundation_status": audit_contract[
                "foundation_status"
            ],
            "runtime_writer_active": False,
            "persistence_active": False,
            "runtime_event_fetch_active": False,
            "runtime_event_count": 0,
            "events": [],
            "event_state": (
                "no_runtime_audit_writer"
            ),
            "read_only": True,
            "actions_allowed": False,
        }

    def memory_panel(
        self,
        status: dict[str, Any],
    ) -> dict[str, Any]:
        memory = status["memory"]

        return {
            "panel_id": "memory",
            "title": "Memory Status",
            "status": memory["status"],
            "available": bool(memory["available"]),
            "readable": bool(memory["readable"]),
            "storage_path": memory["storage_path"],
            "record_count": int(
                memory["record_count"]
            ),
            "valid_record_count": int(
                memory["valid_record_count"]
            ),
            "invalid_record_count": int(
                memory["invalid_record_count"]
            ),
            "size_bytes": int(memory["size_bytes"]),
            "modified_at_utc": memory[
                "modified_at_utc"
            ],
            "writable_probe_performed": bool(
                memory["writable_probe_performed"]
            ),
            "mutation_performed": bool(
                memory["mutation_performed"]
            ),
            "create_enabled": False,
            "edit_enabled": False,
            "delete_enabled": False,
            "pin_enabled": False,
            "read_only": True,
            "actions_allowed": False,
        }

    def readiness_panel(
        self,
        status: dict[str, Any],
        foundations: dict[str, Any],
    ) -> dict[str, Any]:
        safety = status["safety"]

        ready_surfaces = {
                             'localhost_listener': True,
                             'deterministic_lifecycle': True,
                             'health_status_api': True,
                             'control_center_backend_core': True,
                             'control_center_web_shell': True,
                             'browser_chat_sessions': True,
                             'local_model_bridge_core': True,
                             'local_model_provider_contracts': True,
                             'local_model_browser_chat_route': True,
                             'local_model_response_persistence': True,
                             'interactive_control_center_chat': True,
                             'interactive_chat_web_surface': True,
                             'interactive_chat_model_status_ui': True,
                             'interactive_chat_explicit_confirmation': True,
                             'interactive_chat_idempotent_retry': True,
                             'interactive_chat_response_kind_visibility': True,
                             'permission_audit_recovery_visibility': True,
                             'permission_visibility_surface': True,
                             'audit_contract_visibility_surface': True,
                             'recovery_guidance_visibility_surface': True,
                             'visibility_http_api': True,
                             'visibility_browser_panel': True,
                             'visibility_redaction_contract': True,
                             'local_chat_history_persistence': True,
                             'validated_message_submission': True,
                             'explicit_clear_confirmation': True,
                             'local_static_asset_delivery': True,
                             'responsive_dashboard_layout': True,
                             'accessibility_contract': True,
                             'identity_status': bool(
                status["identity"]["available"]
            ),
                             'plugin_status': bool(
                status["plugins"]["all_available"]
            ),
                             'capability_status': bool(
                status["capabilities"]["available"]
            ),
                             'service_status': status["service"]["state"]
                != "unknown",
                             'memory_status': True,
                             'safety_status': True,
                             'foundation_contracts': bool(
                foundations["all_available"]
            ),
                         }
        blocked_surfaces = {
                               'permission_decision_runtime': False,
                               'audit_writer_runtime': False,
                               'background_service': False,
                               'systemd_runtime': False,
                               'automatic_start': False,
                               'public_or_lan_listener': False,
                               'command_or_tool_execution': False,
                               'autonomous_actions': False,
                           }

        backend_ready = all(ready_surfaces.values())
        blockers = [
            key
            for key, enabled in blocked_surfaces.items()
            if enabled is False
        ]

        return {
                   'panel_id': "readiness",
                   'title': "Runtime Readiness",
                   'status': "permission_audit_recovery_visibility_ready" if backend_ready else "degraded",
                   'backend_ready': backend_ready,
                   'web_shell_ready': True,
                   'interaction_runtime_ready': bool(
                safety["runtime_ready"]
            ),
                   'execution_ready': bool(
                safety["execution_ready"]
            ),
                   'current_stage': "permission_audit_recovery_visibility_runtime",
                   'ready_surfaces': ready_surfaces,
                   'blocked_surfaces': blocked_surfaces,
                   'blockers': blockers,
                   'next_sprint': "Sprint 191 — Voice Runtime Activation Foundation",
                   'read_only': False,
                   'actions_allowed': False,
                   'shell_asset_route_count': 3,
                   'total_route_count': 37,
                   'browser_auto_launch': False,
                   'external_dependencies': False,
                   'browser_chat_ready': True,
                   'local_model_bridge_ready': True,
                   'bounded_session_mutation': True,
                   'chat_asset_route_count': 3,
                   'chat_route_contract_count': 7,
                   'model_bridge_active': False,
                   'aura_memory_write_active': False,
                   'model_route_contract_count': 2,
                   'model_bridge_configured': False,
                   'local_model_enabled_by_default': False,
                   'interactive_chat_ready': True,
                   'interactive_chat_web_surface_ready': True,
                   'interactive_chat_runtime_ready': True,
                   'interactive_chat_web_assertion_count': 166,
                   'interactive_chat_runtime_assertion_count': 119,
                   'save_only_default': True,
                   'explicit_model_request_confirmation': True,
                   'explicit_model_probe_confirmation': True,
                   'idempotent_model_retry': True,
                   'response_kind_visibility': True,
                   'local_browser_storage_active': False,
                   'websocket_active': False,
                   'eventsource_active': False,
                   'permission_audit_recovery_visibility_ready': True,
                   'permission_visibility_ready': True,
                   'audit_contract_visibility_ready': True,
                   'recovery_guidance_visibility_ready': True,
                   'visibility_core_assertion_count': 127,
                   'visibility_web_assertion_count': 143,
                   'visibility_api_route_count': 4,
                   'visibility_asset_route_count': 3,
                   'visibility_total_route_count': 7,
                   'visibility_page_route': "/visibility",
                   'visibility_read_only': True,
                   'sensitive_values_exposed': False,
                   'permission_mutation_active': False,
                   'audit_writer_active': False,
                   'audit_persistence_active': False,
                   'automatic_recovery_active': False,
                   'rollback_execution_active': False,
               }

    def snapshot(self) -> dict[str, Any]:
        """Build the complete read-only Control Center backend snapshot."""

        status = self.status_manager.snapshot()
        foundations, foundation_errors = (
            self.foundation_contracts()
        )
        cards, card_errors = self.capability_cards()

        panels = {
            "overview": self.overview_panel(
                status,
                foundations,
            ),
            "service": self.service_panel(status),
            "capabilities": self.capabilities_panel(
                status,
                cards,
            ),
            "plugins": self.plugins_panel(status),
            "permissions": self.permissions_panel(
                status,
                foundations,
            ),
            "audit": self.audit_panel(foundations),
            "memory": self.memory_panel(status),
            "readiness": self.readiness_panel(
                status,
                foundations,
            ),
        }

        errors = (
            list(status["errors"])
            + foundation_errors
            + card_errors
        )

        degraded_panels = sorted(
            panel_id
            for panel_id, panel in panels.items()
            if panel["status"]
            in {
                "degraded",
                "error",
            }
        )
        degraded = bool(
            status["degraded"]
            or errors
            or degraded_panels
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
            "degraded_panels": degraded_panels,
            "error_count": len(errors),
            "errors": errors,
            "route_count": len(self.ROUTES),
            "routes": list(self.ROUTES),
            "panel_count": len(self.PANEL_IDS),
            "panel_ids": list(self.PANEL_IDS),
            "foundations": foundations,
            "panels": panels,
            "source_status": {
                "schema_version": status[
                    "schema_version"
                ],
                "status": status["status"],
                "generated_at_utc": status[
                    "generated_at_utc"
                ],
                "sprint": status["sprint"],
            },
            "read_only": True,
            "mutation_allowed": False,
            "frontend_rendered": False,
            "listener_started_by_backend": False,
        }

    def payload_for_route(
        self,
        route: str,
        *,
        snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return one Control Center backend route payload."""

        backend = (
            snapshot
            if snapshot is not None
            else self.snapshot()
        )

        route_to_panel = {
            "/api/control-center/overview": "overview",
            "/api/control-center/service": "service",
            "/api/control-center/capabilities": (
                "capabilities"
            ),
            "/api/control-center/plugins": "plugins",
            "/api/control-center/permissions": (
                "permissions"
            ),
            "/api/control-center/audit": "audit",
            "/api/control-center/memory": "memory",
            "/api/control-center/readiness": "readiness",
        }

        if route == "/api/control-center":
            return backend

        try:
            panel_id = route_to_panel[route]
        except KeyError as exc:
            raise KeyError(
                f"Unknown Sprint 184 backend route: {route}"
            ) from exc

        panel = backend["panels"][panel_id]
        return {
            "schema_version": backend["schema_version"],
            "generated_at_utc": backend[
                "generated_at_utc"
            ],
            "backend_status": backend["status"],
            "backend_degraded": backend["degraded"],
            "error_count": backend["error_count"],
            "panel": panel,
            "read_only": True,
            "mutation_allowed": False,
        }

    def safety_boundary(self) -> dict[str, Any]:
        """Return the Sprint 184 backend safety boundary."""

        return {
                   'control_center_backend_runtime': True,
                   'read_only_backend_view_models': True,
                   'backend_route_count': len(self.ROUTES),
                   'backend_panel_count': len(self.PANEL_IDS),
                   'frontend_runtime': True,
                   'static_file_serving_runtime': True,
                   'browser_chat_session_runtime': True,
                   'browser_chat_http_routes': True,
                   'browser_chat_asset_route_count': 3,
                   'browser_chat_route_contract_count': 7,
                   'total_route_contract_count': 37,
                   'bounded_session_mutation': True,
                   'atomic_session_persistence': True,
                   'session_integrity_hash': True,
                   'optimistic_revision_control': True,
                   'idempotent_message_submission': True,
                   'explicit_clear_confirmation': True,
                   'local_model_bridge_runtime': True,
                   'model_inference_runtime': True,
                   'model_route_contract_count': 2,
                   'browser_chat_model_bridge_runtime': True,
                   'interactive_control_center_chat_runtime': True,
                   'interactive_chat_web_surface_runtime': True,
                   'interactive_chat_orchestration_runtime': True,
                   'interactive_chat_save_only_default': True,
                   'interactive_chat_explicit_model_confirmation': True,
                   'interactive_chat_explicit_probe_confirmation': True,
                   'interactive_chat_idempotent_retry': True,
                   'interactive_chat_response_kind_visibility': True,
                   'permission_audit_recovery_visibility_runtime': True,
                   'permission_visibility_runtime': True,
                   'audit_contract_visibility_runtime': True,
                   'recovery_guidance_visibility_runtime': True,
                   'permission_audit_recovery_http_routes': True,
                   'permission_audit_recovery_browser_panel': True,
                   'permission_audit_recovery_api_route_count': 4,
                   'permission_audit_recovery_asset_route_count': 3,
                   'permission_audit_recovery_total_route_count': 7,
                   'permission_audit_recovery_read_only': True,
                   'sensitive_values_exposed': False,
                   'permission_mutation_runtime': False,
                   'permission_persistence_runtime': False,
                   'automatic_recovery_runtime': False,
                   'automatic_retry_runtime': False,
                   'rollback_execution_runtime': False,
                   'interactive_chat_local_browser_storage_runtime': False,
                   'interactive_chat_websocket_runtime': False,
                   'interactive_chat_eventsource_runtime': False,
                   'interactive_chat_tool_action_command_ui': False,
                   'model_provider_profiles_environment_only': True,
                   'model_loopback_endpoint_enforcement': True,
                   'model_resolved_loopback_enforcement': True,
                   'model_redirect_following_runtime': False,
                   'explicit_model_probe_confirmation': True,
                   'explicit_model_request_confirmation': True,
                   'model_response_persistence': True,
                   'model_download_runtime': False,
                   'model_streaming_runtime': False,
                   'model_tool_calling_runtime': False,
                   'network_fallback_runtime': False,
                   'aura_long_term_memory_write': False,
                   'control_center_web_shell_runtime': True,
                   'shell_asset_route_count': 3,
                   'total_route_count': 21,
                   'responsive_layout': True,
                   'accessibility_contract': True,
                   'degraded_state_ui': True,
                   'external_dependency_runtime': False,
                   'browser_launch_runtime': False,
                   'backend_mutation_runtime': False,
                   'service_control_runtime': False,
                   'plugin_control_runtime': False,
                   'permission_decision_runtime': False,
                   'permission_grant_runtime': False,
                   'permission_deny_runtime': False,
                   'audit_writer_runtime': False,
                   'audit_persistence_runtime': False,
                   'memory_write_runtime': False,
                   'chat_runtime': False,
                   'model_runtime': False,
                   'command_execution': False,
                   'tool_execution': False,
                   'action_dispatch': False,
                   'background_service_runtime': False,
                   'systemd_runtime': False,
                   'automatic_start_runtime': False,
                   'public_listener_runtime': False,
                   'lan_listener_runtime': False,
                   'autonomous_action': False,
                   'safe_idle': True,
                   'read_only': True,
               }

    def self_test(self) -> dict[str, Any]:
        """Validate contracts, degraded visibility, and no side effects."""

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

        after = {
            str(path): self._file_fingerprint(path)
            for path in watched_paths
        }

        assertions["schema_one"] = (
            snapshot["schema_version"] == "1.0"
        )
        assertions["sprint_184"] = (
            snapshot["sprint"] == 184
        )
        assertions["route_count_nine"] = (
            snapshot["route_count"] == 9
        )
        assertions["panel_count_eight"] = (
            snapshot["panel_count"] == 8
        )
        assertions["routes_exact"] = (
            tuple(snapshot["routes"]) == self.ROUTES
        )
        assertions["panels_exact"] = (
            tuple(snapshot["panel_ids"])
            == self.PANEL_IDS
        )
        assertions["backend_read_only"] = (
            snapshot["read_only"] is True
        )
        assertions["mutation_false"] = (
            snapshot["mutation_allowed"] is False
        )
        assertions["frontend_false"] = (
            snapshot["frontend_rendered"] is False
        )
        assertions["listener_not_started"] = (
            snapshot["listener_started_by_backend"]
            is False
        )
        assertions["healthy_status"] = (
            snapshot["status"] == "ok"
        )
        assertions["healthy_not_degraded"] = (
            snapshot["degraded"] is False
        )
        assertions["healthy_error_zero"] = (
            snapshot["error_count"] == 0
        )
        assertions["foundation_expected_eight"] = (
            snapshot["foundations"]["expected_count"]
            == 8
        )
        assertions["foundation_available_eight"] = (
            snapshot["foundations"]["available_count"]
            == 8
        )
        assertions["foundation_all_available"] = (
            snapshot["foundations"]["all_available"]
            is True
        )
        assertions["foundation_runtime_false"] = (
            snapshot["foundations"]["runtime_activated"]
            is False
        )

        panels = snapshot["panels"]
        overview = panels["overview"]
        service = panels["service"]
        capabilities = panels["capabilities"]
        plugins = panels["plugins"]
        permissions = panels["permissions"]
        audit = panels["audit"]
        memory = panels["memory"]
        readiness = panels["readiness"]

        assertions['overview_version_189'] = (
            overview["identity"]["version"]
            == '0.190.0-genesis'
        )
        assertions["overview_boot_ready"] = (
            overview["core_boot_ready"] is True
        )
        assertions["overview_safe_idle"] = (
            overview["safe_idle"] is True
        )
        assertions["overview_service_stopped"] = (
            overview["service_state"] == "stopped"
        )
        assertions["overview_listener_false"] = (
            overview["listener_active"] is False
        )
        assertions['overview_capability_total_121'] = (
            overview["capability_total"] == 121
        )
        assertions['overview_online_119'] = (
            overview["online_capabilities"] == 119
        )
        assertions['overview_permission_gated_twelve'] = (
            overview[
                "permission_gated_capabilities"
            ]
            == 12
        )
        assertions['overview_runtime_feature_four'] = (
            overview["runtime_execution_features"]
            == 4
        )
        assertions["overview_plugins_two"] = (
            overview["plugin_available_count"] == 2
        )
        assertions["overview_read_only"] = (
            overview["read_only"] is True
        )
        assertions["overview_actions_false"] = (
            overview["actions_allowed"] is False
        )

        assertions["service_stopped"] = (
            service["state"] == "stopped"
        )
        assertions["service_listener_false"] = (
            service["listener_active"] is False
        )
        assertions["service_controls_false"] = (
            service["start_control_enabled"] is False
            and service["stop_control_enabled"] is False
            and service["restart_control_enabled"] is False
        )
        assertions["service_systemd_false"] = (
            service["systemd_control_enabled"] is False
        )
        assertions["service_auto_start_false"] = (
            service["auto_start_control_enabled"]
            is False
        )

        assertions['capability_card_count_121'] = (
            capabilities["card_count"] == 121
        )
        assertions['capability_summary_total_121'] = (
            capabilities["summary"][
                "total_capabilities"
            ]
            == 121
        )
        assertions["capability_mutation_false"] = (
            capabilities["mutation_enabled"] is False
        )
        assertions["all_capability_actions_false"] = all(
            card["actions_allowed"] is False
            for card in capabilities["cards"]
        )

        assertions["plugins_two_available"] = (
            plugins["available_count"] == 2
        )
        assertions["plugins_not_started"] = (
            plugins["plugins_started"] is False
        )
        assertions["plugin_controls_false"] = (
            plugins["install_enabled"] is False
            and plugins["enable_enabled"] is False
            and plugins["disable_enabled"] is False
            and plugins["reload_enabled"] is False
        )

        assertions["permission_foundation_available"] = (
            permissions["foundation_available"] is True
        )
        assertions['permission_gated_count_twelve'] = (
            permissions[
                "permission_gated_capability_count"
            ]
            == 12
        )
        assertions["pending_runtime_false"] = (
            permissions[
                "pending_request_runtime_active"
            ]
            is False
        )
        assertions["pending_count_unknown"] = (
            permissions["pending_request_count"]
            is None
        )
        assertions["decision_runtime_false"] = (
            permissions["decision_runtime_active"]
            is False
        )
        assertions["grant_runtime_false"] = (
            permissions["grant_runtime_active"]
            is False
        )
        assertions["scope_mutation_false"] = (
            permissions["scope_mutation_enabled"]
            is False
        )

        assertions["audit_foundation_available"] = (
            audit["foundation_available"] is True
        )
        assertions["audit_not_activated"] = (
            audit["status"] == "not_activated"
        )
        assertions["audit_writer_false"] = (
            audit["runtime_writer_active"] is False
        )
        assertions["audit_persistence_false"] = (
            audit["persistence_active"] is False
        )
        assertions["audit_fetch_false"] = (
            audit["runtime_event_fetch_active"]
            is False
        )
        assertions["audit_events_empty"] = (
            audit["runtime_event_count"] == 0
            and audit["events"] == []
        )

        assertions["memory_read_only"] = (
            memory["read_only"] is True
        )
        assertions["memory_no_write_probe"] = (
            memory["writable_probe_performed"]
            is False
        )
        assertions["memory_no_mutation"] = (
            memory["mutation_performed"] is False
        )
        assertions["memory_controls_false"] = (
            memory["create_enabled"] is False
            and memory["edit_enabled"] is False
            and memory["delete_enabled"] is False
            and memory["pin_enabled"] is False
        )

        assertions["readiness_backend_ready"] = (
            readiness["backend_ready"] is True
        )
        assertions['readiness_visibility_true'] = (
            readiness["permission_audit_recovery_visibility_ready"] is True
        )
        assertions["readiness_runtime_false"] = (
            readiness["interaction_runtime_ready"]
            is False
        )
        assertions["readiness_execution_false"] = (
            readiness["execution_ready"] is False
        )
        assertions['readiness_next_sprint_191'] = (
            readiness["next_sprint"]
            == "Sprint 191 — Voice Runtime Activation Foundation"
        )

        for route in self.ROUTES:
            payload = self.payload_for_route(
                route,
                snapshot=snapshot,
            )
            assertions[
                "route_"
                + route.replace("/", "_").strip("_")
            ] = isinstance(payload, dict)

        unknown_blocked = False
        try:
            self.payload_for_route(
                "/api/control-center/unknown",
                snapshot=snapshot,
            )
        except KeyError:
            unknown_blocked = True
        assertions["unknown_route_blocked"] = (
            unknown_blocked
        )

        boundary = self.safety_boundary()
        assertions["boundary_backend_true"] = (
            boundary["control_center_backend_runtime"]
            is True
        )
        assertions["boundary_route_nine"] = (
            boundary["backend_route_count"] == 9
        )
        assertions["boundary_panel_eight"] = (
            boundary["backend_panel_count"] == 8
        )

        disabled_boundary_keys = (
                                     'browser_launch_runtime',
                                     'backend_mutation_runtime',
                                     'service_control_runtime',
                                     'plugin_control_runtime',
                                     'permission_decision_runtime',
                                     'permission_grant_runtime',
                                     'permission_deny_runtime',
                                     'audit_writer_runtime',
                                     'audit_persistence_runtime',
                                     'memory_write_runtime',
                                     'chat_runtime',
                                     'model_runtime',
                                     'command_execution',
                                     'tool_execution',
                                     'action_dispatch',
                                     'background_service_runtime',
                                     'systemd_runtime',
                                     'automatic_start_runtime',
                                     'public_listener_runtime',
                                     'lan_listener_runtime',
                                     'autonomous_action',
                                 )
        assertions["boundary_frontend_true"] = (
            boundary["frontend_runtime"] is True
        )
        assertions["boundary_static_delivery_true"] = (
            boundary["static_file_serving_runtime"] is True
        )

        for key in disabled_boundary_keys:
            assertions[
                "boundary_disabled_" + key
            ] = boundary[key] is False

        assertions["watched_files_unchanged"] = (
            before == after
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s184-degraded-"
        ) as temporary:
            degraded_root = Path(temporary)
            degraded_manager = (
                AuraControlCenterBackendRuntimeManager(
                    project_root=degraded_root,
                    capability_manager=(
                        self.capability_manager
                    ),
                    clock=self._clock,
                )
            )
            degraded = degraded_manager.snapshot()

            assertions["degraded_fixture_visible"] = (
                degraded["degraded"] is True
            )
            assertions["degraded_status_visible"] = (
                degraded["status"] == "degraded"
            )
            assertions["degraded_has_errors"] = (
                degraded["error_count"] >= 2
            )
            assertions["degraded_overview_visible"] = (
                degraded["panels"]["overview"][
                    "status"
                ]
                == "degraded"
            )
            assertions["degraded_readiness_visible"] = (
                degraded["panels"]["readiness"][
                    "status"
                ]
                == "degraded"
            )
            assertions["degraded_no_memory_created"] = (
                not degraded_manager.memory_file.exists()
            )
            assertions["degraded_no_settings_created"] = (
                not degraded_manager.settings_path.exists()
            )
            assertions["degraded_listener_false"] = (
                degraded[
                    "listener_started_by_backend"
                ]
                is False
            )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise ControlCenterBackendError(
                "Control Center backend self-test failed: "
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
            "panel_count": len(self.PANEL_IDS),
            "routes": list(self.ROUTES),
            "panel_ids": list(self.PANEL_IDS),
            "foundation_contract_count": len(
                self.FOUNDATION_MODULES
            ),
            "foundation_contracts_available": 8,
            "capability_card_count": 121,
            "degraded_fixture_verified": True,
            "read_only_file_integrity_verified": True,
            "frontend_rendered": False,
            "listener_started_by_backend": False,
            "mutation_performed": False,
        }
