from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .persistent_local_chat_session_activation_alpha_manager import (
    PersistentLocalChatSessionActivationAlphaManager,
)


PERSISTENT_LOCAL_CHAT_SESSION_ACTIVATION_COMMANDS = frozenset(
    {
        "persistent-local-chat-session-activation-status",
        "persistent-local-chat-session-activation-context",
        "persistent-local-chat-session-activation-check",
        "persistent-local-chat-session-activation-review",
        "persistent-local-chat-session-storage-posture",
        "persistent-local-chat-session-history-preview",
        "persistent-local-chat-session-migration-preview",
        "persistent-local-chat-session-isolated-rehearsal",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(json.dumps(packet, indent=2, sort_keys=True))


def _usage_error(
    command: str,
    extras: Sequence[str],
) -> NoReturn:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "unexpected_arguments",
                "command": command,
                "provided_arguments": list(extras),
                "expected_arguments": [],
                "canonical_session_mutation_available": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_persistent_local_chat_session_activation_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in PERSISTENT_LOCAL_CHAT_SESSION_ACTIVATION_COMMANDS
    ):
        return False

    command = args[0]
    extras = list(args[1:])

    if extras:
        _usage_error(command, extras)

    owner = (
        PersistentLocalChatSessionActivationAlphaManager(
            project_root=Path.cwd()
        )
    )

    if command.endswith("-status"):
        packet = owner.status()
    elif command.endswith("-context"):
        packet = owner.context()
    elif command.endswith("-check"):
        packet = owner.check()
    elif command.endswith("-review"):
        packet = owner.review()
    elif command.endswith("-storage-posture"):
        packet = owner.storage_posture()
    elif command.endswith("-history-preview"):
        packet = owner.history_preview()
    elif command.endswith("-migration-preview"):
        packet = owner.migration_preview()
    elif command.endswith("-isolated-rehearsal"):
        packet = owner.isolated_rehearsal()
    else:
        return False

    _print_json(packet)
    return True
