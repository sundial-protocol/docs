document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.createElement("button");
    toggleButton.innerText = "Toggle Theme";
    toggleButton.className = "theme-toggle-inline";
  
    toggleButton.onclick = () => {
      const body = document.body;
      const current = body.classList.contains("dark-mode") ? "dark-mode" : "light-mode";
      const next = current === "dark-mode" ? "light-mode" : "dark-mode";
      body.classList.remove(current);
      body.classList.add(next);
      localStorage.setItem("theme", next);
    };
  
    // Insert the button next to "View page source"
    const sourceLink = document.querySelector("div.rst-other-versions, div.rst-footer-buttons, div.related, div.headerlink")?.parentElement;
    const pageActions = document.querySelector("div.rst-versions, div.related");
  
    const parent = document.querySelector("div[role='main'] > div");
    if (parent) parent.appendChild(toggleButton);
  
    // Apply saved theme
    const savedTheme = localStorage.getItem("theme") || "light-mode";
    document.body.classList.add(savedTheme);
  });
  