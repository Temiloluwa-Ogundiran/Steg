console.log("[STEG] app.js v3 loaded");

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
    { content: `filename: "${escapeHtml(data.filename)}"`, type: "variable" },
    { content: "" },
    { content: `<img class="terminal__preview" src="${escapeHtml(data.download_url)}" alt="Encoded image preview">`, type: "" },
    { content: "" },
    { content: `<div class="terminal__actions"><a class="terminal__link" href="${escapeHtml(data.download_url)}" download="${escapeHtml(data.filename)}">DOWNLOAD &gt;</a></div>`, type: "" },
  ];

  if (data.metrics) {
    lines.push({ content: "" });
    lines.push({ content: `// RAM: ${data.metrics.ram_percent}%  CPU: ${data.metrics.cpu_percent}%`, type: "comment" });
  }

  renderTerminal(lines);
}

function renderDecodeResult(data) {
  const lines = [];

  if (data.ok) {
    lines.push({ content: "STATUS ok", type: "success" });
    lines.push({ content: `message: "${escapeHtml(data.message)}"`, type: "string" });
    lines.push({ content: 'architecture: "dense"', type: "variable" });
  } else {
    lines.push({ content: "STATUS no_message", type: "keyword" });
    lines.push({ content: "" });
    lines.push({ content: escapeHtml(data.message || "No hidden message found."), type: "comment" });
  }

  if (data.metrics) {
    lines.push({ content: "" });
    lines.push({ content: `// RAM: ${data.metrics.ram_percent}%  CPU: ${data.metrics.cpu_percent}%`, type: "comment" });
  }

  renderTerminal(lines);
}

function renderCheckResult(data) {
  const statusType = data.hidden_data ? "success" : "comment";
  const statusText = data.hidden_data ? "true" : "false";

  const lines = [
    { content: "STATUS ok", type: "success" },
    { content: `hidden_data: ${statusText}`, type: statusType },
    { content: 'architecture: "dense"', type: "variable" },
  ];

  if (data.metrics) {
    lines.push({ content: "" });
    lines.push({ content: `// RAM: ${data.metrics.ram_percent}%  CPU: ${data.metrics.cpu_percent}%`, type: "comment" });
  }

  renderTerminal(lines);
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
});
