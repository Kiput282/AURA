# AURA Local Chat Runtime Foundation

Sprint 161 starts the Sprint 161-170 Local Chat Runtime block.

This sprint records the safe foundation for local chat sessions, message schema,
chat loop boundaries, persona response boundaries, history boundaries,
permission/audit links, model adapter boundaries, and the Sprint 162 CLI alpha
handoff.

## Product direction

After v0.160.0-genesis, AURA moves from blueprint-only work toward a safe thin
runtime. The agreed product order is:

1. Sprint 161-170: Local Chat Runtime
2. Sprint 171-180: Memory Runtime
3. Sprint 181-190: Local Interaction Runtime Activation
4. Sprint 191-200: Voice Interaction Runtime
5. Sprint 201-210: Vision and Screen Awareness Runtime
6. Sprint 211-220: Permission, Audit, and Safe Local Actions
7. Sprint 221-230: Unified Partner Runtime Integration
8. Sprint 231-240: Genesis Final Integration and Release

## Runtime boundary

Sprint 161 does not create chat sessions at runtime, accept live chat messages,
persist chat history, dispatch model requests, write memory, mutate permissions,
write audit logs, execute commands, mutate files, control desktop applications,
start voice or vision runtime, start a web server, mount routes, bind ports, or
perform autonomous actions.

## Validation targets

- `local-chat-runtime-foundation-status`
- `local-chat-session-contract-plan`
- `local-chat-message-schema-plan`
- `local-chat-loop-boundary-plan`
- `aura-persona-response-boundary-plan`
- `local-chat-history-boundary-plan`
- `local-chat-permission-audit-link-plan`
- `local-chat-model-adapter-boundary-plan`
- `local-chat-cli-alpha-readiness-plan`
- `no-local-chat-runtime-activation-plan`
- `local-chat-next-sprint-readiness-plan`

## Sprint 162 handoff

Sprint 162 may introduce a safe Local Chat CLI Session Alpha. That future alpha
should be explicit, local-only, manually initiated, and should not execute
commands, mutate files, call a model without permission, or perform autonomous
actions.
