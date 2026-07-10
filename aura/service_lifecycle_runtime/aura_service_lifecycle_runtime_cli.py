"""CLI routing for Sprint 182 Service Lifecycle Runtime."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import NoReturn

from .aura_service_lifecycle_runtime_manager import (
    AuraServiceLifecycleRuntimeManager,
    LifecycleError,
)
from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    build_browser_chat_session_lifecycle_manager,
)


STATUS_COMMAND = "service-lifecycle-status"
SELF_TEST_COMMAND = "service-lifecycle-self-test"
START_COMMAND = "service-lifecycle-start"

SERVICE_LIFECYCLE_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        SELF_TEST_COMMAND,
        START_COMMAND,
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


def _usage_error(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    print("Usage:", file=sys.stderr)
    print(
        f"  python3 main.py {STATUS_COMMAND}",
        file=sys.stderr,
    )
    print(
        f"  python3 main.py {SELF_TEST_COMMAND}",
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
    """Handle Sprint 182 lifecycle commands.

    Returns False only when the first argument is not owned by this router.
    A recognized command is fully handled or exits with a nonzero status.
    """

    if not args:
        return False

    command = str(args[0])
    if command not in SERVICE_LIFECYCLE_COMMANDS:
        return False

    extra = [str(item) for item in args[1:]]
    manager = build_browser_chat_session_lifecycle_manager()

    try:
        if command == STATUS_COMMAND:
            if extra:
                _usage_error(
                    f"{STATUS_COMMAND} does not accept arguments."
                )
            _print_json(manager.snapshot())
            return True

        if command == SELF_TEST_COMMAND:
            if extra:
                _usage_error(
                    f"{SELF_TEST_COMMAND} does not accept arguments."
                )
            _print_json(manager.self_test())
            return True

        if extra != ["--confirm-localhost"]:
            _usage_error(
                (
                    f"{START_COMMAND} requires the exact explicit "
                    "confirmation flag --confirm-localhost."
                )
            )

        config = manager.web_runtime.load_config()
        print("AURA Service Lifecycle Runtime Alpha")
        print("====================================")
        print("Lifecycle  : stopped -> starting -> running")
        print(f"Bind target: http://{config.host}:{config.port}")
        print("Mode       : safe_idle")
        print("Process    : foreground-only")
        print("Stop       : Ctrl+C, SIGINT, or SIGTERM")
        print("Background : DISABLED")
        print("Systemd    : DISABLED")
        print("Auto-start : DISABLED")
        print("Status API : 9 read-only payload routes")
        print("Control Center backend: 9 read-only routes")
        print("Web shell  : ENABLED / 3 dashboard assets")
        print("Local chat : ENABLED / 3 chat assets / 6 route contracts")
        print("Model bridge: DISABLED until Sprint 187")
        print("Browser launch: DISABLED")
        print()

        manager.run_foreground(confirmed=True)

        print("AURA Service Lifecycle Runtime stopped.")
        _print_json(manager.snapshot())
        return True
    except SystemExit:
        raise
    except LifecycleError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "SERVICE_LIFECYCLE_COMMANDS",
    "handle_service_lifecycle_command",
]
