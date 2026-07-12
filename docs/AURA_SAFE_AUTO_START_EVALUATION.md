# AURA Safe Auto-Start Evaluation

## Checkpoint

- Version: `v0.228.0-genesis`
- Sprint: 228
- Block: Sprint 221-230 Unified Partner Runtime Integration
- Runtime state: contract-only and read-only
- Assertions: 358
- Failed assertions: 0
- Next sprint: 229
- Next boundary: `genesis_acceptance_rehearsal`

## Purpose

Sprint 228 evaluates the prerequisites for possible future automatic startup
of AURA on ATLAS.

The sprint does not enable auto-start. It defines and verifies the safety
conditions that must exist before automatic service activation can be
considered.

## Implementation

The Sprint 228 implementation provides:

    aura/partner_runtime/safe_auto_start_evaluation_planner.py
    aura/partner_runtime/safe_auto_start_evaluation_alpha_manager.py
    aura/partner_runtime/__init__.py
    aura/core/cli.py
    aura/core/shell.py

It also advances canonical identity compatibility to
`0.228.0-genesis`.

## Canonical lifecycle owner

The canonical lifecycle owner remains:

    aura.service_lifecycle_runtime.AuraServiceLifecycleRuntimeManager

Its Sprint 228 access mode is:

    static_contract_metadata_only

Sprint 228 may inspect static class metadata such as:

- class identity
- constructor signature
- declared member names
- descriptor types
- source identity
- source hash

Sprint 228 does not:

- instantiate the lifecycle manager
- invoke lifecycle snapshots
- invoke foreground execution
- invoke stop or restart behavior
- acquire process ownership
- install signal handlers
- perform startup rollback
- bind or inspect a live port

## Foundation owners

Sprint 228 uses nine bounded read-only foundation metadata owners:

1. safe-idle boot boundary
2. localhost security review
3. health endpoint foundation
4. permission-gate boundary
5. audit-link foundation
6. recovery and restart policy foundation
7. boot-plan review foundation
8. launcher health monitor foundation
9. Control Center service-monitor foundation

These owners do not receive runtime authority.

## Method policy

The owner contract contains 90 audited methods.

### Zero-argument metadata methods

Thirty-three methods require no argument.

They are:

- invoked read-only
- invoked twice
- verified deterministic
- prevented from opening runtime authority

### Target-plan methods

Fifty-seven methods require one argument named `target`.

Their canonical future target is:

    safe_auto_start_evaluation

These methods are recorded by signature but are not invoked during Sprint 228.

## Evaluation domains

Sprint 228 defines ten evaluation domains:

1. `safe_idle_boot_precondition`
2. `localhost_only_binding_precondition`
3. `health_readiness_precondition`
4. `permission_confirmation_precondition`
5. `audit_traceability_precondition`
6. `manual_recovery_precondition`
7. `emergency_stop_precondition`
8. `operator_visibility_precondition`
9. `systemd_unit_review_precondition`
10. `rollback_and_disable_precondition`

Every domain remains non-activating.

## Safe-idle requirement

A future auto-start implementation must begin in a deterministic safe-idle
state.

Failure to satisfy permission, audit, health, security, or recovery
prerequisites must preserve or return AURA to safe idle.

Sprint 228 does not implement boot activation.

## Localhost requirement

Any future automatically started web or service surface must remain bound to
localhost unless a separate, explicit, reviewed security boundary is approved.

Sprint 228 opens no listener and no socket.

## Permission and audit requirement

Future auto-start must not bypass:

- explicit permission policy
- operator confirmation requirements
- audit traceability
- visible failure reporting
- manual disable and rollback controls

Sprint 228 mutates no permission or audit state.

## Recovery requirement

Recovery remains manual and review-driven.

Sprint 228 does not enable:

- automatic restart
- autonomous recovery
- unattended process relaunch
- hidden retry loops
- background repair actions

## Systemd requirement

A future systemd unit would require a separate implementation and review.

Sprint 228 does not:

- create a unit file
- write a unit file
- install a unit file
- enable a unit
- start a unit
- stop a unit
- restart a unit
- call `systemctl`

## Operator visibility

A future startup surface must expose sufficient status for the operator to
understand:

- whether AURA is stopped, starting, ready, degraded, or failed
- whether localhost binding is preserved
- whether health checks pass
- whether recovery is required
- whether auto-start is disabled
- how to stop or disable the service safely

Sprint 228 provides metadata contracts only.

## CLI and shell routes

The following read-only routes are available:

    partner-runtime-safe-auto-start-evaluation-status
    partner-runtime-safe-auto-start-evaluation-context
    partner-runtime-safe-auto-start-evaluation-check

CLI and shell return identical deterministic packets.

## Validation contract

The Sprint 228 planner validates 358 assertions.

Required properties include:

- Sprint 227 remains stable at 208/208
- nine foundation owners are available
- 90 owner methods are classified
- 33 zero-argument methods are deterministic
- 57 target methods remain uninvoked
- ten safety domains remain non-activating
- lifecycle access remains static-only
- lifecycle instance count remains zero
- lifecycle runtime invocation count remains zero
- all runtime-effect counters remain zero
- runtime data remains unchanged
- release gate remains closed

## Runtime and safety boundary

Sprint 228 does not:

- enable auto-start
- create or install a systemd unit
- call `systemctl`
- start, stop, or restart a service
- open a listener or socket
- start a thread or subprocess
- execute a launcher
- auto-launch a browser
- enable automatic restart
- enable autonomous recovery
- write service or PID state
- activate runtime authority
- open a release gate
- perform autonomous action

## Next boundary

Sprint 229 — Genesis Acceptance Rehearsal

Canonical boundary identifier:

    genesis_acceptance_rehearsal
