"use strict";

const BACKEND_ENDPOINT = "/api/control-center";
const REFRESH_INTERVAL_MS = 5000;

const shellState = {
  payload: null,
  capabilityQuery: "",
  refreshTimer: null,
  activeController: null,
};

function byId(id) {
  return document.getElementById(id);
}

function all(selector) {
  return Array.from(document.querySelectorAll(selector));
}

function setText(binding, value) {
  all(`[data-bind="${binding}"]`).forEach((node) => {
    node.textContent = value ?? "—";
  });
}

function readableBoolean(value) {
  return value === true ? "Yes" : value === false ? "No" : "Unknown";
}

function readableState(value) {
  return String(value ?? "unknown").replaceAll("_", " ");
}

function formatNumber(value) {
  const number = Number(value);
  return Number.isFinite(number)
    ? new Intl.NumberFormat().format(number)
    : "—";
}

function formatBytes(value) {
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0) {
    return "—";
  }
  if (number < 1024) {
    return `${number} B`;
  }
  if (number < 1024 * 1024) {
    return `${(number / 1024).toFixed(1)} KiB`;
  }
  return `${(number / (1024 * 1024)).toFixed(1)} MiB`;
}

function formatUptime(value) {
  const seconds = Math.max(0, Number(value) || 0);
  if (seconds < 60) {
    return `${seconds.toFixed(1)} seconds`;
  }
  if (seconds < 3600) {
    return `${Math.floor(seconds / 60)} minutes`;
  }
  return `${Math.floor(seconds / 3600)} hours`;
}

function setBadge(node, label, state) {
  if (!node) {
    return;
  }
  node.textContent = label;
  node.dataset.state = state;
  node.classList.remove(
    "status-good",
    "status-warn",
    "status-bad",
    "status-neutral",
  );

  if (state === "ok" || state === "running" || state === "ready") {
    node.classList.add("status-good");
  } else if (
    state === "degraded"
    || state === "warning"
    || state === "stopped"
    || state === "not_activated"
  ) {
    node.classList.add("status-warn");
  } else if (state === "error" || state === "failed") {
    node.classList.add("status-bad");
  } else {
    node.classList.add("status-neutral");
  }
}

function setPanelBadge(binding, status) {
  all(`[data-bind="${binding}"]`).forEach((node) => {
    setBadge(node, readableState(status), String(status ?? "unknown"));
  });
}

function renderOverview(panel, payload) {
  setText("identity-name", panel.identity?.name ?? "AURA");
  setText("identity-version", panel.identity?.version ?? "unknown");
  setText("identity-codename", panel.identity?.codename ?? "—");
  setText("identity-creator", panel.identity?.creator ?? "—");
  setText("boot-health", panel.core_boot_ready ? "Ready" : "Degraded");
  setText("service-state", readableState(panel.service_state));
  setText(
    "capability-summary",
    `${formatNumber(panel.online_capabilities)} / `
      + `${formatNumber(panel.capability_total)} online`,
  );
  setText(
    "plugin-summary",
    `${formatNumber(panel.plugin_available_count)} / `
      + `${formatNumber(panel.plugin_expected_count)} available`,
  );
  setText(
    "memory-summary",
    panel.memory_available
      ? readableState(panel.memory_status)
      : "Unavailable",
  );
  setText(
    "runtime-features",
    formatNumber(panel.runtime_execution_features),
  );
  setText("safe-idle", readableBoolean(panel.safe_idle));
  setText(
    "last-updated",
    new Date(payload.generated_at_utc).toLocaleString(),
  );
  setPanelBadge("overview-status", panel.status);

  const runtimeState = byId("runtime-state");
  const runtimeLabel = payload.degraded
    ? "Degraded"
    : panel.service_state === "running"
      ? "Running · Read only"
      : `${readableState(panel.service_state)} · Read only`;
  setBadge(
    runtimeState,
    runtimeLabel,
    payload.degraded ? "degraded" : panel.service_state,
  );
}

function renderService(panel) {
  setText("service-detail-state", readableState(panel.state));
  setText(
    "service-listener",
    panel.listener_active ? "Active" : "Inactive",
  );
  setText(
    "service-binding",
    panel.bound_host && panel.bound_port
      ? `${panel.bound_host}:${panel.bound_port}`
      : "Not bound",
  );
  setText("service-uptime", formatUptime(panel.uptime_seconds));
  setText("service-transitions", formatNumber(panel.transition_count));
  setText("service-last-stop", panel.last_stop_reason ?? "—");
  setPanelBadge("service-panel-status", panel.status);
}

function capabilitySearchText(card) {
  return [
    card.id,
    card.name,
    card.state,
    card.runtime_level,
    card.risk_level,
    card.permission_required,
    card.category,
    card.description,
  ]
    .join(" ")
    .toLowerCase();
}

function renderCapabilities(panel) {
  const list = byId("capability-list");
  const template = byId("capability-card-template");
  if (!list || !(template instanceof HTMLTemplateElement)) {
    return;
  }

  const query = shellState.capabilityQuery.trim().toLowerCase();
  const cards = Array.isArray(panel.cards) ? panel.cards : [];
  const filtered = query
    ? cards.filter((card) => capabilitySearchText(card).includes(query))
    : cards;

  list.replaceChildren();
  const fragment = document.createDocumentFragment();

  filtered.forEach((card) => {
    const clone = template.content.cloneNode(true);
    clone.querySelector(".capability-category").textContent =
      readableState(card.category);
    clone.querySelector(".capability-name").textContent =
      card.name || card.id || "Unnamed capability";
    clone.querySelector(".capability-description").textContent =
      card.description || "No description.";
    clone.querySelector(".capability-runtime").textContent =
      readableState(card.runtime_level);
    clone.querySelector(".capability-risk").textContent =
      readableState(card.risk_level);
    clone.querySelector(".capability-permission").textContent =
      readableState(card.permission_required);

    const stateNode = clone.querySelector(".capability-state");
    setBadge(stateNode, readableState(card.state), card.state);

    fragment.append(clone);
  });

  list.append(fragment);
  setText(
    "capability-count",
    `${formatNumber(filtered.length)} shown`,
  );

  if (filtered.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No capabilities match the local filter.";
    list.append(empty);
  }
}

function renderPlugins(panel) {
  const list = byId("plugin-list");
  if (!list) {
    return;
  }

  list.replaceChildren();
  const items = Array.isArray(panel.items) ? panel.items : [];

  items.forEach((item) => {
    const row = document.createElement("article");
    row.className = "item-row";

    const copy = document.createElement("div");
    const title = document.createElement("p");
    const detail = document.createElement("small");
    title.textContent = item.name || item.id || "Plugin";
    detail.textContent = item.module || "Local built-in module";
    copy.append(title, detail);

    const state = document.createElement("span");
    setBadge(
      state,
      item.available ? "Available" : "Unavailable",
      item.available ? "ok" : "degraded",
    );

    row.append(copy, state);
    list.append(row);
  });

  setPanelBadge("plugin-panel-status", panel.status);
}

function renderPermissions(panel) {
  setText(
    "permission-gated-count",
    formatNumber(panel.permission_gated_capability_count),
  );
  setText(
    "pending-runtime",
    readableBoolean(panel.pending_request_runtime_active),
  );
  setText(
    "decision-runtime",
    readableBoolean(panel.decision_runtime_active),
  );
  setText(
    "grant-runtime",
    readableBoolean(panel.grant_runtime_active),
  );
  setPanelBadge("permission-panel-status", panel.status);

  const list = byId("permission-count-list");
  if (!list) {
    return;
  }
  list.replaceChildren();

  Object.entries(panel.declared_permission_counts ?? {})
    .sort(([left], [right]) => left.localeCompare(right))
    .forEach(([name, count]) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = `${readableState(name)}: ${formatNumber(count)}`;
      list.append(tag);
    });
}

function renderAudit(panel) {
  setText("audit-writer", readableBoolean(panel.runtime_writer_active));
  setText("audit-persistence", readableBoolean(panel.persistence_active));
  setText("audit-fetch", readableBoolean(panel.runtime_event_fetch_active));
  setText("audit-event-count", formatNumber(panel.runtime_event_count));
  setPanelBadge("audit-panel-status", panel.status);

  const list = byId("audit-event-list");
  if (!list) {
    return;
  }
  list.replaceChildren();

  const events = Array.isArray(panel.events) ? panel.events : [];
  if (events.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent =
      "No runtime audit writer or persisted event stream is active.";
    list.append(empty);
    return;
  }

  events.forEach((event) => {
    const row = document.createElement("article");
    row.className = "item-row";
    const label = document.createElement("p");
    label.textContent = event.label || event.type || "Audit event";
    row.append(label);
    list.append(row);
  });
}

function renderMemory(panel) {
  setText("memory-available", readableBoolean(panel.available));
  setText(
    "memory-records",
    `${formatNumber(panel.valid_record_count)} valid / `
      + `${formatNumber(panel.record_count)} total`,
  );
  setText("memory-invalid", formatNumber(panel.invalid_record_count));
  setText("memory-size", formatBytes(panel.size_bytes));
  setText("memory-path", panel.storage_path ?? "—");
  setText("memory-mutation", readableBoolean(panel.mutation_performed));
  setPanelBadge("memory-panel-status", panel.status);
}

function renderSurfaceList(elementId, surfaces, readyMode) {
  const list = byId(elementId);
  if (!list) {
    return;
  }
  list.replaceChildren();

  Object.entries(surfaces ?? {}).forEach(([name, value]) => {
    const row = document.createElement("article");
    row.className = "item-row";

    const label = document.createElement("p");
    label.textContent = readableState(name);

    const state = document.createElement("span");
    const enabled = value === true;
    const stateLabel = readyMode
      ? enabled ? "Ready" : "Not ready"
      : enabled ? "Enabled" : "Blocked";
    const stateKind = readyMode
      ? enabled ? "ok" : "degraded"
      : enabled ? "warning" : "ok";
    setBadge(state, stateLabel, stateKind);

    row.append(label, state);
    list.append(row);
  });
}

function renderReadiness(panel) {
  setPanelBadge("readiness-panel-status", panel.status);
  setText("next-sprint", panel.next_sprint ?? "—");
  renderSurfaceList(
    "ready-surface-list",
    panel.ready_surfaces,
    true,
  );
  renderSurfaceList(
    "blocked-surface-list",
    panel.blocked_surfaces,
    false,
  );
}

function renderDashboard(payload) {
  if (
    !payload
    || payload.read_only !== true
    || payload.mutation_allowed !== false
    || payload.panel_count !== 8
    || !payload.panels
  ) {
    throw new Error("Invalid Control Center backend payload.");
  }

  shellState.payload = payload;

  renderOverview(payload.panels.overview, payload);
  renderService(payload.panels.service);
  renderCapabilities(payload.panels.capabilities);
  renderPlugins(payload.panels.plugins);
  renderPermissions(payload.panels.permissions);
  renderAudit(payload.panels.audit);
  renderMemory(payload.panels.memory);
  renderReadiness(payload.panels.readiness);

  setText(
    "connection-detail",
    `Connected to ${BACKEND_ENDPOINT} · `
      + `${payload.route_count} backend routes · read only`,
  );

  const message = byId("shell-message");
  if (message) {
    message.textContent = payload.degraded
      ? `Backend degraded: ${payload.error_count} visible error(s).`
      : "Local backend connected. All dashboard requests are read-only.";
    message.classList.toggle("status-bad", payload.degraded === true);
  }
}

function renderConnectionError(error) {
  const runtimeState = byId("runtime-state");
  setBadge(runtimeState, "Backend unavailable", "error");

  const message = byId("shell-message");
  if (message) {
    message.textContent =
      `Could not read the local backend: ${error.message}`;
    message.classList.add("status-bad");
  }

  setText("connection-detail", "Backend unavailable");
}

async function loadDashboard({ announce = false } = {}) {
  const refreshButton = byId("refresh-data");
  if (refreshButton) {
    refreshButton.disabled = true;
  }

  if (shellState.activeController) {
    shellState.activeController.abort();
  }
  shellState.activeController = new AbortController();

  try {
    const response = await fetch(BACKEND_ENDPOINT, {
      method: "GET",
      cache: "no-store",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
      },
      signal: shellState.activeController.signal,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    renderDashboard(payload);

    if (announce) {
      const message = byId("shell-message");
      if (message && payload.degraded !== true) {
        message.textContent = "Dashboard data refreshed.";
      }
    }
  } catch (error) {
    if (error.name !== "AbortError") {
      renderConnectionError(error);
    }
  } finally {
    if (refreshButton) {
      refreshButton.disabled = false;
    }
  }
}

function scheduleRefresh() {
  window.clearInterval(shellState.refreshTimer);
  shellState.refreshTimer = window.setInterval(() => {
    if (document.visibilityState === "visible") {
      loadDashboard();
    }
  }, REFRESH_INTERVAL_MS);
}

function updateActiveNavigation() {
  const panelIds = [
    "overview",
    "service",
    "capabilities",
    "plugins",
    "permissions",
    "audit",
    "memory",
    "readiness",
  ];
  const current = window.location.hash.slice(1);
  const active = panelIds.includes(current) ? current : "overview";

  all("[data-panel-link]").forEach((link) => {
    if (link.dataset.panelLink === active) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function installEventHandlers() {
  byId("refresh-data")?.addEventListener("click", () => {
    loadDashboard({ announce: true });
  });

  byId("capability-search")?.addEventListener("input", (event) => {
    shellState.capabilityQuery = event.currentTarget.value;
    const capabilityPanel = shellState.payload?.panels?.capabilities;
    if (capabilityPanel) {
      renderCapabilities(capabilityPanel);
    }
  });

  window.addEventListener("hashchange", updateActiveNavigation);

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
      loadDashboard();
    }
  });
}

function startControlCenter() {
  installEventHandlers();
  updateActiveNavigation();
  loadDashboard();
  scheduleRefresh();
}

document.addEventListener("DOMContentLoaded", startControlCenter);
