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


## Sprint 174 — Memory Importance and Pinning Policy

Status: completed in `v0.174.0-genesis` after Sprint 173.

Sprint 174 adds deterministic and explainable importance scoring, durable/temporary signal detection, retention recommendations, and future pin eligibility for one candidate. All results remain preview-only: candidate persistence, permission grant apply, memory writes/store mutation, pin/unpin operations, model/network/credential activity, audit writes, commands, arbitrary file access, and runtime execution remain disabled.

Next: Sprint 175 — Memory Review Queue.


## Sprint 175 — Memory Review Queue

Status: completed in `v0.175.0-genesis` after Sprint 174.

Sprint 175 adds a deterministic, ephemeral in-process review queue preview for one memory candidate, including review priority, privacy hold routing, permission state, and future approve/edit/reject/defer options. Queue items and decisions are not persisted or applied; permission grants, candidate persistence, memory writes/store mutation, pin/unpin actions, model/network/credential activity, audit writes, commands, arbitrary file access, and runtime execution remain disabled.

Next: Sprint 176 — Memory Correction and Deletion Boundary.


## Sprint 176 — Memory Correction and Deletion Boundary

Status: completed in `v0.176.0-genesis` after Sprint 175.

Sprint 176 defines exact-target correction and deletion previews for one user-supplied memory record reference. Correction is modeled as a future versioned replacement rather than in-place editing; deletion is modeled as a future tombstone-first operation, while purge requires a separate future permission scope. Memory-store reads and record lookups, correction/delete/tombstone/purge application, permission grants, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, and runtime execution remain disabled.

Next: Sprint 177 — Chat-to-Memory Handoff Contract.


## Sprint 177 — Chat-to-Memory Handoff Contract

Status: completed in `v0.177.0-genesis` after Sprint 176.

Sprint 177 adds a deterministic, direct-user-turn, preview-only handoff contract from chat into the memory review pipeline. It requires an explicit memory trigger, exact source binding, a local privacy precheck, and default-deny permission state. Chat history/store reads, automatic scan/subscription, queue persistence, permission grants, candidate persistence, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, and runtime execution remain disabled.

Next: Sprint 178 — Memory Privacy and Redaction Layer.


## Sprint 178 — Memory Privacy and Redaction Layer

Status: completed in `v0.178.0-genesis` after Sprint 177.

Sprint 178 adds deterministic, local privacy screening for one directly supplied memory candidate. It provides stable redaction previews for maskable data, blocks credential/token/private-key material from the pipeline, hides original values from rendered output, and routes results to manual privacy review before permission review. Original/redacted candidate persistence, review decisions, permission grants, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, and runtime execution remain disabled.

Next: Sprint 179 — Memory Runtime Integration Review.
