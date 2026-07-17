from __future__ import annotations

from pathlib import Path
from typing import Sequence
import json
import sys

from .chat_history_recovery_ux_planner import (
    ChatHistoryRecoveryUxPlanner,
)


COMMANDS = {
    "chat-history-recovery-ux-status",
    "chat-history-recovery-ux-context",
    "chat-history-recovery-ux-check",
    "chat-history-recovery-ux-review",
    "chat-history-recovery-ux-preview",
    "chat-history-recovery-ux-runtime-status",
    "chat-history-recovery-ux-routes",
    "chat-history-recovery-ux-web-surface",
    "chat-history-recovery-ux-isolated-rehearsal",
}


def _safe_error(
    command: str,
    detail: str,
) -> dict[str, object]:
    return {
        "status": "error",
        "command": command,
        "detail": detail,
        "runtime_mutated": False,
    }


def handle_chat_history_recovery_ux_command(
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
                    "This command does not accept arguments.",
                ),
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    planner = ChatHistoryRecoveryUxPlanner(
        project_root=Path.cwd()
    )
    handlers = {
        "chat-history-recovery-ux-status":
            planner.status,
        "chat-history-recovery-ux-context":
            planner.context,
        "chat-history-recovery-ux-check":
            planner.check,
        "chat-history-recovery-ux-review":
            planner.review,
        "chat-history-recovery-ux-preview":
            planner.preview,
        "chat-history-recovery-ux-runtime-status":
            planner.runtime_status,
        "chat-history-recovery-ux-routes":
            planner.route_status,
        "chat-history-recovery-ux-web-surface":
            planner.web_surface_status,
        "chat-history-recovery-ux-isolated-rehearsal":
            planner.isolated_rehearsal,
    }

    print(
        json.dumps(
            handlers[command](),
            indent=2,
            sort_keys=True,
        )
    )
    return True
