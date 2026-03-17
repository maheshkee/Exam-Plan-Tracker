document.addEventListener("DOMContentLoaded", async () => {
  requireAuth();

  const errorMsg = document.getElementById("error-msg");
  const totalDays = document.getElementById("total-days");
  const streakCount = document.getElementById("streak-count");
  const historyListBody = document.getElementById("history-list-body");
  const noHistoryDiv = document.getElementById("no-history");
  const historyTableWrap = document.getElementById("history-table-wrap");

  try {
    const history = await apiFetch("/progress/history");
    
    if (history.length === 0) {
      noHistoryDiv.classList.remove("hidden");
      historyTableWrap.classList.add("hidden");
      totalDays.textContent = "0";
      streakCount.textContent = "0";
      return;
    }

    noHistoryDiv.classList.add("hidden");
    historyTableWrap.classList.remove("hidden");

    totalDays.textContent = history.length;
    let aheadCount = 0;

    history.forEach(item => {
      if (item.pace_status === "AHEAD") aheadCount++;

      const tr = document.createElement("tr");
      const paceClass = `badge-${item.pace_status.toLowerCase().replace('_', '-')}`;
      
      tr.innerHTML = `
        <td>${item.snapshot_date}</td>
        <td>${item.topics_completed}</td>
        <td>${item.hours_completed}h</td>
        <td><span class="badge ${paceClass}">${item.pace_status}</span></td>
      `;
      historyListBody.appendChild(tr);
    });

    streakCount.textContent = aheadCount;

  } catch (err) {
    errorMsg.textContent = err.message;
    errorMsg.classList.remove("hidden");
  }
});
