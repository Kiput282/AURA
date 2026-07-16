from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .restart_logs_failure_visibility_alpha_manager import (
    RestartLogsFailureVisibilityAlphaManager,
)
from .restart_logs_failure_visibility_executor import (
    RestartLogsFailureVisibilityError,
)


RESTART_LOGS_FAILURE_VISIBILITY_COMMANDS = frozenset(
    {
        "restart-logs-failure-visibility-status",
        "restart-logs-failure-visibility-context",
        "restart-logs-failure-visibility-check",
        "restart-logs-failure-visibility-review",
        "restart-logs-failure-visibility-logs",
        "restart-logs-failure-visibility-failures",
        "restart-logs-failure-visibility-restart-preview",
        "restart-logs-failure-visibility-tail",
        "restart-logs-failure-visibility-restart",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(json.dumps(packet, indent=2, sort_keys=True))


def _print_error(packet: dict[str, Any]) -> None:
    print(
        json.dumps(packet, indent=2, sort_keys=True),
        file=sys.stderr,
    )


def _usage_error(
    command: str,
    extras: Sequence[str],
    expected: Sequence[str],
) -> NoReturn:
    _print_error(
        {
            "ok": False,
            "error": "unexpected_arguments",
            "command": command,
            "provided_arguments": list(extras),
            "expected_arguments": list(expected),
        }
    )
    raise SystemExit(2)


def _require_exact(
    command: str,
    extras: Sequence[str],
    expected: Sequence[str],
) -> None:
    if list(extras) != list(expected):
        _usage_error(command, extras, expected)


def _parse_tail(
    command: str,
    extras: Sequence[str],
) -> tuple[str, int]:
    shape = [
        "--source",
        "<active|latest-rotated|runtime>",
        "--lines",
        "<1-200>",
    ]
    if (
        len(extras) != 4
        or extras[0] != "--source"
        or extras[2] != "--lines"
        or extras[1]
        not in {"active", "latest-rotated", "runtime"}
    ):
        _usage_error(command, extras, shape)
    try:
        lines = int(extras[3])
    except ValueError:
        _usage_error(command, extras, shape)
    if not 1 <= lines <= 200:
        _usage_error(command, extras, shape)
    return extras[1], lines


def handle_restart_logs_failure_visibility_command(
    args: Sequence[str],
) -> bool:
    if not args or args[0] not in RESTART_LOGS_FAILURE_VISIBILITY_COMMANDS:
        return False

    command = args[0]
    extras = list(args[1:])
    owner = RestartLogsFailureVisibilityAlphaManager(
        project_root=Path.cwd()
    )

    try:
        if command.endswith("-restart"):
            _require_exact(
                command,
                extras,
                ["--approve-restart", "--confirm-localhost"],
            )
            _print_json(owner.restart())
        elif command.endswith("-tail"):
            source, lines = _parse_tail(command, extras)
            _print_json(owner.tail(source=source, lines=lines))
        else:
            _require_exact(command, extras, [])
            if command.endswith("-status"):
                _print_json(owner.status())
            elif command.endswith("-context"):
                _print_json(owner.context())
            elif command.endswith("-check"):
                _print_json(owner.check())
            elif command.endswith("-review"):
                _print_json(owner.review())
            elif command.endswith("-logs"):
                _print_json(owner.logs())
            elif command.endswith("-failures"):
                _print_json(owner.failures())
            elif command.endswith("-restart-preview"):
                _print_json(owner.restart_preview())
            else:
                return False
    except RestartLogsFailureVisibilityError as exc:
        _print_error(exc.packet())
        raise SystemExit(1) from exc

    return True
