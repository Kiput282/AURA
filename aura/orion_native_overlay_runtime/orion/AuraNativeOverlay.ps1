#requires -Version 5.1
<#
AURA Sprint 288 native ORION overlay foundation.

Default mode is Inspect and never shows a window. PreviewSafeIdle requires an
exact approval and shows only a bounded synthetic SAFE_IDLE status. There is no
live orchestration binding, session control, quick-stop execution, emergency
stop execution, game-process enumeration, capture, input read, input hook,
input injection, raw media rendering, or network listener in Sprint 288.
#>

[CmdletBinding()]
param(
    [ValidateSet("Inspect", "PreviewSafeIdle")]
    [string]$Mode = "Inspect",

    [string]$Approval = "",

    [ValidateSet("compact", "normal", "expanded")]
    [string]$ViewProfile = "normal",

    [ValidateRange(1, 15)]
    [int]$DurationSeconds = 5,

    [ValidateRange(0, 15)]
    [int]$ScreenIndex = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RequiredPreviewApproval = (
    "APPROVE AURA SPRINT 288 SAFE IDLE OVERLAY PREVIEW"
)
$CapabilityId = "orion.game.overlay.show_operational_status"
$StatusSurface = "ORION_READ_ONLY_OPERATIONAL_STATUS"

$Profiles = @{
    compact = @{
        Width = 360
        Height = 72
        TitleSize = 12.0
        DetailSize = 9.0
    }
    normal = @{
        Width = 440
        Height = 128
        TitleSize = 14.0
        DetailSize = 10.0
    }
    expanded = @{
        Width = 560
        Height = 220
        TitleSize = 16.0
        DetailSize = 11.0
    }
}

function Write-InspectResult {
    $result = [ordered]@{
        schema_version = 1
        sprint = 288
        boundary = "orion_native_overlay_foundation"
        capability_id = $CapabilityId
        status_surface = $StatusSurface
        implementation = (
            "orion_native_powershell_winforms_noactivate_status_overlay"
        )
        powershell_5_1_required = $true
        sta_required = $true
        view_profiles = @("compact", "normal", "expanded")
        default_mode = "Inspect"
        preview_mode = "PreviewSafeIdle"
        preview_requires_exact_approval = $true
        preview_synthetic_safe_idle_only = $true
        preview_duration_min_seconds = 1
        preview_duration_max_seconds = 15
        live_orchestration_status_binding = $false
        session_start = $false
        mode_change = $false
        quick_stop_execution = $false
        emergency_stop_execution = $false
        game_process_enumeration = $false
        window_capture = $false
        audio_capture = $false
        input_telemetry = $false
        input_read = $false
        input_hook = $false
        input_injection = $false
        raw_media_rendering = $false
        network_listener = $false
        overlay_is_authority = $false
        safe_idle = $true
    }

    $result | ConvertTo-Json -Depth 6
}

if ($Mode -ceq "Inspect") {
    Write-InspectResult
    exit 0
}

if ($Approval -cne $RequiredPreviewApproval) {
    throw "Exact approval is required for PreviewSafeIdle."
}

if (
    $PSVersionTable.PSEdition -cne "Desktop" -or
    $PSVersionTable.PSVersion.Major -ne 5 -or
    $PSVersionTable.PSVersion.Minor -ne 1
) {
    throw "Windows PowerShell 5.1 Desktop is required."
}

if (-not [Environment]::Is64BitProcess) {
    throw "A 64-bit PowerShell process is required."
}

if (
    [Threading.Thread]::CurrentThread.GetApartmentState().ToString() -cne
    "STA"
) {
    throw "PreviewSafeIdle requires an STA thread."
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$source = @'
using System;
using System.Windows.Forms;

public sealed class AuraSprint288OverlayForm : Form
{
    public const int WS_EX_NOACTIVATE = unchecked((int)0x08000000);
    public const int WS_EX_TOOLWINDOW = 0x00000080;

    protected override bool ShowWithoutActivation
    {
        get { return true; }
    }

    protected override CreateParams CreateParams
    {
        get
        {
            CreateParams parameters = base.CreateParams;
            parameters.ExStyle |= WS_EX_NOACTIVATE;
            parameters.ExStyle |= WS_EX_TOOLWINDOW;
            return parameters;
        }
    }
}
'@

Add-Type `
    -TypeDefinition $source `
    -Language CSharp `
    -ReferencedAssemblies @(
        "System.dll",
        "System.Drawing.dll",
        "System.Windows.Forms.dll"
    )

$mutexName = "Local\AURA_S288_Native_Overlay_Foundation"
$createdNew = $false
$mutex = New-Object Threading.Mutex(
    $false,
    $mutexName,
    [ref]$createdNew
)

$acquired = $false
$form = $null
$timer = $null

try {
    $acquired = $mutex.WaitOne(0, $false)
    if (-not $acquired) {
        throw "Another AURA native overlay preview is already running."
    }

    $screens = @([Windows.Forms.Screen]::AllScreens)
    if ($ScreenIndex -ge $screens.Count) {
        throw "ScreenIndex exceeds the available display count."
    }

    $screen = $screens[$ScreenIndex]
    $profile = $Profiles[$ViewProfile]

    $form = New-Object AuraSprint288OverlayForm
    $form.TopMost = $true
    $form.ShowInTaskbar = $false
    $form.FormBorderStyle = (
        [Windows.Forms.FormBorderStyle]::None
    )
    $form.StartPosition = (
        [Windows.Forms.FormStartPosition]::Manual
    )
    $form.AutoScaleMode = [Windows.Forms.AutoScaleMode]::Dpi
    $form.BackColor = [Drawing.Color]::FromArgb(18, 20, 26)
    $form.ForeColor = [Drawing.Color]::White
    $form.Opacity = 0.96
    $form.Width = [int]$profile.Width
    $form.Height = [int]$profile.Height

    $working = $screen.WorkingArea
    $form.Left = [Math]::Max(
        $working.Left,
        $working.Right - $form.Width - 24
    )
    $form.Top = [Math]::Max($working.Top, $working.Top + 24)

    $title = New-Object Windows.Forms.Label
    $title.AutoSize = $true
    $title.Left = 16
    $title.Top = 10
    $title.ForeColor = [Drawing.Color]::White
    $title.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.TitleSize,
        [Drawing.FontStyle]::Bold
    )
    $title.Text = "AURA GAME COMPANION"

    $status = New-Object Windows.Forms.Label
    $status.AutoSize = $true
    $status.Left = 16
    $status.Top = 38
    $status.ForeColor = [Drawing.Color]::FromArgb(84, 214, 255)
    $status.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.DetailSize,
        [Drawing.FontStyle]::Regular
    )
    $status.Text = "SAFE IDLE  |  NO ACTIVE SESSION"

    [void]$form.Controls.Add($title)
    [void]$form.Controls.Add($status)

    if ($ViewProfile -cne "compact") {
        $detail = New-Object Windows.Forms.Label
        $detail.AutoSize = $true
        $detail.Left = 16
        $detail.Top = 68
        $detail.ForeColor = [Drawing.Color]::FromArgb(193, 199, 209)
        $detail.Font = New-Object Drawing.Font(
            "Segoe UI",
            [single]$profile.DetailSize,
            [Drawing.FontStyle]::Regular
        )
        $detail.Text = (
            "Synthetic Sprint 288 preview | " +
            "read-only | no live binding"
        )
        [void]$form.Controls.Add($detail)
    }

    $timer = New-Object Windows.Forms.Timer
    $timer.Interval = $DurationSeconds * 1000
    $timer.Add_Tick({
        $timer.Stop()
        $form.Close()
    })
    $timer.Start()

    [Windows.Forms.Application]::Run($form)
}
finally {
    if ($null -ne $timer) {
        $timer.Stop()
        $timer.Dispose()
    }
    if ($null -ne $form) {
        $form.Dispose()
    }
    if ($acquired) {
        $mutex.ReleaseMutex()
    }
    $mutex.Dispose()
}
