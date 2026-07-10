"""CLI routing for Sprint 185 no-bind web shell inspection."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from .aura_control_center_web_shell_runtime_manager import (
    AuraControlCenterWebShellRuntimeManager,
    ControlCenterWebShellError,
)


STATUS_COMMAND = "control-center-web-shell-status"
MANIFEST_COMMAND = "control-center-web-shell-manifest"
SELF_TEST_COMMAND = "control-center-web-shell-self-test"

CONTROL_CENTER_WEB_SHELL_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        MANIFEST_COMMAND,
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


def handle_control_center_web_shell_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 185 no-bind shell commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in CONTROL_CENTER_WEB_SHELL_COMMANDS:
        return False

    if len(args) != 1:
        print(
            f"ERROR: {command} does not accept arguments.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    manager = AuraControlCenterWebShellRuntimeManager()

    try:
        if command == STATUS_COMMAND:
            _print_json(manager.status())
        elif command == MANIFEST_COMMAND:
            _print_json(manager.asset_manifest())
        else:
            _print_json(manager.self_test())
        return True
    except ControlCenterWebShellError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "CONTROL_CENTER_WEB_SHELL_COMMANDS",
    "handle_control_center_web_shell_command",
]
