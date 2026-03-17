document.addEventListener("DOMContentLoaded", async () => {
  requireAuth();

  let selectedDate = new Date().toISOString().split("T")[0];
  let subjects = [];

  const taskDateInput = document.getElementById("task-date");
  taskDateInput.value = selectedDate;

  const errorMsg = document.getElementById("error-msg");
  const subjectSelect = document.getElementById("subject-select");
  const topicSelect = document.getElementById("topic-select");
  const taskListBody = document.getElementById("task-list-body");
  const noTasksDiv = document.getElementById("no-tasks");
  const taskTableWrap = document.getElementById("task-table-wrap");

  // Load subjects from enrolled exam
  async function loadSubjects() {
    try {
      const enrollment = await apiFetch("/exams/my-enrollment");
      const exam = await apiFetch(`/exams/${enrollment.exam_id}`);
      subjects = exam.subjects;
      subjectSelect.innerHTML = '<option value="">Select subject...</option>';
      subjects.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s.id;
        opt.textContent = s.name;
        subjectSelect.appendChild(opt);
      });
    } catch (err) {
      errorMsg.textContent = "Failed to load subjects: " + err.message;
      errorMsg.classList.remove("hidden");
    }
  }

  // When subject changes, populate topics
  subjectSelect.addEventListener("change", () => {
    const subjectId = parseInt(subjectSelect.value);
    const subject = subjects.find(s => s.id === subjectId);
    topicSelect.innerHTML = '<option value="">Select topic...</option>';
    if (subject) {
      subject.topics.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.textContent = `${t.name} (${t.estimated_hours}h)`;
        topicSelect.appendChild(opt);
      });
    }
  });

  // Load tasks for selected date
  async function loadTasks() {
    try {
      errorMsg.classList.add("hidden");
      const tasks = await apiFetch(`/tasks?task_date=${selectedDate}`);
      renderTasks(tasks);
    } catch (err) {
      errorMsg.textContent = "Failed to load tasks: " + err.message;
      errorMsg.classList.remove("hidden");
    }
  }

  function renderTasks(tasks) {
    taskListBody.innerHTML = "";
    if (tasks.length === 0) {
      noTasksDiv.classList.remove("hidden");
      taskTableWrap.classList.add("hidden");
      return;
    }

    noTasksDiv.classList.add("hidden");
    taskTableWrap.classList.remove("hidden");

    tasks.forEach(task => {
      const tr = document.createElement("tr");
      
      let statusHtml = '<span style="color: #9ca3af;">Pending</span>';
      let actionHtml = `
        <div class="action-btns">
          <button onclick="logTask(${task.id}, 'COMPLETED')" class="btn btn-success" style="padding: 4px 8px; font-size: 12px;">✓ Done</button>
          <button onclick="logTask(${task.id}, 'SKIPPED')" class="btn btn-danger" style="padding: 4px 8px; font-size: 12px;">✗ Skip</button>
        </div>
      `;

      if (task.task_log) {
        statusHtml = `<span class="status-badge status-${task.task_log.status}">${task.task_log.status}</span>`;
        actionHtml = `<span style="font-size: 12px; color: #6b7280;">Logged at ${new Date(task.task_log.updated_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>`;
      }

      tr.innerHTML = `
        <td>${task.subject_name}</td>
        <td>${task.topic_name}</td>
        <td>${task.planned_hours}h</td>
        <td>${statusHtml}</td>
        <td>${actionHtml}</td>
      `;
      taskListBody.appendChild(tr);
    });
  }

  // Global log task function
  window.logTask = async (taskId, status) => {
    try {
      await apiFetch(`/tasks/${taskId}/log`, {
        method: "PATCH",
        body: JSON.stringify({ status })
      });
      loadTasks();
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  // Load button
  document.getElementById("load-btn").addEventListener("click", () => {
    selectedDate = taskDateInput.value;
    loadTasks();
  });

  // Add task form
  document.getElementById("add-task-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const topic_id = parseInt(topicSelect.value);
    const task_date = selectedDate;
    const planned_hours = parseFloat(document.getElementById("planned-hours").value);
    
    try {
      await apiFetch("/tasks", {
        method: "POST",
        body: JSON.stringify({ topic_id, task_date, planned_hours })
      });
      loadTasks();
    } catch (err) {
      alert("Error adding task: " + err.message);
    }
  });

  await loadSubjects();
  await loadTasks();
});
