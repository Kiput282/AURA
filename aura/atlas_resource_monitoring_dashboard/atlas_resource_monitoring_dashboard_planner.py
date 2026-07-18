from __future__ import annotations

from pathlib import Path
from typing import Any

from .atlas_resource_monitoring_dashboard_contract import (
    AtlasResourceMonitoringDashboardContract,
)
from .atlas_resource_monitoring_dashboard_runtime_manager import (
    AtlasResourceMonitoringDashboardRuntimeManager,
)


class AtlasResourceMonitoringDashboardPlanner:
    VERSION = "1.2.7"
    CURRENT_SPRINT = 267
    NEXT_SPRINT = 268
    BOUNDARY = "atlas_resource_monitoring_dashboard"
    NEXT_BOUNDARY = "permission_audit_action_visibility_ux"

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def snapshot(
        self,
    ) -> dict[str, Any]:
        runtime = (
            AtlasResourceMonitoringDashboardRuntimeManager(
                project_root=self.project_root
            ).snapshot()
        )
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "mount_points": runtime["mount_points"],
            "sample_interval_seconds": runtime[
                "sample_interval_seconds"
            ],
            "ui_refresh_seconds": runtime[
                "ui_refresh_seconds"
            ],
            "rolling_windows_minutes": runtime[
                "rolling_windows_minutes"
            ],
            "history_sample_count": runtime[
                "history_sample_count"
            ],
            "background_sampler_enabled": False,
            "history_persistence_enabled": False,
            "new_http_route": False,
            "new_external_dependency": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        check = (
            AtlasResourceMonitoringDashboardContract(
                project_root=self.project_root
            ).check()
        )
        return {
            **self.snapshot(),
            "status": (
                "ready"
                if check["status_valid"]
                else "degraded"
            ),
            "status_valid": check[
                "status_valid"
            ],
            "alpha_ready": check["alpha_ready"],
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check[
                "dimension_count"
            ],
            "finding_count": check[
                "finding_count"
            ],
        }

    def context(
        self,
    ) -> dict[str, Any]:
        return {
            **self.status(),
            "scope": (
                "Expose read-only near-real-time ATLAS "
                "CPU, memory, swap, storage, uptime, "
                "process, and rolling-history metrics."
            ),
            "next_scope": self.NEXT_BOUNDARY,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        return (
            AtlasResourceMonitoringDashboardContract(
                project_root=self.project_root
            ).check()
        )
