# AURA Genesis Stabilization Runtime Hardening

Version: `v1.0.1-genesis`

Sprint: `241`

Status: COMPLETED

Current boundary: `genesis_stabilization_runtime_hardening`

Next boundary: `service_lifecycle_determinism`

Next sprint: `242`

## Purpose

Sprint 241 begins the Sprint 241-250 Genesis Stabilization & Runtime
Hardening block by removing avoidable CLI dispatch work and recursive
finalized-release status evaluation.

## Completed hardening

- established an exact nine-command ownership allowlist for the codebase
  compatibility handler;
- rejected unrelated command families before constructing any codebase
  compatibility manager;
- removed 563 `MemoryStore` and 563 `ProjectJournal` initializations from
  unrelated partner-runtime status dispatch;
- replaced recursive Sprint 240 status evaluation with an immutable,
  read-only finalized-release projection;
- preserved explicit deep `contract()` and `check()` validation;
- confirmed zero projection mismatches against the deep contract;
- added a dedicated Sprint 241 planner, manager, CLI route, and permanent
  regression owner;
- added `11` hardening assertions with zero failures.

## Performance result

Before hardening:

- Genesis Final status E2E latency: approximately `20` seconds;
- profiled status latency: approximately `56` seconds under `cProfile`;
- profiled function calls: approximately `183.5 million` per status call;
- unrelated initialization logs: `1,126`.

After hardening:

- Sprint 240 status E2E latency: approximately `0.19` seconds;
- Sprint 241 status E2E latency: approximately `0.19` seconds;
- direct finalized-release status projection: below `0.001` seconds;
- unrelated initialization logs: `0`.

## Capability registry

After Sprint 241 registration:

- total capabilities: `122`;
- online capabilities: `120`;
- foundation-only capabilities: `78`;
- planner-only capabilities: `7`;
- permission-gated capabilities: `12`;
- review-only capabilities: `12`;
- disabled runtime capabilities: `2`;
- runtime execution features: `4`.

## Historical checkpoint compatibility

Sprint 241 distinguishes immutable historical checkpoint metadata from the
current canonical identity. Sprint 221-240 contracts retain their original
`1.0.0-genesis` release anchors, while read-only compatibility checks accept
later canonical semantic versions from `1.0.0` onward. Explicit pre-v1
historical versions remain allowlisted by their original owner.

This preserves old assertion totals and historical packet values without
requiring every completed checkpoint to be rewritten after each patch release.

## Safety boundary

Sprint 241 does not:

- start the AURA service;
- open the localhost listener;
- configure or enable systemd;
- enable automatic startup;
- open a release gate;
- activate ORION control;
- broadly activate voice or vision;
- mutate memory or journal data;
- enable autonomous execution.

## Acceptance

Sprint 241 is accepted when:

- permanent hardening assertions pass `11/11`;
- Sprint 240 deep validation remains available;
- status projection matches the deep contract;
- capability registry reports `122/120`;
- identity reports `1.0.1-genesis`;
- boot remains `READY`;
- memory and journal hashes remain unchanged;
- no unexpected listener or service activation occurs.

Next: Sprint 242 — Service Lifecycle Determinism.
