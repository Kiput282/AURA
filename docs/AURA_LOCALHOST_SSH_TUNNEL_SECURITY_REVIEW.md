# AURA Localhost and SSH Tunnel Security Review

Version: `v1.0.8-genesis`
Sprint: `248`
Boundary: `localhost_ssh_tunnel_security_review`
Next sprint: `249`
Next boundary: `permission_expiry_recovery_review`

## Purpose

Sprint 248 provides a deterministic, read-only security posture review for
AURA's localhost Control Center access and the SSH tunnel path used from ORION
to ATLAS.

## Commands

- `localhost-ssh-security-status`
- `localhost-ssh-security-context`
- `localhost-ssh-security-check`
- `localhost-ssh-security-review`

All commands return pure JSON and do not fall through to normal AURA boot.

## Review States

Each dimension reports one of:

- `secure`
- `review`
- `warning`
- `unavailable`

The overall posture is the worst observed dimension. A `review` or `warning`
state is an observational result, not a failed contract assertion.

## Review Dimensions

The contract reviews:

- canonical AURA binding policy;
- AURA listener exposure;
- SSH listener scope;
- visible sshd configuration;
- SSH tunnel policy;
- SSH file permission metadata;
- firewall visibility metadata;
- AURA runtime activation.

## Canonical Local Access

- Expected AURA host: `127.0.0.1`
- Expected AURA port: `8765`
- Expected SSH tunnel destination: `127.0.0.1:8765`
- Public, LAN, wildcard, and external tunnel exposure remain denied by default.

## Source Boundary

The review reads only:

- `aura/config/settings.yaml`;
- `/proc/net/tcp` and `/proc/net/tcp6`;
- readable sshd configuration text;
- filesystem metadata for `~/.ssh`;
- firewall presence metadata;
- process metadata from `/proc`.

It does not read private-key content, credentials, authorized-key contents,
known-host contents, or firewall rules.

## Runtime Boundary

Sprint 248 keeps the following disabled:

- SSH configuration mutation;
- firewall mutation;
- sshd restart;
- service activation;
- socket activation;
- network connection;
- tunnel creation;
- process control;
- credential reading;
- private-key content reading;
- key generation;
- known-host mutation;
- systemd mutation;
- command execution.

## Canonical Validation

- Base checks: `80`
- Assertions: `80`
- Failed assertions: `0`
- Security dimensions: `8`
- Contract mode: `read_only_security_review`
- Review mode: `single_local_posture_snapshot`

The current posture can legitimately be `review` or `warning` while
`alpha_ready` remains true, provided all safety assertions pass.

## Next Boundary

Sprint 249 continues with `permission_expiry_recovery_review`.
