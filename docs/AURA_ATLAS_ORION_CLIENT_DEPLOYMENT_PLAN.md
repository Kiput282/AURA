# AURA ATLAS-ORION Client Deployment Plan

Status: CANONICAL DEPLOYMENT DIRECTION
Current anchor: v0.92.0-genesis
Owner: Kiput
Project motto: Grow Together

## Purpose

This document defines the long-term deployment direction for AURA across ATLAS and ORION.

AURA should not force every workload to run on one machine. ATLAS should remain the core server, brain, memory, permission authority, planner, and audit center. ORION should act as the local client workstation that provides AURA with screen access, voice access, avatar presence, local app bridges, local action execution, and GPU-heavy visual or creative workloads.

This document exists so future Control Center, API schema, data aggregator, client agent, action bridge, voice, vision, avatar, Blender, VS Code, game companion, streaming, and plugin work remains aligned.

## Core Split

### ATLAS Role

ATLAS is the AURA core server.

ATLAS is responsible for:

- AURA core reasoning
- personality and identity
- memory and long-term state
- permission manager
- planning and decision making
- action proposal creation
- audit log and journal
- dashboard backend in future runtime stages
- API and Control Center backend in future runtime stages
- plugin registry
- device registry
- client pairing authority
- session state
- safety policy
- roadmap and continuity state

ATLAS should be treated as the brain, memory, planner, and authority layer.

### ORION Role

ORION is the AURA client workstation.

ORION is responsible for:

- AURA Client Agent
- screen capture
- short screen recording
- frame sampling
- microphone capture
- speaker output
- voice playback
- avatar runtime
- 3D environment runtime
- lip sync
- expression sync
- OBS and streaming bridge
- game companion capture
- Blender bridge
- VS Code or local project bridge
- local file/folder/software action bridge
- local permission prompt
- emergency stop
- local app/plugin execution
- GPU-heavy visual workloads

ORION should be treated as the eyes, ears, voice, hands, body, and local reflex layer.

## Conceptual Model

AURA should be understood as one AI Partner with distributed components.

ATLAS is the brain.

ORION is the body and local client.

The ORION Agent is not a separate personality. It is a trusted client executor, sensor bridge, visual renderer, and local tool layer for AURA.

AURA thinks.
The agent sees, hears, displays, and executes.
Permission defines the boundary.
Audit log records the result.

## General Command Flow

The default command flow is:

1. User gives an instruction.
2. ORION Agent captures the relevant input.
3. ORION sends the request, context, or metadata to ATLAS.
4. AURA core on ATLAS analyzes the request.
5. AURA creates a response, plan, or action proposal.
6. Permission is checked.
7. ORION executes only approved local actions.
8. ORION sends result, output, or error back to ATLAS.
9. ATLAS records the action in journal, audit log, or memory where appropriate.

Default flow:

User -> ORION Agent -> ATLAS AURA Core -> ORION Agent -> Local result

This flow is safe for normal commands, but not every real-time behavior should wait for a full round trip.

## Latency Principles

AURA must avoid unnecessary delay by separating normal commands from fast local reflexes.

### Normal Command Path

Normal commands may go through ATLAS.

Examples:

- chat
- open folder
- open file
- open allowlisted software
- create folder with approval
- create simple file with approval
- check status
- analyze a screenshot
- plan a project task
- prepare a Blender workflow
- prepare a VS Code patch

This path can tolerate small delay because the action is deliberate and reviewable.

### Fast Local Reflex Path

Fast local reflexes should be handled by ORION.

Examples:

- show listening state
- show thinking state
- show speaking state
- animate avatar idle state
- render expression change
- run lip sync
- play voice output
- display emergency stop
- stop local client activity immediately
- update OBS/avatar visuals
- react visually to local state

ATLAS sends high-level state. ORION renders or reacts locally.

### Session Approved Action Path

Some actions may be approved for a limited session.

Examples:

- allow screen capture for one app for 10 minutes
- allow reading the active Blender window during this session
- allow creating files inside one workspace folder
- allow opening files under one project root
- allow OBS status reading during one stream
- allow game companion observation for one game window

ORION can act within the approved scope without asking ATLAS for every small local step.

### Real-Time Companion Path

Game companion, avatar presence, and streaming presence require low-latency local behavior.

ORION should handle local capture, sampling, filtering, avatar reaction, and voice playback. ATLAS provides reasoning, personality, commentary, memory, and safety policy.

### Full Automation Path

Full automation is not part of Genesis foundation work.

Examples:

- desktop automation
- game input control
- Blender automation
- OBS automation
- terminal command execution
- multi-step project execution
- plugin runtime actions

These belong to later Co-Pilot or Ecosystem phases and must be strongly permission-gated.

## ORION Client Agent

The ORION Client Agent is the main local process installed on ORION.

It should eventually provide:

- secure pairing with ATLAS
- local client identity
- health heartbeat
- local status reporting
- voice bridge
- screen bridge
- local action bridge
- avatar and 3D environment bridge
- OBS bridge
- Blender bridge
- VS Code/project bridge
- game companion bridge
- plugin runtime bridge
- local permission prompt
- local emergency stop
- audit event forwarding

The agent must be local-first, permission-first, visible, controllable, and revocable.

## Dashboard Access

ORION should access AURA Control Center from ATLAS through a local network dashboard.

Future dashboard usage from ORION:

- chat with AURA
- check AURA status
- check ATLAS status
- check ORION client status
- review permission requests
- review action queue
- inspect plugin status
- inspect voice/screen/avatar connection
- inspect Blender/VS Code/OBS/game bridge status
- inspect audit logs

In early Genesis stages, ORION may only need a browser and client pairing.

## Voice Bridge

ORION should provide the voice bridge because microphone and speaker devices are local to the user.

ORION handles:

- microphone capture
- push-to-talk state
- optional wake/listen mode in later phases
- local audio buffering
- speaker output
- voice playback
- TTS playback if generated locally
- lip sync signal extraction if needed
- listening/thinking/speaking UI feedback

ATLAS handles:

- conversation reasoning
- intent understanding
- response generation
- permission decisions
- memory and context updates

Default safe mode:

- push-to-talk first
- continuous listening later
- clear listening indicator required
- no hidden microphone capture

## Screen Capture and Short Recording

ORION should provide screen capture and short recording.

AURA should support multiple observation modes:

- single screenshot mode
- active window screenshot mode
- short recording mode
- low-FPS frame sampling mode
- event-triggered capture mode
- app/window-specific capture mode
- screen plus log analysis mode

AURA should not continuously stream full-resolution screen video to ATLAS by default.

Safe defaults:

- capture only when requested or session-approved
- prefer selected app/window over full monitor
- short recording duration should be limited
- low FPS for analysis
- downscale and compress before sending
- remove duplicate frames when possible
- send only relevant keyframes and metadata
- show capture indicator on ORION and dashboard

ORION pre-processes:

- selected window capture
- downscaling
- compression
- frame sampling
- keyframe extraction
- duplicate-frame removal
- optional OCR metadata
- active app/window metadata
- short ring buffer

ATLAS analyzes:

- visual context
- likely issue
- error location
- workflow meaning
- next-step recommendation
- action proposal if needed

## Screen Debugging Flow

Example user request:

Aura, coba cek layar sekarang.

If the issue is static, ORION may send one screenshot.

If the issue only appears while a program is running, ORION should use short recording or frame sampling.

Recommended flow:

1. User asks AURA to check the screen.
2. ORION asks for or confirms screen capture permission.
3. User selects screenshot, active window, or short recording.
4. ORION captures locally.
5. ORION extracts relevant frames or metadata.
6. ORION sends only relevant frames and metadata to ATLAS.
7. ATLAS analyzes the issue.
8. AURA explains the likely problem and suggests next steps.

For development debugging, screen analysis should be combined with logs when available.

## Local Action Bridge

ORION should execute local actions only after approval.

Examples of allowed early local actions:

- open folder
- open file
- open allowlisted software
- open AURA dashboard
- open project location
- create folder with confirmation
- create simple file with confirmation
- create template file with preview and confirmation

ORION must not execute unsafe actions by default.

Not allowed by default:

- delete files
- edit many files automatically
- run arbitrary commands
- control games
- control desktop freely
- control Blender automatically
- control OBS automatically
- install dependencies automatically
- execute plugin actions without runtime gating
- bypass permission workflow

Every action should include:

- source
- target
- action type
- risk level
- permission state
- planned change
- execution result
- audit metadata

## Software Allowlist

ORION should maintain an allowlist of software that AURA may open or interact with.

Example allowlist candidates:

- File Explorer
- VS Code
- Blender
- OBS
- browser
- terminal
- approved project tools

Opening software should still require permission unless a scoped session permission exists.

## Workspace Root Mapping

ORION should maintain approved workspace roots.

Example workspace roots:

- D:/Projects
- D:/AURA
- D:/Blender
- D:/Streaming
- D:/Assets

AURA actions should be limited to approved roots unless the user explicitly grants broader access.

Protected paths should be blocked by default.

Protected examples:

- Windows system folders
- Program Files
- browser profile directories
- password or secret folders
- personal/private folders without approval
- unrelated drives or folders

## Permission Model

AURA should support multiple permission scopes.

### One-Time Permission

Applies to one action only.

Example:

- open this folder once
- create this file once

### Session Permission

Applies for a temporary session.

Example:

- observe Blender window for 30 minutes
- allow game companion for this session
- allow reading this project folder for this coding session

### Scoped Permission

Applies only to a folder, app, plugin, or action class.

Example:

- allow creating files under D:/Projects/AURA
- allow opening Blender project files under D:/Blender
- allow OBS status reading only

### Mode Permission

Applies to a named mode.

Example:

- streaming companion mode
- gaming companion mode
- Blender assistant mode
- work mode

### Plugin Permission

Applies to one plugin.

Example:

- OBS Plugin
- Blender Plugin
- VS Code Project Plugin
- Game Companion Plugin
- Avatar Runtime Plugin

Permissions must be visible, revocable, and auditable.

## Emergency Stop

ORION must have a local emergency stop.

Emergency stop should:

- stop local action execution
- stop screen recording
- stop microphone capture
- stop avatar/plugin activity if needed
- notify ATLAS
- write audit event
- revoke active session permissions if configured

Emergency stop must work even if ATLAS is slow or unreachable.

## Avatar and 3D Environment Runtime

AURA's avatar and 3D environment should run on ORION, not ATLAS.

ATLAS handles:

- personality
- memory
- dialogue
- mood-like state
- expression intention
- speaking/listening/thinking state
- permission and safety state

ORION handles:

- avatar rendering
- 3D room/environment rendering
- camera/view
- animation state
- expression controller
- lip sync
- voice playback
- OBS or virtual camera output
- local visual effects
- fast visual feedback

AURA sends state and intention. ORION renders them.

Example state packet:

- state: thinking
- expression: curious
- mood: focused
- speaking: false
- avatar_motion: idle_focus

ORION should not interpret visual state as permission for real-world actions.

## Streaming Bridge

Streaming presence belongs to ORION.

ORION handles:

- OBS presence
- avatar source
- audio routing
- voice playback
- expression sync
- stream-safe visual mode
- optional OBS status bridge
- optional chat overlay bridge in later phases

Early streaming mode should allow:

- avatar appears in OBS
- AURA can speak
- AURA can react visually
- expression sync works
- streaming-safe personality mode

Deferred:

- automatic OBS control
- automatic scene switching
- automatic moderation
- automatic public chat reading without filtering
- streaming automation without permission

Advanced streaming automation belongs to Co-Pilot or Ecosystem.

## Game Companion

Game companion should use the same screen observation principles as screen analysis, but with stricter latency, performance, and privacy constraints.

Early/default game companion should use:

- selected game window capture
- manual screenshot
- low-FPS frame sampling
- event-triggered observations
- ORION-side downscaling and compression
- keyframe selection
- ATLAS-side reasoning and commentary
- ORION-side avatar reaction and voice playback

AURA should not analyze every game frame.

Game companion levels:

1. Passive Screenshot Comment
2. Periodic Low-FPS Companion Observation
3. Event-Triggered Observation
4. Game-Specific Telemetry or Plugin
5. Permission-Gated Game Input Control

Game input control is not the same as game companion.

Game input control must be delayed until later phases, must be game-specific, must be permission-gated, and must include emergency stop.

## Blender Bridge

Blender workflow should be split between ATLAS and ORION.

ATLAS handles:

- intent understanding
- planning
- texture/material strategy
- prompt generation
- workflow reasoning
- safety review
- permission request
- result evaluation

ORION handles:

- Blender local scene access
- selected object metadata
- material slot metadata
- UV map metadata
- Blender Python/addon execution
- texture file creation or import after approval
- applying materials/textures
- local preview
- GPU-heavy texture generation if local
- result capture and reporting

Example request:

Aura, buatkan texture untuk model ini.

Recommended flow:

1. ORION detects selected Blender object.
2. ORION sends object/material/UV metadata and optional preview to ATLAS.
3. AURA creates a texture/material plan.
4. AURA asks for approval if writing/applying files.
5. ORION performs approved Blender-local work.
6. ORION reports result.
7. AURA reviews and suggests next steps.

Heavy texture generation should run on ORION or an approved external/local tool, not ATLAS CPU-only.

## VS Code and Project Work Bridge

VS Code and coding workflows should execute on the machine that owns the project files.

If the project is on ATLAS:

- ATLAS can read the repo
- ATLAS can plan patch
- ATLAS can run approved local tests
- ATLAS can commit after permission

If the project is on ORION:

- AURA plans on ATLAS
- ORION Agent reads local project files after permission
- ORION Agent opens VS Code if approved
- ORION Agent applies approved patches
- ORION Agent runs tests if approved
- ORION Agent sends output/errors back to ATLAS

AURA is the architect, programmer, reviewer, and planner.

The agent is the local hand that touches files, editor, terminal, and test runner.

## Plugin Runtime Direction

In the Ecosystem phase, ORION should support local plugins.

Potential ORION plugins:

- ORION Screen Plugin
- ORION Voice Plugin
- ORION File Action Plugin
- ORION Blender Plugin
- ORION OBS Plugin
- ORION Avatar Plugin
- ORION Game Companion Plugin
- ORION Input Control Plugin
- ORION VS Code Project Plugin

Every plugin should have:

- manifest
- permission scope
- enable/disable toggle
- risk level
- config
- health status
- audit log
- allowed actions
- denied actions

Plugin execution should remain permission-gated and visible.

## Security and Pairing

ORION must pair securely with ATLAS.

Security requirements:

- trusted device pairing
- client token
- local network only by default
- firewall awareness
- trusted client list
- revocation support
- permission prompts
- emergency stop
- audit event forwarding
- no hidden remote control
- no unauthenticated client action
- no public exposure by default

ATLAS should be able to revoke ORION access.

ORION should be able to stop itself locally.

## Data Aggregator Implication

Sprint 93 Control Center Data Aggregator Foundation should account for ATLAS-ORION deployment.

The future Control Center should be able to display:

- ATLAS core status
- ORION client status
- pairing status
- voice bridge status
- screen bridge status
- avatar runtime status
- 3D environment status
- local action bridge status
- Blender bridge status
- VS Code/project bridge status
- OBS/streaming bridge status
- game companion status
- active permission scopes
- active session permissions
- emergency stop state
- recent client audit events

Sprint 93 should not activate runtime data fetching. It should only plan aggregator packets and data contracts.

## Phase Mapping

### Genesis Final / v1.0

ORION needs:

- dashboard access
- basic AURA Client Agent
- push-to-talk voice bridge
- speaker output
- screenshot or window capture
- short recording or frame sampling foundation
- basic local action bridge
- app/folder allowlist
- permission prompt
- emergency stop

### Genesis Stabilization / v1.x

ORION improves:

- reconnect behavior
- latency
- permission UX
- client health monitor
- action reliability
- log/audit viewer
- startup behavior
- safer local action handling

### Embodiment / v2.x

ORION adds:

- avatar runtime
- 3D environment runtime
- expression sync
- lip sync
- voice/avatar sync
- OBS/VTuber bridge
- streaming presence
- gaming companion

### Co-Pilot / v3.x

ORION adds:

- workspace manager
- file/folder builder
- VS Code/project bridge
- Blender bridge
- OBS/content pipeline bridge
- controlled command runner
- task/action queue execution with approval

### Ecosystem / v4.x

ORION adds:

- plugin runtime
- plugin installer
- plugin sandbox
- plugin settings UI
- plugin permissions
- plugin health monitor
- game/app-specific plugins

### Continuity / v5.x

ORION adds:

- long-term client profile
- device migration
- backup/restore settings
- multi-device continuity
- performance optimization
- client history and reliability tracking

## Hardware Direction

ATLAS current role should remain server/core.

ATLAS is suitable for:

- AURA core
- dashboard/backend
- permission manager
- memory/journal/log
- action planner
- API/control center backend
- plugin registry
- client coordination
- lightweight model usage

ATLAS should not be forced to handle all heavy workloads.

Heavy or visual workloads should prefer ORION:

- avatar rendering
- 3D environment
- OBS/streaming
- game companion capture
- Blender viewport and automation
- AI texture generation
- image/video generation
- real-time voice/audio devices
- screen capture and short recording

Recommended ATLAS upgrade priority:

1. larger SSD or NVMe storage
2. backup storage
3. more RAM if needed
4. GPU only if ATLAS will run heavy local AI models

## Final Principle

ATLAS and ORION are not competing AURA instances.

ATLAS is AURA's brain and authority.

ORION is AURA's local body, senses, voice, visual presence, and execution bridge.

AURA remains one AI Partner.

All local power must remain:

- permission-first
- local-first
- visible
- revocable
- auditable
- safe_idle by default
- controllable by Kiput
