"""Standalone no-bind entry point for Sprint 186 Part A."""

from __future__ import annotations

import argparse
import json
import sys

from .aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
    BrowserChatSessionError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m aura.browser_chat_session_runtime",
        description=(
            "Inspect and validate AURA's local browser chat "
            "session core without opening a listener or writing "
            "to canonical project session storage."
        ),
    )

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument(
        "--status",
        action="store_true",
        help="Inspect canonical local chat-session storage.",
    )
    actions.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Validate creation, persistence, reload, submission, "
            "response delivery, confirmation, limits, and safety "
            "inside an isolated temporary directory."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manager = AuraBrowserChatSessionRuntimeManager()

    try:
        payload = (
            manager.status()
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
    except BrowserChatSessionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
