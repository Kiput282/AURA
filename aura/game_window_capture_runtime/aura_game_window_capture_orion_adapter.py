"""Guarded Windows adapter for Sprint 283 one-shot game-window capture."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from .aura_game_window_capture_runtime_manager import (
    AuraGameWindowCaptureRuntimeManager,
    GameWindowCaptureRuntimeError,
)


class AuraWindowsGameWindowCaptureAdapter:
    """Capture one exact reviewed game window into a temporary private PNG."""

    CAPTURE_TIMEOUT_SECONDS = 10

    def __init__(
        self,
        *,
        manager: AuraGameWindowCaptureRuntimeManager,
        capture_root: Path,
        enabled: bool = False,
        platform_name: str | None = None,
        runner: Callable[
            [Mapping[str, Any], Path],
            Mapping[str, Any],
        ]
        | None = None,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.manager = manager
        self.capture_root = Path(capture_root).expanduser().resolve()
        self.enabled = bool(enabled)
        self.platform_name = (
            platform_name or platform.system()
        ).strip().casefold()
        self._runner = runner or self._run_powershell
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self.capture_active = False

    @staticmethod
    def _powershell_quote(value: str) -> str:
        return "'" + value.replace("'", "''") + "'"

    def build_powershell_script(
        self,
        request: Mapping[str, Any],
        *,
        output_path: Path | None = None,
    ) -> str:
        """Build an exact-PID, exact-executable, selected-window script."""
        validated = self.manager.validate_capture_request(
            request,
            require_issued_permission=False,
        )
        path = (
            Path(output_path)
            if output_path is not None
            else self.capture_root
            / f"{validated['request_id']}.png"
        )
        pid = int(validated["process_id"])
        executable = self._powershell_quote(
            str(validated["executable_basename"])
        )
        output = self._powershell_quote(str(path))
        max_width = int(validated["max_width"])
        max_height = int(validated["max_height"])
        max_pixels = int(validated["max_pixels"])
        max_bytes = int(validated["max_encoded_bytes"])
        return f"""
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class AuraSprint283Window {{
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {{
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }}
    [DllImport("user32.dll", SetLastError=true)]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
}}
'@
$expectedExe = {executable}
$outputPath = {output}
$process = Get-Process -Id {pid} -ErrorAction Stop
$actualExe = ([string]$process.ProcessName) + '.exe'
if (-not $actualExe.Equals(
    $expectedExe,
    [System.StringComparison]::OrdinalIgnoreCase
)) {{
    throw 'Target process executable changed.'
}}
$handle = $process.MainWindowHandle
if ($handle -eq [IntPtr]::Zero) {{
    throw 'Target game window is unavailable.'
}}
$rect = New-Object AuraSprint283Window+RECT
if (-not [AuraSprint283Window]::GetWindowRect($handle, [ref]$rect)) {{
    throw 'Unable to read selected game-window bounds.'
}}
$width = [int]($rect.Right - $rect.Left)
$height = [int]($rect.Bottom - $rect.Top)
if ($width -lt 1 -or $height -lt 1) {{
    throw 'Selected game-window dimensions are invalid.'
}}
if ($width -gt {max_width} -or $height -gt {max_height}) {{
    throw 'Selected game-window dimensions exceed the approved limit.'
}}
if (([int64]$width * [int64]$height) -gt {max_pixels}) {{
    throw 'Selected game-window pixel count exceeds the approved limit.'
}}
if (Test-Path -LiteralPath $outputPath) {{
    throw 'Temporary capture output already exists.'
}}
$directory = Split-Path -Parent $outputPath
[System.IO.Directory]::CreateDirectory($directory) | Out-Null
$bitmap = New-Object System.Drawing.Bitmap(
    $width,
    $height,
    [System.Drawing.Imaging.PixelFormat]::Format32bppArgb
)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {{
    $graphics.CopyFromScreen(
        $rect.Left,
        $rect.Top,
        0,
        0,
        (New-Object System.Drawing.Size($width, $height)),
        [System.Drawing.CopyPixelOperation]::SourceCopy
    )
    $bitmap.Save(
        $outputPath,
        [System.Drawing.Imaging.ImageFormat]::Png
    )
}}
finally {{
    $graphics.Dispose()
    $bitmap.Dispose()
}}
$file = Get-Item -LiteralPath $outputPath -ErrorAction Stop
if ($file.Length -gt {max_bytes}) {{
    Remove-Item -LiteralPath $outputPath -Force -ErrorAction SilentlyContinue
    throw 'Temporary capture exceeds the approved byte limit.'
}}
[ordered]@{{
    status = 'captured'
    process_id = [int64]$process.Id
    executable_basename = $actualExe
    window_handle_nonzero = $true
    screen_fallback_used = $false
    width = $width
    height = $height
}} | ConvertTo-Json -Compress
""".strip()

    def _run_powershell(
        self,
        request: Mapping[str, Any],
        output_path: Path,
    ) -> Mapping[str, Any]:
        executable = shutil.which("powershell.exe") or shutil.which(
            "pwsh.exe"
        )
        if executable is None:
            raise GameWindowCaptureRuntimeError(
                "PowerShell is unavailable on ORION."
            )
        script = self.build_powershell_script(
            request,
            output_path=output_path,
        )
        encoded = base64.b64encode(
            script.encode("utf-16le")
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
            timeout=self.CAPTURE_TIMEOUT_SECONDS,
            shell=False,
        )
        if completed.returncode != 0:
            message = (completed.stderr or "").strip()
            if len(message) > 256:
                message = message[:256]
            raise GameWindowCaptureRuntimeError(
                "PowerShell game-window capture failed closed"
                + (f": {message}" if message else ".")
            )
        raw = completed.stdout.strip()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GameWindowCaptureRuntimeError(
                "PowerShell game-window capture output is not JSON."
            ) from exc
        if not isinstance(payload, Mapping):
            raise GameWindowCaptureRuntimeError(
                "PowerShell game-window capture output is invalid."
            )
        return payload

    def _guard(self) -> None:
        if not self.enabled:
            raise GameWindowCaptureRuntimeError(
                "The game-window capture adapter is disabled."
            )
        if self.platform_name not in {"windows", "win32"}:
            raise GameWindowCaptureRuntimeError(
                "The game-window capture adapter can only run on Windows."
            )
        if self.capture_active:
            raise GameWindowCaptureRuntimeError(
                "A game-window capture is already active."
            )

    def _output_path(
        self,
        request: Mapping[str, Any],
    ) -> Path:
        self.capture_root.mkdir(parents=True, exist_ok=True)
        if self.capture_root.is_symlink():
            raise GameWindowCaptureRuntimeError(
                "Capture root must not be a symlink."
            )
        request_id = str(request["request_id"])
        path = (self.capture_root / f"{request_id}.png").resolve()
        try:
            path.relative_to(self.capture_root)
        except ValueError as exc:
            raise GameWindowCaptureRuntimeError(
                "Capture output escaped the configured root."
            ) from exc
        if path.suffix.casefold() != ".png":
            raise GameWindowCaptureRuntimeError(
                "Capture output must use .png."
            )
        if path.exists():
            raise GameWindowCaptureRuntimeError(
                "Capture output already exists."
            )
        return path

    def capture_once(
        self,
        request: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Execute exactly one selected-window capture."""
        self._guard()
        validated = self.manager.validate_capture_request(
            request,
            require_issued_permission=False,
        )
        if validated["frame_limit"] != 1:
            raise GameWindowCaptureRuntimeError(
                "The adapter accepts one frame only."
            )
        output_path = self._output_path(validated)
        started = time.monotonic()
        self.capture_active = True
        try:
            result = self._runner(validated, output_path)
            if not isinstance(result, Mapping):
                raise GameWindowCaptureRuntimeError(
                    "Capture backend result is invalid."
                )
            if (
                result.get("status") != "captured"
                or result.get("process_id") != validated["process_id"]
                or str(
                    result.get("executable_basename", "")
                ).casefold()
                != str(validated["executable_basename"]).casefold()
                or result.get("window_handle_nonzero") is not True
                or result.get("screen_fallback_used") is not False
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture backend target binding changed."
                )
            if not output_path.is_file() or output_path.is_symlink():
                raise GameWindowCaptureRuntimeError(
                    "Capture backend did not create a regular PNG."
                )
            data = output_path.read_bytes()
            if len(data) > validated["max_encoded_bytes"]:
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact exceeds the approved byte limit."
                )
            width, height = self.manager.parse_png_dimensions(data)
            if (
                width > validated["max_width"]
                or height > validated["max_height"]
                or width * height > validated["max_pixels"]
            ):
                raise GameWindowCaptureRuntimeError(
                    "Capture artifact dimensions exceed the approved limit."
                )
            if result.get("width") != width or result.get("height") != height:
                raise GameWindowCaptureRuntimeError(
                    "Capture backend dimensions do not match the PNG."
                )
            digest = hashlib.sha256(data).hexdigest()
            artifact_id = (
                "game-capture-"
                + digest[:24]
            )
            receipt = self.manager.build_capture_receipt(
                validated,
                captured_at_utc=self.manager._format_utc(
                    self._now_provider().astimezone(timezone.utc)
                ),
                artifact_id=artifact_id,
                artifact_sha256=digest,
                size_bytes=len(data),
                width=width,
                height=height,
                capture_succeeded=True,
            )
            return {
                "status": "capture_created",
                "receipt": receipt,
                "local_artifact_path": str(output_path),
                "duration_ms": int(
                    (time.monotonic() - started) * 1000
                ),
                "raw_bytes_returned": False,
                "path_in_receipt": False,
            }
        except subprocess.TimeoutExpired as exc:
            if output_path.exists():
                output_path.unlink(missing_ok=True)
            raise GameWindowCaptureRuntimeError(
                "Game-window capture timed out."
            ) from exc
        except Exception:
            if output_path.exists():
                output_path.unlink(missing_ok=True)
            raise
        finally:
            self.capture_active = False

    def cleanup_once(
        self,
        receipt: Mapping[str, Any],
        *,
        local_artifact_path: Path,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != self.manager.CLEANUP_CONFIRMATION:
            raise GameWindowCaptureRuntimeError(
                "Exact cleanup confirmation is required."
            )
        validated = self.manager.validate_capture_receipt(receipt)
        artifact = validated["artifact"]
        if artifact is None:
            raise GameWindowCaptureRuntimeError(
                "Cleanup requires a successful capture artifact."
            )
        path = Path(local_artifact_path).expanduser().resolve()
        try:
            path.relative_to(self.capture_root)
        except ValueError as exc:
            raise GameWindowCaptureRuntimeError(
                "Cleanup path escaped the configured capture root."
            ) from exc
        if not path.is_file() or path.is_symlink():
            raise GameWindowCaptureRuntimeError(
                "Cleanup target is not a regular artifact."
            )
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != artifact["sha256"]:
            raise GameWindowCaptureRuntimeError(
                "Cleanup target digest mismatch."
            )
        path.unlink()
        return self.manager.build_cleanup_receipt(
            request_id=validated["request_id"],
            artifact_id=artifact["artifact_id"],
            artifact_sha256=artifact["sha256"],
            deleted=not path.exists(),
            cleanup_at_utc=self.manager._format_utc(
                self._now_provider().astimezone(timezone.utc)
            ),
        )

    def status(self) -> dict[str, Any]:
        is_windows = self.platform_name in {"windows", "win32"}
        return {
            "status": (
                "ready"
                if self.enabled and is_windows
                else "guarded"
            ),
            "enabled": self.enabled,
            "platform": self.platform_name,
            "capture_root": str(self.capture_root),
            "capture_active": self.capture_active,
            "one_shot_only": True,
            "selected_window_only": True,
            "full_screen_fallback": False,
            "continuous_capture": False,
            "audio_capture": False,
            "recording": False,
            "telemetry": False,
            "coaching": False,
            "game_input_control": False,
            "raw_bytes_returned": False,
            "path_exported_to_atlas": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "adapter": "AuraWindowsGameWindowCaptureAdapter",
            "expected_platform": "windows",
            "backend": "PowerShell_System.Drawing_CopyFromScreen",
            "target_binding": [
                "exact process_id",
                "exact executable_basename",
                "nonzero MainWindowHandle",
                "GetWindowRect selected-window bounds",
            ],
            "limits": {
                "one_frame": True,
                "PNG_only": True,
                "timeout_seconds": self.CAPTURE_TIMEOUT_SECONDS,
                "max_dimensions_from_request": True,
                "max_pixels_from_request": True,
                "max_bytes_from_request": True,
            },
            "privacy": {
                "raw_window_title_read": False,
                "raw_window_title_exported": False,
                "raw_image_bytes_to_atlas": False,
                "local_path_to_atlas": False,
                "temporary_private_storage": True,
            },
        }
