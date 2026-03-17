document.addEventListener("DOMContentLoaded", () => {
  requireAuth();

  const targetDateInput = document.getElementById("target-date");
  const generateBtn = document.getElementById("generate-btn");
  const errorMsg = document.getElementById("error-msg");
  const resultCard = document.getElementById("result-card");

  // Default to today
  targetDateInput.value = new Date().toISOString().split("T")[0];

  generateBtn.addEventListener("click", async () => {
    const targetDate = targetDateInput.value;
    errorMsg.classList.add("hidden");
    resultCard.classList.add("hidden");

    try {
      const data = await apiFetch(`/progress/end-of-day?target_date=${targetDate}`, {
        method: "POST"
      });

      // Populate results
      document.getElementById("result-title").textContent = `Summary for ${data.snapshot_date}`;
      document.getElementById("planned-tasks").textContent = data.tasks_planned;
      document.getElementById("completed-tasks").textContent = data.tasks_completed;
      document.getElementById("skipped-tasks").textContent = data.tasks_skipped;
      document.getElementById("pending-tasks").textContent = data.tasks_pending;
      document.getElementById("hours-planned").textContent = `${data.hours_planned}h`;
      document.getElementById("hours-completed").textContent = `${data.hours_completed}h`;

      const dayStatus = document.getElementById("day-status");
      dayStatus.textContent = `Day: ${data.day_status}`;
      dayStatus.className = `badge badge-${data.day_status === 'COMPLETED' ? 'ahead' : (data.day_status === 'PARTIAL' ? 'on-track' : 'behind')}`;

      const paceStatus = document.getElementById("pace-status");
      paceStatus.textContent = `Pace: ${data.pace_status}`;
      paceStatus.className = `badge badge-${data.pace_status.toLowerCase().replace('_', '-')}`;

      resultCard.classList.remove("hidden");

    } catch (err) {
      errorMsg.textContent = err.message;
      errorMsg.classList.remove("hidden");
    }
  });
});
