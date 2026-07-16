from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json

from .local_model_service_discovery_health_contract import (
    LocalModelServiceDiscoveryHealthContract,
)


class LocalModelServiceDiscoveryHealthPlanner:
    VERSION = "1.1.7"
    ANCHOR_VERSION = "1.1.6"
    CURRENT_SPRINT = 257
    NEXT_SPRINT = 258
    NEXT_VERSION = "1.1.8"
    BOUNDARY = (
        "local_model_service_discovery_health"
    )
    NEXT_BOUNDARY = (
        "local_model_router_activation"
    )
    EXPECTED_ASSERTION_COUNT = 264

    DIMENSION_ORDER = (
        "canonical_owner",
        "binary_discovery",
        "unit_discovery",
        "process_discovery",
        "listener_discovery",
        "loopback_only",
        "provider_contract",
        "profile_resolution",
        "probe_default_off",
        "explicit_confirmation",
        "bounded_timeout",
        "no_redirects",
        "proxy_disabled",
        "response_bound",
        "metadata_only_models",
        "health_classification",
        "failure_classification",
        "no_activation",
        "no_download",
        "no_routing",
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
            LocalModelServiceDiscoveryHealthContract(
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
            "host": (
                self.contract.host_posture()
            ),
            "contracts": (
                self.contract.provider_contracts()
            ),
            "preview": (
                self.contract.health_preview()
            ),
            "rehearsal": (
                self.contract.isolated_rehearsal()
            ),
        }

    def _assertions(
        self,
    ) -> list[tuple[str, bool]]:
        evidence = self._evidence()
        host = evidence["host"]
        contracts = evidence["contracts"]
        preview = evidence["preview"]
        rehearsal = evidence["rehearsal"]

        shared = [
            self.VERSION == "1.1.7",
            self.ANCHOR_VERSION == "1.1.6",
            self.CURRENT_SPRINT == 257,
            self.NEXT_SPRINT == 258,
            self.NEXT_VERSION == "1.1.8",
            self.NEXT_BOUNDARY
            == "local_model_router_activation",
            preview[
                "health_probe_performed"
            ]
            is False,
            preview[
                "network_connection_opened"
            ]
            is False,
            host["service_started"] is False,
            host["model_downloaded"] is False,
            host["chat_routed"] is False,
        ]

        primary = {
            "canonical_owner": (
                contracts["sprint_257_owner"]
                == "existing_local_model_bridge_runtime"
            ),
            "binary_discovery": (
                host["binary"][
                    "metadata_only"
                ]
                is True
                and host["binary"][
                    "binary_executed"
                ]
                is False
            ),
            "unit_discovery": (
                host["unit"][
                    "mutation_performed"
                ]
                is False
                and "fields"
                in host["unit"]
            ),
            "process_discovery": (
                host["process"][
                    "command_line_exposed"
                ]
                is False
                and "exists"
                in host["process"]
            ),
            "listener_discovery": (
                host["listener_count"]
                == len(host["listeners"])
                and all(
                    item["state"]
                    == "listen"
                    for item in host[
                        "listeners"
                    ]
                )
            ),
            "loopback_only": (
                host[
                    "wildcard_listener_count"
                ]
                == 0
                and contracts[
                    "resolved_loopback_enforcement"
                ]
                is True
            ),
            "provider_contract": (
                "ollama"
                in contracts["providers"]
                and contracts[
                    "default_health_endpoint"
                ]
                == "http://127.0.0.1:11434"
            ),
            "profile_resolution": (
                host["profile"][
                    "persistent_configuration_write"
                ]
                is False
                and host["profile"][
                    "credentials_read"
                ]
                is False
            ),
            "probe_default_off": (
                contracts[
                    "health_probe_default"
                ]
                is False
                and preview[
                    "health_probe_performed"
                ]
                is False
            ),
            "explicit_confirmation": (
                rehearsal[
                    "denied_without_confirmation"
                ]
                is True
                and contracts[
                    "health_confirmation_token"
                ]
                == "PROBE_LOCAL_MODEL_SERVICE"
            ),
            "bounded_timeout": (
                contracts[
                    "health_timeout_seconds"
                ]
                == 2.0
                and rehearsal[
                    "transport_timeout"
                ]
                == 2.0
            ),
            "no_redirects": (
                contracts[
                    "redirect_following"
                ]
                is False
            ),
            "proxy_disabled": (
                contracts[
                    "network_fallback"
                ]
                is False
                and rehearsal[
                    "loopback_endpoint"
                ]
                is True
            ),
            "response_bound": (
                self.contract.MAX_HEALTH_BODY_BYTES
                == 1024 * 1024
                and rehearsal[
                    "confirmed_probe_state"
                ]
                == "healthy"
            ),
            "metadata_only_models": (
                contracts[
                    "model_inventory_metadata_only"
                ]
                is True
                and rehearsal[
                    "model_names_exposed"
                ]
                is False
            ),
            "health_classification": (
                host["state"]
                in {
                    "available_unprobed",
                    "degraded_unprobed",
                    "unavailable",
                }
                and rehearsal[
                    "confirmed_probe_state"
                ]
                == "healthy"
            ),
            "failure_classification": (
                rehearsal[
                    "invalid_endpoint_rejected"
                ]
                is True
                and host["profile"]["state"]
                in {
                    "unconfigured",
                    "configured",
                    "invalid_configuration",
                }
            ),
            "no_activation": (
                host["service_started"]
                is False
                and host["service_stopped"]
                is False
                and host[
                    "service_installed"
                ]
                is False
            ),
            "no_download": (
                host["model_downloaded"]
                is False
                and host["model_loaded"]
                is False
                and host["model_unloaded"]
                is False
            ),
            "no_routing": (
                host["chat_routed"]
                is False
                and rehearsal[
                    "chat_routed"
                ]
                is False
            ),
            "safe_idle": (
                host[
                    "health_probe_performed"
                ]
                is False
                and host[
                    "network_connection_opened"
                ]
                is False
                and host["systemd_mutated"]
                is False
                and host[
                    "autostart_mutated"
                ]
                is False
            ),
            "handoff": (
                self.BOUNDARY
                == "local_model_service_discovery_health"
                and self.NEXT_BOUNDARY
                == "local_model_router_activation"
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
                "LocalModelServiceDiscoveryHealthPlanner"
            ),
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "read_only_discovery_and_explicit_loopback_health"
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
            "host_posture": (
                self.contract.host_posture()
            ),
            "health_preview": (
                self.contract.health_preview()
            ),
            "health_probe_performed": False,
            "network_connection_opened": False,
            "service_activated": False,
            "model_downloaded": False,
            "model_loaded": False,
            "chat_routed": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "canonical_owner": (
                "AuraLocalModelBridgeRuntimeManager"
            ),
            "provider": "ollama",
            "endpoint": (
                "http://127.0.0.1:11434"
            ),
            "health_path": "/api/tags",
            "health_timeout_seconds": 2.0,
            "health_probe_default": False,
            "health_confirmation_token": (
                "PROBE_LOCAL_MODEL_SERVICE"
            ),
            "model_inventory": (
                "metadata_count_only"
            ),
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
                "automatic_health_probe": True,
                "service_start_stop": True,
                "service_install": True,
                "model_download_pull": True,
                "model_load_unload": True,
                "chat_routing": True,
                "non_loopback_network": True,
                "credentials": True,
                "systemd_mutation": True,
                "autostart_mutation": True,
            },
        }

    def host_posture(self) -> dict[str, Any]:
        return self.contract.host_posture()

    def provider_contracts(
        self,
    ) -> dict[str, Any]:
        return self.contract.provider_contracts()

    def health_preview(self) -> dict[str, Any]:
        return self.contract.health_preview()

    def health_probe(
        self,
        confirmation: str,
    ) -> dict[str, Any]:
        return (
            self.contract.explicit_health_probe(
                confirmation=confirmation
            )
        )
