# AURA Sprint 282 - Supported Game Detection

Status: IMPLEMENTED — LIVE ORION ACCEPTANCE PENDING

- Sprint: 282
- Product version: v1.4.2
- Boundary: `supported_game_detection`
- Capability: `orion.game.detect_supported.read_only`
- Reference game: `osu_offline`
- Next sprint: 283
- Next boundary: `game_window_capture`

## Delivered boundary

Sprint 282 adds an explicit, read-only supported-game detection runtime.

The ORION side:

- performs only a one-shot scan after an explicit enable flag;
- filters exact allowlisted executable basenames locally;
- requires a visible top-level window;
- hashes the window title locally;
- exports only matched evidence;
- never exports the complete process inventory, process command line,
  executable path, or raw window title.

The ATLAS side:

- requires the existing authenticated ORION live-link boundary;
- validates the canonical game and detection profile;
- verifies packet schema, digest, freshness, sequence, and device binding;
- suppresses repeated prompts with an in-memory event key;
- creates a `game_detected_pending_review` prompt;
- keeps mode selection and session start under operator authority.

## Active detection profile

Only `osu_offline` is active for Sprint 282.

The exact executable basename is:

```text
osu!.exe
```

Catalog membership for other games remains planning metadata. Beat Saber,
Monster Hunter: World, Ace Combat, Mortal Kombat, Resident Evil 4, Minecraft,
and Arknights: Endfield do not gain active detection merely because they are
present in the Sprint 281 catalog.

## Safety state

Detection does not start:

- game-window or audio capture;
- recording;
- input telemetry;
- coaching;
- application launch;
- voice-command-to-action;
- keyboard, mouse, controller, or virtual-controller control;
- autonomous or multiplayer gameplay;
- a network listener;
- persistent Game Companion state.

A no-match result remains `safe_idle`. A match creates a review prompt only.
Dismissal returns to `safe_idle`. Session start remains unavailable in the
Sprint 282 prompt.

## Validation contract

The deterministic self-test covers:

- the exact allowlist and active reference game;
- local filtering and redaction;
- packet digest, freshness, and schema;
- authenticated identity binding;
- monotonic sequence replay rejection;
- duplicate prompt suppression;
- no-match safe-idle behavior;
- disabled and non-Windows adapter rejection;
- runner failure and timeout-safe behavior;
- closed capture, recording, telemetry, coaching, launch, and control fields;
- preservation of the Sprint 281 catalog, modes, and state machine.

The Sprint 282 contract contains 174 deterministic assertions.

## Acceptance note

The repository patch does not itself scan ATLAS or ORION. A separate live ORION
acceptance must prove both a no-match scan and, when `osu!.exe` is manually
running, one bounded match packet before Sprint 282 is committed.
