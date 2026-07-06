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
