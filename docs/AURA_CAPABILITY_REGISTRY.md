# AURA Capability Registry Consolidation

Target version: v0.82.0-genesis
Status: CAPABILITY REGISTRY ONLINE

## Purpose

The Capability Registry provides a central planner-only metadata layer for describing what AURA can do, what is only a foundation, what is planner-only, what requires permission, what is review-only, what is planned, and what is currently disabled as runtime action.

This registry prepares capability data for:

- CLI
- shell
- system status
- future service monitor
- future launcher
- future AURA Control Center
- future plugin and permission dashboards

## Current Capability Summary

| Metric | Count |
|---|---:|
| Total capabilities tracked | 18 |
| Online capabilities | 12 |
| Foundation-only capabilities | 3 |
| Planner-only capabilities | 6 |
| Permission-gated planner capabilities | 2 |
| Review-only capabilities | 1 |
| Planned future capabilities | 4 |
| Disabled runtime capabilities | 2 |
| Runtime execution features | 0 |

## Online Capabilities

AURA currently tracks these online capabilities:

- Thought Loop Planner
- Reasoning Context Manager
- Knowledge Uncertainty & Internet Search Gate
- Voice Input Runtime Foundation
- Voice Intent Understanding Layer
- Vision Input Runtime Foundation
- Visual Context Understanding Layer
- Coder Project Generation Planner
- Dependency & Download Permission Gate
- Review & Stabilization 71-80
- Shared Output Formatter
- Capability Registry Consolidation

## Planned Future Capabilities

Tracked as planned, not active runtime:

- Unified Permission Workflow Manager
- AURA Runtime Service Foundation
- AURA Launcher & Health Monitor
- AURA Control Center

## Disabled Runtime Capabilities

Tracked as deferred and locked:

- Controlled File Write Runtime
- Controlled Command Execution Runtime

These are intentionally deferred to the Sprint 91-100 block unless explicitly reprioritized.

## Permission Categories

The registry tracks permission categories such as:

- read_project
- user_confirmation
- microphone_permission
- camera_permission
- screen_permission
- file_write_permission
- command_execution_permission
- dependency_download_permission
- internet_search_permission
- desktop_control_permission
- git_operation_permission

The registry only describes permission requirements. It does not grant permission.

## Control Center Use

The future AURA Control Center can use this registry to show:

- capability name
- current state
- runtime level
- risk level
- required permission
- introduced version
- category
- whether a capability is visible in the Control Center

Important rule:

The Control Center may display capability status, but it must not enable capabilities without the future Unified Permission Workflow.

## Safety Boundary

This sprint is registry-only, planner-only, proposal-only, and metadata-only.

It does not enable:

- runtime behavior changes
- automatic capability enablement
- dynamic runtime discovery
- runtime action activation
- permission grant runtime
- UI runtime
- web server runtime
- chat runtime
- service runtime
- launcher runtime
- file operations
- command execution
- test execution
- code execution
- dependency install
- package download
- internet or network action
- tool execution
- memory write
- desktop control
- git execution
- external action execution
- real tool execution

## Design Principle

AURA must know her capabilities clearly before she is allowed to perform runtime actions.


## Sprint 83 Update — Unified Permission Workflow Online

Status: UPDATED FOR v0.83.0-genesis

The Capability Registry now marks Unified Permission Workflow Manager as online.

Updated registry summary:
- total capabilities tracked: 18
- online capabilities: 13
- foundation-only capabilities: 3
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 3
- disabled runtime capabilities: 2
- runtime execution features: 0

Unified Permission Workflow remains planner-only. It does not grant permission or enable runtime action.


## Sprint 84 Update — Runtime Service Foundation Online

Status: UPDATED FOR v0.84.0-genesis

The Capability Registry now marks AURA Runtime Service Foundation as online.

Updated registry summary:
- total capabilities tracked: 18
- online capabilities: 14
- foundation-only capabilities: 4
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 2
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Runtime Service Foundation remains foundation-only. It does not create, enable, start, stop, restart, or run a real service.


## Sprint 85 Update — Launcher Health Monitor Foundation Online

Status: UPDATED FOR v0.85.0-genesis

The Capability Registry now marks AURA Launcher & Health Monitor Foundation as online.

Updated registry summary:
- total capabilities tracked: 18
- online capabilities: 15
- foundation-only capabilities: 5
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 1
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Launcher & Health Monitor Foundation remains foundation-only. It does not start, stop, restart, monitor, query, or control a real service or process.


## Sprint 86 Update — Control Center UI Blueprint Online

Status: UPDATED FOR v0.86.0-genesis

The Capability Registry now marks AURA Control Center as online.

Updated registry summary:
- total capabilities tracked: 18
- online capabilities: 16
- foundation-only capabilities: 6
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Control Center remains foundation-only and blueprint-only. It does not create, run, open, bind, control, execute, or serve a real UI/web runtime.


## Sprint 87 Update — Local Console Web Foundation Online

Status: UPDATED FOR v0.87.0-genesis

The Capability Registry now tracks AURA Local Console Web Foundation as online.

Updated registry summary:
- total capabilities tracked: 19
- online capabilities: 17
- foundation-only capabilities: 7
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Local Console Web Foundation remains foundation-only and blueprint-only. It does not start a web server, bind ports, create live routes, serve files, open browsers, or enable frontend/backend/API/session runtime.


## Sprint 88 Update — Chat Bridge & Session State Foundation Online

Status: UPDATED FOR v0.88.0-genesis

The Capability Registry now tracks AURA Chat Bridge & Session State Foundation as online.

Updated registry summary:
- total capabilities tracked: 20
- online capabilities: 18
- foundation-only capabilities: 8
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Chat Bridge & Session State Foundation remains foundation-only and blueprint-only. It does not start chat runtime, websocket runtime, session runtime, web/API runtime, grant permissions, activate actions, persist sessions, send messages, receive messages, or execute tools.


## Sprint 89 Update — Plugin / Permission Dashboard Foundation Online

Status: UPDATED FOR v0.89.0-genesis

The Capability Registry now tracks AURA Plugin / Permission Dashboard Foundation as online.

Updated registry summary:
- total capabilities tracked: 21
- online capabilities: 19
- foundation-only capabilities: 9
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Plugin / Permission Dashboard Foundation remains foundation-only and blueprint-only. It does not enable plugin runtime, execute plugin actions, grant or deny permissions, resolve permission requests, execute chat-originated actions, activate runtime actions, call tools, or run dashboard/web runtime.


## Sprint 91 Update — Local Console Static Prototype Foundation Online

Status: UPDATED FOR v0.91.0-genesis

The Capability Registry now tracks AURA Local Console Static Prototype Foundation as online.

Updated registry summary:
- total capabilities tracked: 22
- online capabilities: 20
- foundation-only capabilities: 10
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Local Console Static Prototype Foundation remains foundation-only and blueprint-only. It does not start a web server, serve static files, bind ports, launch a browser, create runtime routes, run frontend/backend/API runtime, activate chat/session/plugin/permission/action runtime, create static assets at runtime, or execute tools.


## Sprint 92 Update — Local Console API Schema Foundation Online

Status: UPDATED FOR v0.92.0-genesis

The Capability Registry now tracks AURA Local Console API Schema Foundation as online.

Updated registry summary:
- total capabilities tracked: 23
- online capabilities: 21
- foundation-only capabilities: 11
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

AURA Local Console API Schema Foundation remains foundation-only and blueprint-only. It does not start API runtime, create API routes, handle API requests, serve API responses, bind ports, fetch runtime data, run runtime validation, run runtime serialization, emit runtime errors, or execute tools.

## Sprint 181 Update — Local Web Runtime Alpha Online

Status: UPDATED FOR v0.181.0-genesis

The registry now tracks `aura_local_web_runtime_alpha` as an online,
permission-gated alpha runtime.

Current summary:

- total capabilities tracked: 112
- online capabilities: 110
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 4
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

Scoped availability now reports:

- `local_web_runtime_alpha: true`
- `localhost_only_runtime: true`
- `foreground_only_runtime: true`
- `read_only_http_runtime: true`
- `explicit_start_confirmation_required: true`
- `ui_runtime: true`
- `web_server_runtime: true`
- `service_runtime: true`

These true values refer only to the narrow Sprint 181 runtime. Full Genesis
runtime readiness remains false. Public, LAN, wildcard, background,
automatic-start, mutating-dashboard, chat, model, permission-grant, command,
tool, file, desktop, voice, vision, and autonomous runtimes remain disabled.

## Sprint 182 Update — Service Lifecycle Runtime Online

Status: UPDATED FOR v0.182.0-genesis

The registry now tracks `aura_service_lifecycle_runtime` as an online,
permission-gated alpha capability.

Current summary:

- total capabilities tracked: 113
- online capabilities: 111
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 5
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

New scoped availability fields:

- `service_lifecycle_runtime: true`
- `deterministic_lifecycle_state_machine: true`
- `single_listener_enforced: true`
- `port_conflict_fail_closed: true`
- `startup_rollback_runtime: true`
- `clean_programmatic_stop_runtime: true`
- `clean_signal_shutdown_runtime: true`

Still false:

- `runtime_ready`
- `execution_ready`
- `background_service_runtime`
- `automatic_service_start_runtime`
- `persistent_pid_file_runtime`
- `persistent_lifecycle_state_runtime`
- `remote_lifecycle_control_runtime`
- `http_lifecycle_mutation_runtime`
- chat, command, tool, file, memory-write, permission-grant, desktop, voice,
  vision, and autonomous runtime gates

Sprint 182 does not increase the runtime execution feature count because it
controls the existing Sprint 181 localhost listener.

## Sprint 183 Update — Health and Status API Runtime Online

Status: UPDATED FOR v0.183.0-genesis

The registry now tracks `aura_health_status_api_runtime` as an online,
permission-gated alpha capability.

Current summary:

- total capabilities tracked: 114
- online capabilities: 112
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 6
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

New scoped availability fields:

- `health_status_api_runtime: true`
- `read_only_status_routes: true`
- `status_route_count: 9`
- `degraded_status_reporting: true`
- `identity_status_runtime: true`
- `plugin_status_runtime: true`
- `capability_status_runtime: true`
- `service_status_runtime: true`
- `memory_status_runtime: true`
- `safety_status_runtime: true`
- `error_status_runtime: true`

Still false:

- `runtime_ready`
- `execution_ready`
- `status_api_mutation_runtime`
- `status_api_plugin_start_runtime`
- `status_api_memory_mutation_runtime`
- `status_api_listener_start_probe_runtime`
- `background_service_runtime`
- `automatic_service_start_runtime`
- chat, command, tool, file, memory-write, permission-grant, desktop, voice,
  vision, and autonomous runtime gates

Sprint 183 does not increase the runtime execution feature count because all
payloads are served through the existing Sprint 181 listener.
