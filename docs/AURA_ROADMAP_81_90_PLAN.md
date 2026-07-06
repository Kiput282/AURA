# AURA Roadmap Plan — Sprint 81-90

Status: PLANNED  
Starting version: v0.81.0-genesis  
Direction: operational control before major runtime action

## Roadmap Decision

After Sprint 80, AURA will prioritize operational control foundations before enabling major runtime actions.

The core direction remains:

Think → Hear → See → Act Safely → Grow Together

The revised Sprint 81-90 block adds service, launcher, monitor, and Control Center foundations before controlled file, command, voice, or vision runtime execution.

## Planned Sprint 81-90 Sequence

| Sprint | Focus |
|---|---|
| 81 | Shared Output Formatter Foundation |
| 82 | Capability Registry Consolidation |
| 83 | Unified Permission Workflow Manager |
| 84 | AURA Runtime Service Foundation |
| 85 | AURA Launcher & Health Monitor Foundation |
| 86 | AURA Control Center UI Blueprint |
| 87 | Local Console Web Foundation |
| 88 | Chat Bridge & Session State Foundation |
| 89 | Plugin/Permission Dashboard Foundation |
| 90 | Review & Stabilization 81-90 |

## Deferred to Sprint 91-100 Unless Reprioritized

The following should be deferred until AURA has stronger operational control:

- controlled file write approval runtime
- command execution approval runtime
- voice runtime adapter
- vision runtime adapter
- advanced runtime safety monitor
- larger runtime action execution layer

## AURA Control Center Direction

AURA Control Center is now an official future AURA feature, starting as a local tester/developer console.

Planned areas:

- Genesis Dashboard
- Chat Console
- Avatar / Presence Panel
- Plugin Manager
- Permission Center
- Action Log
- Service Monitor
- Launcher Control
- Roadmap / Capability Viewer

Initial mode:

- local-only
- ATLAS-hosted
- safe_idle by default
- permission-first
- no automatic action execution

## Auto-Boot Direction

AURA should eventually be able to start automatically when the ATLAS server boots.

The default boot behavior must be safe:

- start AURA service
- enter safe_idle mode
- load identity/status/capabilities
- expose status and local console readiness
- execute no command automatically
- write no files automatically
- download/install nothing automatically
- keep microphone/camera/screen/network/desktop/git locked until explicitly approved

## Design Principle

AURA may wake automatically, but AURA must not act automatically.


## Sprint 82 Update — Capability Registry Consolidation

Status: CAPABILITY REGISTRY ONLINE  
Target version: v0.82.0-genesis

Sprint 82 adds a central planner-only Capability Registry for AURA. The registry tracks online, foundation-only, planner-only, permission-gated, review-only, planned-future, and disabled-runtime capabilities.

Current registry summary:
- total capabilities tracked: 18
- online capabilities: 12
- foundation-only capabilities: 3
- planner-only capabilities: 6
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 4
- disabled runtime capabilities: 2
- runtime execution features: 0

The registry prepares metadata for the future AURA Control Center, service monitor, launcher, plugin dashboard, and permission dashboard.

The registry does not grant permissions, enable runtime actions, start UI/web/chat/service/launcher runtime, perform file operations, execute commands, install dependencies, download packages, use internet/network actions, execute tools, write memory, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 83 Update — Unified Permission Workflow Manager

Status: UNIFIED PERMISSION WORKFLOW ONLINE  
Target version: v0.83.0-genesis

Sprint 83 adds a planner-only Unified Permission Workflow Manager. It prepares permission request planning, approval/deny state transition planning, risk review planning, confirmation prompt planning, permission audit trail planning, future Control Center Permission Center view planning, and permission policy gap review.

Current workflow summary:
- permission templates: 12
- permission categories: 13
- permission request states: 7
- approval modes: 5
- risk levels: 4
- explicit confirmation required templates: 11
- runtime-enabled templates: 0
- always-approve templates: 0
- runtime execution features: 0

This sprint does not grant permission, approve actions automatically, enable always-approve mode, activate runtime actions, start UI/web/chat/service/launcher runtime, perform file operations, execute commands, install dependencies, download packages, use internet/network actions, execute tools, write memory, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 84 Update — AURA Runtime Service Foundation

Status: RUNTIME SERVICE FOUNDATION ONLINE  
Target version: v0.84.0-genesis

Sprint 84 adds a planner-only AURA Runtime Service Foundation for ATLAS safe_idle boot planning, service lifecycle planning, health check planning, systemd unit blueprint planning, service recovery planning, service monitor view planning, and auto-boot policy planning.

Current service foundation summary:
- service plan types: 9
- boot modes: 4
- lifecycle states: 9
- health check fields: 11
- runtime-enabled services: 0
- systemd units created: 0
- background processes started: 0
- auto-boot runtime enabled: 0
- runtime execution features: 0

Core rule: AURA may wake automatically in the future, but only in safe_idle and never as auto-action.
