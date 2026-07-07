# AURA Permission Request Review Queue Foundation

Status: COMPLETED
Version: v0.94.0-genesis
Sprint: 94.0
Phase: Genesis
Owner: Kiput
Motto: Grow Together

## Purpose

AURA Permission Request Review Queue Foundation prepares the planner-only queue layer for future permission request review.

This sprint does not create runtime permission requests, collect runtime permission requests, persist runtime permission requests, mutate queue state, submit live requests, review live requests, grant permissions, deny permissions, resolve permissions, activate scopes, revoke scopes, or trigger actions.

The purpose is to define request blueprints, queue states, review packet fields, permission scope boundaries, decision proposal contracts, reviewer checklist items, audit visibility fields, and safety policy for future permission review workflows.

## Relationship to ATLAS and ORION

Sprint 94 follows the canonical ATLAS-ORION deployment plan.

ATLAS remains the permission authority, planner, memory, audit center, and policy layer.

ORION or another local agent may become a future executor only after permission runtime is safely implemented and approved.

This sprint only prepares the review queue blueprints. It does not activate ORION, local actions, screen capture, short recording, voice bridge, avatar runtime, Blender bridge, VS Code bridge, OBS bridge, game companion, or plugin runtime.

## Added Module

Package:

- aura/permission_request_review_queue/

Manager:

- AuraPermissionRequestReviewQueueFoundationManager

The manager prepares:

- permission request review queue status
- permission request blueprint plan
- queue state blueprint plan
- review packet field plan
- permission scope boundary plan
- decision proposal contract plan
- reviewer checklist plan
- audit visibility field plan
- permission request safety policy plan
- permission request review queue context
- permission request review queue status packet

## Plan Types

Sprint 94 defines 11 plan types:

1. permission_request_review_queue_status
2. permission_request_blueprint_plan
3. queue_state_blueprint_plan
4. review_packet_field_plan
5. permission_scope_boundary_plan
6. decision_proposal_contract_plan
7. reviewer_checklist_plan
8. audit_visibility_field_plan
9. permission_request_safety_policy_plan
10. permission_request_review_queue_context
11. permission_request_review_queue_status_packet

## Blueprint Counts

Final blueprint counts:

- permission request blueprints: 12
- queue states: 8
- review packet fields: 10
- permission scope boundaries: 8
- decision proposal contracts: 6
- reviewer checklist items: 9
- audit visibility fields: 8
- total review queue blueprints/fields: 61

## Permission Request Blueprints

Sprint 94 reserves future review blueprints for:

- screen capture request
- short recording request
- voice bridge request
- ORION client bridge request
- avatar and 3D environment request
- Blender bridge request
- VS Code project bridge request
- local file action request
- app open request
- OBS and streaming bridge request
- game companion request
- plugin action request

No runtime permission request is created.

## Queue State Blueprints

Sprint 94 reserves future queue states:

- draft
- submitted
- pending_review
- needs_scope
- approved_proposal
- denied_proposal
- expired
- cancelled

These are blueprint states only. They do not mutate live queue state.

## Review Packet Fields

Sprint 94 reserves future review packet fields:

- request_id
- request_type
- source_agent
- target_resource
- requested_scope
- requested_duration
- risk_level
- reason
- expected_effect
- safe_alternative

No runtime request data is collected.

## Permission Scope Boundaries

Sprint 94 reserves future scope boundaries:

- one_time_scope
- session_scope
- workspace_scope
- app_window_scope
- mode_scope
- plugin_scope
- bridge_scope
- emergency_stop_scope

No runtime scope is activated or revoked.

## Decision Proposal Contracts

Sprint 94 reserves future decision proposal contracts:

- allow_once_proposal
- allow_session_proposal
- allow_scoped_proposal
- require_narrower_scope_proposal
- deny_proposal
- expire_or_cancel_proposal

These are proposal contracts only. They do not grant or deny permissions.

## Reviewer Checklist

Sprint 94 reserves future checklist items:

- verify intent
- verify target
- verify scope
- verify duration
- verify risk
- verify safe alternative
- verify audit visibility
- verify revocation
- verify emergency stop

No runtime review action is performed.

## Audit Visibility Fields

Sprint 94 reserves future audit visibility fields:

- review_event_id
- review_state
- review_source
- review_target
- review_scope
- review_risk_level
- review_outcome_proposal
- review_timestamp

No audit event is written or fetched.

## Integration

Sprint 94 integrates with:

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

Sprint 94 adds commands for:

- permission-request-review-queue-status
- permission-request-blueprint-plan
- queue-state-blueprint-plan
- review-packet-field-plan
- permission-scope-boundary-plan
- decision-proposal-contract-plan
- reviewer-checklist-plan
- audit-visibility-field-plan
- permission-request-safety-policy-plan
- permission-request-review-queue-status-packet
- permission-request-review-queue-context

All commands are planner-only, proposal-only, metadata-only, and side-effect-free.

## Safety Boundary

Sprint 94 explicitly keeps disabled:

- permission request queue runtime
- permission request collection runtime
- permission request persistence runtime
- permission request mutation runtime
- permission request submission runtime
- permission request review runtime
- permission resolution runtime
- permission grant runtime
- permission deny runtime
- permission scope activation runtime
- permission scope revocation runtime
- approval runtime
- denial runtime
- session permission runtime
- scoped permission runtime
- plugin permission runtime
- mode permission runtime
- workspace permission runtime
- app permission runtime
- bridge permission runtime
- emergency stop runtime
- ORION client runtime
- ORION client connection
- client pairing runtime
- client heartbeat runtime
- screen capture runtime
- short recording runtime
- voice bridge runtime
- avatar runtime
- 3D environment runtime
- OBS bridge runtime
- game companion runtime
- Blender bridge runtime
- VS Code project bridge runtime
- local action bridge runtime
- runtime action activation
- runtime behavior change
- dashboard render runtime
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
- port binding
- browser launch
- websocket runtime
- chat runtime
- session runtime
- plugin runtime
- service runtime
- launcher runtime
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

- runtime_permission_requests_created: 0
- runtime_permission_requests_collected: 0
- runtime_permission_requests_persisted: 0
- runtime_permission_requests_mutated: 0
- runtime_permission_requests_submitted: 0
- runtime_permission_requests_reviewed: 0
- runtime_permissions_granted: 0
- runtime_permissions_denied: 0
- runtime_permissions_resolved: 0
- runtime_permission_scopes_activated: 0
- runtime_permission_scopes_revoked: 0
- runtime_actions_triggered: 0
- runtime_execution_features: 0

## Result

Sprint 94 prepares AURA for future permission review workflows without enabling actual permission decisions.

The future Control Center can use these blueprints to display safe, reviewable permission requests before any runtime permission system is activated.
