# AURA v2 to v4 Product Roadmap

Status: CANONICAL POST-GENESIS PRODUCT ROADMAP

Current canonical anchor: `v1.0.0-genesis`

Current completed sprint: `240`

Next sprint: `241`

Next boundary: `genesis_stabilization`

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

The current canonical version remains `v1.0.0-genesis` until an implementation
sprint explicitly promotes it.

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

Current canonical state: `v1.0.0-genesis`

Current completed sprint: `240`

Next sprint: `241`

Next boundary: `genesis_stabilization`

Sprint 241 begins the Genesis Stabilization & Runtime Hardening block.

The next implementation must start with discovery and may not activate broad
runtime behavior merely because this roadmap has been approved.
