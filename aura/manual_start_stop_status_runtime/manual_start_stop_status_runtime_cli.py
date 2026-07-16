from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .manual_start_stop_status_runtime_alpha_manager import (
    ManualStartStopStatusRuntimeAlphaManager,
)
from .manual_start_stop_status_runtime_executor import (
    ManualRuntimeControlError,
)


MANUAL_START_STOP_STATUS_RUNTIME_COMMANDS = frozenset(
    {
        "manual-start-stop-status-runtime-start",
        "manual-start-stop-status-runtime-stop",
        "manual-start-stop-status-runtime-status",
        "manual-start-stop-status-runtime-context",
        "manual-start-stop-status-runtime-check",
        "manual-start-stop-status-runtime-review",
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


def _print_error(
    packet: dict[str, Any],
) -> None:
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )


def _usage_error(
    command: str,
    extras: Sequence[str],
    expected: Sequence[str],
) -> "NoReturn":
    _print_error(
        {
            "ok": False,
            "error": "unexpected_arguments",
            "command": command,
            "provided_arguments": list(extras),
            "expected_arguments": list(
                expected
            ),
        }
    )
    raise SystemExit(2)


def _require_exact_flags(
    command: str,
    extras: Sequence[str],
    expected: Sequence[str],
) -> None:
    if (
        len(extras) != len(expected)
        or len(set(extras)) != len(extras)
        or set(extras) != set(expected)
    ):
        _usage_error(
            command,
            extras,
            expected,
        )


def handle_manual_start_stop_status_runtime_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = args[0]

    if (
        command
        not in MANUAL_START_STOP_STATUS_RUNTIME_COMMANDS
    ):
        return False

    extras = list(args[1:])
    owner = ManualStartStopStatusRuntimeAlphaManager(
        project_root=Path.cwd()
    )

    try:
        if command == (
            "manual-start-stop-status-runtime-start"
        ):
            _require_exact_flags(
                command,
                extras,
                (
                    "--approve-start",
                    "--confirm-localhost",
                ),
            )
            _print_json(
                owner.start(
                    approved=True,
                    confirmed_localhost=True,
                )
            )
            return True

        if command == (
            "manual-start-stop-status-runtime-stop"
        ):
            _require_exact_flags(
                command,
                extras,
                ("--approve-stop",),
            )
            _print_json(
                owner.stop(
                    approved=True
                )
            )
            return True

        if extras:
            _usage_error(
                command,
                extras,
                (),
            )

        dispatch = {
            (
                "manual-start-stop-status-runtime-status"
            ): owner.status,
            (
                "manual-start-stop-status-runtime-context"
            ): owner.context,
            (
                "manual-start-stop-status-runtime-check"
            ): owner.check,
            (
                "manual-start-stop-status-runtime-review"
            ): owner.review,
        }

        _print_json(
            dispatch[command]()
        )
        return True
    except ManualRuntimeControlError as exc:
        packet = exc.packet()
        packet["command"] = command
        _print_error(packet)
        raise SystemExit(3) from exc


__all__ = [
    "MANUAL_START_STOP_STATUS_RUNTIME_COMMANDS",
    "handle_manual_start_stop_status_runtime_command",
]
