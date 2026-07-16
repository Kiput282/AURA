# AURA Local Model Bridge Runtime

Version: v0.187.0-genesis
Sprint: 187 — Local Model Bridge Activation
Status: COMPLETED — PERMISSION-GATED LOCAL ALPHA RUNTIME

## Purpose

Sprint 187 connects AURA's bounded browser chat sessions to an explicitly
configured local text model without activating tools, actions, commands,
desktop control, arbitrary file access, internet fallback, or AURA long-term
memory writes.

## Provider Contracts

Supported local provider contracts:

- Ollama:
  - default base URL `http://127.0.0.1:11434`;
  - probe `GET /api/tags`;
  - inference `POST /api/chat`.
- OpenAI-compatible:
  - default base URL `http://127.0.0.1:8080`;
  - probe `GET /v1/models`;
  - inference `POST /v1/chat/completions`.

Only `localhost`, `127.0.0.1`, and `::1` are accepted. A port is mandatory.
Resolved addresses must remain loopback and redirects are rejected.

## Runtime Configuration

Configuration is environment-only and non-persistent:

- `AURA_LOCAL_MODEL_PROVIDER`;
- `AURA_LOCAL_MODEL_BASE_URL`;
- `AURA_LOCAL_MODEL_NAME`;
- `AURA_LOCAL_MODEL_ENABLED`;
- `AURA_LOCAL_MODEL_TIMEOUT_SECONDS`;
- `AURA_LOCAL_MODEL_MAX_OUTPUT_TOKENS`;
- `AURA_LOCAL_MODEL_TEMPERATURE`.

The provider remains disabled by default.

## Browser Chat Integration

Runtime contracts:

- `GET /api/model/status`;
- `POST /api/model/probe`;
- `POST /api/chat/sessions/{session_id}/model-messages`.

The Sprint 186 placeholder route remains available.

A model request requires:

- a valid session;
- a valid `client_message_id`;
- the expected session revision;
- a safe `modelreq_...` request identifier;
- `confirm_model_request: true`.

A successful response is persisted as `local_model_response`. Duplicate
client-message retries return the stored pair and never invoke the provider
again. A provider or response failure performs no session write.

## Safety Boundary

Enabled:

- loopback-only provider profiles;
- resolved-loopback checks;
- redirect rejection;
- explicit provider probe;
- explicit text-model inference;
- bounded request and response validation;
- model-response persistence;
- restart-safe local session history.

Disabled:

- model downloads;
- remote model providers;
- provider credentials;
- internet fallback;
- streaming;
- tool and function schemas;
- tool calls;
- command or action dispatch;
- arbitrary file access;
- desktop control;
- AURA long-term memory writes;
- background/systemd/auto-start runtime;
- public or LAN listener;
- autonomous actions.

## Validation

- bridge core self-test: 150/150;
- profile resolver self-test: 28/28;
- combined bridge CLI self-test: 178/178;
- Sprint 186 session core: 152/152;
- Sprint 186 chat web: 85/85;
- live model HTTP route: passed;
- idempotent retry without reinvocation: passed;
- provider failure without session write: passed;
- restart persistence: passed;
- SIGTERM and SIGINT shutdown: passed;
- canonical identity/settings/memory and chat data: unchanged during runtime
  tests;
- port `8765`: closed after tests.

## Next Sprint

Sprint 188 — Interactive Control Center Chat.

## Sprint 257 health handoff

Sprint 257 keeps `AuraLocalModelBridgeRuntimeManager` as the canonical provider
owner and adds read-only host discovery plus a default-off, exact-confirmation
loopback health check. The bridge's existing generation and browser-chat
permission boundaries remain unchanged.

Next boundary: `local_model_router_activation`.
