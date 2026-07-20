"""CLI adapter for the Sprint 273 ORION agent foundation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .aura_orion_agent_foundation_manager import (
    AuraOrionAgentFoundationManager,
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


def handle_orion_agent_foundation_command(
    raw_args: list[str],
    *,
    project_root: Path,
) -> bool:
    """Handle foundation-only ORION agent inspection commands."""

    if not raw_args:
        return False

    command = raw_args[0]
    supported = {
        "orion-agent-foundation-status",
        "orion-agent-foundation-inspect",
        "orion-agent-foundation-self-test",
    }
    if command not in supported:
        return False

    manager = AuraOrionAgentFoundationManager(
        project_root=project_root
    )

    if command == "orion-agent-foundation-status":
        _print_json(manager.status())
        return True

    if command == "orion-agent-foundation-inspect":
        _print_json(manager.inspect_foundation())
        return True

    _print_json(manager.self_test())
    return True
