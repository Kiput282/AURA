# AURA Runtime Service Foundation

Target version: v0.84.0-genesis  
Status: RUNTIME SERVICE FOUNDATION ONLINE

## Purpose

AURA Runtime Service Foundation prepares planner-only service metadata for future ATLAS-hosted AURA service behavior.

It prepares:
- safe_idle boot planning
- service lifecycle planning
- service health check planning
- systemd unit blueprint planning
- service recovery planning
- service monitor view planning
- auto-boot policy planning
- future AURA Control Center service monitor data

## Core Rule

AURA may wake automatically in the future, but only in safe_idle.

AURA must not act automatically.

## Current Summary

- service plan types: 9
- boot modes: 4
- lifecycle states: 9
- health check fields: 11
- runtime-enabled services: 0
- systemd units created: 0
- background processes started: 0
- auto-boot runtime enabled: 0
- runtime execution features: 0

## Planned Service Identity

- service name: aura.service
- display name: AURA Runtime Service
- server: ATLAS
- default boot mode: safe_idle
- default runtime mode: locked
- auto-action allowed: false

## Safety Boundary

This sprint is service-foundation-only, planner-only, proposal-only, metadata-only, and safe_idle-required.

It does not enable service runtime, systemd unit creation, systemd enable/start/stop/restart, background process start, auto-boot runtime, port binding, web server runtime, UI/chat/launcher runtime, service control runtime, permission grant runtime, runtime action activation, runtime behavior changes, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git execution, external action execution, or real tool execution.
