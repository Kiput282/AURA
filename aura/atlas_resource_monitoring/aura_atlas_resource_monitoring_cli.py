from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_atlas_resource_monitoring_alpha_manager import (
    AuraAtlasResourceMonitoringAlphaManager,
)


ATLAS_RESOURCE_MONITORING_COMMANDS = frozenset(
    {
        "atlas-resource-monitor-status",
        "atlas-resource-monitor-context",
        "atlas-resource-monitor-check",
        "atlas-resource-monitor-snapshot",
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


def handle_atlas_resource_monitoring_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if command not in ATLAS_RESOURCE_MONITORING_COMMANDS:
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = AuraAtlasResourceMonitoringAlphaManager(
        project_root=Path.cwd()
    )

    dispatch = {
        "atlas-resource-monitor-status": owner.status,
        "atlas-resource-monitor-context": owner.context,
        "atlas-resource-monitor-check": owner.check,
        "atlas-resource-monitor-snapshot": owner.snapshot,
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "ATLAS_RESOURCE_MONITORING_COMMANDS",
    "handle_atlas_resource_monitoring_command",
]
