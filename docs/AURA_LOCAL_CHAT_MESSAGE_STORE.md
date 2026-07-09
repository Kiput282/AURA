# AURA Sprint 163 — Local Chat Message Store

Sprint 163 adds the first controlled local chat message store for AURA. It can
accept one manual CLI message, create a transient session packet, return a safe
local AURA persona response, and append a JSONL turn record to an AURA-owned
local store.

Example:

```bash
python3 main.py local-chat-store-alpha "Aura simpan pesan ini"
```

Default store path:

```text
.aura_runtime/local_chat/messages.jsonl
```

The store can be redirected for testing:

```bash
AURA_LOCAL_CHAT_STORE_DIR=/tmp/aura_chat_store python3 main.py local-chat-store-alpha "test"
```

Sprint 163 only allows a controlled message-store write. It does not dispatch
model requests, write memory runtime, mutate permissions, write audit logs,
execute commands/tools/plugin actions, launch apps, create folders, mutate
arbitrary files, start servers, bind ports, use voice, capture screens, or
perform autonomous actions.

Sprint 164 should add the AURA Persona Response Layer.
