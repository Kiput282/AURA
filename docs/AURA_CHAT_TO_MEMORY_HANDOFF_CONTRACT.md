# AURA Chat-to-Memory Handoff Contract

Sprint 177 defines a deterministic, preview-only contract for handing one directly supplied **user** chat turn into the memory review pipeline.

The handoff requires an explicit memory trigger such as `remember that`, `ingat`, or `catat`. It binds the exact user message hash to one candidate fingerprint, performs a local sensitive-pattern precheck, and prepares a read-only destination for the Sprint 175 Memory Review Queue. Assistant, system, tool, and external-event sources are blocked. This sprint does not scan chat history, read the chat store, persist a queue item, apply a permission grant, write memory, mutate the memory store, call a model, use network, execute commands, or access arbitrary files.

## Alpha command

```bash
python3 main.py chat-to-memory-handoff-alpha "remember that AURA is local-first and permission-gated"
```

Expected state: `Handoff Eligible: True`, destination `memory_review_queue_preview`, permission `required_not_granted`, `Candidate Persisted: False`, chat-store reads `0`, and memory writes `0`.
