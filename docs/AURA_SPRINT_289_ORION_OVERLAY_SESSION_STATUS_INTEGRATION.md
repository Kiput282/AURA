# AURA Sprint 289 — ORION Overlay Session Status Integration

Status: implemented on ATLAS; pending bounded ORION live-status and reviewed
control acceptance before commit.

## Boundary

Sprint 289 integrates the native ORION overlay foundation with the authoritative
Sprint 287 Game Companion session-orchestration metadata contract.

The overlay remains a local ORION status surface and reviewed request origin.
It is never authority and cannot authorize or start a session, change mode, or
execute a stop directly.

## Live status contract

The integration projects 26 metadata fields:

- the 25 Sprint 288 foundation fields;
- `session_elapsed_milliseconds`.

The overlay polls a local atomic JSON status snapshot every 250 milliseconds.
Snapshots become stale after 1500 milliseconds. Invalid, missing, expired, or
regressed snapshots fail closed and hide all active mode indicators.

Visible state includes:

- Coach, Observer, and Recording badges;
- game display name;
- canonical orchestration state;
- monotonic session timer;
- foreground-loss/waiting warning;
- paused, blocked, stopping, stale, and safe-idle state.

## Reviewed controls

### Quick stop

Quick stop applies only to the currently verified session. The user must click
once to arm the request and click again within five seconds. The overlay writes
a metadata-only request file but does not execute the stop.

### Emergency stop all

Emergency stop-all is always available. The user must press and hold the local
button for at least 1500 milliseconds. The request does not bind to a session
ID and is handled by the authoritative Game Companion session orchestrator.

Both request types include:

- exact command and request ID;
- five-second expiry;
- confirmation timing;
- reviewed and audit-required markers;
- permission-snapshot SHA-256;
- idempotency key;
- non-authoritative overlay origin;
- `direct_execution=false`;
- `raw_input_included=false`.

Acknowledgement files are written by the authoritative handler and expose
accepted, duplicate, expired, or rejected disposition.

## Contract evidence

Sprint 289 discovery passed at SHA-256
`7a9be49b2a861721221f097ba5ed7963049de9dbe6d0545473400ab22ccad970`.

The noninteractive integration contract probe passed 144/144 assertions at
SHA-256
`ae1dec2cfacd72c8f5e3d89a2ceb45414613f6f3c5eaa244fe1879b09342da6b`.

It validated all 10 states, monotonic status sequence and timer, stale
fail-closed behavior, 10 reviewed requests and 10 acknowledgements, expiry,
idempotency, current-session binding, emergency hold, and non-authoritative
execution boundaries. No command was executed.

## Deferred to Sprint 290

Sprint 290 owns full live end-to-end block acceptance, relevant
failure/recovery tests, and final return to safe idle.

## Safety boundary

Sprint 289 adds no session start from overlay, mode change, arbitrary process
control, capture, raw media/input display, global input hook, input injection,
network listener, cloud dependency, autonomous gameplay, or multiplayer
automation.

## Final ORION Acceptance Evidence

The final bounded ORION acceptance completed successfully with the overlay
remaining a non-authoritative local operational surface.

- Final helper SHA-256: `5727c6a770dd7d41b8a1d06e3c1af4a9a89cb43ef99908125bcbb60c1b2a69b5`
- Windows PowerShell 5.1 parser and fail-closed preflight: PASS
- Ten-phase live-status binding acceptance: PASS
- Overlay foreground attribution: zero overlay window/process samples
- No-activate mouse delivery: `MA_NOACTIVATE`, click not eaten
- Shared event-state transport: explicit script scope for six runtime fields
- Reviewed quick stop: PASS with two-step local confirmation
- Short emergency hold cancellation: PASS at 746 ms with no request
- Reviewed emergency stop-all: PASS at 2723 ms
- Reviewed request count: 2
- Synthetic acknowledgement count: 2
- Stop commands executed during acceptance: 0
- Raw input/media exported: none
- Final lifecycle: overlay closed, runtime files cleaned, `SAFE_IDLE`

Evidence SHA-256 chain:

- Preflight v5: `532b903683525d81b330d17bf08ce05ca78c620cb56f9945e58d2ac83cc1f002`
- Bounded live-status acceptance v2: `655bbc4cc7fe2bd84147eb0b1fe159e37ba7444af06d6540c21099e132803e9a`
- Focus attribution v2: `b1b7b482e3991d932121e6fc8d3c6200116182057100759af9f9b2d697419fd7`
- Focused-click probe v2: `1b9e0d52d901d855271e667f2a9c85dbe1d738bef04507777443ab3b6a663bc5`
- Reviewed-controls acceptance v3: `33c9077d8643308e60962f336c00e99aad8a839d03c3629823f2e5094ea27ead`
- ATLAS evidence review: `83322196621e1ab7d451c86bf3ef385868213f120c1c5fd905dacd023266f96d`

The evidence files remain operational artifacts outside the repository. The
repository records only their bounded metadata and SHA-256 chain.
