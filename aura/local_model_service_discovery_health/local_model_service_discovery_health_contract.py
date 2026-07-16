from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping
import json
import os
import shutil
import socket
import stat
import subprocess
import urllib.error
import urllib.request

from aura.local_model_bridge_runtime.aura_local_model_bridge_profile_resolver import (
    AuraLocalModelBridgeProfileResolver,
)
from aura.local_model_bridge_runtime.aura_local_model_bridge_runtime_manager import (
    AuraLocalModelBridgeRuntimeManager,
    LocalModelBridgeConfigurationError,
    LocalModelBridgePermissionError,
    LocalModelBridgeResponseError,
    LocalModelBridgeTransportError,
    LocalModelTransportResponse,
    LocalhostHTTPTransport,
)


HealthTransport = Callable[
    [str, str, bytes | None, Mapping[str, str], float],
    LocalModelTransportResponse,
]


class LocalModelServiceDiscoveryHealthContract:
    VERSION = "1.1.7"
    SPRINT = 257
    DEFAULT_PROVIDER = "ollama"
    DEFAULT_ENDPOINT = "http://127.0.0.1:11434"
    DEFAULT_PROBE_PATH = "/api/tags"
    HEALTH_TIMEOUT_SECONDS = 2.0
    CONFIRMATION_TOKEN = "PROBE_LOCAL_MODEL_SERVICE"
    MAX_HEALTH_BODY_BYTES = 1024 * 1024

    def __init__(
        self,
        project_root: str | Path,
        *,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.environ = dict(
            os.environ
            if environ is None
            else environ
        )

    @staticmethod
    def _systemctl_show(
        unit: str,
    ) -> dict[str, Any]:
        completed = subprocess.run(
            [
                "systemctl",
                "show",
                unit,
                "--property=LoadState",
                "--property=UnitFileState",
                "--property=ActiveState",
                "--property=SubState",
                "--property=MainPID",
                "--property=FragmentPath",
                "--no-pager",
            ],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
            env={
                **os.environ,
                "LC_ALL": "C",
            },
        )
        fields: dict[str, str] = {}

        for line in completed.stdout.splitlines():
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            fields[key] = value

        return {
            "exit_code": completed.returncode,
            "stderr_line_count": len(
                completed.stderr.splitlines()
            ),
            "fields": fields,
            "mutation_performed": False,
        }

    @staticmethod
    def _listener_records(
        port: int,
    ) -> list[dict[str, Any]]:
        records = []

        for table in (
            Path("/proc/net/tcp"),
            Path("/proc/net/tcp6"),
        ):
            if not table.is_file():
                continue

            for line in table.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines()[1:]:
                fields = line.split()

                if len(fields) < 10:
                    continue

                local = fields[1]
                state = fields[3]

                if ":" not in local:
                    continue

                address_hex, port_hex = local.rsplit(
                    ":",
                    1,
                )

                try:
                    current_port = int(
                        port_hex,
                        16,
                    )
                except ValueError:
                    continue

                if (
                    current_port != port
                    or state != "0A"
                ):
                    continue

                if table.name == "tcp":
                    loopback = (
                        address_hex.upper()
                        == "0100007F"
                    )
                    wildcard = (
                        address_hex.upper()
                        == "00000000"
                    )
                else:
                    normalized = (
                        address_hex.upper()
                    )
                    loopback = normalized in {
                        "00000000000000000000000001000000",
                        "00000000000000000000000000000001",
                    }
                    wildcard = normalized == (
                        "00000000000000000000000000000000"
                    )

                records.append(
                    {
                        "table": table.name,
                        "port": current_port,
                        "state": "listen",
                        "loopback": loopback,
                        "wildcard": wildcard,
                        "address_redacted": True,
                    }
                )

        return records

    @staticmethod
    def _process_metadata(
        pid: int,
    ) -> dict[str, Any]:
        path = Path(f"/proc/{pid}")

        if pid <= 0 or not path.is_dir():
            return {
                "pid": pid,
                "exists": False,
                "uid": None,
                "comm": None,
                "command_line_exposed": False,
            }

        metadata = path.stat()
        comm = None

        try:
            comm = (
                path
                / "comm"
            ).read_text(
                encoding="utf-8",
                errors="replace",
            ).strip()
        except OSError:
            pass

        return {
            "pid": pid,
            "exists": True,
            "uid": metadata.st_uid,
            "comm": comm,
            "command_line_exposed": False,
        }

    def profile_posture(self) -> dict[str, Any]:
        try:
            status = (
                AuraLocalModelBridgeProfileResolver
                .status(self.environ)
            )
        except LocalModelBridgeConfigurationError as exc:
            return {
                "configured": False,
                "enabled": False,
                "state": "invalid_configuration",
                "error_type": type(exc).__name__,
                "provider": None,
                "base_url": None,
                "model_configured": False,
                "persistent_configuration_write": False,
                "credentials_read": False,
            }

        profile = status.get("profile")
        configured = bool(
            status.get("configured")
        )

        return {
            "configured": configured,
            "enabled": bool(
                status.get("enabled")
            ),
            "state": status.get("status"),
            "provider": (
                profile.get("provider")
                if isinstance(profile, dict)
                else None
            ),
            "base_url": (
                profile.get("base_url")
                if isinstance(profile, dict)
                else None
            ),
            "model_configured": bool(
                isinstance(profile, dict)
                and profile.get("model")
            ),
            "model_name_exposed": False,
            "persistent_configuration_write": False,
            "credentials_read": False,
        }

    def provider_contracts(
        self,
    ) -> dict[str, Any]:
        contracts = (
            AuraLocalModelBridgeRuntimeManager
            .provider_contracts()
        )

        return {
            **contracts,
            "sprint_257_owner": (
                "existing_local_model_bridge_runtime"
            ),
            "default_health_endpoint": (
                self.DEFAULT_ENDPOINT
            ),
            "default_health_path": (
                self.DEFAULT_PROBE_PATH
            ),
            "health_timeout_seconds": (
                self.HEALTH_TIMEOUT_SECONDS
            ),
            "health_probe_default": False,
            "health_confirmation_token": (
                self.CONFIRMATION_TOKEN
            ),
            "model_inventory_metadata_only": True,
        }

    def host_posture(self) -> dict[str, Any]:
        binary = shutil.which("ollama")
        binary_record: dict[str, Any] = {
            "available": binary is not None,
            "path": binary,
            "metadata_only": True,
            "binary_executed": False,
        }

        if binary is not None:
            path = Path(binary)
            metadata = path.stat()
            binary_record.update(
                {
                    "uid": metadata.st_uid,
                    "mode": oct(
                        stat.S_IMODE(
                            metadata.st_mode
                        )
                    ),
                    "size": metadata.st_size,
                    "regular_file": (
                        stat.S_ISREG(
                            metadata.st_mode
                        )
                    ),
                }
            )

        unit = self._systemctl_show(
            "ollama.service"
        )
        fields = unit["fields"]
        raw_pid = fields.get(
            "MainPID",
            "0",
        )

        try:
            pid = int(raw_pid or "0")
        except ValueError:
            pid = 0

        process = self._process_metadata(pid)
        listeners = self._listener_records(
            11434
        )
        loopback_count = sum(
            1
            for item in listeners
            if item["loopback"]
        )
        wildcard_count = sum(
            1
            for item in listeners
            if item["wildcard"]
        )
        active = (
            fields.get("ActiveState")
            == "active"
        )
        loaded = (
            fields.get("LoadState")
            == "loaded"
        )

        if (
            binary_record["available"]
            and loaded
            and active
            and process["exists"]
            and loopback_count >= 1
            and wildcard_count == 0
        ):
            state = "available_unprobed"
        elif (
            binary_record["available"]
            or loaded
            or process["exists"]
            or listeners
        ):
            state = "degraded_unprobed"
        else:
            state = "unavailable"

        return {
            "state": state,
            "provider": self.DEFAULT_PROVIDER,
            "endpoint": self.DEFAULT_ENDPOINT,
            "binary": binary_record,
            "unit": unit,
            "process": process,
            "listeners": listeners,
            "listener_count": len(
                listeners
            ),
            "loopback_listener_count": (
                loopback_count
            ),
            "wildcard_listener_count": (
                wildcard_count
            ),
            "profile": self.profile_posture(),
            "health_probe_performed": False,
            "service_started": False,
            "service_stopped": False,
            "service_installed": False,
            "model_downloaded": False,
            "model_loaded": False,
            "model_unloaded": False,
            "chat_routed": False,
            "network_connection_opened": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }

    def health_preview(self) -> dict[str, Any]:
        posture = self.host_posture()

        return {
            "state": posture["state"],
            "provider": self.DEFAULT_PROVIDER,
            "endpoint": self.DEFAULT_ENDPOINT,
            "probe_path": self.DEFAULT_PROBE_PATH,
            "timeout_seconds": (
                self.HEALTH_TIMEOUT_SECONDS
            ),
            "confirmation_required": True,
            "confirmation_token": (
                self.CONFIRMATION_TOKEN
            ),
            "command": (
                "python3 main.py "
                "local-model-service-health-probe "
                f"{self.CONFIRMATION_TOKEN}"
            ),
            "expected_response": (
                "HTTP 200 JSON object with models list"
            ),
            "returned_model_metadata": (
                "count_only"
            ),
            "health_probe_performed": False,
            "network_connection_opened": False,
            "service_activation_performed": False,
            "model_request_performed": False,
        }

    @classmethod
    def explicit_health_probe(
        cls,
        *,
        confirmation: str,
        transport: HealthTransport | None = None,
        endpoint: str | None = None,
    ) -> dict[str, Any]:
        if confirmation != cls.CONFIRMATION_TOKEN:
            raise LocalModelBridgePermissionError(
                "Local model health probe requires "
                "the exact confirmation token."
            )

        base_url = (
            AuraLocalModelBridgeRuntimeManager
            ._validate_base_url(
                endpoint
                or cls.DEFAULT_ENDPOINT
            )
        )
        url = (
            base_url
            + cls.DEFAULT_PROBE_PATH
        )
        selected_transport = (
            transport
            or LocalhostHTTPTransport()
        )
        response = selected_transport(
            "GET",
            url,
            None,
            {
                "Accept": "application/json",
            },
            cls.HEALTH_TIMEOUT_SECONDS,
        )

        if response.status_code != 200:
            raise LocalModelBridgeTransportError(
                "Local model health probe returned "
                f"HTTP {response.status_code}."
            )

        if len(response.body) > (
            cls.MAX_HEALTH_BODY_BYTES
        ):
            raise LocalModelBridgeResponseError(
                "Local model health response exceeds "
                "the body limit."
            )

        try:
            payload = json.loads(
                response.body.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise LocalModelBridgeResponseError(
                "Local model health response is not "
                "valid UTF-8 JSON."
            ) from exc

        if not isinstance(payload, dict):
            raise LocalModelBridgeResponseError(
                "Local model health response must be "
                "a JSON object."
            )

        models = payload.get("models")

        if not isinstance(models, list):
            raise LocalModelBridgeResponseError(
                "Ollama health response must contain "
                "a models list."
            )

        valid_count = sum(
            1
            for item in models
            if isinstance(item, dict)
            and isinstance(
                item.get("name"),
                str,
            )
        )

        return {
            "state": "healthy",
            "provider": cls.DEFAULT_PROVIDER,
            "endpoint": base_url,
            "available_model_count": (
                valid_count
            ),
            "model_names_exposed": False,
            "local_connection_confirmed": True,
            "health_probe_performed": True,
            "network_connection_opened": True,
            "non_loopback_connection": False,
            "redirect_followed": False,
            "proxy_used": False,
            "model_request_performed": False,
            "service_activation_performed": False,
            "model_downloaded": False,
            "model_loaded": False,
            "chat_routed": False,
        }

    @classmethod
    def isolated_rehearsal(
        cls,
    ) -> dict[str, Any]:
        class FakeTransport:
            def __init__(self) -> None:
                self.calls = []

            def __call__(
                self,
                method: str,
                url: str,
                body: bytes | None,
                headers: Mapping[str, str],
                timeout_seconds: float,
            ) -> LocalModelTransportResponse:
                self.calls.append(
                    {
                        "method": method,
                        "url": url,
                        "body": body,
                        "headers": dict(headers),
                        "timeout_seconds": (
                            timeout_seconds
                        ),
                    }
                )
                return LocalModelTransportResponse(
                    status_code=200,
                    headers={
                        "Content-Type": (
                            "application/json"
                        )
                    },
                    body=json.dumps(
                        {
                            "models": [
                                {
                                    "name": (
                                        "fixture-model-a"
                                    )
                                },
                                {
                                    "name": (
                                        "fixture-model-b"
                                    )
                                },
                                {
                                    "invalid": True,
                                },
                            ]
                        }
                    ).encode("utf-8"),
                )

        fake = FakeTransport()
        denied = False

        try:
            cls.explicit_health_probe(
                confirmation="",
                transport=fake,
            )
        except LocalModelBridgePermissionError:
            denied = True

        result = cls.explicit_health_probe(
            confirmation=(
                cls.CONFIRMATION_TOKEN
            ),
            transport=fake,
        )
        invalid_endpoint_rejected = False

        try:
            cls.explicit_health_probe(
                confirmation=(
                    cls.CONFIRMATION_TOKEN
                ),
                transport=fake,
                endpoint=(
                    "http://192.168.100.20:11434"
                ),
            )
        except LocalModelBridgeConfigurationError:
            invalid_endpoint_rejected = True

        return {
            "denied_without_confirmation": denied,
            "confirmed_probe_state": result[
                "state"
            ],
            "available_model_count": result[
                "available_model_count"
            ],
            "model_names_exposed": result[
                "model_names_exposed"
            ],
            "loopback_endpoint": (
                result["endpoint"]
                == cls.DEFAULT_ENDPOINT
            ),
            "invalid_endpoint_rejected": (
                invalid_endpoint_rejected
            ),
            "transport_call_count": len(
                fake.calls
            ),
            "transport_method": (
                fake.calls[0]["method"]
                if fake.calls
                else None
            ),
            "transport_timeout": (
                fake.calls[0][
                    "timeout_seconds"
                ]
                if fake.calls
                else None
            ),
            "canonical_network_opened": False,
            "service_activated": False,
            "model_downloaded": False,
            "model_loaded": False,
            "chat_routed": False,
        }
