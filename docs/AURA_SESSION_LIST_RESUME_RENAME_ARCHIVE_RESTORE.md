# AURA Session List, Resume, Rename, Archive, and Restore

- Version: `v1.2.3`
- Sprint: `263`
- Boundary: `session_list_resume_rename_archive_restore`
- Next boundary: `chat_history_recovery_ux`

## Product Outcome

Sprint 263 turns the persistent browser chat store into a daily-usable
session lifecycle:

1. Active sessions are listed by default.
2. Archived sessions require an explicit archived filter.
3. Resume opens the same session ID and only that session's history.
4. Rename changes only the validated display title.
5. Archive changes status to `archived` without moving or deleting the file.
6. Restore changes status back to `active` without duplication.

## Runtime Ownership

- Session domain:
  `AuraBrowserChatSessionRuntimeManager`
- HTTP adapter:
  `AuraBrowserChatSessionHttpRuntimeManager`
- Browser UI:
  `AuraBrowserChatWebSurfaceManager`
- Contract package:
  `aura/session_list_resume_rename_archive_restore/`

## HTTP Routes

- `GET /api/chat/sessions?state=active`
- `GET /api/chat/sessions?state=archived`
- `GET /api/chat/sessions?state=all`
- `POST /api/chat/sessions/{session_id}/resume`
- `POST /api/chat/sessions/{session_id}/rename`
- `POST /api/chat/sessions/{session_id}/archive`
- `POST /api/chat/sessions/{session_id}/restore`

All POST routes require the existing localhost mutation guard and optimistic
`expected_revision`.

## Safety Boundary

- Session ID is immutable.
- Lifecycle operations do not merge histories.
- Rename does not mutate messages.
- Archive and restore do not delete or move files.
- Archived sessions cannot receive messages, model messages, or clear-history
  mutations until restored.
- Permanent deletion is not available.
- Lifecycle operations do not invoke the model.
- Lifecycle operations do not open network connections.
- Constructors remain safe-idle.
