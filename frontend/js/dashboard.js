document.addEventListener("DOMContentLoaded", async () => {
  requireAuth();

  const errorMsg = document.getElementById("error-msg");
  const daysLeft = document.getElementById("days-left");
  const topicsDone = document.getElementById("topics-done");
  const hoursDone = document.getElementById("hours-done");
  const paceStatusText = document.getElementById("pace-status-text");
  const completionText = document.getElementById("completion-text");
  const completionPct = document.getElementById("completion-pct");
  const progressFill = document.getElementById("progress-fill");
  const todayTasksSummary = document.getElementById("today-tasks-summary");
  const reqHours = document.getElementById("req-hours");
  const actHours = document.getElementById("act-hours");
  const paceBadge = document.getElementById("pace-badge");

  try {
    const d = await apiFetch("/progress/dashboard");

    // Populate elements
    daysLeft.textContent = d.days_remaining;
    topicsDone.textContent = d.topics_completed;
    hoursDone.textContent = Math.round(d.hours_studied * 10) / 10;
    paceStatusText.textContent = d.pace_status;

    completionText.textContent = `${d.topics_completed} of ${d.total_topics} topics`;
    completionPct.textContent = `${d.completion_percentage}%`;
    progressFill.style.width = `${d.completion_percentage}%`;

    todayTasksSummary.textContent = `Today: ${d.tasks_today} tasks planned, ${d.tasks_completed_today} completed.`;

    reqHours.textContent = d.required_hours_per_day;
    actHours.textContent = d.actual_hours_per_day;

    paceBadge.textContent = d.pace_status;
    const badgeClass = `badge-${d.pace_status.toLowerCase().replace("_", "-")}`;
    paceBadge.className = `badge ${badgeClass}`;

  } catch (err) {
    errorMsg.textContent = err.message;
    errorMsg.classList.remove("hidden");
  }
});
