"""CLI commands for Sprint 188 Interactive Control Center Chat."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from .aura_interactive_control_center_chat_runtime_manager import (
    AuraInteractiveControlCenterChatRuntimeManager,
    InteractiveControlCenterChatError,
)


STATUS_COMMAND = "interactive-chat-status"
CONTRACTS_COMMAND = "interactive-chat-contracts"
SELF_TEST_COMMAND = "interactive-chat-self-test"

INTERACTIVE_CHAT_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        CONTRACTS_COMMAND,
        SELF_TEST_COMMAND,
    }
)


def _print_json(payload: dict[str, Any]) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def _parser(command: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog=f"python3 main.py {command}",
        description=(
            "Inspect or validate the bounded Sprint 188 "
            "Interactive Control Center Chat runtime."
        ),
    )


def handle_interactive_chat_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 188 interactive-chat operator commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in INTERACTIVE_CHAT_COMMANDS:
        return False

    _parser(command).parse_args(list(args[1:]))

    try:
        manager = (
            AuraInteractiveControlCenterChatRuntimeManager()
        )
        if command == STATUS_COMMAND:
            payload = manager.status()
        elif command == CONTRACTS_COMMAND:
            payload = {
                **manager.contracts(),
                "safety_boundary": (
                    manager.safety_boundary()
                ),
            }
        else:
            payload = manager.self_test()

        _print_json(payload)
        return True
    except InteractiveControlCenterChatError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main(argv: Sequence[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    if not values:
        values = [STATUS_COMMAND]

    if handle_interactive_chat_command(values):
        return 0

    print(
        "ERROR: unknown interactive-chat command.",
        file=sys.stderr,
    )
    return 2


__all__ = [
    "INTERACTIVE_CHAT_COMMANDS",
    "handle_interactive_chat_command",
    "main",
]
