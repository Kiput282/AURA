# AURA Local Model Router Activation

- Version: `v1.1.8`
- Sprint: `258`
- Boundary: `local_model_router_activation`
- Contract: `288/288`
- Secure dimensions: `24`
- Canonical route owner: `ModelRouter`
- Bridge owner: `AuraLocalModelBridgeRuntimeManager`
- Health dependency: `local_model_service_discovery_health`

## Purpose

Sprint 258 activates bounded route selection between AURA task targets and the
existing local model bridge. It does not introduce a second route registry or a
second model client.

## Activation rules

Execution requires all of the following:

- an exact known route after alias normalization;
- no fallback execution;
- route status `online`;
- route provider and model matching the validated reasoning configuration;
- a loopback-only provider profile;
- explicit provider-health verification;
- explicit model-request permission;
- exact token `ROUTE_LOCAL_MODEL_REQUEST`;
- bridge-compatible bounded message and request schemas.

At the current checkpoint, the `companion` route is the only configured local
route eligible for execution. Foundation, internal, and planned routes remain
non-executable through this boundary.

## Disabled boundaries

- no automatic route execution;
- no persisted route choice;
- no real runtime switching;
- no service start, stop, restart, installation, or enablement;
- no model download, pull, load, or unload;
- no request queue;
- no resource-budget mutation;
- no non-loopback networking;
- no credentials;
- no systemd or autostart mutation.

Next boundary: `model_loading_unloading_queue_resource_budgets`.
