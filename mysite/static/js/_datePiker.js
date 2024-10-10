// main.js

document.addEventListener('DOMContentLoaded', function () {
    // Constante de días marcados
    const markedDates = [
        "2024-08-20",
        "2024-08-25",
        "2024-09-10"
    ];

    flatpickr("#date-picker", {
        dateFormat: "Y-m-d",
        mode: "range",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                const selectedDate = selectedDates[0];
                const previousDay = new Date(selectedDate);
                const nextDay = new Date(selectedDate);

                // Calcular un día antes y un día después
                previousDay.setDate(selectedDate.getDate() - 1);
                nextDay.setDate(selectedDate.getDate() + 1);

                // Establecer solo los días de los extremos (anterior y posterior)
                instance.clear();
                instance.setDate([previousDay, nextDay]);
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
