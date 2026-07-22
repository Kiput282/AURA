# AURA ORION Watchdog, Emergency Stop, Recovery, and Dialogue Evaluation

## Status

Sprint 279 introduces the fail-closed ORION supervision and recovery runtime.
It is an in-memory, explicit-tick coordinator built on top of the public
pairing, live-link, action-preview, scoped-permission, and bounded-action APIs.
It does not create a listener, network connection, background thread, process,
or real platform side effect inside AURA core.

## Runtime package

- Package: `aura/orion_supervision_recovery_runtime`
- Manager: `AuraOrionSupervisionRecoveryRuntimeManager`
- Safety protocol: `AuraOrionSafetyControlAdapter`
- Component version: `0.1.0`
- Product version: `v1.3.1`

The default adapter is non-executing. The fake adapter is limited to
self-tests. The guarded Windows adapter can call only explicitly injected
callbacks and remains unavailable on ATLAS.

## State machine

The runtime owns nine states and sixteen explicit transitions:

1. `idle`
2. `armed`
3. `healthy`
4. `stale`
5. `emergency_latched`
6. `recovery_pending`
7. `recovery_review`
8. `recovered`
9. `failed`

Emergency state is latched. It cannot automatically clear itself. Recovery
requires an explicit recorded outcome, a review request, safe-idle evidence,
a valid audit chain, outcome reconciliation, and an explicit operator review
resolution.

## Heartbeat and watchdog

The watchdog reuses the live-link public contract:

- expected interval: 5 seconds
- stale threshold: 15 seconds
- failed threshold: 30 seconds
- maximum clock skew: 5 seconds

The watchdog runs only when `tick()` is called. AURA core starts no watchdog
thread or timer loop. A fresh live-link heartbeat moves an armed or stale
session to `healthy`; a stale heartbeat moves a healthy session to `stale`;
a failed heartbeat latches emergency stop.

## Emergency-stop order

Emergency stop follows a fixed fail-closed order:

1. latch `emergency_latched`
2. cancel pending preview through the public preview API
3. revoke scoped permission through the public permission API
4. close the live-link session through the public live-link API
5. invoke the injected safety-control adapter
6. record execution outcome and audit through public APIs when evidence exists
7. verify safe-idle through the injected safety-control adapter

Repeated emergency-stop requests are idempotent and do not clear the latch.
No emergency-stop or action-execution CLI command is exposed.

## Recovery and reconciliation

Automatic recovery is forbidden. `outcome_unconfirmed` cannot be cleared by a
reset. Recovery uses a review object containing only bounded evidence and
redacted summaries. Approval requires:

- explicit `RECONCILE OUTCOME` confirmation
- a lowercase SHA-256 evidence digest
- verified safe-idle
- valid permission audit chain
- explicit `APPROVE RECOVERY` confirmation

Rejection moves the session to `failed`. Either `recovered` or `failed` may be
returned to `idle` only with explicit `RESET SAFE IDLE` confirmation and a new
safe-idle verification.

## Dialogue evaluation

Dialogue evaluation is deterministic and local. It uses eight rules covering
approval bypass, emergency acknowledgement, outcome uncertainty, unevidenced
recovery claims, scope escalation, sensitive-data exposure, unsafe-action
language, and unsupported capability claims.

Results use four verdicts: `pass`, `warn`, `requires_review`, and `block`.
Inputs are bounded to 4096 characters by default. Sensitive values are
redacted. Raw dialogue is not retained, no cloud or LLM is required, and no
general memory handoff occurs.

## Public CLI

The only Sprint 279 CLI commands are read-only:

- `orion-supervision-status`
- `orion-supervision-inspect`
- `orion-supervision-self-test`

## Safety boundaries

The Sprint 279 core contract keeps all of the following false:

- core network listener
- core network connection
- core background thread
- core process execution
- automatic recovery
- private mutation of earlier runtimes
- real action execution on ATLAS
- real emergency side effect on ATLAS
- raw dialogue retention
- general memory handoff

Sprint 280 owns the live ORION end-to-end acceptance and the `v1.4.0` release
boundary.
