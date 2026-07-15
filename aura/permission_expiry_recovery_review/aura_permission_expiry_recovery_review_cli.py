from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_permission_expiry_recovery_review_alpha_manager import (
    AuraPermissionExpiryRecoveryReviewAlphaManager,
)


PERMISSION_EXPIRY_RECOVERY_REVIEW_COMMANDS = frozenset(
    {
        "permission-expiry-recovery-status",
        "permission-expiry-recovery-context",
        "permission-expiry-recovery-check",
        "permission-expiry-recovery-review",
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


def handle_permission_expiry_recovery_review_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if command not in PERMISSION_EXPIRY_RECOVERY_REVIEW_COMMANDS:
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = AuraPermissionExpiryRecoveryReviewAlphaManager(
        project_root=Path.cwd()
    )

    dispatch = {
        "permission-expiry-recovery-status": owner.status,
        "permission-expiry-recovery-context": owner.context,
        "permission-expiry-recovery-check": owner.check,
        "permission-expiry-recovery-review": owner.review,
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "PERMISSION_EXPIRY_RECOVERY_REVIEW_COMMANDS",
    "handle_permission_expiry_recovery_review_command",
]

