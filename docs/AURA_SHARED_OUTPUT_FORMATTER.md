# AURA Shared Output Formatter Foundation

Target version: v0.81.0-genesis  
Status: SHARED OUTPUT FORMATTER ONLINE

## Purpose

The Shared Output Formatter provides a reusable renderer-only formatting layer for AURA CLI, shell, future service monitor output, and the future AURA Control Center.

This foundation exists to reduce repeated packet-printing logic across managers, CLI commands, shell commands, service monitor output, and future UI bridges.

## Current Capabilities

AURA can now plan and provide shared rendering helpers for:

- title/header rendering
- key-value packet rendering
- compact list/dictionary summaries
- safety boundary rendering
- CLI output format planning
- shell output format planning
- future console output format planning
- future UI output contract planning
- formatter migration planning

## Current Runtime Boundary

This sprint is renderer-only and foundation-only.

It does not enable:

- runtime behavior change
- automatic CLI refactor
- automatic shell refactor
- UI runtime
- web server runtime
- chat runtime
- service runtime
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

## Future Use

The formatter is intended to support:

- AURA CLI
- AURA shell
- AURA service monitor
- AURA launcher
- AURA Control Center dashboard
- Chat console status blocks
- Permission center request details
- Plugin manager capability summaries
- Action log detail views

## Migration Notes

Formatter migration should be gradual:

1. Use shared formatter for new commands first.
2. Migrate checkpoint and permission-style packet printers.
3. Migrate repeated CLI packet helpers.
4. Migrate repeated shell packet helpers.
5. Reuse formatted output in service monitor and Control Center bridges.
6. Avoid changing command semantics during migration.

## Design Principle

Format once, reuse across CLI, shell, service monitor, and future Control Center.

The formatter may display safety and capability information, but it must not convert display rendering into permission approval or runtime action.
