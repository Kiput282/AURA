"""CLI commands for Sprint 262 operational handoff."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any
import json
import sys

from .operational_browser_chat_model_handoff_planner import (
    OperationalBrowserChatModelHandoffPlanner,
)


COMMANDS = (
    "operational-browser-chat-model-handoff-status",
    "operational-browser-chat-model-handoff-context",
    "operational-browser-chat-model-handoff-check",
    "operational-browser-chat-model-handoff-review",
    "operational-browser-chat-model-handoff-preview",
    (
        "operational-browser-chat-model-"
        "handoff-browser-route"
    ),
    (
        "operational-browser-chat-model-"
        "handoff-process-roles"
    ),
    (
        "operational-browser-chat-model-"
        "handoff-isolated-rehearsal"
    ),
)


def _safe_error(
    command: str,
    message: str,
) -> dict[str, Any]:
    return {
        "status": "rejected",
        "command": command,
        "error": message,
        "source_mutated": False,
        "runtime_activated": False,
        "network_connection_opened": False,
        "model_request_executed": False,
        "repository_committed": False,
        "repository_pushed": False,
    }


def handle_operational_browser_chat_model_handoff_command(
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
                _safe_error(
                    command,
                    (
                        "This command does not "
                        "accept arguments."
                    ),
                ),
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    planner = (
        OperationalBrowserChatModelHandoffPlanner(
            project_root=Path.cwd()
        )
    )
    handlers = {
        (
            "operational-browser-chat-model-"
            "handoff-status"
        ): planner.status,
        (
            "operational-browser-chat-model-"
            "handoff-context"
        ): planner.context,
        (
            "operational-browser-chat-model-"
            "handoff-check"
        ): planner.check,
        (
            "operational-browser-chat-model-"
            "handoff-review"
        ): planner.review,
        (
            "operational-browser-chat-model-"
            "handoff-preview"
        ): planner.preview,
        (
            "operational-browser-chat-model-"
            "handoff-browser-route"
        ): planner.browser_route,
        (
            "operational-browser-chat-model-"
            "handoff-process-roles"
        ): planner.process_roles,
        (
            "operational-browser-chat-model-"
            "handoff-isolated-rehearsal"
        ): planner.isolated_rehearsal,
    }

    print(
        json.dumps(
            handlers[command](),
            indent=2,
            sort_keys=True,
        )
    )
    return True
