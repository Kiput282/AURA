"""CLI for Sprint 289 overlay session-status integration."""

import argparse
import json
from pathlib import Path
from typing import Sequence

from .aura_orion_overlay_session_status_integration_manager import (
    AuraOrionOverlaySessionStatusIntegrationManager,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m aura.orion_overlay_session_status_runtime"
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument(
        "command",
        choices=("status", "inspect", "self-test"),
    )
    args = parser.parse_args(argv)

    manager = AuraOrionOverlaySessionStatusIntegrationManager(
        project_root=Path(args.project_root)
    )
    payload = (
        manager.status()
        if args.command == "status"
        else manager.inspect_runtime()
        if args.command == "inspect"
        else manager.self_test()
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("status") != "FAILED" else 1
