// AQUI SE GUARDAN LAS VALIDACIONES DE LOS FORMULARIOS //
// validaciones.js

document.addEventListener('DOMContentLoaded', () => {
    const fechaEntregaInput = document.getElementById('fecha_entrega');

    if (fechaEntregaInput) {
        // Obtener la fecha actual en formato YYYY-MM-DD
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Evitar problemas de comparación por horas

        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // Meses en JavaScript son de 0-11
        const dd = String(today.getDate()).padStart(2, '0');

        const todayFormatted = `${yyyy}-${mm}-${dd}`;

        // Establecer la fecha mínima en el input
        fechaEntregaInput.setAttribute('min', todayFormatted);

        // Crear un mensaje de error (opcional)
        let errorMsg = document.createElement('p');
        errorMsg.style.color = 'red';
        errorMsg.style.display = 'none';
        errorMsg.textContent = 'La fecha de entrega no puede ser anterior al día de hoy.';
        fechaEntregaInput.insertAdjacentElement('afterend', errorMsg);

        // Validar cuando cambie la fecha
        fechaEntregaInput.addEventListener('change', (e) => {
            const selectedDate = new Date(e.target.value);
            selectedDate.setHours(0, 0, 0, 0); // Asegurar comparación en la misma zona horaria

            if (selectedDate < today) {
                errorMsg.style.display = 'block';
                e.target.value = todayFormatted; // Reestablecer al mínimo permitido
            } else {
                errorMsg.style.display = 'none';
            }
        });
    }
});
