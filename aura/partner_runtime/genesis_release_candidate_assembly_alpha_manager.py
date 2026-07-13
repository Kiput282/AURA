from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_assembly_planner import (
    GenesisReleaseCandidateAssemblyPlanner,
)


class GenesisReleaseCandidateAssemblyAlphaManager:
    """Thin read-only manager for the Sprint 232 contract."""

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.planner = (
            GenesisReleaseCandidateAssemblyPlanner(
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
