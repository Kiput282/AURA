"""Standalone entry point for Sprint 183 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_health_status_api_runtime_manager import (
    AuraHealthStatusApiRuntimeManager,
    HealthStatusAggregationError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.health_status_api_runtime",
        description=(
            "AURA Sprint 183 read-only health and status "
            "aggregation core."
        ),
    )

    actions = parser.add_mutually_exclusive_group(
        required=True
    )
    actions.add_argument(
        "--status",
        action="store_true",
        help=(
            "Print the full read-only status snapshot "
            "without opening a listener."
        ),
    )
    actions.add_argument(
        "--health",
        action="store_true",
        help=(
            "Print the compact read-only health payload "
            "without opening a listener."
        ),
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Validate healthy, degraded, route-contract, "
            "and side-effect-free behavior."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraHealthStatusApiRuntimeManager()

    try:
        if args.status:
            payload = manager.snapshot()
        elif args.health:
            payload = manager.health_payload()
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
    except HealthStatusAggregationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
