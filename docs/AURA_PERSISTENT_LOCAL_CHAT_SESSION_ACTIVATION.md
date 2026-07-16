# AURA Persistent Local Chat Session Activation

- Version: `v1.1.6`
- Sprint: `256`
- Boundary: `persistent_local_chat_session_activation`
- Contract: `240/240`
- Secure dimensions: `20`
- Canonical owner: `AuraBrowserChatSessionRuntimeManager`
- Session root: `data/chat_sessions`

## Purpose

Sprint 256 activates hardened persistent local chat sessions while preserving
the existing browser-chat schema and saved session content.

## Storage security

- storage directory target mode: `0700`;
- session file target mode: `0600`;
- directory-relative descriptor operations;
- `O_NOFOLLOW` and `O_CLOEXEC`;
- regular-file and UID verification through `fstat`;
- shared/exclusive cross-process `flock`;
- bounded session reads;
- exclusive temporary creation;
- file fsync, atomic replace, and directory fsync;
- symlink and corrupt-record rejection without overwrite.

## Compatibility

Schema `1.0`, session IDs, integrity hashes, optimistic revisions, idempotent
client-message IDs, clear confirmation, and existing browser routes remain
compatible.

## History and memory

History listing is bounded and metadata-only. Exact session loading remains
available through the existing session owner. Chat-to-memory stays behind the
existing explicit permission, privacy, and review gates; no automatic handoff
is introduced.

## Migration boundary

The existing `data/chat_sessions` directory was discovered as owner-correct but
mode `0775`. Implementation does not mutate it. Finalization may change only the
directory mode to `0700` after validating ownership, all session files, JSON,
integrity hashes, and before/after content hashes.

## Disabled boundaries

- no model-service activation;
- no network dependency or fallback;
- no non-loopback binding;
- no automatic memory handoff;
- no session-content logging;
- no systemd mutation;
- no autostart activation.

Next boundary: `local_model_service_discovery_health`.
