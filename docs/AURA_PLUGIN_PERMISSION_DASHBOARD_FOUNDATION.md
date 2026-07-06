# AURA Plugin / Permission Dashboard Foundation

Target version: v0.89.0-genesis  
Status: PLUGIN / PERMISSION DASHBOARD FOUNDATION ONLINE

## Purpose

AURA Plugin / Permission Dashboard Foundation prepares planner-only metadata for plugin/action visibility, permission request visibility, chat-originated action request visibility, capability-permission matrix planning, Control Center dashboard bridge planning, Local Console dashboard contract planning, and audit trail dashboard blueprint planning.

It prepares:

- plugin registry dashboard planning
- permission request dashboard planning
- permission decision visibility planning
- chat-originated action visibility planning
- capability-permission matrix planning
- Control Center dashboard bridge planning
- Local Console dashboard contract planning
- audit trail dashboard blueprint planning
- dashboard safety policy

This sprint does not enable plugin runtime, install plugins, enable plugins, disable plugins, execute plugin actions, grant permissions, deny permissions, resolve permission requests, activate runtime actions, execute chat-originated actions, call tools, run service/launcher/chat/session/web/frontend/backend/API runtime, create routes, bind ports, read logs, write logs, perform file operations, execute commands, or perform external actions.

## Core Rule

AURA Plugin / Permission Dashboard may show plugin and permission visibility, but it must not execute actions or grant permissions.

The dashboard must be:

- visibility-only
- permission-aware
- safe_idle-first
- Control Center compatible
- Local Console compatible
- chat-action-review aware
- unable to bypass the Unified Permission Workflow
- unable to bypass the Capability Registry

## Current Summary

- dashboard plan types: 11
- dashboard panels: 8
- plugin dashboard cards: 9
- permission dashboard cards: 10
- chat action visibility fields: 8
- capability-permission matrix fields: 8
- audit trail fields: 8
- dashboard filters: 7
- runtime-enabled panels: 0
- plugin actions executed: 0
- permission requests resolved: 0
- permissions granted: 0
- permissions denied: 0
- chat-originated actions executed: 0
- dashboard routes created: 0
- web panels rendered: 0
- runtime execution features: 0

## Planned Dashboard Panels

- Plugin Registry
- Plugin Action Detail
- Permission Request Queue
- Permission Decision Review
- Chat-Originated Actions
- Capability Permission Matrix
- Audit Trail Blueprint
- Dashboard Safety Boundary

These are dashboard blueprints only. No UI runtime, web runtime, plugin runtime, or permission runtime is created.

## Planned Dashboard Identity

- dashboard name: AURA Plugin / Permission Dashboard
- control center panel: Plugin & Permission Dashboard
- local console route: /plugins
- permission center panel: Permission Center
- server: ATLAS
- default mode: safe_idle_required
- runtime mode: blueprint_only
- auto-action allowed: false

## Permission-Aware Boundary

The dashboard must not grant or deny permissions directly.

Permission decisions from future UI controls must remain routed to:

- Unified Permission Workflow
- Capability Registry
- Shared Output Formatter
- Control Center UI Blueprint
- Local Console Web Foundation
- Chat Bridge & Session State Foundation

Chat-originated action requests must remain review-only until future explicit runtime layers exist.

## Safety Boundary

This sprint is plugin-permission-dashboard-foundation-only, plugin-dashboard-blueprint-only, permission-dashboard-blueprint-only, dashboard-visibility-only, planner-only, proposal-only, metadata-only, permission-aware, and safe-idle-required.

It does not enable plugin runtime, plugin enable/disable/install runtime, plugin action execution, permission grant runtime, permission deny runtime, permission decision runtime, runtime action activation, runtime behavior changes, chat action execution, tool call runtime, tool execution, service runtime, launcher runtime, chat runtime, session runtime, web server runtime, frontend runtime, backend runtime, API runtime, route creation runtime, port binding, browser launch, log file read/write, file operations, command execution, dependency install, package download, internet/network action, memory write, desktop control, git execution, external action execution, or real tool execution.

## Future Direction

Sprint 90 can perform the 81–90 review and stabilization checkpoint.

The checkpoint should review Control Center readiness, Local Console readiness, Chat Bridge readiness, Plugin/Permission Dashboard readiness, and remaining gaps before any future runtime activation.
