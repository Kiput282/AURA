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

## Sprint 259 lifecycle handoff

The router remains exact-route only; Sprint 259 adds explicit lifecycle permission, bounded queueing, and read-only budgets.

## Sprint 260 exact-route integration

The integrated chain permits only the exact `companion` route.

## Next Operational Product Boundary

The verified `companion` route becomes the primary model route for the daily
browser chat product block. Sprint 262 owns operational browser chat handoff
and native process-role classification. This Sprint 261 update does not execute
a model request or open a network connection.

## Browser Chat Operational Handoff

Sprint 262 connects the browser model-message route to the verified
`companion` router as the canonical product handoff. Explicit confirmation is
mandatory for each model request. No model download, network fallback, tools,
actions, commands, or memory writes are enabled.
