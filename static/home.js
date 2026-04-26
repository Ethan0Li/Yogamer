// AI-GENERATED COMMENT:
// Home page behavior for starting a session and showing runtime status.
const startButton = document.getElementById("startSessionBtn");
const statusText = document.getElementById("sessionStatus");

async function refreshSessionStatus() {
  const response = await fetch("/api/session/status");
  const data = await response.json();
  statusText.textContent = data.running
    ? `Session running (tracking starts after ${data.pose_hold_seconds}s hold)`
    : "Session idle";
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

setInterval(refreshSessionStatus, 2500);
refreshSessionStatus();
