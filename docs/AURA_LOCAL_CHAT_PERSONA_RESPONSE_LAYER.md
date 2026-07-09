# AURA Local Chat Persona Response Layer

Sprint 164 adds a deterministic local AURA persona response layer for the safe local chat alpha path.

## What is enabled

- one manual CLI message
- deterministic AURA persona response
- persona mode classification
- honest capability boundary response
- controlled JSONL message store append

## What remains disabled

- model runtime
- memory runtime
- command execution
- arbitrary file mutation
- plugin action execution
- desktop control
- voice runtime
- vision runtime
- public network access
- autonomous actions

## Example

```bash
python3 main.py local-chat-persona-alpha "Aura siapa kamu?"
```

Sprint 165 should add the Model Adapter Boundary without automatically dispatching model requests.
