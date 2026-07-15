"""Canonical read-only Sprint 243 configuration-integrity planner."""

from __future__ import annotations

import hashlib
import stat
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


class AuraConfigurationIntegrityPlanner:
    """Validate canonical settings without mutating configuration."""

    VERSION = "1.0.3-genesis"
    CANONICAL_ANCHOR_VERSION = "1.0.2-genesis"
    CURRENT_SPRINT = 243
    NEXT_SPRINT = 244
    BOUNDARY = "configuration_integrity"
    NEXT_BOUNDARY = "session_memory_persistence_checks"
    EXPECTED_ASSERTION_COUNT = 61
    MAX_SETTINGS_BYTES = 65_536

    EXPECTED_TOP_LEVEL_KEYS = frozenset(
        {
            "app",
            "server",
            "paths",
            "boot",
            "reasoning",
            "local_web_runtime",
        }
    )

    EXPECTED_SECTION_KEYS = {
        "app": frozenset(
            {
                "name",
                "environment",
                "debug",
            }
        ),
        "server": frozenset(
            {
                "name",
                "role",
            }
        ),
        "paths": frozenset(
            {
                "logs",
                "data",
            }
        ),
        "boot": frozenset(
            {
                "show_banner",
                "enable_logger",
            }
        ),
        "reasoning": frozenset(
            {
                "provider",
                "host",
                "model",
                "timeout",
            }
        ),
        "local_web_runtime": frozenset(
            {
                "host",
                "port",
                "mode",
                "require_explicit_confirmation",
            }
        ),
    }

    SECRET_KEY_TOKENS = (
        "secret",
        "token",
        "password",
        "credential",
        "api_key",
        "apikey",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()
        self.settings_path = (
            self.project_root
            / "aura"
            / "config"
            / "settings.yaml"
        )

    @staticmethod
    def _mapping(
        value: object,
    ) -> dict[str, Any]:
        if not isinstance(value, dict):
            return {}

        return {
            str(key): item
            for key, item in value.items()
        }

    @classmethod
    def _contains_secret_key(
        cls,
        value: object,
    ) -> bool:
        if isinstance(value, dict):
            for key, child in value.items():
                normalized = str(key).casefold()

                if any(
                    token in normalized
                    for token in cls.SECRET_KEY_TOKENS
                ):
                    return True

                if cls._contains_secret_key(child):
                    return True

        elif isinstance(value, list):
            return any(
                cls._contains_secret_key(item)
                for item in value
            )

        return False

    @staticmethod
    def _safe_relative_path(
        value: object,
    ) -> bool:
        if not isinstance(value, str):
            return False

        normalized = value.strip().replace("\\", "/")

        if not normalized:
            return False

        path = PurePosixPath(normalized)

        if path.is_absolute():
            return False

        if any(
            part in {"", ".", ".."}
            for part in path.parts
        ):
            return False

        return True

    @staticmethod
    def _integer(
        value: object,
    ) -> bool:
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
        )

    @staticmethod
    def _packet(
        *,
        source: str,
        checks: dict[str, bool],
        size_bytes: int,
        sha256: str,
    ) -> dict[str, Any]:
        failed_checks = [
            name
            for name, passed in checks.items()
            if not passed
        ]

        return {
            "source": source,
            "valid": not failed_checks,
            "check_count": len(checks),
            "failed_check_count": len(failed_checks),
            "failed_checks": failed_checks,
            "size_bytes": size_bytes,
            "sha256": sha256,
            "checks": checks,
        }

    def _document_checks(
        self,
        text: str,
    ) -> tuple[dict[str, bool], str]:
        checks: dict[str, bool] = {}

        try:
            loaded = yaml.safe_load(text)
        except yaml.YAMLError:
            loaded = None
            parse_success = False
        else:
            parse_success = True

        checks["yaml_parse_success"] = parse_success
        checks["root_mapping"] = isinstance(
            loaded,
            dict,
        )

        root = self._mapping(loaded)

        checks["top_level_keys_exact"] = (
            frozenset(root)
            == self.EXPECTED_TOP_LEVEL_KEYS
        )
        checks["secret_like_keys_absent"] = (
            not self._contains_secret_key(root)
        )

        app = self._mapping(root.get("app"))
        checks["app_mapping"] = bool(app)
        checks["app_keys_exact"] = (
            frozenset(app)
            == self.EXPECTED_SECTION_KEYS["app"]
        )
        checks["app_name_string"] = isinstance(
            app.get("name"),
            str,
        )
        checks["app_name_aura"] = (
            app.get("name") == "AURA"
        )
        checks["app_environment_string"] = isinstance(
            app.get("environment"),
            str,
        )
        checks["app_environment_development"] = (
            app.get("environment") == "development"
        )
        checks["app_debug_true"] = (
            app.get("debug") is True
        )

        server = self._mapping(root.get("server"))
        checks["server_mapping"] = bool(server)
        checks["server_keys_exact"] = (
            frozenset(server)
            == self.EXPECTED_SECTION_KEYS["server"]
        )
        checks["server_name_atlas"] = (
            server.get("name") == "ATLAS"
        )
        checks["server_role_ai_server"] = (
            server.get("role") == "AI Server"
        )

        paths = self._mapping(root.get("paths"))
        checks["paths_mapping"] = bool(paths)
        checks["paths_keys_exact"] = (
            frozenset(paths)
            == self.EXPECTED_SECTION_KEYS["paths"]
        )
        checks["logs_path_string"] = isinstance(
            paths.get("logs"),
            str,
        )
        checks["logs_path_safe_relative"] = (
            self._safe_relative_path(
                paths.get("logs")
            )
        )
        checks["data_path_string"] = isinstance(
            paths.get("data"),
            str,
        )
        checks["data_path_safe_relative"] = (
            self._safe_relative_path(
                paths.get("data")
            )
        )

        boot = self._mapping(root.get("boot"))
        checks["boot_mapping"] = bool(boot)
        checks["boot_keys_exact"] = (
            frozenset(boot)
            == self.EXPECTED_SECTION_KEYS["boot"]
        )
        checks["boot_show_banner_true"] = (
            boot.get("show_banner") is True
        )
        checks["boot_enable_logger_true"] = (
            boot.get("enable_logger") is True
        )

        reasoning = self._mapping(
            root.get("reasoning")
        )
        checks["reasoning_mapping"] = bool(
            reasoning
        )
        checks["reasoning_keys_exact"] = (
            frozenset(reasoning)
            == self.EXPECTED_SECTION_KEYS[
                "reasoning"
            ]
        )
        checks["reasoning_provider_string"] = (
            isinstance(
                reasoning.get("provider"),
                str,
            )
        )
        checks["reasoning_provider_ollama"] = (
            reasoning.get("provider") == "ollama"
        )
        checks["reasoning_host_string"] = (
            isinstance(
                reasoning.get("host"),
                str,
            )
        )
        checks["reasoning_host_local_only"] = (
            reasoning.get("host")
            == "http://localhost:11434"
        )
        checks["reasoning_model_nonempty"] = (
            isinstance(
                reasoning.get("model"),
                str,
            )
            and bool(
                str(
                    reasoning.get("model")
                ).strip()
            )
        )
        timeout = reasoning.get("timeout")
        checks["reasoning_timeout_integer"] = (
            self._integer(timeout)
        )
        checks["reasoning_timeout_range"] = (
            self._integer(timeout)
            and 1 <= int(timeout) <= 300
        )

        local_web = self._mapping(
            root.get("local_web_runtime")
        )
        checks["local_web_mapping"] = bool(
            local_web
        )
        checks["local_web_keys_exact"] = (
            frozenset(local_web)
            == self.EXPECTED_SECTION_KEYS[
                "local_web_runtime"
            ]
        )
        checks["local_web_host_loopback"] = (
            local_web.get("host")
            == "127.0.0.1"
        )
        port = local_web.get("port")
        checks["local_web_port_integer"] = (
            self._integer(port)
        )
        checks["local_web_port_range"] = (
            self._integer(port)
            and 1024 <= int(port) <= 65_535
        )
        checks["local_web_mode_safe_idle"] = (
            local_web.get("mode")
            == "safe_idle"
        )
        checks[
            "local_web_confirmation_true"
        ] = (
            local_web.get(
                "require_explicit_confirmation"
            )
            is True
        )

        return checks, (
            "mapping"
            if isinstance(loaded, dict)
            else type(loaded).__name__
        )

    def validate_text(
        self,
        text: str,
        *,
        source: str = "memory",
    ) -> dict[str, Any]:
        checks, root_type = self._document_checks(
            text
        )
        encoded = text.encode("utf-8")

        packet = self._packet(
            source=source,
            checks=checks,
            size_bytes=len(encoded),
            sha256=hashlib.sha256(
                encoded
            ).hexdigest(),
        )
        packet["root_type"] = root_type
        packet["document_check_count"] = len(
            checks
        )
        return packet

    def validate_path(
        self,
        path: str | Path,
    ) -> dict[str, Any]:
        candidate = Path(path)
        expected = self.settings_path
        resolved = candidate.resolve(
            strict=False
        )

        path_checks = {
            "settings_path_expected": (
                candidate == expected
            ),
            "settings_exists": candidate.exists(),
            "settings_is_file": candidate.is_file(),
            "settings_not_symlink": (
                not candidate.is_symlink()
            ),
            "settings_within_project_root": (
                resolved == self.project_root
                or self.project_root
                in resolved.parents
            ),
            "settings_size_nonzero": (
                candidate.is_file()
                and candidate.stat().st_size > 0
            ),
            "settings_size_bounded": (
                candidate.is_file()
                and candidate.stat().st_size
                <= self.MAX_SETTINGS_BYTES
            ),
            "settings_not_world_writable": (
                candidate.is_file()
                and not bool(
                    stat.S_IMODE(
                        candidate.stat().st_mode
                    )
                    & stat.S_IWOTH
                )
            ),
        }

        if not candidate.is_file():
            return self._packet(
                source=str(candidate),
                checks=path_checks,
                size_bytes=0,
                sha256="",
            )

        raw = candidate.read_bytes()

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
            path_checks[
                "settings_utf8_decodable"
            ] = False
        else:
            path_checks[
                "settings_utf8_decodable"
            ] = True

        document = self.validate_text(
            text,
            source=str(candidate),
        )
        checks = {
            **path_checks,
            **document["checks"],
        }

        packet = self._packet(
            source=str(candidate),
            checks=checks,
            size_bytes=len(raw),
            sha256=hashlib.sha256(
                raw
            ).hexdigest(),
        )
        packet["root_type"] = document.get(
            "root_type",
            "unknown",
        )
        packet["document_check_count"] = (
            document["document_check_count"]
        )
        packet["file_mode_octal"] = (
            f"{stat.S_IMODE(candidate.stat().st_mode):04o}"
        )
        return packet

    def validate(
        self,
    ) -> dict[str, Any]:
        return self.validate_path(
            self.settings_path
        )

    def contract(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version": (
                self.CANONICAL_ANCHOR_VERSION
            ),
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "title": "Configuration Integrity",
            "expected_assertion_count": (
                self.EXPECTED_ASSERTION_COUNT
            ),
            "canonical_settings_path": (
                "aura/config/settings.yaml"
            ),
            "validation_mode": (
                "read_only_fail_closed"
            ),
            "consumer_replacement_allowed": False,
            "persistent_configuration_write_allowed": (
                False
            ),
            "environment_mutation_allowed": False,
            "runtime_activation_allowed": False,
            "socket_binding_allowed": False,
            "memory_write_allowed": False,
            "journal_write_allowed": False,
            "systemd_mutation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        validation = self.validate()

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version": (
                self.CANONICAL_ANCHOR_VERSION
            ),
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "settings_path": str(
                self.settings_path
            ),
            "configuration_valid": validation[
                "valid"
            ],
            "configuration_check_count": (
                validation["check_count"]
            ),
            "configuration_failed_check_count": (
                validation["failed_check_count"]
            ),
            "configuration_sha256": (
                validation["sha256"]
            ),
            "read_only_validator_ready": True,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        validation = self.validate()

        return {
            **self.contract(),
            "project_root": str(
                self.project_root
            ),
            "settings_path": str(
                self.settings_path
            ),
            "configuration_validation": validation,
            "source_paths": [
                (
                    "aura/configuration_integrity/"
                    "aura_configuration_integrity_planner.py"
                ),
                (
                    "aura/configuration_integrity/"
                    "aura_configuration_integrity_alpha_manager.py"
                ),
                (
                    "aura/configuration_integrity/"
                    "aura_configuration_integrity_cli.py"
                ),
                "aura/config/settings.yaml",
            ],
            "known_consumer_policy_variance": [
                "local_web_fail_closed",
                "model_router_empty_mapping_fallback",
                "reasoning_factory_rule_based_fallback",
                "system_status_empty_mapping_fallback",
            ],
            "consumer_mutation_applied": False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "parts": [
                "validate canonical settings path and file safety",
                "validate YAML mapping and exact current schema",
                "enforce local-only and safe-idle boundaries",
                "reject traversal and secret-like configuration keys",
                "preserve existing consumer behavior without mutation",
            ],
            "persistent_configuration_write_allowed": False,
            "runtime_activation_allowed": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        current = self.validate()
        repeated = self.validate()

        canonical_text = (
            self.settings_path.read_text(
                encoding="utf-8"
            )
        )

        missing = self.validate_path(
            self.settings_path.with_name(
                "settings.missing.yaml"
            )
        )
        empty = self.validate_text(
            "",
            source="fixture:empty",
        )
        non_mapping = self.validate_text(
            "- one\n- two\n",
            source="fixture:non_mapping",
        )
        malformed = self.validate_text(
            "app: [\n",
            source="fixture:malformed",
        )
        unsafe_host = self.validate_text(
            canonical_text.replace(
                "host: 127.0.0.1",
                "host: 0.0.0.0",
                1,
            ),
            source="fixture:unsafe_host",
        )
        confirmation_false = self.validate_text(
            canonical_text.replace(
                (
                    "require_explicit_confirmation: "
                    "true"
                ),
                (
                    "require_explicit_confirmation: "
                    "false"
                ),
                1,
            ),
            source="fixture:confirmation_false",
        )
        traversal = self.validate_text(
            canonical_text.replace(
                "logs: logs",
                "logs: ../logs",
                1,
            ),
            source="fixture:traversal",
        )
        secret_key = self.validate_text(
            canonical_text
            + "\napi_key: forbidden\n",
            source="fixture:secret_key",
        )

        assertions = dict(
            current["checks"]
        )

        if len(assertions) != 50:
            raise RuntimeError(
                "Canonical configuration check catalog "
                f"must contain 50 checks, got "
                f"{len(assertions)}."
            )

        assertions.update(
            {
                "current_configuration_valid": (
                    current["valid"] is True
                ),
                "current_configuration_errors_zero": (
                    current[
                        "failed_check_count"
                    ]
                    == 0
                ),
                "repeated_validation_deterministic": (
                    current == repeated
                ),
                "missing_settings_rejected": (
                    missing["valid"] is False
                ),
                "empty_settings_rejected": (
                    empty["valid"] is False
                ),
                "non_mapping_settings_rejected": (
                    non_mapping["valid"] is False
                ),
                "malformed_yaml_rejected": (
                    malformed["valid"] is False
                ),
                "unsafe_web_host_rejected": (
                    unsafe_host["valid"] is False
                    and (
                        "local_web_host_loopback"
                        in unsafe_host[
                            "failed_checks"
                        ]
                    )
                ),
                "confirmation_false_rejected": (
                    confirmation_false[
                        "valid"
                    ]
                    is False
                    and (
                        "local_web_confirmation_true"
                        in confirmation_false[
                            "failed_checks"
                        ]
                    )
                ),
                "traversal_path_rejected": (
                    traversal["valid"] is False
                    and (
                        "logs_path_safe_relative"
                        in traversal[
                            "failed_checks"
                        ]
                    )
                ),
                "secret_like_key_rejected": (
                    secret_key["valid"] is False
                    and (
                        "secret_like_keys_absent"
                        in secret_key[
                            "failed_checks"
                        ]
                    )
                ),
            }
        )

        failed_assertions = [
            name
            for name, passed in assertions.items()
            if not passed
        ]

        assertion_count = len(assertions)
        failed_assertion_count = len(
            failed_assertions
        )

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version": (
                self.CANONICAL_ANCHOR_VERSION
            ),
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": assertion_count,
            "failed_assertion_count": (
                failed_assertion_count
            ),
            "failed_assertions": failed_assertions,
            "assertions": assertions,
            "expected_assertion_count": (
                self.EXPECTED_ASSERTION_COUNT
            ),
            "assertion_count_preserved": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
            ),
            "configuration_validation": current,
            "planning_ready": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
                and failed_assertion_count == 0
            ),
            "alpha_ready": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
                and failed_assertion_count == 0
            ),
            "persistent_configuration_write_allowed": (
                False
            ),
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }


__all__ = [
    "AuraConfigurationIntegrityPlanner",
]
