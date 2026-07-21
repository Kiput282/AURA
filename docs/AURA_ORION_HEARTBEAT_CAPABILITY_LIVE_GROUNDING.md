# AURA ORION Heartbeat, Capability Negotiation, and Live Grounding

## Sprint

Sprint 275 — heartbeat, capability negotiation, and live grounding.

## Scope

Sprint 275 adds an authenticated, transport-agnostic live-link runtime
between the paired ORION identity and ATLAS. It processes signed
envelopes in memory and does not activate a network listener or outbound
connection.

The runtime is implemented in:

```text
aura/orion_live_link_runtime/
```

The product version remains `v1.3.1`; the live-link component version is
`0.1.0`.

## Pairing integration

Sprint 274 pairing remains the owner of the shared credential and stable
device identity. Sprint 275 adds three narrow public methods to the
pairing manager:

- `authenticated_binding`
- `sign_authenticated_envelope`
- `verify_authenticated_envelope`

These methods expose only public binding metadata. The shared secret is
never returned by status, inspection, signing, verification, or the
live-link runtime.

Every live-link envelope is bound to:

- pairing ID
- device ID
- credential ID and fingerprint through the active pairing record
- a live-link session ID
- a strictly monotonic sequence
- a domain-separated HMAC-SHA256 proof

Verification uses `hmac.compare_digest`.

## Transport boundary

Sprint 275 is transport-agnostic:

- network listener: inactive
- network connection: inactive
- direct socket or HTTP send/receive: absent
- ingress: direct manager method or a future injected transport adapter
- egress: signed response data returned to the caller
- runtime state: in memory only

A later transport adapter must preserve the authenticated envelope
contract. Existing ORION transport precedents are not automatically
trusted as Sprint 275 authentication bindings.

## State machine

States:

- `disconnected`
- `connecting`
- `live`
- `stale`
- `failed`

Valid transitions:

- `disconnected → connecting` when an authenticated session opens
- `connecting → live` when the first valid heartbeat is accepted
- `live → live` when a subsequent valid heartbeat is accepted
- `live → stale` after heartbeat staleness
- `stale → live` when a fresh heartbeat is accepted
- `stale → failed` after heartbeat failure timeout
- `connecting → failed` on authentication or handshake timeout
- `live → disconnected` through normal close
- `stale → disconnected` through normal close
- `failed → disconnected` through explicit reset

Invalid transitions fail closed.

## Heartbeat contract

- protocol version: `aura-orion-live-link-v1`
- interval: 5 seconds
- stale after: 15 seconds
- failed after: 30 seconds
- maximum accepted future clock skew: 5 seconds
- sequence starts at 1
- sequence must increase strictly
- duplicates and out-of-order messages are rejected
- stale session, wrong pairing, wrong device, wrong session, tampering,
  and invalid proof are rejected

Heartbeat fields include:

- protocol version and message type
- live-link session ID
- pairing ID and device ID
- monotonic sequence
- sent timestamp
- device state
- capability digest

## Capability negotiation

The existing capability registry and Control Center capability viewer
remain reference-only foundations. Sprint 275 owns the behavioral
negotiation state.

ATLAS advertises three read-only capabilities:

- `orion.heartbeat`
- `orion.capability_negotiation`
- `orion.live_grounding`

Capability entries contain:

- capability ID
- version
- mode
- constraints
- source

The agreed capability list is canonicalized as deterministic compact
UTF-8 JSON and hashed with SHA-256. Unknown optional capabilities are
rejected individually. Unknown required capabilities fail closed.
Deferred action capabilities are rejected.

No action is enabled by capability negotiation.

## Live grounding

Grounding envelopes include:

- source and subject
- redacted summary
- confidence
- provenance
- observation and send timestamps
- capability digest
- explicit redaction marker

Freshness policy:

- fresh: age up to 5 seconds
- stale: age over 5 seconds and up to 15 seconds
- expired: age over 15 seconds
- future timestamps beyond the clock-skew allowance: rejected

Expired grounding is rejected. Stale grounding is never usable for an
action decision. Sprint 275 does not execute actions.

Raw grounding payloads and heartbeat history are not persisted. Status
returns only bounded current metadata and does not return the raw
grounding summary.

## CLI

The CLI exposes inspection and self-test commands only:

```bash
python main.py orion-live-link-status
python main.py orion-live-link-inspect
python main.py orion-live-link-self-test
```

Live envelope ingress remains a manager/API surface for a future
authenticated transport adapter.

## Deferred boundaries

Sprint 275 does not activate:

- action preview or explicit approval — Sprint 276
- scoped permission, expiry, audit writes, or reviewed memory —
  Sprint 277
- capture, app, file, or OBS actions — Sprint 278
- watchdog, emergency-stop runtime, recovery, or dialogue evaluation —
  Sprint 279

The following fields remain false:

- `network_listener_active`
- `network_connection_active`
- `action_preview_active`
- `approval_active`
- `permission_active`
- `audit_write_active`
- `real_action_execution_active`
- `watchdog_active`
- `emergency_stop_active`
- `recovery_active`
