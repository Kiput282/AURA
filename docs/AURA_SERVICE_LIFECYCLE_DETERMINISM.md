# AURA Service Lifecycle Determinism

Version: `v1.0.2-genesis`
Sprint: `242`
Status: COMPLETED
Boundary: `service_lifecycle_determinism`
Next sprint: `243`
Next boundary: `configuration_integrity`

## Purpose

Sprint 242 hardens the existing Sprint 182 foreground lifecycle runtime
without creating a second service owner or enabling automatic startup.

## Completed changes

- Reject stop requests while lifecycle startup is still in progress.
- Preserve deterministic `already_stopped` responses.
- Preserve deterministic `stop_already_in_progress` responses.
- Add a 25-assertion lifecycle determinism check.
- Add canonical lifecycle determinism status, context, and check commands.
- Restore pure-JSON output for the historical lifecycle self-test.
- Preserve normal runtime access logging.
- Preserve the Sprint 182 historical baseline at 41 assertions.

## Canonical commands

    service-lifecycle-determinism-status
    service-lifecycle-determinism-context
    service-lifecycle-determinism-check

## Deterministic policies

    stopped  + stop request -> rejected / already_stopped
    starting + stop request -> rejected / startup_in_progress
    stopping + stop request -> rejected / stop_already_in_progress

Rejecting a stop request during startup prevents an invalid
`stopping -> running` race while the listener is being assembled.

## Safety boundary

Sprint 242 does not enable:

- background daemon execution;
- automatic startup;
- persistent PID files;
- persistent lifecycle-state files;
- systemd installation or control;
- remote lifecycle control;
- HTTP lifecycle mutation;
- public or LAN binding;
- autonomous recovery;
- browser auto-launch;
- additional runtime execution features.

The lifecycle listener remains localhost-only, foreground-only, and
requires the historical explicit confirmation command.

## Acceptance baseline

- Sprint 242 determinism check: `25/25`;
- Sprint 182 lifecycle self-test: `41/41`;
- lifecycle CLI output: pure JSON;
- normal interactive access logging: preserved;
- listener after validation: absent;
- memory and project journal hashes: unchanged;
- runtime activation from the Sprint 242 owner: disabled.

## Handoff

Sprint 243 will review `configuration_integrity` while preserving the
deterministic lifecycle and safe-idle boundaries established here.
