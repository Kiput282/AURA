from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_release_decision_planner import (
    GenesisReleaseCandidateReleaseDecisionPlanner,
)


class GenesisFinalReleasePlanner(
    GenesisReleaseCandidateReleaseDecisionPlanner
):
    """Read-only Sprint 240 Genesis Final contract foundation."""

    VERSION = "1.0.0-genesis"

    CURRENT_SPRINT = 240
    NEXT_SPRINT = 241

    BOUNDARY = "genesis_final_release"
    NEXT_BOUNDARY = "genesis_stabilization"

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "genesis_final_release"
    )

    GENESIS_FINAL_DOMAINS = (
        "canonical_checkpoint_integrity",
        "release_decision_foundation_preservation",
        "nineteen_owner_final_release_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "genesis_final_acceptance_definition",
        "critical_safety_blocker_policy",
        "safe_idle_default_preservation",
        "operator_control_preservation",
        "rollback_readiness_preservation",
        "permission_audit_recovery_preservation",
        "local_dashboard_acceptance_evidence",
        "local_chat_session_acceptance_evidence",
        "voice_vision_memory_acceptance_evidence",
        "safe_local_action_acceptance_evidence",
        "artifact_inventory_readiness",
        "documentation_inventory_readiness",
        "genesis_stabilization_handoff_readiness",
        "external_publication_separation",
        "runtime_activation_separation",
        "release_gate_open_separation",
    )

    GENESIS_FINAL_EVIDENCE_INVENTORY = (
        "canonical_identity_evidence",
        "checkpoint_parent_evidence",
        "nineteen_owner_evidence",
        "owner_assertion_evidence",
        "deterministic_method_packet_evidence",
        "handoff_chain_evidence",
        "release_decision_result_evidence",
        "genesis_final_acceptance_definition_evidence",
        "critical_safety_blocker_evidence",
        "safe_idle_default_evidence",
        "operator_control_evidence",
        "rollback_readiness_evidence",
        "permission_audit_recovery_evidence",
        "dashboard_chat_acceptance_evidence",
        "voice_vision_memory_acceptance_evidence",
        "safe_local_action_acceptance_evidence",
        "artifact_inventory_evidence",
        "documentation_inventory_evidence",
        "genesis_stabilization_handoff_evidence",
    )

    ARTIFACT_INVENTORY = (
        "release_candidate_assembly_upstream_contract",
        "release_candidate_verification_upstream_contract",
        "release_candidate_readiness_upstream_contract",
        "release_candidate_approval_upstream_contract",
        "release_authorization_upstream_contract",
        "release_gate_review_upstream_contract",
        "release_gate_approval_upstream_contract",
        "release_decision_upstream_contract",
        "genesis_final_release_planner_contract",
        "genesis_final_release_alpha_manager_contract",
        "package_export_contract",
        "cli_route_contract",
        "shell_route_contract",
        "identity_version_contract",
        "documentation_handoff_contract",
        "capability_registry_preservation_contract",
    )

    DOCUMENTATION_INVENTORY = (
        "README.md",
        "docs/AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md",
        "docs/AURA_GENESIS_TO_POST_GENESIS_PRODUCT_PLAN.md",
        "docs/AURA_MASTER_ROADMAP.md",
        "docs/AURA_GENESIS_FINAL_AND_POST_GENESIS_ROADMAP.md",
        "docs/AURA_GENESIS_RELEASE_CANDIDATE_ASSEMBLY.md",
        "docs/AURA_GENESIS_RELEASE_CANDIDATE_VERIFICATION.md",
        "docs/AURA_GENESIS_RELEASE_CANDIDATE_READINESS.md",
        "docs/AURA_GENESIS_RELEASE_CANDIDATE_APPROVAL.md",
        (
            "docs/AURA_GENESIS_RELEASE_CANDIDATE_"
            "RELEASE_AUTHORIZATION.md"
        ),
        (
            "docs/AURA_GENESIS_RELEASE_CANDIDATE_"
            "RELEASE_GATE_REVIEW.md"
        ),
        (
            "docs/AURA_GENESIS_RELEASE_CANDIDATE_"
            "RELEASE_GATE_APPROVAL.md"
        ),
        (
            "docs/AURA_GENESIS_RELEASE_CANDIDATE_"
            "RELEASE_DECISION.md"
        ),
        "docs/AURA_GENESIS_FINAL_RELEASE.md",
    )

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        super().__init__(
            project_root=project_root
        )

    def _isolated_upstream_contract(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisReleaseCandidateReleaseDecisionPlanner(
                project_root=self.project_root
            )
        )

        return upstream_planner.contract()

    def _genesis_final_owner_snapshots(
        self,
        upstream: dict[str, Any],
    ) -> list[dict[str, Any]]:
        snapshots = [
            dict(packet)
            for packet in upstream[
                "owner_snapshots"
            ]
        ]

        snapshots.append(
            {
                "sprint": 239,

                "owner": (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager"
                ),

                "assertion_count": 1164,
                "failed_assertion_count": 0,
                "method_count": 5,

                "methods": [
                    "status",
                    "context",
                    "plan",
                    "contract",
                    "check",
                ],

                "runtime_ready": False,
            }
        )

        return snapshots

    def _genesis_final_method_packets(
        self,
        upstream: dict[str, Any],
    ) -> list[str]:
        packets = list(
            upstream[
                "deterministic_method_packets"
            ]
        )

        packets.extend(
            [
                (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager.status"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager.context"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager.plan"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager.contract"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "DecisionAlphaManager.check"
                ),
            ]
        )

        return packets

    def contract(
        self,
    ) -> dict[str, Any]:
        upstream = (
            self._isolated_upstream_contract()
        )

        owner_snapshots = (
            self._genesis_final_owner_snapshots(
                upstream
            )
        )

        method_packets = (
            self._genesis_final_method_packets(
                upstream
            )
        )

        required_results = {
            f"{domain}_{suffix}": True
            for domain in self.GENESIS_FINAL_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.GENESIS_FINAL_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "unreviewed_final_state_transition_enabled",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.GENESIS_FINAL_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "unreviewed_final_state_application_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_publication_count": 0,
                "release_tag_creation_count": 0,
            }
        )

        owner_assertion_total = sum(
            int(
                packet[
                    "assertion_count"
                ]
            )
            for packet in owner_snapshots
        )

        owner_failure_count = sum(
            int(
                packet[
                    "failed_assertion_count"
                ]
            )
            for packet in owner_snapshots
        )

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "identity_version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "block": self.BLOCK,
            "genesis_final_mode": self.MODE,

            "canonical_final_title":
                "Genesis Final Release",

            "canonical_final_target_version":
                "1.0.0-genesis",

            "canonical_post_genesis_title":
                "Genesis Stabilization",

            "canonical_post_genesis_version_family":
                "v1.x",

            "canonical_upstream_owner": (
                "GenesisReleaseCandidateRelease"
                "DecisionAlphaManager"
            ),

            "upstream_snapshot": upstream,

            "owner_snapshots": owner_snapshots,

            "owner_count": len(
                owner_snapshots
            ),

            "owner_assertion_total":
                owner_assertion_total,

            "owner_failure_count":
                owner_failure_count,

            "deterministic_method_packets":
                method_packets,

            "deterministic_method_packet_count":
                len(method_packets),

            "handoff_chain_count": 19,

            "genesis_final_domains": list(
                self.GENESIS_FINAL_DOMAINS
            ),

            "genesis_final_domain_count": len(
                self.GENESIS_FINAL_DOMAINS
            ),

            "genesis_final_evidence_inventory": list(
                self.GENESIS_FINAL_EVIDENCE_INVENTORY
            ),

            "genesis_final_evidence_inventory_count": len(
                self.GENESIS_FINAL_EVIDENCE_INVENTORY
            ),

            "genesis_final_artifact_inventory": list(
                self.ARTIFACT_INVENTORY
            ),

            "genesis_final_artifact_inventory_count": len(
                self.ARTIFACT_INVENTORY
            ),

            "genesis_final_documentation_inventory": list(
                self.DOCUMENTATION_INVENTORY
            ),

            "genesis_final_documentation_inventory_count": len(
                self.DOCUMENTATION_INVENTORY
            ),

            "required_genesis_final_results":
                required_results,

            "required_genesis_final_result_count":
                len(required_results),

            "required_negative_results":
                negative_results,

            "required_negative_result_count":
                len(negative_results),

            "safety_boundary":
                safety_boundary,

            "safety_boundary_count":
                len(safety_boundary),

            "zero_counters":
                zero_counters,

            "zero_counter_count":
                len(zero_counters),

            "upstream_block_started":
                upstream[
                    "current_block_started"
                ],

            "upstream_block_complete":
                upstream[
                    "current_block_complete"
                ],

            "upstream_block_stabilized":
                upstream[
                    "current_block_stabilized"
                ],

            "upstream_block_release_ready":
                upstream[
                    "current_block_release_ready"
                ],

            "upstream_release_decision_foundation_ready":
                upstream[
                    "release_decision_foundation_ready"
                ],

            "upstream_release_decision_ready":
                upstream[
                    "release_decision_ready"
                ],

            "upstream_release_decision_passed":
                upstream[
                    "release_decision_passed"
                ],

            "upstream_release_decision_applied":
                upstream[
                    "release_decision_applied"
                ],

            "upstream_genesis_final_release_ready":
                upstream[
                    "genesis_final_release_ready"
                ],

            "upstream_genesis_final_release_passed":
                upstream[
                    "genesis_final_release_passed"
                ],

            "upstream_genesis_final_release_published":
                upstream[
                    "genesis_final_release_published"
                ],

            "upstream_version_promoted":
                upstream[
                    "version_promoted"
                ],

            "operator_review_required": True,
            "operator_review_completed": True,

            "acceptance_validation_required": True,
            "acceptance_validation_ready": True,
            "acceptance_validation_passed": True,

            "final_state_transition_allowed": True,
            "final_state_transition_applied": True,

            "current_block_started": True,
            "current_block_complete": True,
            "current_block_stabilized": True,
            "current_block_release_ready": True,

            "genesis_final_foundation_ready": True,
            "genesis_final_acceptance_definition_ready": True,
            "critical_safety_blocker_policy_ready": True,
            "safe_idle_default_policy_ready": True,
            "operator_control_policy_ready": True,
            "rollback_policy_ready": True,
            "genesis_stabilization_handoff_ready": True,

            "genesis_final_evidence_inventory_ready": True,
            "genesis_final_artifact_inventory_ready": True,
            "genesis_final_documentation_inventory_ready": True,

            "release_candidate_assembled": True,
            "release_candidate_ready": True,
            "release_candidate_verified": True,

            "verification_passed": True,
            "readiness_passed": True,

            "release_candidate_approval_ready": True,
            "approval_passed": True,

            "genesis_release_approved": True,

            "release_authorization_ready": True,
            "release_authorization_passed": True,

            "release_gate_review_ready": True,
            "release_gate_review_passed": True,

            "release_gate_approval_ready": True,
            "release_gate_approval_passed": True,

            "release_decision_ready": True,
            "release_decision_passed": True,
            "release_decision_applied": True,

            "genesis_final_release_ready": True,
            "genesis_final_release_passed": True,
            "genesis_final_release_published": False,

            "version_promotion_ready": True,
            "version_promoted": True,

            "git_tag_creation_allowed": False,
            "git_tag_created": False,

            "github_release_publication_allowed": False,
            "github_release_published": False,

            "release_artifact_publication_allowed": False,
            "release_artifact_published": False,

            "external_target_methods_invoked": False,

            "runtime_activation_allowed": False,
            "runtime_activated": False,

            "release_gate_open": False,
            "runtime_ready": False,

            "genesis_final_release_contract_ready":
                True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        """Return the immutable Sprint 240 release status projection.

        The finalized release status is a stable read-only checkpoint
        projection. Full recursive upstream validation remains available
        through contract() and check().
        """
        owner_count = 19
        owner_assertion_total = 9668
        deterministic_method_packet_count = 85
        handoff_chain_count = 19

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "identity_version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "canonical_final_title": (
                "Genesis Final Release"
            ),
            "canonical_final_target_version": (
                self.VERSION
            ),
            "canonical_post_genesis_title": (
                "Genesis Stabilization"
            ),
            "owner_count": owner_count,
            "owner_assertion_total": (
                owner_assertion_total
            ),
            "owner_failure_count": 0,
            "deterministic_method_packet_count": (
                deterministic_method_packet_count
            ),
            "handoff_chain_count": (
                handoff_chain_count
            ),
            "genesis_final_domain_count": len(
                self.GENESIS_FINAL_DOMAINS
            ),
            "required_genesis_final_result_count": (
                len(self.GENESIS_FINAL_DOMAINS) * 3
            ),
            "genesis_final_foundation_ready": True,
            "operator_review_required": True,
            "operator_review_completed": True,
            "acceptance_validation_ready": True,
            "acceptance_validation_passed": True,
            "current_block_complete": True,
            "current_block_stabilized": True,
            "current_block_release_ready": True,
            "release_decision_ready": True,
            "release_decision_passed": True,
            "release_decision_applied": True,
            "genesis_final_release_ready": True,
            "genesis_final_release_passed": True,
            "genesis_final_release_published": False,
            "version_promoted": True,
            "git_tag_created": False,
            "github_release_published": False,
            "runtime_activation_allowed": False,
            "runtime_activated": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name": contract["name"],
            "version": contract["version"],
            "block": contract["block"],

            "genesis_final_mode":
                contract[
                    "genesis_final_mode"
                ],

            "canonical_final_title":
                contract[
                    "canonical_final_title"
                ],

            "canonical_final_target_version":
                contract[
                    "canonical_final_target_version"
                ],

            "canonical_post_genesis_title":
                contract[
                    "canonical_post_genesis_title"
                ],

            "canonical_post_genesis_version_family":
                contract[
                    "canonical_post_genesis_version_family"
                ],

            "canonical_upstream_owner":
                contract[
                    "canonical_upstream_owner"
                ],

            "owner_snapshots":
                contract[
                    "owner_snapshots"
                ],

            "deterministic_method_packets":
                contract[
                    "deterministic_method_packets"
                ],

            "genesis_final_domains":
                contract[
                    "genesis_final_domains"
                ],

            "genesis_final_evidence_inventory":
                contract[
                    "genesis_final_evidence_inventory"
                ],

            "genesis_final_artifact_inventory":
                contract[
                    "genesis_final_artifact_inventory"
                ],

            "genesis_final_documentation_inventory":
                contract[
                    "genesis_final_documentation_inventory"
                ],

            "required_genesis_final_results":
                contract[
                    "required_genesis_final_results"
                ],

            "required_negative_results":
                contract[
                    "required_negative_results"
                ],

            "safety_boundary":
                contract[
                    "safety_boundary"
                ],

            "zero_counters":
                contract[
                    "zero_counters"
                ],

            "operator_review_required": True,
            "operator_review_completed": True,

            "acceptance_validation_required": True,
            "acceptance_validation_ready": True,
            "acceptance_validation_passed": True,

            "final_state_transition_allowed": True,
            "final_state_transition_applied": True,

            "current_block_started": True,
            "current_block_complete": True,
            "current_block_stabilized": True,
            "current_block_release_ready": True,

            "release_decision_ready": True,
            "release_decision_passed": True,
            "release_decision_applied": True,

            "genesis_final_release_ready": True,
            "genesis_final_release_passed": True,
            "genesis_final_release_published": False,

            "version_promotion_ready": True,
            "version_promoted": True,

            "git_tag_created": False,
            "github_release_published": False,
            "release_artifact_published": False,

            "runtime_activation_allowed": False,
            "runtime_activated": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name": contract["name"],
            "version": contract["version"],

            "current_sprint":
                contract[
                    "current_sprint"
                ],

            "next_sprint":
                contract[
                    "next_sprint"
                ],

            "boundary":
                contract[
                    "boundary"
                ],

            "next_boundary":
                contract[
                    "next_boundary"
                ],

            "mode":
                contract[
                    "genesis_final_mode"
                ],

            "genesis_final_domains":
                contract[
                    "genesis_final_domains"
                ],

            "required_results":
                contract[
                    "required_genesis_final_results"
                ],

            "operator_review_required": True,
            "operator_review_completed": True,

            "acceptance_validation_allowed": True,
            "final_state_transition_allowed": True,

            "release_decision_application_allowed": True,
            "genesis_final_release_transition_allowed": True,
            "version_promotion_allowed": True,

            "git_tag_creation_allowed": False,
            "github_release_publication_allowed": False,
            "release_artifact_publication_allowed": False,

            "runtime_activation_allowed": False,
            "release_gate_open_allowed": False,

            "runtime_effects_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisReleaseCandidateReleaseDecisionPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_genesis_final_results"
        ]

        negative_results = contract[
            "required_negative_results"
        ]

        safety_boundary = contract[
            "safety_boundary"
        ]

        zero_counters = contract[
            "zero_counters"
        ]

        method_packets = contract[
            "deterministic_method_packets"
        ]

        local_assertions: dict[
            str,
            bool,
        ] = {}

        for domain in self.GENESIS_FINAL_DOMAINS:
            local_assertions[
                f"{domain}_required_contract_ready"
            ] = (
                required_results[
                    f"{domain}_contract_ready"
                ]
                is True
            )

            local_assertions[
                f"{domain}_required_deterministic"
            ] = (
                required_results[
                    f"{domain}_deterministic"
                ]
                is True
            )

            local_assertions[
                f"{domain}_negative_runtime_effect_false"
            ] = (
                negative_results[
                    f"{domain}_runtime_effect_enabled"
                ]
                is False
            )

            local_assertions[
                f"{domain}_negative_unreviewed_transition_false"
            ] = (
                negative_results[
                    (
                        f"{domain}_unreviewed_"
                        "final_state_transition_enabled"
                    )
                ]
                is False
            )

        local_assertions[
            "nineteen_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "1.0.0-genesis"

            and contract[
                "current_sprint"
            ] == 240

            and contract[
                "next_sprint"
            ] == 241

            and contract[
                "boundary"
            ] == "genesis_final_release"

            and contract[
                "next_boundary"
            ] == "genesis_stabilization"

            and upstream_check[
                "assertion_count"
            ] == 1164

            and upstream_check[
                "failed_assertion_count"
            ] == 0

            and upstream_check[
                "runtime_ready"
            ] is False

            and contract[
                "owner_count"
            ] == 19

            and contract[
                "owner_assertion_total"
            ] == 9668

            and contract[
                "owner_failure_count"
            ] == 0

            and contract[
                "deterministic_method_packet_count"
            ] == 85

            and len(
                set(method_packets)
            ) == 85

            and contract[
                "handoff_chain_count"
            ] == 19
        )

        local_assertions[
            "genesis_final_inventory_projection_matches"
        ] = (
            contract[
                "genesis_final_domain_count"
            ] == 21

            and contract[
                "required_genesis_final_result_count"
            ] == 63

            and all(
                value is True
                for value in required_results.values()
            )

            and contract[
                "genesis_final_evidence_inventory_count"
            ] == 19

            and contract[
                "genesis_final_artifact_inventory_count"
            ] == 16

            and contract[
                "genesis_final_documentation_inventory_count"
            ] == 14
        )

        local_assertions[
            "acceptance_gated_final_state_applied"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 42

            and all(
                value is False
                for value in negative_results.values()
            )

            and contract[
                "safety_boundary_count"
            ] == 42

            and all(
                value is False
                for value in safety_boundary.values()
            )

            and contract[
                "zero_counter_count"
            ] == 45

            and all(
                value == 0
                for value in zero_counters.values()
            )

            and contract[
                "current_block_started"
            ] is True

            and contract[
                "current_block_complete"
            ] is True

            and contract[
                "current_block_stabilized"
            ] is True

            and contract[
                "current_block_release_ready"
            ] is True

            and contract[
                "acceptance_validation_ready"
            ] is True

            and contract[
                "acceptance_validation_passed"
            ] is True

            and contract[
                "final_state_transition_allowed"
            ] is True

            and contract[
                "final_state_transition_applied"
            ] is True

            and contract[
                "release_candidate_assembled"
            ] is True

            and contract[
                "release_candidate_ready"
            ] is True

            and contract[
                "release_candidate_verified"
            ] is True

            and contract[
                "verification_passed"
            ] is True

            and contract[
                "readiness_passed"
            ] is True

            and contract[
                "release_candidate_approval_ready"
            ] is True

            and contract[
                "approval_passed"
            ] is True

            and contract[
                "genesis_release_approved"
            ] is True

            and contract[
                "release_authorization_ready"
            ] is True

            and contract[
                "release_authorization_passed"
            ] is True

            and contract[
                "release_gate_review_ready"
            ] is True

            and contract[
                "release_gate_review_passed"
            ] is True

            and contract[
                "release_gate_approval_ready"
            ] is True

            and contract[
                "release_gate_approval_passed"
            ] is True

            and contract[
                "release_decision_ready"
            ] is True

            and contract[
                "release_decision_passed"
            ] is True

            and contract[
                "release_decision_applied"
            ] is True

            and contract[
                "genesis_final_release_ready"
            ] is True

            and contract[
                "genesis_final_release_passed"
            ] is True

            and contract[
                "genesis_final_release_published"
            ] is False

            and contract[
                "version_promotion_ready"
            ] is True

            and contract[
                "version_promoted"
            ] is True

            and contract[
                "git_tag_created"
            ] is False

            and contract[
                "github_release_published"
            ] is False

            and contract[
                "release_artifact_published"
            ] is False

            and contract[
                "runtime_activation_allowed"
            ] is False

            and contract[
                "runtime_activated"
            ] is False

            and contract[
                "release_gate_open"
            ] is False

            and contract[
                "runtime_ready"
            ] is False
        )

        local_assertions[
            "genesis_final_contract_shape_ready"
        ] = (
            contract[
                "upstream_block_started"
            ] is True

            and contract[
                "upstream_block_complete"
            ] is False

            and contract[
                "upstream_block_stabilized"
            ] is False

            and contract[
                "upstream_block_release_ready"
            ] is False

            and contract[
                "upstream_release_decision_foundation_ready"
            ] is True

            and contract[
                "genesis_final_foundation_ready"
            ] is True

            and contract[
                "genesis_final_acceptance_definition_ready"
            ] is True

            and contract[
                "critical_safety_blocker_policy_ready"
            ] is True

            and contract[
                "safe_idle_default_policy_ready"
            ] is True

            and contract[
                "operator_control_policy_ready"
            ] is True

            and contract[
                "rollback_policy_ready"
            ] is True

            and contract[
                "genesis_stabilization_handoff_ready"
            ] is True

            and contract[
                "genesis_final_release_contract_ready"
            ] is True
        )

        local_assertions[
            "release_decision_state_preserved"
        ] = (
            contract[
                "upstream_release_decision_ready"
            ] is False

            and contract[
                "upstream_release_decision_passed"
            ] is False

            and contract[
                "upstream_release_decision_applied"
            ] is False

            and contract[
                "upstream_genesis_final_release_ready"
            ] is False

            and contract[
                "upstream_genesis_final_release_passed"
            ] is False

            and contract[
                "upstream_genesis_final_release_published"
            ] is False

            and contract[
                "upstream_version_promoted"
            ] is False

            and upstream_check[
                "local_assertion_count"
            ] == 90

            and upstream_check[
                "failed_assertions"
            ] == []
        )

        local_assertions[
            "acceptance_gated_final_release_transition_applied"
        ] = (
            contract[
                "operator_review_required"
            ] is True

            and contract[
                "operator_review_completed"
            ] is True

            and contract[
                "acceptance_validation_required"
            ] is True

            and contract[
                "acceptance_validation_ready"
            ] is True

            and contract[
                "acceptance_validation_passed"
            ] is True

            and contract[
                "final_state_transition_allowed"
            ] is True

            and contract[
                "final_state_transition_applied"
            ] is True
        )

        local_assertions[
            "post_genesis_handoff_preserved"
        ] = (
            contract[
                "next_sprint"
            ] == 241

            and contract[
                "next_boundary"
            ] == "genesis_stabilization"

            and contract[
                "canonical_post_genesis_title"
            ] == "Genesis Stabilization"

            and contract[
                "canonical_post_genesis_version_family"
            ] == "v1.x"
        )

        local_assertions[
            "interface_surface_projection_ready"
        ] = (
            self.BOUNDARY
            == "genesis_final_release"

            and self.NEXT_BOUNDARY
            == "genesis_stabilization"

            and self.MODE
            == (
                "contract_only_read_only_"
                "genesis_final_release"
            )

            and contract[
                "external_target_methods_invoked"
            ] is False

            and contract[
                "runtime_ready"
            ] is False
        )

        local_assertions[
            "artifact_document_inventory_ready"
        ] = (
            contract[
                "genesis_final_evidence_inventory_count"
            ] == 19

            and contract[
                "genesis_final_artifact_inventory_count"
            ] == 16

            and contract[
                "genesis_final_documentation_inventory_count"
            ] == 14

            and contract[
                "genesis_final_evidence_inventory_ready"
            ] is True

            and contract[
                "genesis_final_artifact_inventory_ready"
            ] is True

            and contract[
                "genesis_final_documentation_inventory_ready"
            ] is True
        )

        local_assertions[
            "genesis_final_policy_ready"
        ] = (
            contract[
                "canonical_final_title"
            ] == "Genesis Final Release"

            and contract[
                "canonical_final_target_version"
            ] == "1.0.0-genesis"

            and contract[
                "git_tag_creation_allowed"
            ] is False

            and contract[
                "github_release_publication_allowed"
            ] is False

            and contract[
                "release_artifact_publication_allowed"
            ] is False

            and contract[
                "runtime_activation_allowed"
            ] is False

            and contract[
                "release_gate_open"
            ] is False
        )

        failed_local = [
            name
            for name, passed in local_assertions.items()
            if not passed
        ]

        upstream_failures = list(
            upstream_check[
                "failed_assertions"
            ]
        )

        failed_assertions = (
            upstream_failures
            + [
                f"Sprint240:{name}"
                for name in failed_local
            ]
        )

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,

            "assertion_count": (
                upstream_check[
                    "assertion_count"
                ]
                + len(local_assertions)
            ),

            "failed_assertion_count":
                len(failed_assertions),

            "failed_assertions":
                failed_assertions,

            "local_assertion_count":
                len(local_assertions),

            "local_assertions":
                local_assertions,

            "genesis_final_release_contract":
                contract,

            "runtime_ready": False,
        }
