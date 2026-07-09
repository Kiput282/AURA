# AURA Service Recovery and Restart Policy Foundation

Version: v0.148.0-genesis  
Sprint: 148.0  
Status: Foundation-only / planner-only / metadata-only  
Runtime state: disabled by design

## Purpose

Sprint 148 defines the future service recovery and restart policy foundation for AURA on ATLAS. It prepares failure classification, safe-idle recovery policy, restart approval policy, retry cooldown policy, rollback visibility, Control Center recovery surfaces, permission links, audit links, and no recovery/restart runtime activation review.

## Runtime boundary

This sprint does not start, stop, or restart services. It does not create retry timers, write recovery state, modify configuration, modify files, revert git, call systemd, execute shell commands, open sockets, bind ports, probe networks, dispatch actions, execute tools/commands, use ORION, or enable runtime execution features.

## Safety counters

- Runtime recovery state writes: 0
- Runtime restart commands executed: 0
- Runtime retry timers started: 0
- Runtime retry loops started: 0
- Runtime rollback files modified: 0
- Runtime config files modified: 0
- Runtime git reverts executed: 0
- Runtime systemd commands executed: 0
- Runtime service process restarts: 0
- Runtime execution features: 0

## Next step

Sprint 149.0 — Service Security and Localhost Binding Review.
