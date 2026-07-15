from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_backup_restore_rehearsal_alpha_manager import (
    AuraBackupRestoreRehearsalAlphaManager,
)


BACKUP_RESTORE_REHEARSAL_COMMANDS = frozenset(
    {
        "backup-restore-rehearsal-status",
        "backup-restore-rehearsal-context",
        "backup-restore-rehearsal-check",
        "backup-restore-rehearsal-review",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        )
    )


def _usage_error(
    command: str,
    extras: Sequence[str],
) -> None:
    packet = {
        "error": "unexpected_arguments",
        "command": command,
        "unexpected_arguments": list(extras),
        "expected_argument_count": 0,
    }
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_backup_restore_rehearsal_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if command not in BACKUP_RESTORE_REHEARSAL_COMMANDS:
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = AuraBackupRestoreRehearsalAlphaManager(
        project_root=Path.cwd()
    )

    dispatch = {
        "backup-restore-rehearsal-status": owner.status,
        "backup-restore-rehearsal-context": owner.context,
        "backup-restore-rehearsal-check": owner.check,
        "backup-restore-rehearsal-review": owner.review,
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "BACKUP_RESTORE_REHEARSAL_COMMANDS",
    "handle_backup_restore_rehearsal_command",
]
