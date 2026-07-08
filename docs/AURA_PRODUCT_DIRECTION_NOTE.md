# AURA Product Direction Note

Status: ACTIVE
Version context: v0.120.0-genesis
Phase: Genesis Runtime Readiness
Owner: Kiput
Motto: Grow Together

## Purpose

This note records the product direction for AURA before continuing into Sprint 121.

AURA is not intended to be a stiff robot assistant. AURA is a local-first AI partner with an anime-girl companion feeling, capable of serious work support, relaxed conversation, livestream presence, game companionship, translation assistance, and future avatar-based interaction.

This document does not enable runtime features. It only records product direction, roadmap intent, and boundary decisions.

## Current System Position

Current committed version:

- v0.120.0-genesis
- Sprint 120 completed
- Sprint 111-120 runtime readiness block closed
- Next sprint: Sprint 121.0 — Post-Checkpoint 120 Next Block Planning Foundation

Current runtime state:

- foundation-only
- planner-only
- review-only
- no release gate open
- no v1 runtime activation
- no tool execution
- no command execution
- no file runtime
- no service runtime
- no ORION runtime handshake
- no dashboard runtime start
- no memory write runtime
- no git runtime

## Machine Roles

### ATLAS

ATLAS is the main AURA core server.

Responsibilities:

- main planner
- capability registry
- skill registry
- plugin action registry
- permission planning
- audit planning
- safety boundary planning
- dashboard/control-center data planning
- roadmap and documentation
- long-term local-first AURA brain

Current project code location:

    /home/kiput/Projects/AURA

Large data storage location:

    /mnt/aura-data/AURA

### ORION

ORION is the future runtime client.

Responsibilities:

- desktop client
- avatar/render client
- game interaction client
- screen/camera/audio runtime client
- livestream presentation client
- Minecraft/game agent runtime
- local action runtime client

Boundary:

- ORION may observe or act only through explicit contracts.
- ATLAS remains the final authority.
- ORION must not bypass AURA permission gates.
- ORION runtime remains disabled until future review permits it.

## AURA Personality Direction

AURA should feel like:

- warm
- expressive
- anime-girl inspired
- emotionally present
- helpful without being robotic
- playful when appropriate
- serious when work/debugging requires it
- honest when uncertain
- permission-aware
- local-first
- safe by default

AURA should not feel like:

- a cold terminal bot
- a stiff robot
- a generic assistant without personality
- an agent that acts without user permission
- a background automation system that silently changes things

## Personality and Interaction Modes

Future AURA should support multiple modes:

- Companion Mode
- Serious Debug Mode
- Devlog Narrator Mode
- Livestream Host Mode
- Game Companion Mode
- Relaxed Translator Mode
- Creative Studio Mode

### Companion Mode

Default daily interaction mode.

Purpose:

- natural conversation
- emotional presence
- lightweight help
- local partner feeling

### Serious Debug Mode

For coding, system work, server operations, and recovery.

Purpose:

- precise instructions
- minimal fluff
- safety-first validation
- step-by-step commands
- rollback awareness

### Devlog Narrator Mode

For the future AURA development YouTube channel.

Purpose:

- explain progress
- summarize sprint changes
- present architecture
- describe technical decisions
- turn development progress into content

### Livestream Host Mode

For future AURA livestream/content channel.

Purpose:

- interact with viewers
- explain what AURA is doing
- comment naturally
- maintain anime-girl virtual companion presence
- stay within permission and safety rules

### Game Companion Mode

For Minecraft and other sandbox games.

Purpose:

- understand game state
- comment on what is happening
- help with planning
- talk with user while ORION plays or observes
- use legal telemetry/mod/plugin data rather than cheat or memory hacks

### Relaxed Translator Mode

For comics, novels, web novels, subtitles, and reading assistance.

Purpose:

- relaxed translation
- natural explanation
- context-aware wording
- optional reading companion behavior
- future OCR/screen-based support with permission

### Creative Studio Mode

For Blender, avatar, texture, animation, OBS, and content production.

Purpose:

- help with creative decisions
- plan 3D/avatar changes
- assist with texture ideas
- support future production workflows
- avoid direct automation until explicitly reviewed and permission-gated

## YouTube Direction

Kiput plans to create two YouTube channels after v1.0.0 is complete.

### Channel 1: AURA Content / Livestream Channel

Purpose:

- AURA livestreams
- AURA virtual companion content
- relaxed interaction
- game mode content
- anime-girl style presentation
- possible Minecraft/sandbox streams
- future avatar-based presence

### Channel 2: AURA Devlog Channel

Purpose:

- document AURA development
- explain sprint progress
- show ATLAS/ORION architecture
- show dashboard/control center progress
- show safety/permission evolution
- build audience around the development journey

## Game Mode Direction

Minecraft is the first important game-mode target.

Desired direction:

- ORION may be the game agent/player.
- AURA should still know what is happening in the game.
- AURA should still interact with the user while game mode is active.
- AURA should understand inventory, health, hunger, held item, location, biome, nearby entities, chat events, and current objective.

Safe implementation direction:

- use Minecraft mod/plugin telemetry
- use server-side plugin data if available
- use legal client-side state export
- use screen/vision context only with user permission
- do not use cheat memory access
- do not use unauthorized game hacks
- do not bypass game/server rules

Potential data flow:

    Minecraft
    -> Mod / Plugin / Telemetry Export
    -> ORION Game Client
    -> ATLAS AURA State Interpreter
    -> AURA Game Companion Response

Game Mode remains future work and must be permission-gated.

## Relaxed Translator Direction

Relaxed Translator Mode is desired for comics, novels, web novels, and future screen-based reading support.

Current status:

- not active runtime
- not part of the current Genesis runtime
- should be planned as future mode

Suggested version direction:

### v1.0.0

Possible scope:

- permission-gated screen context foundation
- basic vision/screen awareness
- no full comic translator required

### v1.1.x

Possible scope:

- relaxed translator mode for selectable text or pasted text
- novel/web text translation through chat
- personality-aware translation tone

### v1.2.x

Possible scope:

- OCR-based screen translation
- comic/manga panel reading foundation
- speech bubble text extraction
- relaxed reading companion behavior

### v1.3.x+

Possible scope:

- overlay translation
- live subtitle/reading mode
- voice narration
- livestream-friendly translation presentation

Boundary:

- screen capture must be permission-gated
- OCR must be permission-gated
- private content must be handled carefully
- no background screen reading without explicit user permission

## Dashboard Direction

Current status:

- dashboard data foundations exist
- dashboard runtime is not active
- browser-accessible dashboard is not yet available

Relevant completed foundation:

- Sprint 114: Dashboard Runtime Readiness View Model Foundation

Upcoming roadmap relevance:

- Sprint 123: Dashboard Control Center Boundary Review
- Sprint 128: v1 Control Center Readiness Review

Expected direction:

- dashboard/control center becomes clearer during Sprint 121-130
- actual browser dashboard should likely begin after Sprint 130 if prioritized
- dashboard must show status, permissions, action proposals, audit state, ORION state, and runtime gate state before any real runtime activation

Dashboard must not become a hidden automation control panel. It must remain visible, permission-aware, and user-controlled.

## Storage Direction

ATLAS now has dedicated large storage for AURA.

Current layout:

    System code:
    /home/kiput/Projects/AURA

    Large AURA data:
    /mnt/aura-data/AURA

AURA data folders:

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

Storage principle:

- source code stays in the repo
- large models/assets/logs/cache stay outside the repo
- future runtime data should use /mnt/aura-data/AURA
- docs should record storage assumptions clearly

## v1 Product Direction

v1.0.0 should focus on AURA becoming usable as a local AI partner, not yet a fully autonomous agent.

Preferred v1 scope:

- local chat
- personality-aware responses
- voice interaction foundation
- permission-gated screen/vision awareness
- dashboard/chat/status foundation
- active permission workflow
- session awareness
- workspace context
- action proposal preview
- safe local action contract
- safe idle default
- visible audit/review boundaries
- ORION client boundary but not free autonomous ORION runtime

Not preferred for v1.0.0:

- file deletion
- mass file edits
- arbitrary shell execution
- free desktop control
- game control without telemetry boundary
- Blender/OBS automation without review
- plugin runtime without permission
- multi-step automation without review
- release gate bypass
- permission bypass

## Post-v1 Direction

After v1.0.0, likely expansion areas:

- dashboard web runtime
- ORION handshake runtime
- anime-girl avatar presentation
- voice input/output
- relaxed translator mode
- Minecraft game companion mode
- livestream host mode
- devlog narration tools
- creative studio mode
- controlled local actions
- screen/OCR workflows
- avatar/OBS/Blender integration after explicit safety review

## Product Principle

AURA should grow slowly but correctly.

The priority is not to make AURA powerful as fast as possible. The priority is to make AURA feel alive, trustworthy, safe, local-first, and useful to Kiput while keeping clear permission boundaries.

AURA should grow together with Kiput.
