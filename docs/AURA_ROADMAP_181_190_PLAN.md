# AURA Roadmap 181-190 — Voice Foundation Runtime

This block follows Sprint 180 Memory Runtime Stabilization.

## Sprint Plan

- Sprint 181 — Voice Runtime Foundation
- Sprint 182 — Push-to-Talk and Explicit Listen Boundary
- Sprint 183 — Speech-to-Text Adapter Boundary
- Sprint 184 — Voice Intent Understanding Runtime
- Sprint 185 — Voice Output and TTS Adapter Boundary
- Sprint 186 — Voice Permission and Safety Boundary
- Sprint 187 — Voice Audit Link
- Sprint 188 — Control Center Voice Integration
- Sprint 189 — Voice Runtime Integration Review
- Sprint 190 — Voice Runtime Stabilization

## Guardrails

Voice interaction remains local-first and explicit-listen by default. No always-listening mode, voice-triggered command execution, microphone capture, STT/TTS process start, network model call, or voice-driven action may activate without the required permission, safety, audit, and runtime gates.

## Sprint 181 — Voice Runtime Foundation

Status: planned after Sprint 180.

Sprint 181 should define the local voice session envelope, explicit listen state, input/output adapter boundaries, permission and audit handoff, Control Center status contract, and safe-idle behavior while keeping microphone capture, STT/TTS execution, voice command execution, network, credentials, arbitrary file access, and runtime execution disabled.
