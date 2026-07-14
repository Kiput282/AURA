from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_final_release_planner import (
    GenesisFinalReleasePlanner,
)


class GenesisFinalReleaseAlphaManager:
    """Thin read-only manager for the Sprint 240 foundation."""

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.planner = GenesisFinalReleasePlanner(
            project_root=project_root
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
