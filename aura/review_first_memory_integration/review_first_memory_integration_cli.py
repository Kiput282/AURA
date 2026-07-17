from __future__ import annotations

from pathlib import Path
from typing import Sequence, Any
import json
import sys

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    AuraBrowserChatSessionHttpRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
)
from .review_first_memory_integration_planner import (
    ReviewFirstMemoryIntegrationPlanner,
)
from .review_first_memory_integration_runtime_manager import (
    ReviewFirstMemoryIntegrationRuntimeManager,
)


COMMANDS = {
    "review-first-memory-integration-status",
    "review-first-memory-integration-context",
    "review-first-memory-integration-check",
    "review-first-memory-integration-review",
    "review-first-memory-integration-preview",
    "review-first-memory-integration-runtime-status",
    "review-first-memory-integration-routes",
    "review-first-memory-integration-web-surface",
    "review-first-memory-integration-isolated-rehearsal",
}


def _error(command: str, detail: str) -> dict[str, Any]:
    return {
        "status": "invalid_request",
        "command": command,
        "detail": detail,
    }


def handle_review_first_memory_integration_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = str(args[0])
    if command not in COMMANDS:
        return False

    if len(args) != 1:
        print(
            json.dumps(
                _error(
                    command,
                    "This command does not accept arguments.",
                ),
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return True

    root = Path.cwd()
    planner = ReviewFirstMemoryIntegrationPlanner(
        project_root=root
    )
    manager = ReviewFirstMemoryIntegrationRuntimeManager(
        project_root=root
    )

    if command == (
        "review-first-memory-integration-runtime-status"
    ):
        payload = manager.status()
    elif command == (
        "review-first-memory-integration-routes"
    ):
        payload = {
            "status": "ok",
            "chat_route_contracts": len(
                AuraBrowserChatSessionHttpRuntimeManager
                .CHAT_ROUTE_CONTRACTS
            ),
            "total_route_contracts": (
                AuraBrowserChatSessionHttpRuntimeManager
                .TOTAL_ROUTE_CONTRACT_COUNT
            ),
            "routes": list(
                AuraBrowserChatSessionHttpRuntimeManager
                .CHAT_ROUTE_CONTRACTS
            ),
            "durable_memory_write": False,
            "memory_store_mutation": False,
        }
    elif command == (
        "review-first-memory-integration-web-surface"
    ):
        web = AuraBrowserChatWebSurfaceManager(
            project_root=root
        )
        payload = {
            **web.status(),
            "self_test": web.self_test(),
        }
    elif command == (
        "review-first-memory-integration-isolated-rehearsal"
    ):
        payload = manager.self_test()
    elif command == (
        "review-first-memory-integration-status"
    ):
        payload = planner.status()
    elif command == (
        "review-first-memory-integration-context"
    ):
        payload = planner.context()
    elif command == (
        "review-first-memory-integration-check"
    ):
        payload = planner.check()
    elif command == (
        "review-first-memory-integration-review"
    ):
        payload = planner.review()
    else:
        payload = planner.preview()

    print(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
    )
    return True
