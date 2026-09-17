document.querySelectorAll(".reveal").forEach((button) => {
  button.addEventListener("click", () => {
    const input = document.getElementById(button.getAttribute("aria-controls"));
    const visible = input.type === "password";
    input.type = visible ? "text" : "password";
    button.textContent = visible ? "Masquer" : "Afficher";
    button.setAttribute("aria-pressed", String(visible));
  });
});
document.querySelectorAll("[data-demo-form]").forEach((form) => {
  // No credentials are sent or persisted while the backend is not connected.
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = form.querySelector("[data-form-status]");
    status.textContent = "Mode démonstration : le service d’authentification n’est pas encore connecté. Aucune donnée n’a été envoyée.";
    status.hidden = false;
  });
});

document.querySelectorAll("[data-demo-fields]").forEach((fields) => { fields.disabled = false; });
