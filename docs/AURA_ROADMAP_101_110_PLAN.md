# AURA Roadmap 101–110 Plan

Status: DRAFT SEED
Phase: Genesis Runtime Readiness
Source: Sprint 100 Review & Stabilization
Version seed: v0.100.0-genesis

## Principle

Sprint 101–110 should bridge AURA from foundation-only systems toward controlled runtime readiness without enabling unsafe automatic action execution.

The block must remain:

- safe_idle-first
- permission-first
- local-first
- reviewable
- capability-aware
- runtime-gated
- dry-run-first
- audit-visible

## Proposed Sprint Seed

### Sprint 101 — Genesis Runtime Readiness Baseline

Prepare a baseline readiness layer for deciding which foundation systems may become dry-run or runtime candidates.

No runtime execution.

### Sprint 102 — Safe Runtime Configuration Profile

Define configuration profiles for local-safe runtime modes, still disabled by default.

No runtime execution.

### Sprint 103 — Local Service Start Proposal Review

Prepare proposal review for starting local services, ports, and dashboard processes.

No service start runtime.

### Sprint 104 — Dashboard API Contract Consolidation

Consolidate Control Center, status, plugin, permission, and queue API contracts.

No API server runtime.

### Sprint 105 — Permission Decision Runtime Dry-Run

Prepare dry-run simulation of permission grant/deny decisions.

No actual permission grant or deny runtime.

### Sprint 106 — Controlled File Write Dry-Run Renderer

Prepare dry-run file write preview renderer using proposal metadata.

No file read/write/modify/delete runtime.

### Sprint 107 — Runtime Action Queue Dry-Run Simulator

Prepare a dry-run simulator for queue state transitions.

No queue persistence, dispatch, or execution runtime.

### Sprint 108 — ORION Client Handshake Blueprint

Prepare handshake blueprint for future ATLAS–ORION connection.

No ORION client connection runtime.

### Sprint 109 — End-to-End Preflight Review

Prepare cross-system preflight review across permissions, file write, queue, web gate, and ORION boundary.

No runtime preflight execution.

### Sprint 110 — Review & Stabilization 101–110

Review the 101–110 block and decide next safe runtime direction.

No automatic runtime execution.

## Deferred Until Explicit Approval

- actual dashboard server
- actual API server
- actual websocket runtime
- actual permission mutation
- actual file write execution
- actual action dispatch/execution
- actual ORION connection
- actual screen/voice runtime
- actual plugin/tool execution
- actual desktop control
- actual memory write runtime
