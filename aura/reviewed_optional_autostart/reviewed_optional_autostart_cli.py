from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .reviewed_optional_autostart_alpha_manager import (
    ReviewedOptionalAutostartAlphaManager,
)


REVIEWED_OPTIONAL_AUTOSTART_COMMANDS = frozenset(
    {
        "reviewed-optional-autostart-status",
        "reviewed-optional-autostart-context",
        "reviewed-optional-autostart-check",
        "reviewed-optional-autostart-review",
        "reviewed-optional-autostart-unit-preview",
        "reviewed-optional-autostart-activation-preview",
        "reviewed-optional-autostart-rollback-preview",
        "reviewed-optional-autostart-host-posture",
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
                "mutation_commands_available": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_reviewed_optional_autostart_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in REVIEWED_OPTIONAL_AUTOSTART_COMMANDS
    ):
        return False

    command = args[0]
    extras = list(args[1:])

    if extras:
        _usage_error(command, extras)

    owner = ReviewedOptionalAutostartAlphaManager(
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
    elif command.endswith("-unit-preview"):
        packet = owner.unit_preview()
    elif command.endswith("-activation-preview"):
        packet = owner.activation_preview()
    elif command.endswith("-rollback-preview"):
        packet = owner.rollback_preview()
    elif command.endswith("-host-posture"):
        packet = owner.host_posture()
    else:
        return False

    _print_json(packet)
    return True
