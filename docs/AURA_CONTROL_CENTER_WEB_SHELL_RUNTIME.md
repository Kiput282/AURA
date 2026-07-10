# AURA Control Center Web Shell Runtime

Version: v0.185.0-genesis
Sprint: 185 — Control Center Web Shell
Status: COMPLETED — READ-ONLY ALPHA RUNTIME

## Purpose

Sprint 185 provides AURA's first usable browser dashboard. It serves local
HTML, CSS, and JavaScript through the same manually confirmed foreground
localhost listener used by Sprints 181-184.

No second listener, background process, external frontend dependency, or
browser auto-launch behavior is introduced.

## Shell Routes

```text
/
/assets/control-center.css
/assets/control-center.js
```

The listener also preserves:

- nine Sprint 183 status routes;
- nine Sprint 184 Control Center backend routes.

Total route surface: twenty-one.

## Dashboard Panels

The shell renders eight read-only panels:

- overview;
- service;
- capabilities;
- plugins;
- permissions;
- audit;
- memory;
- readiness.

The dashboard reads the complete backend payload from:

```text
GET /api/control-center
```

## Browser Behavior

The shell provides:

- responsive desktop, tablet, and mobile layouts;
- skip-link and keyboard focus visibility;
- polite live-status announcements;
- reduced-motion support;
- safe-idle and degraded-state visibility;
- manual read-only refresh;
- automatic read-only refresh every five seconds while visible;
- local capability filtering;
- safe DOM rendering through `textContent` and created elements;
- no `innerHTML`, `eval`, WebSocket, EventSource, or browser storage.

## Security Contract

- binding remains `127.0.0.1:8765`;
- explicit `--confirm-localhost` remains required;
- GET and HEAD are allowed;
- mutation methods are rejected with `405`;
- unknown assets and path traversal are rejected with `404`;
- non-local Host headers are rejected with `403`;
- CORS remains disabled;
- HTML uses a self-only Content Security Policy;
- camera, microphone, geolocation, payment, and USB browser permissions are
  denied by response policy;
- all responses remain `no-store`;
- browser auto-launch remains disabled.

## Validation Evidence

Sprint 185 validation proves:

- static shell self-test: 140/140 assertions;
- three local asset contracts;
- eight panel contracts;
- nine backend read contracts;
- degraded asset fixture visibility;
- responsive and accessibility contracts;
- zero external dependencies;
- zero inline scripts and styles;
- zero mutation controls;
- live HTTP assertions: 232/232;
- shell GET routes: 3/3;
- shell HEAD routes: 3/3;
- JSON GET routes: 18/18;
- JSON HEAD routes: 18/18;
- 116 capability cards after registry activation;
- clean SIGTERM and SIGINT shutdown;
- port `8765` closes after shutdown;
- Sprint 184 backend regression remains 108/108;
- Sprint 183 status regression remains 59/59;
- Sprint 182 lifecycle regression remains 41/41;
- Sprint 181 web regression remains 21/21;
- normal AURA boot remains `READY`.

## Runtime Feature Count

Runtime execution features remain `1` because Sprint 185 serves the dashboard
through the existing Sprint 181 listener and does not add another executor.

## Still Disabled

- browser chat sessions and message submission;
- local model request and response runtime;
- browser auto-launch;
- service start, stop, restart, systemd, and auto-start controls;
- plugin installation, enable, disable, and reload controls;
- permission request decisions, grants, denials, and scope mutation;
- audit writer and persistence;
- memory create, edit, delete, pin, and write operations;
- command, tool, action, arbitrary file, desktop, voice, and vision execution;
- background daemon, public/LAN binding, and autonomous behavior.

## Next Sprint

Sprint 186 — Browser Chat Session Runtime
