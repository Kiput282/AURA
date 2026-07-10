# AURA Interactive Control Center Chat Runtime

Version: v0.188.0-genesis
Sprint: 188 — Interactive Control Center Chat
Status: COMPLETED — PERMISSION-GATED LOCAL ALPHA RUNTIME

## Purpose

Sprint 188 exposes the bounded local model bridge through a responsive
localhost Control Center chat interface while retaining an honest save-only
path and explicit confirmation for every provider or model request.

## User Experience

The `/chat` surface provides:

- local session creation, selection, reload, and clearing;
- persistent local transcripts;
- provider and model status;
- explicit provider probe dialog;
- save-only mode selected by default;
- local-model mode enabled only when the bridge is active;
- per-message model confirmation;
- visible pending-retry state;
- visible response kind;
- keyboard submission and responsive layout.

## Retry and Persistence

A failed request keeps its client message ID and model request ID in memory.
Retrying the same operation therefore preserves backend idempotency. A
duplicate model request returns the already stored response without invoking
the provider again.

Session history remains local JSON with revision checks, integrity hashes,
atomic replacement, restart persistence, and exact clear confirmation.

## Safety Boundary

Enabled:

- localhost browser chat;
- persistent bounded sessions;
- save-only local messaging;
- explicit provider probe;
- explicit text-only local-model messages;
- optimistic revision conflicts;
- idempotent retry;
- response-kind visibility;
- restart persistence;
- confirmed clearing.

Disabled:

- provider activation by default;
- model downloads;
- remote providers;
- internet fallback;
- streaming;
- tool or function schemas;
- commands or action dispatch;
- arbitrary file access;
- desktop control;
- AURA long-term memory writes;
- localStorage, sessionStorage, or IndexedDB;
- WebSocket or EventSource;
- external browser dependencies;
- background/systemd/auto-start runtime;
- public or LAN listener;
- browser auto-launch;
- autonomous actions.

## Validation

- interactive runtime self-test: 119/119;
- interactive web self-test: 166/166;
- local model bridge self-test: 178/178;
- browser chat session core: 152/152;
- live save-only browser path: passed;
- live model browser path: passed;
- provider probe confirmation: passed;
- per-message model confirmation: passed;
- duplicate retry without reinvocation: passed;
- stale request blocked with `409`: passed;
- restart persistence: passed;
- clear confirmation: passed;
- SIGTERM and SIGINT: passed;
- canonical data unchanged;
- port `8765` closed after tests.

## Next Sprint

Sprint 189 — Permission, Audit, and Recovery Visibility.
