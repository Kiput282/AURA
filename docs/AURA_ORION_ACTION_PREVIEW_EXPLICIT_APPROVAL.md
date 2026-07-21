# AURA ORION Action Preview and Explicit Approval

## Sprint 276 scope

Sprint 276 adds a transport-agnostic, in-memory runtime for creating
human-readable ORION action previews and recording an explicit operator
approval or denial. It does not execute actions and does not issue a
permission.

Package:

```text
aura/orion_action_preview_approval_runtime
```

Manager:

```text
AuraOrionActionPreviewApprovalRuntimeManager
```

Component version: `0.1.0`
Product version: `1.3.1`

## Safety boundary

An approval recorded by this runtime means only that the operator explicitly
approved the exact immutable preview digest.

It does **not** mean:

- a scoped permission was issued;
- execution was authorized;
- an action was performed;
- an audit event was written;
- reviewed memory was written;
- a network listener or connection was activated.

Those boundaries remain deferred to later sprints.

## State machine

```text
idle
  -> preview_ready
      -> pending_approval
          -> approved
          -> denied
          -> cancelled
          -> expired
      -> cancelled
      -> expired

approved / denied / cancelled / expired
  -> idle
```

There are seven states and twelve valid transitions. Every other transition
fails closed.

## Preview contract

A preview is bound to:

- paired ORION identity;
- device identity;
- active live-link session;
- current capability digest;
- optional fresh redacted grounding reference;
- canonical SHA-256 preview digest;
- creation and expiry timestamps.

The preview exposes:

- action type and human-readable summary;
- exact target and parameters;
- reason;
- future required capability and whether it is currently available;
- risk level and risk reasons;
- possible side effects;
- reversibility and rollback summary;
- authorization boundary showing that execution remains disabled.

Eight preview-only action types are recognized:

- `capture_single_screenshot`
- `capture_selected_window`
- `open_allowlisted_application`
- `create_controlled_file`
- `create_controlled_folder`
- `obs_start_recording`
- `obs_stop_recording`
- `obs_switch_scene`

Recognition does not activate any of these capabilities.

## Voice-originated action requests

For a voice-originated action preview:

- the raw STT transcript is required;
- STT confidence is required and must be between `0.0` and `1.0`;
- a corrected transcript is optional;
- raw and corrected text remain visible when they differ;
- silent correction followed by action authorization is prohibited;
- explicit approval is still required.

## Approval contract

Approval requests use:

- a single-use 32-byte nonce;
- sequence number beginning at one;
- strict monotonic sequence validation;
- exact preview digest binding;
- pairing, device, live-link session, and capability digest binding;
- HMAC-SHA256 proof through the public Sprint 274 pairing API;
- `hmac.compare_digest` verification;
- explicit operator confirmation;
- separate preview and approval expiry.

Supported decision values are `approve` and `deny`. Cancellation is a local
terminal transition. Expiry is driven by `tick()`.

Replay, tampering, wrong identity, wrong session, wrong digest, wrong nonce,
future timestamp, expired decision, duplicate sequence, and out-of-order
sequence fail closed.

## Runtime properties

```text
transport_agnostic        = True
runtime_persistence       = in_memory_only
network_listener_active   = False
network_connection_active = False
real_execution_active     = False
scoped_permission_active  = False
audit_write_active        = False
reviewed_memory_write     = False
```

The runtime does not write files, start processes, open network connections,
execute actions, issue permissions, write audit events, or write memory.

## CLI

Read-only commands:

```text
orion-action-preview-status
orion-action-preview-inspect
orion-action-preview-self-test
```

The self-test contract is exactly `152/152` assertions with zero filesystem,
network, and action side effects.

## Deferred roadmap

Sprint 277 owns scoped permission, permission expiry, audit integration, and
reviewed-memory linkage.

Sprint 278 owns bounded ORION capture, allowlisted application, controlled
file, and OBS actions.

Sprint 279 owns watchdog, emergency stop, and recovery.

Sprint 280 owns live end-to-end acceptance and the v1.4.0 boundary.
