# AURA Local Web Runtime Alpha

Version: v0.181.0-genesis
Sprint: 181 — Local Web Runtime Activation Cutline
Status: COMPLETED — PERMISSION-GATED ALPHA RUNTIME

## Purpose

Sprint 181 activates AURA's first real web listener as the narrowest safe
runtime cutline for the Local Interaction Runtime Activation block.

The runtime proves that AURA can:

- validate fail-closed local configuration;
- bind an HTTP listener only to IPv4 localhost;
- expose a minimal read-only Control Center shell;
- expose health and runtime status endpoints;
- start only after explicit manual confirmation;
- run only in the foreground;
- stop cleanly and release its configured port.

## Commands

```bash
python3 main.py local-web-runtime-status
python3 main.py local-web-runtime-self-test
python3 main.py local-web-runtime-start --confirm-localhost
```

Stop the foreground runtime with `Ctrl+C`.

## Configuration

```yaml
local_web_runtime:
  host: 127.0.0.1
  port: 8765
  mode: safe_idle
  require_explicit_confirmation: true
```

Any host other than `127.0.0.1`, mode other than `safe_idle`, invalid port, or
disabled explicit confirmation causes startup to fail closed.

## Routes

- `GET /` — static read-only Control Center alpha shell
- `GET /health` — current listener health envelope
- `GET /api/status` — current Sprint 181 runtime boundary
- `HEAD` is supported for the same read-only routes
- unknown routes return `404`
- mutating and negotiation methods return `405`

## Runtime Capability

Sprint 181 contributes exactly one runtime execution feature: an explicitly
confirmed localhost HTTP listener. Availability does not mean it is always
running. Its default state is stopped.

## Security Boundary

Enabled:

- IPv4 localhost bind at `127.0.0.1:8765`
- foreground process
- explicit manual start
- read-only HTTP handling
- static Control Center alpha shell
- health and status JSON
- clean `SIGINT` shutdown
- no-store and browser-hardening headers
- Host-header allowlist for `127.0.0.1` and `localhost`

Still disabled:

- public, LAN, wildcard, and IPv6-wildcard binding
- automatic or background service start
- systemd installation or activation
- browser auto-launch
- CORS and WebSocket runtime
- chat and model runtime
- memory writes and memory-store mutation
- permission grants or permission mutation
- audit persistence
- commands, tools, action dispatch, and arbitrary file access
- desktop control
- voice and vision runtime
- autonomous actions

## Validation Evidence

Sprint 181 validation proves:

- status inspection keeps port `8765` closed;
- the listener binds to `127.0.0.1:8765`;
- `/`, `/health`, and `/api/status` work;
- unknown routes return `404`;
- mutating methods return `405`;
- 21 runtime assertions pass;
- `SIGINT` stops the listener cleanly;
- port `8765` is closed after shutdown;
- normal AURA boot remains `READY`.

## Next Sprint

Sprint 182 — Service Lifecycle Runtime
