"""CLI routing for Sprint 184 Control Center backend inspection."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from .aura_control_center_backend_runtime_manager import (
    AuraControlCenterBackendRuntimeManager,
    ControlCenterBackendError,
)


STATUS_COMMAND = "control-center-backend-status"
OVERVIEW_COMMAND = "control-center-backend-overview"
SELF_TEST_COMMAND = "control-center-backend-self-test"

CONTROL_CENTER_BACKEND_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        OVERVIEW_COMMAND,
        SELF_TEST_COMMAND,
    }
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


def handle_control_center_backend_command(
    args: Sequence[str],
) -> bool:
    """Handle no-bind Sprint 184 backend inspection commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in CONTROL_CENTER_BACKEND_COMMANDS:
        return False

    if len(args) != 1:
        print(
            f"ERROR: {command} does not accept arguments.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    manager = AuraControlCenterBackendRuntimeManager()

    try:
        if command == STATUS_COMMAND:
            _print_json(manager.snapshot())
        elif command == OVERVIEW_COMMAND:
            snapshot = manager.snapshot()
            _print_json(
                manager.payload_for_route(
                    "/api/control-center/overview",
                    snapshot=snapshot,
                )
            )
        else:
            _print_json(manager.self_test())
        return True
    except ControlCenterBackendError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "CONTROL_CENTER_BACKEND_COMMANDS",
    "handle_control_center_backend_command",
]
