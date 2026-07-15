from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_atlas_resource_monitoring_planner import (
    AuraAtlasResourceMonitoringPlanner,
)


class AuraAtlasResourceMonitoringAlphaManager:
    def __init__(self, project_root: Path) -> None:
        self.planner = AuraAtlasResourceMonitoringPlanner(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def snapshot(self) -> dict[str, Any]:
        return self.planner.snapshot()

    def check(self) -> dict[str, Any]:
        return self.planner.check()
