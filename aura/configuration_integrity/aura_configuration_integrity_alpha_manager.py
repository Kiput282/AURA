"""Thin canonical Sprint 243 configuration-integrity owner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_configuration_integrity_planner import (
    AuraConfigurationIntegrityPlanner,
)


class AuraConfigurationIntegrityAlphaManager:
    """Expose the read-only Sprint 243 contract."""

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner: AuraConfigurationIntegrityPlanner
        | None = None,
    ) -> None:
        self.planner = (
            planner
            if planner is not None
            else AuraConfigurationIntegrityPlanner(
                project_root=project_root
            )
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def plan(self) -> dict[str, Any]:
        return self.planner.plan()

    def contract(self) -> dict[str, Any]:
        return self.planner.contract()

    def check(self) -> dict[str, Any]:
        return self.planner.check()


__all__ = [
    "AuraConfigurationIntegrityAlphaManager",
]
