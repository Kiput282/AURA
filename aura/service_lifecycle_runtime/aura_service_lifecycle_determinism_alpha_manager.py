from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_service_lifecycle_determinism_planner import (
    AuraServiceLifecycleDeterminismPlanner,
)


class AuraServiceLifecycleDeterminismAlphaManager:
    """Thin canonical Sprint 242 lifecycle owner."""

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.planner = (
            AuraServiceLifecycleDeterminismPlanner(
                project_root=project_root,
            )
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def plan(self) -> dict[str, Any]:
        return self.planner.plan()

    def contract(self) -> dict[str, Any]:
        return self.planner.contract()

    def check(self) -> dict[str, Any]:
        return self.planner.check()
