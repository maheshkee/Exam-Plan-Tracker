const API_BASE = import.meta.env.VITE_API_URL ||
                 "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

export function isLoggedIn() {
  return !!getToken();
}

export async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...headers, ...(options.headers || {}) },
  });

  if (res.status === 401) {
    clearToken();
    window.location.href = "/";
    return;
  }

  const data = await res.json();
  if (!res.ok) {
    const detail = typeof data.detail === "string"
      ? data.detail
      : JSON.stringify(data.detail) || "Request failed";
    throw new Error(detail);
  }
  return data;
}

export const login = (email, password) =>
  apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const register = (email, password) =>
  apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const getMe = () => apiFetch("/auth/me");

export const getExams = () => apiFetch("/exams");
export const getExamDetail = (id) => apiFetch(`/exams/${id}`);
export const enrollExam = (data) =>
  apiFetch("/exams/enroll", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const getActiveEnrollment = () =>
  apiFetch("/exams/my-enrollment");
export const getAllEnrollments = () =>
  apiFetch("/exams/my-enrollments");
export const switchExam = (userExamId) =>
  apiFetch(`/exams/switch/${userExamId}`, { method: "POST" });

export const getTasks = (date) =>
  apiFetch(`/tasks?task_date=${date}`);
export const createTask = (data) =>
  apiFetch("/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });
export const logTask = (taskId, data) =>
  apiFetch(`/tasks/${taskId}/log`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });

export const getDashboard = () =>
  apiFetch("/progress/dashboard");
export const getHistory = () =>
  apiFetch("/progress/history");
export const submitEndOfDay = (date) =>
  apiFetch(`/progress/end-of-day?target_date=${date}`, {
    method: "POST",
  });
