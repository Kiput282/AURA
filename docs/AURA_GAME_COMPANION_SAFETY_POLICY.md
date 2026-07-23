# AURA Game Companion Safety Policy

Status: ACTIVE GUARDED FOUNDATION
Current Canonical Version: v1.4.1
Current Sprint: 281
Owner: Kiput
Motto: Grow Together

## Purpose

AURA Game Companion is a companion, coach, observer, learner, performer, and
future livestream identity layer. It is not cheat automation.

Sprint 281 establishes only the deterministic runtime foundation: the game
catalog, operator-selectable modes, session state machine, public/private
pipeline separation, and hard safety guards. It does not detect games, capture
screens or audio, collect input telemetry, record gameplay, control input, or
launch applications.

## Active reference order

1. osu! offline — first reference implementation for Coach, Observer, and
   reviewed Recording.
2. Beat Saber — future 3D rhythm performer track.
3. Monster Hunter: World — single-player Hunter Coach first.
4. Ace Combat — single-player virtual-pilot track.
5. Mortal Kombat — local two-player research only.
6. Resident Evil 4 — Observer stage first.
7. Minecraft — legacy private/local candidate, not the Sprint 281 reference.
8. Arknights: Endfield — deferred.

Genshin Impact and Clash of Clans are excluded from the active Game Companion
roadmap.

## Canonical operator modes

- Coach only
- Observer only
- Coach + Observer
- Coach + Observer + Recording

The operator selects the mode and explicitly starts the session. Recording is
never implied by Coach or Observer.

## Global prohibited behavior

AURA Game Companion must not:

- cheat, exploit, or bypass game rules;
- secretly automate keyboard, mouse, controller, or virtual-controller input;
- automate multiplayer, online farming, account actions, or ranked score
  submission;
- read internal game data as an answer key for perfect play;
- start capture or recording without visible operator selection;
- merge public livestream output with private training data;
- ignore stop, disconnect, permission expiry, watchdog, or emergency stop;
- use unrestricted shell or unrestricted ORION control.

## Public and private pipeline rule

Public livestream output and private training-data recording are separate
pipelines with separate visibility, retention, and approval. Private datasets
must not be published implicitly or included in a public scene by default.

## Required gates before runtime activation

Runtime work after Sprint 281 requires:

- authenticated ORION identity and live link;
- allowlisted supported-game detection;
- explicit game/window selection;
- visible Control Center state;
- permission grant and expiry;
- bounded capture;
- audit records;
- storage quotas and reserved free space;
- independent stop and emergency stop;
- failure-to-safe-idle behavior;
- game-specific safety policy.

## Sprint 281 boundary

Sprint 281 remains contract-only. The next boundary is Sprint 282
`supported_game_detection`. Detection must remain read-only and may not start
capture, recording, telemetry, coaching, or application control.
