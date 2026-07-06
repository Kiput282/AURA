# AURA Capability Registry Consolidation

Target version: v0.82.0-genesis  
Status: CAPABILITY REGISTRY ONLINE

## Purpose

The Capability Registry provides a central planner-only metadata layer for describing what AURA can do, what is only a foundation, what is planner-only, what requires permission, what is review-only, what is planned, and what is currently disabled as runtime action.

This registry prepares capability data for:

- CLI
- shell
- system status
- future service monitor
- future launcher
- future AURA Control Center
- future plugin and permission dashboards

## Current Capability Summary

| Metric | Count |
|---|---:|
| Total capabilities tracked | 18 |
| Online capabilities | 12 |
| Foundation-only capabilities | 3 |
| Planner-only capabilities | 6 |
| Permission-gated planner capabilities | 2 |
| Review-only capabilities | 1 |
| Planned future capabilities | 4 |
| Disabled runtime capabilities | 2 |
| Runtime execution features | 0 |

## Online Capabilities

AURA currently tracks these online capabilities:

- Thought Loop Planner
- Reasoning Context Manager
- Knowledge Uncertainty & Internet Search Gate
- Voice Input Runtime Foundation
- Voice Intent Understanding Layer
- Vision Input Runtime Foundation
- Visual Context Understanding Layer
- Coder Project Generation Planner
- Dependency & Download Permission Gate
- Review & Stabilization 71-80
- Shared Output Formatter
- Capability Registry Consolidation

## Planned Future Capabilities

Tracked as planned, not active runtime:

- Unified Permission Workflow Manager
- AURA Runtime Service Foundation
- AURA Launcher & Health Monitor
- AURA Control Center

## Disabled Runtime Capabilities

Tracked as deferred and locked:

- Controlled File Write Runtime
- Controlled Command Execution Runtime

These are intentionally deferred to the Sprint 91-100 block unless explicitly reprioritized.

## Permission Categories

The registry tracks permission categories such as:

- read_project
- user_confirmation
- microphone_permission
- camera_permission
- screen_permission
- file_write_permission
- command_execution_permission
- dependency_download_permission
- internet_search_permission
- desktop_control_permission
- git_operation_permission

The registry only describes permission requirements. It does not grant permission.

## Control Center Use

The future AURA Control Center can use this registry to show:

- capability name
- current state
- runtime level
- risk level
- required permission
- introduced version
- category
- whether a capability is visible in the Control Center

Important rule:

The Control Center may display capability status, but it must not enable capabilities without the future Unified Permission Workflow.

## Safety Boundary

This sprint is registry-only, planner-only, proposal-only, and metadata-only.

It does not enable:

- runtime behavior changes
- automatic capability enablement
- dynamic runtime discovery
- runtime action activation
- permission grant runtime
- UI runtime
- web server runtime
- chat runtime
- service runtime
- launcher runtime
- file operations
- command execution
- test execution
- code execution
- dependency install
- package download
- internet or network action
- tool execution
- memory write
- desktop control
- git execution
- external action execution
- real tool execution

## Design Principle

AURA must know her capabilities clearly before she is allowed to perform runtime actions.
