// Mobile navigation
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.getElementById("site-nav");

if (navToggle && siteNav) {
  const setOpen = (open) => {
    navToggle.setAttribute("aria-expanded", String(open));
    siteNav.classList.toggle("is-open", open);
  };
  navToggle.addEventListener("click", () => setOpen(navToggle.getAttribute("aria-expanded") !== "true"));
  siteNav.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") setOpen(false); });
  matchMedia("(min-width: 52.01rem)").addEventListener("change", (e) => { if (e.matches) setOpen(false); });
}

// Contact form.
// No form-processing service is connected yet, so submitting opens the visitor's
// email app with the message pre-filled. To use a hosted form service instead,
// set the form's `action` and `method="post"` and remove the `data-mailto` attribute.
const form = document.querySelector("form[data-mailto]");

if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    const name = `${data.get("first_name")} ${data.get("last_name")}`.trim();
    const lines = [
      `Name: ${name}`,
      `Email: ${data.get("email")}`,
      `Phone: ${data.get("phone") || "-"}`,
      `Industry: ${data.get("industry") || "-"}`,
      "",
      data.get("message"),
    ];
    const subject = `Website enquiry from ${name}`;
    window.location.href =
      `mailto:${form.dataset.mailto}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;

    const note = form.querySelector(".form-note");
    if (note) note.textContent = `Your email app should open with your message ready to send. If it doesn't, email us at ${form.dataset.mailto}.`;
  });
}
