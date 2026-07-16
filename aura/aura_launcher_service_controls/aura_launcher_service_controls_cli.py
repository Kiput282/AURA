from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_launcher_service_controls_alpha_manager import (
    AuraLauncherServiceControlsAlphaManager,
)


AURA_LAUNCHER_SERVICE_CONTROLS_COMMANDS = frozenset(
    {
        "aura-launcher-service-controls-status",
        "aura-launcher-service-controls-context",
        "aura-launcher-service-controls-check",
        "aura-launcher-service-controls-review",
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


def handle_aura_launcher_service_controls_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if (
        command
        not in AURA_LAUNCHER_SERVICE_CONTROLS_COMMANDS
    ):
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = AuraLauncherServiceControlsAlphaManager(
        project_root=Path.cwd()
    )

    dispatch = {
        "aura-launcher-service-controls-status": (
            owner.status
        ),
        "aura-launcher-service-controls-context": (
            owner.context
        ),
        "aura-launcher-service-controls-check": (
            owner.check
        ),
        "aura-launcher-service-controls-review": (
            owner.review
        ),
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "AURA_LAUNCHER_SERVICE_CONTROLS_COMMANDS",
    "handle_aura_launcher_service_controls_command",
]
