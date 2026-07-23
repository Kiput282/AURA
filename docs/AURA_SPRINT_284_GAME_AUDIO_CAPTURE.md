# AURA Sprint 284 — Game Audio Capture

Status: complete; live ORION acceptance passed

- Version: `v1.4.4`
- Sprint: `284`
- Boundary: `game_audio_capture`
- Previous checkpoint: `v1.4.3`
- Previous commit: `62c304b59547cff0774c9ee8244774f97d49929c`
- Reference game: `osu_offline`
- Next sprint: `285`
- Next boundary: `game_input_telemetry`

## Delivered boundary

Sprint 284 adds one explicit, permission-bound game-audio sample. ATLAS creates
the visible preview, grants one expiring single-use permission, authorizes one
request, and reviews a metadata-only receipt. ORION is the only capture host.

The real ORION source must use Windows process-loopback
`VAD\Process_Loopback` with `IncludeTargetProcessTree` for the exact reviewed
`osu!.exe` process. Missing helper support fails closed. Microphone enumeration,
microphone capture, arbitrary endpoint selection, and whole-system fallback are
forbidden.

## Hard limits

- reference game `osu_offline`;
- exact agent, device, game, process, executable, and window evidence;
- maximum duration five seconds;
- WAV signed 16-bit PCM;
- 48 kHz stereo;
- maximum encoded size one MiB;
- one temporary private ORION artifact;
- metadata and SHA-256 only on ATLAS;
- no raw audio or local path in ATLAS packets;
- explicit cleanup and return to `safe_idle`.

## Closed capabilities

Continuous audio capture, recording sessions, transcription, telemetry,
coaching, application launch, voice-command-to-action, keyboard, mouse,
controller, autonomous gameplay, multiplayer automation, public streaming
output, and persistent raw-audio storage remain disabled.

## Live ORION acceptance

Live acceptance passed on ORION using Windows process-loopback for exactly one
visible `osu!.exe` process and its target process tree.

- implementation path: PowerShell `Add-Type` helper compiled in memory;
- source contract: `VAD\Process_Loopback`;
- mode: `PROCESS_LOOPBACK_MODE_INCLUDE_TARGET_PROCESS_TREE`;
- requested duration: five seconds;
- captured duration: 4,990 ms;
- format: PCM signed 16-bit, 48 kHz, stereo;
- frame count: 239,520;
- encoded size: 958,124 bytes;
- signal detected: true;
- microphone read or enumeration: false;
- whole-system audio or fallback: false;
- raw audio exported to ATLAS: false;
- temporary artifact deleted after review: true;
- final runtime state: `safe_idle`.

The private WAV remained on ORION only for bounded review and was deleted after
its SHA-256 and metadata were verified. No raw audio or local path is committed.

### Local audit evidence SHA-256

- patch report:
  `3ce6e8db38037664cddb1a8168e2396d47b733f66140e96ee248227bc665cc81`;
- ORION preflight:
  `63de409376aabb797dde241325c17fa7844765a2f755e2621aeffb6a8375b783`;
- in-memory helper compile probe:
  `97993f6ba5af15d2cdbce7731c50646f40b13c1ff71658e405bef4dfdb1f9edf`;
- process-loopback acceptance metadata:
  `f0769139fbb7d7a9f1a274f5a03bc1724ff1bf26e216f805a57544194395dd2e`;
- explicit temporary-audio cleanup:
  `f614bc7aa936ffbf74a633e84a34278702d47ecdb1449198870bc34f6bf74dac`.

These evidence files remain outside the repository and contain metadata only.

Sprint 285 owns `game_input_telemetry`.
