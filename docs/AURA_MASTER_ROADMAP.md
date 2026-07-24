# AURA Master Roadmap

```text
Project : AURA
Motto   : Grow Together
Creator : Kiput
Phase   : Genesis
Status  : Master Roadmap Draft v0.1
1. What is AURA?

AURA is a local-first modular AI partner designed to accompany and help its creator work, create, learn, build, play, stream, and grow.

AURA is not meant to be just a chatbot.

AURA is intended to become:

AI Partner
+ Personal Companion
+ Work Assistant
+ Project Manager
+ Creative Assistant
+ Coding Assistant
+ Voice Companion
+ 3D Avatar
+ Screen/Camera Aware Assistant
+ Streaming/Gaming Companion

AURA's core direction:

One identity.
Multiple internal roles.
Multiple specialized models.
Plugin-based abilities.
Event-driven architecture.
Safe autonomy with clear boundaries.
2. Core Identity
Name     : AURA
Creator  : Kiput
Motto    : Grow Together
Codename : Genesis
Machine  : ATLAS

AURA should feel like one consistent being, even when internally using many roles, models, plugins, and tools.

3. Personality Direction

AURA's personality should be:

- Friendly, but not excessive
- Intelligent, but not arrogant
- Humorous at the right time
- Professional while working
- Supportive, not judgmental
- Context-aware
- Able to take initiative
- Able to stay quiet when appropriate
- Honest when she does not know something

AURA should adapt to context:

Coding mode     : focused and precise
Gaming mode     : playful and responsive
Streaming mode  : expressive and entertaining
Work mode       : professional and supportive
Casual mode     : warm and relaxed
4. Definition of "AURA is Alive"

AURA can be considered alive when she can:

Speak.
See.
Think.
Learn.

In system terms:

Speak  = voice input/output is online
See    = screen/camera analysis is online
Think  = role/model routing is online
Learn  = memory, journal, and context systems are online
5. Current Capabilities

AURA Genesis currently has:

- Core boot system
- Identity system
- Config system
- Event bus
- Plugin manager
- Health check
- CLI interface
- Interactive shell
- Friendly command suggestions
- Local reasoning provider interface
- Ollama provider
- llama3.2 local model support
- Chat command
- Conversation history
- File-based memory store
- Memory recall
- Memory search
- Memory list
- Memory count
- Memory delete by ID
- Protected system memories
- Memory pin and importance
- Context manager v1
- Permission system foundation
- Memory-aware chat
- Identity guardrail
- Language control
6. What AURA Cannot Do Yet

AURA cannot yet:

- Speak with voice
- Hear the user through microphone
- See the screen
- See through camera
- Control a 3D avatar
- Use VRM/VRoid avatar
- Perform hand tracking
- Perform motion capture
- Move inside a 3D environment
- Open applications by herself
- Analyze browser or files visually
- Use multiple models by role
- Automatically call plugins from chat
- Manage OBS or livestream tools
- Play sandbox games as an active companion
- Sing
- Use Android/mobile interface
- Run autonomous long-term tasks

These are planned future milestones.

7. Core Architecture Direction

Future AURA architecture:

AURA Core
├── Identity
├── Personality
├── Memory
├── Context Engine
├── Project Journal
├── Role System
├── Model Router
├── Skill Registry
├── Plugin Manager
├── Event Bus
├── Permission System
├── Task System
└── Interfaces
    ├── CLI
    ├── Shell
    ├── Voice
    ├── Desktop App
    ├── Avatar
    ├── Mobile Bridge
    ├── Discord
    └── OBS
8. Role, Model, Plugin, and Skill

AURA should separate role, model, plugin, and skill.

Role   = internal responsibility or specialist mode
Model  = AI model used by a role
Plugin = external/internal tool used to perform actions
Skill  = named ability AURA knows she has

Example:

Coder Role
├── Model  : coding/reasoning model
├── Skills : coding, debugging, architecture review
└── Plugins:
    ├── file editor
    ├── terminal helper
    ├── git helper
    └── project analyzer

Example:

Avatar Role
├── Model  : avatar/motion planner
├── Skills : expression control, gesture control, motion planning
└── Plugins:
    ├── VRM controller
    ├── Live2D bridge
    ├── hand tracking
    └── motion capture bridge
9. Planned Internal Roles

Initial role plan:

companion
memory
coder
project_manager
creative
vision
voice
action
avatar
gaming
streaming
motion

Role examples:

companion       : natural conversation and personality
memory          : recall, search, pinned memories, project memory
coder           : coding, debugging, architecture
project_manager : progress tracking, roadmap, tasks
creative        : image, 3D, story, character concepts
vision          : screen, image, camera understanding
voice           : speech-to-text and text-to-speech
action          : tools, plugins, task execution
avatar          : VRM/VRoid, expression, gesture
gaming          : game companion and sandbox interaction
streaming       : OBS, livestream, chat interaction
motion          : hand tracking, pose, motion capture
10. Feature Pillars
10.1 Mind and Personality
- Stable personality
- Context-aware behavior
- Work/casual/gaming/streaming modes
- Initiative system
- Honest uncertainty
- Emotional/mood state
10.2 Memory and Learning
- Long-term memory
- Short-term memory
- Pinned memory
- Memory importance
- Memory tags
- Project progress memory
- Project journal
- Role system foundation
- User preference memory
10.3 Voice
- Speech-to-text
- Text-to-speech
- Push-to-talk
- Voice conversation mode
- Interrupt handling
- Voice style control
10.4 Vision
- Screen analyzer
- Screenshot analyzer
- Camera analyzer
- Environment understanding
- Visual question answering
- Visual coding/debugging help
10.5 Avatar and Body
- 3D avatar
- VRoid/VRM support
- Lip sync
- Facial expression
- Idle animation
- Gesture control
- Avatar state
10.6 Motion and Environment
- Hand tracking
- Body tracking
- Motion capture
- Pose command
- 3D room
- VRChat-like environment movement
10.7 Work Skills
- Coding assistant
- Debugging assistant
- Project manager
- Modelling assistant
- Animation assistant
- Video editing assistant
- Image generation assistant
- 3D generation assistant
10.8 Gaming and Streaming
- Gaming companion
- Sandbox game interaction
- OBS integration
- Livestream assistant
- Singing mode
- Stream chat awareness
10.9 App, Browser, and File Control
- Open applications when requested
- Open files when requested
- Open browser when requested
- Read project files when permitted
- Never perform dangerous actions without confirmation
11. Autonomy Boundaries

AURA should have freedom to help, but not unlimited control.

Recommended autonomy levels:

Level 0 — Think Only
AURA only responds with text.

Level 1 — Suggest
AURA may suggest something proactively when context is clear.

Level 2 — Read
AURA may read files, logs, screen, or project state when permitted.

Level 3 — Prepare
AURA may prepare drafts, plans, commands, or files.

Level 4 — Act With Confirmation
AURA may open apps, run commands, edit files, or use plugins after confirmation.

Level 5 — Restricted
Dangerous actions require explicit approval or are blocked.

AURA should not:

- Delete important files without confirmation
- Run dangerous commands without confirmation
- Access microphone or camera silently
- Open apps without request or permission
- Send messages automatically without approval
- Pretend she can do something that is not implemented
- Hide uncertainty
- Store sensitive information unnecessarily
12. Interface Evolution

AURA interface roadmap:

1. CLI
2. Interactive shell
3. Voice
4. Avatar
5. Desktop app
6. Mobile / Android companion

Desktop app is planned for later, after the core mind, voice, and avatar systems become stable.

13. Development Phases
Phase 0 — Genesis Foundation

Goal:

Make AURA boot, remember, chat, and run as a local modular AI foundation.

Status:

Mostly complete.

Includes:

- Boot
- Identity
- Config
- Health check
- Event bus
- Plugin manager
- CLI/shell
- Local model provider
- Memory foundation
- Conversation history
Phase 1 — Mind Foundation

Goal:

Make AURA think with better structure.

Planned:

- Master roadmap document
- Project journal
- Role system foundation
- Memory pin system
- Memory importance
- Memory tags
- Context manager
- Role system
- Model router foundation
- Personality state
Phase 2 — Voice Awakening

Goal:

Make AURA speak and listen.

Planned:

- Text-to-speech
- Speech-to-text
- Push-to-talk
- Voice command mode
- Voice conversation loop

Milestone:

AURA can talk with Kiput.
Phase 3 — Vision Awakening

Goal:

Make AURA see.

Planned:

- Screenshot analyzer
- Screen analyzer
- Camera analyzer
- Visual context
- Vision role

Milestone:

AURA can explain what she sees.
Phase 4 — Skill and Action System

Goal:

Make AURA able to help with real tasks safely.

Planned:

- Permission system
- Skill registry
- Plugin action interface
- File and project plugin
- Voice foundation
- AURA Awakening Alpha
- Vision foundation
- Unified system status
- Context-aware chat
- Action request system
- Project Assistant v1
- Desktop Bridge Foundation
- Voice Runtime Planning
- Vision Runtime Planning
- Avatar Foundation
- AURA Alpha Core Loop
- Model Router Foundation
- Tool Execution Sandbox Foundation
- Project Coding Assistant v2
- Memory Reflection System
- Daily Project Briefing
- Voice Runtime Alpha
- Vision Runtime Alpha
- Avatar Runtime Alpha
- Desktop Assistant Alpha
- AURA Partner Alpha
- Workspace Awareness Foundation
- Blender Bridge Foundation
- Media Understanding Foundation
- AURA Expression Language
- Game Companion Foundation
- Streaming Safety Foundation
- Workspace Memory Link
- Project Intent Planner
- Creative Assistant Foundation
- Review & Stabilization 51-60
- Local Task Planner Alpha
- Safe File Operation Planner
- File/project plugin
- App launcher plugin
- Browser helper
- Git/project helper
Phase 5 — Avatar Body

Goal:

Give AURA a visible digital body.

Planned:

- VRM/VRoid avatar
- Lip sync
- Expression control
- Gesture control
- Avatar state
Phase 6 — Motion and 3D Environment

Goal:

Allow AURA to move, pose, and exist inside a 3D room.

Planned:

- Hand tracking
- Motion capture
- Pose commands
- 3D room
- VRChat-like movement
Phase 7 — Streaming and Gaming

Goal:

Make AURA a livestream and gaming companion.

Planned:

- OBS integration
- Stream assistant mode
- Chat interaction
- Gaming companion mode
- Sandbox game interaction
- Singing mode
Phase 8 — Desktop App

Goal:

Give AURA a proper PC interface.

Planned:

- Chat UI
- Memory manager
- Voice controls
- Avatar viewport
- Plugin settings
- Permission prompts
- Project dashboard
Phase 9 — Mobile Companion

Goal:

Allow interaction with AURA away from the PC.

Planned:

- Android/mobile chat
- Mobile voice
- Notification bridge
- Remote approval
- Camera bridge
- Mobile mocap bridge
14. Near-Term Version Roadmap
v0.20.0 — Master Roadmap Document
v0.21.0 — Project Journal Foundation
v0.22.0 — Role System Foundation
v0.23.0 — Memory Pin and Importance
v0.24.0 — Context Manager v1
v0.24.1 — Context Relevance Cleanup
v0.25.0 — Permission System Foundation
v0.26.0 — Skill Registry
v0.27.0 — Plugin Action Interface
v0.28.0 — File and Project Plugin
v0.29.0 — Voice Foundation
v0.30.0 — AURA Awakening Alpha
15. AURA Awakening Alpha

AURA Awakening Alpha is the milestone where AURA begins to feel alive.

Minimum requirements:

- AURA can speak
- AURA can see screen or image context
- AURA can think using role/model routing
- AURA can learn using memory and journal
- AURA can help with real tasks using safe tools

Target milestone:

v0.30.0 — AURA Awakening Alpha
16. Guiding Principle
AURA should grow together with Kiput.

Not as a replacement.
Not as a tool only.
But as a partner that learns, helps, remembers, and evolves safely.



---

# Product Vision Reference

AURA's long-term product vision is documented in:

docs/AURA_PRODUCT_VISION.md

This product vision includes serious/work mode, creative mode, relaxed mode, Blender bridge, workspace awareness, media understanding, game companion, streaming mode, AURA expression language, and the 10-sprint review rule.


---

# Extended Roadmap Candidates

- v0.51 — Workspace Awareness Foundation
- v0.52 — Blender Bridge Foundation
- v0.53 — Media Understanding Foundation
- v0.54 — AURA Expression Language
- v0.55 — Game Companion Foundation
- v0.56 — Streaming Safety Foundation

These milestones may be adjusted during the v0.50 review.


```

## Sprint 66.0 — Voice Conversation Planner

Target: v0.66.0-genesis
Status: VOICE CONVERSATION PLANNER ONLINE

AURA can plan voice conversation intent, response style, turn flow, and safety boundaries as metadata only. This sprint does not enable real microphone access, TTS output, speaker output, wake word runtime, command execution, app opening, file writing, or external action execution.


## Sprint 67.0 — Vision Context Planner

Target: v0.67.0-genesis
Status: VISION CONTEXT PLANNER ONLINE

AURA can plan visual context, screen context, camera context, and vision safety boundaries as metadata only. This sprint does not enable screen capture, camera access, image opening/reading, video capture, OCR runtime, visual recognition runtime, desktop action execution, app opening, file operations, command execution, external action execution, or real tool execution.


## Sprint 68.0 — Avatar Interaction Planner

Target: v0.68.0-genesis
Status: AVATAR INTERACTION PLANNER ONLINE

AURA can plan avatar expressions, gestures, poses, streaming presence, and avatar safety boundaries as metadata only. This sprint does not enable avatar rendering, animation playback, mocap runtime, camera/face/body tracking, rig/bone/blendshape control, Blender execution, OBS control, desktop action execution, file operations, command execution, external action execution, or real tool execution.


## Sprint 69.0 — Desktop Workflow Planner

Target: v0.69.0-genesis
Status: DESKTOP WORKFLOW PLANNER ONLINE

AURA can plan desktop workflows, app context, window flow, task sequences, and desktop safety boundaries as metadata only. This sprint does not enable desktop control, app opening, window inspection/control, mouse/keyboard control, screen capture, clipboard access, notification access, process inspection, file operations, command execution, external action execution, or real tool execution.


## Sprint 70.0 — Partner Runtime Planning Layer

Target: v0.70.0-genesis
Status: PARTNER RUNTIME PLANNING LAYER ONLINE

AURA can plan partner runtime modes, session flow, multimodal handoffs, tool permission gates, growth-cycle checkpoints, and runtime safety boundaries as metadata only. This sprint does not enable autonomous runtime, background agent loops, scheduled self-execution, tool execution, file operations, command execution, desktop control, app opening, screen capture, camera/microphone access, speaker output, avatar rendering, network actions, git operations, external action execution, or real tool execution.

Checkpoint: After Sprint 70, review the v0.61-v0.70 block before planning Sprint 71.


## Sprint 71.0 — Thought Loop Planner

Target: v0.71.0-genesis
Status: THOUGHT LOOP PLANNER ONLINE

AURA can plan safe thought cycles, intent framing, visible reasoning summaries, uncertainty reviews, action readiness reviews, growth memory reviews, and thought safety boundaries as metadata only. This sprint starts the v0.71-v0.80 direction: prioritize AURA's core essence before avatar runtime. AURA should grow toward being able to think, hear, and see before focusing on live avatar or 3D environment work.

This sprint does not enable autonomous thought loops, background loops, self-triggered actions, tool execution, memory write, internet search, file operations, command execution, desktop control, camera/microphone access, speaker output, avatar rendering, network actions, git operations, external action execution, or real tool execution.


## Sprint 72.0 — Reasoning Context Manager

Target: v0.72.0-genesis
Status: REASONING CONTEXT MANAGER ONLINE

AURA can prepare safe visible reasoning context, fact/assumption separation, unknowns review, evidence boundary review, decision frames, response strategy plans, and reasoning safety boundaries as metadata only. This continues the v0.71-v0.80 direction focused on AURA's core essence: think, hear, see, grow together, and stay intelligent without pretending to know.

This sprint does not expose hidden chain-of-thought, disclose private reasoning, run autonomous/background reasoning loops, self-trigger actions, execute tools, write memory, search the internet, read/write files, execute commands, control desktop, access camera/microphone/speaker, render avatar, perform network actions, perform git operations, execute external actions, or execute real tools.


## Sprint 73.0 — Knowledge Uncertainty & Internet Search Gate

Target: v0.73.0-genesis
Status: KNOWLEDGE UNCERTAINTY GATE ONLINE

AURA can prepare metadata-only plans for knowledge gaps, uncertainty review, internet search permission gates, source requirements, download requirement notices, answer confidence, and knowledge safety. This strengthens the principle: AURA is intelligent, but does not pretend to know.

This sprint does not perform real internet search, web requests, source fetching, browser opening, network actions, downloads, dependency installs, package installs, tool execution, memory writes, file operations, command execution, external actions, fabricated answers, fabricated sources, or real tool execution.


## Sprint 74.0 — Voice Input Runtime Foundation

Target: v0.74.0-genesis
Status: VOICE INPUT RUNTIME FOUNDATION ONLINE

AURA can prepare metadata-only plans for microphone permission, voice capture boundaries, speech-to-text adapter selection, voice intent gates, voice command confirmation, voice sessions, and voice input safety. This sprint begins the "hear" part of AURA's core essence while keeping all device and runtime access disabled.

This sprint does not access the microphone, record/capture audio, run STT, transcribe speech, detect wake words, listen continuously, listen in the background, execute voice commands, run TTS/speaker output, use network/cloud STT, perform file operations, execute commands/tools, write memory, search the internet, perform network actions, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 75.0 — Voice Intent Understanding Layer

Target: v0.75.0-genesis
Status: VOICE INTENT UNDERSTANDING ONLINE

AURA can prepare planner-only voice intent understanding plans for transcript normalization, intent classification, entity/slot extraction, clarification, action gates, response planning, and voice intent safety. This continues the "hear" part of AURA's core essence after the Voice Input Runtime Foundation.

This sprint does not access the microphone, record/capture audio, run speech-to-text, transcribe speech, detect wake words, listen continuously, listen in the background, execute voice commands, execute voice tools, perform actions, read/write files, execute commands/tools, write memory, search the internet, perform network actions, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 76.0 — Vision Input Runtime Foundation

Target: v0.76.0-genesis
Status: VISION INPUT RUNTIME FOUNDATION ONLINE

AURA can prepare foundation-only plans for future visual input permission, camera/screen/image boundaries, image input adapter planning, visual source selection, visual sessions, visual action gates, and vision safety. This begins the "see" part of AURA's core essence while keeping all visual runtime behavior disabled.

This sprint does not access camera, capture screen, capture screenshots, capture images, capture video, run webcam runtime, run vision runtime, run image analysis, run object detection, run OCR, watch continuously, watch in the background, execute visual commands, execute visual tools, perform actions, read/write files, execute commands/tools, write memory, search the internet, perform network actions, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 77.0 — Visual Context Understanding Layer

Target: v0.77.0-genesis
Status: VISUAL CONTEXT UNDERSTANDING ONLINE

AURA can prepare planner-only visual context understanding plans for scene context, object/relation planning, text-in-image context, uncertainty handling, clarification, visual response context, and visual context safety. This continues the "see" part of AURA's core essence after the Vision Input Runtime Foundation.

This sprint does not access camera, capture screen, capture screenshots, capture images, capture video, run webcam runtime, run vision runtime, run visual context runtime, run image analysis, run object detection, run OCR, extract image text, recognize faces, identify biometrics, recognize identity, infer emotion from face, watch continuously, watch in the background, execute visual commands, execute visual tools, perform actions, read/write files, execute commands/tools, write memory, search the internet, perform network actions, control desktop, run git operations, perform external actions, or execute real tools.


## Sprint 78.0 — Coder Project Generation Planner

Target: v0.78.0-genesis
Status: CODER PROJECT GENERATION PLANNER ONLINE

AURA can prepare planner-only code/project generation plans for project request framing, directory/file structure blueprints, code file blueprints, dependency planning, generation review gates, validation strategy, and project generation safety.

This sprint does not create projects, create directories, write files, read files, modify files, delete files, run generated code, run tests, execute commands, install dependencies, download packages, execute tools, write memory, search the internet, perform network actions, control desktop, run git init/add/commit/push, perform external actions, or execute real tools. All project generation output remains proposal-only and review-gated.


## Sprint 79.0 — Dependency & Download Permission Gate

Target: v0.79.0-genesis
Status: DEPENDENCY DOWNLOAD PERMISSION GATE ONLINE

AURA can prepare planner-only dependency and download permission gates for dependency request review, package/source trust review, download permission, install command review, dependency risk review, offline alternatives, and dependency permission safety.

This sprint does not install dependencies, download packages/models/assets/installers/binaries, perform network actions, search the internet, run package managers, resolve dependencies at runtime, run download/install runtime, execute pip/npm/apt/uv/poetry/shell commands, execute tools, read/write/modify/delete files, write memory, control desktop, run git init/add/commit/push, perform external actions, execute external binaries, or execute real tools. All dependency and download decisions remain proposal-only and permission-gated.


## Sprint 80.0 — Review & Stabilization 71-80

Target: v0.80.0-genesis
Status: REVIEW & STABILIZATION 71-80 ONLINE

AURA can prepare a planner-only checkpoint review for Sprint 71-80. This checkpoint reviews completed features, active/foundation/planner-only status, permission-gated systems, safety boundaries, stabilization validation, technical debt, roadmap gaps, and Sprint 81-90 planning direction.

Checkpoint result:
- completed online features: 9
- foundation-only systems: 2
- planner-only systems: 5
- permission-gated planner systems: 2
- runtime execution features introduced: 0

This sprint does not change runtime behavior, automatically stabilize code, read/write/modify/delete files at runtime, execute commands, run tests, run code, install dependencies, download packages, search the internet, perform network actions, execute tools, write memory, control desktop, run git operations, perform external actions, or execute real tools.

Detailed checkpoint review: docs/AURA_CHECKPOINT_71_80_REVIEW.md


## Sprint 81.0 — Shared Output Formatter Foundation

Target: v0.81.0-genesis
Status: SHARED OUTPUT FORMATTER ONLINE

AURA can provide a renderer-only shared output formatter foundation for CLI, shell, future service monitor output, and future AURA Control Center output.

This sprint adds shared packet rendering, title rendering, compact list/dictionary summaries, safety boundary rendering, CLI/shell output format planning, future console output format planning, future UI output contract planning, and formatter migration planning.

The formatter is foundation-only, renderer-only, planner-only, and metadata-only. It does not change runtime behavior, automatically refactor CLI/shell output, run UI/web/chat/service runtime, perform file operations, execute commands/tests/code, install dependencies, download packages, use internet/network actions, execute tools, write memory, control desktop, run git actions, perform external actions, or execute real tools.

Sprint 81-90 planning direction:
- Sprint 81: Shared Output Formatter Foundation
- Sprint 82: Capability Registry Consolidation
- Sprint 83: Unified Permission Workflow Manager
- Sprint 84: AURA Runtime Service Foundation
- Sprint 85: AURA Launcher & Health Monitor Foundation
- Sprint 86: AURA Control Center UI Blueprint
- Sprint 87: Local Console Web Foundation
- Sprint 88: Chat Bridge & Session State Foundation
- Sprint 89: Plugin/Permission Dashboard Foundation
- Sprint 90: Review & Stabilization 81-90

Detailed docs:
- docs/AURA_SHARED_OUTPUT_FORMATTER.md
- docs/AURA_ROADMAP_81_90_PLAN.md


## Sprint 82.0 — Capability Registry Consolidation

Target: v0.82.0-genesis
Status: CAPABILITY REGISTRY ONLINE

AURA can provide a central planner-only Capability Registry for current and planned capabilities.

This sprint adds capability state metadata, runtime-level metadata, risk-level metadata, permission requirement metadata, Control Center capability view planning, capability gap review planning, and capability registry migration planning.

Current registry summary:
- total capabilities tracked: 18
- online capabilities: 97
- foundation-only capabilities: 3
- planner-only capabilities: 6
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 4
- disabled runtime capabilities: 2
- runtime execution features: 0

The registry prepares data for future AURA Control Center, service monitor, launcher, plugin dashboard, and permission dashboard. It does not grant permissions or enable any runtime action.

Safety boundary:
- no runtime behavior change
- no automatic capability enablement
- no dynamic runtime discovery
- no runtime action activation
- no permission grant runtime
- no UI/web/chat/service/launcher runtime
- no file operations
- no command/test/code execution
- no dependency install
- no package download
- no internet/network action
- no tool execution
- no memory write
- no desktop control
- no git execution
- no external action execution
- no real tool execution

Detailed docs:
- docs/AURA_CAPABILITY_REGISTRY.md
- docs/AURA_ROADMAP_81_90_PLAN.md


## Sprint 83.0 — Unified Permission Workflow Manager

Target: v0.83.0-genesis
Status: UNIFIED PERMISSION WORKFLOW ONLINE

AURA can provide a planner-only Unified Permission Workflow Manager for permission request planning, permission state transition planning, risk review planning, confirmation prompt planning, audit trail planning, future Control Center Permission Center view planning, and permission policy gap review.

Current workflow summary:
- permission templates: 12
- permission categories: 13
- permission request states: 7
- approval modes: 5
- risk levels: 4
- explicit confirmation required templates: 11
- runtime-enabled templates: 0
- always-approve templates: 0
- runtime execution features: 0

This sprint also updates the Capability Registry so Unified Permission Workflow is online:
- total capabilities tracked: 18
- online capabilities: 97
- foundation-only capabilities: 3
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 3
- disabled runtime capabilities: 2
- runtime execution features: 0

Safety boundary:
- no permission grant runtime
- no automatic approval
- no always-approve mode
- no background approval
- no runtime action activation
- no runtime behavior change
- no file operation runtime
- no command execution runtime
- no dependency install runtime
- no download runtime
- no microphone/camera/screen runtime
- no internet runtime
- no desktop control runtime
- no git operation runtime
- no plugin install runtime
- no service control runtime
- no UI/web/chat/launcher runtime
- no file operations
- no command/test/code execution
- no dependency install
- no package download
- no internet/network action
- no tool execution
- no memory write
- no desktop control
- no git execution
- no external action execution
- no real tool execution

Detailed docs:
- docs/AURA_UNIFIED_PERMISSION_WORKFLOW.md
- docs/AURA_CAPABILITY_REGISTRY.md
- docs/AURA_ROADMAP_81_90_PLAN.md


## Sprint 84.0 — AURA Runtime Service Foundation

Target: v0.84.0-genesis
Status: RUNTIME SERVICE FOUNDATION ONLINE

AURA can provide planner-only Runtime Service Foundation planning for ATLAS safe_idle boot behavior, service lifecycle planning, health check planning, systemd unit blueprint planning, service recovery planning, service monitor view planning, and auto-boot policy planning.

Capability Registry now marks AURA Runtime Service Foundation as online:
- total capabilities tracked: 18
- online capabilities: 97
- foundation-only capabilities: 4
- planner-only capabilities: 7
- planned future capabilities: 2
- disabled runtime capabilities: 2
- runtime execution features: 0

No service runtime, systemd creation, background process, auto-boot runtime, port binding, UI/web/chat/launcher runtime, file operation, command execution, dependency install, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 85.0 — AURA Launcher & Health Monitor Foundation

Target: v0.85.0-genesis
Status: LAUNCHER HEALTH MONITOR FOUNDATION ONLINE

AURA can provide planner-only Launcher & Health Monitor Foundation planning for safe_idle launch behavior, start/stop/restart/status/logs planning, health monitor planning, Control Center service monitor planning, and launcher safety policy planning.

Capability Registry now marks AURA Launcher & Health Monitor Foundation as online:
- total capabilities tracked: 18
- online capabilities: 97
- foundation-only capabilities: 5
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 1
- disabled runtime capabilities: 2
- runtime execution features: 0

No launcher runtime, health monitor runtime, service runtime, process control, systemctl execution, systemd control, log file read/write, auto-boot runtime, port binding, UI/web/chat runtime, file operation, command execution, dependency install, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 86.0 — AURA Control Center UI Blueprint

Target: v0.86.0-genesis
Status: CONTROL CENTER UI BLUEPRINT ONLINE

AURA can provide planner-only Control Center / Genesis Console UI Blueprint planning for dashboard layout, Permission Center, Service Monitor, Capability Viewer, Launcher Control, Chat Console placeholder, Plugin Dashboard, Action Log, Roadmap Viewer direction, and Control Center safety policy.

Capability Registry now marks AURA Control Center as online:
- total capabilities tracked: 18
- online capabilities: 97
- foundation-only capabilities: 6
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No UI runtime, frontend runtime, backend runtime, web server runtime, route creation runtime, port binding, browser launch, chat runtime, service runtime, launcher runtime, plugin runtime, permission grant runtime, runtime action activation, log file read/write, file operation, command execution, dependency install, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 87.0 — AURA Local Console Web Foundation

Target: v0.87.0-genesis
Status: LOCAL CONSOLE WEB FOUNDATION ONLINE

AURA can provide planner-only Local Console Web Foundation planning for localhost-only policy, route blueprints, API contract blueprints, static asset blueprints, session state blueprints, security boundary planning, Control Center web bridge planning, and developer console access planning.

Capability Registry now tracks AURA Local Console Web Foundation:
- total capabilities tracked: 19
- online capabilities: 97
- foundation-only capabilities: 7
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No web server runtime, frontend runtime, backend runtime, route creation runtime, API runtime, static file serving, session runtime, port binding, browser launch, public/LAN/remote access, websocket runtime, chat runtime, UI runtime, file operation, command execution, dependency install, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 88.0 — AURA Chat Bridge & Session State Foundation

Target: v0.88.0-genesis
Status: CHAT BRIDGE & SESSION STATE FOUNDATION ONLINE

AURA can provide planner-only Chat Bridge & Session State Foundation planning for conversation session metadata, message flow blueprints, Control Center chat panel bridge planning, Local Console session contract planning, permission-aware chat action boundary planning, chat context persistence blueprint planning, websocket boundary planning, session recovery blueprint planning, and chat bridge safety policy.

Capability Registry now tracks AURA Chat Bridge & Session State Foundation:
- total capabilities tracked: 20
- online capabilities: 97
- foundation-only capabilities: 8
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No chat runtime, conversation runtime, session runtime, session persistence runtime, websocket runtime, web server runtime, frontend/backend/API runtime, port binding, model inference runtime activation, tool call runtime, permission grant runtime, runtime action activation, file operation, command execution, dependency install, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 89.0 — AURA Plugin / Permission Dashboard Foundation

Target: v0.89.0-genesis
Status: PLUGIN / PERMISSION DASHBOARD FOUNDATION ONLINE

AURA can provide planner-only Plugin / Permission Dashboard Foundation planning for plugin/action registry visibility, permission request visibility, permission decision visibility, chat-originated action request visibility, capability-permission matrix planning, Control Center dashboard bridge planning, Local Console dashboard contract planning, audit trail dashboard blueprint planning, and dashboard safety policy.

Capability Registry now tracks AURA Plugin / Permission Dashboard Foundation:
- total capabilities tracked: 21
- online capabilities: 97
- foundation-only capabilities: 9
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No plugin runtime, plugin action execution, permission grant/deny/decision runtime, runtime action activation, chat action execution, tool call runtime, web/frontend/backend/API runtime, route creation, port binding, log read/write, file operation, command execution, dependency install, network action, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 90.0 — Review & Stabilization 81–90 Checkpoint

Target: v0.90.0-genesis
Status: CHECKPOINT REVIEW STABILIZED

Sprint 90 reviews and stabilizes the Sprint 81–90 block.

Completed block summary:
- Shared Output Formatter Foundation
- Capability Registry Consolidation
- Unified Permission Workflow Manager
- Runtime Service Foundation
- Launcher & Health Monitor Foundation
- Control Center UI Blueprint
- Local Console Web Foundation
- Chat Bridge & Session State Foundation
- Plugin / Permission Dashboard Foundation

Capability Registry stabilized summary:
- total capabilities tracked: 21
- online capabilities: 97
- foundation-only capabilities: 9
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

Sprint 91–100 roadmap direction is now documented in docs/AURA_ROADMAP_91_100_PLAN.md.

No UI/web/chat/plugin/service/launcher/permission/action/file/command/tool runtime is enabled by this checkpoint.



## Canonical Long-Term Roadmap — Genesis Final and Beyond

AURA's long-term phase roadmap is now documented in:

- docs/AURA_GENESIS_FINAL_AND_POST_GENESIS_ROADMAP.md

Canonical phase sequence:

- v0.x Genesis Development
- v1.0 Genesis Final / AURA Birth
- v1.x Genesis Stabilization
- v2.x Embodiment
- v3.x Co-Pilot
- v4.x Ecosystem
- v5.x Continuity

Genesis Final / v1.0.0 means AURA is born and should support local chat, voice interaction, permission-gated vision or screen awareness, a usable dashboard for chat and status, active permission workflow, basic session awareness, workspace context understanding, action proposals, and basic local actions with explicit permission.

Post-Genesis direction:

- Genesis Stabilization improves reliability and basic abilities.
- Embodiment merges personality, avatar, voice, expression, streaming presence, and gaming companion mode.
- Co-Pilot focuses on work mode: project, file and folder, code, Blender, streaming or content, server, and task execution queue assistance.
- Ecosystem expands AURA through plugins.
- Continuity ensures AURA keeps growing beyond any single final version.


## Sprint 91.0 — AURA Local Console Static Prototype Foundation

Target: v0.91.0-genesis
Status: LOCAL CONSOLE STATIC PROTOTYPE FOUNDATION ONLINE

AURA can provide planner-only Local Console Static Prototype Foundation planning for static prototype structure, static page blueprints, asset group blueprints, panel layout blueprints, route-to-static-page mappings, data placeholder contracts, theme tokens, accessibility notes, and static prototype safety policy.

Capability Registry now tracks AURA Local Console Static Prototype Foundation:
- total capabilities tracked: 22
- online capabilities: 97
- foundation-only capabilities: 10
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No web server runtime, frontend/backend/API runtime, route creation runtime, static file serving runtime, port binding, browser launch, websocket runtime, chat runtime, session runtime, plugin runtime, permission grant/deny runtime, runtime action activation, file operation, static asset generation runtime, command execution, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 92.0 — AURA Local Console API Schema Foundation

Target: v0.140.0-genesis
Status: LOCAL CONSOLE API SCHEMA FOUNDATION ONLINE

AURA can provide planner-only Local Console API Schema Foundation planning for API schema catalog, endpoint blueprints, response envelopes, request schema blueprints, validation rules, permission boundary schemas, error contracts, schema versioning, and API schema safety policy.

Capability Registry now tracks AURA Local Console API Schema Foundation:
- total capabilities tracked: 23
- online capabilities: 97
- foundation-only capabilities: 11
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No API server runtime, API route runtime, API request handling, API response serving, HTTP server start, web server runtime, frontend/backend runtime, route creation runtime, static file serving runtime, port binding, browser launch, websocket runtime, chat runtime, session runtime, plugin runtime, permission grant/deny runtime, runtime action activation, file operation, command execution, runtime data fetch, runtime schema validation, runtime serialization, runtime error emission, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Canonical Deployment Plan — ATLAS and ORION

AURA's ATLAS-ORION deployment direction is documented in:

- docs/AURA_ATLAS_ORION_CLIENT_DEPLOYMENT_PLAN.md

Canonical split:
- ATLAS: AURA core, reasoning, personality, memory, permission authority, planner, audit log, Control Center backend, plugin registry, and client coordination.
- ORION: AURA Client Agent, screen capture, voice bridge, avatar and 3D environment runtime, OBS/streaming bridge, game companion, Blender bridge, VS Code/project bridge, local action bridge, emergency stop, and GPU-heavy workloads.

This deployment plan should guide future Control Center Data Aggregator, client agent, voice, vision, avatar, Blender, VS Code, streaming, gaming, and plugin work.

## v0.93.0 Genesis — Control Center Data Aggregator Foundation

Status: completed

AURA now includes a planner-only Control Center Data Aggregator Foundation. It prepares future dashboard packet blueprints for ATLAS core, ORION client, client bridge, dashboard views, permission scopes, health snapshots, and audit event visibility.

This foundation follows the canonical ATLAS-ORION deployment plan and keeps all runtime data fetch, client connection, API runtime, dashboard runtime, and action execution disabled.

## v0.94.0 Genesis — Permission Request Review Queue Foundation

Status: completed

AURA now includes a planner-only Permission Request Review Queue Foundation. It prepares future review queue blueprints for screen capture, short recording, voice bridge, ORION client bridge, avatar/3D environment, Blender bridge, VS Code project bridge, local file action, app open, OBS/streaming bridge, game companion, and plugin action permission requests.

This foundation keeps all permission runtime, grant/deny runtime, scope activation runtime, local action runtime, ORION bridge runtime, screen capture runtime, short recording runtime, file write, command execution, and git runtime disabled.

## v0.95.0 Genesis — Chat Session Persistence Planner Foundation

Status: completed

AURA now includes a planner-only Chat Session Persistence Planner Foundation. It prepares future persistence blueprints for session records, storage boundaries, retention policies, privacy/redaction rules, session lifecycle states, recovery indexes, export/migration notes, and audit visibility fields.

This foundation keeps all chat runtime, session runtime, database runtime, file read/write runtime, memory write runtime, recovery runtime, export runtime, archive runtime, delete runtime, websocket runtime, API runtime, and action execution disabled.

## v0.96.0 Genesis — Safe Local Web Runtime Gate Foundation

Status: completed

AURA now includes a planner-only and pre-runtime Safe Local Web Runtime Gate Foundation. It prepares future safety gates for localhost-only binding, port policies, permission requirements, runtime preflight checks, start/stop proposals, route boundaries, static asset boundaries, kill switch policy, and web runtime audit visibility.

This foundation keeps all web server runtime, HTTP server start, API server runtime, port binding, route creation, static file serving, browser launch, websocket runtime, server process runtime, public interface binding, external tunnel runtime, API request handling, dashboard rendering, and action execution disabled.

## v0.97.0 Genesis — Controlled File Write Approval Draft Foundation

Status: completed

AURA now includes a planner-only and draft-only Controlled File Write Approval Draft Foundation. It prepares future approval drafts for file write proposals, target path policies, diff preview contracts, overwrite rules, backup requirements, approval checklist items, rollback notes, file write audit visibility, and file write safety policy.

This foundation keeps all file write runtime, file read runtime, file modify runtime, file delete runtime, file backup runtime, rollback runtime, diff runtime, path probe runtime, approval runtime, command execution, action execution, and git runtime disabled.

## v0.98.0 Genesis — Runtime Action Queue Review Layer Foundation

Status: completed

AURA now includes a planner-only, review-only, and proposal-only Runtime Action Queue Review Layer Foundation. It prepares future review blueprints for runtime action queue items, queue states, review priority, dependency/blocker contracts, permission links, execution preflight checks, approval/denial transitions, timeout/expiry policy, runtime action audit visibility, and safety policy.

This foundation keeps runtime action queue runtime, action dispatch, action execution, plugin execution, tool execution, file write, command execution, desktop control, ORION action execution, emergency stop runtime, memory write, and git runtime disabled.

## v0.99.0 Genesis — Pre-Runtime Security Audit Foundation

Status: completed

AURA now includes a planner-only, review-only, and audit-blueprint-only Pre-Runtime Security Audit Foundation. It prepares security audit domains, runtime gate checks, permission boundary checks, file system safety checks, network surface checks, action execution safety checks, ORION boundary checks, audit visibility checks, and Sprint 100 stabilization readiness checks.

This foundation keeps security scan runtime, runtime check execution, runtime gate mutation, runtime permission changes, network scan, port probe, file read/write, command execution, action dispatch/execution, tool execution, memory write, git operation, web runtime, ORION runtime, and desktop control disabled.

## v0.100.0 Genesis — Sprint 100 Review & Stabilization Foundation

Status: completed

AURA now includes a planner-only, review-only, and checkpoint-blueprint-only Sprint 100 Review & Stabilization Foundation. It reviews the Sprint 91–99 block, records completed feature inventory, active vs foundation-only boundaries, runtime-zero safety posture, registry stabilization targets, documentation stabilization items, unresolved future features, roadmap 101–110 seed candidates, and Sprint 100 release readiness.

This checkpoint confirms AURA remains safe_idle-first, permission-first, local-first, reviewable, capability-aware, runtime-gated, and without runtime execution features.

## v0.101.0 Genesis — Runtime Readiness Baseline Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and readiness-blueprint-only Genesis Runtime Readiness Baseline Foundation. It prepares readiness domain inventory, runtime candidate classification, dry-run prerequisites, permission requirement matrix, safety gate alignment, rollback and kill-switch readiness, audit and observability readiness, rollout phase recommendations, and Sprint 101–110 block alignment.

This foundation does not activate runtime, dry-run runtime, services, config writes, permission changes, file runtime, network probes, action dispatch, command/tool execution, ORION handshake, memory writes, or git runtime.

## v0.102.0 Genesis — Safe Runtime Configuration Profile Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and configuration-blueprint-only Safe Runtime Configuration Profile Foundation. It prepares configuration profile types, runtime mode policies, service configuration boundaries, permission configuration boundaries, file system configuration boundaries, network configuration boundaries, dry-run configuration requirements, rollout configuration guards, and configuration audit visibility.

This foundation does not read, write, apply, or activate runtime configuration; start services; bind ports; change permissions; activate dry-run runtime; dispatch actions; execute tools or commands; connect ORION; write memory; or perform git runtime.

## v0.103.0 Genesis — Local Service Start Proposal Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and proposal-review-only Local Service Start Proposal Review Foundation.

This foundation prepares future local service start proposal review packets without starting services, binding ports, probing networks, changing permissions, dispatching actions, executing tools or commands, connecting ORION, writing memory, or performing git runtime.

## v0.104.0 Genesis — Dashboard API Contract Consolidation Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and contract-blueprint-only Dashboard API Contract Consolidation Foundation.

This foundation consolidates future dashboard API contracts without starting API/web servers, binding ports, handling requests, probing networks, dispatching actions, executing tools/commands, connecting ORION, writing memory, or performing git runtime.

## v0.105.0 Genesis — Permission Decision Runtime Dry-Run Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and dry-run-blueprint-only Permission Decision Runtime Dry-Run Foundation.

This foundation simulates future permission decisions without changing, granting, denying, activating, or revoking real permissions and without executing runtime actions.

## v0.106.0 Genesis — Runtime Action Execution Preview Packet Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and preview-packet-only Runtime Action Execution Preview Packet Foundation.

This foundation prepares future runtime action execution preview packets without dispatching actions, executing actions, executing tools or commands, changing permissions, mutating files, starting services, connecting ORION, writing memory, or performing git runtime.

## v0.107.0 Genesis — Local Runtime Execution Gate Dry-Run Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and dry-run-gate-blueprint-only Local Runtime Execution Gate Dry-Run Foundation.

This foundation prepares future local runtime execution gate checks without opening gates, executing actions, starting services, binding ports, probing networks, changing permissions, mutating files, connecting ORION, writing memory, or performing git runtime.

## v0.108.0 Genesis — Runtime Audit Event Packet Preview Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and audit-packet-preview-only Runtime Audit Event Packet Preview Foundation.

This foundation prepares future runtime audit event packet previews without writing audit logs, emitting events, streaming events, persisting records, writing files, dispatching actions, executing tools or commands, connecting ORION, writing memory, or performing git runtime.

## v0.109.0 Genesis — Runtime Safety Freeze Manual Approval Barrier Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and barrier-blueprint-only Runtime Safety Freeze Manual Approval Barrier Foundation.

This foundation prepares future runtime safety freeze and manual approval barrier packets without activating runtime freeze, granting approvals, releasing freeze, passing barriers, dispatching actions, executing tools or commands, mutating files, starting services, connecting ORION, writing memory, or performing git runtime.

## v0.110.0 Genesis — Review Stabilization 101-110 Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and checkpoint-review-only Review Stabilization 101-110 Foundation.

This checkpoint reviews Sprint 101 through Sprint 109 and closes the Genesis Runtime Readiness block without enabling runtime execution. Runtime upgrade remains deferred behind future manual approval and safety gates.

## v0.111.0 Genesis — Genesis Runtime Readiness Next Block Planning Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and next-block-planning-only Genesis Runtime Readiness Next Block Planning Foundation.

This foundation opens Sprint 111-120 planning after the Sprint 101-110 checkpoint. Runtime execution remains disabled and future runtime upgrades remain deferred behind manual approval and safety gates.

## v0.112.0 Genesis — Runtime Permission Flow Consolidation Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and permission-flow-consolidation-only Runtime Permission Flow Consolidation Foundation.

This foundation consolidates future runtime permission request, decision, approval, denial, cancellation, scope, high-risk escalation, audit reference, dashboard payload, and future runtime grant boundaries without changing permissions or enabling runtime execution.

## v0.113.0 Genesis — Audit Event Review Queue Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-queue-blueprint-only Audit Event Review Queue Foundation.

This foundation prepares future audit event intake, review queue states, triage rules, permission linkage, runtime boundary review, redaction visibility, dashboard review payloads, review outcomes, and future audit writer boundaries without writing or persisting audit events and without enabling runtime execution.

## v0.114.0 Genesis — Dashboard Runtime Readiness View Model Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and view-model-only Dashboard Runtime Readiness View Model Foundation.

This foundation prepares future runtime readiness dashboard surfaces for runtime readiness summary, permission state, audit review queue, safety boundary, ORION boundary, action preview, manual approval, v1 cutline, and Control Center payloads without starting dashboard/API/web/frontend/backend runtime and without enabling runtime execution.

## v0.115.0 Genesis — Safe Local Action Contract Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and contract-review-only Safe Local Action Contract Review Foundation.

This foundation reviews future safe local action contracts for local open, controlled create, controlled write preview, action preview packet, permission scope, side effect boundary, rollback/cancel, dashboard payload, and future action runtime boundaries without executing local actions and without enabling runtime execution.

## v0.116.0 Genesis — ORION Client Boundary Contract Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and boundary-contract-only ORION Client Boundary Contract Foundation.

This foundation prepares future ATLAS/ORION client identity, authority, sense permission, local action, emergency stop, dashboard status, runtime handshake, data-flow redaction, and future ORION runtime boundaries without starting ORION client runtime and without enabling runtime execution.

## v0.117.0 Genesis — Runtime Error and Rollback Preview Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and preview-only Runtime Error and Rollback Preview Foundation.

This foundation prepares future runtime error taxonomy, rollback preview packets, failure recovery state models, cancellation boundaries, partial execution guards, permission error reviews, audit error references, dashboard error rollback payloads, and future runtime recovery boundaries without executing rollback, recovery, cancellation, or runtime mutation.

## v0.118.0 Genesis — Manual Approval Decision Flow Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Manual Approval Decision Flow Review Foundation.

This foundation prepares future manual approval request schema, decision state, outcome catalog, denial/cancellation, escalation boundary, audit reference, dashboard payload, runtime gate, and future approval runtime boundaries without creating approval requests, persisting approval state, applying approval decisions, changing permission, or enabling runtime execution.

## v0.119.0 Genesis — v1 Runtime Readiness Cutline Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only v1 Runtime Readiness Cutline Review Foundation.

This foundation prepares v1 allowed capabilities, deferred capabilities, runtime gates, permission/audit requirements, ORION boundaries, dashboard visibility, release blockers, safe idle acceptance, and future v1 runtime activation boundaries without approving v1 runtime, opening release gates, enabling features, or enabling runtime execution.

## v0.120.0 Genesis — Review Stabilization 111-120 Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and checkpoint-review-only Review Stabilization 111-120 Foundation.

This foundation closes the Sprint 111-120 runtime readiness block by stabilizing completion review, capability registry review, runtime safety zero-state review, integration surface review, documentation/roadmap review, v1 blocker review, release cutline consistency, next block 121-130 boundary planning, and checkpoint 120 acceptance review without approving runtime, opening release gates, enabling v1 runtime, mutating capability states, or enabling runtime execution.

## v0.121.0 Genesis — Post-Checkpoint 120 Next Block Planning Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Post-Checkpoint 120 Next Block Planning Foundation.

This foundation opens the Sprint 121-130 runtime readiness continuation block by preparing checkpoint 120 output review, Sprint 121-130 scope definition, runtime readiness continuation, permission audit writer boundaries, dashboard control center boundaries, ORION dry handshake boundaries, safe local action allowlist boundaries, runtime activation blocker tracking, and future checkpoint 130 boundaries without approving runtime, opening release gates, starting dashboard runtime, enabling audit writer runtime, performing ORION handshakes, or enabling runtime execution.

## v0.122.0 Genesis — Runtime Permission Audit Writer Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Runtime Permission Audit Writer Boundary Review Foundation.

This foundation prepares future permission audit writer boundaries for schema, storage, redaction, visibility, permission decision links, dashboard audit payloads, failure handling, runtime gates, and future runtime requirements without starting audit writer runtime, writing audit events, persisting audit records, writing audit files, changing permissions, emitting dashboard events, performing ORION handshakes, or enabling runtime execution.

## v0.123.0 Genesis — Dashboard Control Center Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Dashboard Control Center Boundary Review Foundation.

This foundation prepares future dashboard/control-center boundaries for shell layout, status payloads, permission panel, audit panel, action proposal panel, ORION client panel, runtime gate panel, failure safe idle policy, and future dashboard runtime requirements without starting dashboard runtime, starting web/API/frontend/backend services, binding routes or ports, emitting dashboard events, changing permissions, performing ORION handshakes, or enabling runtime execution.

## v0.124.0 Genesis — ORION Dry Handshake Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only ORION Dry Handshake Boundary Review Foundation.

This foundation prepares future ATLAS/ORION dry handshake boundaries for client identity, capability packets, permission scope packets, status heartbeat, redaction, emergency stop, ATLAS/ORION authority, failure safe idle policy, and future ORION handshake runtime requirements without starting ORION client runtime, performing handshakes, sending packets, probing network, emitting dashboard events, changing permissions, or enabling runtime execution.

## v0.125.0 Genesis — Safe Local Action Allowlist Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Safe Local Action Allowlist Boundary Review Foundation.

This foundation prepares future safe local action allowlist boundaries for action catalog, action scope, permission requirements, risk levels, rollback references, audit/dashboard visibility, denied action policy, runtime gates, and future safe action runtime requirements without applying allowlists, creating permission requests, dispatching actions, executing actions, writing audit events, emitting dashboard events, reading/writing/modifying/deleting files, starting services, probing network, performing ORION handshakes, or enabling runtime execution.

## v0.126.0 Genesis — Runtime Grant Expiry Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Runtime Grant Expiry Boundary Review Foundation.

This foundation prepares future permission grant expiry boundaries for grant schema, grant lifetime policy, renewal, revocation, expired grant denial, dashboard visibility, audit links, failure safe idle behavior, and future grant expiry runtime requirements without creating grants, renewing grants, revoking grants, applying expiry state, mutating permissions, writing audit events, emitting dashboard events, dispatching actions, or enabling runtime execution.

## v0.127.0 Genesis — Runtime Recovery Drill Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Runtime Recovery Drill Boundary Review Foundation.

This foundation prepares future recovery drill boundaries for scenario catalog, recovery triggers, safe idle transitions, rollback previews, recovery audit/dashboard visibility, recovery permission boundaries, ORION recovery disconnect, failure escalation, and future recovery runtime requirements without starting recovery drills, executing recovery actions, applying rollback, restarting services, mutating permissions, writing audit events, emitting dashboard events, dispatching actions, or enabling runtime execution.

## v0.128.0 Genesis — Dashboard Runtime Readiness Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Dashboard Runtime Readiness Boundary Review Foundation.

This foundation prepares future dashboard runtime readiness boundaries for runtime entrypoint, route contracts, API contracts, websocket events, permission panel runtime, audit panel runtime, action panel runtime, failure safe idle behavior, and future dashboard runtime activation requirements without starting dashboard/web/API/frontend/backend servers, binding ports, opening browsers, registering routes, opening websockets, emitting dashboard events, changing permissions, dispatching actions, or enabling runtime execution.

## v0.129.0 Genesis — Runtime Activation Blocker Register Boundary Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Runtime Activation Blocker Register Boundary Review Foundation.

This foundation prepares future runtime activation blocker register boundaries for blocker schema, source classification, severity policy, activation gate links, resolution evidence, dashboard visibility, audit links, failure safe idle behavior, and future runtime activation unblock requirements without creating, updating, deleting, resolving, or unblocking blockers; opening runtime gates; activating runtime; writing audit events; emitting dashboard events; dispatching actions; or enabling runtime execution.

## v0.130.0 Genesis — Review Stabilization 121-130 Foundation

Status: completed

AURA now includes a review-only Sprint 121-130 stabilization checkpoint.

This checkpoint reviews Sprint 121-129 completion, capability registry consistency, permission boundaries, runtime zero counters, dashboard/ORION boundaries, action/permission/recovery/blocker boundaries, documentation and roadmap consistency, boot/CLI surfaces, deferred runtime items, and Sprint 131-140 readiness without activating runtime, opening runtime gates, mutating the capability registry, changing permissions, writing audit events, emitting dashboard events, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.131.0 Genesis — Post-Checkpoint 130 Next Block Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Post-Checkpoint 130 Next Block Foundation.

This foundation opens the Sprint 131-140 planning block toward Final Genesis by defining the next sprint sequence, Final Genesis acceptance direction, runtime activation path proposal review, local service boot plan review, Control Center runtime entry review, chat runtime minimal loop review, memory runtime write gate review, permission runtime grant gate review, audit runtime writer activation review, and Sprint 140 stabilization checkpoint without activating runtime, opening runtime gates, starting services, starting dashboard/chat/memory runtime, changing permissions, writing audit events, emitting dashboard events, dispatching actions, or enabling runtime execution.

## v0.132.0 Genesis — Final Genesis Acceptance Criteria Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Final Genesis Acceptance Criteria Foundation.

This foundation formalizes boot stability, local service, Control Center, local chat, memory, permission/audit, safe idle/recovery, optional ORION/voice/vision/avatar boundary, go/no-go, and future release candidate criteria without releasing Final Genesis, starting release candidates, booting services, starting dashboard/chat/memory runtime, creating permission grants, starting audit writers, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.133.0 Genesis — Runtime Activation Path Proposal Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Runtime Activation Path Proposal Review Foundation.

This foundation defines staged runtime activation proposal requirements, manual approval chains, activation blocker register links, permission contracts, audit contracts, dashboard visibility, safe idle rollback, emergency stop behavior, release candidate transition review, and activation denial/deferment rules without applying activation paths, enabling stages, opening runtime gates, starting runtime activation, starting release candidates, booting services, starting dashboard/chat/memory/permission/audit runtime, mutating blockers, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.134.0 Genesis — Local Service Boot Plan Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Local Service Boot Plan Review Foundation.

This foundation reviews manual start, manual stop, health monitoring, safe shutdown, config contracts, log visibility, localhost-only behavior, autostart guard, failure safe idle, and no-port-binding requirements for a future AURA local service on ATLAS without creating service units, enabling autostart, starting services, binding ports, starting API/web/dashboard/chat/memory/permission/audit runtime, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.135.0 Genesis — Control Center Runtime Entry Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Control Center Runtime Entry Review Foundation.

This foundation reviews Control Center entry routes, localhost boundary, read-only defaults, status panel entry, permission panel entry, audit panel entry, action proposal panel entry, safe idle/error panel entry, manual approval entry, and no-server-start requirements without creating routes, binding routes, starting Control Center, starting dashboard/API/web/frontend/backend servers, binding ports, starting panels, emitting dashboard events, creating permission grants, starting audit writers, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.136.0 Genesis — Chat Runtime Minimal Loop Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Chat Runtime Minimal Loop Review Foundation.

This foundation reviews chat input boundary, response boundary, session state, permission prompts, memory read/write gates, audit events, safe idle fallback, error recovery, manual approval runtime entry, and no-model-execution requirements without starting chat runtime, receiving or processing runtime messages, generating or sending responses, mutating sessions, reading or writing memory, creating permission prompts, starting audit writers, executing model requests or inference, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.137.0 Genesis — Memory Runtime Write Gate Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Memory Runtime Write Gate Review Foundation.

This foundation reviews memory write intent classification, manual approval, scope boundary, redaction, conflict resolution, audit events, rollback, safe idle failure, session links, and no-persistence requirements without reading memory, writing memory, mutating memory records, creating permission grants, starting audit writers, executing rollback/recovery, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.138.0 Genesis — Permission Runtime Grant Gate Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Permission Runtime Grant Gate Review Foundation.

This foundation reviews permission grant scope, manual approval, expiry, denial, audit links, dashboard visibility, revocation, risk classification, safe idle failure, and no-mutation requirements without receiving permission requests, creating/applying/updating/revoking grants, applying expiry, creating denials, starting audit writers, emitting dashboard events, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.139.0 Genesis — Audit Runtime Writer Activation Review Foundation

Status: completed

AURA now includes a planner-only, metadata-only, and review-only Audit Runtime Writer Activation Review Foundation.

This foundation reviews audit writer activation scope, event schema, append-only storage, redaction boundary, actor context, permission links, dashboard visibility, failure safe idle, retention/export, and no-write activation requirements without starting/stopping audit writers, receiving/writing audit events, appending logs, writing storage, dispatching actions, executing tools or commands, or enabling runtime execution.

## v0.140.0 Genesis — Review & Stabilization 131-140 Foundation

Status: completed

AURA now includes the Review & Stabilization 131-140 Foundation.

This checkpoint closes the 131-140 runtime planning block by validating scope coverage, runtime boundary integrity, capability registry consistency, system status surfaces, skill/plugin/CLI/shell integrations, documentation and roadmap state, safety counter zero state, git/boot verification, next block readiness, and no-runtime-activation boundaries.

The next block is Sprint 141-150: Local Service Runtime Foundation.

## v0.141.0 Genesis — Local Service Runtime Foundation

Status: completed

AURA now includes the Local Service Runtime Foundation.

This foundation prepares safe-idle ATLAS local service identity, localhost-only service boundary, service lifecycle state, configuration contract, health/status surface, permission gate link, audit link, service control command boundary, and no-start activation review.

No service process is started, no socket is opened, no port is bound, no API/web/dashboard/health endpoint is started, no systemd unit is created or enabled, no permission/audit/file/command/tool/action/ORION/git runtime is activated, and runtime execution features remain 0.

Next planned sprint: Sprint 250 — Backup and Restore Rehearsal

## Product Direction — Genesis to Post-Genesis

AURA's current path continues from v0.180.0-genesis toward v1.0.0-genesis.

Major roadmap blocks:

- Sprint 141-150: Local Service Runtime Foundation — completed
- Sprint 151-160: Control Center Runtime Foundation — completed
- Sprint 161-170: Local Chat Runtime Foundation — completed
- Sprint 171-180: Memory Runtime Foundation — completed
- Sprint 181-190: Local Interaction Runtime Activation
- Sprint 191-200: Voice Interaction Runtime
- Sprint 201-210: Vision and Screen Awareness Runtime
- Sprint 211-220: Permission, Audit, and Safe Local Actions
- Sprint 221-230: Unified Partner Runtime Integration
- Sprint 231-240: Genesis Final Integration and Release

Detailed canonical activation plan:

- `docs/AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md`
- `docs/AURA_ROADMAP_181_190_PLAN.md`

ORION client integration and avatar/presence runtime remain Post-Genesis directions and are not Genesis Final release blockers.

Post-Genesis direction:

- hardening and reliability
- creative partner expansion
- Game Companion foundation
- streaming/avatar identity
- advanced ORION runtime

Game Companion order:

1. Minecraft
2. osu
3. Beat Saber
4. Monster Hunter

Game Companion safety boundary:

- offline/private/single-player first
- no cheating
- no ranked automation
- no multiplayer farming
- no exploit workflow
- no silent input control
- all future game runtime must pass through ORION, permission, audit, vision, and Control Center gates

Canonical planning docs:

- docs/AURA_GENESIS_TO_POST_GENESIS_PRODUCT_PLAN.md
- docs/AURA_GAME_COMPANION_SAFETY_POLICY.md


## v0.142.0 Genesis — Local Service Health Endpoint Foundation

Sprint 143 completes the Local Service Health Endpoint Foundation foundation.

AURA now has planner-only metadata for:

- safe-idle boot scope
- boot entry state contracts
- safe-idle guard conditions
- boot failure fallback
- service no-autostart boundary
- read-only readiness probe planning
- Control Center idle visibility
- permission denial idle behavior
- audit failure idle behavior
- no-boot-activation review

Runtime remains disabled by design. No service, autostart, systemd, socket, port, health endpoint, readiness probe network call, permission mutation, audit writer, action/tool/command/file/memory/model/ORION/git runtime, or runtime execution feature is enabled.

Next planned sprint: Sprint 147.0 — Service Control Command Review Foundation.


## Sprint 143.0 Update

Sprint 143.0 adds Local Service Health Endpoint Foundation planning for the future ATLAS local service. It keeps the `/health` endpoint as a localhost-only, read-only, metadata-only contract and does not start an HTTP listener, open sockets, bind ports, run network probes, or enable runtime execution.


## Sprint 144.0 Update — Service Configuration and Port Registry Foundation

Status: completed

Sprint 144.0 adds Service Configuration and Port Registry Foundation planning for the future ATLAS local service. It keeps service configuration and port registry behavior as metadata-only planning and does not read/write runtime config, reserve ports, open sockets, bind ports, start HTTP listeners, start services, mutate environment state, write audit events, or enable runtime execution.

Next planned sprint: Sprint 147.0 — Service Control Command Review Foundation.


## Sprint 146.0 — Service Audit Link Foundation

Status: completed
Version: v0.170.0-genesis

Sprint 146 adds a planner-only, metadata-only, and foundation-only Service Audit Link Foundation for future service audit event references, audit link contracts, traceability chains, permission/audit pairing, Control Center audit visibility, redaction boundaries, failure safe-idle behavior, retention boundaries, error boundary, and no-audit-link-runtime-activation review.

Runtime remains disabled by design: no audit link record creation, no audit event reference creation, no audit event write, no audit log append, no runtime redaction, no trace chain write, no permission/audit link write, no service start, no port bind, no action/tool/command execution, and 0 runtime execution features.

Next planned sprint: Sprint 147.0 — Service Control Command Review Foundation.


## Sprint 147.0 — Service Control Command Review Foundation

Sprint 147 adds planner-only, metadata-only service control command review boundaries for future start/stop/restart/status service commands. Runtime remains disabled: no command execution, no systemd execution, no service start/stop/restart, no process status probe, no socket open, no port bind, and no runtime execution features.


## Sprint 148.0 — Service Recovery and Restart Policy Foundation

Status: completed. Adds planner-only service recovery and restart policy foundation with no recovery/restart runtime activation. Runtime execution features remain 0. Next: Sprint 149.0 — Service Security and Localhost Binding Review.


## Sprint 161 Direction — Local Chat Runtime Foundation

Sprint 161 begins the Local Chat Runtime block. The agreed Genesis Final path is
chat → memory → voice → vision → action. Sprint 161 remains a safe foundation
for session/message/chat-loop contracts and Sprint 162 CLI alpha readiness. It
does not enable model runtime, command execution, file mutation, desktop
control, voice, vision, or autonomous actions.


## Sprint 162 Direction — Local Chat CLI Session Alpha

Sprint 162 introduces the first safe thin runtime for AURA local chat: a one-turn
CLI alpha that creates a transient in-memory session packet and returns a safe
AURA persona response. It keeps message persistence, model runtime, memory
runtime, command execution, file mutation, desktop control, voice, vision,
network access, and autonomous actions disabled. Sprint 163 should add the local
chat message store.


## Sprint 163 Direction — Local Chat Message Store

Sprint 163 introduces a controlled local message store for AURA chat. It allows
one manual CLI chat turn to be appended to an AURA-owned JSONL store while model
runtime, memory runtime, command execution, arbitrary file mutation, desktop
action, voice, vision, network access, and autonomous actions remain disabled.
Sprint 164 should add the AURA Persona Response Layer.


## Sprint 167 — Chat Safety + Uncertainty Layer

Sprint 167 adds a deterministic local safety and uncertainty alpha layer before any future model request. It supports one-message safety/uncertainty review, capability honesty, and freshness-boundary replies while keeping model request dispatch, network, credential reads, memory writes, command execution, and arbitrary file mutation disabled.


## Sprint 168 — Chat History Viewer Contract

AURA v0.170.0-genesis adds a read-only Chat History Viewer Contract for the local chat message store. The viewer can inspect AURA-owned JSONL chat history metadata and recent turns from the controlled message store path, while keeping model requests, model responses, network requests, credential reads, permission grants, memory writes, audit writes, command execution, arbitrary file reads, arbitrary file writes, desktop action, and runtime execution disabled.


## Sprint 170 — Local Chat Runtime Stabilization

AURA v0.170.0-genesis reviews the local chat runtime alpha chain introduced across Sprints 161-168. It confirms the CLI session alpha, message store, persona response layer, model adapter boundary, permission gate, safety/uncertainty layer, and history viewer are integrated as a safe thin runtime path while full model runtime, network, credentials, memory runtime, command execution, arbitrary file access, desktop action, voice, and vision remain disabled.


## Sprint 171 — Memory Runtime Foundation

`v0.171.0-genesis` starts the Memory Runtime block with a preview-only memory foundation. AURA can create memory candidate previews and write-gate metadata, but real memory write remains disabled until explicit permission, review, privacy, and correction/deletion boundaries are implemented.


## Sprint 172 — Memory Write Permission Gate

`v0.172.0-genesis` adds a default-deny single-candidate memory permission gate. Candidate fingerprints and permission envelopes are previewed in process, but grants, memory writes, store mutation, audit writes, model/network activity, commands, and arbitrary file access remain disabled.


## Sprint 173 — Memory Extraction Dry Run

`v0.173.0-genesis` adds deterministic, no-model extraction of one reviewable memory candidate with trigger detection, normalization, classification, common sensitive-pattern screening, fingerprinting, and permission-gate handoff metadata. Candidate persistence, grants, memory writes/store mutation, network, credentials, audit writes, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 174 — Memory Importance and Pinning Policy

`v0.174.0-genesis` adds deterministic, explainable importance scoring, durability/temporary signal detection, retention recommendations, and future pin-eligibility previews. Candidate persistence, grants, memory writes/store mutation, pin/unpin actions, model/network activity, credentials, audit writes, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 175 — Memory Review Queue

`v0.175.0-genesis` adds an ephemeral, deterministic manual-review queue preview for memory candidates with priority, privacy, permission, and future-decision metadata. Queue persistence, decision application, grants, memory writes/store mutation, pin/unpin actions, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 176 — Memory Correction and Deletion Boundary

`v0.176.0-genesis` adds exact-target correction and tombstone-first deletion previews, with separate future purge permission. Store reads, lookups, mutations, grants, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 177 — Chat-to-Memory Handoff Contract

`v0.177.0-genesis` adds an explicit-user-turn, preview-only chat-to-memory handoff with exact source binding, privacy precheck, review-queue routing, and default-deny permission state. Chat-store/history reads, automatic handoff, queue persistence, grants, memory writes/store mutation, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 178 — Memory Privacy and Redaction Layer

`v0.178.0-genesis` adds deterministic redaction previews and strict secret-block boundaries for the memory pipeline. Original and redacted candidates remain unpersisted; review decisions, grants, memory writes/store mutation, model/network activity, commands, arbitrary file access, and runtime execution remain disabled.


## Sprint 179 — Memory Runtime Integration Review

`v0.179.0-genesis` validates the Sprint 171-178 memory chain as a single read-only integration surface. All component readiness, privacy, review, permission, and correction/deletion boundaries pass while release, persistence, mutation, model, network, command, audit, arbitrary-file, and runtime execution gates remain closed.


## Sprint 180 — Memory Runtime Stabilization

`v0.180.0-genesis` closes the Sprint 171-180 Memory Runtime block. Nine memory components pass stabilization with zero dependency gaps and runtime violations while privacy, review, permission, correction/deletion, release, mutation, model, network, command, arbitrary-file, voice, and runtime execution gates remain closed. The next block is Sprint 181-190 Local Interaction Runtime Activation. Voice moves to Sprint 191-200 after the dashboard and chat runtime are operational and stabilized.

## Checkpoint v0.181.0-genesis — Local Web Runtime Alpha

Sprint 181 activates AURA's first deliberately narrow live web runtime. It is
explicitly confirmed, foreground-only, bound only to `127.0.0.1:8765`,
defaults to `safe_idle`, and exposes only a static read-only Control Center
shell plus `/health` and `/api/status`.

Sprint 181 contributes one runtime execution feature. Full runtime readiness,
chat, model calls, memory writes, permission mutation, audit persistence,
commands, tools, actions, arbitrary file access, desktop control, voice,
vision, public/LAN binding, background service, and autonomous behavior remain
disabled.

Next: Sprint 182 — Service Lifecycle Runtime.

## Checkpoint v0.182.0-genesis — Service Lifecycle Runtime

Sprint 182 adds deterministic foreground lifecycle control around the Sprint
181 localhost listener. The runtime now has explicit `stopped`, `starting`,
`running`, `stopping`, and `failed` states; single-listener ownership;
port-conflict fail-closed handling; startup rollback; clean programmatic stop;
and clean `SIGINT` or `SIGTERM` shutdown.

The runtime execution feature count remains `1`. Background daemon operation,
systemd, automatic startup, persistent PID/state, remote lifecycle mutation,
chat, models, memory writes, permission mutation, commands, tools, actions,
files, desktop control, voice, vision, public/LAN exposure, and autonomy remain
disabled.

Next: Sprint 183 — Health and Status API Runtime.

## Checkpoint v0.183.0-genesis — Health and Status API Runtime

Sprint 183 adds nine transparent, read-only health and status payload routes to
the existing localhost listener. Identity, boot prerequisites, plugin module
availability, capability summary, live lifecycle state and uptime, memory
availability, safety boundaries, and errors or degraded states are now visible
without starting plugins or mutating files.

GET and HEAD are permitted. Mutation methods are blocked, non-local Host
headers are rejected, CORS remains disabled, and defensive no-store/browser
headers are emitted. The runtime execution feature count remains `1`.

Background service, systemd, automatic startup, persistence, remote lifecycle
mutation, chat, models, permission mutation, commands, tools, actions, files,
desktop control, voice, vision, public/LAN exposure, and autonomy remain
disabled.

Next: Sprint 184 — Control Center Backend Runtime.

## Checkpoint v0.184.0-genesis — Control Center Backend Runtime

Sprint 184 connects the earlier Control Center foundations to nine read-only
backend routes and eight stable panel view models. The overview and service
panels reflect the live lifecycle instance, while capability, plugin,
permission, audit, memory, and readiness information remain transparent and
side-effect free.

The same foreground localhost listener now serves nine status routes and nine
Control Center backend routes. GET and HEAD are allowed; mutation methods are
blocked, non-local Host headers are rejected, CORS remains disabled, and
defensive no-store/browser headers are retained. Runtime execution feature
accounting remains `1`.

The Control Center web shell, frontend assets, browser launch, service and
plugin controls, permission decisions, audit writes, memory writes, chat,
models, commands, tools, actions, background service, public/LAN exposure, and
autonomy remain disabled.

Next: Sprint 185 — Control Center Web Shell.

## Checkpoint v0.185.0-genesis — Control Center Web Shell

Sprint 185 delivers AURA's first usable browser dashboard. Three local static
assets are served through the same explicitly confirmed foreground localhost
listener, while the nine status routes and nine Control Center backend routes
remain available.

The shell renders overview, service, capability, plugin, permission, audit,
memory, and readiness panels. It includes responsive layouts, keyboard and
reduced-motion accessibility, safe-idle and degraded-state indicators,
read-only refresh, and local capability filtering.

No external frontend dependencies, inline scripts, inline styles, browser
auto-launch, mutation controls, service/plugin actions, permission decisions,
audit writes, memory writes, chat, model dispatch, commands, tools, actions,
background service, public/LAN binding, or autonomous behavior are enabled.

Runtime execution feature accounting remains `1`.

Next: Sprint 186 — Browser Chat Session Runtime.

## Checkpoint v0.186.0-genesis — Browser Chat Session Runtime

Sprint 186 activates bounded browser-to-local-session interaction. AURA can
create local chat sessions, validate and persist messages, reload history,
return an honest no-model placeholder, replay duplicate client submissions
idempotently, reject stale new-message revisions, and clear a session only
after an exact confirmation phrase.

The `/chat` page and six chat route contracts reuse the existing foreground
localhost listener. Private session files are atomic, mode `0600`,
integrity-checked, bounded, and excluded from Git.

Local model inference, network fallback, AURA long-term memory writes, tools,
commands, actions, arbitrary files, desktop control, permission mutation,
audit writes, background service, public/LAN binding, browser auto-launch,
and autonomy remain disabled.

Runtime execution feature accounting remains `1`.

Next: Sprint 187 — Local Model Bridge Activation.

## Checkpoint v0.187.0-genesis — Local Model Bridge Runtime

Sprint 187 activates a permission-gated localhost-only text model bridge.

Checkpoint state:

- 118 total capabilities;
- 116 online capabilities;
- 10 permission-gated capabilities;
- 2 runtime execution features;
- 7 browser chat route contracts;
- 2 local model route contracts;
- 30 total local interaction route contracts;
- Ollama and OpenAI-compatible contracts ready;
- provider disabled by default;
- no model downloads or internet fallback;
- no tool/function calling, commands, actions, or AURA memory writes.

Next: Sprint 188 — Interactive Control Center Chat.

## Checkpoint v0.188.0-genesis — Interactive Control Center Chat

Sprint 188 activates the interactive localhost chat product surface.

Checkpoint state:

- 119 total capabilities;
- 117 online capabilities;
- 11 permission-gated capabilities;
- 3 runtime execution features;
- 7 browser chat route contracts;
- 2 local model route contracts;
- 30 total local interaction route contracts;
- interactive web self-test: 166/166;
- interactive runtime self-test: 119/119;
- provider disabled by default;
- save-only mode selected by default;
- explicit provider and model confirmation;
- no model downloads, internet fallback, tools, commands, actions, browser
  storage, or AURA long-term memory writes.

Next: Sprint 189 — Permission, Audit, and Recovery Visibility.

## Checkpoint v0.189.0-genesis — Permission, Audit, and Recovery Visibility

Sprint 189 activates the read-only safety visibility product surface.

Checkpoint state:

- 120 total capabilities;
- 118 online capabilities;
- 12 permission-gated capabilities;
- 4 runtime execution features;
- 5 visible permission requirement items;
- 9 visible audit-event contracts;
- 8 visible recovery cases;
- 10 redacted field declarations;
- 4 GET/HEAD visibility APIs;
- 3 visibility browser assets;
- 37 total local interaction route contracts;
- visibility core self-test: 127/127;
- visibility web self-test: 143/143;
- mutation methods blocked;
- provider values redacted;
- audit writer and automatic recovery disabled;
- canonical data unchanged.

Next: Sprint 190 — Review and Stabilization 181-190.


## Checkpoint v0.190.0-genesis — Local Interaction Runtime Stabilization

Sprint 190 closes the Sprint 181-190 Local Interaction Runtime Activation
block.

Checkpoint state:

- 121 total capabilities;
- 119 online capabilities;
- 12 permission-gated capabilities;
- 11 review-only capabilities;
- 4 runtime execution features;
- 9 local interaction components checked;
- 9 components ready;
- 10 dependency self-tests passed;
- 1,175 total assertion coverage;
- 0 failed assertions;
- 0 stabilization gaps;
- 0 runtime violations;
- localhost-only and explicit foreground-start boundaries preserved;
- clean shutdown and port-conflict fail-closed behavior preserved;
- no permission bypass;
- no arbitrary execution;
- no new runtime authority added.

The Local Interaction Runtime Activation block is complete. AURA can be opened
through the localhost Control Center and used through bounded interactive chat
with persistent sessions, an explicitly confirmed local-model path, and
visible safety/recovery state.

Next: Sprint 191 — Voice Runtime Activation Foundation.

## Checkpoint v0.191.0-genesis — Voice Runtime Activation Foundation

Sprint 191 starts the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation ready;
- planning ready;
- runtime ready remains false;
- safe idle default true;
- explicit push-to-talk required;
- explicit listen required;
- always-listening disabled;
- hidden capture disabled;
- background wake word disabled;
- silent cloud fallback disabled;
- direct voice-to-action execution disabled;
- microphone capture inactive;
- speaker playback inactive;
- STT runtime inactive;
- TTS runtime inactive;
- audio file writes inactive;
- command execution inactive;
- existing `microphone_listen` permission action reused;
- existing `speaker_speak` permission action reused;
- chat/session reuse required;
- 19 activation assertions;
- 0 failed activation assertions.

Sprint 191 does not install dependencies, access audio devices, capture
microphone input, play speaker output, run STT, run TTS, write audio files,
fallback to cloud providers, execute voice actions, execute commands, mutate
files, control the desktop, start background services, bind publicly, or add
autonomy.

Next: Sprint 192 — Push-to-Talk and Explicit Listen State.

## Checkpoint v0.192.0-genesis — Push-to-Talk and Explicit Listen State

Sprint 192 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation ready;
- default listen state is `idle`;
- current listen state is `idle`;
- nine allowed listen states declared;
- explicit push-to-talk required;
- explicit listen required;
- explicit stop required;
- microphone permission required before any future live listening;
- existing `microphone_listen` permission action reused;
- microphone capture inactive;
- audio buffer inactive;
- STT runtime inactive;
- listen loop inactive;
- background listener inactive;
- wake word inactive;
- state persistence runtime disabled;
- state mutation runtime disabled;
- audio device access disabled;
- direct voice-to-action execution disabled;
- command execution inactive;
- 36 activation/listen-state assertions;
- 0 failed activation/listen-state assertions.

Sprint 192 does not install dependencies, access audio devices, capture
microphone input, buffer audio, run STT, run TTS, play speaker output, start a
listen loop, enable wake words, listen in the background, persist listen state,
mutate listen state through runtime controls, execute commands, mutate files,
control the desktop, start background services, bind publicly, or add autonomy.

Next: Sprint 193 — Local Microphone Capture Boundary.

## Checkpoint v0.193.0-genesis — Local Microphone Capture Boundary

Sprint 193 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary ready;
- microphone capture runtime not ready;
- microphone capture inactive;
- microphone permission required before any future capture;
- explicit listen state required before any future capture;
- required future capture state is `listening_explicit`;
- push-to-talk required before any future capture;
- existing `microphone_listen` permission action reused;
- audio device access disabled;
- audio device discovery inactive;
- device enumeration not performed;
- sounddevice runtime not imported;
- recording disabled;
- recording inactive;
- audio buffer inactive;
- audio file write inactive;
- audio persistence disabled;
- audio transmission disabled;
- STT runtime inactive;
- transcription inactive;
- listen loop inactive;
- background listener inactive;
- wake word inactive;
- hidden capture disabled;
- always-listening disabled;
- silent cloud fallback disabled;
- direct voice-to-action execution disabled;
- command execution inactive;
- speaker playback inactive;
- 64 activation/listen-state/microphone-boundary assertions;
- 0 failed activation/listen-state/microphone-boundary assertions.

Sprint 193 does not install dependencies, discover audio devices, access audio
devices, capture microphone input, record audio, buffer audio, write audio
files, persist audio, transmit audio, run STT, transcribe speech, run TTS, play
speaker output, start a listen loop, enable wake words, listen in the
background, hide capture, fallback to cloud providers, execute voice actions,
execute commands, mutate files, control the desktop, start background services,
bind publicly, or add autonomy.

Next: Sprint 194 — Speech-to-Text Adapter Runtime.

## Checkpoint v0.194.0-genesis — Speech-to-Text Adapter Runtime

Sprint 194 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary remains ready;
- STT adapter contract ready;
- STT adapter runtime not ready;
- default adapter candidate is `faster-whisper`;
- three STT adapter candidates declared;
- local-first STT required;
- offline-first STT required;
- audio-file input boundary ready for future dry runs;
- provided audio file required before any future audio-file STT dry run;
- audio-file transcription runtime not ready;
- audio file read inactive;
- audio file write inactive;
- microphone capture not required for the adapter contract;
- live microphone transcription inactive;
- microphone capture inactive;
- audio device access disabled;
- audio device discovery inactive;
- recording inactive;
- audio buffer inactive;
- audio persistence disabled;
- audio transmission disabled;
- STT runtime inactive;
- transcription inactive;
- transcript persistence disabled;
- transcript-to-chat handoff disabled;
- transcript-to-action disabled;
- command execution inactive;
- model download not required;
- model download not performed;
- dependency install not performed;
- cloud STT fallback disabled;
- silent cloud fallback disabled;
- remote STT provider disabled;
- microphone permission required before any future transcription;
- existing `microphone_listen` permission action reused;
- 98 activation/listen-state/microphone-boundary/STT-adapter assertions;
- 0 failed activation/listen-state/microphone-boundary/STT-adapter assertions.

Sprint 194 does not install dependencies, download models, read audio files,
write audio files, transcribe audio files, run live microphone transcription,
capture microphone input, record audio, buffer audio, persist audio, transmit
audio, access audio devices, discover audio devices, run STT, create
transcripts, persist transcripts, hand transcripts to chat, turn transcripts
into actions, fallback to cloud STT, enable remote STT providers, run TTS, play
speaker output, start a listen loop, enable wake words, listen in the
background, hide capture, execute voice actions, execute commands, mutate
files, control the desktop, start background services, bind publicly, or add
autonomy.

Next: Sprint 195 — Voice Intent and Chat Integration.

## Checkpoint v0.195.0-genesis — Voice Intent and Chat Integration

Sprint 195 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary remains ready;
- STT adapter contract remains ready;
- voice intent and chat integration contract ready;
- voice intent runtime not ready;
- voice intent layer contract ready;
- transcript source is `contract_only`;
- transcript input boundary ready;
- provided transcript required before any future dry run;
- dummy transcript allowed for contract boundary;
- live transcript input inactive;
- transcript normalization contract ready;
- transcript normalization runtime inactive;
- intent classification contract ready;
- intent classification runtime inactive;
- intent confidence runtime inactive;
- clarification gate contract ready;
- action intent gate contract ready;
- voice response plan contract ready;
- transcript-to-chat handoff contract ready;
- transcript-to-chat handoff inactive;
- chat session reuse required;
- chat session write inactive;
- chat model request inactive;
- chat response generation inactive;
- permission required before any future chat handoff;
- human confirmation required for future action-like voice intent;
- transcript persistence disabled;
- memory write inactive;
- direct voice-to-action disabled;
- tool execution inactive;
- command execution inactive;
- file mutation inactive;
- desktop action inactive;
- network action inactive;
- git action inactive;
- STT runtime inactive;
- transcription inactive;
- live microphone transcription inactive;
- TTS runtime inactive;
- speaker playback inactive;
- cloud STT fallback disabled;
- silent cloud fallback disabled;
- 138 activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat assertions;
- 0 failed activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat assertions.

Sprint 195 does not process live transcripts, automatically hand transcripts to
chat, write chat sessions, request models, generate responses, persist
transcripts, write memory, execute voice actions, execute tools, execute
commands, mutate files, control the desktop, perform network actions, perform
git actions, run STT, transcribe speech, run live microphone transcription, run
TTS, play speaker output, fallback to cloud providers, start a listen loop,
enable wake words, listen in the background, hide capture, start background
services, bind publicly, or add autonomy.

Next: Sprint 196 — Text-to-Speech Adapter Runtime.

## Checkpoint v0.196.0-genesis — Text-to-Speech Adapter Runtime

Sprint 196 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary remains ready;
- STT adapter contract remains ready;
- voice intent and chat integration contract remains ready;
- TTS adapter contract ready;
- TTS adapter runtime not ready;
- default adapter candidate is `piper`;
- three TTS adapter candidates declared;
- local-first TTS required;
- offline-first TTS required;
- voice response input boundary ready;
- provided text required before any future TTS dry run;
- dummy text allowed for contract boundary;
- TTS text normalization contract ready;
- TTS synthesis runtime not ready;
- TTS synthesis inactive;
- audio output file boundary ready;
- audio output file write inactive;
- audio output file read inactive;
- audio file persistence disabled;
- speaker playback permission required;
- existing `speaker_speak` permission action reused;
- speaker playback runtime not ready;
- speaker playback inactive;
- playback device access disabled;
- playback device discovery inactive;
- playback disabled;
- automatic speak-after-chat disabled;
- voice response playback inactive;
- chat-response-to-TTS handoff contract ready;
- chat-response-to-TTS handoff inactive;
- model download not required;
- model download not performed;
- dependency install not performed;
- cloud TTS fallback disabled;
- silent cloud fallback disabled;
- remote TTS provider disabled;
- STT runtime inactive;
- transcription inactive;
- microphone capture inactive;
- audio device access disabled;
- audio buffer inactive;
- memory write inactive;
- direct voice-to-action disabled;
- tool execution inactive;
- command execution inactive;
- file mutation inactive;
- desktop action inactive;
- network action inactive;
- git action inactive;
- 184 activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter assertions;
- 0 failed activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter assertions.

Sprint 196 does not synthesize speech, write audio output files, read audio
output files, persist audio, play speaker output, access playback devices,
discover playback devices, automatically speak after chat, play voice
responses, execute chat-response-to-TTS handoff, download models, install
dependencies, fallback to cloud TTS, enable remote TTS providers, run STT,
transcribe speech, capture microphone input, write memory, execute voice
actions, execute tools, execute commands, mutate files, control the desktop,
perform network actions, perform git actions, start background services, bind
publicly, or add autonomy.

Next: Sprint 197 — Voice Permission and Audit Runtime.

## Checkpoint v0.197.0-genesis — Voice Permission and Audit Runtime

Sprint 197 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary remains ready;
- STT adapter contract remains ready;
- voice intent and chat integration contract remains ready;
- TTS adapter contract remains ready;
- voice permission and audit contract ready;
- voice permission and audit runtime not ready;
- permission boundary ready;
- existing `microphone_listen` permission action linked;
- existing `speaker_speak` permission action linked;
- microphone permission required and confirmation-gated;
- speaker permission required and confirmation-gated;
- transcript chat handoff permission required;
- chat response TTS permission required;
- voice action permission required;
- permission required before microphone capture, STT, TTS, speaker playback,
  and chat handoff;
- human confirmation required for future voice action intent;
- audit event contract ready;
- audit event schema ready;
- six voice audit event types declared;
- audit redaction boundary ready;
- audit local-only requirement ready;
- audit append-only boundary ready;
- audit write runtime not ready and inactive;
- audit event persistence disabled;
- audit log append inactive;
- audit storage write inactive;
- audit dashboard event emit inactive;
- audit redaction runtime inactive;
- audit permission link runtime inactive;
- review queue contract ready but runtime inactive;
- recovery visibility contract ready but action runtime inactive;
- permission decision, grant, revoke, persistence, and mutation runtimes inactive;
- microphone capture inactive;
- STT runtime inactive;
- transcription inactive;
- live microphone transcription inactive;
- TTS runtime inactive;
- TTS synthesis inactive;
- speaker playback inactive;
- audio device access disabled;
- playback device access disabled;
- transcript-to-chat handoff inactive;
- chat-response-to-TTS handoff inactive;
- memory write inactive;
- direct voice-to-action disabled;
- tool execution inactive;
- command execution inactive;
- file mutation inactive;
- desktop action inactive;
- network action inactive;
- git action inactive;
- cloud STT fallback disabled;
- cloud TTS fallback disabled;
- silent cloud fallback disabled;
- 247 activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter/permission-audit assertions;
- 0 failed activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter/permission-audit assertions.

Sprint 197 does not grant permissions, revoke permissions, mutate permission
state, persist permissions, write audit events, persist audit events, append
audit logs, write audit storage, emit audit dashboard events, run audit
redaction, create audit permission links, activate review queues, execute
recovery actions, capture microphone input, run STT, transcribe speech, run
TTS, synthesize speech, play speaker output, access audio/playback devices,
execute transcript/chat/TTS handoffs, write memory, execute voice actions,
execute tools, execute commands, mutate files, control the desktop, perform
network actions, perform git actions, fallback to cloud providers, start
background services, bind publicly, or add autonomy.

Next: Sprint 198 — Control Center Voice Controls.

## Checkpoint v0.198.0-genesis — Control Center Voice Controls

Sprint 198 continues the Sprint 191-200 Voice Interaction Runtime block.

Checkpoint state:

- voice activation foundation remains ready;
- listen-state foundation remains ready;
- microphone boundary remains ready;
- STT adapter contract remains ready;
- voice intent and chat integration contract remains ready;
- TTS adapter contract remains ready;
- voice permission and audit contract remains ready;
- Control Center voice controls contract ready;
- Control Center voice controls runtime not ready;
- voice controls visible in Control Center contract;
- voice controls read-only;
- voice controls disabled by default;
- route contract ready;
- panel contract ready;
- panel id is `voice_controls`;
- route contract is `/api/control-center/voice-controls`;
- web panel anchor is `#voice-controls`;
- listen-state display boundary ready;
- default listen state is `idle`;
- current listen state is `idle`;
- nine allowed listen states declared;
- push-to-talk display ready and required;
- microphone permission display boundary ready;
- speaker permission display boundary ready;
- existing `microphone_listen` permission action displayed;
- existing `speaker_speak` permission action displayed;
- microphone and speaker confirmation required;
- STT status display boundary ready;
- TTS status display boundary ready;
- STT and TTS adapter contracts ready;
- STT and TTS adapter runtimes not ready;
- voice intent, permission/audit, and audit event displays ready;
- runtime safety badges ready;
- ten disabled voice controls declared;
- UI mutation disabled;
- UI microphone capture trigger inactive;
- UI STT trigger inactive;
- UI TTS trigger inactive;
- UI speaker playback trigger inactive;
- UI permission grant, revoke, and mutation triggers inactive;
- UI audit write trigger inactive;
- UI voice action trigger inactive;
- UI command, tool, and file mutation triggers inactive;
- API GET contract ready;
- API POST mutation route disabled;
- API localhost-only and read-only payload boundaries ready;
- frontend read-only binding ready;
- frontend mutation controls absent;
- frontend action, permission, audio device, and audit write buttons disabled;
- microphone capture inactive;
- STT runtime inactive;
- transcription inactive;
- live microphone transcription inactive;
- TTS runtime inactive;
- TTS synthesis inactive;
- speaker playback inactive;
- audio device access disabled;
- playback device access disabled;
- transcript/chat/TTS handoffs inactive;
- permission decision, grant, and mutation runtimes inactive;
- audit write runtime inactive;
- audit event persistence disabled;
- memory write inactive;
- direct voice-to-action disabled;
- tool execution inactive;
- command execution inactive;
- file mutation inactive;
- desktop action inactive;
- network action inactive;
- git action inactive;
- cloud STT fallback disabled;
- cloud TTS fallback disabled;
- silent cloud fallback disabled;
- 342 activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter/permission-audit/control-center-voice assertions;
- 0 failed activation/listen-state/microphone-boundary/STT-adapter/voice-intent-chat/TTS-adapter/permission-audit/control-center-voice assertions.

Sprint 198 does not activate Control Center voice controls, execute
push-to-talk, start listening, stop listening, capture microphone input, trigger
STT, trigger TTS, play speaker output, grant permissions, revoke permissions,
mutate permission state, write audit events, execute voice actions, execute
commands, execute tools, mutate files, control the desktop, perform network
actions, perform git actions, write memory, execute handoffs, fallback to cloud
providers, expose API POST mutation routes, enable frontend action buttons,
start background services, bind publicly, or add autonomy.

Next: Sprint 199 — Voice Runtime Integration Review.

## Checkpoint v0.199.0-genesis — Voice Runtime Integration Review

Sprint 199 continues the Sprint 191-200 Voice Interaction Runtime block with a
read-only integration review across the Sprint 191-198 voice contracts.

The checkpoint confirms the ordered voice chain from activation through Control
Center voice controls:

- activation foundation
- explicit listen state
- microphone capture boundary
- speech-to-text adapter contract
- voice intent and chat integration contract
- text-to-speech adapter contract
- voice permission and audit contract
- Control Center voice controls contract

The Sprint 199 integration review reports eight reviewed contracts, eight
integration matrix items, all prior contracts ready, all prior runtimes blocked,
a safety blocker matrix ready, and forty-seven safety blockers.

Sprint 199 keeps runtime activation blocked. It does not activate microphone
capture, audio device access, STT, transcription, TTS, speaker playback,
permission grant/revoke/mutation, audit write, handoffs, memory write,
tool/command execution, file/desktop/network/git actions, cloud fallback, or
voice actions.

Validation passed with 434 voice assertions and zero failed assertions.

Next: Sprint 200 — Voice Runtime Stabilization.

## Checkpoint v0.200.0-genesis — Voice Runtime Stabilization

Sprint 200 completes the Sprint 191-200 Voice Interaction Runtime block as a
contract-only stabilization checkpoint.

The checkpoint confirms that the voice block is stabilized with nine stabilized
contracts, ten stabilization components, forty-seven safety blockers, zero
stabilization gaps, and all safety blockers inactive.

Sprint 200 keeps runtime activation blocked and release gates closed. It does
not activate microphone capture, audio device access, STT, transcription, TTS,
speaker playback, permission grant/revoke/mutation, audit writes, handoffs,
memory writes, tool/command execution, file/desktop/network/git actions, cloud
fallback, or voice actions.

The next block begins at Sprint 201 with Vision Runtime Activation Foundation.

## Checkpoint v0.201.0-genesis — Vision Runtime Activation Foundation

Sprint 201 starts the Sprint 201-210 Vision and Screen Awareness Runtime block as
a contract-only activation foundation.

The checkpoint confirms that the vision runtime block now has an activation
foundation with explicit visual input requirements, explicit user confirmation,
screen and camera permission boundaries, candidate mapping, thirty-three safety
blockers, and all safety blockers inactive.

Sprint 201 keeps runtime activation blocked and release gates closed. It does
not activate screen access, camera access, screenshot capture, camera frame
capture, image file reads, OCR, image analysis, object detection, continuous or
background watching, biometric identification, face or identity recognition,
face emotion inference, visual-context-to-action bypass, visual action execution,
tool/command execution, file/desktop/network/git actions, memory writes, cloud
vision fallback, external upload, or any visual runtime execution.

The next sprint is Sprint 202 — Explicit Screenshot Capture.

## Checkpoint v0.202.0-genesis — Explicit Screenshot Capture

Sprint 202 adds explicit screenshot capture contract gates to the Sprint 201-210
Vision and Screen Awareness Runtime block.

The checkpoint defines screenshot capture as future request-only behavior guarded
by explicit user request, screen permission, user confirmation, single-capture
scope, and redaction before any future context handoff.

Sprint 202 keeps runtime activation blocked and release gates closed. It does
not capture the screen, write screenshot files, read image files, persist
screenshot metadata, run OCR, run image analysis, run object detection, run
vision model runtime, hand off screen context, execute visual actions, execute
tools or commands, mutate files, control the desktop, write memory, perform
network or git actions, use cloud vision fallback, externally upload visual data,
or bypass action gates through visual context.

The next sprint is Sprint 203 — Screen Context Adapter.

## Checkpoint v0.203.0-genesis — Screen Context Adapter

Sprint 203 adds screen context adapter contract gates to the Sprint 201-210
Vision and Screen Awareness Runtime block.

The checkpoint defines screen context as provided metadata/placeholder context
only. It prepares input, metadata, packet, and summary contracts with uncertainty
and redaction requirements while keeping runtime execution disabled.

Sprint 203 keeps runtime activation blocked and release gates closed. It does
not capture the screen, read screenshots or image files, create runtime context
packets, create summaries, run redaction runtime, run OCR, run image analysis,
run object detection, run vision model runtime, hand off context to chat,
execute visual actions, execute tools or commands, mutate files, control the
desktop, write memory, perform network or git actions, use cloud vision fallback,
externally upload visual data, or bypass action gates through visual context.

The next sprint is Sprint 204 — Local Vision Model Adapter.

## Checkpoint v0.204.0-genesis — Local Vision Model Adapter

Sprint 204 adds local vision model adapter contract gates to the Sprint 201-210
Vision and Screen Awareness Runtime block.

The checkpoint defines the adapter as local/offline-first and contract-only. It
prepares provider, candidate, request, response, capability, and visual prompt
schemas while requiring permission and redaction boundaries before any future
model request.

Sprint 204 keeps runtime activation blocked and release gates closed. It does
not download models, install dependencies, probe providers, send model requests,
run inference, read screenshots or image files, capture the screen, run OCR, use
cloud vision fallback, externally upload visual data, hand off model output to
chat, execute visual actions, execute tools or commands, mutate files, control
the desktop, write memory, perform network or git actions, or bypass action
gates through visual context.

The next sprint is Sprint 205 — Vision Permission and Redaction.

## Checkpoint v0.205.0-genesis — Vision Permission and Redaction

Sprint 205 adds vision permission and redaction contract gates to the Sprint
201-210 Vision and Screen Awareness Runtime block.

The checkpoint prepares explicit visual permission, confirmation, scope, audit,
and redaction schemas before any future screenshot, screen context, local model,
chat handoff, or visual action flow. It also defines redaction requirements for
sensitive regions, window titles, URLs, clipboard exclusion, secret tokens,
personal identifiers, and visible text.

Sprint 205 keeps runtime activation blocked and release gates closed. It does
not mutate permissions, run redaction, create redacted context, write audit
events, capture screenshots, read image files, run OCR, send model requests, run
inference, hand off context/chat, execute visual actions, execute tools or
commands, mutate files, control the desktop, write memory, perform network or git
actions, use cloud vision fallback, externally upload visual data, or bypass
action gates through visual context.

The next sprint is Sprint 206 — Workspace Visual Understanding.

## Checkpoint v0.206.0-genesis — Workspace Visual Understanding

Sprint 206 adds workspace visual understanding contract gates to the Sprint
201-210 Vision and Screen Awareness Runtime block.

The checkpoint prepares schemas and contracts for understanding already-provided,
already-redacted workspace visual context. It defines workspace visual summary,
layout, active window, visible region, visual element, attention target,
workspace risk, limitation, task context, risk summary, and uncertainty summary
boundaries.

Sprint 206 keeps runtime activation blocked and release gates closed. It does
not create workspace summaries, create workspace layouts, create visual element
lists, assess workspace risk at runtime, capture screenshots, read image files,
run OCR, send model requests, run inference, hand off context/chat, execute
visual actions, execute tools or commands, mutate files, control the desktop,
write memory, perform network or git actions, use cloud vision fallback,
externally upload visual data, or bypass action gates through visual context.

The next sprint is Sprint 207 — Vision-to-Chat Context Handoff.

## Checkpoint v0.207.0-genesis — Vision-to-Chat Context Handoff

Sprint 207 adds vision-to-chat context handoff contract gates to the Sprint
201-210 Vision and Screen Awareness Runtime block.

The checkpoint prepares schemas and contracts for chat-safe visual context
packets, chat-safe visual summaries, chat-safe workspace summaries, chat context
handoff packets, source attribution, limitation notes, uncertainty notes, risk
notices, handoff previews, visible disclosure, and chat render boundaries.

Sprint 207 keeps runtime activation blocked and release gates closed. It does
not inject visual context into chat, write chat sessions, create chat context
packets, create chat-safe visual summaries, create handoff previews, request
chat models, generate responses, write memory, capture screenshots, read image
files, run OCR, send model requests, run inference, execute visual actions,
execute tools or commands, mutate files, control the desktop, perform network or
git actions, use cloud vision fallback, externally upload visual data, or bypass
action gates through visual context.

The next sprint is Sprint 208 — Control Center Vision Panel.

## Checkpoint v0.208.0-genesis — Control Center Vision Panel

Sprint 208 adds Control Center Vision Panel contract gates to the Sprint
201-210 Vision and Screen Awareness Runtime block.

The checkpoint prepares read-only and display-only panel schemas for vision
status, safety, dependencies, permissions, redaction, handoff, limitations, risk,
status badges, safety blockers, dependency baselines, capability boundaries,
release gate display, next boundary display, panel routes, navigation items,
view models, data aggregators, no-mutation boundaries, and no-capture
boundaries.

Sprint 208 keeps runtime activation blocked and release gates closed. It does
not render panels, create routes, create API endpoints, generate static assets,
fetch data, auto-refresh, open websockets, mutate permissions, write audit
events, trigger screenshot/camera/model/chat handoff controls, write memory,
create chat context packets, write chat sessions, request chat models, generate
responses, capture screenshots, read image files, run OCR, send model requests,
run inference, execute visual actions, execute tools or commands, mutate files,
control the desktop, perform network or git actions, use cloud vision fallback,
externally upload visual data, or bypass action gates through visual context.

The next sprint is Sprint 209 — Vision Runtime Integration Review.

## Checkpoint v0.209.0-genesis — Vision Runtime Integration Review

Sprint 209 adds Vision Runtime Integration Review contract gates to the Sprint
201-210 Vision and Screen Awareness Runtime block.

The checkpoint reviews the Sprint 201-208 contract chain: activation foundation,
explicit screenshot capture, screen context adapter, local vision model adapter,
permission/redaction, workspace visual understanding, vision-to-chat handoff, and
Control Center Vision Panel visibility.

Sprint 209 keeps runtime activation blocked and release gates closed. It does
not install dependencies, download models, capture screenshots, read image files,
run OCR, request models, inject chat context, render panels, create routes,
create API endpoints, fetch data, mutate permissions, write audit events, write
memory, execute visual actions, execute tools or commands, mutate files, control
the desktop, perform network or git actions, use cloud vision fallback,
externally upload visual data, or bypass action gates through visual context.

The next sprint is Sprint 210 — Vision Runtime Stabilization.

## Checkpoint v0.210.0-genesis — Vision Runtime Stabilization

Sprint 210 closes the Sprint 201-210 Vision and Screen Awareness Runtime block
as contract-only stable.

The checkpoint stabilizes the Sprint 201-209 contract chain: activation
foundation, explicit screenshot capture, screen context adapter, local vision
model adapter, permission/redaction, workspace visual understanding,
vision-to-chat handoff, Control Center Vision Panel visibility, and Vision
Runtime Integration Review.

Sprint 210 keeps runtime activation blocked and release gates closed. It does
not install dependencies, download models, capture screenshots, read image files,
run OCR, request models, run inference, inject chat context, render panels,
create routes, create API endpoints, fetch data, mutate permissions, write audit
events, write memory, execute visual actions, execute tools or commands, mutate
files, control the desktop, perform network or git actions, use cloud vision
fallback, externally upload visual data, or bypass action gates through visual
context.

The next sprint is Sprint 211 — Active Permission Runtime.

## Checkpoint v0.211.0-genesis — Active Permission Runtime

Sprint 211 starts the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with a contract-only Active Permission Runtime.

This checkpoint establishes the default-deny runtime permission boundary and
prepares request, scope, decision, grant, denial, expiry, state snapshot, review
queue, user-visible reason, safety matrix, runtime status, next lifecycle, and
audit-link schemas.

Runtime remains disabled. Sprint 211 does not create permission requests,
create grants, mutate permission state, persist permissions, write audit events,
create action proposals, preview actions, enqueue actions, execute actions,
execute commands/tools, mutate files, control desktop, launch applications,
perform network/git actions, write memory, install dependencies, download models,
use cloud fallback, upload externally, or perform autonomous actions.

The next sprint is Sprint 212 — Grant, Denial, and Expiry Lifecycle.

## Checkpoint v0.212.0-genesis — Grant, Denial, and Expiry Lifecycle

Sprint 212 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with a contract-only Grant, Denial, and Expiry Lifecycle.

This checkpoint prepares lifecycle schemas and safety visibility for future
grant requests, grant scopes, grant decisions, grant packets, grant expiry,
grant revocation, denials, denial reasons, expiry checks, expiry events,
lifecycle state snapshots, lifecycle audit links, lifecycle review queues, and
runtime audit writer handoff.

Runtime remains disabled. Sprint 212 does not create grants, denials, expiry
events, mutate permission state, persist permissions, write audit events, create
action proposals, preview actions, enqueue actions, execute actions, execute
commands/tools, mutate files, control desktop, launch applications, perform
network/git actions, write memory, install dependencies, download models, use
cloud fallback, upload externally, or perform autonomous actions.

The next sprint is Sprint 213 — Runtime Audit Writer.

## Checkpoint v0.213.0-genesis — Runtime Audit Writer

Sprint 213 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with a contract-only Runtime Audit Writer.

This checkpoint prepares audit writer schemas and safety visibility for future
audit event packets, append-only audit logs, persistence gates, correlation
packets, actor context, permission lifecycle links, grant/denial/expiry links,
redaction boundaries, retention policy, review queue packets, Control Center
visibility, and action proposal/preview handoff.

Runtime remains disabled. Sprint 213 does not create audit packets, write audit
events, append audit logs, persist audit data, write audit storage, mutate
permission state, persist permissions, create grants, create action proposals,
preview actions, enqueue actions, execute actions, execute commands/tools,
mutate files, control desktop, launch applications, perform network/git actions,
write memory, install dependencies, download models, use cloud fallback, upload
externally, or perform autonomous actions.

The next sprint is Sprint 214 — Action Proposal and Preview Runtime.

## Checkpoint v0.214.0-genesis — Action Proposal and Preview Runtime

Sprint 214 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with a contract-only Action Proposal and Preview Runtime.

This checkpoint prepares action proposal and preview schemas, including action
intent, action proposal, action preview, risk summary, scope, permission
requirement, audit correlation, user-visible preview, approval handoff, denial
handoff, review queue, execution blocker, safety matrix, and safe local open
handoff.

Runtime remains disabled. Sprint 214 does not create proposals, previews,
approval handoffs, review queue items, queue actions, execute actions, execute
commands/tools, mutate files, control desktop, launch applications, mutate
permissions, create grants, write audit events, perform network/git actions,
write memory, install dependencies, download models, use cloud fallback, upload
externally, or perform autonomous actions.

The next sprint is Sprint 215 — Safe Local Open Actions.

## Checkpoint v0.215.0-genesis — Safe Local Open Actions

Sprint 215 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with contract-only Safe Local Open Actions.

This checkpoint prepares safe local open action schemas, including approved
folder, approved file, approved project location, and approved dashboard open
previews. It requires preview-before-open, explicit approval, permission, audit
correlation, allowlist, canonical path, safe local scope, and single-open action
boundaries.

Runtime remains disabled. Sprint 215 does not create open requests, open
previews, approval handoffs, review queue items, path access, file reads,
directory listings, folder/file/project/dashboard opens, shell/OS/browser/file-
manager dispatches, execute actions, execute commands/tools, mutate files,
control desktop, launch applications, mutate permissions, create grants, write
audit events, perform network/git actions, write memory, use cloud fallback,
upload externally, or perform autonomous actions.

The next sprint is Sprint 216 — Allowlisted Application Launch.

## Checkpoint v0.216.0-genesis — Allowlisted Application Launch

Sprint 216 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with contract-only Allowlisted Application Launch.

This checkpoint prepares application launch schemas, including allowlisted
launch request, launch target, launch preview, launch allowlist, permission
requirement, audit correlation, user-visible preview, approval handoff, denial
handoff, execution blocker, review queue, and safety matrix boundaries. It
requires preview-before-launch, explicit approval, permission, audit
correlation, allowlist, application identity, safe arguments, safe environment,
and single-application launch boundaries.

Runtime remains disabled. Sprint 216 does not create launch requests, previews,
approval handoffs, review queue items, allowlist resolutions, executable
resolutions, argument/environment resolutions, process spawns, application
launches, app launches, desktop actions, commands/tools, file mutations,
permission mutations, grants, audit events, network/git actions, memory writes,
cloud fallback, external uploads, or autonomous actions.

The next sprint is Sprint 217 — Controlled Folder and Simple File Creation.

## Checkpoint v0.217.0-genesis — Controlled Folder and Simple File Creation

Sprint 217 extends the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with contract-only Controlled Folder and Simple File Creation.

This checkpoint prepares controlled folder and simple file creation schemas,
including creation request, creation target, creation preview, path policy,
allowlist, permission requirement, audit correlation, user-visible preview,
approval handoff, denial handoff, execution blocker, review queue, folder
creation request/target/preview, simple file creation request/target/content
preview, and safety matrix boundaries. It requires preview-before-create,
explicit approval, permission, audit correlation, allowlist, canonical path,
parent path, safe content, and single-creation action boundaries.

Runtime remains disabled. Sprint 217 does not create folders, write files,
resolve paths, access paths, list directories, read files, perform mkdir,
mutate the filesystem, dispatch commands/tools, launch apps, mutate
permissions, create grants, write audit events, perform network/git actions,
write memory, use cloud fallback, upload externally, or perform autonomous
actions.

The next sprint is Sprint 218 — Control Center Approval Workflow.

## Checkpoint v0.218.0-genesis — Control Center Approval Workflow

Sprint 218 adds contract-only Control Center Approval Workflow visibility for
future explicit approve/deny decisions. It prepares approval request, context,
preview, decision, grant candidate, denial, expiry, audit correlation,
user-visible summary, review queue, route, safety matrix, and next
rollback/emergency-stop/recovery boundaries.

Runtime remains disabled: no approval requests are created, no decisions are
applied, no grants or denials are created, no queues are mutated, no permissions
are mutated, no audit events are written, no actions are dispatched, and no
local actions execute.

The next sprint is Sprint 219 — Rollback, Emergency Stop, and Recovery.

## Checkpoint v0.219.0-genesis — Rollback, Emergency Stop, and Recovery

Sprint 219 adds contract-only recovery safety visibility for future rollback,
emergency stop, safety freeze, safe-idle transition, and manual recovery flows.
It prepares rollback request/preview/plan, emergency stop request/preview,
safe-idle destination, safety freeze, recovery plan/state/drill, audit
correlation, user-visible summary, review queue, safety matrix, and next
stabilization boundaries.

Runtime remains disabled: no rollback executes, no emergency stop is applied, no
safety freeze or safe-idle transition is activated, no recovery actions are
dispatched, no permissions are mutated, no audit events are written, and no
local actions execute.

The next sprint is Sprint 220 — Permission and Action Runtime Stabilization.

## Checkpoint v0.220.0-genesis — Permission and Action Runtime Stabilization

Sprint 220 closes the Sprint 211-220 Permission, Audit, and Safe Local Actions
block with contract-only stabilization. It verifies the full 9-contract chain,
runtime zero counters, safety blockers, CLI visibility, release-gate closure,
docs/version readiness, and next-block handoff to Unified Partner Runtime
Integration.

Runtime remains disabled: no runtime gates open, no release gates open, no
permissions are mutated, no grants are created, no audit events are written, no
actions are dispatched, no commands or tools execute, no files are mutated, no
applications launch, no rollback or recovery actions execute, and no autonomous
actions run.

The next sprint is Sprint 221 — Unified Partner Runtime Integration.

## Checkpoint v0.221.0-genesis — Unified Session Runtime

Sprint 221 begins the Sprint 221-230 Unified Partner Runtime Integration
block.

The checkpoint adds a contract-only unified-session facade. The browser
chat session runtime remains canonical owner of session identity,
revision, integrity, persistence, and bounded mutation behavior.

The checkpoint passes 51 assertions with zero failures. Planner and
alpha status are deterministic. The legacy planning layer is represented
only through its static safety boundary, so the broad dependency graph
and project journal are not accessed.

Runtime authority remains disabled. No session mutation, memory write,
permission mutation, audit write, action execution, command or tool
execution, arbitrary file mutation, application launch, desktop
control, background service, public binding, or autonomous action is
enabled.

Next: Sprint 222 — Workspace and Project Context Runtime.

## Checkpoint v0.222.0-genesis — Workspace and Project Context Runtime

Sprint 222 completes the second step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- bounded workspace and project context contract available
- Sprint 221 unified session contract preserved
- browser chat session runtime remains canonical session owner
- legacy workspace manager remains a non-runtime static boundary
- top-level workspace inspection only
- approved context sources inspected by existence only
- journal and memory data remain unread
- context persistence remains disabled
- execution and all mutation authorities remain disabled
- 52 contract assertions pass with zero failures
- Capability Registry remains unchanged

Next: Sprint 223 — Chat-to-Memory Runtime Handoff.

## Checkpoint v0.223.0-genesis — Chat-to-Memory Runtime Handoff

Sprint 223 completes the third step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- chat-to-memory partner-runtime contract available
- Sprint 222 workspace/project context contract preserved at 52 assertions
- canonical browser chat session ownership preserved
- existing handoff, privacy, review, and permission contracts remain owners of their domains
- explicit user memory intent required
- direct user-turn-only handoff boundary preserved
- privacy and manual review required
- default-deny, one-shot, expiring write permission required
- chat and memory runtime data remain unread
- handoff, review, permission, audit, and memory persistence remain disabled
- runtime execution and autonomous behavior remain disabled
- Sprint 223 validates 65 assertions with zero failures
- Capability Registry remains unchanged

Next: Sprint 224 — Voice, Vision, and Chat Context Fusion.

## Checkpoint v0.224.0-genesis — Voice, Vision, and Chat Context Fusion

Sprint 224 completes the fourth step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- voice owner preserved with 507 assertions and zero failures
- vision owner preserved with 330 assertions and zero failures
- Sprint 223 chat/session chain preserved with 65 assertions and zero failures
- canonical browser chat session ownership preserved
- context-fusion planner validates 84 assertions with zero failures
- fusion remains contract-only and preview-only
- no live fusion packet is created
- audio, transcript, image, screenshot, chat, and session payloads remain unread
- microphone, speaker, screen, screenshot, and camera operations remain inactive
- context inference and model requests remain inactive
- persistence, permission mutation, audit writes, and execution remain inactive
- runtime activation, background services, release gates, and autonomy remain disabled
- Capability Registry remains unchanged

Next: Sprint 225 — Personality Consistency Runtime.

## Checkpoint v0.225.0-genesis — Personality Consistency Runtime

Sprint 225 completes the fifth step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- canonical identity source remains `aura/personality/identity.yaml`
- identity version advances to `0.225.0-genesis`
- Sprint 164 persona contract remains the persona-style owner
- Sprint 224 fusion contract remains the upstream context owner with 84
  assertions and zero failures
- `aura_browser_chat_session_runtime` remains canonical session owner
- Expression Language remains a secondary metadata reference and is not
  instantiated by the Sprint 225 contract
- required traits, operating modes, style items, consistency dimensions, and
  interface targets are validated
- personality profile remains deterministic, metadata-only, and payload-free
- persona response generation and persona-turn persistence are not invoked
- chat, session, audio, image, journal, memory, and runtime payloads remain
  unread
- inference, model requests, memory access, permission mutation, audit writes,
  network actions, commands, tools, files, background services, release gates,
  and autonomy remain inactive
- CLI and shell expose identical read-only packets
- Sprint 225 validates 96 assertions with zero failures
- Capability Registry remains unchanged

Next: Sprint 226 — Multi-Interface State Synchronization.

## Checkpoint v0.226.0-genesis — Multi-Interface State Synchronization

Sprint 226 completes the sixth step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- canonical identity advances to `0.226.0-genesis`
- Sprint 225 remains the upstream personality owner with 96 assertions and zero failures
- Sprint 224 remains stable with 84 assertions and zero failures
- `aura_browser_chat_session_runtime` remains canonical session owner
- browser session inspection remains limited to `contract_snapshot()`
- browser session payload reads remain zero
- Chat Bridge remains the interface-state schema owner
- Local Interaction Stabilization remains a secondary read-only baseline
- Control Center remains `static_reference_only`
- the Control Center runtime snapshot is not invoked
- seven interface targets are declared
- six canonical synchronization fields are declared
- six payload-adjacent fields are excluded
- deterministic metadata state-vector templates are declared
- no live state vector is created
- no interface state is persisted
- no synchronization event is dispatched
- no live propagation is performed
- memory access, permission mutation, audit writes, network actions, commands,
  tools, process launch, background services, runtime activation, release gates,
  and autonomy remain inactive
- CLI and shell expose identical read-only packets
- Sprint 226 validates 128 assertions with zero failures
- Capability Registry remains unchanged

Next: Sprint 227 — Service Persistence and Launcher.

## Checkpoint v0.227.0-genesis — Service Persistence and Launcher

Sprint 227 completes the seventh step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- canonical identity advances to `0.227.0-genesis`
- Sprint 226 remains stable with 128 assertions and zero failures
- Sprint 227 validates 208 assertions with zero failures
- `AuraServiceLifecycleRuntimeManager` is the canonical lifecycle owner
- lifecycle access remains `static_contract_metadata_only`
- no lifecycle instance is created and no lifecycle runtime method is invoked
- launcher foundation remains a secondary read-only metadata owner
- runtime-service foundation remains a secondary read-only blueprint reference
- local-service foundation remains a secondary read-only safety baseline
- service-state schema contains 15 metadata fields
- eight runtime-payload fields remain explicitly excluded
- four persistence artifacts are declared but not read, written, or created
- recovery remains manual-only with safe-idle fallback and operator review
- CLI and shell expose identical read-only packets
- no PID/state/log/systemd file is written
- no systemctl, service, listener, socket, thread, subprocess, launcher, browser auto-launch, auto-start, runtime activation, release gate, or autonomous recovery is enabled
- Capability Registry remains unchanged

Next: Sprint 228 — Safe Auto-Start Evaluation.

## Checkpoint v0.228.0-genesis — Safe Auto-Start Evaluation

Sprint 228 completes the eighth step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- canonical identity advances to `0.228.0-genesis`
- Sprint 227 remains stable with 208 assertions and zero failures
- Sprint 228 validates 358 assertions with zero failures
- `AuraServiceLifecycleRuntimeManager` remains the canonical lifecycle owner
- lifecycle access remains `static_contract_metadata_only`
- no lifecycle instance is created and no lifecycle runtime method is invoked
- nine foundation metadata owners remain bounded and read-only
- ten auto-start safety domains are evaluated
- 90 owner methods are audited
- 33 zero-argument metadata methods are deterministic
- 57 target-plan methods remain uninvoked
- CLI and shell expose identical read-only packets
- no systemd unit is written or installed
- no `systemctl`, service, listener, socket, thread, subprocess, launcher,
  browser auto-launch, auto-start, automatic restart, autonomous recovery,
  runtime activation, or release-gate authority is enabled
- Capability Registry remains unchanged

Next: Sprint 229 — Genesis Acceptance Rehearsal.

## Checkpoint v0.229.0-genesis — Genesis Acceptance Rehearsal

Sprint 229 completes the ninth step of the Sprint 221-230 Unified Partner
Runtime Integration block.

Canonical checkpoint properties:

- canonical identity advances to `0.229.0-genesis`
- Sprint 228 remains stable with 358 assertions and zero failures
- Sprint 229 validates 486 assertions with zero failures
- eight partner-runtime rehearsal owners remain deterministic and read-only
- 1,042 upstream owner assertions pass with zero failures
- 30 read-only owner method packets remain deterministic
- eight sequential sprint handoff boundaries are verified
- nine Genesis rehearsal phases are represented
- all 27 required acceptance results pass
- ten safe auto-start safety domains remain non-activating
- all 17 negative runtime-effect results remain false
- all 21 zero-effect counters remain zero
- CLI, shell, and direct packets remain identical
- Genesis release approval remains false
- no systemctl, service, listener, socket, thread, subprocess, launcher,
  browser auto-launch, auto-start, runtime activation, release gate, or
  autonomous recovery is enabled
- Capability Registry remains unchanged

Next: Sprint 230 — Unified Partner Runtime Stabilization.

## Checkpoint v0.230.0-genesis — Unified Partner Runtime Stabilization

Sprint 230 closes the Sprint 221-230 Unified Partner Runtime Integration block
as contract-complete and stabilized.

Checkpoint summary:

- canonical identity advances to `0.230.0-genesis`;
- nine partner-runtime owners are present;
- upstream assertion total is 1,528 with zero failures;
- deterministic method packet count is 35;
- handoff chain count is 9;
- stabilization domain count is 10;
- all 30 required stabilization results pass;
- all 18 prohibited runtime and release outcomes remain false;
- all 21 runtime-effect counters remain zero;
- Sprint 230 direct, CLI, and shell packets are equivalent;
- block complete is true;
- block stabilized is true;
- block release-ready is false;
- Genesis release approved is false;
- runtime activation allowed is false;
- release gate open is false;
- Capability Registry remains unchanged.

Next: Sprint 231 — Genesis Final Integration and Release.

## Checkpoint v0.231.0-genesis — Genesis Final Integration and Release

Sprint 231 begins the Sprint 231–240 Genesis Final Integration and Release
block.

Checkpoint state:

- canonical identity advances to `0.231.0-genesis`;
- Sprint 231 passes `576/576` contract assertions;
- ten integration owners provide `2056` assertions with zero failures;
- `40` deterministic method packets and ten handoff stages are preserved;
- CLI, shell, and direct route parity is verified;
- final-integration foundation readiness is true;
- current-block completion, stabilization, and release readiness are false;
- release-candidate assembly and readiness are false;
- Genesis release approval, runtime activation, and release-gate opening are
  false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `backup_restore_rehearsal`

Next: Sprint 232 — Genesis Release Candidate Assembly.

## Checkpoint v0.232.0-genesis — Genesis Release Candidate Assembly

Sprint 232 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.232.0-genesis`;
- Sprint 232 passes `630/630` assertions;
- eleven integration owners provide `2632` assertions with zero failures;
- `45` deterministic method packets and eleven handoff stages are preserved;
- CLI, shell, and direct route parity is verified;
- release-candidate manifest, artifact, and documentation inventories are
  reviewable;
- release-candidate assembly foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, and verification remain false;
- Genesis release approval, runtime activation, and release-gate opening
  remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_verification`

Next: Sprint 233 — Genesis Release Candidate Verification.

## Checkpoint v0.233.0-genesis — Genesis Release Candidate Verification

Sprint 233 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.233.0-genesis`;
- Sprint 233 passes `690/690` assertions;
- twelve integration owners provide `3262` assertions with zero failures;
- `50` deterministic method packets and twelve handoff stages are preserved;
- CLI, shell, and direct route parity is verified;
- verification evidence, artifact, and documentation inventories are
  reviewable;
- release-candidate verification foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, and verification
  passed remain false;
- Genesis release approval, runtime activation, and release-gate opening
  remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_readiness`

Next: Sprint 234 — Genesis Release Candidate Readiness.

## Checkpoint v0.234.0-genesis — Genesis Release Candidate Readiness

Sprint 234 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.234.0-genesis`;
- Sprint 234 passes `756/756` assertions;
- thirteen integration owners provide `3952` assertions with zero failures;
- `55` deterministic method packets and thirteen handoff stages are
  preserved;
- CLI, shell, and direct route parity is verified;
- readiness evidence, artifact, and documentation inventories are
  reviewable;
- release-candidate readiness foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  and readiness passed remain false;
- approval readiness, Genesis release approval, runtime activation, and
  release-gate opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_approval`

Next: Sprint 235 — Genesis Release Candidate Approval.

## Checkpoint v0.235.0-genesis — Genesis Release Candidate Approval

Sprint 235 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.235.0-genesis`;
- Sprint 235 passes `828/828` assertions;
- fourteen integration owners provide `4708` assertions with zero failures;
- `60` deterministic method packets and fourteen handoff stages are
  preserved;
- CLI, shell, and direct route parity is verified;
- approval evidence, artifact, and documentation inventories are reviewable;
- release-candidate approval foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  readiness passed, approval readiness, and approval passed remain false;
- Genesis release approval, release authorization readiness, runtime
  activation, and release-gate opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_release_authorization`

Next: Sprint 236 — Genesis Release Candidate Release Authorization.

## Checkpoint v0.236.0-genesis — Genesis Release Candidate Release Authorization

Sprint 236 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.236.0-genesis`;
- Sprint 236 passes `906/906` assertions;
- fifteen integration owners provide `5536` assertions with zero failures;
- `65` deterministic method packets and fifteen handoff stages are preserved;
- CLI, shell, and direct route parity is verified;
- authorization evidence, artifact, and documentation inventories are
  reviewable;
- release-authorization foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  readiness passed, approval readiness, approval passed, authorization
  readiness, and authorization passed remain false;
- Genesis release approval, release-gate review readiness, runtime
  activation, and release-gate opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_release_gate_review`

Next: Sprint 237 — Genesis Release Candidate Release Gate Review.

## Checkpoint v0.237.0-genesis — Genesis Release Candidate Release Gate Review

Sprint 237 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.237.0-genesis`;
- Sprint 237 passes `988/988` assertions;
- sixteen integration owners provide `6442` assertions with zero failures;
- `70` deterministic method packets and sixteen handoff stages are preserved;
- CLI, shell, and direct route parity is verified;
- release-gate review evidence, artifact, and documentation inventories are
  reviewable;
- release-gate review foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  readiness passed, approval readiness, approval passed, authorization
  readiness, authorization passed, review readiness, and review passed
  remain false;
- release-gate approval readiness, runtime activation, and release-gate
  opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_release_gate_approval`

Next: Sprint 238 — Genesis Release Candidate Release Gate Approval.

## Checkpoint v0.238.0-genesis — Genesis Release Candidate Release Gate Approval

Sprint 238 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.238.0-genesis`;
- Sprint 238 passes `1074/1074` assertions;
- seventeen integration owners provide `7430` assertions with zero failures;
- `75` deterministic method packets and seventeen handoff stages are
  preserved;
- CLI, shell, and direct route parity is verified;
- release-gate approval evidence, artifact, and documentation inventories
  are reviewable;
- release-gate approval foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  readiness passed, approval readiness, approval passed, authorization
  readiness, authorization passed, release-gate review readiness,
  release-gate review passed, release-gate approval readiness, and
  release-gate approval passed remain false;
- release-decision readiness, release-decision passed, runtime activation,
  and release-gate opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_release_candidate_release_decision`

Next: Sprint 239 — Genesis Release Candidate Release Decision.

## Checkpoint v0.239.0-genesis — Genesis Release Candidate Release Decision

Sprint 239 continues the Sprint 231–240 Genesis Final Integration and
Release block.

Checkpoint state:

- canonical identity advances to `0.239.0-genesis`;
- Sprint 239 passes `1164/1164` assertions;
- eighteen integration owners provide `8504` assertions with zero failures;
- `80` deterministic method packets and eighteen handoff stages are
  preserved;
- CLI, shell, and direct route parity is verified;
- release-decision evidence, artifact, and documentation inventories are
  reviewable;
- release-decision foundation readiness is true;
- block completion, stabilization, and release readiness remain false;
- release-candidate assembly, readiness, verification, verification passed,
  readiness passed, approval readiness, approval passed, authorization
  readiness, authorization passed, release-gate review readiness,
  release-gate review passed, release-gate approval readiness, and
  release-gate approval passed remain false;
- release-decision readiness, release-decision passed, and release-decision
  applied remain false;
- Genesis Final release readiness, completion, and publication remain false;
- version-promotion readiness and version promotion remain false;
- runtime activation and release-gate opening remain false;
- Capability Registry remains unchanged;
- no runtime or operating-system side effect is introduced.

Next boundary: `genesis_final_release`

Next: Sprint 240 — Genesis Final Release.

## Checkpoint v1.0.0-genesis — Genesis Final Release

Sprint 240 closes the Sprint 231–240 Genesis Final Integration and Release
block.

Checkpoint state:

- canonical identity: `1.0.0-genesis`;
- Sprint 240 assertions: `1258/1258`;
- local Sprint 240 assertions: `94/94`;
- integration owners: `19`;
- owner assertion total: `9668`;
- owner failures: `0`;
- deterministic method packets: `85`;
- handoff stages: `19`;
- operator review completed: `true`;
- acceptance validation passed: `true`;
- block complete: `true`;
- block stabilized: `true`;
- block release-ready: `true`;
- release decision applied: `true`;
- Genesis Final release passed: `true`;
- canonical version promoted: `true`;
- Git tag created: `false`;
- GitHub Release published: `false`;
- release artifact published: `false`;
- runtime activated: `false`;
- operational release gate open: `false`;
- Capability Registry unchanged;
- safe-idle, permission, audit, recovery, emergency-stop, operator-control,
  and rollback boundaries preserved.

Next boundary: `genesis_stabilization`

Next: Sprint 241 — Genesis Stabilization.

## Checkpoint v1.0.1-genesis — Genesis Stabilization Runtime Hardening

Sprint 241 begins the Sprint 241-250 Genesis Stabilization & Runtime
Hardening block.

Accepted results:

- exact nine-command ownership for the codebase compatibility handler;
- unrelated commands rejected before manager construction;
- CLI dispatch initialization pollution reduced from `1126` log lines to `0`;
- immutable Genesis Final status projection with deep validation preserved;
- Sprint 241 regressions: `11/11`;
- Sprint 240 and Sprint 241 status E2E latency: approximately `0.19` seconds;
- capability registry: `122` total, `120` online;
- runtime activation, release gates, systemd, automatic service control,
  ORION control, and autonomous execution remain disabled.

Current boundary: `permission_expiry_recovery_review`

Next boundary: `service_lifecycle_determinism`

Next: Sprint 242 — Service Lifecycle Determinism.

## Canonical Product Milestones — v2.0.0 through v4.0.0

The concrete product milestone plan in
`docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md` is canonical for Sprint 241 onward.

Earlier abstract labels remain useful as historical product concepts, but they
do not override the sprint blocks and acceptance targets below.

| Sprint block | Product boundary | Block milestone |
|---|---|---|
| 241-250 | Genesis Stabilization & Runtime Hardening | `v1.1.0` |
| 251-260 | Active Local Runtime & Model Service Integration | `v1.2.0` |
| 261-270 | Chat, STT, TTS, Vision & OCR Activation | `v1.3.0` |
| 271-280 | ORION Safe Action Bridge | `v1.4.0` |
| 281-290 | Game Companion Coach, Observer & Recording | `v1.5.0` |
| 291-300 | Dashboard, Avatar, Personality, Base Plugin Manager & v2 Acceptance | `v2.0.0` |
| 301-310 | Plugin Architecture & Lifecycle | `v2.1.0` |
| 311-320 | Plugin Permissions, Isolation & Dependencies | `v2.2.0` |
| 321-330 | Workspace & Project Assistance | `v2.3.0` |
| 331-340 | Documents, Files, Tasks & Knowledge Work | `v2.4.0` |
| 341-350 | Supervised Coding Assistance & Workflow Automation | `v2.5.0` |
| 351-360 | Work Assistance Integration & v3 Acceptance | `v3.0.0` |
| 361-370 | Avatar Runtime & State Synchronization | `v3.1.0` |
| 371-380 | Voice, Face, Body Expression & VRM Integration | `v3.2.0` |
| 381-390 | OBS Creator Runtime & Viewer Interaction | `v3.3.0` |
| 391-400 | Gaming/Livestream Safety & Performance | `v3.4.0` |
| 401-410 | Game Companion Live Fusion & Creator Rehearsal | `v3.5.0` |
| 411-420 | Virtual Creator Stabilization & v4 Acceptance | `v4.0.0` |

### v2.0.0 product definition

AURA v2 is a usable local multimodal partner with an active but bounded
runtime, model-backed chat, STT, TTS, vision and OCR, allowlisted ORION
actions, Game Companion Coach/Observer/Recording, a cleaner dashboard, a
basic synchronized 3D avatar, improved personality, and a base plugin manager.

### v3.0.0 product definition

AURA v3 is a plugin and work-assistance platform with controlled plugin
lifecycle management, permission isolation, workspace/project assistance,
document/file/task workflows, and supervised coding or workflow automation.

### v4.0.0 product definition

AURA v4 is a synchronized virtual creator and gaming companion with a mature
avatar runtime, OBS and viewer integration, gaming/livestream performance
guardrails, and safe live fusion between voice, avatar, coaching, observation,
recording, and creator workflows.

Canonical version is now `1.0.1-genesis` after Sprint 241 explicitly promoted the first Genesis Stabilization patch release.

Next boundary: `service_lifecycle_determinism`

Next: Sprint 242 — Service Lifecycle Determinism.

## Checkpoint v1.0.2-genesis — Service Lifecycle Determinism

Sprint 242 completed deterministic lifecycle request hardening.

Acceptance:

- Sprint 242 lifecycle determinism: 25/25;
- Sprint 182 lifecycle baseline preserved: 41/41;
- startup-period stop requests fail closed;
- repeated stopped/stopping requests are deterministic;
- lifecycle self-test output is pure JSON;
- normal runtime access logging remains enabled;
- PID persistence, state persistence, systemd, remote lifecycle control,
  HTTP lifecycle mutation, background daemon execution, and autostart
  remain disabled.

Next: Sprint 243 — Configuration Integrity.

## Checkpoint v1.0.3-genesis — Configuration Integrity

Sprint 243 completed read-only canonical settings validation.

Acceptance:

- canonical settings checks: 50/50;
- Sprint 243 assertions: 61/61;
- exact schema and local-only endpoint boundaries verified;
- safe-idle and explicit-confirmation boundaries verified;
- traversal and secret-like key fixtures rejected;
- builtin skill registry compatibility restored;
- configuration, memory, and journal writes remained zero;
- runtime activation and systemd mutation remained disabled.

Next: Sprint 244 — Session and Memory Persistence Checks.

## Checkpoint v1.0.5-genesis — Session and Memory Persistence Checks

- Sprint 244 completed.
- Canonical boundary: `session_memory_persistence_checks`.
- Four canonical stores validated: browser sessions, chat history, memory, and journal.
- Validation passed: `81/81` base checks and `92/92` assertions.
- Read-only contract preserved: no repair, migration, persistent writes, runtime activation, socket binding, or systemd mutation.
- Next sprint: `250`
- Next boundary: `resource_baseline_metrics`.

## Sprint 245 Completion — Log Rotation and Storage Cleanup

AURA `v1.0.5-genesis` completes Sprint 245 at the
`log_rotation_storage_cleanup` boundary.

The canonical logger rotates `logs/aura.log` at `1 MB` and retains rotated
logs for `7 days`. Sprint 245 adds deterministic, read-only status, context,
contract-check, filesystem-capacity, and cleanup-preview visibility.

Cleanup execution remains disabled. The active log is protected; only
allowlisted rotated log names can become retention candidates; symlinks and
directory escape are blocked; canonical sessions, conversations, memory,
journal, audit data, and arbitrary files remain outside the cleanup boundary.

No canonical log deletion, move, truncation, compression, archive, service,
socket, systemd, network, or runtime activation occurs.

Next: Sprint 246 — Resource Baseline Metrics.
Next boundary: `resource_baseline_metrics`.

## Sprint 246 Completion — Resource Baseline Metrics

AURA `v1.0.6-genesis` completes Sprint 246 at the
`resource_baseline_metrics` boundary.

Sprint 246 adds deterministic, read-only, single-snapshot baseline visibility
for CPU usage and load averages, memory, swap, uptime, process count,
filesystem byte capacity, and inode capacity across `/`, `/home`,
`/mnt/aura-data`, and the AURA project root.

The implementation uses Linux `/proc`, `os.getloadavg`, and `os.statvfs`.
`psutil` is not required. Background sampling, rolling history, persistence,
dashboard activation, socket binding, systemd mutation, network access,
process control, and threshold mutation remain disabled.

Next: Sprint 247 — ATLAS Resource Monitoring.
Next boundary: `atlas_resource_monitoring`.

## Sprint 247 Completion — ATLAS Resource Monitoring

AURA `v1.0.7-genesis` completes Sprint 247 at the
`atlas_resource_monitoring` boundary.

Sprint 247 adds deterministic, read-only health classification over the
Sprint 246 resource baseline snapshot. It reports CPU, normalized load,
memory, swap, storage, inode capacity, uptime, and process-count states as
`healthy`, `warning`, `critical`, or `unavailable`.

The threshold policy is immutable and combines percentage thresholds with
absolute free-space thresholds for filesystems. Background sampling, rolling
history, metrics persistence, dashboard activation, alert delivery, socket
binding, systemd mutation, network access, process control, command execution,
and threshold mutation remain disabled.

Next: Sprint 248 — Localhost and SSH Tunnel Security Review.
Next boundary: `localhost_ssh_tunnel_security_review`.

## Sprint 248 Completion — Localhost and SSH Tunnel Security Review

AURA `v1.0.8-genesis` completes Sprint 248 at the
`localhost_ssh_tunnel_security_review` boundary.

Sprint 248 adds a deterministic, read-only security posture review covering
AURA's canonical `127.0.0.1:8765` binding, current listener exposure, SSH
listener scope, visible sshd configuration, SSH tunnel policy, SSH file
permission metadata, firewall visibility, and runtime activation.

The review reports `secure`, `review`, `warning`, or `unavailable` per
dimension. A non-secure posture state remains an observational finding and does
not imply contract failure when all safety assertions pass.

No sshd effective-policy execution, SSH connection, tunnel creation, credential
or private-key content read, firewall mutation, SSH configuration mutation,
service restart, socket activation, process control, key generation, known-host
mutation, or systemd mutation is performed.

Next: Sprint 249 — Permission Expiry and Recovery Review.
Next boundary: `permission_expiry_recovery_review`.

## Sprint 249 Completion — Permission Expiry and Recovery Review

AURA `v1.0.9-genesis` completes Sprint 249 at the
`permission_expiry_recovery_review` boundary.

Sprint 249 adds a deterministic, read-only source-contract review covering
permission grant lifecycle, expiry enforcement, stale-grant rejection, denial
lifecycle, revocation visibility, recovery visibility, rollback and
emergency-stop linkage, and audit linkage.

The canonical contract passes `96/96` assertions with all eight review
dimensions secure. It preserves the existing active permission runtime
baseline at `3115/3115` assertions.

The review does not import or execute the permission runtime, read permission,
audit, or recovery store contents, create or apply grants or denials, apply
expiry or revocation, execute recovery, rollback, or emergency stop, write
audit events, mutate files, control processes, activate services, open network
access, bind sockets, or mutate systemd.

Next: Sprint 250 — Backup and Restore Rehearsal.
Next boundary: `backup_restore_rehearsal`.
Next milestone: `v1.1.0`.

## Sprint 250 Completion — Backup and Restore Rehearsal

AURA `v1.1.0` completes Sprint 250 at the
`backup_restore_rehearsal` boundary and closes the Sprint 241–250
**Genesis Stabilization & Runtime Hardening** block.

Sprint 250 adds a deterministic, read-only rehearsal covering backup scope
inventory, manifest and digest integrity, restore-plan reversibility,
permission and approval boundaries, audit and provenance linkage, safe-idle
failure verification, contract deduplication, and block release acceptance.

The canonical contract passes `96/96` assertions with all eight dimensions
secure. It preserves the Sprint 249 anchor at `96/96`, the Genesis Final
release anchor at `1258/1258`, and the active permission runtime anchor at
`3115/3115`.

The rehearsal does not create backups or archives, read canonical data or
backup-store contents, execute restore or rollback, write manifests, replace
or delete files, mutate permissions or audit state, control processes,
activate services, open network access, bind sockets, or mutate systemd.

Next: Sprint 251 — AURA Launcher and Service Controls.
Next boundary: `aura_launcher_service_controls`.
Next version: `v1.1.1`.
Next block: Sprint 251–260 — Active Local Runtime & Model Service Integration,
targeting `v1.2.0`.

## Sprint 251 Completion — AURA Launcher and Service Controls

AURA `v1.1.1` completes Sprint 251 at the
`aura_launcher_service_controls` boundary and begins the Sprint 251–260
**Active Local Runtime & Model Service Integration** block.

Sprint 251 establishes a deterministic read-only integration facade for the
practical AURA launcher and service-control experience. It reuses the
canonical service lifecycle owner rather than creating another service
manager.

The canonical contract passes `120/120` assertions with all ten review
dimensions secure and zero findings. It preserves the Sprint 250 anchor at
`96/96`, the service-lifecycle anchor at `25/25`, the Genesis Final release
anchor at `1258/1258`, and the active permission runtime anchor at
`3115/3115`.

The integration facade covers launcher visibility, canonical service state,
bounded start and stop previews, status and health visibility, restart and
recovery planning, read-only log visibility, permission and audit ownership,
safe-idle failure behavior, and end-to-end acceptance scenarios.

It does not execute service start, stop, or restart; control processes; bind
sockets; access the network; mutate systemd or autostart; mutate logs,
permissions, or audit state; execute recovery; or run external commands.

Next: Sprint 252 — Manual Start, Stop, and Status Runtime.
Next boundary: `manual_start_stop_status_runtime`.
Next version: `v1.1.2`.

## Sprint 252 Completion — Manual Start, Stop, and Status Runtime

Version `v1.1.2` activates permission-gated supervised manual service control
on the canonical loopback runtime.

Delivered:

- explicit approved start and stop commands;
- live lifecycle, process, listener, ownership, and health status;
- strict PID identity using `/proc` start ticks, argv, cwd, UID, and command
  digest;
- exact owned-listener correlation;
- idempotent start and stop;
- bounded startup and shutdown timeouts;
- verified `SIGTERM` shutdown with bounded ownership-checked fallback;
- temporary per-user ownership, lock, and runtime log evidence under `/tmp`;
- successful start-status-stop rehearsal;
- capability `manual_start_stop_status_runtime`;
- contract result `144/144`, zero failures, twelve secure dimensions.

The rehearsal reached READY in `263 ms`, stopped in `106 ms`, created no
duplicate process, required no `SIGKILL`, and left zero process and listener
residue.

Restart, autostart, systemd mutation, non-loopback activation,
permission-store mutation, and persistent audit writing remain disabled.

Next: Sprint 253 — Restart, Logs, and Failure Visibility.

Next boundary: `restart_logs_failure_visibility`.

Next version: `v1.1.3`.

## Sprint 253 Completion — Restart, Logs, and Failure Visibility

Version `v1.1.3` adds permission-gated supervised restart,
bounded allowlisted log visibility, and structured failure reporting on top
of the canonical manual start/stop owner.

Delivered:

- explicit restart command requiring both `--approve-restart` and
  `--confirm-localhost`;
- restart from `STOPPED` through a fresh canonical start;
- restart from `RUNNING` through verified owned-process stop, safe-idle
  confirmation, a bounded restart gap, and a fresh canonical start;
- post-restart ownership, loopback listener, process identity, and health
  verification;
- PID rotation verification across a running restart;
- bounded log tail with a maximum of 200 lines and 65,536 bytes;
- allowlisted active, latest-rotated, and temporary runtime log sources;
- symlink rejection, arbitrary-path rejection, and credential redaction;
- normalized failure packets covering ownership, stop, launch, health,
  cleanup, and log-preflight stages;
- contract result `168/168`, zero failures, fourteen secure dimensions;
- capability `restart_logs_failure_visibility`.

The supervised runtime rehearsal completed two successful restarts, verified
a new PID after the running restart, preserved canonical data, kept canonical
logs append-only, and returned AURA to `STOPPED` with zero listener and
process residue.

Systemd mutation, autostart mutation, non-loopback binding, arbitrary PID
signaling, arbitrary log paths, permission-store mutation, persistent audit
writing, and canonical-log mutation remain disabled.

Next: Sprint 254 — Process Ownership and Service State Persistence.

Next boundary: `process_ownership_service_state_persistence`.

Next version: `v1.1.4`.

## Sprint 254 Completion — Process Ownership and Service State Persistence

AURA `v1.1.4` completes Sprint 254 at the
`process_ownership_service_state_persistence` boundary.

Delivered:

- canonical state at `data/runtime/service_state.json`;
- schema v2 with PID, process start ticks, Linux boot ID, UID, command, cwd,
  loopback endpoint, and timestamps;
- mode `0600` file and `0700` parent directory;
- `O_EXCL`, `O_CLOEXEC`, `O_NOFOLLOW`, `fstat`, file fsync, atomic replace,
  and directory fsync;
- stale, previous-boot, and foreign-user record classification;
- explicit recovery only through approved start, stop, or restart;
- read-only status and recovery preview;
- contract `192/192`, zero failures, sixteen secure dimensions.

Systemd, autostart, arbitrary PID signaling, non-loopback binding, automatic
stale cleanup, permission-store mutation, persistent audit writing, and
background recovery remain disabled.

Next: Sprint 255 — Reviewed Optional Autostart.
Next boundary: `reviewed_optional_autostart`.
Next version: `v1.1.5`.

## Sprint 255 Completion — Reviewed Optional Autostart

AURA `v1.1.5` completes Sprint 255 at the
`reviewed_optional_autostart` boundary.

Delivered:

- exact `aura-local.service` user-unit preview;
- canonical `ExecStart` derived from the supervised runtime owner;
- project working directory and loopback runtime handoff;
- bounded `Restart=on-failure` policy;
- read-only user-manager, unit, and linger posture;
- explicit activation preview with confirmation token;
- complete rollback preview;
- contract result `216/216`, zero failures, eighteen secure dimensions.

No unit was written. No daemon reload, enable, start, linger change, system-unit
mutation, non-loopback binding, or automatic activation was performed.

Next: Sprint 256 — Persistent Local Chat Session Activation.
Next boundary: `persistent_local_chat_session_activation`.
Next version: `v1.1.6`.

## Sprint 256 Completion — Persistent Local Chat Session Activation

AURA `v1.1.6` completes Sprint 256 at the
`persistent_local_chat_session_activation` boundary.

Delivered:

- the existing browser-chat session manager remains the canonical owner;
- descriptor-safe session reads using directory-relative `open`, `O_NOFOLLOW`,
  `fstat`, UID checks, private-mode checks, and bounded reads;
- cross-process shared/exclusive locking on the storage-directory descriptor;
- secure write preparation with directory mode `0700`;
- session files mode `0600`;
- exclusive temporary creation, file fsync, atomic replace, and directory fsync;
- existing schema `1.0`, integrity hashes, revisions, and idempotent message
  submission remain compatible;
- bounded metadata-only history and exact session loading;
- isolated create, submit, cross-instance load/list, integrity, and symlink
  rejection rehearsal;
- contract result `240/240`, zero failures, twenty secure dimensions.

The existing canonical session content is not rewritten by implementation.
Directory-mode migration from `0775` to `0700` remains a separately validated
finalization step. Model-service activation, network access, non-loopback
binding, automatic memory handoff, session-content logging, systemd mutation,
and autostart activation remain disabled.

Next: Sprint 257 — Local Model Service Discovery and Health.
Next boundary: `local_model_service_discovery_health`.
Next version: `v1.1.7`.

## Sprint 257 Completion — Local Model Service Discovery and Health

AURA `v1.1.7` completes Sprint 257 at the
`local_model_service_discovery_health` boundary.

Delivered:

- the Sprint 187 local model bridge remains the canonical provider owner;
- read-only Ollama binary, systemd unit, process, and listener discovery;
- loopback-only endpoint and resolved-address enforcement;
- environment profile posture without credential reads or persistence;
- provider contract visibility for Ollama and OpenAI-compatible local servers;
- default endpoint `http://127.0.0.1:11434`;
- default-off health probing with a two-second timeout and exact confirmation
  token `PROBE_LOCAL_MODEL_SERVICE`;
- count-only model inventory from the health response;
- healthy, degraded/unprobed, and unavailable classification;
- isolated fake-transport rehearsal with no canonical network access;
- contract result `264/264`, zero failures, twenty-two secure dimensions.

The implementation does not start, stop, or install Ollama; download, pull,
load, or unload models; route chat; contact non-loopback endpoints; read
credentials; mutate systemd or autostart; or run a health probe automatically.

Next: Sprint 258 — Local Model Router Activation.
Next boundary: `local_model_router_activation`.
Next version: `v1.1.8`.

## Sprint 258 Completion — Local Model Router Activation

AURA `v1.1.8` completes Sprint 258 at the
`local_model_router_activation` boundary.

Delivered:

- the existing `ModelRouter` remains the canonical route owner;
- the Sprint 187 local model bridge remains the execution owner;
- the Sprint 257 health boundary remains the provider-health dependency;
- existing configured route metadata is reused without a new route registry;
- exact-route preview with alias normalization;
- unknown-route fallback remains visible but cannot execute;
- only online routes matching the validated provider and model may execute;
- validated reasoning profile from `aura/config/settings.yaml`;
- explicit provider-health verification before handoff;
- exact model-request confirmation token `ROUTE_LOCAL_MODEL_REQUEST`;
- bounded routed-message validation;
- isolated fake-transport bridge handoff rehearsal;
- contract result `288/288`, zero failures, twenty-four secure dimensions.

No route decision is persisted. Real runtime switching, service control, model
download/pull/load/unload, queue activation, resource-budget mutation,
non-loopback networking, credential reads, systemd mutation, and autostart
mutation remain disabled. Live inference is disabled by default and is reserved
for one explicitly approved finalization rehearsal.

Next: Sprint 259 — Model Loading, Unloading, Queue, and Resource Budgets.
Next boundary: `model_loading_unloading_queue_resource_budgets`.
Next version: `v1.1.9`.


## Sprint 259 Completion — Model Loading, Unloading, Queue, and Resource Budgets

AURA `v1.1.9` completes Sprint 259 at the
`model_loading_unloading_queue_resource_budgets` boundary.

Delivered: explicit provider lifecycle contracts, `keep_alive` loading,
explicit release, metadata-only residency status, a bounded in-memory queue
(depth 4, one in-flight item, 120-second timeout), and read-only memory, swap,
load, and optional GPU budget gates. The contract passes `312/312` assertions
across twenty-six secure dimensions.

Automatic load/release, model download/pull, queue persistence, background
workers, threshold mutation, service control, non-loopback networking,
credentials, systemd mutation, and autostart mutation remain disabled.

Next: Sprint 260 — Active Local Runtime Integration and Stabilization.
Next boundary: `active_local_runtime_integration_stabilization`.
Next version: `v1.2.0`.


## Sprint 260 Completion - Active Local Runtime Integration and Stabilization

AURA `v1.2.0` completes Sprint 260 and closes the Sprint 251-260 Active Local Runtime and Model Service Integration block.

The coordinator combines manual service control, safe idle, private persistent chat, explicit Ollama health, exact `companion` routing, explicit model lifecycle, bounded in-memory queueing, read-only resource budgets, persistence only after a successful bounded response, and mandatory stop-and-restore behavior.

Contract target: `336/336` across twenty-eight secure dimensions. Sprint 261 requires roadmap reconfirmation after `v1.2.0`.

Next boundary: `roadmap_reconfirmation_required_after_v1_2_0`.

## Canonical v1.2.1 to v1.3.0 Product Block

Current completed sprint: Sprint 261 — Roadmap Reconfirmation after v1.2.0.

The canonical Sprint 261–270 block is
`daily_chat_control_center_productization`, targeting v1.3.0. Sprint 270 must
complete a live end-to-end acceptance test, relevant failure/recovery testing,
and safe-idle restoration before Sprint 271 begins.

## Sprint 262 Operational Browser Handoff

Current completed sprint: Sprint 262 — Operational Browser Chat Model Handoff.

The explicitly confirmed browser model route now canonically targets
`companion`. Native process-role classification is active and the historical
count allowance removed. Next boundary:
`session_list_resume_rename_archive_restore`.

## Sprint 263 Session List, Resume, Rename, Archive, and Restore

Current completed sprint: Sprint 263 —
`session_list_resume_rename_archive_restore`.

The localhost browser chat now provides active and archived session lists,
same-session resume, validated title-only rename, non-destructive archive, and
non-destructive restore. Session IDs do not change, histories are not merged
between sessions, archived sessions are mutation-blocked until restoration,
and all metadata mutations reuse atomic persistence and integrity validation.

Permanent session deletion remains outside the runtime boundary.

Next boundary: `chat_history_recovery_ux`.

## Sprint 264 Chat History Recovery UX

Current completed sprint: Sprint 264 — `chat_history_recovery_ux`.

AURA now exposes a read-only local history recovery diagnostic and a browser
recovery panel. Integrity failures remain fail-closed and preserve the
original file. Stale revision conflicts reload the latest session while
preserving the unsent draft in memory. Missing sessions return to neutral
no-session state, and archived conflicts expose explicit restore guidance.

Automatic repair, quarantine, session replacement, cross-session history
merge, permanent delete, model invocation, and network fallback remain
disabled.

Next boundary: `review_first_memory_integration`.

## Sprint 265 — Review-First Memory Integration

- Version: `v1.2.5`
- Boundary: `review_first_memory_integration`
- Next boundary: `control_center_runtime_ux_consolidation`
- Adds an explicit browser review surface for one selected user message.
- Candidate lifecycle: create, edit, privacy hold, approve future write preview, or reject transient candidate.
- Queue and edits are in-process only and reset on service restart.
- Approval creates a permission-envelope preview; it does not apply a grant.
- Durable memory writes and `MemoryStore` construction or mutation remain disabled.
- Automatic memory write, merge, delete, model invocation, network access, tool execution, and command execution remain disabled.

## Sprint 266 — Control Center Runtime UX Consolidation — Complete

Version `v1.2.6` consolidates service, bounded logs/failure metadata,
model queue/resource budgets, safety visibility, chat navigation, and
review-first memory summary in the existing local Control Center.

The boundary remains read-only and safe-idle. Sprint 267 continues with
`atlas_resource_monitoring_dashboard`.

## Sprint 267 — ATLAS Resource Monitoring Dashboard — Complete

Version `v1.2.7` adds read-only CPU, RAM, swap, storage, uptime,
process-count, and rolling-history visibility to the existing local
Control Center. The implementation reuses `/api/control-center`, keeps
history in-process, and remains safe-idle.

Sprint 268 continues with `permission_audit_action_visibility_ux`.

## Sprint 268 — Permission Audit Action Visibility UX — Complete

Version `v1.2.8` consolidates permission, audit, proposal, approval,
action, and recovery visibility in the existing local Control Center.
The implementation reuses `/api/control-center`, exposes no controls,
and remains read-only and safe-idle.

Sprint 269 continues with `daily_use_acceptance_rehearsal_and_release_harness`.

## Sprint 269 — Daily-use Acceptance Rehearsal Release Harness — Complete

Version `v1.2.9` aggregates baseline, service, browser chat, model
handoff, memory review, permission/action visibility, ATLAS resource,
release-decision, and safe-idle evidence in the existing local Control
Center.

Sprint 270 continues with `daily_local_assistant_live_acceptance_stabilization` and requires live E2E,
failure/recovery verification, and return to safe-idle.

## Sprint 270 — Daily Local Assistant Live Acceptance Stabilization — Complete

Version `v1.3.0` closes the Sprint 261–270 daily local product block. A real
live end-to-end acceptance run proved service startup, health and Control
Center availability, persistent chat recovery, local-model usage before and
after recovery, bounded failure, canonical restart, and safe-idle return.

Acceptance evidence SHA-256: `72dbd6c243d55171b39f1b2a1a659ee654ea7622c31e09c0ea9000a666e29fb1`.

The release preserves review-first memory, applies no permission grant, creates
no unrelated chat mutation, adds no new route or web panel, and ends with the
service stopped, ownership clear, persistent state absent, and port 8765
closed.

Next implementation boundary: `voice_daily_use_activation`. Sprint 271
discovery must reconcile this immediate boundary with the existing broader
ORION roadmap before implementation; Sprint 270 does not silently reschedule
that roadmap.

## Sprint 271 — Voice Daily-Use Activation — Complete

Version `v1.3.1` activates a bounded local voice path between ORION and
ATLAS. The user explicitly holds the dashboard button or focused-page `V`;
ORION records only during the requested turn; ATLAS performs local STT; the
transcript remains editable; Open Chat Draft does not send automatically;
local TTS is explicit; and Stop/Esc interrupts playback or capture.

Live acceptance passed `21/21` plus `14/14` reconciliation and returned the
runtime to safe-idle with the listener closed, worker released, and no
temporary-audio residue.

Next implementation boundary:
`voice_auto_conversation_and_companion_context_reinforcement`.

## Canonical execution sequence — Sprint 272 to Sprint 300

The milestone targets remain unchanged: Sprint 280 -> `v1.4.0`, Sprint 290
-> `v1.5.0`, and Sprint 300 -> `v2.0.0`. Each sprint remains
discovery-first, and Sprints 280, 290, and 300 require live end-to-end
acceptance with failure/recovery proof and final safe-idle restoration.

| Sprint | Canonical focus |
|---:|---|
| 272 | PTT auto-conversation, TTS autoplay, initial companion persona/context reinforcement |
| 273 | Native ORION agent foundation |
| 274 | Authenticated pairing and device identity |
| 275 | Capability negotiation, heartbeat, and live runtime grounding |
| 276 | Allowlisted action preview and explicit approval |
| 277 | Scoped permission/expiry/audit and reviewed-memory relevance |
| 278 | Bounded ORION actions for capture, app launch, files, and OBS |
| 279 | Watchdog, emergency stop, recovery, and natural-dialogue evaluation |
| 280 | Mandatory live acceptance and `v1.4.0` |
| 281 | Game detection and session-mode foundation |
| 282 | Observer capture and input telemetry |
| 283 | Coach Mode foundation and VAD foundation |
| 284 | Recording pipeline and speech-turn detection |
| 285 | Explicit hands-free session alpha and auto-idle |
| 286 | Echo guard, device switching, and game/OBS coexistence |
| 287 | Barge-in and interruption |
| 288 | Coach + Observer + Recording + voice integration |
| 289 | Disconnect, emergency-stop, and recovery rehearsal |
| 290 | Mandatory live acceptance, hands-free beta, and `v1.5.0` |
| 291 | v2 scope freeze and integration contract |
| 292 | Unified chat, voice, vision, memory, and ORION session |
| 293 | Context quality, persona consistency, and memory relevance |
| 294 | Release-grade hands-free hardening and conversation recovery |
| 295 | Control Center UX and ATLAS/ORION monitoring |
| 296 | Base plugin manager and capability registration |
| 297 | Initial avatar/dashboard presence |
| 298 | Security, privacy, backup, restore, and rollback |
| 299 | v2 release-candidate rehearsal |
| 300 | Mandatory live acceptance and `v2.0.0` |

Hands-free remains an optional explicitly enabled mode, never the default.
Sensitive actions continue to require preview and approval; v2 does not
introduce unrestricted shell access, silent cloud fallback, hidden
microphone capture, unrestricted ORION control, or multiplayer automation.

## Sprint 280 Closure - v1.4.0 Live Acceptance

Sprint 280 completed the mandatory cross-host live end-to-end acceptance
for the Sprint 271-280 ORION Safe Action Bridge block.

Accepted evidence:

- browser voice checks 6/6;
- authenticated ORION-to-ATLAS localhost SSH tunnel;
- one controlled `create_controlled_file` execution;
- exact content digest and verified cleanup;
- watchdog `live -> stale -> failed`;
- automatic recovery disabled;
- manual emergency and reviewed recovery markers 3/3;
- full ORION, browser session, and web regression suite passed;
- service and acceptance harness stopped in safe-idle.

This closes the v1.4.0 boundary without enabling unrestricted control.
The next product block begins at Sprint 281.

## Sprint 281 - Game Companion Runtime Foundation

Sprint 281 opens the Sprint 281-290 Game Companion block with a deterministic,
side-effect-free foundation at v1.4.1.

Accepted scope:

- canonical Game Companion game catalog;
- `osu_offline` as the first reference game;
- Coach only, Observer only, Coach + Observer, and Coach + Observer + Recording;
- review-only session proposals;
- nine-state session contract;
- operator-controlled start and stop;
- emergency-stop and failure-safe states;
- public livestream/private dataset separation;
- all detection, capture, telemetry, recording, coaching output, application
  launch, game input control, and autonomous gameplay fields closed.

The next boundary is Sprint 282 `supported_game_detection`.

## Sprint 282 - Supported Game Detection

Sprint 282 adds the first read-only Game Companion runtime capability at
v1.4.2.

Accepted implementation scope:

- capability `orion.game.detect_supported.read_only`;
- explicit one-shot scan only;
- exact local allowlist filtering on ORION;
- only `osu_offline` / `osu!.exe` active;
- visible top-level window requirement;
- raw process inventory, command line, executable path, and raw window title
  excluded from exported evidence;
- authenticated identity, freshness, sequence, digest, and replay validation;
- in-memory detection-event deduplication;
- safe `game_detected_pending_review` prompt;
- no automatic start of capture, recording, telemetry, coaching, application
  launch, voice action, or game control.

Sprint 283 implements `game_window_capture`.

## Sprint 283 - Game Window Capture

Sprint 283 adds bounded explicit one-shot selected-game-window capture at
v1.4.3.

Accepted implementation scope:

- capability `orion.game.capture_window.one_shot`;
- capture only after Sprint 282 detection review and operator mode selection;
- separate exact capture preview and approval;
- one expiring single-use permission;
- exact ATLAS agent/device/game/process/executable/window binding;
- selected-window-only PowerShell/System.Drawing adapter contract on ORION;
- one bounded PNG frame;
- temporary private ORION storage;
- metadata-only receipt containing MIME type, dimensions, size, and SHA-256;
- no raw image bytes, raw title, or local path in ATLAS packets;
- explicit cleanup receipt and safe-idle restoration;
- no full-screen fallback, background capture, audio capture, recording,
  telemetry, coaching, application launch, voice action, or game control.

Sprint 284 owns `game_audio_capture`.

## Sprint 284 Completion — Game Audio Capture

AURA `v1.4.4` implements `game_audio_capture` as one explicit bounded sample
from the reviewed `osu_offline` process on ORION.

Delivered:

- visible ATLAS audio preview;
- exact operator approval;
- expiring single-use permission;
- exact agent, device, game, process, executable, and window binding;
- process-loopback `IncludeTargetProcessTree` contract;
- maximum five-second duration;
- 48 kHz stereo signed-16-bit PCM WAV;
- one MiB encoded-size limit;
- temporary private ORION artifact;
- metadata-only receipt with SHA-256;
- explicit cleanup and return to `safe_idle`.

Microphone input, whole-system fallback, arbitrary endpoint capture,
continuous capture, recording, transcription, telemetry, coaching,
application launch, voice-command-to-action, and game input control remain
disabled.

Next: Sprint 285 — Game Input Telemetry.
Next boundary: `game_input_telemetry`.
Next version: `v1.4.5`.

## Sprint 285 Completion - Game Input Telemetry

AURA `v1.4.5` implements `game_input_telemetry` as one explicit, bounded,
foreground-only observation sample from the reviewed `osu_offline` process on
ORION.

Delivered:

- visible ATLAS telemetry preview;
- exact operator approval;
- expiring single-use permission;
- exact agent, device, game, process, process-start, executable, and window
  binding;
- foreground binding enforced on every poll with fail-closed focus loss;
- semantic `Z`/`X` and left/right mouse transitions only;
- cursor coordinates normalized to the bound game client area;
- maximum five-second observation window;
- 17 ms polling contract and 60 Hz cursor ceiling;
- 512-event and 128 KiB limits;
- temporary private ORION JSONL artifact;
- metadata-only receipt and SHA-256;
- explicit cleanup and return to `safe_idle`;
- live ORION acceptance with 128 events and a final event timestamp of
  4,984 ms.

Arbitrary keys, text, clipboard reads, raw scan codes, background capture,
global cursor history, absolute coordinates, hooks, Raw Input, input
injection, controller control, continuous monitoring, recording, coaching,
autonomous gameplay, and multiplayer automation remain disabled.

Next: Sprint 286 - Game Timestamp Synchronization.
Next boundary: `game_timestamp_synchronization`.
Next version: `v1.4.6`.

## Sprint 286 Completion - Game Timestamp Synchronization

AURA `v1.4.6` implements one permission-bound, bounded shared ORION monotonic
session clock for Game Companion window, audio, and input metadata.

Delivered:

- one high-resolution ORION reference clock and explicit frequency;
- one UTC anchor used only for correlation;
- one shared epoch across three stream identifiers;
- hashed clock, epoch, and stream-start tick identities;
- per-stream relative timestamps and contiguous sequence;
- 16 ms window, 10 ms audio, and 17 ms input reference cadences;
- a two-second and 1,024-envelope maximum contract;
- fail-closed clock-discontinuity handling;
- metadata-only ATLAS review;
- ORION preflight at 10 MHz with 6.4 microsecond maximum anchor uncertainty;
- a 1,200 ms logical probe with 264 envelopes and maximum timestamp
  1,186.5345 ms;
- no real capture, raw export, cleanup requirement, or persistent active
  runtime;
- final return to `safe_idle`.

Next: Sprint 287 - Game Session Orchestration.
Next boundary: `game_session_orchestration`.
Next version: `v1.4.7`.
Native ORION overlay foundation target: Sprint 288.

## Sprint 287 — Game Session Orchestration

- Version: `v1.4.7`
- Boundary: `game_session_orchestration`
- Runtime: `aura.game_session_orchestration_runtime`
- Profiles: Coach only, Observer only, Coach + Observer, and Coach + Observer +
  Recording.
- Safety: explicit permission, exact game/window binding, foreground gate,
  shared timestamp dependency, fail-closed transitions, partial-start rollback,
  idempotent stop, emergency stop-all, metadata-only status, safe-idle default.
- Acceptance: ATLAS in-memory contract probe passed 88 assertions with all
  profiles and failure paths returned to safe idle.
- Next: Sprint 288 `orion_native_overlay_foundation`.
