# AURA Control Center Runtime UX Consolidation

## Sprint 266 checkpoint

- Version: `v1.2.6`
- Boundary: `control_center_runtime_ux_consolidation`
- Next sprint: Sprint 267
- Next boundary: `atlas_resource_monitoring_dashboard`

Sprint 266 consolidates existing operational visibility into the local
Control Center. The existing Control Center web shell remains the
operational home, while `/chat` remains the dedicated browser-chat
workspace and `/visibility` remains the permission, audit, and recovery
visibility workspace.

## Consolidated surfaces

The Operations panel presents six read-only cards:

1. Service status.
2. Bounded logs and failure metadata.
3. Model queue and resource-budget visibility.
4. Permission, audit, and recovery visibility.
5. A link to the full chat workspace.
6. Review-first memory summary and workspace link.

The backend reuses the existing `/api/control-center` and
`/api/control-center/service` routes. No new HTTP action route is added.

## Safety boundary

Sprint 266 does not add execution authority. It does not add service
start, stop, or restart routes; arbitrary log-file reads; raw log
content; implicit model activation; permission grants; recovery
execution; durable memory writes; automatic service start; automatic
model activation; automatic permission changes; automatic recovery; or
network fallback.

The runtime remains localhost-oriented, operator-controlled, and
safe-idle.

## Validation target

The Sprint 266 contract contains 480 assertions across 40 dimensions.
It verifies the runtime aggregator, backend payload enrichment, web
surface, registry, CLI, version metadata, documentation, Sprint 265
historical anchor, and the complete safety boundary.

Sprint 267 continues with `atlas_resource_monitoring_dashboard`.
