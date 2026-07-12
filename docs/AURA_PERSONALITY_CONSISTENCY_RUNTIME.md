# AURA Personality Consistency Runtime

## Checkpoint

- Version: `v0.225.0-genesis`
- Sprint: 225
- Block: Sprint 221-230 Unified Partner Runtime Integration
- Runtime state: contract-only and metadata-only
- Assertions: 96
- Failed assertions: 0
- Next sprint: 226
- Next boundary: `multi_interface_state_synchronization`

## Purpose

Sprint 225 defines a single personality consistency contract across AURA's
canonical identity, existing persona-style owner, stabilized multimodal context
metadata, and canonical browser-chat session ownership.

The sprint establishes what must remain consistent when future interactions
move between browser chat, local CLI, Control Center, voice metadata, vision
metadata, shell, and CLI surfaces.

It does not synchronize live interface state. That work is deferred to Sprint
226.

## Implementation

The Sprint 225 implementation provides:

    aura/partner_runtime/personality_consistency_runtime_planner.py
    aura/partner_runtime/personality_consistency_runtime_alpha_manager.py

The classes are exported by:

    aura/partner_runtime/__init__.py

Read-only commands are exposed through CLI and shell.

## Canonical owners

Canonical identity source:

    aura/personality/identity.yaml

Canonical persona contract owner:

    aura.local_chat_persona_response_layer.
    aura_local_chat_persona_response_layer_manager.
    AuraLocalChatPersonaResponseLayerManager

Canonical upstream context owner:

    aura.partner_runtime.
    voice_vision_chat_context_fusion_alpha_manager.
    VoiceVisionChatContextFusionAlphaManager

Canonical session owner:

    aura_browser_chat_session_runtime

Secondary expression reference:

    aura.expression.expression_language_manager.
    ExpressionLanguageManager

Expression Language remains a secondary metadata reference. Sprint 225 does
not instantiate it and does not grant it personality runtime authority.

## Identity contract

The contract requires:

- name: AURA
- version: `0.225.0-genesis`
- codename: Genesis
- creator: Kiput
- motto: Grow Together
- a non-empty personality description

Required traits:

- friendly
- intelligent
- supportive
- curious
- adaptive
- honest

Required modes:

- coding
- gaming
- learning
- streaming

## Persona-style contract

The existing Sprint 164 persona owner remains authoritative for persona style.

Required style items include:

- warm AI partner tone
- clear Indonesian default
- concise but supportive style
- honest capability boundaries
- no false autonomy claims
- no fake model claims
- no fake memory claims
- AURA project-context awareness
- safe developer-assistant identity
- Genesis Final alignment

Sprint 225 uses only the persona owner's read-only status, context, and plan
methods.

The following methods are not invoked:

    generate_persona_response
    run_persona_turn
    render_persona_turn

## Consistency dimensions

The personality profile declares:

- identity continuity
- trait continuity
- mode-style continuity
- warm partner tone
- capability honesty
- safety-boundary consistency
- canonical session continuity
- modality neutrality
- no false autonomy
- no fake memory or model claims

## Interface targets

The contract declares future consistency targets for:

- browser chat
- local chat CLI
- Control Center
- voice metadata
- vision metadata
- shell
- CLI

These are metadata targets only. Sprint 225 does not propagate or synchronize
live state between them.

## Upstream fusion boundary

Sprint 224 remains the upstream voice, vision, and chat context owner.

The Sprint 225 contract requires the Sprint 224 baseline to remain:

- 84 assertions
- zero failures
- planning ready
- runtime not ready
- no live fusion packet
- no context inference
- no model request
- no memory write
- no permission mutation
- no audit write
- no execution

## Payload boundary

Sprint 225 does not read:

- chat messages
- browser session records
- persona JSONL records
- raw audio
- transcripts
- images
- screenshots
- OCR output
- journal data
- long-term memory
- runtime data

## Runtime boundary

Sprint 225 does not:

- mutate the identity file during runtime
- generate a persona response
- execute a persona turn
- persist persona or chat data
- synchronize interface state
- invoke a local or remote model
- perform context inference
- read or write memory
- mutate permissions
- write audit records
- perform network actions
- execute commands
- execute tools
- mutate arbitrary files
- activate voice, vision, or avatar runtime
- start background services
- open release gates
- perform autonomous actions

## Commands

The following read-only commands are available:

    partner-runtime-personality-consistency-status
    partner-runtime-personality-consistency-context
    partner-runtime-personality-consistency-check

CLI and shell routes expose identical deterministic packets.

## Validation contract

The Sprint 225 planner validates 96 assertions.

Required properties include:

- canonical identity and persona ownership
- supported identity version
- required traits and modes
- exact persona-style items
- Sprint 224 fusion baseline preserved
- canonical browser-chat session ownership preserved
- Expression Language remains secondary and uninstantiated
- personality profile is deterministic and payload-free
- runtime false flags remain false
- no persistence or execution authority
- runtime activation and release gates remain closed

## Next boundary

Sprint 226 — Multi-Interface State Synchronization

Canonical boundary identifier:

    multi_interface_state_synchronization
