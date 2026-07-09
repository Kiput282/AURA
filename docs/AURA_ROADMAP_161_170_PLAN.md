# AURA Roadmap 161-170 — Local Chat Runtime

This block turns AURA from a blueprint-heavy system into a safe thin local chat
runtime. The goal is not autonomy. The goal is a local, permission-aware chat
loop that can be tested from the CLI and later connected to memory, voice,
vision, and action layers.

## Sprint sequence

- Sprint 161 — Local Chat Runtime Foundation
- Sprint 162 — Local Chat CLI Session Alpha
- Sprint 163 — Local Chat Message Store
- Sprint 164 — AURA Persona Response Layer
- Sprint 165 — Model Adapter Boundary
- Sprint 166 — Permission-Gated Model Request
- Sprint 167 — Chat Safety + Uncertainty Layer
- Sprint 168 — Chat History Viewer Contract
- Sprint 169 — Local Chat Integration Review
- Sprint 170 — Local Chat Runtime Stabilization

## Deferred capabilities

- Voice starts in Sprint 181-190.
- Vision/screen awareness starts in Sprint 191-200.
- Local action and desktop commands, such as opening Blender, opening VS Code,
  and creating project folders, start around Sprint 201-210 after permission,
  audit, allowlist, and recovery boundaries are ready.

## Runtime safety

The block must keep command execution, file mutation, plugin action execution,
desktop control, public network exposure, and autonomous actions disabled until
later explicitly gated runtime blocks.


## Sprint 162 Direction — Local Chat CLI Session Alpha

Sprint 162 introduces the first safe thin runtime for AURA local chat: a one-turn
CLI alpha that creates a transient in-memory session packet and returns a safe
AURA persona response. It keeps message persistence, model runtime, memory
runtime, command execution, file mutation, desktop control, voice, vision,
network access, and autonomous actions disabled. Sprint 163 should add the local
chat message store.


## Sprint 163 Direction — Local Chat Message Store

Sprint 163 introduces a controlled local message store for AURA chat. It allows
one manual CLI chat turn to be appended to an AURA-owned JSONL store while model
runtime, memory runtime, command execution, arbitrary file mutation, desktop
action, voice, vision, network access, and autonomous actions remain disabled.
Sprint 164 should add the AURA Persona Response Layer.


## Sprint 164 Direction — AURA Persona Response Layer

Sprint 164 adds a deterministic persona response layer so AURA's local chat alpha
feels more consistent and honest. It classifies simple persona modes, gives
capability-aware responses, politely refuses action requests, and continues to
append controlled local chat turns to the JSONL message store. Model runtime,
memory runtime, command execution, arbitrary file mutation, desktop action,
voice, vision, network access, and autonomous actions remain disabled. Sprint
165 should add the Model Adapter Boundary without automatically dispatching
model requests.
