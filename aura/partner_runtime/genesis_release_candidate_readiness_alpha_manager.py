from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_readiness_planner import (
    GenesisReleaseCandidateReadinessPlanner,
)


class GenesisReleaseCandidateReadinessAlphaManager:
    """Thin read-only manager for the Sprint 234 contract."""

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.planner = (
            GenesisReleaseCandidateReadinessPlanner(
                project_root=project_root
            )
        )

    def status(
        self,
    ) -> dict[str, Any]:
        return self.planner.status()

    def context(
        self,
    ) -> dict[str, Any]:
        return self.planner.context()

    def plan(
        self,
    ) -> dict[str, Any]:
        return self.planner.plan()

    def contract(
        self,
    ) -> dict[str, Any]:
        return self.planner.contract()

    def check(
        self,
    ) -> dict[str, Any]:
        return self.planner.check()
