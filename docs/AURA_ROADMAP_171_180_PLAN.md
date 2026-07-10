# AURA Roadmap 171-180 — Memory Runtime

This block follows Sprint 170 Local Chat Runtime Stabilization.

## Sprint Plan

- Sprint 171 — Memory Runtime Foundation
- Sprint 172 — Memory Write Permission Gate
- Sprint 173 — Memory Extraction Dry Run
- Sprint 174 — Memory Importance and Pinning Policy
- Sprint 175 — Memory Review Queue
- Sprint 176 — Memory Correction and Deletion Boundary
- Sprint 177 — Chat-to-Memory Handoff Contract
- Sprint 178 — Memory Privacy and Redaction Layer
- Sprint 179 — Memory Runtime Integration Review
- Sprint 180 — Memory Runtime Stabilization

## Guardrails

Memory must not be written automatically from chat until permission, review, correction, deletion, and privacy boundaries are in place. Model-based summarization stays deferred until model request permission is ready.


## Sprint 171 — Memory Runtime Foundation

Status: completed in `v0.171.0-genesis` after Sprint 170.

Sprint 171 creates a preview-only foundation for memory candidate packets, write-gate planning, privacy boundary planning, and chat-to-memory handoff. It keeps memory writes, memory store mutation, model requests, network, credentials, permission grants, command execution, arbitrary file access, full memory runtime, and runtime execution disabled.

Next: Sprint 172 — Memory Write Permission Gate.


## Sprint 172 — Memory Write Permission Gate

Status: completed in `v0.172.0-genesis` after Sprint 171.

Sprint 172 adds a default-deny, preview-only permission gate for one memory candidate fingerprint and the exact `memory.write.single_candidate` scope. It requires an explicit future approve-once decision while keeping permission request persistence, permission grant apply, memory candidate persistence, memory write/store mutation, model requests, network, credentials, audit writes, commands, arbitrary file access, and runtime execution disabled.

Next: Sprint 173 — Memory Extraction Dry Run.


## Sprint 173 — Memory Extraction Dry Run

Status: completed in `v0.173.0-genesis` after Sprint 172.

Sprint 173 adds deterministic, rule-based extraction of one reviewable memory candidate from a user-supplied message. It detects explicit memory triggers, normalizes and classifies candidate text, screens common sensitive patterns, creates a candidate fingerprint, and prepares permission/review handoff metadata while keeping model requests, permission persistence and grant apply, candidate persistence, memory writes/store mutation, network, credentials, audit writes, commands, arbitrary file access, and runtime execution disabled.

Next: Sprint 174 — Memory Importance and Pinning Policy.
