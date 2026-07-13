from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_approval_planner import (
    GenesisReleaseCandidateApprovalPlanner,
)


class GenesisReleaseCandidateReleaseAuthorizationPlanner(
    GenesisReleaseCandidateApprovalPlanner
):
    """Read-only Sprint 236 release-authorization contract."""

    VERSION = "0.236.0-genesis"

    CURRENT_SPRINT = 236
    NEXT_SPRINT = 237

    BOUNDARY = (
        "genesis_release_candidate_release_authorization"
    )

    NEXT_BOUNDARY = (
        "genesis_release_candidate_release_gate_review"
    )

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "release_candidate_release_authorization"
    )

    AUTHORIZATION_DOMAINS = (
        "canonical_checkpoint_integrity",
        "release_candidate_approval_foundation_preservation",
        "fifteen_owner_authorization_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "approval_evidence_preservation",
        "release_authorization_policy_readiness",
        "release_authorization_evidence_readiness",
        "artifact_inventory_readiness",
        "documentation_inventory_readiness",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "operator_control_and_rollback_readiness",
        "safe_idle_and_emergency_stop_preservation",
        "runtime_effect_hold",
        "release_authorization_decision_separation",
        "release_gate_review_separation",
    )

    AUTHORIZATION_EVIDENCE_INVENTORY = (
        "canonical_identity_evidence",
        "checkpoint_parent_evidence",
        "fifteen_owner_evidence",
        "owner_assertion_evidence",
        "deterministic_method_packet_evidence",
        "handoff_chain_evidence",
        "approval_result_evidence",
        "approval_policy_evidence",
        "release_authorization_policy_evidence",
        "release_authorization_evidence",
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
        "release_authorization_planner_contract",
        "release_authorization_alpha_manager_contract",
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
            GenesisReleaseCandidateApprovalPlanner(
                project_root=self.project_root
            )
        )

        return upstream_planner.contract()

    def _authorization_owner_snapshots(
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
                "sprint": 235,

                "owner": (
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager"
                ),

                "assertion_count": 828,
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

    def _authorization_method_packets(
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
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager.status"
                ),
                (
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager.context"
                ),
                (
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager.plan"
                ),
                (
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager.contract"
                ),
                (
                    "GenesisReleaseCandidateApproval"
                    "AlphaManager.check"
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
            self._authorization_owner_snapshots(
                upstream
            )
        )

        method_packets = (
            self._authorization_method_packets(
                upstream
            )
        )

        required_results = {
            f"{domain}_{suffix}": True
            for domain in self.AUTHORIZATION_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.AUTHORIZATION_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "authorization_decision_applied",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.AUTHORIZATION_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "authorization_decision_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_authorization_write_count": 0,
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
            "authorization_mode": self.MODE,

            "canonical_upstream_owner": (
                "GenesisReleaseCandidateApproval"
                "AlphaManager"
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

            "handoff_chain_count": 15,

            "authorization_domains": list(
                self.AUTHORIZATION_DOMAINS
            ),

            "authorization_domain_count": len(
                self.AUTHORIZATION_DOMAINS
            ),

            "authorization_evidence_inventory": list(
                self.AUTHORIZATION_EVIDENCE_INVENTORY
            ),

            "authorization_evidence_inventory_count": len(
                self.AUTHORIZATION_EVIDENCE_INVENTORY
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

            "required_authorization_results":
                required_results,

            "required_authorization_result_count":
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

            "upstream_release_candidate_approval_foundation_ready":
                upstream[
                    "release_candidate_approval_foundation_ready"
                ],

            "upstream_release_candidate_approval_ready":
                upstream[
                    "release_candidate_approval_ready"
                ],

            "upstream_approval_passed":
                upstream[
                    "approval_passed"
                ],

            "upstream_genesis_release_approved":
                upstream[
                    "genesis_release_approved"
                ],

            "upstream_release_authorization_ready":
                upstream[
                    "release_authorization_ready"
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

            "authorization_evidence_inventory_ready": True,
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

            "external_target_methods_invoked": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,

            "genesis_release_candidate_release_authorization_contract_ready":
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

            "authorization_domain_count":
                contract[
                    "authorization_domain_count"
                ],

            "required_authorization_result_count":
                contract[
                    "required_authorization_result_count"
                ],

            "release_authorization_foundation_ready":
                contract[
                    "release_authorization_foundation_ready"
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

            "authorization_mode":
                contract[
                    "authorization_mode"
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

            "authorization_domains":
                contract[
                    "authorization_domains"
                ],

            "authorization_evidence_inventory":
                contract[
                    "authorization_evidence_inventory"
                ],

            "release_candidate_artifact_inventory":
                contract[
                    "release_candidate_artifact_inventory"
                ],

            "release_candidate_documentation_inventory":
                contract[
                    "release_candidate_documentation_inventory"
                ],

            "required_authorization_results":
                contract[
                    "required_authorization_results"
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
                    "authorization_mode"
                ],

            "authorization_domains":
                contract[
                    "authorization_domains"
                ],

            "required_results":
                contract[
                    "required_authorization_results"
                ],

            "release_candidate_approval_decision_allowed": False,
            "genesis_release_approval_allowed": False,
            "release_authorization_decision_allowed": False,
            "release_gate_review_transition_allowed": False,
            "release_gate_open_allowed": False,

            "runtime_effects_allowed": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisReleaseCandidateApprovalPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_authorization_results"
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

        for domain in self.AUTHORIZATION_DOMAINS:
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
                f"{domain}_negative_authorization_decision_false"
            ] = (
                negative_results[
                    f"{domain}_authorization_decision_applied"
                ]
                is False
            )

        local_assertions[
            "fifteen_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "0.236.0-genesis"

            and contract[
                "current_sprint"
            ] == 236

            and contract[
                "next_sprint"
            ] == 237

            and contract[
                "boundary"
            ] == (
                "genesis_release_candidate_"
                "release_authorization"
            )

            and contract[
                "next_boundary"
            ] == (
                "genesis_release_candidate_"
                "release_gate_review"
            )

            and upstream_check[
                "assertion_count"
            ] == 828

            and upstream_check[
                "failed_assertion_count"
            ] == 0

            and upstream_check[
                "runtime_ready"
            ] is False

            and contract[
                "owner_count"
            ] == 15

            and contract[
                "owner_assertion_total"
            ] == 5536

            and contract[
                "owner_failure_count"
            ] == 0

            and contract[
                "deterministic_method_packet_count"
            ] == 65

            and len(
                set(method_packets)
            ) == 65

            and contract[
                "handoff_chain_count"
            ] == 15
        )

        local_assertions[
            "authorization_inventory_projection_matches"
        ] = (
            contract[
                "authorization_domain_count"
            ] == 17

            and contract[
                "required_authorization_result_count"
            ] == 51

            and all(
                value is True
                for value in required_results.values()
            )

            and contract[
                "authorization_evidence_inventory_count"
            ] == 15

            and contract[
                "release_candidate_artifact_inventory_count"
            ] == 12

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 10
        )

        local_assertions[
            "authorization_hold_state_preserved"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 34

            and all(
                value is False
                for value in negative_results.values()
            )

            and contract[
                "safety_boundary_count"
            ] == 34

            and all(
                value is False
                for value in safety_boundary.values()
            )

            and contract[
                "zero_counter_count"
            ] == 37

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
            "authorization_contract_shape_ready"
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
                "upstream_release_candidate_approval_foundation_ready"
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
                "authorization_evidence_inventory_ready"
            ] is True

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True

            and contract[
                "genesis_release_candidate_release_authorization_contract_ready"
            ] is True
        )

        local_assertions[
            "approval_state_preserved"
        ] = (
            contract[
                "upstream_release_candidate_approval_ready"
            ] is False

            and contract[
                "upstream_approval_passed"
            ] is False

            and contract[
                "upstream_genesis_release_approved"
            ] is False

            and contract[
                "upstream_release_authorization_ready"
            ] is False

            and upstream_check[
                "local_assertion_count"
            ] == 72

            and upstream_check[
                "failed_assertions"
            ] == []
        )

        local_assertions[
            "authorization_decision_separation_preserved"
        ] = (
            contract[
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
        )

        local_assertions[
            "release_gate_review_separation_preserved"
        ] = (
            contract[
                "release_authorization_ready"
            ] is False

            and contract[
                "release_authorization_passed"
            ] is False

            and contract[
                "release_gate_review_ready"
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
                "release_authorization"
            )

            and self.NEXT_BOUNDARY
            == (
                "genesis_release_candidate_"
                "release_gate_review"
            )

            and self.MODE
            == (
                "contract_only_read_only_"
                "release_candidate_release_authorization"
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
            ] == 12

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 10

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True
        )

        local_assertions[
            "authorization_policy_review_ready"
        ] = (
            contract[
                "authorization_domain_count"
            ] == 17

            and contract[
                "authorization_evidence_inventory_count"
            ] == 15

            and contract[
                "release_authorization_foundation_ready"
            ] is True

            and contract[
                "release_authorization_ready"
            ] is False

            and contract[
                "release_authorization_passed"
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
                f"Sprint236:{name}"
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

            "genesis_release_candidate_release_authorization_contract":
                contract,

            "runtime_ready": False,
        }
