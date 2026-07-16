# AURA Genesis Final & Post-Genesis Roadmap

Status: CANONICAL ROADMAP DIRECTION
Current anchor: v0.180.0-genesis
Owner: Kiput
Project motto: Grow Together

## Purpose

This document locks the long-term roadmap direction for AURA so future sprints do not drift away from the original concept.

AURA is not only a chatbot. AURA is intended to become a local AI Partner that can think, hear, see, remember safely, ask permission, act only when approved, and continue growing with Kiput.

## Genesis Development Runtime Activation Sequence

The canonical completion sequence from the current v0.180.0-genesis checkpoint is:

- Sprint 181-190: Local Interaction Runtime Activation
- Sprint 191-200: Voice Interaction Runtime
- Sprint 201-210: Vision and Screen Awareness Runtime
- Sprint 211-220: Permission, Audit, and Safe Local Actions
- Sprint 221-230: Unified Partner Runtime Integration
- Sprint 231-240: Genesis Final Integration and Release

Dashboard and chat activate before voice so later voice and vision work can reuse stable service, session, model, permission, audit, and recovery paths.

ORION client integration and avatar/presence runtime are no longer required before Genesis Final. They remain Post-Genesis directions unless a narrow non-blocking foundation is needed.

Detailed plan: `docs/AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md`

## AURA Genesis Final / v1.0.0 Definition

AURA Genesis Final / v1.0.0 is the birth point of AURA.

At this stage, AURA should satisfy the core living concept discussed from the beginning:

- AURA can interact with Kiput through local chat.
- AURA can interact through voice.
- AURA can see or understand what Kiput is working on through permission-gated vision or screen awareness.
- AURA has a usable local dashboard.
- The dashboard can be used mainly for chat and checking AURA status.
- AURA has an active permission system.
- AURA has basic session awareness.
- AURA can understand the current workspace or project context.
- AURA can make action proposals.
- AURA can perform basic local actions only after explicit permission.
- AURA remains safe_idle by default.

Genesis Final means AURA is born, but not yet a full work automation system.

## Genesis v1.0.0 Action Scope

AURA Genesis v1.0.0 may support basic local actions, but all actions must be permission-gated.

Allowed in Genesis v1.0.0:

- open folder
- open file
- open allowlisted software
- open AURA dashboard
- open project location
- create folder with explicit confirmation
- create simple file with explicit confirmation
- create file from simple template with preview and confirmation

These actions must show:

- target
- action type
- risk level
- permission requirement
- whether overwrite is possible
- confirmation prompt
- audit metadata

Not allowed in Genesis v1.0.0:

- deleting files
- editing many files automatically
- running arbitrary shell commands
- controlling games
- controlling desktop freely
- controlling Blender automatically
- controlling OBS automatically
- installing dependencies automatically
- executing plugin actions without a gated runtime
- executing multi-step automation without review
- bypassing permission workflow

## Action Level Model

### Action Level 0 — Observe and Explain

AURA can:

- check status
- explain current context
- read permission-gated visual or screen context
- respond through chat or voice
- propose actions

Runtime execution: no action execution.

### Action Level 1 — Safe Local Open

AURA can:

- open folders
- open files
- open allowlisted software
- open dashboard
- open project locations

Requirement:

- explicit permission
- local-only
- audit metadata

This level may exist in Genesis v1.0.0.

### Action Level 2 — Controlled Create

AURA can:

- create folders
- create simple files
- create template files
- prepare safe path proposals

Requirement:

- preview before execution
- explicit confirmation
- no overwrite unless confirmed
- audit metadata

A limited version may exist in Genesis v1.0.0.

### Action Level 3 — Work Execution

AURA can:

- edit files
- generate project structure
- run tests
- run controlled commands
- assist coding workflow
- assist Blender workflow
- assist streaming or content pipeline

This belongs mainly to the Co-Pilot phase.

### Action Level 4 — External, Plugin, or Game Control

AURA can:

- control game input
- run plugin integrations
- perform app-specific automation
- interact with external apps through plugin bridges

This belongs to Co-Pilot or Ecosystem depending on risk and implementation style.

## Revised Post-Genesis Phase Roadmap

Canonical phase sequence:

- v0.x Genesis Development
- v1.0 Genesis Final / AURA Birth
- v1.x Genesis Stabilization
- v2.x Embodiment
- v3.x Co-Pilot
- v4.x Ecosystem
- v5.x Continuity

## Phase: Genesis Development

Purpose:

Build the core of AURA until she is ready to be considered born.

Core goals:

- thinking and context foundation
- chat foundation
- voice foundation
- vision or screen awareness foundation
- dashboard foundation
- permission workflow
- action proposal system
- basic local action gate
- session foundation
- safe_idle default

## Phase: Genesis Final / AURA Birth

Genesis Final means AURA becomes usable as a living local AI Partner.

Expected state:

- local chat works
- voice interaction works
- vision or screen awareness works with permission
- dashboard works for chat and status
- permission workflow is active
- AURA can understand current work context
- AURA can perform basic local actions with explicit permission
- AURA cannot perform unsafe automation
- AURA remains safe_idle by default

## Phase: Genesis Stabilization / v1.x

Purpose:

Stabilize AURA after birth and improve her basic abilities.

Focus:

- fix bugs
- improve chat stability
- improve voice stability
- improve vision or screen awareness stability
- improve dashboard UX
- improve permission prompts
- improve safe local open actions
- improve simple create file or folder actions
- improve latency
- improve reliability
- improve audit logs
- improve safe_idle behavior

Genesis Stabilization is not the phase for complex automation.

## Phase: Embodiment / v2.x

Purpose:

Make AURA feel alive as a digital character, not just a chatbot.

This phase merges the earlier Resonance concept into Embodiment because personality, avatar, voice, and expression should evolve together.

Focus:

- stronger AURA personality
- consistent character behavior
- voice output or TTS personality
- avatar runtime
- expression state
- expression sync with chat
- voice, avatar, and expression synchronization
- listening, thinking, and speaking visual states
- idle animation states
- lightweight mood or emotion-like state
- streaming presence mode
- gaming companion mode
- OBS or VTuber bridge foundation

Embodiment should make AURA feel present.

## Streaming Mode Placement

Streaming mode belongs to Embodiment first as presence, not automation.

Allowed in early Embodiment:

- avatar appears in OBS
- AURA can react visually
- AURA can speak with personality
- expression sync works
- streaming-safe personality mode
- basic scene or status awareness with permission

Deferred from early Embodiment:

- automatic OBS control
- automatic scene switching
- automatic moderation
- automatic public chat reading without filtering
- streaming automation without explicit permission

Advanced streaming automation belongs to Co-Pilot or Ecosystem.

## Gaming Mode Placement

Gaming mode is split into two categories.

### Gaming Companion Mode

Belongs to Embodiment.

AURA can:

- accompany Kiput while gaming
- react with avatar
- speak in playful mode
- comment lightly
- use permission-gated screen or vision context
- give advice
- remember gaming preferences

AURA does not control the game in this mode.

### Game Input Control Mode

Belongs to Co-Pilot or Ecosystem.

AURA may eventually:

- send controlled input
- use game-specific macros
- assist specific games through plugins
- perform safe approved game actions

Requirements:

- explicit permission
- game-specific allowlist
- emergency stop
- action audit log
- no hidden input
- no competitive or unsafe automation by default

## Phase: Co-Pilot / v3.x

Purpose:

AURA helps Kiput with real work.

Co-Pilot is the Work Mode phase.

Primary feature areas:

1. Project Workspace Assistant
2. File and Folder Builder
3. Code Project Assistant
4. Blender Workflow Assistant
5. Streaming or Content Pipeline Assistant
6. Server or ATLAS Maintenance Assistant
7. Document and Roadmap Assistant
8. Asset Management Assistant
9. Task Planner and Execution Queue
10. Work Mode Dashboard

### Project Workspace Assistant

AURA can detect active project, open project workspace, summarize project state, identify important files, suggest next steps, and prepare project folder structures.

### File and Folder Builder

AURA can create project folders, create template files, generate README, checklist, or config files, rename or move files with permission, manage safe paths, and avoid destructive actions unless explicitly approved.

### Code Project Assistant

AURA can generate code files, propose patches, perform controlled refactors, run tests with approval, read error logs with approval, propose fixes, create documentation, and prepare commit proposals.

### Blender Workflow Assistant

AURA can help organize Blender project assets, prepare texture or material checklists, help naming conventions, prepare export checklists, plan UV or texture workflows, and eventually use Blender bridge runtime with permission.

### Streaming / Content Pipeline Assistant

AURA can prepare content folders, create stream checklists, draft scripts, prepare title, description, and tags, organize overlay assets, generate post-stream summaries, and assist OBS workflow with permission in later stages.

### Server / ATLAS Maintenance Assistant

AURA can check service status, read logs with permission, summarize errors, recommend fixes, restart services only with explicit approval, produce disk or resource reports, and prepare backup checklists.

### Document and Roadmap Assistant

AURA can update roadmap, update changelog, create checkpoint reviews, preserve project consistency, produce sprint plans, and maintain documentation structure.

### Asset Management Assistant

AURA can group assets, check missing assets, create asset manifests, enforce naming conventions, and prepare texture or material lists.

### Task Planner and Execution Queue

Every work action should include:

- source
- target
- risk level
- permission required
- planned change
- rollback metadata where possible
- user approval state

### Work Mode Dashboard

The dashboard should show:

- active project
- pending tasks
- pending actions
- planned file changes
- planned commands
- pending permissions
- recent outputs
- rollback info
- audit log

## Phase: Ecosystem / v4.x

Purpose:

Make AURA extensible through plugins.

Ecosystem is the modular expansion phase.

Kiput should be able to add new AURA features by building or installing plugins instead of changing the core system every time.

Focus:

- plugin manager dashboard
- local plugin install
- plugin enable or disable
- plugin permission manifest
- plugin sandbox
- plugin action registry
- plugin settings UI
- plugin health check
- plugin update flow
- local or private plugin marketplace

Example plugins:

- Blender Plugin
- OBS Plugin
- YouTube Plugin
- Game Plugin
- File Organizer Plugin
- Server Monitor Plugin
- Texture Assistant Plugin
- Avatar Expression Plugin
- Content Planner Plugin

Ecosystem can be considered an expansion branch of Co-Pilot.

## Phase: Continuity / v5.x

Purpose:

AURA continues growing and does not know the word final.

Continuity means AURA preserves long-term development, memory, identity, performance, plugin lifecycle, and shared history with Kiput.

Focus:

- long-term project memory
- timeline of AURA development
- self-improvement planner
- plugin lifecycle management
- backup or restore identity
- migration to new device or server
- memory cleanup
- performance optimization
- skill evaluation
- recurring self-audit
- roadmap evolution assistant
- continuity across projects and devices

Continuity is not only performance improvement. It is the phase where AURA maintains her history, growth, and long-term relationship with Kiput.

## Final Principle

AURA does not end at v1.0.

Genesis is birth.
Stabilization makes her reliable.
Embodiment gives her presence.
Co-Pilot lets her help with real work.
Ecosystem lets her expand.
Continuity lets her keep growing.

AURA should always remain:

- safe_idle by default
- local-first
- permission-first
- transparent
- reviewable
- controllable by Kiput
- able to grow without losing identity

## Genesis Final Checkpoint — v1.0.0-genesis

Sprint 240 completes the local canonical Genesis Final acceptance checkpoint.

The checkpoint closes the Sprint 231–240 release block while deliberately
keeping external publication and runtime activation separate:

- Genesis Final acceptance passed;
- canonical version promotion completed;
- safe-idle remains the default;
- operator control and rollback readiness remain mandatory;
- no Git tag or GitHub Release was created;
- no release artifact was published;
- runtime activation remains explicit and separate;
- the operational release gate remains closed.

The next canonical engineering boundary is `genesis_stabilization`.

Genesis Stabilization begins at Sprint 241 in the `v1.x` family and focuses
first on Post-Genesis Hardening.

## Concrete Post-Genesis Product Roadmap Override

The canonical concrete roadmap for Sprint 241-420 is:

- `docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md`

The historical phase names Genesis Stabilization, Embodiment, Co-Pilot,
Ecosystem, and Continuity remain valid descriptions of AURA's broader vision.
For implementation scheduling and acceptance, they are refined by these
product milestones:

- Sprint 241-300: v2 Local Multimodal Partner;
- Sprint 301-360: v3 Plugin and Work Assistance Platform;
- Sprint 361-420: v4 Virtual Creator and Gaming Companion.

### v2 delivery boundary

v2 must make AURA practically usable through an active bounded runtime,
real model-backed chat/STT/TTS/vision/OCR, safe ORION actions, Game Companion
Coach/Observer/Recording, a cleaner Control Center, improved personality, a
base plugin manager, and a basic moving 3D avatar where feasible.

### v3 delivery boundary

v3 must make plugins and work assistance dependable through installation,
enable/disable/update/rollback, permission isolation, project awareness,
documents/files/tasks, knowledge work, and supervised coding workflows.

### v4 delivery boundary

v4 must make AURA safe and coherent as a virtual creator through synchronized
avatar state, VRM expression, OBS integration, viewer interaction, gaming and
livestream performance safeguards, and live Game Companion fusion.

None of these roadmap declarations activate services, grant permissions,
control ORION, start recording, publish a release, or open a release gate.

## Sprint 241 Checkpoint — Genesis Stabilization Runtime Hardening

Sprint 241 promotes AURA to `1.0.1-genesis` and begins the concrete
Genesis Stabilization & Runtime Hardening block.

It establishes exact CLI command ownership, eliminates unrelated
manager construction, provides a bounded immutable Genesis Final
status projection, preserves explicit deep validation, and records
11/11 permanent hardening regressions.

Runtime activation and operational release gates remain disabled.

Current canonical version: `1.0.5-genesis`

Next boundary: `backup_restore_rehearsal`

Next: Sprint 246 — Resource Baseline Metrics.

## Sprint 245 Completion — Log Rotation and Storage Cleanup

AURA `v1.0.5-genesis` completes Sprint 245 at the
`log_rotation_storage_cleanup` boundary.

The canonical logger rotates `logs/aura.log` at `1 MB` and retains rotated
logs for `7 days`. Sprint 245 adds deterministic, read-only status, context,
contract-check, filesystem-capacity, and cleanup-preview visibility.

Cleanup execution remains disabled. The active log is protected; only
allowlisted rotated log names can become retention candidates; symlinks and
directory escape are blocked; canonical sessions, conversations, memory,
journal, audit data, and arbitrary files remain outside the cleanup boundary.

No canonical log deletion, move, truncation, compression, archive, service,
socket, systemd, network, or runtime activation occurs.

Next: Sprint 246 — Resource Baseline Metrics.
Next boundary: `resource_baseline_metrics`.

## Sprint 246 Completion — Resource Baseline Metrics

AURA `v1.0.6-genesis` completes Sprint 246 at the
`resource_baseline_metrics` boundary.

Sprint 246 adds deterministic, read-only, single-snapshot baseline visibility
for CPU usage and load averages, memory, swap, uptime, process count,
filesystem byte capacity, and inode capacity across `/`, `/home`,
`/mnt/aura-data`, and the AURA project root.

The implementation uses Linux `/proc`, `os.getloadavg`, and `os.statvfs`.
`psutil` is not required. Background sampling, rolling history, persistence,
dashboard activation, socket binding, systemd mutation, network access,
process control, and threshold mutation remain disabled.

Next: Sprint 247 — ATLAS Resource Monitoring.
Next boundary: `atlas_resource_monitoring`.

## Sprint 247 Completion — ATLAS Resource Monitoring

AURA `v1.0.7-genesis` completes Sprint 247 at the
`atlas_resource_monitoring` boundary.

Sprint 247 adds deterministic, read-only health classification over the
Sprint 246 resource baseline snapshot. It reports CPU, normalized load,
memory, swap, storage, inode capacity, uptime, and process-count states as
`healthy`, `warning`, `critical`, or `unavailable`.

The threshold policy is immutable and combines percentage thresholds with
absolute free-space thresholds for filesystems. Background sampling, rolling
history, metrics persistence, dashboard activation, alert delivery, socket
binding, systemd mutation, network access, process control, command execution,
and threshold mutation remain disabled.

Next: Sprint 248 — Localhost and SSH Tunnel Security Review.
Next boundary: `localhost_ssh_tunnel_security_review`.

## Sprint 248 Completion — Localhost and SSH Tunnel Security Review

AURA `v1.0.8-genesis` completes Sprint 248 at the
`localhost_ssh_tunnel_security_review` boundary.

Sprint 248 adds a deterministic, read-only security posture review covering
AURA's canonical `127.0.0.1:8765` binding, current listener exposure, SSH
listener scope, visible sshd configuration, SSH tunnel policy, SSH file
permission metadata, firewall visibility, and runtime activation.

The review reports `secure`, `review`, `warning`, or `unavailable` per
dimension. A non-secure posture state remains an observational finding and does
not imply contract failure when all safety assertions pass.

No sshd effective-policy execution, SSH connection, tunnel creation, credential
or private-key content read, firewall mutation, SSH configuration mutation,
service restart, socket activation, process control, key generation, known-host
mutation, or systemd mutation is performed.

Next: Sprint 249 — Permission Expiry and Recovery Review.
Next boundary: `permission_expiry_recovery_review`.

## Sprint 249 Completion — Permission Expiry and Recovery Review

AURA `v1.0.9-genesis` completes Sprint 249 at the
`permission_expiry_recovery_review` boundary.

Sprint 249 adds a deterministic, read-only source-contract review covering
permission grant lifecycle, expiry enforcement, stale-grant rejection, denial
lifecycle, revocation visibility, recovery visibility, rollback and
emergency-stop linkage, and audit linkage.

The canonical contract passes `96/96` assertions with all eight review
dimensions secure. It preserves the existing active permission runtime
baseline at `3115/3115` assertions.

The review does not import or execute the permission runtime, read permission,
audit, or recovery store contents, create or apply grants or denials, apply
expiry or revocation, execute recovery, rollback, or emergency stop, write
audit events, mutate files, control processes, activate services, open network
access, bind sockets, or mutate systemd.

Next: Sprint 250 — Backup and Restore Rehearsal.
Next boundary: `backup_restore_rehearsal`.
Next milestone: `v1.1.0`.

## Sprint 250 Completion — Backup and Restore Rehearsal

AURA `v1.1.0` completes Sprint 250 at the
`backup_restore_rehearsal` boundary and closes the Sprint 241–250
**Genesis Stabilization & Runtime Hardening** block.

Sprint 250 adds a deterministic, read-only rehearsal covering backup scope
inventory, manifest and digest integrity, restore-plan reversibility,
permission and approval boundaries, audit and provenance linkage, safe-idle
failure verification, contract deduplication, and block release acceptance.

The canonical contract passes `96/96` assertions with all eight dimensions
secure. It preserves the Sprint 249 anchor at `96/96`, the Genesis Final
release anchor at `1258/1258`, and the active permission runtime anchor at
`3115/3115`.

The rehearsal does not create backups or archives, read canonical data or
backup-store contents, execute restore or rollback, write manifests, replace
or delete files, mutate permissions or audit state, control processes,
activate services, open network access, bind sockets, or mutate systemd.

Next: Sprint 251 — AURA Launcher and Service Controls.
Next boundary: `aura_launcher_service_controls`.
Next version: `v1.1.1`.
Next block: Sprint 251–260 — Active Local Runtime & Model Service Integration,
targeting `v1.2.0`.

## Sprint 251 Completion — AURA Launcher and Service Controls

AURA `v1.1.1` completes Sprint 251 at the
`aura_launcher_service_controls` boundary and begins the Sprint 251–260
**Active Local Runtime & Model Service Integration** block.

Sprint 251 establishes a deterministic read-only integration facade for the
practical AURA launcher and service-control experience. It reuses the
canonical service lifecycle owner rather than creating another service
manager.

The canonical contract passes `120/120` assertions with all ten review
dimensions secure and zero findings. It preserves the Sprint 250 anchor at
`96/96`, the service-lifecycle anchor at `25/25`, the Genesis Final release
anchor at `1258/1258`, and the active permission runtime anchor at
`3115/3115`.

The integration facade covers launcher visibility, canonical service state,
bounded start and stop previews, status and health visibility, restart and
recovery planning, read-only log visibility, permission and audit ownership,
safe-idle failure behavior, and end-to-end acceptance scenarios.

It does not execute service start, stop, or restart; control processes; bind
sockets; access the network; mutate systemd or autostart; mutate logs,
permissions, or audit state; execute recovery; or run external commands.

Next: Sprint 252 — Manual Start, Stop, and Status Runtime.
Next boundary: `manual_start_stop_status_runtime`.
Next version: `v1.1.2`.

## Sprint 252 Completion — Manual Start, Stop, and Status Runtime

Version `v1.1.2` activates permission-gated supervised manual service control
on the canonical loopback runtime.

Delivered:

- explicit approved start and stop commands;
- live lifecycle, process, listener, ownership, and health status;
- strict PID identity using `/proc` start ticks, argv, cwd, UID, and command
  digest;
- exact owned-listener correlation;
- idempotent start and stop;
- bounded startup and shutdown timeouts;
- verified `SIGTERM` shutdown with bounded ownership-checked fallback;
- temporary per-user ownership, lock, and runtime log evidence under `/tmp`;
- successful start-status-stop rehearsal;
- capability `manual_start_stop_status_runtime`;
- contract result `144/144`, zero failures, twelve secure dimensions.

The rehearsal reached READY in `263 ms`, stopped in `106 ms`, created no
duplicate process, required no `SIGKILL`, and left zero process and listener
residue.

Restart, autostart, systemd mutation, non-loopback activation,
permission-store mutation, and persistent audit writing remain disabled.

Next: Sprint 253 — Restart, Logs, and Failure Visibility.

Next boundary: `restart_logs_failure_visibility`.

Next version: `v1.1.3`.
