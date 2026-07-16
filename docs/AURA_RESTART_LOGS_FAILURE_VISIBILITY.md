# AURA Restart, Logs, and Failure Visibility

## Canonical metadata

- Version: `v1.1.3`
- Sprint: `253`
- Boundary: `restart_logs_failure_visibility`
- Contract: `168/168`
- Secure dimensions: `14`
- Runtime mode: `permission_gated_alpha_runtime`
- Canonical process owner: `ManualStartStopStatusRuntimeExecutor`

## Purpose

Sprint 253 extends the operational local runtime with three tightly bounded
surfaces:

1. supervised restart;
2. bounded allowlisted log visibility;
3. structured failure visibility.

The implementation does not replace the canonical manual lifecycle owner.
Start, stop, process identity, listener ownership, and health semantics remain
delegated to the Sprint 252 runtime.

## CLI surface

Read-only commands:

- `restart-logs-failure-visibility-status`
- `restart-logs-failure-visibility-context`
- `restart-logs-failure-visibility-check`
- `restart-logs-failure-visibility-review`
- `restart-logs-failure-visibility-logs`
- `restart-logs-failure-visibility-failures`
- `restart-logs-failure-visibility-restart-preview`

Bounded log-tail command:

```bash
python3 main.py restart-logs-failure-visibility-tail \
  --source runtime \
  --lines 40
```

Approved restart command:

```bash
python3 main.py restart-logs-failure-visibility-restart \
  --approve-restart \
  --confirm-localhost
```

Both approval flags are mandatory. Missing, duplicated, or unexpected
arguments are rejected before runtime control is attempted.

## Restart state machine

### Restart from stopped

1. verify that no unowned process or listener exists;
2. acquire the per-user restart coordination lock;
3. delegate fresh start with explicit approval and localhost confirmation;
4. verify owned process identity;
5. verify canonical loopback listener;
6. verify the `/health` contract;
7. return the supervised restart packet.

### Restart from running

1. verify that the visible runtime is owned by the canonical temporary
   ownership record;
2. delegate approved stop;
3. verify safe idle with zero process and listener evidence;
4. wait through the bounded restart gap;
5. delegate fresh approved localhost start;
6. verify a new owned PID, listener, and health packet;
7. return the supervised restart packet.

Unowned runtime evidence is rejected. The restart wrapper does not call
`Popen`, `os.kill`, `os.killpg`, `systemctl`, or shell execution directly.

## Log visibility

Allowed sources:

- active canonical log;
- latest allowlisted rotated canonical log;
- temporary owned runtime log.

Limits:

- maximum requested lines: `200`;
- maximum byte window: `65,536`;
- no arbitrary paths;
- no symlink following;
- no log mutation.

Redaction covers password-like values, token-like values, and bearer
authorization values before content is emitted.

The runtime log may remain available after a clean stop for failure
inspection. Rehearsal cleanup may remove only the known temporary per-user
runtime log after confirming that it is a regular file owned by the current
user, uses restrictive permissions, is not a symlink, and has no open file
holders.

## Failure visibility

Failure packets normalize:

- operation and stage;
- error code and message;
- lifecycle, ownership, listener, and process summary;
- cleanup and rollback status;
- retryability and safe-idle status;
- mutation and execution boundaries.

Important rejected conditions include:

- unowned runtime evidence;
- ownership mismatch;
- failed stop verification;
- failed fresh launch;
- failed listener or health verification;
- unavailable or unsafe log source;
- arbitrary PID or arbitrary path requests.

## Runtime rehearsal

Sprint 253 validated:

- one supervised restart from stopped;
- one supervised restart from running;
- verified PID rotation;
- bounded and redacted tail while running;
- failure visibility while running and stopped;
- bounded and redacted post-stop runtime-log tail;
- safe temporary runtime-log rehearsal cleanup;
- structured `log_source_unavailable` after cleanup;
- final stopped state with zero process and listener residue.

Canonical data remained unchanged. Canonical logs remained append-only.
No systemd unit or autostart entry was created.

## Disabled boundaries

Sprint 253 does not enable:

- systemd mutation;
- autostart mutation;
- non-loopback binding;
- arbitrary PID signaling;
- arbitrary log paths;
- canonical-log mutation;
- permission-store mutation;
- persistent audit writing;
- uncontrolled external command execution.

## Handoff

Next sprint: Sprint 254 — Process Ownership and Service State Persistence.

Next boundary: `process_ownership_service_state_persistence`.

Next version: `v1.1.4`.
