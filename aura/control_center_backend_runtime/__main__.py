"""Standalone entry point for Sprint 184 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_control_center_backend_runtime_manager import (
    AuraControlCenterBackendRuntimeManager,
    ControlCenterBackendError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.control_center_backend_runtime",
        description=(
            "AURA Sprint 184 read-only Control Center "
            "backend view-model core."
        ),
    )

    actions = parser.add_mutually_exclusive_group(
        required=True
    )
    actions.add_argument(
        "--status",
        action="store_true",
        help=(
            "Print the complete Control Center backend "
            "snapshot without opening a listener."
        ),
    )
    actions.add_argument(
        "--overview",
        action="store_true",
        help=(
            "Print only the Control Center overview "
            "view-model without opening a listener."
        ),
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Validate panel contracts, degraded visibility, "
            "and side-effect-free behavior."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraControlCenterBackendRuntimeManager()

    try:
        if args.status:
            payload = manager.snapshot()
        elif args.overview:
            snapshot = manager.snapshot()
            payload = manager.payload_for_route(
                "/api/control-center/overview",
                snapshot=snapshot,
            )
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
    except ControlCenterBackendError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
