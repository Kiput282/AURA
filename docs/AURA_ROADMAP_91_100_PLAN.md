# AURA Roadmap 91–100 Plan

Target block: v0.91.0-genesis through v0.100.0-genesis  
Status: PROPOSED AFTER SPRINT 90 CHECKPOINT

## Roadmap Principle

Sprint 91–100 should begin bridging blueprint systems toward controlled local runtime foundations without enabling unsafe automatic actions.

AURA must remain:

- local-first
- safe_idle-first
- permission-first
- reviewable
- capability-aware
- runtime-gated
- no automatic action execution

## Proposed Sprint 91–100 Plan

### Sprint 91 — Local Console Static Prototype Foundation

Purpose:

- prepare static Control Center prototype file structure
- define HTML/CSS/JS asset blueprint
- prepare static route mapping
- still no web server runtime
- still no port binding

Runtime execution: 0

### Sprint 92 — Local Console API Schema Foundation

Purpose:

- define local API response schemas
- map system status, capabilities, permissions, launcher, chat, plugins, roadmap
- no backend server yet
- no API runtime yet

Runtime execution: 0

### Sprint 93 — Control Center Data Aggregator Foundation

Purpose:

- aggregate metadata from Capability Registry, Permission Workflow, Runtime Service Foundation, Launcher Monitor, Chat Bridge, and Plugin Dashboard
- prepare single dashboard data packet
- no UI runtime yet
- no service control

Runtime execution: 0

### Sprint 94 — Permission Request Review Queue Foundation

Purpose:

- formalize permission request queue metadata
- define review states
- define approval/deny UI metadata
- no real permission grant/deny runtime yet

Runtime execution: 0

### Sprint 95 — Chat Session Persistence Planner

Purpose:

- plan safe chat session persistence
- define what may be saved
- define privacy/safety boundary
- no real session file/database write yet

Runtime execution: 0

### Sprint 96 — Safe Local Web Runtime Gate

Purpose:

- create explicit gate for future local web runtime activation
- define localhost-only runtime requirements
- define port binding approval requirements
- still no automatic runtime activation

Runtime execution: 0

### Sprint 97 — Controlled File Write Approval Draft

Purpose:

- prepare controlled file write approval flow
- connect Safe File Operation Planner to Permission Workflow
- no actual file write runtime unless explicitly approved in a later sprint

Runtime execution: 0

### Sprint 98 — Runtime Action Queue Review Layer

Purpose:

- prepare review queue for runtime action proposals
- show pending actions, source, risk, permission requirement, and execution disabled flag
- no runtime action execution yet

Runtime execution: 0

### Sprint 99 — Pre-Runtime Security Audit

Purpose:

- audit all runtime-gated systems
- verify no bypass exists
- verify capability/permission/control-center consistency
- verify safe_idle defaults

Runtime execution: 0

### Sprint 100 — Review & Stabilization 91–100

Purpose:

- checkpoint review for Sprint 91–100
- update changelog and roadmap
- decide whether any tightly gated runtime can begin after v0.100

Runtime execution: 0 unless explicitly reprioritized and approved before Sprint 100.

## Deferred Until After Sprint 100 Unless Reprioritized

- actual local web server runtime
- actual frontend/backend runtime
- actual websocket runtime
- actual chat runtime
- actual plugin runtime
- actual permission grant/deny runtime
- actual service start/stop/restart
- actual launcher start/stop/restart
- actual file write execution
- actual command/tool execution
- desktop control
- memory write runtime

## Sprint 91 Entry Requirement

Before Sprint 91 starts, Sprint 90 must confirm:

- working tree clean
- v0.90.0-genesis boot READY
- runtime execution features remain 0
- Capability Registry counts are stable
- roadmap 91–100 approved

## Sprint 90 Approval Notes

This roadmap is proposed after the 81–90 checkpoint.

Entry assumptions for Sprint 91:

- AURA boots as v0.90.0-genesis
- Capability Registry remains stable
- runtime execution features remain 0
- local UI/web/chat/plugin/runtime systems remain gated
- Sprint 91 starts with static prototype foundation only
- no server, port, websocket, plugin runtime, permission runtime, action runtime, file write runtime, command runtime, or tool runtime is enabled automatically


## Sprint 91 Update — AURA Local Console Static Prototype Foundation

Status: LOCAL CONSOLE STATIC PROTOTYPE FOUNDATION ONLINE
Target version: v0.91.0-genesis

Sprint 91 adds a planner-only AURA Local Console Static Prototype Foundation for static prototype structure planning, static page blueprint planning, static asset blueprint planning, panel layout blueprint planning, route-to-static-page mapping planning, data placeholder contract planning, theme token blueprint planning, accessibility blueprint planning, and static prototype safety policy.

Current Local Console static prototype summary:
- prototype plan types: 11
- static pages: 9
- asset groups: 6
- panel layouts: 9
- route static mappings: 9
- data placeholder contracts: 8
- theme tokens: 6
- accessibility notes: 6
- runtime-enabled pages: 0
- static files created: 0
- HTML files created: 0
- CSS files created: 0
- JS files created: 0
- routes created: 0
- web servers started: 0
- ports bound: 0
- browser windows opened: 0
- frontend apps started: 0
- backend services started: 0
- API services started: 0
- runtime execution features: 0

Core rule: AURA Local Console Static Prototype may prepare static blueprints, but must not run web runtime yet.
