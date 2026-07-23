# AURA Sprint 283 — Game Window Capture

Status: implemented, pending live ORION acceptance and commit

- Version: `v1.4.3`
- Sprint: `283`
- Boundary: `game_window_capture`
- Previous checkpoint: `v1.4.2`
- Previous commit: `3e8565a38030f11a34e848b37965813628087d4e`
- Reference game: `osu_offline`
- Next sprint: `284`
- Next boundary: `game_audio_capture`

## Delivered boundary

Sprint 283 adds a bounded one-shot selected-game-window capture contract.

The capture flow is:

1. Sprint 282 produces `game_detected_pending_review`.
2. The operator reviews the detected game and selects a mode.
3. ATLAS creates a visible capture preview.
4. The operator gives exact one-shot capture approval.
5. ATLAS issues one expiring, single-use permission.
6. ORION revalidates the exact process and visible selected window.
7. ORION captures one PNG frame into temporary private storage.
8. ORION returns only bounded artifact metadata and SHA-256.
9. ATLAS reviews the receipt.
10. ORION deletes the temporary artifact after explicit cleanup confirmation.
11. The runtime returns to `safe_idle`.

## Host authority

ATLAS remains the control and permission authority.

ORION is the explicit one-shot capture source. It may capture only the reviewed
`osu_offline` target bound to the expected agent, device, process ID,
executable basename, and window evidence.

## Hard limits

- one frame per request;
- selected game window only;
- PNG only;
- maximum dimensions, pixel count, and encoded bytes;
- short-lived preview and permission;
- single-use permission consumption;
- temporary private ORION artifact;
- artifact MIME type, dimensions, size, and SHA-256 receipt;
- no raw image bytes or local artifact path in ATLAS packets;
- no raw window-title export;
- no full-screen fallback;
- no background or continuous capture.

## Closed capabilities

Sprint 283 does not activate:

- game audio capture;
- recording;
- telemetry;
- coaching;
- application launch;
- voice-command-to-action;
- keyboard, mouse, controller, or game input;
- autonomous gameplay;
- multiplayer automation;
- public streaming output;
- persistent capture storage.

## Failure behavior

Missing or changed windows, changed processes, expired permissions, capture
timeouts, unavailable backends, oversized artifacts, integrity failures, and
cleanup failures all fail closed. Automatic recovery is not performed.

Sprint 284 owns `game_audio_capture`.
