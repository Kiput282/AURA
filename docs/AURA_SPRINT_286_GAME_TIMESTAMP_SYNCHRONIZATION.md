# AURA Sprint 286 - Game Timestamp Synchronization

Status: complete; ORION clock preflight and bounded multistream probe passed

- Version: `v1.4.6`
- Sprint: `286`
- Boundary: `game_timestamp_synchronization`
- Previous checkpoint: `v1.4.5`
- Previous commit: `e44795d02efa5379754ea3e79a29da2ca725f829`
- Previous tree: `421c8e8b76cdfcd3204507bb053ccdfe37875b42`
- Reference game: `osu_offline`
- Next sprint: `287`
- Next boundary: `game_session_orchestration`

## Delivered boundary

Sprint 286 defines one explicit, permission-bound, bounded shared session-clock
envelope for the three Game Companion observation streams:

- `game_window_capture`;
- `game_audio_capture`;
- `game_input_telemetry`.

ORION is the monotonic clock source. ATLAS remains the review and permission
authority. UTC is recorded only as the session epoch anchor and is never the
sole stream-ordering source. ATLAS and ORION wall clocks are not assumed to be
equivalent.

## Shared clock contract

Every envelope carries:

- one `session_id`;
- one hashed `clock_id`;
- explicit high-resolution clock frequency;
- one UTC session anchor;
- a hashed monotonic session epoch;
- one stream identifier;
- a hashed stream-start tick value;
- stream-start relative milliseconds;
- sample relative milliseconds;
- a contiguous per-stream sequence.

The three streams must share the same session epoch, clock identity, clock
frequency, and UTC anchor. Sequence must remain contiguous and timestamps must
remain monotonic non-decreasing within each stream. A clock discontinuity fails
closed.

## Bounded limits

- maximum requested clock session: 2,000 ms;
- default probe duration: 1,200 ms;
- maximum logical envelopes: 1,024;
- reference cadences: window 16 ms, audio 10 ms, input 17 ms;
- metadata-only evidence to ATLAS;
- no temporary raw-stream artifact;
- no cleanup required;
- final state: `safe_idle`.

## ORION preflight

The read-only preflight passed using `.NET Stopwatch`:

- 64-bit PowerShell process: true;
- high-resolution clock: true;
- frequency: 10,000,000 Hz;
- monotonic sample count: 64;
- positive deltas: 63/63;
- minimum positive delta: 9 ticks;
- elapsed consistency: true;
- maximum anchor uncertainty: 6.4 microseconds;
- system clock changed: false;
- NTP changed: false;
- Windows Time service changed: false;
- capture started: false;
- final state: `safe_idle`.

## Bounded multistream probe

The metadata-only logical probe passed:

- duration request: 1,200 ms;
- logical envelope count: 264;
- window envelopes: 75;
- audio envelopes: 119;
- input envelopes: 70;
- maximum sample timestamp: 1,186.5345 ms;
- shared session epoch: true;
- all sequences contiguous: true;
- all timestamps monotonic non-decreasing: true;
- all samples inside the bounded window: true;
- clock discontinuity detected: false;
- real window capture: false;
- real audio capture: false;
- real input telemetry: false;
- raw logical events exported: false;
- cleanup required: false;
- final state: `safe_idle`.

## Local metadata evidence SHA-256

These files remain outside the repository and contain metadata only.

- ATLAS patch report:
  `8af430f8e146fe5490cc6c3386755d9d85e6fdbbb91020a344d5c47b554c6381`;
- ORION clock preflight:
  `cd70deee8affcefa010c1e54fb21aa72aae5943df8b49e34c2b491f249722cbb`;
- bounded multistream clock probe:
  `c1342cc1f3f4b9b99f45eacc978b5ac487725aa72ba2553a6cf0ca6cb7adead5`.

## Closed capabilities

Sprint 286 does not change the Windows system clock, NTP configuration, or
Windows Time service. It does not use the ATLAS clock for stream ordering and
does not use wall clock as the sole ordering source. Raw monotonic ticks, raw
logical envelopes, raw window frames, raw audio, and raw input are not exported.

Real window/audio/input alignment, long-running drift compensation, automatic
resampling, frame interpolation, audio time stretching, recording session
orchestration, Observer orchestration, Coach runtime, autonomous gameplay, and
multiplayer automation remain disabled.

Sprint 287 owns Game Companion session orchestration and the shared live session
state needed by the future native ORION overlay.
