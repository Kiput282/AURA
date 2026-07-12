# AURA Multi-Interface State Synchronization

## Checkpoint

- Version: `v0.226.0-genesis`
- Sprint: 226
- Block: Sprint 221-230 Unified Partner Runtime Integration
- Runtime state: contract-only and metadata-only
- Assertions: 128
- Failed assertions: 0
- Next sprint: 227
- Next boundary: `service_persistence_and_launcher`

## Purpose

Sprint 226 defines one deterministic metadata synchronization contract across
AURA's declared partner interfaces.

The sprint does not activate live synchronization. It defines which metadata is
safe to represent consistently and which payload-adjacent state must remain
outside the synchronization boundary.

## Implementation

The Sprint 226 implementation provides:

    aura/partner_runtime/multi_interface_state_synchronization_planner.py
    aura/partner_runtime/multi_interface_state_synchronization_alpha_manager.py
    aura/partner_runtime/__init__.py
    aura/core/cli.py
    aura/core/shell.py

Version compatibility updates are applied to:

    aura/personality/identity.yaml
    aura/partner_runtime/personality_consistency_runtime_planner.py
    aura/partner_runtime/workspace_project_context_planner.py

Read-only commands are exposed through CLI and shell.

## Canonical upstream owner

The upstream personality owner remains:

    aura.partner_runtime.personality_consistency_runtime_alpha_manager.
    PersonalityConsistencyRuntimeAlphaManager

Its Sprint 225 baseline remains:

- 96 assertions
- zero failures
- planning ready
- runtime closed
- payload-free
- deterministic
- synchronization deferred to Sprint 226

## Canonical session owner

The canonical session owner remains:

    aura_browser_chat_session_runtime

Sprint 226 invokes only:

    contract_snapshot
    safety_boundary

The following browser-session methods are excluded:

    status
    load_session
    list_sessions
    create_session
    submit_message
    submit_local_model_message
    clear_session
    self_test

Browser session payload reads remain zero.

## Interface-state schema owner

The interface-state schema owner remains:

    aura.chat_bridge.aura_chat_bridge_session_state_foundation_manager.
    AuraChatBridgeSessionStateFoundationManager

The declared schema contains 12 fields and eight planned events.

## Canonical synchronization fields

Six metadata fields are admitted into the deterministic state-vector template:

- `aura_identity_version`
- `selected_channel`
- `safe_idle_mode`
- `permission_boundary_state`
- `session_recovery_hint`
- `session_runtime_enabled`

The canonical defaults are:

- identity version: `0.226.0-genesis`
- selected channel: `metadata_only`
- safe idle: `true`
- permission boundary: `default_deny`
- recovery hint: `manual_recovery_only`
- session runtime enabled: `false`

## Excluded payload-adjacent fields

Six fields remain outside the synchronization vector:

- `session_id_planned`
- `conversation_id_planned`
- `user_display_name`
- `last_user_message_metadata`
- `last_aura_response_metadata`
- `pending_action_request_metadata`

These fields are not read, copied, persisted, propagated, or synchronized.

## Interface targets

The metadata contract declares seven interface targets:

- browser chat
- local chat CLI
- Control Center
- voice metadata
- vision metadata
- shell
- CLI

Each target receives only the same declarative state-vector template. No live
interface state is created or propagated.

## Control Center boundary

Control Center is classified as:

    static_reference_only

Sprint 226 reads only static class metadata such as name, sprint, schema
version, routes, and panel identifiers.

The runtime `snapshot()` method is not invoked because it may traverse broader
runtime sources, including memory visibility data.

## Local Interaction boundary

Local Interaction Stabilization is used only as a secondary read-only baseline.

The baseline confirms:

- nine expected components present
- no runtime mutation
- no listener started by status inspection
- no subprocess started by status inspection
- release gate closed

## State-vector policy

The synchronization scope is:

    deterministic_metadata_state_vector_only

Sprint 226 declares templates only.

It does not:

- create a live state vector
- persist interface state
- read a state store
- write a state store
- dispatch events
- propagate state
- create background synchronization loops

## Runtime and safety boundary

Sprint 226 does not:

- read chat or session payloads
- access long-term memory
- write memory
- mutate permissions
- write audit records
- perform network requests
- execute commands
- execute tools
- launch interface processes
- start background services
- activate runtime authority
- open release gates
- perform autonomous state propagation

## Commands

The following read-only commands are available:

    partner-runtime-multi-interface-state-synchronization-status
    partner-runtime-multi-interface-state-synchronization-context
    partner-runtime-multi-interface-state-synchronization-check

CLI and shell routes expose identical deterministic packets.

## Validation contract

The Sprint 226 planner validates 128 assertions.

Required properties include:

- Sprint 225 upstream baseline remains 96/96
- Sprint 224 upstream baseline remains 84/84
- canonical browser session ownership is preserved
- browser session payload reads remain zero
- Chat Bridge schema remains 12 fields and eight events
- six canonical fields are present
- six excluded fields remain disjoint
- seven interface targets use identical metadata templates
- Control Center remains static-reference-only
- no runtime-data mutation occurs
- no propagation, persistence, execution, service, release, or autonomy opens

## Next boundary

Sprint 227 — Service Persistence and Launcher

Canonical boundary identifier:

    service_persistence_and_launcher
