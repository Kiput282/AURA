"""CLI adapter for authenticated ORION pairing and identity."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .aura_orion_pairing_identity_runtime_manager import (
    AuraOrionPairingIdentityRuntimeManager,
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


def _parse_flags(arguments: list[str]) -> dict[str, str]:
    options: dict[str, str] = {}
    index = 0
    while index < len(arguments):
        token = arguments[index]
        if not token.startswith("--") or len(token) <= 2:
            raise ValueError(f"Unexpected argument: {token}")
        key = token[2:]
        if key in options:
            raise ValueError(f"Duplicate option: --{key}")
        index += 1
        if index >= len(arguments):
            raise ValueError(f"Missing value for --{key}")
        value = arguments[index]
        if value.startswith("--"):
            raise ValueError(f"Missing value for --{key}")
        options[key] = value
        index += 1
    return options


def _require_options(
    options: dict[str, str],
    *,
    required: set[str],
) -> None:
    missing = sorted(required - set(options))
    unknown = sorted(set(options) - required)
    if missing:
        raise ValueError(
            "Missing required options: "
            + ", ".join(f"--{item}" for item in missing)
        )
    if unknown:
        raise ValueError(
            "Unknown options: "
            + ", ".join(f"--{item}" for item in unknown)
        )


def _manager(project_root: Path) -> AuraOrionPairingIdentityRuntimeManager:
    configured = os.environ.get("AURA_ORION_PAIRING_STATE_ROOT")
    return AuraOrionPairingIdentityRuntimeManager(
        project_root=project_root,
        state_root=(
            None
            if configured is None
            else Path(configured)
        ),
    )


def handle_orion_pairing_identity_command(
    raw_args: list[str],
    *,
    project_root: Path,
) -> bool:
    """Handle explicit local Sprint 274 pairing commands."""

    if not raw_args:
        return False

    command = raw_args[0]
    supported = {
        "orion-pairing-status",
        "orion-pairing-begin",
        "orion-pairing-complete",
        "orion-pairing-cancel",
        "orion-pairing-revoke",
        "orion-pairing-reset",
        "orion-pairing-inspect",
        "orion-pairing-self-test",
    }
    if command not in supported:
        return False

    options = _parse_flags(raw_args[1:])
    manager = _manager(project_root)

    if command == "orion-pairing-status":
        _require_options(options, required=set())
        _print_json(manager.status())
        return True

    if command == "orion-pairing-inspect":
        _require_options(options, required=set())
        _print_json(manager.inspect_runtime())
        return True

    if command == "orion-pairing-self-test":
        _require_options(options, required=set())
        _print_json(manager.self_test())
        return True

    if command == "orion-pairing-begin":
        _require_options(
            options,
            required={"display-name", "platform"},
        )
        _print_json(
            manager.begin_pairing(
                display_name=options["display-name"],
                platform=options["platform"],
            )
        )
        return True

    if command == "orion-pairing-complete":
        _require_options(
            options,
            required={
                "pairing-id",
                "device-id",
                "challenge-id",
                "proof",
            },
        )
        _print_json(
            manager.complete_pairing(
                pairing_id=options["pairing-id"],
                device_id=options["device-id"],
                challenge_id=options["challenge-id"],
                proof_b64url=options["proof"],
            )
        )
        return True

    if command == "orion-pairing-cancel":
        _require_options(options, required=set())
        _print_json(manager.cancel_pairing())
        return True

    if command == "orion-pairing-revoke":
        _require_options(options, required={"confirm"})
        _print_json(
            manager.revoke_pairing(
                confirmation=options["confirm"]
            )
        )
        return True

    _require_options(options, required={"confirm"})
    _print_json(
        manager.reset_pairing(
            confirmation=options["confirm"]
        )
    )
    return True
