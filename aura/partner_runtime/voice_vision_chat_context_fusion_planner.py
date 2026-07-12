"""Contract-only voice, vision, and chat context fusion planning."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.partner_runtime.chat_to_memory_runtime_handoff_planner import (
    ChatToMemoryRuntimeHandoffPlanner,
)
from aura.vision.vision_runtime_planner import (
    VisionRuntimePlanner,
)
from aura.voice.voice_runtime_planner import (
    VoiceRuntimePlanner,
)


class VoiceVisionChatContextFusionPlanner:
    """Fuse bounded owner contract metadata without activating runtimes."""

    name = "voice_vision_chat_context_fusion"
    version = "0.1.0"

    current_sprint = 224
    next_sprint = 225
    next_boundary = "personality_consistency_runtime"

    canonical_voice_owner = (
        "aura.voice.voice_runtime_planner.VoiceRuntimePlanner"
    )

    canonical_vision_owner = (
        "aura.vision.vision_runtime_planner.VisionRuntimePlanner"
    )

    canonical_chat_owner = (
        "aura.partner_runtime."
        "chat_to_memory_runtime_handoff_planner."
        "ChatToMemoryRuntimeHandoffPlanner"
    )

    canonical_session_owner = (
        "aura_browser_chat_session_runtime"
    )

    safety_blockers = (
        "voice_microphone_capture_active",
        "voice_recording_active",
        "voice_transcription_active",
        "voice_tts_synthesis_active",
        "voice_speaker_playback_active",
        "vision_screen_access_active",
        "vision_screen_capture_active",
        "vision_screenshot_capture_active",
        "vision_camera_capture_active",
        "vision_image_file_read_active",
        "vision_ocr_active",
        "chat_payload_read_active",
        "chat_history_scan_active",
        "chat_session_write_active",
        "fusion_packet_create_active",
        "context_inference_active",
        "model_request_active",
        "memory_write_active",
        "permission_mutation_active",
        "audit_write_active",
        "network_action_active",
        "command_execution_active",
        "tool_execution_active",
        "file_mutation_active",
        "background_service_active",
        "release_gate_open",
        "autonomous_action_active",
        "personality_runtime_active",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        voice_planner: VoiceRuntimePlanner | None = None,
        vision_planner: VisionRuntimePlanner | None = None,
        chat_planner: ChatToMemoryRuntimeHandoffPlanner | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

        self.voice_planner = (
            voice_planner
            or VoiceRuntimePlanner(
                self.project_root
            )
        )

        self.vision_planner = (
            vision_planner
            or VisionRuntimePlanner(
                self.project_root
            )
        )

        self.chat_planner = (
            chat_planner
            or ChatToMemoryRuntimeHandoffPlanner(
                self.project_root
            )
        )

    def _voice_snapshot(self) -> dict[str, Any]:
        """Return bounded voice contract metadata."""

        try:
            status = self.voice_planner.status()
            check = self.voice_planner.check()
            assertions = check.get(
                "assertions",
                {},
            )

            if not isinstance(
                assertions,
                dict,
            ):
                assertions = {}

        except Exception as exc:  # pragma: no cover
            return {
                "available": False,
                "contract_ready": False,
                "owner": self.canonical_voice_owner,
                "name": None,
                "version": None,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "runtime_ready": False,
                "error": (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            }

        ready = (
            check.get(
                "assertion_count"
            )
            == 507
            and check.get(
                "failed_assertion_count"
            )
            == 0
            and status.get(
                "runtime_ready"
            )
            is False
        )

        return {
            "available": True,
            "contract_ready": ready,
            "owner": self.canonical_voice_owner,
            "name": getattr(
                self.voice_planner,
                "name",
                None,
            ),
            "version": getattr(
                self.voice_planner,
                "version",
                None,
            ),
            "assertion_count": check.get(
                "assertion_count"
            ),
            "failed_assertion_count": check.get(
                "failed_assertion_count"
            ),
            "runtime_ready": status.get(
                "runtime_ready"
            ),
            "voice_runtime_stabilization_contract_ready":
                assertions.get(
                    "voice_runtime_stabilization_contract_ready"
                )
                is True,
            "voice_runtime_stabilization_runtime_blocked":
                assertions.get(
                    "voice_runtime_stabilization_runtime_not_ready_final"
                )
                is True,
            "transcript_to_chat_handoff_contract_ready":
                assertions.get(
                    "transcript_to_chat_handoff_contract_ready"
                )
                is True,
            "transcript_to_chat_handoff_inactive":
                assertions.get(
                    "transcript_to_chat_handoff_inactive"
                )
                is True,
            "chat_response_to_tts_handoff_contract_ready":
                assertions.get(
                    "chat_response_to_tts_handoff_contract_ready"
                )
                is True,
            "chat_response_to_tts_handoff_inactive":
                assertions.get(
                    "chat_response_to_tts_handoff_inactive"
                )
                is True,
            "microphone_capture_inactive":
                assertions.get(
                    "voice_runtime_stabilization_microphone_capture_inactive"
                )
                is True,
            "speaker_playback_inactive":
                assertions.get(
                    "voice_runtime_stabilization_speaker_playback_inactive"
                )
                is True,
            "contract_metadata_only": True,
            "raw_audio_included": False,
            "transcript_payload_included": False,
            "error": None,
        }

    def _vision_snapshot(self) -> dict[str, Any]:
        """Return bounded vision contract metadata."""

        try:
            status = self.vision_planner.status()
            check = self.vision_planner.check()
            assertions = check.get(
                "assertions",
                {},
            )

            if not isinstance(
                assertions,
                dict,
            ):
                assertions = {}

        except Exception as exc:  # pragma: no cover
            return {
                "available": False,
                "contract_ready": False,
                "owner": self.canonical_vision_owner,
                "name": None,
                "version": None,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "runtime_ready": False,
                "error": (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            }

        ready = (
            check.get(
                "assertion_count"
            )
            == 330
            and check.get(
                "failed_assertion_count"
            )
            == 0
            and status.get(
                "runtime_ready"
            )
            is False
        )

        return {
            "available": True,
            "contract_ready": ready,
            "owner": self.canonical_vision_owner,
            "name": getattr(
                self.vision_planner,
                "name",
                None,
            ),
            "version": getattr(
                self.vision_planner,
                "version",
                None,
            ),
            "assertion_count": check.get(
                "assertion_count"
            ),
            "failed_assertion_count": check.get(
                "failed_assertion_count"
            ),
            "runtime_ready": status.get(
                "runtime_ready"
            ),
            "vision_runtime_stabilization_contract_ready":
                assertions.get(
                    "stabilization_contract_ready"
                )
                is True,
            "vision_runtime_stabilization_runtime_blocked":
                assertions.get(
                    "stabilization_runtime_not_ready"
                )
                is True,
            "vision_to_chat_context_handoff_contract_ready":
                assertions.get(
                    "vision_to_chat_context_handoff_contract_ready"
                )
                is True,
            "vision_to_chat_context_handoff_runtime_blocked":
                assertions.get(
                    "vision_to_chat_context_handoff_runtime_not_ready"
                )
                is True,
            "screenshot_capture_not_performed":
                assertions.get(
                    "screenshot_capture_not_performed"
                )
                is True,
            "chat_context_packet_not_created":
                assertions.get(
                    "chat_context_packet_not_created"
                )
                is True,
            "contract_metadata_only": True,
            "raw_image_included": False,
            "screenshot_payload_included": False,
            "error": None,
        }

    def _chat_snapshot(self) -> dict[str, Any]:
        """Return bounded Sprint 223 chat-chain contract metadata."""

        try:
            check = self.chat_planner.check()
            contract = check[
                "chat_to_memory_runtime_handoff_contract"
            ]

        except Exception as exc:  # pragma: no cover
            return {
                "available": False,
                "contract_ready": False,
                "owner": self.canonical_chat_owner,
                "canonical_session_owner": None,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "runtime_ready": False,
                "error": (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            }

        ready = (
            check.get(
                "assertion_count"
            )
            == 65
            and check.get(
                "failed_assertion_count"
            )
            == 0
            and contract.get(
                "chat_to_memory_runtime_handoff_contract_ready"
            )
            is True
            and contract.get(
                "runtime_ready"
            )
            is False
            and contract.get(
                "canonical_session_owner"
            )
            == self.canonical_session_owner
        )

        return {
            "available": True,
            "contract_ready": ready,
            "owner": self.canonical_chat_owner,
            "canonical_session_owner":
                contract.get(
                    "canonical_session_owner"
                ),
            "assertion_count": check.get(
                "assertion_count"
            ),
            "failed_assertion_count": check.get(
                "failed_assertion_count"
            ),
            "runtime_ready": contract.get(
                "runtime_ready"
            ),
            "current_sprint": contract.get(
                "partner_runtime_current_sprint"
            ),
            "next_sprint": contract.get(
                "partner_runtime_next_sprint"
            ),
            "next_boundary": contract.get(
                "partner_runtime_next_boundary"
            ),
            "default_deny_without_grant":
                contract.get(
                    "default_deny_without_grant"
                )
                is True,
            "memory_write_performed":
                contract.get(
                    "memory_write_performed"
                )
                is True,
            "memory_store_mutated":
                contract.get(
                    "memory_store_mutated"
                )
                is True,
            "handoff_persisted":
                contract.get(
                    "handoff_persisted"
                )
                is True,
            "contract_metadata_only": True,
            "chat_payload_included": False,
            "session_payload_included": False,
            "error": None,
        }

    def voice_vision_chat_context_fusion_contract(
        self,
    ) -> dict[str, Any]:
        """Build a non-executing fusion contract from owner metadata."""

        voice = self._voice_snapshot()
        vision = self._vision_snapshot()
        chat = self._chat_snapshot()

        blockers = {
            name: False
            for name in self.safety_blockers
        }

        all_blockers_inactive = all(
            value is False
            for value in blockers.values()
        )

        ready = (
            voice.get(
                "contract_ready"
            )
            is True
            and vision.get(
                "contract_ready"
            )
            is True
            and chat.get(
                "contract_ready"
            )
            is True
            and all_blockers_inactive
        )

        contract: dict[str, Any] = {
            "name": self.name,
            "version": self.version,
            "voice_vision_chat_context_fusion_contract_ready":
                ready,
            "voice_vision_chat_context_fusion_runtime_ready":
                False,
            "status": (
                "voice_vision_chat_context_fusion_contract_ready"
                if ready
                else
                "voice_vision_chat_context_fusion_contract_degraded"
            ),
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "contract_only": True,
            "preview_only": True,
            "planning_ready": ready,
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "canonical_voice_owner":
                self.canonical_voice_owner,
            "canonical_vision_owner":
                self.canonical_vision_owner,
            "canonical_chat_owner":
                self.canonical_chat_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "voice_snapshot": voice,
            "vision_snapshot": vision,
            "chat_snapshot": chat,
            "fusion_input_order": [
                "chat_session_anchor",
                "voice_contract_metadata",
                "vision_contract_metadata",
            ],
            "fusion_policy": {
                "chat_session_anchor_preserved": True,
                "voice_contract_metadata_only": True,
                "vision_contract_metadata_only": True,
                "redaction_before_future_visual_context": True,
                "permission_before_future_voice_input": True,
                "no_context_inference": True,
                "no_modality_precedence_execution": True,
            },
            "fusion_packet_created": False,
            "raw_audio_included": False,
            "transcript_payload_included": False,
            "raw_image_included": False,
            "screenshot_payload_included": False,
            "chat_payload_included": False,
            "session_payload_included": False,
            "model_request_performed": False,
            "context_inference_performed": False,
            "memory_write_performed": False,
            "permission_mutation_performed": False,
            "audit_write_performed": False,
            "network_action_performed": False,
            "command_execution_performed": False,
            "tool_execution_performed": False,
            "file_mutation_performed": False,
            "background_service_started": False,
            "personality_consistency_deferred_to_sprint_225":
                True,
            "safety_blockers":
                list(self.safety_blockers),
            "safety_blocker_count":
                len(self.safety_blockers),
            "all_safety_blockers_inactive":
                all_blockers_inactive,
        }

        contract.update(blockers)
        return contract

    def status(self) -> dict[str, Any]:
        contract = (
            self.voice_vision_chat_context_fusion_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "planning_ready":
                contract["planning_ready"],
            "runtime_ready": False,
            "alpha_ready":
                contract[
                    "voice_vision_chat_context_fusion_contract_ready"
                ],
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "canonical_voice_owner":
                self.canonical_voice_owner,
            "canonical_vision_owner":
                self.canonical_vision_owner,
            "canonical_chat_owner":
                self.canonical_chat_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "voice_assertion_count":
                contract[
                    "voice_snapshot"
                ].get(
                    "assertion_count"
                ),
            "vision_assertion_count":
                contract[
                    "vision_snapshot"
                ].get(
                    "assertion_count"
                ),
            "chat_assertion_count":
                contract[
                    "chat_snapshot"
                ].get(
                    "assertion_count"
                ),
            "all_safety_blockers_inactive":
                contract[
                    "all_safety_blockers_inactive"
                ],
            "contract": contract,
        }

    def context(self) -> dict[str, Any]:
        contract = (
            self.voice_vision_chat_context_fusion_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "canonical_voice_owner":
                self.canonical_voice_owner,
            "canonical_vision_owner":
                self.canonical_vision_owner,
            "canonical_chat_owner":
                self.canonical_chat_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "fusion_input_order":
                contract[
                    "fusion_input_order"
                ],
            "fusion_policy":
                contract[
                    "fusion_policy"
                ],
            "voice_snapshot":
                contract[
                    "voice_snapshot"
                ],
            "vision_snapshot":
                contract[
                    "vision_snapshot"
                ],
            "chat_snapshot":
                contract[
                    "chat_snapshot"
                ],
            "contract_only": True,
            "preview_only": True,
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        contract = (
            self.voice_vision_chat_context_fusion_contract()
        )

        voice = contract[
            "voice_snapshot"
        ]

        vision = contract[
            "vision_snapshot"
        ]

        chat = contract[
            "chat_snapshot"
        ]

        assertions = {
            "contract_ready":
                contract[
                    "voice_vision_chat_context_fusion_contract_ready"
                ]
                is True,
            "runtime_disabled":
                contract[
                    "runtime_ready"
                ]
                is False,
            "activation_blocked":
                contract[
                    "runtime_activation_allowed"
                ]
                is False,
            "release_gate_closed":
                contract[
                    "release_gate_open"
                ]
                is False,
            "current_sprint_224":
                contract[
                    "partner_runtime_current_sprint"
                ]
                == 224,
            "next_sprint_225":
                contract[
                    "partner_runtime_next_sprint"
                ]
                == 225,
            "next_boundary_correct":
                contract[
                    "partner_runtime_next_boundary"
                ]
                == "personality_consistency_runtime",
            "voice_owner_correct":
                contract[
                    "canonical_voice_owner"
                ]
                == self.canonical_voice_owner,
            "vision_owner_correct":
                contract[
                    "canonical_vision_owner"
                ]
                == self.canonical_vision_owner,
            "chat_owner_correct":
                contract[
                    "canonical_chat_owner"
                ]
                == self.canonical_chat_owner,
            "voice_contract_ready":
                voice.get(
                    "contract_ready"
                )
                is True,
            "voice_assertions_507":
                voice.get(
                    "assertion_count"
                )
                == 507,
            "voice_failed_zero":
                voice.get(
                    "failed_assertion_count"
                )
                == 0,
            "voice_runtime_disabled":
                voice.get(
                    "runtime_ready"
                )
                is False,
            "vision_contract_ready":
                vision.get(
                    "contract_ready"
                )
                is True,
            "vision_assertions_330":
                vision.get(
                    "assertion_count"
                )
                == 330,
            "vision_failed_zero":
                vision.get(
                    "failed_assertion_count"
                )
                == 0,
            "vision_runtime_disabled":
                vision.get(
                    "runtime_ready"
                )
                is False,
            "chat_contract_ready":
                chat.get(
                    "contract_ready"
                )
                is True,
            "chat_assertions_65":
                chat.get(
                    "assertion_count"
                )
                == 65,
            "chat_failed_zero":
                chat.get(
                    "failed_assertion_count"
                )
                == 0,
            "chat_runtime_disabled":
                chat.get(
                    "runtime_ready"
                )
                is False,
            "chat_session_owner_preserved":
                chat.get(
                    "canonical_session_owner"
                )
                == self.canonical_session_owner,
            "voice_stabilization_ready":
                voice.get(
                    "voice_runtime_stabilization_contract_ready"
                )
                is True,
            "voice_stabilization_runtime_blocked":
                voice.get(
                    "voice_runtime_stabilization_runtime_blocked"
                )
                is True,
            "voice_transcript_handoff_contract_ready":
                voice.get(
                    "transcript_to_chat_handoff_contract_ready"
                )
                is True,
            "voice_transcript_handoff_inactive":
                voice.get(
                    "transcript_to_chat_handoff_inactive"
                )
                is True,
            "voice_tts_handoff_contract_ready":
                voice.get(
                    "chat_response_to_tts_handoff_contract_ready"
                )
                is True,
            "voice_tts_handoff_inactive":
                voice.get(
                    "chat_response_to_tts_handoff_inactive"
                )
                is True,
            "vision_stabilization_ready":
                vision.get(
                    "vision_runtime_stabilization_contract_ready"
                )
                is True,
            "vision_stabilization_runtime_blocked":
                vision.get(
                    "vision_runtime_stabilization_runtime_blocked"
                )
                is True,
            "vision_to_chat_contract_ready":
                vision.get(
                    "vision_to_chat_context_handoff_contract_ready"
                )
                is True,
            "vision_to_chat_runtime_blocked":
                vision.get(
                    "vision_to_chat_context_handoff_runtime_blocked"
                )
                is True,
            "vision_no_screenshot_capture":
                vision.get(
                    "screenshot_capture_not_performed"
                )
                is True,
            "vision_no_chat_packet":
                vision.get(
                    "chat_context_packet_not_created"
                )
                is True,
            "fusion_contract_only":
                contract[
                    "contract_only"
                ]
                is True,
            "fusion_preview_only":
                contract[
                    "preview_only"
                ]
                is True,
            "fusion_packet_not_created":
                contract[
                    "fusion_packet_created"
                ]
                is False,
            "no_raw_audio":
                contract[
                    "raw_audio_included"
                ]
                is False,
            "no_transcript_payload":
                contract[
                    "transcript_payload_included"
                ]
                is False,
            "no_raw_image":
                contract[
                    "raw_image_included"
                ]
                is False,
            "no_screenshot_payload":
                contract[
                    "screenshot_payload_included"
                ]
                is False,
            "no_chat_payload":
                contract[
                    "chat_payload_included"
                ]
                is False,
            "no_session_payload":
                contract[
                    "session_payload_included"
                ]
                is False,
            "no_model_request":
                contract[
                    "model_request_performed"
                ]
                is False,
            "no_context_inference":
                contract[
                    "context_inference_performed"
                ]
                is False,
            "no_memory_write":
                contract[
                    "memory_write_performed"
                ]
                is False,
            "no_permission_mutation":
                contract[
                    "permission_mutation_performed"
                ]
                is False,
            "no_audit_write":
                contract[
                    "audit_write_performed"
                ]
                is False,
            "no_network":
                contract[
                    "network_action_performed"
                ]
                is False,
            "no_command":
                contract[
                    "command_execution_performed"
                ]
                is False,
            "no_tool":
                contract[
                    "tool_execution_performed"
                ]
                is False,
            "no_file_mutation":
                contract[
                    "file_mutation_performed"
                ]
                is False,
            "no_background_service":
                contract[
                    "background_service_started"
                ]
                is False,
            "all_safety_blockers_inactive":
                contract[
                    "all_safety_blockers_inactive"
                ]
                is True,
            "personality_consistency_deferred":
                contract[
                    "personality_consistency_deferred_to_sprint_225"
                ]
                is True,
        }

        assertions.update(
            {
                f"{name}_inactive":
                    contract[name]
                    is False
                for name
                in self.safety_blockers
            }
        )

        failed = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "status": "checked",
            "planning_ready":
                contract[
                    "planning_ready"
                ],
            "runtime_ready": False,
            "assertion_count":
                len(assertions),
            "failed_assertion_count":
                len(failed),
            "failed_assertions":
                failed,
            "assertions": assertions,
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "voice_vision_chat_context_fusion_contract":
                contract,
        }

    def plan(self) -> dict[str, Any]:
        contract = (
            self.voice_vision_chat_context_fusion_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "planning_ready":
                contract[
                    "planning_ready"
                ],
            "runtime_ready": False,
            "contract_only": True,
            "preview_only": True,
            "fusion_packet_created": False,
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "canonical_session_owner":
                self.canonical_session_owner,
            "fusion_input_order":
                contract[
                    "fusion_input_order"
                ],
            "safety_blocker_count":
                contract[
                    "safety_blocker_count"
                ],
        }
