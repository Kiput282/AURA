"""Sprint 229 Genesis Acceptance Rehearsal alpha manager."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_acceptance_rehearsal_planner import (
    GenesisAcceptanceRehearsalPlanner,
)


class GenesisAcceptanceRehearsalAlphaManager:
    """Expose the bounded Sprint 229 rehearsal contract."""

    name = "genesis_acceptance_rehearsal_alpha"
    version = "0.1.0-alpha"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner:
            GenesisAcceptanceRehearsalPlanner | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
            if project_root is not None
            else Path.cwd()
        ).resolve()

        self._planner = (
            planner
            if planner is not None
            else GenesisAcceptanceRehearsalPlanner(
                project_root=self.project_root
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
        return (
            self._planner
            .genesis_acceptance_rehearsal_contract()
        )

    def check(
        self,
    ) -> dict[str, Any]:
        return self._planner.check()
