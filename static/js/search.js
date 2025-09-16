// Función para verificar si hay resultados en la tabla y mostrar feedback
function checkForResults() {
    const tableBody = document.querySelector("table tbody");

    if (!tableBody) {
        showFeedback(" No se encontró la tabla.", true);
        return false;
    }

    // Obtener filas válidas (evitar contar filas vacías)
    const rows = [...tableBody.querySelectorAll("tr")].filter(row => row.innerText.trim() !== "");

    // Determinar si la tabla tiene datos
    const hasResults = rows.length > 0;

    // Mostrar feedback directamente desde aquí
    showFeedback(
        hasResults ? `La tabla tiene ${rows.length} fila(s).` : " La tabla está vacía.",
        !hasResults
    );

    return hasResults;
}

// Función para mostrar el mensaje de feedback con mejoras
function showFeedback(message, isError = false) {
    // Evitar actualizar si el mensaje no ha cambiado
    if (localStorage.getItem("scanFeedback") === message) return;

    // Guardar en localStorage
    localStorage.setItem("scanFeedback", message);
    localStorage.setItem("scanFeedbackTime", new Date().getTime());
    localStorage.setItem("isError", isError);

    // Mostrar en la página
    displayFeedbackMessage(message, isError);
}

// Función para mostrar el mensaje en la página (ajustada para error de 9s)
function displayFeedbackMessage(message, isError = false) {
    const existingFeedback = document.getElementById("scanFeedbackMessage");
    if (existingFeedback) {
        existingFeedback.remove();
    }

    const feedbackDiv = document.createElement("div");
    feedbackDiv.id = "scanFeedbackMessage";
    feedbackDiv.textContent = message;
    feedbackDiv.style.position = "fixed";
    feedbackDiv.style.top = "50%";
    feedbackDiv.style.left = "50%";
    feedbackDiv.style.transform = "translate(-50%, -50%)";
    feedbackDiv.style.padding = "15px 25px";
    feedbackDiv.style.backgroundColor = isError ? "#ef4444" : "#4a5568";
    feedbackDiv.style.color = "white";
    feedbackDiv.style.borderRadius = "8px";
    feedbackDiv.style.zIndex = "1000";
    feedbackDiv.style.fontSize = "16px";
    feedbackDiv.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
    feedbackDiv.style.textAlign = "center";

    document.body.appendChild(feedbackDiv);

    // Configurar tiempo de desaparición: 9 segundos para errores, 3 segundos para normales
    const DISPLAY_DURATION = isError ? 9000 : 3000;

    setTimeout(() => {
        if (feedbackDiv && feedbackDiv.parentNode) {
            feedbackDiv.remove();
        }
    }, DISPLAY_DURATION);
}

// Esta función se ejecuta solo en el HOME
// Redirige la búsqueda a /buscar-global/ para que Django encuentre en todos los modelos
// Función principal de búsqueda manual
function submitSearch(event) {
    event.preventDefault();

    const searchInput = document.getElementById("search");
    let searchValue = searchInput.value.trim().toLowerCase(); // Convertir a minúsculas para búsqueda insensible a mayúsculas/minúsculas
    if (!searchValue) return;

    // Mostrar el primer mensaje de feedback
    showFeedback(`Buscando: ${searchValue}`);

    // Detectar si estamos en home
    const isHome = window.location.pathname === "/" || window.location.pathname === "/home/";

    // Crear un nuevo formulario temporal
    const tempForm = document.createElement("form");
    tempForm.method = "GET";
    tempForm.action = isHome ? "/buscar-global/" : window.location.pathname;

    // Agrega el campo de búsqueda
    const hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "search";
    hiddenInput.value = searchValue;
    tempForm.appendChild(hiddenInput);

    // Si hay filtro de ubicación visible en la página, también lo envía
    const filterUbicacion = document.getElementById("filter_ubicacion");
    if (filterUbicacion) {
        const ubicacionInput = document.createElement("input");
        ubicacionInput.type = "hidden";
        ubicacionInput.name = "filter_ubicacion";
        ubicacionInput.value = filterUbicacion.value;
        tempForm.appendChild(ubicacionInput);
    }

    // Almacenar el valor de búsqueda para verificar después
    localStorage.setItem("lastSearchValue", searchValue);

    // Pequeño retraso antes de enviar el formulario para que el mensaje sea visible
    setTimeout(() => {
        // Limpiar el input
        searchInput.value = "";

        // Enviar el formulario
        document.body.appendChild(tempForm);
        tempForm.submit();
        document.body.removeChild(tempForm);
    }, 2000); // Espera 2 segundos antes de recargar
}

// Esta función se ejecuta en páginas como /notebooks/, /mini_pc/, etc.
// Solo busca dentro del módulo actual, no redirige a /buscar-global/
function submitLocalSearch(event) {
    event.preventDefault();

    const searchInput = document.getElementById("search");
    let searchValue = searchInput.value.trim().toLowerCase();
    if (!searchValue) return;

    showFeedback(`Buscando local: ${searchValue}`);

    // Formulario que envía la búsqueda por GET a la misma página
    const form = document.createElement("form");
    form.method = "GET";
    form.action = window.location.pathname;

    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "search";
    input.value = searchValue;
    form.appendChild(input);

    // Guarda para feedback en caso de que no haya resultados
    localStorage.setItem("lastSearchValue", searchValue);

    setTimeout(() => {
        searchInput.value = "";
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    }, 500);
}


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const searchButton = searchInput.nextElementSibling;

    // Verificar resultados después de que la página carga
    const lastSearchValue = localStorage.getItem("lastSearchValue");
    if (lastSearchValue) {
        // Esperar a que la página esté completamente cargada
        setTimeout(() => {
            if (!checkForResults()) {
                showFeedback("Dispositivo no encontrado", true);
            }
            localStorage.removeItem("lastSearchValue");
        }, 1000); // Espera 1 segundo después de la carga
    }

    // Configuración del escáner
    let scanBuffer = "";
    let scanTimeout = null;

    // Detector de entrada del escáner
    document.addEventListener("keypress", function (e) {
        if (
            !e.target.isContentEditable &&
            (e.target === searchInput ||
                !(e.target instanceof HTMLInputElement))
        ) {
            if (scanTimeout) {
                clearTimeout(scanTimeout);
            }

            // Cuando se presiona "Enter", se detecta que es escaneo
            if (e.key === "Enter") {
                e.preventDefault();
                if (scanBuffer) {
                    // Convertir a minúsculas para una búsqueda insensible a capitalización
                    scanBuffer = scanBuffer.toLowerCase();

                    // Eliminar letras al inicio del código (si existen 3 letras), solo para la búsqueda con escáner
                    if (/^[A-Za-z]{3}/.test(scanBuffer)) {
                        scanBuffer = scanBuffer.replace(/^[A-Za-z]{3}/, '');
                    }

                    // Actualizar el valor del input con el código limpio
                    searchInput.value = scanBuffer;
                    
                    if (window.location.pathname === "/" || window.location.pathname === "/home/") {
                        submitSearch(new Event("submit"));
                    } else {
                        submitLocalSearch(new Event("submit"));
                    }
                    scanBuffer = "";
                }
                return;
            }

            if (e.target === searchInput) {
                scanBuffer = searchInput.value + e.key;
            } else {
                e.preventDefault();
                scanBuffer += e.key;
                searchInput.value = scanBuffer;
            }
        }
    });

    // Limpiar el buffer si hay una pausa muy larga entre caracteres
    document.addEventListener("keyup", function (e) {
        if (e.key !== "Enter") {
            if (scanTimeout) {
                clearTimeout(scanTimeout);
            }

            scanTimeout = setTimeout(() => {
                scanBuffer = "";
            }, 50);
        }
    });
});

// **********************************************************************************************************

// Función para mostrar todos los registros
function showAllRecords(event) {
    if (event) {
        event.preventDefault();
    }

    // Limpiar el input de búsqueda
    const searchInput = document.getElementById("search");
    if (searchInput) {
        searchInput.value = "";
    }

    // Limpiar localStorage
    localStorage.removeItem("lastSearchValue");
    localStorage.removeItem("scanFeedback");
    localStorage.removeItem("scanFeedbackTime");
    localStorage.removeItem("isError");

    // Mostrar mensaje de feedback
    showFeedback("Mostrando todos los registros");

    // Forzar la recarga de la página con la URL base
    setTimeout(() => {
        // Usar window.location.replace para evitar entradas en el historial
        window.location.search = "";
    }, 500);
}

// Asegurar que la función está disponible globalmente
window.showAllRecords = showAllRecords;


// ************************   espacio para búsqueda por fecha***************************
document.addEventListener("DOMContentLoaded", function () {
    // Capturar elementos de filtro
    const usuarioSelect = document.getElementById("usuario");
    const fechaInicioInput = document.getElementById("fecha_inicio");
    const fechaFinInput = document.getElementById("fecha_fin");

    // Función para redirigir con los parámetros seleccionados
    function updateFilters() {
        const params = new URLSearchParams(window.location.search);
        
        if (usuarioSelect && usuarioSelect.value) {
            params.set("usuario", usuarioSelect.value);
        } else {
            params.delete("usuario");
        }

        if (fechaInicioInput && fechaInicioInput.value) {
            params.set("fecha_inicio", fechaInicioInput.value);
        } else {
            params.delete("fecha_inicio");
            
        }

        if (fechaFinInput && fechaFinInput.value) {
            params.set("fecha_fin", fechaFinInput.value);
        } else {
            params.delete("fecha_fin");
        }

        // actualizar la url sin recargar la pagina
        const newUrl = `${window.location.pathname}?${params.toString()}`;
        history.replaceState(null, "", newUrl);
    }
    
    // solo agregar event listeners si los elementos existen
    if (usuarioSelect) usuarioSelect.addEventListener("change", updateFilters);
    if (fechaInicioInput) fechaInicioInput.addEventListener("input", updateFilters);
    if (fechaFinInput) fechaFinInput.addEventListener("input", updateFilters);

});

// ************************   espacio para busqueda por fecha***************************


