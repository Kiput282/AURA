"""CLI routing for Sprint 244 persistence checks."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import NoReturn

from .aura_session_memory_persistence_checks_alpha_manager import (
    AuraSessionMemoryPersistenceChecksAlphaManager,
)


STATUS_COMMAND = (
    "session-memory-persistence-status"
)
CONTEXT_COMMAND = (
    "session-memory-persistence-context"
)
CHECK_COMMAND = (
    "session-memory-persistence-check"
)

SESSION_MEMORY_PERSISTENCE_COMMANDS = frozenset(
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


def handle_session_memory_persistence_command(
    args: Sequence[str],
) -> bool:
    """Route only Sprint 244 commands."""

    if not args:
        return False

    command = str(args[0])

    if (
        command
        not in SESSION_MEMORY_PERSISTENCE_COMMANDS
    ):
        return False

    extra = [
        str(item)
        for item in args[1:]
    ]

    if extra:
        _usage_error(
            f"{command} does not accept arguments."
        )

    owner = (
        AuraSessionMemoryPersistenceChecksAlphaManager()
    )

    if command == STATUS_COMMAND:
        _print_json(owner.status())
        return True

    if command == CONTEXT_COMMAND:
        _print_json(owner.context())
        return True

    _print_json(owner.check())
    return True


__all__ = [
    "SESSION_MEMORY_PERSISTENCE_COMMANDS",
    "handle_session_memory_persistence_command",
]
