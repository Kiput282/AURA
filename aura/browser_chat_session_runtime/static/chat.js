"use strict";

const API_BASE = "/api/chat";
const MODEL_API_BASE = "/api/model";
const LOCAL_INTENT = "browser-chat-session";
const MAX_MESSAGE_CHARACTERS = 8192;

const state = {
  sessions: [],
  activeSession: null,
  modelStatus: null,
  busy: false,
  pendingSubmission: null,
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
  return byId("mode-local-model").checked
    ? "local-model"
    : "save-only";
}

function modelIsActive() {
  return Boolean(
    state.modelStatus
    && state.modelStatus.active === true
    && state.modelStatus.degraded !== true,
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

function syncComposerControls() {
  const hasSession = Boolean(state.activeSession);
  const activeModel = modelIsActive();
  const useModel = selectedMode() === "local-model";

  byId("create-session").disabled = state.busy;
  byId("refresh-sessions").disabled = state.busy;
  byId("refresh-model-status").disabled = state.busy;
  byId("probe-model").disabled =
    state.busy
    || !Boolean(state.modelStatus?.enabled)
    || Boolean(state.modelStatus?.degraded);

  byId("clear-session").disabled =
    state.busy || !hasSession;
  byId("message-input").disabled =
    state.busy || !hasSession;
  byId("mode-save-only").disabled =
    state.busy || !hasSession;
  byId("mode-local-model").disabled =
    state.busy || !hasSession || !activeModel;
  byId("confirm-model-request").disabled =
    state.busy || !hasSession || !activeModel || !useModel;

  if (!activeModel && useModel) {
    byId("mode-save-only").checked = true;
    byId("confirm-model-request").checked = false;
  }

  const effectiveModelMode =
    selectedMode() === "local-model";
  const confirmationReady =
    !effectiveModelMode
    || byId("confirm-model-request").checked;

  byId("send-message").disabled =
    state.busy
    || !hasSession
    || !byId("message-input").value.trim()
    || !confirmationReady;

  byId("send-message").textContent =
    effectiveModelMode
      ? "Send to local model"
      : "Save without model";

  setStatus(
    state.busy
      ? "Working"
      : hasSession
      ? "Ready"
      : "Idle",
    state.busy
      ? "busy"
      : hasSession
      ? "ready"
      : "idle",
  );
}

function setBusy(value) {
  state.busy = value;
  syncComposerControls();
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
    body: options.body
      ? JSON.stringify(options.body)
      : undefined,
    cache: "no-store",
    credentials: "same-origin",
  });

  const contentType =
    response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : {
        detail: await response.text(),
      };

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

function sessionButton(session) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "session-item";
  button.dataset.sessionId = session.session_id;
  button.setAttribute(
    "aria-current",
    String(
      state.activeSession?.session_id
      === session.session_id,
    ),
  );

  const title = document.createElement("strong");
  title.textContent = session.title;

  const detail = document.createElement("small");
  detail.textContent =
    `${session.message_count} messages · `
    + `revision ${session.revision}`;

  button.append(title, detail);
  button.addEventListener("click", () => {
    loadSession(session.session_id);
  });
  return button;
}

function renderSessionList() {
  const list = byId("session-list");
  list.replaceChildren();

  if (state.sessions.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No local chat sessions yet.";
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
    + `revision ${state.activeSession.revision}`;

  if (state.activeSession.messages.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent =
      "This local session has no messages.";
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
      "Ready for explicitly confirmed text requests. "
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
    return `client_${
      crypto.randomUUID().replaceAll("-", "")
    }`;
  }
  return `client_${Date.now()}_${
    Math.random().toString(36).slice(2)
  }`;
}

function modelRequestId() {
  if (globalThis.crypto?.randomUUID) {
    return `modelreq_${
      crypto.randomUUID().replaceAll("-", "")
    }`;
  }
  return `modelreq_${Date.now()}_${
    Math.random().toString(36).slice(2)
  }`;
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
      mode === "local-model"
        ? modelRequestId()
        : null,
    expectedRevision: state.activeSession.revision,
  };
  updatePendingStatus();
  return state.pendingSubmission;
}

async function refreshSessions({
  preserveActive = true,
} = {}) {
  const payload = await apiRequest(`${API_BASE}/sessions`);
  state.sessions = payload.sessions;

  if (preserveActive && state.activeSession) {
    const stillExists = state.sessions.some(
      (session) =>
        session.session_id
        === state.activeSession.session_id,
    );
    if (!stillExists) {
      state.activeSession = null;
      clearPendingSubmission();
    }
  }

  renderSessionList();
  renderTranscript();
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
        body: {
          title: title || null,
        },
      },
    );
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
    `${API_BASE}/sessions/${
      encodeURIComponent(sessionId)
    }`,
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
        body: {
          confirm_local_connection: true,
        },
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
  if (state.busy || !state.activeSession) {
    return;
  }

  const input = byId("message-input");
  const content = input.value.trim();
  if (!content) {
    setStatus("Message is empty", "error");
    return;
  }

  const mode = selectedMode();
  if (
    mode === "local-model"
    && !modelIsActive()
  ) {
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
    const encodedSessionId = encodeURIComponent(
      pending.sessionId,
    );
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

    setStatus(
      result.idempotent_replay
        ? "Recovered saved response"
        : useModel
        ? "Model response saved"
        : "Message saved locally",
      "ready",
    );
  } catch (error) {
    if (
      error.status === 409
      && state.activeSession
    ) {
      try {
        await loadSession(
          state.activeSession.session_id,
          {
            preservePending: true,
          },
        );
      } catch (reloadError) {
        setStatus(reloadError.message, "error");
        return;
      }
    }

    setStatus(
      `${error.message} · retry keeps the same request ID`,
      "error",
    );
    updatePendingStatus();
  } finally {
    setBusy(false);
  }
}

function requestClear() {
  if (!state.activeSession || state.busy) {
    return;
  }

  const phrase =
    `CLEAR ${state.activeSession.session_id}`;
  byId("clear-phrase").textContent = phrase;
  byId("clear-confirmation").value = "";
  byId("clear-dialog").showModal();
}

async function confirmClear() {
  if (!state.activeSession || state.busy) {
    return;
  }

  const dialog = byId("clear-dialog");
  const confirmation =
    byId("clear-confirmation").value;
  setBusy(true);

  try {
    await apiRequest(
      `${API_BASE}/sessions/`
      + `${
        encodeURIComponent(
          state.activeSession.session_id,
        )
      }/clear`,
      {
        method: "POST",
        body: {
          confirmation,
          expected_revision:
            state.activeSession.revision,
        },
      },
    );
    dialog.close();
    clearPendingSubmission();
    await loadSession(
      state.activeSession.session_id,
    );
    await refreshSessions();
  } catch (error) {
    setStatus(error.message, "error");
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
      refreshSessions()
        .catch((error) => {
          setStatus(error.message, "error");
        })
        .finally(() => {
          setBusy(false);
        });
    },
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
    () => {
      byId("probe-dialog").close();
    },
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
    () => {
      byId("clear-dialog").close();
    },
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
}

async function start() {
  installHandlers();
  updateMessageCount();
  updatePendingStatus();
  setBusy(true);

  const results = await Promise.allSettled([
    refreshSessions({
      preserveActive: false,
    }),
    refreshModelStatus(),
  ]);

  const failure = results.find(
    (result) => result.status === "rejected",
  );
  if (failure) {
    setStatus(
      failure.reason?.message
      || "Interactive chat initialization failed.",
      "error",
    );
  }

  setBusy(false);
}

document.addEventListener("DOMContentLoaded", start);
