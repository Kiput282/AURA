from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .active_local_runtime_integration_alpha_manager import (
    ActiveLocalRuntimeIntegrationAlphaManager,
)


ACTIVE_LOCAL_RUNTIME_INTEGRATION_COMMANDS = frozenset(
    {
        "active-local-runtime-integration-status",
        "active-local-runtime-integration-context",
        "active-local-runtime-integration-check",
        "active-local-runtime-integration-review",
        "active-local-runtime-integration-preview",
        "active-local-runtime-chat-turn-preview",
        "active-local-runtime-stop-restore-preview",
        "active-local-runtime-integration-isolated-rehearsal",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(json.dumps(packet, indent=2, sort_keys=True))


def _usage_error(
    command: str,
    extras: Sequence[str],
) -> NoReturn:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "invalid_arguments",
                "command": command,
                "expected": "<no-arguments>",
                "provided_arguments": list(extras),
                "network_connection_opened": False,
                "runtime_activated": False,
                "model_request_executed": False,
                "session_mutated": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_active_local_runtime_integration_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in ACTIVE_LOCAL_RUNTIME_INTEGRATION_COMMANDS
    ):
        return False

    command = args[0]
    extras = list(args[1:])
    if extras:
        _usage_error(command, extras)

    owner = ActiveLocalRuntimeIntegrationAlphaManager(
        project_root=Path.cwd()
    )

    if command.endswith("-status"):
        packet = owner.status()
    elif command.endswith("-context"):
        packet = owner.context()
    elif command.endswith("-check"):
        packet = owner.check()
    elif command.endswith("-review"):
        packet = owner.review()
    elif command.endswith("-integration-preview"):
        packet = owner.integration_preview()
    elif command.endswith("-chat-turn-preview"):
        packet = owner.chat_turn_preview()
    elif command.endswith("-stop-restore-preview"):
        packet = owner.stop_restore_preview()
    elif command.endswith("-isolated-rehearsal"):
        packet = owner.isolated_rehearsal()
    else:
        return False

    _print_json(packet)
    return True
