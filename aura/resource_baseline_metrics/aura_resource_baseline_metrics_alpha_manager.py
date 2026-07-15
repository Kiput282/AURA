from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_resource_baseline_metrics_planner import (
    AuraResourceBaselineMetricsPlanner,
)


class AuraResourceBaselineMetricsAlphaManager:
    def __init__(self, project_root: Path) -> None:
        self.planner = AuraResourceBaselineMetricsPlanner(
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
