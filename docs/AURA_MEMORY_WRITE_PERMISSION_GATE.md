# AURA Memory Write Permission Gate

Version: `v0.172.0-genesis`

Sprint 172 adds a default-deny permission gate between memory candidate preview and any future memory-store write.

## Purpose

The gate defines:

- a permission request envelope for one memory candidate
- an exact `memory.write.single_candidate` scope
- an in-memory candidate fingerprint
- explicit user decision requirements
- default denial without a matching grant
- future approve-once and one-shot grant semantics
- expiry and revocation requirements
- audit and Control Center handoff metadata

## Current Runtime Boundary

Sprint 172 does not persist permission requests, apply grants or denials, activate permission scopes, start expiry timers, consume grants, persist candidates, write or mutate the memory store, delete or export memory, call a model, use network, read credentials, write audit events, execute commands, or access arbitrary files.

## CLI

```bash
python3 main.py memory-write-permission-gate-alpha "remember that AURA is local-first"
python3 main.py memory-write-permission-gate-status
python3 main.py no-memory-write-permission-gate-unsafe-runtime-plan
```

## Next Sprint

Sprint 173 should add Memory Extraction Dry Run. Extraction must remain preview-only and must not bypass the Sprint 172 permission gate.
