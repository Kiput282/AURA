# AURA ORION Agent Foundation

## Sprint

Sprint 273 — ORION agent foundation.

## Purpose

This package establishes a deterministic ATLAS-side component identity,
status schema, inspection contract, and self-test entry point for a
future ORION agent.

It is a foundation only. It does not activate an ORION client or Safe
Action Bridge.

## Runtime state

The foundation always reports:

- `safe_idle: true`
- `foundation_only: true`
- no network listener
- no outbound network connection
- no authentication or pairing
- no device identity binding
- no heartbeat
- no capability negotiation or live grounding
- no action preview or approval
- no permission activation or audit writes
- no real action execution
- no watchdog, emergency-stop runtime, or recovery execution

## Deferred boundaries

- Sprint 274: authenticated pairing and device identity
- Sprint 275: heartbeat, capability negotiation, and live grounding
- Sprint 276: action preview and explicit approval
- Sprint 277: scoped permission, expiry, audit, and reviewed memory
- Sprint 278: bounded ORION capture, app, file, and OBS actions
- Sprint 279: watchdog, emergency stop, recovery, and dialogue evaluation

## CLI inspection

```bash
python main.py orion-agent-foundation-status
python main.py orion-agent-foundation-inspect
python main.py orion-agent-foundation-self-test
```

These commands are read-only and do not start services, bind ports,
open connections, persist runtime state, or execute actions.

## Product version

Sprint 273 retains product version `v1.3.1`. The component uses internal
foundation version `0.1.0`.
