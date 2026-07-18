from __future__ import annotations

from pathlib import Path
from typing import Any

from .daily_use_acceptance_rehearsal_release_harness_contract import (
    DailyUseAcceptanceRehearsalReleaseHarnessContract,
)


class DailyUseAcceptanceRehearsalReleaseHarnessPlanner:
    VERSION = "1.2.9"
    CURRENT_SPRINT = 269
    NEXT_SPRINT = 270
    BOUNDARY = (
        "daily_use_acceptance_rehearsal_and_release_harness"
    )
    NEXT_BOUNDARY = "daily_local_assistant_live_acceptance_stabilization"

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
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )

        backend = AuraControlCenterBackendRuntimeManager(
            project_root=self.project_root
        )
        packet = backend.payload_for_route(
            "/api/control-center"
        )[
            "daily_use_acceptance_rehearsal_release_harness"
        ]
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "status": packet["status"],
            "runtime_mode": packet["runtime_mode"],
            "step_count": packet["step_count"],
            "ready_step_count": packet[
                "ready_step_count"
            ],
            "blocked_step_count": packet[
                "blocked_step_count"
            ],
            "rehearsal_ready": packet[
                "rehearsal_ready"
            ],
            "release_harness_ready": packet[
                "release_harness_ready"
            ],
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "sprint_270_failure_recovery_required": True,
            "sprint_270_safe_idle_return_required": True,
            "result_persistence_enabled": False,
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
        check = DailyUseAcceptanceRehearsalReleaseHarnessContract(
            project_root=self.project_root
        ).check()
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
                "Aggregate nine daily-use readiness "
                "checks into a contract-only rehearsal "
                "and release decision harness."
            ),
            "next_scope": self.NEXT_BOUNDARY,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        return DailyUseAcceptanceRehearsalReleaseHarnessContract(
            project_root=self.project_root
        ).check()
