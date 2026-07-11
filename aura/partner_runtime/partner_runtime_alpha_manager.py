"""Sprint 221 Unified Session Runtime alpha facade.

The alpha manager exposes contract status only. It does not activate partner
runtime execution or mutate the canonical browser chat session store.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.partner_runtime.partner_runtime_planner import PartnerRuntimePlanner


class PartnerRuntimeAlphaManager:
    """Read-only facade over the Sprint 221 partner runtime contract."""

    name = "partner_runtime_alpha"
    version = "0.1.0-alpha"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner: PartnerRuntimePlanner | None = None,
    ) -> None:
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.planner = planner or PartnerRuntimePlanner(self.project_root)

    def status(self) -> dict[str, Any]:
        planner_status = self.planner.status()
        planner_check = self.planner.check()
        contract = planner_status["contract"]
        return {
            "name": self.name,
            "version": self.version,
            "status": "ready" if not planner_check["failed_assertions"] else "degraded",
            "alpha_ready": planner_check["failed_assertion_count"] == 0,
            "planning_ready": planner_status["planning_ready"],
            "runtime_ready": False,
            "runtime_active": False,
            "contract_only": True,
            "unified_session_runtime_contract_ready": contract[
                "unified_session_runtime_contract_ready"
            ],
            "unified_session_runtime_ready": False,
            "partner_runtime_current_sprint": contract[
                "partner_runtime_current_sprint"
            ],
            "partner_runtime_next_sprint": contract[
                "partner_runtime_next_sprint"
            ],
            "partner_runtime_next_boundary": contract[
                "partner_runtime_next_boundary"
            ],
            "canonical_session_owner": contract["canonical_session_owner"],
            "session_count": contract["session_snapshot"]["session_count"],
            "total_message_count": contract["session_snapshot"][
                "total_message_count"
            ],
            "assertion_count": planner_check["assertion_count"],
            "failed_assertion_count": planner_check[
                "failed_assertion_count"
            ],
            "failed_assertions": planner_check["failed_assertions"],
            "all_safety_blockers_inactive": contract[
                "all_safety_blockers_inactive"
            ],
            "runtime_scope": contract["runtime_scope"],
            "planner_status": planner_status,
        }

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def context(self) -> dict[str, Any]:
        return self.planner.context()
