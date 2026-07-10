# AURA Control Center Backend Runtime

Version: v0.184.0-genesis
Sprint: 184 — Control Center Backend Runtime
Status: COMPLETED — READ-ONLY ALPHA RUNTIME

## Purpose

Sprint 184 converts the earlier Control Center foundations and Sprint 183
health/status data into stable browser-facing backend view models. It uses the
same manually confirmed foreground localhost listener and does not create a
second executor.

## Backend Routes

```text
/api/control-center
/api/control-center/overview
/api/control-center/service
/api/control-center/capabilities
/api/control-center/plugins
/api/control-center/permissions
/api/control-center/audit
/api/control-center/memory
/api/control-center/readiness
```

The nine Sprint 183 status routes remain available. The listener therefore
serves eighteen read-only JSON routes plus the informational root page.

## View-Model Panels

The backend provides eight panels:

- overview;
- service monitor;
- capability viewer;
- plugin viewer;
- declared permission state;
- audit state;
- memory status;
- runtime readiness.

## Runtime Behavior

The backend reports:

- AURA identity and version;
- boot readiness and safe-idle state;
- live service state, binding, transition count, and uptime;
- all capability cards and capability summaries;
- plugin module availability without starting plugins;
- declared permission requirements without accepting or deciding requests;
- audit foundation visibility without a writer or persistence;
- memory availability and record validity without mutation;
- current backend readiness and explicit blockers.

## HTTP Contract

Allowed:

- `GET`
- `HEAD`

Mutation methods are rejected with `405`. Host headers outside the localhost
allowlist are rejected with `403`. CORS remains disabled. Responses use
no-store and defensive browser security headers.

## Validation Evidence

Sprint 184 validation proves:

- backend self-test: 108/108 assertions;
- eight panel contracts;
- nine backend route contracts;
- eight foundation contracts available;
- 115 capability cards after registry activation;
- live HTTP assertions: 210/210;
- nine status GET routes;
- nine backend GET routes;
- eighteen combined HEAD routes;
- overview and service report `running` while the listener is active;
- service and plugin controls remain disabled;
- permission and audit state remain visible and read-only;
- memory mutation remains disabled;
- file fingerprints remain unchanged;
- SIGTERM and SIGINT stop cleanly;
- port `8765` closes after shutdown;
- Sprint 183 regression remains 59/59;
- Sprint 182 regression remains 41/41;
- Sprint 181 regression remains 21/21;
- normal AURA boot remains `READY`.

## Security Boundary

Still disabled:

- Control Center web shell and frontend asset serving;
- automatic browser launch;
- backend mutation routes;
- service start, stop, restart, systemd, and auto-start controls;
- plugin installation, enable, disable, and reload controls;
- permission request decision, grant, deny, and scope mutation;
- audit writer, runtime event fetching, and persistence;
- memory create, edit, delete, pin, and write operations;
- chat and model runtime;
- command, tool, action, file, and desktop execution;
- background service, public/LAN exposure, and autonomous behavior.

## Runtime Feature Count

The runtime execution feature count remains `1` because Sprint 184 reuses the
same localhost listener rather than introducing a second runtime executor.

## Next Sprint

Sprint 185 — Control Center Web Shell
