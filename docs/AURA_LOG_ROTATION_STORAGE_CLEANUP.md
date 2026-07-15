# AURA Log Rotation and Storage Cleanup

Version: `v1.0.5-genesis`
Sprint: `245`
Boundary: `log_rotation_storage_cleanup`
Next sprint: `246`
Next boundary: `resource_baseline_metrics`

## Purpose

Sprint 245 makes AURA's existing log rotation and retention behavior visible,
deterministic, and reviewable without enabling destructive cleanup.

The canonical Loguru sink writes to `logs/aura.log`, rotates at `1 MB`, retains
rotated logs for `7 days`, and does not currently enable compression.

## Commands

- `log-rotation-storage-status`
- `log-rotation-storage-context`
- `log-rotation-storage-check`
- `log-rotation-storage-cleanup-preview`

All commands return pure JSON without falling through to normal boot or
appending to the active log.

## Cleanup Safety Boundary

- `logs/aura.log` is always protected.
- Only recognized rotated AURA log names can become retention candidates.
- Rotated logs within seven days remain retained.
- Symlinks are never followed.
- Directory escape is blocked.
- Temporary-like names require explicit review.
- Session, conversation, memory, journal, audit, and arbitrary project files
  are excluded.
- Cleanup execution, deletion, move, truncation, compression, and archive
  remain disabled.

## Storage Visibility

The context packet reports total, used, free, used percentage, and free
percentage for `/`, `/home`, `/mnt/aura-data`, and the project root.

This sprint does not create quotas, reserve disk space, remount storage,
change permissions, mutate systemd, start services, bind sockets, or access
the network.

## Canonical Validation

- Base checks: `40`
- Assertions: `40`
- Failed assertions: `0`
- Cleanup execution enabled: `false`
- Canonical deletion performed: `false`
- CLI log writes: `0`
- Persistence data mutation: `0`
- Runtime activation: `0`

## Next Boundary

Sprint 246 continues with `resource_baseline_metrics`.
