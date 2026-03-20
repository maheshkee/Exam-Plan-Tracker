import { useState, useEffect } from "react";
import { getHistory } from "../services/api";
import PageLayout from "../components/PageLayout";
import Card from "../components/Card";
import Badge from "../components/Badge";

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

const statRowStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: 16,
};

const statCardStyle = {
  background: "var(--gray-100)",
  border: "1px solid var(--gray-200)",
  borderRadius: 8,
  padding: 18,
};

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    setLoading(true);
    setError("");

    try {
      const historyData = await getHistory();
      setHistory(historyData || []);
    } catch (err) {
      setError(err?.message || String(err) || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const aheadDays = history.filter((entry) => entry.pace_status === "AHEAD").length;

  return (
    <PageLayout>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <h1 style={{ marginBottom: 20 }}>History</h1>

          {error ? (
            <Card>
              <p style={{ color: "var(--danger)" }}>{error}</p>
            </Card>
          ) : null}

          <div style={statRowStyle}>
            <Card style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>
                Days Tracked
              </p>
              <h2>{history.length}</h2>
            </Card>
            <Card style={statCardStyle}>
              <p style={{ color: "var(--gray-500)", fontSize: 13, marginBottom: 6 }}>
                Ahead Days
              </p>
              <h2>{aheadDays}</h2>
            </Card>
          </div>

          <Card>
            <h2 style={{ marginBottom: 16 }}>Progress History</h2>
            {history.length === 0 ? (
              <p>No history yet.</p>
            ) : (
              <div style={{ overflowX: "auto" }}>
                <table style={tableStyle}>
                  <thead>
                    <tr>
                      <th style={thStyle}>Date</th>
                      <th style={thStyle}>Topics Done</th>
                      <th style={thStyle}>Hours</th>
                      <th style={thStyle}>Pace</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((entry) => (
                      <tr key={entry.id}>
                        <td style={tdStyle}>{entry.snapshot_date}</td>
                        <td style={tdStyle}>{entry.topics_completed}</td>
                        <td style={tdStyle}>{entry.hours_completed}</td>
                        <td style={tdStyle}>
                          <Badge status={entry.pace_status} />
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
