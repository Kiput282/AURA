"""Standalone validation entry point for Sprint 182 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_service_lifecycle_runtime_manager import (
    AuraServiceLifecycleRuntimeManager,
    LifecycleError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.service_lifecycle_runtime",
        description=(
            "AURA Sprint 182 deterministic lifecycle runtime core."
        ),
    )

    actions = parser.add_mutually_exclusive_group(
        required=True
    )
    actions.add_argument(
        "--status",
        action="store_true",
        help=(
            "Print a stopped lifecycle snapshot without "
            "starting a listener."
        ),
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Exercise deterministic transitions, clean stop, "
            "single-listener enforcement, port conflict handling, "
            "and startup rollback."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraServiceLifecycleRuntimeManager()

    try:
        payload = (
            manager.snapshot()
            if args.status
            else manager.self_test()
        )
        print(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except LifecycleError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
