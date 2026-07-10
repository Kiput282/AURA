"""Standalone no-bind entry point for Sprint 185 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_control_center_web_shell_runtime_manager import (
    AuraControlCenterWebShellRuntimeManager,
    ControlCenterWebShellError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.control_center_web_shell_runtime",
        description=(
            "AURA Sprint 185 static Control Center Web Shell "
            "inspection without opening a listener."
        ),
    )

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        "--status",
        action="store_true",
        help="Print shell status and safety boundaries.",
    )
    actions.add_argument(
        "--manifest",
        action="store_true",
        help="Print the local static-asset manifest.",
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Validate HTML, CSS, JavaScript, accessibility, "
            "route, and read-only contracts."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraControlCenterWebShellRuntimeManager()

    try:
        if args.status:
            payload = manager.status()
        elif args.manifest:
            payload = manager.asset_manifest()
        else:
            payload = manager.self_test()

        print(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except ControlCenterWebShellError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
