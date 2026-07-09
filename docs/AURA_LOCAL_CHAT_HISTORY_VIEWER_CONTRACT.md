# AURA Local Chat History Viewer Contract

Version: v0.168.0-genesis  
Sprint: 168 — Chat History Viewer Contract

## Purpose

Sprint 168 adds a read-only Chat History Viewer Contract for AURA's local chat path. It allows AURA to inspect recent controlled message-store turns from the AURA-owned JSONL store path.

## Safe current capability

- Read the controlled local chat message store path.
- Parse bounded JSONL records.
- Show recent user/AURA turn previews.
- Handle missing or empty store safely.
- Prepare a read-only Control Center handoff for future UI.

## Boundaries

The Sprint 168 viewer does not:

- dispatch model requests
- receive model responses
- use network
- read credentials
- create or apply permission grants
- write memory
- write audit events
- execute commands/tools/plugin actions
- read arbitrary user-supplied paths
- mutate arbitrary files
- delete, export, replay, or promote history

## CLI

```bash
python3 main.py local-chat-history-alpha
python3 main.py local-chat-history-alpha 5
python3 main.py local-chat-history-viewer-contract-status
python3 main.py no-local-chat-history-viewer-unsafe-runtime-plan
```

## Next sprint

Sprint 169 should review the full local chat integration path from CLI session, message store, persona response, model adapter boundary, permission gate, safety/uncertainty layer, and history viewer.
