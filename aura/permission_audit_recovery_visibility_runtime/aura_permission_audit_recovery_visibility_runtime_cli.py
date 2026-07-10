"""CLI commands for Sprint 189 permission/audit/recovery visibility."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from .aura_permission_audit_recovery_visibility_runtime_manager import (
    AuraPermissionAuditRecoveryVisibilityRuntimeManager,
    PermissionAuditRecoveryVisibilityError,
)
from .aura_permission_audit_recovery_web_surface_manager import (
    AuraPermissionAuditRecoveryWebSurfaceManager,
    PermissionAuditRecoveryWebSurfaceError,
)


STATUS_COMMAND = "permission-audit-recovery-status"
SNAPSHOT_COMMAND = "permission-audit-recovery-snapshot"
SELF_TEST_COMMAND = "permission-audit-recovery-self-test"
WEB_STATUS_COMMAND = "permission-audit-recovery-web-status"
WEB_SELF_TEST_COMMAND = "permission-audit-recovery-web-self-test"

PERMISSION_AUDIT_RECOVERY_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        SNAPSHOT_COMMAND,
        SELF_TEST_COMMAND,
        WEB_STATUS_COMMAND,
        WEB_SELF_TEST_COMMAND,
    }
)


def _print_json(payload: dict[str, Any]) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def _parser(command: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog=f"python3 main.py {command}",
        description=(
            "Inspect the read-only Sprint 189 permission, audit, "
            "and recovery visibility core."
        ),
    )


def handle_permission_audit_recovery_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 189 read-only visibility commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in PERMISSION_AUDIT_RECOVERY_COMMANDS:
        return False

    _parser(command).parse_args(list(args[1:]))

    try:
        manager = (
            AuraPermissionAuditRecoveryVisibilityRuntimeManager()
        )
        web_manager = (
            AuraPermissionAuditRecoveryWebSurfaceManager()
        )
        if command == STATUS_COMMAND:
            payload = manager.status()
        elif command == SNAPSHOT_COMMAND:
            payload = manager.visibility_snapshot()
        elif command == SELF_TEST_COMMAND:
            payload = manager.self_test()
        elif command == WEB_STATUS_COMMAND:
            payload = web_manager.status()
        else:
            payload = web_manager.self_test()

        _print_json(payload)
        return True
    except (
        PermissionAuditRecoveryVisibilityError,
        PermissionAuditRecoveryWebSurfaceError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def main(argv: Sequence[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    if not values:
        values = [STATUS_COMMAND]

    if handle_permission_audit_recovery_command(values):
        return 0

    print(
        "ERROR: unknown permission/audit/recovery command.",
        file=sys.stderr,
    )
    return 2


__all__ = [
    "PERMISSION_AUDIT_RECOVERY_COMMANDS",
    "handle_permission_audit_recovery_command",
    "main",
]
