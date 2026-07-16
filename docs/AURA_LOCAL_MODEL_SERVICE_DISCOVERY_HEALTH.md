# AURA Local Model Service Discovery and Health

- Version: `v1.1.7`
- Sprint: `257`
- Boundary: `local_model_service_discovery_health`
- Contract: `264/264`
- Secure dimensions: `22`
- Canonical owner: `AuraLocalModelBridgeRuntimeManager`
- Default provider: `ollama`
- Default endpoint: `http://127.0.0.1:11434`

## Purpose

Sprint 257 discovers local model service posture without activating or mutating
the provider. It adds an explicitly confirmed loopback-only health boundary on
top of the existing Sprint 187 local model bridge.

## Read-only discovery

The status surface may inspect:

- Ollama binary path and regular-file metadata;
- `ollama.service` load, enable, active, sub-state, main PID, and fragment path;
- main-process UID and command name without exposing its full command line;
- `/proc/net/tcp*` listener metadata for port `11434`;
- AURA local-model environment-key presence and validated profile posture;
- provider contracts and safe endpoint rules.

## Health probe

The health probe is disabled by default. It requires the exact token:

`PROBE_LOCAL_MODEL_SERVICE`

The probe is restricted to plain HTTP loopback, rejects redirects and proxies,
uses a two-second timeout, accepts at most one MiB of JSON, and returns only the
count of valid model records. It does not expose model names.

## Disabled boundaries

- no automatic health polling;
- no service start, stop, restart, install, or enable;
- no model download, pull, load, or unload;
- no chat routing or model inference;
- no non-loopback network connection;
- no credential or secret read;
- no systemd or autostart mutation.

Next boundary: `local_model_router_activation`.

## Sprint 258 router handoff

Sprint 258 consumes the provider-health boundary as an explicit prerequisite.
It does not turn health discovery into automatic polling. A route request must
still receive separate model-request permission.

Next boundary: `model_loading_unloading_queue_resource_budgets`.
