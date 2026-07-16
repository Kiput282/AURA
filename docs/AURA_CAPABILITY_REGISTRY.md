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

## Sprint 184 Update — Control Center Backend Runtime Online

Status: UPDATED FOR v0.184.0-genesis

The registry now tracks `aura_control_center_backend_runtime` as an online,
permission-gated alpha capability.

Current summary:

- total capabilities tracked: 115
- online capabilities: 113
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 7
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

New scoped availability fields:

- `control_center_backend_runtime: true`
- `read_only_control_center_backend: true`
- `control_center_backend_route_count: 9`
- `control_center_backend_panel_count: 8`
- `control_center_backend_foundation_contract_count: 8`

Still false:

- `runtime_ready`
- `execution_ready`
- `control_center_web_shell_runtime`
- `control_center_frontend_asset_runtime`
- `control_center_browser_launch_runtime`
- `control_center_backend_mutation_runtime`
- `control_center_service_control_runtime`
- `control_center_plugin_control_runtime`
- `control_center_permission_decision_runtime`
- `control_center_audit_writer_runtime`
- `control_center_memory_write_runtime`
- background service, automatic startup, chat, model, command, tool, action,
  arbitrary file, desktop, voice, vision, and autonomous runtime gates

Sprint 184 does not increase the runtime execution feature count because all
backend view models are served through the existing Sprint 181 listener.

## Sprint 185 Update — Control Center Web Shell Runtime Online

Status: UPDATED FOR v0.185.0-genesis

The registry now tracks `aura_control_center_web_shell_runtime` as an online,
permission-gated alpha capability.

Current summary:

- total capabilities tracked: 116
- online capabilities: 114
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 8
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

Activated scoped fields:

- `control_center_web_shell_runtime: true`
- `control_center_frontend_asset_runtime: true`
- `control_center_web_shell_asset_route_count: 3`
- `control_center_web_shell_panel_count: 8`
- `control_center_total_route_count: 21`
- `control_center_responsive_layout: true`
- `control_center_accessibility_contract: true`
- `control_center_degraded_state_ui: true`
- `control_center_safe_idle_indicator: true`

Still false:

- `runtime_ready`
- `execution_ready`
- `control_center_browser_launch_runtime`
- `control_center_backend_mutation_runtime`
- `control_center_service_control_runtime`
- `control_center_plugin_control_runtime`
- `control_center_permission_decision_runtime`
- `control_center_audit_writer_runtime`
- `control_center_memory_write_runtime`
- `control_center_external_dependency_runtime`
- browser chat, model, background service, automatic startup, command, tool,
  action, arbitrary file, desktop, voice, vision, and autonomous runtime gates

Sprint 185 does not increase the runtime execution feature count because the
dashboard uses the same Sprint 181 listener.

## Sprint 186 Update — Browser Chat Session Runtime Online

Status: UPDATED FOR v0.186.0-genesis

The registry now tracks `aura_browser_chat_session_runtime` as an online,
permission-gated alpha capability.

Current summary:

- total capabilities tracked: 117
- online capabilities: 115
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 9
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 1

Activated scoped fields include:

- `browser_chat_session_runtime: true`
- `browser_chat_http_routes: true`
- `browser_chat_session_creation: true`
- `browser_chat_validated_submission: true`
- `browser_chat_response_delivery: true`
- `browser_chat_history_persistence: true`
- `browser_chat_session_reload: true`
- `browser_chat_clear_confirmation: true`
- `browser_chat_revision_control: true`
- `browser_chat_idempotent_submission: true`
- `browser_chat_integrity_hash: true`
- `browser_chat_bounded_mutation: true`
- `browser_chat_asset_route_count: 3`
- `browser_chat_route_contract_count: 6`
- `local_interaction_total_route_contract_count: 27`
- `local_session_file_write_runtime: true`
- `chat_runtime: true`

Still false:

- `runtime_ready`
- `execution_ready`
- `local_model_bridge_runtime`
- `local_model_inference_runtime`
- `network_fallback_runtime`
- `aura_long_term_memory_write_runtime`
- `control_center_browser_launch_runtime`
- service/plugin control and permission mutation
- audit writer
- tools, commands, external actions, arbitrary files, and desktop control
- background service, systemd, automatic startup, public/LAN binding,
  voice, vision, and autonomy

`file_write` remains false because Sprint 186 does not enable arbitrary file
writes; only the fixed, validated local chat-session storage boundary is
active.

Runtime execution features remain `1`.

## Sprint 187 Update — Local Model Bridge Runtime Online

Status: UPDATED FOR v0.187.0-genesis

The registry now tracks `aura_local_model_bridge_runtime` as an online,
permission-gated alpha runtime.

Current summary:

- total capabilities tracked: 118
- online capabilities: 116
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 10
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 2

New active boundaries include:

- `local_model_bridge_runtime: true`
- `local_model_inference_runtime: true`
- `browser_chat_model_bridge_runtime: true`
- `local_model_probe_runtime: true`
- `local_model_response_persistence: true`
- `browser_chat_route_contract_count: 7`
- `local_interaction_total_route_contract_count: 30`

Model downloads, remote providers, redirect following, internet fallback,
streaming, tool/function calling, commands, actions, arbitrary files, desktop
control, AURA long-term memory writes, background service, public/LAN binding,
and autonomy remain disabled.

## Sprint 188 Update — Interactive Control Center Chat Online

Status: UPDATED FOR v0.188.0-genesis

The registry now tracks
`aura_interactive_control_center_chat_runtime` as an online,
permission-gated alpha runtime.

Current summary:

- total capabilities tracked: 119
- online capabilities: 117
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 11
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 3

New active boundaries include:

- `interactive_control_center_chat_runtime: true`
- `interactive_chat_web_surface_runtime: true`
- `interactive_chat_orchestration_runtime: true`
- `interactive_chat_save_only_default: true`
- `interactive_chat_model_request_confirmation_ui: true`
- `interactive_chat_idempotent_retry_ui: true`
- `interactive_chat_response_kind_visibility: true`

Provider default activation, model downloads, remote providers, internet
fallback, streaming, tools, commands, actions, arbitrary files, desktop
control, AURA long-term memory writes, browser storage,
WebSocket/EventSource, background service, public/LAN binding, browser
auto-launch, and autonomy remain disabled.

## Sprint 189 Update — Permission, Audit, and Recovery Visibility Online

Status: UPDATED FOR v0.189.0-genesis

The registry now tracks
`aura_permission_audit_recovery_visibility_runtime` as an online,
permission-gated alpha runtime.

Current summary:

- total capabilities tracked: 120
- online capabilities: 118
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 12
- review-only capabilities: 10
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 4

The runtime adds seven local visibility routes: three browser assets and four
GET/HEAD API routes. Total local interaction route contracts are now 37.

New active boundaries include:

- `permission_audit_recovery_visibility_runtime: true`
- `permission_visibility_runtime: true`
- `audit_contract_visibility_runtime: true`
- `recovery_guidance_visibility_runtime: true`
- `permission_audit_recovery_read_only: true`
- `sensitive_values_exposed: false`

Permission mutation/persistence, audit writing/persistence, automatic
recovery/retry/restart, rollback execution, downloads, remote providers,
internet fallback, streaming, tools, commands, actions, arbitrary files,
desktop control, AURA long-term memory writes, browser storage,
WebSocket/EventSource, background service, public/LAN binding, browser
auto-launch, and autonomy remain disabled.


## Sprint 190 Update — Local Interaction Runtime Stabilization

Status: UPDATED FOR v0.190.0-genesis

The registry now tracks
`aura_local_interaction_runtime_stabilization` as an online, review-only
checkpoint capability.

Current summary:

- total capabilities tracked: 121
- online capabilities: 119
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 12
- review-only capabilities: 11
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 4

Stabilization evidence:

- 9 components checked and ready;
- 10 dependency self-tests;
- 1,088 dependency assertions;
- 87 checkpoint assertions;
- 1,175 total assertion coverage;
- 0 failed assertions;
- 0 stabilization gaps;
- 0 runtime violations;
- block 181-190 complete;
- voice runtime block ready.

The review-only capability does not increase runtime execution feature
accounting. No listener, provider, persistence store, permission mutation,
audit writer, recovery executor, command, tool, action, arbitrary file,
desktop, voice, vision, background, public/LAN, or autonomous runtime is added.

## Sprint 241 Update — Genesis Stabilization Runtime Hardening

Status: UPDATED FOR v1.0.1-genesis

Sprint 241 adds the online, review-only
`aura_genesis_stabilization_runtime_hardening` capability.

Current registry summary:

- total capabilities: 122
- online capabilities: 120
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 12
- review-only capabilities: 12
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 4

The capability verifies exact CLI ownership, rejects unrelated commands
before manager construction, preserves explicit deep Genesis Final
validation, enforces bounded finalized-release status projection latency,
and confirms memory/journal integrity.

It does not activate runtime behavior, start services or listeners, enable
systemd, open release gates, control ORION, or enable autonomous execution.

## Sprint 242 Update — Service Lifecycle Determinism

The registry now includes
`aura_service_lifecycle_determinism` as an online, low-risk,
read-project, review-only stabilization capability.

Current canonical summary:

- total capabilities: 123
- online capabilities: 121
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 12
- review-only capabilities: 13
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 4

Sprint 242 does not add another runtime executor. It hardens deterministic
control of the existing localhost foreground lifecycle owner.

## Sprint 243 Update — Configuration Integrity

The registry now includes `aura_configuration_integrity` as an online,
low-risk, read-project, review-only stabilization capability.

Current canonical summary:

- total capabilities: 124
- online capabilities: 122
- foundation-only capabilities: 78
- planner-only capabilities: 7
- permission-gated capabilities: 12
- review-only capabilities: 14
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 4

Sprint 243 does not add a runtime executor. It validates the existing
canonical settings file without writing configuration or activating
service runtime.

## Sprint 244 Update — Session and Memory Persistence Checks

- Added capability `aura_session_memory_persistence_checks`.
- State: `online`.
- Runtime level: `review_only`.
- Risk level: `low`.
- Permission required: `read_project`.
- Introduced in: `1.0.4-genesis`.
- Capability totals: `125` total, `123` online, `78` foundation-only, `7` planner-only, `12` permission-gated, `15` review-only, `0` planned, `2` disabled runtime, and `4` runtime execution features.
- The capability exposes read-only persistence validation and does not repair, migrate, write, activate runtime, bind sockets, or mutate systemd state.

## AURA Log Rotation and Storage Cleanup

- ID: `aura_log_rotation_storage_cleanup`
- Version introduced: `1.0.5-genesis`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Visible: `true`

Provides deterministic read-only status, context, contract checks, filesystem
capacity visibility, and cleanup-preview packets for the canonical `1 MB`
rotation and `7 days` retention policy. The active log is protected, rotated
names are allowlisted, symlinks and directory escape are blocked, and cleanup
execution remains disabled.

## AURA Resource Baseline Metrics

- ID: `aura_resource_baseline_metrics`
- Version introduced: `1.0.6-genesis`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Control Center visible: `true`

Provides read-only, single-snapshot CPU, load, memory, swap, uptime, process,
filesystem-capacity, and inode-capacity baselines for ATLAS without `psutil`,
background sampling, persistence, dashboard activation, sockets, systemd,
network access, process control, or threshold mutation.

## AURA ATLAS Resource Monitoring

- ID: `aura_atlas_resource_monitoring`
- Version introduced: `1.0.7-genesis`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Control Center visible: `true`

Provides read-only health classification for CPU, normalized load, memory,
swap, storage, inode capacity, uptime, and process count from the Sprint 246
resource snapshot. Thresholds are immutable, and no background monitoring,
history persistence, dashboard activation, alert delivery, sockets, systemd,
network access, process control, command execution, or threshold mutation is
enabled.

## AURA Localhost and SSH Tunnel Security Review

- ID: `aura_localhost_ssh_tunnel_security_review`
- Version introduced: `1.0.8-genesis`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Control Center visible: `true`

Provides read-only posture visibility for the AURA localhost binding, port
`8765`, SSH listener scope, visible sshd settings, tunnel policy, SSH file
permission metadata, firewall visibility, and runtime activation. It does not
execute sshd, create network connections or tunnels, read credentials or
private-key content, mutate SSH/firewall configuration, restart services,
bind sockets, control processes, generate keys, modify known hosts, or mutate
systemd.

## AURA Permission Expiry and Recovery Review

- ID: `aura_permission_expiry_recovery_review`
- Version introduced: `1.0.9-genesis`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Control Center visible: `true`

Provides read-only source-contract visibility for grant lifecycle, expiry
enforcement, stale-grant rejection, denial lifecycle, revocation, recovery,
rollback/emergency-stop linkage, and audit linkage. It does not import or
execute permission runtime, read permission/audit/recovery store contents,
create or apply grants or denials, apply expiry or revocation, execute
recovery, rollback, or emergency stop, write audit events, mutate files,
control processes, activate services, open network access, bind sockets, or
mutate systemd.

## AURA Backup and Restore Rehearsal

- ID: `aura_backup_restore_rehearsal`
- Version introduced: `1.1.0`
- Category: `stabilization`
- State: `online`
- Runtime level: `review_only`
- Risk: `low`
- Permission: `read_project`
- Control Center visible: `true`

Provides read-only rehearsal visibility for backup scope, manifest and digest
integrity, restore-plan reversibility, permission and approval boundaries,
audit and provenance linkage, safe-idle failure behavior, contract
deduplication, and Sprint 241–250 block release acceptance. It does not create
backups or archives, read canonical data or backup-store contents, execute
restore or rollback, write manifests, replace or delete files, mutate
permissions or audit state, control processes, activate services, open network
access, bind sockets, or mutate systemd.

## AURA Launcher and Service Controls

- Capability ID: `aura_launcher_service_controls`
- State: `online`
- Runtime level: `review_only`
- Risk level: `low`
- Permission required: `read_project`
- Introduced in: `1.1.1`
- Category: `runtime_integration`
- Control Center visible: `true`

This capability provides a read-only integration facade over the canonical
launcher, lifecycle, health, status, log-visibility, permission, audit,
recovery, and safe-idle owners.

It does not create a duplicate service manager or execute service start,
stop, restart, process control, socket activation, network access, systemd
mutation, autostart mutation, log mutation, permission mutation, audit
writes, recovery actions, or external commands.

## Sprint 252 capability — Manual Start, Stop, and Status Runtime

- ID: `manual_start_stop_status_runtime`
- State: `online`
- Runtime level: `permission_gated_alpha_runtime`
- Risk level: `high`
- Permission required: `user_confirmation`
- Introduced in: `1.1.2`
- Category: `runtime_control`
- Control Center visible: yes

This capability provides explicit supervised local start, verified owned
process stop, and live status for the canonical loopback service. Runtime
execution is fail-closed and requires exact approval flags. Restart,
autostart, systemd mutation, non-loopback activation, permission-store
mutation, and persistent audit writing remain disabled.

After registration:

- total capabilities: `133`;
- online capabilities: `131`;
- foundation-only capabilities: `78`;
- planner-only capabilities: `7`;
- permission-gated capabilities: `13`;
- review-only capabilities: `22`;
- planned-future capabilities: `0`;
- disabled-runtime capabilities: `2`;
- runtime execution features: `5`.

## Sprint 253 capability — Restart, Logs, and Failure Visibility

- ID: `restart_logs_failure_visibility`
- Name: Restart, Logs, and Failure Visibility
- State: `online`
- Runtime level: `permission_gated_alpha_runtime`
- Risk level: `high`
- Permission required: `user_confirmation`
- Introduced in: `1.1.3`
- Category: `runtime_control`
- Control Center visible: `true`

This capability provides supervised local restart through the canonical
manual runtime owner, bounded allowlisted and redacted log tail visibility,
and structured failure packets. It rejects unowned runtime evidence,
arbitrary PID signaling, arbitrary log paths, non-loopback activation,
systemd mutation, autostart mutation, permission-store mutation, persistent
audit writes, and canonical-log mutation.

## Sprint 254 capability — Process Ownership and Service State Persistence

- ID: `process_ownership_service_state_persistence`
- State: `online`
- Runtime level: `permission_gated_alpha_runtime`
- Risk: `high`
- Permission: `user_confirmation`
- Introduced in: `1.1.4`
- Category: `runtime_control`
- Control Center visible: `true`

Persistent ownership state is descriptor-safe, atomic, permission-gated, and
recoverable only through approved runtime controls.

## Sprint 255 capability — Reviewed Optional Autostart

- ID: `reviewed_optional_autostart`
- State: `online`
- Runtime level: `permission_gated_alpha_runtime`
- Risk: `high`
- Permission: `user_confirmation`
- Introduced in: `1.1.5`
- Category: `runtime_control`
- Control Center visible: `true`

The capability renders and reviews an exact user-unit contract, host posture,
activation plan, and rollback plan. It performs no systemd mutation.

## Sprint 256 capability — Persistent Local Chat Session Activation

- ID: `persistent_local_chat_session_activation`
- State: `online`
- Runtime level: `permission_gated_alpha_runtime`
- Risk: `high`
- Permission: `user_confirmation`
- Introduced in: `1.1.6`
- Category: `local_chat`
- Control Center visible: `true`

The capability hardens existing browser-chat persistence with descriptor-safe
reads, cross-process locking, private storage, atomic writes, bounded metadata
history, integrity verification, and explicit existing memory gates.
