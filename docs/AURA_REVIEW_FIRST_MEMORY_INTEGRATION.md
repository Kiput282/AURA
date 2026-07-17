# AURA Review-First Memory Integration

## Release

- Version: `v1.2.5`
- Sprint: 265
- Boundary: `review_first_memory_integration`
- Next boundary: `control_center_runtime_ux_consolidation`

## Purpose

Sprint 265 surfaces memory candidates for explicit human review before any future durable write. A candidate can only be created from one user message selected in the active browser chat session.

## Runtime Flow

1. Select one user message.
2. Create a transient in-process candidate.
3. Review or edit content, category, importance, and pin recommendation.
4. Resolve any privacy hold by editing and reviewing the redacted candidate.
5. Approve a future permission-envelope preview, or reject the transient candidate.

## Persistence Boundary

The queue exists only in the current local service process. Restarting the service clears all candidates. Candidate content, edits, queue entries, approval previews, and rejection decisions are not persisted.

## Approval Boundary

Approval does not authorize or execute a memory write. It creates a permission-gated write preview with:

- `write_authorized=false`
- `permission_grant_applied=false`
- `durable_memory_written=false`
- `memory_store_mutated=false`

## Safety Boundary

Disabled in Sprint 265:

- durable memory writes;
- `MemoryStore` construction and mutation;
- candidate or review-queue persistence;
- permission-grant application;
- automatic memory write, merge, or delete;
- cross-session memory import;
- model invocation;
- network access;
- tool, action, or command execution.

Safe idle remains preserved.
