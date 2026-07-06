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


## Sprint 85 Update — AURA Launcher & Health Monitor Foundation

Status: LAUNCHER HEALTH MONITOR FOUNDATION ONLINE  
Target version: v0.85.0-genesis

Sprint 85 adds a planner-only AURA Launcher & Health Monitor Foundation for safe_idle launch planning, start/stop/restart/status/logs planning, health monitor planning, Control Center service monitor planning, and launcher safety policy planning.

Current launcher monitor summary:
- launcher plan types: 10
- launcher modes: 4
- launcher actions: 6
- health states: 5
- monitor fields: 12
- runtime-enabled launchers: 0
- processes started: 0
- processes stopped: 0
- processes restarted: 0
- systemctl commands executed: 0
- log files read: 0
- runtime execution features: 0

Core rule: AURA may prepare launcher and monitor visibility, but must not control runtime yet.


## Sprint 86 Update — AURA Control Center UI Blueprint

Status: CONTROL CENTER UI BLUEPRINT ONLINE  
Target version: v0.86.0-genesis

Sprint 86 adds a planner-only AURA Control Center / Genesis Console UI Blueprint for dashboard layout, Permission Center, Service Monitor, Capability Viewer, Launcher Control, Chat Console placeholder, Plugin Dashboard, Action Log, Roadmap Viewer direction, and Control Center safety policy.

Current Control Center blueprint summary:
- blueprint plan types: 11
- UI panels: 9
- navigation items: 9
- Permission Center cards: 9
- Service Monitor cards: 10
- Launcher Control cards: 6
- Capability Viewer cards: 7
- runtime-enabled panels: 0
- frontend apps created: 0
- backend services created: 0
- web routes created: 0
- ports bound: 0
- browser windows opened: 0
- runtime execution features: 0

Core rule: AURA Control Center may show visibility, but must not control runtime yet.


## Sprint 87 Update — AURA Local Console Web Foundation

Status: LOCAL CONSOLE WEB FOUNDATION ONLINE  
Target version: v0.87.0-genesis

Sprint 87 adds a planner-only AURA Local Console Web Foundation for localhost-only policy planning, route blueprint planning, API contract blueprint planning, static asset blueprint planning, session state blueprint planning, security boundary planning, Control Center web bridge planning, and developer console access planning.

Current local console web summary:
- web foundation plan types: 10
- local host policies: 6
- route blueprints: 9
- API contracts: 8
- static asset groups: 6
- session state fields: 7
- runtime-enabled routes: 0
- runtime-enabled APIs: 0
- web servers started: 0
- ports bound: 0
- frontend apps created: 0
- backend services created: 0
- routes created: 0
- static files served: 0
- sessions started: 0
- browser windows opened: 0
- runtime execution features: 0

Core rule: AURA Local Console may prepare local visibility, but must not run web runtime yet.
