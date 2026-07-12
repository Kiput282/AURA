"""AURA Sprint 228 safe auto-start evaluation alpha manager."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .safe_auto_start_evaluation_planner import (
    SafeAutoStartEvaluationPlanner,
)


class SafeAutoStartEvaluationAlphaManager:
    """Expose deterministic read-only Sprint 228 packets."""

    name = "safe_auto_start_evaluation_alpha"
    version = "0.1.0-alpha"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner:
            SafeAutoStartEvaluationPlanner
            | None = None,
    ) -> None:
        self._planner = (
            planner
            or SafeAutoStartEvaluationPlanner(
                project_root=project_root
            )
        )

    def status(
        self,
    ) -> dict[str, Any]:
        return self._planner.status()

    def context(
        self,
    ) -> dict[str, Any]:
        return self._planner.context()

    def plan(
        self,
    ) -> dict[str, Any]:
        return self._planner.plan()

    def contract(
        self,
    ) -> dict[str, Any]:
        return (
            self._planner
            .safe_auto_start_evaluation_contract()
        )

    def check(
        self,
    ) -> dict[str, Any]:
        return self._planner.check()
