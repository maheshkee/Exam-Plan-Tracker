import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  getDashboard,
  getAllEnrollments,
  switchExam,
} from "../services/api";
import PageLayout from "../components/PageLayout";
import Card from "../components/Card";
import Button from "../components/Button";
import Badge from "../components/Badge";

const statGridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: 16,
  marginBottom: 20,
};

const statBoxStyle = {
  background: "var(--gray-100)",
  border: "1px solid var(--gray-200)",
  borderRadius: 8,
  padding: 18,
};

export default function DashboardPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [switching, setSwitching] = useState(false);
  const [error, setError] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [enrollments, setEnrollments] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const [dashboardData, enrollmentData] = await Promise.all([
        getDashboard(),
        getAllEnrollments(),
      ]);
      setDashboard(dashboardData);
      setEnrollments(enrollmentData);
    } catch (err) {
      setError(typeof err === "string" ? err : err?.message || "Request failed");
    } finally {
      setLoading(false);
      setSwitching(false);
    }
  }

  function handleGoToTasks() {
    navigate("/tasks");
  }

  function handleGoToEndOfDay() {
    navigate("/end-of-day");
  }

  async function handleSwitchClick(event) {
    const enrollmentId = Number(event.currentTarget.dataset.enrollmentId);
    setSwitching(true);
    setError("");

    try {
      await switchExam(enrollmentId);
      await loadDashboard();
    } catch (err) {
      setError(typeof err === "string" ? err : err?.message || "Request failed");
      setSwitching(false);
    }
  }

  const completionWidth = dashboard
    ? `${Math.max(0, Math.min(100, dashboard.completion_percentage))}%`
    : "0%";

  return (
    <PageLayout>
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <Card>
          <p style={{ color: "var(--danger)" }}>{error}</p>
        </Card>
      ) : (
        <>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
            <div>
              <h1 style={{ marginBottom: 8 }}>{dashboard.exam_name}</h1>
              <p style={{ color: "var(--gray-500)" }}>
                Exam date: {dashboard.exam_date}
              </p>
            </div>
            <Badge status={dashboard.pace_status} />
          </div>

          <div style={statGridStyle}>
            <div style={statBoxStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>Days Left</p>
              <h2>{dashboard.days_remaining}</h2>
            </div>
            <div style={statBoxStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>
                Topics Completed
              </p>
              <h2>{dashboard.topics_completed}</h2>
            </div>
            <div style={statBoxStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>
                Hours Studied
              </p>
              <h2>{dashboard.hours_studied}</h2>
            </div>
            <div style={statBoxStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>
                Completion %
              </p>
              <h2>{dashboard.completion_percentage}%</h2>
            </div>
          </div>

          <Card>
            <h2 style={{ marginBottom: 12 }}>Progress</h2>
            <p style={{ marginBottom: 12, color: "var(--gray-500)" }}>
              {dashboard.topics_completed} of {dashboard.total_topics} topics (
              {dashboard.completion_percentage}%)
            </p>
            <div
              style={{
                background: "var(--gray-200)",
                borderRadius: 999,
                overflow: "hidden",
                height: 12,
              }}
            >
              <div
                style={{
                  width: completionWidth,
                  height: "100%",
                  background: "var(--primary)",
                  transition: "width 0.35s ease",
                }}
              />
            </div>
          </Card>

          <Card>
            <h2 style={{ marginBottom: 12 }}>Pace</h2>
            <p style={{ marginBottom: 8 }}>
              Required: <strong>{dashboard.required_hours_per_day} hrs/day</strong>
            </p>
            <p style={{ marginBottom: 16 }}>
              Actual: <strong>{dashboard.actual_hours_per_day} hrs/day</strong>
            </p>
            <Badge status={dashboard.pace_status} />
          </Card>

          <Card>
            <h2 style={{ marginBottom: 12 }}>Today's Summary</h2>
            <p style={{ marginBottom: 16 }}>
              Today: {dashboard.tasks_today} tasks planned, {dashboard.tasks_completed_today} completed
            </p>
            <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
              <Button onClick={handleGoToTasks}>Go to Tasks</Button>
              <Button variant="secondary" onClick={handleGoToEndOfDay}>
                End of Day
              </Button>
            </div>
          </Card>

          <Card>
            <h2 style={{ marginBottom: 16 }}>Switch Exam</h2>
            <div style={{ display: "grid", gap: 12 }}>
              {enrollments.map((enrollment) => (
                <div
                  key={enrollment.id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 12,
                    padding: 14,
                    borderRadius: 8,
                    border: enrollment.is_active
                      ? "1px solid var(--primary)"
                      : "1px solid var(--gray-200)",
                    background: enrollment.is_active
                      ? "rgba(79, 70, 229, 0.08)"
                      : "var(--white)",
                  }}
                >
                  <div>
                    <p style={{ fontWeight: 600, marginBottom: 4 }}>
                      Exam #{enrollment.exam_id}
                    </p>
                    <p style={{ fontSize: 13, color: "var(--gray-500)" }}>
                      Exam date: {enrollment.exam_date}
                    </p>
                  </div>

                  {enrollment.is_active ? (
                    <Badge status="ON_TRACK" />
                  ) : (
                    <Button
                      data-enrollment-id={enrollment.id}
                      onClick={handleSwitchClick}
                      disabled={switching}
                      variant="secondary"
                    >
                      {switching ? "Loading..." : "Switch"}
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </PageLayout>
  );
}
