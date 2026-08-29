const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);
let currentMarkdown = "";
let currentIssue = "test-plan";

async function api(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const data = await response.json().catch(() => ({ ok: false, error: { message: "Invalid server response." } }));
  if (!response.ok || data.ok === false) throw new Error(data.error?.message || "Request failed.");
  return data;
}

function toast(message, isError = false) {
  const node = $("#toast");
  node.textContent = message;
  node.className = `${isError ? "error " : ""}show`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { node.className = ""; }, 4200);
}

function showView(name) {
  $$(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === name));
  $$(".view").forEach((item) => item.classList.toggle("active", item.id === `view-${name}`));
  history.replaceState(null, "", `#${name}`);
  if (name === "settings") loadSettings();
}

$$(".nav-item").forEach((item) => item.addEventListener("click", () => showView(item.dataset.view)));
$$(".example").forEach((item) => item.addEventListener("click", () => { $("#prompt").value = item.textContent; $("#prompt").focus(); }));
$$(".reveal").forEach((button) => button.addEventListener("click", () => {
  const input = document.getElementById(button.dataset.target);
  input.type = input.type === "password" ? "text" : "password";
  button.textContent = input.type === "password" ? "Show" : "Hide";
}));

async function loadSettings() {
  try {
    const data = await api("/api/settings");
    $("#jira-url").value = data.jira_url || "";
    $("#jira-email").value = data.jira_email || "";
    $("#jira-token-note").textContent = data.jira_token_configured ? "A Jira token is saved locally." : "No token saved.";
    $("#openrouter-key-note").textContent = data.openrouter_api_key_configured ? "An OpenRouter key is saved locally." : "No key saved.";
  } catch (error) { toast(error.message, true); }
}

$("#settings-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  try {
    await api("/api/settings", { method: "POST", body: JSON.stringify({
      jira_url: $("#jira-url").value, jira_email: $("#jira-email").value,
      jira_token: $("#jira-token").value, openrouter_api_key: $("#openrouter-key").value,
    }) });
    $("#jira-token").value = ""; $("#openrouter-key").value = "";
    await loadSettings(); toast("Settings saved locally.");
  } catch (error) { toast(error.message, true); } finally { button.disabled = false; }
});

async function testConnection(service) {
  const button = $(`#test-${service}`), badge = $(`#${service}-badge`);
  button.disabled = true; badge.className = "badge neutral"; badge.textContent = "Testing…";
  try {
    const data = await api(`/api/connections/${service}/test`, { method: "POST", body: "{}" });
    badge.className = "badge good"; badge.textContent = "Connected"; toast(data.message);
  } catch (error) {
    badge.className = "badge bad"; badge.textContent = "Failed"; toast(error.message, true);
  } finally { button.disabled = false; }
}
$("#test-jira").addEventListener("click", () => testConnection("jira"));
$("#test-openrouter").addEventListener("click", () => testConnection("openrouter"));

$("#generate-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = $("#generate-button");
  button.disabled = true; $("#empty-state").classList.add("hidden"); $("#result-state").classList.add("hidden"); $("#loading-state").classList.remove("hidden");
  try {
    const data = await api("/api/generate", { method: "POST", body: JSON.stringify({ prompt: $("#prompt").value }) });
    currentMarkdown = data.markdown; currentIssue = data.issue_key;
    $("#markdown-output").textContent = currentMarkdown;
    $("#result-meta").textContent = `Created ${data.issue_key} · Saved to ${data.saved_to}${data.warnings.length ? ` · ${data.warnings.length} warning(s)` : ""}`;
    $("#download-button").disabled = false; $("#loading-state").classList.add("hidden"); $("#result-state").classList.remove("hidden");
    toast(`Test plan created for ${data.issue_key}.`);
  } catch (error) {
    $("#loading-state").classList.add("hidden"); $("#empty-state").classList.remove("hidden"); toast(error.message, true);
    if (/configure/i.test(error.message)) showView("settings");
  } finally { button.disabled = false; }
});

$("#download-button").addEventListener("click", () => {
  const blob = new Blob([currentMarkdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob), link = document.createElement("a");
  link.href = url; link.download = `${currentIssue}-test-plan.md`; link.click(); URL.revokeObjectURL(url);
});

showView(location.hash === "#settings" ? "settings" : "create");
