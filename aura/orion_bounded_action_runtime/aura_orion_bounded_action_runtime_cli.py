"""CLI adapter for the Sprint 278 bounded ORION action runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aura.orion_bounded_action_runtime import (
    AuraOrionBoundedActionRuntimeManager,
)


def _print_json(payload: dict[str, Any]) -> None:
    print(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def _manager(
    project_root: Path,
) -> AuraOrionBoundedActionRuntimeManager:
    return AuraOrionBoundedActionRuntimeManager(
        project_root=project_root,
    )


def handle_orion_bounded_action_command(
    raw_args: list[str],
    *,
    project_root: Path,
) -> bool:
    """Handle read-only Sprint 278 status, inspect, and self-test commands."""

    if not raw_args:
        return False

    command = raw_args[0]
    supported = {
        "orion-bounded-action-status",
        "orion-bounded-action-inspect",
        "orion-bounded-action-self-test",
    }
    if command not in supported:
        return False
    if len(raw_args) != 1:
        raise ValueError(
            f"{command} does not accept additional arguments."
        )

    manager = _manager(project_root)
    if command == "orion-bounded-action-status":
        _print_json(manager.status())
        return True
    if command == "orion-bounded-action-inspect":
        _print_json(manager.inspect_runtime())
        return True

    _print_json(manager.self_test())
    return True
