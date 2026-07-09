# AURA Genesis to Post-Genesis Product Plan

Status: PLANNED
Current Canonical Version: v0.154.0-genesis
Current Canonical Sprint: Sprint 144.0 — Service Configuration and Port Registry Foundation
Next Planned Sprint: Sprint 147.0 — Service Control Command Review Foundation
Final Genesis Target: Sprint 240.0 — Genesis Final Release v1.0.0-genesis
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

- Version: v0.154.0-genesis
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

### Sprint 181-190 — Voice Foundation Runtime

Purpose: introduce local voice interaction foundation.

Planned direction:

- voice input runtime
- push-to-talk or explicit listen boundary
- speech-to-text adapter
- voice intent understanding
- voice output / TTS
- voice permission and safety boundary
- voice audit link
- Control Center integration
- stabilization

Boundary:

- no always-listening mode by default
- no voice command execution without permission gate
- audit visible for voice-driven actions

### Sprint 191-200 — Vision / Screen Awareness Runtime

Purpose: introduce permission-gated visual and screen context.

Planned direction:

- screen permission boundary
- screenshot context pipeline
- visual context understanding
- screen region/app context
- camera input boundary
- visual safety and redaction
- visual memory link
- visual audit/permission link
- Control Center integration
- stabilization

Boundary:

- no silent screen capture
- no camera access without approval
- no sensitive visual storage without redaction and memory gate
- screen awareness must be visible in Control Center

### Sprint 201-210 — ORION Client Bridge

Purpose: connect ATLAS core with ORION Windows-side client safely.

Planned direction:

- ORION bridge foundation
- pairing and trust boundary
- status and heartbeat
- screen context bridge
- command receive boundary
- creative tool context bridge
- audit and permission link
- reconnect safe-idle
- Control Center integration
- stabilization

Boundary:

- ORION must be paired and trusted
- ORION must expose status and disconnect controls
- no silent desktop control
- no silent game input
- no silent app/file action

### Sprint 211-220 — Avatar / Presence Foundation

Purpose: introduce AURA's visible presence.

Planned direction:

- avatar/presence foundation
- status and emotion mapping
- voice lip sync / viseme boundary
- idle presence animation
- motion capture bridge plan
- OBS / streaming scene integration
- livestream persona mode
- avatar permission/audit link
- stabilization

Boundary:

- avatar is expression first, not uncontrolled automation
- livestream mode must be safe and controllable
- OBS integration must be explicit and local
- no unauthorized scene switching or stream action

### Sprint 221-230 — Final Genesis Integration

Purpose: integrate all Genesis systems.

Planned direction:

- service + Control Center + chat integration
- memory + permission + audit integration
- voice integration pass
- vision integration pass
- ORION + avatar integration pass
- end-to-end safe workflow test
- Genesis test matrix
- release checklist
- review and stabilization

Boundary:

- integration must not bypass permission gates
- all runtime actions require audit trail
- safe-idle fallback remains active

### Sprint 231-240 — Genesis Release Candidate

Purpose: finalize AURA v1.0.0-genesis.

Planned direction:

- RC freeze
- bugfix pass
- final security/safety review
- final usability review
- backup/recovery finalization
- Genesis demo scenario
- README/docs/roadmap final pass
- release candidate validation
- v1.0.0 acceptance pass
- Genesis Final Release

## Genesis Final Target

At v1.0.0-genesis, AURA should be born as a safe local-first AI partner.

Genesis Final target:

- local ATLAS service foundation
- local Control Center
- local chat runtime
- gated memory read/write
- permission system
- audit system
- safe-idle fallback
- voice foundation
- vision/screen awareness with permission
- ORION bridge foundation
- avatar/presence foundation
- clear documentation and release checklist

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
