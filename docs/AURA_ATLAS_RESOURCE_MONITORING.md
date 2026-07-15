# AURA ATLAS Resource Monitoring

Version: `v1.0.7-genesis`
Sprint: `247`
Boundary: `atlas_resource_monitoring`
Next sprint: `248`
Next boundary: `localhost_ssh_tunnel_security_review`

## Purpose

Sprint 247 converts the Sprint 246 resource baseline snapshot into a
deterministic, read-only ATLAS health-classification packet.

## Commands

- `atlas-resource-monitor-status`
- `atlas-resource-monitor-context`
- `atlas-resource-monitor-check`
- `atlas-resource-monitor-snapshot`

All commands return pure JSON and do not fall through to normal AURA boot.

## Health States

Every monitored dimension uses one of four states:

- `healthy`
- `warning`
- `critical`
- `unavailable`

The overall state is the worst state among all monitored dimensions.

## Health Dimensions

The monitor classifies:

- CPU usage;
- one-minute load normalized by logical CPU count;
- memory use;
- swap use;
- storage capacity;
- inode capacity;
- uptime;
- process count.

Storage covers `/`, `/home`, `/mnt/aura-data`, and the AURA project root.

## Threshold Policy

The threshold policy is read-only.

- CPU: warning at 75%, critical at 90%.
- Normalized one-minute load: warning at 75%, critical at 100%.
- Memory: warning at 75%, critical at 90%.
- Swap: warning at 25%, critical at 75%.
- Filesystem use: warning at 80%, critical at 90%.
- Filesystem available space: warning at or below 20 GiB, critical at or
  below 10 GiB.
- Inodes: warning at 80%, critical at 90%.
- Process count: warning at 1024, critical at 2048.

## Source Contract

Sprint 247 consumes the Sprint 246
`AuraResourceBaselineMetricsPlanner` snapshot.

Required source properties:

- source version `1.0.6-genesis`;
- source assertions `50`;
- source failed assertions `0`;
- source metric groups `7`;
- source filesystem records `4`.

## Runtime Boundary

Sprint 247 keeps the following disabled:

- background sampling;
- rolling history;
- metrics persistence;
- dashboard activation;
- alert delivery;
- socket binding;
- systemd mutation;
- network access;
- process control;
- command execution;
- threshold mutation.

Pressure metrics and temperature classification remain deferred.

## Canonical Validation

- Base checks: `60`
- Assertions: `60`
- Failed assertions: `0`
- Health dimensions: `8`
- Contract mode: `read_only_health_snapshot`
- Snapshot mode: `single_read_only`

## Next Boundary

Sprint 248 continues with `localhost_ssh_tunnel_security_review`.
