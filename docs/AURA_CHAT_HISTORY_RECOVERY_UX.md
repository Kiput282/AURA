# AURA Chat History Recovery UX

- Version: `v1.2.4`
- Sprint: `264`
- Boundary: `chat_history_recovery_ux`
- Next boundary: `review_first_memory_integration`

## Product Outcome

Sprint 264 provides clear history, failure visibility, retry, and recovery UX
without introducing an automatic repair engine.

## Runtime Ownership

- Session domain:
  `AuraBrowserChatSessionRuntimeManager.recovery_status`
- HTTP adapter:
  `AuraBrowserChatSessionHttpRuntimeManager`
- Browser surface:
  `AuraBrowserChatWebSurfaceManager`
- Contract package:
  `aura/chat_history_recovery_ux/`

## Read-Only Diagnostic Route

`GET /api/chat/recovery` returns:

- readable active and archived session counts;
- structured unreadable-session issues;
- stale-revision, missing-session, archived-session, and corruption guidance;
- explicit declarations that no repair, quarantine, replacement, deletion,
  model invocation, network access, or runtime mutation occurred.

No POST recovery route exists.

## Browser Recovery UX

The inline recovery panel provides:

- integrity failure visibility;
- retry of the read-only diagnostic;
- dismissible guidance;
- stale-revision reload with unsent draft preservation in memory;
- missing-session neutral-state recovery;
- archived-session restore guidance;
- visible safe-idle and original-file-preservation boundaries.

## Safety Boundary

- Corrupt files are not overwritten.
- Corrupt files are not moved to quarantine.
- No automatic repair is attempted.
- No replacement session is created.
- No histories are merged.
- No session is permanently deleted.
- Recovery does not invoke a model.
- Recovery does not open network connections.
- All diagnostics remain localhost-only and read-only.
