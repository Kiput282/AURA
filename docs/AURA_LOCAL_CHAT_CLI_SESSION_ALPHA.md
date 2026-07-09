# AURA Sprint 162 — Local Chat CLI Session Alpha

Sprint 162 adds the first safe thin runtime for local chat. AURA can accept one
manual CLI message, create a transient in-memory chat session packet, and return
a deterministic safe persona response.

This alpha intentionally does not persist chat history, dispatch model requests,
write memory, mutate permissions, write audit logs, execute commands/tools,
launch applications, create folders, mutate files, start servers, mount routes,
bind ports, use voice, capture screens, or perform autonomous actions.

Example:

```bash
python3 main.py local-chat-alpha "Aura kamu aktif?"
```

Expected behavior:

- creates a transient session id
- accepts one manual message
- returns a safe AURA response
- shows model runtime disabled
- shows memory runtime disabled
- shows command execution disabled
- shows file mutation disabled
- persists no history
- dispatches no model request

Sprint 163 should add the Local Chat Message Store after this one-turn alpha is
validated.
