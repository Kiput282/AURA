from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_release_gate_review_planner import (
    GenesisReleaseCandidateReleaseGateReviewPlanner,
)


class GenesisReleaseCandidateReleaseGateReviewAlphaManager:
    """Thin read-only manager for the Sprint 237 contract."""

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.planner = (
            GenesisReleaseCandidateReleaseGateReviewPlanner(
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
