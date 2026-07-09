# AURA Local Service Runtime Foundation

Version: v0.141.0-genesis  
Sprint: 141.0  
Status: completed  
Owner: Kiput  
Motto: Grow Together

## Purpose

Sprint 141 begins the Sprint 141-150 Local Service Runtime Foundation block.

This sprint prepares the first ATLAS local service runtime foundation as a safe-idle, localhost-only, permission-gated, audit-linked, and manually reviewed foundation.

It does not start a service.
It does not bind a port.
It does not open a socket.
It does not create or enable a systemd unit.
It does not activate unrestricted runtime execution.

## Foundation Scope

The Sprint 141 foundation defines planning metadata for:

- ATLAS local service identity
- safe-idle service entry
- localhost-only binding boundary
- service lifecycle states
- service configuration contract
- service health/status surface
- permission gate link
- audit link
- service control command boundary
- no-start activation review

## Plan Types

The foundation manager exposes 12 plan types:

- local_service_runtime_foundation_status
- service_foundation_scope_plan
- service_safe_idle_entry_plan
- localhost_binding_boundary_plan
- service_lifecycle_state_plan
- service_config_contract_plan
- service_health_surface_plan
- service_permission_gate_link_plan
- service_audit_link_plan
- service_control_command_boundary_plan
- service_no_start_activation_plan
- local_service_runtime_foundation_context

## Blueprint Counts

Sprint 141 includes:

- 10 service foundation scope items
- 10 safe-idle entry items
- 10 localhost binding boundary items
- 10 lifecycle state items
- 10 service config contract items
- 10 service health surface items
- 10 permission gate link items
- 10 audit link items
- 10 service control command boundary items
- 10 no-start activation items
- 100 total local service runtime foundation blueprint items

## Safety Boundary

Sprint 141 keeps the following disabled by design:

- no service process start
- no service stop or restart runtime
- no API server start
- no web server start
- no dashboard server start
- no health endpoint runtime start
- no socket open
- no port binding
- no network probe
- no background worker start
- no systemd unit creation or enablement
- no config runtime read/write
- no permission runtime mutation
- no audit writer runtime
- no audit event write
- no action dispatch
- no action execution
- no tool execution
- no command execution
- no file runtime
- no memory runtime
- no model runtime
- no ORION handshake runtime
- no git runtime
- no runtime execution features

## Expected CLI Surface

```bash
python3 main.py local-service-runtime-foundation-status
python3 main.py local-service-runtime-foundation-context
python3 main.py service-foundation-scope-plan "AURA ATLAS service"
python3 main.py service-safe-idle-entry-plan "AURA safe idle service"
python3 main.py localhost-binding-boundary-plan "AURA localhost service boundary"
python3 main.py service-lifecycle-state-plan "AURA service lifecycle"
python3 main.py service-config-contract-plan "AURA service config"
python3 main.py service-health-surface-plan "AURA service health"
python3 main.py service-permission-gate-link-plan "AURA service permission gate"
python3 main.py service-audit-link-plan "AURA service audit link"
python3 main.py service-control-command-boundary-plan "AURA service controls"
python3 main.py service-no-start-activation-plan "AURA service no-start review"
```

## Acceptance Criteria

Sprint 141 is complete when:

- local service runtime foundation manager exists
- status and context packets render safely
- all 10 plan functions return side-effect-free blueprint packets
- CLI and shell command routes exist
- skill registry and plugin action metadata exist
- capability registry includes Sprint 141 as foundation-only
- README and roadmap point to v0.141.0-genesis and Sprint 142 next
- Python compile succeeds
- boot still reports READY
- runtime execution feature counter remains 0

## Next Sprint

Sprint 142.0 — Local Service Safe Idle Boot Boundary

Sprint 142 should refine how the future local service enters safe-idle boot state, how it exposes readiness without actions, and how it refuses unsafe startup paths until explicit approval gates exist.
