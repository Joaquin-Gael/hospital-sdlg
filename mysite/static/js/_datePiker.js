// main.js

document.addEventListener('DOMContentLoaded', function () {
    // Constante de días marcados
    const markedDates = [
        "2024-10-20",
        "2024-10-25",
        "2024-10-10"
    ];

    // Obtener la fecha actual
    const today = new Date();

    // Función para obtener el nombre del día en español
    function getDayName(date) {
        const days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
        return days[date.getDay()];
    }

    // Función para desactivar los días que no están disponibles
    function disableUnavailableDays(date, availableDays) {
        const dayName = getDayName(date);
        return !availableDays.includes(dayName);
    }

    // Función para obtener los días disponibles desde la API
    async function getAvailableDays(servicioID) {
        try {
            const response = await fetch(`/API/schedules/${servicioID}/days/`);
            const data = await response.json();
            return data.days_availables;
        } catch (error) {
            console.error('Error fetching available days:', error);
            return [];
        }
    }

    // Función para inicializar el calendario
    async function initCalendar(servicioID) {
        const availableDays = await getAvailableDays(servicioID);

        flatpickr("#date-picker", {
            dateFormat: "Y-m-d",
            minDate: today, // Desactivar fechas pasadas
            disable: [
                function(date) {
                    return disableUnavailableDays(date, availableDays);
                }
            ],
            onDayCreate: function(dObj, dStr, fp, dayElem) {
                // Verificar si la fecha es una de las fechas marcadas
                if (markedDates.includes(dayElem.dateObj.toISOString().split('T')[0])) {
                    dayElem.classList.add('marked');
                }
            }
        });
    }

    // Evento de cambio en el select de servicios
    servicioSelect.addEventListener('change', function (event) {
        const servicioID = servicioSelect.value;
        if (servicioID) {
            initCalendar(servicioID);
        }
    });
});
