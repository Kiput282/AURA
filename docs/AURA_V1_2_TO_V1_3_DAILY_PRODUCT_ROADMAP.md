# AURA v1.2 to v1.3 Daily Product Roadmap

Canonical block: `daily_chat_control_center_productization`

- Start: Sprint 261
- End: Sprint 270
- Anchor: `v1.2.0`
- Current roadmap checkpoint: `v1.2.1`
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
