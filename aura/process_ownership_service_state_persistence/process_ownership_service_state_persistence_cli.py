from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .process_ownership_service_state_persistence_alpha_manager import (
    ProcessOwnershipServiceStatePersistenceAlphaManager,
)


PROCESS_OWNERSHIP_SERVICE_STATE_PERSISTENCE_COMMANDS = frozenset(
    {
        "process-ownership-service-state-persistence-status",
        "process-ownership-service-state-persistence-context",
        "process-ownership-service-state-persistence-check",
        "process-ownership-service-state-persistence-review",
        "process-ownership-service-state-persistence-inspect",
        "process-ownership-service-state-persistence-recovery-preview",
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
                "error": "unexpected_arguments",
                "command": command,
                "provided_arguments": list(extras),
                "expected_arguments": [],
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_process_ownership_service_state_persistence_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in PROCESS_OWNERSHIP_SERVICE_STATE_PERSISTENCE_COMMANDS
    ):
        return False

    command = args[0]
    extras = list(args[1:])

    if extras:
        _usage_error(command, extras)

    owner = ProcessOwnershipServiceStatePersistenceAlphaManager(
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
    elif command.endswith("-inspect"):
        packet = owner.inspect()
    elif command.endswith("-recovery-preview"):
        packet = owner.recovery_preview()
    else:
        return False

    _print_json(packet)
    return True
