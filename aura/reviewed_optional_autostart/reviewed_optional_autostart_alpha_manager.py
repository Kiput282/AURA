from __future__ import annotations

from pathlib import Path
from typing import Any

from .reviewed_optional_autostart_planner import (
    ReviewedOptionalAutostartPlanner,
)


class ReviewedOptionalAutostartAlphaManager:
    def __init__(self, project_root: str | Path) -> None:
        self.planner = ReviewedOptionalAutostartPlanner(
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

    def unit_preview(self) -> dict[str, Any]:
        return self.planner.unit_preview()

    def activation_preview(self) -> dict[str, Any]:
        return self.planner.activation_preview()

    def rollback_preview(self) -> dict[str, Any]:
        return self.planner.rollback_preview()

    def host_posture(self) -> dict[str, Any]:
        return self.planner.host_posture()
