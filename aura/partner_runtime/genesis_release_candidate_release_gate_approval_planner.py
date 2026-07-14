from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_release_gate_review_planner import (
    GenesisReleaseCandidateReleaseGateReviewPlanner,
)


class GenesisReleaseCandidateReleaseGateApprovalPlanner(
    GenesisReleaseCandidateReleaseGateReviewPlanner
):
    """Read-only Sprint 238 release-gate approval contract."""

    VERSION = "0.238.0-genesis"

    CURRENT_SPRINT = 238
    NEXT_SPRINT = 239

    BOUNDARY = (
        "genesis_release_candidate_release_gate_approval"
    )

    NEXT_BOUNDARY = (
        "genesis_release_candidate_release_decision"
    )

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "release_candidate_release_gate_approval"
    )

    RELEASE_GATE_APPROVAL_DOMAINS = (
        "canonical_checkpoint_integrity",
        "release_authorization_foundation_preservation",
        "release_gate_review_foundation_preservation",
        "seventeen_owner_release_gate_approval_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "release_gate_review_evidence_preservation",
        "release_gate_approval_policy_readiness",
        "release_gate_approval_evidence_readiness",
        "release_gate_condition_inventory_readiness",
        "release_decision_separation",
        "artifact_inventory_readiness",
        "documentation_inventory_readiness",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "operator_control_and_rollback_readiness",
        "safe_idle_and_emergency_stop_preservation",
        "runtime_effect_hold",
        "release_gate_open_separation",
    )

    RELEASE_GATE_APPROVAL_EVIDENCE_INVENTORY = (
        "canonical_identity_evidence",
        "checkpoint_parent_evidence",
        "seventeen_owner_evidence",
        "owner_assertion_evidence",
        "deterministic_method_packet_evidence",
        "handoff_chain_evidence",
        "release_authorization_result_evidence",
        "release_gate_review_result_evidence",
        "release_gate_review_policy_evidence",
        "release_gate_approval_policy_evidence",
        "release_gate_condition_evidence",
        "release_decision_separation_evidence",
        "artifact_inventory_evidence",
        "documentation_inventory_evidence",
        "permission_audit_recovery_evidence",
        "safe_idle_emergency_stop_evidence",
        "operator_control_rollback_evidence",
    )

    ARTIFACT_INVENTORY = (
        "release_candidate_assembly_upstream_contract",
        "release_candidate_verification_upstream_contract",
        "release_candidate_readiness_upstream_contract",
        "release_candidate_approval_upstream_contract",
        "release_authorization_upstream_contract",
        "release_gate_review_upstream_contract",
        "release_gate_approval_planner_contract",
        "release_gate_approval_alpha_manager_contract",
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
        "docs/AURA_GENESIS_FINAL_INTEGRATION_AND_RELEASE.md",
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
            GenesisReleaseCandidateReleaseGateReviewPlanner(
                project_root=self.project_root
            )
        )

        return upstream_planner.contract()

    def _approval_owner_snapshots(
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
                "sprint": 237,

                "owner": (
                    "GenesisReleaseCandidateRelease"
                    "GateReviewAlphaManager"
                ),

                "assertion_count": 988,
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

    def _approval_method_packets(
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
                    "GateReviewAlphaManager.status"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "GateReviewAlphaManager.context"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "GateReviewAlphaManager.plan"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "GateReviewAlphaManager.contract"
                ),
                (
                    "GenesisReleaseCandidateRelease"
                    "GateReviewAlphaManager.check"
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
            self._approval_owner_snapshots(
                upstream
            )
        )

        method_packets = (
            self._approval_method_packets(
                upstream
            )
        )

        required_results = {
            f"{domain}_{suffix}": True
            for domain in self.RELEASE_GATE_APPROVAL_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.RELEASE_GATE_APPROVAL_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "release_gate_approval_decision_applied",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.RELEASE_GATE_APPROVAL_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "release_gate_approval_decision_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_gate_approval_write_count": 0,
                "release_gate_transition_count": 0,
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
            "release_gate_approval_mode": self.MODE,

            "canonical_upstream_owner": (
                "GenesisReleaseCandidateRelease"
                "GateReviewAlphaManager"
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

            "handoff_chain_count": 17,

            "release_gate_approval_domains": list(
                self.RELEASE_GATE_APPROVAL_DOMAINS
            ),

            "release_gate_approval_domain_count": len(
                self.RELEASE_GATE_APPROVAL_DOMAINS
            ),

            "release_gate_approval_evidence_inventory": list(
                self.RELEASE_GATE_APPROVAL_EVIDENCE_INVENTORY
            ),

            "release_gate_approval_evidence_inventory_count": len(
                self.RELEASE_GATE_APPROVAL_EVIDENCE_INVENTORY
            ),

            "release_candidate_artifact_inventory": list(
                self.ARTIFACT_INVENTORY
            ),

            "release_candidate_artifact_inventory_count": len(
                self.ARTIFACT_INVENTORY
            ),

            "release_candidate_documentation_inventory": list(
                self.DOCUMENTATION_INVENTORY
            ),

            "release_candidate_documentation_inventory_count": len(
                self.DOCUMENTATION_INVENTORY
            ),

            "required_release_gate_approval_results":
                required_results,

            "required_release_gate_approval_result_count":
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

            "upstream_release_gate_review_foundation_ready":
                upstream[
                    "release_gate_review_foundation_ready"
                ],

            "upstream_release_gate_review_ready":
                upstream[
                    "release_gate_review_ready"
                ],

            "upstream_release_gate_review_passed":
                upstream[
                    "release_gate_review_passed"
                ],

            "upstream_release_gate_approval_ready":
                upstream[
                    "release_gate_approval_ready"
                ],

            "current_block_started": True,
            "current_block_complete": False,
            "current_block_stabilized": False,
            "current_block_release_ready": False,

            "release_candidate_assembly_foundation_ready": True,
            "release_candidate_verification_foundation_ready": True,
            "release_candidate_readiness_foundation_ready": True,
            "release_candidate_approval_foundation_ready": True,
            "release_authorization_foundation_ready": True,
            "release_gate_review_foundation_ready": True,
            "release_gate_approval_foundation_ready": True,

            "release_gate_approval_evidence_inventory_ready": True,
            "release_candidate_artifact_inventory_ready": True,
            "release_candidate_documentation_inventory_ready": True,

            "release_candidate_assembled": False,
            "release_candidate_ready": False,
            "release_candidate_verified": False,

            "verification_passed": False,
            "readiness_passed": False,

            "release_candidate_approval_ready": False,
            "approval_passed": False,

            "genesis_release_approved": False,
            "release_authorization_ready": False,
            "release_authorization_passed": False,

            "release_gate_review_ready": False,
            "release_gate_review_passed": False,

            "release_gate_approval_ready": False,
            "release_gate_approval_passed": False,

            "release_decision_ready": False,
            "release_decision_passed": False,

            "external_target_methods_invoked": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,

            "genesis_release_candidate_release_gate_approval_contract_ready":
                True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name": contract["name"],
            "version": contract["version"],

            "identity_version":
                contract[
                    "identity_version"
                ],

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

            "owner_count":
                contract[
                    "owner_count"
                ],

            "owner_assertion_total":
                contract[
                    "owner_assertion_total"
                ],

            "owner_failure_count":
                contract[
                    "owner_failure_count"
                ],

            "deterministic_method_packet_count":
                contract[
                    "deterministic_method_packet_count"
                ],

            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ],

            "release_gate_approval_domain_count":
                contract[
                    "release_gate_approval_domain_count"
                ],

            "required_release_gate_approval_result_count":
                contract[
                    "required_release_gate_approval_result_count"
                ],

            "release_gate_approval_foundation_ready":
                contract[
                    "release_gate_approval_foundation_ready"
                ],

            "release_candidate_assembled":
                contract[
                    "release_candidate_assembled"
                ],

            "release_candidate_ready":
                contract[
                    "release_candidate_ready"
                ],

            "release_candidate_verified":
                contract[
                    "release_candidate_verified"
                ],

            "verification_passed":
                contract[
                    "verification_passed"
                ],

            "readiness_passed":
                contract[
                    "readiness_passed"
                ],

            "release_candidate_approval_ready":
                contract[
                    "release_candidate_approval_ready"
                ],

            "approval_passed":
                contract[
                    "approval_passed"
                ],

            "genesis_release_approved":
                contract[
                    "genesis_release_approved"
                ],

            "release_authorization_ready":
                contract[
                    "release_authorization_ready"
                ],

            "release_authorization_passed":
                contract[
                    "release_authorization_passed"
                ],

            "release_gate_review_ready":
                contract[
                    "release_gate_review_ready"
                ],

            "release_gate_review_passed":
                contract[
                    "release_gate_review_passed"
                ],

            "release_gate_approval_ready":
                contract[
                    "release_gate_approval_ready"
                ],

            "release_gate_approval_passed":
                contract[
                    "release_gate_approval_passed"
                ],

            "release_decision_ready":
                contract[
                    "release_decision_ready"
                ],

            "runtime_activation_allowed":
                contract[
                    "runtime_activation_allowed"
                ],

            "release_gate_open":
                contract[
                    "release_gate_open"
                ],

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

            "release_gate_approval_mode":
                contract[
                    "release_gate_approval_mode"
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

            "release_gate_approval_domains":
                contract[
                    "release_gate_approval_domains"
                ],

            "release_gate_approval_evidence_inventory":
                contract[
                    "release_gate_approval_evidence_inventory"
                ],

            "release_candidate_artifact_inventory":
                contract[
                    "release_candidate_artifact_inventory"
                ],

            "release_candidate_documentation_inventory":
                contract[
                    "release_candidate_documentation_inventory"
                ],

            "required_release_gate_approval_results":
                contract[
                    "required_release_gate_approval_results"
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

            "current_block_started": True,
            "current_block_complete": False,
            "current_block_stabilized": False,
            "current_block_release_ready": False,

            "release_candidate_assembled": False,
            "release_candidate_ready": False,
            "release_candidate_verified": False,

            "verification_passed": False,
            "readiness_passed": False,

            "release_candidate_approval_ready": False,
            "approval_passed": False,

            "genesis_release_approved": False,
            "release_authorization_ready": False,
            "release_authorization_passed": False,

            "release_gate_review_ready": False,
            "release_gate_review_passed": False,

            "release_gate_approval_ready": False,
            "release_gate_approval_passed": False,

            "release_decision_ready": False,
            "release_decision_passed": False,

            "runtime_activation_allowed": False,
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
                    "release_gate_approval_mode"
                ],

            "release_gate_approval_domains":
                contract[
                    "release_gate_approval_domains"
                ],

            "required_results":
                contract[
                    "required_release_gate_approval_results"
                ],

            "release_gate_review_decision_allowed": False,
            "release_gate_approval_decision_allowed": False,
            "release_decision_allowed": False,
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
            GenesisReleaseCandidateReleaseGateReviewPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_release_gate_approval_results"
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

        for domain in self.RELEASE_GATE_APPROVAL_DOMAINS:
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
                f"{domain}_negative_approval_decision_false"
            ] = (
                negative_results[
                    f"{domain}_release_gate_approval_decision_applied"
                ]
                is False
            )

        local_assertions[
            "seventeen_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "0.238.0-genesis"

            and contract[
                "current_sprint"
            ] == 238

            and contract[
                "next_sprint"
            ] == 239

            and contract[
                "boundary"
            ] == (
                "genesis_release_candidate_"
                "release_gate_approval"
            )

            and contract[
                "next_boundary"
            ] == (
                "genesis_release_candidate_"
                "release_decision"
            )

            and upstream_check[
                "assertion_count"
            ] == 988

            and upstream_check[
                "failed_assertion_count"
            ] == 0

            and upstream_check[
                "runtime_ready"
            ] is False

            and contract[
                "owner_count"
            ] == 17

            and contract[
                "owner_assertion_total"
            ] == 7430

            and contract[
                "owner_failure_count"
            ] == 0

            and contract[
                "deterministic_method_packet_count"
            ] == 75

            and len(
                set(method_packets)
            ) == 75

            and contract[
                "handoff_chain_count"
            ] == 17
        )

        local_assertions[
            "release_gate_approval_inventory_projection_matches"
        ] = (
            contract[
                "release_gate_approval_domain_count"
            ] == 19

            and contract[
                "required_release_gate_approval_result_count"
            ] == 57

            and all(
                value is True
                for value in required_results.values()
            )

            and contract[
                "release_gate_approval_evidence_inventory_count"
            ] == 17

            and contract[
                "release_candidate_artifact_inventory_count"
            ] == 14

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 12
        )

        local_assertions[
            "release_gate_hold_state_preserved"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 38

            and all(
                value is False
                for value in negative_results.values()
            )

            and contract[
                "safety_boundary_count"
            ] == 38

            and all(
                value is False
                for value in safety_boundary.values()
            )

            and contract[
                "zero_counter_count"
            ] == 41

            and all(
                value == 0
                for value in zero_counters.values()
            )

            and contract[
                "current_block_started"
            ] is True

            and contract[
                "current_block_complete"
            ] is False

            and contract[
                "current_block_stabilized"
            ] is False

            and contract[
                "current_block_release_ready"
            ] is False

            and contract[
                "release_candidate_assembled"
            ] is False

            and contract[
                "release_candidate_ready"
            ] is False

            and contract[
                "release_candidate_verified"
            ] is False

            and contract[
                "verification_passed"
            ] is False

            and contract[
                "readiness_passed"
            ] is False

            and contract[
                "release_candidate_approval_ready"
            ] is False

            and contract[
                "approval_passed"
            ] is False

            and contract[
                "genesis_release_approved"
            ] is False

            and contract[
                "release_authorization_ready"
            ] is False

            and contract[
                "release_authorization_passed"
            ] is False

            and contract[
                "release_gate_review_ready"
            ] is False

            and contract[
                "release_gate_review_passed"
            ] is False

            and contract[
                "release_gate_approval_ready"
            ] is False

            and contract[
                "release_gate_approval_passed"
            ] is False

            and contract[
                "release_decision_ready"
            ] is False

            and contract[
                "release_decision_passed"
            ] is False

            and contract[
                "external_target_methods_invoked"
            ] is False

            and contract[
                "runtime_activation_allowed"
            ] is False

            and contract[
                "release_gate_open"
            ] is False

            and contract[
                "runtime_ready"
            ] is False
        )

        local_assertions[
            "release_gate_approval_contract_shape_ready"
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
                "upstream_release_gate_review_foundation_ready"
            ] is True

            and contract[
                "release_candidate_assembly_foundation_ready"
            ] is True

            and contract[
                "release_candidate_verification_foundation_ready"
            ] is True

            and contract[
                "release_candidate_readiness_foundation_ready"
            ] is True

            and contract[
                "release_candidate_approval_foundation_ready"
            ] is True

            and contract[
                "release_authorization_foundation_ready"
            ] is True

            and contract[
                "release_gate_review_foundation_ready"
            ] is True

            and contract[
                "release_gate_approval_foundation_ready"
            ] is True

            and contract[
                "release_gate_approval_evidence_inventory_ready"
            ] is True

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True

            and contract[
                "genesis_release_candidate_release_gate_approval_contract_ready"
            ] is True
        )

        local_assertions[
            "release_gate_review_state_preserved"
        ] = (
            contract[
                "upstream_release_gate_review_ready"
            ] is False

            and contract[
                "upstream_release_gate_review_passed"
            ] is False

            and contract[
                "upstream_release_gate_approval_ready"
            ] is False

            and upstream_check[
                "local_assertion_count"
            ] == 82

            and upstream_check[
                "failed_assertions"
            ] == []
        )

        local_assertions[
            "release_gate_approval_decision_separation_preserved"
        ] = (
            contract[
                "release_gate_review_ready"
            ] is False

            and contract[
                "release_gate_review_passed"
            ] is False

            and contract[
                "release_gate_approval_ready"
            ] is False

            and contract[
                "release_gate_approval_passed"
            ] is False
        )

        local_assertions[
            "release_decision_separation_preserved"
        ] = (
            contract[
                "release_gate_approval_ready"
            ] is False

            and contract[
                "release_gate_approval_passed"
            ] is False

            and contract[
                "release_decision_ready"
            ] is False

            and contract[
                "release_decision_passed"
            ] is False

            and contract[
                "runtime_activation_allowed"
            ] is False

            and contract[
                "release_gate_open"
            ] is False
        )

        local_assertions[
            "interface_surface_projection_ready"
        ] = (
            self.BOUNDARY
            == (
                "genesis_release_candidate_"
                "release_gate_approval"
            )

            and self.NEXT_BOUNDARY
            == (
                "genesis_release_candidate_"
                "release_decision"
            )

            and self.MODE
            == (
                "contract_only_read_only_"
                "release_candidate_release_gate_approval"
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
                "release_candidate_artifact_inventory_count"
            ] == 14

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 12

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True
        )

        local_assertions[
            "release_gate_approval_policy_ready"
        ] = (
            contract[
                "release_gate_approval_domain_count"
            ] == 19

            and contract[
                "release_gate_approval_evidence_inventory_count"
            ] == 17

            and contract[
                "release_gate_approval_foundation_ready"
            ] is True

            and contract[
                "release_gate_approval_ready"
            ] is False

            and contract[
                "release_gate_approval_passed"
            ] is False

            and contract[
                "release_decision_ready"
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
                f"Sprint238:{name}"
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

            "genesis_release_candidate_release_gate_approval_contract":
                contract,

            "runtime_ready": False,
        }
