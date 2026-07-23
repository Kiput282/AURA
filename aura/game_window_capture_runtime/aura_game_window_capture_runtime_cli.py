"""CLI for Sprint 283 game-window capture runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .aura_game_window_capture_runtime_manager import (
    AuraGameWindowCaptureRuntimeManager,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m aura.game_window_capture_runtime",
        description=(
            "Inspect the bounded Sprint 283 one-shot game-window "
            "capture contract."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "command",
        choices=(
            "status",
            "inspect",
            "self-test",
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = AuraGameWindowCaptureRuntimeManager(
        project_root=args.project_root
    )
    operations = {
        "status": manager.status,
        "inspect": manager.inspect_runtime,
        "self-test": manager.self_test,
    }
    payload = operations[args.command]()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
