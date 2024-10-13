// main.js

document.addEventListener('DOMContentLoaded', function () {
    // Constante de días marcados
    const markedDates = [
        "2024-10-20",
        "2024-10-25",
        "2024-10-10"
    ];

    flatpickr("#date-picker", {
        dateFormat: "Y-m-d",
        mode: "range",
        onChange: function(selectedDates, dateStr, instance) {
            // Solo hacer algo cuando el usuario haya seleccionado 2 fechas (rango completo)
            if (selectedDates.length === 2) {
                const startDate = selectedDates[0];
                const endDate = selectedDates[1];

                // Calcular un día antes del inicio y un día después del fin
                const previousDay = new Date(startDate);
                const nextDay = new Date(endDate);

                previousDay.setDate(startDate.getDate() - 1);
                nextDay.setDate(endDate.getDate() + 1);

                // Establecer el nuevo rango (un día antes y un día después del rango seleccionado)
                instance.setDate([previousDay, nextDay], false); // 'false' para no volver a disparar onChange
            }
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            // Verificar si la fecha es una de las fechas marcadas
            if (markedDates.includes(dayElem.dateObj.toISOString().split('T')[0])) {
                dayElem.classList.add('marked');
            }
        }
    });
});