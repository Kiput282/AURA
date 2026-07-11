# AURA Workspace and Project Context Runtime

Version: `0.222.0-genesis`
Sprint: `222`
Block: `Sprint 221-230 — Unified Partner Runtime Integration`
Runtime state: contract-only, read-only, inactive

## Purpose

The Workspace and Project Context Runtime provides a bounded bridge between
the Sprint 221 Unified Session Runtime and stable project metadata.

It does not attempt full repository understanding. It establishes a safe,
deterministic contract that later partner-runtime stages can consume.

## Components

### WorkspaceProjectContextPlanner

Location:

    aura/partner_runtime/workspace_project_context_planner.py

Responsibilities:

- preserve the Sprint 221 unified session contract
- identify the canonical project root
- read the approved identity source
- read bounded Git HEAD metadata without executing Git
- list only top-level workspace entries
- check availability of explicitly approved context sources
- expose a static legacy workspace safety boundary
- validate the contract through deterministic assertions

### WorkspaceProjectContextAlphaManager

Location:

    aura/partner_runtime/workspace_project_context_alpha_manager.py

Responsibilities:

- expose status, context, and check views
- retain contract-only behavior
- keep runtime activation disabled
- provide zero-authority integration output for CLI and shell surfaces

## Canonical ownership

The canonical session owner remains:

    aura_browser_chat_session_runtime

Sprint 222 does not introduce another session store, session ID format, or
session lifecycle owner.

## Bounded context sources

The planner checks only the approved sources declared in its contract,
including the project README, entry point, identity, CLI, shell, activation
roadmap, and Unified Session Runtime document.

File contents are not bulk-loaded as a repository context corpus.

## Workspace inspection boundary

Workspace inspection is limited to the project root at depth one.

The following categories are excluded from the workspace listing:

- `.git`
- `.venv`
- `data`
- `logs`
- `__pycache__`

Recursive scans are not performed.

## Legacy workspace boundary

`WorkspaceAwarenessManager` is not imported or constructed by Sprint 222.

Its legacy dependency graph includes journal, memory, reflection, coding, and
plugin components. Sprint 222 records only static source metadata confirming
that the legacy manager exists while leaving all of its runtime methods unused.

## Safety properties

Sprint 222 does not:

- read journal entries
- read or write memory
- persist workspace context
- recursively scan the repository
- mutate browser chat sessions
- modify permissions
- write audit records
- execute local actions, commands, or tools
- perform Git or network actions
- control desktop applications
- start background services
- activate runtime execution
- open release gates
- perform autonomous actions

## CLI and shell commands

The following read-only commands are available:

    partner-runtime-workspace-project-context-status
    partner-runtime-workspace-project-context-context
    partner-runtime-workspace-project-context-check

## Validation contract

The Sprint 222 planner validates 52 assertions.

Required final properties include:

- contract ready
- runtime disabled
- Sprint 222 current boundary
- Sprint 223 next boundary
- Sprint 221 session contract preserved
- canonical session owner preserved
- bounded scan depth
- no recursive scan
- no journal or memory access
- no persistence or mutation
- all safety blockers inactive

## Next boundary

Sprint 223 — Chat-to-Memory Runtime Handoff

Canonical boundary identifier:

    chat_to_memory_runtime_handoff
