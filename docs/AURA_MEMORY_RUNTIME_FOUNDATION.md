# AURA Memory Runtime Foundation

Version: `v0.171.0-genesis`

Sprint 171 starts the Memory Runtime block after the Sprint 161-170 Local Chat Runtime stabilization checkpoint.

## Purpose

Create a safe foundation for future memory runtime by defining:

- memory candidate preview packets
- memory write-gate requirements
- memory source boundaries
- privacy and redaction requirements
- review queue handoff requirements
- correction and deletion policy requirements
- chat-to-memory handoff boundaries
- model-summary boundaries
- Control Center handoff data

## Current Runtime Boundary

Sprint 171 is preview-only and metadata-only. It does not write memory, mutate the memory store, delete memory, export memory, call a model, use network, read credentials, apply permission grants, write audit events, execute commands, read arbitrary files, write arbitrary files, or open the full memory runtime.

## CLI

```bash
python3 main.py memory-runtime-alpha "remember that AURA is local-first"
python3 main.py memory-runtime-foundation-status
python3 main.py no-memory-runtime-unsafe-runtime-plan
```

## Next Sprint

Sprint 172 should add the Memory Write Permission Gate. Memory write must remain blocked by default until explicit permission, review, correction/deletion, privacy, and audit boundaries are ready.
