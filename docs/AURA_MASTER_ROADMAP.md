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
- online capabilities: 12
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
- online capabilities: 13
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
- online capabilities: 14
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
- online capabilities: 15
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
- online capabilities: 16
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
- online capabilities: 17
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
- online capabilities: 18
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
- online capabilities: 19
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
- online capabilities: 19
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
- online capabilities: 20
- foundation-only capabilities: 10
- planner-only capabilities: 7
- permission-gated planner capabilities: 2
- review-only capabilities: 1
- planned future capabilities: 0
- disabled runtime capabilities: 2
- runtime execution features: 0

No web server runtime, frontend/backend/API runtime, route creation runtime, static file serving runtime, port binding, browser launch, websocket runtime, chat runtime, session runtime, plugin runtime, permission grant/deny runtime, runtime action activation, file operation, static asset generation runtime, command execution, network action, tool execution, memory write, desktop control, git execution, external action, or real tool execution is enabled.


## Sprint 92.0 — AURA Local Console API Schema Foundation

Target: v0.102.0-genesis
Status: LOCAL CONSOLE API SCHEMA FOUNDATION ONLINE

AURA can provide planner-only Local Console API Schema Foundation planning for API schema catalog, endpoint blueprints, response envelopes, request schema blueprints, validation rules, permission boundary schemas, error contracts, schema versioning, and API schema safety policy.

Capability Registry now tracks AURA Local Console API Schema Foundation:
- total capabilities tracked: 23
- online capabilities: 21
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
