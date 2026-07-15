# AURA Backup and Restore Rehearsal

Version: `v1.1.0`
Sprint: `250`
Boundary: `backup_restore_rehearsal`
Block: `Sprint 241–250 — Genesis Stabilization & Runtime Hardening`
Next sprint: `251`
Next title: `AURA Launcher and Service Controls`
Next boundary: `aura_launcher_service_controls`
Next version: `v1.1.1`
Next block: `Sprint 251–260 — Active Local Runtime & Model Service Integration`
Next block target: `v1.2.0`

## Purpose

Sprint 250 closes the Genesis Stabilization and Runtime Hardening block with a
deterministic, read-only rehearsal of AURA's backup, restore, integrity,
recovery, safe-idle, and release-acceptance contracts.

## Commands

- `backup-restore-rehearsal-status`
- `backup-restore-rehearsal-context`
- `backup-restore-rehearsal-check`
- `backup-restore-rehearsal-review`

All commands return pure JSON and do not fall through to normal AURA boot.

## Review Dimensions

The contract reviews:

- backup scope inventory;
- manifest and digest integrity;
- restore-plan reversibility;
- permission and approval boundaries;
- audit and provenance linkage;
- safe-idle failure verification;
- contract deduplication;
- block release acceptance.

## Canonical Result

- Base checks: `96`
- Assertions: `96`
- Failed assertions: `0`
- Review dimensions: `8`
- Secure dimensions: `8`
- Review dimensions requiring follow-up: `0`
- Warning dimensions: `0`
- Unavailable dimensions: `0`
- Sprint 249 anchor: `96/96`
- Genesis Final release anchor: `1258/1258`
- Active permission runtime anchor: `3115/3115`

## Source and Data Boundary

The rehearsal reads selected Python source files, their abstract syntax trees,
and metadata describing canonical path topology.

It does not read canonical data contents, backup-store contents, restore-source
contents, permission-store contents, audit-store contents, or recovery-store
contents.

## Runtime Boundary

Sprint 250 keeps the following disabled:

- backup creation and backup writes;
- archive creation;
- manifest writes;
- restore execution and restore writes;
- file replacement and deletion;
- permission mutation;
- audit writing;
- recovery and rollback execution;
- process control;
- service activation;
- network access;
- socket activation;
- systemd mutation;
- command execution.

## Block Closure

Sprint 250 completes the Sprint 241–250 **Genesis Stabilization & Runtime
Hardening** block at milestone `v1.1.0`.

The completed sequence includes configuration integrity, persistence checks,
storage/log review, resource baseline and monitoring, localhost/SSH security,
permission expiry and recovery review, backup/restore rehearsal, contract
deduplication review, and safe-idle failure verification.

## Sprint 251 Handoff

Sprint 251 begins the Active Local Runtime & Model Service Integration block
with **AURA Launcher and Service Controls** at the
`aura_launcher_service_controls` boundary, targeting `v1.1.1`.

Sprint 251 remains contract-only unless separately authorized to perform
service start, stop, restart, autostart, systemd, socket, network, or log
mutation.
