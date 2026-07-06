# AURA Local Console Web Foundation

Target version: v0.87.0-genesis  
Status: LOCAL CONSOLE WEB FOUNDATION ONLINE

## Purpose

AURA Local Console Web Foundation prepares planner-only metadata for a future local-only web console that can host the AURA Control Center / Genesis Console.

It prepares:

- localhost-only policy planning
- route blueprint planning
- API contract blueprint planning
- static asset blueprint planning
- session state blueprint planning
- security boundary planning
- Control Center web bridge planning
- developer console access planning

This sprint does not start a web server, bind ports, create live routes, serve static files, open a browser, create frontend/backend runtime, enable API runtime, enable session runtime, or allow public/LAN/remote access.

## Core Rule

AURA Local Console may prepare local visibility, but it must not run web runtime yet.

The future console must be:

- local-first
- localhost-only
- safe_idle-first
- permission-first
- unable to bypass the Unified Permission Workflow

## Current Summary

- web foundation plan types: 10
- local host policies: 6
- route blueprints: 9
- API contracts: 8
- static asset groups: 6
- session state fields: 7
- runtime-enabled routes: 0
- runtime-enabled APIs: 0
- web servers started: 0
- ports bound: 0
- frontend apps created: 0
- backend services created: 0
- routes created: 0
- static files served: 0
- sessions started: 0
- browser windows opened: 0
- runtime execution features: 0

## Planned Local Console Identity

- console name: AURA Local Console
- control center name: AURA Control Center
- genesis console name: Genesis Console
- server: ATLAS
- default host policy: localhost_only
- default runtime mode: blueprint_only
- auto-action allowed: false

## Planned Routes

- /
- /permissions
- /service
- /launcher
- /capabilities
- /plugins
- /chat
- /logs
- /roadmap

These are route blueprints only. No route runtime is created.

## Planned API Contracts

- /api/status
- /api/capabilities
- /api/permissions
- /api/service
- /api/launcher
- /api/control-center
- /api/plugins
- /api/health

These are API contracts only. No backend or endpoint runtime is created.

## Safety Boundary

This sprint is local-console-web-foundation-only, web-blueprint-only, local-only-policy, planner-only, proposal-only, metadata-only, and safe-idle-visibility-only.

It does not enable web server runtime, frontend runtime, backend runtime, route creation runtime, API runtime, static file serving, session runtime, port binding, browser launch, public network bind, LAN network bind, remote access, websocket runtime, chat runtime, UI runtime, service runtime, launcher runtime, permission grant runtime, runtime action activation, runtime behavior changes, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git execution, external action execution, or real tool execution.

## Future Direction

Sprint 88 can build on this foundation with Chat Bridge & Session State Foundation.

The future web console must not enable chat runtime until chat bridge/session state safety exists.
