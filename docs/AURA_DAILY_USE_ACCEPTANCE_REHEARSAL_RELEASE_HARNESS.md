# AURA Daily-use Acceptance Rehearsal Release Harness

## Sprint 269 checkpoint

- Version: `v1.2.9`
- Boundary: `daily_use_acceptance_rehearsal_and_release_harness`
- Next sprint: Sprint 270
- Next boundary: `daily_local_assistant_live_acceptance_stabilization`

Sprint 269 aggregates nine daily-use readiness checks into a
contract-only rehearsal and release-decision harness. It reuses the
existing `/api/control-center` payload and adds no HTTP route.

## Rehearsal steps

The harness evaluates:

1. Baseline readiness.
2. Service visibility.
3. Browser chat readiness.
4. Model handoff readiness.
5. Memory review readiness.
6. Permission and action visibility.
7. ATLAS resource readiness.
8. Release decision.
9. Safe-idle return.

## Safety boundary

Sprint 269 does not start or stop the service, create a chat session,
invoke a model, write memory, grant permission, execute recovery,
persist rehearsal results, start a background worker, add an external
dependency, or add execution authority.

Live end-to-end acceptance, failure/recovery verification, and the
mandatory return to safe-idle belong to Sprint 270.

## Validation target

The Sprint 269 contract contains 552 assertions across 46 dimensions.
The runtime self-test contains 72 assertions across nine steps. The
Control Center web-shell target is 190 assertions.
