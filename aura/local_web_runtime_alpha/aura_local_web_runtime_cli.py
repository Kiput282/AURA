"""CLI routing for the Sprint 181 Local Web Runtime Alpha."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence

from .aura_local_web_runtime_alpha_manager import (
    AuraLocalWebRuntimeAlphaManager,
)


STATUS_COMMAND = "local-web-runtime-status"
SELF_TEST_COMMAND = "local-web-runtime-self-test"
START_COMMAND = "local-web-runtime-start"

LOCAL_WEB_RUNTIME_COMMANDS = frozenset(
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


def _usage_error(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    print(
        "Usage:",
        file=sys.stderr,
    )
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


def handle_local_web_runtime_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 181 runtime commands.

    Returns False only when the first argument is not owned by this router.
    A recognized command is fully handled or exits with a nonzero status.
    """

    if not args:
        return False

    command = str(args[0])
    if command not in LOCAL_WEB_RUNTIME_COMMANDS:
        return False

    extra = [str(item) for item in args[1:]]
    manager = AuraLocalWebRuntimeAlphaManager()

    try:
        if command == STATUS_COMMAND:
            if extra:
                _usage_error(
                    f"{STATUS_COMMAND} does not accept arguments."
                )
            _print_json(manager.status())
            return True

        if command == SELF_TEST_COMMAND:
            if extra:
                _usage_error(
                    f"{SELF_TEST_COMMAND} does not accept arguments."
                )
            _print_json(
                manager.self_test(configured_port=True)
            )
            return True

        if extra != ["--confirm-localhost"]:
            _usage_error(
                (
                    f"{START_COMMAND} requires the exact explicit "
                    "confirmation flag --confirm-localhost."
                )
            )

        manager.serve_forever(confirmed=True)
        return True
    except SystemExit:
        raise
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
