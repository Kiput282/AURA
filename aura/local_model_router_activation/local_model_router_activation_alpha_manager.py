from __future__ import annotations

from pathlib import Path
from typing import Any

from .local_model_router_activation_planner import (
    LocalModelRouterActivationPlanner,
)


class LocalModelRouterActivationAlphaManager:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.planner = (
            LocalModelRouterActivationPlanner(
                project_root=project_root
            )
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def route_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.planner.route_preview(
            target
        )

    def profile_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.planner.profile_preview(
            target
        )

    def request_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.planner.request_preview(
            target
        )

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        return self.planner.isolated_rehearsal()
