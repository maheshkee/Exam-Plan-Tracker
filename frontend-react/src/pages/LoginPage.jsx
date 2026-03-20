import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  login,
  register,
  getActiveEnrollment,
  setToken,
  isLoggedIn,
} from "../services/api";
import Card from "../components/Card";
import Button from "../components/Button";

const pageStyle = {
  minHeight: "100vh",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  padding: 16,
};

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

const tabBaseStyle = {
  flex: 1,
  padding: "10px 12px",
  border: "none",
  borderRadius: 6,
  fontSize: 14,
  fontWeight: 600,
  cursor: "pointer",
};

export default function LoginPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function checkExistingSession() {
      if (!isLoggedIn()) {
        setLoading(false);
        return;
      }

      const timeout = new Promise((_, reject) =>
        setTimeout(() => reject(new Error("timeout")), 5000)
      );

      try {
        await Promise.race([getActiveEnrollment(), timeout]);
        navigate("/dashboard", { replace: true });
      } catch (err) {
        setLoading(false);
      }
    }

    checkExistingSession();
  }, [navigate]);

  function handleShowLogin() {
    setMode("login");
    setError("");
  }

  function handleShowRegister() {
    setMode("register");
    setError("");
  }

  function handleEmailChange(event) {
    setEmail(event.target.value);
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  async function redirectAfterAuth() {
    try {
      await getActiveEnrollment();
      navigate("/dashboard", { replace: true });
    } catch (err) {
      if (err.message === "No active enrollment") {
        navigate("/setup", { replace: true });
        return;
      }
      throw err;
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (mode === "register" && password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setSubmitting(true);
    try {
      if (mode === "register") {
        await register(email, password);
      }

      const tokenData = await login(email, password);
      setToken(tokenData.access_token);
      await redirectAfterAuth();
    } catch (err) {
      setError(err.message || "Authentication failed");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div style={pageStyle}>Loading...</div>;
  }

  return (
    <div style={pageStyle}>
      <Card style={{ width: "100%", maxWidth: 400, marginBottom: 0 }}>
        <div style={{ textAlign: "center", marginBottom: 24 }}>
          <h1 style={{ fontSize: 28, marginBottom: 8 }}>📚 Exam Plan Tracker</h1>
          <p style={{ color: "var(--gray-500)", fontSize: 14 }}>
            Build your study plan and stay on track.
          </p>
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          <button
            type="button"
            onClick={handleShowLogin}
            style={{
              ...tabBaseStyle,
              background: mode === "login" ? "var(--primary)" : "var(--gray-200)",
              color: mode === "login" ? "white" : "var(--gray-700)",
            }}
          >
            Login
          </button>
          <button
            type="button"
            onClick={handleShowRegister}
            style={{
              ...tabBaseStyle,
              background: mode === "register" ? "var(--primary)" : "var(--gray-200)",
              color: mode === "register" ? "white" : "var(--gray-700)",
            }}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <label htmlFor="email" style={labelStyle}>
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={handleEmailChange}
            required
            style={inputStyle}
          />

          <label htmlFor="password" style={labelStyle}>
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={handlePasswordChange}
            required
            minLength={mode === "register" ? 8 : undefined}
            style={inputStyle}
          />

          <Button type="submit" fullWidth disabled={submitting}>
            {submitting
              ? "Loading..."
              : mode === "login"
                ? "Login"
                : "Register"}
          </Button>
        </form>

        {error ? (
          <p style={{ color: "var(--danger)", fontSize: 14, marginTop: 12 }}>
            {error}
          </p>
        ) : null}
      </Card>
    </div>
  );
}
