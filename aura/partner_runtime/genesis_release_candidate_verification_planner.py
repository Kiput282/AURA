from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_release_candidate_assembly_planner import (
    GenesisReleaseCandidateAssemblyPlanner,
)


class GenesisReleaseCandidateVerificationPlanner(
    GenesisReleaseCandidateAssemblyPlanner
):
    """Read-only Sprint 233 release-candidate verification contract."""

    VERSION = "0.237.0-genesis"

    CURRENT_SPRINT = 233
    NEXT_SPRINT = 234

    BOUNDARY = "genesis_release_candidate_verification"

    NEXT_BOUNDARY = (
        "genesis_release_candidate_readiness"
    )

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "release_candidate_verification"
    )

    VERIFICATION_DOMAINS = (
        "canonical_checkpoint_integrity",
        "release_candidate_assembly_foundation_preservation",
        "twelve_owner_verification_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "manifest_verification_inventory",
        "artifact_verification_inventory",
        "documentation_verification_inventory",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "runtime_effect_hold",
        "release_decision_separation",
        "operator_control_and_rollback_readiness",
        "verification_result_separation",
    )

    VERIFICATION_EVIDENCE_INVENTORY = (
        "canonical_identity_evidence",
        "checkpoint_parent_evidence",
        "twelve_owner_evidence",
        "owner_assertion_evidence",
        "deterministic_method_packet_evidence",
        "handoff_chain_evidence",
        "manifest_inventory_evidence",
        "artifact_inventory_evidence",
        "documentation_inventory_evidence",
        "permission_audit_recovery_evidence",
        "operator_control_evidence",
        "rollback_readiness_evidence",
    )

    ARTIFACT_INVENTORY = (
        "release_candidate_assembly_upstream_contract",
        "release_candidate_verification_planner_contract",
        "release_candidate_verification_alpha_manager_contract",
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
            GenesisReleaseCandidateAssemblyPlanner(
                project_root=self.project_root
            )
        )

        return upstream_planner.contract()

    def _verification_owner_snapshots(
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
                "sprint": 232,

                "owner": (
                    "GenesisReleaseCandidateAssembly"
                    "AlphaManager"
                ),

                "assertion_count": 630,
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

    def _verification_method_packets(
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
                    "GenesisReleaseCandidateAssembly"
                    "AlphaManager.status"
                ),
                (
                    "GenesisReleaseCandidateAssembly"
                    "AlphaManager.context"
                ),
                (
                    "GenesisReleaseCandidateAssembly"
                    "AlphaManager.plan"
                ),
                (
                    "GenesisReleaseCandidateAssembly"
                    "AlphaManager.contract"
                ),
                (
                    "GenesisReleaseCandidateAssembly"
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
            self._verification_owner_snapshots(
                upstream
            )
        )

        method_packets = (
            self._verification_method_packets(
                upstream
            )
        )

        required_results = {
            f"{domain}_{suffix}": True
            for domain in self.VERIFICATION_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.VERIFICATION_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "verification_decision_applied",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.VERIFICATION_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "verification_decision_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_candidate_verification_write_count": 0,
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
            "verification_mode": self.MODE,

            "canonical_upstream_owner": (
                "GenesisReleaseCandidateAssembly"
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

            "handoff_chain_count": 12,

            "verification_domains": list(
                self.VERIFICATION_DOMAINS
            ),

            "verification_domain_count": len(
                self.VERIFICATION_DOMAINS
            ),

            "verification_evidence_inventory": list(
                self.VERIFICATION_EVIDENCE_INVENTORY
            ),

            "verification_evidence_inventory_count": len(
                self.VERIFICATION_EVIDENCE_INVENTORY
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

            "required_verification_results":
                required_results,

            "required_verification_result_count":
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

            "upstream_release_candidate_assembly_foundation_ready":
                upstream[
                    "release_candidate_assembly_foundation_ready"
                ],

            "current_block_started": True,
            "current_block_complete": False,
            "current_block_stabilized": False,
            "current_block_release_ready": False,

            "release_candidate_assembly_foundation_ready": True,
            "release_candidate_verification_foundation_ready": True,
            "verification_evidence_inventory_ready": True,
            "release_candidate_artifact_inventory_ready": True,
            "release_candidate_documentation_inventory_ready": True,

            "release_candidate_assembled": False,
            "release_candidate_ready": False,
            "release_candidate_verified": False,
            "verification_passed": False,
            "genesis_release_approved": False,

            "external_target_methods_invoked": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,

            "genesis_release_candidate_verification_contract_ready":
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

            "verification_domain_count":
                contract[
                    "verification_domain_count"
                ],

            "required_verification_result_count":
                contract[
                    "required_verification_result_count"
                ],

            "release_candidate_verification_foundation_ready":
                contract[
                    "release_candidate_verification_foundation_ready"
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

            "genesis_release_approved":
                contract[
                    "genesis_release_approved"
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

            "verification_mode":
                contract[
                    "verification_mode"
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

            "verification_domains":
                contract[
                    "verification_domains"
                ],

            "verification_evidence_inventory":
                contract[
                    "verification_evidence_inventory"
                ],

            "release_candidate_artifact_inventory":
                contract[
                    "release_candidate_artifact_inventory"
                ],

            "release_candidate_documentation_inventory":
                contract[
                    "release_candidate_documentation_inventory"
                ],

            "required_verification_results":
                contract[
                    "required_verification_results"
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
            "genesis_release_approved": False,

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
                    "verification_mode"
                ],

            "verification_domains":
                contract[
                    "verification_domains"
                ],

            "required_results":
                contract[
                    "required_verification_results"
                ],

            "release_candidate_assembly_allowed": False,
            "release_candidate_verification_allowed": False,
            "release_candidate_readiness_allowed": False,
            "release_candidate_approval_allowed": False,
            "genesis_release_approval_allowed": False,

            "runtime_effects_allowed": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisReleaseCandidateAssemblyPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_verification_results"
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

        for domain in self.VERIFICATION_DOMAINS:
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
                f"{domain}_negative_verification_decision_false"
            ] = (
                negative_results[
                    f"{domain}_verification_decision_applied"
                ]
                is False
            )

        local_assertions[
            "twelve_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "0.237.0-genesis"

            and contract[
                "current_sprint"
            ] == 233

            and contract[
                "next_sprint"
            ] == 234

            and contract[
                "boundary"
            ] == (
                "genesis_release_candidate_verification"
            )

            and contract[
                "next_boundary"
            ] == (
                "genesis_release_candidate_readiness"
            )

            and upstream_check[
                "assertion_count"
            ] == 630

            and upstream_check[
                "failed_assertion_count"
            ] == 0

            and upstream_check[
                "runtime_ready"
            ] is False

            and contract[
                "owner_count"
            ] == 12

            and contract[
                "owner_assertion_total"
            ] == 3262

            and contract[
                "owner_failure_count"
            ] == 0

            and contract[
                "deterministic_method_packet_count"
            ] == 50

            and len(
                set(method_packets)
            ) == 50

            and contract[
                "handoff_chain_count"
            ] == 12
        )

        local_assertions[
            "verification_inventory_projection_matches"
        ] = (
            contract[
                "verification_domain_count"
            ] == 14

            and contract[
                "required_verification_result_count"
            ] == 42

            and all(
                value is True
                for value in required_results.values()
            )

            and contract[
                "verification_evidence_inventory_count"
            ] == 12

            and contract[
                "release_candidate_artifact_inventory_count"
            ] == 9

            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 7
        )

        local_assertions[
            "verification_hold_state_preserved"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 28

            and all(
                value is False
                for value in negative_results.values()
            )

            and contract[
                "safety_boundary_count"
            ] == 28

            and all(
                value is False
                for value in safety_boundary.values()
            )

            and contract[
                "zero_counter_count"
            ] == 31

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
                "genesis_release_approved"
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
            "verification_contract_shape_ready"
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
                "upstream_release_candidate_assembly_foundation_ready"
            ] is True

            and contract[
                "release_candidate_assembly_foundation_ready"
            ] is True

            and contract[
                "release_candidate_verification_foundation_ready"
            ] is True

            and contract[
                "verification_evidence_inventory_ready"
            ] is True

            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True

            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True

            and contract[
                "genesis_release_candidate_verification_contract_ready"
            ] is True
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
                f"Sprint233:{name}"
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

            "genesis_release_candidate_verification_contract":
                contract,

            "runtime_ready": False,
        }
