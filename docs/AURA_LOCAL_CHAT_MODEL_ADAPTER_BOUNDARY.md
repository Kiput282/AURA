# AURA Local Chat Model Adapter Boundary

Sprint 165 introduces the Model Adapter Boundary for local chat.

This is not a live model integration. It is a dry-run boundary that defines how
AURA will eventually package prompts, select provider metadata, request
permission, handle credentials, receive responses, and fail safely.

## Enabled in this sprint

- dry-run adapter packet creation
- prompt envelope metadata
- provider candidate metadata
- permission handoff contract for Sprint 166
- explicit zero counters for model/network/credential runtime

## Disabled in this sprint

- model request dispatch
- model response receive
- local LLM process start
- remote API call
- network request
- credential or API key read
- memory write
- command execution
- arbitrary file mutation
- desktop control

## Safe test command

```bash
python3 main.py local-chat-model-adapter-dry-run "Aura coba model adapter"
```

Expected result: one adapter dry-run packet is created while model requests,
network requests, credential reads, commands, file writes, and runtime execution
remain zero.
