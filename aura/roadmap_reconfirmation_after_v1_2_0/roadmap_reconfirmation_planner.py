"""Sprint 261 roadmap planner facade."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .roadmap_reconfirmation_contract import (
    RoadmapReconfirmationContract,
)


class RoadmapReconfirmationPlanner:
    """Provide read-only roadmap commands."""

    def __init__(
        self,
        *,
        project_root: Path | None = None,
    ) -> None:
        self.contract = RoadmapReconfirmationContract(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.contract.status()

    def context(self) -> dict[str, Any]:
        return self.contract.context()

    def check(self) -> dict[str, Any]:
        return self.contract.check()

    def review(self) -> dict[str, Any]:
        return self.contract.review()

    def preview(self) -> dict[str, Any]:
        return self.contract.preview()

    def live_acceptance_policy(
        self,
    ) -> dict[str, Any]:
        return (
            self.contract.manager
            .live_acceptance_policy()
        )

    def gap_ownership(
        self,
    ) -> dict[str, Any]:
        return (
            self.contract.manager
            .gap_ownership()
        )

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        return self.contract.isolated_rehearsal()
