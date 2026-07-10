# AURA Roadmap 181-190 — Local Interaction Runtime Activation

Status: ACTIVE — SPRINT 181 COMPLETE
Current anchor: v0.181.0-genesis
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

Add a deterministic service state machine and lifecycle controls for:

- starting;
- running;
- stopping;
- stopped;
- failed;
- port conflict handling;
- startup rollback;
- clean signal handling;
- single-listener enforcement.

Systemd and automatic startup remain disabled until later evaluation.

### Sprint 183 — Health and Status API Runtime

Expose read-only runtime data for:

- identity and version;
- core boot health;
- plugin health;
- capability summary;
- service state and uptime;
- memory availability;
- runtime safety boundary;
- current errors and degraded state.

### Sprint 184 — Control Center Backend Runtime

Connect existing Control Center contracts to real read-only APIs for:

- overview status;
- service monitor;
- capability viewer;
- plugin viewer;
- permission state;
- audit state;
- memory status;
- runtime readiness.

### Sprint 185 — Control Center Web Shell

Deliver the first usable browser dashboard with:

- overview page;
- service status;
- capability viewer;
- plugin viewer;
- memory status;
- permission panel in read-only mode;
- action/audit log visibility;
- responsive local UI;
- clear safe-idle and degraded-state indicators.

### Sprint 186 — Browser Chat Session Runtime

Activate browser-to-AURA chat sessions with:

- session creation;
- validated message submission;
- response delivery;
- local history persistence;
- session reload;
- explicit clear-session confirmation;
- input size and schema limits;
- no tool or action execution.

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
