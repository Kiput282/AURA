# AURA Manual Start, Stop, and Status Runtime

## Canonical identity

- Version: `v1.1.2`
- Sprint: `252`
- Boundary: `manual_start_stop_status_runtime`
- Runtime level: `permission_gated_alpha_runtime`
- Risk level: `high`
- Permission: `user_confirmation`
- Capability state: `online`
- Control Center visibility: enabled

## Purpose

Sprint 252 activates the first supervised operational launcher path for AURA.
It turns the read-only launcher façade from Sprint 251 into an explicit local
runtime that can start, observe, and stop the canonical foreground lifecycle
service without adding a second service manager.

The canonical lifecycle owner remains:

`aura.service_lifecycle_runtime`

The canonical runtime surface remains:

`aura.local_web_runtime_alpha`

The launcher façade remains:

`aura.aura_launcher_service_controls`

## User-facing commands

Read-only commands:

```text
python3 main.py manual-start-stop-status-runtime-status
python3 main.py manual-start-stop-status-runtime-context
python3 main.py manual-start-stop-status-runtime-check
python3 main.py manual-start-stop-status-runtime-review
```

Explicit approved runtime commands:

```text
python3 main.py manual-start-stop-status-runtime-start --approve-start --confirm-localhost
python3 main.py manual-start-stop-status-runtime-stop --approve-stop
```

Start and stop fail closed when their required confirmation flags are absent.

## Runtime ownership model

The executor launches exactly this canonical child command:

```text
<current-venv-python> <project-root>/main.py service-lifecycle-start --confirm-localhost
```

No shell command is used.

The temporary ownership record is stored under `/tmp` for the current user. It
contains the child PID, `/proc` start ticks, exact argument vector, command
digest, working directory, owner UID, bind host, bind port, and creation time.

A process is considered owned only when all of the following match:

1. PID is alive.
2. `/proc` start ticks match the ownership record.
3. Exact argument vector matches the canonical lifecycle command.
4. Working directory matches the AURA project root.
5. UID matches the current user.
6. Command digest matches.
7. Listener inode belongs to the verified process.

A stop request may signal only that verified owned process.

## Start behavior

An approved start:

1. acquires an exclusive per-user lock;
2. confirms there is no unowned AURA process or listener;
3. launches the canonical lifecycle process using the active virtual
   environment interpreter;
4. writes the temporary ownership record atomically;
5. waits within a bounded timeout for the owned loopback listener;
6. probes `http://127.0.0.1:8765/health`;
7. requires HTTP `200`, `status=ok`, `safe_idle=true`, and
   `command_execution=false`;
8. returns a visible status and non-persistent audit preview.

Repeated approved start is idempotent. It does not create a duplicate process.

## Stop behavior

An approved stop:

1. acquires the same exclusive lock;
2. loads the temporary ownership record;
3. revalidates PID identity before sending any signal;
4. sends `SIGTERM` to the verified owned process;
5. waits for process and listener shutdown;
6. may use bounded `SIGKILL` fallback only after ownership is verified again;
7. removes the temporary ownership record only after shutdown is verified;
8. returns the final stopped status and a non-persistent audit preview.

Repeated approved stop is idempotent and sends no signal when already stopped.

## Status behavior

Status is read from local process metadata and the canonical port:

- lifecycle state;
- ownership state;
- safe-idle state;
- strict Python `main.py` process count;
- listener count;
- owned-listener count;
- temporary ownership record validity;
- loopback health result when an owned listener is present.

No remote probe or non-loopback listener is used.

## Rehearsal evidence

The Sprint 252 runtime rehearsal completed successfully:

- approved start result: `started`;
- time to ready: `263 ms`;
- strict process count while running: `1`;
- listener count while running: `1`;
- owned-listener count while running: `1`;
- health result: HTTP `200`, healthy;
- second start result: `already_running`;
- duplicate process created: no;
- approved stop result: `stopped`;
- primary signal: `SIGTERM`;
- time to stopped: `106 ms`;
- `SIGKILL` used: no;
- second stop result: `already_stopped`;
- listener count after stop: `0`;
- strict process count after stop: `0`;
- temporary state, lock, and log artifacts cleaned: yes.

The rehearsal did not mutate canonical data, permission storage, systemd,
autostart configuration, or persistent audit storage.

## Contract and safety evidence

- Contract assertions: `144/144`
- Failed assertions: `0`
- Dimensions: `12`
- Secure dimensions: `12`
- Findings: `0`
- Sprint 251 launcher façade anchor: `120`
- Service lifecycle anchor: `25`
- Genesis Final anchor: `1258`
- Active permission anchor: `3115`

## Capability registry effect

After Sprint 252:

- total capabilities: `133`;
- online capabilities: `131`;
- foundation-only capabilities: `78`;
- planner-only capabilities: `7`;
- permission-gated capabilities: `13`;
- review-only capabilities: `22`;
- planned-future capabilities: `0`;
- disabled-runtime capabilities: `2`;
- runtime execution features: `5`;
- skill registry entries: `158`.

## Explicitly disabled boundaries

Sprint 252 does not enable:

- restart;
- autostart;
- systemd service creation or mutation;
- non-loopback binding;
- remote lifecycle mutation;
- HTTP lifecycle mutation;
- shell execution;
- permission-store mutation;
- persistent audit writing;
- persistent PID storage;
- autonomous background daemon behavior.

## Sprint 253 handoff

Next sprint: Sprint 253 — Restart, Logs, and Failure Visibility.

Next boundary: `restart_logs_failure_visibility`.

Target version: `v1.1.3`.

Sprint 253 may add explicit supervised restart, durable log visibility,
failure-reason surfacing, and recovery evidence. It must retain strict process
ownership, bounded timeouts, loopback-only networking, approval gates, and
fail-closed behavior.

## Sprint 253 activation outcome

Sprint 253 completed the handoff from manual start/stop/status to supervised
restart, bounded log visibility, and structured failure reporting.

The implementation reuses `ManualStartStopStatusRuntimeExecutor` as the
canonical process owner. It does not create a second lifecycle owner and does
not signal unowned processes.

Validated outcomes:

- restart from stopped reached a verified owned running state;
- restart from running stopped the old owned process and launched a new PID;
- loopback listener and health verification succeeded after each start;
- runtime log tail stayed within line and byte limits and applied redaction;
- failure visibility correctly represented both running and stopped states;
- final state was stopped with zero process and listener residue.

Next sprint: Sprint 254 — Process Ownership and Service State Persistence.

Next boundary: `process_ownership_service_state_persistence`.

Next version: `v1.1.4`.

## Sprint 254 persistence outcome

The canonical manual runtime owner now stores service ownership state at
`data/runtime/service_state.json` using schema v2, mode `0600`, parent mode
`0700`, process start ticks, Linux boot ID, UID, exact command, cwd, and
loopback endpoint identity. Status remains read-only and recovery remains
explicit.

Next: Sprint 255 — Reviewed Optional Autostart.
