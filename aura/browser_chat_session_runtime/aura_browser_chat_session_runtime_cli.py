"""Main CLI routing for Sprint 186 no-bind inspection."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from .aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
    BrowserChatSessionError,
)
from .aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
    BrowserChatWebSurfaceError,
)


STATUS_COMMAND = "browser-chat-session-status"
SELF_TEST_COMMAND = "browser-chat-session-self-test"
WEB_STATUS_COMMAND = "browser-chat-web-status"
WEB_SELF_TEST_COMMAND = "browser-chat-web-self-test"

BROWSER_CHAT_SESSION_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        SELF_TEST_COMMAND,
        WEB_STATUS_COMMAND,
        WEB_SELF_TEST_COMMAND,
    }
)


def _print_json(payload: dict[str, object]) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def handle_browser_chat_session_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 186 no-bind chat inspection commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in BROWSER_CHAT_SESSION_COMMANDS:
        return False

    if len(args) != 1:
        print(
            f"ERROR: {command} does not accept arguments.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        if command == STATUS_COMMAND:
            payload = (
                AuraBrowserChatSessionRuntimeManager()
                .status()
            )
        elif command == SELF_TEST_COMMAND:
            payload = (
                AuraBrowserChatSessionRuntimeManager()
                .self_test()
            )
        elif command == WEB_STATUS_COMMAND:
            payload = AuraBrowserChatWebSurfaceManager().status()
        else:
            payload = (
                AuraBrowserChatWebSurfaceManager()
                .self_test()
            )
        _print_json(payload)
        return True
    except (
        BrowserChatSessionError,
        BrowserChatWebSurfaceError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "BROWSER_CHAT_SESSION_COMMANDS",
    "handle_browser_chat_session_command",
]
