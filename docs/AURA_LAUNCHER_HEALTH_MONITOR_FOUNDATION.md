# AURA Launcher & Health Monitor Foundation

Target version: v0.85.0-genesis  
Status: LAUNCHER HEALTH MONITOR FOUNDATION ONLINE

## Purpose

AURA Launcher & Health Monitor Foundation prepares planner-only launcher and monitor metadata for future ATLAS-hosted AURA service visibility.

It prepares:

- safe_idle launcher planning
- start plan
- stop plan
- restart plan
- status plan
- log view plan
- health monitor plan
- Control Center service monitor plan
- launcher safety policy plan

This sprint does not start, stop, restart, or control any real process or service.

## Core Rule

AURA may prepare launcher and monitor visibility, but AURA must not control runtime yet.

Launcher planning must remain safe_idle-first.

## Current Summary

- launcher plan types: 10
- launcher modes: 4
- launcher actions: 6
- health states: 5
- monitor fields: 12
- runtime-enabled launchers: 0
- processes started: 0
- processes stopped: 0
- processes restarted: 0
- systemctl commands executed: 0
- log files read: 0
- runtime execution features: 0

## Planned Launcher Identity

- launcher name: aura-launcher
- display name: AURA Launcher & Health Monitor
- server: ATLAS
- default launch mode: safe_idle
- default monitor mode: metadata_only
- service name: aura.service
- auto-action allowed: false

## Safety Boundary

This sprint is launcher-foundation-only, health-monitor-foundation-only, planner-only, proposal-only, metadata-only, and safe_idle-required.

It does not enable launcher runtime, health monitor runtime, service runtime, process start/stop/restart, background process start, systemctl execution, systemd enable/start/stop/restart, service control runtime, log file read/write, auto-boot runtime, port binding, web server runtime, UI runtime, chat runtime, permission grant runtime, runtime action activation, runtime behavior changes, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git execution, external action execution, or real tool execution.

## Future Direction

Sprint 86 can build on this foundation with AURA Control Center UI Blueprint.

The Control Center may show launcher and service monitor cards, but it must not bypass the permission workflow or control runtime.
