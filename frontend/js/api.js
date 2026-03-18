const API = "https://exam-plan-tracker.onrender.com"; 

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function clearToken() {
  localStorage.removeItem("token");
}

function isLoggedIn() {
  return !!getToken();
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "index.html";
  }
}

function logout() {
  clearToken();
  window.location.href = "index.html";
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, {
    ...options,
    headers: { ...headers, ...(options.headers || {}) },
  });

  if (res.status === 401) {
    clearToken();
    window.location.href = "index.html";
    return;
  }

  const text = await res.text();
  let data = null;

  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      if (!res.ok) {
        throw new Error(text);
      }
      throw new Error("Invalid JSON response from server");
    }
  }

  if (!res.ok) throw new Error(data?.detail || text || "Request failed");
  return data;
}
