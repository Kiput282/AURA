# AURA Health and Status API Runtime

Version: v0.183.0-genesis
Sprint: 183 — Health and Status API Runtime
Status: COMPLETED — READ-ONLY ALPHA RUNTIME

## Purpose

Sprint 183 exposes transparent local health and status data through the same
foreground localhost listener introduced in Sprint 181 and controlled by the
Sprint 182 lifecycle runtime.

## Read-Only Routes

```text
/health
/api/status
/api/status/identity
/api/status/plugins
/api/status/capabilities
/api/status/service
/api/status/memory
/api/status/safety
/api/status/errors
```

The root `/` remains a static safe-idle information page.

## Reported Data

The runtime reports:

- AURA identity and version;
- read-only boot prerequisite health without executing normal boot;
- built-in plugin module availability without starting plugins;
- capability registry summary;
- live service state, listener state, transition count, and uptime;
- memory-store availability and JSONL record validity without writes;
- consolidated safety boundaries;
- transparent error and degraded-state information.

## HTTP Contract

Allowed:

- `GET`
- `HEAD`

Blocked with `405`:

- `POST`
- `PUT`
- `PATCH`
- `DELETE`
- `OPTIONS`
- `CONNECT`
- `TRACE`

Host headers outside the localhost allowlist are rejected with `403`.
CORS is not enabled. Responses use no-store and defensive browser headers.

## Validation Evidence

Sprint 183 validation proves:

- aggregator self-test: 59/59 assertions;
- healthy and degraded fixtures are both visible;
- route payload mapping: 9/9;
- live HTTP assertions: 116/116;
- GET routes: 9/9;
- HEAD routes: 9/9;
- live service payload reports `running`;
- POST and OPTIONS mutation attempts are blocked;
- non-local Host headers are blocked;
- identity, settings, and memory fingerprints remain unchanged;
- plugins are not started by status probes;
- memory is not created or mutated by probes;
- SIGTERM and SIGINT stop cleanly;
- port `8765` closes after shutdown;
- Sprint 182 lifecycle regression remains 41/41;
- Sprint 181 direct runtime regression remains 21/21;
- normal AURA boot remains `READY`.

## Security Boundary

Still disabled:

- status mutation routes;
- plugin activation from status probes;
- memory writes from status probes;
- listener start from no-bind probes;
- background daemon runtime;
- systemd and automatic startup;
- persistent PID or lifecycle state;
- remote lifecycle control;
- public, LAN, wildcard, and IPv6-wildcard binding;
- chat and model runtime;
- permission mutation;
- commands, tools, actions, arbitrary file access, and desktop control;
- voice, vision, and autonomous behavior.

## Runtime Feature Count

The runtime execution feature count remains `1`. Sprint 183 exposes data through
the same localhost listener rather than introducing another executor.

## Next Sprint

Sprint 184 — Control Center Backend Runtime
