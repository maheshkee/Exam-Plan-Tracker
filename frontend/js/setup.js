document.addEventListener("DOMContentLoaded", async () => {
  requireAuth();

  const setupForm = document.getElementById("setup-form");
  const examSelect = document.getElementById("exam-select");
  const syllabusInfo = document.getElementById("syllabus-info");
  const setupCard = document.getElementById("setup-card");
  const resultCard = document.getElementById("result-card");
  const planSummary = document.getElementById("plan-summary");
  const errorMsg = document.getElementById("error-msg");

  // Set min date for exam to tomorrow
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  document.getElementById("exam-date").min = tomorrow.toISOString().split("T")[0];

  // 1. Check if already enrolled
  try {
    await apiFetch("/exams/my-enrollment");
    window.location.href = "dashboard.html";
    return;
  } catch (err) {
    // Not enrolled, continue
  }

  // 2. Load exams
  try {
    const exams = await apiFetch("/exams");
    exams.forEach(exam => {
      const option = document.createElement("option");
      option.value = exam.id;
      option.textContent = exam.name;
      examSelect.appendChild(option);
    });
  } catch (err) {
    errorMsg.textContent = "Failed to load exams.";
    errorMsg.classList.remove("hidden");
  }

  // 3. Show syllabus info on exam change
  examSelect.addEventListener("change", async () => {
    const examId = examSelect.value;
    if (!examId) return;

    try {
      const exam = await apiFetch(`/exams/${examId}`);
      let totalTopics = 0;
      let totalHours = 0;
      exam.subjects.forEach(s => {
        totalTopics += s.topics.length;
        s.topics.forEach(t => totalHours += t.estimated_hours);
      });

      syllabusInfo.innerHTML = `
        <strong>Syllabus Summary:</strong><br>
        • ${exam.subjects.length} Subjects<br>
        • ${totalTopics} Topics<br>
        • ${totalHours} Estimated Study Hours
      `;
      syllabusInfo.classList.remove("hidden");
    } catch (err) {
      console.error(err);
    }
  });

  // 4. Handle form submission
  setupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorMsg.classList.add("hidden");

    const exam_id = parseInt(examSelect.value);
    const exam_date = document.getElementById("exam-date").value;
    const study_hours_per_day = parseFloat(document.getElementById("study-hours").value);

    try {
      const res = await apiFetch("/exams/enroll", {
        method: "POST",
        body: JSON.stringify({ exam_id, exam_date, study_hours_per_day })
      });

      // Show success
      setupCard.classList.add("hidden");
      planSummary.innerHTML = `
        <div class="stat-grid" style="margin-top: 20px;">
          <div class="stat-box">
            <div class="value">${res.days_remaining}</div>
            <div class="label">Days Left</div>
          </div>
          <div class="stat-box">
            <div class="value">${res.required_hours_per_day}</div>
            <div class="label">Hours/Day Required</div>
          </div>
        </div>
        <p style="text-align: center; color: #4b5563;">
          You need to study <strong>${res.required_hours_per_day} hours per day</strong> 
          to complete the <strong>${res.total_syllabus_hours} hour</strong> syllabus before your exam.
        </p>
      `;
      resultCard.classList.remove("hidden");

    } catch (err) {
      errorMsg.textContent = err.message;
      errorMsg.classList.remove("hidden");
    }
  });
});
