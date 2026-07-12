# AURA Voice, Vision, and Chat Context Fusion

## Checkpoint

- Version: `v0.224.0-genesis`
- Sprint: 224
- Block: Sprint 221-230 Unified Partner Runtime Integration
- Runtime state: contract-only
- Next sprint: 225
- Next boundary: `personality_consistency_runtime`

## Purpose

Sprint 224 defines the bounded contract used to represent voice, vision, and
chat/session context as one coherent partner-runtime surface without activating
any modality runtime.

The implementation provides:

- `VoiceVisionChatContextFusionPlanner`
- `VoiceVisionChatContextFusionAlphaManager`

Locations:

    aura/partner_runtime/voice_vision_chat_context_fusion_planner.py
    aura/partner_runtime/voice_vision_chat_context_fusion_alpha_manager.py

## Canonical owners

Sprint 224 does not replace existing domain owners.

Voice owner:

    aura.voice.voice_runtime_planner.VoiceRuntimePlanner

Vision owner:

    aura.vision.vision_runtime_planner.VisionRuntimePlanner

Chat-chain owner:

    aura.partner_runtime.chat_to_memory_runtime_handoff_planner.ChatToMemoryRuntimeHandoffPlanner

Canonical session owner:

    aura_browser_chat_session_runtime

## Owner baselines

The fusion contract requires:

- Voice Runtime: 507 assertions, zero failures
- Vision Runtime: 330 assertions, zero failures
- Sprint 223 chat/session chain: 65 assertions, zero failures

All owner runtimes remain inactive.

## Fusion order

The declared contract order is:

1. chat/session anchor
2. voice contract metadata
3. vision contract metadata

This order preserves the browser chat session runtime as the canonical identity
and continuity anchor.

## Metadata-only boundary

Voice contributes only:

- contract readiness
- stabilization readiness
- transcript-to-chat handoff readiness
- chat-response-to-TTS handoff readiness
- runtime-inactive and permission-boundary metadata

Vision contributes only:

- contract readiness
- stabilization readiness
- vision-to-chat handoff readiness
- screenshot and chat-packet inactivity metadata
- runtime-inactive and redaction-boundary metadata

Chat contributes only:

- Sprint 223 contract readiness
- canonical session ownership
- current and next partner-runtime boundaries
- default-deny and persistence-inactive metadata

## Payload boundary

Sprint 224 does not include or read:

- raw audio
- recorded audio
- transcript payloads
- raw images
- screenshot payloads
- camera frames
- OCR output
- chat message payloads
- browser session payloads

## Runtime boundary

Sprint 224 does not:

- activate microphone capture
- record audio
- perform speech-to-text
- synthesize or play speech
- capture the screen
- take screenshots
- access a camera
- read image files
- perform OCR
- create a live fusion packet
- infer meaning across modalities
- call a model
- write memory
- mutate permissions
- write audit records
- access the network
- execute commands or tools
- mutate files
- start a background service
- open a release gate
- perform autonomous action

## Commands

The following read-only commands are available:

    partner-runtime-voice-vision-chat-context-fusion-status
    partner-runtime-voice-vision-chat-context-fusion-context
    partner-runtime-voice-vision-chat-context-fusion-check

CLI and shell routes expose identical deterministic packets.

## Validation contract

The Sprint 224 planner validates 84 assertions.

Required properties include:

- Sprint 224 current boundary
- Sprint 225 next boundary
- canonical owners preserved
- owner assertion baselines preserved
- all owner runtimes inactive
- no modality payload included
- no fusion packet created
- no context inference performed
- no mutation or execution authority
- all safety blockers inactive

## Next boundary

Sprint 225 — Personality Consistency Runtime

Canonical boundary identifier:

    personality_consistency_runtime
