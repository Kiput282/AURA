"""Sprint 227 alpha facade for service persistence and launcher metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.partner_runtime.service_persistence_and_launcher_planner import (
    ServicePersistenceAndLauncherPlanner,
)


class ServicePersistenceAndLauncherAlphaManager:
    """Expose the Sprint 227 contract through deterministic read-only methods."""

    name = "service_persistence_and_launcher_alpha"
    version = "0.1.0-alpha"
    sprint = 227

    def __init__(
        self,
        project_root: Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
            or Path.cwd()
        ).resolve()

        self.planner = (
            ServicePersistenceAndLauncherPlanner(
                project_root=self.project_root
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

    def check(
        self,
    ) -> dict[str, Any]:
        return self.planner.check()

    def contract(
        self,
    ) -> dict[str, Any]:
        return (
            self.planner
            .service_persistence_and_launcher_contract()
        )
