# AURA Service Persistence and Launcher

## Checkpoint

- Version: `v0.227.0-genesis`
- Sprint: 227
- Block: Sprint 221-230 Unified Partner Runtime Integration
- Runtime state: contract-only and metadata-only
- Assertions: 208
- Failed assertions: 0
- Next sprint: 228
- Next boundary: `safe_auto_start_evaluation`

## Purpose

Sprint 227 defines the metadata and safety contract for AURA's future persistent
ATLAS service state and launcher surfaces.

The sprint does not activate persistence or service authority. It defines what
may eventually be represented and which runtime operations must remain closed.

The contract declares 15 service-state metadata fields and eight explicitly excluded runtime-payload fields.

## Implementation

The Sprint 227 implementation provides:

    aura/partner_runtime/service_persistence_and_launcher_planner.py
    aura/partner_runtime/service_persistence_and_launcher_alpha_manager.py
    aura/partner_runtime/__init__.py
    aura/core/cli.py
    aura/core/shell.py

The public read-only methods are:

    status
    context
    plan
    check
    contract

## Canonical lifecycle owner

The canonical lifecycle owner is:

    aura.service_lifecycle_runtime.AuraServiceLifecycleRuntimeManager

Its Sprint 227 access mode is:

    static_contract_metadata_only

Sprint 227 may inspect:

- class identity
- constructor signature
- lifecycle enum values
- declared method names
- component metadata

Sprint 227 does not:

- instantiate the lifecycle manager
- invoke `snapshot()`
- invoke `run_foreground()`
- invoke `request_stop()`
- invoke `self_test()`
- start or stop a service
- open or bind a socket
- start a thread

## Secondary metadata owners

The launcher foundation owner is:

    AuraLauncherHealthMonitorFoundationManager

Its role is:

    secondary_read_only_metadata_owner

The runtime-service foundation owner is:

    AuraRuntimeServiceFoundationManager

Its role is:

    secondary_read_only_blueprint_reference

The local-service foundation owner is:

    AuraLocalServiceRuntimeFoundationManager

Its role is:

    secondary_read_only_safety_baseline

Only bounded read-only metadata methods are used.

## Service-state schema

The canonical service-state metadata fields are:

1. `service_name`
2. `identity_version`
3. `lifecycle_state`
4. `boot_mode`
5. `launch_mode`
6. `safe_idle_required`
7. `runtime_actions_locked`
8. `health_state`
9. `recovery_hint`
10. `pid_file_status`
11. `state_file_status`
12. `systemd_unit_status`
13. `last_transition_metadata`
14. `persistence_runtime_enabled`
15. `launcher_runtime_enabled`

The defaults keep the service:

- stopped
- safe-idle
- manual-only
- runtime-locked
- persistence-disabled
- launcher-runtime-disabled

No state object is created, loaded, or written.

## Excluded runtime payloads

The following payload-adjacent fields are outside the Sprint 227 contract:

- `process_id`
- `process_handle`
- `server_instance`
- `socket_handle`
- `thread_handle`
- `service_log_payload`
- `environment_payload`
- `command_result_payload`

The service-state schema remains payload-free.

## Persistence artifacts

Sprint 227 declares four future artifact roles:

- service-state file
- PID file
- launcher log file
- systemd user unit

For every artifact:

- read is disabled
- write is disabled
- creation is disabled

No filesystem persistence is performed.

## Launcher policy

The declared launcher actions are:

- status
- start
- stop
- restart
- logs
- health check

All actions remain planned metadata only.

The policy requires:

- safe-idle as the default mode
- explicit operator start
- manual confirmation
- metadata-only status visibility

The policy forbids:

- process spawn
- systemctl
- service mutation
- log-file reads
- health network probes
- browser auto-launch
- automatic startup

## Recovery policy

Recovery remains:

- manual-only
- safe-idle fallback
- operator-review required
- automatic restart disabled
- autonomous recovery disabled

No PID-file or state-file recovery is performed.

## Commands

The following read-only commands are available:

    partner-runtime-service-persistence-launcher-status
    partner-runtime-service-persistence-launcher-context
    partner-runtime-service-persistence-launcher-check

CLI and shell expose identical deterministic packets.

## Validation contract

The Sprint 227 planner validates 208 assertions.

Required properties include:

- Sprint 226 upstream baseline remains 128/128
- canonical lifecycle owner remains static-only
- lifecycle manager is not instantiated
- lifecycle methods are not invoked
- service-state schema contains 15 fields
- excluded runtime payload list contains eight fields
- persistence schema contains four artifacts
- all runtime safety flags remain false
- all runtime counters remain zero
- no runtime data changes
- no service or launcher authority opens

## Runtime and safety boundary

Sprint 227 does not:

- write service state
- write a PID or lifecycle state file
- create or write launcher logs
- create or install a systemd unit
- call systemctl
- start, stop, or restart a service
- start a listener
- open or bind a socket
- start a thread or subprocess
- execute a launcher
- auto-launch a browser
- enable auto-start
- perform automatic restart
- perform autonomous recovery
- activate runtime authority
- open a release gate
- perform autonomous action

## Next boundary

Sprint 228 — Safe Auto-Start Evaluation

Canonical boundary identifier:

    safe_auto_start_evaluation
