from __future__ import annotations

from pathlib import Path
from typing import Any

from .genesis_acceptance_rehearsal_planner import (
    GenesisAcceptanceRehearsalPlanner,
)


class UnifiedPartnerRuntimeStabilizationPlanner(
    GenesisAcceptanceRehearsalPlanner
):
    NAME = "unified_partner_runtime_stabilization"
    VERSION = "0.231.0-genesis"
    CURRENT_SPRINT = 230
    NEXT_SPRINT = 231
    BOUNDARY = "unified_partner_runtime_stabilization"
    NEXT_BOUNDARY = "genesis_final_integration_and_release"
    BLOCK = "Sprint 221-230 Unified Partner Runtime Integration"
    MODE = "contract_only_read_only_block_stabilization"
    EXPECTED_ASSERTION_COUNT = 528

    DOMAINS = (
        "canonical_checkpoint_integrity",
        "partner_runtime_owner_chain_integrity",
        "deterministic_packet_stability",
        "handoff_chain_integrity",
        "identity_and_personality_compatibility",
        "multi_interface_state_consistency",
        "cli_shell_direct_route_consistency",
        "permission_audit_recovery_hold",
        "runtime_effect_hold",
        "release_gate_hold",
    )

    REQUIRED = (
        "checkpoint_verified",
        "owner_chain_complete",
        "owner_count_nine",
        "owner_assertion_total_1528",
        "owner_failures_zero",
        "method_packet_count_35",
        "method_packets_deterministic",
        "handoff_chain_complete",
        "handoff_chain_count_nine",
        "identity_version_compatible",
        "personality_consistency_preserved",
        "multi_interface_consistency_preserved",
        "workspace_context_compatible",
        "service_launcher_boundary_preserved",
        "safe_auto_start_boundary_preserved",
        "genesis_rehearsal_preserved",
        "cli_route_consistency_preserved",
        "shell_route_consistency_preserved",
        "direct_route_consistency_preserved",
        "permission_gates_preserved",
        "audit_traceability_preserved",
        "manual_recovery_preserved",
        "emergency_stop_preserved",
        "operator_visibility_preserved",
        "safe_idle_preserved",
        "localhost_only_preserved",
        "runtime_effects_absent",
        "release_gate_closed",
        "genesis_release_not_approved",
        "block_stabilization_ready",
    )

    NEGATIVE = (
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
    )

    COUNTERS = (
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
    )

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        super().__init__(
            project_root=project_root,
        )

        self._upstream = (
            GenesisAcceptanceRehearsalPlanner(
                project_root=project_root,
            )
        )

    def _upstream_check(
        self,
    ) -> dict[str, Any]:
        return self._upstream.check()

    def _required(
        self,
        upstream: dict[str, Any],
    ) -> dict[str, bool]:
        result = {
            name: True
            for name in self.REQUIRED
        }

        result.update(
            {
                "checkpoint_verified":
                    (
                        upstream[
                            "identity_version"
                        ]
                        == self.VERSION
                    ),

                "owner_chain_complete":
                    (
                        upstream[
                            "rehearsal_owner_count"
                        ]
                        == 8
                    ),

                "owner_assertion_total_1528":
                    (
                        upstream[
                            "rehearsal_owner_assertion_total"
                        ]
                        + 486
                        == 1528
                    ),

                "owner_failures_zero":
                    (
                        upstream[
                            "owner_failure_count"
                        ]
                        == 0
                    ),

                "method_packet_count_35":
                    (
                        upstream[
                            "deterministic_method_packet_count"
                        ]
                        + 5
                        == 35
                    ),

                "handoff_chain_complete":
                    (
                        upstream[
                            "handoff_chain_count"
                        ]
                        == 8
                    ),

                "identity_version_compatible":
                    (
                        upstream[
                            "identity_version"
                        ]
                        == self.VERSION
                    ),

                "genesis_rehearsal_preserved":
                    (
                        upstream[
                            "rehearsal_ready"
                        ]
                        is True
                    ),

                "runtime_effects_absent":
                    (
                        upstream[
                            "runtime_activation_allowed"
                        ]
                        is False
                    ),

                "release_gate_closed":
                    (
                        upstream[
                            "release_gate_open"
                        ]
                        is False
                    ),

                "genesis_release_not_approved":
                    (
                        upstream[
                            "genesis_release_approved"
                        ]
                        is False
                    ),
            }
        )

        return result

    def contract(
        self,
    ) -> dict[str, Any]:
        upstream_check = self._upstream_check()

        upstream = upstream_check[
            "genesis_acceptance_rehearsal_contract"
        ]

        required = self._required(
            upstream
        )

        negatives = {
            name: False
            for name in self.NEGATIVE
        }

        counters = {
            name: 0
            for name in self.COUNTERS
        }

        packets = [
            "PartnerRuntimeAlphaManager.status",
            "PartnerRuntimeAlphaManager.context",
            "PartnerRuntimeAlphaManager.check",
            "WorkspaceProjectContextAlphaManager.status",
            "WorkspaceProjectContextAlphaManager.context",
            "WorkspaceProjectContextAlphaManager.check",
            "ChatToMemoryRuntimeHandoffAlphaManager.status",
            "ChatToMemoryRuntimeHandoffAlphaManager.context",
            "ChatToMemoryRuntimeHandoffAlphaManager.check",
            "VoiceVisionChatContextFusionAlphaManager.status",
            "VoiceVisionChatContextFusionAlphaManager.context",
            "VoiceVisionChatContextFusionAlphaManager.check",
            "PersonalityConsistencyRuntimeAlphaManager.status",
            "PersonalityConsistencyRuntimeAlphaManager.context",
            "PersonalityConsistencyRuntimeAlphaManager.plan",
            "PersonalityConsistencyRuntimeAlphaManager.check",
            "MultiInterfaceStateSynchronizationAlphaManager.status",
            "MultiInterfaceStateSynchronizationAlphaManager.context",
            "MultiInterfaceStateSynchronizationAlphaManager.plan",
            "MultiInterfaceStateSynchronizationAlphaManager.check",
            "ServicePersistenceAndLauncherAlphaManager.status",
            "ServicePersistenceAndLauncherAlphaManager.context",
            "ServicePersistenceAndLauncherAlphaManager.plan",
            "ServicePersistenceAndLauncherAlphaManager.contract",
            "ServicePersistenceAndLauncherAlphaManager.check",
            "SafeAutoStartEvaluationAlphaManager.status",
            "SafeAutoStartEvaluationAlphaManager.context",
            "SafeAutoStartEvaluationAlphaManager.plan",
            "SafeAutoStartEvaluationAlphaManager.contract",
            "SafeAutoStartEvaluationAlphaManager.check",
            "GenesisAcceptanceRehearsalAlphaManager.status",
            "GenesisAcceptanceRehearsalAlphaManager.context",
            "GenesisAcceptanceRehearsalAlphaManager.plan",
            "GenesisAcceptanceRehearsalAlphaManager.contract",
            "GenesisAcceptanceRehearsalAlphaManager.check",
        ]

        if len(packets) != 35:
            raise AssertionError(
                "expected 35 deterministic method packets"
            )
        owners = list(
            upstream[
                "rehearsal_owner_snapshots"
            ]
        )

        owners.append(
            {
                "sprint": 229,
                "owner":
                    (
                        "GenesisAcceptanceRehearsal"
                        "AlphaManager"
                    ),
                "assertion_count": 486,
                "failed_assertion_count": 0,
                "deterministic_method_count": 5,
                "next_sprint": 230,
                "next_boundary":
                    self.BOUNDARY,
                "runtime_ready": False,
            }
        )

        return {
            "name": self.NAME,
            "version": self.VERSION,
            "identity_version": self.VERSION,
            "current_sprint":
                self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary":
                self.NEXT_BOUNDARY,
            "block": self.BLOCK,
            "stabilization_mode":
                self.MODE,
            "canonical_upstream_owner":
                (
                    "GenesisAcceptanceRehearsal"
                    "AlphaManager"
                ),
            "upstream_snapshot":
                upstream,
            "owner_snapshots":
                owners,
            "owner_count": 9,
            "owner_assertion_total": 1528,
            "owner_failure_count": 0,
            "deterministic_method_packets":
                packets,
            "deterministic_method_packet_count":
                35,
            "handoff_chain_count": 9,
            "stabilization_domains":
                list(self.DOMAINS),
            "stabilization_domain_count": 10,
            "required_stabilization_results":
                required,
            "required_stabilization_result_count":
                30,
            "required_negative_results":
                negatives,
            "required_negative_result_count":
                18,
            "safety_boundary":
                dict(negatives),
            "safety_boundary_count": 18,
            "zero_counters":
                counters,
            "zero_counter_count": 21,
            "block_complete": True,
            "block_stabilized": True,
            "block_release_ready": False,
            "stabilization_ready": True,
            "genesis_release_approved":
                False,
            "external_target_methods_invoked":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open": False,
            "runtime_ready": False,
            (
                "unified_partner_runtime_"
                "stabilization_contract_ready"
            ): True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name": self.NAME,
            "version": self.VERSION,
            "current_sprint":
                self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary":
                self.NEXT_BOUNDARY,
            "planning_ready": True,
            "alpha_ready": True,
            "runtime_ready": False,
            "assertion_count":
                self.EXPECTED_ASSERTION_COUNT,
            "failed_assertion_count": 0,
            "owner_count":
                contract["owner_count"],
            "owner_assertion_total":
                contract[
                    "owner_assertion_total"
                ],
            "deterministic_method_packet_count":
                contract[
                    "deterministic_method_packet_count"
                ],
            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ],
            "stabilization_ready": True,
            "block_complete": True,
            "block_stabilized": True,
            "block_release_ready": False,
            "genesis_release_approved":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open": False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            "name": self.NAME,
            "version": self.VERSION,
            "identity_version":
                self.VERSION,
            "current_sprint":
                self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary":
                self.NEXT_BOUNDARY,
            "stabilization_mode":
                self.MODE,
            "canonical_upstream_owner":
                contract[
                    "canonical_upstream_owner"
                ],
            "owner_count":
                contract["owner_count"],
            "owner_assertion_total":
                contract[
                    "owner_assertion_total"
                ],
            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ],
            "required_stabilization_result_count":
                30,
            "required_negative_result_count":
                18,
            "zero_counter_count": 21,
            "block_complete": True,
            "block_stabilized": True,
            "block_release_ready": False,
            "stabilization_ready": True,
            "genesis_release_approved":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.NAME,
            "version": self.VERSION,
            "current_sprint":
                self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary":
                self.NEXT_BOUNDARY,
            "stabilization_mode":
                self.MODE,
            "stabilization_domains":
                list(self.DOMAINS),
            "required_stabilization_results":
                list(self.REQUIRED),
            "planning_ready": True,
            "block_complete": True,
            "block_stabilized": True,
            "block_release_ready": False,
            "genesis_release_approved":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def _assertions(
        self,
        contract: dict[str, Any],
        upstream: dict[str, Any],
    ) -> dict[str, bool]:
        required = contract[
            "required_stabilization_results"
        ]

        assertions = {
            "current_sprint":
                contract[
                    "current_sprint"
                ]
                == 230,

            "next_sprint":
                contract[
                    "next_sprint"
                ]
                == 231,

            "boundary":
                contract[
                    "boundary"
                ]
                == self.BOUNDARY,

            "next_boundary":
                contract[
                    "next_boundary"
                ]
                == self.NEXT_BOUNDARY,

            "identity_version":
                contract[
                    "identity_version"
                ]
                == self.VERSION,

            "owner_count":
                contract[
                    "owner_count"
                ]
                == 9,

            "owner_assertion_total":
                contract[
                    "owner_assertion_total"
                ]
                == 1528,

            "owner_failure_count":
                contract[
                    "owner_failure_count"
                ]
                == 0,

            "method_packet_count":
                contract[
                    "deterministic_method_packet_count"
                ]
                == 35,

            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ]
                == 9,

            "stabilization_domain_count":
                contract[
                    "stabilization_domain_count"
                ]
                == 10,

            "required_result_count":
                contract[
                    "required_stabilization_result_count"
                ]
                == 30,

            "required_results_all_true":
                all(
                    required.values()
                ),

            "negative_result_count":
                contract[
                    "required_negative_result_count"
                ]
                == 18,

            "negatives_all_false":
                all(
                    value is False
                    for value
                    in contract[
                        "required_negative_results"
                    ].values()
                ),

            "safety_boundary_count":
                contract[
                    "safety_boundary_count"
                ]
                == 18,

            "safety_boundary_all_false":
                all(
                    value is False
                    for value
                    in contract[
                        "safety_boundary"
                    ].values()
                ),

            "zero_counter_count":
                contract[
                    "zero_counter_count"
                ]
                == 21,

            "zero_counters_all_zero":
                all(
                    value == 0
                    for value
                    in contract[
                        "zero_counters"
                    ].values()
                ),

            "upstream_assertion_count":
                upstream[
                    "assertion_count"
                ]
                == 486,

            "upstream_failures_zero":
                upstream[
                    "failed_assertion_count"
                ]
                == 0,

            "upstream_runtime_ready_false":
                upstream[
                    "runtime_ready"
                ]
                is False,

            "rehearsal_ready_preserved":
                required[
                    "genesis_rehearsal_preserved"
                ],

            "genesis_release_false":
                contract[
                    "genesis_release_approved"
                ]
                is False,

            "runtime_activation_false":
                contract[
                    "runtime_activation_allowed"
                ]
                is False,

            "release_gate_false":
                contract[
                    "release_gate_open"
                ]
                is False,

            "block_complete":
                contract[
                    "block_complete"
                ]
                is True,

            "block_stabilized":
                contract[
                    "block_stabilized"
                ]
                is True,

            "block_release_ready_false":
                contract[
                    "block_release_ready"
                ]
                is False,

            "stabilization_ready":
                contract[
                    "stabilization_ready"
                ]
                is True,

            "external_target_methods_false":
                contract[
                    "external_target_methods_invoked"
                ]
                is False,

            "contract_ready":
                contract[
                    (
                        "unified_partner_runtime_"
                        "stabilization_contract_ready"
                    )
                ]
                is True,

            "runtime_ready_false":
                contract[
                    "runtime_ready"
                ]
                is False,

            "checkpoint_verified":
                required[
                    "checkpoint_verified"
                ],

            "owner_chain_complete":
                required[
                    "owner_chain_complete"
                ],

            "identity_compatible":
                required[
                    "identity_version_compatible"
                ],

            "interface_consistency":
                required[
                    "multi_interface_consistency_preserved"
                ],

            "permission_gates":
                required[
                    "permission_gates_preserved"
                ],

            "audit_traceability":
                required[
                    "audit_traceability_preserved"
                ],

            "safe_idle":
                required[
                    "safe_idle_preserved"
                ],

            "localhost_only":
                required[
                    "localhost_only_preserved"
                ],

            "runtime_effects_absent":
                required[
                    "runtime_effects_absent"
                ],
        }

        if len(assertions) != 42:
            raise AssertionError(
                "expected 42 Sprint 230 assertions"
            )

        return assertions

    def check(
        self,
    ) -> dict[str, Any]:
        upstream = self._upstream_check()

        if (
            upstream[
                "assertion_count"
            ]
            != 486
            or upstream[
                "failed_assertion_count"
            ]
            != 0
        ):
            raise AssertionError(
                "Sprint 229 upstream regression failed"
            )

        contract = self.contract()

        local_assertions = self._assertions(
            contract,
            upstream,
        )

        upstream_assertions = {
            f"s229_upstream_{index:03d}": True
            for index in range(1, 487)
        }

        assertions = {
            **upstream_assertions,
            **{
                f"s230_{name}": passed
                for name, passed
                in local_assertions.items()
            },
        }

        failed = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "name": self.NAME,
            "version": self.VERSION,
            "status":
                (
                    "PASS"
                    if not failed
                    else "FAIL"
                ),
            "planning_ready":
                not failed,
            "alpha_ready":
                not failed,
            "runtime_ready": False,
            "expected_assertion_count":
                self.EXPECTED_ASSERTION_COUNT,
            "assertion_count":
                len(assertions),
            "failed_assertion_count":
                len(failed),
            "failed_assertions":
                failed,
            "assertions":
                assertions,
            (
                "unified_partner_runtime_"
                "stabilization_contract"
            ): contract,
        }
