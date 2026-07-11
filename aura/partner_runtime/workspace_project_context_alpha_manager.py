"""Sprint 222 Workspace and Project Context alpha facade."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.partner_runtime.workspace_project_context_planner import (
    WorkspaceProjectContextPlanner,
)


class WorkspaceProjectContextAlphaManager:
    """Read-only facade over the Sprint 222 contract."""

    name = "workspace_project_context_alpha"
    version = "0.1.0-alpha"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner: (
            WorkspaceProjectContextPlanner
            | None
        ) = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

        self.planner = (
            planner
            or WorkspaceProjectContextPlanner(
                self.project_root
            )
        )

    def status(self) -> dict[str, Any]:
        planner_status = self.planner.status()
        planner_check = self.planner.check()
        contract = planner_status["contract"]

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "ready"
                if planner_check[
                    "failed_assertion_count"
                ]
                == 0
                else "degraded"
            ),
            "alpha_ready": (
                planner_check[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "planning_ready": (
                planner_status[
                    "planning_ready"
                ]
            ),
            "runtime_ready": False,
            "runtime_active": False,
            "contract_only": True,
            "workspace_project_context_"
            "contract_ready": contract[
                "workspace_project_context_"
                "contract_ready"
            ],
            "workspace_project_context_"
            "runtime_ready": False,
            "partner_runtime_current_sprint":
                contract[
                    "partner_runtime_current_sprint"
                ],
            "partner_runtime_next_sprint":
                contract[
                    "partner_runtime_next_sprint"
                ],
            "partner_runtime_next_boundary":
                contract[
                    "partner_runtime_next_boundary"
                ],
            "canonical_project_root":
                contract[
                    "canonical_project_root"
                ],
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "assertion_count":
                planner_check[
                    "assertion_count"
                ],
            "failed_assertion_count":
                planner_check[
                    "failed_assertion_count"
                ],
            "failed_assertions":
                planner_check[
                    "failed_assertions"
                ],
            "all_safety_blockers_inactive":
                contract[
                    "all_safety_blockers_inactive"
                ],
            "runtime_scope":
                contract["runtime_scope"],
            "planner_status": planner_status,
        }

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def context(self) -> dict[str, Any]:
        return self.planner.context()
