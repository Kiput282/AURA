from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .aura_resource_baseline_metrics_alpha_manager import (
    AuraResourceBaselineMetricsAlphaManager,
)


RESOURCE_BASELINE_METRICS_COMMANDS = frozenset(
    {
        "resource-baseline-status",
        "resource-baseline-context",
        "resource-baseline-check",
        "resource-baseline-snapshot",
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


def handle_resource_baseline_metrics_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if command not in RESOURCE_BASELINE_METRICS_COMMANDS:
        return False

    if len(args) != 1:
        _usage_error(
            command=command,
            extras=args[1:],
        )

    owner = AuraResourceBaselineMetricsAlphaManager(
        project_root=Path.cwd()
    )

    dispatch = {
        "resource-baseline-status": owner.status,
        "resource-baseline-context": owner.context,
        "resource-baseline-check": owner.check,
        "resource-baseline-snapshot": owner.snapshot,
    }

    _print_json(dispatch[command]())
    return True


__all__ = [
    "RESOURCE_BASELINE_METRICS_COMMANDS",
    "handle_resource_baseline_metrics_command",
]
