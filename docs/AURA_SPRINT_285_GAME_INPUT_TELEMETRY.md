# AURA Sprint 285 - Game Input Telemetry

Status: complete; live ORION acceptance passed

- Version: `v1.4.5`
- Sprint: `285`
- Boundary: `game_input_telemetry`
- Previous checkpoint: `v1.4.4`
- Previous commit: `5370535ef172b5696107d416710ebc14edbf9f0a`
- Previous tree: `436239f3ea62f223f8b7f822ea5bfa17b827d778`
- Reference game: `osu_offline`
- Next sprint: `286`
- Next boundary: `game_timestamp_synchronization`

## Delivered boundary

Sprint 285 adds one explicit, permission-bound, foreground-only game-input
telemetry sample. ATLAS remains the review and permission authority. ORION is
the only observation host.

The exact reviewed `osu!.exe` process, process-start evidence, visible window,
and foreground window binding must remain valid for every poll. Focus loss
fails closed.

## Sanitized observation contract

Only these semantic events are allowed:

- `osu_key_1_down` and `osu_key_1_up`, mapped to `Z`;
- `osu_key_2_down` and `osu_key_2_up`, mapped to `X`;
- `mouse_left_down` and `mouse_left_up`;
- `mouse_right_down` and `mouse_right_up`;
- `cursor_normalized`, with coordinates normalized to the bound osu! client
  area.

The runtime does not export raw virtual keys, scan codes, characters, text,
clipboard data, raw window handles, executable paths, absolute screen
coordinates, or raw event records to ATLAS.

## Hard limits

- maximum observation request: five seconds;
- maximum event timestamp: 5,000 ms;
- polling interval contract: 17 ms;
- cursor sample-rate ceiling: 60 Hz;
- maximum events: 512;
- maximum encoded JSONL: 131,072 bytes;
- one temporary private ORION artifact;
- metadata and SHA-256 only on ATLAS;
- explicit cleanup and return to `safe_idle`.

## Live ORION acceptance

Live acceptance passed using a PowerShell `Add-Type` helper compiled in memory.

- implementation: foreground-gated allowlisted polling;
- exact target: one visible `osu!.exe` window;
- requested duration: five seconds;
- reported wall duration: 5,016 ms;
- minimum event timestamp: 1 ms;
- maximum event timestamp: 4,984 ms;
- event count: 128;
- action transitions: 7;
- normalized cursor events: 121;
- encoded size: 11,756 bytes;
- artifact SHA-256:
  `1af6c2fd25bc7d66def40ad9a849c4d122cd2cbcb03eb13f4a7856a75f0f2b4e`;
- sequence contiguous: true;
- timestamps monotonic: true;
- semantic allowlist only: true;
- normalized coordinates valid: true;
- foreground binding preserved: true;
- arbitrary key capture: false;
- text logging: false;
- background input capture: false;
- input hooks or Raw Input registration: false;
- input injection: false;
- raw events exported: false;
- temporary artifact deleted: true;
- final state: `safe_idle`.

The 5,016 ms wall duration includes loop shutdown overhead. The final observed
event timestamp was 4,984 ms, inside the 5,000 ms contract limit.

## Local metadata evidence SHA-256

These files remain outside the repository and contain metadata only.

- ATLAS patch report:
  `0e9b36c27c110f1e98704f545bc0cd4e95a3053acde9192534269fa735e04c8f`;
- ORION preflight:
  `4eebe748bff84f93500dba62a4167de5ad2768a649f2c2aad9716c54c07c627d`;
- in-memory helper compile probe:
  `1213fddf90e0f1d418a88565ea4cc7962d1456de29066724400e5b65d6022e5f`;
- foreground-only live acceptance:
  `99c2e0d4e2dcb07123994cf8e203bdca861fc80632b1cf976ba48c41e08396f4`;
- local metadata review:
  `0b153034f97749c09a7b736bf6c2f21830761ecb7e4de86aae956cfe5c0a7453`;
- explicit temporary-artifact cleanup:
  `79060eb08f1f97fdb37d4a3129fbab154222b827cf9404b76acd1b40000b538c`.

## Closed capabilities

Arbitrary-key observation, text or character logging, clipboard reads, raw
scan-code export, background input capture, global cursor history, absolute
screen-coordinate export, hooks, Raw Input registration, input injection,
keyboard or mouse control, controller control, continuous monitoring,
recording, coaching, autonomous gameplay, and multiplayer automation remain
disabled.

Sprint 286 owns cross-stream timestamp alignment, clock offset, drift, and
synchronization between window, audio, and input observations.
