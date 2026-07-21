# AURA ORION Scoped Permission, Expiry, Audit, and Reviewed Memory

Sprint 277 adds a fail-closed authorization layer between the explicit action
approval completed in Sprint 276 and the bounded action adapters reserved for
Sprint 278.

## Runtime identity

```text
package           = aura/orion_scoped_permission_runtime
manager           = AuraOrionScopedPermissionRuntimeManager
component_version = 0.1.0
product_version   = 1.3.1
sprint            = 277
```

The runtime is transport-agnostic. It composes only public pairing, live-link,
and Sprint 276 preview/approval APIs.

## Permission lifecycle

A permission is issued only after an approved Sprint 276 result, explicit
operator confirmation, a valid paired identity, and a live authenticated
ORION session. Each permission is bound to the exact preview digest, action
type, target digest, parameters digest, pairing ID, device ID, live-link
session ID, and capability digest.

```text
active -> consumed -> outcome_recorded
active -> expired
active -> revoked
```

Permissions are single-use, use a default TTL of 30 seconds, accept at most a
120-second TTL, and live only in the current process. Restarting the runtime
invalidates all active permissions.

Permission consumption returns an authorization receipt with:

```text
execution_authorized = True
execution_performed  = False
```

Sprint 277 records externally reported outcomes but never invokes an action.

## Durable audit

Audit events are redacted, append-only JSONL records stored outside the
repository under the default state root:

```text
~/.local/state/aura/orion_scoped_permission
```

The directory is mode `0700`; audit and reviewed-memory files are mode `0600`.
Every event participates in a SHA-256 previous-digest chain. Appends are
flushed and fsynced before a successful result is returned. Startup verifies
existing audit and reviewed-memory integrity. Corruption fails closed.

Audit events cover permission issuance, validation, consumption, expiry,
revocation, outcome recording, memory-candidate creation, explicit review,
and candidate expiry.

## Reviewed memory

A memory candidate may be created only from a terminal permission audit event.
Candidates remain ephemeral and require explicit signed review. Approval
persists only a redacted summary in the runtime-owned reviewed-memory store.

The memory-review wire schema remains exactly 11 fields. Its HMAC canonical
payload is additionally bound to the pairing ID and device ID derived from the
candidate's source permission. Those identity fields are not caller-supplied,
so a reviewer cannot substitute another paired identity while preserving the
same candidate payload.

The following remain prohibited:

```text
raw grounding persistence
raw STT transcript persistence
corrected STT transcript persistence
automatic or silent memory approval
general AURA memory handoff
```

Rejected and expired candidates are audited but never persisted as reviewed
memory.

## Public runtime surface

```text
issue_permission
inspect_permission
validate_permission
consume_permission
record_execution_outcome
revoke_permission
tick
audit_events
verify_audit_chain
create_memory_candidate
review_memory_candidate
reviewed_memory_records
reset_ephemeral
status
inspect_runtime
self_test
```

Read-only CLI commands:

```text
orion-scoped-permission-status
orion-scoped-permission-inspect
orion-scoped-permission-self-test
```

The self-test contract is exactly `224/224` assertions.

## Safety boundary

Sprint 277 activates scoped permission, expiry, permission validation and
consumption, authorization receipts, durable audit, audit-chain verification,
and explicitly reviewed redacted memory.

Sprint 278 exclusively owns bounded screenshot capture, allowlisted
application launch, controlled file/folder creation, and OBS actions. Sprint
277 does not start a network listener, open a network connection, capture the
screen, launch an application, change a file, control OBS, or execute any
other real action.

Sprint 279 owns watchdog, emergency stop, and recovery. Sprint 280 owns the
live end-to-end acceptance test and v1.4.0 boundary.
