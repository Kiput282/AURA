# AURA Memory Extraction Dry Run

Sprint 173 adds deterministic, rule-based extraction of one memory candidate from a user-supplied message.

## Safe boundary

The dry run may normalize text, detect an explicit memory trigger, classify a candidate, screen common sensitive patterns, calculate a candidate fingerprint, and prepare a permission-gate handoff preview. It does not call a model, persist the candidate, persist a permission request, apply a grant, write the memory store, write audit events, use network or credentials, execute commands, or access arbitrary files.

## Alpha command

```bash
python3 main.py memory-extraction-dry-run-alpha "remember that AURA is local-first"
```

Expected decision state:

- extraction method: `deterministic_rule_based_no_model`
- permission state: `required_not_granted`
- gate decision: `blocked_no_explicit_grant`
- candidate persisted: `False`
- memory state: `dry_run_preview_only_not_saved`
- all side-effect counters: `0`

The next planned sprint is Sprint 174 — Memory Importance and Pinning Policy.
