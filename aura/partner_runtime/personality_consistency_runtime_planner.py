from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aura.local_chat_persona_response_layer.aura_local_chat_persona_response_layer_manager import (
    AuraLocalChatPersonaResponseLayerManager,
)
from aura.partner_runtime.voice_vision_chat_context_fusion_alpha_manager import (
    VoiceVisionChatContextFusionAlphaManager,
)


class PersonalityConsistencyRuntimePlanner:
    """Compose identity and persona metadata without producing responses."""

    name = "personality_consistency_runtime"
    version = "0.1.0"

    current_sprint = 225
    next_sprint = 226
    next_boundary = "multi_interface_state_synchronization"

    canonical_identity_source = "aura/personality/identity.yaml"

    canonical_persona_contract_owner = (
        "aura.local_chat_persona_response_layer."
        "aura_local_chat_persona_response_layer_manager."
        "AuraLocalChatPersonaResponseLayerManager"
    )

    canonical_upstream_context_owner = (
        "aura.partner_runtime."
        "voice_vision_chat_context_fusion_alpha_manager."
        "VoiceVisionChatContextFusionAlphaManager"
    )

    canonical_session_owner = "aura_browser_chat_session_runtime"

    secondary_expression_reference = (
        "aura.expression.expression_language_manager."
        "ExpressionLanguageManager"
    )

    expression_source = (
        "aura/expression/expression_language_manager.py"
    )

    supported_identity_versions = (
        "0.224.0-genesis",
        "0.225.0-genesis",
        "0.226.0-genesis",
        "0.227.0-genesis",
        "0.234.0-genesis",
    )

    required_traits = (
        "friendly",
        "intelligent",
        "supportive",
        "curious",
        "adaptive",
        "honest",
    )

    required_modes = (
        "coding",
        "gaming",
        "learning",
        "streaming",
    )

    required_style_items = (
        "warm_ai_partner_tone",
        "clear_indonesian_default",
        "concise_but_supportive_style",
        "honest_capability_boundary",
        "no_false_autonomy_claims",
        "no_fake_model_claims",
        "no_fake_memory_claims",
        "project_aura_context_awareness",
        "safe_developer_assistant_identity",
        "genesis_final_alignment",
    )

    consistency_dimensions = (
        "identity_continuity",
        "trait_continuity",
        "mode_style_continuity",
        "warm_partner_tone",
        "capability_honesty",
        "safety_boundary_consistency",
        "canonical_session_continuity",
        "modality_neutrality",
        "no_false_autonomy",
        "no_fake_memory_or_model_claims",
    )

    interface_targets = (
        "browser_chat",
        "local_chat_cli",
        "control_center",
        "voice_metadata",
        "vision_metadata",
        "shell",
        "cli",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        persona_manager: (
            AuraLocalChatPersonaResponseLayerManager
            | None
        ) = None,
        fusion_manager: (
            VoiceVisionChatContextFusionAlphaManager
            | None
        ) = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()

        self.identity_path = (
            self.project_root
            / self.canonical_identity_source
        )

        self.expression_path = (
            self.project_root
            / self.expression_source
        )

        contract_store = (
            self.project_root
            / ".aura_runtime"
            / "personality_consistency_contract_only"
        )

        self.persona_manager = (
            persona_manager
            or AuraLocalChatPersonaResponseLayerManager(
                project_root=self.project_root,
                store_dir=contract_store,
            )
        )

        self.fusion_manager = (
            fusion_manager
            or VoiceVisionChatContextFusionAlphaManager(
                project_root=self.project_root
            )
        )

    def _identity_snapshot(self) -> dict[str, Any]:
        if not self.identity_path.is_file():
            return {
                "available": False,
                "source": self.canonical_identity_source,
                "version": None,
                "name": None,
                "codename": None,
                "creator": None,
                "motto": None,
                "description": None,
                "traits": [],
                "modes": {},
                "version_supported": False,
                "required_traits_present": False,
                "required_modes_present": False,
                "contract_ready": False,
                "error": "missing",
            }

        try:
            data = yaml.safe_load(
                self.identity_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as exc:
            return {
                "available": False,
                "source": self.canonical_identity_source,
                "version": None,
                "name": None,
                "codename": None,
                "creator": None,
                "motto": None,
                "description": None,
                "traits": [],
                "modes": {},
                "version_supported": False,
                "required_traits_present": False,
                "required_modes_present": False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        if not isinstance(data, dict):
            return {
                "available": False,
                "source": self.canonical_identity_source,
                "version": None,
                "name": None,
                "codename": None,
                "creator": None,
                "motto": None,
                "description": None,
                "traits": [],
                "modes": {},
                "version_supported": False,
                "required_traits_present": False,
                "required_modes_present": False,
                "contract_ready": False,
                "error": "invalid_root",
            }

        personality = data.get("personality", {})
        modes = data.get("modes", {})

        if not isinstance(personality, dict):
            personality = {}

        if not isinstance(modes, dict):
            modes = {}

        traits_value = personality.get("traits", [])

        if not isinstance(traits_value, list):
            traits_value = []

        traits = [
            str(item).strip().lower()
            for item in traits_value
            if str(item).strip()
        ]

        normalized_modes = {
            str(key).strip().lower():
                str(value).strip()
            for key, value in modes.items()
            if (
                str(key).strip()
                and str(value).strip()
            )
        }

        version = data.get("version")

        version_supported = (
            version
            in self.supported_identity_versions
        )

        required_traits_present = (
            set(self.required_traits)
            .issubset(set(traits))
        )

        required_modes_present = (
            set(self.required_modes)
            .issubset(
                set(normalized_modes)
            )
        )

        description = personality.get(
            "description"
        )

        ready = all(
            (
                data.get("name") == "AURA",
                data.get("codename") == "Genesis",
                data.get("creator") == "Kiput",
                data.get("motto") == "Grow Together",
                isinstance(description, str),
                bool(
                    str(description).strip()
                ),
                version_supported,
                required_traits_present,
                required_modes_present,
            )
        )

        return {
            "available": True,
            "source": self.canonical_identity_source,
            "version": version,
            "name": data.get("name"),
            "codename": data.get("codename"),
            "creator": data.get("creator"),
            "motto": data.get("motto"),
            "description": description,
            "traits": traits,
            "modes": normalized_modes,
            "version_supported": version_supported,
            "required_traits_present":
                required_traits_present,
            "required_modes_present":
                required_modes_present,
            "contract_ready": ready,
            "error": None,
        }

    def _persona_snapshot(self) -> dict[str, Any]:
        try:
            status = self.persona_manager.status()
            context = self.persona_manager.context()

            style = (
                self.persona_manager
                .aura_persona_style_contract_plan(
                    "Sprint 225 personality consistency"
                )
            )

            honesty = (
                self.persona_manager
                .persona_capability_honesty_plan(
                    "Sprint 225 personality consistency"
                )
            )

            safety = (
                self.persona_manager
                .persona_safety_boundary_plan(
                    "Sprint 225 personality consistency"
                )
            )
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.canonical_persona_contract_owner,
                "name": None,
                "status": None,
                "context_sprint": None,
                "context_version": None,
                "status_ready": False,
                "data_ready": False,
                "thin_runtime_alpha": False,
                "persona_runtime_enabled": False,
                "release_gate_closed": False,
                "context_boundary_ready": False,
                "style_plan_ready": False,
                "style_runtime_ready": True,
                "style_items": [],
                "honesty_plan_ready": False,
                "honesty_runtime_ready": True,
                "safety_plan_ready": False,
                "safety_runtime_ready": True,
                "runtime_false_flags_all_false":
                    False,
                "runtime_zero_counters_all_zero":
                    False,
                "persona_turn_runtime_invoked":
                    False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        context_boundary = context.get(
            "safety_boundary",
            {},
        )

        if not isinstance(
            context_boundary,
            dict,
        ):
            context_boundary = {}

        style_counters = style.get(
            "runtime_counters",
            {},
        )

        if not isinstance(
            style_counters,
            dict,
        ):
            style_counters = {}

        runtime_false_flags_all_false = all(
            context_boundary.get(key) is False
            for key in (
                self.persona_manager
                .RUNTIME_FALSE_FLAGS
            )
        )

        runtime_zero_counters_all_zero = all(
            style_counters.get(key) == 0
            for key in (
                self.persona_manager
                .RUNTIME_ZERO_COUNTERS
            )
        )

        style_items = style.get(
            "items",
            [],
        )

        if not isinstance(style_items, list):
            style_items = []

        style_items_exact = (
            set(style_items)
            == set(
                self.required_style_items
            )
        )

        ready = all(
            (
                getattr(
                    self.persona_manager,
                    "name",
                    None,
                )
                == (
                    "aura_local_chat_"
                    "persona_response_layer"
                ),
                getattr(
                    self.persona_manager,
                    "status_name",
                    None,
                )
                == "online",
                status.get(
                    "local_chat_persona_"
                    "response_layer_ready"
                )
                is True,
                status.get(
                    "local_chat_persona_"
                    "response_layer_data_ready"
                )
                is True,
                status.get(
                    "thin_runtime_alpha"
                )
                is True,
                status.get(
                    "persona_response_layer_"
                    "runtime_enabled"
                )
                is True,
                status.get(
                    "release_gate_closed"
                )
                is True,
                context.get(
                    "current_sprint"
                )
                == "164",
                context.get(
                    "current_version"
                )
                == "0.164.0-genesis",
                bool(context_boundary),
                style.get("alpha_ready") is True,
                style.get("runtime_ready") is False,
                style_items_exact,
                honesty.get("alpha_ready") is True,
                honesty.get("runtime_ready") is False,
                safety.get("alpha_ready") is True,
                safety.get("runtime_ready") is False,
                runtime_false_flags_all_false,
                runtime_zero_counters_all_zero,
            )
        )

        return {
            "available": True,
            "owner":
                self.canonical_persona_contract_owner,
            "name": getattr(
                self.persona_manager,
                "name",
                None,
            ),
            "status": getattr(
                self.persona_manager,
                "status_name",
                None,
            ),
            "context_sprint": context.get(
                "current_sprint"
            ),
            "context_version": context.get(
                "current_version"
            ),
            "status_ready": status.get(
                "local_chat_persona_"
                "response_layer_ready"
            ),
            "data_ready": status.get(
                "local_chat_persona_"
                "response_layer_data_ready"
            ),
            "thin_runtime_alpha": status.get(
                "thin_runtime_alpha"
            ),
            "persona_runtime_enabled":
                status.get(
                    "persona_response_layer_"
                    "runtime_enabled"
                ),
            "release_gate_closed":
                status.get(
                    "release_gate_closed"
                ),
            "context_boundary_ready":
                bool(context_boundary),
            "style_plan_ready":
                style.get("alpha_ready"),
            "style_runtime_ready":
                style.get("runtime_ready"),
            "style_items": style_items,
            "honesty_plan_ready":
                honesty.get("alpha_ready"),
            "honesty_runtime_ready":
                honesty.get("runtime_ready"),
            "safety_plan_ready":
                safety.get("alpha_ready"),
            "safety_runtime_ready":
                safety.get("runtime_ready"),
            "runtime_false_flags_all_false":
                runtime_false_flags_all_false,
            "runtime_zero_counters_all_zero":
                runtime_zero_counters_all_zero,
            "persona_turn_runtime_invoked":
                False,
            "contract_ready": ready,
            "error": None,
        }

    def _fusion_snapshot(self) -> dict[str, Any]:
        try:
            check = self.fusion_manager.check()
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.canonical_upstream_context_owner,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "alpha_ready": False,
                "runtime_ready": False,
                "current_sprint": None,
                "next_sprint": None,
                "next_boundary": None,
                "canonical_session_owner": None,
                "fusion_packet_created": False,
                "context_inference_performed":
                    False,
                "model_request_performed": False,
                "memory_write_performed": False,
                "permission_mutation_performed":
                    False,
                "audit_write_performed": False,
                "execution_performed": False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        contract = check.get(
            "voice_vision_chat_context_"
            "fusion_contract",
            {},
        )

        if not isinstance(contract, dict):
            contract = {}

        fusion_alpha_ready = (
            check.get("alpha_ready") is True
            or check.get("planning_ready") is True
        )

        execution_performed = any(
            contract.get(key) is True
            for key in (
                "command_execution_performed",
                "tool_execution_performed",
                "file_mutation_performed",
                "network_action_performed",
                "background_service_started",
            )
        )

        ready = all(
            (
                check.get("assertion_count") == 84,
                check.get(
                    "failed_assertion_count"
                )
                == 0,
                fusion_alpha_ready is True,
                check.get("runtime_ready") is False,
                contract.get(
                    "partner_runtime_current_sprint"
                )
                == 224,
                contract.get(
                    "partner_runtime_next_sprint"
                )
                == 225,
                contract.get(
                    "partner_runtime_next_boundary"
                )
                == "personality_consistency_runtime",
                contract.get(
                    "canonical_session_owner"
                )
                == self.canonical_session_owner,
                contract.get(
                    "fusion_packet_created"
                )
                is False,
                contract.get(
                    "context_inference_performed"
                )
                is False,
                contract.get(
                    "model_request_performed"
                )
                is False,
                contract.get(
                    "memory_write_performed"
                )
                is False,
                contract.get(
                    "permission_mutation_performed"
                )
                is False,
                contract.get(
                    "audit_write_performed"
                )
                is False,
                execution_performed is False,
            )
        )

        return {
            "available": True,
            "owner":
                self.canonical_upstream_context_owner,
            "assertion_count":
                check.get("assertion_count"),
            "failed_assertion_count":
                check.get(
                    "failed_assertion_count"
                ),
            "alpha_ready":
                fusion_alpha_ready,
            "runtime_ready":
                check.get("runtime_ready"),
            "current_sprint":
                contract.get(
                    "partner_runtime_current_sprint"
                ),
            "next_sprint":
                contract.get(
                    "partner_runtime_next_sprint"
                ),
            "next_boundary":
                contract.get(
                    "partner_runtime_next_boundary"
                ),
            "canonical_session_owner":
                contract.get(
                    "canonical_session_owner"
                ),
            "fusion_packet_created":
                contract.get(
                    "fusion_packet_created"
                ),
            "context_inference_performed":
                contract.get(
                    "context_inference_performed"
                ),
            "model_request_performed":
                contract.get(
                    "model_request_performed"
                ),
            "memory_write_performed":
                contract.get(
                    "memory_write_performed"
                ),
            "permission_mutation_performed":
                contract.get(
                    "permission_mutation_performed"
                ),
            "audit_write_performed":
                contract.get(
                    "audit_write_performed"
                ),
            "execution_performed":
                execution_performed,
            "contract_ready": ready,
            "error": None,
        }

    def _expression_reference_snapshot(
        self,
    ) -> dict[str, Any]:
        available = self.expression_path.is_file()

        class_marker = False

        if available:
            try:
                source = self.expression_path.read_text(
                    encoding="utf-8"
                )

                class_marker = (
                    "class ExpressionLanguageManager"
                    in source
                )
            except Exception:
                class_marker = False

        ready = (
            available
            and class_marker
        )

        return {
            "available": available,
            "source": self.expression_source,
            "reference":
                self.secondary_expression_reference,
            "class_marker": class_marker,
            "role": "secondary_metadata_reference",
            "promoted_to_personality_owner":
                False,
            "instantiated": False,
            "runtime_authority": False,
            "voice_runtime_activated": False,
            "avatar_runtime_activated": False,
            "contract_ready": ready,
        }

    def _personality_profile(
        self,
        identity: dict[str, Any],
        persona: dict[str, Any],
        fusion: dict[str, Any],
    ) -> dict[str, Any]:
        ready = all(
            (
                identity.get(
                    "contract_ready"
                )
                is True,
                persona.get(
                    "contract_ready"
                )
                is True,
                fusion.get(
                    "contract_ready"
                )
                is True,
            )
        )

        return {
            "name":
                "aura_personality_consistency_profile",
            "scope":
                "identity_and_persona_contract_"
                "metadata_only",
            "identity_source":
                self.canonical_identity_source,
            "persona_owner":
                self.canonical_persona_contract_owner,
            "upstream_context_owner":
                self.canonical_upstream_context_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "consistency_dimensions":
                list(self.consistency_dimensions),
            "required_traits":
                list(self.required_traits),
            "required_modes":
                list(self.required_modes),
            "required_style_items":
                list(self.required_style_items),
            "interface_targets":
                list(self.interface_targets),
            "capability_honesty_required":
                True,
            "safety_consistency_required":
                True,
            "modality_neutral":
                True,
            "multi_interface_state_"
            "synchronization_deferred":
                True,
            "payload_free":
                True,
            "deterministic":
                True,
            "ready": ready,
        }

    def _safety_boundary(self) -> dict[str, Any]:
        return {
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "identity_file_mutation_performed":
                False,
            "persona_store_read_performed":
                False,
            "persona_store_write_performed":
                False,
            "persona_response_generated":
                False,
            "persona_turn_runtime_invoked":
                False,
            "chat_payload_read": False,
            "session_payload_read": False,
            "audio_payload_read": False,
            "image_payload_read": False,
            "model_request_performed": False,
            "context_inference_performed":
                False,
            "memory_read_performed": False,
            "memory_write_performed": False,
            "permission_mutation_performed":
                False,
            "audit_write_performed": False,
            "network_action_performed": False,
            "command_execution_performed":
                False,
            "tool_execution_performed": False,
            "file_mutation_performed": False,
            "voice_runtime_activated": False,
            "vision_runtime_activated": False,
            "avatar_runtime_activated": False,
            "background_service_started": False,
            "autonomous_action_performed":
                False,
        }

    def personality_consistency_runtime_contract(
        self,
    ) -> dict[str, Any]:
        identity = self._identity_snapshot()
        persona = self._persona_snapshot()
        fusion = self._fusion_snapshot()

        expression = (
            self._expression_reference_snapshot()
        )

        profile = self._personality_profile(
            identity,
            persona,
            fusion,
        )

        safety = self._safety_boundary()

        safety_closed = all(
            value is False
            for value in safety.values()
        )

        ready = all(
            (
                identity.get(
                    "contract_ready"
                )
                is True,
                persona.get(
                    "contract_ready"
                )
                is True,
                fusion.get(
                    "contract_ready"
                )
                is True,
                expression.get(
                    "contract_ready"
                )
                is True,
                profile.get("ready") is True,
                safety_closed,
            )
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "personality_consistency_"
                "contract_ready"
                if ready
                else (
                    "personality_consistency_"
                    "contract_degraded"
                )
            ),
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "contract_only": True,
            "preview_only": True,
            "metadata_only": True,
            "planning_ready": ready,
            "alpha_ready": ready,
            "runtime_ready": False,
            "personality_consistency_"
            "runtime_contract_ready":
                ready,
            "canonical_identity_source":
                self.canonical_identity_source,
            "canonical_persona_contract_owner":
                self.canonical_persona_contract_owner,
            "canonical_upstream_context_owner":
                self.canonical_upstream_context_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "secondary_expression_reference":
                self.secondary_expression_reference,
            "identity_snapshot": identity,
            "persona_snapshot": persona,
            "fusion_snapshot": fusion,
            "expression_reference_snapshot":
                expression,
            "personality_profile": profile,
            "safety_boundary": safety,
            "multi_interface_state_"
            "synchronization_deferred_to_"
            "sprint_226":
                True,
        }

    def plan(self) -> dict[str, Any]:
        contract = (
            self
            .personality_consistency_runtime_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "planning_ready":
                contract["planning_ready"],
            "runtime_ready": False,
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "personality_profile":
                contract[
                    "personality_profile"
                ],
            "safety_boundary":
                contract["safety_boundary"],
            "note": (
                "Sprint 225 composes identity, "
                "persona, and Sprint 224 fusion "
                "metadata only. It does not "
                "generate responses, read chat "
                "payloads, synchronize interfaces, "
                "invoke models, write memory, or "
                "activate runtime authority."
            ),
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        contract = check[
            "personality_consistency_runtime_contract"
        ]

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
            "planning_ready":
                contract["planning_ready"],
            "alpha_ready":
                contract["alpha_ready"],
            "runtime_ready": False,
            "assertion_count":
                check["assertion_count"],
            "failed_assertion_count":
                check[
                    "failed_assertion_count"
                ],
            "contract_only": True,
            "metadata_only": True,
        }

    def context(self) -> dict[str, Any]:
        contract = (
            self
            .personality_consistency_runtime_contract()
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
            "canonical_identity_source":
                self.canonical_identity_source,
            "canonical_persona_contract_owner":
                self.canonical_persona_contract_owner,
            "canonical_upstream_context_owner":
                self.canonical_upstream_context_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "secondary_expression_reference":
                self.secondary_expression_reference,
            "personality_profile":
                contract[
                    "personality_profile"
                ],
            "identity_snapshot":
                contract["identity_snapshot"],
            "persona_snapshot":
                contract["persona_snapshot"],
            "fusion_snapshot":
                contract["fusion_snapshot"],
            "expression_reference_snapshot":
                contract[
                    "expression_reference_snapshot"
                ],
            "safety_boundary":
                contract["safety_boundary"],
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        contract = (
            self
            .personality_consistency_runtime_contract()
        )

        identity = contract[
            "identity_snapshot"
        ]

        persona = contract[
            "persona_snapshot"
        ]

        fusion = contract[
            "fusion_snapshot"
        ]

        expression = contract[
            "expression_reference_snapshot"
        ]

        profile = contract[
            "personality_profile"
        ]

        safety = contract[
            "safety_boundary"
        ]

        assertions = {
            "project_root_available":
                self.project_root.is_dir(),
            "identity_source_available":
                self.identity_path.is_file(),
            "identity_available":
                identity["available"] is True,
            "identity_version_supported":
                identity[
                    "version_supported"
                ]
                is True,
            "identity_name_aura":
                identity["name"] == "AURA",
            "identity_codename_genesis":
                identity["codename"] == "Genesis",
            "identity_creator_kiput":
                identity["creator"] == "Kiput",
            "identity_motto_grow_together":
                identity["motto"] == "Grow Together",
            "identity_description_present":
                isinstance(
                    identity["description"],
                    str,
                )
                and bool(
                    identity[
                        "description"
                    ].strip()
                ),
            "identity_traits_list":
                isinstance(
                    identity["traits"],
                    list,
                ),
            "identity_required_traits_present":
                identity[
                    "required_traits_present"
                ]
                is True,
            "identity_modes_mapping":
                isinstance(
                    identity["modes"],
                    dict,
                ),
            "identity_required_modes_present":
                identity[
                    "required_modes_present"
                ]
                is True,
            "identity_file_not_mutated":
                safety[
                    "identity_file_"
                    "mutation_performed"
                ]
                is False,
            "identity_contract_ready":
                identity[
                    "contract_ready"
                ]
                is True,

            "persona_owner_available":
                persona["available"] is True,
            "persona_owner_name":
                persona["name"]
                == (
                    "aura_local_chat_"
                    "persona_response_layer"
                ),
            "persona_owner_online":
                persona["status"] == "online",
            "persona_status_ready":
                persona[
                    "status_ready"
                ]
                is True,
            "persona_data_ready":
                persona[
                    "data_ready"
                ]
                is True,
            "persona_thin_runtime_alpha":
                persona[
                    "thin_runtime_alpha"
                ]
                is True,
            "persona_response_runtime_enabled":
                persona[
                    "persona_runtime_enabled"
                ]
                is True,
            "persona_release_gate_closed":
                persona[
                    "release_gate_closed"
                ]
                is True,
            "persona_context_sprint_164":
                persona[
                    "context_sprint"
                ]
                == "164",
            "persona_context_version_164":
                persona[
                    "context_version"
                ]
                == "0.164.0-genesis",
            "persona_context_has_safety_boundary":
                persona[
                    "context_boundary_ready"
                ]
                is True,
            "persona_context_boundary_matches":
                persona[
                    "runtime_false_flags_all_false"
                ]
                is True,
            "persona_style_plan_ready":
                persona[
                    "style_plan_ready"
                ]
                is True,
            "persona_style_plan_runtime_closed":
                persona[
                    "style_runtime_ready"
                ]
                is False,
            "persona_style_items_exact":
                set(
                    persona[
                        "style_items"
                    ]
                )
                == set(
                    self.required_style_items
                ),
            "persona_honesty_plan_ready":
                persona[
                    "honesty_plan_ready"
                ]
                is True,
            "persona_honesty_plan_runtime_closed":
                persona[
                    "honesty_runtime_ready"
                ]
                is False,
            "persona_safety_plan_ready":
                persona[
                    "safety_plan_ready"
                ]
                is True,
            "persona_safety_plan_runtime_closed":
                persona[
                    "safety_runtime_ready"
                ]
                is False,
            "persona_false_flags_all_false":
                persona[
                    "runtime_false_flags_all_false"
                ]
                is True,
            "persona_zero_counters_all_zero":
                persona[
                    "runtime_zero_counters_all_zero"
                ]
                is True,
            "persona_turn_runtime_not_invoked":
                persona[
                    "persona_turn_runtime_invoked"
                ]
                is False,
            "persona_contract_ready":
                persona[
                    "contract_ready"
                ]
                is True,

            "fusion_owner_available":
                fusion["available"] is True,
            "fusion_assertion_count_84":
                fusion[
                    "assertion_count"
                ]
                == 84,
            "fusion_failed_zero":
                fusion[
                    "failed_assertion_count"
                ]
                == 0,
            "fusion_alpha_ready":
                fusion[
                    "alpha_ready"
                ]
                is True,
            "fusion_runtime_closed":
                fusion[
                    "runtime_ready"
                ]
                is False,
            "fusion_current_sprint_224":
                fusion[
                    "current_sprint"
                ]
                == 224,
            "fusion_next_sprint_225":
                fusion[
                    "next_sprint"
                ]
                == 225,
            "fusion_next_boundary_personality":
                fusion[
                    "next_boundary"
                ]
                == "personality_consistency_runtime",
            "fusion_session_owner_preserved":
                fusion[
                    "canonical_session_owner"
                ]
                == self.canonical_session_owner,
            "fusion_packet_not_created":
                fusion[
                    "fusion_packet_created"
                ]
                is False,
            "fusion_inference_not_performed":
                fusion[
                    "context_inference_performed"
                ]
                is False,
            "fusion_model_not_requested":
                fusion[
                    "model_request_performed"
                ]
                is False,
            "fusion_memory_not_written":
                fusion[
                    "memory_write_performed"
                ]
                is False,
            "fusion_permission_not_mutated":
                fusion[
                    "permission_mutation_performed"
                ]
                is False,
            "fusion_audit_not_written":
                fusion[
                    "audit_write_performed"
                ]
                is False,
            "fusion_execution_not_performed":
                fusion[
                    "execution_performed"
                ]
                is False,
            "fusion_contract_ready":
                fusion[
                    "contract_ready"
                ]
                is True,

            "expression_reference_available":
                expression[
                    "available"
                ]
                is True,
            "expression_reference_class_marker":
                expression[
                    "class_marker"
                ]
                is True,
            "expression_reference_secondary_only":
                expression[
                    "role"
                ]
                == "secondary_metadata_reference",
            "expression_reference_not_instantiated":
                expression[
                    "instantiated"
                ]
                is False,
            "expression_reference_no_runtime_authority":
                expression[
                    "runtime_authority"
                ]
                is False,
            "expression_reference_no_voice_activation":
                expression[
                    "voice_runtime_activated"
                ]
                is False,
            "expression_reference_no_avatar_activation":
                expression[
                    "avatar_runtime_activated"
                ]
                is False,
            "expression_reference_ready":
                expression[
                    "contract_ready"
                ]
                is True,

            "profile_name":
                profile["name"]
                == (
                    "aura_personality_"
                    "consistency_profile"
                ),
            "profile_scope":
                profile["scope"]
                == (
                    "identity_and_persona_"
                    "contract_metadata_only"
                ),
            "profile_identity_source":
                profile[
                    "identity_source"
                ]
                == self.canonical_identity_source,
            "profile_persona_owner":
                profile[
                    "persona_owner"
                ]
                == self.canonical_persona_contract_owner,
            "profile_upstream_owner":
                profile[
                    "upstream_context_owner"
                ]
                == self.canonical_upstream_context_owner,
            "profile_session_owner":
                profile[
                    "canonical_session_owner"
                ]
                == self.canonical_session_owner,
            "profile_consistency_dimensions":
                profile[
                    "consistency_dimensions"
                ]
                == list(
                    self.consistency_dimensions
                ),
            "profile_required_traits":
                profile[
                    "required_traits"
                ]
                == list(
                    self.required_traits
                ),
            "profile_required_modes":
                profile[
                    "required_modes"
                ]
                == list(
                    self.required_modes
                ),
            "profile_style_items":
                profile[
                    "required_style_items"
                ]
                == list(
                    self.required_style_items
                ),
            "profile_capability_honesty":
                profile[
                    "capability_honesty_required"
                ]
                is True,
            "profile_safety_consistency":
                profile[
                    "safety_consistency_required"
                ]
                is True,
            "profile_modality_neutral":
                profile[
                    "modality_neutral"
                ]
                is True,
            "profile_interface_sync_deferred":
                profile[
                    "multi_interface_state_"
                    "synchronization_deferred"
                ]
                is True,
            "profile_payload_free":
                profile[
                    "payload_free"
                ]
                is True,
            "profile_deterministic":
                profile[
                    "deterministic"
                ]
                is True,
            "profile_ready":
                profile["ready"] is True,

            "runtime_ready_false":
                safety[
                    "runtime_ready"
                ]
                is False,
            "runtime_activation_disallowed":
                safety[
                    "runtime_activation_allowed"
                ]
                is False,
            "release_gate_closed":
                safety[
                    "release_gate_open"
                ]
                is False,
            "identity_mutation_false":
                safety[
                    "identity_file_"
                    "mutation_performed"
                ]
                is False,
            "persona_store_read_false":
                safety[
                    "persona_store_read_performed"
                ]
                is False,
            "persona_store_write_false":
                safety[
                    "persona_store_write_performed"
                ]
                is False,
            "chat_payload_read_false":
                safety[
                    "chat_payload_read"
                ]
                is False,
            "session_payload_read_false":
                safety[
                    "session_payload_read"
                ]
                is False,
            "model_request_false":
                safety[
                    "model_request_performed"
                ]
                is False,
            "memory_read_false":
                safety[
                    "memory_read_performed"
                ]
                is False,
            "memory_write_false":
                safety[
                    "memory_write_performed"
                ]
                is False,
            "permission_mutation_false":
                safety[
                    "permission_mutation_performed"
                ]
                is False,
            "audit_write_false":
                safety[
                    "audit_write_performed"
                ]
                is False,
            "network_action_false":
                safety[
                    "network_action_performed"
                ]
                is False,
            "execution_false":
                all(
                    safety[key] is False
                    for key in (
                        "command_execution_performed",
                        "tool_execution_performed",
                        "file_mutation_performed",
                        "autonomous_action_performed",
                    )
                ),
            "background_service_false":
                safety[
                    "background_service_started"
                ]
                is False,
        }

        failed_assertions = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "passed"
                if not failed_assertions
                else "failed"
            ),
            "planning_ready":
                not failed_assertions,
            "alpha_ready":
                not failed_assertions,
            "runtime_ready": False,
            "assertion_count":
                len(assertions),
            "failed_assertion_count":
                len(failed_assertions),
            "failed_assertions":
                failed_assertions,
            "assertions": assertions,
            "personality_consistency_runtime_contract":
                contract,
        }
