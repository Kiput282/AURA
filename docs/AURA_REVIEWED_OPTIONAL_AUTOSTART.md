# AURA Reviewed Optional Autostart

- Version: `v1.1.5`
- Sprint: `255`
- Boundary: `reviewed_optional_autostart`
- Contract: `216/216`
- Secure dimensions: `18`
- Unit type: systemd user service
- Unit name: `aura-local.service`
- Target path: `~/.config/systemd/user/aura-local.service`

## Scope

Sprint 255 produces a deterministic, reviewable user-unit contract and
activation/rollback previews. It does not install or activate autostart.

## Unit contract

The preview includes:

- canonical foreground runtime argv from `ManualStartStopStatusRuntimeExecutor`;
- `WorkingDirectory` set to the AURA project root;
- `Restart=on-failure`;
- five-second restart delay;
- 120-second start-limit window with a burst limit of three;
- `UMask=0077`;
- `NoNewPrivileges=true`;
- `WantedBy=default.target`.

## Host posture

The review reads the user systemd manager, target-unit state, and current linger
value without mutating any of them. A linger value of `no` means boot before
interactive login is not ready; Sprint 255 does not change it.

## Approval boundary

Future activation requires the explicit confirmation token:

`ENABLE_AURA_AUTOSTART`

Activation remains a separate reviewed operation. The default is not to write,
reload, enable, start, or change linger.

## Rollback preview

Rollback includes disable-and-stop, removing the exact user unit, user-manager
daemon reload, and reset-failed. Sprint 255 previews but does not execute these
steps.

## Disabled boundaries

- no unit write or installation;
- no `systemctl --user daemon-reload`;
- no enable or start;
- no linger mutation;
- no system-level unit;
- no non-loopback binding;
- no automatic activation.

Next boundary: `persistent_local_chat_session_activation`.

## Sprint 256 successor

Sprint 256 activates hardened persistent local chat sessions independently of
autostart. No systemd unit is installed or activated.

Next boundary: `local_model_service_discovery_health`.
