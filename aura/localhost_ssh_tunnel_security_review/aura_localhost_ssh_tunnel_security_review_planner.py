from __future__ import annotations

import hashlib
import ipaddress
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


class AuraLocalhostSshTunnelSecurityReviewPlanner:
    VERSION = "1.0.8-genesis"
    ANCHOR_VERSION = "1.0.7-genesis"
    CURRENT_SPRINT = 248
    NEXT_SPRINT = 249
    BOUNDARY = "localhost_ssh_tunnel_security_review"
    NEXT_BOUNDARY = "permission_expiry_recovery_review"
    OWNER = "AuraLocalhostSshTunnelSecurityReviewPlanner"
    CONTRACT_MODE = "read_only_security_review"
    REVIEW_MODE = "single_local_posture_snapshot"
    EXPECTED_ASSERTION_COUNT = 80
    EXPECTED_AURA_HOST = "127.0.0.1"
    EXPECTED_AURA_PORT = 8765
    EXPECTED_TUNNEL_DESTINATION = "127.0.0.1:8765"
    REVIEW_STATES = (
        "secure",
        "review",
        "warning",
        "unavailable",
    )
    STATE_PRIORITY = {
        "secure": 0,
        "review": 1,
        "warning": 2,
        "unavailable": 3,
    }
    SELECTED_SSH_DIRECTIVES = (
        "addressfamily",
        "allowtcpforwarding",
        "gatewayports",
        "listenaddress",
        "passwordauthentication",
        "permitopen",
        "permitrootlogin",
        "pubkeyauthentication",
        "x11forwarding",
    )
    SSHD_BINARY_CANDIDATES = (
        "/usr/sbin/sshd",
        "/sbin/sshd",
        "/usr/bin/sshd",
    )

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self._packet = self._build_review_packet()
        self._packet["review_digest"] = self._packet_digest(
            self._packet
        )

    @classmethod
    def _state_valid(cls, value: object) -> bool:
        return value in cls.REVIEW_STATES

    @classmethod
    def _worst_state(
        cls,
        states: list[str] | tuple[str, ...],
    ) -> str:
        if not states:
            return "unavailable"

        return max(
            states,
            key=lambda state: cls.STATE_PRIORITY.get(
                state,
                cls.STATE_PRIORITY["unavailable"],
            ),
        )

    @staticmethod
    def _packet_digest(packet: dict[str, Any]) -> str:
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
    def _normalize_scalar(value: object) -> object:
        if isinstance(value, str):
            return " ".join(value.split())

        return value

    def _settings_binding_packet(self) -> dict[str, Any]:
        path = (
            self.project_root
            / "aura/config/settings.yaml"
        )
        exists = path.is_file()
        readable = exists and os.access(path, os.R_OK)
        pairs: list[dict[str, Any]] = []

        if readable:
            payload = yaml.safe_load(
                path.read_text(encoding="utf-8")
            )

            def walk(
                value: object,
                location: tuple[str, ...],
            ) -> None:
                if isinstance(value, dict):
                    host = value.get("host")
                    port = value.get("port")

                    if (
                        isinstance(host, str)
                        and isinstance(port, int)
                        and not isinstance(port, bool)
                    ):
                        pairs.append(
                            {
                                "path": ".".join(location),
                                "host": self._normalize_scalar(
                                    host
                                ),
                                "port": port,
                            }
                        )

                    for key, item in value.items():
                        walk(
                            item,
                            (*location, str(key)),
                        )

                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        walk(
                            item,
                            (*location, str(index)),
                        )

            walk(payload, ())

        expected = [
            item
            for item in pairs
            if (
                item["host"] == self.EXPECTED_AURA_HOST
                and item["port"] == self.EXPECTED_AURA_PORT
            )
        ]
        wildcard = [
            item
            for item in pairs
            if item["host"] in {
                "0.0.0.0",
                "::",
                "[::]",
            }
        ]

        if not exists or not readable:
            state = "unavailable"
        elif expected and not wildcard:
            state = "secure"
        elif wildcard:
            state = "warning"
        else:
            state = "review"

        return {
            "id": "aura_binding_policy",
            "state": state,
            "settings_path": str(path),
            "settings_exists": exists,
            "settings_readable": readable,
            "binding_pair_count": len(pairs),
            "binding_pairs": pairs,
            "expected_host": self.EXPECTED_AURA_HOST,
            "expected_port": self.EXPECTED_AURA_PORT,
            "expected_binding_found": bool(expected),
            "wildcard_binding_pair_count": len(wildcard),
            "source": "aura/config/settings.yaml",
        }

    @staticmethod
    def _decode_ipv4(raw: str) -> str:
        packed = bytes.fromhex(raw)
        return str(
            ipaddress.IPv4Address(packed[::-1])
        )

    @staticmethod
    def _decode_ipv6_scope(
        raw: str,
    ) -> tuple[str, str]:
        normalized = raw.upper()

        if normalized == "0" * 32:
            return "::", "wildcard"

        if normalized in {
            "00000000000000000000000001000000",
            "00000000000000000000000000000001",
        }:
            return "::1", "loopback"

        return normalized, "non_loopback"

    @staticmethod
    def _address_scope(address: str) -> str:
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            return "unknown"

        if parsed.is_unspecified:
            return "wildcard"

        if parsed.is_loopback:
            return "loopback"

        return "non_loopback"

    def _listener_inventory(self) -> dict[str, Any]:
        records: list[dict[str, Any]] = []
        source_paths = (
            (Path("/proc/net/tcp"), "ipv4"),
            (Path("/proc/net/tcp6"), "ipv6"),
        )
        source_count = 0

        for path, family in source_paths:
            if not path.is_file():
                continue

            source_count += 1

            for line in path.read_text(
                encoding="utf-8"
            ).splitlines()[1:]:
                fields = line.split()

                if len(fields) < 10:
                    continue

                if fields[3] != "0A":
                    continue

                raw_address, raw_port = fields[1].split(
                    ":",
                    1,
                )

                if family == "ipv4":
                    address = self._decode_ipv4(
                        raw_address
                    )
                    scope = self._address_scope(
                        address
                    )
                else:
                    (
                        address,
                        scope,
                    ) = self._decode_ipv6_scope(
                        raw_address
                    )

                records.append(
                    {
                        "family": family,
                        "address": address,
                        "scope": scope,
                        "port": int(raw_port, 16),
                    }
                )

        records.sort(
            key=lambda item: (
                item["port"],
                item["family"],
                item["address"],
            )
        )

        aura = [
            item
            for item in records
            if item["port"] == self.EXPECTED_AURA_PORT
        ]
        ssh = [
            item
            for item in records
            if item["port"] == 22
        ]

        aura_nonloopback = [
            item
            for item in aura
            if item["scope"] != "loopback"
        ]
        ssh_wildcard = [
            item
            for item in ssh
            if item["scope"] == "wildcard"
        ]

        return {
            "source_count": source_count,
            "records": records,
            "record_count": len(records),
            "aura_records": aura,
            "aura_listener_count": len(aura),
            "aura_non_loopback_count": len(
                aura_nonloopback
            ),
            "ssh_records": ssh,
            "ssh_listener_count": len(ssh),
            "ssh_wildcard_count": len(
                ssh_wildcard
            ),
        }

    def _aura_listener_dimension(
        self,
        inventory: dict[str, Any],
    ) -> dict[str, Any]:
        aura_count = inventory[
            "aura_listener_count"
        ]
        nonloopback_count = inventory[
            "aura_non_loopback_count"
        ]

        if inventory["source_count"] == 0:
            state = "unavailable"
        elif nonloopback_count > 0:
            state = "warning"
        elif aura_count == 0:
            state = "secure"
        else:
            state = "review"

        return {
            "id": "aura_listener_exposure",
            "state": state,
            "expected_host": self.EXPECTED_AURA_HOST,
            "expected_port": self.EXPECTED_AURA_PORT,
            "listener_count": aura_count,
            "non_loopback_listener_count": (
                nonloopback_count
            ),
            "listeners": inventory[
                "aura_records"
            ],
            "source": "/proc/net/tcp,/proc/net/tcp6",
        }

    def _ssh_listener_dimension(
        self,
        inventory: dict[str, Any],
    ) -> dict[str, Any]:
        count = inventory["ssh_listener_count"]
        wildcard = inventory["ssh_wildcard_count"]

        if inventory["source_count"] == 0:
            state = "unavailable"
        elif count == 0:
            state = "warning"
        elif wildcard > 0:
            state = "review"
        else:
            state = "secure"

        return {
            "id": "ssh_listener_scope",
            "state": state,
            "port": 22,
            "listener_count": count,
            "wildcard_listener_count": wildcard,
            "listeners": inventory["ssh_records"],
            "source": "/proc/net/tcp,/proc/net/tcp6",
        }

    def _ssh_config_packet(self) -> dict[str, Any]:
        main = Path("/etc/ssh/sshd_config")
        dropin_dir = Path(
            "/etc/ssh/sshd_config.d"
        )
        dropins = (
            sorted(dropin_dir.glob("*.conf"))
            if dropin_dir.is_dir()
            else []
        )
        config_paths = [
            path
            for path in [main, *dropins]
            if path.is_file()
            and os.access(path, os.R_OK)
        ]
        pattern = re.compile(
            r"^\s*("
            + "|".join(
                re.escape(item)
                for item in self.SELECTED_SSH_DIRECTIVES
            )
            + r")\s+(.+?)\s*$",
            re.IGNORECASE,
        )
        configured = {
            key: []
            for key in self.SELECTED_SSH_DIRECTIVES
        }

        for path in config_paths:
            for raw_line in path.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines():
                line = raw_line.split(
                    "#",
                    1,
                )[0].strip()

                if not line:
                    continue

                match = pattern.match(line)

                if not match:
                    continue

                key = match.group(1).lower()
                value = " ".join(
                    match.group(2).split()
                )
                configured[key].append(value)

        binaries = [
            raw
            for raw in self.SSHD_BINARY_CANDIDATES
            if Path(raw).is_file()
            and os.access(raw, os.X_OK)
        ]

        return {
            "main_config_path": str(main),
            "main_config_exists": main.is_file(),
            "main_config_readable": os.access(
                main,
                os.R_OK,
            ),
            "dropin_count": len(dropins),
            "config_paths": [
                str(path)
                for path in config_paths
            ],
            "config_path_count": len(config_paths),
            "configured_directives": configured,
            "selected_directives": list(
                self.SELECTED_SSH_DIRECTIVES
            ),
            "sshd_binary_candidates": binaries,
            "sshd_binary_candidate_count": len(
                binaries
            ),
            "effective_policy_execution_enabled": False,
            "effective_policy_available": False,
            "source": (
                "/etc/ssh/sshd_config,"
                "/etc/ssh/sshd_config.d/*.conf"
            ),
        }

    @staticmethod
    def _directive_last(
        packet: dict[str, Any],
        key: str,
    ) -> str | None:
        values = packet[
            "configured_directives"
        ][key]

        if not values:
            return None

        return values[-1].lower()

    @staticmethod
    def _policy_state(
        value: str | None,
        *,
        secure: set[str],
        warning: set[str],
    ) -> str:
        if value is None:
            return "review"

        if value in secure:
            return "secure"

        if value in warning:
            return "warning"

        return "review"

    def _sshd_config_dimension(
        self,
        packet: dict[str, Any],
    ) -> dict[str, Any]:
        if (
            not packet["main_config_exists"]
            or not packet["main_config_readable"]
        ):
            state = "unavailable"
        elif packet["config_path_count"] > 0:
            state = "review"
        else:
            state = "unavailable"

        return {
            "id": "sshd_effective_policy",
            "state": state,
            **packet,
            "review_reason": (
                "effective policy execution is intentionally "
                "disabled; configured directives only"
            ),
        }

    def _ssh_tunnel_dimension(
        self,
        packet: dict[str, Any],
    ) -> dict[str, Any]:
        gatewayports = self._directive_last(
            packet,
            "gatewayports",
        )
        allowtcp = self._directive_last(
            packet,
            "allowtcpforwarding",
        )
        permitopen = self._directive_last(
            packet,
            "permitopen",
        )
        root_login = self._directive_last(
            packet,
            "permitrootlogin",
        )
        password_auth = self._directive_last(
            packet,
            "passwordauthentication",
        )
        pubkey_auth = self._directive_last(
            packet,
            "pubkeyauthentication",
        )
        x11 = self._directive_last(
            packet,
            "x11forwarding",
        )

        states = {
            "gatewayports": self._policy_state(
                gatewayports,
                secure={"no"},
                warning={"yes", "clientspecified"},
            ),
            "allowtcpforwarding": self._policy_state(
                allowtcp,
                secure={"yes", "all", "local"},
                warning={"no", "remote"},
            ),
            "permitopen": (
                "secure"
                if permitopen
                == self.EXPECTED_TUNNEL_DESTINATION
                else (
                    "warning"
                    if permitopen == "none"
                    else "review"
                )
            ),
            "permitrootlogin": self._policy_state(
                root_login,
                secure={
                    "no",
                    "prohibit-password",
                    "without-password",
                    "forced-commands-only",
                },
                warning={"yes"},
            ),
            "passwordauthentication": (
                self._policy_state(
                    password_auth,
                    secure={"no"},
                    warning={"yes"},
                )
            ),
            "pubkeyauthentication": (
                self._policy_state(
                    pubkey_auth,
                    secure={"yes"},
                    warning={"no"},
                )
            ),
            "x11forwarding": self._policy_state(
                x11,
                secure={"no"},
                warning={"yes"},
            ),
        }

        return {
            "id": "ssh_tunnel_policy",
            "state": self._worst_state(
                list(states.values())
            ),
            "tunnel_destination": (
                self.EXPECTED_TUNNEL_DESTINATION
            ),
            "configured_values": {
                "gatewayports": gatewayports,
                "allowtcpforwarding": allowtcp,
                "permitopen": permitopen,
                "permitrootlogin": root_login,
                "passwordauthentication": password_auth,
                "pubkeyauthentication": pubkey_auth,
                "x11forwarding": x11,
            },
            "directive_states": states,
            "effective_policy_available": packet[
                "effective_policy_available"
            ],
            "effective_policy_execution_enabled": (
                packet[
                    "effective_policy_execution_enabled"
                ]
            ),
            "source": packet["source"],
        }

    def _ssh_file_permissions_dimension(
        self,
    ) -> dict[str, Any]:
        ssh_dir = Path.home() / ".ssh"
        exists = ssh_dir.is_dir()
        owner_ok = (
            ssh_dir.stat().st_uid == os.getuid()
            if exists
            else True
        )
        mode = (
            stat.S_IMODE(ssh_dir.stat().st_mode)
            if exists
            else None
        )
        mode_secure = (
            mode is None
            or mode & 0o077 == 0
        )
        files = (
            [
                path
                for path in ssh_dir.iterdir()
                if path.is_file()
            ]
            if exists
            else []
        )
        private_candidates = [
            path
            for path in files
            if (
                path.name.startswith("id_")
                and not path.name.endswith(".pub")
            )
        ]
        private_modes_secure = all(
            (
                stat.S_IMODE(path.stat().st_mode)
                & 0o077
            )
            == 0
            for path in private_candidates
        )

        def metadata(name: str) -> dict[str, Any]:
            path = ssh_dir / name
            present = path.is_file()

            return {
                "exists": present,
                "mode": (
                    stat.S_IMODE(path.stat().st_mode)
                    if present
                    else None
                ),
                "owner_is_current_user": (
                    path.stat().st_uid == os.getuid()
                    if present
                    else True
                ),
            }

        authorized = metadata("authorized_keys")
        known_hosts = metadata("known_hosts")

        if not exists:
            state = "review"
        elif (
            owner_ok
            and mode_secure
            and private_modes_secure
            and authorized["owner_is_current_user"]
            and known_hosts["owner_is_current_user"]
        ):
            state = "secure"
        else:
            state = "warning"

        return {
            "id": "ssh_file_permissions",
            "state": state,
            "ssh_directory_exists": exists,
            "ssh_directory_mode": mode,
            "ssh_directory_owner_is_current_user": (
                owner_ok
            ),
            "ssh_directory_mode_secure": mode_secure,
            "ssh_file_count": len(files),
            "private_key_candidate_count": len(
                private_candidates
            ),
            "private_key_modes_secure": (
                private_modes_secure
            ),
            "authorized_keys_metadata": authorized,
            "known_hosts_metadata": known_hosts,
            "private_key_content_read": False,
            "credential_content_read": False,
            "source": "filesystem metadata only",
        }

    @staticmethod
    def _firewall_dimension() -> dict[str, Any]:
        ufw_config = Path("/etc/ufw/ufw.conf")
        ufw_unit_candidates = (
            Path(
                "/lib/systemd/system/ufw.service"
            ),
            Path(
                "/usr/lib/systemd/system/ufw.service"
            ),
            Path(
                "/etc/systemd/system/ufw.service"
            ),
        )
        unit_visible = any(
            path.exists()
            for path in ufw_unit_candidates
        )
        config_exists = ufw_config.is_file()

        if config_exists or unit_visible:
            state = "review"
        else:
            state = "unavailable"

        return {
            "id": "firewall_visibility",
            "state": state,
            "ufw_config_exists": config_exists,
            "ufw_unit_visible": unit_visible,
            "rules_content_read": False,
            "visibility_metadata_only": True,
            "source": (
                "/etc/ufw/ufw.conf and "
                "systemd unit metadata"
            ),
        }

    @staticmethod
    def _strict_aura_process_count() -> int:
        count = 0

        current_pid = os.getpid()

        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue

            if int(entry.name) == current_pid:
                continue

            try:
                raw = (
                    entry / "cmdline"
                ).read_bytes()
            except (
                FileNotFoundError,
                PermissionError,
                ProcessLookupError,
            ):
                continue

            argv = [
                item.decode(
                    "utf-8",
                    errors="replace",
                )
                for item in raw.split(b"\0")
                if item
            ]

            if not argv:
                continue

            executable = Path(
                argv[0]
            ).name.lower()

            if (
                executable.startswith("python")
                and any(
                    Path(item).name == "main.py"
                    for item in argv[1:]
                )
            ):
                count += 1

        return count

    def _runtime_dimension(
        self,
        inventory: dict[str, Any],
    ) -> dict[str, Any]:
        process_count = (
            self._strict_aura_process_count()
        )
        aura_listener_count = inventory[
            "aura_listener_count"
        ]

        if (
            process_count == 0
            and aura_listener_count == 0
        ):
            state = "secure"
        else:
            state = "warning"

        return {
            "id": "runtime_activation",
            "state": state,
            "strict_python_main_process_count": (
                process_count
            ),
            "aura_listener_count": (
                aura_listener_count
            ),
            "service_activation_detected": (
                process_count > 0
                or aura_listener_count > 0
            ),
            "source": "/proc",
        }

    @staticmethod
    def _runtime_boundary() -> dict[str, bool]:
        return {
            "config_mutation_enabled": False,
            "ssh_config_mutation_enabled": False,
            "firewall_mutation_enabled": False,
            "sshd_restart_enabled": False,
            "service_activation_enabled": False,
            "socket_activation_enabled": False,
            "network_connection_enabled": False,
            "process_control_enabled": False,
            "credential_read_enabled": False,
            "private_key_content_read_enabled": False,
            "key_generation_enabled": False,
            "known_hosts_mutation_enabled": False,
            "systemd_mutation_enabled": False,
            "command_execution_enabled": False,
        }

    def _build_review_packet(
        self,
    ) -> dict[str, Any]:
        inventory = self._listener_inventory()
        ssh_config = self._ssh_config_packet()
        dimensions = [
            self._settings_binding_packet(),
            self._aura_listener_dimension(
                inventory
            ),
            self._ssh_listener_dimension(
                inventory
            ),
            self._sshd_config_dimension(
                ssh_config
            ),
            self._ssh_tunnel_dimension(
                ssh_config
            ),
            self._ssh_file_permissions_dimension(),
            self._firewall_dimension(),
            self._runtime_dimension(
                inventory
            ),
        ]
        overall = self._worst_state(
            [
                item["state"]
                for item in dimensions
            ]
        )
        state_counts = {
            state: sum(
                item["state"] == state
                for item in dimensions
            )
            for state in self.REVIEW_STATES
        }
        findings = [
            {
                "dimension": item["id"],
                "state": item["state"],
            }
            for item in dimensions
            if item["state"] != "secure"
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
            "review_mode": self.REVIEW_MODE,
            "captured_at": datetime.now(
                timezone.utc
            ).astimezone().isoformat(),
            "project_root": str(self.project_root),
            "expected_aura_host": (
                self.EXPECTED_AURA_HOST
            ),
            "expected_aura_port": (
                self.EXPECTED_AURA_PORT
            ),
            "expected_tunnel_destination": (
                self.EXPECTED_TUNNEL_DESTINATION
            ),
            "review_states": list(
                self.REVIEW_STATES
            ),
            "overall_state": overall,
            "dimension_count": len(dimensions),
            "dimensions": dimensions,
            "state_counts": state_counts,
            "finding_count": len(findings),
            "findings": findings,
            "listener_source_count": inventory[
                "source_count"
            ],
            "listener_record_count": inventory[
                "record_count"
            ],
            "runtime_boundary": (
                self._runtime_boundary()
            ),
            "source_contract": {
                "aura_settings_read_only": True,
                "proc_listener_tables_read_only": True,
                "sshd_config_read_only": True,
                "ssh_metadata_only": True,
                "firewall_metadata_only": True,
                "effective_sshd_execution_used": False,
                "network_connection_used": False,
                "credential_content_read": False,
                "private_key_content_read": False,
            },
        }

    def snapshot(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._packet))

    def review(self) -> dict[str, Any]:
        return self.snapshot()

    def status(self) -> dict[str, Any]:
        packet = self._packet
        runtime = packet["runtime_boundary"]
        valid = all(
            (
                self._timestamp_valid(
                    packet["captured_at"]
                ),
                self._state_valid(
                    packet["overall_state"]
                ),
                packet["dimension_count"] == 8,
                sum(
                    packet["state_counts"].values()
                )
                == packet["dimension_count"],
                len(packet["review_digest"]) == 64,
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
            "review_mode": self.REVIEW_MODE,
            "status_valid": valid,
            "alpha_ready": valid,
            "captured_at": packet["captured_at"],
            "overall_state": packet["overall_state"],
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            **runtime,
        }

    def context(self) -> dict[str, Any]:
        packet = self._packet

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "review_states": list(
                self.REVIEW_STATES
            ),
            "dimension_ids": [
                item["id"]
                for item in packet["dimensions"]
            ],
            "expected_aura_host": (
                self.EXPECTED_AURA_HOST
            ),
            "expected_aura_port": (
                self.EXPECTED_AURA_PORT
            ),
            "expected_tunnel_destination": (
                self.EXPECTED_TUNNEL_DESTINATION
            ),
            "source_contract": dict(
                packet["source_contract"]
            ),
            "runtime_boundary": dict(
                packet["runtime_boundary"]
            ),
            "scope_boundary": {
                "read_only_review_only": True,
                "effective_sshd_execution_deferred": True,
                "firewall_rule_inspection_deferred": True,
                "ssh_mutation_deferred": True,
                "tunnel_connection_deferred": True,
                "credential_and_key_content_excluded": True,
            },
        }

    def check(self) -> dict[str, Any]:
        packet = self._packet
        status = self.status()
        context = self.context()
        dimensions = packet["dimensions"]
        dimension_map = {
            item["id"]: item
            for item in dimensions
        }
        runtime = packet["runtime_boundary"]
        binding = dimension_map[
            "aura_binding_policy"
        ]
        listener = dimension_map[
            "aura_listener_exposure"
        ]
        ssh_listener = dimension_map[
            "ssh_listener_scope"
        ]
        sshd = dimension_map[
            "sshd_effective_policy"
        ]
        tunnel = dimension_map[
            "ssh_tunnel_policy"
        ]
        ssh_files = dimension_map[
            "ssh_file_permissions"
        ]
        firewall = dimension_map[
            "firewall_visibility"
        ]
        activation = dimension_map[
            "runtime_activation"
        ]
        expected_ids = {
            "aura_binding_policy",
            "aura_listener_exposure",
            "ssh_listener_scope",
            "sshd_effective_policy",
            "ssh_tunnel_policy",
            "ssh_file_permissions",
            "firewall_visibility",
            "runtime_activation",
        }

        checks: list[tuple[str, bool]] = []

        def add(name: str, value: object) -> None:
            checks.append((name, value is True))

        # Core contract: 15.
        add("version", status["version"] == self.VERSION)
        add(
            "anchor_version",
            status["anchor_version"]
            == self.ANCHOR_VERSION,
        )
        add(
            "current_sprint",
            status["current_sprint"]
            == self.CURRENT_SPRINT,
        )
        add(
            "next_sprint",
            status["next_sprint"]
            == self.NEXT_SPRINT,
        )
        add(
            "boundary",
            status["boundary"] == self.BOUNDARY,
        )
        add(
            "next_boundary",
            status["next_boundary"]
            == self.NEXT_BOUNDARY,
        )
        add(
            "contract_mode",
            status["contract_mode"]
            == self.CONTRACT_MODE,
        )
        add(
            "review_mode",
            status["review_mode"]
            == self.REVIEW_MODE,
        )
        add("owner", status["owner"] == self.OWNER)
        add(
            "captured_at_valid",
            self._timestamp_valid(
                status["captured_at"]
            ),
        )
        add(
            "status_valid",
            status["status_valid"] is True,
        )
        add(
            "alpha_ready",
            status["alpha_ready"] is True,
        )
        add(
            "overall_state_valid",
            self._state_valid(
                status["overall_state"]
            ),
        )
        add(
            "dimension_count",
            status["dimension_count"] == 8,
        )
        add(
            "state_count_total",
            sum(status["state_counts"].values())
            == 8,
        )

        # Binding and listeners: 15.
        add(
            "settings_exists",
            binding["settings_exists"] is True,
        )
        add(
            "settings_readable",
            binding["settings_readable"] is True,
        )
        add(
            "binding_pair_count_positive",
            binding["binding_pair_count"] >= 1,
        )
        add(
            "expected_binding_found",
            binding["expected_binding_found"]
            is True,
        )
        add(
            "expected_host",
            binding["expected_host"]
            == self.EXPECTED_AURA_HOST,
        )
        add(
            "expected_port",
            binding["expected_port"]
            == self.EXPECTED_AURA_PORT,
        )
        add(
            "configured_pairs_valid",
            all(
                isinstance(item["host"], str)
                and isinstance(item["port"], int)
                and not isinstance(item["port"], bool)
                for item in binding["binding_pairs"]
            ),
        )
        add(
            "wildcard_pair_absent",
            binding[
                "wildcard_binding_pair_count"
            ]
            == 0,
        )
        add(
            "listener_sources_exact",
            packet["listener_source_count"] == 2,
        )
        add(
            "listener_records_valid",
            all(
                item["scope"]
                in {
                    "loopback",
                    "wildcard",
                    "non_loopback",
                    "unknown",
                }
                and isinstance(item["port"], int)
                for item in (
                    listener["listeners"]
                    + ssh_listener["listeners"]
                )
            ),
        )
        add(
            "aura_listener_count_zero",
            listener["listener_count"] == 0,
        )
        add(
            "aura_nonloopback_zero",
            listener[
                "non_loopback_listener_count"
            ]
            == 0,
        )
        add(
            "ssh_listener_count_positive",
            ssh_listener["listener_count"] >= 1,
        )
        add(
            "ssh_listener_scopes_valid",
            all(
                item["scope"]
                in {
                    "loopback",
                    "wildcard",
                    "non_loopback",
                    "unknown",
                }
                for item in ssh_listener["listeners"]
            ),
        )
        add(
            "ssh_listener_port_exact",
            all(
                item["port"] == 22
                for item in ssh_listener["listeners"]
            ),
        )

        # SSH daemon/config policy: 15.
        add(
            "sshd_config_exists",
            sshd["main_config_exists"] is True,
        )
        add(
            "sshd_config_readable",
            sshd["main_config_readable"] is True,
        )
        add(
            "sshd_config_path_count_positive",
            sshd["config_path_count"] >= 1,
        )
        add(
            "selected_directive_keys_exact",
            set(
                sshd[
                    "configured_directives"
                ]
            )
            == set(self.SELECTED_SSH_DIRECTIVES),
        )
        add(
            "directive_values_strings",
            all(
                isinstance(value, str)
                for values in sshd[
                    "configured_directives"
                ].values()
                for value in values
            ),
        )
        add(
            "effective_policy_execution_disabled",
            sshd[
                "effective_policy_execution_enabled"
            ]
            is False,
        )
        add(
            "sshd_binary_candidate_count_nonnegative",
            sshd[
                "sshd_binary_candidate_count"
            ]
            >= 0,
        )
        add(
            "gatewayports_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["gatewayports"]
            ),
        )
        add(
            "allowtcpforwarding_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["allowtcpforwarding"]
            ),
        )
        add(
            "permitopen_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["permitopen"]
            ),
        )
        add(
            "permitrootlogin_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["permitrootlogin"]
            ),
        )
        add(
            "passwordauthentication_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["passwordauthentication"]
            ),
        )
        add(
            "pubkeyauthentication_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["pubkeyauthentication"]
            ),
        )
        add(
            "x11forwarding_state_valid",
            self._state_valid(
                tunnel[
                    "directive_states"
                ]["x11forwarding"]
            ),
        )
        add(
            "ssh_tunnel_policy_state_valid",
            self._state_valid(
                tunnel["state"]
            ),
        )

        # SSH metadata: 10.
        add(
            "ssh_directory_exists_bool",
            isinstance(
                ssh_files[
                    "ssh_directory_exists"
                ],
                bool,
            ),
        )
        add(
            "ssh_directory_mode_valid",
            (
                ssh_files["ssh_directory_mode"]
                is None
                or isinstance(
                    ssh_files[
                        "ssh_directory_mode"
                    ],
                    int,
                )
            ),
        )
        add(
            "ssh_directory_owner_bool",
            isinstance(
                ssh_files[
                    "ssh_directory_owner_is_current_user"
                ],
                bool,
            ),
        )
        add(
            "ssh_file_count_nonnegative",
            ssh_files["ssh_file_count"] >= 0,
        )
        add(
            "private_key_candidate_count_nonnegative",
            ssh_files[
                "private_key_candidate_count"
            ]
            >= 0,
        )
        add(
            "private_key_modes_secure_bool",
            isinstance(
                ssh_files[
                    "private_key_modes_secure"
                ],
                bool,
            ),
        )
        add(
            "authorized_keys_metadata_bool",
            isinstance(
                ssh_files[
                    "authorized_keys_metadata"
                ]["exists"],
                bool,
            ),
        )
        add(
            "known_hosts_metadata_bool",
            isinstance(
                ssh_files[
                    "known_hosts_metadata"
                ]["exists"],
                bool,
            ),
        )
        add(
            "private_key_content_not_read",
            ssh_files[
                "private_key_content_read"
            ]
            is False,
        )
        add(
            "credential_content_not_read",
            ssh_files[
                "credential_content_read"
            ]
            is False,
        )

        # Firewall metadata: 5.
        add(
            "firewall_state_valid",
            self._state_valid(
                firewall["state"]
            ),
        )
        add(
            "ufw_config_exists_bool",
            isinstance(
                firewall["ufw_config_exists"],
                bool,
            ),
        )
        add(
            "ufw_unit_visible_bool",
            isinstance(
                firewall["ufw_unit_visible"],
                bool,
            ),
        )
        add(
            "firewall_rules_not_read",
            firewall["rules_content_read"]
            is False,
        )
        add(
            "firewall_visibility_metadata_only",
            firewall[
                "visibility_metadata_only"
            ]
            is True,
        )

        # Dimensions and counts: 10.
        add(
            "dimension_ids_exact",
            set(dimension_map) == expected_ids,
        )
        add(
            "dimension_states_valid",
            all(
                self._state_valid(item["state"])
                for item in dimensions
            ),
        )
        add(
            "dimension_count_exact",
            len(dimensions) == 8,
        )
        add(
            "overall_equals_worst",
            packet["overall_state"]
            == self._worst_state(
                [
                    item["state"]
                    for item in dimensions
                ]
            ),
        )
        add(
            "secure_count_consistent",
            packet["state_counts"]["secure"]
            == sum(
                item["state"] == "secure"
                for item in dimensions
            ),
        )
        add(
            "review_count_consistent",
            packet["state_counts"]["review"]
            == sum(
                item["state"] == "review"
                for item in dimensions
            ),
        )
        add(
            "warning_count_consistent",
            packet["state_counts"]["warning"]
            == sum(
                item["state"] == "warning"
                for item in dimensions
            ),
        )
        add(
            "unavailable_count_consistent",
            packet[
                "state_counts"
            ]["unavailable"]
            == sum(
                item["state"] == "unavailable"
                for item in dimensions
            ),
        )
        add(
            "health_count_sum",
            sum(packet["state_counts"].values())
            == len(dimensions),
        )
        add(
            "findings_count_consistent",
            packet["finding_count"]
            == sum(
                item["state"] != "secure"
                for item in dimensions
            ),
        )

        # Runtime mutation boundary: 10.
        add(
            "config_mutation_disabled",
            runtime["config_mutation_enabled"]
            is False,
        )
        add(
            "ssh_config_mutation_disabled",
            runtime[
                "ssh_config_mutation_enabled"
            ]
            is False,
        )
        add(
            "firewall_mutation_disabled",
            runtime[
                "firewall_mutation_enabled"
            ]
            is False,
        )
        add(
            "sshd_restart_disabled",
            runtime["sshd_restart_enabled"]
            is False,
        )
        add(
            "service_activation_disabled",
            runtime[
                "service_activation_enabled"
            ]
            is False,
        )
        add(
            "socket_activation_disabled",
            runtime[
                "socket_activation_enabled"
            ]
            is False,
        )
        add(
            "network_connection_disabled",
            runtime[
                "network_connection_enabled"
            ]
            is False,
        )
        add(
            "process_control_disabled",
            runtime["process_control_enabled"]
            is False,
        )
        add(
            "key_generation_disabled",
            runtime["key_generation_enabled"]
            is False,
        )
        add(
            "systemd_mutation_disabled",
            runtime[
                "systemd_mutation_enabled"
            ]
            is False,
        )

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
            "review_mode": self.REVIEW_MODE,
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
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            "expected_aura_host": (
                self.EXPECTED_AURA_HOST
            ),
            "expected_aura_port": (
                self.EXPECTED_AURA_PORT
            ),
            "expected_tunnel_destination": (
                self.EXPECTED_TUNNEL_DESTINATION
            ),
            "aura_listener_count": listener[
                "listener_count"
            ],
            "aura_non_loopback_listener_count": (
                listener[
                    "non_loopback_listener_count"
                ]
            ),
            "ssh_listener_count": ssh_listener[
                "listener_count"
            ],
            "ssh_wildcard_listener_count": (
                ssh_listener[
                    "wildcard_listener_count"
                ]
            ),
            "strict_python_main_process_count": (
                activation[
                    "strict_python_main_process_count"
                ]
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
