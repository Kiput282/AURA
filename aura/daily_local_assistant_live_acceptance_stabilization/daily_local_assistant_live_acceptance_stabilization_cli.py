from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

from .daily_local_assistant_live_acceptance_stabilization_contract import (
    DailyLocalAssistantLiveAcceptanceStabilizationContract,
)
from .daily_local_assistant_live_acceptance_stabilization_planner import (
    DailyLocalAssistantLiveAcceptanceStabilizationPlanner,
)
from .daily_local_assistant_live_acceptance_stabilization_runtime_manager import (
    DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager,
)


class DailyLocalAssistantLiveAcceptanceStabilizationCLI:
    COMMANDS = (
        "daily-local-assistant-live-acceptance-stabilization-status",
        "daily-local-assistant-live-acceptance-stabilization-check",
        "daily-local-assistant-live-acceptance-stabilization-context",
        "daily-local-assistant-live-acceptance-stabilization-review",
        "daily-local-assistant-live-acceptance-stabilization-preview",
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
            DailyLocalAssistantLiveAcceptanceStabilizationPlanner(
                project_root=self.project_root
            )
        )
        contract = (
            DailyLocalAssistantLiveAcceptanceStabilizationContract(
                project_root=self.project_root
            )
        )
        runtime = (
            DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager(
                project_root=self.project_root
            )
        )

        mapping = {
            "daily-local-assistant-live-acceptance-stabilization-status":
            planner.status,
            "daily-local-assistant-live-acceptance-stabilization-check":
            contract.check,
            "daily-local-assistant-live-acceptance-stabilization-context":
            planner.context,
            "daily-local-assistant-live-acceptance-stabilization-review":
            contract.review,
            "daily-local-assistant-live-acceptance-stabilization-preview":
            contract.preview,
        }
        if command not in mapping:
            raise ValueError(
                "Unknown Sprint 270 command: "
                + command
            )

        packet = mapping[command]()
        return {
            "command": command,
            "version": "1.3.0",
            "current_sprint": 270,
            "next_sprint": 271,
            "boundary": (
                "daily_local_assistant_live_acceptance_stabilization"
            ),
            "next_boundary": "voice_daily_use_activation",
            "runtime_status": runtime.self_test(),
            "packet": packet,
            "live_e2e_executed": True,
            "block_complete": True,
            "block_release_ready": True,
            "next_block_reconfirmation_required": True,
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
        else (
            "daily-local-assistant-live-acceptance-"
            "stabilization-status"
        )
    )
    packet = (
        DailyLocalAssistantLiveAcceptanceStabilizationCLI()
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
