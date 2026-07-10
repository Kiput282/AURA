# AURA Memory Correction and Deletion Boundary

Sprint 176 defines exact-target, preview-only correction and deletion boundaries for one user-supplied memory record reference.

Correction is modeled as a future versioned replacement rather than an in-place edit. Deletion is modeled as a future tombstone-first operation, while hard purge requires a separate future permission scope. This sprint performs no memory-store read or record lookup, applies no correction/delete/tombstone/purge, persists no permission request or grant, and performs no model, network, command, or arbitrary-file operation.

## Alpha command

```bash
python3 main.py memory-correction-deletion-alpha correction "AURA is local-first => AURA is local-first and permission-gated"
```

Expected state: exact target binding `True`, permission `required_not_granted`, correction/deletion authorization `False`, store reads `0`, and memory state `correction_boundary_preview_only_no_mutation`.
