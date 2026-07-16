# AURA Model Loading, Unloading, Queue, and Resource Budgets

- Version: `v1.1.9`
- Sprint: `259`
- Boundary: `model_loading_unloading_queue_resource_budgets`
- Contract: `312/312`
- Secure dimensions: `26`
- Queue: depth `4`, max in-flight `1`, timeout `120` seconds
- Memory reserve ratio: `0.20`
- Next boundary: `active_local_runtime_integration_stabilization`

Lifecycle work is default-off and requires explicit permission, verified
provider health, and an approved read-only resource budget. Load uses
provider-managed keep-alive semantics; release uses explicit provider release.
No download, pull, persistent queue, background worker, threshold mutation,
service control, systemd, or autostart mutation is enabled.

## Sprint 260 end-to-end integration

Lifecycle, bounded queueing, and read-only budgets are coordinated with service, chat, health, routing, persistence, and stop-and-restore.
