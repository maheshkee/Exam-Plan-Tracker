import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../services/api";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    clearToken();
    navigate("/");
  }

  return (
    <nav style={{
      background: "var(--primary)",
      padding: "12px 24px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    }}>
      <Link to="/dashboard" style={{
        color: "white",
        fontWeight: 700,
        fontSize: 16,
        textDecoration: "none",
      }}>
        📚 Exam Plan Tracker
      </Link>
      <div style={{ display: "flex", gap: 16 }}>
        {["Dashboard", "Tasks", "History"].map((item) => (
          <Link
            key={item}
            to={`/${item.toLowerCase()}`}
            style={{
              color: "white",
              textDecoration: "none",
              fontSize: 14,
              opacity: 0.85,
            }}
          >
            {item}
          </Link>
        ))}
        <button
          onClick={handleLogout}
          style={{
            background: "transparent",
            border: "1px solid rgba(255,255,255,0.5)",
            color: "white",
            padding: "4px 12px",
            borderRadius: 4,
            cursor: "pointer",
            fontSize: 14,
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
