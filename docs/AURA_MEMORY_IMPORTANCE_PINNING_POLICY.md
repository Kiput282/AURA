# AURA Memory Importance and Pinning Policy

Sprint 174 adds deterministic, explainable importance scoring and pinning recommendations for one user-supplied memory candidate.

## Safe boundary

The policy may classify a candidate, score importance, detect durable and temporary signals, recommend a retention tier, and mark whether the candidate is eligible for future pin review. It does not persist the candidate or policy result, apply a permission grant, write or mutate the memory store, pin or unpin memory, call a model, use network or credentials, write audit events, execute commands, or access arbitrary files.

## Alpha command

```bash
python3 main.py memory-importance-pinning-alpha "remember that AURA is local-first and permission-gated"
```

Expected safe state:

- scoring method: `deterministic_explainable_no_model`
- pin state: `not_pinned`
- automatic pin applied: `False`
- write permission state: `required_not_granted`
- candidate persisted: `False`
- memory state: `policy_preview_only_not_saved`
- all side-effect counters: `0`

The next planned sprint is Sprint 175 — Memory Review Queue.
