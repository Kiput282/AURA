# AURA Genesis Runtime Activation Roadmap — Sprint 181-240

Status: CANONICAL GENESIS COMPLETION PATH
Current anchor: v0.186.0-genesis
Final target: v1.0.0-genesis at Sprint 240

## Roadmap Principle

Sprint 141-180 completed the service, Control Center, local chat, and memory foundations. Sprint 181 begins controlled runtime activation.

Each block is gate-based. A later block must not be activated merely because its sprint number is next; the previous block must pass its review and stabilization checkpoint first.

The Genesis Final objective is the smallest complete version of AURA as a safe local AI partner: usable chat and dashboard, explicit voice interaction, permission-gated screen awareness, active permission and audit workflows, basic safe local actions, unified context and memory, and reliable recovery.

ORION client integration, avatar/presence runtime, advanced desktop control, game control, streaming automation, and broad work execution are not release blockers for Genesis Final. They remain Post-Genesis work unless a small non-blocking foundation is needed internally.

## Current Runtime Activation Checkpoint

- Current version: v0.186.0-genesis
- Completed: Sprint 186 — Browser Chat Session Runtime
- Runtime execution features: 1
- Active scope: explicitly confirmed foreground localhost listener,
  transparent status routes, read-only Control Center backend, responsive
  browser dashboard, and permission-gated bounded local chat sessions
- Status routes: 9
- Control Center backend routes: 9
- Control Center dashboard assets: 3
- Control Center panels: 8
- Browser chat assets: 3
- Browser chat route contracts: 6
- Total local interaction route contracts: 27
- Session persistence: local, atomic, integrity-checked, Git-ignored
- Default listener state: stopped
- Local Model Bridge and inference: disabled
- AURA long-term memory writes: disabled
- Browser auto-launch: disabled
- Background/systemd/auto-start: disabled
- Next: Sprint 187 — Local Model Bridge Activation
## Block 181-190 — Local Interaction Runtime Activation

Outcome: AURA can be opened in a browser and used through a localhost Control Center and interactive local chat.

- 181 — Local Web Runtime Activation Cutline
- 182 — Service Lifecycle Runtime
- 183 — Health and Status API Runtime
- 184 — Control Center Backend Runtime
- 185 — Control Center Web Shell
- 186 — Browser Chat Session Runtime
- 187 — Local Model Bridge Activation
- 188 — Interactive Control Center Chat
- 189 — Permission, Audit, and Recovery Visibility
- 190 — Local Interaction Runtime Review and Stabilization

## Block 191-200 — Voice Interaction Runtime

Outcome: AURA can listen through explicit push-to-talk and answer by voice while reusing the stable chat/session path.

- 191 — Voice Runtime Activation Foundation
- 192 — Push-to-Talk and Explicit Listen State
- 193 — Local Microphone Capture Boundary
- 194 — Speech-to-Text Adapter Runtime
- 195 — Voice Intent and Chat Integration
- 196 — Text-to-Speech Adapter Runtime
- 197 — Voice Permission and Audit Runtime
- 198 — Control Center Voice Controls
- 199 — Voice Runtime Integration Review
- 200 — Voice Runtime Stabilization

Guardrails: no always-listening mode, hidden capture, background wake word, direct voice-to-action execution, or silent cloud fallback.

## Block 201-210 — Vision and Screen Awareness Runtime

Outcome: AURA can understand explicitly supplied screenshots or screen context with visible permission and redaction boundaries.

- 201 — Vision Runtime Activation Foundation
- 202 — Explicit Screenshot Capture
- 203 — Screen Context Adapter
- 204 — Local Vision Model Adapter
- 205 — Vision Permission and Redaction
- 206 — Workspace Visual Understanding
- 207 — Vision-to-Chat Context Handoff
- 208 — Control Center Vision Panel
- 209 — Vision Runtime Integration Review
- 210 — Vision Runtime Stabilization

Guardrails: no silent capture, continuous watching, camera activation by default, biometric identification, or visual-context-to-action bypass.

## Block 211-220 — Permission, Audit, and Safe Local Actions

Outcome: AURA can perform a narrow Genesis action scope only after preview and explicit approval.

- 211 — Active Permission Runtime
- 212 — Grant, Denial, and Expiry Lifecycle
- 213 — Runtime Audit Writer
- 214 — Action Proposal and Preview Runtime
- 215 — Safe Local Open Actions
- 216 — Allowlisted Application Launch
- 217 — Controlled Folder and Simple File Creation
- 218 — Control Center Approval Workflow
- 219 — Rollback, Emergency Stop, and Recovery
- 220 — Permission and Action Runtime Stabilization

Genesis action scope may include opening approved folders/files/project locations/dashboard, launching allowlisted applications, and creating a folder or simple file after preview and confirmation.

Deleting files, arbitrary shell execution, broad desktop control, dependency installation, plugin action execution without gates, and multi-step autonomous automation remain blocked.

## Block 221-230 — Unified Partner Runtime Integration

Outcome: AURA's chat, voice, vision, memory, workspace, permissions, and actions behave as one coherent partner runtime.

- 221 — Unified Session Runtime
- 222 — Workspace and Project Context Runtime
- 223 — Chat-to-Memory Runtime Handoff
- 224 — Voice, Vision, and Chat Context Fusion
- 225 — Personality Consistency Runtime
- 226 — Multi-Interface State Synchronization
- 227 — Service Persistence and Launcher
- 228 — Safe Auto-Start Evaluation
- 229 — Genesis Acceptance Rehearsal
- 230 — Unified Partner Runtime Stabilization

Auto-start may be accepted only after safe-idle boot, recovery, localhost binding, and emergency-stop behavior pass review.

## Block 231-240 — Genesis Final Integration and Release

Outcome: AURA reaches the defined birth point as a reliable, reviewable, local-first AI partner.

- 231 — Genesis Final Runtime Cutline
- 232 — End-to-End Security Review
- 233 — Privacy and Data Integrity Review
- 234 — Failure and Recovery Drills
- 235 — Dashboard and Interaction UX Polish
- 236 — Launcher and Deployment Stabilization
- 237 — Installation, Backup, and Migration Flow
- 238 — Final Genesis Acceptance Test
- 239 — v1.0.0 Release Candidate
- 240 — AURA Genesis Final / v1.0.0-genesis

## Genesis Final Acceptance Definition

AURA Genesis Final requires:

- usable local dashboard for chat and status;
- stable local chat and session history;
- explicit voice input and voice output;
- permission-gated screenshot or screen awareness;
- active permission, audit, denial, expiry, and recovery workflows;
- safe-idle default behavior;
- workspace/project context awareness;
- safe memory use and correction boundaries;
- action proposal and preview;
- a narrow set of approved local open/create actions;
- clean startup, shutdown, restart, backup, and recovery;
- no unsafe or hidden automation.

Genesis Final means AURA is born. It does not mean AURA is finished.

## Post-Genesis Deferrals

The following remain primarily Post-Genesis:

- avatar and embodiment runtime;
- livestream presence and OBS automation;
- Game Companion execution;
- ORION remote/client expansion;
- broad coding/work execution;
- Blender automation;
- unrestricted plugin actions;
- advanced multi-step autonomy.
