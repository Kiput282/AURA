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
Version : 0.24.0-genesis
Status  : CONTEXT MANAGER V1 ONLINE
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

