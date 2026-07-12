from __future__ import annotations

from pathlib import Path
from typing import Any

from .unified_partner_runtime_stabilization_planner import (
    UnifiedPartnerRuntimeStabilizationPlanner,
)


class UnifiedPartnerRuntimeStabilizationAlphaManager:
    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self._planner = (
            UnifiedPartnerRuntimeStabilizationPlanner(
                project_root=project_root,
            )
        )

    def status(
        self,
    ) -> dict[str, Any]:
        return self._planner.status()

    def context(
        self,
    ) -> dict[str, Any]:
        return self._planner.context()

    def plan(
        self,
    ) -> dict[str, Any]:
        return self._planner.plan()

    def contract(
        self,
    ) -> dict[str, Any]:
        return self._planner.contract()

    def check(
        self,
    ) -> dict[str, Any]:
        return self._planner.check()
