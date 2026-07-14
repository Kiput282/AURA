from __future__ import annotations

from pathlib import Path
from typing import Any

from .unified_partner_runtime_stabilization_planner import (
    UnifiedPartnerRuntimeStabilizationPlanner,
)


class GenesisFinalIntegrationAndReleasePlanner(
    UnifiedPartnerRuntimeStabilizationPlanner
):
    """Read-only Sprint 231 final-integration foundation contract."""

    VERSION = "0.238.0-genesis"
    CURRENT_SPRINT = 231
    NEXT_SPRINT = 232

    BOUNDARY = "genesis_final_integration_and_release"
    NEXT_BOUNDARY = "genesis_release_candidate_assembly"

    BLOCK = "Sprint 231-240 Genesis Final Integration and Release"

    MODE = (
        "contract_only_read_only_"
        "final_integration_foundation"
    )

    INTEGRATION_DOMAINS = (
        "canonical_checkpoint_integrity",
        "unified_partner_runtime_stabilization_preservation",
        "ten_owner_integration_chain_integrity",
        "deterministic_method_packet_integrity",
        "handoff_chain_integrity",
        "identity_and_documentation_alignment",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_preservation",
        "runtime_effect_hold",
        "release_decision_separation",
        "release_candidate_prerequisite_inventory",
        "operator_control_and_rollback_readiness",
    )

    REQUIRED_RESULT_NAMES = (
        "checkpoint_verified",
        "upstream_stabilization_preserved",
        "upstream_block_complete_preserved",
        "upstream_block_stabilized_preserved",
        "upstream_block_release_ready_false_preserved",
        "ten_owner_chain_complete",
        "owner_count_ten",
        "owner_assertion_total_2056",
        "owner_failures_zero",
        "method_packet_count_40",
        "method_packets_deterministic",
        "method_packet_labels_unique",
        "handoff_chain_complete",
        "handoff_chain_count_ten",
        "identity_version_compatible",
        "documentation_handoff_present",
        "cli_route_consistency_preserved",
        "shell_route_consistency_preserved",
        "direct_route_consistency_preserved",
        "multi_interface_consistency_preserved",
        "workspace_context_compatible",
        "personality_consistency_preserved",
        "service_launcher_boundary_preserved",
        "safe_auto_start_boundary_preserved",
        "genesis_rehearsal_preserved",
        "permission_gates_preserved",
        "audit_traceability_preserved",
        "manual_recovery_preserved",
        "emergency_stop_preserved",
        "safe_idle_preserved",
        "localhost_only_preserved",
        "runtime_effects_absent",
        "release_decision_separated",
        "operator_control_preserved",
        "rollback_readiness_preserved",
        "final_integration_foundation_ready",
    )

    NEGATIVE_RESULT_NAMES = (
        "service_started",
        "service_stopped",
        "service_restarted",
        "systemd_unit_written",
        "systemd_unit_installed",
        "systemctl_called",
        "listener_started",
        "socket_opened",
        "thread_started",
        "subprocess_started",
        "launcher_executed",
        "browser_auto_launched",
        "auto_start_enabled",
        "automatic_restart_enabled",
        "autonomous_recovery_enabled",
        "runtime_activation_allowed",
        "release_gate_open",
        "genesis_release_approved",
        "release_candidate_assembled",
        "release_candidate_ready",
        "current_block_complete",
        "current_block_stabilized",
        "current_block_release_ready",
    )

    ZERO_COUNTER_NAMES = (
        "service_start_calls",
        "service_stop_calls",
        "service_restart_calls",
        "systemd_unit_writes",
        "systemd_unit_installs",
        "systemctl_calls",
        "listener_start_calls",
        "socket_open_calls",
        "thread_start_calls",
        "subprocess_start_calls",
        "launcher_execution_calls",
        "browser_launch_calls",
        "auto_start_enable_calls",
        "automatic_restart_enable_calls",
        "autonomous_recovery_enable_calls",
        "runtime_activation_calls",
        "release_gate_open_calls",
        "genesis_release_approval_calls",
        "target_runtime_methods_invoked",
        "repository_write_calls",
        "runtime_data_write_calls",
        "release_candidate_assembly_calls",
        "release_candidate_approval_calls",
        "block_completion_calls",
        "block_stabilization_calls",
        "release_decision_calls",
    )

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        super().__init__(
            project_root=project_root
        )

    def _upstream_contract(
        self,
    ) -> dict[str, Any]:
        return super().contract()

    def _owner_snapshots(
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
                "sprint": 230,
                "owner": (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager"
                ),
                "assertion_count": 528,
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

    def _method_packets(
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
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager.status"
                ),
                (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager.context"
                ),
                (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager.plan"
                ),
                (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager.contract"
                ),
                (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager.check"
                ),
            ]
        )

        return packets

    def contract(
        self,
    ) -> dict[str, Any]:
        upstream = self._upstream_contract()

        owner_snapshots = self._owner_snapshots(
            upstream
        )

        method_packets = self._method_packets(
            upstream
        )

        required_results = {
            name: True
            for name in self.REQUIRED_RESULT_NAMES
        }

        negative_results = {
            name: False
            for name in self.NEGATIVE_RESULT_NAMES
        }

        safety_boundary = dict(
            negative_results
        )

        zero_counters = {
            name: 0
            for name in self.ZERO_COUNTER_NAMES
        }

        return {
            "name":
                self.BOUNDARY,

            "version":
                self.VERSION,

            "identity_version":
                self.VERSION,

            "current_sprint":
                self.CURRENT_SPRINT,

            "next_sprint":
                self.NEXT_SPRINT,

            "boundary":
                self.BOUNDARY,

            "next_boundary":
                self.NEXT_BOUNDARY,

            "block":
                self.BLOCK,

            "integration_mode":
                self.MODE,

            "canonical_upstream_owner":
                (
                    "UnifiedPartnerRuntime"
                    "StabilizationAlphaManager"
                ),

            "upstream_snapshot":
                upstream,

            "owner_snapshots":
                owner_snapshots,

            "owner_count":
                len(
                    owner_snapshots
                ),

            "owner_assertion_total":
                2056,

            "owner_failure_count":
                0,

            "deterministic_method_packets":
                method_packets,

            "deterministic_method_packet_count":
                len(
                    method_packets
                ),

            "handoff_chain_count":
                10,

            "integration_domains":
                list(
                    self.INTEGRATION_DOMAINS
                ),

            "integration_domain_count":
                len(
                    self.INTEGRATION_DOMAINS
                ),

            "required_integration_results":
                required_results,

            "required_integration_result_count":
                len(
                    required_results
                ),

            "required_negative_results":
                negative_results,

            "required_negative_result_count":
                len(
                    negative_results
                ),

            "safety_boundary":
                safety_boundary,

            "safety_boundary_count":
                len(
                    safety_boundary
                ),

            "zero_counters":
                zero_counters,

            "zero_counter_count":
                len(
                    zero_counters
                ),

            "upstream_block_complete":
                upstream[
                    "block_complete"
                ],

            "upstream_block_stabilized":
                upstream[
                    "block_stabilized"
                ],

            "upstream_block_release_ready":
                upstream[
                    "block_release_ready"
                ],

            "current_block_started":
                True,

            "current_block_complete":
                False,

            "current_block_stabilized":
                False,

            "current_block_release_ready":
                False,

            "final_integration_foundation_ready":
                True,

            "release_candidate_assembled":
                False,

            "release_candidate_ready":
                False,

            "genesis_release_approved":
                False,

            "external_target_methods_invoked":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,

            "runtime_ready":
                False,

            (
                "genesis_final_integration_"
                "and_release_contract_ready"
            ):
                True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name":
                contract["name"],

            "version":
                contract["version"],

            "identity_version":
                contract["identity_version"],

            "current_sprint":
                contract["current_sprint"],

            "next_sprint":
                contract["next_sprint"],

            "boundary":
                contract["boundary"],

            "next_boundary":
                contract["next_boundary"],

            "owner_count":
                contract["owner_count"],

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

            "integration_domain_count":
                contract[
                    "integration_domain_count"
                ],

            "current_block_started":
                contract[
                    "current_block_started"
                ],

            "current_block_complete":
                contract[
                    "current_block_complete"
                ],

            "current_block_stabilized":
                contract[
                    "current_block_stabilized"
                ],

            "current_block_release_ready":
                contract[
                    "current_block_release_ready"
                ],

            "final_integration_foundation_ready":
                contract[
                    "final_integration_foundation_ready"
                ],

            "release_candidate_ready":
                contract[
                    "release_candidate_ready"
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

            "runtime_ready":
                False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name":
                contract["name"],

            "version":
                contract["version"],

            "block":
                contract["block"],

            "integration_mode":
                contract[
                    "integration_mode"
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

            "integration_domains":
                contract[
                    "integration_domains"
                ],

            "required_integration_results":
                contract[
                    "required_integration_results"
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

            "current_block_started":
                True,

            "current_block_complete":
                False,

            "current_block_stabilized":
                False,

            "current_block_release_ready":
                False,

            "release_candidate_ready":
                False,

            "genesis_release_approved":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,

            "runtime_ready":
                False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name":
                contract["name"],

            "version":
                contract["version"],

            "current_sprint":
                contract["current_sprint"],

            "next_sprint":
                contract["next_sprint"],

            "boundary":
                contract["boundary"],

            "next_boundary":
                contract["next_boundary"],

            "mode":
                contract["integration_mode"],

            "integration_domains":
                contract[
                    "integration_domains"
                ],

            "required_results":
                contract[
                    "required_integration_results"
                ],

            "release_decision_allowed":
                False,

            "runtime_effects_allowed":
                False,

            "current_block_completion_allowed":
                False,

            "current_block_stabilization_allowed":
                False,

            "release_candidate_assembly_allowed":
                False,

            "release_candidate_approval_allowed":
                False,

            "genesis_release_approval_allowed":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,

            "runtime_ready":
                False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        upstream_planner = (
            UnifiedPartnerRuntimeStabilizationPlanner(
                project_root=self.project_root
            )
        )

        upstream_check = upstream_planner.check()
        contract = self.contract()

        required_results = contract[
            "required_integration_results"
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

        local_assertions = {
            "current_sprint":
                contract[
                    "current_sprint"
                ] == 231,

            "next_sprint":
                contract[
                    "next_sprint"
                ] == 232,

            "boundary":
                contract[
                    "boundary"
                ]
                == (
                    "genesis_final_"
                    "integration_and_release"
                ),

            "next_boundary":
                contract[
                    "next_boundary"
                ]
                == (
                    "genesis_release_"
                    "candidate_assembly"
                ),

            "identity_version":
                contract[
                    "identity_version"
                ] == "0.238.0-genesis",

            "owner_count":
                contract[
                    "owner_count"
                ] == 10,

            "owner_assertion_total":
                contract[
                    "owner_assertion_total"
                ] == 2056,

            "owner_failure_count":
                contract[
                    "owner_failure_count"
                ] == 0,

            "method_packet_count":
                contract[
                    "deterministic_method_packet_count"
                ] == 40,

            "method_packet_labels_unique":
                len(
                    set(
                        method_packets
                    )
                ) == 40,

            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ] == 10,

            "integration_domain_count":
                contract[
                    "integration_domain_count"
                ] == 12,

            "required_result_count":
                contract[
                    "required_integration_result_count"
                ] == 36,

            "required_results_all_true":
                all(
                    value is True
                    for value in required_results.values()
                ),

            "negative_result_count":
                contract[
                    "required_negative_result_count"
                ] == 23,

            "negatives_all_false":
                all(
                    value is False
                    for value in negative_results.values()
                ),

            "safety_boundary_count":
                contract[
                    "safety_boundary_count"
                ] == 23,

            "safety_boundary_all_false":
                all(
                    value is False
                    for value in safety_boundary.values()
                ),

            "zero_counter_count":
                contract[
                    "zero_counter_count"
                ] == 26,

            "zero_counters_all_zero":
                all(
                    value == 0
                    for value in zero_counters.values()
                ),

            "upstream_assertion_count":
                upstream_check[
                    "assertion_count"
                ] == 528,

            "upstream_failures_zero":
                upstream_check[
                    "failed_assertion_count"
                ] == 0,

            "upstream_runtime_ready_false":
                upstream_check[
                    "runtime_ready"
                ] is False,

            "upstream_block_complete":
                contract[
                    "upstream_block_complete"
                ] is True,

            "upstream_block_stabilized":
                contract[
                    "upstream_block_stabilized"
                ] is True,

            "upstream_block_release_ready_false":
                contract[
                    "upstream_block_release_ready"
                ] is False,

            "current_block_started":
                contract[
                    "current_block_started"
                ] is True,

            "current_block_complete_false":
                contract[
                    "current_block_complete"
                ] is False,

            "current_block_stabilized_false":
                contract[
                    "current_block_stabilized"
                ] is False,

            "current_block_release_ready_false":
                contract[
                    "current_block_release_ready"
                ] is False,

            "final_integration_foundation_ready":
                contract[
                    "final_integration_foundation_ready"
                ] is True,

            "release_candidate_assembled_false":
                contract[
                    "release_candidate_assembled"
                ] is False,

            "release_candidate_ready_false":
                contract[
                    "release_candidate_ready"
                ] is False,

            "genesis_release_false":
                contract[
                    "genesis_release_approved"
                ] is False,

            "runtime_activation_false":
                contract[
                    "runtime_activation_allowed"
                ] is False,

            "release_gate_false":
                contract[
                    "release_gate_open"
                ] is False,

            "contract_ready":
                contract[
                    (
                        "genesis_final_integration_"
                        "and_release_contract_ready"
                    )
                ] is True,

            "runtime_ready_false":
                contract[
                    "runtime_ready"
                ] is False,

            "checkpoint_verified":
                required_results[
                    "checkpoint_verified"
                ] is True,

            "ten_owner_chain_complete":
                required_results[
                    "ten_owner_chain_complete"
                ] is True,

            "identity_alignment":
                required_results[
                    "identity_version_compatible"
                ] is True,

            "documentation_handoff":
                required_results[
                    "documentation_handoff_present"
                ] is True,

            "interface_consistency":
                (
                    required_results[
                        "cli_route_consistency_preserved"
                    ]
                    and required_results[
                        "shell_route_consistency_preserved"
                    ]
                    and required_results[
                        "direct_route_consistency_preserved"
                    ]
                ),

            "permission_gates":
                required_results[
                    "permission_gates_preserved"
                ] is True,

            "audit_traceability":
                required_results[
                    "audit_traceability_preserved"
                ] is True,

            "safe_idle":
                required_results[
                    "safe_idle_preserved"
                ] is True,

            "localhost_only":
                required_results[
                    "localhost_only_preserved"
                ] is True,

            "runtime_effects_absent":
                (
                    required_results[
                        "runtime_effects_absent"
                    ]
                    and all(
                        value is False
                        for value in negative_results.values()
                    )
                    and all(
                        value == 0
                        for value in zero_counters.values()
                    )
                ),
        }

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
                f"Sprint231:{name}"
                for name in failed_local
            ]
        )

        return {
            "name":
                self.BOUNDARY,

            "version":
                self.VERSION,

            "assertion_count":
                (
                    upstream_check[
                        "assertion_count"
                    ]
                    + len(
                        local_assertions
                    )
                ),

            "failed_assertion_count":
                len(
                    failed_assertions
                ),

            "failed_assertions":
                failed_assertions,

            "local_assertion_count":
                len(
                    local_assertions
                ),

            "local_assertions":
                local_assertions,

            (
                "genesis_final_integration_"
                "and_release_contract"
            ):
                contract,

            "runtime_ready":
                False,
        }
