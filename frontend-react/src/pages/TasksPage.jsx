import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  getTasks,
  createTask,
  logTask,
  getActiveEnrollment,
  getExamDetail,
} from "../services/api";
import PageLayout from "../components/PageLayout";
import Card from "../components/Card";
import Button from "../components/Button";
import Badge from "../components/Badge";

const today = new Date().toISOString().split("T")[0];

const inputStyle = {
  width: "100%",
  padding: 10,
  border: "1px solid #d1d5db",
  borderRadius: 6,
  fontSize: 14,
  marginBottom: 12,
};

const labelStyle = {
  display: "block",
  fontSize: 13,
  fontWeight: 600,
  marginBottom: 4,
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  fontSize: 14,
};

const thStyle = {
  textAlign: "left",
  padding: "10px 12px",
  background: "#f9fafb",
  borderBottom: "1px solid #e5e7eb",
  fontWeight: 600,
};

const tdStyle = {
  padding: "10px 12px",
  borderBottom: "1px solid #f3f4f6",
};

const actionButtonStyle = {
  padding: "6px 12px",
  border: "none",
  borderRadius: 6,
  cursor: "pointer",
  fontSize: 14,
  fontWeight: 600,
};

export default function TasksPage() {
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState(today);
  const [tasks, setTasks] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState("");
  const [selectedTopicId, setSelectedTopicId] = useState("");
  const [plannedHours, setPlannedHours] = useState(1);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function initializePage() {
      setLoading(true);
      setError("");

      try {
        const enrollment = await getActiveEnrollment();
        const examDetail = await getExamDetail(enrollment.exam_id);
        const taskList = await getTasks(today);

        setSubjects(examDetail.subjects || []);
        setTasks(taskList || []);

        if (examDetail.subjects && examDetail.subjects.length > 0) {
          const firstSubject = examDetail.subjects[0];
          setSelectedSubjectId(String(firstSubject.id));
          if (firstSubject.topics && firstSubject.topics.length > 0) {
            setSelectedTopicId(String(firstSubject.topics[0].id));
          }
        }
      } catch (err) {
        if (err.message === "No active enrollment") {
          navigate("/setup", { replace: true });
          return;
        }
        setError(err.message || "Failed to load tasks");
      } finally {
        setLoading(false);
      }
    }

    initializePage();
  }, [navigate]);

  function handleDateChange(event) {
    setSelectedDate(event.target.value);
  }

  async function handleLoadTasks() {
    setLoading(true);
    setError("");

    try {
      const taskList = await getTasks(selectedDate);
      setTasks(taskList || []);
    } catch (err) {
      setError(err.message || "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  function handleSubjectChange(event) {
    const nextSubjectId = event.target.value;
    setSelectedSubjectId(nextSubjectId);

    const subject = subjects.find((item) => String(item.id) === nextSubjectId);
    if (subject && subject.topics.length > 0) {
      setSelectedTopicId(String(subject.topics[0].id));
    } else {
      setSelectedTopicId("");
    }
  }

  function handleTopicChange(event) {
    setSelectedTopicId(event.target.value);
  }

  function handleHoursChange(event) {
    setPlannedHours(event.target.value);
  }

  async function handleAddTask(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      await createTask({
        topic_id: Number(selectedTopicId),
        task_date: selectedDate,
        planned_hours: Number(plannedHours),
      });
      await handleLoadTasks();
    } catch (err) {
      setError(err.message || "Failed to add task");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDone(taskId) {
    setSubmitting(true);
    setError("");

    try {
      await logTask(taskId, { status: "COMPLETED" });
      await handleLoadTasks();
    } catch (err) {
      setError(err.message || "Failed to mark task done");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleSkip(taskId) {
    setSubmitting(true);
    setError("");

    try {
      await logTask(taskId, { status: "SKIPPED" });
      await handleLoadTasks();
    } catch (err) {
      setError(err.message || "Failed to skip task");
    } finally {
      setSubmitting(false);
    }
  }

  const selectedSubject = subjects.find(
    (subject) => String(subject.id) === selectedSubjectId
  );

  const availableTopics = selectedSubject ? selectedSubject.topics : [];

  function handleDoneClick(event) {
    const taskId = Number(event.currentTarget.dataset.taskId);
    handleDone(taskId);
  }

  function handleSkipClick(event) {
    const taskId = Number(event.currentTarget.dataset.taskId);
    handleSkip(taskId);
  }

  return (
    <PageLayout>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <h1 style={{ marginBottom: 20 }}>Tasks</h1>

          {error ? (
            <Card>
              <p style={{ color: "var(--danger)" }}>{error}</p>
            </Card>
          ) : null}

          <Card>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "end" }}>
              <div style={{ flex: "1 1 220px" }}>
                <label htmlFor="task-date" style={labelStyle}>
                  Date
                </label>
                <input
                  id="task-date"
                  type="date"
                  value={selectedDate}
                  onChange={handleDateChange}
                  style={inputStyle}
                />
              </div>
              <Button onClick={handleLoadTasks} disabled={submitting}>
                Load
              </Button>
            </div>
          </Card>

          <Card>
            <h2 style={{ marginBottom: 16 }}>Add Task</h2>
            <form onSubmit={handleAddTask}>
              <label htmlFor="subject" style={labelStyle}>
                Subject
              </label>
              <select
                id="subject"
                value={selectedSubjectId}
                onChange={handleSubjectChange}
                style={inputStyle}
              >
                <option value="">Select subject</option>
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>
                    {subject.name}
                  </option>
                ))}
              </select>

              <label htmlFor="topic" style={labelStyle}>
                Topic
              </label>
              <select
                id="topic"
                value={selectedTopicId}
                onChange={handleTopicChange}
                style={inputStyle}
              >
                <option value="">Select topic</option>
                {availableTopics.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.name}
                  </option>
                ))}
              </select>

              <label htmlFor="planned-hours" style={labelStyle}>
                Planned Hours
              </label>
              <input
                id="planned-hours"
                type="number"
                min="0.5"
                max="16"
                step="0.5"
                value={plannedHours}
                onChange={handleHoursChange}
                style={inputStyle}
              />

              <Button
                type="submit"
                disabled={submitting || !selectedSubjectId || !selectedTopicId}
              >
                {submitting ? "Loading..." : "Add Task"}
              </Button>
            </form>
          </Card>

          <Card>
            <h2 style={{ marginBottom: 16 }}>Task List</h2>
            {tasks.length === 0 ? (
              <p>No tasks for this date.</p>
            ) : (
              <div style={{ overflowX: "auto" }}>
                <table style={tableStyle}>
                  <thead>
                    <tr>
                      <th style={thStyle}>Subject</th>
                      <th style={thStyle}>Topic</th>
                      <th style={thStyle}>Planned Hrs</th>
                      <th style={thStyle}>Status</th>
                      <th style={thStyle}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tasks.map((task) => (
                      <tr key={task.id}>
                        <td style={tdStyle}>{task.subject_name}</td>
                        <td style={tdStyle}>{task.topic_name}</td>
                        <td style={tdStyle}>{task.planned_hours}</td>
                        <td style={tdStyle}>
                          {task.task_log ? (
                            <Badge status={task.task_log.status} />
                          ) : (
                            <span style={{ color: "var(--gray-500)" }}>Pending</span>
                          )}
                        </td>
                        <td style={tdStyle}>
                          {task.task_log ? null : (
                            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                              <button
                                type="button"
                                data-task-id={task.id}
                                onClick={handleDoneClick}
                                disabled={submitting}
                                style={{
                                  ...actionButtonStyle,
                                  background: "var(--success)",
                                  color: "white",
                                  opacity: submitting ? 0.6 : 1,
                                }}
                              >
                                ✓ Done
                              </button>
                              <button
                                type="button"
                                data-task-id={task.id}
                                onClick={handleSkipClick}
                                disabled={submitting}
                                style={{
                                  ...actionButtonStyle,
                                  background: "var(--danger)",
                                  color: "white",
                                  opacity: submitting ? 0.6 : 1,
                                }}
                              >
                                ✗ Skip
                              </button>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        </>
      )}
    </PageLayout>
  );
}
