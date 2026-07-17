"""Read-only Sprint 261 product roadmap manager."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class RoadmapReconfirmationAlphaManager:
    """Expose the canonical v1.2 to v1.3 product direction."""

    VERSION = "1.2.1"
    ANCHOR_VERSION = "1.2.0"
    CURRENT_SPRINT = 261
    NEXT_SPRINT = 262
    BOUNDARY = "roadmap_reconfirmation_after_v1_2_0"
    NEXT_BOUNDARY = "operational_browser_chat_model_handoff"
    BLOCK = "daily_chat_control_center_productization"
    BLOCK_START = 261
    BLOCK_END = 270
    RELEASE_TARGET = "1.3.0"

    SEQUENCE = (
        (
            261,
            "roadmap_reconfirmation_after_v1_2_0",
        ),
        (
            262,
            "operational_browser_chat_model_handoff",
        ),
        (
            263,
            "session_list_resume_rename_archive_restore",
        ),
        (
            264,
            "chat_history_recovery_ux",
        ),
        (
            265,
            "review_first_memory_integration",
        ),
        (
            266,
            "control_center_runtime_ux_consolidation",
        ),
        (
            267,
            "atlas_resource_monitoring_dashboard",
        ),
        (
            268,
            "permission_audit_action_visibility_ux",
        ),
        (
            269,
            "daily_use_acceptance_rehearsal_and_release_harness",
        ),
        (
            270,
            "daily_local_assistant_live_acceptance_stabilization",
        ),
    )

    GAP_OWNERSHIP = {
        "native_process_role_classification": 262,
        "session_rename_archive_restore": 263,
        "reusable_release_harness": 269,
        "live_end_to_end_acceptance": 270,
    }

    def __init__(
        self,
        *,
        project_root: Path | None = None,
    ) -> None:
        self.project_root = (
            project_root or Path.cwd()
        ).resolve()

    def product_direction(
        self,
    ) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "block": self.BLOCK,
            "block_start_sprint": self.BLOCK_START,
            "block_end_sprint": self.BLOCK_END,
            "release_target": self.RELEASE_TARGET,
            "primary_interface": "browser_control_center",
            "primary_model_route": "companion",
            "autostart_default": "disabled",
            "memory_write_policy": "review_first",
            "voice_activation": "after_1_3_0",
            "vision_activation": "after_voice_stabilization",
            "orion_client": "after_local_dashboard_maturity",
            "game_companion_activation": "deferred",
            "runtime_mutated": False,
        }

    def sprint_sequence(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "sprint": sprint,
                "boundary": boundary,
            }
            for sprint, boundary in self.SEQUENCE
        ]

    def gap_ownership(
        self,
    ) -> dict[str, Any]:
        return {
            "gap_count": len(
                self.GAP_OWNERSHIP
            ),
            "ownership": dict(
                self.GAP_OWNERSHIP
            ),
            "all_gaps_owned": True,
            "runtime_mutated": False,
        }

    def live_acceptance_policy(
        self,
    ) -> dict[str, Any]:
        return {
            "required": True,
            "sprint": 270,
            "scope": (
                "daily_chat_control_center_productization"
            ),
            "must_prove_real_functionality": True,
            "must_verify_user_visible_results": True,
            "must_test_relevant_failure_recovery": True,
            "must_restore_safe_idle": True,
            "must_finish_before_next_block": True,
            "contract_only_is_insufficient": True,
            "runtime_mutated": False,
        }
