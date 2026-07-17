"""Sprint 262 operational handoff planner facade."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .operational_browser_chat_model_handoff_contract import (
    OperationalBrowserChatModelHandoffContract,
)


class OperationalBrowserChatModelHandoffPlanner:
    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.contract = (
            OperationalBrowserChatModelHandoffContract(
                project_root=project_root
            )
        )

    def status(self) -> dict[str, Any]:
        return self.contract.status()

    def context(self) -> dict[str, Any]:
        return self.contract.context()

    def check(self) -> dict[str, Any]:
        return self.contract.check()

    def review(self) -> dict[str, Any]:
        return self.contract.review()

    def preview(self) -> dict[str, Any]:
        return self.contract.preview()

    def browser_route(self) -> dict[str, Any]:
        return (
            self.contract.manager
            .browser_route_status()
        )

    def process_roles(self) -> dict[str, Any]:
        return (
            self.contract.manager
            .process_role_status()
        )

    def isolated_rehearsal(self) -> dict[str, Any]:
        return (
            self.contract.manager
            .isolated_rehearsal()
        )
