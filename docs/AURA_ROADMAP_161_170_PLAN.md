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
- Sprint 166 — Permission-Gated Model Request
- Sprint 166 — Permission-Gated Model Request
- Sprint 167 — Chat Safety + Uncertainty Layer
- Sprint 168 — Chat History Viewer Contract
- Sprint 170 — Local Chat Runtime Stabilization
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
165 should add the Permission-Gated Model Request without automatically dispatching
model requests.


## Sprint 166 Direction — Permission-Gated Model Request

Sprint 166 defines the model adapter boundary for AURA local chat. It introduces
a dry-run adapter packet, provider metadata contract, prompt envelope contract,
response envelope contract, model error boundary, credential/network boundary,
and Sprint 166 permission handoff. It does not dispatch model requests, call
local or remote providers, read credentials, write memory, execute commands, or
mutate arbitrary files.


## Sprint 166 — Permission-Gated Model Request

Sprint 166 adds the permission-gated model request dry-run layer. AURA can create a permission preview packet and a model request envelope, but the gate decision remains blocked without explicit grant. No model request is dispatched, no local LLM process starts, no remote API/network call occurs, no credential is read, no memory is written, no command executes, and no arbitrary file mutation happens.

Next: Sprint 167 — Chat Safety + Uncertainty Layer.


### Sprint 170 — Local Chat Runtime Stabilization

Status: completed in v0.170.0-genesis.

Sprint 170 reviews the local chat alpha chain and verifies that CLI session alpha, message store, persona response, model adapter boundary, permission-gated model request, safety/uncertainty, and history viewer remain integrated behind safe boundaries. The review is metadata-only and read-only: no model dispatch, network, credentials, memory writes, audit writes, command execution, arbitrary file access, desktop action, voice, vision, or full chat runtime activation.
