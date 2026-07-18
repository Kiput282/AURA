# AURA v2 to v4 Product Roadmap

Status: CANONICAL POST-GENESIS PRODUCT ROADMAP

Current canonical anchor: `v1.2.0`

Current completed sprint: Sprint 260 — Active Local Runtime Integration and Stabilization

Next sprint: `261`

Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`

Owner: Kiput

Project motto: Grow Together

## Purpose

This document converts AURA's broad Post-Genesis vision into concrete product
milestones from Sprint 241 through Sprint 420.

The roadmap defines:

- what AURA must become by v2.0.0, v3.0.0, and v4.0.0;
- the sprint blocks used to reach each target;
- ATLAS and ORION responsibilities;
- model and dataset direction;
- plugin, work-assistance, avatar, gaming, and livestream boundaries;
- cost and safety policies;
- acceptance criteria for each major product version.

This is a planning document. It does not activate runtime, install software,
grant permissions, control ORION, start recording, create a Git tag, publish a
release, or open an operational release gate.

## Canonical roadmap policy

Earlier phase labels such as Embodiment, Co-Pilot, Ecosystem, and Continuity
remain historical descriptions of AURA's long-term concept.

For Sprint 241 onward, the concrete product milestones in this document are
canonical for:

- sprint scheduling;
- implementation sequence;
- block acceptance;
- version targets;
- product readiness;
- dependency ordering;
- safety gating.

## Versioning policy

Block endpoints use semantic product milestones.

Individual implementation sprints may use patch releases within the currently
active minor line. Exact per-sprint version promotion must be resolved during
that sprint's discovery and acceptance process.

Canonical block endpoints:

| Sprint | Version |
|---|---|
| 250 | `v1.1.0` |
| 260 | `v1.2.0` |
| 270 | `v1.3.0` |
| 280 | `v1.4.0` |
| 290 | `v1.5.0` |
| 300 | `v2.0.0` |
| 310 | `v2.1.0` |
| 320 | `v2.2.0` |
| 330 | `v2.3.0` |
| 340 | `v2.4.0` |
| 350 | `v2.5.0` |
| 360 | `v3.0.0` |
| 370 | `v3.1.0` |
| 380 | `v3.2.0` |
| 390 | `v3.3.0` |
| 400 | `v3.4.0` |
| 410 | `v3.5.0` |
| 420 | `v4.0.0` |

The current canonical version is `v1.1.3`, promoted by Sprint 253.

# Part I — Target v2.0.0

## Product definition

AURA v2.0.0 is the first fully usable local multimodal partner milestone.

At v2, AURA should provide:

- an active, stable, operator-controlled local runtime;
- real model-backed chat;
- usable STT and TTS;
- permission-gated vision and OCR;
- authenticated allowlisted actions to ORION;
- Game Companion Coach Mode;
- Game Companion Observer Mode;
- Game Companion data Recording Mode;
- an improved Control Center;
- ATLAS and ORION monitoring;
- better personality consistency;
- a base plugin manager;
- a basic moving 3D avatar in the dashboard where feasible.

Autonomous gameplay is not required for v2.

## Sprint 241-250 — Genesis Stabilization & Runtime Hardening

Target milestone: `v1.1.0`

Primary goals:

- long-running service stability;
- deterministic startup, shutdown, restart, and recovery;
- configuration integrity;
- session and memory persistence checks;
- log rotation and storage cleanup;
- CPU, RAM, storage, process, and latency baselines;
- ATLAS resource monitoring;
- security review for localhost and SSH-tunnel access;
- permission expiry and recovery tests;
- backup and restore rehearsal;
- reduction of avoidable contract duplication;
- safe-idle verification after failure.

This block does not broadly activate voice, vision, ORION control, or Game
Companion recording.

## Sprint 251-260 — Active Local Runtime & Model Service Integration

Target milestone: `v1.2.0`

Primary goals:

- practical AURA launcher and service controls;
- manual start, stop, status, restart, and logs;
- optional reviewed autostart;
- persistent local chat sessions;
- model service discovery and health checks;
- local model router;
- model loading/unloading policy;
- inference queue and timeout handling;
- dashboard runtime integration;
- recovery when a model service fails;
- explicit resource budgets.

ATLAS remains the trusted authority.

## Sprint 261-270 — Chat, STT, TTS, Vision & OCR Activation

Target milestone: `v1.3.0`

Primary goals:

- local language model used by chat;
- personality-consistent response generation;
- push-to-talk STT before always-listening research;
- voice-activity detection;
- interruptible TTS;
- listening, thinking, and speaking states;
- explicit screenshot or selected-window capture;
- dedicated OCR;
- selected-frame vision-language analysis;
- memory retrieval integrated with conversation;
- privacy redaction;
- no silent cloud fallback.

Each modality must be independently stoppable.

## Sprint 271-280 — ORION Safe Action Bridge

Target milestone: `v1.4.0`

Primary goals:

- native ORION-side AURA Agent;
- authenticated ATLAS-to-ORION communication;
- device identity and capability negotiation;
- named and allowlisted actions;
- action preview and approval;
- scoped permission and expiry;
- timeout and cancellation;
- audit response packets;
- watchdog and independent emergency stop;
- rollback or neutral recovery where possible;
- screenshot/window capture requests;
- allowlisted application launch;
- allowlisted file/folder operations;
- reviewed OBS actions;
- no arbitrary shell by default.

ORION must never become an unrestricted remote execution endpoint.

## Sprint 281-290 — Game Companion Coach, Observer & Recording

Target milestone: `v1.5.0`

Primary goals:

- supported-game detection;
- safe-idle prompt when a game is detected;
- operator-selectable modes:
  - Coach only;
  - Observer only;
  - Coach + Observer;
  - Coach + Observer + Recording;
- game-window capture;
- game audio capture;
- input telemetry;
- timestamps and synchronization;
- session metadata;
- dataset manifest generation;
- storage quotas and reserved free space;
- post-session analysis;
- coach feedback;
- no autonomous game control.

Public livestream output and private training-data recording must remain
separate pipelines.

## Sprint 291-300 — v2 Product Integration & Acceptance

Target milestone: `v2.0.0`

Primary goals:

- cleaner and more usable Control Center;
- persistent chat interface;
- model and modality status;
- voice controls;
- vision and OCR panels;
- permission and action queues;
- ATLAS and ORION resource monitoring;
- Game Companion session panel;
- dataset recording controls;
- base plugin manager;
- improved AURA personality;
- 3D avatar viewport where feasible;
- idle, listening, thinking, speaking, warning, and recording avatar states;
- integrated recovery and emergency stop;
- v2 acceptance rehearsal and stabilization.

## v2 acceptance criteria

v2 is complete only when:

- AURA can be used through the dashboard during normal daily sessions;
- runtime start, stop, restart, and recovery are reliable;
- chat uses a real model;
- STT, TTS, vision, and OCR are usable;
- modality permission and privacy rules are enforced;
- ORION actions are authenticated, allowlisted, audited, and stoppable;
- Coach, Observer, and Recording modes operate without autonomous control;
- dataset metadata and retention are reliable;
- the dashboard presents understandable state and failures;
- personality is consistent across chat, voice, and dashboard states;
- base plugin discovery, enable, disable, and health checks work;
- avatar failure does not block core chat or safety functions;
- restart and rollback tests pass.

# Part II — Target v3.0.0

## Product definition

AURA v3.0.0 is the Plugin and Work Assistance Platform milestone.

At v3, AURA should support controlled extensibility and practical assistance
for projects, documents, files, tasks, knowledge work, and supervised coding.

## Sprint 301-310 — Plugin Architecture & Lifecycle

Target milestone: `v2.1.0`

Primary goals:

- canonical plugin manifest;
- plugin identity and compatibility;
- discovery and registration;
- installation;
- enable and disable;
- update;
- uninstall;
- health checks;
- configuration schema;
- plugin logs;
- rollback;
- trusted and untrusted status.

## Sprint 311-320 — Plugin Permissions, Isolation & Dependencies

Target milestone: `v2.2.0`

Primary goals:

- per-plugin permissions;
- declared capabilities;
- dependency validation;
- checksum and signature support;
- resource budgets;
- process or container isolation where appropriate;
- failure isolation;
- plugin-specific storage;
- plugin-specific memory namespace;
- audit and revocation;
- safe dependency updates.

A failed plugin must not bring down AURA Core.

## Sprint 321-330 — Workspace & Project Assistance

Target milestone: `v2.3.0`

Primary goals:

- project detection;
- workspace context;
- project summaries;
- status and milestone tracking;
- repository awareness;
- task and issue context;
- safe project-file retrieval;
- source attribution;
- project-specific memory;
- operator-reviewed action plans.

## Sprint 331-340 — Documents, Files, Tasks & Knowledge Work

Target milestone: `v2.4.0`

Primary goals:

- document search and summarization;
- safe file creation and editing;
- structured notes;
- task planning;
- report generation;
- spreadsheet analysis;
- document conversion workflows;
- knowledge retrieval;
- provenance and citations;
- permission-scoped connectors.

## Sprint 341-350 — Supervised Coding Assistance & Workflow Automation

Target milestone: `v2.5.0`

Primary goals:

- repository discovery;
- code explanation;
- patch proposals;
- exact scope previews;
- trusted supervisor validation;
- operator approval;
- test execution;
- rollback;
- protected-file policy;
- workflow templates;
- no unrestricted self-modification.

## Sprint 351-360 — v3 Integration & Acceptance

Target milestone: `v3.0.0`

Primary goals:

- unified plugin dashboard;
- dependable plugin lifecycle;
- workspace and document integration;
- supervised coding workflows;
- plugin isolation tests;
- permission revocation tests;
- connector privacy tests;
- work-assistance performance review;
- v3 acceptance and stabilization.

## v3 acceptance criteria

v3 is complete only when:

- plugin lifecycle operations are safe and reversible;
- plugin permissions are visible and enforceable;
- plugin failure is isolated;
- workspace assistance works on real projects;
- document and task workflows are reviewable;
- coding assistance never bypasses approval;
- provenance is visible;
- connector access can be revoked;
- work assistance remains usable without cloud dependency.

# Part III — Target v4.0.0

## Product definition

AURA v4.0.0 is a synchronized virtual creator and safe gaming companion.

At v4, the avatar, voice, dashboard, OBS, viewer interaction, coaching,
observation, recording, and creator workflow should behave as one coherent
runtime.

## Sprint 361-370 — Avatar Runtime & State Synchronization

Target milestone: `v3.1.0`

Primary goals:

- avatar runtime service;
- VRM asset loading;
- dashboard avatar viewport;
- canonical avatar state machine;
- idle, listening, thinking, speaking, warning, coach, observer, recording,
  disconnected, and emergency-stop states;
- avatar failure isolation;
- state synchronization between ATLAS, ORION, dashboard, and creator runtime.

## Sprint 371-380 — Voice, Face, Body Expression & VRM Integration

Target milestone: `v3.2.0`

Primary goals:

- lip sync;
- phoneme or viseme timing;
- blinking;
- eye gaze;
- head motion;
- expression tags;
- body idle animation;
- gesture selection;
- emotion constraints;
- interruption and reset;
- no direct unconstrained LLM bone control.

## Sprint 381-390 — OBS Creator Runtime & Viewer Interaction

Target milestone: `v3.3.0`

Primary goals:

- authenticated OBS integration;
- scene and source awareness;
- curated scene actions;
- stream status;
- viewer request queue;
- challenge queue;
- moderated interaction;
- content metadata assistance;
- public/private data separation;
- no accidental private-window capture.

## Sprint 391-400 — Gaming/Livestream Safety & Performance

Target milestone: `v3.4.0`

Primary goals:

- GPU, CPU, RAM, storage, encoder, and latency monitoring;
- resource budgets;
- graceful model degradation;
- safe fallback when game FPS drops;
- OBS and avatar recovery;
- recording quota enforcement;
- privacy redaction;
- audio routing verification;
- independent emergency stop;
- session recovery;
- livestream rehearsal.

## Sprint 401-410 — Game Companion Live Fusion & Creator Rehearsal

Target milestone: `v3.5.0`

Primary goals:

- synchronized Coach and Observer output;
- avatar reactions to game events;
- TTS and avatar timing;
- viewer challenge integration;
- clean public scene;
- separate dataset capture;
- creator-mode state machine;
- rhythm-performer workflow;
- repeated offline and private rehearsal;
- post-session analysis.

## Sprint 411-420 — v4 Stabilization & Acceptance

Target milestone: `v4.0.0`

Primary goals:

- long-running creator sessions;
- recovery under model or network-component failure;
- safe livestream rehearsals;
- avatar and voice synchronization review;
- gaming performance review;
- data-retention review;
- emergency-stop drills;
- privacy and permission audit;
- creator workflow documentation;
- v4 acceptance and stabilization.

## v4 acceptance criteria

v4 is complete only when:

- avatar state matches AURA runtime state;
- TTS, expression, and animation remain synchronized;
- OBS actions are allowlisted and auditable;
- viewer commands are curated;
- gaming performance remains within accepted limits;
- public output excludes private dataset and desktop content;
- Coach, Observer, and Recording work during creator sessions;
- emergency stop is independent and tested;
- no autonomous game control is required for acceptance.

# Part IV — Deployment responsibilities

## ATLAS responsibilities

ATLAS remains the trusted brain and control authority.

Planned responsibilities:

- AURA Core;
- Control Center backend;
- permission and audit authority;
- memory and relationship state;
- model router;
- stable checkpoint registry;
- dataset manifests and provenance;
- annotation and evaluation records;
- plugin trust and permission policy;
- backup and rollback;
- ORION command authorization;
- resource and service monitoring.

Likely installation families:

- Python environment and build tools;
- Git;
- FFmpeg;
- SQLite and migration tooling;
- Node.js and pnpm for dashboard builds;
- systemd service definitions;
- structured logging;
- backup tooling;
- CPU fallback model runtime;
- optional container isolation.

Exact software and versions must be selected in the relevant sprint.

## ORION responsibilities

ORION remains the interactive Windows workstation and GPU host.

Planned responsibilities:

- game and desktop capture;
- audio capture and playback;
- input telemetry;
- OBS;
- avatar rendering;
- game detection;
- local model inference requiring GPU;
- dataset workspace;
- training and evaluation workloads;
- allowlisted Windows actions;
- emergency-stop endpoint.

Likely installation families:

- stable NVIDIA driver;
- Python environment;
- Visual Studio Build Tools;
- Git;
- CMake and Ninja;
- FFmpeg;
- OBS Studio;
- Blender and VRM tools;
- AURA ORION Agent;
- capture and telemetry components;
- local model runtimes;
- optional WSL2 environment for training.

No installer is approved merely by appearing in this roadmap.

# Part V — Model architecture

## Multi-model principle

AURA is not planned as one giant model.

AURA Core should orchestrate specialized models with explicit responsibilities.

## Core language model

Responsibilities:

- conversation;
- reasoning summaries;
- planning;
- tool proposals;
- response generation;
- personality expression.

Use an existing pretrained model first. Do not train a foundation model from
zero.

## Personality layer

Responsibilities:

- canonical identity;
- speaking style;
- relationship continuity;
- expression tags;
- response critique;
- consistency evaluation.

Personality fine-tuning should use reviewed conversations and small adapters
only after sufficient clean data exists.

## Embedding and retrieval model

Responsibilities:

- memory search;
- project context;
- document retrieval;
- plugin knowledge;
- prior-session retrieval.

## STT

Responsibilities:

- live utterance transcription;
- language-mixed Indonesian and English support;
- game and project vocabulary;
- optional post-utterance correction.

Push-to-talk is the initial activation target.

## TTS

Responsibilities:

- local speech synthesis;
- interruption;
- speaking-state events;
- future viseme timing;
- future expression styles.

Voice assets must have valid usage rights.

## Vision-language model

Responsibilities:

- selected screenshot understanding;
- selected gameplay-frame interpretation;
- visual context summaries;
- coach reasoning support.

It must not process every captured frame with a large model.

## OCR

Responsibilities:

- application text;
- menus;
- subtitles;
- HUD text;
- error messages;
- document screenshots.

OCR remains separate from general visual reasoning.

## Game perception models

Potential responsibilities:

- HUD detection;
- state classification;
- event detection;
- timing analysis;
- input and outcome alignment;
- audio cue detection;
- post-session metrics.

Per-game models should be small and specialized.

## Future action-policy model

A future bounded game policy may use imitation learning, behavior cloning, or
offline reinforcement learning.

It is not required for v2, v3, or v4 acceptance and must never bypass
watchdog, permission, offline/single-player policy, or emergency stop.

# Part VI — Dataset and training policy

## Dataset separation

Public livestream and private training data are separate outputs.

ORION stores:

- raw capture;
- processed frames;
- clips;
- input telemetry;
- audio;
- temporary training workspace.

ATLAS stores:

- manifests;
- annotations;
- evaluation;
- provenance;
- approved subsets;
- stable model registry;
- rollback checkpoints.

## Initial recording standard

The planned standard remains `1920x1080` for dataset recording unless a game
requires a lower resource profile.

Recording policy must include:

- quotas;
- reserved free space;
- retention windows;
- temporary raw-data cleanup;
- event-based clips;
- selective transfer;
- session metadata;
- consent and privacy checks.

## Training policy

Training order:

1. collect;
2. validate synchronization;
3. annotate;
4. curate;
5. split train/evaluation data;
6. train small adapters or specialized models;
7. evaluate;
8. approve;
9. register;
10. preserve rollback.

Training heavy models during a public livestream is not a product requirement.

# Part VII — Cost policy

## Mandatory subscription policy

AURA should not require a mandatory cloud or software subscription.

Local-first open-source components remain the default.

## Expected operational costs

Expected costs may include:

- electricity;
- SSD or HDD storage;
- backup media;
- UPS protection;
- hardware replacement;
- microphone or audio equipment;
- legally licensed avatar or animation assets.

## Optional costs

Optional costs may include:

- cloud model APIs;
- rented GPU time;
- encrypted cloud backup;
- domain registration;
- commissioned avatar work;
- paid animation or creator assets;
- code-signing certificates for public distribution;
- external data annotation.

Any paid service requires explicit budget approval, quota, and disable control.

# Part VIII — Permanent safety invariants

The v2-v4 roadmap must preserve:

- local-first behavior;
- explicit operator control;
- safe-idle default and recovery state;
- permission before sensitive access;
- audit before and after controlled actions;
- grant expiry and revocation;
- independent emergency stop;
- rollback readiness;
- authenticated ATLAS-to-ORION communication;
- no arbitrary ORION shell by default;
- no silent microphone, screen capture, recording, or cloud upload;
- no autonomous multiplayer or public-game automation;
- no hidden self-modification;
- no plugin permission escalation without review;
- no automatic release publication;
- no release gate opening merely because a version number is reached.

# Immediate handoff

Current canonical state: `v1.1.1`

Current completed sprint: `245`

Next sprint: `246`

Next boundary: `resource_baseline_metrics`

Sprint 241 completed CLI dispatch and finalized-release status hardening. Sprint 242 continues the block with Service Lifecycle Determinism.

The next implementation must start with discovery and may not activate broad
runtime behavior merely because this roadmap has been approved.

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

## Sprint 253 Completion — Restart, Logs, and Failure Visibility

Version `v1.1.3` adds permission-gated supervised restart,
bounded allowlisted log visibility, and structured failure reporting on top
of the canonical manual start/stop owner.

Delivered:

- explicit restart command requiring both `--approve-restart` and
  `--confirm-localhost`;
- restart from `STOPPED` through a fresh canonical start;
- restart from `RUNNING` through verified owned-process stop, safe-idle
  confirmation, a bounded restart gap, and a fresh canonical start;
- post-restart ownership, loopback listener, process identity, and health
  verification;
- PID rotation verification across a running restart;
- bounded log tail with a maximum of 200 lines and 65,536 bytes;
- allowlisted active, latest-rotated, and temporary runtime log sources;
- symlink rejection, arbitrary-path rejection, and credential redaction;
- normalized failure packets covering ownership, stop, launch, health,
  cleanup, and log-preflight stages;
- contract result `168/168`, zero failures, fourteen secure dimensions;
- capability `restart_logs_failure_visibility`.

The supervised runtime rehearsal completed two successful restarts, verified
a new PID after the running restart, preserved canonical data, kept canonical
logs append-only, and returned AURA to `STOPPED` with zero listener and
process residue.

Systemd mutation, autostart mutation, non-loopback binding, arbitrary PID
signaling, arbitrary log paths, permission-store mutation, persistent audit
writing, and canonical-log mutation remain disabled.

Next: Sprint 254 — Process Ownership and Service State Persistence.

Next boundary: `process_ownership_service_state_persistence`.

Next version: `v1.1.4`.


## Sprint 254 Completion — Process Ownership and Service State Persistence

AURA `v1.1.4` completes Sprint 254 at the
`process_ownership_service_state_persistence` boundary.

Delivered:

- canonical state at `data/runtime/service_state.json`;
- schema v2 with PID, process start ticks, Linux boot ID, UID, command, cwd,
  loopback endpoint, and timestamps;
- mode `0600` file and `0700` parent directory;
- `O_EXCL`, `O_CLOEXEC`, `O_NOFOLLOW`, `fstat`, file fsync, atomic replace,
  and directory fsync;
- stale, previous-boot, and foreign-user record classification;
- explicit recovery only through approved start, stop, or restart;
- read-only status and recovery preview;
- contract `192/192`, zero failures, sixteen secure dimensions.

Systemd, autostart, arbitrary PID signaling, non-loopback binding, automatic
stale cleanup, permission-store mutation, persistent audit writing, and
background recovery remain disabled.

Next: Sprint 255 — Reviewed Optional Autostart.
Next boundary: `reviewed_optional_autostart`.
Next version: `v1.1.5`.


## Sprint 255 Completion — Reviewed Optional Autostart

AURA `v1.1.5` completes Sprint 255 at the
`reviewed_optional_autostart` boundary.

Delivered:

- exact `aura-local.service` user-unit preview;
- canonical `ExecStart` derived from the supervised runtime owner;
- project working directory and loopback runtime handoff;
- bounded `Restart=on-failure` policy;
- read-only user-manager, unit, and linger posture;
- explicit activation preview with confirmation token;
- complete rollback preview;
- contract result `216/216`, zero failures, eighteen secure dimensions.

No unit was written. No daemon reload, enable, start, linger change, system-unit
mutation, non-loopback binding, or automatic activation was performed.

Next: Sprint 256 — Persistent Local Chat Session Activation.
Next boundary: `persistent_local_chat_session_activation`.
Next version: `v1.1.6`.


## Sprint 256 Completion — Persistent Local Chat Session Activation

AURA `v1.1.6` completes Sprint 256 at the
`persistent_local_chat_session_activation` boundary.

Delivered:

- the existing browser-chat session manager remains the canonical owner;
- descriptor-safe session reads using directory-relative `open`, `O_NOFOLLOW`,
  `fstat`, UID checks, private-mode checks, and bounded reads;
- cross-process shared/exclusive locking on the storage-directory descriptor;
- secure write preparation with directory mode `0700`;
- session files mode `0600`;
- exclusive temporary creation, file fsync, atomic replace, and directory fsync;
- existing schema `1.0`, integrity hashes, revisions, and idempotent message
  submission remain compatible;
- bounded metadata-only history and exact session loading;
- isolated create, submit, cross-instance load/list, integrity, and symlink
  rejection rehearsal;
- contract result `240/240`, zero failures, twenty secure dimensions.

The existing canonical session content is not rewritten by implementation.
Directory-mode migration from `0775` to `0700` remains a separately validated
finalization step. Model-service activation, network access, non-loopback
binding, automatic memory handoff, session-content logging, systemd mutation,
and autostart activation remain disabled.

Next: Sprint 257 — Local Model Service Discovery and Health.
Next boundary: `local_model_service_discovery_health`.
Next version: `v1.1.7`.


## Sprint 257 Completion — Local Model Service Discovery and Health

AURA `v1.1.7` completes Sprint 257 at the
`local_model_service_discovery_health` boundary.

Delivered:

- the Sprint 187 local model bridge remains the canonical provider owner;
- read-only Ollama binary, systemd unit, process, and listener discovery;
- loopback-only endpoint and resolved-address enforcement;
- environment profile posture without credential reads or persistence;
- provider contract visibility for Ollama and OpenAI-compatible local servers;
- default endpoint `http://127.0.0.1:11434`;
- default-off health probing with a two-second timeout and exact confirmation
  token `PROBE_LOCAL_MODEL_SERVICE`;
- count-only model inventory from the health response;
- healthy, degraded/unprobed, and unavailable classification;
- isolated fake-transport rehearsal with no canonical network access;
- contract result `264/264`, zero failures, twenty-two secure dimensions.

The implementation does not start, stop, or install Ollama; download, pull,
load, or unload models; route chat; contact non-loopback endpoints; read
credentials; mutate systemd or autostart; or run a health probe automatically.

Next: Sprint 258 — Local Model Router Activation.
Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`.
Next version: `v1.1.8`.


## Sprint 258 Completion — Local Model Router Activation

AURA `v1.1.8` completes Sprint 258 at the
`local_model_router_activation` boundary.

Delivered:

- the existing `ModelRouter` remains the canonical route owner;
- the Sprint 187 local model bridge remains the execution owner;
- the Sprint 257 health boundary remains the provider-health dependency;
- existing configured route metadata is reused without a new route registry;
- exact-route preview with alias normalization;
- unknown-route fallback remains visible but cannot execute;
- only online routes matching the validated provider and model may execute;
- validated reasoning profile from `aura/config/settings.yaml`;
- explicit provider-health verification before handoff;
- exact model-request confirmation token `ROUTE_LOCAL_MODEL_REQUEST`;
- bounded routed-message validation;
- isolated fake-transport bridge handoff rehearsal;
- contract result `288/288`, zero failures, twenty-four secure dimensions.

No route decision is persisted. Real runtime switching, service control, model
download/pull/load/unload, queue activation, resource-budget mutation,
non-loopback networking, credential reads, systemd mutation, and autostart
mutation remain disabled. Live inference is disabled by default and is reserved
for one explicitly approved finalization rehearsal.

Next: Sprint 259 — Model Loading, Unloading, Queue, and Resource Budgets.
Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`.
Next version: `v1.1.9`.


## Sprint 259 Completion — Model Loading, Unloading, Queue, and Resource Budgets

AURA `v1.1.9` completes Sprint 259 at the
`model_loading_unloading_queue_resource_budgets` boundary.

Delivered: explicit provider lifecycle contracts, `keep_alive` loading,
explicit release, metadata-only residency status, a bounded in-memory queue
(depth 4, one in-flight item, 120-second timeout), and read-only memory, swap,
load, and optional GPU budget gates. The contract passes `312/312` assertions
across twenty-six secure dimensions.

Automatic load/release, model download/pull, queue persistence, background
workers, threshold mutation, service control, non-loopback networking,
credentials, systemd mutation, and autostart mutation remain disabled.

Next: Sprint 260 — Active Local Runtime Integration and Stabilization.
Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`.
Next version: `v1.2.0`.


## Sprint 260 Completion - Active Local Runtime Integration and Stabilization

AURA `v1.2.0` completes Sprint 260 and closes the Sprint 251-260 Active Local Runtime and Model Service Integration block.

The coordinator combines manual service control, safe idle, private persistent chat, explicit Ollama health, exact `companion` routing, explicit model lifecycle, bounded in-memory queueing, read-only resource budgets, persistence only after a successful bounded response, and mandatory stop-and-restore behavior.

Contract target: `336/336` across twenty-eight secure dimensions. Sprint 261 requires roadmap reconfirmation after `v1.2.0`.

Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`.

## Canonical Checkpoint after v1.2.0

Current canonical anchor: `v1.2.1`

Current completed sprint: Sprint 261 — Roadmap Reconfirmation after v1.2.0

Next sprint: `262`

Next boundary: `operational_browser_chat_model_handoff`

The Sprint 261–270 daily product block targets `v1.3.0` and requires live
end-to-end acceptance at Sprint 270 before the next block begins.

## Canonical Checkpoint at v1.2.2

Current completed sprint: Sprint 262 — Operational Browser Chat Model Handoff.

Current version: `v1.2.2`

Next sprint: Sprint 263

Next boundary: `session_list_resume_rename_archive_restore`

Sprint 262 finalization requires one live model handoff rehearsal followed by
safe-idle restoration.

## Daily product checkpoint — Sprint 267 / v1.2.7

The v1.2 product line now includes a read-only ATLAS Resource
Monitoring Dashboard in the existing Control Center. It covers current
system metrics, storage health for the canonical mount points, and
in-process CPU/RAM rolling history while preserving the safe-idle,
localhost-oriented operating boundary.

Next implementation boundary: `permission_audit_action_visibility_ux`.

## Daily product checkpoint — Sprint 268 / v1.2.8

The v1.2 product line now includes a consolidated Permission Audit
Action Visibility UX in the existing Control Center. It surfaces the
full review chain while preserving manual approval, read-only
operation, and the safe-idle execution boundary.

Next implementation boundary: `daily_use_acceptance_rehearsal_and_release_harness`.
