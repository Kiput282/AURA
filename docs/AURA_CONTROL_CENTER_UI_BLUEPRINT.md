# AURA Control Center UI Blueprint

Target version: v0.86.0-genesis  
Status: CONTROL CENTER UI BLUEPRINT ONLINE

## Purpose

AURA Control Center UI Blueprint prepares planner-only metadata for the future AURA Genesis Console.

It prepares:

- Genesis Dashboard blueprint
- Permission Center blueprint
- Service Monitor blueprint
- Launcher Control blueprint
- Capability Viewer blueprint
- Chat Console placeholder
- Plugin Dashboard blueprint
- Action Log blueprint
- Roadmap Viewer direction
- Control Center safety policy

This sprint does not create a frontend app, backend service, web route, browser window, UI runtime, web server runtime, chat runtime, service runtime, launcher runtime, or plugin runtime.

## Core Rule

AURA Control Center may show visibility, but it must not control runtime yet.

The Control Center must not bypass:

- Capability Registry
- Unified Permission Workflow
- Runtime Service Foundation
- Launcher & Health Monitor Foundation
- safe_idle policy

## Current Blueprint Summary

- blueprint plan types: 11
- UI panels: 9
- navigation items: 9
- Permission Center cards: 9
- Service Monitor cards: 10
- Launcher Control cards: 6
- Capability Viewer cards: 7
- runtime-enabled panels: 0
- frontend apps created: 0
- backend services created: 0
- web routes created: 0
- ports bound: 0
- browser windows opened: 0
- runtime execution features: 0

## Planned UI Panels

- Genesis Dashboard
- Permission Center
- Service Monitor
- Launcher Control
- Capability Viewer
- Chat Console Placeholder
- Plugin Dashboard
- Action Log
- Roadmap Viewer

## Planned Identity

- UI name: AURA Control Center
- Console name: Genesis Console
- Server: ATLAS
- Default mode: safe_idle_visibility_only
- Runtime mode: blueprint_only
- Auto-action allowed: false

## Safety Boundary

This sprint is control-center-blueprint-only, UI-blueprint-only, planner-only, proposal-only, metadata-only, and safe-idle-visibility-only.

It does not enable UI runtime, frontend runtime, backend runtime, web server runtime, route creation runtime, port binding, browser launch, chat runtime, service runtime, launcher runtime, health monitor runtime, plugin runtime, permission grant runtime, runtime action activation, runtime behavior changes, process start, systemctl execution, systemd start, log file read/write, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git execution, external action execution, or real tool execution.

## Future Direction

Sprint 87 can build on this blueprint with Local Console Web Foundation planning.

The future web console must remain local-first, permission-first, safe_idle-first, and unable to bypass the permission workflow.
