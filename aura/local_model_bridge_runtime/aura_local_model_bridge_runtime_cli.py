"""Main CLI routing for Sprint 187 local model bridge operations."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from typing import Any

from .aura_local_model_bridge_profile_resolver import (
    AuraLocalModelBridgeProfileResolver,
)
from .aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeError,
)


STATUS_COMMAND = "local-model-bridge-status"
CONTRACTS_COMMAND = "local-model-bridge-contracts"
SELF_TEST_COMMAND = "local-model-bridge-self-test"
PROBE_COMMAND = "local-model-bridge-probe"
GENERATE_COMMAND = "local-model-bridge-generate"

LOCAL_MODEL_BRIDGE_COMMANDS = frozenset(
    {
        STATUS_COMMAND,
        CONTRACTS_COMMAND,
        SELF_TEST_COMMAND,
        PROBE_COMMAND,
        GENERATE_COMMAND,
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


def _manager_from_environment() -> AuraLocalModelBridgeRuntimeManager:
    profile = AuraLocalModelBridgeProfileResolver.resolve(
        os.environ
    )
    return AuraLocalModelBridgeRuntimeManager(profile)


def _no_argument_parser(command: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog=f"python3 main.py {command}",
        add_help=True,
    )


def _probe_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"python3 main.py {PROBE_COMMAND}",
        description=(
            "Probe an explicitly enabled localhost-only model provider."
        ),
    )
    parser.add_argument(
        "--confirm-local-connection",
        action="store_true",
        help="Confirm one localhost provider probe.",
    )
    return parser


def _generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"python3 main.py {GENERATE_COMMAND}",
        description=(
            "Send one explicitly confirmed text-only request to an "
            "enabled localhost model provider. The JSON object is read "
            "from standard input and must contain only a messages array."
        ),
    )
    parser.add_argument(
        "--confirm-model-request",
        action="store_true",
        help="Confirm one local model inference request.",
    )
    parser.add_argument(
        "--request-id",
        required=True,
        help="Safe request id beginning with modelreq_.",
    )
    parser.add_argument(
        "--messages-stdin",
        action="store_true",
        help="Read a JSON object containing messages from standard input.",
    )
    return parser


def _read_messages_from_stdin() -> Any:
    limit = (
        AuraLocalModelBridgeRuntimeManager.MAX_REQUEST_BODY_BYTES
    )
    body = sys.stdin.buffer.read(limit + 1)
    if len(body) > limit:
        raise LocalModelBridgeError(
            "Standard-input model request exceeds the body limit."
        )
    try:
        payload = json.loads(body.decode("utf-8"))
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise LocalModelBridgeError(
            "Standard input must be valid UTF-8 JSON."
        ) from exc
    if not isinstance(payload, dict):
        raise LocalModelBridgeError(
            "Standard-input request must be a JSON object."
        )
    if set(payload) != {"messages"}:
        raise LocalModelBridgeError(
            "Standard-input request must contain only messages."
        )
    return payload["messages"]


def handle_local_model_bridge_command(
    args: Sequence[str],
) -> bool:
    """Handle Sprint 187 local-model bridge CLI commands."""

    if not args:
        return False

    command = str(args[0])
    if command not in LOCAL_MODEL_BRIDGE_COMMANDS:
        return False

    command_args = list(args[1:])

    try:
        if command == STATUS_COMMAND:
            _no_argument_parser(command).parse_args(
                command_args
            )
            profile_status = (
                AuraLocalModelBridgeProfileResolver.status(
                    os.environ
                )
            )
            manager = _manager_from_environment()
            payload = {
                **manager.status(),
                "profile_resolution": profile_status,
            }
        elif command == CONTRACTS_COMMAND:
            _no_argument_parser(command).parse_args(
                command_args
            )
            payload = (
                AuraLocalModelBridgeRuntimeManager
                .provider_contracts()
            )
        elif command == SELF_TEST_COMMAND:
            _no_argument_parser(command).parse_args(
                command_args
            )
            core = (
                AuraLocalModelBridgeRuntimeManager()
                .self_test()
            )
            resolver = (
                AuraLocalModelBridgeProfileResolver
                .self_test()
            )
            payload = {
                "status": "ok",
                "component": (
                    "aura_local_model_bridge_runtime_cli"
                ),
                "sprint": 187,
                "assertion_count": (
                    core["assertion_count"]
                    + resolver["assertion_count"]
                ),
                "failed_assertion_count": 0,
                "core": core,
                "profile_resolver": resolver,
                "provider_network_calls": 0,
                "model_download_runtime": False,
                "internet_fallback_runtime": False,
            }
        elif command == PROBE_COMMAND:
            parsed = _probe_parser().parse_args(
                command_args
            )
            manager = _manager_from_environment()
            payload = manager.probe(
                confirm_local_connection=(
                    parsed.confirm_local_connection
                )
            )
        else:
            parsed = _generate_parser().parse_args(
                command_args
            )
            if not parsed.messages_stdin:
                raise LocalModelBridgeError(
                    "--messages-stdin is required."
                )
            messages = _read_messages_from_stdin()
            manager = _manager_from_environment()
            payload = manager.generate(
                messages=messages,
                request_id=parsed.request_id,
                confirm_model_request=(
                    parsed.confirm_model_request
                ),
            )

        _print_json(payload)
        return True
    except LocalModelBridgeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


__all__ = [
    "LOCAL_MODEL_BRIDGE_COMMANDS",
    "handle_local_model_bridge_command",
]
