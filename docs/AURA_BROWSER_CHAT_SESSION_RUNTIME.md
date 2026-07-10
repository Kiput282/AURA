# AURA Browser Chat Session Runtime

Version: v0.186.0-genesis
Sprint: 186 — Browser Chat Session Runtime
Status: COMPLETED — PERMISSION-GATED LOCAL ALPHA RUNTIME

## Purpose

Sprint 186 activates AURA's first browser-to-local-session interaction path
without activating local model inference. Users can create local sessions,
submit bounded messages, reload persistent history, and clear a session after
an exact confirmation phrase.

The runtime delivers an honest placeholder response until Sprint 187 rather
than pretending that a model generated an answer.

## Browser Surface

```text
http://127.0.0.1:8765/chat
```

Local assets:

```text
/chat
/assets/control-center-chat.css
/assets/control-center-chat.js
```

The Control Center dashboard links to the local chat page. Full chat
integration inside Control Center panels remains assigned to Sprint 188.

## Chat Route Contracts

```text
GET  /api/chat/status
GET  /api/chat/sessions
POST /api/chat/sessions
GET  /api/chat/sessions/{session_id}
POST /api/chat/sessions/{session_id}/messages
POST /api/chat/sessions/{session_id}/clear
```

Total local interaction route contracts: 27.

## Session Persistence

Each session is stored as a bounded local JSON document under:

```text
data/chat_sessions/
```

The directory is ignored by Git so private transcripts are not included in
normal repository commits.

Persistence protections include:

- one file per validated `chat_<32 lowercase hex>` session id;
- atomic temporary-file replacement;
- file mode `0600`;
- SHA-256 integrity field;
- maximum 500 messages per session;
- maximum 2 MiB serialized session file;
- contiguous message sequence validation;
- corruption detection and degraded-state reporting;
- optimistic revision checks;
- idempotent retry through `client_message_id`.

AURA long-term memory is not written by this runtime.

## Mutation Guard

Chat POST requests require:

```text
Content-Type: application/json
X-AURA-Local-Intent: browser-chat-session
Origin: http://127.0.0.1:8765
```

The listener also accepts the equivalent localhost origin. Unknown fields,
invalid schemas, oversized bodies, invalid revisions, invalid ids, and
non-local origins fail closed.

Clear-session mutation requires the exact phrase:

```text
CLEAR <session_id>
```

## Response Boundary

Until Sprint 187, every accepted user message receives a deterministic runtime
notice stating that the message was saved locally and that the Local Model
Bridge is unavailable.

No model request, network fallback, tool execution, command execution, action
dispatch, arbitrary-file operation, desktop control, or autonomous behavior
occurs.

## Validation Evidence

- session core self-test: 152/152;
- browser chat web self-test: 85/85;
- live chat HTTP assertions: 82/82;
- chat asset GET/HEAD: 3/3 plus 3/3;
- session create: HTTP 201;
- list, detail, submit, reload, and clear: verified;
- stale-revision idempotent retry: verified;
- new-message revision conflict: HTTP 409;
- wrong clear confirmation: rejected;
- JSON content type, local intent, and same-origin guards: enforced;
- canonical identity, settings, AURA memory, and chat-session data unchanged
  during isolated validation;
- clean SIGTERM and SIGINT shutdown;
- port `8765` closed after shutdown;
- Sprint 185 shell regression: 140/140;
- Sprint 184 backend regression: 108/108;
- Sprint 183 status regression: 59/59;
- Sprint 182 lifecycle regression: 41/41;
- Sprint 181 web regression: 21/21;
- normal AURA boot: READY.

## Runtime Accounting

Capability summary after activation:

- total: 117;
- online: 115;
- permission-gated: 9;
- runtime execution features: 1.

The runtime feature count remains `1` because Sprint 186 reuses the existing
foreground localhost listener and does not introduce a command, tool, action,
model, desktop, or autonomous executor.

## Still Disabled

- Local Model Bridge and model inference;
- automatic network fallback;
- AURA long-term memory writes;
- tools, commands, actions, and arbitrary-file operations;
- service and plugin controls;
- permission grant or scope mutation;
- audit writer;
- background daemon, systemd, and automatic startup;
- public/LAN/wildcard binding;
- browser auto-launch;
- voice, vision, desktop control, and autonomy.

## Next Sprint

Sprint 187 — Local Model Bridge Activation
