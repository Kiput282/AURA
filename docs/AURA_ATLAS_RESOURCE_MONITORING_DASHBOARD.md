# AURA ATLAS Resource Monitoring Dashboard

## Sprint 267 checkpoint

- Version: `v1.2.7`
- Boundary: `atlas_resource_monitoring_dashboard`
- Next sprint: Sprint 268
- Next boundary: `permission_audit_action_visibility_ux`

Sprint 267 adds a read-only ATLAS resource dashboard to the existing
local Control Center. It reuses the existing `/api/control-center`
payload and does not add a new HTTP route.

## Runtime metrics

The dashboard displays:

- CPU usage with current, minimum, average, and maximum values.
- RAM usage with current, minimum, average, and maximum values.
- Native SVG rolling charts for CPU and RAM.
- Rolling windows of 5, 15, and 60 minutes.
- Swap usage, uptime, and process count.
- Storage used, free, total, percentage, and health state for `/`,
  `/home`, and `/mnt/aura-data`.

Samples are collected on dashboard reads at a minimum one-second
interval. The rolling history remains in-process and is not persisted.

## Safety boundary

The dashboard is read-only. It adds no process control, command
execution, service action, systemd mutation, threshold mutation,
network fallback, background sampler, history persistence, external
dependency, or new execution authority.

The runtime remains localhost-oriented and safe-idle.

## Validation target

The Sprint 267 contract contains 504 assertions across 42 dimensions.
It validates the resource runtime, live payload, Control Center
integration, responsive resource UI, registry, CLI, version and
documentation metadata, Sprint 266 historical anchor, and safety
boundary.
