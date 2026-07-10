"use strict";

const API_BASE = "/api/chat";
const LOCAL_INTENT = "browser-chat-session";

const state = {
  sessions: [],
  activeSession: null,
  busy: false,
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

function setBusy(value) {
  state.busy = value;
  const hasSession = Boolean(state.activeSession);

  byId("create-session").disabled = value;
  byId("refresh-sessions").disabled = value;
  byId("send-message").disabled = value || !hasSession;
  byId("clear-session").disabled = value || !hasSession;
  byId("message-input").disabled = value || !hasSession;

  setStatus(value ? "Working" : hasSession ? "Ready" : "Idle",
    value ? "busy" : hasSession ? "ready" : "idle");
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

  const payload = await response.json();
  if (!response.ok) {
    const error = new Error(
      payload.detail || payload.reason || `HTTP ${response.status}`,
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
    String(state.activeSession?.session_id === session.session_id),
  );

  const title = document.createElement("strong");
  title.textContent = session.title;

  const detail = document.createElement("small");
  detail.textContent =
    `${session.message_count} messages · revision ${session.revision}`;

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

    const header = document.createElement("header");
    const role = document.createElement("strong");
    role.textContent =
      message.role === "user" ? "You" : "AURA runtime";
    const sequence = document.createElement("span");
    sequence.textContent = `#${message.sequence}`;
    header.append(role, sequence);

    const content = document.createElement("p");
    content.textContent = message.content;

    article.append(header, content);
    transcript.append(article);
  });

  transcript.scrollTop = transcript.scrollHeight;
}

function clientMessageId() {
  if (globalThis.crypto?.randomUUID) {
    return `client_${crypto.randomUUID().replaceAll("-", "")}`;
  }
  return `client_${Date.now()}_${Math.random()
    .toString(36)
    .slice(2)}`;
}

async function refreshSessions({ preserveActive = true } = {}) {
  const payload = await apiRequest(`${API_BASE}/sessions`);
  state.sessions = payload.sessions;

  if (preserveActive && state.activeSession) {
    const stillExists = state.sessions.some(
      (session) =>
        session.session_id === state.activeSession.session_id,
    );
    if (!stillExists) {
      state.activeSession = null;
    }
  }

  renderSessionList();
  renderTranscript();
}

async function createSession() {
  if (state.busy) {
    return;
  }

  setBusy(true);
  try {
    const title = byId("session-title").value.trim();
    const payload = await apiRequest(`${API_BASE}/sessions`, {
      method: "POST",
      body: {
        title: title || null,
      },
    });
    state.activeSession = payload.session;
    byId("session-title").value = "";
    await refreshSessions();
    renderTranscript();
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function loadSession(sessionId) {
  if (state.busy) {
    return;
  }

  setBusy(true);
  try {
    const payload = await apiRequest(
      `${API_BASE}/sessions/${encodeURIComponent(sessionId)}`,
    );
    state.activeSession = payload.session;
    renderSessionList();
    renderTranscript();
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

  setBusy(true);
  try {
    await apiRequest(
      `${API_BASE}/sessions/`
      + `${encodeURIComponent(state.activeSession.session_id)}`
      + "/messages",
      {
        method: "POST",
        body: {
          content,
          client_message_id: clientMessageId(),
          expected_revision: state.activeSession.revision,
        },
      },
    );
    input.value = "";
    await loadSession(state.activeSession.session_id);
    await refreshSessions();
  } catch (error) {
    if (error.status === 409) {
      await loadSession(state.activeSession.session_id);
    }
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

function requestClear() {
  if (!state.activeSession || state.busy) {
    return;
  }

  const phrase = `CLEAR ${state.activeSession.session_id}`;
  byId("clear-phrase").textContent = phrase;
  byId("clear-confirmation").value = "";
  byId("clear-dialog").showModal();
}

async function confirmClear() {
  if (!state.activeSession || state.busy) {
    return;
  }

  const dialog = byId("clear-dialog");
  const confirmation = byId("clear-confirmation").value;

  setBusy(true);
  try {
    await apiRequest(
      `${API_BASE}/sessions/`
      + `${encodeURIComponent(state.activeSession.session_id)}`
      + "/clear",
      {
        method: "POST",
        body: {
          confirmation,
          expected_revision: state.activeSession.revision,
        },
      },
    );
    dialog.close();
    await loadSession(state.activeSession.session_id);
    await refreshSessions();
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

function installHandlers() {
  byId("create-session").addEventListener("click", createSession);
  byId("refresh-sessions").addEventListener("click", () => {
    if (!state.busy) {
      setBusy(true);
      refreshSessions()
        .catch((error) => setStatus(error.message, "error"))
        .finally(() => setBusy(false));
    }
  });
  byId("send-message").addEventListener("click", submitMessage);
  byId("clear-session").addEventListener("click", requestClear);
  byId("confirm-clear").addEventListener("click", confirmClear);
  byId("cancel-clear").addEventListener("click", () => {
    byId("clear-dialog").close();
  });
  byId("message-input").addEventListener("keydown", (event) => {
    if (
      event.key === "Enter"
      && !event.shiftKey
      && !event.isComposing
    ) {
      event.preventDefault();
      submitMessage();
    }
  });
}

async function start() {
  installHandlers();
  setBusy(true);
  try {
    await refreshSessions({ preserveActive: false });
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
}

document.addEventListener("DOMContentLoaded", start);
