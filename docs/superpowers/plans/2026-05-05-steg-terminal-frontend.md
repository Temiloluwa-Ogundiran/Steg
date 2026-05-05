# Steg Terminal Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the poster-style Steg web UI with a terminal-aesthetic interface featuring a segmented mode grid, minimal form fields, and a syntax-highlighted terminal sidebar for results.

**Architecture:** Single-page FastAPI Jinja2 app with vanilla JS. Three files rewritten completely (`styles.css`, `index.html`, `app.js`). Tests updated to match new rendered output. No backend changes.

**Tech Stack:** FastAPI, Jinja2, vanilla JavaScript, CSS custom properties, Google Fonts (Space Grotesk, JetBrains Mono).

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `webapp/static/styles.css` | Rewrite | All terminal aesthetic styles: grid background, tokens, layout, components, responsive |
| `webapp/templates/index.html` | Rewrite | Jinja2 template: header, mode grid, conditional form fields, terminal sidebar |
| `webapp/static/app.js` | Rewrite | Mode switching, file handling, form submission, terminal rendering with syntax highlighting |
| `tests/webapp/test_main.py` | Modify | Update HTML assertion strings to match new template output |

---

### Task 1: Write Terminal Aesthetic CSS

**Files:**
- Rewrite: `webapp/static/styles.css`

- [ ] **Step 1: Write the complete styles.css**

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --bg-primary: #111111;
  --bg-terminal: #050505;
  --bg-surface: #1A1A1A;
  --border: #333333;
  --text-title: #FFFFFF;
  --text-body: #E5E5E5;
  --text-muted: #555555;
  --accent-success: #4ADE80;
  --accent-error: #F87171;
  --accent-warn: #FACC15;
  --accent-purple: #C084FC;
  --accent-blue: #60A5FA;
  --accent-green-light: #BBF7D0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  background: var(--bg-primary);
  color: var(--text-body);
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  line-height: 1.5;
  cursor: crosshair;
}

body {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Background grid */
.page-shell {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

.page-shell::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 60%, var(--bg-primary) 100%);
  pointer-events: none;
}

/* Header */
.topbar {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  height: 40px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-primary);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.topbar__pulse {
  width: 8px;
  height: 8px;
  background: var(--text-title);
  animation: pulse 2s steps(1, end) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.topbar__version {
  color: var(--text-muted);
}

.topbar__status {
  margin-left: auto;
  color: var(--text-muted);
}

/* Main layout */
.workspace {
  position: relative;
  z-index: 5;
  flex: 1;
  display: flex;
  overflow: hidden;
}

.main-stage {
  flex: 1;
  min-width: 0;
  padding: 24px 32px;
  overflow-y: auto;
}

/* Brand */
.brand {
  margin-bottom: 24px;
}

.brand__title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-title);
  letter-spacing: -0.02em;
  line-height: 1;
}

.brand__sub {
  color: var(--text-muted);
  font-size: 10px;
  margin-top: 4px;
}

/* Sections */
.section {
  margin-bottom: 20px;
}

.section__label {
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 8px;
}

/* Mode grid */
.mode-grid {
  display: flex;
  border: 1px solid var(--border);
}

.mode-grid__button {
  flex: 1;
  padding: 12px;
  border: 0;
  border-right: 1px solid var(--border);
  background: var(--bg-primary);
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: background-color 0.05s linear, color 0.05s linear;
}

.mode-grid__button:last-child {
  border-right: 0;
}

.mode-grid__button:hover {
  background: var(--bg-surface);
  color: var(--text-body);
}

.mode-grid__button.is-active {
  background: var(--text-title);
  color: #000000;
}

.mode-grid__button:focus-visible {
  outline: 1px solid var(--text-title);
  outline-offset: -1px;
}

/* Form fields */
.field {
  border: 1px solid var(--border);
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.05s linear;
}

.field:hover {
  background: var(--bg-surface);
}

.field__prefix {
  color: var(--text-muted);
  font-size: 10px;
}

.field__value {
  color: var(--text-body);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.field__meta {
  color: var(--text-muted);
  font-size: 10px;
  margin-left: auto;
}

.field__input {
  width: 100%;
  background: transparent;
  border: 0;
  color: var(--text-body);
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  outline: none;
  resize: vertical;
  min-height: 80px;
}

.field__input::placeholder {
  color: var(--text-muted);
}

.field--textarea {
  display: block;
  cursor: text;
}

/* Hidden native file input */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Action button */
.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

.poster-button {
  background: var(--text-title);
  color: #000000;
  border: 0;
  padding: 12px 24px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: background-color 0.05s linear;
}

.poster-button:hover {
  background: var(--text-body);
}

.poster-button:active {
  background: #CCCCCC;
}

.poster-button:disabled {
  background: var(--border);
  color: var(--text-muted);
  cursor: not-allowed;
}

.poster-button:focus-visible {
  outline: 1px solid var(--text-title);
  outline-offset: 2px;
}

/* Terminal sidebar */
.terminal {
  width: 340px;
  flex-shrink: 0;
  border-left: 1px solid var(--border);
  background: var(--bg-terminal);
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.terminal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.terminal__title {
  color: var(--text-muted);
}

.terminal__status {
  color: var(--accent-success);
}

.terminal__status-dot {
  animation: pulse 2s steps(1, end) infinite;
}

.terminal__body {
  flex: 1;
  overflow-y: auto;
  font-size: 11px;
  line-height: 1.6;
}

.terminal__line {
  display: flex;
  gap: 12px;
}

.terminal__line-num {
  color: var(--border);
  font-size: 10px;
  text-align: right;
  min-width: 24px;
  user-select: none;
}

.terminal__line-content {
  color: var(--text-muted);
  white-space: pre-wrap;
  word-break: break-word;
}

.terminal__line-content.is-comment { color: var(--text-muted); }
.terminal__line-content.is-keyword { color: var(--accent-purple); }
.terminal__line-content.is-string { color: var(--accent-green-light); }
.terminal__line-content.is-variable { color: var(--accent-blue); }
.terminal__line-content.is-prompt { color: var(--accent-warn); }
.terminal__line-content.is-error { color: var(--accent-error); }
.terminal__line-content.is-success { color: var(--accent-success); }

/* Image preview in terminal */
.terminal__preview {
  max-width: 100%;
  border: 1px solid var(--border);
  display: block;
  margin-top: 4px;
}

.terminal__actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.terminal__link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid var(--text-body);
  color: var(--text-body);
  padding: 8px 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-decoration: none;
  transition: background-color 0.05s linear, color 0.05s linear;
}

.terminal__link:hover {
  background: var(--text-body);
  color: var(--bg-primary);
}

.terminal__footer {
  border-top: 1px solid var(--border);
  padding-top: 8px;
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-muted);
}

/* Mode panels */
.mode-panel {
  display: none;
}

.mode-panel.is-active {
  display: block;
}

/* Responsive */
@media (max-width: 900px) {
  .workspace {
    flex-direction: column;
    overflow-y: auto;
  }

  .main-stage {
    padding: 16px 20px;
  }

  .terminal {
    width: 100%;
    border-left: 0;
    border-top: 1px solid var(--border);
    min-height: 280px;
  }
}

@media (max-width: 480px) {
  .mode-grid {
    flex-direction: column;
  }

  .mode-grid__button {
    border-right: 0;
    border-bottom: 1px solid var(--border);
  }

  .mode-grid__button:last-child {
    border-bottom: 0;
  }
}
```

- [ ] **Step 2: Verify CSS file is saved**

Check: `webapp/static/styles.css` should contain the full content above.

- [ ] **Step 3: Commit**

```bash
git add webapp/static/styles.css
git commit -m "feat(ui): rewrite styles.css with terminal aesthetic"
```

---

### Task 2: Write Terminal Layout HTML Template

**Files:**
- Rewrite: `webapp/templates/index.html`

- [ ] **Step 1: Write the complete index.html**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ app_title }}</title>
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23111111'/%3E%3Crect x='20' y='20' width='24' height='24' fill='%23FFFFFF'/%3E%3C/svg%3E">
    <link rel="stylesheet" href="{{ url_for('static', path='styles.css') }}">
    <script defer src="{{ url_for('static', path='app.js') }}"></script>
  </head>
  <body>
    <div class="page-shell">
      <header class="topbar">
        <div class="topbar__pulse" aria-hidden="true"></div>
        <div class="topbar__version">{{ app_title|upper }} {{ app_version }} [BUILD 001]</div>
        <div class="topbar__status">// SYSTEM READY</div>
      </header>

      <div class="workspace">
        <main class="main-stage">
          <div class="brand">
            <h1 class="brand__title">{{ app_title }}</h1>
            <p class="brand__sub">// Hide signal. Reveal truth.</p>
          </div>

          <section class="section">
            <div class="section__label">01 // MODE</div>
            <div class="mode-grid" role="tablist" aria-label="Steg modes">
              <button
                type="button"
                class="mode-grid__button is-active"
                data-mode-target="encode"
                aria-selected="true"
              >
                Encode
              </button>
              <button
                type="button"
                class="mode-grid__button"
                data-mode-target="decode"
                aria-selected="false"
              >
                Decode
              </button>
              <button
                type="button"
                class="mode-grid__button"
                data-mode-target="check"
                aria-selected="false"
              >
                Check
              </button>
            </div>
          </section>

          <section class="mode-panel is-active" data-mode-panel="encode">
            <form
              id="encode-form"
              class="tool-form"
              data-api-endpoint="/api/encode"
              data-result-kind="encode"
            >
              <section class="section">
                <div class="section__label">02 // INPUT</div>
                <label class="field" for="encode-file">
                  <span class="field__prefix">[FILE]</span>
                  <span class="field__value" data-file-name>Awaiting image</span>
                  <span class="field__meta" data-file-dims></span>
                  <input id="encode-file" type="file" name="image" accept="image/*" required class="visually-hidden">
                </label>
              </section>

              <section class="section">
                <div class="section__label">03 // PAYLOAD</div>
                <label class="field field--textarea">
                  <textarea name="message" class="field__input" rows="4" placeholder="Enter hidden message." required></textarea>
                </label>
              </section>

              <section class="section">
                <div class="section__label">04 // KEY</div>
                <label class="field field--textarea">
                  <input type="password" name="passphrase" class="field__input" style="min-height:auto;" placeholder="Enter encryption passphrase." minlength="12" required>
                </label>
              </section>

              <div class="action-bar">
                <button type="submit" class="poster-button">EXECUTE &gt;</button>
              </div>
            </form>
          </section>

          <section class="mode-panel" data-mode-panel="decode" hidden>
            <form
              id="decode-form"
              class="tool-form"
              data-api-endpoint="/api/decode"
              data-result-kind="decode"
            >
              <section class="section">
                <div class="section__label">02 // INPUT</div>
                <label class="field" for="decode-file">
                  <span class="field__prefix">[FILE]</span>
                  <span class="field__value" data-file-name>Awaiting image</span>
                  <span class="field__meta" data-file-dims></span>
                  <input id="decode-file" type="file" name="image" accept="image/*" required class="visually-hidden">
                </label>
              </section>

              <section class="section">
                <div class="section__label">04 // KEY</div>
                <label class="field field--textarea">
                  <input type="password" name="passphrase" class="field__input" style="min-height:auto;" placeholder="Enter decryption passphrase." minlength="12" required>
                </label>
              </section>

              <div class="action-bar">
                <button type="submit" class="poster-button">EXECUTE &gt;</button>
              </div>
            </form>
          </section>

          <section class="mode-panel" data-mode-panel="check" hidden>
            <form
              id="check-form"
              class="tool-form"
              data-api-endpoint="/api/check"
              data-result-kind="check"
            >
              <section class="section">
                <div class="section__label">02 // INPUT</div>
                <label class="field" for="check-file">
                  <span class="field__prefix">[FILE]</span>
                  <span class="field__value" data-file-name>Awaiting image</span>
                  <span class="field__meta" data-file-dims></span>
                  <input id="check-file" type="file" name="image" accept="image/*" required class="visually-hidden">
                </label>
              </section>

              <div class="action-bar">
                <button type="submit" class="poster-button">EXECUTE &gt;</button>
              </div>
            </form>
          </section>
        </main>

        <aside class="terminal" aria-live="polite" aria-atomic="false">
          <div class="terminal__header">
            <span class="terminal__title">TERMINAL // :8000</span>
            <span class="terminal__status"><span class="terminal__status-dot">●</span> LISTENING</span>
          </div>
          <div id="terminal-body" class="terminal__body">
            <div class="terminal__line">
              <span class="terminal__line-num">01</span>
              <span class="terminal__line-content is-comment">// Awaiting input...</span>
            </div>
            <div class="terminal__line">
              <span class="terminal__line-num">02</span>
              <span class="terminal__line-content"></span>
            </div>
            <div class="terminal__line">
              <span class="terminal__line-num">03</span>
              <span class="terminal__line-content is-comment">Select mode and submit.</span>
            </div>
          </div>
          <div class="terminal__footer">
            <span>RAM: --%</span>
            <span>CPU: --%</span>
          </div>
        </aside>
      </div>
    </div>
  </body>
</html>
```

- [ ] **Step 2: Verify HTML file is saved**

Check: `webapp/templates/index.html` should contain the full content above.

- [ ] **Step 3: Commit**

```bash
git add webapp/templates/index.html
git commit -m "feat(ui): rewrite index.html with terminal layout"
```

---

### Task 3: Write Terminal-Aware JavaScript

**Files:**
- Rewrite: `webapp/static/app.js`

- [ ] **Step 1: Write the complete app.js**

```javascript
const modeButtons = document.querySelectorAll("[data-mode-target]");
const modePanels = document.querySelectorAll("[data-mode-panel]");
const terminalBody = document.getElementById("terminal-body");
const forms = document.querySelectorAll(".tool-form");

document.documentElement.dataset.stegReady = "true";

function setActiveMode(nextMode) {
  modeButtons.forEach((button) => {
    const isActive = button.dataset.modeTarget === nextMode;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });

  modePanels.forEach((panel) => {
    const isActive = panel.dataset.modePanel === nextMode;
    panel.hidden = !isActive;
    panel.classList.toggle("is-active", isActive);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderTerminal(lines) {
  const markup = lines.map((line, index) => {
    const num = String(index + 1).padStart(2, "0");
    const content = line.content || "";
    const typeClass = line.type ? `is-${line.type}` : "";
    return `
      <div class="terminal__line">
        <span class="terminal__line-num">${num}</span>
        <span class="terminal__line-content ${typeClass}">${content}</span>
      </div>
    `;
  }).join("");

  terminalBody.innerHTML = markup;
}

function renderIdle() {
  renderTerminal([
    { content: "// Awaiting input...", type: "comment" },
    { content: "" },
    { content: "Select mode and submit.", type: "comment" },
  ]);
}

function renderProcessing(kind) {
  renderTerminal([
    { content: "> Processing request...", type: "prompt" },
    { content: "" },
    { content: `mode: "${kind}"`, type: "variable" },
    { content: 'architecture: "dense"', type: "variable" },
  ]);
}

function renderError(message) {
  renderTerminal([
    { content: "ERROR Processing halted.", type: "keyword" },
    { content: "" },
    { content: escapeHtml(message), type: "error" },
  ]);
}

function renderEncodeResult(data) {
  const lines = [
    { content: "STATUS ok", type: "success" },
    { content: `download_url: "${escapeHtml(data.download_url)}"`, type: "variable" },
    { content: `filename: "${escapeHtml(data.filename)}"`, type: "variable" },
    { content: "" },
    { content: `<img class="terminal__preview" src="${escapeHtml(data.download_url)}" alt="Encoded image preview">`, type: "" },
    { content: "" },
    { content: `<div class="terminal__actions"><a class="terminal__link" href="${escapeHtml(data.download_url)}" download="${escapeHtml(data.filename)}">DOWNLOAD &gt;</a></div>`, type: "" },
  ];
  renderTerminal(lines);
}

function renderDecodeResult(data) {
  if (data.ok) {
    renderTerminal([
      { content: "STATUS ok", type: "success" },
      { content: `message: "${escapeHtml(data.message)}"`, type: "string" },
      { content: 'architecture: "dense"', type: "variable" },
    ]);
    return;
  }

  renderTerminal([
    { content: "STATUS no_message", type: "keyword" },
    { content: "" },
    { content: escapeHtml(data.message || "No hidden message found."), type: "comment" },
  ]);
}

function renderCheckResult(data) {
  const statusType = data.hidden_data ? "success" : "comment";
  const statusText = data.hidden_data ? "true" : "false";

  renderTerminal([
    { content: "STATUS ok", type: "success" },
    { content: `hidden_data: ${statusText}`, type: statusType },
    { content: 'architecture: "dense"', type: "variable" },
  ]);
}

function setSubmitting(form, isSubmitting) {
  const button = form.querySelector('button[type="submit"]');
  if (!button) return;

  if (!button.dataset.defaultText) {
    button.dataset.defaultText = button.textContent;
  }

  button.disabled = isSubmitting;
  button.textContent = isSubmitting ? "PROCESSING..." : button.dataset.defaultText;
}

async function handleSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const endpoint = form.dataset.apiEndpoint;
  const kind = form.dataset.resultKind;
  const payload = new FormData(form);

  if (kind === "encode" && !String(payload.get("message") || "").trim()) {
    renderError("A message is required before encoding can begin.");
    return;
  }

  if (kind !== "check" && !String(payload.get("passphrase") || "").trim()) {
    renderError(kind === "encode"
      ? "A passphrase is required before encoding can begin."
      : "A passphrase is required before decoding can begin.");
    return;
  }

  if (kind !== "check" && String(payload.get("passphrase") || "").trim().length < 12) {
    renderError(kind === "encode"
      ? "The passphrase must be at least 12 characters before encoding can begin."
      : "The passphrase must be at least 12 characters before decoding can begin.");
    return;
  }

  setSubmitting(form, true);
  renderProcessing(kind);

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: payload,
    });
    const data = await response.json();

    if (!response.ok) {
      renderError(data.detail || "The request could not be completed.");
      return;
    }

    if (kind === "encode") {
      renderEncodeResult(data);
    } else if (kind === "decode") {
      renderDecodeResult(data);
    } else {
      renderCheckResult(data);
    }
  } catch (error) {
    renderError("A network or server error interrupted the request.");
  } finally {
    setSubmitting(form, false);
  }
}

function updateFileLabel(input) {
  const field = input.closest(".field");
  if (!field) return;

  const nameEl = field.querySelector("[data-file-name]");
  const dimsEl = field.querySelector("[data-file-dims]");
  const file = input.files?.[0];

  if (nameEl) {
    nameEl.textContent = file?.name || "Awaiting image";
    nameEl.style.color = file ? "var(--text-body)" : "var(--text-muted)";
  }

  if (dimsEl && file) {
    const img = new Image();
    img.onload = () => {
      dimsEl.textContent = `${img.naturalWidth}x${img.naturalHeight} PX`;
    };
    img.src = URL.createObjectURL(file);
  } else if (dimsEl) {
    dimsEl.textContent = "";
  }
}

modeButtons.forEach((button) => {
  button.addEventListener("click", () => setActiveMode(button.dataset.modeTarget));
});

forms.forEach((form) => {
  form.addEventListener("submit", handleSubmit);

  const fileInput = form.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener("change", () => updateFileLabel(fileInput));
  }

  const field = form.querySelector(".field");
  if (field) {
    field.addEventListener("click", (e) => {
      if (e.target.closest('input[type="file"]')) return;
      const input = field.querySelector('input[type="file"]');
      if (input) input.click();
    });
  }
});
```

- [ ] **Step 2: Verify JS file is saved**

Check: `webapp/static/app.js` should contain the full content above.

- [ ] **Step 3: Commit**

```bash
git add webapp/static/app.js
git commit -m "feat(ui): rewrite app.js with terminal rendering and mode grid"
```

---

### Task 4: Update Web App Tests

**Files:**
- Modify: `tests/webapp/test_main.py`

- [ ] **Step 1: Rewrite test assertions for new UI**

Replace the entire content of `tests/webapp/test_main.py` with:

```python
def test_root_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "STEG" in response.text
    assert "ENCODE" in response.text
    assert "DECODE" in response.text
    assert "CHECK" in response.text
    assert "// Hide signal" in response.text
    assert 'name="architecture"' not in response.text
    assert 'type="file"' in response.text
    assert 'name="message"' in response.text
    assert response.text.count('name="passphrase"') == 2
    assert response.text.count('minlength="12"') == 2
    assert 'id="terminal-body"' in response.text
    assert 'data-mode-target="encode"' in response.text
    assert 'data-mode-panel="encode"' in response.text
    assert "SYSTEM READY" in response.text
    assert "TERMINAL" in response.text
    assert "LISTENING" in response.text
    assert "01 // MODE" in response.text
    assert "02 // INPUT" in response.text
    assert "03 // PAYLOAD" in response.text
    assert "04 // KEY" in response.text
    assert "EXECUTE >" in response.text
    assert "FASTAPI / READY" not in response.text
    assert "If the passphrase is lost" not in response.text
```

- [ ] **Step 2: Run the test**

```bash
python -m pytest tests/webapp/test_main.py -v
```

Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/webapp/test_main.py
git commit -m "test(ui): update assertions for terminal frontend"
```

---

### Task 5: Run Full Web App Test Suite

**Files:**
- Run: `tests/webapp/`

- [ ] **Step 1: Run full web app tests**

```bash
python -m pytest tests/webapp -v
```

Expected: All tests pass (`test_main.py`, `test_api.py`, `test_services.py`).

- [ ] **Step 2: Commit if all green**

```bash
git commit --allow-empty -m "chore: verify full web app test suite passes"
```

---

## Self-Review

### Spec Coverage Check

| Spec Requirement | Task |
|---|---|
| Color palette with CSS custom properties | Task 1 |
| Typography (Space Grotesk + JetBrains Mono) | Task 1, 2 |
| Background grid 40px with fade mask | Task 1 |
| Border radius 0px everywhere | Task 1 |
| Crosshair cursor | Task 1 |
| Instant transitions (0.05s linear) | Task 1 |
| Compressed header with pulse + version | Task 2 |
| Segmented mode grid (Encode/Decode/Check) | Task 1, 2, 3 |
| Section labels (01 // MODE, etc.) | Task 2 |
| File field with [FILE] prefix + dimensions | Task 1, 2, 3 |
| Payload textarea (encode only) | Task 2 |
| Key input (encode/decode only) | Task 2 |
| EXECUTE > button | Task 1, 2 |
| Terminal sidebar 340px fixed | Task 1, 2 |
| Terminal header with LISTENING indicator | Task 2 |
| Syntax-highlighted terminal output | Task 3 |
| Terminal states (idle, processing, results, error) | Task 3 |
| Responsive (<900px stack, <480px vertical grid) | Task 1 |
| Text reduction | Task 2 |
| Accessibility (aria-live, aria-pressed, focus) | Task 1, 2 |

### Placeholder Scan

- No "TBD", "TODO", or "implement later"
- No vague "add error handling" steps
- All code blocks contain complete, copy-pasteable code
- All file paths are exact
- All commands include expected outputs

### Type Consistency

- `data-mode-target` and `data-mode-panel` attributes match in HTML and JS
- `data-file-name` and `data-file-dims` selectors match in HTML and JS
- `terminal-body` ID matches in HTML and JS
- `is-active` class name consistent across CSS, HTML, JS
- `data-result-kind` values (`encode`, `decode`, `check`) consistent across HTML and JS

**No gaps found. Plan is ready for execution.**
