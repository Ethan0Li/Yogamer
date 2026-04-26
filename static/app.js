// AI-GENERATED COMMENT:
// This frontend script was generated with AI assistance to control session launch
// and live pose catalog updates from the Flask backend API.
const startButton = document.getElementById("startSessionBtn");
const resetButton = document.getElementById("resetBtn");
const statusText = document.getElementById("sessionStatus");
const catalogList = document.getElementById("catalogList");

function formatSeconds(value) {
  const totalSeconds = Math.max(0, Math.floor(value));
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${mins}m ${secs}s`;
}

async function refreshCatalog() {
  const response = await fetch("/api/poses");
  const data = await response.json();
  catalogList.innerHTML = "";

  if (!data.poses || data.poses.length === 0) {
    const row = document.createElement("div");
    row.className = "pose-row";
    row.textContent = "No pose stats yet. Start a session.";
    catalogList.appendChild(row);
    return;
  }

  data.poses.forEach((item) => {
    const row = document.createElement("div");
    row.className = "pose-row";
    row.innerHTML = `<span>${item.pose}</span><span class="pose-time">${formatSeconds(item.total_seconds)}</span>`;
    catalogList.appendChild(row);
  });
}

async function refreshSessionStatus() {
  const response = await fetch("/api/session/status");
  const data = await response.json();
  const runtimeCommand = (data.runtime_command || []).join(" ");
  let text = data.running
    ? `Session running (${data.pose_hold_seconds}s hold) | ${data.runtime_source} | ${runtimeCommand}`
    : `Session idle | backend: ${data.backend_python} | ${data.runtime_source} | ${runtimeCommand}`;

  if (!data.running && data.last_exit) {
    const snippet = (data.last_exit.log_tail || "").split("\n").filter(Boolean).slice(-1)[0] || "See session_runtime.log";
    text += ` | last exit ${data.last_exit.exit_code}: ${snippet}`;
  }
  statusText.textContent = text;
}

startButton.addEventListener("click", async () => {
  startButton.disabled = true;
  try {
    await fetch("/api/session/start", { method: "POST" });
    await refreshSessionStatus();
  } finally {
    startButton.disabled = false;
  }
});

resetButton.addEventListener("click", async () => {
  await fetch("/api/poses/reset", { method: "POST" });
  await refreshCatalog();
});

setInterval(async () => {
  await refreshSessionStatus();
  await refreshCatalog();
}, 2500);

refreshSessionStatus();
refreshCatalog();
