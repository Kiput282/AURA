"use strict";

const ENDPOINTS = Object.freeze({
  status: "/api/visibility/status",
  permissions: "/api/visibility/permissions",
  audit: "/api/visibility/audit",
  recovery: "/api/visibility/recovery",
});

const DISABLED_BOUNDARIES = Object.freeze([
  ["permission_mutation_runtime", "Permission mutation"],
  ["audit_writer_runtime", "Audit writer"],
  ["audit_persistence_runtime", "Audit persistence"],
  ["automatic_recovery_runtime", "Automatic recovery"],
  ["automatic_retry_runtime", "Automatic retry"],
  ["rollback_execution_runtime", "Rollback execution"],
  ["model_download_runtime", "Model download"],
  ["remote_provider_runtime", "Remote provider"],
  ["internet_fallback_runtime", "Internet fallback"],
  ["tool_calling_runtime", "Tool calling"],
  ["action_dispatch_runtime", "Action dispatch"],
  ["command_execution_runtime", "Command execution"],
  ["aura_long_term_memory_write_runtime", "AURA memory writes"],
  ["background_service_runtime", "Background service"],
  ["public_listener_runtime", "Public listener"],
  ["lan_listener_runtime", "LAN listener"],
  ["websocket_runtime", "WebSocket"],
  ["eventsource_runtime", "EventSource"],
  ["autonomous_action_runtime", "Autonomous actions"],
]);

const state = {
  busy: false,
  status: null,
  permissions: null,
  audit: null,
  recovery: null,
};

function byId(id) {
  return document.getElementById(id);
}

function yesNo(value) {
  return value === true ? "Yes" : "No";
}

function makeElement(tag, className, text) {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  if (text !== undefined) {
    node.textContent = String(text);
  }
  return node;
}

function setBusy(value) {
  state.busy = value;
  byId("refresh-visibility").disabled = value;
  byId("visibility-status").textContent =
    value ? "Refreshing" : "Ready";
}

function showError(message) {
  const node = byId("visibility-error");
  node.hidden = false;
  node.textContent = message;
}

function clearError() {
  const node = byId("visibility-error");
  node.hidden = true;
  node.textContent = "";
}

async function fetchJson(path) {
  const response = await fetch(path, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
    credentials: "same-origin",
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(
      payload.detail
      || payload.reason
      || payload.error
      || `HTTP ${response.status}`,
    );
  }
  return payload;
}

function renderStatus() {
  const status = state.status;
  const permission = state.permissions;
  const audit = state.audit;
  const recovery = state.recovery;

  byId("visibility-status").textContent =
    status.visibility_ready ? "Ready" : "Degraded";
  byId("visibility-detail").textContent =
    status.read_only
      ? "Read-only visibility is active."
      : "Unexpected writable state detected.";

  byId("permission-count").textContent =
    String(permission.permission_item_count);
  byId("audit-count").textContent =
    String(audit.event_contract_count);
  byId("recovery-count").textContent =
    String(recovery.case_count);

  const profile = permission.provider_profile;
  byId("provider-configured").textContent =
    yesNo(profile.configured);
  byId("provider-enabled").textContent =
    yesNo(profile.enabled_requested);
  byId("provider-candidate").textContent =
    yesNo(profile.active_candidate);
  byId("provider-raw-values").textContent =
    yesNo(profile.raw_values_exposed);

  const badge = byId("provider-state");
  if (profile.configuration_degraded) {
    badge.textContent = "Degraded";
    badge.dataset.state = "error";
  } else if (profile.active_candidate) {
    badge.textContent = "Enabled profile";
    badge.dataset.state = "ready";
  } else if (profile.configured) {
    badge.textContent = "Configured / disabled";
    badge.dataset.state = "idle";
  } else {
    badge.textContent = "Not configured";
    badge.dataset.state = "idle";
  }
}

function renderPermissions() {
  const list = byId("permission-list");
  list.replaceChildren();

  state.permissions.items.forEach((item) => {
    const card = makeElement("article", "visibility-item");
    const header = makeElement("div", "item-heading");
    header.append(
      makeElement("strong", "", item.label),
      makeElement("span", "item-state", item.state),
    );

    const scope = makeElement(
      "p",
      "item-detail",
      `Scope: ${item.scope}`,
    );
    const confirmation = makeElement(
      "p",
      "item-detail",
      item.confirmation
        ? `Confirmation: ${item.confirmation}`
        : "Confirmation: not available",
    );
    const mutation = makeElement(
      "p",
      "item-detail",
      item.mutable_from_visibility_runtime
        ? "Visibility surface may mutate this permission."
        : "Visibility surface cannot mutate this permission.",
    );

    card.append(header, scope, confirmation, mutation);
    list.append(card);
  });
}

function renderAudit() {
  const list = byId("audit-list");
  list.replaceChildren();

  state.audit.event_contracts.forEach((event) => {
    const card = makeElement("article", "visibility-item");
    const header = makeElement("div", "item-heading");
    header.append(
      makeElement("strong", "", event.event_type),
      makeElement("span", "item-state", event.severity),
    );

    card.append(
      header,
      makeElement(
        "p",
        "item-detail",
        `Category: ${event.category}`,
      ),
      makeElement(
        "p",
        "item-detail",
        event.content_included
          ? "Message content would be included."
          : "Message and response content are excluded.",
      ),
    );
    list.append(card);
  });
}

function renderRecovery() {
  const list = byId("recovery-list");
  list.replaceChildren();

  state.recovery.cases.forEach((item) => {
    const card = makeElement("article", "recovery-card");
    const header = makeElement("div", "item-heading");
    header.append(
      makeElement("strong", "", item.id),
      makeElement("span", "item-state", item.severity),
    );

    card.append(
      header,
      makeElement("p", "item-detail", item.safe_guidance),
      makeElement(
        "p",
        "item-detail",
        item.automatic_action
          ? "Automatic action is active."
          : "Operator action is required.",
      ),
    );
    list.append(card);
  });
}

function renderBoundary() {
  const list = byId("boundary-list");
  list.replaceChildren();

  const safety = state.status.safety_boundary;
  DISABLED_BOUNDARIES.forEach(([key, label]) => {
    const item = makeElement("li", "boundary-item");
    const disabled = safety[key] === false;
    item.append(
      makeElement("span", "", label),
      makeElement(
        "strong",
        disabled ? "boundary-disabled" : "boundary-warning",
        disabled ? "Disabled" : "Review",
      ),
    );
    list.append(item);
  });
}

function renderAll() {
  renderStatus();
  renderPermissions();
  renderAudit();
  renderRecovery();
  renderBoundary();
}

async function refreshVisibility() {
  if (state.busy) {
    return;
  }

  clearError();
  setBusy(true);
  try {
    const [
      status,
      permissions,
      audit,
      recovery,
    ] = await Promise.all([
      fetchJson(ENDPOINTS.status),
      fetchJson(ENDPOINTS.permissions),
      fetchJson(ENDPOINTS.audit),
      fetchJson(ENDPOINTS.recovery),
    ]);

    state.status = status;
    state.permissions = permissions;
    state.audit = audit;
    state.recovery = recovery;
    renderAll();
  } catch (error) {
    byId("visibility-status").textContent = "Degraded";
    showError(
      error instanceof Error
        ? error.message
        : "Visibility refresh failed.",
    );
  } finally {
    setBusy(false);
  }
}

function start() {
  byId("refresh-visibility").addEventListener(
    "click",
    refreshVisibility,
  );
  refreshVisibility();
}

document.addEventListener("DOMContentLoaded", start);
