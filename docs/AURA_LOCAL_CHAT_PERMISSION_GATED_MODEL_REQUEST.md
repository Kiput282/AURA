# AURA Local Chat Permission-Gated Model Request

Sprint: 166  
Version: v0.166.0-genesis

This sprint adds a permission-gated model request dry-run layer for AURA Local Chat.

It does not call a model provider. Instead, it creates a permission preview packet, a model request envelope, and a blocked gate decision proving that real model dispatch requires explicit future approval.

## Safe alpha command

```bash
python3 main.py local-chat-permission-model-dry-run "Aura boleh pakai model?"
```

## Runtime boundary

Enabled in Sprint 166:

- Thin runtime alpha.
- Permission preview packet creation.
- Model request envelope dry-run creation.
- Gate decision preview.
- Safe explanation when model dispatch is blocked.

Still disabled:

- Real model request dispatch.
- Model response runtime.
- Local LLM process start.
- Remote API calls.
- Network requests.
- Credential reads.
- Permission grant mutation.
- Memory writes.
- Audit writes.
- Command execution.
- Arbitrary file mutation.
- Desktop action.

## Next sprint

Sprint 167 should add the Chat Safety + Uncertainty Layer before any real model provider is allowed.
