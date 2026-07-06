# AURA

```text

========================================================

            █████╗ ██╗   ██╗██████╗  █████╗
           ██╔══██╗██║   ██║██╔══██╗██╔══██╗
           ███████║██║   ██║██████╔╝███████║
           ██╔══██║██║   ██║██╔══██╗██╔══██║
           ██║  ██║╚██████╔╝██║  ██║██║  ██║
           ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

                 PROJECT GENESIS
                  STATUS : ACTIVE

========================================================



AI Partner that grows together with its creator.

Motto: Grow Together
Creator: Kiput
Codename: Genesis
Current Phase: Foundation / Early Mind

What is AURA?

AURA is a local-first modular AI partner designed to accompany and help its creator work, create, learn, build, play, stream, and grow.

AURA is not just a chatbot.

AURA is being built as:

Companion
+ Work Assistant
+ Coding Assistant
+ Project Manager
+ Creative Assistant
+ Voice Companion
+ 3D Avatar
+ Screen/Camera Aware Assistant
+ Gaming/Streaming Companion

AURA's long-term architecture is:

One identity.
Multiple internal roles.
Multiple specialized models.
Plugin-based abilities.
Event-driven core.
Safe autonomy.
Current Status
Version : 0.62.0-genesis
Status  : SAFE FILE OPERATION PLANNER ONLINE
Runtime : Local-first
Server  : ATLAS
Model   : Ollama / llama3.2
Current Capabilities

AURA currently supports:

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
- Project journal
- Role system foundation
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
- Memory-aware chat
- Identity guardrail
- Language control
Planned Capabilities

AURA is planned to eventually support:

- Voice input and output
- Screen analyzer
- Camera analyzer
- 3D VRM/VRoid avatar
- Hand tracking
- Motion capture
- 3D environment movement
- Coding assistant
- Modelling assistant
- Animation assistant
- Video editing assistant
- Image and 3D generation support
- Project manager
- App/browser/file control when requested
- Livestream assistant
- Gaming companion
- Sandbox game interaction
- Singing mode
- Desktop app
- Android/mobile companion
Core Philosophy

AURA should be:

Friendly, but not excessive.
Intelligent, but not arrogant.
Humorous at the right time.
Professional while working.
Supportive, not judgmental.
Context-aware.
Honest when she does not know.
Able to take initiative.
Able to stay quiet when appropriate.
When is AURA considered alive?

AURA can be considered alive when she can:

Speak.
See.
Think.
Learn.

System meaning:

Speak  = voice system is online
See    = screen/camera vision is online
Think  = role/model routing is online
Learn  = memory, journal, and context systems are online
Documentation

Main roadmap:

AURA Master Roadmap
Current Architecture
main.py
└── AuraCLI
    ├── commands
    ├── interactive shell
    ├── chat
    ├── memory management
    └── provider checks

AuraApp
├── AuraBoot
├── EventBus
├── PluginManager
├── HealthCheck
├── MemoryStore
├── ConversationStore
└── ReasoningProvider
    └── OllamaProvider
Current Commands
python3 main.py
python3 main.py shell

python3 main.py chat "hello"
python3 main.py history --limit 5

python3 main.py remember "something important"
python3 main.py recall --limit 5
python3 main.py memory-search "query"
python3 main.py memory-count
python3 main.py memory-list --limit 5
python3 main.py memory-delete "<memory_id>"

python3 main.py provider
python3 main.py provider-check

python3 main.py desktop-status
python3 main.py desktop-capabilities
python3 main.py desktop-action app.open

python3 main.py system-status
python3 main.py status-full

python3 main.py vision-runtime-status
python3 main.py vision-runtime-plan
python3 main.py vision-runtime-check

python3 main.py vision-status
python3 main.py vision-providers

python3 main.py awakening-status
python3 main.py awaken

python3 main.py voice-runtime-status
python3 main.py voice-runtime-plan
python3 main.py voice-runtime-check

python3 main.py voice-status
python3 main.py voice-providers

python3 main.py project-map
python3 main.py project-inspect aura/core
python3 main.py project-find ContextManager

python3 main.py project-summary
python3 main.py project-files --limit 30
python3 main.py project-read README.md

Aliases are also available for several commands, including:

ask
mem
mem-search
mem-count
mem-list
mem-delete
reason
reason-check
Near-Term Roadmap
v0.20.0 — Master Roadmap Document
v0.21.0 — Project Journal Foundation
v0.22.0 — Role System Foundation
v0.23.0 — Memory Pin and Importance
v0.24.0 — Context Manager v1
v0.25.0 — Permission System Foundation
v0.26.0 — Skill Registry
v0.27.0 — Plugin Action Interface
v0.28.0 — File and Project Plugin
v0.29.0 — Voice Foundation
v0.30.0 — AURA Awakening Alpha
Development Notes

AURA is currently in the Genesis phase.

The current priority is to build a stable mind foundation before moving into voice, vision, avatar, desktop app, and mobile interaction.

Grow Together.



## Product Vision

The long-term product vision for AURA is documented in:

docs/AURA_PRODUCT_VISION.md

This document defines AURA's future serious/work mode, creative mode, relaxed mode, media understanding, game companion direction, streaming mode, app bridge vision, Blender bridge plan, safety philosophy, expression language, and 10-sprint review rule.


## Sprint 63.0 — Codebase Change Planner

AURA includes a Codebase Change Planner foundation for metadata-only planning around codebase changes.

Capabilities:
- codebase_change.status
- codebase_change.intent_plan
- codebase_change.impact_plan
- codebase_change.patch_plan
- codebase_change.validation_plan
- codebase_change.rollback_plan
- codebase_change.context

Safety boundary:
- no automatic file reads
- no automatic file opens
- no automatic file writes or edits
- no move/copy/delete operations
- no command execution
- no git commit or push
- proposal-only planning until explicit confirmation and validation


## Sprint 64.0 — Codebase Patch Proposal Renderer

AURA includes a Codebase Patch Proposal Renderer foundation for proposal-only patch review packets.

Capabilities:
- codebase_patch_proposal.status
- codebase_patch_proposal.render
- codebase_patch_proposal.review_packet
- codebase_patch_proposal.validation_packet
- codebase_patch_proposal.rollback_packet
- codebase_patch_proposal.context

Safety boundary:
- no automatic file reads
- no automatic file opens
- no automatic file writes or edits
- no automatic patch apply
- no move/copy/delete operations
- no command or test execution
- no git commit or push
- proposal-only review packets until explicit confirmation and validation


## Sprint 65.0 — Codebase Validation Gate Planner

AURA includes a Codebase Validation Gate Planner foundation for proposal-only validation gates around codebase changes.

Capabilities:
- codebase_validation_gate.status
- codebase_validation_gate.plan
- codebase_validation_gate.preflight
- codebase_validation_gate.static_validation
- codebase_validation_gate.registry_validation
- codebase_validation_gate.runtime_smoke
- codebase_validation_gate.diff_review
- codebase_validation_gate.rollback
- codebase_validation_gate.commit_push
- codebase_validation_gate.context

Safety boundary:
- no automatic file reads
- no automatic file opens
- no automatic file writes or edits
- no automatic patch apply
- no command or test execution
- no git commit or push
- validation gates are proposal-only until explicit confirmation and manual execution



## Sprint 66.0 — Voice Conversation Planner

AURA includes a Voice Conversation Planner foundation for metadata-only voice conversation planning.

Status: VOICE CONVERSATION PLANNER ONLINE

Safety boundary:
- no microphone access
- no speaker output
- no TTS runtime output
- no audio recording
- no wake word runtime
- no voice command execution
- no app opening
- no file writing
- no command execution
- no external action execution
- no real tool execution


## Sprint 67.0 — Vision Context Planner

AURA includes a Vision Context Planner foundation for metadata-only visual context planning.

Status: VISION CONTEXT PLANNER ONLINE

Safety boundary:
- no screen capture
- no camera access
- no image opening or reading
- no video capture
- no OCR runtime
- no visual recognition runtime
- no desktop action execution
- no app opening
- no file reading or writing
- no command execution
- no external action execution
- no real tool execution


## Sprint 68.0 — Avatar Interaction Planner

AURA includes an Avatar Interaction Planner foundation for metadata-only avatar interaction planning.

Status: AVATAR INTERACTION PLANNER ONLINE

Safety boundary:
- no avatar rendering
- no animation playback
- no mocap runtime
- no camera, face, or body tracking
- no rig, bone, or blendshape control
- no Blender execution
- no OBS control
- no desktop action execution
- no app opening
- no file reading or writing
- no command execution
- no external action execution
- no real tool execution


## Sprint 69.0 — Desktop Workflow Planner

AURA includes a Desktop Workflow Planner foundation for metadata-only desktop workflow planning.

Status: DESKTOP WORKFLOW PLANNER ONLINE

Safety boundary:
- no desktop control
- no app opening
- no window inspection or control
- no mouse or keyboard control
- no screen capture
- no clipboard access
- no notification access
- no process inspection
- no file reading or writing
- no command execution
- no external action execution
- no real tool execution


## Sprint 70.0 — Partner Runtime Planning Layer

AURA includes a Partner Runtime Planning Layer for metadata-only coordination across partner-mode planners.

Status: PARTNER RUNTIME PLANNING LAYER ONLINE

Safety boundary:
- no autonomous runtime
- no background agent loop
- no scheduled self-execution
- no tool execution
- no file reading or writing
- no command execution
- no desktop control
- no app opening
- no screen capture
- no camera or microphone access
- no speaker output
- no avatar rendering
- no network action
- no git commit or push execution
- no external action execution
- no real tool execution


## Sprint 71.0 — Thought Loop Planner

AURA includes a Thought Loop Planner foundation for metadata-only thinking cycles.

Status: THOUGHT LOOP PLANNER ONLINE

Purpose:
- support the core AURA concept: Grow Together
- help AURA think before acting
- help AURA stay intelligent without pretending to know
- plan uncertainty review before answering
- plan permission gates before future actions
- plan growth memory review without writing memory automatically

Safety boundary:
- no autonomous thought loop
- no background loop
- no continuous self-prompting
- no self-triggered action
- no tool execution
- no memory write
- no internet search
- no file reading or writing
- no command execution
- no desktop control
- no camera or microphone access
- no speaker output
- no avatar rendering
- no network action
- no git execution
- no external action execution
- no real tool execution


## Sprint 72.0 — Reasoning Context Manager

AURA includes a Reasoning Context Manager foundation for safe visible reasoning context.

Status: REASONING CONTEXT MANAGER ONLINE

Purpose:
- help AURA organize context before answering
- separate facts, assumptions, unknowns, constraints, and goals
- prepare visible reasoning summaries without exposing hidden chain-of-thought
- support the principle: cerdas, tetapi tidak sok tahu
- prepare evidence boundaries and confidence framing
- prepare response strategy before action

Safety boundary:
- no hidden chain-of-thought exposure
- no private reasoning disclosure
- no autonomous reasoning loop
- no background reasoning loop
- no self-triggered action
- no tool execution
- no memory write
- no internet search
- no file reading or writing
- no command execution
- no desktop control
- no camera or microphone access
- no speaker output
- no avatar rendering
- no network action
- no git execution
- no external action execution
- no real tool execution


## Sprint 73.0 — Knowledge Uncertainty & Internet Search Gate

AURA includes a Knowledge Uncertainty Gate foundation for honest knowledge behavior and future internet/search/download permission gates.

Status: KNOWLEDGE UNCERTAINTY GATE ONLINE

Purpose:
- help AURA avoid pretending to know
- separate known facts, assumptions, and unknowns
- plan when AURA should ask Kiput first
- plan when internet search permission is needed
- plan source requirements before future search
- plan download/dependency notices before future project downloads
- plan answer confidence before responding

Safety boundary:
- no real internet search
- no web request
- no source fetch
- no browser opening
- no network action
- no download execution
- no file download
- no dependency/package install
- no tool execution
- no memory write
- no file reading or writing
- no command execution
- no fabricated answers or fabricated sources
- no external action execution
- no real tool execution


## Sprint 74.0 — Voice Input Runtime Foundation

AURA includes a Voice Input Runtime Foundation for future safe hearing capability.

Status: VOICE INPUT RUNTIME FOUNDATION ONLINE

Purpose:
- prepare AURA's future ability to hear Kiput through voice
- plan microphone permission before any microphone access
- plan voice capture boundaries without recording audio
- plan speech-to-text adapter selection without running STT
- separate normal conversation from voice commands
- require confirmation before future voice command execution
- support AURA's essence: think, hear, see

Safety boundary:
- no microphone access
- no audio recording or capture
- no speech-to-text runtime
- no wake word detection
- no always-listening mode
- no background listening
- no voice command execution
- no speaker/TTS runtime
- no network/cloud STT
- no file operations
- no command execution
- no tool execution
- no memory write
- no internet/network action
- no desktop control
- no git execution
- no external action execution
- no real tool execution
