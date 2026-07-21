"""CLI adapter for the Sprint 277 ORION scoped-permission runtime."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from aura.orion_action_preview_approval_runtime import (
    AuraOrionActionPreviewApprovalRuntimeManager,
)
from aura.orion_live_link_runtime import (
    AuraOrionLiveLinkRuntimeManager,
)
from aura.orion_pairing_identity_runtime import (
    AuraOrionPairingIdentityRuntimeManager,
)
from aura.orion_scoped_permission_runtime import (
    AuraOrionScopedPermissionRuntimeManager,
)


def _print_json(payload: dict[str, Any]) -> None:
    print(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def _manager(
    project_root: Path,
) -> AuraOrionScopedPermissionRuntimeManager:
    pairing_root = os.environ.get("AURA_ORION_PAIRING_STATE_ROOT")
    scoped_root = os.environ.get(
        "AURA_ORION_SCOPED_PERMISSION_STATE_ROOT"
    )
    pairing = AuraOrionPairingIdentityRuntimeManager(
        project_root=project_root,
        state_root=(
            None
            if pairing_root is None
            else Path(pairing_root)
        ),
    )
    live_link = AuraOrionLiveLinkRuntimeManager(
        project_root=project_root,
        pairing_manager=pairing,
    )
    preview = AuraOrionActionPreviewApprovalRuntimeManager(
        project_root=project_root,
        pairing_manager=pairing,
        live_link_manager=live_link,
    )
    return AuraOrionScopedPermissionRuntimeManager(
        project_root=project_root,
        pairing_manager=pairing,
        live_link_manager=live_link,
        preview_manager=preview,
        state_root=(
            None
            if scoped_root is None
            else Path(scoped_root)
        ),
    )


def handle_orion_scoped_permission_command(
    raw_args: list[str],
    *,
    project_root: Path,
) -> bool:
    """Handle read-only Sprint 277 status, inspect, and self-test commands."""
    if not raw_args:
        return False

    command = raw_args[0]
    supported = {
        "orion-scoped-permission-status",
        "orion-scoped-permission-inspect",
        "orion-scoped-permission-self-test",
    }
    if command not in supported:
        return False
    if len(raw_args) != 1:
        raise ValueError(
            f"{command} does not accept additional arguments."
        )

    manager = _manager(project_root)
    if command == "orion-scoped-permission-status":
        _print_json(manager.status())
        return True
    if command == "orion-scoped-permission-inspect":
        _print_json(manager.inspect_runtime())
        return True

    _print_json(manager.self_test())
    return True
