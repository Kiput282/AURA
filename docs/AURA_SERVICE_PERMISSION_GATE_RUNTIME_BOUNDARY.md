# AURA Service Permission Gate Runtime Boundary

Version seed: v0.145.0-genesis  
Sprint: 145.0  
Status: completed  
Runtime state: disabled by design

## Purpose

Sprint 145 defines the planner-only service permission gate runtime boundary for AURA's future ATLAS local service runtime.

It prepares metadata contracts for service permission scopes, permission request shape, grant preflight, denial-to-safe-idle behavior, Control Center visibility, audit linkage, grant expiry review, error handling, manual approval boundary, and no-permission-runtime-activation review.

## Safety boundary

Sprint 145 does not create permission requests, apply grants, revoke grants, mutate permission state, read or write permission stores, start services, bind ports, open sockets, start HTTP listeners, write audit events, dispatch actions, execute tools or commands, read/write files, connect ORION, or enable runtime execution features.

## Current counters

- Runtime permission requests created: 0
- Runtime permission grants applied: 0
- Runtime permission mutations: 0
- Runtime permission store writes: 0
- Runtime audit events written: 0
- Runtime services started: 0
- Runtime ports bound: 0
- Runtime execution features: 0

## Next sprint

Sprint 146 — Service Audit Link Foundation.
