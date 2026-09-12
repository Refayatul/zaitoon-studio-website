// Zaitoon Studio — Public Site Interactive Controller

document.addEventListener("DOMContentLoaded", () => {
  // Mobile Nav Toggle
  const mobileToggle = document.querySelector(".mobile-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
      const isOpen = navLinks.classList.contains("open");
      mobileToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      mobileToggle.innerHTML = isOpen ? "✕" : "☰";
    });

    // Close nav on link click
    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        mobileToggle.innerHTML = "☰";
      });
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const targetElem = document.querySelector(targetId);
      if (targetElem) {
        e.preventDefault();
        targetElem.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Set current year in footer
  const yearSpan = document.getElementById("currentYear");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
});
