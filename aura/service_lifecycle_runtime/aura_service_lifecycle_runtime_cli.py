"""CLI routing for AURA Service Lifecycle Runtime."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import NoReturn

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    build_browser_chat_session_lifecycle_manager,
)

from .aura_service_lifecycle_determinism_alpha_manager import (
    AuraServiceLifecycleDeterminismAlphaManager,
)
from .aura_service_lifecycle_runtime_manager import (
    LifecycleError,
)


STATUS_COMMAND = "service-lifecycle-status"
SELF_TEST_COMMAND = "service-lifecycle-self-test"

DETERMINISM_STATUS_COMMAND = (
    "service-lifecycle-determinism-status"
)
DETERMINISM_CONTEXT_COMMAND = (
    "service-lifecycle-determinism-context"
)
DETERMINISM_CHECK_COMMAND = (
    "service-lifecycle-determinism-check"
)

START_COMMAND = "service-lifecycle-start"


DETERMINISM_COMMANDS = frozenset(
    {
        DETERMINISM_STATUS_COMMAND,
        DETERMINISM_CONTEXT_COMMAND,
        DETERMINISM_CHECK_COMMAND,
    }
)


SERVICE_LIFECYCLE_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        SELF_TEST_COMMAND,
        DETERMINISM_STATUS_COMMAND,
        DETERMINISM_CONTEXT_COMMAND,
        DETERMINISM_CHECK_COMMAND,
        START_COMMAND,
    }
)


def _print_json(
    payload: dict[str, object],
) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def _usage_error(
    message: str,
) -> NoReturn:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )

    print("Usage:", file=sys.stderr)

    for command in (
        STATUS_COMMAND,
        SELF_TEST_COMMAND,
        DETERMINISM_STATUS_COMMAND,
        DETERMINISM_CONTEXT_COMMAND,
        DETERMINISM_CHECK_COMMAND,
    ):
        print(
            f"  python3 main.py {command}",
            file=sys.stderr,
        )

    print(
        (
            f"  python3 main.py {START_COMMAND} "
            "--confirm-localhost"
        ),
        file=sys.stderr,
    )

    raise SystemExit(2)


def handle_service_lifecycle_command(
    args: Sequence[str],
) -> bool:
    """Route only commands owned by the lifecycle package."""

    if not args:
        return False

    command = str(args[0])

    if command not in SERVICE_LIFECYCLE_COMMANDS:
        return False

    extra = [
        str(item)
        for item in args[1:]
    ]

    try:
        if command in DETERMINISM_COMMANDS:
            if extra:
                _usage_error(
                    f"{command} does not accept arguments."
                )

            owner = (
                AuraServiceLifecycleDeterminismAlphaManager()
            )

            if command == DETERMINISM_STATUS_COMMAND:
                _print_json(owner.status())
                return True

            if command == DETERMINISM_CONTEXT_COMMAND:
                _print_json(owner.context())
                return True

            _print_json(owner.check())
            return True

        manager = (
            build_browser_chat_session_lifecycle_manager()
        )

        if command == STATUS_COMMAND:
            if extra:
                _usage_error(
                    f"{STATUS_COMMAND} "
                    "does not accept arguments."
                )

            _print_json(manager.snapshot())
            return True

        if command == SELF_TEST_COMMAND:
            if extra:
                _usage_error(
                    f"{SELF_TEST_COMMAND} "
                    "does not accept arguments."
                )

            _print_json(manager.self_test())
            return True

        if extra != ["--confirm-localhost"]:
            _usage_error(
                (
                    f"{START_COMMAND} requires the exact "
                    "explicit confirmation flag "
                    "--confirm-localhost."
                )
            )

        config = manager.web_runtime.load_config()

        print("AURA Service Lifecycle Runtime Alpha")
        print("====================================")
        print(
            "Lifecycle : "
            "stopped -> starting -> running"
        )
        print(
            f"Bind target: "
            f"http://{config.host}:{config.port}"
        )
        print("Mode      : safe_idle")
        print("Process   : foreground-only")
        print(
            "Stop      : "
            "Ctrl+C, SIGINT, or SIGTERM"
        )
        print("Background: DISABLED")
        print("Systemd   : DISABLED")
        print("Auto-start: DISABLED")
        print(
            "Status API: "
            "9 read-only payload routes"
        )
        print(
            "Control Center backend: "
            "9 read-only routes"
        )
        print(
            "Web shell : "
            "ENABLED / 3 dashboard assets"
        )
        print(
            "Local chat: "
            "ENABLED / 3 chat assets / "
            "7 route contracts"
        )
        print(
            "Model bridge: "
            "READY / 2 model routes / "
            "interactive chat ready / "
            "disabled by default"
        )
        print(
            "Visibility: "
            "READY / 4 GET-only APIs / "
            "3 assets / read-only"
        )
        print("Browser launch: DISABLED")
        print()

        manager.run_foreground(
            confirmed=True
        )

        print(
            "AURA Service Lifecycle Runtime stopped."
        )

        _print_json(manager.snapshot())

        return True

    except SystemExit:
        raise

    except LifecycleError as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        raise SystemExit(1) from exc


__all__ = [
    "DETERMINISM_COMMANDS",
    "SERVICE_LIFECYCLE_COMMANDS",
    "handle_service_lifecycle_command",
]
