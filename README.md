# AURA

Local-first AI partner by Kiput.

AURA is a long-term AI companion project designed to grow into a local-first anime-girl virtual partner for work, creativity, livestreaming, game companionship, translation assistance, and safe desktop collaboration.

AURA is currently in the Genesis Runtime Readiness phase.

Current version: v0.165.0-genesis  
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

AURA has completed Sprint 161.0 and has started the Sprint 161-170 Local Chat Runtime block.

Latest completed checkpoint:

- v0.163.0-genesis
- Sprint 161: Local Chat Runtime Foundation
- Sprint 131-140 block: closed as a stabilized planning block
- Sprint 141 completed: Local Service Runtime Foundation
- Sprint 141-150 block: completed
- Sprint 151-160 block: active
- Next planned sprint: Sprint 147.0 — Service Control Command Review Foundation

Current capability registry summary:

- total capabilities: 92
- online capabilities: 90
- foundation-only capabilities: 74
- planner-only capabilities: 7
- permission-gated capabilities: 2
- review-only capabilities: 4
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
      review_stabilization_131_140/
      local_service_runtime_foundation/
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
      AURA_ROADMAP_131_140_PLAN.md
      AURA_ROADMAP_141_150_PLAN.md
      AURA_REVIEW_STABILIZATION_131_140_FOUNDATION.md
      AURA_LOCAL_SERVICE_RUNTIME_FOUNDATION.md

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

    Version  : 0.143.0-genesis
    Status   : READY

Check a foundation status example:

    python3 main.py local-service-safe-idle-boot-boundary-status

Check capability registry summary:

    python3 main.py capability-registry-status

---

## Development Flow

AURA development is sprint-based.

Typical sprint flow:

1. Part A — module and foundation manager
2. Part B — skill, plugin, system status, CLI, and shell integration
3. Part C — docs, roadmap, capability registry, final validation, commit, push

Every 10 sprints, AURA performs a review stabilization checkpoint.

Completed recent block:

- Sprint 131: Post-Checkpoint 130 Next Block Foundation
- Sprint 132: Final Genesis Acceptance Criteria Foundation
- Sprint 133: Runtime Activation Path Proposal Review
- Sprint 134: Local Service Boot Plan Review
- Sprint 135: Control Center Runtime Entry Review
- Sprint 136: Chat Runtime Minimal Loop Review
- Sprint 137: Memory Runtime Write Gate Review
- Sprint 138: Permission Runtime Grant Gate Review
- Sprint 139: Audit Runtime Writer Activation Review
- Sprint 140: Review & Stabilization 131-140

Completed service block:

- Sprint 141-150 Local Service Runtime Foundation completed

Active block:

- Sprint 151-160 Control Center Runtime
- Sprint 141: Local Service Runtime Foundation completed
- Sprint 142: Local Service Safe Idle Boot Boundary completed
- Sprint 143: Local Service Health Endpoint Foundation completed
- Sprint 144: Service Configuration and Port Registry Foundation completed
- Sprint 151: Control Center Runtime Foundation completed
- Sprint 152: Control Center Read-Only Status Panel Foundation completed
- Sprint 165: Model Adapter Boundary completed
- Next: Sprint 154 Control Center Service Monitor Panel Foundation

---

## Documentation Map

Primary docs:

- docs/AURA_PRODUCT_DIRECTION_NOTE.md
- docs/AURA_MASTER_ROADMAP.md
- docs/AURA_ROADMAP_111_120_PLAN.md
- docs/AURA_ROADMAP_121_130_PLAN.md
- docs/AURA_ROADMAP_131_140_PLAN.md
- docs/AURA_ROADMAP_141_150_PLAN.md
- docs/AURA_REVIEW_STABILIZATION_131_140_FOUNDATION.md
- docs/AURA_LOCAL_SERVICE_RUNTIME_FOUNDATION.md

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

## Sprint 124.0 — ORION Dry Handshake Boundary Review Foundation

Status: completed
Version: v0.124.0-genesis

Sprint 124 adds a planner-only, metadata-only, and review-only ORION Dry Handshake Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total ORION dry handshake boundary review blueprints/items
- 0 runtime ORION clients started
- 0 runtime ORION handshakes started
- 0 runtime ORION dry handshakes started
- 0 runtime ORION identity/capability/permission packets sent
- 0 runtime ORION status heartbeats sent
- 0 runtime ORION redactions applied
- 0 runtime ORION emergency stops triggered
- 0 runtime ATLAS/ORION authorities mutated
- 0 runtime dashboard events emitted
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- ORION boundary review only
- ORION client runtime disabled
- ORION handshake runtime disabled
- ORION network probe disabled
- ORION authority mutation disabled
- dashboard event emit disabled
- permission mutation disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 125.0 — Safe Local Action Allowlist Boundary Review Foundation

Status: completed
Version: v0.125.0-genesis

Sprint 125 adds a planner-only, metadata-only, and review-only Safe Local Action Allowlist Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total safe local action allowlist boundary review blueprints/items
- 0 runtime safe action catalogs applied
- 0 runtime safe action allowlists applied
- 0 runtime safe action permission requests created
- 0 runtime safe action risk evaluations
- 0 runtime safe action rollback snapshots
- 0 runtime safe action audit writes
- 0 runtime safe action dashboard events emitted
- 0 runtime safe actions dispatched
- 0 runtime safe actions executed
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- safe action allowlist boundary review only
- safe action runtime disabled
- safe action allowlist apply disabled
- safe action dispatch disabled
- safe action execution disabled
- permission request runtime disabled
- audit write disabled
- dashboard event emit disabled
- file runtime disabled
- service runtime disabled
- network probe disabled
- ORION handshake runtime disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 126.0 — Runtime Grant Expiry Boundary Review Foundation

Status: completed
Version: v0.126.0-genesis

Sprint 126 adds a planner-only, metadata-only, and review-only Runtime Grant Expiry Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total runtime grant expiry boundary review blueprints/items
- 0 runtime grants created
- 0 runtime grants renewed
- 0 runtime grants revoked
- 0 runtime grant expiries applied
- 0 runtime expired grant denials applied
- 0 runtime grant states mutated
- 0 runtime grant renewal requests created
- 0 runtime grant revocations applied
- 0 runtime dashboard grant events emitted
- 0 runtime audit grant events written
- 0 runtime grant runtime gates opened
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- grant expiry boundary review only
- grant expiry runtime disabled
- grant creation runtime disabled
- grant renewal runtime disabled
- grant revocation runtime disabled
- grant state mutation disabled
- expired grant denial runtime disabled
- permission mutation disabled
- audit write disabled
- dashboard event emit disabled
- action dispatch/execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 127.0 — Runtime Recovery Drill Boundary Review Foundation

Status: completed
Version: v0.127.0-genesis

Sprint 127 adds a planner-only, metadata-only, and review-only Runtime Recovery Drill Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total runtime recovery drill boundary review blueprints/items
- 0 runtime recovery drills started
- 0 runtime recovery drills executed
- 0 runtime recovery triggers applied
- 0 runtime recovery safe idle transitions
- 0 runtime rollback previews applied
- 0 runtime rollbacks executed
- 0 runtime recovery audit writes
- 0 runtime recovery dashboard events emitted
- 0 runtime recovery permission requests created
- 0 runtime recovery permissions mutated
- 0 runtime ORION recovery disconnects/handshakes
- 0 runtime recovery failure escalations
- 0 runtime recovery runtime gates opened
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- recovery drill boundary review only
- recovery drill runtime disabled
- recovery execution disabled
- rollback runtime disabled
- service restart runtime disabled
- permission mutation disabled
- audit write disabled
- dashboard event emit disabled
- action dispatch/execution disabled
- file/service/network/ORION runtime disabled
- ORION recovery runtime disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 128.0 — Dashboard Runtime Readiness Boundary Review Foundation

Status: completed
Version: v0.128.0-genesis

Sprint 128 adds a planner-only, metadata-only, and review-only Dashboard Runtime Readiness Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total dashboard runtime readiness boundary review blueprints/items
- 0 runtime dashboard servers started
- 0 runtime web/API/frontend/backend servers started
- 0 runtime dashboard routes registered
- 0 runtime dashboard ports bound
- 0 runtime dashboard browsers opened
- 0 runtime dashboard websockets opened
- 0 runtime dashboard events emitted
- 0 runtime dashboard permission commands sent
- 0 runtime dashboard audit writes
- 0 runtime dashboard actions dispatched
- 0 runtime dashboard runtime gates opened
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- dashboard runtime readiness boundary review only
- dashboard runtime disabled
- dashboard/web/API/frontend/backend server start disabled
- dashboard route register disabled
- dashboard port bind disabled
- dashboard browser open disabled
- dashboard websocket open disabled
- dashboard event emit disabled
- dashboard permission command disabled
- dashboard action dispatch disabled
- permission mutation disabled
- audit write disabled
- action dispatch/execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- runtime activation disabled
- future runtime still requires manual approval

## Sprint 129.0 — Runtime Activation Blocker Register Boundary Review Foundation

Status: completed
Version: v0.129.0-genesis

Sprint 129 adds a planner-only, metadata-only, and review-only Runtime Activation Blocker Register Boundary Review Foundation.

Counts:

- 11 plan types
- 72 total runtime activation blocker register boundary review blueprints/items
- 0 runtime activation blocker registers created
- 0 runtime activation blockers added
- 0 runtime activation blockers updated
- 0 runtime activation blockers deleted
- 0 runtime activation blockers resolved
- 0 runtime activation gate links created
- 0 runtime activation gates unblocked
- 0 runtime activation gates opened
- 0 runtime activations started
- 0 runtime blocker resolution evidence writes
- 0 runtime blocker dashboard events emitted
- 0 runtime blocker audit events written
- 0 runtime blocker failure recoveries
- 0 runtime blocker runtime gates opened
- 0 runtime permissions changed
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime execution features

Safety result:

- runtime activation blocker register boundary review only
- runtime activation blocker register runtime disabled
- blocker register mutation disabled
- blocker resolution runtime disabled
- runtime gate unblock disabled
- runtime gate open disabled
- runtime activation disabled
- permission mutation disabled
- audit write disabled
- dashboard event emit disabled
- action dispatch/execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 130.0 — Review Stabilization 121-130 Foundation

Status: completed
Version: v0.130.0-genesis

Sprint 130 adds a review-only stabilization checkpoint for Sprint 121-129 and closes the Sprint 121-130 block.

Counts:

- 12 plan types
- 100 total review stabilization 121-130 blueprints/items
- 0 runtime checkpoints applied
- 0 runtime checkpoint mutations
- 0 runtime capability registry mutations
- 0 runtime permissions changed
- 0 runtime audit events written
- 0 runtime dashboard events emitted
- 0 runtime actions/tools/commands/files/services/network/ORION/memory/git
- 0 runtime dashboard/web/API/frontend/backend servers started
- 0 runtime dashboard routes/websockets opened
- 0 runtime activation gates opened
- 0 runtime activations started
- 0 runtime recovery drills started
- 0 runtime rollbacks executed
- 0 runtime blocker register mutations
- 0 runtime execution features

Safety result:

- review stabilization 121-130 review only
- checkpoint runtime disabled
- runtime activation disabled
- runtime gate open disabled
- capability registry runtime mutation disabled
- permission mutation disabled
- audit write disabled
- dashboard event emit disabled
- action dispatch/execution disabled
- tool/command execution disabled
- file/service/network/ORION runtime disabled
- dashboard runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 131.0 — Post-Checkpoint 130 Next Block Foundation

Status: completed
Version: v0.131.0-genesis

Sprint 131 adds a planner-only, metadata-only, and review-only Post-Checkpoint 130 Next Block Foundation.

Counts:

- 12 plan types
- 100 total post-checkpoint 130 next block blueprints/items
- 0 runtime next block foundations activated
- 0 runtime Final Genesis acceptance applied
- 0 runtime activation paths applied
- 0 runtime local services booted
- 0 runtime service autostarts enabled
- 0 runtime Control Centers started
- 0 runtime dashboard servers started
- 0 runtime chat loops started
- 0 runtime memory reads/writes
- 0 runtime permission grants created/applied
- 0 runtime audit writers started
- 0 runtime audit events written
- 0 runtime dashboard events emitted
- 0 runtime actions/tools/commands/files/services/network/ORION/git
- 0 runtime execution features

Safety result:

- post-checkpoint 130 next block review only
- Final Genesis runtime activation disabled
- local service runtime disabled
- Control Center runtime disabled
- chat runtime disabled
- memory runtime disabled
- permission runtime disabled
- audit runtime disabled
- runtime activation disabled
- runtime gate open disabled
- action/tool/command execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 132.0 — Final Genesis Acceptance Criteria Foundation

Status: completed
Version: v0.132.0-genesis

Sprint 132 adds a planner-only, metadata-only, and review-only Final Genesis Acceptance Criteria Foundation.

Counts:

- 12 plan types
- 100 total Final Genesis acceptance criteria blueprints/items
- 0 runtime Final Genesis releases started
- 0 runtime Final Genesis acceptance applied
- 0 runtime go/no-go applied
- 0 runtime release candidates started
- 0 runtime local services booted
- 0 runtime service autostarts enabled
- 0 runtime Control Centers started
- 0 runtime dashboard servers started
- 0 runtime chat loops started
- 0 runtime memory reads/writes
- 0 runtime permission grants created/applied
- 0 runtime audit writers started
- 0 runtime safe idle/recovery/rollback/emergency stop
- 0 runtime ORION/voice/vision/avatar/streaming
- 0 runtime actions/tools/commands/files/services/network/git
- 0 runtime execution features

Safety result:

- Final Genesis release disabled
- release candidate runtime disabled
- local service runtime disabled
- Control Center/dashboard/chat/memory runtime disabled
- permission/audit runtime disabled
- safe idle recovery runtime disabled
- ORION/voice/vision/avatar/streaming runtime disabled
- action/tool/command execution disabled
- file/service/network runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 133.0 — Runtime Activation Path Proposal Review Foundation

Status: completed
Version: v0.133.0-genesis

Sprint 133 adds a planner-only, metadata-only, and review-only Runtime Activation Path Proposal Review Foundation.

Counts:

- 12 plan types
- 100 total runtime activation path proposal review blueprints/items
- 0 runtime activation path proposals applied
- 0 runtime activation stages enabled
- 0 runtime activation gates opened
- 0 runtime activations started
- 0 runtime release candidates started
- 0 runtime local services booted
- 0 runtime service autostarts enabled
- 0 runtime Control Centers started
- 0 runtime dashboard servers started
- 0 runtime chat loops started
- 0 runtime memory reads/writes
- 0 runtime permission grants created/applied
- 0 runtime audit writers started
- 0 runtime blocker register mutations
- 0 runtime blockers resolved
- 0 runtime safe idle/recovery/rollback/emergency stop
- 0 runtime actions/tools/commands/files/services/network/ORION/git
- 0 runtime execution features

Safety result:

- runtime activation path apply disabled
- runtime activation stage enable disabled
- runtime activation gate open disabled
- runtime activation start disabled
- release candidate runtime disabled
- local service/dashboard/chat/memory runtime disabled
- permission/audit/blocker register runtime disabled
- action/tool/command execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 134.0 — Local Service Boot Plan Review Foundation

Status: completed
Version: v0.134.0-genesis

Sprint 134 adds a planner-only, metadata-only, and review-only Local Service Boot Plan Review Foundation for ATLAS.

Counts:

- 12 plan types
- 100 total local service boot plan review blueprints/items
- 0 runtime local service boot plans applied
- 0 runtime local services booted
- 0 runtime local services started/stopped
- 0 runtime service autostarts enabled
- 0 runtime service units created/modified/deleted
- 0 runtime health monitors/checks
- 0 runtime safe shutdowns
- 0 runtime config/log file reads or writes
- 0 runtime ports bound
- 0 runtime API/web/dashboard servers started
- 0 runtime chat loops started
- 0 runtime memory reads/writes
- 0 runtime permission grants created/applied
- 0 runtime audit writers/events
- 0 runtime dashboard events emitted
- 0 runtime actions/tools/commands/files/services/network/ORION/git
- 0 runtime execution features

Safety result:

- local service boot plan apply disabled
- local service boot/start/stop disabled
- service autostart disabled
- service unit mutation disabled
- health monitor/check runtime disabled
- safe shutdown runtime disabled
- config/log file runtime disabled
- port binding disabled
- API/web/dashboard/chat/memory runtime disabled
- permission/audit runtime disabled
- action/tool/command execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 135.0 — Control Center Runtime Entry Review Foundation

Status: completed
Version: v0.135.0-genesis

Sprint 135 adds a planner-only, metadata-only, and review-only Control Center Runtime Entry Review Foundation.

Counts:

- 12 plan types
- 100 total Control Center runtime entry review blueprints/items
- 0 runtime Control Center entries applied
- 0 runtime Control Centers started
- 0 runtime Control Center routes created/bound
- 0 runtime dashboard/API/web/frontend/backend servers started
- 0 runtime ports bound
- 0 runtime status/permission/audit/action/safe-idle/manual approval panels started
- 0 runtime dashboard events emitted
- 0 runtime permission grants created/applied
- 0 runtime audit writers/events
- 0 runtime actions dispatched/executed
- 0 runtime chat loops started
- 0 runtime memory reads/writes
- 0 runtime tools/commands/files/services/network/ORION/git
- 0 runtime execution features

Safety result:

- Control Center runtime entry apply disabled
- Control Center start disabled
- Control Center route mutation/binding disabled
- dashboard/API/web/frontend/backend runtime disabled
- port binding disabled
- all panel runtime disabled
- dashboard event emit disabled
- permission/audit/action/chat/memory runtime disabled
- action/tool/command execution disabled
- file/service/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 136.0 — Chat Runtime Minimal Loop Review Foundation

Status: completed
Version: v0.136.0-genesis

Sprint 136 adds a planner-only, metadata-only, and review-only Chat Runtime Minimal Loop Review Foundation.

Counts:

- 12 plan types
- 100 total chat runtime minimal loop review blueprints/items
- 0 runtime chat minimal loop plans applied
- 0 runtime chat loops started
- 0 runtime chat messages received/processed
- 0 runtime chat responses generated/sent
- 0 runtime chat sessions created/updated/deleted
- 0 runtime permission prompts created/applied
- 0 runtime memory reads/writes
- 0 runtime audit writers/events
- 0 runtime safe idle recoveries
- 0 runtime error recoveries
- 0 runtime model requests/inferences
- 0 runtime tools/commands/files/services/ports/network/ORION/git
- 0 runtime dashboard events/actions
- 0 runtime execution features

Safety result:

- chat minimal loop apply disabled
- chat loop start disabled
- chat message receive/process disabled
- chat response generate/send disabled
- chat session mutation disabled
- permission prompt runtime disabled
- memory/audit runtime disabled
- safe idle/error recovery runtime disabled
- model request/inference runtime disabled
- dashboard event emit disabled
- action/tool/command execution disabled
- file/service/port/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 137.0 — Memory Runtime Write Gate Review Foundation

Status: completed
Version: v0.137.0-genesis

Sprint 137 adds a planner-only, metadata-only, and review-only Memory Runtime Write Gate Review Foundation.

Counts:

- 12 plan types
- 100 total memory runtime write gate review blueprints/items
- 0 runtime memory write gate plans applied
- 0 runtime memory write requests received
- 0 runtime memory write intents classified
- 0 runtime memory write approvals requested/applied
- 0 runtime memory scopes applied
- 0 runtime memory redactions executed
- 0 runtime memory conflict resolutions executed
- 0 runtime memory reads/writes
- 0 runtime memory records created/updated/deleted
- 0 runtime memory indexes updated
- 0 runtime memory files/databases/caches written
- 0 runtime memory rollbacks/session links
- 0 runtime permission grants created/applied
- 0 runtime audit writers/events
- 0 runtime safe idle recoveries
- 0 runtime dashboard events/actions
- 0 runtime tools/commands/files/services/ports/network/ORION/git
- 0 runtime execution features

Safety result:

- memory write gate apply disabled
- memory write request receive disabled
- memory write intent classification disabled
- memory write approval runtime disabled
- memory scope/redaction/conflict runtime disabled
- memory read/write disabled
- memory record mutation disabled
- memory index update disabled
- memory persistence disabled
- memory rollback/session link runtime disabled
- permission/audit/dashboard/action runtime disabled
- tool/command execution disabled
- file/service/port/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 138.0 — Permission Runtime Grant Gate Review Foundation

Status: completed
Version: v0.138.0-genesis

Sprint 138 adds a planner-only, metadata-only, and review-only Permission Runtime Grant Gate Review Foundation.

Counts:

- 12 plan types
- 100 total permission runtime grant gate review blueprints/items
- 0 runtime permission grant gate plans applied
- 0 runtime permission grant requests received
- 0 runtime permission grant scopes classified
- 0 runtime permission grant approvals requested/applied
- 0 runtime permission grants created/applied/updated/revoked
- 0 runtime permission grant expiries applied
- 0 runtime permission denials created
- 0 runtime permission risks classified
- 0 runtime permission audit links created
- 0 runtime permission dashboard events emitted
- 0 runtime permission stores/caches written
- 0 runtime audit writers/events
- 0 runtime safe idle recoveries
- 0 runtime dashboard events/actions
- 0 runtime tools/commands/files/services/ports/network/ORION/git
- 0 runtime execution features

Safety result:

- permission grant gate apply disabled
- permission grant request receive disabled
- permission grant scope classification disabled
- permission grant approval runtime disabled
- permission grant create/apply/update/revoke disabled
- permission grant expiry apply disabled
- permission denial create disabled
- permission risk classification disabled
- permission audit link/dashboard event runtime disabled
- permission store/cache write disabled
- permission mutation disabled
- audit/dashboard/action runtime disabled
- tool/command execution disabled
- file/service/port/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 139.0 — Audit Runtime Writer Activation Review Foundation

Status: completed
Version: v0.139.0-genesis

Sprint 139 adds a planner-only, metadata-only, and review-only Audit Runtime Writer Activation Review Foundation.

Counts:

- 12 plan types
- 100 total audit runtime writer activation review blueprints/items
- 0 runtime audit writer activation plans applied
- 0 runtime audit writers started/stopped
- 0 runtime audit events received
- 0 runtime audit event schemas validated
- 0 runtime audit events written
- 0 runtime audit logs appended
- 0 runtime audit storages/files/databases/caches written
- 0 runtime audit redactions executed
- 0 runtime audit actor contexts resolved
- 0 runtime audit permission links created
- 0 runtime audit dashboard events emitted
- 0 runtime audit rotations/exports/retentions/corruption checks
- 0 runtime permission mutations/grants
- 0 runtime safe idle recoveries
- 0 runtime dashboard events/actions
- 0 runtime tools/commands/files/services/ports/network/ORION/git
- 0 runtime execution features

Safety result:

- audit writer activation apply disabled
- audit writer start/stop disabled
- audit event receive/schema/write disabled
- audit log append disabled
- audit storage/file/database/cache write disabled
- audit redaction/actor/permission/dashboard runtime disabled
- audit rotation/export/retention/corruption check disabled
- permission mutation disabled
- dashboard/action runtime disabled
- tool/command execution disabled
- file/service/port/network/ORION runtime disabled
- release gate closed
- future runtime still requires manual approval

## Sprint 140.0 — Review & Stabilization 131-140 Foundation

Status: completed
Version: v0.140.0-genesis

Sprint 140 closes the 131-140 runtime planning block with a planner-only, metadata-only, and review-only stabilization checkpoint.

Counts:

- 12 plan types
- 100 total review stabilization 131-140 blueprints/items
- 0 runtime review stabilization plans applied
- 0 runtime services/API/web/dashboard/control center
- 0 runtime chat/memory/permission/audit/model
- 0 runtime actions/tools/commands/files/ports/network/ORION/git
- 0 runtime execution features

Safety result:

- service runtime disabled
- API/web/dashboard/control center runtime disabled
- chat/memory/permission/audit/model runtime disabled
- action/tool/command execution disabled
- file/port/network/ORION/git runtime disabled
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 144.0 — Service Configuration and Port Registry Foundation

## Product Direction: Genesis to Post-Genesis

AURA is a local-first AI partner.

Current canonical state:

- Version: v0.165.0-genesis
- Current completed sprint: Sprint 161.0 — Local Chat Runtime Foundation
- Next planned sprint: Sprint 166.0 — Permission-Gated Model Request
- Final Genesis target: Sprint 240.0 — Genesis Final Release v1.0.0-genesis

Roadmap summary:

- Sprint 141-150: Local Service Runtime Foundation
- Sprint 151-160: Control Center Runtime
- Sprint 161-170: Local Chat Runtime
- Sprint 171-180: Memory Runtime
- Sprint 181-190: Voice Foundation Runtime
- Sprint 191-200: Vision / Screen Awareness Runtime
- Sprint 201-210: ORION Client Bridge
- Sprint 211-220: Avatar / Presence Foundation
- Sprint 221-230: Final Genesis Integration
- Sprint 231-240: Genesis Release Candidate to v1.0.0-genesis

Canonical planning docs:

- docs/AURA_GENESIS_TO_POST_GENESIS_PRODUCT_PLAN.md
- docs/AURA_GAME_COMPANION_SAFETY_POLICY.md

## Future Game Companion Plan

AURA Game Companion is a future post-core pillar.

Planned order:

1. Minecraft Companion
2. osu Companion
3. Beat Saber Companion
4. Monster Hunter Companion

Direction:

- Minecraft: private/local sandbox companion for survival, building, resource planning, navigation, base planning, and devlog progression.
- osu: offline rhythm learner that learns from vision/audio/feedback without using beatmap files as answer keys or submitting online scores.
- Beat Saber: 3D rhythm performer with avatar movement, cinematic camera planning, viewer challenge queue, and livestream identity.
- Monster Hunter: single-player Hunter Coach for observation, positioning advice, item/loadout guidance, and offline learning research.

Safety boundary:

- no cheating
- no ranked/online score automation
- no multiplayer farming
- no exploit workflows
- no silent game input control
- no public server abuse
- no ORION/game runtime before permission, audit, vision, and Control Center gates exist

## Current Capability Boundary

At v0.165.0-genesis, AURA can:

- boot to READY
- expose identity and version
- show capability registry metadata
- show skill and plugin action metadata
- provide planner-only review packets through CLI/shell
- document sprint progress
- maintain roadmap and journal records
- define safety boundaries
- define future runtime plans
- define future local service safe-idle boot boundary plans
- define future local service health endpoint foundation plans
- define future service configuration and port registry foundation plans
- define future service permission gate runtime boundary plans
- define future service audit link foundation plans
- validate that runtime counters remain zero
- support Git-tracked project evolution

At v0.165.0-genesis, AURA cannot yet:

- start active local service runtime
- serve a real web Control Center
- run real chat runtime
- read/write memory at runtime
- create/apply permission grants at runtime
- start audit writers or write audit events
- use microphone, camera, screen, or ORION bridge
- control desktop apps, OBS, Blender, avatar, or games
- execute tools or commands autonomously
- read/write/modify/delete files at runtime
- bind ports or expose network services as active runtime
- serve a real /health endpoint as active runtime
- read/write service config or bind/reserve ports as active runtime

## Sprint 141.0 — Local Service Runtime Foundation

Status: completed  
Version: v0.141.0-genesis

Sprint 141 opens the Sprint 141-150 Local Service Runtime Foundation block.

It adds a planner-only, metadata-only, and foundation-only Local Service Runtime Foundation for ATLAS safe-idle service identity, localhost-only boundary, lifecycle state, configuration contract, health surface, permission gate link, audit link, control command boundary, and no-start activation review.

Counts:

- 12 plan types
- 100 total local service runtime foundation blueprint/items
- 0 runtime services started
- 0 runtime sockets opened
- 0 runtime ports bound
- 0 runtime health endpoints started
- 0 runtime systemd units created or enabled
- 0 runtime permission mutations
- 0 runtime audit events written
- 0 runtime actions/tools/commands/files/services/network/memory/model/ORION/git
- 0 runtime execution features

Safety result:

- foundation-only local service planning
- safe-idle default preserved
- localhost-only policy documented
- no silent port binding
- no service start activation
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 142.0 — Local Service Safe Idle Boot Boundary

## Sprint 142.0 — Local Service Safe Idle Boot Boundary

Status: completed  
Version: v0.142.0-genesis

Sprint 142 defines the safe-idle boot boundary for AURA's future ATLAS local service.

It adds a planner-only, metadata-only, and foundation-only Local Service Safe Idle Boot Boundary for boot entry states, safe-idle guard conditions, boot failure fallback, no-autostart policy, read-only readiness probes, Control Center idle visibility, permission denial idle behavior, audit failure idle behavior, and no-boot-activation review.

Counts:

- 12 plan types
- 100 total local service safe-idle boot boundary blueprint/items
- 0 runtime services started
- 0 runtime autostarts enabled
- 0 runtime systemd units created, enabled, or started
- 0 runtime sockets opened
- 0 runtime ports bound
- 0 runtime health endpoints started
- 0 runtime permission mutations
- 0 runtime audit events written
- 0 runtime actions/tools/commands/files/services/network/memory/model/ORION/git
- 0 runtime execution features

Safety result:

- safe-idle boot default preserved
- boot runtime activation disabled
- no autostart activation
- no service start at boot
- no silent port binding
- readiness probe remains metadata-only
- permission denial keeps service idle
- audit failure keeps service idle
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 143.0 — Local Service Health Endpoint Foundation

## Sprint 143.0 — Local Service Health Endpoint Foundation

Status: completed  
Version: v0.143.0-genesis

Sprint 143 defines the future local-service health endpoint foundation for AURA's ATLAS service path.

It adds a planner-only, metadata-only, and foundation-only Local Service Health Endpoint Foundation for future localhost-only health endpoint scope, read-only /health contract, health response schema, localhost binding boundary, safe-idle health state, dependency visibility, permission/audit health linkage, Control Center health card, error fallback, and no-health-endpoint-activation review.

Counts:

- 12 plan types
- 100 total local service health endpoint foundation blueprint/items
- 0 runtime health endpoint servers started
- 0 runtime HTTP listeners started
- 0 runtime sockets opened
- 0 runtime ports bound
- 0 runtime network probes
- 0 runtime services started
- 0 runtime permission mutations
- 0 runtime audit events written
- 0 runtime actions/tools/commands/files/services/network/memory/model/ORION/git
- 0 runtime execution features

Safety result:

- health endpoint contract remains metadata-only
- localhost-only policy preserved
- no HTTP listener starts
- no socket opens
- no port binding occurs
- no network probe runs
- permission/audit health linkage is read-only planning only
- Control Center health card remains a future display contract
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 144.0 — Service Configuration and Port Registry Foundation

## Sprint 144.0 — Service Configuration and Port Registry Foundation

Status: completed  
Version: v0.144.0-genesis

Sprint 144 defines the future service configuration and port registry foundation for AURA's ATLAS service path.

It adds a planner-only, metadata-only, and foundation-only Service Configuration and Port Registry Foundation for future service configuration scope, config schema, port registry schema, localhost port policy, reserved port policy, port conflict preflight, environment override boundary, Control Center config card, permission/audit config linkage, and no config/port runtime activation review.

Counts:

- 12 plan types
- 100 total service configuration and port registry blueprint/items
- 0 runtime config files read
- 0 runtime config files written
- 0 runtime port registry writes
- 0 runtime ports reserved
- 0 runtime sockets opened
- 0 runtime ports bound
- 0 runtime HTTP listeners started
- 0 runtime services started
- 0 runtime permission mutations
- 0 runtime audit events written
- 0 runtime actions/tools/commands/files/services/network/memory/model/ORION/git
- 0 runtime execution features

Safety result:

- service configuration remains metadata-only
- port registry remains blueprint-only
- localhost-only policy preserved
- no port reservation occurs
- no port binding occurs
- no socket opens
- no HTTP listener starts
- no config file read/write runtime is active
- environment override runtime remains disabled
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 145.0 — Service Permission Gate Runtime Boundary



## Sprint 145.0 — Service Permission Gate Runtime Boundary

Status: completed  
Version: v0.145.0-genesis

Sprint 145 defines the Service Permission Gate Runtime Boundary for AURA's future ATLAS service path.

This checkpoint adds planner-only and metadata-only contracts for service permission scopes, grant preflight, denial behavior, safe-idle fallback, Control Center permission visibility, audit linkage, grant expiry awareness, and no-permission-runtime-activation review. It does not create permission requests, grant permissions, mutate permissions, start services, bind ports, write audit logs, execute tools or commands, or enable runtime execution features.

Sprint 145 keeps AURA safe by default: service runtime remains disabled, permission runtime remains disabled, and any future service activation must pass explicit review, permission, audit, localhost-only, and safe-idle boundaries.


## Sprint 146.0 — Service Audit Link Foundation

Status: completed  
Version: v0.146.0-genesis

Sprint 146 defines the Service Audit Link Foundation for AURA's future ATLAS service path.

This checkpoint adds planner-only and metadata-only contracts for service audit event references, audit link records, traceability chains, permission/audit pairing, Control Center audit visibility, redaction boundaries, failure safe-idle behavior, retention boundaries, error handling, and no-audit-link-runtime-activation review.

Counts:

- 12 plan types
- 100 total service audit link blueprint/items
- 0 runtime audit link records created/read/written/modified/deleted
- 0 runtime audit event references created
- 0 runtime audit events written
- 0 runtime audit logs appended
- 0 runtime audit redactions executed
- 0 runtime audit trace chains written
- 0 runtime permission audit links written
- 0 runtime services started
- 0 runtime ports bound
- 0 runtime execution features

Safety result:

- audit link foundation remains metadata-only
- audit writer runtime remains disabled
- audit event runtime remains disabled
- audit log runtime remains disabled
- permission/audit link writes remain disabled
- service start remains disabled
- socket and port binding remain disabled
- public network exposure remains disabled
- release gate closed
- future runtime still requires manual approval

Next planned sprint:

- Sprint 147.0 — Service Control Command Review Foundation


## Sprint 147.0 — Service Control Command Review Foundation

Version: v0.165.0-genesis

Sprint 147 defines the Service Control Command Review Foundation for AURA's future ATLAS service control path. It prepares planner-only and metadata-only start/stop/restart/status command review scopes, proposal contracts, permission boundaries, audit links, Control Center command surfaces, failure safe-idle behavior, and no-service-control-command-runtime-activation review.

Runtime remains disabled by design:

- no service start/stop/restart command execution
- no runtime process status probe
- no systemd command execution
- no shell command execution
- no socket open
- no port binding
- no HTTP listener start
- no audit event write
- no permission mutation
- no action/tool/command/file/memory/model/ORION/git runtime
- no runtime execution features

Next planned sprint: Sprint 162.0 — Local Chat CLI Session Alpha.

## Sprint 148.0 — Service Recovery and Restart Policy Foundation

Version: v0.165.0-genesis

Sprint 148 defines the Service Recovery and Restart Policy Foundation for AURA's future ATLAS service runtime. It prepares planner-only and metadata-only failure classification, safe-idle recovery policy, restart approval policy, retry cooldown policy, rollback visibility, Control Center recovery surfaces, permission links, audit links, error boundaries, and no-recovery-restart-runtime-activation review.

Runtime remains disabled by design: no service process is started/stopped/restarted, no retry timer or retry loop is started, no recovery state is written, no file/config/git rollback is executed, no systemd/shell command is executed, no socket or port is opened, and runtime execution features remain 0.

Next planned sprint: Sprint 162.0 — Local Chat CLI Session Alpha.

## Sprint 149.0 — Service Security and Localhost Binding Review

Version: v0.165.0-genesis

Sprint 149 defines the Service Security and Localhost Binding Review foundation for AURA's future ATLAS service runtime. It prepares planner-only and metadata-only localhost-only binding policy, public network exposure block policy, origin/host allowlist policy, loopback interface policy, deferred TLS/CORS/external-access review, permission/audit links, port-binding preflight security, Control Center security surfaces, security error boundaries, and no-security-localhost-runtime-activation review.

Runtime remains disabled by design: no socket is opened, no port is bound, no HTTP/public listener is started, no security config or allowlist is written, no network probe is executed, no service command runs, and runtime execution features remain 0.

Next planned sprint: Sprint 162.0 — Local Chat CLI Session Alpha.











## Sprint 163 — Local Chat Message Store

Sprint 163 adds the first controlled local message store for AURA chat. AURA can
now accept one manual CLI message, return a safe local persona response, and
append the turn to an AURA-owned JSONL store:

```bash
python3 main.py local-chat-store-alpha "Aura simpan pesan ini"
```

Default store path:

```text
.aura_runtime/local_chat/messages.jsonl
```

This is a controlled store write only. It does not dispatch model requests,
write memory runtime, mutate permissions, write audit logs, execute commands,
launch applications, create folders, mutate arbitrary files, start servers, bind
ports, use voice, capture screens, or perform autonomous actions.

## Sprint 162 — Local Chat CLI Session Alpha

Sprint 162 adds the first safe thin runtime in the Local Chat block. AURA can
now be tried from the CLI with a one-turn transient local chat alpha:

```bash
python3 main.py local-chat-alpha "Aura kamu aktif?"
```

This creates an in-memory/transient session packet, accepts one manual message,
and returns a deterministic safe AURA persona response. It does not persist chat
history, dispatch model requests, write memory, mutate permissions, write audit
logs, execute commands/tools, launch applications, create folders, mutate files,
start servers, bind ports, use voice, capture screens, or perform autonomous
actions.

## Sprint 161 — Local Chat Runtime Foundation

Sprint 161 starts the Local Chat Runtime block and records the safe foundation
for local chat sessions, message schemas, chat loop boundaries, AURA persona
response boundaries, history boundaries, permission/audit links, model adapter
boundaries, and Sprint 162 CLI alpha readiness. This block shifts AURA from
blueprint-only development toward a safe thin runtime, while keeping command
execution, file mutation, desktop control, voice, vision, model runtime, and
autonomous actions disabled until their later gated blocks.

Sprint 161 does not create chat sessions at runtime, accept chat messages,
persist chat history, dispatch model requests, write memory, mutate permissions,
write audit logs, execute commands/tools, mutate files, control desktop apps,
start voice/vision runtime, start servers, mount routes, bind ports, or enable
runtime execution features.

## Sprint 160 — Control Center Runtime Review & Stabilization 151–160

Sprint 160 closes the Control Center Runtime block with a review and
stabilization checkpoint across Sprint 151–159. It reviews Control Center panel
readiness, runtime-disabled boundaries, route/navigation metadata, read-only
data contracts, permission/audit links, service monitor/action log surfaces,
security/accessibility notes, and next Local Chat Runtime block readiness. It
does not write stabilization records at runtime, open release gates, activate the
next block at runtime, start Control Center servers, start frontend/backend
runtime, mount routes, serve dashboard requests, read live stores, open sockets,
bind ports, dispatch actions, execute commands/tools, mutate permissions, write
audit logs, or enable runtime execution features.

## Sprint 159 — Control Center Read-Only Route Map Foundation

Sprint 159 adds the Control Center Read-Only Route Map Foundation. It defines
route map layout, dashboard navigation surfaces, route definition summaries,
panel crosslinks, route guard boundaries, filtering/grouping, empty/error
states, accessibility/security review, no route map runtime activation, and
Sprint 160 stabilization readiness. It does not mount routes, serve dashboard
requests, start Control Center servers, start frontend/backend runtime, open
sockets, bind ports, dispatch actions, execute commands, or enable runtime
execution features.

## Sprint 158 — Control Center Action Log Panel Foundation

Sprint 158 adds the Control Center Action Log Panel Foundation. It defines
action log layout, action history summaries, action boundary visibility,
plugin/action linkage, permission/audit linkage, filtering/grouping,
redaction/privacy boundaries, empty/error states, accessibility/security review,
and no action log panel runtime activation. It does not read live action stores,
append logs, dispatch actions, execute plugin/tool/command actions, mount routes,
serve dashboard requests, bind ports, or enable runtime execution features.

## Sprint 157 — Control Center Service Monitor Panel Foundation

Sprint 157 adds the Control Center Service Monitor Panel Foundation. It defines
service monitor layout, service runtime state summaries, process boundary
visibility, health signal cards, restart/recovery status surfaces,
security/localhost status, filters/grouping, error boundaries,
accessibility/security review, and no service monitor panel runtime activation.
It does not probe live processes, run health checks, start/stop/restart
services, mount routes, serve dashboard requests, bind ports, or enable runtime
execution features.

## Sprint 156 — Control Center Audit Panel Foundation

Sprint 156 adds the Control Center Audit Panel Foundation. It defines audit
panel layout, audit link summaries, audit event reference visibility, audit log
boundaries, trace-chain summaries, retention/redaction boundaries, audit filters
and grouping, error boundaries, accessibility/security review, and no audit
panel runtime activation. It does not read live audit logs, create or modify
audit link records, write audit events, append audit logs, execute redactions,
start dashboard servers, mount routes, serve requests, bind ports, or enable
runtime execution features.

## Sprint 155 — Control Center Permission Panel Foundation

Sprint 155 adds the Control Center Permission Panel Foundation. It defines
permission panel layout, permission request summaries, grant boundary visibility,
risk badges, permission filters/grouping, security and accessibility review,
next audit-viewer readiness, and no permission panel runtime activation. It does
not create permission requests, apply or revoke grants, mutate permissions, read
live permission stores, write audit events, start dashboard servers, mount
routes, serve requests, bind ports, or enable runtime execution features.

## Sprint 154 — Control Center Plugin Panel Foundation

Sprint 154 adds the Control Center Plugin Panel Foundation. It defines plugin
panel layout, plugin registry summary, plugin action status semantics,
permission boundary visibility, plugin filter/grouping behavior, security and
accessibility review, next service-monitor readiness, and no plugin panel runtime
activation. It does not start a dashboard server, read plugin runtime data,
render a live plugin panel, mount routes, serve requests, bind ports, dispatch
actions, mutate permissions, or enable runtime execution features.



### Sprint 165 — Model Adapter Boundary

Sprint 165 adds the first model-adapter boundary for local chat. AURA can create
a dry-run prompt/provider adapter packet and explain the future model request
path, but it still does not call a local model, remote API, network endpoint, or
credential store. Sprint 166 must add permission-gated model request handling
before any real model request can be dispatched.
