"""CLI commands for Sprint 261 roadmap reconfirmation."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any
import json
import sys

from .roadmap_reconfirmation_planner import (
    RoadmapReconfirmationPlanner,
)


ROADMAP_RECONFIRMATION_COMMANDS = (
    "roadmap-reconfirmation-status",
    "roadmap-reconfirmation-context",
    "roadmap-reconfirmation-check",
    "roadmap-reconfirmation-review",
    "roadmap-reconfirmation-preview",
    "roadmap-live-acceptance-policy",
    "roadmap-gap-ownership",
    "roadmap-reconfirmation-isolated-rehearsal",
)


def _safe_error(
    command: str,
    message: str,
) -> dict[str, Any]:
    return {
        "status": "rejected",
        "command": command,
        "error": message,
        "source_mutated": False,
        "runtime_activated": False,
        "network_connection_opened": False,
        "repository_committed": False,
        "repository_pushed": False,
    }


def handle_roadmap_reconfirmation_after_v1_2_0_command(
    args: Sequence[str],
) -> bool:
    """Handle one exact Sprint 261 command."""

    if not args:
        return False

    command = str(args[0])

    if command not in ROADMAP_RECONFIRMATION_COMMANDS:
        return False

    if len(args) != 1:
        print(
            json.dumps(
                _safe_error(
                    command,
                    "This command does not accept arguments.",
                ),
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    planner = RoadmapReconfirmationPlanner(
        project_root=Path.cwd()
    )
    handlers = {
        "roadmap-reconfirmation-status": (
            planner.status
        ),
        "roadmap-reconfirmation-context": (
            planner.context
        ),
        "roadmap-reconfirmation-check": (
            planner.check
        ),
        "roadmap-reconfirmation-review": (
            planner.review
        ),
        "roadmap-reconfirmation-preview": (
            planner.preview
        ),
        "roadmap-live-acceptance-policy": (
            planner.live_acceptance_policy
        ),
        "roadmap-gap-ownership": (
            planner.gap_ownership
        ),
        "roadmap-reconfirmation-isolated-rehearsal": (
            planner.isolated_rehearsal
        ),
    }

    print(
        json.dumps(
            handlers[command](),
            indent=2,
            sort_keys=True,
        )
    )
    return True
