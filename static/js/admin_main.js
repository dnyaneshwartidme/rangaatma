const body = document.body;
const desktopToggleBtn = document.getElementById("sidebarToggleDesktop");
const mobileToggleBtn = document.getElementById("sidebarToggleMobile");
let userToggled = false;

function applySidebarState() {
  if (!userToggled) {
    if (window.innerWidth < 992) {
      body.classList.add("sidebar-collapsed");
    } else {
      body.classList.remove("sidebar-collapsed");
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  applySidebarState();

  // 👉 Desktop toggle
  desktopToggleBtn.addEventListener("click", function () {
    body.classList.toggle("sidebar-collapsed");
    userToggled = true;
  });

  // 👉 Mobile toggle
  mobileToggleBtn.addEventListener("click", function () {
    body.classList.toggle("sidebar-collapsed");
    userToggled = true;
  });

  // 👉 Submenu toggle (optional)
  document.querySelectorAll(".has-submenu").forEach((menu) => {
    menu.addEventListener("click", (e) => {
      e.preventDefault();
      const nextSubmenu = menu.nextElementSibling;
      if (nextSubmenu.classList.contains("collapse")) {
        nextSubmenu.classList.toggle("show");
      }
    });
  });
});

window.addEventListener("resize", applySidebarState);
