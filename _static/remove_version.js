document.addEventListener("DOMContentLoaded", function () {
    // Wait a short moment to let Read the Docs inject it
    setTimeout(() => {
      const versionEls = document.querySelectorAll(
        '.rst-versions, .rst-current-version, .wy-side-nav-search .rst-current-version, .wy-side-nav-search div:nth-child(1)'
      );
      versionEls.forEach(el => el.remove());
    }, 250); // 250ms delay should be enough
  });
  