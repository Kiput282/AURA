from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_final_integration_and_release_planner import (
    GenesisFinalIntegrationAndReleasePlanner,
)


class GenesisReleaseCandidateAssemblyPlanner(
    GenesisFinalIntegrationAndReleasePlanner
):
    """Read-only Sprint 232 release-candidate assembly contract."""

    VERSION = "0.235.0-genesis"

    CURRENT_SPRINT = 232
    NEXT_SPRINT = 233

    BOUNDARY = "genesis_release_candidate_assembly"

    NEXT_BOUNDARY = (
        "genesis_release_candidate_verification"
    )

    BLOCK = (
        "Sprint 231-240 Genesis Final "
        "Integration and Release"
    )

    MODE = (
        "contract_only_read_only_"
        "release_candidate_assembly"
    )

    ASSEMBLY_DOMAINS = (
        "canonical_checkpoint_integrity",
        "final_integration_foundation_preservation",
        "eleven_owner_release_candidate_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "release_candidate_manifest_inventory",
        "release_candidate_artifact_inventory",
        "release_candidate_documentation_inventory",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "runtime_effect_hold",
        "release_decision_separation",
        "operator_control_and_rollback_readiness",
    )

    MANIFEST_INVENTORY = (
        "canonical_identity_manifest",
        "checkpoint_parent_manifest",
        "eleven_owner_manifest",
        "owner_assertion_manifest",
        "deterministic_method_packet_manifest",
        "handoff_chain_manifest",
        "permission_boundary_manifest",
        "audit_boundary_manifest",
        "recovery_boundary_manifest",
        "operator_control_manifest",
        "rollback_manifest",
    )

    ARTIFACT_INVENTORY = (
        "release_candidate_assembly_planner_contract",
        "release_candidate_assembly_alpha_manager_contract",
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
            GenesisFinalIntegrationAndReleasePlanner(
                project_root=self.project_root
            )
        )

        return upstream_planner.contract()

    def _assembly_owner_snapshots(
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
                "sprint": 231,
                "owner": (
                    "GenesisFinalIntegrationAndRelease"
                    "AlphaManager"
                ),
                "assertion_count": 576,
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

    def _assembly_method_packets(
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
                    "GenesisFinalIntegrationAndRelease"
                    "AlphaManager.status"
                ),
                (
                    "GenesisFinalIntegrationAndRelease"
                    "AlphaManager.context"
                ),
                (
                    "GenesisFinalIntegrationAndRelease"
                    "AlphaManager.plan"
                ),
                (
                    "GenesisFinalIntegrationAndRelease"
                    "AlphaManager.contract"
                ),
                (
                    "GenesisFinalIntegrationAndRelease"
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
            self._assembly_owner_snapshots(
                upstream
            )
        )

        method_packets = (
            self._assembly_method_packets(
                upstream
            )
        )

        required_results = {
            f"{domain}_{suffix}": True
            for domain in self.ASSEMBLY_DOMAINS
            for suffix in (
                "contract_ready",
                "deterministic",
                "reviewable",
            )
        }

        negative_results = {
            f"{domain}_{suffix}": False
            for domain in self.ASSEMBLY_DOMAINS
            for suffix in (
                "runtime_effect_enabled",
                "release_decision_applied",
            )
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            f"{domain}_{suffix}": 0
            for domain in self.ASSEMBLY_DOMAINS
            for suffix in (
                "runtime_effect_count",
                "release_decision_count",
            )
        }

        zero_counters.update(
            {
                "external_target_method_call_count": 0,
                "release_candidate_artifact_write_count": 0,
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
            "assembly_mode": self.MODE,
            "canonical_upstream_owner": (
                "GenesisFinalIntegrationAndRelease"
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
            "handoff_chain_count": 11,
            "assembly_domains": list(
                self.ASSEMBLY_DOMAINS
            ),
            "assembly_domain_count": len(
                self.ASSEMBLY_DOMAINS
            ),
            "release_candidate_manifest_inventory":
                list(
                    self.MANIFEST_INVENTORY
                ),
            "release_candidate_manifest_inventory_count":
                len(
                    self.MANIFEST_INVENTORY
                ),
            "release_candidate_artifact_inventory":
                list(
                    self.ARTIFACT_INVENTORY
                ),
            "release_candidate_artifact_inventory_count":
                len(
                    self.ARTIFACT_INVENTORY
                ),
            "release_candidate_documentation_inventory":
                list(
                    self.DOCUMENTATION_INVENTORY
                ),
            "release_candidate_documentation_inventory_count":
                len(
                    self.DOCUMENTATION_INVENTORY
                ),
            "required_assembly_results":
                required_results,
            "required_assembly_result_count":
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
            "upstream_block_started": upstream[
                "current_block_started"
            ],
            "upstream_block_complete": upstream[
                "current_block_complete"
            ],
            "upstream_block_stabilized": upstream[
                "current_block_stabilized"
            ],
            "upstream_block_release_ready": upstream[
                "current_block_release_ready"
            ],
            "upstream_final_integration_foundation_ready":
                upstream[
                    "final_integration_foundation_ready"
                ],
            "current_block_started": True,
            "current_block_complete": False,
            "current_block_stabilized": False,
            "current_block_release_ready": False,
            "final_integration_foundation_ready":
                True,
            "release_candidate_assembly_foundation_ready":
                True,
            "release_candidate_manifest_inventory_ready":
                True,
            "release_candidate_artifact_inventory_ready":
                True,
            "release_candidate_documentation_inventory_ready":
                True,
            "release_candidate_assembled": False,
            "release_candidate_ready": False,
            "release_candidate_verified": False,
            "genesis_release_approved": False,
            "external_target_methods_invoked": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
            "genesis_release_candidate_assembly_contract_ready":
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
            "assembly_domain_count":
                contract[
                    "assembly_domain_count"
                ],
            "required_assembly_result_count":
                contract[
                    "required_assembly_result_count"
                ],
            "release_candidate_assembly_foundation_ready":
                contract[
                    "release_candidate_assembly_foundation_ready"
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
            "assembly_mode":
                contract[
                    "assembly_mode"
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
            "assembly_domains":
                contract[
                    "assembly_domains"
                ],
            "release_candidate_manifest_inventory":
                contract[
                    "release_candidate_manifest_inventory"
                ],
            "release_candidate_artifact_inventory":
                contract[
                    "release_candidate_artifact_inventory"
                ],
            "release_candidate_documentation_inventory":
                contract[
                    "release_candidate_documentation_inventory"
                ],
            "required_assembly_results":
                contract[
                    "required_assembly_results"
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
                    "assembly_mode"
                ],
            "assembly_domains":
                contract[
                    "assembly_domains"
                ],
            "required_results":
                contract[
                    "required_assembly_results"
                ],
            "release_candidate_assembly_allowed":
                False,
            "release_candidate_verification_allowed":
                False,
            "release_candidate_approval_allowed":
                False,
            "genesis_release_approval_allowed":
                False,
            "runtime_effects_allowed":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            GenesisFinalIntegrationAndReleasePlanner(
                project_root=self.project_root
            )
        )

        upstream_check = (
            upstream_planner.check()
        )

        contract = self.contract()

        required_results = contract[
            "required_assembly_results"
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

        for domain in self.ASSEMBLY_DOMAINS:
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
                f"{domain}_negative_release_decision_false"
            ] = (
                negative_results[
                    f"{domain}_release_decision_applied"
                ]
                is False
            )

        local_assertions[
            "eleven_owner_projection_matches"
        ] = (
            contract[
                "identity_version"
            ] == "0.235.0-genesis"
            and contract[
                "current_sprint"
            ] == 232
            and contract[
                "next_sprint"
            ] == 233
            and contract[
                "boundary"
            ] == (
                "genesis_release_candidate_assembly"
            )
            and contract[
                "next_boundary"
            ] == (
                "genesis_release_candidate_verification"
            )
            and upstream_check[
                "assertion_count"
            ] == 576
            and upstream_check[
                "failed_assertion_count"
            ] == 0
            and upstream_check[
                "runtime_ready"
            ] is False
            and contract[
                "owner_count"
            ] == 11
            and contract[
                "owner_assertion_total"
            ] == 2632
            and contract[
                "owner_failure_count"
            ] == 0
            and contract[
                "deterministic_method_packet_count"
            ] == 45
            and len(
                set(method_packets)
            ) == 45
            and contract[
                "handoff_chain_count"
            ] == 11
            and contract[
                "assembly_domain_count"
            ] == 13
            and contract[
                "required_assembly_result_count"
            ] == 39
            and all(
                value is True
                for value in required_results.values()
            )
            and contract[
                "release_candidate_manifest_inventory_count"
            ] == 11
            and contract[
                "release_candidate_artifact_inventory_count"
            ] == 8
            and contract[
                "release_candidate_documentation_inventory_count"
            ] == 6
        )

        local_assertions[
            "release_hold_state_preserved"
        ] = (
            contract[
                "required_negative_result_count"
            ] == 26
            and all(
                value is False
                for value in negative_results.values()
            )
            and contract[
                "safety_boundary_count"
            ] == 26
            and all(
                value is False
                for value in safety_boundary.values()
            )
            and contract[
                "zero_counter_count"
            ] == 29
            and all(
                value == 0
                for value in zero_counters.values()
            )
            and contract[
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
                "upstream_final_integration_foundation_ready"
            ] is True
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
                "final_integration_foundation_ready"
            ] is True
            and contract[
                "release_candidate_assembly_foundation_ready"
            ] is True
            and contract[
                "release_candidate_manifest_inventory_ready"
            ] is True
            and contract[
                "release_candidate_artifact_inventory_ready"
            ] is True
            and contract[
                "release_candidate_documentation_inventory_ready"
            ] is True
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
            and contract[
                "genesis_release_candidate_assembly_contract_ready"
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
                f"Sprint232:{name}"
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
            "genesis_release_candidate_assembly_contract":
                contract,
            "runtime_ready": False,
        }
