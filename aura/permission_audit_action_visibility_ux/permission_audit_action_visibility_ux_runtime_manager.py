from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from aura.permission_audit_recovery_visibility_runtime.aura_permission_audit_recovery_visibility_runtime_manager import (
    AuraPermissionAuditRecoveryVisibilityRuntimeManager,
)
from aura.permissions.active_permission_runtime_planner import (
    ActivePermissionRuntimePlanner,
)


class PermissionAuditActionVisibilityUxError(
    RuntimeError
):
    """Raised when the Sprint 268 facade fails validation."""


class PermissionAuditActionVisibilityUxRuntimeManager:
    """Compose existing permission/audit/action visibility read-only."""

    VERSION = "1.2.8"
    ANCHOR_VERSION = "1.2.7"
    CURRENT_SPRINT = 268
    NEXT_SPRINT = 269
    BOUNDARY = "permission_audit_action_visibility_ux"
    NEXT_BOUNDARY = (
        "daily_use_acceptance_rehearsal_and_release_harness"
    )
    SECTION_IDS = (
        "permission",
        "audit",
        "proposal",
        "approval",
        "action",
        "recovery",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()
        self.environment = (
            dict(environment)
            if environment is not None
            else None
        )
        self._permission_planner = (
            ActivePermissionRuntimePlanner(
                project_root=self.project_root
            )
        )
        self._visibility_runtime = (
            AuraPermissionAuditRecoveryVisibilityRuntimeManager(
                environment=self.environment
            )
        )

    @staticmethod
    def _dict(
        value: Any,
    ) -> dict[str, Any]:
        return (
            value
            if isinstance(value, dict)
            else {}
        )

    @staticmethod
    def _bool(
        value: Any,
    ) -> bool:
        return value is True

    @staticmethod
    def _int(
        value: Any,
    ) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

    @classmethod
    def _json_safe(
        cls,
        value: Any,
    ) -> Any:
        if isinstance(value, dict):
            return {
                str(key): cls._json_safe(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [
                cls._json_safe(item)
                for item in value
            ]
        if value is None or isinstance(
            value,
            (str, int, float, bool),
        ):
            return value
        return repr(value)

    @staticmethod
    def _section(
        section_id: str,
        title: str,
        state: str,
        detail: str,
        *,
        visible: bool = True,
        source: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "section_id": section_id,
            "title": title,
            "state": state,
            "detail": detail,
            "visible": visible,
            "source": source or {},
            "actions_allowed": False,
            "mutation_allowed": False,
            "read_only": True,
            "safe_idle": True,
        }

    def snapshot(
        self,
        *,
        permission_panel: dict[str, Any] | None = None,
        audit_panel: dict[str, Any] | None = None,
        runtime_ux: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        permission = self._dict(permission_panel)
        audit = self._dict(audit_panel)
        operations = self._dict(runtime_ux)
        visibility = self._dict(
            operations.get("visibility")
        )

        planner_status = self._json_safe(
            self._permission_planner.status()
        )
        visibility_status = self._json_safe(
            self._visibility_runtime.status()
        )
        permission_owner = self._json_safe(
            self._visibility_runtime.permission_snapshot()
        )
        audit_owner = self._json_safe(
            self._visibility_runtime.audit_snapshot()
        )
        recovery_owner = self._json_safe(
            self._visibility_runtime.recovery_snapshot()
        )
        safety_owner = self._json_safe(
            self._visibility_runtime.safety_boundary()
        )

        pending_count = self._int(
            permission.get("pending_request_count")
        )
        permission_ready = (
            self._bool(
                permission.get("foundation_available")
            )
            and self._bool(
                permission.get("read_only")
            )
        )
        audit_ready = (
            self._bool(
                audit.get("foundation_available")
            )
            and self._bool(
                audit.get("read_only")
            )
        )

        automatic_permission_grant = self._bool(
            operations.get(
                "automatic_permission_grant"
            )
        )
        automatic_recovery = self._bool(
            operations.get("automatic_recovery")
        )
        permission_grant_route = self._bool(
            operations.get("permission_grant_route")
        )
        recovery_execution_route = self._bool(
            operations.get(
                "recovery_execution_route"
            )
        )
        service_action_routes = self._bool(
            operations.get("service_action_routes")
        )
        restart_action_routes = self._bool(
            operations.get("restart_action_routes")
        )

        proposal_state = (
            "pending_review"
            if pending_count > 0
            else "idle"
        )
        approval_state = (
            "manual_review_required"
            if pending_count > 0
            else "manual_only"
        )
        action_routes_exposed = (
            service_action_routes
            or restart_action_routes
            or permission_grant_route
        )

        sections = {
            "permission": self._section(
                "permission",
                "Permission",
                (
                    "visible"
                    if permission_ready
                    else "degraded"
                ),
                (
                    "Permission counts and runtime state are "
                    "visible without grant controls."
                ),
                source={
                    "status": permission.get("status"),
                    "foundation_status": permission.get(
                        "foundation_status"
                    ),
                    "pending_request_count": pending_count,
                    "permission_gated_capability_count":
                    self._int(
                        permission.get(
                            "permission_gated_capability_count"
                        )
                    ),
                    "declared_permission_counts":
                    self._json_safe(
                        permission.get(
                            "declared_permission_counts",
                            {},
                        )
                    ),
                    "decision_runtime_active":
                    self._bool(
                        permission.get(
                            "decision_runtime_active"
                        )
                    ),
                    "grant_runtime_active":
                    self._bool(
                        permission.get(
                            "grant_runtime_active"
                        )
                    ),
                    "deny_runtime_active":
                    self._bool(
                        permission.get(
                            "deny_runtime_active"
                        )
                    ),
                    "planner": planner_status,
                    "owner": permission_owner,
                },
            ),
            "audit": self._section(
                "audit",
                "Audit",
                (
                    "visible"
                    if audit_ready
                    else "degraded"
                ),
                (
                    "Audit state and bounded event metadata "
                    "are visible without writer activation."
                ),
                source={
                    "status": audit.get("status"),
                    "event_state": audit.get("event_state"),
                    "runtime_event_count": self._int(
                        audit.get("runtime_event_count")
                    ),
                    "runtime_writer_active":
                    self._bool(
                        audit.get(
                            "runtime_writer_active"
                        )
                    ),
                    "runtime_event_fetch_active":
                    self._bool(
                        audit.get(
                            "runtime_event_fetch_active"
                        )
                    ),
                    "persistence_active":
                    self._bool(
                        audit.get("persistence_active")
                    ),
                    "events": self._json_safe(
                        audit.get("events", [])
                    ),
                    "owner": audit_owner,
                },
            ),
            "proposal": self._section(
                "proposal",
                "Proposal",
                proposal_state,
                (
                    f"{pending_count} pending request(s); "
                    "proposal visibility does not execute a "
                    "decision."
                ),
                source={
                    "pending_request_count": pending_count,
                    "pending_request_runtime_active":
                    self._bool(
                        permission.get(
                            "pending_request_runtime_active"
                        )
                    ),
                    "decision_runtime_active":
                    self._bool(
                        permission.get(
                            "decision_runtime_active"
                        )
                    ),
                },
            ),
            "approval": self._section(
                "approval",
                "Approval",
                approval_state,
                (
                    "Approval remains manual-only; no "
                    "automatic grant route is exposed."
                ),
                source={
                    "automatic_permission_grant":
                    automatic_permission_grant,
                    "permission_grant_route":
                    permission_grant_route,
                    "permission_read_only":
                    self._bool(
                        visibility.get(
                            "permission_read_only"
                        )
                    ),
                },
            ),
            "action": self._section(
                "action",
                "Action",
                (
                    "route_visible"
                    if action_routes_exposed
                    else "not_exposed"
                ),
                (
                    "Action-route state is visible, but this "
                    "facade provides no execution control."
                ),
                source={
                    "service_action_routes":
                    service_action_routes,
                    "restart_action_routes":
                    restart_action_routes,
                    "permission_grant_route":
                    permission_grant_route,
                    "actions_allowed":
                    self._bool(
                        permission.get("actions_allowed")
                    )
                    or self._bool(
                        audit.get("actions_allowed")
                    ),
                },
            ),
            "recovery": self._section(
                "recovery",
                "Recovery",
                (
                    "read_only"
                    if self._bool(
                        visibility.get(
                            "recovery_read_only"
                        )
                    )
                    else "degraded"
                ),
                (
                    "Recovery state is visible without "
                    "automatic or route-based execution."
                ),
                source={
                    "automatic_recovery":
                    automatic_recovery,
                    "recovery_execution_route":
                    recovery_execution_route,
                    "recovery_read_only":
                    self._bool(
                        visibility.get(
                            "recovery_read_only"
                        )
                    ),
                    "owner": recovery_owner,
                },
            ),
        }

        ready_count = sum(
            1
            for section in sections.values()
            if section["state"] not in {
                "degraded",
            }
        )

        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "status": (
                "available"
                if permission_ready and audit_ready
                else "degraded"
            ),
            "section_count": len(sections),
            "available_section_count": ready_count,
            "sections": sections,
            "permission_owner": (
                "ActivePermissionRuntimePlanner"
            ),
            "visibility_owner": (
                "AuraPermissionAuditRecoveryVisibilityRuntimeManager"
            ),
            "visibility_status": visibility_status,
            "safety_owner": safety_owner,
            "automatic_permission_grant":
            automatic_permission_grant,
            "automatic_recovery": automatic_recovery,
            "permission_grant_route":
            permission_grant_route,
            "recovery_execution_route":
            recovery_execution_route,
            "service_action_routes":
            service_action_routes,
            "restart_action_routes":
            restart_action_routes,
            "new_http_route": False,
            "mutation_routes": False,
            "background_worker_enabled": False,
            "external_dependency_added": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(
        self,
        *,
        permission_panel: dict[str, Any] | None = None,
        audit_panel: dict[str, Any] | None = None,
        runtime_ux: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        snapshot = self.snapshot(
            permission_panel=permission_panel,
            audit_panel=audit_panel,
            runtime_ux=runtime_ux,
        )
        return {
            "version": snapshot["version"],
            "current_sprint":
            snapshot["current_sprint"],
            "boundary": snapshot["boundary"],
            "status": snapshot["status"],
            "section_count":
            snapshot["section_count"],
            "read_only": True,
            "safe_idle": True,
        }

    def context(
        self,
        *,
        permission_panel: dict[str, Any] | None = None,
        audit_panel: dict[str, Any] | None = None,
        runtime_ux: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        snapshot = self.snapshot(
            permission_panel=permission_panel,
            audit_panel=audit_panel,
            runtime_ux=runtime_ux,
        )
        return {
            "version": snapshot["version"],
            "current_sprint":
            snapshot["current_sprint"],
            "next_sprint":
            snapshot["next_sprint"],
            "boundary": snapshot["boundary"],
            "next_boundary":
            snapshot["next_boundary"],
            "section_ids": list(
                snapshot["sections"]
            ),
            "read_only": True,
            "safe_idle": True,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        return self.self_test()

    def self_test(
        self,
    ) -> dict[str, Any]:
        fixture_permission = {
            "status": "not_activated",
            "foundation_available": True,
            "foundation_status": "online",
            "pending_request_count": 2,
            "permission_gated_capability_count": 27,
            "declared_permission_counts": {
                None: 1,
                "file_write_permission": 2,
            },
            "decision_runtime_active": False,
            "grant_runtime_active": False,
            "deny_runtime_active": False,
            "pending_request_runtime_active": False,
            "scope_mutation_enabled": False,
            "actions_allowed": False,
            "read_only": True,
        }
        fixture_audit = {
            "status": "not_activated",
            "foundation_available": True,
            "foundation_status": "online",
            "event_state": "no_runtime_audit_writer",
            "events": [],
            "runtime_event_count": 0,
            "runtime_event_fetch_active": False,
            "runtime_writer_active": False,
            "persistence_active": False,
            "actions_allowed": False,
            "read_only": True,
        }
        fixture_operations = {
            "visibility": {
                "audit_read_only": True,
                "permission_grant_route": False,
                "permission_read_only": True,
                "recovery_execution_route": False,
                "recovery_read_only": True,
            },
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "permission_grant_route": False,
            "recovery_execution_route": False,
            "restart_action_routes": False,
            "service_action_routes": False,
        }

        snapshot = self.snapshot(
            permission_panel=fixture_permission,
            audit_panel=fixture_audit,
            runtime_ux=fixture_operations,
        )

        assertions: dict[str, bool] = {
            "version": snapshot["version"] == "1.2.8",
            "anchor_version":
            snapshot["anchor_version"] == "1.2.7",
            "current_sprint":
            snapshot["current_sprint"] == 268,
            "next_sprint":
            snapshot["next_sprint"] == 269,
            "boundary":
            snapshot["boundary"]
            == "permission_audit_action_visibility_ux",
            "next_boundary":
            snapshot["next_boundary"]
            == "daily_use_acceptance_rehearsal_and_release_harness",
            "section_count":
            snapshot["section_count"] == 6,
            "read_only":
            snapshot["read_only"] is True,
            "safe_idle":
            snapshot["safe_idle"] is True,
            "new_execution_authority_false":
            snapshot["new_execution_authority"]
            is False,
            "new_http_route_false":
            snapshot["new_http_route"] is False,
            "runtime_mutated_false":
            snapshot["runtime_mutated"] is False,
        }

        for section_id in self.SECTION_IDS:
            section = snapshot["sections"][section_id]
            assertions[
                f"{section_id}_dict"
            ] = isinstance(section, dict)
            assertions[
                f"{section_id}_identity"
            ] = section["section_id"] == section_id
            assertions[
                f"{section_id}_title"
            ] = isinstance(section["title"], str)
            assertions[
                f"{section_id}_visible"
            ] = section["visible"] is True
            assertions[
                f"{section_id}_state"
            ] = isinstance(section["state"], str)
            assertions[
                f"{section_id}_read_only"
            ] = section["read_only"] is True
            assertions[
                f"{section_id}_actions_false"
            ] = section["actions_allowed"] is False
            assertions[
                f"{section_id}_mutation_false"
            ] = section["mutation_allowed"] is False

        failed = [
            name
            for name, passed in assertions.items()
            if not passed
        ]
        if len(assertions) != 60:
            raise PermissionAuditActionVisibilityUxError(
                "Sprint 268 runtime self-test must contain "
                f"60 assertions, found {len(assertions)}."
            )
        if failed:
            raise PermissionAuditActionVisibilityUxError(
                "Sprint 268 runtime self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "section_count": len(self.SECTION_IDS),
            "new_http_route": False,
            "mutation_routes": False,
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }
