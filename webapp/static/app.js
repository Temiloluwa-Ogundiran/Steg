const modeButtons = document.querySelectorAll("[data-mode-target]");
const modePanels = document.querySelectorAll("[data-mode-panel]");
const resultPanel = document.getElementById("result-panel");
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

function renderResult(markup, state) {
  resultPanel.dataset.state = state;
  resultPanel.innerHTML = markup;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderError(message) {
  renderResult(
    `
      <p class="result-panel__kicker">ERROR</p>
      <h2 class="result-panel__headline">Processing halted.</h2>
      <p class="result-panel__copy">${escapeHtml(message)}</p>
    `,
    "error",
  );
}

function renderDecodeResult(data) {
  if (data.ok) {
    renderResult(
      `
        <p class="result-panel__kicker">DECODED MESSAGE</p>
        <h2 class="result-panel__headline">Message recovered.</h2>
        <p class="result-panel__message">${escapeHtml(data.message)}</p>
      `,
      "success",
    );
    return;
  }

  renderResult(
    `
      <p class="result-panel__kicker">NO MESSAGE</p>
      <h2 class="result-panel__headline">Nothing recovered.</h2>
      <p class="result-panel__copy">${escapeHtml(data.message)}</p>
    `,
    "missing",
  );
}

function renderCheckResult(data) {
  const state = data.hidden_data ? "found" : "missing";
  const headline = data.hidden_data ? "Hidden data found." : "No hidden data found.";
  renderResult(
    `
      <p class="result-panel__kicker">STRICT CHECK</p>
      <h2 class="result-panel__headline">${headline}</h2>
      <p class="result-panel__copy">${escapeHtml(data.message)}</p>
    `,
    state,
  );
}

function renderEncodeResult(data) {
  renderResult(
    `
      <p class="result-panel__kicker">ENCODE COMPLETE</p>
      <h2 class="result-panel__headline">Output generated.</h2>
      <img class="result-panel__preview" src="${data.download_url}" alt="Encoded image preview">
      <p class="result-panel__copy">The encoded image is ready for inspection or download.</p>
      <div class="result-panel__actions">
        <a class="result-link" href="${data.download_url}" download="${escapeHtml(data.filename)}">Download image</a>
      </div>
    `,
    "success",
  );
}

function setSubmitting(form, isSubmitting) {
  const button = form.querySelector('button[type="submit"]');
  if (!button) {
    return;
  }

  if (!button.dataset.defaultText) {
    button.dataset.defaultText = button.textContent;
  }

  button.disabled = isSubmitting;
  button.textContent = isSubmitting ? "Processing..." : button.dataset.defaultText;
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
  renderResult(
    `
      <p class="result-panel__kicker">WORKING</p>
      <h2 class="result-panel__headline">Processing request.</h2>
      <p class="result-panel__copy">The selected image and architecture are being evaluated now.</p>
    `,
    "idle",
  );

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
  const meta = input.closest(".field")?.querySelector("[data-file-name]");
  if (!meta) {
    return;
  }

  meta.textContent = input.files?.[0]?.name || "Awaiting image";
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
