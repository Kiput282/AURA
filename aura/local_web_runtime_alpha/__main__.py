"""Command entry point for AURA Local Web Runtime Alpha."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_local_web_runtime_alpha_manager import (
    AuraLocalWebRuntimeAlphaManager,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.local_web_runtime_alpha",
        description=(
            "AURA Sprint 181 localhost-only foreground web runtime alpha."
        ),
    )

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--status",
        action="store_true",
        help="Validate configuration and print status without binding a port.",
    )
    action.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Temporarily bind the configured localhost port, exercise all "
            "read-only routes, verify mutation blocking, then shut down."
        ),
    )
    action.add_argument(
        "--confirm-localhost",
        action="store_true",
        help=(
            "Explicitly confirm and start the foreground localhost-only "
            "runtime. Stop it with Ctrl+C."
        ),
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    manager = AuraLocalWebRuntimeAlphaManager()

    try:
        if args.status:
            print(
                json.dumps(
                    manager.status(),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0

        if args.self_test:
            print(
                json.dumps(
                    manager.self_test(configured_port=True),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0

        manager.serve_forever(confirmed=args.confirm_localhost)
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
