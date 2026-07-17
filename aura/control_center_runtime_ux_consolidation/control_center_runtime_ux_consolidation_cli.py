"""Sprint 266 Control Center runtime UX consolidation CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

from .control_center_runtime_ux_consolidation_contract import (
    ControlCenterRuntimeUxConsolidationContract,
)
from .control_center_runtime_ux_consolidation_planner import (
    ControlCenterRuntimeUxConsolidationPlanner,
)
from .control_center_runtime_ux_consolidation_runtime_manager import (
    ControlCenterRuntimeUxConsolidationRuntimeManager,
)


class ControlCenterRuntimeUxConsolidationCLI:
    COMMANDS = (
        "control-center-runtime-ux-status",
        "control-center-runtime-ux-check",
        "control-center-runtime-ux-context",
        "control-center-runtime-ux-review",
        "control-center-runtime-ux-preview",
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
        planner = ControlCenterRuntimeUxConsolidationPlanner(
            project_root=self.project_root
        )
        contract = ControlCenterRuntimeUxConsolidationContract(
            project_root=self.project_root
        )
        runtime = ControlCenterRuntimeUxConsolidationRuntimeManager(
            project_root=self.project_root
        )

        mapping = {
            "control-center-runtime-ux-status": planner.status,
            "control-center-runtime-ux-check": contract.check,
            "control-center-runtime-ux-context": planner.context,
            "control-center-runtime-ux-review": contract.review,
            "control-center-runtime-ux-preview": contract.preview,
        }
        if command not in mapping:
            raise ValueError(
                "Unknown Sprint 266 command: " + command
            )

        packet = mapping[command]()
        return {
            "command": command,
            "version": "1.2.6",
            "current_sprint": 266,
            "next_sprint": 267,
            "boundary": "control_center_runtime_ux_consolidation",
            "next_boundary": "atlas_resource_monitoring_dashboard",
            "runtime_status": runtime.status(),
            "packet": packet,
            "runtime_mutated": False,
            "safe_idle": True,
        }


def main(argv: list[str] | None = None) -> int:
    arguments = list(argv if argv is not None else sys.argv[1:])
    command = (
        arguments[0]
        if arguments
        else "control-center-runtime-ux-status"
    )
    packet = ControlCenterRuntimeUxConsolidationCLI().run_command(
        command
    )
    print(json.dumps(packet, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
