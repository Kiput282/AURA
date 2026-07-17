"""Sprint 266 read-only Control Center runtime aggregator.

The aggregator composes existing runtime status contracts into a bounded
operational summary. It does not expose action routes, raw log content,
arbitrary file paths, secrets, model activation, permission mutation,
recovery execution, or durable memory writes.
"""

from __future__ import annotations

from copy import deepcopy
from importlib import import_module
from inspect import signature
from pathlib import Path
from typing import Any


class ControlCenterRuntimeUxConsolidationError(
    RuntimeError
):
    """Sprint 266 aggregator contract error."""


class ControlCenterRuntimeUxConsolidationRuntimeManager:
    """Aggregate existing runtime visibility without new authority."""

    name = "control_center_runtime_ux_consolidation"
    component_version = "0.1.0-alpha"
    schema_version = "1.0"
    sprint = 266

    CHAT_DESTINATION = "/chat"

    OWNER_SPECS = {
        "service": {
            "module": (
                "aura.manual_start_stop_status_runtime."
                "manual_start_stop_status_runtime_executor"
            ),
            "class": "ManualStartStopStatusRuntimeExecutor",
            "methods": ("status",),
            "kwargs": {"probe_health": False},
        },
        "restart_logs": {
            "module": (
                "aura.restart_logs_failure_visibility."
                "restart_logs_failure_visibility_alpha_manager"
            ),
            "class": "RestartLogsFailureVisibilityAlphaManager",
            "methods": (
                "product_status",
                "status",
                "runtime_status",
            ),
            "kwargs": {},
        },
        "model_runtime": {
            "module": (
                "aura.model_loading_unloading_queue_resource_budgets."
                "model_lifecycle_queue_budget_alpha_manager"
            ),
            "class": "ModelLifecycleQueueBudgetAlphaManager",
            "methods": (
                "status",
                "product_status",
                "runtime_status",
            ),
            "kwargs": {},
        },
        "visibility": {
            "module": (
                "aura.permission_audit_recovery_visibility_runtime."
                "aura_permission_audit_recovery_visibility_runtime_manager"
            ),
            "class": (
                "AuraPermissionAuditRecoveryVisibilityRuntimeManager"
            ),
            "methods": ("status", "visibility_snapshot"),
            "kwargs": {},
        },
        "memory_review": {
            "module": (
                "aura.review_first_memory_integration."
                "review_first_memory_integration_runtime_manager"
            ),
            "class": (
                "ReviewFirstMemoryIntegrationRuntimeManager"
            ),
            "methods": ("status", "list_candidates"),
            "kwargs": {},
        },
    }

    BLOCKED_KEY_PARTS = (
        "authorization",
        "credential",
        "secret",
        "token",
        "password",
        "api_key",
        "raw_value",
        "raw_values",
        "environment",
        "command",
        "argv",
        "stdout",
        "stderr",
        "log_content",
        "log_lines",
        "log_tail",
        "file_content",
        "message_content",
        "response_content",
    )

    PATH_KEY_PARTS = (
        "log_path",
        "file_path",
        "socket_path",
        "pid_file",
        "project_root",
        "storage_dir",
    )

    MAX_LIST_ITEMS = 32
    MAX_DEPTH = 8

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    @classmethod
    def _blocked_key(cls, key: str) -> bool:
        lowered = str(key).lower()
        return any(
            part in lowered
            for part in cls.BLOCKED_KEY_PARTS
        )

    @classmethod
    def _path_key(cls, key: str) -> bool:
        lowered = str(key).lower()
        return any(
            part in lowered
            for part in cls.PATH_KEY_PARTS
        )

    @classmethod
    def _sanitize(
        cls,
        value: Any,
        *,
        depth: int = 0,
    ) -> Any:
        if depth > cls.MAX_DEPTH:
            return "[bounded]"

        if value is None or isinstance(
            value,
            (bool, int, float),
        ):
            return value

        if isinstance(value, str):
            return value[:320]

        if isinstance(value, dict):
            clean: dict[str, Any] = {}
            for key, item in value.items():
                key_text = str(key)
                if cls._blocked_key(key_text):
                    continue
                if cls._path_key(key_text):
                    clean["bounded_sensitive_paths_exposed"] = False
                    continue
                clean[key_text] = cls._sanitize(
                    item,
                    depth=depth + 1,
                )
            return clean

        if isinstance(value, (list, tuple, set)):
            items = list(value)[: cls.MAX_LIST_ITEMS]
            return [
                cls._sanitize(
                    item,
                    depth=depth + 1,
                )
                for item in items
            ]

        return str(value)[:160]

    @staticmethod
    def _resolve_class(
        module: Any,
        preferred_name: str,
    ) -> type[Any]:
        preferred = getattr(
            module,
            preferred_name,
            None,
        )
        if isinstance(preferred, type):
            return preferred

        candidates = [
            value
            for value in vars(module).values()
            if isinstance(value, type)
            and value.__module__ == module.__name__
            and (
                value.__name__.endswith("Manager")
                or value.__name__.endswith("Executor")
            )
        ]
        if len(candidates) != 1:
            raise ControlCenterRuntimeUxConsolidationError(
                "Unable to resolve runtime owner class for "
                + module.__name__
            )
        return candidates[0]

    def _construct(
        self,
        owner_class: type[Any],
    ) -> Any:
        parameters = signature(
            owner_class
        ).parameters
        if "project_root" in parameters:
            return owner_class(
                project_root=self.project_root
            )
        return owner_class()

    @staticmethod
    def _call_method(
        owner: Any,
        method_names: tuple[str, ...],
        kwargs: dict[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        for method_name in method_names:
            method = getattr(
                owner,
                method_name,
                None,
            )
            if not callable(method):
                continue

            parameters = signature(
                method
            ).parameters
            accepted = {
                key: value
                for key, value in kwargs.items()
                if key in parameters
            }
            result = method(**accepted)
            if isinstance(result, dict):
                return method_name, result

        raise ControlCenterRuntimeUxConsolidationError(
            "No compatible read-only status method was found."
        )

    def _owner_snapshot(
        self,
        owner_id: str,
    ) -> dict[str, Any]:
        spec = self.OWNER_SPECS[owner_id]
        module = import_module(spec["module"])
        owner_class = self._resolve_class(
            module,
            spec["class"],
        )
        owner = self._construct(owner_class)
        method_name, payload = self._call_method(
            owner,
            tuple(spec["methods"]),
            dict(spec["kwargs"]),
        )
        sanitized = self._sanitize(payload)

        return {
            "owner_id": owner_id,
            "owner_module": spec["module"],
            "owner_class": owner_class.__name__,
            "source_method": method_name,
            "status": (
                sanitized.get("status", "available")
                if isinstance(sanitized, dict)
                else "available"
            ),
            "available": True,
            "degraded": (
                bool(sanitized.get("degraded", False))
                if isinstance(sanitized, dict)
                else False
            ),
            "snapshot": sanitized,
            "read_only": True,
            "runtime_mutated": False,
        }

    def _safe_owner_snapshot(
        self,
        owner_id: str,
    ) -> dict[str, Any]:
        try:
            return self._owner_snapshot(owner_id)
        except Exception as exc:
            return {
                "owner_id": owner_id,
                "status": "degraded",
                "available": False,
                "degraded": True,
                "detail": (
                    type(exc).__name__
                    + ": "
                    + str(exc)[:240]
                ),
                "snapshot": {},
                "read_only": True,
                "runtime_mutated": False,
            }

    def operations_snapshot(
        self,
    ) -> dict[str, Any]:
        service = self._safe_owner_snapshot(
            "service"
        )
        restart_logs = self._safe_owner_snapshot(
            "restart_logs"
        )
        model_runtime = self._safe_owner_snapshot(
            "model_runtime"
        )
        visibility = self._safe_owner_snapshot(
            "visibility"
        )
        memory_review = self._safe_owner_snapshot(
            "memory_review"
        )

        owners = {
            item["owner_id"]: item
            for item in (
                service,
                restart_logs,
                model_runtime,
                visibility,
                memory_review,
            )
        }
        available_count = sum(
            item["available"]
            for item in owners.values()
        )
        degraded_count = sum(
            item["degraded"]
            for item in owners.values()
        )

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": (
                "ready"
                if available_count == len(owners)
                else "degraded"
            ),
            "degraded": degraded_count > 0,
            "owner_count": len(owners),
            "available_owner_count": available_count,
            "degraded_owner_count": degraded_count,
            "owners": owners,
            "chat": {
                "workspace_route": self.CHAT_DESTINATION,
                "embedded": False,
                "available": True,
                "description": (
                    "Open the existing full browser chat workspace."
                ),
            },
            "service_controls": {
                "status_visible": True,
                "start_action_route": False,
                "stop_action_route": False,
                "restart_action_route": False,
                "explicit_existing_runtime_confirmation_preserved": True,
            },
            "logs": {
                "failure_metadata_visible": True,
                "bounded_metadata_only": True,
                "raw_log_content_visible": False,
                "arbitrary_log_file_read": False,
                "sensitive_paths_exposed": False,
            },
            "model_runtime": {
                "queue_and_budget_visibility": True,
                "activation_route": False,
                "implicit_model_activation": False,
                "model_request_executed": False,
            },
            "visibility": {
                "permission_read_only": True,
                "audit_read_only": True,
                "recovery_read_only": True,
                "permission_grant_route": False,
                "recovery_execution_route": False,
            },
            "memory_review": {
                "summary_visible": True,
                "workspace_route": "/chat",
                "candidate_persistence": False,
                "review_queue_persistence": False,
                "durable_memory_write": False,
                "memory_store_mutation": False,
            },
            "new_execution_authority": False,
            "service_action_routes": False,
            "restart_action_routes": False,
            "model_activation_route": False,
            "permission_grant_route": False,
            "recovery_execution_route": False,
            "memory_write_route": False,
            "automatic_service_start": False,
            "automatic_model_activation": False,
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "automatic_memory_write": False,
            "network_fallback": False,
            "browser_auto_launch": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        snapshot = self.operations_snapshot()
        return {
            key: deepcopy(value)
            for key, value in snapshot.items()
            if key != "owners"
        }

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "read_only_runtime_aggregation": True,
            "existing_control_center_shell_owner": True,
            "existing_control_center_backend_owner": True,
            "chat_link_only": True,
            "chat_embedded": False,
            "new_execution_authority": False,
            "service_action_routes": False,
            "restart_action_routes": False,
            "arbitrary_log_content_read": False,
            "bounded_log_metadata_only": True,
            "model_activation_route": False,
            "permission_grant_route": False,
            "recovery_execution_route": False,
            "memory_write_route": False,
            "automatic_service_start": False,
            "automatic_model_activation": False,
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "automatic_memory_write": False,
            "network_fallback": False,
            "browser_auto_launch": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    @classmethod
    def _contains_blocked_key(
        cls,
        value: Any,
    ) -> bool:
        if isinstance(value, dict):
            for key, item in value.items():
                if cls._blocked_key(str(key)):
                    return True
                if cls._path_key(str(key)):
                    return True
                if cls._contains_blocked_key(item):
                    return True
            return False
        if isinstance(value, list):
            return any(
                cls._contains_blocked_key(item)
                for item in value
            )
        return False

    def self_test(self) -> dict[str, Any]:
        snapshot = self.operations_snapshot()
        status = self.status()
        safety = self.safety_boundary()

        assertions = {
            "snapshot_name": (
                snapshot["name"] == self.name
            ),
            "snapshot_sprint": (
                snapshot["sprint"] == 266
            ),
            "owner_count_five": (
                snapshot["owner_count"] == 5
            ),
            "owners_present": (
                set(snapshot["owners"])
                == set(self.OWNER_SPECS)
            ),
            "chat_route": (
                snapshot["chat"]["workspace_route"]
                == "/chat"
            ),
            "chat_not_embedded": (
                snapshot["chat"]["embedded"] is False
            ),
            "service_status_visible": (
                snapshot["service_controls"][
                    "status_visible"
                ]
                is True
            ),
            "service_start_route_false": (
                snapshot["service_controls"][
                    "start_action_route"
                ]
                is False
            ),
            "service_stop_route_false": (
                snapshot["service_controls"][
                    "stop_action_route"
                ]
                is False
            ),
            "service_restart_route_false": (
                snapshot["service_controls"][
                    "restart_action_route"
                ]
                is False
            ),
            "bounded_log_metadata": (
                snapshot["logs"][
                    "bounded_metadata_only"
                ]
                is True
            ),
            "raw_logs_false": (
                snapshot["logs"][
                    "raw_log_content_visible"
                ]
                is False
            ),
            "arbitrary_log_read_false": (
                snapshot["logs"][
                    "arbitrary_log_file_read"
                ]
                is False
            ),
            "log_path_false": (
                snapshot["logs"][
                    "sensitive_paths_exposed"
                ]
                is False
            ),
            "queue_visible": (
                snapshot["model_runtime"][
                    "queue_and_budget_visibility"
                ]
                is True
            ),
            "model_activation_false": (
                snapshot["model_runtime"][
                    "activation_route"
                ]
                is False
            ),
            "permission_read_only": (
                snapshot["visibility"][
                    "permission_read_only"
                ]
                is True
            ),
            "audit_read_only": (
                snapshot["visibility"][
                    "audit_read_only"
                ]
                is True
            ),
            "recovery_read_only": (
                snapshot["visibility"][
                    "recovery_read_only"
                ]
                is True
            ),
            "permission_grant_false": (
                snapshot["visibility"][
                    "permission_grant_route"
                ]
                is False
            ),
            "memory_summary_visible": (
                snapshot["memory_review"][
                    "summary_visible"
                ]
                is True
            ),
            "memory_persistence_false": (
                snapshot["memory_review"][
                    "candidate_persistence"
                ]
                is False
            ),
            "memory_write_false": (
                snapshot["memory_review"][
                    "durable_memory_write"
                ]
                is False
            ),
            "memory_store_false": (
                snapshot["memory_review"][
                    "memory_store_mutation"
                ]
                is False
            ),
            "new_authority_false": (
                snapshot["new_execution_authority"]
                is False
            ),
            "runtime_mutated_false": (
                snapshot["runtime_mutated"] is False
            ),
            "safe_idle_true": (
                snapshot["safe_idle"] is True
            ),
            "bounded_path_marker_safe": (
                all(
                    (
                        owner["snapshot"].get(
                            "bounded_sensitive_paths_exposed",
                            False,
                        )
                        is False
                    )
                    for owner in snapshot["owners"].values()
                )
            ),
            "blocked_keys_absent": (
                all(
                    self._contains_blocked_key(
                        owner["snapshot"]
                    )
                    is False
                    for owner in snapshot["owners"].values()
                )
            ),
            "aggregate_boundary_labels_visible": (
                snapshot["logs"][
                    "raw_log_content_visible"
                ]
                is False
                and snapshot["logs"][
                    "arbitrary_log_file_read"
                ]
                is False
            ),
            "status_owners_omitted": (
                "owners" not in status
            ),
            "safety_read_only": (
                safety[
                    "read_only_runtime_aggregation"
                ]
                is True
            ),
            "safety_action_false": (
                safety["service_action_routes"]
                is False
            ),
            "safety_restart_false": (
                safety["restart_action_routes"]
                is False
            ),
            "safety_model_false": (
                safety["model_activation_route"]
                is False
            ),
            "safety_permission_false": (
                safety["permission_grant_route"]
                is False
            ),
            "safety_recovery_false": (
                safety["recovery_execution_route"]
                is False
            ),
            "safety_memory_false": (
                safety["memory_write_route"]
                is False
            ),
            "safety_network_false": (
                safety["network_fallback"]
                is False
            ),
            "safety_idle_true": (
                safety["safe_idle"] is True
            ),
        }

        failed = [
            name
            for name, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise ControlCenterRuntimeUxConsolidationError(
                "Sprint 266 aggregator self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "owner_count": snapshot["owner_count"],
            "available_owner_count": snapshot[
                "available_owner_count"
            ],
            "degraded_owner_count": snapshot[
                "degraded_owner_count"
            ],
            "new_execution_authority": False,
            "service_action_routes": False,
            "restart_action_routes": False,
            "arbitrary_log_content_read": False,
            "bounded_log_metadata_only": True,
            "model_activation_route": False,
            "permission_grant_route": False,
            "recovery_execution_route": False,
            "memory_write_route": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }
