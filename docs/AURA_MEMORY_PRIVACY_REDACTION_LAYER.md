# AURA Memory Privacy and Redaction Layer

Sprint 178 adds deterministic, local, preview-only privacy screening for one directly supplied memory candidate.

The layer classifies a candidate as **clear**, **redaction review required**, or **blocked sensitive secret**. Email addresses, phone numbers, IPv4 addresses, and payment-card-like sequences receive stable placeholder previews. Credential assignments, bearer tokens, and private-key material are blocked from the memory pipeline. Only the redacted form is rendered; the original value is represented by fingerprints and lengths, not displayed or persisted.

This sprint does not persist original or redacted candidates, write a review queue item, apply a permission grant, write or mutate memory, call a model, use network, execute commands, or access arbitrary files.

## Alpha command

```bash
python3 main.py memory-privacy-redaction-alpha "remember that contact email is demo@example.com and AURA is local-first"
```

Expected state: one redaction match, preview containing `[REDACTED_EMAIL]`, privacy state `redaction_review_required`, permission `required_not_granted`, both persistence flags `False`, and memory writes `0`.
