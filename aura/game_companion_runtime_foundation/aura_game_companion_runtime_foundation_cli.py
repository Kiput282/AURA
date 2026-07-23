"""CLI adapter for the Sprint 281 Game Companion runtime foundation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .aura_game_companion_runtime_foundation_manager import (
    AuraGameCompanionRuntimeFoundationManager,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aura.game_companion_runtime_foundation",
        description=(
            "Inspect the side-effect-free Sprint 281 Game Companion "
            "runtime foundation."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")
    subparsers.add_parser("inspect")
    subparsers.add_parser("self-test")

    proposal = subparsers.add_parser("propose")
    proposal.add_argument("--game", required=True, dest="game_id")
    proposal.add_argument("--mode", required=True, dest="mode_id")

    return parser


def main(raw_args: list[str] | None = None) -> int:
    args = build_parser().parse_args(raw_args)
    project_root = Path(__file__).resolve().parents[2]
    manager = AuraGameCompanionRuntimeFoundationManager(
        project_root=project_root
    )

    if args.command == "status":
        _print_json(manager.status())
        return 0
    if args.command == "inspect":
        _print_json(manager.inspect_foundation())
        return 0
    if args.command == "self-test":
        _print_json(manager.self_test())
        return 0
    if args.command == "propose":
        _print_json(
            manager.build_session_proposal(
                game_id=args.game_id,
                mode_id=args.mode_id,
            )
        )
        return 0

    raise AssertionError(f"unhandled command: {args.command}")
