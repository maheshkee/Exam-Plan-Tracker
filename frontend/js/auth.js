document.addEventListener("DOMContentLoaded", () => {
  if (isLoggedIn()) {
    checkEnrollmentAndRedirect();
    return;
  }

  const tabLogin = document.getElementById("tab-login");
  const tabRegister = document.getElementById("tab-register");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const messageDiv = document.getElementById("message");

  tabLogin.addEventListener("click", () => {
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
    messageDiv.classList.add("hidden");
  });

  tabRegister.addEventListener("click", () => {
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    messageDiv.classList.add("hidden");
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageDiv.classList.add("hidden");
    
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      setToken(data.access_token);
      await checkEnrollmentAndRedirect();
    } catch (err) {
      messageDiv.textContent = err.message;
      messageDiv.classList.remove("hidden");
    }
  });

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageDiv.classList.add("hidden");

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    try {
      await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      
      // Auto-login after registration
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      setToken(data.access_token);
      await checkEnrollmentAndRedirect();
    } catch (err) {
      messageDiv.textContent = err.message;
      messageDiv.classList.remove("hidden");
    }
  });
});

async function checkEnrollmentAndRedirect() {
  try {
    await apiFetch("/exams/my-enrollment");
    window.location.href = "dashboard.html";
  } catch (err) {
    window.location.href = "setup.html";
  }
}
