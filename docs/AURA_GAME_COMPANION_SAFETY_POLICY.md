# AURA Game Companion Safety Policy

Status: ACTIVE GUARDED FOUNDATION
Current Canonical Version: v1.4.2
Current Sprint: 282
Owner: Kiput
Motto: Grow Together

## Purpose

AURA Game Companion is a companion, coach, observer, learner, performer, and
future livestream identity layer. It is not cheat automation.

Sprint 281 establishes only the deterministic runtime foundation: the game
catalog, operator-selectable modes, session state machine, public/private
pipeline separation, and hard safety guards. It does not detect games, capture
screens or audio, collect input telemetry, record gameplay, control input, or
launch applications.

## Active reference order

1. osu! offline — first reference implementation for Coach, Observer, and
   reviewed Recording.
2. Beat Saber — future 3D rhythm performer track.
3. Monster Hunter: World — single-player Hunter Coach first.
4. Ace Combat — single-player virtual-pilot track.
5. Mortal Kombat — local two-player research only.
6. Resident Evil 4 — Observer stage first.
7. Minecraft — legacy private/local candidate, not the Sprint 281 reference.
8. Arknights: Endfield — deferred.

Genshin Impact and Clash of Clans are excluded from the active Game Companion
roadmap.

## Canonical operator modes

- Coach only
- Observer only
- Coach + Observer
- Coach + Observer + Recording

The operator selects the mode and explicitly starts the session. Recording is
never implied by Coach or Observer.

## Global prohibited behavior

AURA Game Companion must not:

- cheat, exploit, or bypass game rules;
- secretly automate keyboard, mouse, controller, or virtual-controller input;
- automate multiplayer, online farming, account actions, or ranked score
  submission;
- read internal game data as an answer key for perfect play;
- start capture or recording without visible operator selection;
- merge public livestream output with private training data;
- ignore stop, disconnect, permission expiry, watchdog, or emergency stop;
- use unrestricted shell or unrestricted ORION control.

## Public and private pipeline rule

Public livestream output and private training-data recording are separate
pipelines with separate visibility, retention, and approval. Private datasets
must not be published implicitly or included in a public scene by default.

## Required gates before runtime activation

Runtime work after Sprint 281 requires:

- authenticated ORION identity and live link;
- allowlisted supported-game detection;
- explicit game/window selection;
- visible Control Center state;
- permission grant and expiry;
- bounded capture;
- audit records;
- storage quotas and reserved free space;
- independent stop and emergency stop;
- failure-to-safe-idle behavior;
- game-specific safety policy.

## Sprint 281 boundary

Sprint 281 remains contract-only. The next boundary is Sprint 282
`supported_game_detection`. Detection must remain read-only and may not start
capture, recording, telemetry, coaching, or application control.

## Sprint 282 supported-game detection boundary

Sprint 282 activates only an explicit read-only detection capability.

- Active reference profile: `osu_offline`
- Exact executable basename: `osu!.exe`
- A visible top-level window is required.
- Filtering occurs locally on ORION.
- Only matched evidence may be exported.
- Full process inventories, command lines, executable paths, and raw window
  titles must not leave ORION.
- ATLAS must receive the observation through the existing authenticated
  live-link boundary and bind it to the expected agent and device identity.
- A match creates `game_detected_pending_review`; it does not start a session.
- Duplicate observations must not create repeated prompts.
- A no-match observation remains `safe_idle`.

Capture, recording, telemetry, coaching, application launch,
voice-command-to-action, game input control, autonomous gameplay, and
multiplayer automation remain prohibited in Sprint 282.

The Sprint 283 `game_window_capture` boundary is implemented.

## Sprint 283 game-window capture boundary

Sprint 283 activates only bounded explicit one-shot capture for the already
reviewed `osu_offline` window.

- ATLAS remains the permission and session authority.
- Detection alone cannot start capture.
- Operator mode selection and a separate capture approval are required.
- Permission is exact-target, expiring, single-use, and limited to one frame.
- ORION must revalidate process ID, executable basename, and selected-window
  availability immediately before capture.
- The output is one bounded temporary private PNG.
- The receipt contains MIME type, dimensions, size, and SHA-256 only.
- Raw image bytes, raw window titles, and local artifact paths must not enter
  ATLAS packets.
- Full-screen fallback and arbitrary-window capture are prohibited.
- Explicit cleanup evidence is required before returning to `safe_idle`.

Game audio capture, continuous capture, recording, telemetry, coaching,
application launch, voice-command-to-action, game input control, autonomous
gameplay, and multiplayer automation remain prohibited.

Sprint 286 implements `game_timestamp_synchronization`; the next boundary is Sprint 287 `game_session_orchestration`.

## Sprint 284 bounded game-audio boundary

Game audio may be sampled only after the detected `osu_offline` process and
mode have been reviewed, a visible audio preview has been approved, and ATLAS
has issued one short-lived single-use permission.

The ORION source must use process-scoped loopback for the exact reviewed
process tree. Microphone capture, endpoint enumeration, arbitrary audio-device
selection, and whole-system fallback are forbidden. The sample is limited to
five seconds, 48 kHz stereo signed-16-bit PCM WAV, temporary private storage,
metadata-only receipt, and explicit cleanup.

Continuous capture, recording sessions, transcription, telemetry, coaching,
application launch, voice actions, and game input control remain outside
Sprint 284. Sprint 285 owns `game_input_telemetry`.

## Sprint 285 bounded foreground input-telemetry boundary

Game-input telemetry may be sampled only after the detected `osu_offline`
process and mode have been reviewed, a visible telemetry preview has been
approved, and ATLAS has issued one short-lived single-use permission.

Every poll must remain bound to the exact reviewed `osu!.exe` process,
process-start evidence, visible window, and foreground window. Focus loss
fails closed. Only semantic `Z`/`X`, left/right mouse transitions, and cursor
coordinates normalized to the bound game client area are allowed.

Arbitrary keys, characters, text, clipboard data, raw scan codes, background
input, global cursor history, absolute screen coordinates, hooks, Raw Input,
input injection, controller reads, continuous monitoring, recording,
coaching, autonomous gameplay, and multiplayer automation are forbidden.
The sample is limited to five seconds, 512 events, 128 KiB, temporary private
ORION storage, metadata-only ATLAS receipt, and explicit cleanup.

Sprint 286 owns cross-stream timestamp alignment and clock synchronization.

## Sprint 286 bounded shared-clock boundary

Timestamp synchronization may begin only after a visible ATLAS preview,
explicit operator approval, and one short-lived single-use permission. ORION
must create one high-resolution monotonic session epoch and explicit clock
frequency shared by window, audio, and input metadata envelopes.

UTC may be recorded only as a session anchor. Wall clock must not be the sole
ordering source, and ATLAS/ORION wall-clock equivalence must not be assumed.
Clock identity, frequency, epoch, per-stream start, sequence, and relative
sample timestamp are validated. A monotonic clock discontinuity fails closed.

The runtime must not change the Windows system clock, NTP, or Windows Time
service. It must not export raw monotonic ticks, raw logical envelopes, window
frames, audio, or input. Real capture alignment, drift compensation,
resampling, interpolation, time stretching, session orchestration, coaching,
autonomous gameplay, and multiplayer automation remain disabled.

Sprint 287 owns Game Companion session orchestration and shared live session
state for the future native ORION overlay.

## Sprint 287 — Game Session Orchestration Boundary

Game Companion sessions are explicit, single-session, permission-bound, and
safe-idle by default. Supported profiles are `coach_only`, `observer_only`,
`coach_observer`, and `coach_observer_recording`; recording-only is forbidden.

Any future start requires exact process/window binding, foreground verification,
a valid permission snapshot, and one shared timestamp session. Partial start
failure must roll back all already-started dependencies. Invalid transitions
fail closed. Normal stop and emergency stop-all are idempotent.

ORION operational status and the Sprint 288 overlay are read-only status
surfaces, not authority. Implicit start, background observation, unreviewed
recording, autonomous gameplay, multiplayer automation, anti-cheat bypass,
input injection, and raw media/input export to ATLAS remain forbidden.
