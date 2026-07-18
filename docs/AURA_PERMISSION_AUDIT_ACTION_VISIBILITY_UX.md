# AURA Permission Audit Action Visibility UX

## Sprint 268 checkpoint

- Version: `v1.2.8`
- Boundary: `permission_audit_action_visibility_ux`
- Next sprint: Sprint 269
- Next boundary: `daily_use_acceptance_rehearsal_and_release_harness`

Sprint 268 consolidates permission, audit, proposal, approval, action,
and recovery state into one read-only Control Center panel. It reuses
the existing `/api/control-center` payload and adds no HTTP route.

## Visibility sections

The panel displays:

- Permission requirement counts and runtime-gate state.
- Audit writer, persistence, fetch, and bounded event state.
- Pending proposal visibility without decision execution.
- Manual approval boundaries without automatic grant.
- Service, restart, and permission-route visibility without controls.
- Recovery state without automatic or route-based execution.

## Safety boundary

The panel provides no buttons, action links, mutation routes,
automatic permission grant, automatic recovery, service action,
restart action, approval action, recovery execution, background
worker, external dependency, or new execution authority.

The runtime remains read-only and safe-idle.

## Validation target

The Sprint 268 contract contains 528 assertions across 44 dimensions.
It validates the six-section runtime facade, root Control Center
payload integration, UI renderer and safety boundary, registry, CLI,
version and documentation metadata, Sprint 267 historical anchor, and
the no-execution boundary.
