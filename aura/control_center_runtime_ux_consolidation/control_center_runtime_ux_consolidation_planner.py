"""Sprint 266 Control Center runtime UX consolidation planner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .control_center_runtime_ux_consolidation_contract import (
    ControlCenterRuntimeUxConsolidationContract,
)
from .control_center_runtime_ux_consolidation_runtime_manager import (
    ControlCenterRuntimeUxConsolidationRuntimeManager,
)


class ControlCenterRuntimeUxConsolidationPlanner:
    VERSION = "1.2.6"
    CURRENT_SPRINT = 266
    NEXT_SPRINT = 267
    BOUNDARY = "control_center_runtime_ux_consolidation"
    NEXT_BOUNDARY = "atlas_resource_monitoring_dashboard"

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def snapshot(self) -> dict[str, Any]:
        runtime = ControlCenterRuntimeUxConsolidationRuntimeManager(
            project_root=self.project_root
        ).operations_snapshot()
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "primary_interface": "browser_control_center",
            "shell_owner": "control_center_web_shell_runtime",
            "backend_owner": "control_center_backend_runtime",
            "chat_destination": "/chat",
            "chat_embedding": False,
            "owner_count": runtime["owner_count"],
            "available_owner_count": runtime[
                "available_owner_count"
            ],
            "degraded_owner_count": runtime[
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
            "automatic_service_start": False,
            "automatic_model_activation": False,
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "automatic_memory_write": False,
            "network_fallback": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        check = ControlCenterRuntimeUxConsolidationContract(
            project_root=self.project_root
        ).check()
        return {
            **self.snapshot(),
            "status": (
                "ready"
                if check["status_valid"]
                else "degraded"
            ),
            "status_valid": check["status_valid"],
            "alpha_ready": check["alpha_ready"],
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check["dimension_count"],
            "finding_count": check["finding_count"],
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "scope": (
                "Consolidate existing service, logs, model, queue, "
                "chat, visibility, and memory-review UX."
            ),
            "next_scope": (
                "Add near-real-time ATLAS resource monitoring."
            ),
        }

    def check(self) -> dict[str, Any]:
        return ControlCenterRuntimeUxConsolidationContract(
            project_root=self.project_root
        ).check()
