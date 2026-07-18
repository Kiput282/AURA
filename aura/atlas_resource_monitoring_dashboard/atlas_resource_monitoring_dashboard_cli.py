from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

from .atlas_resource_monitoring_dashboard_contract import (
    AtlasResourceMonitoringDashboardContract,
)
from .atlas_resource_monitoring_dashboard_planner import (
    AtlasResourceMonitoringDashboardPlanner,
)
from .atlas_resource_monitoring_dashboard_runtime_manager import (
    AtlasResourceMonitoringDashboardRuntimeManager,
)


class AtlasResourceMonitoringDashboardCLI:
    COMMANDS = (
        "atlas-resource-monitoring-dashboard-status",
        "atlas-resource-monitoring-dashboard-check",
        "atlas-resource-monitoring-dashboard-context",
        "atlas-resource-monitoring-dashboard-review",
        "atlas-resource-monitoring-dashboard-preview",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def run_command(
        self,
        command: str,
    ) -> dict[str, Any]:
        planner = (
            AtlasResourceMonitoringDashboardPlanner(
                project_root=self.project_root
            )
        )
        contract = (
            AtlasResourceMonitoringDashboardContract(
                project_root=self.project_root
            )
        )
        runtime = (
            AtlasResourceMonitoringDashboardRuntimeManager(
                project_root=self.project_root
            )
        )

        mapping = {
            "atlas-resource-monitoring-dashboard-status":
            planner.status,
            "atlas-resource-monitoring-dashboard-check":
            contract.check,
            "atlas-resource-monitoring-dashboard-context":
            planner.context,
            "atlas-resource-monitoring-dashboard-review":
            contract.review,
            "atlas-resource-monitoring-dashboard-preview":
            contract.preview,
        }
        if command not in mapping:
            raise ValueError(
                "Unknown Sprint 267 command: "
                + command
            )

        packet = mapping[command]()
        return {
            "command": command,
            "version": "1.2.7",
            "current_sprint": 267,
            "next_sprint": 268,
            "boundary": (
                "atlas_resource_monitoring_dashboard"
            ),
            "next_boundary": "permission_audit_action_visibility_ux",
            "runtime_status": runtime.status(),
            "packet": packet,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }


def main(
    argv: list[str] | None = None,
) -> int:
    arguments = list(
        argv
        if argv is not None
        else sys.argv[1:]
    )
    command = (
        arguments[0]
        if arguments
        else "atlas-resource-monitoring-dashboard-status"
    )
    packet = (
        AtlasResourceMonitoringDashboardCLI()
        .run_command(command)
    )
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
