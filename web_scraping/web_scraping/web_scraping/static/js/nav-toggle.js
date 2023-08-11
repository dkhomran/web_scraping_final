let toggleIcon = document.querySelector("#toggle-icon");
let toggleContainer = document.querySelector(".topnav-phone");

toggleIcon.addEventListener("click", (eo) => {
  toggleContainer.classList.toggle("active");
});
