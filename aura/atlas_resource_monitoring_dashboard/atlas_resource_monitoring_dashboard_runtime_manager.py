"""Read-only ATLAS resource dashboard runtime for Sprint 267."""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any, Callable
import math
import time

from aura.atlas_resource_monitoring.aura_atlas_resource_monitoring_alpha_manager import (
    AuraAtlasResourceMonitoringAlphaManager,
)
from aura.resource_baseline_metrics.aura_resource_baseline_metrics_alpha_manager import (
    AuraResourceBaselineMetricsAlphaManager,
)


class AtlasResourceMonitoringDashboardError(
    RuntimeError
):
    """Sprint 267 resource dashboard runtime error."""


class AtlasResourceMonitoringDashboardRuntimeManager:
    VERSION = "1.2.7"
    ANCHOR_VERSION = "1.2.6"
    CURRENT_SPRINT = 267
    BOUNDARY = "atlas_resource_monitoring_dashboard"

    SAMPLE_INTERVAL_SECONDS = 1.0
    UI_REFRESH_SECONDS = 1
    HISTORY_MAX_SECONDS = 60 * 60
    HISTORY_WINDOWS_MINUTES = (5, 15, 60)
    MOUNT_POINTS = (
        "/",
        "/home",
        "/mnt/aura-data",
    )

    _shared_lock = RLock()
    _shared_history: deque[dict[str, Any]] = deque(
        maxlen=HISTORY_MAX_SECONDS + 5
    )
    _shared_last_sample_monotonic: float | None = None

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        baseline_manager: Any | None = None,
        monitor_manager: Any | None = None,
        monotonic: Callable[[], float] | None = None,
        wall_clock: Callable[[], float] | None = None,
        history: deque[dict[str, Any]] | None = None,
        lock: RLock | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()
        self._baseline_manager_injected = (
            baseline_manager is not None
        )
        self._monitor_manager_injected = (
            monitor_manager is not None
        )
        self._baseline = baseline_manager or (
            AuraResourceBaselineMetricsAlphaManager(
                project_root=self.project_root
            )
        )
        self._monitor = monitor_manager or (
            AuraAtlasResourceMonitoringAlphaManager(
                project_root=self.project_root
            )
        )
        self._monotonic = monotonic or time.monotonic
        self._wall_clock = wall_clock or time.time
        self._history = (
            history
            if history is not None
            else self.__class__._shared_history
        )
        self._lock = (
            lock
            if lock is not None
            else self.__class__._shared_lock
        )
        self._uses_shared_history = history is None

    @staticmethod
    def _finite_number(
        value: Any,
        default: float = 0.0,
    ) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return default
        return (
            number
            if math.isfinite(number)
            else default
        )

    @classmethod
    def _percent(cls, value: Any) -> float:
        return max(
            0.0,
            min(
                100.0,
                round(
                    cls._finite_number(value),
                    3,
                ),
            ),
        )

    @staticmethod
    def _integer(
        value: Any,
        default: int = 0,
    ) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _state_color(state: Any) -> str:
        normalized = str(
            state or "unknown"
        ).strip().lower()
        if normalized in {
            "healthy",
            "ok",
            "ready",
            "normal",
            "green",
        }:
            return "green"
        if normalized in {
            "warning",
            "warn",
            "degraded",
            "yellow",
        }:
            return "yellow"
        if normalized in {
            "critical",
            "error",
            "failed",
            "red",
        }:
            return "red"
        return "gray"

    @staticmethod
    def _dimensions_by_id(
        monitor: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        dimensions = monitor.get(
            "dimensions",
            [],
        )
        if not isinstance(dimensions, list):
            return {}

        result: dict[str, dict[str, Any]] = {}
        for item in dimensions:
            if not isinstance(item, dict):
                continue
            identifier = str(
                item.get("id")
                or item.get("dimension")
                or item.get("name")
                or ""
            ).strip()
            if identifier:
                result[identifier] = item
        return result

    @classmethod
    def _metric_state(
        cls,
        dimensions: dict[str, dict[str, Any]],
        identifier: str,
    ) -> dict[str, str]:
        raw = dimensions.get(identifier, {})
        state = str(
            raw.get("state", "unknown")
        )
        return {
            "state": state,
            "color": cls._state_color(state),
        }

    @classmethod
    def _storage_states(
        cls,
        dimensions: dict[str, dict[str, Any]],
    ) -> dict[str, dict[str, str]]:
        storage = dimensions.get(
            "storage",
            {},
        )
        records = storage.get(
            "records",
            [],
        )
        result: dict[str, dict[str, str]] = {}

        if isinstance(records, list):
            for record in records:
                if not isinstance(record, dict):
                    continue
                requested = str(
                    record.get("requested_path")
                    or record.get("path")
                    or record.get("mount_point")
                    or ""
                )
                if requested:
                    state = str(
                        record.get(
                            "state",
                            storage.get(
                                "state",
                                "unknown",
                            ),
                        )
                    )
                    result[requested] = {
                        "state": state,
                        "color": cls._state_color(
                            state
                        ),
                    }

        fallback_state = str(
            storage.get(
                "state",
                "unknown",
            )
        )
        fallback = {
            "state": fallback_state,
            "color": cls._state_color(
                fallback_state
            ),
        }
        for mount in cls.MOUNT_POINTS:
            result.setdefault(
                mount,
                fallback,
            )
        return result

    @classmethod
    def _storage_records(
        cls,
        baseline: dict[str, Any],
        dimensions: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        raw_records = baseline.get(
            "filesystems",
            [],
        )
        by_requested: dict[str, dict[str, Any]] = {}

        if isinstance(raw_records, list):
            for record in raw_records:
                if not isinstance(record, dict):
                    continue
                requested = str(
                    record.get(
                        "requested_path",
                        "",
                    )
                )
                if requested:
                    by_requested[requested] = record

        states = cls._storage_states(
            dimensions
        )
        output = []

        for mount in cls.MOUNT_POINTS:
            raw = by_requested.get(
                mount,
                {},
            )
            state = states[mount]
            exists = bool(
                raw.get("exists", False)
            )
            total = cls._integer(
                raw.get("total_bytes")
            )
            used = cls._integer(
                raw.get("used_bytes")
            )
            available = cls._integer(
                raw.get("available_bytes")
            )
            output.append({
                "mount_point": mount,
                "requested_path": mount,
                "exists": exists,
                "total_bytes": total,
                "used_bytes": used,
                "free_bytes": available,
                "available_bytes": available,
                "used_percent": cls._percent(
                    raw.get("used_percent")
                ),
                "free_percent": cls._percent(
                    raw.get(
                        "available_percent"
                    )
                ),
                "inode_used_percent": cls._percent(
                    raw.get(
                        "inode_used_percent"
                    )
                ),
                "state": state["state"],
                "color": state["color"],
            })

        return output

    def _collect_raw(
        self,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
    ]:
        baseline_manager = self._baseline
        if not self._baseline_manager_injected:
            baseline_manager = (
                AuraResourceBaselineMetricsAlphaManager(
                    project_root=self.project_root
                )
            )

        monitor_manager = self._monitor
        if not self._monitor_manager_injected:
            monitor_manager = (
                AuraAtlasResourceMonitoringAlphaManager(
                    project_root=self.project_root
                )
            )

        baseline = baseline_manager.snapshot()
        monitor = monitor_manager.snapshot()

        if not isinstance(baseline, dict):
            raise AtlasResourceMonitoringDashboardError(
                "Baseline snapshot must be a mapping."
            )
        if not isinstance(monitor, dict):
            raise AtlasResourceMonitoringDashboardError(
                "Monitor snapshot must be a mapping."
            )
        return baseline, monitor

    def _build_sample(
        self,
        baseline: dict[str, Any],
        monitor: dict[str, Any],
        *,
        monotonic_value: float,
        wall_clock_value: float,
    ) -> dict[str, Any]:
        dimensions = self._dimensions_by_id(
            monitor
        )
        cpu = baseline.get("cpu", {})
        memory = baseline.get(
            "memory",
            {},
        )
        swap = baseline.get("swap", {})
        uptime = baseline.get(
            "uptime",
            {},
        )
        processes = baseline.get(
            "processes",
            {},
        )

        if not isinstance(cpu, dict):
            cpu = {}
        if not isinstance(memory, dict):
            memory = {}
        if not isinstance(swap, dict):
            swap = {}
        if not isinstance(uptime, dict):
            uptime = {}
        if not isinstance(processes, dict):
            processes = {}

        captured_at = datetime.fromtimestamp(
            wall_clock_value,
            tz=timezone.utc,
        ).isoformat()

        return {
            "captured_at": captured_at,
            "monotonic_seconds": round(
                monotonic_value,
                6,
            ),
            "cpu": {
                "usage_percent": self._percent(
                    cpu.get("usage_percent")
                ),
                "logical_count": self._integer(
                    cpu.get("logical_count"),
                    default=1,
                ),
                **self._metric_state(
                    dimensions,
                    "cpu",
                ),
            },
            "memory": {
                "total_bytes": self._integer(
                    memory.get("total_bytes")
                ),
                "used_bytes": self._integer(
                    memory.get("used_bytes")
                ),
                "available_bytes": self._integer(
                    memory.get(
                        "available_bytes"
                    )
                ),
                "used_percent": self._percent(
                    memory.get(
                        "used_percent"
                    )
                ),
                "available_percent": self._percent(
                    memory.get(
                        "available_percent"
                    )
                ),
                **self._metric_state(
                    dimensions,
                    "memory",
                ),
            },
            "swap": {
                "total_bytes": self._integer(
                    swap.get("total_bytes")
                ),
                "used_bytes": self._integer(
                    swap.get("used_bytes")
                ),
                "free_bytes": self._integer(
                    swap.get("free_bytes")
                ),
                "used_percent": self._percent(
                    swap.get(
                        "used_percent"
                    )
                ),
                "free_percent": self._percent(
                    swap.get(
                        "free_percent"
                    )
                ),
                **self._metric_state(
                    dimensions,
                    "swap",
                ),
            },
            "uptime": {
                "seconds": round(
                    self._finite_number(
                        uptime.get("seconds")
                    ),
                    3,
                ),
                **self._metric_state(
                    dimensions,
                    "uptime",
                ),
            },
            "processes": {
                "count": self._integer(
                    processes.get("count")
                ),
                **self._metric_state(
                    dimensions,
                    "process_count",
                ),
            },
            "storage": self._storage_records(
                baseline,
                dimensions,
            ),
            "overall_state": str(
                monitor.get(
                    "overall_state",
                    "unknown",
                )
            ),
            "overall_color": self._state_color(
                monitor.get(
                    "overall_state",
                    "unknown",
                )
            ),
        }

    def _sample_due(
        self,
        monotonic_value: float,
    ) -> bool:
        if not self._history:
            return True
        last_value = self._finite_number(
            self._history[-1].get(
                "monotonic_seconds"
            ),
            default=-1.0,
        )
        return (
            monotonic_value - last_value
            >= self.SAMPLE_INTERVAL_SECONDS
        )

    def collect(
        self,
        *,
        force: bool = False,
    ) -> dict[str, Any]:
        with self._lock:
            monotonic_value = float(
                self._monotonic()
            )
            if (
                not force
                and not self._sample_due(
                    monotonic_value
                )
            ):
                return deepcopy(
                    self._history[-1]
                )

            baseline, monitor = self._collect_raw()
            sample = self._build_sample(
                baseline,
                monitor,
                monotonic_value=monotonic_value,
                wall_clock_value=float(
                    self._wall_clock()
                ),
            )
            self._history.append(sample)

            if self._uses_shared_history:
                self.__class__._shared_last_sample_monotonic = (
                    monotonic_value
                )

            return deepcopy(sample)

    @classmethod
    def _series_stats(
        cls,
        values: list[float],
    ) -> dict[str, float]:
        if not values:
            return {
                "minimum": 0.0,
                "average": 0.0,
                "maximum": 0.0,
            }
        return {
            "minimum": round(
                min(values),
                3,
            ),
            "average": round(
                sum(values) / len(values),
                3,
            ),
            "maximum": round(
                max(values),
                3,
            ),
        }

    def _history_window(
        self,
        *,
        minutes: int,
        current_monotonic: float,
    ) -> dict[str, Any]:
        cutoff = (
            current_monotonic
            - minutes * 60
        )
        samples = [
            item
            for item in self._history
            if self._finite_number(
                item.get(
                    "monotonic_seconds"
                )
            )
            >= cutoff
        ]

        cpu_values = [
            self._percent(
                item["cpu"]["usage_percent"]
            )
            for item in samples
        ]
        memory_values = [
            self._percent(
                item["memory"]["used_percent"]
            )
            for item in samples
        ]

        return {
            "minutes": minutes,
            "sample_count": len(samples),
            "cpu": {
                "stats": self._series_stats(
                    cpu_values
                ),
                "series": [
                    {
                        "captured_at": item[
                            "captured_at"
                        ],
                        "value_percent": value,
                    }
                    for item, value in zip(
                        samples,
                        cpu_values,
                    )
                ],
            },
            "memory": {
                "stats": self._series_stats(
                    memory_values
                ),
                "series": [
                    {
                        "captured_at": item[
                            "captured_at"
                        ],
                        "value_percent": value,
                    }
                    for item, value in zip(
                        samples,
                        memory_values,
                    )
                ],
            },
        }

    def snapshot(
        self,
    ) -> dict[str, Any]:
        current = self.collect()
        current_monotonic = self._finite_number(
            current.get(
                "monotonic_seconds"
            )
        )

        with self._lock:
            windows = {
                str(minutes): self._history_window(
                    minutes=minutes,
                    current_monotonic=(
                        current_monotonic
                    ),
                )
                for minutes
                in self.HISTORY_WINDOWS_MINUTES
            }
            history_count = len(
                self._history
            )

        threshold_policy = (
            self._monitor.snapshot().get(
                "threshold_policy",
                {},
            )
        )
        if not isinstance(
            threshold_policy,
            dict,
        ):
            threshold_policy = {}

        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "owner": (
                "atlas_resource_monitoring_dashboard"
            ),
            "source_owners": [
                "resource_baseline_metrics",
                "atlas_resource_monitoring",
            ],
            "captured_at": current[
                "captured_at"
            ],
            "current": current,
            "history": windows,
            "history_sample_count": history_count,
            "history_max_samples": (
                self.HISTORY_MAX_SECONDS + 5
            ),
            "sample_interval_seconds": (
                self.SAMPLE_INTERVAL_SECONDS
            ),
            "ui_refresh_seconds": (
                self.UI_REFRESH_SECONDS
            ),
            "rolling_windows_minutes": list(
                self.HISTORY_WINDOWS_MINUTES
            ),
            "mount_points": list(
                self.MOUNT_POINTS
            ),
            "threshold_policy": deepcopy(
                threshold_policy
            ),
            "threshold_policy_read_only": True,
            "sample_on_read": True,
            "background_sampler_enabled": False,
            "history_persistence_enabled": False,
            "network_access_enabled": False,
            "process_control_enabled": False,
            "command_execution_enabled": False,
            "systemd_mutation_enabled": False,
            "threshold_mutation_enabled": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        snapshot = self.snapshot()
        current = snapshot["current"]
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "status": (
                "ready"
                if current["overall_color"]
                in {"green", "yellow", "red"}
                else "degraded"
            ),
            "overall_state": current[
                "overall_state"
            ],
            "overall_color": current[
                "overall_color"
            ],
            "history_sample_count": snapshot[
                "history_sample_count"
            ],
            "mount_count": len(
                current["storage"]
            ),
            "sample_interval_seconds": (
                self.SAMPLE_INTERVAL_SECONDS
            ),
            "ui_refresh_seconds": (
                self.UI_REFRESH_SECONDS
            ),
            "read_only": True,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def self_test(
        self,
    ) -> dict[str, Any]:
        class FakeBaseline:
            def __init__(self) -> None:
                self.value = 0

            def snapshot(
                self,
            ) -> dict[str, Any]:
                self.value += 1
                usage = float(
                    self.value * 10
                )
                return {
                    "cpu": {
                        "usage_percent": usage,
                        "logical_count": 8,
                    },
                    "memory": {
                        "total_bytes": 1000,
                        "used_bytes": int(
                            usage * 10
                        ),
                        "available_bytes": int(
                            1000 - usage * 10
                        ),
                        "used_percent": usage,
                        "available_percent": (
                            100.0 - usage
                        ),
                    },
                    "swap": {
                        "total_bytes": 500,
                        "used_bytes": 50,
                        "free_bytes": 450,
                        "used_percent": 10.0,
                        "free_percent": 90.0,
                    },
                    "uptime": {
                        "seconds": 123.0,
                    },
                    "processes": {
                        "count": 42,
                    },
                    "filesystems": [
                        {
                            "requested_path": mount,
                            "exists": True,
                            "total_bytes": 1000,
                            "used_bytes": 500,
                            "available_bytes": 500,
                            "used_percent": 50.0,
                            "available_percent": 50.0,
                            "inode_used_percent": 25.0,
                        }
                        for mount in self_mounts
                    ],
                }

        class FakeMonitor:
            def snapshot(
                self,
            ) -> dict[str, Any]:
                return {
                    "overall_state": "healthy",
                    "dimensions": [
                        {
                            "id": "cpu",
                            "state": "healthy",
                        },
                        {
                            "id": "memory",
                            "state": "warning",
                        },
                        {
                            "id": "swap",
                            "state": "healthy",
                        },
                        {
                            "id": "uptime",
                            "state": "healthy",
                        },
                        {
                            "id": "process_count",
                            "state": "critical",
                        },
                        {
                            "id": "storage",
                            "state": "healthy",
                            "records": [
                                {
                                    "requested_path": mount,
                                    "state": "healthy",
                                }
                                for mount
                                in self_mounts
                            ],
                        },
                    ],
                    "threshold_policy": {
                        "cpu_usage_percent": {
                            "warning": 80,
                            "critical": 95,
                        },
                    },
                }

        self_mounts = self.MOUNT_POINTS
        monotonic_values = iter(
            (
                0.0,
                0.5,
                1.0,
                2.0,
                3.0,
            )
        )
        wall_values = iter(
            (
                1000.0,
                1000.5,
                1001.0,
                1002.0,
                1003.0,
            )
        )
        history: deque[
            dict[str, Any]
        ] = deque(maxlen=3605)

        manager = self.__class__(
            project_root=self.project_root,
            baseline_manager=FakeBaseline(),
            monitor_manager=FakeMonitor(),
            monotonic=lambda: next(
                monotonic_values
            ),
            wall_clock=lambda: next(
                wall_values
            ),
            history=history,
            lock=RLock(),
        )

        first = manager.collect()
        reused = manager.collect()
        second = manager.collect()
        snapshot = manager.snapshot()
        status = manager.status()

        assertions = {
            "first_cpu_ten": (
                first["cpu"]["usage_percent"]
                == 10.0
            ),
            "reused_same_sample": (
                reused["captured_at"]
                == first["captured_at"]
            ),
            "second_cpu_twenty": (
                second["cpu"]["usage_percent"]
                == 20.0
            ),
            "history_count_three": (
                snapshot["history_sample_count"]
                == 3
            ),
            "cpu_current_thirty": (
                snapshot["current"]["cpu"][
                    "usage_percent"
                ]
                == 30.0
            ),
            "memory_current_thirty": (
                snapshot["current"]["memory"][
                    "used_percent"
                ]
                == 30.0
            ),
            "memory_warning_yellow": (
                snapshot["current"]["memory"][
                    "color"
                ]
                == "yellow"
            ),
            "process_critical_red": (
                snapshot["current"]["processes"][
                    "color"
                ]
                == "red"
            ),
            "overall_green": (
                snapshot["current"][
                    "overall_color"
                ]
                == "green"
            ),
            "mount_count_three": (
                len(
                    snapshot["current"][
                        "storage"
                    ]
                )
                == 3
            ),
            "mount_order": (
                [
                    item["mount_point"]
                    for item in snapshot[
                        "current"
                    ]["storage"]
                ]
                == list(self.MOUNT_POINTS)
            ),
            "storage_fields": all(
                {
                    "mount_point",
                    "used_bytes",
                    "free_bytes",
                    "total_bytes",
                    "used_percent",
                    "state",
                    "color",
                }.issubset(item)
                for item in snapshot[
                    "current"
                ]["storage"]
            ),
            "window_keys": (
                sorted(
                    snapshot["history"]
                )
                == ["15", "5", "60"]
            ),
            "five_minute_samples_three": (
                snapshot["history"]["5"][
                    "sample_count"
                ]
                == 3
            ),
            "cpu_stats": (
                snapshot["history"]["5"][
                    "cpu"
                ]["stats"]
                == {
                    "minimum": 10.0,
                    "average": 20.0,
                    "maximum": 30.0,
                }
            ),
            "memory_stats": (
                snapshot["history"]["5"][
                    "memory"
                ]["stats"]
                == {
                    "minimum": 10.0,
                    "average": 20.0,
                    "maximum": 30.0,
                }
            ),
            "cpu_series_three": (
                len(
                    snapshot["history"]["5"][
                        "cpu"
                    ]["series"]
                )
                == 3
            ),
            "memory_series_three": (
                len(
                    snapshot["history"]["5"][
                        "memory"
                    ]["series"]
                )
                == 3
            ),
            "sample_interval_one": (
                snapshot[
                    "sample_interval_seconds"
                ]
                == 1.0
            ),
            "ui_refresh_one": (
                snapshot["ui_refresh_seconds"]
                == 1
            ),
            "rolling_windows": (
                snapshot[
                    "rolling_windows_minutes"
                ]
                == [5, 15, 60]
            ),
            "threshold_read_only": (
                snapshot[
                    "threshold_policy_read_only"
                ]
                is True
            ),
            "threshold_present": (
                "cpu_usage_percent"
                in snapshot["threshold_policy"]
            ),
            "sample_on_read": (
                snapshot["sample_on_read"]
                is True
            ),
            "background_sampler_disabled": (
                snapshot[
                    "background_sampler_enabled"
                ]
                is False
            ),
            "history_not_persisted": (
                snapshot[
                    "history_persistence_enabled"
                ]
                is False
            ),
            "network_disabled": (
                snapshot[
                    "network_access_enabled"
                ]
                is False
            ),
            "process_control_disabled": (
                snapshot[
                    "process_control_enabled"
                ]
                is False
            ),
            "command_execution_disabled": (
                snapshot[
                    "command_execution_enabled"
                ]
                is False
            ),
            "systemd_mutation_disabled": (
                snapshot[
                    "systemd_mutation_enabled"
                ]
                is False
            ),
            "threshold_mutation_disabled": (
                snapshot[
                    "threshold_mutation_enabled"
                ]
                is False
            ),
            "no_execution_authority": (
                snapshot[
                    "new_execution_authority"
                ]
                is False
            ),
            "runtime_not_mutated": (
                snapshot["runtime_mutated"]
                is False
            ),
            "read_only": (
                snapshot["read_only"]
                is True
            ),
            "safe_idle": (
                snapshot["safe_idle"]
                is True
            ),
            "status_ready": (
                status["status"]
                == "ready"
            ),
            "status_mount_count_three": (
                status["mount_count"]
                == 3
            ),
            "status_additional_sample": (
                status["history_sample_count"]
                == 4
            ),
            "status_read_only": (
                status["read_only"]
                is True
            ),
            "status_safe_idle": (
                status["safe_idle"]
                is True
            ),
            "owner": (
                snapshot["owner"]
                == "atlas_resource_monitoring_dashboard"
            ),
            "boundary": (
                snapshot["boundary"]
                == self.BOUNDARY
            ),
            "version": (
                snapshot["version"]
                == "1.2.7"
            ),
            "current_sprint": (
                snapshot["current_sprint"]
                == 267
            ),
            "source_owners": (
                snapshot["source_owners"]
                == [
                    "resource_baseline_metrics",
                    "atlas_resource_monitoring",
                ]
            ),
            "history_capacity": (
                snapshot[
                    "history_max_samples"
                ]
                == 3605
            ),
            "uptime_value": (
                snapshot["current"]["uptime"][
                    "seconds"
                ]
                == 123.0
            ),
            "process_value": (
                snapshot["current"][
                    "processes"
                ]["count"]
                == 42
            ),
            "swap_value": (
                snapshot["current"]["swap"][
                    "used_percent"
                ]
                == 10.0
            ),
        }

        failed = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]
        if failed:
            raise AtlasResourceMonitoringDashboardError(
                "Sprint 267 resource dashboard self-test "
                "failed: "
                + ", ".join(failed)
            )

        return {
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "failed_assertions": [],
            "status_valid": True,
            "runtime_ready": True,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }
