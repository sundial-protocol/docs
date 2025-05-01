document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("toggle-theme");
    if (!toggle) return;
  
    toggle.onclick = () => {
      const body = document.body;
      const current = body.classList.contains("dark-mode") ? "dark-mode" : "light-mode";
      const next = current === "dark-mode" ? "light-mode" : "dark-mode";
      body.classList.remove(current);
      body.classList.add(next);
      localStorage.setItem("theme", next);
    };
  
    // Restore saved theme
    const savedTheme = localStorage.getItem("theme") || "light-mode";
    document.body.classList.add(savedTheme);
  });
  