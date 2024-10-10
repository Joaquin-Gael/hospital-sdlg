import { successMessage, errorMessage } from './utils/messages.js';
import { getToken } from './utils/tokens.js';

$(() => {
    const turnoID = localStorage.getItem('turnoID');
    const url = `/turnero/turnos/${turnoID}/`;
    console.log(url);

    // Función para mostrar un toast
    function showToast(messageHtml) {
        $('#response').append(messageHtml);
        const toastEl = $('#response .toast').last()[0];
        if (toastEl) {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
    }

    // Manejar la respuesta de eliminación
    function handleDeleteResponse(response) {
        if (!response.ok) {
            showToast(errorMessage(response.statusText));
            throw new Error(response.statusText);
        }
        showToast(successMessage('Solicitud enviada'));
        return response.json();
    }

    // Manejar errores
    function handleError(error) {
        showToast(errorMessage(error.message));
        alert(error.message);
        console.log(error);
    }

    // Manejar clic en el botón de eliminar turno
    $('#deleteTurno').on('click',() => {
        fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getToken()
            }
        })
        .then(handleDeleteResponse)
        .then(data => {
            window.location.href = data.url;
        })
        .catch(handleError);
    });
});