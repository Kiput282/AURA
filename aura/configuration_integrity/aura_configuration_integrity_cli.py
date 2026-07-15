"""CLI routing for Sprint 243 configuration integrity."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import NoReturn

from .aura_configuration_integrity_alpha_manager import (
    AuraConfigurationIntegrityAlphaManager,
)


STATUS_COMMAND = "configuration-integrity-status"
CONTEXT_COMMAND = "configuration-integrity-context"
CHECK_COMMAND = "configuration-integrity-check"

CONFIGURATION_INTEGRITY_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        CONTEXT_COMMAND,
        CHECK_COMMAND,
    }
)


def _print_json(
    payload: dict[str, object],
) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def _usage_error(
    message: str,
) -> NoReturn:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    print("Usage:", file=sys.stderr)

    for command in (
        STATUS_COMMAND,
        CONTEXT_COMMAND,
        CHECK_COMMAND,
    ):
        print(
            f"  python3 main.py {command}",
            file=sys.stderr,
        )

    raise SystemExit(2)


def handle_configuration_integrity_command(
    args: Sequence[str],
) -> bool:
    """Route only Sprint 243 commands."""

    if not args:
        return False

    command = str(args[0])

    if command not in CONFIGURATION_INTEGRITY_COMMANDS:
        return False

    extra = [
        str(item)
        for item in args[1:]
    ]

    if extra:
        _usage_error(
            f"{command} does not accept arguments."
        )

    owner = AuraConfigurationIntegrityAlphaManager()

    if command == STATUS_COMMAND:
        _print_json(owner.status())
        return True

    if command == CONTEXT_COMMAND:
        _print_json(owner.context())
        return True

    _print_json(owner.check())
    return True


__all__ = [
    "CONFIGURATION_INTEGRITY_COMMANDS",
    "handle_configuration_integrity_command",
]
