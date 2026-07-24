#requires -Version 5.1
<#
AURA Sprint 289 native ORION overlay.

Inspect never shows a window. PreviewSafeIdle retains the bounded Sprint 288
preview. LiveStatus polls one local atomic metadata-only JSON status snapshot,
shows Coach/Observer/Recording/focus/session-time state, and creates reviewed
local request files for quick-stop or emergency-stop-all.

The overlay never authorizes or starts a session, changes mode, executes stop
directly, enumerates game processes, captures media, installs input hooks,
injects input, displays raw media/input, contacts ATLAS, or opens a network
listener.
#>

[CmdletBinding()]
param(
    [ValidateSet("Inspect", "PreviewSafeIdle", "LiveStatus")]
    [string]$Mode = "Inspect",

    [AllowEmptyString()]
    [string]$Approval = "",

    [ValidateSet("compact", "normal", "expanded")]
    [string]$ViewProfile = "normal",

    [ValidateRange(0, 3600)]
    [int]$DurationSeconds = 5,

    [ValidateRange(0, 15)]
    [int]$ScreenIndex = 0,

    [AllowEmptyString()]
    [string]$StatusPath = "",

    [AllowEmptyString()]
    [string]$RequestDirectory = "",

    [AllowEmptyString()]
    [string]$AcknowledgementDirectory = "",

    [AllowEmptyString()]
    [string]$PermissionSnapshotSha256 = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SafeIdleApproval = (
    "APPROVE AURA SPRINT 288 SAFE IDLE OVERLAY PREVIEW"
)
$LiveStatusApproval = (
    "APPROVE AURA SPRINT 289 LIVE STATUS OVERLAY"
)

$CapabilityId = "orion.game.overlay.session_status_integration"
$StatusSurface = "ORION_READ_ONLY_OPERATIONAL_STATUS"
$PollIntervalMilliseconds = 250
$StaleTimeoutMilliseconds = 1500
$RequestExpiryMilliseconds = 5000
$EmergencyHoldMilliseconds = 1500

$Profiles = @{
    compact = @{
        Width = 360
        Height = 72
        TitleSize = 12.0
        DetailSize = 9.0
    }
    normal = @{
        Width = 440
        Height = 176
        TitleSize = 14.0
        DetailSize = 10.0
    }
    expanded = @{
        Width = 560
        Height = 272
        TitleSize = 16.0
        DetailSize = 11.0
    }
}

$AllowedStates = @(
    "SAFE_IDLE",
    "ARMED",
    "WAITING_FOR_FOREGROUND",
    "OBSERVER_ACTIVE",
    "COACH_ACTIVE",
    "COACH_OBSERVER_ACTIVE",
    "COACH_OBSERVER_RECORDING_ACTIVE",
    "PAUSED_FOCUS_LOST",
    "STOPPING",
    "BLOCKED"
)

$AllowedModes = @(
    "coach_only",
    "observer_only",
    "coach_observer",
    "coach_observer_recording"
)

$RequiredStatusFields = @(
    "schema_version",
    "surface",
    "authority",
    "sequence",
    "state",
    "session_id",
    "mode_profile",
    "game_id",
    "game_display_name",
    "coach",
    "observer",
    "recording",
    "foreground_verified",
    "paused",
    "blocked",
    "safe_idle",
    "reason",
    "quick_stop_available",
    "emergency_stop_available",
    "updated_monotonic_milliseconds",
    "snapshot_age_milliseconds",
    "stale",
    "can_start_or_authorize_session",
    "raw_media_included",
    "raw_input_included",
    "session_elapsed_milliseconds"
)

function Write-InspectResult {
    $result = [ordered]@{
        schema_version = 1
        product_version = "1.4.9"
        sprint = 289
        boundary = "orion_overlay_session_status_integration"
        capability_id = $CapabilityId
        status_surface = $StatusSurface
        modes = @("Inspect", "PreviewSafeIdle", "LiveStatus")
        live_status_binding_available = $true
        status_transport = "local_atomic_json_snapshot_polling"
        command_transport = (
            "local_atomic_reviewed_command_request_and_acknowledgement"
        )
        poll_interval_milliseconds = $PollIntervalMilliseconds
        stale_timeout_milliseconds = $StaleTimeoutMilliseconds
        request_expiry_milliseconds = $RequestExpiryMilliseconds
        emergency_hold_milliseconds = $EmergencyHoldMilliseconds
        live_required_field_count = $RequiredStatusFields.Count
        session_timer_available = $true
        foreground_warning_available = $true
        coach_observer_recording_indicators_available = $true
        reviewed_quick_stop_available = $true
        reviewed_emergency_stop_all_available = $true
        quick_stop_confirmation = "two_step_local_confirmation"
        emergency_confirmation = "press_and_hold_local_confirmation"
        overlay_is_authority = $false
        direct_stop_execution = $false
        session_start_from_overlay = $false
        mode_change_from_overlay = $false
        game_process_enumeration = $false
        window_capture = $false
        audio_capture = $false
        input_telemetry = $false
        input_hook = $false
        input_injection = $false
        raw_media_display = $false
        raw_input_display = $false
        atlas_contacted = $false
        network_listener = $false
        safe_idle = $true
    }
    $result | ConvertTo-Json -Depth 7
}

function Get-MonotonicMilliseconds {
    $ticks = [Diagnostics.Stopwatch]::GetTimestamp()
    $frequency = [Diagnostics.Stopwatch]::Frequency
    return [long][Math]::Floor(
        ([double]$ticks * 1000.0) / [double]$frequency
    )
}

function Test-Sha256Hex {
    param(
        [AllowEmptyString()][string]$Value
    )
    return $Value -cmatch "^[0-9a-f]{64}$"
}

function Write-AtomicJson {
    param(
        [Parameter(Mandatory = $true)]$Value,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $directory = Split-Path -Parent $Path
    [IO.Directory]::CreateDirectory($directory) | Out-Null

    $temporary = $Path + ".tmp"
    $json = $Value | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText(
        $temporary,
        $json + [Environment]::NewLine,
        (New-Object Text.UTF8Encoding($false))
    )
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Read-StatusSnapshot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][long]$PreviousSequence
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return [ordered]@{
            Valid = $false
            Reason = "STATUS MISSING"
            Sequence = $PreviousSequence
            Snapshot = $null
        }
    }

    try {
        $snapshot = (
            Get-Content -LiteralPath $Path -Raw |
            ConvertFrom-Json
        )

        $propertyNames = @($snapshot.PSObject.Properties.Name)
        foreach ($field in $RequiredStatusFields) {
            if ($propertyNames -notcontains $field) {
                throw "missing field: $field"
            }
        }

        if ([int]$snapshot.schema_version -ne 1) {
            throw "schema mismatch"
        }
        if ([string]$snapshot.surface -cne $StatusSurface) {
            throw "surface mismatch"
        }
        if ([bool]$snapshot.authority) {
            throw "authority forbidden"
        }
        if ([bool]$snapshot.can_start_or_authorize_session) {
            throw "session authorization forbidden"
        }
        if ([bool]$snapshot.raw_media_included) {
            throw "raw media forbidden"
        }
        if ([bool]$snapshot.raw_input_included) {
            throw "raw input forbidden"
        }

        $sequence = [long]$snapshot.sequence
        if ($sequence -lt $PreviousSequence) {
            throw "sequence regression"
        }

        $state = [string]$snapshot.state
        if ($AllowedStates -notcontains $state) {
            throw "unknown state"
        }

        $modeProfile = [string]$snapshot.mode_profile
        if (
            $state -cne "SAFE_IDLE" -and
            -not [string]::IsNullOrWhiteSpace($modeProfile) -and
            $AllowedModes -notcontains $modeProfile
        ) {
            throw "unknown mode profile"
        }

        $age = [long]$snapshot.snapshot_age_milliseconds
        $isStale = [bool]$snapshot.stale
        if ($age -gt $StaleTimeoutMilliseconds -and -not $isStale) {
            throw "expired snapshot not marked stale"
        }

        return [ordered]@{
            Valid = $true
            Reason = ""
            Sequence = $sequence
            Snapshot = $snapshot
        }
    }
    catch {
        return [ordered]@{
            Valid = $false
            Reason = "INVALID STATUS"
            Sequence = $PreviousSequence
            Snapshot = $null
        }
    }
}

function Format-Elapsed {
    param(
        [long]$Milliseconds
    )
    $totalSeconds = [Math]::Max(
        0,
        [Math]::Floor($Milliseconds / 1000)
    )
    $hours = [Math]::Floor($totalSeconds / 3600)
    $minutes = [Math]::Floor(($totalSeconds % 3600) / 60)
    $seconds = $totalSeconds % 60
    if ($hours -gt 0) {
        return "{0:00}:{1:00}:{2:00}" -f $hours, $minutes, $seconds
    }
    return "{0:00}:{1:00}" -f $minutes, $seconds
}

function New-ReviewedRequest {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet(
            "QUICK_STOP_CURRENT_SESSION",
            "EMERGENCY_STOP_ALL"
        )]
        [string]$Command,

        [AllowNull()]
        [string]$SessionId,

        [Parameter(Mandatory = $true)]
        [long]$ConfirmationStarted,

        [Parameter(Mandatory = $true)]
        [long]$ConfirmationCompleted
    )

    $issued = Get-MonotonicMilliseconds
    $requestId = (
        "req-s289-{0}-{1}" -f
        [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssfffZ"),
        [Guid]::NewGuid().ToString("N").Substring(0, 12)
    )
    $idempotencyKey = (
        "idem-s289-{0}" -f
        [Guid]::NewGuid().ToString("N")
    )

    if ($Command -ceq "QUICK_STOP_CURRENT_SESSION") {
        $confirmationType = "two_step_local_confirmation"
    }
    else {
        $confirmationType = "press_and_hold_local_confirmation"
    }

    return [ordered]@{
        schema_version = 1
        request_id = $requestId
        command = $Command
        session_id = $SessionId
        issued_monotonic_milliseconds = $issued
        expires_monotonic_milliseconds = (
            $issued + $RequestExpiryMilliseconds
        )
        confirmation_type = $confirmationType
        confirmation_started_monotonic_milliseconds = (
            $ConfirmationStarted
        )
        confirmation_completed_monotonic_milliseconds = (
            $ConfirmationCompleted
        )
        confirmation_hold_milliseconds = (
            $ConfirmationCompleted - $ConfirmationStarted
        )
        reviewed = $true
        permission_snapshot_sha256 = $PermissionSnapshotSha256
        audit_required = $true
        idempotency_key = $idempotencyKey
        overlay_origin = $true
        authority = $false
        direct_execution = $false
        raw_input_included = $false
    }
}

if ($Mode -ceq "Inspect") {
    Write-InspectResult
    exit 0
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
    throw "An STA thread is required."
}

if ($Mode -ceq "PreviewSafeIdle") {
    if ($Approval -cne $SafeIdleApproval) {
        throw "Exact Sprint 288 SAFE_IDLE preview approval is required."
    }
}
elseif ($Mode -ceq "LiveStatus") {
    if ($Approval -cne $LiveStatusApproval) {
        throw "Exact Sprint 289 live-status approval is required."
    }
    if ([string]::IsNullOrWhiteSpace($StatusPath)) {
        throw "StatusPath is required."
    }
    if ([string]::IsNullOrWhiteSpace($RequestDirectory)) {
        throw "RequestDirectory is required."
    }
    if ([string]::IsNullOrWhiteSpace($AcknowledgementDirectory)) {
        throw "AcknowledgementDirectory is required."
    }
    if (-not (Test-Sha256Hex $PermissionSnapshotSha256)) {
        throw "PermissionSnapshotSha256 must be lowercase SHA-256 hex."
    }
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$source = @'
using System;
using System.Windows.Forms;

public sealed class AuraSprint289OverlayForm : Form
{
    public const int WS_EX_NOACTIVATE = unchecked((int)0x08000000);
    public const int WS_EX_TOOLWINDOW = 0x00000080;
    public const int WM_MOUSEACTIVATE = 0x0021;
    public const int MA_NOACTIVATE = 3;

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

    protected override void WndProc(ref Message message)
    {
        if (message.Msg == WM_MOUSEACTIVATE)
        {
            message.Result = (IntPtr)MA_NOACTIVATE;
            return;
        }

        base.WndProc(ref message);
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

$mutexName = "Local\AURA_S289_Overlay_Session_Status"
$createdNew = $false
$mutex = New-Object Threading.Mutex(
    $false,
    $mutexName,
    [ref]$createdNew
)

$acquired = $false
$form = $null
$pollTimer = $null
$durationTimer = $null
$script:emergencyHoldWatch = $null
$script:quickStopArmedUntil = [long]0
$script:currentSequence = [long]0
$script:currentSnapshot = $null
$script:lastRequestId = ""
$script:lastAcknowledgementText = ""

try {
    $acquired = $mutex.WaitOne(0, $false)
    if (-not $acquired) {
        throw "Another AURA native overlay is already running."
    }

    $screens = @([Windows.Forms.Screen]::AllScreens)
    if ($ScreenIndex -ge $screens.Count) {
        throw "ScreenIndex exceeds the available display count."
    }

    $screen = $screens[$ScreenIndex]
    $profile = $Profiles[$ViewProfile]

    $form = New-Object AuraSprint289OverlayForm
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

    $statusLabel = New-Object Windows.Forms.Label
    $statusLabel.AutoSize = $true
    $statusLabel.Left = 16
    $statusLabel.Top = 38
    $statusLabel.ForeColor = [Drawing.Color]::FromArgb(84, 214, 255)
    $statusLabel.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.DetailSize,
        [Drawing.FontStyle]::Bold
    )

    $detailLabel = New-Object Windows.Forms.Label
    $detailLabel.AutoSize = $true
    $detailLabel.Left = 16
    $detailLabel.Top = 66
    $detailLabel.ForeColor = [Drawing.Color]::FromArgb(193, 199, 209)
    $detailLabel.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.DetailSize,
        [Drawing.FontStyle]::Regular
    )

    $warningLabel = New-Object Windows.Forms.Label
    $warningLabel.AutoSize = $true
    $warningLabel.Left = 16
    $warningLabel.Top = 92
    $warningLabel.ForeColor = [Drawing.Color]::FromArgb(255, 190, 84)
    $warningLabel.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.DetailSize,
        [Drawing.FontStyle]::Bold
    )

    $ackLabel = New-Object Windows.Forms.Label
    $ackLabel.AutoSize = $true
    $ackLabel.Left = 16
    $ackLabel.Top = 116
    $ackLabel.ForeColor = [Drawing.Color]::FromArgb(155, 225, 155)
    $ackLabel.Font = New-Object Drawing.Font(
        "Segoe UI",
        [single]$profile.DetailSize,
        [Drawing.FontStyle]::Regular
    )

    [void]$form.Controls.Add($title)
    [void]$form.Controls.Add($statusLabel)
    [void]$form.Controls.Add($detailLabel)
    [void]$form.Controls.Add($warningLabel)
    [void]$form.Controls.Add($ackLabel)

    $quickButton = $null
    $emergencyButton = $null

    if ($Mode -ceq "LiveStatus" -and $ViewProfile -cne "compact") {
        $quickButton = New-Object Windows.Forms.Button
        $quickButton.Left = 16
        $quickButton.Top = 142
        $quickButton.Width = 174
        $quickButton.Height = 28
        $quickButton.Text = "QUICK STOP"
        $quickButton.Enabled = $false
        $quickButton.TabStop = $false

        $emergencyButton = New-Object Windows.Forms.Button
        $emergencyButton.Left = 198
        $emergencyButton.Top = 142
        $emergencyButton.Width = 222
        $emergencyButton.Height = 28
        $emergencyButton.Text = "HOLD 1.5S STOP ALL"
        $emergencyButton.Enabled = $true
        $emergencyButton.TabStop = $false

        $quickButton.Add_Click({
            $now = Get-MonotonicMilliseconds
            if (
                $null -eq $script:currentSnapshot -or
                [bool]$script:currentSnapshot.stale -or
                -not [bool]$script:currentSnapshot.quick_stop_available
            ) {
                $script:lastAcknowledgementText = "Quick stop unavailable"
                return
            }

            if ($now -gt $script:quickStopArmedUntil) {
                $script:quickStopArmedUntil = $now + 5000
                $quickButton.Text = "CLICK AGAIN TO CONFIRM"
                $script:lastAcknowledgementText = "Quick stop armed for 5 seconds"
                return
            }

            $request = New-ReviewedRequest `
                -Command "QUICK_STOP_CURRENT_SESSION" `
                -SessionId ([string]$script:currentSnapshot.session_id) `
                -ConfirmationStarted ($script:quickStopArmedUntil - 5000) `
                -ConfirmationCompleted $now

            $requestPath = Join-Path `
                $RequestDirectory `
                ($request.request_id + ".json")
            Write-AtomicJson -Value $request -Path $requestPath

            $script:lastRequestId = [string]$request.request_id
            $script:lastAcknowledgementText = "Quick-stop request submitted"
            $script:quickStopArmedUntil = [long]0
            $quickButton.Text = "QUICK STOP"
        })

        $emergencyButton.Add_MouseDown({
            $script:emergencyHoldWatch = [Diagnostics.Stopwatch]::StartNew()
            $emergencyButton.Text = "KEEP HOLDING..."
        })

        $emergencyButton.Add_MouseUp({
            if ($null -eq $script:emergencyHoldWatch) {
                return
            }

            $script:emergencyHoldWatch.Stop()
            $held = [long]$script:emergencyHoldWatch.ElapsedMilliseconds
            $script:emergencyHoldWatch = $null

            if ($held -lt $EmergencyHoldMilliseconds) {
                $emergencyButton.Text = "HOLD 1.5S STOP ALL"
                $script:lastAcknowledgementText = (
                    "Emergency hold cancelled ({0} ms)" -f $held
                )
                return
            }

            $completed = Get-MonotonicMilliseconds
            $request = New-ReviewedRequest `
                -Command "EMERGENCY_STOP_ALL" `
                -SessionId $null `
                -ConfirmationStarted ($completed - $held) `
                -ConfirmationCompleted $completed

            $requestPath = Join-Path `
                $RequestDirectory `
                ($request.request_id + ".json")
            Write-AtomicJson -Value $request -Path $requestPath

            $script:lastRequestId = [string]$request.request_id
            $script:lastAcknowledgementText = (
                "Emergency stop-all request submitted"
            )
            $emergencyButton.Text = "HOLD 1.5S STOP ALL"
        })

        [void]$form.Controls.Add($quickButton)
        [void]$form.Controls.Add($emergencyButton)
    }

    if ($Mode -ceq "PreviewSafeIdle") {
        $statusLabel.Text = "SAFE IDLE  |  NO ACTIVE SESSION"
        $detailLabel.Text = (
            "Synthetic Sprint 288 preview | read-only | no live binding"
        )
        $warningLabel.Text = ""
        $ackLabel.Text = ""
    }
    else {
        $pollTimer = New-Object Windows.Forms.Timer
        $pollTimer.Interval = $PollIntervalMilliseconds
        $pollTimer.Add_Tick({
            $result = Read-StatusSnapshot `
                -Path $StatusPath `
                -PreviousSequence $script:currentSequence

            if (-not [bool]$result.Valid) {
                $script:currentSnapshot = $null
                $statusLabel.Text = "STALE | " + [string]$result.Reason
                $detailLabel.Text = "Active mode hidden until status is valid"
                $warningLabel.Text = "SAFE FALLBACK"
                if ($null -ne $quickButton) {
                    $quickButton.Enabled = $false
                    $quickButton.Text = "QUICK STOP"
                }
            }
            else {
                $script:currentSequence = [long]$result.Sequence
                $script:currentSnapshot = $result.Snapshot

                if ([bool]$script:currentSnapshot.stale) {
                    $statusLabel.Text = "STALE | ACTIVE MODE HIDDEN"
                    $detailLabel.Text = (
                        "Snapshot age {0} ms" -f
                        [long]$script:currentSnapshot.snapshot_age_milliseconds
                    )
                    $warningLabel.Text = "SAFE FALLBACK"
                    if ($null -ne $quickButton) {
                        $quickButton.Enabled = $false
                        $quickButton.Text = "QUICK STOP"
                    }
                }
                else {
                    $badges = @()
                    if ([bool]$script:currentSnapshot.coach) {
                        $badges += "COACH"
                    }
                    if ([bool]$script:currentSnapshot.observer) {
                        $badges += "OBSERVER"
                    }
                    if ([bool]$script:currentSnapshot.recording) {
                        $badges += "RECORDING"
                    }
                    if ([bool]$script:currentSnapshot.safe_idle) {
                        $badges += "SAFE IDLE"
                    }
                    if ([bool]$script:currentSnapshot.paused) {
                        $badges += "PAUSED"
                    }
                    if ([bool]$script:currentSnapshot.blocked) {
                        $badges += "BLOCKED"
                    }

                    $badgeText = $badges -join " | "
                    $timerText = Format-Elapsed (
                        [long]$script:currentSnapshot.session_elapsed_milliseconds
                    )
                    $statusLabel.Text = $badgeText
                    $detailLabel.Text = (
                        "{0} | {1} | {2}" -f
                        [string]$script:currentSnapshot.game_display_name,
                        [string]$script:currentSnapshot.state,
                        $timerText
                    )

                    if (
                        -not [bool]$script:currentSnapshot.safe_idle -and
                        -not [bool]$script:currentSnapshot.foreground_verified
                    ) {
                        $warningLabel.Text = "GAME FOCUS LOST / WAITING"
                    }
                    elseif (
                        -not [string]::IsNullOrWhiteSpace(
                            [string]$script:currentSnapshot.reason
                        )
                    ) {
                        $warningLabel.Text = [string]$script:currentSnapshot.reason
                    }
                    else {
                        $warningLabel.Text = ""
                    }

                    if ($null -ne $quickButton) {
                        $quickButton.Enabled = (
                            [bool]$script:currentSnapshot.quick_stop_available
                        )
                    }
                }
            }

            if (
                -not [string]::IsNullOrWhiteSpace($script:lastRequestId)
            ) {
                $ackPath = Join-Path `
                    $AcknowledgementDirectory `
                    ($script:lastRequestId + ".ack.json")
                if (Test-Path -LiteralPath $ackPath -PathType Leaf) {
                    try {
                        $ack = (
                            Get-Content -LiteralPath $ackPath -Raw |
                            ConvertFrom-Json
                        )
                        $script:lastAcknowledgementText = (
                            "{0}: {1}" -f
                            [string]$ack.disposition,
                            [string]$ack.reason
                        )
                    }
                    catch {
                        $script:lastAcknowledgementText = "Invalid acknowledgement"
                    }
                }
            }

            $ackLabel.Text = $script:lastAcknowledgementText

            if (
                $script:quickStopArmedUntil -gt 0 -and
                (Get-MonotonicMilliseconds) -gt $script:quickStopArmedUntil
            ) {
                $script:quickStopArmedUntil = [long]0
                if ($null -ne $quickButton) {
                    $quickButton.Text = "QUICK STOP"
                }
            }
        })
        $pollTimer.Start()
    }

    if ($DurationSeconds -gt 0) {
        $durationTimer = New-Object Windows.Forms.Timer
        $durationTimer.Interval = $DurationSeconds * 1000
        $durationTimer.Add_Tick({
            $durationTimer.Stop()
            $form.Close()
        })
        $durationTimer.Start()
    }

    [Windows.Forms.Application]::Run($form)
}
finally {
    if ($null -ne $pollTimer) {
        $pollTimer.Stop()
        $pollTimer.Dispose()
    }
    if ($null -ne $durationTimer) {
        $durationTimer.Stop()
        $durationTimer.Dispose()
    }
    if ($null -ne $script:emergencyHoldWatch) {
        $script:emergencyHoldWatch.Stop()
    }
    if ($null -ne $form) {
        $form.Dispose()
    }
    if ($acquired) {
        $mutex.ReleaseMutex()
    }
    $mutex.Dispose()
}
