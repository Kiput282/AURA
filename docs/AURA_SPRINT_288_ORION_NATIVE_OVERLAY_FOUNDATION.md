# AURA Sprint 288 — ORION Native Overlay Foundation

Status: completed; ORION preflight, noninteractive contract probe, and bounded live SAFE_IDLE preview passed.

## Boundary

Sprint 288 adds the disabled-by-default native ORION overlay foundation. The
native overlay is the primary operational indicator during Game Companion use;
the browser Control Center remains the secondary configuration, history, and
technical-detail surface.

The implementation uses Windows PowerShell 5.1, WinForms, System.Drawing, an STA
UI thread, `WS_EX_NOACTIVATE`, `WS_EX_TOOLWINDOW`, top-most borderless window
behavior, a local single-instance mutex, bounded screen positioning, and three
view profiles:

- `compact` — 360 × 72;
- `normal` — 440 × 128;
- `expanded` — 560 × 220.

## Status contract

The runtime validates the Sprint 287 metadata-only operational status schema:

- 25 required fields;
- 10 orchestration states;
- four approved mode profiles;
- strictly increasing sequence;
- stale timeout of 1500 milliseconds;
- 250-millisecond polling contract;
- invalid, missing, expired, or regressed status fails closed;
- stale status hides any previously active mode.

The overlay is never authority and cannot authorize or start a session.

## ORION acceptance evidence

The UI capability preflight passed on ORION with Windows PowerShell 5.1 64-bit,
STA, WinForms, System.Drawing, user32 interop, two displays, 96 DPI,
`WS_EX_NOACTIVATE`, `WS_EX_TOOLWINDOW`, top-most, hidden-from-taskbar,
single-instance mutex, atomic local metadata snapshot, unchanged focus, no
window shown, and safe idle.

The noninteractive contract probe passed with:

- eight valid status snapshots;
- invalid schema and sequence regression rejected;
- stale/invalid/missing status fail-closed;
- 30 unique synthetic render digests across 10 cases and three view profiles;
- six valid placements across two displays;
- no window, form handle, session, capture, input, network listener, or raw
  render export.

## Included ORION helper

`AuraNativeOverlay.ps1` defaults to `Inspect`, which never shows a window.
`PreviewSafeIdle` requires the exact approval:

`APPROVE AURA SPRINT 288 SAFE IDLE OVERLAY PREVIEW`

Preview mode displays only a bounded synthetic `SAFE_IDLE` overlay for 1–15
seconds. It has no live status binding and no session or stop controls.

## Deferred to Sprint 289

- live Sprint 287 orchestration status binding;
- Coach/Observer/Recording live indicators;
- foreground warning integration;
- session timer integration;
- reviewed quick-stop control;
- reviewed emergency stop-all control.

## Safety boundary

Sprint 288 does not add session authorization, session start, mode change,
quick-stop execution, emergency-stop execution, game-process control, window or
audio capture, input telemetry, input hooks, input injection, raw media
rendering, raw input display, network listeners, or cloud dependency.

## Local metadata evidence SHA-256

- Discovery: `3ee0710356109508d25245412fefb534667fe41a9043b63a8924a23f85a9dc65`;
- ORION UI preflight: `b0f8590fbb5d13bbbc3243f53251fc83e1059139adadd27439a59c4e672105db`;
- ORION noninteractive contract probe: `eb463d287e37ced9c18bb31aedc1a18f41cc8dda1a6a8e17955c7cad6c191427`.

## Bounded live SAFE_IDLE preview acceptance

The reviewed ORION preview acceptance v2 displayed the `normal` overlay
for a requested five seconds and completed in 5375.637 milliseconds. The observed
window was exactly 440 × 128, remained within the selected monitor working
area, and exposed `WS_EX_TOPMOST`, `WS_EX_TOOLWINDOW`, and
`WS_EX_NOACTIVATE`.

Foreground focus was unchanged while the overlay was visible and after it
closed. The helper exited with code zero, the window was removed after exit,
no cleanup was required, and runtime returned to safe idle.

The repository helper was normalized to UTF-8 BOM with LF line endings
without semantic changes before this repeated acceptance.

Acceptance v2 evidence SHA-256: `a047fd6a22e77d711b38ecaf7fdbb7167485c12be19a08ed8949c2ba2ae33261`.
