"""Sprint 229 Genesis Acceptance Rehearsal contract planner."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterator

from .chat_to_memory_runtime_handoff_alpha_manager import (
    ChatToMemoryRuntimeHandoffAlphaManager,
)
from .multi_interface_state_synchronization_alpha_manager import (
    MultiInterfaceStateSynchronizationAlphaManager,
)
from .partner_runtime_alpha_manager import (
    PartnerRuntimeAlphaManager,
)
from .personality_consistency_runtime_alpha_manager import (
    PersonalityConsistencyRuntimeAlphaManager,
)
from .safe_auto_start_evaluation_alpha_manager import (
    SafeAutoStartEvaluationAlphaManager,
)
from .service_persistence_and_launcher_alpha_manager import (
    ServicePersistenceAndLauncherAlphaManager,
)
from .voice_vision_chat_context_fusion_alpha_manager import (
    VoiceVisionChatContextFusionAlphaManager,
)
from .workspace_project_context_alpha_manager import (
    WorkspaceProjectContextAlphaManager,
)


class GenesisAcceptanceRehearsalPlanner:
    """Build the read-only Sprint 229 Genesis acceptance rehearsal."""

    name = "genesis_acceptance_rehearsal"
    version = "0.1.0-alpha"

    identity_version = "0.230.0-genesis"

    current_sprint = 229
    next_sprint = 230

    boundary = "genesis_acceptance_rehearsal"
    next_boundary = "unified_partner_runtime_stabilization"

    rehearsal_mode = (
        "contract_only_read_only_rehearsal"
    )

    canonical_upstream_owner = (
        "aura.partner_runtime."
        "safe_auto_start_evaluation_alpha_manager."
        "SafeAutoStartEvaluationAlphaManager"
    )

    expected_owner_count = 8
    expected_owner_assertion_total = 1042
    expected_method_packet_count = 30
    expected_handoff_chain_count = 8
    expected_phase_count = 9
    expected_acceptance_result_count = 27
    expected_safety_domain_count = 10
    expected_negative_result_count = 17
    expected_safety_boundary_count = 17
    expected_zero_counter_count = 21
    expected_assertion_count = 486

    _PUBLIC_METHOD_ORDER = (
        "status",
        "context",
        "plan",
        "contract",
        "check",
    )

    _OWNER_SPECS = (
        {
            "label":
                "Sprint 221 Partner Runtime",

            "manager_class":
                PartnerRuntimeAlphaManager,

            "manager_name":
                "PartnerRuntimeAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "partner_runtime_alpha_manager.py"
                ),

            "current_sprint":
                221,

            "next_sprint":
                222,

            "next_boundary":
                "workspace_project_context_runtime",

            "expected_assertion_count":
                51,

            "expected_method_count":
                3,
        },
        {
            "label":
                "Sprint 222 Workspace Project Context",

            "manager_class":
                WorkspaceProjectContextAlphaManager,

            "manager_name":
                "WorkspaceProjectContextAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "workspace_project_context_alpha_manager.py"
                ),

            "current_sprint":
                222,

            "next_sprint":
                223,

            "next_boundary":
                "chat_to_memory_runtime_handoff",

            "expected_assertion_count":
                52,

            "expected_method_count":
                3,
        },
        {
            "label":
                "Sprint 223 Chat-to-Memory Handoff",

            "manager_class":
                ChatToMemoryRuntimeHandoffAlphaManager,

            "manager_name":
                "ChatToMemoryRuntimeHandoffAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "chat_to_memory_runtime_handoff_alpha_manager.py"
                ),

            "current_sprint":
                223,

            "next_sprint":
                224,

            "next_boundary":
                "voice_vision_chat_context_fusion",

            "expected_assertion_count":
                65,

            "expected_method_count":
                3,
        },
        {
            "label":
                "Sprint 224 Voice Vision Chat Fusion",

            "manager_class":
                VoiceVisionChatContextFusionAlphaManager,

            "manager_name":
                "VoiceVisionChatContextFusionAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "voice_vision_chat_context_fusion_alpha_manager.py"
                ),

            "current_sprint":
                224,

            "next_sprint":
                225,

            "next_boundary":
                "personality_consistency_runtime",

            "expected_assertion_count":
                84,

            "expected_method_count":
                3,
        },
        {
            "label":
                "Sprint 225 Personality Consistency",

            "manager_class":
                PersonalityConsistencyRuntimeAlphaManager,

            "manager_name":
                "PersonalityConsistencyRuntimeAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "personality_consistency_runtime_alpha_manager.py"
                ),

            "current_sprint":
                225,

            "next_sprint":
                226,

            "next_boundary":
                "multi_interface_state_synchronization",

            "expected_assertion_count":
                96,

            "expected_method_count":
                4,
        },
        {
            "label":
                "Sprint 226 Multi-Interface Synchronization",

            "manager_class":
                MultiInterfaceStateSynchronizationAlphaManager,

            "manager_name":
                "MultiInterfaceStateSynchronizationAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "multi_interface_state_synchronization_alpha_manager.py"
                ),

            "current_sprint":
                226,

            "next_sprint":
                227,

            "next_boundary":
                "service_persistence_and_launcher",

            "expected_assertion_count":
                128,

            "expected_method_count":
                4,
        },
        {
            "label":
                "Sprint 227 Service Persistence and Launcher",

            "manager_class":
                ServicePersistenceAndLauncherAlphaManager,

            "manager_name":
                "ServicePersistenceAndLauncherAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "service_persistence_and_launcher_alpha_manager.py"
                ),

            "current_sprint":
                227,

            "next_sprint":
                228,

            "next_boundary":
                "safe_auto_start_evaluation",

            "expected_assertion_count":
                208,

            "expected_method_count":
                5,
        },
        {
            "label":
                "Sprint 228 Safe Auto-Start Evaluation",

            "manager_class":
                SafeAutoStartEvaluationAlphaManager,

            "manager_name":
                "SafeAutoStartEvaluationAlphaManager",

            "source":
                (
                    "aura/partner_runtime/"
                    "safe_auto_start_evaluation_alpha_manager.py"
                ),

            "current_sprint":
                228,

            "next_sprint":
                229,

            "next_boundary":
                "genesis_acceptance_rehearsal",

            "expected_assertion_count":
                358,

            "expected_method_count":
                5,
        },
    )

    _REHEARSAL_PHASES = (
        (
            "canonical_checkpoint",
            (
                "Verify the canonical identity, upstream checkpoint, "
                "and bounded rehearsal metadata."
            ),
        ),
        (
            "partner_runtime_chain",
            (
                "Rehearse all deterministic Sprint 221-228 owner "
                "checks and handoff boundaries."
            ),
        ),
        (
            "identity_and_personality",
            (
                "Verify Genesis identity compatibility and personality "
                "consistency remain stable."
            ),
        ),
        (
            "multi_interface_consistency",
            (
                "Verify browser, shell, CLI, and shared-state contracts "
                "remain synchronized."
            ),
        ),
        (
            "service_and_launcher_safety",
            (
                "Verify persistence and launcher surfaces remain "
                "declarative and non-executing."
            ),
        ),
        (
            "safe_auto_start_safety",
            (
                "Verify all ten safe auto-start evaluation domains "
                "remain non-activating."
            ),
        ),
        (
            "permission_audit_recovery",
            (
                "Verify permission, audit, manual recovery, emergency "
                "stop, and operator visibility contracts."
            ),
        ),
        (
            "runtime_effect_hold",
            (
                "Verify no service, listener, socket, thread, "
                "subprocess, launcher, browser, or systemd runtime "
                "effect occurs."
            ),
        ),
        (
            "release_gate_hold",
            (
                "Confirm rehearsal readiness without granting release "
                "approval or runtime activation."
            ),
        ),
    )

    _ACCEPTANCE_RESULT_NAMES = (
        "checkpoint_verified",
        "owner_chain_ready",
        "owner_failures_zero",
        "handoff_chain_complete",
        "identity_compatible",
        "interface_consistency_preserved",
        "permission_gates_preserved",
        "audit_traceability_preserved",
        "manual_recovery_preserved",
        "emergency_stop_preserved",
        "operator_visibility_preserved",
        "safe_idle_preserved",
        "localhost_only_preserved",
        "service_control_absent",
        "systemd_write_absent",
        "systemd_install_absent",
        "systemctl_absent",
        "listener_absent",
        "socket_absent",
        "thread_absent",
        "subprocess_absent",
        "launcher_execution_absent",
        "browser_auto_launch_absent",
        "automatic_restart_absent",
        "autonomous_recovery_absent",
        "runtime_activation_closed",
        "release_gate_closed",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        upstream_manager:
            SafeAutoStartEvaluationAlphaManager | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
            if project_root is not None
            else Path.cwd()
        ).resolve()

        self._upstream_manager = (
            upstream_manager
            if upstream_manager is not None
            else SafeAutoStartEvaluationAlphaManager(
                project_root=self.project_root
            )
        )

        self._owner_snapshot_cache: list[dict[str, Any]] | None = None

        self._contract_cache: dict[str, Any] | None = None

        self._check_cache: dict[str, Any] | None = None

    @staticmethod
    def _walk_dicts(
        value: Any,
    ) -> Iterator[dict[str, Any]]:
        if isinstance(
            value,
            dict,
        ):
            yield value

            for child in value.values():
                yield from (
                    GenesisAcceptanceRehearsalPlanner
                    ._walk_dicts(child)
                )

        elif isinstance(
            value,
            (
                list,
                tuple,
            ),
        ):
            for child in value:
                yield from (
                    GenesisAcceptanceRehearsalPlanner
                    ._walk_dicts(child)
                )

    @staticmethod
    def _normalize_sprint(
        value: Any,
    ) -> int | None:
        if isinstance(
            value,
            bool,
        ):
            return None

        if isinstance(
            value,
            int,
        ):
            return value

        if (
            isinstance(
                value,
                str,
            )
            and value.isdigit()
        ):
            return int(value)

        return None

    @classmethod
    def _handoff_present(
        cls,
        packet: dict[str, Any],
        *,
        current_sprint: int,
        next_sprint: int,
        next_boundary: str,
    ) -> bool:
        for candidate in cls._walk_dicts(
            packet
        ):
            candidate_current = (
                cls._normalize_sprint(
                    candidate.get(
                        "current_sprint"
                    )
                )
            )

            if candidate_current is None:
                candidate_current = (
                    cls._normalize_sprint(
                        candidate.get(
                            "partner_runtime_current_sprint"
                        )
                    )
                )

            candidate_next = (
                cls._normalize_sprint(
                    candidate.get(
                        "next_sprint"
                    )
                )
            )

            if candidate_next is None:
                candidate_next = (
                    cls._normalize_sprint(
                        candidate.get(
                            "partner_runtime_next_sprint"
                        )
                    )
                )

            candidate_boundary = (
                candidate.get(
                    "next_boundary"
                )
            )

            if candidate_boundary is None:
                candidate_boundary = (
                    candidate.get(
                        "partner_runtime_next_boundary"
                    )
                )

            if (
                candidate_current
                == current_sprint
                and candidate_next
                == next_sprint
                and candidate_boundary
                == next_boundary
            ):
                return True

        return False

    @staticmethod
    def _packet_summary(
        value: Any,
    ) -> dict[str, Any]:
        if isinstance(
            value,
            dict,
        ):
            return {
                "packet_type":
                    "dict",

                "key_count":
                    len(value),

                "keys":
                    sorted(
                        str(key)
                        for key in value
                    ),
            }

        if isinstance(
            value,
            list,
        ):
            return {
                "packet_type":
                    "list",

                "item_count":
                    len(value),
            }

        return {
            "packet_type":
                type(value).__name__,

            "representation":
                repr(value)[:200],
        }

    def _manager_for_spec(
        self,
        spec: dict[str, Any],
    ) -> Any:
        manager_class = spec[
            "manager_class"
        ]

        if (
            manager_class
            is SafeAutoStartEvaluationAlphaManager
        ):
            return self._upstream_manager

        return manager_class(
            project_root=self.project_root
        )

    def rehearsal_owner_snapshots(
        self,
    ) -> list[dict[str, Any]]:
        if (
            self._owner_snapshot_cache
            is not None
        ):
            return deepcopy(
                self._owner_snapshot_cache
            )

        snapshots = []

        for sequence, spec in enumerate(
            self._OWNER_SPECS,
            start=1,
        ):
            manager = (
                self._manager_for_spec(
                    spec
                )
            )

            method_packets = []

            for method_name in (
                self._PUBLIC_METHOD_ORDER
            ):
                method = getattr(
                    manager,
                    method_name,
                    None,
                )

                if not callable(method):
                    continue

                first = method()
                second = method()

                method_packets.append(
                    {
                        "method":
                            method_name,

                        "deterministic":
                            first == second,

                        "packet_summary":
                            self._packet_summary(
                                first
                            ),
                    }
                )

            check_packet = (
                manager.check()
            )

            assertion_count = (
                check_packet.get(
                    "assertion_count"
                )
            )

            failed_assertion_count = (
                check_packet.get(
                    "failed_assertion_count"
                )
            )

            failed_assertions = list(
                check_packet.get(
                    "failed_assertions",
                    [],
                )
            )

            planning_ready = bool(
                check_packet.get(
                    "planning_ready",
                    False,
                )
            )

            alpha_ready_value = (
                check_packet.get(
                    "alpha_ready"
                )
            )

            if alpha_ready_value is None:
                alpha_ready = (
                    planning_ready
                )
            else:
                alpha_ready = bool(
                    alpha_ready_value
                )

            runtime_ready = bool(
                check_packet.get(
                    "runtime_ready",
                    False,
                )
            )

            handoff_metadata_present = (
                self._handoff_present(
                    check_packet,
                    current_sprint=(
                        spec[
                            "current_sprint"
                        ]
                    ),
                    next_sprint=(
                        spec[
                            "next_sprint"
                        ]
                    ),
                    next_boundary=(
                        spec[
                            "next_boundary"
                        ]
                    ),
                )
            )

            snapshots.append(
                {
                    "sequence":
                        sequence,

                    "label":
                        spec["label"],

                    "manager":
                        spec["manager_name"],

                    "source":
                        spec["source"],

                    "current_sprint":
                        spec[
                            "current_sprint"
                        ],

                    "next_sprint":
                        spec[
                            "next_sprint"
                        ],

                    "next_boundary":
                        spec[
                            "next_boundary"
                        ],

                    "expected_assertion_count":
                        spec[
                            "expected_assertion_count"
                        ],

                    "assertion_count":
                        assertion_count,

                    "expected_method_count":
                        spec[
                            "expected_method_count"
                        ],

                    "method_packet_count":
                        len(
                            method_packets
                        ),

                    "method_packets":
                        method_packets,

                    "failed_assertion_count":
                        failed_assertion_count,

                    "failed_assertions":
                        failed_assertions,

                    "planning_ready":
                        planning_ready,

                    "alpha_ready":
                        alpha_ready,

                    "runtime_ready":
                        runtime_ready,

                    "handoff_metadata_present":
                        handoff_metadata_present,
                }
            )

        self._owner_snapshot_cache = (
            deepcopy(
                snapshots
            )
        )

        return deepcopy(
            snapshots
        )

    def rehearsal_phases(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "sequence":
                    sequence,

                "phase":
                    phase,

                "purpose":
                    purpose,

                "execution_mode":
                    (
                        "read_only_deterministic_"
                        "contract_rehearsal"
                    ),

                "runtime_effects_allowed":
                    False,
            }
            for sequence, (
                phase,
                purpose,
            ) in enumerate(
                self._REHEARSAL_PHASES,
                start=1,
            )
        ]

    def _upstream_packets(
        self,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
    ]:
        check_packet = (
            self._upstream_manager
            .check()
        )

        contract_packet = (
            self._upstream_manager
            .contract()
        )

        return (
            check_packet,
            contract_packet,
        )

    def _acceptance_results(
        self,
        *,
        owner_snapshots:
            list[dict[str, Any]],
        upstream_check:
            dict[str, Any],
        upstream_contract:
            dict[str, Any],
    ) -> dict[str, bool]:
        domains = {
            packet["domain"]:
                packet
            for packet in (
                upstream_contract[
                    "evaluation_domains"
                ]
            )
        }

        negative = (
            upstream_contract[
                "required_negative_results"
            ]
        )

        owner_by_sprint = {
            packet[
                "current_sprint"
            ]:
                packet
            for packet in owner_snapshots
        }

        owner_chain_ready = all(
            packet[
                "planning_ready"
            ]
            and packet[
                "alpha_ready"
            ]
            and not packet[
                "runtime_ready"
            ]
            for packet in owner_snapshots
        )

        owner_failures_zero = all(
            packet[
                "failed_assertion_count"
            ]
            == 0
            and packet[
                "failed_assertions"
            ]
            == []
            for packet in owner_snapshots
        )

        handoff_complete = all(
            packet[
                "handoff_metadata_present"
            ]
            for packet in owner_snapshots
        )

        deterministic = all(
            method_packet[
                "deterministic"
            ]
            for owner in owner_snapshots
            for method_packet in owner[
                "method_packets"
            ]
        )

        def domain_ready(
            name: str,
        ) -> bool:
            packet = domains.get(
                name,
                {}
            )

            return (
                packet.get(
                    "activation_permitted"
                )
                is False
                and packet.get(
                    "evaluation_mode"
                )
                == (
                    "read_only_contract_"
                    "precondition_review"
                )
            )

        service_control_absent = all(
            negative.get(
                key
            )
            is False
            for key in (
                "service_started",
                "service_stopped",
                "service_restarted",
            )
        )

        return {
            "checkpoint_verified":
                (
                    upstream_check[
                        "assertion_count"
                    ]
                    == 358
                    and upstream_check[
                        "failed_assertion_count"
                    ]
                    == 0
                ),

            "owner_chain_ready":
                owner_chain_ready,

            "owner_failures_zero":
                owner_failures_zero,

            "handoff_chain_complete":
                handoff_complete,

            "identity_compatible":
                (
                    upstream_contract[
                        "identity_version"
                    ]
                    == self.identity_version
                ),

            "interface_consistency_preserved":
                (
                    owner_by_sprint[
                        226
                    ][
                        "planning_ready"
                    ]
                    and owner_by_sprint[
                        226
                    ][
                        "alpha_ready"
                    ]
                    and deterministic
                ),

            "permission_gates_preserved":
                domain_ready(
                    "permission_confirmation_precondition"
                ),

            "audit_traceability_preserved":
                domain_ready(
                    "audit_traceability_precondition"
                ),

            "manual_recovery_preserved":
                domain_ready(
                    "manual_recovery_precondition"
                ),

            "emergency_stop_preserved":
                domain_ready(
                    "emergency_stop_precondition"
                ),

            "operator_visibility_preserved":
                domain_ready(
                    "operator_visibility_precondition"
                ),

            "safe_idle_preserved":
                domain_ready(
                    "safe_idle_boot_precondition"
                ),

            "localhost_only_preserved":
                domain_ready(
                    "localhost_only_binding_precondition"
                ),

            "service_control_absent":
                service_control_absent,

            "systemd_write_absent":
                negative[
                    "systemd_unit_written"
                ]
                is False,

            "systemd_install_absent":
                negative[
                    "systemd_unit_installed"
                ]
                is False,

            "systemctl_absent":
                negative[
                    "systemctl_called"
                ]
                is False,

            "listener_absent":
                negative[
                    "listener_started"
                ]
                is False,

            "socket_absent":
                negative[
                    "socket_opened"
                ]
                is False,

            "thread_absent":
                negative[
                    "thread_started"
                ]
                is False,

            "subprocess_absent":
                negative[
                    "subprocess_started"
                ]
                is False,

            "launcher_execution_absent":
                negative[
                    "launcher_executed"
                ]
                is False,

            "browser_auto_launch_absent":
                negative[
                    "browser_auto_launched"
                ]
                is False,

            "automatic_restart_absent":
                negative[
                    "automatic_restart_enabled"
                ]
                is False,

            "autonomous_recovery_absent":
                negative[
                    "autonomous_recovery_enabled"
                ]
                is False,

            "runtime_activation_closed":
                negative[
                    "runtime_activation_allowed"
                ]
                is False,

            "release_gate_closed":
                negative[
                    "release_gate_open"
                ]
                is False,
        }

    def safety_boundary(
        self,
    ) -> dict[str, bool]:
        if self._contract_cache is not None:
            return deepcopy(
                self._contract_cache[
                    "safety_boundary"
                ]
            )

        _, upstream_contract = (
            self._upstream_packets()
        )

        return dict(
            upstream_contract[
                "safety_boundary"
            ]
        )

    def zero_counters(
        self,
    ) -> dict[str, int]:
        if self._contract_cache is not None:
            return deepcopy(
                self._contract_cache[
                    "zero_counters"
                ]
            )

        _, upstream_contract = (
            self._upstream_packets()
        )

        return dict(
            upstream_contract[
                "zero_counters"
            ]
        )

    def genesis_acceptance_rehearsal_contract(
        self,
    ) -> dict[str, Any]:
        if self._contract_cache is not None:
            return deepcopy(
                self._contract_cache
            )

        owner_snapshots = (
            self.rehearsal_owner_snapshots()
        )

        upstream_check, upstream_contract = (
            self._upstream_packets()
        )

        phases = (
            self.rehearsal_phases()
        )

        acceptance_results = (
            self._acceptance_results(
                owner_snapshots=(
                    owner_snapshots
                ),
                upstream_check=(
                    upstream_check
                ),
                upstream_contract=(
                    upstream_contract
                ),
            )
        )

        owner_assertion_total = sum(
            packet[
                "assertion_count"
            ]
            for packet in owner_snapshots
        )

        method_packet_count = sum(
            packet[
                "method_packet_count"
            ]
            for packet in owner_snapshots
        )

        handoff_chain_count = sum(
            packet[
                "handoff_metadata_present"
            ]
            is True
            for packet in owner_snapshots
        )

        owner_failure_count = sum(
            packet[
                "failed_assertion_count"
            ]
            for packet in owner_snapshots
        )

        deterministic_method_packets = all(
            method_packet[
                "deterministic"
            ]
            for owner in owner_snapshots
            for method_packet in owner[
                "method_packets"
            ]
        )

        rehearsal_ready = (
            all(
                acceptance_results.values()
            )
            and owner_assertion_total
            == self.expected_owner_assertion_total
            and method_packet_count
            == self.expected_method_packet_count
            and handoff_chain_count
            == self.expected_handoff_chain_count
            and owner_failure_count
            == 0
            and deterministic_method_packets
        )

        contract = {
            "name":
                self.name,

            "version":
                self.version,

            "identity_version":
                self.identity_version,

            "block":
                (
                    "Sprint 221-230 Unified "
                    "Partner Runtime Integration"
                ),

            "current_sprint":
                self.current_sprint,

            "boundary":
                self.boundary,

            "next_sprint":
                self.next_sprint,

            "next_boundary":
                self.next_boundary,

            "rehearsal_mode":
                self.rehearsal_mode,

            "canonical_upstream_owner":
                self.canonical_upstream_owner,

            "upstream_snapshot": {
                "assertion_count":
                    upstream_check[
                        "assertion_count"
                    ],

                "expected_assertion_count":
                    upstream_check[
                        "expected_assertion_count"
                    ],

                "failed_assertion_count":
                    upstream_check[
                        "failed_assertion_count"
                    ],

                "failed_assertions":
                    list(
                        upstream_check[
                            "failed_assertions"
                        ]
                    ),

                "planning_ready":
                    upstream_check[
                        "planning_ready"
                    ],

                "alpha_ready":
                    upstream_check[
                        "alpha_ready"
                    ],

                "runtime_ready":
                    upstream_check[
                        "runtime_ready"
                    ],

                "current_sprint":
                    upstream_contract[
                        "current_sprint"
                    ],

                "next_sprint":
                    upstream_contract[
                        "next_sprint"
                    ],

                "next_boundary":
                    upstream_contract[
                        "next_boundary"
                    ],
            },

            "rehearsal_owner_count":
                len(
                    owner_snapshots
                ),

            "expected_rehearsal_owner_count":
                self.expected_owner_count,

            "rehearsal_owner_assertion_total":
                owner_assertion_total,

            "expected_rehearsal_owner_assertion_total":
                self.expected_owner_assertion_total,

            "deterministic_method_packet_count":
                method_packet_count,

            "expected_deterministic_method_packet_count":
                self.expected_method_packet_count,

            "handoff_chain_count":
                handoff_chain_count,

            "expected_handoff_chain_count":
                self.expected_handoff_chain_count,

            "owner_failure_count":
                owner_failure_count,

            "deterministic_method_packets":
                deterministic_method_packets,

            "rehearsal_owner_snapshots":
                owner_snapshots,

            "rehearsal_phase_count":
                len(
                    phases
                ),

            "expected_rehearsal_phase_count":
                self.expected_phase_count,

            "rehearsal_phases":
                phases,

            "required_acceptance_result_count":
                len(
                    acceptance_results
                ),

            "expected_required_acceptance_result_count":
                self.expected_acceptance_result_count,

            "required_acceptance_results":
                acceptance_results,

            "safe_auto_start_domain_count":
                len(
                    upstream_contract[
                        "evaluation_domains"
                    ]
                ),

            "evaluation_domains":
                deepcopy(
                    upstream_contract[
                        "evaluation_domains"
                    ]
                ),

            "required_negative_result_count":
                len(
                    upstream_contract[
                        "required_negative_results"
                    ]
                ),

            "required_negative_results":
                dict(
                    upstream_contract[
                        "required_negative_results"
                    ]
                ),

            "safety_boundary_count":
                len(
                    upstream_contract[
                        "safety_boundary"
                    ]
                ),

            "safety_boundary":
                dict(
                    upstream_contract[
                        "safety_boundary"
                    ]
                ),

            "zero_counter_count":
                len(
                    upstream_contract[
                        "zero_counters"
                    ]
                ),

            "zero_counters":
                dict(
                    upstream_contract[
                        "zero_counters"
                    ]
                ),

            "genesis_acceptance_rehearsal_contract_ready":
                rehearsal_ready,

            "rehearsal_ready":
                rehearsal_ready,

            "genesis_release_approved":
                False,

            "runtime_ready":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,

            "external_target_methods_invoked":
                False,

            "auto_start_enabled":
                False,

            "service_started":
                False,

            "listener_started":
                False,

            "socket_opened":
                False,

            "thread_started":
                False,

            "subprocess_started":
                False,

            "launcher_executed":
                False,

            "browser_auto_launched":
                False,
        }

        self._contract_cache = deepcopy(
            contract
        )

        return deepcopy(
            contract
        )

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .genesis_acceptance_rehearsal_contract()
        )

        return {
            "name":
                self.name,

            "version":
                self.version,

            "current_sprint":
                self.current_sprint,

            "boundary":
                self.boundary,

            "next_sprint":
                self.next_sprint,

            "next_boundary":
                self.next_boundary,

            "rehearsal_mode":
                self.rehearsal_mode,

            "rehearsal_phases":
                deepcopy(
                    contract[
                        "rehearsal_phases"
                    ]
                ),

            "required_acceptance_results":
                list(
                    contract[
                        "required_acceptance_results"
                    ].keys()
                ),

            "planning_ready":
                contract[
                    "rehearsal_ready"
                ],

            "runtime_ready":
                False,

            "genesis_release_approved":
                False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .genesis_acceptance_rehearsal_contract()
        )

        return {
            "name":
                self.name,

            "version":
                self.version,

            "current_sprint":
                self.current_sprint,

            "boundary":
                self.boundary,

            "next_sprint":
                self.next_sprint,

            "next_boundary":
                self.next_boundary,

            "rehearsal_owner_count":
                contract[
                    "rehearsal_owner_count"
                ],

            "rehearsal_owner_assertion_total":
                contract[
                    "rehearsal_owner_assertion_total"
                ],

            "deterministic_method_packet_count":
                contract[
                    "deterministic_method_packet_count"
                ],

            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ],

            "rehearsal_phase_count":
                contract[
                    "rehearsal_phase_count"
                ],

            "required_acceptance_result_count":
                contract[
                    "required_acceptance_result_count"
                ],

            "rehearsal_ready":
                contract[
                    "rehearsal_ready"
                ],

            "planning_ready":
                contract[
                    "rehearsal_ready"
                ],

            "alpha_ready":
                contract[
                    "rehearsal_ready"
                ],

            "runtime_ready":
                False,

            "genesis_release_approved":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .genesis_acceptance_rehearsal_contract()
        )

        return {
            "name":
                self.name,

            "identity_version":
                self.identity_version,

            "current_sprint":
                self.current_sprint,

            "next_sprint":
                self.next_sprint,

            "boundary":
                self.boundary,

            "next_boundary":
                self.next_boundary,

            "rehearsal_mode":
                self.rehearsal_mode,

            "canonical_upstream_owner":
                self.canonical_upstream_owner,

            "rehearsal_owner_count":
                contract[
                    "rehearsal_owner_count"
                ],

            "handoff_chain_count":
                contract[
                    "handoff_chain_count"
                ],

            "safe_auto_start_domain_count":
                contract[
                    "safe_auto_start_domain_count"
                ],

            "required_negative_result_count":
                contract[
                    "required_negative_result_count"
                ],

            "zero_counter_count":
                contract[
                    "zero_counter_count"
                ],

            "rehearsal_ready":
                contract[
                    "rehearsal_ready"
                ],

            "runtime_ready":
                False,

            "genesis_release_approved":
                False,

            "runtime_activation_allowed":
                False,

            "release_gate_open":
                False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        if self._check_cache is not None:
            return deepcopy(
                self._check_cache
            )

        contract = (
            self
            .genesis_acceptance_rehearsal_contract()
        )

        assertions: dict[str, bool] = {}

        def add(
            name: str,
            value: Any,
        ) -> None:
            if name in assertions:
                raise RuntimeError(
                    "duplicate Sprint 229 assertion: "
                    + name
                )

            assertions[name] = bool(
                value
            )

        global_checks = (
            (
                "metadata name",
                contract["name"]
                == self.name,
            ),
            (
                "metadata version",
                contract["version"]
                == self.version,
            ),
            (
                "identity version",
                contract["identity_version"]
                == self.identity_version,
            ),
            (
                "current sprint",
                contract["current_sprint"]
                == 229,
            ),
            (
                "next sprint",
                contract["next_sprint"]
                == 230,
            ),
            (
                "current boundary",
                contract["boundary"]
                == self.boundary,
            ),
            (
                "next boundary",
                contract["next_boundary"]
                == self.next_boundary,
            ),
            (
                "rehearsal mode",
                contract["rehearsal_mode"]
                == self.rehearsal_mode,
            ),
            (
                "owner count",
                contract["rehearsal_owner_count"]
                == 8,
            ),
            (
                "expected owner count",
                contract[
                    "expected_rehearsal_owner_count"
                ]
                == 8,
            ),
            (
                "owner assertion total",
                contract[
                    "rehearsal_owner_assertion_total"
                ]
                == 1042,
            ),
            (
                "expected owner assertion total",
                contract[
                    "expected_rehearsal_owner_assertion_total"
                ]
                == 1042,
            ),
            (
                "method packet count",
                contract[
                    "deterministic_method_packet_count"
                ]
                == 30,
            ),
            (
                "expected method packet count",
                contract[
                    "expected_deterministic_method_packet_count"
                ]
                == 30,
            ),
            (
                "handoff chain count",
                contract["handoff_chain_count"]
                == 8,
            ),
            (
                "expected handoff chain count",
                contract[
                    "expected_handoff_chain_count"
                ]
                == 8,
            ),
            (
                "phase count",
                contract["rehearsal_phase_count"]
                == 9,
            ),
            (
                "expected phase count",
                contract[
                    "expected_rehearsal_phase_count"
                ]
                == 9,
            ),
            (
                "acceptance result count",
                contract[
                    "required_acceptance_result_count"
                ]
                == 27,
            ),
            (
                "expected acceptance result count",
                contract[
                    "expected_required_acceptance_result_count"
                ]
                == 27,
            ),
            (
                "safe auto-start domain count",
                contract[
                    "safe_auto_start_domain_count"
                ]
                == 10,
            ),
            (
                "negative result count",
                contract[
                    "required_negative_result_count"
                ]
                == 17,
            ),
            (
                "safety boundary count",
                contract[
                    "safety_boundary_count"
                ]
                == 17,
            ),
            (
                "zero counter count",
                contract[
                    "zero_counter_count"
                ]
                == 21,
            ),
            (
                "contract ready",
                contract[
                    "genesis_acceptance_rehearsal_contract_ready"
                ]
                is True,
            ),
            (
                "rehearsal ready",
                contract[
                    "rehearsal_ready"
                ]
                is True,
            ),
            (
                "Genesis release not approved",
                contract[
                    "genesis_release_approved"
                ]
                is False,
            ),
            (
                "runtime not ready",
                contract[
                    "runtime_ready"
                ]
                is False,
            ),
            (
                "runtime activation closed",
                contract[
                    "runtime_activation_allowed"
                ]
                is False,
            ),
            (
                "release gate closed",
                contract[
                    "release_gate_open"
                ]
                is False,
            ),
            (
                "auto-start disabled",
                contract[
                    "auto_start_enabled"
                ]
                is False,
            ),
            (
                "service not started",
                contract[
                    "service_started"
                ]
                is False,
            ),
            (
                "listener not started",
                contract[
                    "listener_started"
                ]
                is False,
            ),
            (
                "socket not opened",
                contract[
                    "socket_opened"
                ]
                is False,
            ),
            (
                "thread not started",
                contract[
                    "thread_started"
                ]
                is False,
            ),
            (
                "subprocess not started",
                contract[
                    "subprocess_started"
                ]
                is False,
            ),
            (
                "launcher not executed",
                contract[
                    "launcher_executed"
                ]
                is False,
            ),
            (
                "browser not auto-launched",
                contract[
                    "browser_auto_launched"
                ]
                is False,
            ),
            (
                "owner failures zero",
                contract[
                    "owner_failure_count"
                ]
                == 0,
            ),
            (
                "method packets deterministic",
                contract[
                    "deterministic_method_packets"
                ]
                is True,
            ),
        )

        if len(global_checks) != 40:
            raise RuntimeError(
                "Sprint 229 global assertion "
                "schema must contain 40 entries"
            )

        for name, value in global_checks:
            add(
                name,
                value,
            )

        upstream = contract[
            "upstream_snapshot"
        ]

        upstream_checks = (
            (
                "upstream assertion count",
                upstream[
                    "assertion_count"
                ]
                == 358,
            ),
            (
                "upstream expected assertion count",
                upstream[
                    "expected_assertion_count"
                ]
                == 358,
            ),
            (
                "upstream failures zero",
                upstream[
                    "failed_assertion_count"
                ]
                == 0,
            ),
            (
                "upstream failed assertions empty",
                upstream[
                    "failed_assertions"
                ]
                == [],
            ),
            (
                "upstream planning ready",
                upstream[
                    "planning_ready"
                ]
                is True,
            ),
            (
                "upstream alpha ready",
                upstream[
                    "alpha_ready"
                ]
                is True,
            ),
            (
                "upstream runtime closed",
                upstream[
                    "runtime_ready"
                ]
                is False,
            ),
            (
                "upstream current sprint",
                upstream[
                    "current_sprint"
                ]
                == 228,
            ),
            (
                "upstream next sprint",
                upstream[
                    "next_sprint"
                ]
                == 229,
            ),
            (
                "upstream next boundary",
                upstream[
                    "next_boundary"
                ]
                == self.boundary,
            ),
        )

        for name, value in upstream_checks:
            add(
                name,
                value,
            )

        for owner in contract[
            "rehearsal_owner_snapshots"
        ]:
            prefix = (
                f"owner {owner['sequence']:02d} "
                f"{owner['manager']}"
            )

            owner_checks = (
                (
                    "label",
                    bool(
                        owner[
                            "label"
                        ]
                    ),
                ),
                (
                    "manager",
                    bool(
                        owner[
                            "manager"
                        ]
                    ),
                ),
                (
                    "current sprint",
                    owner[
                        "current_sprint"
                    ]
                    == (
                        owner[
                            "sequence"
                        ]
                        + 220
                    ),
                ),
                (
                    "next sprint",
                    owner[
                        "next_sprint"
                    ]
                    == (
                        owner[
                            "current_sprint"
                        ]
                        + 1
                    ),
                ),
                (
                    "next boundary",
                    bool(
                        owner[
                            "next_boundary"
                        ]
                    ),
                ),
                (
                    "assertion count",
                    owner[
                        "assertion_count"
                    ]
                    == owner[
                        "expected_assertion_count"
                    ],
                ),
                (
                    "failed count",
                    owner[
                        "failed_assertion_count"
                    ]
                    == 0,
                ),
                (
                    "failed assertions",
                    owner[
                        "failed_assertions"
                    ]
                    == [],
                ),
                (
                    "planning ready",
                    owner[
                        "planning_ready"
                    ]
                    is True,
                ),
                (
                    "alpha ready",
                    owner[
                        "alpha_ready"
                    ]
                    is True,
                ),
                (
                    "runtime closed",
                    owner[
                        "runtime_ready"
                    ]
                    is False,
                ),
                (
                    "handoff metadata",
                    owner[
                        "handoff_metadata_present"
                    ]
                    is True,
                ),
            )

            for suffix, value in owner_checks:
                add(
                    f"{prefix} {suffix}",
                    value,
                )

            for method_packet in owner[
                "method_packets"
            ]:
                method_prefix = (
                    f"{prefix} method "
                    f"{method_packet['method']}"
                )

                add(
                    f"{method_prefix} allowed name",
                    method_packet[
                        "method"
                    ]
                    in self._PUBLIC_METHOD_ORDER,
                )

                add(
                    f"{method_prefix} deterministic",
                    method_packet[
                        "deterministic"
                    ]
                    is True,
                )

                add(
                    f"{method_prefix} packet summary",
                    method_packet[
                        "packet_summary"
                    ][
                        "packet_type"
                    ]
                    in {
                        "dict",
                        "list",
                        "tuple",
                        "str",
                        "int",
                        "bool",
                        "NoneType",
                    },
                )

        phase_names = []

        for sequence, phase in enumerate(
            contract[
                "rehearsal_phases"
            ],
            start=1,
        ):
            prefix = (
                f"rehearsal phase "
                f"{sequence:02d}"
            )

            expected_phase = (
                self._REHEARSAL_PHASES[
                    sequence - 1
                ][0]
            )

            phase_names.append(
                phase[
                    "phase"
                ]
            )

            add(
                f"{prefix} sequence",
                phase[
                    "sequence"
                ]
                == sequence,
            )

            add(
                f"{prefix} name",
                phase[
                    "phase"
                ]
                == expected_phase,
            )

            add(
                f"{prefix} purpose",
                bool(
                    phase[
                        "purpose"
                    ]
                ),
            )

            add(
                f"{prefix} runtime effects closed",
                phase[
                    "runtime_effects_allowed"
                ]
                is False,
            )

        if len(
            set(
                phase_names
            )
        ) != len(
            phase_names
        ):
            raise RuntimeError(
                "Sprint 229 rehearsal phase "
                "names must be unique"
            )

        acceptance_results = contract[
            "required_acceptance_results"
        ]

        acceptance_names = list(
            acceptance_results
        )

        for sequence, expected_name in enumerate(
            self._ACCEPTANCE_RESULT_NAMES,
            start=1,
        ):
            prefix = (
                f"acceptance result "
                f"{sequence:02d}"
            )

            add(
                f"{prefix} ordered name",
                acceptance_names[
                    sequence - 1
                ]
                == expected_name,
            )

            add(
                f"{prefix} boolean value",
                isinstance(
                    acceptance_results[
                        expected_name
                    ],
                    bool,
                ),
            )

            add(
                f"{prefix} passed",
                acceptance_results[
                    expected_name
                ]
                is True,
            )

        for sequence, domain in enumerate(
            contract[
                "evaluation_domains"
            ],
            start=1,
        ):
            prefix = (
                f"safety domain "
                f"{sequence:02d}"
            )

            add(
                f"{prefix} name",
                bool(
                    domain[
                        "domain"
                    ]
                ),
            )

            add(
                f"{prefix} owner",
                bool(
                    domain[
                        "owner_key"
                    ]
                ),
            )

            add(
                f"{prefix} activation denied",
                domain[
                    "activation_permitted"
                ]
                is False,
            )

            add(
                f"{prefix} evaluation mode",
                domain[
                    "evaluation_mode"
                ]
                == (
                    "read_only_contract_"
                    "precondition_review"
                ),
            )

        expected_negative_names = set(
            contract[
                "required_negative_results"
            ]
        )

        for name, value in contract[
            "required_negative_results"
        ].items():
            add(
                f"negative result {name} declared",
                name
                in expected_negative_names,
            )

            add(
                f"negative result {name} false",
                value
                is False,
            )

        for name, value in contract[
            "safety_boundary"
        ].items():
            add(
                f"safety boundary {name} false",
                value
                is False,
            )

        expected_counter_names = set(
            contract[
                "zero_counters"
            ]
        )

        for name, value in contract[
            "zero_counters"
        ].items():
            add(
                f"zero counter {name} declared",
                name
                in expected_counter_names,
            )

            add(
                f"zero counter {name} zero",
                value
                == 0,
            )

        if (
            len(assertions)
            != self.expected_assertion_count
        ):
            raise RuntimeError(
                "Sprint 229 assertion schema "
                f"expected {self.expected_assertion_count} "
                f"entries but produced "
                f"{len(assertions)}"
            )

        failed_assertions = [
            name
            for name, passed in (
                assertions.items()
            )
            if not passed
        ]

        failed_assertion_count = len(
            failed_assertions
        )

        ready = (
            failed_assertion_count
            == 0
        )

        packet = {
            "name":
                self.name,

            "version":
                self.version,

            "status":
                (
                    "PASS"
                    if ready
                    else "BLOCKED"
                ),

            "assertion_count":
                len(
                    assertions
                ),

            "expected_assertion_count":
                self.expected_assertion_count,

            "assertions":
                assertions,

            "failed_assertion_count":
                failed_assertion_count,

            "failed_assertions":
                failed_assertions,

            "planning_ready":
                ready,

            "alpha_ready":
                ready,

            "runtime_ready":
                False,

            "genesis_acceptance_rehearsal_contract":
                contract,
        }

        self._check_cache = deepcopy(
            packet
        )

        return deepcopy(
            packet
        )
