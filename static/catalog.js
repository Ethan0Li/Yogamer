// AI-GENERATED COMMENT:
// Catalog page behavior for loading and resetting pose totals.
const resetButton = document.getElementById("resetBtn");
const catalogList = document.getElementById("catalogList");

// AI-GENERATED COMMENT:
// Curated stock-photo mapping by pose so each catalog item has a visual.
const poseImageMap = {
  "Butterfly Pose": "https://images.pexels.com/photos/6311625/pexels-photo-6311625.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Child's Pose": "https://images.pexels.com/photos/3822525/pexels-photo-3822525.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Cobra Pose": "https://images.pexels.com/photos/4793308/pexels-photo-4793308.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Downward Dog Pose": "https://images.pexels.com/photos/3822688/pexels-photo-3822688.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Ground Quad Stretch": "https://images.pexels.com/photos/6453974/pexels-photo-6453974.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Seated Forward Fold": "https://images.pexels.com/photos/7900279/pexels-photo-7900279.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Bridge Pose": "https://images.pexels.com/photos/6453481/pexels-photo-6453481.jpeg?auto=compress&cs=tinysrgb&w=900",
  "Plank": "https://images.pexels.com/photos/2294354/pexels-photo-2294354.jpeg?auto=compress&cs=tinysrgb&w=900",
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
    const imageUrl = poseImageMap[item.pose] || "https://images.pexels.com/photos/3822906/pexels-photo-3822906.jpeg?auto=compress&cs=tinysrgb&w=900";
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
