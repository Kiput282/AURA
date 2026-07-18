from __future__ import annotations

from pathlib import Path
from typing import Any

from .daily_local_assistant_live_acceptance_stabilization_contract import (
    DailyLocalAssistantLiveAcceptanceStabilizationContract,
)
from .daily_local_assistant_live_acceptance_stabilization_runtime_manager import (
    DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager,
)


class DailyLocalAssistantLiveAcceptanceStabilizationPlanner:
    VERSION = "1.3.0"
    CURRENT_SPRINT = 270
    NEXT_SPRINT = 271
    BOUNDARY = (
        "daily_local_assistant_live_acceptance_stabilization"
    )
    NEXT_BOUNDARY = "voice_daily_use_activation"

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def snapshot(self) -> dict[str, Any]:
        return (
            DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager(
                project_root=self.project_root
            ).snapshot()
        )

    def status(self) -> dict[str, Any]:
        check = (
            DailyLocalAssistantLiveAcceptanceStabilizationContract(
                project_root=self.project_root
            ).check()
        )
        return {
            **self.snapshot(),
            "status": (
                "released"
                if check["status_valid"]
                else "review_required"
            ),
            "status_valid": check["status_valid"],
            "alpha_ready": check["alpha_ready"],
            "assertion_count":
            check["assertion_count"],
            "failed_assertion_count":
            check["failed_assertion_count"],
            "dimension_count":
            check["dimension_count"],
            "finding_count":
            check["finding_count"],
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "scope": (
                "Canonicalize the successful Sprint 270 "
                "live end-to-end acceptance, failure and "
                "recovery proof, and safe-idle release."
            ),
            "next_scope": self.NEXT_BOUNDARY,
            "next_block_reconfirmation_required": True,
        }

    def check(self) -> dict[str, Any]:
        return (
            DailyLocalAssistantLiveAcceptanceStabilizationContract(
                project_root=self.project_root
            ).check()
        )
