const styles = {
  AHEAD: { background: "#dcfce7", color: "#16a34a" },
  ON_TRACK: { background: "#fef9c3", color: "#b45309" },
  BEHIND: { background: "#fee2e2", color: "#dc2626" },
  COMPLETED: { background: "#dcfce7", color: "#16a34a" },
  PARTIAL: { background: "#fef9c3", color: "#b45309" },
  MISSED: { background: "#fee2e2", color: "#dc2626" },
  SKIPPED: { background: "#fee2e2", color: "#dc2626" },
};

export default function Badge({ status }) {
  const s = styles[status] || {
    background: "#e5e7eb",
    color: "#374151",
  };
  return (
    <span style={{
      ...s,
      display: "inline-block",
      padding: "3px 10px",
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 600,
    }}>
      {status}
    </span>
  );
}
