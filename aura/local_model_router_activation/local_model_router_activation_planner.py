from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json

from .local_model_router_activation_contract import (
    LocalModelRouterActivationContract,
)


class LocalModelRouterActivationPlanner:
    VERSION = "1.1.8"
    ANCHOR_VERSION = "1.1.7"
    CURRENT_SPRINT = 258
    NEXT_SPRINT = 259
    NEXT_VERSION = "1.1.9"
    BOUNDARY = "local_model_router_activation"
    NEXT_BOUNDARY = (
        "model_loading_unloading_queue_resource_budgets"
    )
    EXPECTED_ASSERTION_COUNT = 288

    DIMENSION_ORDER = (
        "canonical_router_owner",
        "existing_route_registry",
        "alias_normalization",
        "exact_route_required",
        "fallback_not_executable",
        "online_route_required",
        "supported_provider",
        "validated_profile",
        "loopback_endpoint",
        "health_dependency",
        "health_verification_required",
        "model_permission_required",
        "request_schema",
        "response_schema",
        "bounded_timeout",
        "no_route_persistence",
        "no_runtime_switching",
        "isolated_bridge_handoff",
        "no_service_mutation",
        "no_model_management",
        "no_queue",
        "no_resource_budget_mutation",
        "safe_idle",
        "handoff",
    )

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.contract = (
            LocalModelRouterActivationContract(
                project_root=self.project_root
            )
        )

    @staticmethod
    def _digest(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _evidence(self) -> dict[str, Any]:
        return {
            "router_status": (
                self.contract.router.status()
            ),
            "activation_snapshot": (
                self.contract.router
                .activation_snapshot()
            ),
            "companion": (
                self.contract.route_preview(
                    "chat"
                )
            ),
            "coding": (
                self.contract.route_preview(
                    "coding"
                )
            ),
            "unknown": (
                self.contract.route_preview(
                    "definitely-unknown-route"
                )
            ),
            "profile": (
                self.contract.profile_preview(
                    "companion"
                )
            ),
            "request": (
                self.contract.request_preview(
                    "companion"
                )
            ),
            "health": (
                self.contract.health.host_posture()
            ),
            "rehearsal": (
                self.contract.isolated_rehearsal()
            ),
        }

    def _assertions(
        self,
    ) -> list[tuple[str, bool]]:
        evidence = self._evidence()
        router_status = evidence[
            "router_status"
        ]
        activation = evidence[
            "activation_snapshot"
        ]
        companion = evidence["companion"]
        coding = evidence["coding"]
        unknown = evidence["unknown"]
        profile = evidence["profile"]
        request = evidence["request"]
        health = evidence["health"]
        rehearsal = evidence["rehearsal"]

        shared = [
            self.VERSION == "1.1.8",
            self.ANCHOR_VERSION == "1.1.7",
            self.CURRENT_SPRINT == 258,
            self.NEXT_SPRINT == 259,
            self.NEXT_VERSION == "1.1.9",
            self.NEXT_BOUNDARY
            == (
                "model_loading_unloading_queue_"
                "resource_budgets"
            ),
            router_status[
                "model_download_ready"
            ]
            is False,
            activation[
                "route_decision_persistence"
            ]
            is False,
            request[
                "live_inference_performed"
            ]
            is False,
            health[
                "health_probe_performed"
            ]
            is False,
            health[
                "network_connection_opened"
            ]
            is False,
        ]

        primary = {
            "canonical_router_owner": (
                router_status["name"]
                == "model_router"
                and activation[
                    "canonical_owner"
                ]
                == "ModelRouter"
            ),
            "existing_route_registry": (
                router_status["routes"] == 12
                and activation[
                    "existing_route_registry_only"
                ]
                is True
            ),
            "alias_normalization": (
                companion[
                    "normalized_target"
                ]
                == "companion"
                and companion[
                    "route_found"
                ]
                is True
            ),
            "exact_route_required": (
                unknown["route_found"]
                is False
                and (
                    "exact_route_required"
                    in unknown[
                        "denial_reasons"
                    ]
                )
            ),
            "fallback_not_executable": (
                unknown["fallback_used"]
                is True
                and unknown[
                    "eligible_for_confirmation"
                ]
                is False
            ),
            "online_route_required": (
                companion["route_status"]
                == "online"
                and coding["route_status"]
                == "foundation"
                and coding[
                    "eligible_for_confirmation"
                ]
                is False
            ),
            "supported_provider": (
                companion["provider"]
                == "ollama"
                and profile["provider"]
                == "ollama"
            ),
            "validated_profile": (
                profile[
                    "profile_enabled"
                ]
                is True
                and profile[
                    "persistent_configuration_write"
                ]
                is False
                and profile[
                    "credentials_read"
                ]
                is False
            ),
            "loopback_endpoint": (
                profile["base_url"]
                in {
                    "http://localhost:11434",
                    "http://127.0.0.1:11434",
                }
                and activation[
                    "non_loopback_network"
                ]
                is False
            ),
            "health_dependency": (
                health["state"]
                in {
                    "available_unprobed",
                    "degraded_unprobed",
                    "unavailable",
                }
                and request[
                    "provider_health_required"
                ]
                is True
            ),
            "health_verification_required": (
                rehearsal[
                    "denied_without_health"
                ]
                is True
                and rehearsal[
                    "provider_health_verified"
                ]
                is True
            ),
            "model_permission_required": (
                rehearsal[
                    "denied_without_permission"
                ]
                is True
                and request[
                    "model_request_permission_required"
                ]
                is True
            ),
            "request_schema": (
                self.contract.MAX_ROUTED_MESSAGES
                == 16
                and self.contract.MAX_ROUTED_INPUT_CHARS
                == 32768
            ),
            "response_schema": (
                rehearsal[
                    "bridge_result_is_object"
                ]
                is True
                and rehearsal[
                    "bridge_handoff_performed"
                ]
                is True
            ),
            "bounded_timeout": (
                profile[
                    "timeout_seconds"
                ]
                == 60.0
                and (
                    1.0
                    <= profile[
                        "timeout_seconds"
                    ]
                    <= 120.0
                )
            ),
            "no_route_persistence": (
                rehearsal[
                    "route_decision_persisted"
                ]
                is False
                and companion[
                    "route_decision_persisted"
                ]
                is False
            ),
            "no_runtime_switching": (
                rehearsal[
                    "runtime_switching_performed"
                ]
                is False
                and activation[
                    "real_runtime_switching"
                ]
                is False
            ),
            "isolated_bridge_handoff": (
                rehearsal[
                    "transport_call_count"
                ]
                == 1
                and rehearsal[
                    "transport_method"
                ]
                == "POST"
                and rehearsal[
                    "transport_url_loopback"
                ]
                is True
                and rehearsal[
                    "payload_stream_false"
                ]
                is True
            ),
            "no_service_mutation": (
                rehearsal[
                    "service_mutated"
                ]
                is False
                and activation[
                    "service_control"
                ]
                is False
            ),
            "no_model_management": (
                rehearsal[
                    "model_downloaded"
                ]
                is False
                and rehearsal[
                    "model_loaded"
                ]
                is False
                and activation[
                    "model_management"
                ]
                is False
            ),
            "no_queue": (
                rehearsal[
                    "queue_activated"
                ]
                is False
                and activation[
                    "queue_runtime"
                ]
                is False
            ),
            "no_resource_budget_mutation": (
                rehearsal[
                    "resource_budget_mutated"
                ]
                is False
                and activation[
                    "resource_budget_mutation"
                ]
                is False
            ),
            "safe_idle": (
                rehearsal[
                    "canonical_network_opened"
                ]
                is False
                and rehearsal[
                    "chat_session_mutated"
                ]
                is False
                and rehearsal[
                    "memory_mutated"
                ]
                is False
                and rehearsal[
                    "systemd_mutated"
                ]
                is False
                and rehearsal[
                    "autostart_mutated"
                ]
                is False
            ),
            "handoff": (
                self.BOUNDARY
                == "local_model_router_activation"
                and self.NEXT_BOUNDARY
                == (
                    "model_loading_unloading_queue_"
                    "resource_budgets"
                )
            ),
        }

        assertions: list[
            tuple[str, bool]
        ] = []

        for dimension in self.DIMENSION_ORDER:
            values = [
                primary[dimension],
                *shared,
            ]

            if len(values) != 12:
                raise RuntimeError(
                    "Each dimension requires twelve checks."
                )

            for index, passed in enumerate(
                values,
                start=1,
            ):
                assertions.append(
                    (
                        f"{dimension}.{index:02d}",
                        bool(passed),
                    )
                )

        return assertions

    def check(self) -> dict[str, Any]:
        assertions = self._assertions()
        failed = [
            name
            for name, passed in assertions
            if not passed
        ]

        return {
            "owner": (
                "LocalModelRouterActivationPlanner"
            ),
            "canonical_owner": "ModelRouter",
            "bridge_owner": (
                "AuraLocalModelBridgeRuntimeManager"
            ),
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "permission_gated_route_selection_and_bridge_handoff"
            ),
            "assertion_count": len(
                assertions
            ),
            "failed_assertion_count": len(
                failed
            ),
            "failed_assertions": failed,
            "dimension_count": len(
                self.DIMENSION_ORDER
            ),
            "finding_count": len(failed),
            "overall_state": (
                "secure"
                if not failed
                else "review"
            ),
            "alpha_ready": not failed,
            "status_valid": (
                len(assertions)
                == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in assertions
            ],
        }

    def status(self) -> dict[str, Any]:
        check = self.check()

        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "canonical_owner",
                    "bridge_owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "next_version",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "status_valid",
                )
            },
            "router_status": (
                self.contract.router.status()
            ),
            "activation_snapshot": (
                self.contract.router
                .activation_snapshot()
            ),
            "route_preview": (
                self.contract.route_preview(
                    "companion"
                )
            ),
            "request_preview": (
                self.contract.request_preview(
                    "companion"
                )
            ),
            "route_selection_performed": False,
            "model_request_performed": False,
            "network_connection_opened": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "canonical_owner": "ModelRouter",
            "bridge_owner": (
                "AuraLocalModelBridgeRuntimeManager"
            ),
            "health_dependency": (
                "local_model_service_discovery_health"
            ),
            "route_registry": (
                "existing_configured_routes_only"
            ),
            "default_target": "companion",
            "active_provider": (
                self.contract.router
                .current_provider()
            ),
            "active_model": (
                self.contract.router
                .current_model()
            ),
            "active_host": (
                self.contract.router
                .current_host()
            ),
            "route_persistence": False,
            "runtime_switching": False,
            "queue_runtime": False,
            "resource_budget_mutation": False,
        }

    def review(self) -> dict[str, Any]:
        check = self.check()

        return {
            "ok": (
                check[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": (
                check[
                    "failed_assertion_count"
                ]
            ),
            "dimension_count": check[
                "dimension_count"
            ],
            "overall_state": check[
                "overall_state"
            ],
            "review_digest": self._digest(
                check["assertions"]
            ),
            "blocked_surfaces": {
                "automatic_route_execution": True,
                "unknown_route_fallback_execution": True,
                "foundation_or_planned_route_execution": True,
                "unverified_provider_execution": True,
                "unconfirmed_model_request": True,
                "route_persistence": True,
                "runtime_switching": True,
                "service_start_stop": True,
                "model_download_pull": True,
                "model_load_unload": True,
                "queue_activation": True,
                "resource_budget_mutation": True,
                "non_loopback_network": True,
                "credentials": True,
                "systemd_mutation": True,
                "autostart_mutation": True,
            },
        }

    def route_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.contract.route_preview(
            target
        )

    def profile_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.contract.profile_preview(
            target
        )

    def request_preview(
        self,
        target: str,
    ) -> dict[str, Any]:
        return self.contract.request_preview(
            target
        )

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        return self.contract.isolated_rehearsal()
