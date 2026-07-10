"""CLI routing for Sprint 183 health and status aggregation."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from .aura_health_status_api_runtime_manager import (
    AuraHealthStatusApiRuntimeManager,
    HealthStatusAggregationError,
)

STATUS_COMMAND = "health-status-api-status"
HEALTH_COMMAND = "health-status-api-health"
SELF_TEST_COMMAND = "health-status-api-self-test"
HEALTH_STATUS_API_COMMANDS = frozenset(
    {STATUS_COMMAND, HEALTH_COMMAND, SELF_TEST_COMMAND}
)


def _print_json(payload: dict[str, object]) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def handle_health_status_api_command(args: Sequence[str]) -> bool:
    if not args:
        return False
    command = str(args[0])
    if command not in HEALTH_STATUS_API_COMMANDS:
        return False
    if len(args) != 1:
        print(f"ERROR: {command} does not accept arguments.", file=sys.stderr)
        raise SystemExit(2)

    manager = AuraHealthStatusApiRuntimeManager()
    try:
        if command == STATUS_COMMAND:
            _print_json(manager.snapshot())
        elif command == HEALTH_COMMAND:
            _print_json(manager.health_payload())
        else:
            _print_json(manager.self_test())
        return True
    except HealthStatusAggregationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "HEALTH_STATUS_API_COMMANDS",
    "handle_health_status_api_command",
]
