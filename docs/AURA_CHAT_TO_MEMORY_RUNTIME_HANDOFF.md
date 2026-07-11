# AURA Chat-to-Memory Runtime Handoff

Version: `0.223.0-genesis`
Sprint: `223`
Block: `Sprint 221-230 — Unified Partner Runtime Integration`
Runtime state: contract-only, preview-only, inactive

## Purpose

The Chat-to-Memory Runtime Handoff connects explicit user memory intent to
AURA's existing memory safety contracts without enabling automatic memory
extraction or persistence.

It is a partner-runtime integration facade, not a live memory writer.

## Components

### ChatToMemoryRuntimeHandoffPlanner

Location:

    aura/partner_runtime/chat_to_memory_runtime_handoff_planner.py

Responsibilities:

- preserve the Sprint 222 workspace and project context contract
- preserve the canonical browser chat session owner
- compose existing handoff, privacy, review, and permission status contracts
- verify default-deny memory-write behavior
- verify runtime counters remain zero
- expose deterministic status, context, plan, and check views
- keep runtime activation disabled

### ChatToMemoryRuntimeHandoffAlphaManager

Location:

    aura/partner_runtime/chat_to_memory_runtime_handoff_alpha_manager.py

Responsibilities:

- provide a read-only facade over the Sprint 223 planner
- expose status, context, and contract checks
- report 65 assertions
- retain preview-only and contract-only behavior
- expose no memory-write authority

## Existing contract owners

Sprint 223 does not replace the existing domain owners.

The composed contracts remain:

- `AuraChatToMemoryHandoffContractManager`
- `AuraMemoryPrivacyRedactionLayerManager`
- `AuraMemoryReviewQueueManager`
- `AuraMemoryWritePermissionGateManager`

The facade calls their read-only `status()` surfaces only. It does not call
their preview, creation, review-decision, permission-application, or runtime
execution methods.

## Canonical session ownership

The canonical session owner remains:

    aura_browser_chat_session_runtime

Sprint 223 does not create another chat-session store, scan chat history,
retrieve stored turns, or consume chat runtime events.

## Handoff eligibility

The contract requires:

- an explicit user request to remember something
- one directly supplied user turn
- no assistant, system, or tool-message handoff
- privacy review
- manual review
- permission review after privacy review
- default-deny behavior without a grant
- a one-shot memory-write grant
- permission expiry

These are contract requirements only. No live grant is created or consumed.

## Persistence boundary

Sprint 223 does not persist:

- a chat-to-memory handoff
- a memory candidate
- a redacted candidate
- a review-queue item
- a review decision
- a permission request
- a permission grant
- an audit event
- a memory record

`MemoryStore` is not imported or constructed by the Sprint 223 planner.

## Runtime-data boundary

The contract does not read:

- `data/chat_sessions`
- `data/conversations/chat_history.jsonl`
- `data/journal/aura_journal.jsonl`
- `data/memory/memories.jsonl`

The only project inspection inherited from Sprint 222 remains bounded,
read-only, and non-recursive.

## CLI and shell commands

The following read-only commands are available:

    partner-runtime-chat-to-memory-handoff-status
    partner-runtime-chat-to-memory-handoff-context
    partner-runtime-chat-to-memory-handoff-check

## Safety properties

Sprint 223 does not:

- scan chat history
- perform automatic memory extraction
- write or delete memory
- mutate the memory store
- persist review or permission state
- apply or consume grants
- write audit records
- dispatch model requests
- perform network requests
- execute commands or tools
- mutate arbitrary files
- start background services
- activate runtime execution
- open release gates
- perform autonomous actions

## Validation contract

The Sprint 223 planner validates 65 assertions.

Required final properties include:

- Sprint 223 current boundary
- Sprint 224 next boundary
- Sprint 222 contract preserved at 52 assertions
- canonical session owner preserved
- all four memory-safety dependency contracts ready
- explicit memory intent required
- privacy and manual review required
- default-deny and one-shot permission behavior preserved
- all runtime counters zero
- no runtime data reads or persistence
- no memory-store mutation
- all safety blockers inactive

## Next boundary

Sprint 224 — Voice, Vision, and Chat Context Fusion

Canonical boundary identifier:

    voice_vision_chat_context_fusion
