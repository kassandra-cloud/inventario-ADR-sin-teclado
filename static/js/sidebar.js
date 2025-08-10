document.addEventListener("DOMContentLoaded", function () {
    const sidenav = document.querySelector(".sidenav");
    if (!sidenav) return;
    

    // Crear el boton con la flecha

    const sidenavTrigger = document.createElement("div");
    sidenavTrigger.classList.add("sidenav-trigger");
    document.body.appendChild(sidenavTrigger);

    // Mostrar menú al pasar el mouse por la flecha
    sidenavTrigger.addEventListener("mouseenter", function () {
        sidenav.classList.add("sidenav-open");
    });

    // Ocultar menú cuando el mouse sale del sidebar
    sidenav.addEventListener("mouseleave", function () {
        sidenav.classList.remove("sidenav-open");
    });
});
