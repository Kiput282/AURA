"""Alpha wrapper for Sprint 224 context-fusion contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .voice_vision_chat_context_fusion_planner import (
    VoiceVisionChatContextFusionPlanner,
)


class VoiceVisionChatContextFusionAlphaManager:
    """Expose deterministic Sprint 224 contract packets."""

    name = "voice_vision_chat_context_fusion_alpha"
    version = "0.1.0-alpha"

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        planner: VoiceVisionChatContextFusionPlanner | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

        self.planner = (
            planner
            or VoiceVisionChatContextFusionPlanner(
                self.project_root
            )
        )

    def status(self) -> dict[str, Any]:
        planner_status = self.planner.status()
        planner_check = self.planner.check()
        contract = planner_check[
            "voice_vision_chat_context_fusion_contract"
        ]

        alpha_ready = (
            planner_check[
                "assertion_count"
            ]
            == 84
            and planner_check[
                "failed_assertion_count"
            ]
            == 0
            and contract[
                "voice_vision_chat_context_fusion_contract_ready"
            ]
            is True
            and contract[
                "runtime_ready"
            ]
            is False
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "ready"
                if alpha_ready
                else "degraded"
            ),
            "alpha_ready": alpha_ready,
            "planning_ready":
                planner_status[
                    "planning_ready"
                ],
            "runtime_ready": False,
            "partner_runtime_current_sprint":
                contract[
                    "partner_runtime_current_sprint"
                ],
            "partner_runtime_next_sprint":
                contract[
                    "partner_runtime_next_sprint"
                ],
            "partner_runtime_next_boundary":
                contract[
                    "partner_runtime_next_boundary"
                ],
            "canonical_voice_owner":
                contract[
                    "canonical_voice_owner"
                ],
            "canonical_vision_owner":
                contract[
                    "canonical_vision_owner"
                ],
            "canonical_chat_owner":
                contract[
                    "canonical_chat_owner"
                ],
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "voice_assertion_count":
                contract[
                    "voice_snapshot"
                ][
                    "assertion_count"
                ],
            "vision_assertion_count":
                contract[
                    "vision_snapshot"
                ][
                    "assertion_count"
                ],
            "chat_assertion_count":
                contract[
                    "chat_snapshot"
                ][
                    "assertion_count"
                ],
            "assertion_count":
                planner_check[
                    "assertion_count"
                ],
            "failed_assertion_count":
                planner_check[
                    "failed_assertion_count"
                ],
            "all_safety_blockers_inactive":
                contract[
                    "all_safety_blockers_inactive"
                ],
            "fusion_packet_created": False,
            "runtime_scope":
                "voice_vision_chat_context_fusion_contract_only",
            "contract": contract,
        }

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def context(self) -> dict[str, Any]:
        return self.planner.context()
