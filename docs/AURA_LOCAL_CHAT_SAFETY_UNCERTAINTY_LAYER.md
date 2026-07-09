# AURA Local Chat Safety + Uncertainty Layer

Sprint: 167  
Version: v0.167.0-genesis

This sprint adds a deterministic local chat safety and uncertainty alpha layer.

It evaluates one manual CLI message before any future model request can proceed. It is designed to protect AURA from overclaiming, fake current facts, hidden model calls, hidden network access, command execution, or arbitrary file mutation.

## Safe alpha command

```bash
python3 main.py local-chat-safety-alpha "Aura apakah info ini terbaru?"
```

## Runtime boundary

Enabled in Sprint 167:

- Thin runtime alpha.
- Safety classifier alpha.
- Uncertainty classifier alpha.
- Capability honesty response layer.
- Freshness boundary response.
- Permission-gate handoff preservation from Sprint 166.

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

Sprint 168 should add a read-only Chat History Viewer Contract so AURA can inspect local chat message store structure without adding unsafe mutation paths.
