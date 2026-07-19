# AURA Voice Daily-Use Activation

## Sprint 271 release checkpoint

- Version: `v1.3.1`
- Sprint: `271`
- Boundary: `voice_daily_use_activation`
- Next sprint: `272`
- Next boundary: `voice_auto_conversation_and_companion_context_reinforcement`
- Runtime host: ATLAS
- Browser microphone and playback host: ORION
- Canonical listener: `127.0.0.1:8765`
- External voice release: `/mnt/aura-data/AURA/voice/releases/20260719T160731Z`

## Delivered daily-use flow

Sprint 271 activates the first real local voice path for daily AURA use:

```text
explicit Hold to Talk or focused-page V
-> ORION microphone capture
-> bounded browser PCM/WAV encoding
-> localhost SSH tunnel
-> ATLAS faster-whisper STT
-> editable transcript preview
-> fragment-only Open Chat Draft
-> explicit manual chat send
-> visible local-model response
-> explicit Piper TTS generation
-> ORION playback with Stop/Esc
```

The dashboard remains safe by default. Opening a chat draft does not send a
message automatically, and TTS generation does not approve or dispatch an
action.

## Local voice backend

The backend is isolated from AURA's main virtual environment under
`/mnt/aura-data/AURA/voice/releases`.

- STT package: `faster-whisper 1.2.1`
- STT model: `Systran/faster-whisper-small`
- STT model revision: `536b0662742c02347bc0e980a01041f333bce120`
- STT execution: CPU `int8`
- TTS package: `Piper 1.5.0`
- TTS voice: `id_ID-news_tts-medium`
- TTS voice revision: `67265b`
- Raw uploaded and generated temporary audio: deleted after each request
- Request concurrency: single-flight
- Accepted upload type: WAV only
- Maximum upload: 2 MiB
- Maximum capture duration: 15 seconds

The current Piper voice is a replaceable baseline, not AURA's permanent
voice identity. Later releases may introduce reviewed voice profiles and a
legally sourced custom AURA voice while preserving this baseline as a
fallback.

## HTTP and browser surface

- `GET /api/voice/status`
- `POST /api/voice/transcribe`
- `POST /api/voice/synthesize`
- Dashboard controls: Hold to Talk, `V`, `Esc`, Open Chat Draft, Speak on
  ORION, playback, and stop
- Chat handoff uses a URL fragment and does not use browser Web Storage
- The transcript fragment is not sent to the server as part of the HTTP URL

## Browser security policy

```text
Permissions-Policy:
camera=(), microphone=(self), geolocation=(), payment=(), usb=()

Content-Security-Policy media directive:
media-src 'self' blob:
```

Remote media remains blocked. `default-src 'none'`, `object-src 'none'`,
`frame-ancestors 'none'`, `X-Frame-Options: DENY`, and
`Referrer-Policy: no-referrer` remain active.

## Real ORION acceptance

The reconciled live acceptance passed:

- acceptance assertions: `21/21`
- reconciliation assertions: `14/14`
- microphone permission: passed
- button push-to-talk: passed
- keyboard `V` push-to-talk: passed
- usable Indonesian STT transcript: passed
- chat draft without automatic send: passed
- explicit local-model chat response: passed
- audible TTS on ORION: passed
- playback interruption with Stop/Esc: passed
- capture cancellation with Esc: passed
- no unexpected action, wake-word capture, or cloud fallback: passed
- final safe-idle: passed
- final port `8765`: closed
- voice worker residue: none
- temporary audio leaks: zero
- acceptance evidence SHA-256: `d9a7aa1a5440ad8e67274a2ce1312fca04dcddf6da3c3afae963e4b28cb593f6`
- CSP evidence SHA-256: `773618fb7030c7cfe27fe466eeb34a02f4d343887db42b9e0d662ceacf92d82c`

A harness comparison originally reported a false negative because Python
`str.strip()` removed the first leading space from Git porcelain status.
Binary/content patch hashes before and after the run were identical, and the
fail-closed reconciliation verified the exact eight-entry working tree.

## Explicitly disabled in v1.3.1

- always-listening
- wake word
- automatic chat send
- automatic TTS playback
- hands-free turn taking
- voice-triggered sensitive approval
- direct voice action dispatch
- cloud STT or TTS fallback
- raw-audio retention
- public or LAN listener binding
- background voice listener
- hidden microphone capture

## Sprint 272 handoff

Sprint 272 targets `voice_auto_conversation_and_companion_context_reinforcement`:

```text
PTT release
-> automatic STT
-> explicit enabled auto-conversation session
-> local-model response
-> TTS
-> autoplay on ORION
```

Manual Review remains available. Sensitive actions continue to require a
visible preview and explicit approval. Sprint 272 also begins persona,
project-context, capability-status, session-history, and reviewed-memory
grounding so the model responds as AURA rather than as a generic chatbot.
