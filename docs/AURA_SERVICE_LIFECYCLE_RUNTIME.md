# AURA Service Lifecycle Runtime

Version: v0.182.0-genesis
Sprint: 182 — Service Lifecycle Runtime
Status: COMPLETED — PERMISSION-GATED ALPHA RUNTIME

## Purpose

Sprint 182 wraps the Sprint 181 localhost web listener with a deterministic,
in-memory service lifecycle.

## Lifecycle States

- `stopped`
- `starting`
- `running`
- `stopping`
- `failed`

Normal path:

```text
stopped → starting → running → stopping → stopped
```

Startup failure and rollback path:

```text
stopped → starting → failed → stopped
```

## Commands

```bash
python3 main.py service-lifecycle-status
python3 main.py service-lifecycle-self-test
python3 main.py service-lifecycle-start --confirm-localhost
```

The start command remains foreground-only. Stop it with `Ctrl+C`, `SIGINT`, or
`SIGTERM`.

## Runtime Controls

Enabled:

- explicit start confirmation;
- deterministic state transitions;
- same-process single-listener ownership;
- operating-system port-conflict detection;
- fail-closed startup;
- rollback from startup failure to `stopped`;
- clean programmatic stop;
- clean foreground `SIGINT` and `SIGTERM` shutdown;
- bounded in-memory transition history;
- read-only lifecycle snapshots;
- localhost listener inherited from Sprint 181.

## Validation Evidence

Sprint 182 validation proves:

- no-bind status inspection leaves port `8765` closed;
- 41 lifecycle assertions pass;
- invalid transitions are rejected;
- the normal transition sequence is deterministic;
- a second same-process listener owner is rejected;
- configured-port conflicts fail closed;
- startup failures record a visible error and roll back;
- ownership is released after normal shutdown and failure;
- `SIGTERM` returns exit code `0` and final state `stopped`;
- `SIGINT` returns exit code `0` and final state `stopped`;
- port `8765` is closed after every test;
- Sprint 181 runtime tests remain 21/21;
- normal AURA boot remains `READY`.

## Security Boundary

Still disabled:

- background daemon runtime;
- systemd installation or activation;
- automatic startup;
- persistent PID file;
- persistent lifecycle state;
- remote lifecycle control;
- HTTP lifecycle mutation;
- public, LAN, wildcard, and IPv6-wildcard binding;
- chat and model runtime;
- memory writes and permission mutation;
- audit persistence;
- commands, tools, actions, and arbitrary file access;
- desktop, voice, vision, and autonomous behavior.

## Runtime Feature Count

The runtime execution feature count remains `1`. Sprint 182 controls the same
Sprint 181 localhost listener; it does not introduce a second executor.

## Next Sprint

Sprint 183 — Health and Status API Runtime
