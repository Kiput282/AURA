# AURA Control Center Runtime Foundation

Version: v0.151.0-genesis  
Sprint: 151.0  
Status: foundation-only, planner-only, metadata-only, read-only, review-only

## Purpose

Sprint 151 opens the Sprint 151-160 Control Center Runtime block. It prepares
AURA's future local Control Center dashboard with a conservative runtime shell
contract and read-only metadata surfaces.

This sprint defines:

- Control Center runtime shell contract
- localhost-only entry boundary
- read-only panel manifest
- route blueprints
- data-source contracts
- permission/audit links
- safe-idle and error boundaries
- security review boundaries
- next-panel readiness for Sprint 152
- no-Control-Center-runtime-activation review

## Runtime boundary

This sprint does not start a Control Center server, dashboard frontend, backend
API, HTTP listener, socket, route mount, status poller, data-source reader,
panel renderer, or service runtime. It does not bind ports, serve dashboard
requests, mutate permissions, write audit events, execute service controls,
modify files, execute commands, or enable runtime execution features.

## Safety invariant

Runtime execution features remain `0`. Release gate remains closed. Public
network exposure remains disabled. The future Control Center must start from a
localhost-only, read-only, safe-idle default and require explicit Creator
approval before any runtime activation.

## Next sprint

Sprint 152 — Control Center Read-Only Status Panel Foundation.
