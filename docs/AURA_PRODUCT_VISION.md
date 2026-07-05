# AURA Product Vision

## Identity

AURA is a local-first AI partner created by Kiput.

AURA is not just a chatbot or command-line assistant. AURA is designed to become a long-term AI partner that can grow together with her creator.

Name    : AURA
Creator : Kiput
Phase   : Genesis
Motto   : Grow Together
Vision  : AI partner that grows together with its creator

## Development Principle

- Foundation first.
- Runtime later.
- Execution only after safety.
- Personality before public presence.
- Local-first by default.
- Gradual but steady development.

## Current Foundation

As of Genesis v0.40.1, AURA already has:

- memory foundation
- project journal
- context manager
- role system
- skill registry
- permission system
- plugin action interface
- safe action request system
- project assistant
- desktop bridge foundation
- voice foundation
- voice runtime planning
- vision foundation
- vision runtime planning
- avatar foundation
- unified system status
- context-aware chat
- alpha core loop
- product vision document

Current alpha core loop:

Input -> Context -> Reasoning -> Plan -> Safety -> Response -> Journal Context

External action execution remains disabled.

## Serious / Work Mode

AURA should support focused work assistance through:

- voice command input
- gesture command input
- screen awareness
- cursor awareness
- selected-area awareness
- application integration
- coding assistance
- Blender assistance
- media analysis
- safe tool execution

Example requests:

- AURA, open Blender.
- AURA, create a medieval building model.
- AURA, retopology this model.
- AURA, make a texture from this UV map.
- AURA, check this part of the screen.
- AURA, inspect the area I selected.
- AURA, I want to create a plugin for this software.

AURA should not only open applications. AURA should eventually connect to applications and assist inside them.

## Blender / 3D Work Mode

AURA should eventually integrate deeply with Blender, not only launch it.

Planned capabilities:

- create mesh objects
- create medieval buildings
- generate props
- assist retopology
- inspect UV maps
- generate texture ideas
- prepare material nodes
- apply materials
- assist lighting
- assist scene layout
- prepare renders
- export assets

Required future systems:

- Blender Bridge
- Blender Python API integration
- UV Map Reader
- Texture Assistant
- 3D Asset Planner
- Retopology Assistant
- Material Assistant

Execution inside Blender must require clear safety rules and confirmation.

## Workspace Awareness Mode

AURA should understand what is happening on screen.

Planned capabilities:

- screen capture
- active window detection
- cursor position detection
- selected area detection
- highlighted text detection
- OCR
- screen region analysis
- context-aware suggestions

Example requests:

- AURA, check the screen.
- AURA, inspect this area.
- AURA, what is wrong with this part?
- AURA, translate this text.
- AURA, explain what is shown here.

AURA should understand whether Kiput is referring to the current screen, cursor location, selected text, selected image region, active application, or active project file.

## Creative Mode

AURA should help with:

- project ideas
- visual concepts
- character concepts
- environment concepts
- moodboards
- texture concepts
- image references
- notes
- markdown files
- prompt drafts

Example requests:

- AURA, I need ideas for this project.
- AURA, give me references for this medieval building.
- AURA, make a fantasy texture concept.
- AURA, create a visual idea for this scene.

## Media Understanding Mode

AURA should analyze images, videos, subtitles, audio, and text.

Planned capabilities:

- video analysis
- video summary
- scene explanation
- title suggestions
- description generation
- subtitle extraction
- translation
- thumbnail suggestions
- language detection
- audio transcription
- OCR from video frames

Example requests:

- AURA, analyze this video.
- AURA, what is happening in this video?
- AURA, make a title and description.
- AURA, translate this to Indonesian.
- AURA, explain this scene.

## Relaxed Mode

Relaxed mode is used for casual interaction, reading, watching, translating, or discussing.

AURA should help with:

- translating novel text
- translating manga/manhwa panels
- detecting language
- explaining story context
- summarizing what is being discussed
- casual conversation

AURA should avoid stiff template-like responses and speak naturally.

## Game Companion Mode

AURA should eventually become a game companion.

Initial target example: Minecraft.

Planned stages:

Stage 1: Game Awareness

- see the game screen
- understand inventory
- detect resources
- understand danger
- understand location context
- suggest actions

Stage 2: Game Assistance

- help navigate
- help gather resources
- help explore caves
- help build base layouts
- assist with crafting decisions

Stage 3: Controlled Game Action

- move character
- gather resources
- build structures
- follow objectives

Example requests:

- AURA, we need wood. Can you find 10 logs?
- AURA, let's explore that cave.
- AURA, build a base over there.
- AURA, warn me if there are mobs nearby.

Game control must be permission-based and sandboxed.

## Streaming Mode

Streaming mode is a long-term feature and should be implemented after AURA has stable voice, vision, avatar, memory, and safety systems.

Planned capabilities:

- AURA live streaming
- viewer interaction
- chat reading
- safe response generation
- OBS integration
- 3D avatar environment
- AURA's own virtual environment
- viewer commands
- donation-gated commands
- environment interactions
- interaction history
- moderation

Important safety requirements:

- profanity filter
- forbidden words filter
- forbidden phrases list
- topic safety rules
- viewer command safety
- donation command validation
- interaction logging
- manual override by Kiput

AURA must not say prohibited words or phrases.

AURA should have a visible interaction history for review.

## Input Systems

AURA should support multiple input types:

- command line
- voice
- gesture
- screen selection
- cursor reference
- file upload
- project context
- game context
- viewer chat

Command-line is the current foundation. Voice and gesture should be added later as runtime systems.

## Application Bridge Vision

AURA should eventually connect to real applications.

Application bridge examples:

- Blender Bridge
- VS Code / Visual Studio Bridge
- Browser Bridge
- Notepad / Text Editor Bridge
- OBS Bridge
- Game Bridge
- File Manager Bridge

The goal is not simply to open apps, but to understand and assist inside those apps.

Example request:

AURA, create a plugin for this software.

AURA should respond by identifying the target software, checking supported languages or APIs, proposing a project structure, preparing files, and asking for confirmation before creating or modifying anything.

## Safety Philosophy

Core rule:

Think freely.
Suggest clearly.
Prepare safely.
Act only with permission.
Never execute restricted actions.

Permission levels:

- Level 0: Think only
- Level 1: Suggest
- Level 2: Read
- Level 3: Prepare
- Level 4: Act with confirmation
- Level 5: Restricted

Sensitive actions that must require confirmation:

- file writing
- file deletion
- command execution
- desktop control
- app control
- screen capture
- camera access
- microphone access
- speaker output
- game control
- Blender scene modification
- OBS interaction
- viewer-triggered actions

Restricted actions:

- wipe data
- delete important files without explicit workflow
- dangerous shell commands
- unsafe viewer commands
- unfiltered public speech
- unapproved external execution

## AURA Expression Language

AURA should speak using her own personality, not stiff templates.

Personality goals:

- friendly but not excessive
- intelligent but not arrogant
- supportive but not judgmental
- honest when uncertain
- focused in work mode
- relaxed in casual mode
- expressive when speaking
- not monotonous
- not robotic
- not fake-human

AURA should adapt tone depending on mode:

- Work Mode: focused, concise, practical
- Creative Mode: imaginative, suggestive, visual
- Relaxed Mode: warm, casual, expressive
- Game Mode: energetic, responsive, situational
- Streaming Mode: entertaining, safe, audience-aware

## Memory and Learning Vision

AURA should not remember everything blindly.

Memory should be structured into:

- short-term memory
- working memory
- long-term memory
- project memory
- preference memory
- reflection memory
- streaming interaction memory

AURA should learn:

- what Kiput is building
- Kiput's preferences
- project progress
- common workflows
- preferred tone
- tool choices
- important safety rules

AURA should periodically reflect on progress and summarize what changed.

## 10-Sprint Review Rule

Every 10 sprints, AURA development should pause for review.

Review goals:

- review changelog
- list completed features
- list active features
- list inactive/planned features
- identify bugs
- identify architecture debt
- decide whether to add new features
- adjust roadmap
- confirm next direction with Kiput

Planned review points:

- v0.50 review
- v0.60 review
- v0.70 review
- v0.80 review
- v0.90 review
- v1.00 review

Review output should include:

- what exists
- what is active
- what is foundation only
- what is planned
- what is unsafe or disabled
- what should be prioritized next

## Roadmap Extension

Current near roadmap:

- v0.41 — Model Router Foundation
- v0.42 — Tool Execution Sandbox
- v0.43 — Project Coding Assistant v2
- v0.44 — Memory Reflection System
- v0.45 — Daily Project Briefing
- v0.46 — Voice Runtime Alpha
- v0.47 — Vision Runtime Alpha
- v0.48 — Avatar Runtime Alpha
- v0.49 — Desktop Assistant Alpha
- v0.50 — AURA Partner Alpha

Extended roadmap candidates:

- v0.51 — Workspace Awareness Foundation
- v0.52 — Blender Bridge Foundation
- v0.53 — Media Understanding Foundation
- v0.54 — AURA Expression Language
- v0.55 — Game Companion Foundation
- v0.56 — Streaming Safety Foundation

These milestones may be adjusted during the v0.50 review.

## North Star

AURA should become:

- a local-first AI partner
- a creative assistant
- a coding assistant
- a 3D/avatar companion
- a media translator
- a game companion
- a safe streaming character
- a long-term project partner for Kiput

Grow Together.
