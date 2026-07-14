from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_readiness_planner import (
    GenesisReleaseCandidateReadinessPlanner,
)


class GenesisReleaseCandidateApprovalPlanner(
    GenesisReleaseCandidateReadinessPlanner
):
    """Read-only Sprint 235 release-candidate approval contract."""

    VERSION = "1.0.0-genesis"

    CURRENT_SPRINT = 235
    NEXT_SPRINT = 236

    BOUNDARY = "genesis_release_candidate_approval"

    NEXT_BOUNDARY = (
        "genesis_release_candidate_release_authorization"
    )

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "release_candidate_approval"
    )

    APPROVAL_DOMAINS = (
        "canonical_checkpoint_integrity",
        "release_candidate_readiness_foundation_preservation",
        "fourteen_owner_approval_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "readiness_evidence_preservation",
        "approval_evidence_readiness",
        "artifact_inventory_readiness",
        "documentation_inventory_readiness",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "operator_control_and_rollback_readiness",
        "safe_idle_and_emergency_stop_preservation",
        "runtime_effect_hold",
        "approval_decision_separation",
        "release_authorization_separation",
    )

    APPROVAL_EVIDENCE_INVENTORY = (
        "canonical_identity_evidence",
        "checkpoint_parent_evidence",
        "fourteen_owner_evidence",
        "owner_assertion_evidence",
        "deterministic_method_packet_evidence",
        "handoff_chain_evidence",
        "readiness_result_evidence",
        "approval_policy_evidence",
        "approval_evidence",
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
        "release_candidate_approval_planner_contract",
        "release_candidate_approval_alpha_manager_contract",
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
            GenesisReleaseCandidateReadinessPlanner(
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
                "sprint": 234,

                "owner": (
                    "GenesisReleaseCandidateReadiness"
                    "AlphaManager"
                ),

                "assertion_count": 756,
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
                    "GenesisReleaseCandidateReadiness"
                    "AlphaManager.status"
                ),
                (
                    "GenesisReleaseCandidateReadiness"
                    "AlphaManager.context"
                ),
                (
                    "GenesisReleaseCandidateReadiness"
                    "AlphaManager.plan"
                ),
                (
                    "GenesisReleaseCandidateReadiness"
                    "AlphaManager.contract"
                ),
                (
                    "GenesisReleaseCandidateReadiness"
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
            for domain in self.APPROVAL_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.APPROVAL_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "approval_decision_applied",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.APPROVAL_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "approval_decision_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_candidate_approval_write_count": 0,
                "release_authorization_transition_count": 0,
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
            "approval_mode": self.MODE,

            "canonical_upstream_owner": (
                "GenesisReleaseCandidateReadiness"
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

            "handoff_chain_count": 14,

            "approval_domains": list(
                self.APPROVAL_DOMAINS
            ),

            "approval_domain_count": len(
                self.APPROVAL_DOMAINS
            ),

            "approval_evidence_inventory": list(
                self.APPROVAL_EVIDENCE_INVENTORY
            ),

            "approval_evidence_inventory_count": len(
                self.APPROVAL_EVIDENCE_INVENTORY
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

            "required_approval_results":
                required_results,

            "required_approval_result_count":
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

            "upstream_release_candidate_readiness_foundation_ready":
                upstream[
                    "release_candidate_readiness_foundation_ready"
                ],

            "upstream_readiness_passed":
                upstream[
                    "readiness_passed"
                ],

            "upstream_release_candidate_approval_ready":
                upstream[
                    "release_candidate_approval_ready"
                ],

            "current_block_started": True,
            "current_block_complete": False,
            "current_block_stabilized": False,
            "current_block_release_ready": False,

            "release_candidate_assembly_foundation_ready": True,
            "release_candidate_verification_foundation_ready": True,
            "release_candidate_readiness_foundation_ready": True,
            "release_candidate_approval_foundation_ready": True,

            "approval_evidence_inventory_ready": True,
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

            "external_target_methods_invoked": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,

            "genesis_release_candidate_approval_contract_ready":
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

            "approval_domain_count":
                contract[
                    "approval_domain_count"
                ],

            "required_approval_result_count":
                contract[
                    "required_approval_result_count"
                ],

            "release_candidate_approval_foundation_ready":
                contract[
                    "release_candidate_approval_foundation_ready"
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

            "approval_mode":
                contract[
                    "approval_mode"
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

            "approval_domains":
                contract[
                    "approval_domains"
                ],

            "approval_evidence_inventory":
                contract[
                    "approval_evidence_inventory"
                ],

            "release_candidate_artifact_inventory":
                contract[
                    "release_candidate_artifact_inventory"
                ],

            "release_candidate_documentation_inventory":
                contract[
                    "release_candidate_documentation_inventory"
                ],

            "required_approval_results":
                contract[
                    "required_approval_results"
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
                    "approval_mode"
                ],

            "approval_domains":
                contract[
                    "approval_domains"
                ],

            "required_results":
                contract[
                    "required_approval_results"
                ],

            "release_candidate_assembly_allowed": False,
            "release_candidate_verification_allowed": False,
            "release_candidate_readiness_decision_allowed": False,
            "release_candidate_approval_decision_allowed": False,
            "genesis_release_approval_allowed": False,
            "release_authorization_allowed": False,

            "runtime_effects_allowed": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisReleaseCandidateReadinessPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_approval_results"
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

        for domain in self.APPROVAL_DOMAINS:
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
                    f"{domain}_approval_decision_applied"
                ]
                is False
            )

        local_assertions[
            "fourteen_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "1.0.0-genesis"

            and contract[
                "current_sprint"
            ] == 235

            and contract[
                "next_sprint"
            ] == 236

            and contract[
                "boundary"
            ] == (
                "genesis_release_candidate_approval"
            )

            and contract[
                "next_boundary"
            ] == (
                "genesis_release_candidate_"
                "release_authorization"
            )

            and upstream_check[
                "assertion_count"
            ] == 756

            and upstream_check[
                "failed_assertion_count"
            ] == 0

            and upstream_check[
                "runtime_ready"
            ] is False

            and contract[
                "owner_count"
            ] == 14

            and contract[
                "owner_assertion_total"
            ] == 4708

            and contract[
                "owner_failure_count"
            ] == 0

            and contract[
                "deterministic_method_packet_count"
            ] == 60

            and len(
                set(method_packets)
            ) == 60

            and contract[
                "handoff_chain_count"
            ] == 14
        )

        local_assertions[
            "approval_inventory_projection_matches"
        ] = (
            contract[
                "approval_domain_count"
            ] == 16

            and contract[
                "required_approval_result_count"
            ] == 48

            and all(
                value is True
                for value in required_results.values()
            )

            and contract[
                "approval_evidence_inventory_count"
            ] == 14

            and contract[
                "release_candidate_artifact_inventory_count"
            ] == 11

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 9
        )

        local_assertions[
            "approval_hold_state_preserved"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 32

            and all(
                value is False
                for value in negative_results.values()
            )

            and contract[
                "safety_boundary_count"
            ] == 32

            and all(
                value is False
                for value in safety_boundary.values()
            )

            and contract[
                "zero_counter_count"
            ] == 35

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
            "approval_contract_shape_ready"
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
                "upstream_release_candidate_readiness_foundation_ready"
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
                "approval_evidence_inventory_ready"
            ] is True

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True

            and contract[
                "genesis_release_candidate_approval_contract_ready"
            ] is True
        )

        local_assertions[
            "readiness_state_preserved"
        ] = (
            contract[
                "upstream_readiness_passed"
            ] is False

            and contract[
                "upstream_release_candidate_approval_ready"
            ] is False

            and upstream_check[
                "local_assertion_count"
            ] == 66

            and upstream_check[
                "failed_assertions"
            ] == []

            and contract[
                "readiness_passed"
            ] is False

            and contract[
                "release_candidate_approval_ready"
            ] is False
        )

        local_assertions[
            "approval_decision_separation_preserved"
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
                "runtime_activation_allowed"
            ] is False

            and contract[
                "release_gate_open"
            ] is False
        )

        local_assertions[
            "release_authorization_separation_preserved"
        ] = (
            contract[
                "approval_passed"
            ] is False

            and contract[
                "genesis_release_approved"
            ] is False

            and contract[
                "release_authorization_ready"
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
            == "genesis_release_candidate_approval"

            and self.NEXT_BOUNDARY
            == (
                "genesis_release_candidate_"
                "release_authorization"
            )

            and self.MODE
            == (
                "contract_only_read_only_"
                "release_candidate_approval"
            )

            and contract[
                "external_target_methods_invoked"
            ] is False

            and contract[
                "runtime_ready"
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
                f"Sprint235:{name}"
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

            "genesis_release_candidate_approval_contract":
                contract,

            "runtime_ready": False,
        }
