# AURA Roadmap Reconfirmation after v1.2.0

- Version: `v1.2.1`
- Sprint: `261`
- Boundary: `roadmap_reconfirmation_after_v1_2_0`
- Previous checkpoint: `v1.2.0`
- Next sprint: `262`
- Next boundary: `operational_browser_chat_model_handoff`
- Product block: `daily_chat_control_center_productization`
- Block range: Sprint `261–270`
- Release target: `v1.3.0`

## Product Decision

AURA now has a verified active local runtime and local model chain. The next
product block converts those foundations into a daily-usable browser Control
Center and persistent local chat experience.

Canonical product decisions:

- Primary interface: browser Control Center.
- Primary model route: `companion`.
- Autostart remains disabled by default.
- Memory writes remain review-first.
- Voice activation starts after the v1.3.0 daily-use release.
- Vision activation follows voice stabilization.
- The official ORION client follows localhost dashboard maturity.
- Game Companion activation remains deferred.

## Gap Ownership

The six discovery gaps are assigned without expanding Sprint 261:

- Sprint 262 owns native process-role classification and operational browser
  chat model handoff.
- Sprint 263 owns session rename/archive/restore.
- Sprint 269 owns the reusable release harness and acceptance rehearsal.
- Sprint 270 owns live end-to-end acceptance and v1.3.0 stabilization.

## End-of-Block Acceptance Rule

Every ten-sprint block must finish with a live end-to-end acceptance test before
the next block begins. Contract-only validation is insufficient.

Sprint 270 must:

1. prove real functionality through the browser Control Center;
2. verify user-visible chat and session results;
3. test relevant failure/recovery behavior;
4. stop and restore the runtime to safe-idle;
5. complete before Sprint 271 begins.

This Sprint 261 boundary is read-only. It does not activate runtime, open a
network connection, mutate systemd, enable autostart, or write user memory.
