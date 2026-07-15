# AURA Resource Baseline Metrics

Version: `v1.0.6-genesis`
Sprint: `246`
Boundary: `resource_baseline_metrics`
Next sprint: `247`
Next boundary: `atlas_resource_monitoring`

## Purpose

Sprint 246 establishes a deterministic, read-only, single-snapshot baseline
for ATLAS resource visibility.

## Commands

- `resource-baseline-status`
- `resource-baseline-context`
- `resource-baseline-check`
- `resource-baseline-snapshot`

All commands return pure JSON and do not fall through to normal AURA boot.

## Metrics

The snapshot reports:

- CPU usage sampled from `/proc/stat`;
- logical CPU count and CPU model;
- one-, five-, and fifteen-minute load averages;
- total, used, and available memory;
- total, used, and free swap;
- uptime;
- process count;
- filesystem total, used, available, and raw-free bytes;
- inode total, used, available, and raw-free counts.

Filesystem visibility covers `/`, `/home`, `/mnt/aura-data`, and the AURA
project root.

## Dependency Boundary

The implementation uses Python's standard library and Linux read-only sources:

- `/proc/stat`;
- `/proc/cpuinfo`;
- `/proc/meminfo`;
- `/proc/uptime`;
- `/proc`;
- `os.getloadavg`;
- `os.statvfs`.

`psutil` is not required or installed by this sprint.

## Runtime Boundary

Sprint 246 keeps the following disabled:

- background sampling;
- rolling-window history;
- metrics persistence;
- dashboard activation;
- socket binding;
- systemd mutation;
- network access;
- process control;
- threshold mutation.

## Canonical Validation

- Base checks: `50`
- Assertions: `50`
- Failed assertions: `0`
- Metric groups: `7`
- Filesystem records: `4`
- Contract mode: `read_only_snapshot`
- Snapshot mode: `single_read_only`

## Next Boundary

Sprint 247 continues with `atlas_resource_monitoring`.
