# AURA Roadmap 181-190 — Local Interaction Runtime Activation

Status: ACTIVE — SPRINT 186 COMPLETE
Current anchor: v0.189.0-genesis
Target checkpoint: v0.190.0-genesis

## Purpose

This block converts the service, Control Center, local chat, and memory foundations from Sprint 141-180 into AURA's first usable local interaction runtime.

The activation order is intentionally conservative:

1. localhost-only service runtime,
2. health and status surfaces,
3. read-only Control Center,
4. browser chat sessions,
5. local model bridge,
6. permission, audit, and recovery visibility,
7. stabilization.

Voice is not cancelled. It moves to Sprint 191-200 so it can reuse a stable service, dashboard, chat session, model, permission, and audit path.

## Block Guardrails

Throughout Sprint 181-190:

- bind only to `127.0.0.1`;
- start manually and remain foreground-first until lifecycle safety is verified;
- use `safe_idle` as the default state;
- fail closed when configuration, binding, model, or session initialization fails;
- do not expose a LAN or public listener;
- do not enable arbitrary shell, tool, file, desktop, voice, or vision execution;
- do not permit autonomous action dispatch;
- do not bypass permission, audit, or review boundaries;
- keep chat and dashboard behavior local-first and transparent.

## Sprint Plan

## Sprint 181 — Local Web Runtime Activation Cutline

Status: completed in v0.181.0-genesis.

Delivered:

- real foreground HTTP listener;
- fail-closed `127.0.0.1:8765` binding;
- `safe_idle` default;
- explicit `--confirm-localhost` requirement;
- read-only `/`, `/health`, and `/api/status`;
- mutation methods blocked with `405`;
- CLI status, self-test, and start commands;
- clean `SIGINT` shutdown and port release;
- one registered runtime execution feature.

Still disabled:

- public/LAN/wildcard binding;
- automatic or background service start;
- chat and model runtime;
- memory writes and permission mutation;
- audit persistence;
- commands, tools, actions, arbitrary files, desktop, voice, vision, and
  autonomy.

Next: Sprint 182 — Service Lifecycle Runtime.
### Sprint 182 — Service Lifecycle Runtime

Status: completed in v0.182.0-genesis.

Delivered:

- deterministic `stopped`, `starting`, `running`, `stopping`, and `failed`
  states;
- validated transition contract;
- foreground-only lifecycle ownership;
- explicit confirmation requirement;
- same-process single-listener enforcement;
- port-conflict fail-closed behavior;
- startup error visibility and rollback to `stopped`;
- clean programmatic stop;
- clean `SIGINT` and `SIGTERM` shutdown;
- bounded in-memory transition history;
- CLI status, self-test, and start commands;
- 41/41 lifecycle assertions.

Runtime feature accounting remains `1` because Sprint 182 controls the existing
Sprint 181 localhost listener rather than introducing another executor.

Still disabled:

- systemd and background daemon runtime;
- automatic startup;
- persistent PID or lifecycle state;
- remote or HTTP lifecycle mutation;
- public/LAN/wildcard binding;
- chat, model, memory-write, permission-mutation, audit-write, command, tool,
  action, file, desktop, voice, vision, and autonomy runtime.

Next: Sprint 183 — Health and Status API Runtime.
### Sprint 183 — Health and Status API Runtime

Status: completed in v0.183.0-genesis.

Delivered:

- side-effect-free health and status aggregator;
- nine read-only payload routes;
- identity and version status;
- boot prerequisite health without executing normal boot;
- plugin availability without starting plugins;
- capability summary;
- live lifecycle state and uptime;
- read-only memory availability and record validation;
- consolidated safety boundary;
- transparent errors and degraded-state reporting;
- GET and HEAD support;
- mutation methods rejected with 405;
- localhost Host-header allowlist;
- no CORS;
- defensive no-store and browser security headers;
- 59/59 aggregator assertions;
- 116/116 live HTTP assertions.

Runtime feature accounting remains `1` because Sprint 183 uses the same
localhost listener introduced in Sprint 181.

Still disabled:

- mutation routes and remote lifecycle control;
- plugin start and memory writes from status probes;
- background daemon, systemd, automatic startup, and persistence;
- public/LAN/wildcard binding;
- chat, model, permission mutation, command, tool, action, file, desktop,
  voice, vision, and autonomy runtime.

Next: Sprint 184 — Control Center Backend Runtime.
### Sprint 184 — Control Center Backend Runtime

Status: completed in v0.184.0-genesis.

Delivered:

- read-only Control Center backend view-model core;
- nine backend JSON routes;
- eight panel contracts for overview, service, capabilities, plugins,
  permissions, audit, memory, and readiness;
- eight older foundation contracts connected through read-only status probes;
- live lifecycle-aware overview and service data;
- all capability cards and summaries;
- plugin visibility without plugin activation;
- declared permission visibility without request decisions;
- audit visibility without writer or persistence;
- memory visibility without writes;
- GET and HEAD support across all backend routes;
- mutation methods rejected with 405;
- localhost Host-header allowlist;
- CORS disabled;
- defensive no-store and browser security headers;
- 108/108 backend assertions;
- 210/210 live HTTP assertions.

Runtime feature accounting remains `1` because Sprint 184 uses the same
localhost listener introduced in Sprint 181.

Still disabled:

- Control Center web shell and frontend assets;
- browser auto-launch;
- service and plugin controls;
- permission request decision, grant, deny, and scope mutation;
- audit writer and persistence;
- memory mutation;
- background daemon, systemd, automatic startup, and persistence;
- public/LAN/wildcard binding;
- chat, model, command, tool, action, file, desktop, voice, vision, and
  autonomy runtime.

Next: Sprint 185 — Control Center Web Shell.
### Sprint 185 — Control Center Web Shell

Status: completed in v0.185.0-genesis.

Delivered:

- first usable localhost browser dashboard;
- three local static asset routes;
- eight read-only panels for overview, service, capabilities, plugins,
  permissions, audit, memory, and readiness;
- live read-only connection to `/api/control-center`;
- responsive desktop, tablet, and mobile layouts;
- keyboard focus, skip-link, live-region, and reduced-motion accessibility;
- safe-idle and degraded-state indicators;
- manual and five-second visible-tab read refresh;
- local capability filtering;
- safe DOM rendering without `innerHTML` or `eval`;
- no CDN, external fonts, frontend packages, or external runtime dependency;
- self-only Content Security Policy;
- browser permission restrictions;
- Host-header allowlist;
- path traversal and unknown asset blocking;
- mutation methods rejected with 405;
- browser auto-launch disabled;
- 140/140 shell assertions;
- 232/232 live HTTP assertions.

Runtime feature accounting remains `1` because Sprint 185 uses the same
localhost listener introduced in Sprint 181.

Still disabled:

- browser chat sessions and message submission;
- local model request/response runtime;
- service and plugin controls;
- permission decisions, grants, denials, and scope mutation;
- audit writer and persistence;
- memory mutation;
- background daemon, systemd, automatic startup, and persistence;
- public/LAN/wildcard binding;
- command, tool, action, arbitrary-file, desktop, voice, vision, and
  autonomy runtime.

Next: Sprint 186 — Browser Chat Session Runtime.
### Sprint 186 — Browser Chat Session Runtime

Status: completed in v0.186.0-genesis.

Delivered:

- localhost browser chat page at `/chat`;
- three local chat assets;
- six bounded chat route contracts;
- session creation and metadata listing;
- validated message submission;
- deterministic honest placeholder response delivery;
- atomic local history persistence;
- session reload;
- exact clear-session confirmation;
- 8,192-character and 32,768-byte message limits;
- maximum 500 messages per session;
- optimistic revision conflict protection;
- stale-revision idempotent replay through `client_message_id`;
- SHA-256 session integrity verification;
- degraded-state reporting for corrupt session files;
- `0600` local session files;
- JSON content-type, local-intent, and same-origin mutation guards;
- Control Center link to Local Chat;
- private chat-session directory excluded from Git;
- 152/152 session core assertions;
- 85/85 browser chat web assertions;
- 82/82 live chat HTTP assertions;
- clean SIGTERM and SIGINT shutdown.

Runtime feature accounting remains `1` because Sprint 186 reuses the existing
localhost listener and does not activate a model, command, tool, action,
desktop, or autonomous executor.

Still disabled:

- Local Model Bridge and model inference;
- network fallback;
- AURA long-term memory writes;
- broad permission mutation;
- audit writer;
- tools, commands, actions, arbitrary files, and desktop control;
- background daemon, systemd, automatic startup, and persistence;
- public/LAN/wildcard binding;
- browser auto-launch;
- voice, vision, and autonomy.

Next: Sprint 187 — Local Model Bridge Activation.
### Sprint 187 — Local Model Bridge Activation

Connect chat sessions to the configured local model provider, initially through the existing Ollama boundary, while preserving:

- honest provider/model availability errors;
- timeouts and cancellation;
- session integrity after provider failure;
- safety and uncertainty handoff;
- persona and context handoff;
- no automatic network fallback;
- no tool execution.

### Sprint 188 — Interactive Control Center Chat

Integrate chat into the Control Center with:

- message history;
- input and send controls;
- thinking/loading state;
- model availability state;
- session selection;
- error and retry state;
- memory-use indicator;
- clear separation between conversation and action proposals.

### Sprint 189 — Permission, Audit, and Recovery Visibility

Make existing safety foundations visible without yet enabling broad actions:

- pending permission state;
- accepted and rejected decisions;
- runtime audit events;
- service/model/session errors;
- recovery state;
- emergency-stop state;
- blocked-action explanations.

### Sprint 190 — Local Interaction Runtime Review and Stabilization

Close the block only when:

- dashboard startup is repeatable;
- browser chat works end to end;
- local model responses are stable;
- session history survives restart without corruption;
- the listener remains localhost-only;
- shutdown is clean;
- port conflicts fail closed;
- errors are visible;
- no permission bypass exists;
- no arbitrary execution exists;
- runtime and documentation boundaries agree.

## Block Completion Definition

At v0.190.0-genesis, AURA should have her first usable local body:

- a local service;
- a Control Center dashboard;
- interactive browser chat;
- local model connection;
- persistent sessions;
- visible safety and recovery state.

This checkpoint does not yet require microphone capture, TTS, screen capture, local action execution, ORION, avatar rendering, or autonomous behavior.

## Sprint 187 Completion Checkpoint

Status: completed in v0.187.0-genesis.

Delivered:

- loopback-only Ollama and OpenAI-compatible provider contracts;
- environment-only provider profiles;
- explicit probe and inference confirmation;
- bounded text-only inference;
- resolved-loopback enforcement and redirect rejection;
- browser-chat model message route;
- persistent `local_model_response` pairs;
- duplicate retries without model reinvocation;
- provider failures without partial session writes;
- seven chat routes, two model routes, and thirty total route contracts.

Next: Sprint 188 — Interactive Control Center Chat.

## Sprint 188 Completion Checkpoint

Status: completed in v0.188.0-genesis.

Delivered:

- responsive interactive Control Center chat;
- provider and model status visibility;
- save-only safe default;
- explicit provider probe confirmation;
- explicit per-message model confirmation;
- stable in-memory retry identifiers;
- visible model and placeholder response kinds;
- idempotent retry without duplicate model invocation;
- revision-conflict recovery;
- restart persistence;
- confirmed session clearing;
- no external browser dependencies or browser storage.

Next: Sprint 189 — Permission, Audit, and Recovery Visibility.

## Sprint 189 Completion Checkpoint

Status: completed in v0.189.0-genesis.

Delivered:

- read-only permission requirement visibility;
- read-only audit-event contract visibility;
- read-only manual recovery guidance;
- responsive `/visibility` Control Center page;
- four GET/HEAD visibility APIs;
- three local assets;
- provider-state redaction;
- no message or model-response recording;
- mutation methods blocked;
- interactive chat preserved;
- seven additional local route contracts.

Next: Sprint 190 — Review and Stabilization 181-190.
