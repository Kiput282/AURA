# AURA Permission Expiry and Recovery Review

Version: `v1.0.9-genesis`
Sprint: `249`
Boundary: `permission_expiry_recovery_review`
Next sprint: `250`
Next title: `Backup and Restore Rehearsal`
Next boundary: `backup_restore_rehearsal`
Next milestone: `v1.1.0`

## Purpose

Sprint 249 provides a deterministic, read-only review of AURA's permission
expiry and recovery contracts before the Genesis Stabilization and Runtime
Hardening block closes at Sprint 250.

## Commands

- `permission-expiry-recovery-status`
- `permission-expiry-recovery-context`
- `permission-expiry-recovery-check`
- `permission-expiry-recovery-review`

All commands return pure JSON and do not fall through to normal AURA boot.

## Review Dimensions

The contract reviews:

- grant lifecycle;
- expiry enforcement;
- stale-grant rejection;
- denial lifecycle;
- revocation visibility;
- recovery visibility;
- rollback and emergency-stop linkage;
- audit linkage.

## Canonical Result

- Base checks: `96`
- Assertions: `96`
- Failed assertions: `0`
- Review dimensions: `8`
- Secure dimensions: `8`
- Review dimensions requiring follow-up: `0`
- Warning dimensions: `0`
- Unavailable dimensions: `0`
- Active permission runtime anchor: `3115/3115`

## Source Boundary

The review reads only:

- selected permission-related Python source files;
- their abstract syntax trees;
- filesystem metadata for optional permission, audit, and recovery paths.

The permission runtime is neither imported nor executed. Permission, audit,
and recovery store contents are not read.

## Runtime Boundary

Sprint 249 keeps the following disabled:

- permission-store mutation;
- grant creation or application;
- grant revocation;
- expiry application;
- denial creation or application;
- recovery execution;
- rollback execution;
- emergency-stop execution;
- audit writing;
- file writing;
- network access;
- process control;
- service activation;
- socket activation;
- systemd mutation;
- command execution.

## Sprint 250 Handoff

Sprint 250 is canonically resolved as **Backup and Restore Rehearsal** at the
`backup_restore_rehearsal` boundary, targeting milestone `v1.1.0`.

Sprint 250 must remain rehearsal-only unless a separate explicit authorization
later permits mutative backup or restore behavior.
