# AURA

Local-first AI partner by Kiput.

AURA is a long-term AI companion project designed to grow into a local-first anime-girl virtual partner for work, creativity, livestreaming, game companionship, translation assistance, and safe desktop collaboration.

AURA is currently in the Genesis Runtime Readiness phase.

Current version: v0.123.0-genesis  
Current status: foundation-only, planner-only, review-only  
Current runtime state: disabled by design

---

## What is AURA?

AURA is not intended to be a stiff robot assistant.

AURA is being designed as a local AI partner with:

- warm anime-girl companion personality
- serious debug and development support
- future voice interaction
- future screen and vision awareness with permission
- future dashboard and control center
- future avatar and livestream presence
- future ORION client for desktop, game, avatar, and runtime interaction
- safety-first permission and audit boundaries

The guiding motto is:

Grow Together

---

## Current Project Status

AURA has completed the Sprint 111-120 runtime readiness block.

Latest completed checkpoint:

- v0.123.0-genesis
- Sprint 120: Review Stabilization 111-120 Foundation
- Sprint 111-120 block: closed
- Next planned sprint: Sprint 121.0 — Post-Checkpoint 120 Next Block Planning Foundation

Current capability registry summary:

- total capabilities: 51
- online capabilities: 49
- foundation-only capabilities: 38
- planner-only capabilities: 7
- permission-gated capabilities: 2
- review-only capabilities: 2
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

---

## Safety State

AURA currently does not execute real runtime actions.

Disabled by design:

- no release gate opening
- no v1 runtime activation
- no autonomous desktop control
- no arbitrary shell execution
- no tool execution runtime
- no command execution runtime
- no file read/write/modify/delete runtime
- no service start runtime
- no port binding runtime
- no network probe runtime
- no ORION runtime handshake
- no dashboard runtime start
- no memory write runtime
- no git runtime

AURA can plan, review, summarize, document, and prepare safe boundaries.  
AURA cannot yet act freely.

---

## Architecture Overview

AURA is split into two major machine roles.

### ATLAS

ATLAS is the main AURA core server.

Responsibilities:

- main planner
- capability registry
- skill registry
- plugin action registry
- permission planning
- audit planning
- roadmap and documentation
- dashboard/control-center data planning
- safety boundary planning
- long-term AURA brain

Current code location:

    /home/kiput/Projects/AURA

Large data storage:

    /mnt/aura-data/AURA

### ORION

ORION is the future runtime client.

Planned responsibilities:

- desktop client
- avatar/render client
- screen/camera/audio runtime client
- livestream presentation client
- Minecraft/game runtime client
- local action runtime client

Boundary:

- ATLAS remains the final authority.
- ORION must not bypass permission gates.
- ORION runtime remains disabled until future review permits it.

---

## Product Direction

The active product direction is documented in:

- docs/AURA_PRODUCT_DIRECTION_NOTE.md

Key direction:

- AURA should feel like an anime-girl companion, not a stiff robot.
- AURA should support serious work and relaxed interaction.
- AURA should eventually support two YouTube directions:
  - AURA livestream/content channel
  - AURA development/devlog channel
- AURA should support future Game Companion Mode.
- Minecraft should use legal telemetry, mod, or plugin data, not cheats.
- Relaxed Translator Mode is planned after the v1 core.
- Dashboard runtime should likely start after Sprint 130 if prioritized.

---

## Planned Interaction Modes

Future AURA modes include:

- Companion Mode
- Serious Debug Mode
- Devlog Narrator Mode
- Livestream Host Mode
- Game Companion Mode
- Relaxed Translator Mode
- Creative Studio Mode

These modes are product direction targets.  
They are not all active runtime features yet.

---

## v1.0.0 Direction

AURA v1.0.0 should focus on becoming usable as a safe local AI partner.

Preferred v1 scope:

- local chat
- personality-aware responses
- voice interaction foundation
- permission-gated screen and vision awareness
- dashboard chat/status foundation
- active permission workflow
- session awareness
- workspace context
- action proposal preview
- safe local action contract
- safe idle default
- visible audit and review boundaries
- ORION client boundary, but not free autonomous runtime

Not preferred for v1.0.0:

- file deletion
- mass file edits
- arbitrary shell execution
- free desktop control
- game control without telemetry boundary
- Blender or OBS automation without review
- plugin runtime without permission
- multi-step automation without review
- release gate bypass
- permission bypass

---

## Current Repository Structure

Important project areas:

    aura/
      capability_registry/
      core/
      plugins/
      skills/
      status/
      personality/
      review_stabilization_111_120/
      v1_runtime_readiness_cutline_review/
      manual_approval_decision_flow_review/
      runtime_error_rollback_preview/
      orion_client_boundary_contract/
      safe_local_action_contract_review/
      dashboard_runtime_readiness_view_model/
      audit_event_review_queue/
      runtime_permission_flow_consolidation/
      genesis_runtime_readiness_next_block_planning/

    docs/
      AURA_PRODUCT_DIRECTION_NOTE.md
      AURA_MASTER_ROADMAP.md
      AURA_ROADMAP_111_120_PLAN.md
      AURA_ROADMAP_121_130_PLAN.md
      AURA_REVIEW_STABILIZATION_111_120_FOUNDATION.md

---

## Storage Layout

AURA source code remains in the repository.

Large files should not be committed to git.

ATLAS large data storage:

    /mnt/aura-data/AURA

Data folders:

    /mnt/aura-data/AURA/models
    /mnt/aura-data/AURA/datasets
    /mnt/aura-data/AURA/cache
    /mnt/aura-data/AURA/logs
    /mnt/aura-data/AURA/backups
    /mnt/aura-data/AURA/avatar
    /mnt/aura-data/AURA/voice
    /mnt/aura-data/AURA/vision
    /mnt/aura-data/AURA/orion
    /mnt/aura-data/AURA/minecraft
    /mnt/aura-data/AURA/outputs
    /mnt/aura-data/AURA/projects

Storage documentation:

    /mnt/aura-data/AURA/README_STORAGE.md

---

## Quick Start

From the project root:

    cd /home/kiput/Projects/AURA

Activate the Python environment:

    source .venv/bin/activate

Check AURA status:

    python3 main.py

Expected current output:

    Version  : 0.123.0-genesis
    Status   : READY

Check a foundation status example:

    python3 main.py review-stabilization-111-120-status

Check capability registry summary:

    python3 main.py capability-summary

---

## Development Flow

AURA development is sprint-based.

Typical sprint flow:

1. Part A — module and foundation manager
2. Part B — skill, plugin, system status, CLI, and shell integration
3. Part C — docs, roadmap, capability registry, final validation, commit, push

Every 10 sprints, AURA performs a review stabilization checkpoint.

Completed recent block:

- Sprint 111: Genesis Runtime Readiness Next Block Planning
- Sprint 112: Runtime Permission Flow Consolidation
- Sprint 113: Audit Event Review Queue
- Sprint 114: Dashboard Runtime Readiness View Model
- Sprint 115: Safe Local Action Contract Review
- Sprint 116: ORION Client Boundary Contract
- Sprint 117: Runtime Error and Rollback Preview
- Sprint 118: Manual Approval Decision Flow Review
- Sprint 119: v1 Runtime Readiness Cutline Review
- Sprint 120: Review Stabilization 111-120

Next block:

- Sprint 121-130 Runtime Readiness Continuation

---

## Documentation Map

Primary docs:

- docs/AURA_PRODUCT_DIRECTION_NOTE.md
- docs/AURA_MASTER_ROADMAP.md
- docs/AURA_ROADMAP_111_120_PLAN.md
- docs/AURA_ROADMAP_121_130_PLAN.md
- docs/AURA_REVIEW_STABILIZATION_111_120_FOUNDATION.md

Archived full README history:

- docs/AURA_README_FULL_HISTORY_ARCHIVE.md

---

## Project Principles

AURA should grow slowly but correctly.

The priority is not to make AURA powerful as fast as possible.  
The priority is to make AURA feel alive, trustworthy, safe, local-first, useful, and clearly permission-bound.

AURA should grow together with Kiput.

## Sprint 121.0 — Post-Checkpoint 120 Next Block Planning Foundation

Status: completed
Version: v0.121.0-genesis

Sprint 121 opens the Sprint 121-130 runtime readiness continuation block with a planner-only, metadata-only, and review-only Post-Checkpoint 120 Next Block Planning Foundation.

Counts:

- 11 plan types
- 72 total post-checkpoint 120 next block planning blueprints/items
- 0 runtime post-checkpoint plannings activated
- 0 runtime next block approvals written
- 0 runtime release gates opened
- 0 runtime v1 runtimes activated
- 0 runtime permission audit writers started
- 0 runtime audit writer writes
- 0 runtime dashboard control centers started
- 0 runtime ORION dry handshakes or handshakes
- 0 runtime safe action allowlists applied
- 0 runtime safe actions executed
- 0 runtime grant expiries or recovery drills
- 0 runtime blocker state mutations
- 0 runtime actions/tools/commands/files/services/network/memory/git
- 0 runtime execution features

Safety result:

- next block planning only
- checkpoint followup review only
- release gate closed
- runtime activation disabled
- runtime upgrade deferred
- future runtime still requires manual approval

## Sprint 122.0 — Runtime Permission Audit Writer Boundary Review Foundation

Status: completed
Version: v0.122.0-genesis

Sprint 122 adds a planner-only, metadata-only, and review-only Runtime Permission Audit Writer Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total runtime permission audit writer boundary review blueprints/items
- 0 runtime audit writers started
- 0 runtime audit writer writes
- 0 runtime audit records persisted
- 0 runtime audit files written
- 0 runtime permissions changed
- 0 runtime dashboard audit payloads emitted
- 0 runtime dashboard events emitted
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- audit writer boundary review only
- audit writer runtime disabled
- audit record persistence disabled
- permission mutation disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 123.0 — Dashboard Control Center Boundary Review Foundation

Status: completed
Version: v0.123.0-genesis

Sprint 123 adds a planner-only, metadata-only, and review-only Dashboard Control Center Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total dashboard control center boundary review blueprints/items
- 0 runtime dashboard control centers started
- 0 runtime dashboard web/API/frontend/backend services started
- 0 runtime dashboard routes or ports bound
- 0 runtime dashboard events emitted
- 0 runtime dashboard permission commands
- 0 runtime dashboard action dispatches
- 0 runtime dashboard audit writes
- 0 runtime dashboard ORION handshakes
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- dashboard boundary review only
- dashboard runtime disabled
- dashboard web server disabled
- dashboard API server disabled
- dashboard route binding disabled
- dashboard port binding disabled
- permission mutation disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval
