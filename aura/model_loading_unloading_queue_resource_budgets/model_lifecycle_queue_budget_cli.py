from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .model_lifecycle_queue_budget_alpha_manager import (
    ModelLifecycleQueueBudgetAlphaManager,
)


MODEL_LIFECYCLE_QUEUE_BUDGET_COMMANDS = frozenset(
    {
        "model-lifecycle-queue-budget-status",
        "model-lifecycle-queue-budget-context",
        "model-lifecycle-queue-budget-check",
        "model-lifecycle-queue-budget-review",
        "model-lifecycle-preview",
        "model-lifecycle-queue-preview",
        "model-resource-budget-preview",
        "model-lifecycle-queue-budget-isolated-rehearsal",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(json.dumps(packet, indent=2, sort_keys=True))


def _usage_error(
    command: str,
    extras: Sequence[str],
    expected: str,
) -> NoReturn:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "invalid_arguments",
                "command": command,
                "expected": expected,
                "provided_arguments": list(extras),
                "network_connection_opened": False,
                "model_lifecycle_executed": False,
                "queue_mutated": False,
                "resource_budget_mutated": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_model_lifecycle_queue_budget_command(
    args: Sequence[str],
) -> bool:
    if not args or args[0] not in MODEL_LIFECYCLE_QUEUE_BUDGET_COMMANDS:
        return False

    command = args[0]
    extras = list(args[1:])
    owner = ModelLifecycleQueueBudgetAlphaManager(
        project_root=Path.cwd()
    )

    if command == "model-lifecycle-preview":
        if len(extras) != 1:
            _usage_error(command, extras, "<load|status|release>")
        action = extras[0]
    else:
        if extras:
            _usage_error(command, extras, "<no-arguments>")
        action = None

    if command.endswith("-status"):
        packet = owner.status()
    elif command.endswith("-context"):
        packet = owner.context()
    elif command.endswith("-check"):
        packet = owner.check()
    elif command.endswith("-review"):
        packet = owner.review()
    elif command == "model-lifecycle-preview":
        packet = owner.lifecycle_preview(action or "")
    elif command == "model-lifecycle-queue-preview":
        packet = owner.queue_preview()
    elif command == "model-resource-budget-preview":
        packet = owner.resource_budget_preview()
    elif command.endswith("-isolated-rehearsal"):
        packet = owner.isolated_rehearsal()
    else:
        return False

    _print_json(packet)
    return True
