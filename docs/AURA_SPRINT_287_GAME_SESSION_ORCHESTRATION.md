# AURA Sprint 287 — Game Session Orchestration

Status: complete; logical state-machine contract probe passed

## Boundary

Sprint 287 adds a safe-idle orchestration contract for explicit Game Companion
sessions. It coordinates the existing window-capture, game-audio, bounded input
telemetry, and shared timestamp foundations without activating any real session
by default.

The runtime defines four reviewed mode profiles:

- `coach_only`;
- `observer_only`;
- `coach_observer`;
- `coach_observer_recording`.

Recording-only, implicit session start, background observation, autonomous
gameplay, multiplayer automation, input injection, anti-cheat bypass, and raw
media/input export to ATLAS remain forbidden.

## State machine

The canonical state set is:

- `SAFE_IDLE`;
- `ARMED`;
- `WAITING_FOR_FOREGROUND`;
- `OBSERVER_ACTIVE`;
- `COACH_ACTIVE`;
- `COACH_OBSERVER_ACTIVE`;
- `COACH_OBSERVER_RECORDING_ACTIVE`;
- `PAUSED_FOCUS_LOST`;
- `STOPPING`;
- `BLOCKED`.

One immutable session id and one explicit mode profile bind the entire session.
Exact game-process binding, visible-window binding, foreground verification, a
valid permission snapshot, and the Sprint 286 shared timestamp session are
required before any future mode activation.

A partial dependency start must roll back already-started dependencies. Normal
stop and emergency stop-all are idempotent and return the orchestration state to
`SAFE_IDLE`.

## Sprint 288 overlay handoff

Sprint 287 defines a metadata-only ORION operational status contract. The native
overlay planned for Sprint 288 reads this status; it is not authorization or
session-control authority.

The status contract exposes state, session id, Coach/Observer/Recording mode
flags, foreground verification, paused/blocked/safe-idle state, reason, and
quick-stop availability. It contains no raw media or raw input.

## Contract probe

The ATLAS in-memory probe passed 88 assertions and covered all four mode
profiles, foreground pause/resume, permission and exact-binding failures,
partial-start rollback, invalid-transition rejection, single-session
enforcement, idempotent normal stop, idempotent emergency stop, overlay status,
and final safe idle.

No ORION contact, game-process enumeration, capture, input read, shared-clock
session, Coach/Observer/Recording runtime, overlay window, input injection,
network listener, raw media read, or raw input read occurred.

## Local metadata evidence SHA-256

These files remain outside the repository and contain metadata only.

- ATLAS patch report:
  `0921befe2a555f583d7bbe16c27ffcad8e70c1fdacb9607baa65e8edc53aa7b8`;
- Sprint 287 discovery:
  `deca5a305af23530ffc5d5f29dbba97cc8bab3c75eb2ca91d09b2657e2bf0d82`;
- Session state-machine contract probe:
  `ec64f79ec4a0d167a911563abb5e4e83cfa11991f96bc32e5a8ef7c7ab56cd5a`;

## Deferred

Sprint 288 owns `orion_native_overlay_foundation`: a native, read-only,
always-on-top/no-activate operational status surface. Real Game Companion
session activation remains closed until later reviewed integration and live
acceptance.
