"use strict";

const BACKEND_ENDPOINT = "/api/control-center";
const REFRESH_INTERVAL_MS = 5000;
const RESOURCE_REFRESH_INTERVAL_MS = 1000;

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


function operationOwner(operations, ownerId) {
  const owners = operations && operations.owners;
  if (!owners || !owners[ownerId]) {
    return {
      available: false,
      degraded: true,
      status: "unavailable",
      snapshot: {},
    };
  }
  return owners[ownerId];
}

function operationState(owner) {
  if (!owner || owner.available !== true) {
    return "Unavailable";
  }
  if (owner.degraded === true) {
    return "Degraded";
  }
  return readableState(owner.status || "available");
}

function operationCount(value, fallback) {
  return Number.isFinite(Number(value))
    ? formatNumber(Number(value))
    : fallback;
}


// Sprint 267 — ATLAS resource monitoring dashboard
const RESOURCE_WINDOW_MINUTES = [5, 15, 60];
let activeResourceWindowMinutes = 5;
let latestResourcePayload = null;

function resourceNumber(value, fallback = 0) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function resourcePercent(value) {
  return Math.max(0, Math.min(100, resourceNumber(value)));
}

function formatResourcePercent(value) {
  return `${resourcePercent(value).toFixed(1)}%`;
}

function formatResourceBytes(value) {
  const bytes = Math.max(0, resourceNumber(value));
  const units = ["B", "KiB", "MiB", "GiB", "TiB"];
  let unitIndex = 0;
  let amount = bytes;

  while (amount >= 1024 && unitIndex < units.length - 1) {
    amount /= 1024;
    unitIndex += 1;
  }

  const precision = unitIndex === 0 ? 0 : 1;
  return `${amount.toFixed(precision)} ${units[unitIndex]}`;
}

function formatResourceUptime(value) {
  let seconds = Math.max(0, Math.floor(resourceNumber(value)));
  const days = Math.floor(seconds / 86400);
  seconds %= 86400;
  const hours = Math.floor(seconds / 3600);
  seconds %= 3600;
  const minutes = Math.floor(seconds / 60);

  const parts = [];
  if (days > 0) {
    parts.push(`${days}d`);
  }
  if (hours > 0 || days > 0) {
    parts.push(`${hours}h`);
  }
  parts.push(`${minutes}m`);
  return parts.join(" ");
}

function resourceStateLabel(metric) {
  const state = String(metric?.state || "unknown");
  return state.charAt(0).toUpperCase() + state.slice(1);
}

function setResourceState(id, metric) {
  const element = byId(id);
  if (!element) {
    return;
  }

  const color = String(metric?.color || "gray");
  element.textContent = resourceStateLabel(metric);
  element.dataset.resourceState = color;
}

function renderResourceChart(id, series, label) {
  const svg = byId(id);
  if (!svg) {
    return;
  }

  const line = svg.querySelector(".resource-chart-line");
  if (!line) {
    return;
  }

  const values = Array.isArray(series)
    ? series.map((item) => resourcePercent(item?.value_percent))
    : [];

  if (values.length === 0) {
    line.setAttribute("points", "");
    svg.setAttribute("aria-label", `${label}: no samples yet`);
    return;
  }

  const denominator = Math.max(1, values.length - 1);
  const points = values.map((value, index) => {
    const x = (index / denominator) * 100;
    const y = 39 - (value / 100) * 38;
    return `${x.toFixed(3)},${y.toFixed(3)}`;
  });

  line.setAttribute("points", points.join(" "));
  svg.setAttribute(
    "aria-label",
    `${label}: ${values.length} samples; latest `
      + `${values.at(-1).toFixed(1)} percent`,
  );
}

function resourceStatsText(stats) {
  const payload = stats || {};
  return `Min ${formatResourcePercent(payload.minimum)} · `
    + `Avg ${formatResourcePercent(payload.average)} · `
    + `Max ${formatResourcePercent(payload.maximum)}`;
}

function renderResourceStorage(records) {
  const list = byId("resource-storage-list");
  if (!list) {
    return;
  }

  list.replaceChildren();

  const mounts = Array.isArray(records) ? records : [];
  mounts.forEach((record) => {
    const item = document.createElement("li");
    item.className = "resource-storage-item";
    item.dataset.resourceState = String(record?.color || "gray");

    const heading = document.createElement("div");
    heading.className = "resource-storage-heading";

    const mount = document.createElement("strong");
    mount.textContent = String(record?.mount_point || "Unknown mount");

    const state = document.createElement("span");
    state.textContent = resourceStateLabel(record);

    heading.append(mount, state);

    const meter = document.createElement("div");
    meter.className = "resource-storage-meter";
    meter.setAttribute("aria-hidden", "true");

    const fill = document.createElement("span");
    fill.style.width = `${resourcePercent(record?.used_percent)}%`;
    meter.appendChild(fill);

    const detail = document.createElement("p");
    detail.textContent = `${formatResourceBytes(record?.used_bytes)} used · `
      + `${formatResourceBytes(record?.free_bytes)} free · `
      + `${formatResourceBytes(record?.total_bytes)} total · `
      + `${formatResourcePercent(record?.used_percent)}`;

    item.append(heading, meter, detail);
    list.appendChild(item);
  });
}

function updateResourceWindowButtons() {
  all("[data-resource-window]").forEach((button) => {
    const windowMinutes = Number(button.dataset.resourceWindow);
    const isActive = windowMinutes === activeResourceWindowMinutes;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
}

function renderResources(resourcePayload) {
  latestResourcePayload = resourcePayload || null;
  const payload = latestResourcePayload || {};
  const current = payload.current || {};
  const cpu = current.cpu || {};
  const memory = current.memory || {};
  const swap = current.swap || {};
  const uptime = current.uptime || {};
  const processes = current.processes || {};
  const history = payload.history || {};
  const selected = history[String(activeResourceWindowMinutes)] || {};
  const cpuHistory = selected.cpu || {};
  const memoryHistory = selected.memory || {};

  setPanelBadge(
    "resources-status",
    current.overall_state || "unavailable",
  );

  const sampleCount = resourceNumber(selected.sample_count);
  setText(
    "resources-detail",
    `${sampleCount} samples in the ${activeResourceWindowMinutes}-minute `
      + "window. Metrics are sampled on read and remain in-process only.",
  );

  setText(
    "resource-cpu-current",
    formatResourcePercent(cpu.usage_percent),
  );
  setText(
    "resource-cpu-stats",
    resourceStatsText(cpuHistory.stats),
  );
  setResourceState("resource-cpu-state", cpu);

  setText(
    "resource-memory-current",
    formatResourcePercent(memory.used_percent),
  );
  setText(
    "resource-memory-stats",
    resourceStatsText(memoryHistory.stats),
  );
  setResourceState("resource-memory-state", memory);

  setText(
    "resource-swap-current",
    formatResourcePercent(swap.used_percent),
  );
  setText(
    "resource-swap-detail",
    `${formatResourceBytes(swap.used_bytes)} used · `
      + `${formatResourceBytes(swap.free_bytes)} free`,
  );

  setText(
    "resource-uptime-current",
    formatResourceUptime(uptime.seconds),
  );
  setText(
    "resource-process-count",
    `Processes ${operationCount(processes.count, "0")}`,
  );

  renderResourceChart(
    "resource-cpu-chart",
    cpuHistory.series,
    "CPU usage history",
  );
  renderResourceChart(
    "resource-memory-chart",
    memoryHistory.series,
    "RAM usage history",
  );
  renderResourceStorage(current.storage);
  updateResourceWindowButtons();
}

function renderOperations(operations) {
  const payload = operations || {};
  const service = operationOwner(payload, "service");
  const logs = operationOwner(payload, "restart_logs");
  const model = operationOwner(payload, "model_runtime");
  const visibility = operationOwner(payload, "visibility");
  const memory = operationOwner(payload, "memory_review");

  setPanelBadge(
    "operations-status",
    payload.status || "unavailable",
  );

  const available = operationCount(
    payload.available_owner_count,
    "0",
  );
  const total = operationCount(payload.owner_count, "5");
  const degraded = operationCount(
    payload.degraded_owner_count,
    "0",
  );
  setText(
    "operations-detail",
    `${available} of ${total} runtime owners available; `
      + `${degraded} degraded. This dashboard remains read-only.`,
  );

  setText(
    "operation-service-state",
    operationState(service),
  );
  setText(
    "operation-service-detail",
    payload.service_controls
      && payload.service_controls.status_visible === true
      ? "Service status is visible. Existing confirmation and "
        + "safety gates remain authoritative; no action route was added."
      : "Service status is currently unavailable.",
  );

  setText(
    "operation-logs-state",
    operationState(logs),
  );
  setText(
    "operation-logs-detail",
    payload.logs
      && payload.logs.bounded_metadata_only === true
      ? "Failure state and bounded metadata are visible. Raw log "
        + "content, paths, and arbitrary file reads remain hidden."
      : "Bounded logs and failure metadata are unavailable.",
  );

  setText(
    "operation-model-state",
    operationState(model),
  );
  setText(
    "operation-model-detail",
    payload.model_runtime
      && payload.model_runtime.queue_and_budget_visibility === true
      ? "Queue and resource-budget status are visible without "
        + "activating or invoking the model."
      : "Model queue and budget status are unavailable.",
  );

  setText(
    "operation-visibility-state",
    operationState(visibility),
  );
  setText(
    "operation-visibility-detail",
    payload.visibility
      && payload.visibility.permission_read_only === true
      ? "Permission, audit, and recovery information is read-only. "
        + "No grant or recovery execution route is exposed."
      : "Safety visibility is unavailable.",
  );

  const chat = payload.chat || {};
  const chatRoute = chat.workspace_route || "/chat";
  const chatLink = byId("operation-chat-link");
  chatLink.setAttribute("href", chatRoute);
  setText(
    "operation-chat-state",
    chat.available === true ? "Available" : "Unavailable",
  );
  setText(
    "operation-chat-detail",
    chat.embedded === false
      ? "Chat remains a dedicated full workspace and is linked "
        + "from this operational home."
      : "Chat workspace status is unavailable.",
  );

  setText(
    "operation-memory-state",
    operationState(memory),
  );
  setText(
    "operation-memory-detail",
    payload.memory_review
      && payload.memory_review.summary_visible === true
      ? "Review queue summary is visible. Candidates remain "
        + "transient and approval produces a write preview only."
      : "Memory-review summary is unavailable.",
  );

  setText(
    "operation-boundary-actions",
    payload.service_action_routes === false
      && payload.restart_action_routes === false
      ? "No service or restart action routes"
      : "Review service action boundary",
  );
  setText(
    "operation-boundary-model",
    payload.model_activation_route === false
      ? "No implicit model activation"
      : "Review model activation boundary",
  );
  setText(
    "operation-boundary-permission",
    payload.permission_grant_route === false
      && payload.recovery_execution_route === false
      ? "No permission grant or recovery execution"
      : "Review permission and recovery boundary",
  );
  setText(
    "operation-boundary-memory",
    payload.memory_write_route === false
      ? "No durable memory write"
      : "Review memory-write boundary",
  );
}

function renderPermissionAuditActionVisibility(visibilityPayload) {
  const payload = visibilityPayload || {};
  const sections = payload.sections || {};
  const sectionIds = [
    "permission",
    "audit",
    "proposal",
    "approval",
    "action",
    "recovery",
  ];

  setPanelBadge(
    "permission-visibility-status",
    payload.status || "unavailable",
  );

  const available = Number(payload.available_section_count || 0);
  const total = Number(payload.section_count || sectionIds.length);
  setText(
    "permission-visibility-detail",
    `${available} of ${total} visibility sections available. `
      + "All sections remain read-only and safe-idle.",
  );

  sectionIds.forEach((sectionId) => {
    const section = sections[sectionId] || {};
    setText(
      `permission-visibility-${sectionId}-state`,
      readableState(section.state || "unavailable"),
    );
    setText(
      `permission-visibility-${sectionId}-detail`,
      section.detail || "Visibility data unavailable.",
    );
  });

  setText(
    "permission-visibility-boundary-grant",
    payload.automatic_permission_grant === false
      && payload.permission_grant_route === false
      ? "No automatic permission grant"
      : "Review permission-grant boundary",
  );
  setText(
    "permission-visibility-boundary-action",
    payload.service_action_routes === false
      && payload.restart_action_routes === false
      && payload.mutation_routes === false
      ? "No service, restart, or approval action route"
      : "Review action-route boundary",
  );
  setText(
    "permission-visibility-boundary-recovery",
    payload.automatic_recovery === false
      && payload.recovery_execution_route === false
      ? "No automatic recovery or recovery execution"
      : "Review recovery boundary",
  );
  setText(
    "permission-visibility-boundary-mutation",
    payload.read_only === true
      && payload.runtime_mutated === false
      && payload.new_execution_authority === false
      ? "Read-only visibility; no runtime mutation"
      : "Review mutation and execution boundary",
  );
}

function renderDashboard(payload) {
  renderOperations(payload.runtime_ux_consolidation || {});
  renderResources(payload.atlas_resource_monitoring_dashboard || {});
  renderPermissionAuditActionVisibility(
    payload.permission_audit_action_visibility_ux || {},
  );

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
  }, RESOURCE_REFRESH_INTERVAL_MS);
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

  all("[data-resource-window]").forEach((control) => {
    const activateWindow = () => {
      const nextWindow = Number(control.dataset.resourceWindow);
      if (!RESOURCE_WINDOW_MINUTES.includes(nextWindow)) {
        return;
      }
      activeResourceWindowMinutes = nextWindow;
      renderResources(latestResourcePayload);
    };

    control.addEventListener("click", activateWindow);
    control.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }
      event.preventDefault();
      activateWindow();
    });
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
