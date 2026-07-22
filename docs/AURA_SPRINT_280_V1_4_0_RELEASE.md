# AURA Sprint 280 - v1.4.0 Release

## Status

- Sprint: 280
- Version: v1.4.0
- Release state: live-accepted
- Acceptance contract: AURA-SPRINT-280-LIVE-ACCEPTANCE-v1
- Checkpoint before release patch: 41ce0f48a2862259c13ff14085ffffa016d3f53f

## Accepted cross-host path

The release acceptance used an authenticated SSH localhost tunnel between
ORION and ATLAS. It did not claim or enable an internal public network path.

The accepted path proved:

- six manual browser voice checks;
- authenticated heartbeat continuity;
- watchdog live, stale, and failed transitions;
- no automatic recovery;
- manual emergency stop;
- reviewed recovery rejection and approval;
- exactly one `create_controlled_file` execution;
- required capability `orion.file.create_controlled`;
- exact content SHA-256 verification;
- controlled artifact deletion after verification.

## Regression result

All required ORION foundation, pairing, live-link, action preview, scoped
permission, bounded action, supervision recovery, browser session, and web
regressions passed with zero failed assertions.

## Final state

- AURA service stopped;
- port 8765 closed;
- acceptance server stopped;
- port 18765 closed;
- safe-idle true;
- repository clean before the release patch.

## Safety boundary

v1.4.0 does not enable arbitrary shell execution, unrestricted file access,
unreviewed desktop automation, public network binding, automatic recovery,
or permission bypass.
