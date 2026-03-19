import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  getExams,
  getExamDetail,
  enrollExam,
  getActiveEnrollment,
} from "../services/api";
import Card from "../components/Card";
import Button from "../components/Button";
import PageLayout from "../components/PageLayout";

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

function getTomorrowDate() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split("T")[0];
}

export default function SetupPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [exams, setExams] = useState([]);
  const [selectedExamId, setSelectedExamId] = useState("");
  const [examDate, setExamDate] = useState(getTomorrowDate());
  const [studyHoursPerDay, setStudyHoursPerDay] = useState(4);
  const [selectedExamDetail, setSelectedExamDetail] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function initializePage() {
      try {
        await getActiveEnrollment();
        navigate("/dashboard", { replace: true });
        return;
      } catch (err) {
        if (err.message !== "No active enrollment") {
          setError(err.message || "Failed to check enrollment");
          setLoading(false);
          return;
        }
      }

      try {
        const examList = await getExams();
        setExams(examList);
      } catch (err) {
        setError(err.message || "Failed to load exams");
      } finally {
        setLoading(false);
      }
    }

    initializePage();
  }, [navigate]);

  useEffect(() => {
    if (!selectedExamId) {
      setSelectedExamDetail(null);
      return;
    }

    async function loadExamDetail() {
      try {
        const detail = await getExamDetail(selectedExamId);
        setSelectedExamDetail(detail);
      } catch (err) {
        setError(err.message || "Failed to load exam details");
        setSelectedExamDetail(null);
      }
    }

    loadExamDetail();
  }, [selectedExamId]);

  function handleExamChange(event) {
    setSelectedExamId(event.target.value);
    setResult(null);
    setError("");
  }

  function handleExamDateChange(event) {
    setExamDate(event.target.value);
  }

  function handleStudyHoursChange(event) {
    setStudyHoursPerDay(event.target.value);
  }

  function handleGoToDashboard() {
    navigate("/dashboard");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setResult(null);

    try {
      const response = await enrollExam({
        exam_id: Number(selectedExamId),
        exam_date: examDate,
        study_hours_per_day: Number(studyHoursPerDay),
      });
      setResult(response);
    } catch (err) {
      setError(err.message || "Failed to create your plan");
    } finally {
      setSubmitting(false);
    }
  }

  const topicCount = selectedExamDetail
    ? selectedExamDetail.subjects.reduce((total, subject) => total + subject.topics.length, 0)
    : 0;

  const estimatedHours = selectedExamDetail
    ? selectedExamDetail.subjects.reduce(
        (total, subject) =>
          total + subject.topics.reduce((sum, topic) => sum + topic.estimated_hours, 0),
        0
      )
    : 0;

  return (
    <PageLayout>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <h1 style={{ marginBottom: 20 }}>Set Up Your Exam</h1>

          {error ? (
            <Card>
              <p style={{ color: "var(--danger)" }}>{error}</p>
            </Card>
          ) : null}

          <Card>
            <form onSubmit={handleSubmit}>
              <label htmlFor="exam_id" style={labelStyle}>
                Choose Exam
              </label>
              <select
                id="exam_id"
                value={selectedExamId}
                onChange={handleExamChange}
                required
                style={inputStyle}
              >
                <option value="">Select an exam</option>
                {exams.map((exam) => (
                  <option key={exam.id} value={exam.id}>
                    {exam.name}
                  </option>
                ))}
              </select>

              {selectedExamDetail ? (
                <p style={{ marginBottom: 16, color: "var(--gray-500)", fontSize: 14 }}>
                  {selectedExamDetail.subjects.length} subjects · {topicCount} topics ·{" "}
                  {estimatedHours} estimated hours
                </p>
              ) : null}

              <label htmlFor="exam_date" style={labelStyle}>
                Exam Date
              </label>
              <input
                id="exam_date"
                type="date"
                value={examDate}
                min={getTomorrowDate()}
                onChange={handleExamDateChange}
                required
                style={inputStyle}
              />

              <label htmlFor="study_hours_per_day" style={labelStyle}>
                Study Hours Per Day
              </label>
              <input
                id="study_hours_per_day"
                type="number"
                min="1"
                max="16"
                value={studyHoursPerDay}
                onChange={handleStudyHoursChange}
                required
                style={inputStyle}
              />

              <Button type="submit" disabled={submitting || !selectedExamId}>
                {submitting ? "Loading..." : "Generate My Plan"}
              </Button>
            </form>
          </Card>

          {result ? (
            <Card>
              <h2 style={{ marginBottom: 16 }}>Plan Summary</h2>
              <p style={{ marginBottom: 8 }}>
                Days remaining: <strong>{result.days_remaining}</strong>
              </p>
              <p style={{ marginBottom: 8 }}>
                Total syllabus hours: <strong>{result.total_syllabus_hours}</strong>
              </p>
              <p style={{ marginBottom: 16 }}>
                Required hours/day: <strong>{result.required_hours_per_day}</strong>
              </p>
              <Button onClick={handleGoToDashboard}>Go to Dashboard</Button>
            </Card>
          ) : null}
        </>
      )}
    </PageLayout>
  );
}
