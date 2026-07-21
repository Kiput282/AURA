"""CLI adapter for the Sprint 276 ORION action preview runtime."""

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
) -> AuraOrionActionPreviewApprovalRuntimeManager:
    configured = os.environ.get("AURA_ORION_PAIRING_STATE_ROOT")
    pairing = AuraOrionPairingIdentityRuntimeManager(
        project_root=project_root,
        state_root=(
            None
            if configured is None
            else Path(configured)
        ),
    )
    live_link = AuraOrionLiveLinkRuntimeManager(
        project_root=project_root,
        pairing_manager=pairing,
    )
    return AuraOrionActionPreviewApprovalRuntimeManager(
        project_root=project_root,
        pairing_manager=pairing,
        live_link_manager=live_link,
    )


def handle_orion_action_preview_approval_command(
    raw_args: list[str],
    *,
    project_root: Path,
) -> bool:
    """Handle read-only Sprint 276 preview/approval CLI commands."""
    if not raw_args:
        return False

    command = raw_args[0]
    supported = {
        "orion-action-preview-status",
        "orion-action-preview-inspect",
        "orion-action-preview-self-test",
    }
    if command not in supported:
        return False
    if len(raw_args) != 1:
        raise ValueError(
            f"{command} does not accept additional arguments."
        )

    manager = _manager(project_root)
    if command == "orion-action-preview-status":
        _print_json(manager.status())
        return True
    if command == "orion-action-preview-inspect":
        _print_json(manager.inspect_runtime())
        return True

    _print_json(manager.self_test())
    return True
