# AURA Chat Bridge & Session State Foundation

Target version: v0.88.0-genesis  
Status: CHAT BRIDGE & SESSION STATE FOUNDATION ONLINE

## Purpose

AURA Chat Bridge & Session State Foundation prepares planner-only metadata for future chat bridge and session state handling.

It prepares:

- conversation session metadata
- message flow blueprint planning
- Control Center chat panel bridge planning
- Local Console session contract planning
- permission-aware chat action boundary planning
- chat context persistence blueprint planning
- websocket boundary planning
- session recovery blueprint planning
- chat bridge safety policy

This sprint does not start chat runtime, conversation runtime, session runtime, websocket runtime, web server runtime, frontend/backend/API runtime, send messages, receive messages, persist sessions, grant permissions, activate runtime actions, run model inference, bind ports, write session files, execute tools, or perform external actions.

## Core Rule

AURA Chat Bridge may prepare session metadata, but it must not run chat runtime yet.

The future chat bridge must be:

- safe_idle-first
- permission-aware
- session-metadata-first
- Control Center compatible
- Local Console compatible
- unable to bypass the Unified Permission Workflow
- unable to bypass the Capability Registry

## Current Summary

- chat bridge plan types: 11
- chat channels: 5
- session state fields: 12
- message flow steps: 8
- permission action boundary rules: 10
- session events: 8
- runtime-enabled channels: 0
- chat sessions started: 0
- messages sent: 0
- messages received: 0
- websocket servers started: 0
- session files written: 0
- runtime execution features: 0

## Planned Chat Channels

- CLI Chat Placeholder
- Shell Chat Placeholder
- Control Center Chat Panel
- Local Console Chat Panel
- Future Voice Chat Bridge

These are channel blueprints only. No chat runtime is created.

## Planned Session Identity

- bridge name: AURA Chat Bridge
- session layer name: AURA Session State Foundation
- control center panel: Chat Console Placeholder
- local console route: /chat
- server: ATLAS
- default mode: safe_idle_required
- runtime mode: blueprint_only
- auto-action allowed: false

## Permission-Aware Boundary

The chat bridge must not execute actions directly.

Action intent from a future chat session must be routed to:

- Capability Registry
- Unified Permission Workflow
- Shared Output Formatter
- Runtime Service Foundation
- Launcher & Health Monitor Foundation
- Local Console Web Foundation

Chat must not grant permission by itself.

## Safety Boundary

This sprint is chat-bridge-foundation-only, session-state-foundation-only, chat-blueprint-only, session-blueprint-only, planner-only, proposal-only, metadata-only, permission-aware, and safe-idle-required.

It does not enable chat runtime, conversation runtime, session runtime, session persistence runtime, message send/receive runtime, websocket runtime, websocket server start, web server runtime, frontend runtime, backend runtime, API runtime, port binding, browser launch, model inference runtime activation, tool call runtime, permission grant runtime, runtime action activation, runtime behavior changes, service runtime, launcher runtime, plugin runtime, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git execution, external action execution, or real tool execution.

## Future Direction

Sprint 89 can build on this foundation with Plugin/Permission Dashboard Foundation.

The future dashboard should make chat-originated action requests visible, reviewable, and permission-gated before any runtime activation exists.
