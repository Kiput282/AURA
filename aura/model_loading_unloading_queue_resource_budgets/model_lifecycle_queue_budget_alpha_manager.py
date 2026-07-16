from __future__ import annotations

from pathlib import Path
from typing import Any

from .model_lifecycle_queue_budget_planner import (
    ModelLifecycleQueueBudgetPlanner,
)


class ModelLifecycleQueueBudgetAlphaManager:
    def __init__(self, project_root: str | Path) -> None:
        self.planner = ModelLifecycleQueueBudgetPlanner(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def lifecycle_preview(self, action: str) -> dict[str, Any]:
        return self.planner.lifecycle_preview(action)

    def queue_preview(self) -> dict[str, Any]:
        return self.planner.queue_preview()

    def resource_budget_preview(self) -> dict[str, Any]:
        return self.planner.resource_budget_preview()

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.planner.isolated_rehearsal()
