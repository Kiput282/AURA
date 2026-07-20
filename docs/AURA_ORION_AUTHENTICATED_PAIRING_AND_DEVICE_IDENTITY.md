# AURA Authenticated ORION Pairing and Device Identity

## Sprint

Sprint 274 — authenticated pairing and device identity.

## Scope

This runtime establishes an explicit local enrollment workflow between
ATLAS and the future ORION agent. Pairing is performed through CLI data
exchange; Sprint 274 does not bind a listener or open a network
connection.

The enrollment bundle contains a shared secret and is displayed only by
`orion-pairing-begin`. Treat this output as sensitive and transfer it to
ORION through a trusted manual channel.

## State machine

- `unpaired`
- `challenge_issued`
- `paired`
- `revoked`

Valid transitions:

- `unpaired → challenge_issued` through `begin`
- `revoked → challenge_issued` through `begin`
- `challenge_issued → paired` through a valid HMAC proof
- `challenge_issued → unpaired` through cancel or expiry
- `paired → revoked` through explicit revocation

All other transitions fail closed.

## Device identity

ATLAS generates random UUID4-derived identifiers for the ORION device,
pairing, credential, and challenge. Device identity is not inferred
from hostname alone.

## Authentication

- shared secret: 32 bytes from `secrets.token_bytes`
- challenge: 32 bytes from `secrets.token_bytes`
- challenge TTL: 300 seconds
- proof: HMAC-SHA256
- verification: `hmac.compare_digest`
- challenge use: single-use
- replay ledger: bounded to 256 challenge IDs

## Persistence

Default location:

```text
~/.local/state/aura/orion_pairing/
├── pairing_state.json
└── pairing_secret.key
```

Security contract:

- state remains outside the Git repository
- directory mode is `0700`
- state and secret file modes are `0600`
- writes use a temporary sibling, `fsync`, and `os.replace`
- status and inspection never return the shared secret
- orphaned credentials, invalid JSON, insecure modes, and inconsistent
  state fail closed

Set `AURA_ORION_PAIRING_STATE_ROOT` only for an isolated test state
directory outside the repository.

## CLI

```bash
python main.py orion-pairing-status

python main.py orion-pairing-begin \
  --display-name ORION \
  --platform windows

python main.py orion-pairing-complete \
  --pairing-id <pairing-id> \
  --device-id <device-id> \
  --challenge-id <challenge-id> \
  --proof <base64url-hmac-proof>

python main.py orion-pairing-cancel

python main.py orion-pairing-revoke \
  --confirm REVOKE

python main.py orion-pairing-reset \
  --confirm RESET

python main.py orion-pairing-inspect
python main.py orion-pairing-self-test
```

## Deferred boundaries

Sprint 274 does not activate:

- heartbeat, capability negotiation, or live grounding — Sprint 275
- action preview or explicit approval — Sprint 276
- scoped permission, expiry, audit writes, or reviewed memory — Sprint 277
- capture, app, file, or OBS actions — Sprint 278
- watchdog, emergency-stop runtime, recovery, or dialogue evaluation — Sprint 279

The product version remains `v1.3.1`; the pairing component version is
`0.1.0`.
