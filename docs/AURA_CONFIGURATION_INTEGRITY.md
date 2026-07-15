# AURA Configuration Integrity

Version: `v1.0.3-genesis`
Sprint: `243`
Status: COMPLETED
Boundary: `configuration_integrity`
Next sprint: `244`
Next boundary: `session_memory_persistence_checks`

## Purpose

Sprint 243 establishes one canonical read-only validator for
`aura/config/settings.yaml` without replacing the existing configuration
consumers or enabling persistent configuration mutation.

## Canonical commands

    configuration-integrity-status
    configuration-integrity-context
    configuration-integrity-check

## Validated boundaries

The validator checks:

- canonical settings path and repository containment;
- regular-file and non-symlink status;
- bounded file size and non-world-writable mode;
- UTF-8 decoding and valid YAML;
- exact current top-level and section schemas;
- AURA and ATLAS identity values;
- safe relative data and log paths;
- local-only Ollama host;
- local-only web host and valid non-privileged port;
- `safe_idle` mode;
- explicit lifecycle confirmation;
- bounded reasoning timeout;
- absence of secret-like keys;
- deterministic repeated validation;
- fail-closed negative fixtures for missing, empty, malformed,
  non-mapping, unsafe-host, confirmation-disabled, traversal, and
  secret-like-key configurations.

## Acceptance baseline

- canonical configuration checks: `50/50`;
- total Sprint 243 assertions: `61/61`;
- failed assertions: `0`;
- configuration-integrity CLI output: pure JSON;
- configuration hash: unchanged;
- memory and journal hashes: unchanged;
- lifecycle listener after validation: absent;
- persistent configuration write: disabled;
- environment mutation: disabled;
- runtime activation: disabled;
- socket binding: disabled;
- systemd mutation: disabled.

## Consumer compatibility

Sprint 243 preserves the current consumer policies:

- local web runtime: fail closed;
- model router: empty-mapping fallback;
- reasoning factory: rule-based fallback;
- system status YAML loader: empty-mapping fallback.

A legacy Sprint 147 `AuraSkill` declaration was migrated to the canonical
skill schema so the builtin skill registry can be built deterministically.
This compatibility repair does not activate service control execution.

## Handoff

Sprint 244 will verify session and memory persistence behavior while
preserving the read-only configuration boundary established here.
