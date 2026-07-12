"""AURA Sprint 228 safe auto-start evaluation contract.

This module is contract-only and read-only. It evaluates whether future
auto-start work has sufficient safety prerequisites without enabling,
installing, starting, stopping, restarting, launching, binding, or writing
any runtime service artifact.
"""

from __future__ import annotations

import hashlib
import inspect
from pathlib import Path
from typing import Any

from .service_persistence_and_launcher_alpha_manager import (
    ServicePersistenceAndLauncherAlphaManager,
)

from aura.service_lifecycle_runtime.aura_service_lifecycle_runtime_manager import (
    AuraServiceLifecycleRuntimeManager,
)

from aura.local_service_safe_idle_boot_boundary.aura_local_service_safe_idle_boot_boundary_manager import (
    AuraLocalServiceSafeIdleBootBoundaryManager,
)

from aura.service_security_localhost_binding_review.aura_service_security_localhost_binding_review_manager import (
    AuraServiceSecurityLocalhostBindingReviewManager,
)

from aura.local_service_health_endpoint_foundation.aura_local_service_health_endpoint_foundation_manager import (
    AuraLocalServiceHealthEndpointFoundationManager,
)

from aura.service_permission_gate_runtime_boundary.aura_service_permission_gate_runtime_boundary_manager import (
    AuraServicePermissionGateRuntimeBoundaryManager,
)

from aura.service_audit_link_foundation.aura_service_audit_link_foundation_manager import (
    AuraServiceAuditLinkFoundationManager,
)

from aura.service_recovery_restart_policy_foundation.aura_service_recovery_restart_policy_foundation_manager import (
    AuraServiceRecoveryRestartPolicyFoundationManager,
)

from aura.local_service_boot_plan_review.aura_local_service_boot_plan_review_foundation_manager import (
    AuraLocalServiceBootPlanReviewFoundationManager,
)

from aura.launcher_monitor.aura_launcher_health_monitor_foundation_manager import (
    AuraLauncherHealthMonitorFoundationManager,
)

from aura.control_center_service_monitor_panel_foundation.aura_control_center_service_monitor_panel_foundation_manager import (
    AuraControlCenterServiceMonitorPanelFoundationManager,
)


class SafeAutoStartEvaluationPlanner:
    """Build the read-only Sprint 228 safe auto-start evaluation contract."""

    name = "safe_auto_start_evaluation"
    version = "0.1.0-alpha"

    current_sprint = 228
    next_sprint = 229

    boundary = "safe_auto_start_evaluation"
    next_boundary = "genesis_acceptance_rehearsal"

    identity_version = "0.229.0-genesis"

    evaluation_mode = (
        "contract_only_read_only_safety_evaluation"
    )

    canonical_target = "safe_auto_start_evaluation"

    canonical_lifecycle_owner = (
        "aura.service_lifecycle_runtime."
        "aura_service_lifecycle_runtime_manager."
        "AuraServiceLifecycleRuntimeManager"
    )

    canonical_lifecycle_access_mode = (
        "static_contract_metadata_only"
    )

    _OWNER_SPECS: dict[str, dict[str, Any]] = {
        "safe_idle_boot": {
            "class":
                AuraLocalServiceSafeIdleBootBoundaryManager,

            "role":
                "read_only_safe_idle_boot_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "safe_idle_boot_scope_plan",
                "boot_entry_state_contract_plan",
                "boot_failure_fallback_plan",
                "service_no_autostart_boundary_plan",
                "permission_denial_idle_plan",
                "audit_failure_idle_plan",
                "no_boot_activation_plan",
            ),
        },

        "localhost_security": {
            "class":
                AuraServiceSecurityLocalhostBindingReviewManager,

            "role":
                "read_only_localhost_security_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "service_localhost_binding_policy_plan",
                "service_security_permission_audit_link_plan",
                "service_port_binding_preflight_security_plan",
            ),
        },

        "health_readiness": {
            "class":
                AuraLocalServiceHealthEndpointFoundationManager,

            "role":
                "read_only_health_readiness_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "health_endpoint_scope_plan",
                "health_endpoint_contract_plan",
                "health_response_schema_plan",
                "localhost_health_binding_boundary_plan",
                "safe_idle_health_state_plan",
                "health_dependency_visibility_plan",
                "permission_audit_health_link_plan",
                "control_center_health_card_plan",
                "health_error_fallback_plan",
                "no_health_endpoint_activation_plan",
            ),
        },

        "permission_confirmation": {
            "class":
                AuraServicePermissionGateRuntimeBoundaryManager,

            "role":
                "read_only_permission_confirmation_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "service_permission_scope_catalog_plan",
                "service_permission_request_contract_plan",
                "service_permission_grant_preflight_plan",
                "service_permission_denial_safe_idle_plan",
                "service_permission_control_center_surface_plan",
                "service_permission_audit_link_plan",
                "service_permission_expiry_review_plan",
                "service_permission_error_boundary_plan",
                "service_permission_manual_approval_boundary_plan",
                "no_permission_runtime_activation_plan",
            ),
        },

        "audit_traceability": {
            "class":
                AuraServiceAuditLinkFoundationManager,

            "role":
                "read_only_audit_traceability_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "service_audit_event_reference_plan",
                "service_audit_link_contract_plan",
                "service_audit_traceability_chain_plan",
                "service_audit_permission_link_plan",
                "service_audit_control_center_surface_plan",
                "service_audit_redaction_boundary_plan",
                "service_audit_failure_safe_idle_plan",
                "service_audit_retention_boundary_plan",
                "service_audit_error_boundary_plan",
                "no_audit_link_runtime_activation_plan",
            ),
        },

        "manual_recovery": {
            "class":
                AuraServiceRecoveryRestartPolicyFoundationManager,

            "role":
                "read_only_manual_recovery_precondition_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "service_safe_idle_recovery_policy_plan",
                "service_restart_approval_policy_plan",
                "service_recovery_audit_link_plan",
                "service_recovery_permission_boundary_plan",
                "service_control_center_recovery_surface_plan",
                "service_recovery_error_boundary_plan",
                "no_recovery_restart_runtime_activation_plan",
            ),
        },

        "boot_and_autostart_guard": {
            "class":
                AuraLocalServiceBootPlanReviewFoundationManager,

            "role":
                "read_only_autostart_and_rollback_review_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "local_service_manual_start_review_plan",
                "local_service_manual_stop_review_plan",
                "local_service_health_monitor_review_plan",
                "local_service_config_contract_review_plan",
                "local_service_autostart_guard_review_plan",
                "local_service_no_port_binding_review_plan",
            ),
        },

        "launcher_visibility": {
            "class":
                AuraLauncherHealthMonitorFoundationManager,

            "role":
                "read_only_launcher_visibility_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "launcher_plan_types",
                "launcher_modes",
                "launcher_actions",
                "health_states",
                "monitor_fields",
                "safety_boundary",
                "launcher_summary",
            ),

            "target_methods":
                (),
        },

        "operator_visibility": {
            "class":
                AuraControlCenterServiceMonitorPanelFoundationManager,

            "role":
                "read_only_operator_visibility_owner",

            "zero_argument_methods": (
                "status",
                "context",
                "safety_boundary",
            ),

            "target_methods": (
                "service_monitor_layout_contract_plan",
                "service_health_signal_contract_plan",
                "service_restart_recovery_status_plan",
                "service_security_localhost_status_plan",
            ),
        },
    }

    _EVALUATION_DOMAIN_OWNERS = {
        "safe_idle_boot_precondition":
            "safe_idle_boot",

        "localhost_only_binding_precondition":
            "localhost_security",

        "health_readiness_precondition":
            "health_readiness",

        "permission_confirmation_precondition":
            "permission_confirmation",

        "audit_traceability_precondition":
            "audit_traceability",

        "manual_recovery_precondition":
            "manual_recovery",

        "emergency_stop_precondition":
            "canonical_lifecycle_static_metadata",

        "operator_visibility_precondition":
            "operator_visibility",

        "systemd_unit_review_precondition":
            "boot_and_autostart_guard",

        "rollback_and_disable_precondition":
            "boot_and_autostart_guard",
    }

    _NEGATIVE_RESULTS = {
        "auto_start_enabled":
            False,

        "systemd_unit_written":
            False,

        "systemd_unit_installed":
            False,

        "systemctl_called":
            False,

        "service_started":
            False,

        "service_stopped":
            False,

        "service_restarted":
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

        "automatic_restart_enabled":
            False,

        "autonomous_recovery_enabled":
            False,

        "runtime_activation_allowed":
            False,

        "release_gate_open":
            False,
    }

    _ZERO_COUNTERS = {
        "lifecycle_instances_created":
            0,

        "lifecycle_runtime_methods_invoked":
            0,

        "target_plan_methods_invoked":
            0,

        "service_state_writes":
            0,

        "pid_file_writes":
            0,

        "systemd_unit_writes":
            0,

        "systemd_unit_installs":
            0,

        "systemctl_calls":
            0,

        "service_start_calls":
            0,

        "service_stop_calls":
            0,

        "service_restart_calls":
            0,

        "listener_start_calls":
            0,

        "socket_open_calls":
            0,

        "thread_start_calls":
            0,

        "subprocess_start_calls":
            0,

        "launcher_execution_calls":
            0,

        "browser_launch_calls":
            0,

        "automatic_restart_enables":
            0,

        "autonomous_recovery_enables":
            0,

        "runtime_activation_calls":
            0,

        "release_gate_open_calls":
            0,
    }

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        upstream_manager:
            ServicePersistenceAndLauncherAlphaManager
            | None = None,
    ) -> None:
        if project_root is None:
            self.project_root = (
                Path(__file__)
                .resolve()
                .parents[2]
            )
        else:
            self.project_root = Path(
                project_root
            ).resolve()

        self._upstream_manager = (
            upstream_manager
            or ServicePersistenceAndLauncherAlphaManager(
                project_root=self.project_root
            )
        )

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:
        return hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

    @staticmethod
    def _required_parameters(
        method: Any,
    ) -> list[str]:
        signature = inspect.signature(
            method
        )

        return [
            parameter.name
            for parameter
            in signature.parameters.values()
            if (
                parameter.default
                is inspect.Parameter.empty
                and parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            )
        ]

    def _instantiate_owner(
        self,
        cls: type[Any],
    ) -> Any:
        signature = inspect.signature(cls)

        kwargs: dict[str, Any] = {}

        if (
            "project_root"
            in signature.parameters
        ):
            kwargs[
                "project_root"
            ] = self.project_root

        required = [
            parameter.name
            for parameter
            in signature.parameters.values()
            if (
                parameter.name
                not in kwargs
                and parameter.default
                is inspect.Parameter.empty
                and parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            )
        ]

        if required:
            raise TypeError(
                "unsupported owner constructor "
                "parameters: "
                + ", ".join(required)
            )

        return cls(**kwargs)

    def _upstream_snapshot(
        self,
    ) -> dict[str, Any]:
        packet = (
            self._upstream_manager.check()
        )

        return {
            "owner": (
                "aura.partner_runtime."
                "service_persistence_and_launcher_"
                "alpha_manager."
                "ServicePersistenceAndLauncherAlphaManager"
            ),

            "assertion_count":
                packet.get(
                    "assertion_count"
                ),

            "expected_assertion_count":
                packet.get(
                    "expected_assertion_count"
                ),

            "failed_assertion_count":
                packet.get(
                    "failed_assertion_count"
                ),

            "failed_assertions":
                packet.get(
                    "failed_assertions",
                    [],
                ),

            "planning_ready":
                packet.get(
                    "planning_ready"
                ),

            "alpha_ready":
                packet.get(
                    "alpha_ready"
                ),

            "runtime_ready":
                packet.get(
                    "runtime_ready"
                ),

            "next_boundary":
                packet.get(
                    "service_persistence_and_"
                    "launcher_contract",
                    {},
                ).get(
                    "next_boundary"
                ),
        }

    def _lifecycle_static_snapshot(
        self,
    ) -> dict[str, Any]:
        cls = (
            AuraServiceLifecycleRuntimeManager
        )

        source_text = inspect.getsourcefile(
            cls
        )

        if source_text is None:
            raise RuntimeError(
                "canonical lifecycle source "
                "is unavailable"
            )

        source = Path(
            source_text
        ).resolve()

        members = []

        for name in sorted(
            vars(cls)
        ):
            if name.startswith("__"):
                continue

            descriptor = (
                inspect.getattr_static(
                    cls,
                    name,
                )
            )

            if isinstance(
                descriptor,
                classmethod,
            ):
                descriptor_type = (
                    "classmethod"
                )

            elif isinstance(
                descriptor,
                staticmethod,
            ):
                descriptor_type = (
                    "staticmethod"
                )

            elif isinstance(
                descriptor,
                property,
            ):
                descriptor_type = (
                    "property"
                )

            elif inspect.isfunction(
                descriptor
            ):
                descriptor_type = (
                    "instance_method"
                )

            else:
                descriptor_type = (
                    type(
                        descriptor
                    ).__name__
                )

            members.append(
                {
                    "name":
                        name,

                    "descriptor_type":
                        descriptor_type,
                }
            )

        return {
            "owner":
                self.canonical_lifecycle_owner,

            "access_mode":
                self.canonical_lifecycle_access_mode,

            "constructor_signature":
                str(
                    inspect.signature(
                        cls
                    )
                ),

            "source":
                str(
                    source.relative_to(
                        self.project_root
                    )
                ),

            "source_sha256":
                self._sha256(source),

            "member_count":
                len(members),

            "members":
                members,

            "instance_created":
                False,

            "method_invocation_allowed":
                False,

            "runtime_methods_invoked":
                [],
        }

    def _foundation_owner_snapshot(
        self,
        domain: str,
        spec: dict[str, Any],
    ) -> dict[str, Any]:
        cls = spec["class"]

        instance = (
            self._instantiate_owner(
                cls
            )
        )

        source_text = inspect.getsourcefile(
            cls
        )

        if source_text is None:
            raise RuntimeError(
                "foundation owner source "
                f"unavailable: {domain}"
            )

        source = Path(
            source_text
        ).resolve()

        zero_argument_packets = {}

        for method_name in (
            spec[
                "zero_argument_methods"
            ]
        ):
            method = getattr(
                instance,
                method_name,
                None,
            )

            if not callable(method):
                raise AttributeError(
                    f"{domain}.{method_name} "
                    "is unavailable"
                )

            required = (
                self._required_parameters(
                    method
                )
            )

            if required:
                raise TypeError(
                    f"{domain}.{method_name} "
                    "unexpectedly requires: "
                    + ", ".join(required)
                )

            packet_1 = method()
            packet_2 = method()

            if packet_1 != packet_2:
                raise RuntimeError(
                    f"{domain}.{method_name} "
                    "is not deterministic"
                )

            zero_argument_packets[
                method_name
            ] = {
                "signature":
                    str(
                        inspect.signature(
                            method
                        )
                    ),

                "invoked":
                    True,

                "deterministic":
                    True,

                "return_type":
                    type(
                        packet_1
                    ).__name__,

                "packet":
                    packet_1,
            }

        target_method_packets = {}

        for method_name in (
            spec[
                "target_methods"
            ]
        ):
            method = getattr(
                instance,
                method_name,
                None,
            )

            if not callable(method):
                raise AttributeError(
                    f"{domain}.{method_name} "
                    "is unavailable"
                )

            required = (
                self._required_parameters(
                    method
                )
            )

            target_method_packets[
                method_name
            ] = {
                "signature":
                    str(
                        inspect.signature(
                            method
                        )
                    ),

                "required_parameters":
                    required,

                "canonical_target":
                    self.canonical_target,

                "invoked":
                    False,
            }

        return {
            "domain":
                domain,

            "owner":
                cls.__module__
                + "."
                + cls.__name__,

            "role":
                spec["role"],

            "constructor_signature":
                str(
                    inspect.signature(
                        cls
                    )
                ),

            "source":
                str(
                    source.relative_to(
                        self.project_root
                    )
                ),

            "source_sha256":
                self._sha256(source),

            "zero_argument_method_count":
                len(
                    zero_argument_packets
                ),

            "target_method_count":
                len(
                    target_method_packets
                ),

            "method_count":
                (
                    len(
                        zero_argument_packets
                    )
                    + len(
                        target_method_packets
                    )
                ),

            "zero_argument_methods":
                zero_argument_packets,

            "target_methods":
                target_method_packets,

            "target_methods_invoked":
                False,
        }

    def foundation_owner_snapshots(
        self,
    ) -> dict[str, Any]:
        return {
            domain:
                self._foundation_owner_snapshot(
                    domain,
                    spec,
                )
            for domain, spec
            in self._OWNER_SPECS.items()
        }

    def evaluation_domains(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "domain":
                    domain,

                "owner_key":
                    owner,

                "evaluation_mode":
                    (
                        "read_only_contract_"
                        "precondition_review"
                    ),

                "activation_permitted":
                    False,
            }
            for domain, owner
            in (
                self._EVALUATION_DOMAIN_OWNERS.items()
            )
        ]

    def safety_boundary(
        self,
    ) -> dict[str, bool]:
        return dict(
            self._NEGATIVE_RESULTS
        )

    def zero_counters(
        self,
    ) -> dict[str, int]:
        return dict(
            self._ZERO_COUNTERS
        )

    def safe_auto_start_evaluation_contract(
        self,
    ) -> dict[str, Any]:
        upstream = (
            self._upstream_snapshot()
        )

        lifecycle = (
            self._lifecycle_static_snapshot()
        )

        owners = (
            self.foundation_owner_snapshots()
        )

        evaluation_domains = (
            self.evaluation_domains()
        )

        zero_argument_method_count = sum(
            packet[
                "zero_argument_method_count"
            ]
            for packet in owners.values()
        )

        target_method_count = sum(
            packet[
                "target_method_count"
            ]
            for packet in owners.values()
        )

        total_method_count = sum(
            packet[
                "method_count"
            ]
            for packet in owners.values()
        )

        return {
            "name":
                self.name,

            "version":
                self.version,

            "identity_version":
                self.identity_version,

            "current_sprint":
                self.current_sprint,

            "boundary":
                self.boundary,

            "next_sprint":
                self.next_sprint,

            "next_boundary":
                self.next_boundary,

            "evaluation_mode":
                self.evaluation_mode,

            "canonical_target":
                self.canonical_target,

            "upstream_snapshot":
                upstream,

            "canonical_lifecycle_snapshot":
                lifecycle,

            "foundation_owner_snapshots":
                owners,

            "foundation_owner_count":
                len(owners),

            "foundation_method_count":
                total_method_count,

            "zero_argument_method_count":
                zero_argument_method_count,

            "target_method_count":
                target_method_count,

            "target_methods_invoked":
                False,

            "evaluation_domains":
                evaluation_domains,

            "evaluation_domain_count":
                len(
                    evaluation_domains
                ),

            "required_negative_results":
                dict(
                    self._NEGATIVE_RESULTS
                ),

            "safety_boundary":
                self.safety_boundary(),

            "zero_counters":
                self.zero_counters(),

            "safe_auto_start_evaluation_contract_ready":
                True,

            "auto_start_activation_ready":
                False,

            "runtime_ready":
                False,

            "release_gate_open":
                False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.safe_auto_start_evaluation_contract()
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

            "evaluation_mode":
                self.evaluation_mode,

            "evaluation_domains":
                contract[
                    "evaluation_domains"
                ],

            "required_negative_results":
                contract[
                    "required_negative_results"
                ],

            "runtime_ready":
                False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.safe_auto_start_evaluation_contract()
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

            "foundation_owner_count":
                contract[
                    "foundation_owner_count"
                ],

            "foundation_method_count":
                contract[
                    "foundation_method_count"
                ],

            "zero_argument_method_count":
                contract[
                    "zero_argument_method_count"
                ],

            "target_method_count":
                contract[
                    "target_method_count"
                ],

            "target_methods_invoked":
                False,

            "planning_ready":
                True,

            "alpha_ready":
                True,

            "runtime_ready":
                False,

            "auto_start_enabled":
                False,

            "release_gate_open":
                False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.safe_auto_start_evaluation_contract()
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

            "canonical_target":
                self.canonical_target,

            "evaluation_mode":
                self.evaluation_mode,

            "upstream_owner":
                contract[
                    "upstream_snapshot"
                ][
                    "owner"
                ],

            "canonical_lifecycle_owner":
                contract[
                    "canonical_lifecycle_snapshot"
                ][
                    "owner"
                ],

            "canonical_lifecycle_access_mode":
                contract[
                    "canonical_lifecycle_snapshot"
                ][
                    "access_mode"
                ],

            "foundation_owner_count":
                contract[
                    "foundation_owner_count"
                ],

            "evaluation_domain_count":
                contract[
                    "evaluation_domain_count"
                ],

            "runtime_ready":
                False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.safe_auto_start_evaluation_contract()
        )

        assertions: dict[str, bool] = {}

        def add(
            name: str,
            condition: Any,
        ) -> None:
            assertions[
                name
            ] = bool(condition)

        add(
            "current sprint is 228",
            contract[
                "current_sprint"
            ]
            == 228,
        )

        add(
            "boundary is safe auto-start evaluation",
            contract[
                "boundary"
            ]
            == "safe_auto_start_evaluation",
        )

        add(
            "next sprint is 229",
            contract[
                "next_sprint"
            ]
            == 229,
        )

        add(
            "next boundary is genesis acceptance rehearsal",
            contract[
                "next_boundary"
            ]
            == "genesis_acceptance_rehearsal",
        )

        add(
            "evaluation mode is contract only",
            contract[
                "evaluation_mode"
            ]
            == (
                "contract_only_read_only_"
                "safety_evaluation"
            ),
        )

        add(
            "canonical target is stable",
            contract[
                "canonical_target"
            ]
            == "safe_auto_start_evaluation",
        )

        upstream = contract[
            "upstream_snapshot"
        ]

        add(
            "upstream assertion count is 208",
            upstream[
                "assertion_count"
            ]
            == 208,
        )

        add(
            "upstream failures are zero",
            upstream[
                "failed_assertion_count"
            ]
            == 0,
        )

        add(
            "upstream failed assertions are empty",
            upstream[
                "failed_assertions"
            ]
            == [],
        )

        add(
            "upstream planning ready",
            upstream[
                "planning_ready"
            ]
            is True,
        )

        add(
            "upstream alpha ready",
            upstream[
                "alpha_ready"
            ]
            is True,
        )

        add(
            "upstream runtime closed",
            upstream[
                "runtime_ready"
            ]
            is False,
        )

        add(
            "upstream next boundary aligned",
            upstream[
                "next_boundary"
            ]
            == "safe_auto_start_evaluation",
        )

        lifecycle = contract[
            "canonical_lifecycle_snapshot"
        ]

        add(
            "lifecycle access is static metadata only",
            lifecycle[
                "access_mode"
            ]
            == "static_contract_metadata_only",
        )

        add(
            "lifecycle source hash present",
            len(
                lifecycle[
                    "source_sha256"
                ]
            )
            == 64,
        )

        add(
            "lifecycle members discovered",
            lifecycle[
                "member_count"
            ]
            > 0,
        )

        add(
            "lifecycle instance not created",
            lifecycle[
                "instance_created"
            ]
            is False,
        )

        add(
            "lifecycle invocation disallowed",
            lifecycle[
                "method_invocation_allowed"
            ]
            is False,
        )

        add(
            "lifecycle methods not invoked",
            lifecycle[
                "runtime_methods_invoked"
            ]
            == [],
        )

        owners = contract[
            "foundation_owner_snapshots"
        ]

        add(
            "foundation owner count is nine",
            contract[
                "foundation_owner_count"
            ]
            == 9,
        )

        add(
            "foundation method count is ninety",
            contract[
                "foundation_method_count"
            ]
            == 90,
        )

        add(
            "zero argument method count is thirty three",
            contract[
                "zero_argument_method_count"
            ]
            == 33,
        )

        add(
            "target method count is fifty seven",
            contract[
                "target_method_count"
            ]
            == 57,
        )

        add(
            "target methods remain uninvoked",
            contract[
                "target_methods_invoked"
            ]
            is False,
        )

        for domain, packet in (
            owners.items()
        ):
            add(
                f"{domain} owner source hash present",
                len(
                    packet[
                        "source_sha256"
                    ]
                )
                == 64,
            )

            add(
                f"{domain} method count consistent",
                packet[
                    "method_count"
                ]
                == (
                    packet[
                        "zero_argument_method_count"
                    ]
                    + packet[
                        "target_method_count"
                    ]
                ),
            )

            add(
                f"{domain} target methods not invoked",
                packet[
                    "target_methods_invoked"
                ]
                is False,
            )

            for (
                method_name,
                method_packet,
            ) in packet[
                "zero_argument_methods"
            ].items():
                add(
                    f"{domain}.{method_name} invoked",
                    method_packet[
                        "invoked"
                    ]
                    is True,
                )

                add(
                    f"{domain}.{method_name} deterministic",
                    method_packet[
                        "deterministic"
                    ]
                    is True,
                )

            for (
                method_name,
                method_packet,
            ) in packet[
                "target_methods"
            ].items():
                add(
                    f"{domain}.{method_name} requires target",
                    method_packet[
                        "required_parameters"
                    ]
                    == [
                        "target",
                    ],
                )

                add(
                    f"{domain}.{method_name} canonical target aligned",
                    method_packet[
                        "canonical_target"
                    ]
                    == "safe_auto_start_evaluation",
                )

                add(
                    f"{domain}.{method_name} not invoked",
                    method_packet[
                        "invoked"
                    ]
                    is False,
                )

        add(
            "evaluation domain count is ten",
            contract[
                "evaluation_domain_count"
            ]
            == 10,
        )

        for domain in contract[
            "evaluation_domains"
        ]:
            add(
                (
                    domain[
                        "domain"
                    ]
                    + " remains non-activating"
                ),
                domain[
                    "activation_permitted"
                ]
                is False,
            )

        for name, value in contract[
            "required_negative_results"
        ].items():
            add(
                f"negative result {name} remains false",
                value is False,
            )

        for name, value in contract[
            "safety_boundary"
        ].items():
            add(
                f"safety boundary {name} remains false",
                value is False,
            )

        for name, value in contract[
            "zero_counters"
        ].items():
            add(
                f"zero counter {name} remains zero",
                value == 0,
            )

        add(
            "contract ready",
            contract[
                "safe_auto_start_evaluation_contract_ready"
            ]
            is True,
        )

        add(
            "auto-start activation not ready",
            contract[
                "auto_start_activation_ready"
            ]
            is False,
        )

        add(
            "runtime remains closed",
            contract[
                "runtime_ready"
            ]
            is False,
        )

        add(
            "release gate remains closed",
            contract[
                "release_gate_open"
            ]
            is False,
        )

        failed_assertions = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "name":
                self.name,

            "version":
                self.version,

            "status":
                (
                    "READY"
                    if not failed_assertions
                    else "BLOCKED"
                ),

            "assertion_count":
                len(assertions),

            "expected_assertion_count":
                len(assertions),

            "failed_assertion_count":
                len(
                    failed_assertions
                ),

            "failed_assertions":
                failed_assertions,

            "assertions":
                assertions,

            "planning_ready":
                not failed_assertions,

            "alpha_ready":
                not failed_assertions,

            "runtime_ready":
                False,

            "safe_auto_start_evaluation_contract":
                contract,
        }
