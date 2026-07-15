from __future__ import annotations

import hashlib
import json
import os
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuraResourceBaselineMetricsPlanner:
    VERSION = "1.0.6-genesis"
    ANCHOR_VERSION = "1.0.5-genesis"
    CURRENT_SPRINT = 246
    NEXT_SPRINT = 247
    BOUNDARY = "resource_baseline_metrics"
    NEXT_BOUNDARY = "atlas_resource_monitoring"
    OWNER = "AuraResourceBaselineMetricsPlanner"
    CONTRACT_MODE = "read_only_snapshot"
    SNAPSHOT_MODE = "single_read_only"
    CPU_SAMPLE_INTERVAL_SECONDS = 0.10
    EXPECTED_ASSERTION_COUNT = 50

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.inspection_time = datetime.now(timezone.utc)
        collection_started = time.monotonic()
        self._snapshot_packet = self._collect_snapshot()
        collection_finished = time.monotonic()
        self._snapshot_packet["collection_duration_ms"] = round(
            (collection_finished - collection_started) * 1000.0,
            3,
        )
        self._snapshot_packet["snapshot_digest"] = (
            self._snapshot_digest(self._snapshot_packet)
        )

    @staticmethod
    def _percentage(
        numerator: int | float,
        denominator: int | float,
    ) -> float:
        if denominator <= 0:
            return 0.0

        return round(
            (float(numerator) / float(denominator)) * 100.0,
            2,
        )

    @staticmethod
    def _read_text(path: Path) -> str:
        return path.read_text(
            encoding="utf-8",
            errors="strict",
        )

    @classmethod
    def _read_key_value_file(
        cls,
        path: Path,
    ) -> dict[str, str]:
        packet: dict[str, str] = {}

        for line in cls._read_text(path).splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            packet[key.strip()] = value.strip()

        return packet

    @staticmethod
    def _kibibyte_value(value: str) -> int:
        fields = value.split()

        if not fields:
            return 0

        number = int(fields[0])
        unit = (
            fields[1].lower()
            if len(fields) > 1
            else ""
        )

        if unit == "kb":
            return number * 1024

        return number

    @classmethod
    def _memory_packet(cls) -> dict[str, Any]:
        source = Path("/proc/meminfo")
        values = cls._read_key_value_file(source)

        total = cls._kibibyte_value(
            values.get("MemTotal", "0 kB")
        )

        available = cls._kibibyte_value(
            values.get("MemAvailable", "0 kB")
        )

        if available <= 0:
            available = sum(
                cls._kibibyte_value(
                    values.get(key, "0 kB")
                )
                for key in (
                    "MemFree",
                    "Buffers",
                    "Cached",
                )
            )

        available = min(
            max(0, available),
            total,
        )
        used = max(0, total - available)

        return {
            "source": str(source),
            "total_bytes": total,
            "used_bytes": used,
            "available_bytes": available,
            "used_percent": cls._percentage(
                used,
                total,
            ),
            "available_percent": cls._percentage(
                available,
                total,
            ),
        }

    @classmethod
    def _swap_packet(cls) -> dict[str, Any]:
        source = Path("/proc/meminfo")
        values = cls._read_key_value_file(source)

        total = cls._kibibyte_value(
            values.get("SwapTotal", "0 kB")
        )
        free = cls._kibibyte_value(
            values.get("SwapFree", "0 kB")
        )
        free = min(max(0, free), total)
        used = max(0, total - free)

        return {
            "source": str(source),
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "used_percent": cls._percentage(
                used,
                total,
            ),
            "free_percent": cls._percentage(
                free,
                total,
            ),
        }

    @classmethod
    def _read_cpu_times(cls) -> tuple[int, int]:
        source = Path("/proc/stat")
        first_line = cls._read_text(
            source
        ).splitlines()[0]
        fields = [
            int(value)
            for value in first_line.split()[1:]
        ]

        idle = fields[3]

        if len(fields) > 4:
            idle += fields[4]

        return sum(fields), idle

    @classmethod
    def _cpu_model(cls) -> str:
        source = Path("/proc/cpuinfo")

        for line in cls._read_text(source).splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()

        return "UNKNOWN"

    @classmethod
    def _cpu_packet(cls) -> dict[str, Any]:
        before_total, before_idle = (
            cls._read_cpu_times()
        )
        sample_started = time.monotonic()
        time.sleep(cls.CPU_SAMPLE_INTERVAL_SECONDS)
        after_total, after_idle = (
            cls._read_cpu_times()
        )
        sample_elapsed = (
            time.monotonic() - sample_started
        )

        delta_total = after_total - before_total
        delta_idle = after_idle - before_idle

        if delta_total <= 0:
            usage_percent = 0.0
        else:
            busy = max(
                0,
                delta_total - delta_idle,
            )
            usage_percent = round(
                (busy / delta_total) * 100.0,
                2,
            )

        load_one, load_five, load_fifteen = (
            os.getloadavg()
        )

        return {
            "source": "/proc/stat",
            "model_source": "/proc/cpuinfo",
            "load_source": "os.getloadavg",
            "logical_count": os.cpu_count() or 0,
            "model": cls._cpu_model(),
            "sample_interval_seconds": round(
                sample_elapsed,
                4,
            ),
            "usage_percent": usage_percent,
            "load_average": {
                "one_minute": round(load_one, 4),
                "five_minutes": round(load_five, 4),
                "fifteen_minutes": round(
                    load_fifteen,
                    4,
                ),
            },
        }

    @classmethod
    def _uptime_packet(cls) -> dict[str, Any]:
        source = Path("/proc/uptime")
        uptime_seconds = float(
            cls._read_text(source).split()[0]
        )

        return {
            "source": str(source),
            "seconds": round(
                uptime_seconds,
                3,
            ),
        }

    @staticmethod
    def _process_packet() -> dict[str, Any]:
        source = Path("/proc")
        count = sum(
            1
            for entry in source.iterdir()
            if entry.name.isdigit()
        )

        return {
            "source": str(source),
            "count": count,
        }

    @classmethod
    def _filesystem_packet(
        cls,
        requested_path: Path,
    ) -> dict[str, Any]:
        resolved = requested_path.resolve()
        stat_result = resolved.stat()
        values = os.statvfs(resolved)

        fragment_size = (
            values.f_frsize
            if values.f_frsize > 0
            else values.f_bsize
        )

        total_bytes = values.f_blocks * fragment_size
        raw_free_bytes = values.f_bfree * fragment_size
        available_bytes = values.f_bavail * fragment_size
        used_bytes = max(
            0,
            total_bytes - raw_free_bytes,
        )

        inode_total = values.f_files
        inode_raw_free = values.f_ffree
        inode_available = values.f_favail
        inode_used = max(
            0,
            inode_total - inode_raw_free,
        )

        return {
            "requested_path": str(requested_path),
            "resolved_path": str(resolved),
            "exists": requested_path.exists(),
            "device_id": stat_result.st_dev,
            "total_bytes": total_bytes,
            "used_bytes": used_bytes,
            "available_bytes": available_bytes,
            "raw_free_bytes": raw_free_bytes,
            "used_percent": cls._percentage(
                used_bytes,
                total_bytes,
            ),
            "available_percent": cls._percentage(
                available_bytes,
                total_bytes,
            ),
            "inode_total": inode_total,
            "inode_used": inode_used,
            "inode_available": inode_available,
            "inode_raw_free": inode_raw_free,
            "inode_used_percent": cls._percentage(
                inode_used,
                inode_total,
            ),
            "inode_available_percent": (
                cls._percentage(
                    inode_available,
                    inode_total,
                )
            ),
        }

    def _mount_targets(self) -> tuple[Path, ...]:
        return (
            Path("/"),
            Path("/home"),
            Path("/mnt/aura-data"),
            self.project_root,
        )

    def _collect_snapshot(self) -> dict[str, Any]:
        mount_targets = self._mount_targets()
        filesystems = [
            self._filesystem_packet(path)
            for path in mount_targets
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
            "captured_at": (
                self.inspection_time.isoformat()
            ),
            "hostname": platform.node(),
            "platform": platform.platform(),
            "project_root": str(self.project_root),
            "metric_group_count": 7,
            "cpu": self._cpu_packet(),
            "memory": self._memory_packet(),
            "swap": self._swap_packet(),
            "uptime": self._uptime_packet(),
            "processes": self._process_packet(),
            "filesystems": filesystems,
            "source_contract": {
                "psutil_required": False,
                "proc_read_only": True,
                "statvfs_read_only": True,
                "network_probe_used": False,
                "subprocess_used": False,
            },
            "runtime_boundary": {
                "background_sampler_enabled": False,
                "history_persistence_enabled": False,
                "dashboard_activation_enabled": False,
                "socket_activation_enabled": False,
                "systemd_mutation_enabled": False,
                "network_access_enabled": False,
                "process_control_enabled": False,
                "threshold_mutation_enabled": False,
            },
        }

    @staticmethod
    def _snapshot_digest(
        packet: dict[str, Any],
    ) -> str:
        canonical = json.dumps(
            packet,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(canonical).hexdigest()

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

    @staticmethod
    def _percentage_valid(value: object) -> bool:
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and 0.0 <= float(value) <= 100.0
        )

    def _snapshot_valid(self) -> bool:
        packet = self._snapshot_packet
        cpu = packet["cpu"]
        memory = packet["memory"]
        swap = packet["swap"]
        uptime = packet["uptime"]
        processes = packet["processes"]
        filesystems = packet["filesystems"]

        return all(
            (
                self._timestamp_valid(
                    packet["captured_at"]
                ),
                packet["metric_group_count"] == 7,
                cpu["logical_count"] > 0,
                self._percentage_valid(
                    cpu["usage_percent"]
                ),
                memory["total_bytes"] > 0,
                self._percentage_valid(
                    memory["used_percent"]
                ),
                swap["total_bytes"] >= 0,
                self._percentage_valid(
                    swap["used_percent"]
                ),
                uptime["seconds"] > 0,
                processes["count"] > 0,
                len(filesystems) == 4,
                all(
                    record["exists"]
                    for record in filesystems
                ),
                all(
                    record["total_bytes"] > 0
                    for record in filesystems
                ),
                all(
                    record["inode_total"] > 0
                    for record in filesystems
                ),
            )
        )

    def snapshot(self) -> dict[str, Any]:
        return json.loads(
            json.dumps(self._snapshot_packet)
        )

    def status(self) -> dict[str, Any]:
        packet = self._snapshot_packet
        runtime = packet["runtime_boundary"]
        filesystems = packet["filesystems"]
        status_valid = self._snapshot_valid()

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
            "metric_group_count": (
                packet["metric_group_count"]
            ),
            "filesystem_record_count": len(
                filesystems
            ),
            "captured_at": packet["captured_at"],
            "snapshot_digest": (
                packet["snapshot_digest"]
            ),
            **runtime,
        }

    def context(self) -> dict[str, Any]:
        packet = self._snapshot_packet

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "metric_sources": {
                "cpu": "/proc/stat",
                "cpu_model": "/proc/cpuinfo",
                "load_average": "os.getloadavg",
                "memory": "/proc/meminfo",
                "swap": "/proc/meminfo",
                "uptime": "/proc/uptime",
                "process_count": "/proc",
                "filesystem": "os.statvfs",
            },
            "mount_targets": [
                record["requested_path"]
                for record in packet["filesystems"]
            ],
            "measurement_contract": {
                "single_snapshot_only": True,
                "cpu_sample_interval_seconds": (
                    self.CPU_SAMPLE_INTERVAL_SECONDS
                ),
                "collection_duration_recorded": True,
                "percentages_bounded_0_to_100": True,
                "bytes_reported_as_integers": True,
                "inode_capacity_reported": True,
            },
            "source_contract": dict(
                packet["source_contract"]
            ),
            "runtime_boundary": dict(
                packet["runtime_boundary"]
            ),
        }

    def check(self) -> dict[str, Any]:
        status = self.status()
        context = self.context()
        snapshot = self._snapshot_packet
        cpu = snapshot["cpu"]
        memory = snapshot["memory"]
        swap = snapshot["swap"]
        uptime = snapshot["uptime"]
        processes = snapshot["processes"]
        filesystems = snapshot["filesystems"]
        source = snapshot["source_contract"]
        runtime = snapshot["runtime_boundary"]

        expected_mounts = {
            "/",
            "/home",
            "/mnt/aura-data",
            str(self.project_root),
        }
        actual_mounts = {
            record["requested_path"]
            for record in filesystems
        }

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
                "collection_duration_nonnegative",
                snapshot["collection_duration_ms"]
                >= 0,
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
                "metric_group_count",
                status["metric_group_count"] == 7,
            ),
            (
                "background_sampler_disabled",
                runtime["background_sampler_enabled"]
                is False,
            ),
            (
                "history_persistence_disabled",
                runtime["history_persistence_enabled"]
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
                "threshold_mutation_disabled",
                runtime["threshold_mutation_enabled"]
                is False,
            ),
            (
                "psutil_not_required",
                source["psutil_required"] is False,
            ),
            (
                "proc_read_only",
                source["proc_read_only"] is True,
            ),
            (
                "cpu_logical_count",
                cpu["logical_count"] > 0,
            ),
            (
                "cpu_percent_valid",
                self._percentage_valid(
                    cpu["usage_percent"]
                ),
            ),
            (
                "cpu_sample_interval_positive",
                cpu["sample_interval_seconds"] > 0,
            ),
            (
                "load_average_nonnegative",
                all(
                    value >= 0
                    for value in cpu[
                        "load_average"
                    ].values()
                ),
            ),
            (
                "cpu_model_present",
                bool(cpu["model"]),
            ),
            (
                "memory_total_positive",
                memory["total_bytes"] > 0,
            ),
            (
                "memory_available_range",
                0
                <= memory["available_bytes"]
                <= memory["total_bytes"],
            ),
            (
                "memory_used_range",
                0
                <= memory["used_bytes"]
                <= memory["total_bytes"],
            ),
            (
                "memory_percent_valid",
                self._percentage_valid(
                    memory["used_percent"]
                ),
            ),
            (
                "swap_total_nonnegative",
                swap["total_bytes"] >= 0,
            ),
            (
                "swap_used_range",
                0
                <= swap["used_bytes"]
                <= swap["total_bytes"],
            ),
            (
                "swap_free_range",
                0
                <= swap["free_bytes"]
                <= swap["total_bytes"],
            ),
            (
                "swap_percent_valid",
                self._percentage_valid(
                    swap["used_percent"]
                ),
            ),
            (
                "uptime_positive",
                uptime["seconds"] > 0,
            ),
            (
                "process_count_positive",
                processes["count"] > 0,
            ),
            (
                "filesystem_record_count",
                len(filesystems) == 4,
            ),
            (
                "mount_targets_exact",
                actual_mounts == expected_mounts,
            ),
            (
                "filesystem_paths_exist",
                all(
                    record["exists"]
                    for record in filesystems
                ),
            ),
            (
                "filesystem_total_positive",
                all(
                    record["total_bytes"] > 0
                    for record in filesystems
                ),
            ),
            (
                "filesystem_used_range",
                all(
                    0
                    <= record["used_bytes"]
                    <= record["total_bytes"]
                    for record in filesystems
                ),
            ),
            (
                "filesystem_available_range",
                all(
                    0
                    <= record["available_bytes"]
                    <= record["total_bytes"]
                    for record in filesystems
                ),
            ),
            (
                "filesystem_percentages_valid",
                all(
                    self._percentage_valid(
                        record["used_percent"]
                    )
                    and self._percentage_valid(
                        record[
                            "available_percent"
                        ]
                    )
                    for record in filesystems
                ),
            ),
            (
                "inode_total_positive",
                all(
                    record["inode_total"] > 0
                    for record in filesystems
                ),
            ),
            (
                "inode_used_range",
                all(
                    0
                    <= record["inode_used"]
                    <= record["inode_total"]
                    for record in filesystems
                ),
            ),
            (
                "inode_available_range",
                all(
                    0
                    <= record["inode_available"]
                    <= record["inode_total"]
                    for record in filesystems
                ),
            ),
            (
                "snapshot_digest_present",
                len(snapshot["snapshot_digest"])
                == 64,
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
            "snapshot_digest": (
                snapshot["snapshot_digest"]
            ),
            "background_sampler_enabled": (
                runtime[
                    "background_sampler_enabled"
                ]
            ),
            "history_persistence_enabled": (
                runtime[
                    "history_persistence_enabled"
                ]
            ),
            "dashboard_activation_enabled": (
                runtime[
                    "dashboard_activation_enabled"
                ]
            ),
            "socket_activation_enabled": (
                runtime[
                    "socket_activation_enabled"
                ]
            ),
            "systemd_mutation_enabled": (
                runtime[
                    "systemd_mutation_enabled"
                ]
            ),
            "network_access_enabled": (
                runtime["network_access_enabled"]
            ),
            "process_control_enabled": (
                runtime["process_control_enabled"]
            ),
            "threshold_mutation_enabled": (
                runtime[
                    "threshold_mutation_enabled"
                ]
            ),
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in checks
            ],
            "context_summary": {
                "mount_target_count": len(
                    context["mount_targets"]
                ),
                "metric_source_count": len(
                    context["metric_sources"]
                ),
                "single_snapshot_only": (
                    context[
                        "measurement_contract"
                    ]["single_snapshot_only"]
                ),
            },
        }
