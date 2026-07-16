from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence
import hashlib
import json
import os
import subprocess

from aura.manual_start_stop_status_runtime.manual_start_stop_status_runtime_executor import (
    ManualStartStopStatusRuntimeExecutor,
)


class ReviewedOptionalAutostartUnitContract:
    UNIT_NAME = "aura-local.service"
    CONFIRMATION_TOKEN = "ENABLE_AURA_AUTOSTART"

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        self.user_unit_directory = (
            Path.home() / ".config" / "systemd" / "user"
        )
        self.target_path = self.user_unit_directory / self.UNIT_NAME

    @staticmethod
    def _systemd_quote(value: str) -> str:
        escaped = (
            str(value)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("%", "%%")
        )
        return f'"{escaped}"'

    @staticmethod
    def _read_only_command(
        command: Sequence[str],
    ) -> dict[str, Any]:
        try:
            completed = subprocess.run(
                list(command),
                text=True,
                capture_output=True,
                timeout=8,
                check=False,
            )
        except (
            FileNotFoundError,
            subprocess.TimeoutExpired,
            OSError,
        ) as exc:
            return {
                "command": list(command),
                "exit_code": None,
                "stdout": "",
                "stderr": str(exc),
                "available": False,
                "read_only": True,
            }

        return {
            "command": list(command),
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "available": True,
            "read_only": True,
        }

    @property
    def expected_argv(self) -> tuple[str, ...]:
        return tuple(str(value) for value in self.owner.expected_argv)

    def exec_start_line(self) -> str:
        return " ".join(
            self._systemd_quote(value)
            for value in self.expected_argv
        )

    def unit_text(self) -> str:
        return (
            "[Unit]\n"
            "Description=AURA Local Runtime "
            "(Reviewed Optional Autostart)\n"
            "After=default.target\n"
            "StartLimitIntervalSec=120\n"
            "StartLimitBurst=3\n"
            f"ConditionPathIsDirectory={self.project_root}\n"
            "\n"
            "[Service]\n"
            "Type=simple\n"
            f"WorkingDirectory={self.project_root}\n"
            f"ExecStart={self.exec_start_line()}\n"
            "Restart=on-failure\n"
            "RestartSec=5\n"
            "TimeoutStopSec=30\n"
            "KillSignal=SIGTERM\n"
            "UMask=0077\n"
            "Environment=PYTHONUNBUFFERED=1\n"
            "NoNewPrivileges=true\n"
            "\n"
            "[Install]\n"
            "WantedBy=default.target\n"
        )

    def unit_digest(self) -> str:
        return hashlib.sha256(
            self.unit_text().encode("utf-8")
        ).hexdigest()

    def host_posture(self) -> dict[str, Any]:
        manager = self._read_only_command(
            ("systemctl", "--user", "show-environment")
        )
        unit_query = self._read_only_command(
            (
                "systemctl",
                "--user",
                "list-unit-files",
                self.UNIT_NAME,
                "--no-legend",
                "--plain",
            )
        )
        linger = self._read_only_command(
            (
                "loginctl",
                "show-user",
                str(os.getuid()),
                "-p",
                "Linger",
                "--value",
            )
        )
        linger_value = (
            linger["stdout"].strip().lower()
            if linger["exit_code"] == 0
            else "unknown"
        )
        if linger_value not in {"yes", "no"}:
            linger_value = "unknown"

        return {
            "user_manager_available": manager["exit_code"] == 0,
            "target_path": str(self.target_path),
            "target_exists": (
                self.target_path.exists()
                or self.target_path.is_symlink()
            ),
            "unit_query": unit_query,
            "linger_value": linger_value,
            "boot_without_login_ready": linger_value == "yes",
            "host_inspection_only": True,
            "systemd_mutated": False,
            "autostart_mutated": False,
            "linger_mutated": False,
        }

    def unit_preview(self) -> dict[str, Any]:
        return {
            "ok": True,
            "review_only": True,
            "unit_name": self.UNIT_NAME,
            "unit_type": "user_service",
            "target_path": str(self.target_path),
            "working_directory": str(self.project_root),
            "expected_argv": list(self.expected_argv),
            "exec_start": self.exec_start_line(),
            "unit_text": self.unit_text(),
            "unit_sha256": self.unit_digest(),
            "restart_policy": "on-failure",
            "restart_sec": 5,
            "start_limit_interval_sec": 120,
            "start_limit_burst": 3,
            "umask": "0077",
            "install_target": "default.target",
            "unit_written": False,
            "unit_installed": False,
            "daemon_reload_executed": False,
            "service_enabled": False,
            "service_started": False,
        }

    def activation_preview(self) -> dict[str, Any]:
        posture = self.host_posture()
        return {
            "ok": True,
            "review_only": True,
            "activation_deferred": True,
            "approval_required": True,
            "required_confirmation_token": self.CONFIRMATION_TOKEN,
            "target_path": str(self.target_path),
            "unit_sha256": self.unit_digest(),
            "steps": [
                {
                    "order": 1,
                    "action": "create_user_unit_directory",
                    "command_preview": (
                        "install -d -m 700 "
                        f"{self.user_unit_directory}"
                    ),
                    "executed": False,
                },
                {
                    "order": 2,
                    "action": "write_exact_reviewed_unit",
                    "command_preview": (
                        "write the reviewed unit text to "
                        f"{self.target_path} with mode 0600"
                    ),
                    "executed": False,
                },
                {
                    "order": 3,
                    "action": "daemon_reload",
                    "command_preview": (
                        "systemctl --user daemon-reload"
                    ),
                    "executed": False,
                },
                {
                    "order": 4,
                    "action": "enable_autostart",
                    "command_preview": (
                        "systemctl --user enable "
                        f"{self.UNIT_NAME}"
                    ),
                    "executed": False,
                },
            ],
            "start_now_default": False,
            "enable_default": False,
            "linger_change_included": False,
            "boot_without_login_ready": posture[
                "boot_without_login_ready"
            ],
            "activation_executed": False,
            "unit_written": False,
            "daemon_reload_executed": False,
            "service_enabled": False,
            "service_started": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
            "linger_mutated": False,
        }

    def rollback_preview(self) -> dict[str, Any]:
        return {
            "ok": True,
            "review_only": True,
            "approval_required": True,
            "target_path": str(self.target_path),
            "steps": [
                {
                    "order": 1,
                    "action": "disable_and_stop",
                    "command_preview": (
                        "systemctl --user disable --now "
                        f"{self.UNIT_NAME}"
                    ),
                    "executed": False,
                },
                {
                    "order": 2,
                    "action": "remove_unit",
                    "command_preview": f"rm -- {self.target_path}",
                    "executed": False,
                },
                {
                    "order": 3,
                    "action": "daemon_reload",
                    "command_preview": (
                        "systemctl --user daemon-reload"
                    ),
                    "executed": False,
                },
                {
                    "order": 4,
                    "action": "reset_failed",
                    "command_preview": (
                        "systemctl --user reset-failed "
                        f"{self.UNIT_NAME}"
                    ),
                    "executed": False,
                },
            ],
            "rollback_executed": False,
            "unit_removed": False,
            "daemon_reload_executed": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
            "linger_mutated": False,
        }

    def contract_snapshot(self) -> dict[str, Any]:
        payload = {
            "unit": self.unit_preview(),
            "activation": self.activation_preview(),
            "rollback": self.rollback_preview(),
        }
        return {
            **payload,
            "host_posture": self.host_posture(),
            "contract_sha256": hashlib.sha256(
                json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
        }
