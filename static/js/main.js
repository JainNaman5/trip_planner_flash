/* main.js – Trip Planner India */
(function () {
  "use strict";

  /* ── Theme ── */
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");
  const icon   = document.getElementById("themeIcon");

  function applyTheme(dark) {
    root.setAttribute("data-theme", dark ? "dark" : "light");
    if (icon) icon.textContent = dark ? "light_mode" : "dark_mode";
    localStorage.setItem("theme", dark ? "dark" : "light");
  }

  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved ? saved === "dark" : prefersDark);

  if (toggle) {
    toggle.addEventListener("click", () => {
      applyTheme(root.getAttribute("data-theme") !== "dark");
    });
  }

  /* ── Navbar scroll shrink ── */
  const topBar = document.getElementById("topBar");
  if (topBar) {
    window.addEventListener("scroll", () => {
      topBar.classList.toggle("scrolled", window.scrollY > 40);
    }, { passive: true });
  }

  /* ── Animate cards on scroll ── */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll(
    ".result-card, .result-featured, .stay-card, .transport-card, .featured-card, .itinerary-row"
  ).forEach(el => {
    el.classList.add("fade-up");
    observer.observe(el);
  });

  /* ── Plan button loading state ── */
  const form   = document.getElementById("tripForm");
  const planBtn = document.getElementById("planBtn");
  if (form && planBtn) {
    form.addEventListener("submit", () => {
      planBtn.disabled = true;
      planBtn.querySelector("span:first-child").textContent = "Planning…";
    });
  }

  /* ── Smooth scroll for anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: "smooth" }); }
    });
  });
})();
