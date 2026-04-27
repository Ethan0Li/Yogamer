// AI-GENERATED COMMENT:
// Catalog page behavior for loading and resetting pose totals.
const resetButton = document.getElementById("resetBtn");
const catalogList = document.getElementById("catalogList");

// AI-GENERATED COMMENT:
// Curated stock-photo mapping by pose so each catalog item has a visual.
const poseImageMap = {
  "Butterfly Pose": "/stock-image/Butterfy_pose.jpeg",
  "Child's Pose": "/stock-image/Childs_pose.jpeg",
  "Cobra Pose": "/stock-image/Cobra_pose.jpeg",
  "Downward Dog Pose": "/stock-image/Downward_Dog_pose.jpeg",
  "Ground Quad Stretch": "/stock-image/Ground_Quad_stretch.jpeg",
  "Seated Forward Fold": "/stock-image/Seated_Forward_Fold.jpeg",
};

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
    row.textContent = "No pose stats yet. Start a session from Home.";
    catalogList.appendChild(row);
    return;
  }

  data.poses.forEach((item) => {
    const row = document.createElement("div");
    row.className = "pose-row pose-card";
    const imageUrl = poseImageMap[item.pose] || "/stock-image/Butterfy_pose.jpeg";
    row.innerHTML = `
      <img class="pose-image" src="${imageUrl}" alt="${item.pose}" loading="lazy" />
      <div class="pose-meta">
        <span class="pose-name">${item.pose}</span>
        <span class="pose-time">${formatSeconds(item.total_seconds)}</span>
      </div>
    `;
    catalogList.appendChild(row);
  });
}

resetButton.addEventListener("click", async () => {
  await fetch("/api/poses/reset", { method: "POST" });
  await refreshCatalog();
});

setInterval(refreshCatalog, 2500);
refreshCatalog();
