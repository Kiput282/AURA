from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .local_model_router_activation_alpha_manager import (
    LocalModelRouterActivationAlphaManager,
)


LOCAL_MODEL_ROUTER_ACTIVATION_COMMANDS = frozenset(
    {
        "local-model-router-activation-status",
        "local-model-router-activation-context",
        "local-model-router-activation-check",
        "local-model-router-activation-review",
        "local-model-router-route-preview",
        "local-model-router-profile-preview",
        "local-model-router-request-preview",
        "local-model-router-isolated-rehearsal",
    }
)


def _print_json(packet: dict[str, Any]) -> None:
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        )
    )


def _usage_error(
    command: str,
    extras: Sequence[str],
    expected: str,
) -> NoReturn:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "invalid_arguments",
                "command": command,
                "expected": expected,
                "provided_arguments": list(
                    extras
                ),
                "route_selection_performed": False,
                "model_request_performed": False,
                "network_connection_opened": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_local_model_router_activation_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in (
            LOCAL_MODEL_ROUTER_ACTIVATION_COMMANDS
        )
    ):
        return False

    command = args[0]
    extras = list(args[1:])
    owner = LocalModelRouterActivationAlphaManager(
        project_root=Path.cwd()
    )

    target_commands = {
        "local-model-router-route-preview",
        "local-model-router-profile-preview",
        "local-model-router-request-preview",
    }

    if command in target_commands:
        if len(extras) != 1:
            _usage_error(
                command,
                extras,
                "<exact-route-target>",
            )
        target = extras[0]
    else:
        if extras:
            _usage_error(
                command,
                extras,
                "<no-arguments>",
            )
        target = None

    if command.endswith("-status"):
        packet = owner.status()
    elif command.endswith("-context"):
        packet = owner.context()
    elif command.endswith("-check"):
        packet = owner.check()
    elif command.endswith("-review"):
        packet = owner.review()
    elif command.endswith("-route-preview"):
        packet = owner.route_preview(
            target or ""
        )
    elif command.endswith("-profile-preview"):
        packet = owner.profile_preview(
            target or ""
        )
    elif command.endswith("-request-preview"):
        packet = owner.request_preview(
            target or ""
        )
    elif command.endswith("-isolated-rehearsal"):
        packet = owner.isolated_rehearsal()
    else:
        return False

    _print_json(packet)
    return True
