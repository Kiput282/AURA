"""CLI commands for Sprint 190 Local Interaction Runtime Stabilization."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from .aura_local_interaction_runtime_stabilization_manager import (
    AuraLocalInteractionRuntimeStabilizationManager,
    LocalInteractionRuntimeStabilizationError,
)


STATUS_COMMAND = (
    "local-interaction-runtime-stabilization-status"
)
CONTEXT_COMMAND = (
    "local-interaction-runtime-stabilization-context"
)
REVIEW_COMMAND = (
    "local-interaction-runtime-stabilization-review"
)
SELF_TEST_COMMAND = (
    "local-interaction-runtime-stabilization-self-test"
)

LOCAL_INTERACTION_RUNTIME_STABILIZATION_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        CONTEXT_COMMAND,
        REVIEW_COMMAND,
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
            "Inspect or validate the Sprint 190 Local "
            "Interaction Runtime stabilization checkpoint."
        ),
    )


def handle_local_interaction_runtime_stabilization_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 190 stabilization commands."""

    if not args:
        return False

    command = str(args[0])
    if (
        command
        not in LOCAL_INTERACTION_RUNTIME_STABILIZATION_COMMANDS
    ):
        return False

    _parser(command).parse_args(list(args[1:]))

    try:
        manager = (
            AuraLocalInteractionRuntimeStabilizationManager()
        )

        if command == STATUS_COMMAND:
            payload = manager.status()
        elif command == CONTEXT_COMMAND:
            payload = manager.context()
        elif command == REVIEW_COMMAND:
            payload = manager.run_stabilization_review()
        else:
            payload = manager.self_test()

        _print_json(payload)
        return True
    except LocalInteractionRuntimeStabilizationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main(argv: Sequence[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    if not values:
        values = [STATUS_COMMAND]

    if handle_local_interaction_runtime_stabilization_command(
        values
    ):
        return 0

    print(
        "ERROR: unknown local interaction stabilization command.",
        file=sys.stderr,
    )
    return 2


__all__ = [
    "LOCAL_INTERACTION_RUNTIME_STABILIZATION_COMMANDS",
    "handle_local_interaction_runtime_stabilization_command",
    "main",
]
