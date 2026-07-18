# AURA v1.2 to v1.3 Daily Product Roadmap

Canonical block: `daily_chat_control_center_productization`

- Start: Sprint 261
- End: Sprint 270
- Anchor: `v1.2.0`
- Current roadmap checkpoint: `v1.2.4`
- Release target: `v1.3.0`
- Primary interface: browser Control Center
- Primary model route: `companion`
- End-of-block live acceptance: required

## Sprint Sequence

| Sprint | Canonical boundary | Product outcome |
|---:|---|---|
| Sprint 261 | `roadmap_reconfirmation_after_v1_2_0` | Lock product direction, gap ownership, and live acceptance policy. |
| Sprint 262 | `operational_browser_chat_model_handoff` | Make the normal browser chat path use the verified local companion route and add native process-role classification. |
| Sprint 263 | `session_list_resume_rename_archive_restore` | Complete daily session organization and recovery lifecycle. |
| Sprint 264 | `chat_history_recovery_ux` | Provide clear history, failure visibility, retry, and recovery UX. |
| Sprint 265 | `review_first_memory_integration` | Surface memory candidates for explicit review before durable writes. |
| Sprint 266 | `control_center_runtime_ux_consolidation` | Consolidate start, stop, status, logs, model, queue, and chat UX. |
| Sprint 267 | `atlas_resource_monitoring_dashboard` | Add near-real-time ATLAS storage, CPU, RAM, swap, uptime, and process visibility. |
| Sprint 268 | `permission_audit_action_visibility_ux` | Consolidate permission, audit, proposal, approval, action, and recovery visibility. |
| Sprint 269 | `daily_use_acceptance_rehearsal_and_release_harness` | Build reusable release tooling and rehearse the Sprint 270 acceptance path. |
| Sprint 270 | `daily_local_assistant_live_acceptance_stabilization` | Run the live end-to-end acceptance test and release `v1.3.0`. |

## Sprint 270 Live Acceptance

The final acceptance must exercise the real daily-use chain:

```text
ORION browser
→ SSH tunnel
→ Control Center
→ explicit service start
→ persistent chat session
→ health and resource gates
→ companion model route
→ visible response
→ session list/resume/rename/archive/restore
→ review-first memory candidate
→ resource, permission, audit, and action visibility
→ relevant failure/recovery
→ explicit stop
→ safe-idle
```

The acceptance must verify results rather than only command success. Temporary
rehearsal data must be cleaned or explicitly retained according to the test
plan, and the service must finish stopped with zero listener, zero runtime
process, and no stale state record.

## Deferred Work

- Operational voice is planned after `v1.3.0`.
- Operational vision and ORION capture follow voice stabilization.
- Avatar, livestream, and Game Companion features remain outside this block.

## Sprint 262 Completion

Sprint 262 — `operational_browser_chat_model_handoff` completes the canonical
browser-to-`companion` model handoff while retaining explicit confirmation and
the save-only fallback. Native process-role classification replaces the Sprint
260 count allowance removed from active integration validation.

Next: Sprint 263 — `session_list_resume_rename_archive_restore`.

## Sprint 263 Completion

Sprint 263 — `session_list_resume_rename_archive_restore` completes the
daily session organization and recovery lifecycle. The browser now exposes
explicit active and archived lists, same-session resume, validated title-only
rename, non-destructive archive, and non-destructive restore.

Session IDs and message histories remain isolated and immutable during
lifecycle operations. Archive and restore reuse the existing atomic write and
integrity-hash path. Permanent delete, cross-session history merge, lifecycle
model calls, and lifecycle network access remain disabled.

Next: Sprint 264 — `chat_history_recovery_ux`.

## Sprint 264 Completion

Sprint 264 — `chat_history_recovery_ux` provides clear history, failure
visibility, retry, and recovery UX. The session domain exposes a read-only
diagnostic status, the HTTP adapter adds `GET /api/chat/recovery`, and the
browser presents integrity, missing-session, stale-revision, and
archived-session guidance.

Corrupt files are preserved as original evidence. Stale-revision recovery
keeps the unsent draft in process memory while reloading the current session.
No repair, quarantine, replacement, deletion, model call, or network fallback
is performed.

Current: Sprint 265 — `review_first_memory_integration` completed.

Next: Sprint 266 — `control_center_runtime_ux_consolidation`.

### Sprint 266 completion checkpoint

- Version: `v1.2.6`
- Boundary: `control_center_runtime_ux_consolidation`
- Status: complete
- Contract: 480 assertions across 40 dimensions
- Operational owners: 5/5 available, 0 degraded
- UI: six-card Operations panel in the existing Control Center
- Chat remains at `/chat`
- Visibility remains at `/visibility`
- New execution authority: none
- Next: Sprint 267 — `atlas_resource_monitoring_dashboard`

### Sprint 267 completion checkpoint

- Version: `v1.2.7`
- Boundary: `atlas_resource_monitoring_dashboard`
- Status: complete
- Contract: 504 assertions across 42 dimensions
- Runtime self-test: 49 assertions
- Storage mounts: `/`, `/home`, `/mnt/aura-data`
- CPU/RAM rolling windows: 5, 15, and 60 minutes
- UI refresh: one second
- Background sampler: disabled
- History persistence: disabled
- New HTTP route: none
- New execution authority: none
- Next: Sprint 268 — `permission_audit_action_visibility_ux`

### Sprint 268 completion checkpoint

- Version: `v1.2.8`
- Boundary: `permission_audit_action_visibility_ux`
- Status: complete
- Contract: 528 assertions across 44 dimensions
- Runtime self-test: 60 assertions
- Visibility sections: permission, audit, proposal, approval, action,
  recovery
- New HTTP route: none
- Automatic permission grant: disabled
- Automatic recovery: disabled
- New execution authority: none
- Next: Sprint 269 — `daily_use_acceptance_rehearsal_and_release_harness`

### Sprint 269 completion checkpoint

- Version: `v1.2.9`
- Boundary: `daily_use_acceptance_rehearsal_and_release_harness`
- Status: complete
- Contract: 552 assertions across 46 dimensions
- Runtime self-test: 72 assertions
- Rehearsal steps: 9
- Control Center web shell: 190 assertions
- Result persistence: disabled
- Runtime execution: none
- Live E2E: deferred to Sprint 270
- Next: Sprint 270 — `daily_local_assistant_live_acceptance_stabilization`

### Sprint 270 completion checkpoint

- Version: `v1.3.0`
- Boundary: `daily_local_assistant_live_acceptance_stabilization`
- Live E2E: complete
- Real function and usage result: verified
- Bounded failure and canonical recovery: verified
- Final safe-idle: verified
- Memory write delta: none
- Permission grant: none
- Evidence SHA-256: `72dbd6c243d55171b39f1b2a1a659ee654ea7622c31e09c0ea9000a666e29fb1`
- Block 261–270 complete: yes
- Release ready: yes
- Next: Sprint 271 — `voice_daily_use_activation`

Sprint 271 discovery must reconcile the immediate voice boundary with the
existing broader ORION roadmap before implementation. No larger roadmap
rescheduling is implied by this checkpoint.
