"""Guarded ORION adapter for Sprint 282 supported-game detection."""

from __future__ import annotations

import base64
import hashlib
import json
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from .aura_supported_game_detection_runtime_manager import (
    AuraSupportedGameDetectionRuntimeManager,
    SupportedGameDetectionRuntimeError,
)


class AuraWindowsSupportedGameDetectionAdapter:
    """Perform one explicit local Windows scan and export only matches."""

    SCAN_TIMEOUT_SECONDS = 5
    MAX_LOCAL_ROWS = 32

    def __init__(
        self,
        *,
        manager: AuraSupportedGameDetectionRuntimeManager,
        enabled: bool = False,
        platform_name: str | None = None,
        runner: Callable[[tuple[str, ...]], Sequence[Mapping[str, Any]]]
        | None = None,
        now_provider: Callable[[], datetime] | None = None,
        monotonic_ms_provider: Callable[[], int] | None = None,
    ) -> None:
        self.manager = manager
        self.enabled = bool(enabled)
        self.platform_name = (
            platform_name or platform.system()
        ).strip().casefold()
        self._runner = runner or self._run_powershell
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._monotonic_ms_provider = monotonic_ms_provider or (
            lambda: int(time.monotonic() * 1000)
        )
        self.background_scan_active = False

    def _active_basename_map(self) -> dict[str, dict[str, Any]]:
        mapping: dict[str, dict[str, Any]] = {}
        for profile in self.manager.detection_profiles():
            for basename in profile["executable_basenames"]:
                mapping[basename.casefold()] = profile
        return mapping

    def build_powershell_script(self) -> str:
        """Build a local-only script filtered by exact process basename."""

        names = sorted(self._active_basename_map())
        quoted = ", ".join(
            "'" + item.replace("'", "''") + "'" for item in names
        )
        return (
            "$ErrorActionPreference = 'Stop'\n"
            f"$allowed = @({quoted})\n"
            "$records = @()\n"
            "Get-Process -ErrorAction SilentlyContinue | ForEach-Object {\n"
            "  $basename = ([string]$_.ProcessName) + '.exe'\n"
            "  if ($allowed -contains $basename.ToLowerInvariant()) {\n"
            "    $visible = ($_.MainWindowHandle -ne 0)\n"
            "    $title = ''\n"
            "    if ($visible) { $title = [string]$_.MainWindowTitle }\n"
            "    $records += [PSCustomObject]@{\n"
            "      process_id = [int64]$_.Id\n"
            "      executable_basename = $basename\n"
            "      visible_window = [bool]$visible\n"
            "      window_title = $title\n"
            "    }\n"
            "  }\n"
            "}\n"
            "@($records) | ConvertTo-Json -Compress -Depth 4\n"
        )

    def _run_powershell(
        self,
        allowed_basenames: tuple[str, ...],
    ) -> Sequence[Mapping[str, Any]]:
        del allowed_basenames
        executable = shutil.which("powershell.exe") or shutil.which(
            "pwsh.exe"
        )
        if not executable:
            raise SupportedGameDetectionRuntimeError(
                "PowerShell executable is unavailable on ORION."
            )
        encoded = base64.b64encode(
            self.build_powershell_script().encode("utf-16le")
        ).decode("ascii")
        completed = subprocess.run(
            [
                executable,
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-EncodedCommand",
                encoded,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=self.SCAN_TIMEOUT_SECONDS,
            shell=False,
        )
        if completed.returncode != 0:
            message = (completed.stderr or "").strip()
            if len(message) > 256:
                message = message[:256]
            raise SupportedGameDetectionRuntimeError(
                "PowerShell supported-game scan failed closed"
                + (f": {message}" if message else ".")
            )
        raw = completed.stdout.strip()
        if not raw:
            return []
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SupportedGameDetectionRuntimeError(
                "PowerShell supported-game output was not JSON."
            ) from exc
        if isinstance(payload, Mapping):
            return [payload]
        if isinstance(payload, list):
            return payload
        raise SupportedGameDetectionRuntimeError(
            "PowerShell supported-game output shape is invalid."
        )

    def _normalize_rows(
        self,
        rows: Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        if isinstance(rows, (str, bytes)) or len(rows) > self.MAX_LOCAL_ROWS:
            raise SupportedGameDetectionRuntimeError(
                "Local detection rows are not bounded."
            )
        basename_map = self._active_basename_map()
        normalized: list[dict[str, Any]] = []
        seen: set[tuple[str, int]] = set()

        for row in rows:
            if not isinstance(row, Mapping):
                continue
            basename_raw = row.get("executable_basename")
            if not isinstance(basename_raw, str):
                continue
            profile = basename_map.get(basename_raw.casefold())
            if profile is None:
                continue

            process_id = row.get("process_id")
            if (
                isinstance(process_id, bool)
                or not isinstance(process_id, int)
                or not 1 <= process_id <= self.manager.MAX_PROCESS_ID
            ):
                continue
            visible = row.get("visible_window")
            if not isinstance(visible, bool):
                continue
            if profile["require_visible_top_level_window"] and not visible:
                continue

            key = (profile["game_id"], process_id)
            if key in seen:
                continue
            seen.add(key)

            title = row.get("window_title", "")
            if not isinstance(title, str):
                title = ""
            if len(title) > 1024:
                title = title[:1024]
            title_digest = (
                hashlib.sha256(title.encode("utf-8")).hexdigest()
                if title
                else None
            )
            normalized.append(
                {
                    "game_id": profile["game_id"],
                    "profile_version": profile["profile_version"],
                    "executable_basename": basename_raw,
                    "process_id": process_id,
                    "visible_top_level_window": visible,
                    "window_title_sha256": title_digest,
                    "process_name_exact": True,
                }
            )
        normalized.sort(
            key=lambda item: (
                item["game_id"],
                item["process_id"],
            )
        )
        return normalized[: self.manager.MAX_MATCHES]

    def scan_once(
        self,
        *,
        agent_id: str,
        device_id: str,
        sequence: int,
    ) -> dict[str, Any]:
        """Run one explicit read-only scan; never start a background loop."""

        if not self.enabled:
            raise SupportedGameDetectionRuntimeError(
                "The Windows detection adapter is disabled."
            )
        if self.platform_name not in {"windows", "win32"}:
            raise SupportedGameDetectionRuntimeError(
                "The Windows detection adapter can only run on Windows."
            )

        allowed = tuple(sorted(self._active_basename_map()))
        try:
            rows = self._runner(allowed)
        except SupportedGameDetectionRuntimeError:
            raise
        except subprocess.TimeoutExpired as exc:
            raise SupportedGameDetectionRuntimeError(
                "Supported-game scan timed out."
            ) from exc
        except Exception as exc:
            raise SupportedGameDetectionRuntimeError(
                "Supported-game scan failed closed."
            ) from exc

        matches = self._normalize_rows(rows)
        observed = self.manager._format_utc(self._now_provider())
        monotonic_ms = self._monotonic_ms_provider()
        return self.manager.build_observation_packet(
            agent_id=agent_id,
            device_id=device_id,
            sequence=sequence,
            observed_at_utc=observed,
            monotonic_ms=monotonic_ms,
            matches=matches,
        )
