# AURA Local Service Safe Idle Boot Boundary

Version: v0.142.0-genesis  
Sprint: 142.0  
Status: completed  
Runtime state: disabled by design

## Purpose

Sprint 142 defines the safe-idle boot boundary for AURA's future ATLAS local service runtime.

It is planner-only, metadata-only, foundation-only, and review-only. It prepares boot-state contracts and safe fallback rules without starting a service, enabling autostart, opening sockets, binding ports, creating or starting systemd units, running health endpoints, dispatching actions, executing tools or commands, reading/writing runtime files, mutating permissions, writing audit events, performing ORION handshakes, or enabling runtime execution.

## Plan types

1. `local_service_safe_idle_boot_boundary_status`
2. `safe_idle_boot_scope_plan`
3. `boot_entry_state_contract_plan`
4. `safe_idle_guard_condition_plan`
5. `boot_failure_fallback_plan`
6. `service_no_autostart_boundary_plan`
7. `readiness_probe_read_only_plan`
8. `control_center_idle_visibility_plan`
9. `permission_denial_idle_plan`
10. `audit_failure_idle_plan`
11. `no_boot_activation_plan`
12. `local_service_safe_idle_boot_boundary_context`

## Blueprint inventory

Sprint 142 contains 10 blueprint groups and 100 blueprint/items:

- safe-idle boot scope items: 10
- boot entry state contract items: 10
- safe-idle guard condition items: 10
- boot failure fallback items: 10
- service no-autostart boundary items: 10
- readiness probe read-only items: 10
- Control Center idle visibility items: 10
- permission denial idle items: 10
- audit failure idle items: 10
- no-boot-activation items: 10

## Safe-idle principle

AURA's future local service must boot into safe-idle unless a future reviewed checkpoint explicitly authorizes a stronger runtime state.

Safe-idle means:

- read-only status metadata is allowed
- runtime action dispatch is blocked
- tool and command execution are blocked
- file and memory runtime writes are blocked
- service start and autostart are blocked
- network probes, sockets, and port binding are blocked
- permission mutation is blocked
- audit writer runtime is blocked
- ORION runtime handshake is blocked
- systemd unit creation, enablement, or start is blocked

## Boot-state contract

Sprint 142 defines future states only as metadata:

- `planned`
- `safe_idle`
- `degraded_idle`
- `failed_idle`
- `permission_blocked`
- `config_blocked`
- `audit_blocked`
- `network_blocked`
- `ready_deferred`
- `runtime_active_forbidden_now`

These state names do not activate state transitions. They are schema and planning metadata for future runtime reviews.

## Fallback behavior

Any unresolved condition must keep AURA in safe-idle or failed-idle:

- missing or invalid config
- missing or denied permission
- audit unavailability
- port conflict
- health probe error
- ORION unavailability
- unexpected exception

No fallback may start runtime.

## No-autostart boundary

Sprint 142 explicitly keeps these deferred:

- systemd install
- systemd enable
- systemd start
- reboot autostart
- daemon background worker
- watchdog process
- launcher autostart
- manual start command runtime

## Read-only readiness probe

Future readiness probes must remain metadata-only until a later approved sprint.

Sprint 142 does not create a real probe endpoint, open a port, call a network interface, touch systemd, write files, create permissions, or perform a runtime health check.

## Control Center visibility

Future Control Center may display safe-idle boot metadata, blockers, zero counters, permission state, and audit state. Display visibility must not become activation.

Start, restart, logs, and runtime control buttons remain disabled or deferred until future permission/audit reviews.

## Runtime zero counters

Sprint 142 keeps all runtime counters at zero:

- services started: 0
- autostarts enabled: 0
- systemd units created/enabled/started: 0
- sockets opened: 0
- ports bound: 0
- health endpoints started: 0
- readiness probe network calls: 0
- permissions created/mutated/applied: 0
- audit writers/events/log appends: 0
- actions/tools/commands executed: 0
- runtime file/memory/model actions: 0
- ORION handshakes: 0
- git runtime operations: 0
- runtime execution features: 0

## Validation commands

```bash
python3 -m compileall -q .
python3 main.py
python3 main.py local-service-safe-idle-boot-boundary-status
python3 main.py no-boot-activation-plan
python3 main.py capability-registry-status
```

## Next sprint

Sprint 143.0 — Local Service Health Endpoint Foundation.
