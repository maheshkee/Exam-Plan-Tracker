import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { submitEndOfDay } from "../services/api";
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

const statGridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
  gap: 12,
  marginBottom: 20,
};

const statCardStyle = {
  background: "var(--gray-100)",
  border: "1px solid var(--gray-200)",
  borderRadius: 8,
  padding: 16,
};

export default function EndOfDayPage() {
  const navigate = useNavigate();
  const [targetDate, setTargetDate] = useState(today);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleDateChange(event) {
    setTargetDate(event.target.value);
  }

  async function handleGenerate() {
    setLoading(true);
    setError("");

    try {
      const summary = await submitEndOfDay(targetDate);
      setResult(summary);
    } catch (err) {
      setError(typeof err === "string" ? err : err?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  function handleViewHistory() {
    navigate("/history");
  }

  return (
    <PageLayout>
      <h1 style={{ marginBottom: 20 }}>End of Day Summary</h1>

      {error ? (
        <Card>
          <p style={{ color: "var(--danger)" }}>{error}</p>
        </Card>
      ) : null}

      <Card>
        <label htmlFor="target-date" style={labelStyle}>
          Summary Date
        </label>
        <input
          id="target-date"
          type="date"
          value={targetDate}
          onChange={handleDateChange}
          style={inputStyle}
        />
        <Button onClick={handleGenerate} disabled={loading}>
          {loading ? "Loading..." : "Generate Summary"}
        </Button>
      </Card>

      {result ? (
        <Card>
          <h2 style={{ marginBottom: 16 }}>Summary Result</h2>

          <div style={statGridStyle}>
            <div style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>Planned</p>
              <h3>{result.tasks_planned}</h3>
            </div>
            <div style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>Completed</p>
              <h3>{result.tasks_completed}</h3>
            </div>
            <div style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>Skipped</p>
              <h3>{result.tasks_skipped}</h3>
            </div>
            <div style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>Pending</p>
              <h3>{result.tasks_pending}</h3>
            </div>
          </div>

          <p style={{ marginBottom: 16 }}>
            {result.hours_planned} hrs planned / {result.hours_completed} hrs completed
          </p>

          <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
            <Badge status={result.day_status} />
            <Badge status={result.pace_status} />
          </div>

          <Button onClick={handleViewHistory}>View History</Button>
        </Card>
      ) : null}
    </PageLayout>
  );
}
