"use strict";

const API_BASE = "/api/chat";
const MODEL_API_BASE = "/api/model";
const MEMORY_REVIEW_API = `${API_BASE}/memory-review`;
const MEMORY_CATEGORIES = (
  "note preference project_fact instruction "
  + "milestone relationship other"
).split(" ");
const MEMORY_IMPORTANCE_BANDS = (
  "ephemeral normal important critical_review"
).split(" ");
const LOCAL_INTENT = "browser-chat-session";
const MAX_MESSAGE_CHARACTERS = 8192;

const state = {
  sessions: [],
  activeSession: null,
  sessionFilter: "active",
  modelStatus: null,
  busy: false,
  pendingSubmission: null,
  recovery: null,
  recoveryDismissed: false,
  memoryReview: {
    candidates: [],
    pending_review_count: 0,
    privacy_hold_count: 0,
    approved_write_preview_count: 0,
  },
};

function byId(id) {
  return document.getElementById(id);
}

function setStatus(label, kind = "idle") {
  const node = byId("chat-status");
  if (!node) {
    return;
  }
  node.textContent = label;
  node.dataset.state = kind;
}

function selectedMode() {
  return byId("mode-local-model").checked ? "local-model" : "save-only";
}

function modelIsActive() {
  return Boolean(
    state.modelStatus
    && state.modelStatus.active === true
    && state.modelStatus.degraded !== true,
  );
}

function selectedSessionIsActive() {
  return Boolean(
    state.activeSession
    && state.activeSession.status === "active",
  );
}

function updateMessageCount() {
  const input = byId("message-input");
  byId("message-count").textContent =
    `${input.value.length.toLocaleString()} / 8,192`;
}

function updatePendingStatus() {
  const node = byId("pending-status");
  if (!state.pendingSubmission) {
    node.textContent = "No pending retry";
    node.dataset.state = "idle";
    return;
  }
  node.textContent =
    state.pendingSubmission.mode === "local-model"
      ? "Retry preserves model request ID"
      : "Retry preserves client message ID";
  node.dataset.state = "pending";
}

function clearPendingSubmission() {
  state.pendingSubmission = null;
  updatePendingStatus();
}

const RECOVERY_ERROR_CORRUPTION =
  "chat_session_corruption";
const RECOVERY_TARGET_NEUTRAL =
  "neutral_no_session";
const RECOVERY_DRAFT_FLAG =
  "preserve_unsent_draft_in_memory";
const RECOVERY_ACTION_RESTORE =
  "restore_session";

function recoveryGuidanceFrom(error) {
  return error?.payload?.recovery || null;
}

function recoveryKindLabel(kind) {
  const labels = {
    stale_revision: "Session changed",
    missing_session: "Session unavailable",
    archived_session: "Session archived",
    session_corruption: "History integrity failure",
    storage_unavailable: "Storage unavailable",
    session_unreadable: "History unavailable",
  };
  return labels[kind] || "History recovery";
}

function recoveryActionLabel(kind) {
  const labels = {
    stale_revision: "Reload latest session",
    missing_session: "Refresh session list",
    archived_session: "Reload archived session",
    session_corruption: "Retry read-only check",
    storage_unavailable: "Retry read-only check",
    session_unreadable: "Retry read-only check",
  };
  return labels[kind] || "Retry read-only check";
}

function renderRecoveryStatus() {
  const panel = byId("history-recovery-panel");
  const badge = byId("history-recovery-state");
  const title = byId("history-recovery-title");
  const detail = byId("history-recovery-detail");
  const issues = byId("history-recovery-issues");
  const retry = byId("retry-history-recovery");

  if (!state.recovery || state.recoveryDismissed) {
    panel.hidden = true;
    issues.replaceChildren();
    return;
  }

  const degraded =
    state.recovery.degraded === true
    || state.recovery.status === "attention_required";
  if (!degraded) {
    panel.hidden = true;
    issues.replaceChildren();
    return;
  }

  const guidance =
    state.recovery.guidance
    || state.recovery.recovery
    || {};
  const issueList = Array.isArray(state.recovery.issues)
    ? state.recovery.issues
    : [];

  const kind =
    guidance.kind
    || issueList[0]?.code
    || "session_unreadable";

  panel.hidden = false;
  badge.textContent = "Attention";
  badge.dataset.state = "error";
  title.textContent = recoveryKindLabel(kind);
  detail.textContent =
    state.recovery.detail
    || issueList[0]?.detail
    || "A read-only recovery check found a history issue.";
  retry.textContent = recoveryActionLabel(kind);

  issues.replaceChildren();
  issueList.forEach((issue) => {
    const item = document.createElement("li");
    const heading = document.createElement("strong");
    heading.textContent = recoveryKindLabel(
      issue.code || kind,
    );
    const body = document.createElement("span");
    body.textContent =
      issue.detail
      || issue.recommended_action
      || "Review the read-only recovery guidance.";
    item.append(heading, body);
    issues.append(item);
  });
}

function setRecoveryFromError(error) {
  const guidance = recoveryGuidanceFrom(error);
  if (!guidance) {
    return null;
  }

  state.recoveryDismissed = false;
  state.recovery = {
    status: "attention_required",
    degraded: true,
    issue_count: 1,
    detail: error.message,
    source_error: error.payload?.error || "chat_history_error",
    guidance,
    issues: [
      {
        code: guidance.kind || "session_unreadable",
        detail: error.message,
        recommended_action:
          guidance.action || "review_recovery_status",
        retryable: guidance.retryable === true,
        original_file_preserved:
          guidance.original_file_preserved !== false,
      },
    ],
  };
  renderRecoveryStatus();
  return guidance;
}

async function refreshRecoveryStatus({
  showHealthy = false,
} = {}) {
  const payload = await apiRequest(
    `${API_BASE}/recovery`,
  );
  state.recovery = payload;
  if (payload.degraded) {
    state.recoveryDismissed = false;
  } else if (!showHealthy) {
    state.recoveryDismissed = true;
  }
  renderRecoveryStatus();
  return payload;
}

async function handleChatRecoveryError(
  error,
  {
    sessionId = state.activeSession?.session_id || null,
    preservePending = false,
  } = {},
) {
  const guidance = setRecoveryFromError(error);
  if (!guidance) {
    return false;
  }

  const kind = guidance.kind;
  const sourceError =
    error?.payload?.error || "chat_history_error";
  const preserveDraft =
    guidance[RECOVERY_DRAFT_FLAG] === true;
  const neutralTarget =
    guidance.target_state === RECOVERY_TARGET_NEUTRAL;
  const restoreAction =
    guidance.action === RECOVERY_ACTION_RESTORE;

  if (
    kind === "missing_session"
    && neutralTarget
  ) {
    state.activeSession = null;
    clearPendingSubmission();
    renderSessionList();
    renderTranscript();
    syncComposerControls();
    try {
      await refreshSessions({ preserveActive: false });
    } catch (refreshError) {
      setRecoveryFromError(refreshError);
    }
    return true;
  }

  if (
    (
      kind === "stale_revision"
      || (
        kind === "archived_session"
        && restoreAction
      )
    )
    && sessionId
  ) {
    try {
      await loadSession(
        sessionId,
        {
          preservePending:
            preservePending || preserveDraft,
        },
      );
    } catch (reloadError) {
      setRecoveryFromError(reloadError);
    }
    return true;
  }

  if (
    sourceError === RECOVERY_ERROR_CORRUPTION
    || kind === "session_corruption"
    || kind === "storage_unavailable"
    || kind === "session_unreadable"
  ) {
    try {
      await refreshRecoveryStatus();
    } catch (diagnosticError) {
      setStatus(diagnosticError.message, "error");
    }
    return true;
  }

  if (!preservePending) {
    clearPendingSubmission();
  }
  return true;
}

async function retryHistoryRecovery() {
  if (state.busy) {
    return;
  }

  const guidance =
    state.recovery?.guidance
    || state.recovery?.recovery
    || {};
  const kind =
    guidance.kind
    || state.recovery?.issues?.[0]?.code
    || null;
  const sessionId =
    state.activeSession?.session_id || null;

  setBusy(true);
  try {
    if (
      (kind === "stale_revision"
        || kind === "archived_session")
      && sessionId
    ) {
      await loadSession(
        sessionId,
        { preservePending: true },
      );
    } else if (kind === "missing_session") {
      state.activeSession = null;
      clearPendingSubmission();
      await refreshSessions({ preserveActive: false });
    }

    const payload = await refreshRecoveryStatus({
      showHealthy: true,
    });
    if (!payload.degraded) {
      state.recoveryDismissed = true;
      renderRecoveryStatus();
      setStatus("History recovery check is healthy", "ready");
    } else {
      setStatus("History still requires attention", "error");
    }
  } catch (error) {
    setRecoveryFromError(error);
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

function dismissHistoryRecovery() {
  state.recoveryDismissed = true;
  renderRecoveryStatus();
}

function syncSessionFilterControls() {
  const active = state.sessionFilter === "active";
  byId("session-filter-active").setAttribute(
    "aria-pressed",
    String(active),
  );
  byId("session-filter-archived").setAttribute(
    "aria-pressed",
    String(!active),
  );
  byId("session-state-label").textContent =
    active
      ? "Showing active sessions."
      : "Showing archived sessions. Restore returns a session to the active list.";
}

function syncComposerControls() {
  const hasSession = Boolean(state.activeSession);
  const activeSession = selectedSessionIsActive();
  const archivedSession = hasSession && !activeSession;
  const activeModel = modelIsActive();
  const useModel = selectedMode() === "local-model";

  byId("create-session").disabled = state.busy;
  byId("refresh-sessions").disabled = state.busy;
  byId("session-filter-active").disabled = state.busy;
  byId("session-filter-archived").disabled = state.busy;
  byId("refresh-model-status").disabled = state.busy;
  byId("refresh-memory-review").disabled = state.busy;
  byId("memory-source-message").disabled =
    state.busy || !activeSession;
  byId("create-memory-candidate").disabled =
    state.busy
    || !activeSession
    || !Boolean(byId("memory-source-message").value);
  byId("probe-model").disabled =
    state.busy
    || !Boolean(state.modelStatus?.enabled)
    || Boolean(state.modelStatus?.degraded);

  byId("resume-session").disabled =
    state.busy || !hasSession || !activeSession;
  byId("rename-session").disabled = state.busy || !hasSession;
  byId("archive-session").disabled =
    state.busy || !hasSession || !activeSession;
  byId("restore-session").disabled =
    state.busy || !hasSession || !archivedSession;
  byId("clear-session").disabled =
    state.busy || !hasSession || !activeSession;

  byId("message-input").disabled =
    state.busy || !hasSession || !activeSession;
  byId("mode-save-only").disabled =
    state.busy || !hasSession || !activeSession;
  byId("mode-local-model").disabled =
    state.busy || !hasSession || !activeSession || !activeModel;
  byId("confirm-model-request").disabled =
    state.busy
    || !hasSession
    || !activeSession
    || !activeModel
    || !useModel;

  if ((!activeModel || !activeSession) && useModel) {
    byId("mode-save-only").checked = true;
    byId("confirm-model-request").checked = false;
  }

  const effectiveModelMode = selectedMode() === "local-model";
  const confirmationReady =
    !effectiveModelMode || byId("confirm-model-request").checked;
  byId("send-message").disabled =
    state.busy
    || !hasSession
    || !activeSession
    || !byId("message-input").value.trim()
    || !confirmationReady;
  byId("send-message").textContent =
    effectiveModelMode ? "Send to local model" : "Save without model";

  setStatus(
    state.busy
      ? "Working"
      : archivedSession
        ? "Archived"
        : hasSession
          ? "Ready"
          : "Idle",
    state.busy
      ? "busy"
      : archivedSession
        ? "idle"
        : hasSession
          ? "ready"
          : "idle",
  );
}

function setBusy(value) {
  state.busy = value;
  syncSessionFilterControls();
  syncComposerControls();
  renderMemoryReview();
}

async function apiRequest(path, options = {}) {
  const method = options.method || "GET";
  const headers = {
    Accept: "application/json",
    ...(options.headers || {}),
  };
  if (method !== "GET" && method !== "HEAD") {
    headers["Content-Type"] = "application/json";
    headers["X-AURA-Local-Intent"] = LOCAL_INTENT;
  }
  const response = await fetch(path, {
    method,
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
    cache: "no-store",
    credentials: "same-origin",
  });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : { detail: await response.text() };
  if (!response.ok) {
    const error = new Error(
      payload.detail
      || payload.reason
      || payload.error
      || `HTTP ${response.status}`,
    );
    error.status = response.status;
    error.payload = payload;
    throw error;
  }
  return payload;
}


function renderMemorySourceOptions() {
  const select = byId("memory-source-message");
  select.replaceChildren();

  const placeholder = document.createElement("option");
  placeholder.value = "";

  if (
    !state.activeSession
    || !selectedSessionIsActive()
  ) {
    placeholder.textContent =
      "Select an active session first";
    select.append(placeholder);
    return;
  }

  const userMessages = state.activeSession.messages.filter(
    (message) => message.role === "user",
  );
  placeholder.textContent =
    userMessages.length
      ? "Choose one user message"
      : "No user messages are available";
  select.append(placeholder);

  for (const message of userMessages) {
    const option = document.createElement("option");
    option.value = message.message_id;
    const preview = message.content.length > 80
      ? `${message.content.slice(0, 77)}...`
      : message.content;
    option.textContent =
      `#${message.sequence} · ${preview}`;
    select.append(option);
  }
}

function memoryCandidateById(candidateId) {
  return state.memoryReview.candidates.find(
    (candidate) =>
      candidate.candidate_id === candidateId,
  ) || null;
}

function memoryCandidateCard(candidate) {
  const card = document.createElement("article");
  card.className = "memory-candidate-card";
  card.dataset.memoryCandidateId =
    candidate.candidate_id;

  const heading = document.createElement("div");
  heading.className = "memory-candidate-heading";

  const title = document.createElement("strong");
  title.textContent =
    `Message #${candidate.source_sequence}`;

  const stateBadge = document.createElement("span");
  stateBadge.className = "status-badge";
  stateBadge.dataset.state =
    candidate.review_state === "privacy_hold"
      ? "error"
      : candidate.review_state
        === "approved_write_preview"
        ? "ready"
        : "idle";
  stateBadge.textContent = candidate.review_state;

  heading.append(title, stateBadge);

  const metadata = document.createElement("p");
  metadata.className = "memory-candidate-meta";
  metadata.textContent =
    `${candidate.category} · `
    + `${candidate.importance} · `
    + `revision ${candidate.revision} · `
    + `${candidate.candidate_id}`;

  const contentLabel = document.createElement("label");
  contentLabel.textContent = "Candidate content";
  const content = document.createElement("textarea");
  content.className = "memory-candidate-content";
  content.maxLength = 4000;
  content.value = candidate.content;
  contentLabel.append(content);

  const fields = document.createElement("div");
  fields.className = "memory-candidate-fields";

  const categoryLabel = document.createElement("label");
  categoryLabel.textContent = "Category";
  const category = document.createElement("select");
  category.className = "memory-candidate-category";
  for (const value of MEMORY_CATEGORIES) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    option.selected = value === candidate.category;
    category.append(option);
  }
  categoryLabel.append(category);

  const importanceLabel = document.createElement("label");
  importanceLabel.textContent = "Importance";
  const importance = document.createElement("select");
  importance.className = "memory-candidate-importance";
  for (const value of MEMORY_IMPORTANCE_BANDS) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    option.selected = value === candidate.importance;
    importance.append(option);
  }
  importanceLabel.append(importance);

  const pinnedLabel = document.createElement("label");
  pinnedLabel.className = "memory-candidate-pinned";
  const pinned = document.createElement("input");
  pinned.type = "checkbox";
  pinned.className = "memory-candidate-pinned-input";
  pinned.checked = Boolean(candidate.pinned);
  const pinnedText = document.createElement("span");
  pinnedText.textContent = "Recommend pin";
  pinnedLabel.append(pinned, pinnedText);

  fields.append(
    categoryLabel,
    importanceLabel,
    pinnedLabel,
  );

  const privacy = document.createElement("p");
  privacy.className = "memory-candidate-privacy";
  privacy.textContent = candidate.redaction_applied
    ? `Privacy hold · ${candidate.redaction_notes.join(", ")}`
    : "Privacy preview clear for manual review.";

  const actions = document.createElement("div");
  actions.className = "memory-candidate-actions";

  const save = document.createElement("button");
  save.type = "button";
  save.textContent = "Save review edit";
  save.disabled = state.busy;
  save.addEventListener(
    "click",
    () => editMemoryCandidate(candidate.candidate_id),
  );

  const approve = document.createElement("button");
  approve.type = "button";
  approve.textContent = "Approve write preview";
  approve.disabled =
    state.busy
    || candidate.review_state === "privacy_hold";
  approve.addEventListener(
    "click",
    () => approveMemoryCandidatePreview(
      candidate.candidate_id,
    ),
  );

  const reject = document.createElement("button");
  reject.type = "button";
  reject.textContent = "Reject transient candidate";
  reject.disabled = state.busy;
  reject.addEventListener(
    "click",
    () => rejectMemoryCandidate(candidate.candidate_id),
  );

  actions.append(save, approve, reject);

  if (candidate.write_preview) {
    const preview = document.createElement("p");
    preview.className = "memory-write-preview";
    preview.textContent =
      "Permission envelope preview created. "
      + "write_authorized=false · "
      + "permission_grant_applied=false · "
      + "durable_memory_written=false · "
      + "memory_store_mutated=false";
    card.append(
      heading,
      metadata,
      contentLabel,
      fields,
      privacy,
      preview,
      actions,
    );
  } else {
    card.append(
      heading,
      metadata,
      contentLabel,
      fields,
      privacy,
      actions,
    );
  }

  return card;
}

function renderMemoryReview() {
  const payload = state.memoryReview;
  const list = byId("memory-review-list");
  list.replaceChildren();

  const candidates = payload.candidates || [];
  const badge = byId("memory-review-state");
  badge.textContent = candidates.length
    ? `${candidates.length} queued`
    : "Empty";
  badge.dataset.state = candidates.length
    ? "ready"
    : "idle";

  byId("memory-review-detail").textContent =
    candidates.length
      ? (
        `${payload.pending_review_count || 0} pending · `
        + `${payload.privacy_hold_count || 0} privacy hold · `
        + `${payload.approved_write_preview_count || 0} approved preview`
      )
      : (
        "Select one user message, create a local candidate, "
        + "then review it before any future durable write."
      );

  if (!candidates.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent =
      "No transient memory candidates.";
    list.append(empty);
    return;
  }

  for (const candidate of candidates) {
    list.append(memoryCandidateCard(candidate));
  }
}

async function refreshMemoryReview() {
  const payload = await apiRequest(
    `${MEMORY_REVIEW_API}`,
  );
  state.memoryReview = payload;
  renderMemoryReview();
  return payload;
}

async function createMemoryCandidate() {
  if (
    state.busy
    || !state.activeSession
    || !selectedSessionIsActive()
  ) {
    return;
  }

  const messageId =
    byId("memory-source-message").value;
  if (!messageId) {
    setStatus(
      "Select one user message for memory review.",
      "error",
    );
    return;
  }

  setBusy(true);
  try {
    await apiRequest(
      `${MEMORY_REVIEW_API}/candidates`,
      {
        method: "POST",
        body: {
          session_id: state.activeSession.session_id,
          message_id: messageId,
          confirm_memory_candidate: true,
        },
      },
    );
    await refreshMemoryReview();
    setStatus(
      "Transient memory candidate created",
      "ready",
    );
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

function memoryCandidateCardNode(candidateId) {
  return Array.from(
    byId("memory-review-list").children,
  ).find(
    (node) =>
      node.dataset?.memoryCandidateId === candidateId,
  ) || null;
}

async function editMemoryCandidate(candidateId) {
  if (state.busy) {
    return;
  }
  const candidate = memoryCandidateById(candidateId);
  const card = memoryCandidateCardNode(candidateId);
  if (!candidate || !card) {
    return;
  }

  setBusy(true);
  try {
    await apiRequest(
      `${MEMORY_REVIEW_API}/candidates/`
      + `${encodeURIComponent(candidateId)}/edit`,
      {
        method: "POST",
        body: {
          content:
            card.querySelector(
              ".memory-candidate-content",
            ).value,
          category:
            card.querySelector(
              ".memory-candidate-category",
            ).value,
          importance:
            card.querySelector(
              ".memory-candidate-importance",
            ).value,
          pinned:
            card.querySelector(
              ".memory-candidate-pinned-input",
            ).checked,
          expected_revision: candidate.revision,
          confirm_review_edit: true,
        },
      },
    );
    await refreshMemoryReview();
    setStatus(
      "Memory candidate review edit saved",
      "ready",
    );
  } catch (error) {
    if (error.status === 409) {
      await refreshMemoryReview();
    }
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function approveMemoryCandidatePreview(
  candidateId,
) {
  if (state.busy) {
    return;
  }
  const candidate = memoryCandidateById(candidateId);
  if (!candidate) {
    return;
  }

  setBusy(true);
  try {
    await apiRequest(
      `${MEMORY_REVIEW_API}/candidates/`
      + `${encodeURIComponent(candidateId)}`
      + "/approve-preview",
      {
        method: "POST",
        body: {
          expected_revision: candidate.revision,
          confirm_review_approval: true,
        },
      },
    );
    await refreshMemoryReview();
    setStatus(
      "Permission-gated write preview approved",
      "ready",
    );
  } catch (error) {
    if (error.status === 409) {
      await refreshMemoryReview();
    }
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function rejectMemoryCandidate(candidateId) {
  if (state.busy) {
    return;
  }
  const candidate = memoryCandidateById(candidateId);
  if (!candidate) {
    return;
  }

  setBusy(true);
  try {
    await apiRequest(
      `${MEMORY_REVIEW_API}/candidates/`
      + `${encodeURIComponent(candidateId)}/reject`,
      {
        method: "POST",
        body: {
          expected_revision: candidate.revision,
          confirm_reject: true,
        },
      },
    );
    await refreshMemoryReview();
    setStatus(
      "Transient memory candidate rejected",
      "ready",
    );
  } catch (error) {
    if (error.status === 409) {
      await refreshMemoryReview();
    }
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

function sessionButton(session) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "session-item";
  button.dataset.sessionId = session.session_id;
  button.dataset.sessionState = session.status;
  button.setAttribute(
    "aria-current",
    String(
      state.activeSession?.session_id === session.session_id,
    ),
  );

  const title = document.createElement("strong");
  title.textContent = session.title;
  const detail = document.createElement("small");
  detail.textContent =
    `${session.message_count} messages · revision ${session.revision} · ${session.status}`;

  button.append(title, detail);
  button.addEventListener("click", async () => {
    try {
      if (session.status === "active") {
        await resumeSession(
          session.session_id,
          session.revision,
        );
      } else {
        await loadSession(session.session_id);
      }
    } catch (error) {
      const handled = await handleChatRecoveryError(
        error,
        {
          sessionId: session.session_id,
          preservePending: true,
        },
      );
      if (!handled) {
        setStatus(error.message, "error");
      }
    }
  });
  return button;
}

function renderSessionList() {
  const list = byId("session-list");
  list.replaceChildren();
  if (state.sessions.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent =
      state.sessionFilter === "active"
        ? "No active local chat sessions."
        : "No archived local chat sessions.";
    list.append(empty);
    return;
  }
  state.sessions.forEach((session) => {
    list.append(sessionButton(session));
  });
}

function messageRoleLabel(message) {
  if (message.role === "user") {
    return "You";
  }
  if (message.response_kind === "local_model_response") {
    return "AURA local model";
  }
  if (message.response_kind === "model_bridge_unavailable") {
    return "AURA runtime notice";
  }
  return "AURA response";
}

function messageKindLabel(message) {
  if (message.role === "user") {
    return "Local input";
  }
  if (message.response_kind === "local_model_response") {
    return "Model response";
  }
  return "Saved without model";
}

function renderTranscript() {
  const transcript = byId("chat-transcript");
  transcript.replaceChildren();
  renderMemorySourceOptions();

  if (!state.activeSession) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No active local chat session.";
    transcript.append(empty);
    byId("session-meta").textContent =
      "Create or select a session.";
    return;
  }

  byId("session-meta").textContent =
    `${state.activeSession.title} · `
    + `${state.activeSession.message_count} messages · `
    + `revision ${state.activeSession.revision} · `
    + `${state.activeSession.status}`;

  if (state.activeSession.messages.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent =
      state.activeSession.status === "archived"
        ? "This archived session has no messages."
        : "This local session has no messages.";
    transcript.append(empty);
    return;
  }

  state.activeSession.messages.forEach((message) => {
    const article = document.createElement("article");
    article.className = "message-row";
    article.dataset.role = message.role;
    article.dataset.responseKind =
      message.response_kind || "user";

    const header = document.createElement("header");
    const role = document.createElement("strong");
    role.textContent = messageRoleLabel(message);
    const metadata = document.createElement("span");
    metadata.className = "message-metadata";
    const kind = document.createElement("span");
    kind.className = "message-kind";
    kind.textContent = messageKindLabel(message);
    const sequence = document.createElement("span");
    sequence.textContent = `#${message.sequence}`;
    metadata.append(kind, sequence);
    header.append(role, metadata);

    const content = document.createElement("p");
    content.textContent = message.content;
    article.append(header, content);
    transcript.append(article);
  });
  transcript.scrollTop = transcript.scrollHeight;
}

function renderModelStatus() {
  const badge = byId("model-status-badge");
  const detail = byId("model-status-detail");
  const provider = byId("model-provider");
  const model = byId("model-name");

  if (!state.modelStatus) {
    badge.textContent = "Unavailable";
    badge.dataset.state = "error";
    detail.textContent =
      "The local-model status endpoint is unavailable.";
    provider.textContent = "Unknown";
    model.textContent = "Unknown";
    syncComposerControls();
    return;
  }

  provider.textContent =
    state.modelStatus.provider || "Not configured";
  model.textContent =
    state.modelStatus.model || "Not configured";

  if (state.modelStatus.degraded) {
    badge.textContent = "Degraded";
    badge.dataset.state = "error";
    detail.textContent =
      state.modelStatus.configuration_error
      || "The local model profile is invalid.";
  } else if (state.modelStatus.active) {
    badge.textContent = "Active";
    badge.dataset.state = "ready";
    detail.textContent =
      "Ready for explicitly confirmed text requests.\n"
      + "No tools, actions, streaming, or fallback are connected.";
  } else if (state.modelStatus.configured) {
    badge.textContent = "Disabled";
    badge.dataset.state = "idle";
    detail.textContent =
      "A local profile exists but is not enabled for this process.";
  } else {
    badge.textContent = "Not configured";
    badge.dataset.state = "idle";
    detail.textContent =
      "Start AURA with a valid AURA_LOCAL_MODEL_* profile "
      + "to enable local-model chat.";
  }

  if (!modelIsActive()) {
    byId("mode-save-only").checked = true;
    byId("confirm-model-request").checked = false;
    clearPendingSubmission();
  }
  syncComposerControls();
}

function clientMessageId() {
  if (globalThis.crypto?.randomUUID) {
    return `client_${crypto.randomUUID().replaceAll("-", "")}`;
  }
  return `client_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

function modelRequestId() {
  if (globalThis.crypto?.randomUUID) {
    return `modelreq_${crypto.randomUUID().replaceAll("-", "")}`;
  }
  return `modelreq_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

function submissionFor(content, mode) {
  const sessionId = state.activeSession.session_id;
  if (
    state.pendingSubmission
    && state.pendingSubmission.sessionId === sessionId
    && state.pendingSubmission.content === content
    && state.pendingSubmission.mode === mode
  ) {
    state.pendingSubmission.expectedRevision =
      state.activeSession.revision;
    return state.pendingSubmission;
  }

  state.pendingSubmission = {
    sessionId,
    content,
    mode,
    clientMessageId: clientMessageId(),
    requestId:
      mode === "local-model" ? modelRequestId() : null,
    expectedRevision: state.activeSession.revision,
  };
  updatePendingStatus();
  return state.pendingSubmission;
}

async function refreshSessions({
  preserveActive = true,
} = {}) {
  const payload = await apiRequest(
    `${API_BASE}/sessions?state=${encodeURIComponent(state.sessionFilter)}`,
  );
  state.sessions = payload.sessions;

  if (preserveActive && state.activeSession) {
    const stillVisible = state.sessions.some(
      (session) =>
        session.session_id === state.activeSession.session_id,
    );
    if (!stillVisible) {
      state.activeSession = null;
      clearPendingSubmission();
    }
  }

  renderSessionList();
  renderTranscript();
  syncSessionFilterControls();
  syncComposerControls();
}

async function refreshModelStatus() {
  try {
    state.modelStatus = await apiRequest(
      `${MODEL_API_BASE}/status`,
    );
  } catch (error) {
    state.modelStatus = null;
    renderModelStatus();
    throw error;
  }
  renderModelStatus();
}

async function createSession() {
  if (state.busy) {
    return;
  }
  setBusy(true);
  try {
    const title = byId("session-title").value.trim();
    const payload = await apiRequest(
      `${API_BASE}/sessions`,
      {
        method: "POST",
        body: { title: title || null },
      },
    );
    state.sessionFilter = "active";
    state.activeSession = payload.session;
    byId("session-title").value = "";
    clearPendingSubmission();
    await refreshSessions();
    renderTranscript();
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function loadSession(
  sessionId,
  { preservePending = false } = {},
) {
  if (state.busy && !preservePending) {
    return;
  }
  const previousSessionId =
    state.activeSession?.session_id || null;
  if (!preservePending && previousSessionId !== sessionId) {
    clearPendingSubmission();
  }
  const payload = await apiRequest(
    `${API_BASE}/sessions/${encodeURIComponent(sessionId)}`,
  );
  state.activeSession = payload.session;
  if (
    preservePending
    && state.pendingSubmission
    && state.pendingSubmission.sessionId === sessionId
  ) {
    state.pendingSubmission.expectedRevision =
      state.activeSession.revision;
    updatePendingStatus();
  }
  renderSessionList();
  renderTranscript();
  syncComposerControls();
}

async function resumeSession(
  sessionId = state.activeSession?.session_id,
  expectedRevision = state.activeSession?.revision,
) {
  if (!sessionId || state.busy) {
    return;
  }
  setBusy(true);
  try {
    const payload = await apiRequest(
      `${API_BASE}/sessions/${encodeURIComponent(sessionId)}/resume`,
      {
        method: "POST",
        body: { expected_revision: expectedRevision },
      },
    );
    if (payload.cross_session_history_merged !== false) {
      throw new Error(
        "Resume response violated cross-session history isolation.",
      );
    }
    state.sessionFilter = "active";
    state.activeSession = payload.session;
    clearPendingSubmission();
    await refreshSessions();
    await refreshRecoveryStatus();
    setStatus("Session resumed", "ready");
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

function requestRename() {
  if (!state.activeSession || state.busy) {
    return;
  }
  byId("rename-title").value = state.activeSession.title;
  byId("rename-dialog").showModal();
  byId("rename-title").focus();
}

async function renameSession() {
  if (!state.activeSession || state.busy) {
    return;
  }
  const title = byId("rename-title").value.trim();
  if (!title) {
    setStatus("Session title is empty", "error");
    return;
  }
  const sessionId = state.activeSession.session_id;
  const expectedRevision = state.activeSession.revision;
  byId("rename-dialog").close();
  setBusy(true);
  try {
    const payload = await apiRequest(
      `${API_BASE}/sessions/${encodeURIComponent(sessionId)}/rename`,
      {
        method: "POST",
        body: {
          title,
          expected_revision: expectedRevision,
        },
      },
    );
    state.activeSession = payload.session;
    clearPendingSubmission();
    await refreshSessions();
    renderTranscript();
    await refreshRecoveryStatus();
    setStatus("Session renamed", "ready");
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

async function archiveSession() {
  if (!selectedSessionIsActive() || state.busy) {
    return;
  }
  const sessionId = state.activeSession.session_id;
  const expectedRevision = state.activeSession.revision;
  setBusy(true);
  try {
    await apiRequest(
      `${API_BASE}/sessions/${encodeURIComponent(sessionId)}/archive`,
      {
        method: "POST",
        body: { expected_revision: expectedRevision },
      },
    );
    state.activeSession = null;
    clearPendingSubmission();
    await refreshSessions({ preserveActive: false });
    await refreshRecoveryStatus();
    setStatus("Session archived without deletion", "ready");
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

async function restoreSession() {
  if (
    !state.activeSession
    || state.activeSession.status !== "archived"
    || state.busy
  ) {
    return;
  }
  const sessionId = state.activeSession.session_id;
  const expectedRevision = state.activeSession.revision;
  setBusy(true);
  try {
    const payload = await apiRequest(
      `${API_BASE}/sessions/${encodeURIComponent(sessionId)}/restore`,
      {
        method: "POST",
        body: { expected_revision: expectedRevision },
      },
    );
    state.sessionFilter = "active";
    state.activeSession = payload.session;
    clearPendingSubmission();
    await refreshSessions();
    renderTranscript();
    await refreshRecoveryStatus();
    setStatus("Session restored", "ready");
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

async function setSessionFilter(nextFilter) {
  if (
    state.busy
    || !["active", "archived"].includes(nextFilter)
  ) {
    return;
  }
  state.sessionFilter = nextFilter;
  state.activeSession = null;
  clearPendingSubmission();
  setBusy(true);
  try {
    await refreshSessions({ preserveActive: false });
    await refreshRecoveryStatus();
  } catch (error) {
    const handled = await handleChatRecoveryError(error);
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

function requestProbe() {
  if (
    state.busy
    || !state.modelStatus?.enabled
    || state.modelStatus?.degraded
  ) {
    return;
  }
  byId("probe-dialog").showModal();
}

async function confirmProbe() {
  if (state.busy) {
    return;
  }
  const dialog = byId("probe-dialog");
  dialog.close();
  setBusy(true);
  try {
    const payload = await apiRequest(
      `${MODEL_API_BASE}/probe`,
      {
        method: "POST",
        body: { confirm_local_connection: true },
      },
    );
    setStatus(
      payload.configured_model_visible
        ? "Model available"
        : "Provider available",
      "ready",
    );
    await refreshModelStatus();
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function submitMessage() {
  if (
    state.busy
    || !state.activeSession
    || !selectedSessionIsActive()
  ) {
    return;
  }
  const input = byId("message-input");
  const content = input.value.trim();
  if (!content) {
    setStatus("Message is empty", "error");
    return;
  }

  const mode = selectedMode();
  if (mode === "local-model" && !modelIsActive()) {
    setStatus(
      "The local model bridge is not active.",
      "error",
    );
    return;
  }
  if (
    mode === "local-model"
    && !byId("confirm-model-request").checked
  ) {
    setStatus(
      "Confirm this single local-model request first.",
      "error",
    );
    return;
  }

  const pending = submissionFor(content, mode);
  setBusy(true);
  try {
    const encodedSessionId =
      encodeURIComponent(pending.sessionId);
    const useModel = mode === "local-model";
    const endpoint = useModel
      ? `${API_BASE}/sessions/${encodedSessionId}/model-messages`
      : `${API_BASE}/sessions/${encodedSessionId}/messages`;
    const body = useModel
      ? {
          content: pending.content,
          client_message_id: pending.clientMessageId,
          expected_revision: pending.expectedRevision,
          request_id: pending.requestId,
          confirm_model_request: true,
        }
      : {
          content: pending.content,
          client_message_id: pending.clientMessageId,
          expected_revision: pending.expectedRevision,
        };

    const result = await apiRequest(endpoint, {
      method: "POST",
      body,
    });
    input.value = "";
    byId("confirm-model-request").checked = false;
    clearPendingSubmission();
    await loadSession(pending.sessionId, {
      preservePending: false,
    });
    await refreshSessions();
    await refreshRecoveryStatus();
    setStatus(
      result.idempotent_replay
        ? "Recovered saved response"
        : useModel
          ? "Model response saved"
          : "Message saved locally",
      "ready",
    );
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId: pending.sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(
        `${error.message} · retry keeps the same request ID`,
        "error",
      );
    } else {
      setStatus(error.message, "error");
    }
    updatePendingStatus();
  } finally {
    setBusy(false);
  }
}

function requestClear() {
  if (
    !state.activeSession
    || !selectedSessionIsActive()
    || state.busy
  ) {
    return;
  }
  const phrase = `CLEAR ${state.activeSession.session_id}`;
  byId("clear-phrase").textContent = phrase;
  byId("clear-confirmation").value = "";
  byId("clear-dialog").showModal();
}

async function confirmClear() {
  if (
    !state.activeSession
    || !selectedSessionIsActive()
    || state.busy
  ) {
    return;
  }
  const dialog = byId("clear-dialog");
  const confirmation = byId("clear-confirmation").value;
  const sessionId = state.activeSession.session_id;
  setBusy(true);
  try {
    await apiRequest(
      `${API_BASE}/sessions/`
      + `${encodeURIComponent(sessionId)}/clear`,
      {
        method: "POST",
        body: {
          confirmation,
          expected_revision: state.activeSession.revision,
        },
      },
    );
    dialog.close();
    clearPendingSubmission();
    await loadSession(sessionId);
    await refreshSessions();
    await refreshRecoveryStatus();
  } catch (error) {
    const handled = await handleChatRecoveryError(
      error,
      {
        sessionId,
        preservePending: true,
      },
    );
    if (!handled) {
      setStatus(error.message, "error");
    }
  } finally {
    setBusy(false);
  }
}

function handleComposerChange() {
  updateMessageCount();
  if (
    state.pendingSubmission
    && state.pendingSubmission.content
      !== byId("message-input").value.trim()
  ) {
    clearPendingSubmission();
  }
  syncComposerControls();
}

function handleModeChange() {
  byId("confirm-model-request").checked = false;
  clearPendingSubmission();
  syncComposerControls();
}

function installHandlers() {
  byId("create-session").addEventListener(
    "click",
    createSession,
  );
  byId("refresh-sessions").addEventListener(
    "click",
    () => {
      if (state.busy) {
        return;
      }
      setBusy(true);
      Promise.all([
        refreshSessions(),
        refreshRecoveryStatus(),
        refreshMemoryReview(),
      ])
        .catch(async (error) => {
          const handled =
            await handleChatRecoveryError(error);
          if (!handled) {
            setStatus(error.message, "error");
          }
        })
        .finally(() => {
          setBusy(false);
        });
    },
  );
  byId("session-filter-active").addEventListener(
    "click",
    () => setSessionFilter("active"),
  );
  byId("session-filter-archived").addEventListener(
    "click",
    () => setSessionFilter("archived"),
  );
  byId("resume-session").addEventListener(
    "click",
    () => resumeSession(),
  );
  byId("rename-session").addEventListener(
    "click",
    requestRename,
  );
  byId("confirm-rename").addEventListener(
    "click",
    renameSession,
  );
  byId("cancel-rename").addEventListener(
    "click",
    () => byId("rename-dialog").close(),
  );
  byId("archive-session").addEventListener(
    "click",
    archiveSession,
  );
  byId("restore-session").addEventListener(
    "click",
    restoreSession,
  );
  byId("retry-history-recovery").addEventListener(
    "click",
    retryHistoryRecovery,
  );
  byId("dismiss-history-recovery").addEventListener(
    "click",
    dismissHistoryRecovery,
  );
  byId("refresh-model-status").addEventListener(
    "click",
    () => {
      if (state.busy) {
        return;
      }
      setBusy(true);
      refreshModelStatus()
        .catch((error) => {
          setStatus(error.message, "error");
        })
        .finally(() => {
          setBusy(false);
        });
    },
  );
  byId("probe-model").addEventListener(
    "click",
    requestProbe,
  );
  byId("confirm-probe").addEventListener(
    "click",
    confirmProbe,
  );
  byId("cancel-probe").addEventListener(
    "click",
    () => byId("probe-dialog").close(),
  );
  byId("send-message").addEventListener(
    "click",
    submitMessage,
  );
  byId("clear-session").addEventListener(
    "click",
    requestClear,
  );
  byId("confirm-clear").addEventListener(
    "click",
    confirmClear,
  );
  byId("cancel-clear").addEventListener(
    "click",
    () => byId("clear-dialog").close(),
  );
  byId("message-input").addEventListener(
    "input",
    handleComposerChange,
  );
  byId("mode-save-only").addEventListener(
    "change",
    handleModeChange,
  );
  byId("mode-local-model").addEventListener(
    "change",
    handleModeChange,
  );
  byId("confirm-model-request").addEventListener(
    "change",
    syncComposerControls,
  );
  byId("message-input").addEventListener(
    "keydown",
    (event) => {
      if (
        event.key === "Enter"
        && !event.shiftKey
        && !event.isComposing
      ) {
        event.preventDefault();
        submitMessage();
      }
    },
  );

  byId("refresh-memory-review").addEventListener(
    "click",
    () => {
      if (state.busy) {
        return;
      }
      setBusy(true);
      refreshMemoryReview()
        .catch((error) => {
          setStatus(error.message, "error");
        })
        .finally(() => {
          setBusy(false);
        });
    },
  );
  byId("create-memory-candidate").addEventListener(
    "click",
    createMemoryCandidate,
  );
  byId("memory-source-message").addEventListener(
    "change",
    syncComposerControls,
  );
}

async function start() {
  installHandlers();
  updateMessageCount();
  updatePendingStatus();
  syncSessionFilterControls();
  renderRecoveryStatus();
  renderMemoryReview();
  setBusy(true);
  const results = await Promise.allSettled([
    refreshSessions({ preserveActive: false }),
    refreshRecoveryStatus(),
    refreshMemoryReview(),
    refreshModelStatus(),
  ]);
  const failures = results.filter(
    (result) => result.status === "rejected",
  );
  for (const failure of failures) {
    const handled = await handleChatRecoveryError(
      failure.reason,
    );
    if (!handled) {
      setStatus(
        failure.reason?.message
        || "Interactive chat initialization failed.",
        "error",
      );
    }
  }
  setBusy(false);
}

document.addEventListener("DOMContentLoaded", start);

/* Sprint 271 — import explicit voice transcript drafts */
const AURA_VOICE_CHAT_DRAFT_FRAGMENT = "voice_draft";

function importAuraVoiceTranscriptDraft() {
  const fragmentText = window.location.hash.startsWith("#")
    ? window.location.hash.slice(1)
    : "";
  const fragment = new URLSearchParams(fragmentText);
  const draft = fragment.get(AURA_VOICE_CHAT_DRAFT_FRAGMENT);
  if (!draft) {
    return;
  }

  const cleanUrl = new URL(window.location.href);
  cleanUrl.hash = "";
  window.history.replaceState(
    null,
    "",
    `${cleanUrl.pathname}${cleanUrl.search}`,
  );

  const input = byId("message-input");
  if (!input) {
    return;
  }

  if (input.value.trim()) {
    setStatus(
      "A voice transcript draft was received, but the existing composer "
      + "was not replaced.",
      "idle",
    );
    return;
  }

  input.value = draft.slice(0, 8192);
  updateMessageCount();
  syncComposerControls();
  input.focus();
  setStatus(
    "Voice transcript loaded. Review it and send explicitly.",
    "ready",
  );
}

if (document.readyState === "loading") {
  document.addEventListener(
    "DOMContentLoaded",
    importAuraVoiceTranscriptDraft,
    { once: true },
  );
} else {
  queueMicrotask(importAuraVoiceTranscriptDraft);
}
