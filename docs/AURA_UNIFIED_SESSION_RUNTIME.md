# AURA Unified Session Runtime

Version: v0.221.0-genesis
Sprint: 221 — Unified Session Runtime
Status: COMPLETED — CONTRACT-ONLY

## Purpose

Sprint 221 begins the Sprint 221-230 Unified Partner Runtime Integration
block.

It provides a deterministic partner-facing session contract without
replacing or bypassing the existing browser chat session runtime.

## Canonical Session Ownership

Canonical owner:

    aura_browser_chat_session_runtime

The existing browser runtime continues to own:

- chat session identifiers
- message identifiers
- revision and optimistic conflict handling
- integrity verification
- bounded persistence
- idempotent client-message replay
- existing create, submit, reload, and clear rules

Sprint 221 introduces no second session store, identifier format,
revision implementation, or integrity implementation.

## Components

    aura/partner_runtime/partner_runtime_planning_manager.py
    aura/partner_runtime/partner_runtime_planner.py
    aura/partner_runtime/partner_runtime_alpha_manager.py

The legacy planning manager remains metadata-only.

The Sprint 221 planner exposes the unified-session contract.

The alpha manager exposes bounded status, context, and check visibility
while runtime authority remains disabled.

## Commands

    partner-runtime-unified-session-status
    partner-runtime-unified-session-context
    partner-runtime-unified-session-check

## Validation

- Planner assertion count: 51
- Planner failed assertion count: 0
- Alpha failed assertion count: 0
- Deterministic planner status: true
- Deterministic alpha status: true
- Canonical session owner: aura_browser_chat_session_runtime
- Legacy snapshot mode: static_safety_boundary
- Legacy dependency traversal: false
- Journal accessed: false
- Temporary session storage created: false
- Runtime ready: false
- Execution ready: false

Capability Registry remains unchanged:

- Total capabilities: 121
- Online capabilities: 119
- Foundation-only capabilities: 78
- Planner-only capabilities: 7
- Permission-gated capabilities: 12
- Review-only capabilities: 11
- Disabled runtime capabilities: 2
- Runtime execution features: 4

## Safety Boundary

Sprint 221 does not create or mutate sessions, write long-term memory,
read project-journal history, mutate permissions, create grants, write
audit events, dispatch or execute actions, execute tools or commands,
mutate arbitrary files, launch applications, control the desktop, use
network or Git actions, open runtime or release gates, start background
services, bind public or LAN interfaces, install dependencies, download
models, or perform autonomous actions.

## Next Sprint

Sprint 222 — Workspace and Project Context Runtime
