# AURA Permission, Audit, and Recovery Visibility Runtime

Version: v0.189.0-genesis
Sprint: 189 — Permission, Audit, and Recovery Visibility
Status: COMPLETED — READ-ONLY LOCAL ALPHA RUNTIME

## Purpose

Sprint 189 makes the permission requirements, audit-event contracts, and
manual recovery guidance of the local interaction runtime visible without
granting new authority to the browser or backend.

## Surface

The localhost listener exposes:

- `/visibility`
- `/assets/permission-audit-recovery.css`
- `/assets/permission-audit-recovery.js`
- `/api/visibility/status`
- `/api/visibility/permissions`
- `/api/visibility/audit`
- `/api/visibility/recovery`

The four API routes support GET and HEAD. Mutation methods are blocked.

## Permission Visibility

Five requirement states are visible:

- explicit localhost service-start confirmation;
- explicit provider-probe confirmation;
- explicit per-message model confirmation;
- exact session-clear phrase;
- permission mutation disabled.

No permission can be created, granted, revoked, or persisted from this
runtime.

## Audit Visibility

Nine event contracts are visible without writing events. Ten field names are
declared redacted, including message content, model-response content,
authorization, API keys, tokens, passwords, provider endpoint values,
environment values, request bodies, and response bodies.

The field names are visible so the operator can understand the redaction
boundary. Their values are never exposed.

## Recovery Visibility

Eight manual recovery cases provide safe operator guidance. The runtime does
not automatically retry, restart services, kill processes, change
permissions, repair files, or execute rollback.

## Safety Boundary

Enabled:

- read-only permission visibility;
- read-only audit-contract visibility;
- read-only recovery guidance;
- one local responsive page;
- four GET/HEAD APIs;
- provider-state redaction;
- safe DOM rendering;
- existing chat and model-status visibility.

Disabled:

- permission mutation or persistence;
- audit writer or persistence;
- automatic recovery, retry, or restart;
- automatic process killing;
- rollback execution;
- model downloads;
- remote providers or internet fallback;
- streaming;
- tools, commands, or action dispatch;
- arbitrary file access;
- desktop control;
- AURA long-term memory writes;
- browser storage;
- WebSocket or EventSource;
- external browser dependencies;
- background/systemd/auto-start runtime;
- public or LAN listener;
- browser auto-launch;
- autonomous actions.

## Validation

- visibility core self-test: 127/127;
- visibility web self-test: 143/143;
- live visibility assets: passed;
- live GET visibility APIs: 4/4;
- live HEAD visibility APIs: 4/4;
- POST visibility APIs blocked: 4/4 with `405`;
- provider values redacted;
- audit content recording disabled;
- automatic recovery disabled;
- interactive chat preserved;
- canonical data unchanged;
- SIGTERM shutdown verified;
- port `8765` closed after tests.

## Next Sprint

Sprint 190 — Review and Stabilization 181-190.
