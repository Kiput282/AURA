# AURA Sprint 281 - Game Companion Runtime Foundation

## Status

- Sprint: 281
- Product version: v1.4.1
- Boundary: `game_companion_runtime_foundation`
- State: implemented foundation, runtime closed
- Reference game: `osu_offline`
- Next sprint: 282
- Next boundary: `supported_game_detection`

## Purpose

Sprint 281 converts the historical Game Companion planning layer into a
deterministic runtime contract without activating any external runtime.

## Implemented contracts

- canonical game catalog;
- four operator-selectable modes;
- review-only session proposal;
- nine-state session state machine;
- explicit operator start and stop;
- independent emergency-stop state;
- automatic recovery disabled;
- public livestream and private dataset pipeline separation;
- hard guards for every deferred runtime surface;
- side-effect-free CLI inspection and self-test.

## Canonical modes

1. `coach_only`
2. `observer_only`
3. `coach_observer`
4. `coach_observer_recording`

Only the fourth mode includes recording intent. Sprint 281 still does not start
recording.

## Game catalog

`osu_offline` is the first reference implementation. Beat Saber, Monster
Hunter: World, Ace Combat, Mortal Kombat, Resident Evil 4, and Minecraft remain
planned or candidate tracks. Arknights: Endfield remains deferred. Genshin
Impact and Clash of Clans remain outside the active Game Companion roadmap.

Catalog membership does not mean runtime detection or capture support.

## Runtime fields kept false

- process and window scanning;
- supported-game detection;
- safe-idle game prompt;
- game-window and game-audio capture;
- input telemetry and timestamp synchronization;
- recording and dataset manifest writes;
- public stream and private dataset pipelines;
- post-session analysis and coach feedback;
- voice-command-to-action;
- application launch and game input control;
- autonomous gameplay and multiplayer automation;
- network activity, persistence, and external action execution.

## Validation

The module self-test contains 125 deterministic assertions. Full validation
also requires all Python files to parse, the historical Game Companion
foundation to remain readable, `git diff --check` to pass, and the working tree
to contain only the expected Sprint 281 changes.

## Handoff to Sprint 282

Sprint 282 may add read-only, allowlisted process/window detection and a
safe-idle operator prompt. It must not start capture, recording, telemetry,
coaching, or game control automatically.
