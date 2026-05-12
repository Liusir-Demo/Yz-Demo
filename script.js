const toggles = document.querySelectorAll(".script-toggle");

toggles.forEach((toggle) => {
  toggle.addEventListener("click", () => {
    const targetId = toggle.getAttribute("aria-controls");
    const panel = document.getElementById(targetId);
    if (!panel) return;

    const isExpanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!isExpanded));
    panel.hidden = isExpanded;
    toggle.textContent = isExpanded ? "查看主持提示" : "收起主持提示";
  });
});

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
