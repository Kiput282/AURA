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
