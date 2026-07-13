from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_final_integration_and_release_planner import (
    GenesisFinalIntegrationAndReleasePlanner,
)


class GenesisFinalIntegrationAndReleaseAlphaManager:
    """Thin read-only manager for the Sprint 231 contract."""

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.planner = (
            GenesisFinalIntegrationAndReleasePlanner(
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
