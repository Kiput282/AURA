from __future__ import annotations

from pathlib import Path
from typing import Any

from .local_model_service_discovery_health_planner import (
    LocalModelServiceDiscoveryHealthPlanner,
)


class LocalModelServiceDiscoveryHealthAlphaManager:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.planner = (
            LocalModelServiceDiscoveryHealthPlanner(
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

    def host_posture(
        self,
    ) -> dict[str, Any]:
        return self.planner.host_posture()

    def provider_contracts(
        self,
    ) -> dict[str, Any]:
        return self.planner.provider_contracts()

    def health_preview(
        self,
    ) -> dict[str, Any]:
        return self.planner.health_preview()

    def health_probe(
        self,
        confirmation: str,
    ) -> dict[str, Any]:
        return self.planner.health_probe(
            confirmation
        )
