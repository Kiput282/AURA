# AURA Genesis to Post-Genesis Product Plan

Status: CANONICAL GENESIS PATH
Current Canonical Version: v0.186.0-genesis
Current Canonical Sprint: Sprint 186 — Browser Chat Session Runtime
Next Planned Sprint: Sprint 187 — Local Model Bridge Activation
Final Genesis Target: Sprint 240 — Genesis Final Release v1.0.0-genesis
Owner: Kiput
Motto: Grow Together

## Purpose

This document defines AURA's product direction from the current Genesis path through Final Genesis and into the post-Genesis future.

AURA is a local-first AI partner.

ATLAS is planned as AURA's core brain, safety, service, permission, audit, memory, planning, and local runtime machine.

ORION is planned as the future Windows-side client for desktop presence, creative tools, avatar, game companion, screen context, livestreaming, and visual/audio interaction.

AURA must grow gradually. Runtime capability must be introduced only through explicit review, permission gates, audit links, safe-idle fallback, Control Center visibility, and Creator approval.

## Current State

AURA is currently at:

- Version: v0.170.0-genesis
- Sprint: Sprint 144.0
- State: READY
- Completed block: Sprint 131-140 runtime planning block
- Active block: Sprint 151-160 Control Center Runtime
- Next sprint: Sprint 147.0 — Service Control Command Review Foundation

Current AURA is not yet an active autonomous runtime system.

AURA currently has strong planning, review, registry, status, CLI, shell, documentation, permission, memory, audit, and runtime-boundary foundations, but it does not yet run local service runtime, dashboard runtime, chat runtime, memory runtime, permission runtime, audit runtime, ORION bridge runtime, avatar runtime, or game companion runtime.

## Genesis Roadmap from Current State

### Sprint 141-150 — Local Service Runtime Foundation

Purpose: prepare AURA's safe local service foundation on ATLAS.

Planned direction:

- Sprint 141.0 — Local Service Runtime Foundation
- Sprint 142.0 — Local Service Safe Idle Boot Boundary
- Sprint 143.0 — Local Service Health Endpoint Foundation
- Sprint 144.0 — Service Configuration and Port Registry Foundation
- Sprint 145.0 — Service Permission Gate Runtime Boundary
- Sprint 146.0 — Service Audit Link Foundation completed
- Sprint 147.0 — Service Control Command Review Foundation completed
- Sprint 147.0 — Service Control Command Review Foundation
- Sprint 148.0 — Service Recovery and Restart Policy Foundation
- Sprint 149.0 — Service Security and Localhost Binding Review
- Sprint 150.0 — Review & Stabilization 141-150 completed

Boundary:

- localhost-only by default
- no public network exposure
- no silent port binding
- no unrestricted runtime execution
- no tool, action, file, or command execution without permission gates

### Sprint 151-160 — Control Center Runtime

Purpose: introduce a local Control Center for monitoring AURA safely.

Planned direction:

- service status panel
- capability registry viewer
- runtime gates viewer
- permission center read-only runtime
- audit viewer foundation
- service control UI review
- localhost-only security review
- review and stabilization

Boundary:

- read-only first
- no hidden controls
- all runtime gates visible
- permission and audit status visible before runtime expansion

### Sprint 161-170 — Local Chat Runtime

Purpose: introduce safe local chat sessions.

Planned direction:

- local chat runtime foundation
- chat session API boundary
- safe response mode
- chat session state
- local model gateway
- chat permission prompt bridge
- chat audit link
- chat safe-idle fallback
- Control Center integration
- review and stabilization

Boundary:

- chat first, action later
- no tool execution from chat without approval
- no memory write without explicit gate
- no desktop or ORION control from chat by default

### Sprint 171-180 — Memory Runtime

Purpose: introduce gated memory runtime.

Planned direction:

- memory schema
- memory read gate
- memory write proposal
- manual approval
- redaction and conflict review
- workspace memory link
- audit and rollback
- search/recall safe mode
- stabilization

Boundary:

- no silent memory write
- Creator approval required for long-term memory writes
- audit link required for memory mutation
- rollback path required

### Sprint 181-190 — Local Interaction Runtime Activation

Purpose: make AURA usable through a safe local service, localhost Control Center,
and interactive browser chat before voice activation.

Planned direction:

- localhost-only web runtime activation cutline
- manual foreground service lifecycle
- real health and status API
- Control Center backend data runtime
- usable Control Center web shell
- browser chat session runtime
- permission-gated local model bridge
- integrated interactive dashboard chat
- visible permission, audit, error, and recovery state
- block review and stabilization

Boundary:

- bind only to `127.0.0.1`
- safe-idle is the default state
- no public or LAN exposure
- no arbitrary command, tool, desktop, or file execution
- no automatic permission grants
- chat and model failures must remain visible and recoverable

### Sprint 191-200 — Voice Interaction Runtime

Purpose: add explicit local voice interaction after dashboard and chat are stable.

Planned direction:

- voice runtime activation foundation
- push-to-talk and explicit listen state
- local microphone capture boundary
- speech-to-text adapter runtime
- voice intent and chat integration
- text-to-speech adapter runtime
- voice permission and audit runtime
- Control Center voice controls
- integration review
- stabilization

Boundary:

- no always-listening mode
- microphone use must be explicit and visible
- voice input does not bypass chat, intent, permission, or action gates
- speech output must be interruptible
- voice-triggered actions require the same approval as typed actions

### Sprint 201-210 — Vision and Screen Awareness Runtime

Purpose: add permission-gated visual and screen context.

Planned direction:

- vision runtime activation foundation
- explicit screenshot capture
- screen context adapter
- local vision model adapter
- visual permission, privacy, and redaction
- workspace visual understanding
- vision-to-chat context handoff
- Control Center vision panel
- integration review
- stabilization

Boundary:

- no silent screen or camera capture
- capture target and state must be visible
- sensitive visual content requires redaction and memory gates
- visual understanding cannot directly execute actions
- camera runtime is optional and must not block screenshot-based Genesis scope

### Sprint 211-220 — Permission, Audit, and Safe Local Actions

Purpose: activate narrow, reviewable local actions under explicit permission.

Planned direction:

- active permission runtime
- grant, denial, revocation, and expiry lifecycle
- runtime audit writer
- action proposal and preview runtime
- safe local open actions
- allowlisted application launch
- controlled folder and simple file creation
- dashboard approval workflow
- rollback, emergency stop, and recovery
- stabilization

Boundary:

- every action requires clear scope and visible approval
- no arbitrary shell execution
- no file deletion or mass mutation
- no unrestricted desktop control
- no dependency installation without separate informed permission
- all executed actions require audit and recovery evidence

### Sprint 221-230 — Unified Partner Runtime Integration

Purpose: connect chat, voice, vision, memory, permission, audit, workspace, and
safe actions as one coherent local partner runtime.

Planned direction:

- unified session runtime
- workspace and project context runtime
- chat-to-memory handoff
- chat, voice, and vision context fusion
- personality consistency runtime
- multi-interface state synchronization
- service persistence and launcher
- safe auto-start evaluation
- Genesis acceptance rehearsal
- unified runtime stabilization

Boundary:

- interface integration must not bypass permission gates
- memory relevance must not become silent memory mutation
- safe-idle and emergency stop remain authoritative
- service persistence is allowed only after recovery behavior is proven
- ORION and avatar presence are not required for this block

### Sprint 231-240 — Genesis Final Integration and Release

Purpose: finalize AURA v1.0.0-genesis as a safe, usable local AI partner.

Planned direction:

- Genesis Final runtime cutline
- end-to-end security review
- privacy and data integrity review
- failure and recovery drills
- dashboard and interaction UX polish
- launcher and deployment stabilization
- installation, backup, and migration flow
- final Genesis acceptance test
- v1.0.0 release candidate
- Genesis Final release

Boundary:

- acceptance evidence must cover chat, voice, vision, memory, permission, audit,
  safe actions, recovery, and user-visible status
- release cannot bypass unresolved critical safety blockers
- safe-idle remains the default and recovery destination
- Post-Genesis capabilities cannot be pulled into the release as hidden blockers
## Genesis Final Target

At v1.0.0-genesis, AURA should be born as a safe local-first AI partner.

Genesis Final target:

- local ATLAS service runtime
- localhost Control Center with real status
- interactive browser chat with local model integration
- safe session and history persistence
- gated and privacy-aware memory use
- explicit voice interaction
- permission-gated screenshot and screen awareness
- active permission lifecycle
- visible audit and recovery state
- previewed, narrowly allowlisted safe local actions
- unified workspace and project context
- reliable launcher, backup, migration, and safe-idle behavior
- clear documentation and release evidence

ORION client integration, avatar/presence runtime, advanced desktop control,
Game Companion execution, and streaming automation remain Post-Genesis
directions and are not Genesis Final release blockers.

Genesis Final is not the endpoint. It is AURA's birth point.

## Post-Genesis Phases

### Phase 1 — Post-Genesis Hardening

Focus:

- reliability
- bugfixes
- backup and recovery
- audit persistence
- memory stability
- service uptime
- Control Center usability
- security review

### Phase 2 — Creative Partner Expansion

Focus:

- Blender helper
- texture and UV assistance
- animation planning
- video production assistance
- OBS workflow helper
- project workspace awareness
- asset pipeline support

### Phase 3 — Game Companion Foundation

Focus:

- safe game observation
- coaching before control
- offline/private/single-player first
- screen/audio feedback learning
- game session memory
- devlog documentation
- viewer interaction planning

Game Companion order:

1. Minecraft Companion
2. osu Companion
3. Beat Saber Companion
4. Monster Hunter Companion

### Phase 4 — Streaming / Avatar Identity

Focus:

- virtual rhythm performer identity
- avatar reactions
- cinematic camera planning
- livestream challenge queue
- OBS scene coordination
- audience-safe interaction
- devlog and performance content

### Phase 5 — Advanced ORION Runtime

Focus:

- stronger desktop context
- creative tool bridge
- screen/app-specific awareness
- controlled automation with approval
- local model routing
- multi-agent planning
- richer avatar presence

## AURA Features and Skills

### Current Foundation Skills

At v0.140.0-genesis, AURA has foundation and review skills such as:

- roadmap planning
- project status review
- capability registry visibility
- plugin/action registry planning
- permission workflow planning
- memory write gate review
- audit writer activation review
- local service boot planning
- control center runtime entry review
- chat runtime minimal loop review
- runtime activation blocker review
- safety boundary documentation
- stabilization checkpoint review

These are mostly planner-only, foundation-only, or review-only skills.

### Genesis Target Skills

By Genesis Final, AURA should gain:

- local chat
- local service control visibility
- memory recall with gates
- memory write proposal and approval
- permission prompt workflow
- audit trail visibility
- voice input/output foundation
- vision/screen context with approval
- ORION bridge foundation
- avatar/presence foundation
- Control Center monitoring
- safe-idle fallback

### Post-Genesis Skills

After Genesis, AURA may grow into:

- coding partner
- creative assistant
- Blender helper
- streaming assistant
- OBS assistant
- avatar performer
- Minecraft companion
- osu rhythm learner
- Beat Saber rhythm performer
- Monster Hunter coach
- long-term project partner
- local workflow assistant

## What AURA Can Currently Do

At v0.140.0-genesis, AURA can:

- boot to READY
- expose identity and version
- show capability registry metadata
- show skill and plugin action metadata
- provide planner-only review packets through CLI/shell
- document sprint progress
- maintain roadmap and journal records
- define safety boundaries
- define future runtime plans
- validate that runtime counters remain zero
- support Git-tracked project evolution

## What AURA Cannot Currently Do Yet

At v0.140.0-genesis, AURA cannot yet:

- run as an active local service
- serve a real web Control Center
- run a real chat session runtime
- read or write memory at runtime
- create or apply permission grants at runtime
- start audit writers
- write audit events
- listen to microphone input
- speak through TTS
- see the screen or camera
- connect to ORION
- control desktop apps
- control games
- control OBS
- control Blender
- control avatar runtime
- execute tools or commands autonomously
- read/write/modify/delete files at runtime
- bind ports as active runtime services
- perform network probes
- perform ORION handshakes
- perform git runtime actions

## What AURA Must Never Do Without Approval

AURA must never silently:

- execute commands
- modify files
- delete files
- write memory
- start services
- bind ports
- expose network services
- control ORION
- control desktop input
- control game input
- control OBS or livestream actions
- access microphone
- access camera
- capture screen
- create permission grants
- write audit logs
- submit online game scores
- automate ranked or multiplayer gameplay
- exploit games or services
- bypass safety gates

## Core Design Principle

AURA should grow like a trusted partner, not like an uncontrolled automation system.

Every major capability must pass through:

1. planning
2. review
3. permission gate
4. audit link
5. safe-idle fallback
6. Control Center visibility
7. Creator approval


## Sprint 142.0 Update

Sprint 142.0 adds safe-idle boot boundary planning for the future ATLAS local service. It preserves safe-idle as the default boot posture, blocks autostart and service activation, keeps readiness probes read-only, and ensures permission or audit failure keeps AURA idle. Runtime execution remains 0.


## Sprint 143.0 Update

Sprint 143.0 adds health endpoint foundation planning for the future ATLAS local service. It defines a future localhost-only, read-only `/health` contract, response schema, safe-idle health states, dependency visibility, permission/audit health linkage, Control Center health card planning, and no-health-endpoint-activation boundary. Runtime execution remains 0.


## Sprint 147.0 — Service Control Command Review Foundation

Sprint 147 adds planner-only, metadata-only service control command review boundaries for future start/stop/restart/status service commands. Runtime remains disabled: no command execution, no systemd execution, no service start/stop/restart, no process status probe, no socket open, no port bind, and no runtime execution features.


## Sprint 161 Direction — Local Chat Runtime Foundation

Sprint 161 begins the Local Chat Runtime block. The agreed Genesis Final path is
chat → memory → voice → vision → action. Sprint 161 remains a safe foundation
for session/message/chat-loop contracts and Sprint 162 CLI alpha readiness. It
does not enable model runtime, command execution, file mutation, desktop
control, voice, vision, or autonomous actions.


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


## Sprint 167 — Chat Safety + Uncertainty Layer

Sprint 167 adds a deterministic local safety and uncertainty alpha layer before any future model request. It supports one-message safety/uncertainty review, capability honesty, and freshness-boundary replies while keeping model request dispatch, network, credential reads, memory writes, command execution, and arbitrary file mutation disabled.


## Sprint 168 — Chat History Viewer Contract

AURA v0.170.0-genesis adds a read-only Chat History Viewer Contract for the local chat message store. The viewer can inspect AURA-owned JSONL chat history metadata and recent turns from the controlled message store path, while keeping model requests, model responses, network requests, credential reads, permission grants, memory writes, audit writes, command execution, arbitrary file reads, arbitrary file writes, desktop action, and runtime execution disabled.


## Sprint 170 — Local Chat Runtime Stabilization

AURA v0.170.0-genesis reviews the local chat runtime alpha chain introduced across Sprints 161-168. It confirms the CLI session alpha, message store, persona response layer, model adapter boundary, permission gate, safety/uncertainty layer, and history viewer are integrated as a safe thin runtime path while full model runtime, network, credentials, memory runtime, command execution, arbitrary file access, desktop action, voice, and vision remain disabled.


## Sprint 171 — Memory Runtime Foundation

`v0.171.0-genesis` starts the Memory Runtime block with a preview-only memory foundation. AURA can create memory candidate previews and write-gate metadata, but real memory write remains disabled until explicit permission, review, privacy, and correction/deletion boundaries are implemented.


## Sprint 172 — Memory Write Permission Gate

`v0.172.0-genesis` adds a default-deny single-candidate memory permission gate. Candidate fingerprints and permission envelopes are previewed in process, but grants, memory writes, store mutation, audit writes, model/network activity, commands, and arbitrary file access remain disabled.


## Sprint 173 — Memory Extraction Dry Run

`v0.173.0-genesis` adds deterministic, no-model extraction of one reviewable memory candidate with trigger detection, normalization, classification, common sensitive-pattern screening, fingerprinting, and permission-gate handoff metadata. Candidate persistence, grants, memory writes/store mutation, network, credentials, audit writes, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 174 — Memory Importance and Pinning Policy

`v0.174.0-genesis` adds deterministic, explainable importance scoring, durability/temporary signal detection, retention recommendations, and future pin-eligibility previews. Candidate persistence, grants, memory writes/store mutation, pin/unpin actions, model/network activity, credentials, audit writes, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 175 — Memory Review Queue

`v0.175.0-genesis` adds an ephemeral, deterministic manual-review queue preview for memory candidates with priority, privacy, permission, and future-decision metadata. Queue persistence, decision application, grants, memory writes/store mutation, pin/unpin actions, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 176 — Memory Correction and Deletion Boundary

`v0.176.0-genesis` adds exact-target correction and tombstone-first deletion previews, with separate future purge permission. Store reads, lookups, mutations, grants, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 177 — Chat-to-Memory Handoff Contract

`v0.177.0-genesis` adds an explicit-user-turn, preview-only chat-to-memory handoff with exact source binding, privacy precheck, review-queue routing, and default-deny permission state. Chat-store/history reads, automatic handoff, queue persistence, grants, memory writes/store mutation, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 178 — Memory Privacy and Redaction Layer

`v0.178.0-genesis` adds deterministic redaction previews and strict secret-block boundaries for the memory pipeline. Original and redacted candidates remain unpersisted; review decisions, grants, memory writes/store mutation, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 179 — Memory Runtime Integration Review

`v0.179.0-genesis` validates the Sprint 171-178 memory chain as a single read-only integration surface. All component readiness, privacy, review, permission, and correction/deletion boundaries pass while release, persistence, mutation, model, network, command, audit, arbitrary-file, and runtime execution gates remain closed.


## Sprint 180 — Memory Runtime Stabilization

`v0.180.0-genesis` closes the Sprint 171-180 Memory Runtime block. Nine memory components pass stabilization with zero dependency gaps and runtime violations while privacy, review, permission, correction/deletion, release, mutation, model, network, command, arbitrary-file, voice, and runtime execution gates remain closed. The next block is Sprint 181-190 Local Interaction Runtime Activation. Voice moves to Sprint 191-200 after the dashboard and chat runtime are operational and stabilized.

## Sprint 187 Product Activation Note

AURA now has a bounded backend path from browser chat sessions to an
explicitly configured localhost text model. This is not yet the final
interactive chat product surface: Sprint 188 will integrate the model controls
and conversation experience into the Control Center chat UI.

No online provider, model download, tool use, external action, or autonomous
behavior is enabled.

## Sprint 188 Product Activation Note

AURA now has a usable localhost browser chat experience. The interface keeps
save-only messaging as the safe default and exposes local-model use only when
a provider is active and the user confirms the individual request.

This remains a bounded local alpha: no online model provider, model download,
tool use, external action, browser storage, or autonomous behavior is enabled.

## Sprint 189 Product Activation Note

AURA's localhost Control Center can now explain which interactions require
confirmation, which audit events are defined, which values are redacted, and
how an operator can recover safely from common failures.

The surface remains read-only. It cannot grant permissions, write audit
events, retry actions automatically, restart services, execute rollback, or
increase model/tool authority.


## Sprint 190 — Local Interaction Runtime Stabilization

`v0.190.0-genesis` completes the Local Interaction Runtime Activation block.

AURA now has a bounded usable local interaction product surface:

- localhost Control Center;
- interactive browser chat;
- persistent bounded sessions;
- explicitly confirmed local-model responses;
- transparent health and runtime state;
- visible permission, audit-contract, and recovery guidance;
- stable foreground startup and clean shutdown;
- fail-closed listener and port boundaries.

The checkpoint passes nine component reviews, ten dependency self-tests, and
1,175 total assertions with zero gaps and zero runtime violations.

Voice, vision, broad actions, ORION, avatar, livestream automation, game
control, and autonomy remain outside this checkpoint.


## Sprint 191 — Voice Runtime Activation Foundation

`v0.191.0-genesis` starts the Voice Interaction Runtime block.

AURA now has a safe voice activation foundation contract that prepares the path
for explicit push-to-talk voice interaction while preserving the stable
localhost Control Center, browser chat, session, model permission, permission
visibility, audit-contract, and recovery-visibility foundations from the Local
Interaction Runtime block.

The checkpoint confirms:

- voice activation foundation readiness;
- safe idle default;
- explicit push-to-talk requirement;
- explicit listen requirement;
- stable chat/session reuse requirement;
- reuse of the existing `microphone_listen` permission action;
- reuse of the existing `speaker_speak` permission action;
- disabled always-listening, hidden capture, wake word, silent cloud fallback,
  direct voice-to-action execution, microphone capture, speaker playback,
  STT/TTS runtime, audio file writes, and command execution.

This is not live voice yet. It is the activation foundation that lets later
sprints add push-to-talk state, microphone boundary, STT, chat integration,
TTS, permission/audit linkage, and Control Center voice controls without
breaking the established safety model.

Next product block: Sprint 191-200 Voice Interaction Runtime.


## Sprint 192 — Push-to-Talk and Explicit Listen State

`v0.192.0-genesis` adds the explicit push-to-talk listen-state foundation.

AURA now has a safe voice-state contract for moving from activation foundation
toward live voice without opening microphone capture yet. The state contract
keeps the current/default state at `idle`, declares the future allowed
listen-state path, requires explicit listen and explicit stop, and requires
microphone permission before any future live listening.

The checkpoint confirms that microphone capture, audio buffering, STT runtime,
listen loop, background listener, wake word, always-listening, hidden capture,
silent cloud fallback, direct voice-to-action execution, state persistence,
state mutation, audio device access, and command execution remain disabled.

This is still not live voice. It is the explicit listen-state boundary that
lets Sprint 193 define the local microphone capture boundary without creating
hidden capture or background listening behavior.


## Sprint 193 — Local Microphone Capture Boundary

`v0.193.0-genesis` adds the local microphone capture boundary contract.

AURA now has a safe boundary definition for future microphone capture without
opening live recording. The contract requires microphone permission, an
explicit listen state, and push-to-talk before any future capture. The required
future capture state is `listening_explicit`.

The checkpoint confirms that microphone capture runtime, audio device access,
audio device discovery, device enumeration, recording, audio buffering, audio
file writes, audio persistence, audio transmission, STT runtime, transcription,
listen loop, background listener, wake word, always-listening, hidden capture,
silent cloud fallback, direct voice-to-action execution, command execution, and
speaker playback remain disabled.

This is still not live voice capture. It is the local microphone capture
boundary that lets Sprint 194 add the Speech-to-Text Adapter Runtime without
creating hidden capture, background listening, or unintended audio retention.
