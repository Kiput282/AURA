# AURA Session and Memory Persistence Checks

Version: `v1.0.4-genesis`

Sprint: `244`

Boundary: `session_memory_persistence_checks`

Next sprint: `245`

Next boundary: `log_rotation_storage_cleanup`

## Purpose

Sprint 244 adds a centralized, deterministic, read-only integrity
view across AURA's canonical persisted stores. It validates existing
data without repairing, migrating, rewriting, truncating, or deleting
records.

## Canonical Store Catalog

1. Browser sessions: `data/chat_sessions/*.json`
2. Chat history: `data/conversations/chat_history.jsonl`
3. Memory: `data/memory/memories.jsonl`
4. Project journal: `data/journal/aura_journal.jsonl`

## Validation Coverage

The validator checks canonical paths, containment, regular-file and
symlink boundaries, file size, permissions, UTF-8 and JSON decoding,
exact schemas, timestamps, record counts, unique identifiers, browser
message sequencing, browser-session integrity digests, and absence of
leftover temporary session files.

Canonical validation contains `81` base checks. The Sprint 244 contract
contains `92` assertions, including deterministic status and in-memory
negative fixtures for malformed JSON, schema mismatch, duplicate IDs,
and browser-session integrity tampering.

## Observed Guarantees

Browser-session persistence uses bounded files, integrity digests,
thread-level locking, temporary files, file `fsync`, atomic replacement,
directory `fsync`, private mode `0600`, and symlink rejection.

The JSONL conversation, memory, and journal stores currently use direct
append or rewrite behavior. Sprint 244 does not claim atomic replacement,
`fsync`, thread locking, cross-process locking, integrity digests, or
automatic repair for those stores.

## Safety Boundary

All Sprint 244 commands are read-only:

- `session-memory-persistence-status`
- `session-memory-persistence-context`
- `session-memory-persistence-check`

The checkpoint does not write, repair, migrate, truncate, delete, or
normalize canonical data. It does not activate services, bind sockets,
mutate memory or journal data, start systemd units, or change runtime
execution capabilities.
