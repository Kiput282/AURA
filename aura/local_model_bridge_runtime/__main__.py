"""Standalone no-bind entry point for Sprint 187 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.local_model_bridge_runtime",
        description=(
            "Inspect and validate AURA's localhost-only model bridge "
            "core without opening a listener or contacting a provider."
        ),
    )
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        "--status",
        action="store_true",
        help="Show the default disabled bridge state.",
    )
    actions.add_argument(
        "--contracts",
        action="store_true",
        help="Show supported local provider contracts.",
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Run isolated fake-transport validation for Ollama and "
            "OpenAI-compatible local providers."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraLocalModelBridgeRuntimeManager()

    try:
        if args.status:
            payload = manager.status()
        elif args.contracts:
            payload = manager.provider_contracts()
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
    except LocalModelBridgeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
