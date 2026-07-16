from __future__ import annotations

from pathlib import Path
from typing import Any

from .restart_logs_failure_visibility_executor import (
    RestartLogsFailureVisibilityExecutor,
)
from .restart_logs_failure_visibility_planner import (
    RestartLogsFailureVisibilityPlanner,
)


class RestartLogsFailureVisibilityAlphaManager:
    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        self.project_root = Path(
            project_root if project_root is not None else Path.cwd()
        ).resolve()
        self.planner = RestartLogsFailureVisibilityPlanner(
            project_root=self.project_root
        )
        self.executor = RestartLogsFailureVisibilityExecutor(
            project_root=self.project_root
        )

    def status(self) -> dict[str, Any]:
        packet = self.planner.status()
        packet["executor_status"] = self.executor.status()
        return packet

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def logs(self) -> dict[str, Any]:
        return self.planner.log_visibility()

    def failures(self) -> dict[str, Any]:
        return self.planner.failure_visibility()

    def restart_preview(self) -> dict[str, Any]:
        return self.planner.restart_preview()

    def tail(self, *, source: str, lines: int) -> dict[str, Any]:
        return self.executor.tail(source=source, lines=lines)

    def restart(self) -> dict[str, Any]:
        return self.executor.restart()
