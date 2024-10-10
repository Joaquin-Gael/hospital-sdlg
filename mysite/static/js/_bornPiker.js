// main.js
// id_fecha_nacimiento
document.addEventListener('DOMContentLoaded', function () {
    const markedDates = null;

    flatpickr("#nacidoInput", {
        dateFormat: "Y-m-d",
        mode: "single",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                const selectedDate = selectedDates[0];

                instance.setDate([selectedDate]);
            }
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            // Verificar si la fecha es una de las fechas marcadas
            if (markedDates){
                if (markedDates.includes(dayElem.dateObj.toISOString().split('T')[0])) {
                    dayElem.classList.add('marked');
                }
            }
        }
    });

    flatpickr("#id_fecha_nacimiento", {
        dateFormat: "Y-m-d",
        mode: "single",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                const selectedDate = selectedDates[0];

                instance.setDate([selectedDate]);
            }
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            // Verificar si la fecha es una de las fechas marcadas
            if (markedDates){
                if (markedDates.includes(dayElem.dateObj.toISOString().split('T')[0])) {
                    dayElem.classList.add('marked');
                }
            }
        }
    });
});