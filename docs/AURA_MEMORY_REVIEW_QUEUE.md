# AURA Memory Review Queue

Sprint 175 introduces a deterministic, preview-only queue for manual review of one memory candidate.

The queue is ephemeral and exists only inside the current process. It exposes priority, review state, privacy hold, permission state, and future decision options. It does not persist queue items, apply decisions or grants, write or pin memory, mutate the memory store, call models or networks, execute commands, or access arbitrary files.

## Alpha command

```bash
python3 main.py memory-review-queue-alpha "remember that AURA is local-first and permission-gated"
```

Expected state: `pending_manual_review`, queue persistence `False`, decision applied `False`, permission `required_not_granted`, and memory state `review_queue_preview_only_not_saved`.
