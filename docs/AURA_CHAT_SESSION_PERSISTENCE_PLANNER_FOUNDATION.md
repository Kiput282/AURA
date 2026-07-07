# AURA Chat Session Persistence Planner Foundation

Status: COMPLETED
Version: v0.95.0-genesis
Sprint: 95.0
Phase: Genesis
Owner: Kiput
Motto: Grow Together

## Purpose

AURA Chat Session Persistence Planner Foundation prepares the planner-only persistence layer for future chat and session continuity.

This sprint does not create chat runtime, session runtime, database runtime, file write runtime, file read runtime, memory write runtime, recovery runtime, export runtime, archive runtime, delete runtime, websocket runtime, or API runtime.

The purpose is to define session record blueprints, storage boundaries, retention policies, privacy/redaction rules, session lifecycle states, recovery indexes, export/migration notes, audit visibility fields, and safety policy for future chat/session persistence.

## Added Module

Package:

- aura/chat_session_persistence_planner/

Manager:

- AuraChatSessionPersistencePlannerFoundationManager

The manager prepares:

- chat session persistence planner status
- session record blueprint plan
- storage boundary blueprint plan
- retention policy blueprint plan
- privacy redaction rule plan
- session lifecycle blueprint plan
- recovery index blueprint plan
- export/migration note plan
- chat persistence safety policy plan
- chat session persistence context
- chat session persistence status packet

## Plan Types

Sprint 95 defines 11 plan types:

1. chat_session_persistence_planner_status
2. session_record_blueprint_plan
3. storage_boundary_blueprint_plan
4. retention_policy_blueprint_plan
5. privacy_redaction_rule_plan
6. session_lifecycle_blueprint_plan
7. recovery_index_blueprint_plan
8. export_migration_note_plan
9. chat_persistence_safety_policy_plan
10. chat_session_persistence_context
11. chat_session_persistence_status_packet

## Blueprint Counts

Final blueprint counts:

- session record blueprints: 10
- storage boundary blueprints: 8
- retention policy blueprints: 8
- privacy redaction rules: 8
- session lifecycle blueprints: 8
- recovery index blueprints: 7
- export/migration notes: 6
- audit visibility fields: 8
- total persistence blueprints/fields: 63

## Session Record Blueprints

Sprint 95 reserves future blueprints for:

- session metadata record
- conversation turn record
- message envelope record
- participant state record
- context window snapshot record
- permission reference record
- action proposal reference record
- attachment reference record
- summary checkpoint record
- recovery marker record

No runtime session records are written.

## Storage Boundary Blueprints

Sprint 95 reserves future blueprints for:

- local JSONL storage
- local SQLite storage
- project-scoped storage
- encrypted storage
- index storage
- backup storage
- export storage
- migration storage

No database is opened and no file is written.

## Retention Policy Blueprints

Sprint 95 reserves future blueprints for:

- manual save policy
- session-only policy
- project history policy
- temporary debug policy
- private mode policy
- redacted summary policy
- archive policy
- delete or forget policy

No runtime retention, archive, delete, or forget action is performed.

## Privacy and Redaction Rules

Sprint 95 reserves future rules for:

- secret value redaction
- private path redaction
- personal identity redaction
- attachment metadata redaction
- screen capture redaction
- voice transcript redaction
- permission reason redaction
- plugin payload redaction

No runtime data is redacted.

## Session Lifecycle Blueprints

Sprint 95 reserves future lifecycle states:

- draft_session
- active_session
- paused_session
- summarized_session
- archived_session
- recoverable_session
- deleted_session
- private_session

No runtime session is created, resumed, recovered, archived, or deleted.

## Recovery Index Blueprints

Sprint 95 reserves future index blueprints for:

- session id index
- project index
- time index
- mode index
- permission reference index
- summary checkpoint index
- recovery marker index

No runtime recovery or search index is built.

## Export and Migration Notes

Sprint 95 reserves future notes for:

- JSON export
- Markdown export
- schema versioning
- backup before migration
- migration rollback
- user consent for export

No export or migration is performed.

## Audit Visibility Fields

Sprint 95 reserves future audit fields:

- persistence_event_id
- session_id
- record_type
- storage_boundary
- retention_policy
- redaction_policy
- operation_proposal
- timestamp

No audit event is written or fetched.

## Integration

Sprint 95 integrates with:

- skills registry
- plugin action registry
- system status manager
- CLI
- shell
- documentation
- capability registry
- README
- master roadmap
- roadmap 91–100
- project identity/version metadata

## CLI and Shell Commands

Sprint 95 adds commands for:

- chat-session-persistence-planner-status
- session-record-blueprint-plan
- storage-boundary-blueprint-plan
- retention-policy-blueprint-plan
- privacy-redaction-rule-plan
- session-lifecycle-blueprint-plan
- recovery-index-blueprint-plan
- export-migration-note-plan
- chat-persistence-safety-policy-plan
- chat-session-persistence-status-packet
- chat-session-persistence-context

All commands are planner-only, metadata-only, and side-effect-free.

## Safety Boundary

Sprint 95 explicitly keeps disabled:

- chat persistence runtime
- chat session runtime
- session creation runtime
- session resume runtime
- session recovery runtime
- message persistence runtime
- turn persistence runtime
- context snapshot runtime
- summary checkpoint runtime
- attachment reference runtime
- database runtime
- database connection
- database migration runtime
- JSONL write runtime
- SQLite write runtime
- session file write runtime
- session file read runtime
- session export runtime
- session archive runtime
- session delete runtime
- recovery index runtime
- search index runtime
- privacy redaction runtime
- retention policy runtime
- memory write runtime
- chat runtime
- session runtime
- websocket runtime
- API server runtime
- API route runtime
- API request handling
- API response serving
- HTTP server start
- web server runtime
- local web server start
- frontend runtime
- backend runtime
- route creation runtime
- static file serving runtime
- dashboard render runtime
- port binding
- browser launch
- plugin runtime
- permission grant runtime
- permission deny runtime
- permission resolution runtime
- runtime action activation
- runtime behavior change
- service runtime
- launcher runtime
- ORION client runtime
- client connection
- screen capture runtime
- short recording runtime
- voice bridge runtime
- avatar runtime
- 3D environment runtime
- game companion runtime
- Blender bridge runtime
- VS Code project bridge runtime
- local action bridge runtime
- emergency stop runtime
- file read/write/modify/delete
- command execution
- test execution
- code execution
- dependency install
- package download
- internet search
- network action
- tool execution
- real tool execution
- external action execution
- memory write
- desktop control
- git init/add/commit/push from AURA runtime

## Runtime Counters

Final expected runtime counters:

- runtime_sessions_created: 0
- runtime_sessions_resumed: 0
- runtime_sessions_recovered: 0
- runtime_session_records_written: 0
- runtime_messages_persisted: 0
- runtime_turns_persisted: 0
- runtime_context_snapshots_written: 0
- runtime_summary_checkpoints_written: 0
- runtime_attachment_references_written: 0
- runtime_database_connections_opened: 0
- runtime_database_migrations_run: 0
- runtime_files_written: 0
- runtime_files_read: 0
- runtime_exports_created: 0
- runtime_archives_created: 0
- runtime_deletes_performed: 0
- runtime_recovery_indexes_built: 0
- runtime_search_indexes_built: 0
- runtime_memory_writes: 0
- runtime_execution_features: 0

## Result

Sprint 95 prepares AURA for future chat/session continuity without activating chat runtime or persistence.

The future Control Center and chat bridge can use these blueprints to explain what would be stored, where it would be stored, how it would be retained, how it would be redacted, and how it could later be recovered or exported.
