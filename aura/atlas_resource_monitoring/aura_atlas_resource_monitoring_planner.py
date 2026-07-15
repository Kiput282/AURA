from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from aura.resource_baseline_metrics import (
    AuraResourceBaselineMetricsAlphaManager,
)


class AuraAtlasResourceMonitoringPlanner:
    VERSION = "1.0.7-genesis"
    ANCHOR_VERSION = "1.0.6-genesis"
    CURRENT_SPRINT = 247
    NEXT_SPRINT = 248
    BOUNDARY = "atlas_resource_monitoring"
    NEXT_BOUNDARY = "localhost_ssh_tunnel_security_review"
    OWNER = "AuraAtlasResourceMonitoringPlanner"
    SOURCE_OWNER = "AuraResourceBaselineMetricsPlanner"
    CONTRACT_MODE = "read_only_health_snapshot"
    SNAPSHOT_MODE = "single_read_only"
    EXPECTED_ASSERTION_COUNT = 60
    HEALTH_LEVELS = (
        "healthy",
        "warning",
        "critical",
        "unavailable",
    )
    HEALTH_PRIORITY = {
        "healthy": 0,
        "warning": 1,
        "critical": 2,
        "unavailable": 3,
    }
    GIB = 1024**3

    THRESHOLD_POLICY = {
        "cpu_usage_percent": {
            "warning_at_or_above": 75.0,
            "critical_at_or_above": 90.0,
        },
        "load_per_logical_cpu_percent": {
            "warning_at_or_above": 75.0,
            "critical_at_or_above": 100.0,
        },
        "memory_used_percent": {
            "warning_at_or_above": 75.0,
            "critical_at_or_above": 90.0,
        },
        "swap_used_percent": {
            "warning_at_or_above": 25.0,
            "critical_at_or_above": 75.0,
        },
        "filesystem": {
            "warning_used_percent": 80.0,
            "critical_used_percent": 90.0,
            "warning_available_bytes_at_or_below": 20 * GIB,
            "critical_available_bytes_at_or_below": 10 * GIB,
        },
        "inode_used_percent": {
            "warning_at_or_above": 80.0,
            "critical_at_or_above": 90.0,
        },
        "process_count": {
            "warning_at_or_above": 1024,
            "critical_at_or_above": 2048,
        },
    }

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self._source_owner = (
            AuraResourceBaselineMetricsAlphaManager(
                project_root=self.project_root
            )
        )
        self._source_check = self._source_owner.check()
        self._source_snapshot = self._source_owner.snapshot()
        self._monitor_packet = self._build_monitor_packet()
        self._monitor_packet["monitor_digest"] = (
            self._packet_digest(self._monitor_packet)
        )

    @classmethod
    def _state_valid(cls, state: object) -> bool:
        return state in cls.HEALTH_LEVELS

    @staticmethod
    def _percentage_valid(value: object) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and 0.0 <= float(value) <= 100.0
        )

    @staticmethod
    def _timestamp_valid(value: object) -> bool:
        if not isinstance(value, str):
            return False

        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return False

        return (
            parsed.tzinfo is not None
            and parsed.utcoffset() is not None
        )

    @classmethod
    def _classify_high(
        cls,
        value: object,
        *,
        warning: float,
        critical: float,
    ) -> str:
        if not isinstance(value, (int, float)):
            return "unavailable"

        numeric = float(value)

        if numeric < 0:
            return "unavailable"

        if numeric >= critical:
            return "critical"

        if numeric >= warning:
            return "warning"

        return "healthy"

    @classmethod
    def _worst_state(
        cls,
        states: list[str] | tuple[str, ...],
    ) -> str:
        if not states:
            return "unavailable"

        return max(
            states,
            key=lambda state: cls.HEALTH_PRIORITY.get(
                state,
                cls.HEALTH_PRIORITY["unavailable"],
            ),
        )

    @classmethod
    def _cpu_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        value = snapshot["cpu"]["usage_percent"]
        policy = cls.THRESHOLD_POLICY[
            "cpu_usage_percent"
        ]
        state = cls._classify_high(
            value,
            warning=policy[
                "warning_at_or_above"
            ],
            critical=policy[
                "critical_at_or_above"
            ],
        )

        return {
            "id": "cpu",
            "state": state,
            "value_percent": value,
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": snapshot["cpu"]["source"],
        }

    @classmethod
    def _load_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        logical_count = snapshot["cpu"]["logical_count"]
        one_minute = snapshot["cpu"][
            "load_average"
        ]["one_minute"]

        if logical_count <= 0:
            normalized = None
        else:
            normalized = round(
                (one_minute / logical_count) * 100.0,
                2,
            )

        policy = cls.THRESHOLD_POLICY[
            "load_per_logical_cpu_percent"
        ]
        state = cls._classify_high(
            normalized,
            warning=policy[
                "warning_at_or_above"
            ],
            critical=policy[
                "critical_at_or_above"
            ],
        )

        return {
            "id": "load_average",
            "state": state,
            "one_minute": one_minute,
            "five_minutes": snapshot["cpu"][
                "load_average"
            ]["five_minutes"],
            "fifteen_minutes": snapshot["cpu"][
                "load_average"
            ]["fifteen_minutes"],
            "logical_cpu_count": logical_count,
            "one_minute_per_cpu_percent": normalized,
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": snapshot["cpu"]["load_source"],
        }

    @classmethod
    def _memory_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        packet = snapshot["memory"]
        policy = cls.THRESHOLD_POLICY[
            "memory_used_percent"
        ]
        state = cls._classify_high(
            packet["used_percent"],
            warning=policy[
                "warning_at_or_above"
            ],
            critical=policy[
                "critical_at_or_above"
            ],
        )

        return {
            "id": "memory",
            "state": state,
            "total_bytes": packet["total_bytes"],
            "used_bytes": packet["used_bytes"],
            "available_bytes": packet[
                "available_bytes"
            ],
            "used_percent": packet["used_percent"],
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": packet["source"],
        }

    @classmethod
    def _swap_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        packet = snapshot["swap"]
        policy = cls.THRESHOLD_POLICY[
            "swap_used_percent"
        ]
        state = cls._classify_high(
            packet["used_percent"],
            warning=policy[
                "warning_at_or_above"
            ],
            critical=policy[
                "critical_at_or_above"
            ],
        )

        return {
            "id": "swap",
            "state": state,
            "total_bytes": packet["total_bytes"],
            "used_bytes": packet["used_bytes"],
            "free_bytes": packet["free_bytes"],
            "used_percent": packet["used_percent"],
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": packet["source"],
        }

    @classmethod
    def _filesystem_state(
        cls,
        record: dict[str, Any],
    ) -> str:
        policy = cls.THRESHOLD_POLICY["filesystem"]
        used_state = cls._classify_high(
            record["used_percent"],
            warning=policy["warning_used_percent"],
            critical=policy[
                "critical_used_percent"
            ],
        )

        available = record["available_bytes"]

        if not isinstance(available, int) or available < 0:
            available_state = "unavailable"
        elif (
            available
            <= policy[
                "critical_available_bytes_at_or_below"
            ]
        ):
            available_state = "critical"
        elif (
            available
            <= policy[
                "warning_available_bytes_at_or_below"
            ]
        ):
            available_state = "warning"
        else:
            available_state = "healthy"

        return cls._worst_state(
            [used_state, available_state]
        )

    @classmethod
    def _storage_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        policy = cls.THRESHOLD_POLICY["filesystem"]
        records = []

        for source in snapshot["filesystems"]:
            record = {
                "requested_path": source[
                    "requested_path"
                ],
                "resolved_path": source[
                    "resolved_path"
                ],
                "device_id": source["device_id"],
                "state": cls._filesystem_state(
                    source
                ),
                "total_bytes": source["total_bytes"],
                "used_bytes": source["used_bytes"],
                "available_bytes": source[
                    "available_bytes"
                ],
                "used_percent": source[
                    "used_percent"
                ],
                "available_percent": source[
                    "available_percent"
                ],
            }
            records.append(record)

        return {
            "id": "storage",
            "state": cls._worst_state(
                [
                    record["state"]
                    for record in records
                ]
            ),
            "record_count": len(records),
            "records": records,
            "warning_used_percent": policy[
                "warning_used_percent"
            ],
            "critical_used_percent": policy[
                "critical_used_percent"
            ],
            "warning_available_bytes_at_or_below": (
                policy[
                    "warning_available_bytes_at_or_below"
                ]
            ),
            "critical_available_bytes_at_or_below": (
                policy[
                    "critical_available_bytes_at_or_below"
                ]
            ),
            "source": "os.statvfs",
        }

    @classmethod
    def _inode_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        policy = cls.THRESHOLD_POLICY[
            "inode_used_percent"
        ]
        records = []

        for source in snapshot["filesystems"]:
            state = cls._classify_high(
                source["inode_used_percent"],
                warning=policy[
                    "warning_at_or_above"
                ],
                critical=policy[
                    "critical_at_or_above"
                ],
            )
            records.append(
                {
                    "requested_path": source[
                        "requested_path"
                    ],
                    "state": state,
                    "inode_total": source[
                        "inode_total"
                    ],
                    "inode_used": source[
                        "inode_used"
                    ],
                    "inode_available": source[
                        "inode_available"
                    ],
                    "inode_used_percent": source[
                        "inode_used_percent"
                    ],
                }
            )

        return {
            "id": "inode_capacity",
            "state": cls._worst_state(
                [
                    record["state"]
                    for record in records
                ]
            ),
            "record_count": len(records),
            "records": records,
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": "os.statvfs",
        }

    @staticmethod
    def _uptime_dimension(
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        seconds = snapshot["uptime"]["seconds"]

        return {
            "id": "uptime",
            "state": (
                "healthy"
                if isinstance(seconds, (int, float))
                and seconds > 0
                else "unavailable"
            ),
            "seconds": seconds,
            "source": snapshot["uptime"]["source"],
        }

    @classmethod
    def _process_dimension(
        cls,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        count = snapshot["processes"]["count"]
        policy = cls.THRESHOLD_POLICY[
            "process_count"
        ]
        state = cls._classify_high(
            count,
            warning=float(
                policy["warning_at_or_above"]
            ),
            critical=float(
                policy["critical_at_or_above"]
            ),
        )

        return {
            "id": "process_count",
            "state": state,
            "count": count,
            "warning_at_or_above": policy[
                "warning_at_or_above"
            ],
            "critical_at_or_above": policy[
                "critical_at_or_above"
            ],
            "source": snapshot["processes"]["source"],
        }

    @classmethod
    def _packet_digest(
        cls,
        packet: dict[str, Any],
    ) -> str:
        canonical = json.dumps(
            packet,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(canonical).hexdigest()

    def _build_monitor_packet(self) -> dict[str, Any]:
        snapshot = self._source_snapshot
        dimensions = [
            self._cpu_dimension(snapshot),
            self._load_dimension(snapshot),
            self._memory_dimension(snapshot),
            self._swap_dimension(snapshot),
            self._storage_dimension(snapshot),
            self._inode_dimension(snapshot),
            self._uptime_dimension(snapshot),
            self._process_dimension(snapshot),
        ]
        overall_state = self._worst_state(
            [
                dimension["state"]
                for dimension in dimensions
            ]
        )
        health_counts = {
            level: sum(
                dimension["state"] == level
                for dimension in dimensions
            )
            for level in self.HEALTH_LEVELS
        }

        return {
            "owner": self.OWNER,
            "source_owner": self.SOURCE_OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "snapshot_mode": self.SNAPSHOT_MODE,
            "captured_at": snapshot["captured_at"],
            "hostname": snapshot["hostname"],
            "platform": snapshot["platform"],
            "project_root": str(self.project_root),
            "overall_state": overall_state,
            "health_levels": list(self.HEALTH_LEVELS),
            "dimension_count": len(dimensions),
            "dimensions": dimensions,
            "health_counts": health_counts,
            "threshold_policy": json.loads(
                json.dumps(self.THRESHOLD_POLICY)
            ),
            "threshold_policy_read_only": True,
            "source_contract": {
                "source_snapshot_owner": (
                    snapshot["owner"]
                ),
                "source_snapshot_version": (
                    snapshot["version"]
                ),
                "source_snapshot_digest": (
                    snapshot["snapshot_digest"]
                ),
                "source_assertion_count": (
                    self._source_check[
                        "assertion_count"
                    ]
                ),
                "source_failed_assertion_count": (
                    self._source_check[
                        "failed_assertion_count"
                    ]
                ),
                "source_alpha_ready": (
                    self._source_check["alpha_ready"]
                ),
                "source_metric_group_count": (
                    snapshot["metric_group_count"]
                ),
                "source_filesystem_record_count": (
                    len(snapshot["filesystems"])
                ),
            },
            "runtime_boundary": {
                "background_sampler_enabled": False,
                "rolling_history_enabled": False,
                "metrics_persistence_enabled": False,
                "dashboard_activation_enabled": False,
                "socket_activation_enabled": False,
                "systemd_mutation_enabled": False,
                "network_access_enabled": False,
                "process_control_enabled": False,
                "threshold_mutation_enabled": False,
                "alert_delivery_enabled": False,
                "command_execution_enabled": False,
            },
        }

    def snapshot(self) -> dict[str, Any]:
        return json.loads(
            json.dumps(self._monitor_packet)
        )

    def status(self) -> dict[str, Any]:
        packet = self._monitor_packet
        runtime = packet["runtime_boundary"]
        status_valid = all(
            (
                self._timestamp_valid(
                    packet["captured_at"]
                ),
                self._state_valid(
                    packet["overall_state"]
                ),
                packet["dimension_count"] == 8,
                sum(
                    packet["health_counts"].values()
                )
                == packet["dimension_count"],
                packet[
                    "source_contract"
                ]["source_failed_assertion_count"]
                == 0,
                packet[
                    "source_contract"
                ]["source_alpha_ready"]
                is True,
            )
        )

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "snapshot_mode": self.SNAPSHOT_MODE,
            "status_valid": status_valid,
            "alpha_ready": status_valid,
            "captured_at": packet["captured_at"],
            "overall_state": packet["overall_state"],
            "dimension_count": packet[
                "dimension_count"
            ],
            "health_counts": dict(
                packet["health_counts"]
            ),
            "monitor_digest": packet[
                "monitor_digest"
            ],
            **runtime,
        }

    def context(self) -> dict[str, Any]:
        packet = self._monitor_packet

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "health_levels": list(
                self.HEALTH_LEVELS
            ),
            "dimension_ids": [
                dimension["id"]
                for dimension in packet["dimensions"]
            ],
            "threshold_policy": json.loads(
                json.dumps(
                    packet["threshold_policy"]
                )
            ),
            "threshold_policy_read_only": True,
            "source_contract": dict(
                packet["source_contract"]
            ),
            "runtime_boundary": dict(
                packet["runtime_boundary"]
            ),
            "scope_boundary": {
                "single_snapshot_only": True,
                "pressure_metrics_deferred": True,
                "temperature_classification_deferred": True,
                "rolling_window_deferred": True,
                "dashboard_rendering_deferred": True,
                "alert_delivery_deferred": True,
            },
        }

    def check(self) -> dict[str, Any]:
        status = self.status()
        context = self.context()
        packet = self._monitor_packet
        source = packet["source_contract"]
        runtime = packet["runtime_boundary"]
        dimensions = packet["dimensions"]
        dimension_map = {
            dimension["id"]: dimension
            for dimension in dimensions
        }
        storage = dimension_map["storage"]
        inode = dimension_map["inode_capacity"]

        expected_dimension_ids = {
            "cpu",
            "load_average",
            "memory",
            "swap",
            "storage",
            "inode_capacity",
            "uptime",
            "process_count",
        }
        actual_dimension_ids = set(
            dimension_map
        )
        all_states = [
            dimension["state"]
            for dimension in dimensions
        ]

        checks = [
            ("version", status["version"] == self.VERSION),
            (
                "anchor_version",
                status["anchor_version"]
                == self.ANCHOR_VERSION,
            ),
            (
                "current_sprint",
                status["current_sprint"]
                == self.CURRENT_SPRINT,
            ),
            (
                "next_sprint",
                status["next_sprint"]
                == self.NEXT_SPRINT,
            ),
            (
                "boundary",
                status["boundary"] == self.BOUNDARY,
            ),
            (
                "next_boundary",
                status["next_boundary"]
                == self.NEXT_BOUNDARY,
            ),
            (
                "contract_mode",
                status["contract_mode"]
                == self.CONTRACT_MODE,
            ),
            (
                "snapshot_mode",
                status["snapshot_mode"]
                == self.SNAPSHOT_MODE,
            ),
            (
                "owner",
                status["owner"] == self.OWNER,
            ),
            (
                "captured_at_valid",
                self._timestamp_valid(
                    status["captured_at"]
                ),
            ),
            (
                "status_valid",
                status["status_valid"] is True,
            ),
            (
                "alpha_ready",
                status["alpha_ready"] is True,
            ),
            (
                "health_levels_exact",
                tuple(context["health_levels"])
                == self.HEALTH_LEVELS,
            ),
            (
                "overall_state_valid",
                self._state_valid(
                    status["overall_state"]
                ),
            ),
            (
                "dimension_count",
                status["dimension_count"] == 8,
            ),
            (
                "source_owner",
                source["source_snapshot_owner"]
                == self.SOURCE_OWNER,
            ),
            (
                "source_version",
                source["source_snapshot_version"]
                == self.ANCHOR_VERSION,
            ),
            (
                "source_assertion_count",
                source["source_assertion_count"]
                == 50,
            ),
            (
                "source_failed_assertion_count",
                source[
                    "source_failed_assertion_count"
                ]
                == 0,
            ),
            (
                "source_alpha_ready",
                source["source_alpha_ready"] is True,
            ),
            (
                "source_metric_group_count",
                source[
                    "source_metric_group_count"
                ]
                == 7,
            ),
            (
                "source_filesystem_record_count",
                source[
                    "source_filesystem_record_count"
                ]
                == 4,
            ),
            (
                "threshold_policy_read_only",
                packet["threshold_policy_read_only"]
                is True,
            ),
            (
                "threshold_mutation_disabled",
                runtime["threshold_mutation_enabled"]
                is False,
            ),
            (
                "background_sampler_disabled",
                runtime["background_sampler_enabled"]
                is False,
            ),
            (
                "rolling_history_disabled",
                runtime["rolling_history_enabled"]
                is False,
            ),
            (
                "metrics_persistence_disabled",
                runtime["metrics_persistence_enabled"]
                is False,
            ),
            (
                "dashboard_activation_disabled",
                runtime["dashboard_activation_enabled"]
                is False,
            ),
            (
                "socket_activation_disabled",
                runtime["socket_activation_enabled"]
                is False,
            ),
            (
                "systemd_mutation_disabled",
                runtime["systemd_mutation_enabled"]
                is False,
            ),
            (
                "network_access_disabled",
                runtime["network_access_enabled"]
                is False,
            ),
            (
                "process_control_disabled",
                runtime["process_control_enabled"]
                is False,
            ),
            (
                "alert_delivery_disabled",
                runtime["alert_delivery_enabled"]
                is False,
            ),
            (
                "command_execution_disabled",
                runtime["command_execution_enabled"]
                is False,
            ),
            (
                "cpu_dimension_present",
                "cpu" in dimension_map,
            ),
            (
                "cpu_state_valid",
                self._state_valid(
                    dimension_map["cpu"]["state"]
                ),
            ),
            (
                "cpu_percentage_valid",
                self._percentage_valid(
                    dimension_map[
                        "cpu"
                    ]["value_percent"]
                ),
            ),
            (
                "load_state_valid",
                self._state_valid(
                    dimension_map[
                        "load_average"
                    ]["state"]
                ),
            ),
            (
                "load_normalized_valid",
                (
                    dimension_map[
                        "load_average"
                    ][
                        "one_minute_per_cpu_percent"
                    ]
                    is not None
                    and dimension_map[
                        "load_average"
                    ][
                        "one_minute_per_cpu_percent"
                    ]
                    >= 0
                ),
            ),
            (
                "memory_dimension_present",
                "memory" in dimension_map,
            ),
            (
                "memory_state_valid",
                self._state_valid(
                    dimension_map[
                        "memory"
                    ]["state"]
                ),
            ),
            (
                "memory_percentage_valid",
                self._percentage_valid(
                    dimension_map[
                        "memory"
                    ]["used_percent"]
                ),
            ),
            (
                "swap_state_valid",
                self._state_valid(
                    dimension_map["swap"]["state"]
                ),
            ),
            (
                "swap_percentage_valid",
                self._percentage_valid(
                    dimension_map[
                        "swap"
                    ]["used_percent"]
                ),
            ),
            (
                "storage_record_count",
                storage["record_count"] == 4,
            ),
            (
                "storage_states_valid",
                all(
                    self._state_valid(
                        record["state"]
                    )
                    for record in storage["records"]
                ),
            ),
            (
                "storage_percentages_valid",
                all(
                    self._percentage_valid(
                        record["used_percent"]
                    )
                    and self._percentage_valid(
                        record[
                            "available_percent"
                        ]
                    )
                    for record in storage["records"]
                ),
            ),
            (
                "storage_available_nonnegative",
                all(
                    record["available_bytes"] >= 0
                    for record in storage["records"]
                ),
            ),
            (
                "inode_record_count",
                inode["record_count"] == 4,
            ),
            (
                "inode_states_valid",
                all(
                    self._state_valid(
                        record["state"]
                    )
                    for record in inode["records"]
                ),
            ),
            (
                "inode_percentages_valid",
                all(
                    self._percentage_valid(
                        record[
                            "inode_used_percent"
                        ]
                    )
                    for record in inode["records"]
                ),
            ),
            (
                "uptime_state_healthy",
                dimension_map[
                    "uptime"
                ]["state"]
                == "healthy",
            ),
            (
                "uptime_positive",
                dimension_map[
                    "uptime"
                ]["seconds"]
                > 0,
            ),
            (
                "process_state_valid",
                self._state_valid(
                    dimension_map[
                        "process_count"
                    ]["state"]
                ),
            ),
            (
                "process_count_positive",
                dimension_map[
                    "process_count"
                ]["count"]
                > 0,
            ),
            (
                "overall_equals_worst_dimension",
                packet["overall_state"]
                == self._worst_state(all_states),
            ),
            (
                "health_count_total",
                sum(packet["health_counts"].values())
                == packet["dimension_count"],
            ),
            (
                "dimension_ids_exact",
                actual_dimension_ids
                == expected_dimension_ids,
            ),
            (
                "monitor_digest_present",
                len(packet["monitor_digest"]) == 64,
            ),
            (
                "threshold_policy_group_count",
                len(packet["threshold_policy"]) == 7,
            ),
        ]

        failed = [
            name
            for name, passed in checks
            if not passed
        ]

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "snapshot_mode": self.SNAPSHOT_MODE,
            "base_check_count": len(checks),
            "assertion_count": len(checks),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "status_valid": status["status_valid"],
            "alpha_ready": (
                len(checks)
                == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "overall_state": packet["overall_state"],
            "health_counts": dict(
                packet["health_counts"]
            ),
            "dimension_count": packet[
                "dimension_count"
            ],
            "monitor_digest": packet[
                "monitor_digest"
            ],
            "threshold_policy_read_only": (
                packet["threshold_policy_read_only"]
            ),
            **runtime,
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in checks
            ],
        }
