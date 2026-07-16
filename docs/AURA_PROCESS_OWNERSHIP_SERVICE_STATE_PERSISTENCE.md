# AURA Process Ownership and Service State Persistence

- Version: `v1.1.4`
- Sprint: `254`
- Boundary: `process_ownership_service_state_persistence`
- Contract: `192/192`
- Secure dimensions: `16`
- Canonical owner: `ManualStartStopStatusRuntimeExecutor`
- State authority: `AuraServiceLifecycleRuntimeManager`

## Persistent state

Canonical state location:

`data/runtime/service_state.json`

Schema v2 records PID, process start ticks, Linux boot ID, current UID, exact
command identity, project working directory, loopback host and port, and start
and update timestamps.

## Durability

The persistent store uses:

- parent directory mode `0700`;
- state file mode `0600`;
- same-directory temporary file;
- `O_EXCL`, `O_CLOEXEC`, and `O_NOFOLLOW`;
- regular-file and owner verification through `fstat`;
- file `fsync`;
- atomic replace;
- parent-directory `fsync`.

## Recovery

Status remains read-only. Records are classified as absent, current,
stale-or-changed, previous-boot, or foreign-user. Cleanup and process signaling
are allowed only through explicitly approved start, stop, or restart.

## Disabled boundaries

- no systemd mutation;
- no autostart activation;
- no arbitrary PID signaling;
- no non-loopback binding;
- no automatic stale cleanup;
- no permission-store mutation;
- no persistent audit write from this boundary.

Next boundary: `reviewed_optional_autostart`.


## Final validation target

- target contract `192/192`;
- actual start/status/stop persistence rehearsal;
- Active Permission `3115`, zero violations;
- Genesis Final Release `1258`;
- boot `v1.1.4 READY`;
- final state stopped with no listener, process, or ownership record.

## Sprint 255 successor

Sprint 255 adds only a reviewed optional-autostart contract around the durable
Sprint 254 ownership state. No unit installation or activation is performed.

Next boundary: `persistent_local_chat_session_activation`.
