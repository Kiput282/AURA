"""Pure-JSON CLI routing for Sprint 245."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn

from .aura_log_rotation_storage_cleanup_alpha_manager import (
    AuraLogRotationStorageCleanupAlphaManager,
)


STATUS_COMMAND = "log-rotation-storage-status"
CONTEXT_COMMAND = "log-rotation-storage-context"
CHECK_COMMAND = "log-rotation-storage-check"
PREVIEW_COMMAND = (
    "log-rotation-storage-cleanup-preview"
)

LOG_ROTATION_STORAGE_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        CONTEXT_COMMAND,
        CHECK_COMMAND,
        PREVIEW_COMMAND,
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
        PREVIEW_COMMAND,
    ):
        print(
            f"  python3 main.py {command}",
            file=sys.stderr,
        )

    raise SystemExit(2)


def handle_log_rotation_storage_cleanup_command(
    args: Sequence[str],
) -> bool:
    """Route only Sprint 245 commands."""

    if not args:
        return False

    command = str(args[0])

    if command not in LOG_ROTATION_STORAGE_COMMANDS:
        return False

    extra = [
        str(item)
        for item in args[1:]
    ]

    if extra:
        _usage_error(
            f"{command} does not accept arguments."
        )

    owner = AuraLogRotationStorageCleanupAlphaManager(
        project_root=Path.cwd()
    )

    if command == STATUS_COMMAND:
        _print_json(owner.status())
        return True

    if command == CONTEXT_COMMAND:
        _print_json(owner.context())
        return True

    if command == PREVIEW_COMMAND:
        _print_json(owner.cleanup_preview())
        return True

    _print_json(owner.check())
    return True


__all__ = [
    "LOG_ROTATION_STORAGE_COMMANDS",
    "handle_log_rotation_storage_cleanup_command",
]
