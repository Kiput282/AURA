from __future__ import annotations

from pathlib import Path
from typing import Any

from .personality_consistency_runtime_planner import (
    PersonalityConsistencyRuntimePlanner,
)


class PersonalityConsistencyRuntimeAlphaManager:
    """Read-only facade for the Sprint 225 personality contract."""

    name = "personality_consistency_runtime_alpha"
    version = "0.1.0"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner: (
            PersonalityConsistencyRuntimePlanner
            | None
        ) = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()

        self.planner = (
            planner
            or PersonalityConsistencyRuntimePlanner(
                project_root=self.project_root
            )
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def plan(self) -> dict[str, Any]:
        return self.planner.plan()

    def check(self) -> dict[str, Any]:
        return self.planner.check()
