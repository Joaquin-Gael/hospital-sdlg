import { successMessage, errorMessage } from './utils/messages.js';
import { getToken } from './utils/tokens.js';

$(() => {
    const formFields = {
        servicio: '#servicioSelect',
        motivo: '#motivoTextarea',
        horario: '#horarioSelect',
        fecha: '#date-picker'
    };

    // Actualiza el ícono de validación para un campo específico
    const updateIcon = (key, isValid) => {
        const field = $(formFields[key]).parent();
        const iconId = `#icon${key.charAt(0).toUpperCase() + key.slice(1)}`;
        $(iconId).remove(); // Elimina cualquier ícono anterior
        const iconClass = isValid ? 'fa-check' : 'fa-exclamation-triangle';
        field.append(`<i id="${iconId}" class="fas ${iconClass}"></i>`);
    };

    // Valida los datos del formulario
    const validateForm = (formData) => {
        let isValid = true;
        Object.keys(formFields).forEach(key => {
            if (!formData[key]) {
                isValid = false;
                updateIcon(key, false);
            } else {
                updateIcon(key, true);
            }
        });
        return isValid;
    };

    // Descarga del comprobante
    const handleComprobanteDownload = async (turnoID) => {
        const BUTTON = $('#comprobanteButton');
        BUTTON.addClass('is-loading');

        try {
            const response = await fetch(`/turnero/comprobantes/${turnoID}/`);
            if (!response.ok) throw new Error('Error de red');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'comprobante.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error al descargar el archivo: ', error);
            showToast(errorMessage('Error al descargar el comprobante.'));
        } finally {
            BUTTON.removeClass('is-loading');
        }
    };

    const showToast = (messageHtml) => {
        $('#response').append(messageHtml);
        const toastEl = $('#response .toast').last()[0];
        if (toastEl) {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
    };

    $('#solicitarButton').on('click', async (e) => {
        e.preventDefault();

        const formData = {
            servicio: $(formFields.servicio).val(),
            motivo: $(formFields.motivo).val(),
            horario: $(formFields.horario).val(),
            fecha: $(formFields.fecha).val()
        };

        $('.form-group i').remove();
        $('#response').empty();  

        if (!validateForm(formData)) {
            showToast(errorMessage('Todos los campos son obligatorios'));
            return;
        }

        try {
            const response = await fetch('/turnero/', {
                method: 'POST',
                body: JSON.stringify(formData),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getToken()
                }
            });

            if (!response.ok) throw new Error(response.statusText);

            const data = await response.json();
            const turnoID = data.msg.turnoID;

            showToast(successMessage('Solicitud enviada con éxito'));
            $('#comprobanteButton').off('click').on('click', () => handleComprobanteDownload(turnoID));
        } catch (error) {
            showToast(errorMessage(`Error al enviar la solicitud: ${error.message}`));
            console.error(error);
        }
    });

    // ya tenias en _dataPiker.js para el date-piker
    // Inicia el selector de fecha
    //flatpickr('#date-picker', {
    //    dateFormat: 'Y-m-d',
    //    onChange: function() {
    //        $('#servicioSelect').trigger('change');
    //    }
    //});
});