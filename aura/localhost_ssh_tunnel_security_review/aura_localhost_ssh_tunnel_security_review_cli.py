from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_localhost_ssh_tunnel_security_review_alpha_manager import (
    AuraLocalhostSshTunnelSecurityReviewAlphaManager,
)


LOCALHOST_SSH_TUNNEL_SECURITY_REVIEW_COMMANDS = frozenset(
    {
        "localhost-ssh-security-status",
        "localhost-ssh-security-context",
        "localhost-ssh-security-check",
        "localhost-ssh-security-review",
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


def handle_localhost_ssh_tunnel_security_review_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if (
        command
        not in LOCALHOST_SSH_TUNNEL_SECURITY_REVIEW_COMMANDS
    ):
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = (
        AuraLocalhostSshTunnelSecurityReviewAlphaManager(
            project_root=Path.cwd()
        )
    )

    dispatch = {
        "localhost-ssh-security-status": owner.status,
        "localhost-ssh-security-context": owner.context,
        "localhost-ssh-security-check": owner.check,
        "localhost-ssh-security-review": owner.review,
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "LOCALHOST_SSH_TUNNEL_SECURITY_REVIEW_COMMANDS",
    "handle_localhost_ssh_tunnel_security_review_command",
]
