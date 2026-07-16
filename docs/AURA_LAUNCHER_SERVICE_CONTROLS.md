# AURA Launcher and Service Controls

Version: `v1.1.1`
Sprint: `251`
Boundary: `aura_launcher_service_controls`
Runtime level: `review_only`
Delivery mode: `integration_facade_read_only`

## Purpose

Sprint 251 establishes one canonical read-only facade for the practical AURA
launcher and service-control experience without creating a second service
manager.

The facade reuses the existing service lifecycle runtime and consolidates
evidence from launcher persistence, lifecycle state, health and status
surfaces, permission and audit gates, recovery policy, safe-idle behavior,
and Control Center visibility.

## Contract

- Assertions: `120/120`
- Failed assertions: `0`
- Secure dimensions: `10`
- Review dimensions: `0`
- Warning dimensions: `0`
- Unavailable dimensions: `0`
- Findings: `0`
- Sprint 250 anchor: `96/96`
- Service lifecycle anchor: `25/25`
- Genesis Final anchor: `1258/1258`
- Active permission anchor: `3115/3115`

## Dimensions

1. `launcher_surface_contract`
2. `canonical_service_state_model`
3. `manual_start_preview_boundary`
4. `manual_stop_preview_boundary`
5. `status_and_health_visibility`
6. `restart_and_recovery_preview`
7. `log_visibility_boundary`
8. `permission_audit_and_ownership`
9. `safe_idle_failure_behavior`
10. `integration_acceptance_scenario`

## Ownership

Canonical lifecycle owner:

`aura.service_lifecycle_runtime`

Canonical launcher anchor:

`aura.partner_runtime.service_persistence_and_launcher_planner`

Sprint 251 does not replace either owner and does not create a duplicate
service manager.

## Runtime boundary

The following remain disabled:

- service start execution;
- service stop execution;
- service restart execution;
- process control;
- socket activation;
- network access;
- systemd mutation;
- autostart mutation;
- log mutation;
- permission mutation;
- audit writes;
- recovery execution;
- external command execution.

## Acceptance scenarios

1. ATLAS boots with the AURA service stopped by default.
2. The launcher reads the canonical stopped state without process mutation.
3. A start request returns a bounded preview and approval requirement.
4. Status correlates process ownership, health, port, and safe-idle state.
5. Logs remain read-only and clearly scoped.
6. Restart is represented as stop, verification, start, and health check.
7. Failure returns to safe-idle without an orphan process.
8. Sprint 252 can activate controls without replacing this schema.

## Sprint 252 handoff

Next sprint: `252`
Next title: `Manual Start, Stop, and Status Runtime`
Next boundary: `manual_start_stop_status_runtime`
Next version: `v1.1.2`

Sprint 252 may activate manual start, stop, and status only through explicit
approval, canonical process ownership, loopback-only binding, health
verification, timeout handling, audit linkage, and safe-idle failure
recovery. Restart and autostart remain separately bounded.
