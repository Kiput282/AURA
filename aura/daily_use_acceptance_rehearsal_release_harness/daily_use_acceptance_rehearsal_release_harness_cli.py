from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

from .daily_use_acceptance_rehearsal_release_harness_contract import (
    DailyUseAcceptanceRehearsalReleaseHarnessContract,
)
from .daily_use_acceptance_rehearsal_release_harness_planner import (
    DailyUseAcceptanceRehearsalReleaseHarnessPlanner,
)
from .daily_use_acceptance_rehearsal_release_harness_runtime_manager import (
    DailyUseAcceptanceRehearsalReleaseHarnessRuntimeManager,
)


class DailyUseAcceptanceRehearsalReleaseHarnessCLI:
    COMMANDS = (
        "daily-use-acceptance-rehearsal-release-harness-status",
        "daily-use-acceptance-rehearsal-release-harness-check",
        "daily-use-acceptance-rehearsal-release-harness-context",
        "daily-use-acceptance-rehearsal-release-harness-review",
        "daily-use-acceptance-rehearsal-release-harness-preview",
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
        planner = DailyUseAcceptanceRehearsalReleaseHarnessPlanner(
            project_root=self.project_root
        )
        contract = DailyUseAcceptanceRehearsalReleaseHarnessContract(
            project_root=self.project_root
        )
        runtime = DailyUseAcceptanceRehearsalReleaseHarnessRuntimeManager(
            project_root=self.project_root
        )

        mapping = {
            "daily-use-acceptance-rehearsal-release-harness-status":
            planner.status,
            "daily-use-acceptance-rehearsal-release-harness-check":
            contract.check,
            "daily-use-acceptance-rehearsal-release-harness-context":
            planner.context,
            "daily-use-acceptance-rehearsal-release-harness-review":
            contract.review,
            "daily-use-acceptance-rehearsal-release-harness-preview":
            contract.preview,
        }
        if command not in mapping:
            raise ValueError(
                "Unknown Sprint 269 command: "
                + command
            )

        packet = mapping[command]()
        return {
            "command": command,
            "version": "1.2.9",
            "current_sprint": 269,
            "next_sprint": 270,
            "boundary": (
                "daily_use_acceptance_rehearsal_and_release_harness"
            ),
            "next_boundary": "daily_local_assistant_live_acceptance_stabilization",
            "runtime_status": runtime.self_test(),
            "packet": packet,
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
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
        else "daily-use-acceptance-rehearsal-release-harness-status"
    )
    packet = (
        DailyUseAcceptanceRehearsalReleaseHarnessCLI()
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
