# AURA Control Center Service Monitor Panel Foundation

Sprint 157 defines the Control Center Service Monitor Panel Foundation.

This is a planner-only, metadata-only, and read-only foundation for the future
local Control Center service monitor. It defines service monitor layout,
service runtime state summaries, process boundary visibility, health signal
cards, restart/recovery status surfaces, security and localhost status,
filtering/grouping, error boundaries, accessibility/security review, and a
no-runtime activation contract.

## Runtime boundary

Sprint 157 does not probe live service processes, read process state, run health
checks, start dashboard servers, mount routes, serve requests, open sockets,
bind ports, start/stop/restart services, execute systemd/shell commands, write
recovery state, or enable runtime execution features.

## Safety posture

- Service monitor panel is read-only.
- Service runtime remains disabled.
- Control Center runtime remains disabled.
- Dashboard runtime remains disabled.
- Public network exposure remains disabled.
- Release gate remains closed.
- Runtime execution features remain 0.

## Next sprint

Sprint 158 should prepare the Control Center Configuration and Port Registry
Viewer Foundation.
