from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, Sequence

from .local_model_service_discovery_health_alpha_manager import (
    LocalModelServiceDiscoveryHealthAlphaManager,
)
from .local_model_service_discovery_health_contract import (
    LocalModelServiceDiscoveryHealthContract,
)


LOCAL_MODEL_SERVICE_DISCOVERY_HEALTH_COMMANDS = frozenset(
    {
        "local-model-service-discovery-health-status",
        "local-model-service-discovery-health-context",
        "local-model-service-discovery-health-check",
        "local-model-service-discovery-health-review",
        "local-model-service-host-posture",
        "local-model-service-provider-contracts",
        "local-model-service-health-preview",
        "local-model-service-health-probe",
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
) -> NoReturn:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "unexpected_arguments",
                "command": command,
                "provided_arguments": list(
                    extras
                ),
                "health_probe_performed": False,
                "network_connection_opened": False,
            },
            indent=2,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    raise SystemExit(2)


def handle_local_model_service_discovery_health_command(
    args: Sequence[str],
) -> bool:
    if (
        not args
        or args[0]
        not in (
            LOCAL_MODEL_SERVICE_DISCOVERY_HEALTH_COMMANDS
        )
    ):
        return False

    command = args[0]
    extras = list(args[1:])
    owner = (
        LocalModelServiceDiscoveryHealthAlphaManager(
            project_root=Path.cwd()
        )
    )

    if command.endswith("-health-probe"):
        if extras != [
            LocalModelServiceDiscoveryHealthContract
            .CONFIRMATION_TOKEN
        ]:
            _usage_error(command, extras)

        packet = owner.health_probe(
            extras[0]
        )
    else:
        if extras:
            _usage_error(command, extras)

        if command.endswith("-status"):
            packet = owner.status()
        elif command.endswith("-context"):
            packet = owner.context()
        elif command.endswith("-check"):
            packet = owner.check()
        elif command.endswith("-review"):
            packet = owner.review()
        elif command.endswith("-host-posture"):
            packet = owner.host_posture()
        elif command.endswith(
            "-provider-contracts"
        ):
            packet = owner.provider_contracts()
        elif command.endswith("-health-preview"):
            packet = owner.health_preview()
        else:
            return False

    _print_json(packet)
    return True
