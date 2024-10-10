import { successMessage, errorMessage } from './utils/messages.js';
import { getToken } from './utils/tokens.js';

$(() => {
    // Función para mostrar un toast
    function showToast(messageHtml) {
        $('#response').append(messageHtml);
        const toastEl = $('#response .toast').last()[0];
        if (toastEl) {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
    }

    // Validar formulario
    function isFormDataValid(formData) {
        return Object.values(formData).every(value => value !== null && value !== '');
    }

    // Manejar la respuesta del registro
    function handleRegisterResponse(response) {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        showToast(successMessage('Usuario registrado'));
        window.location.href = '/user/panel/';
    }

    // Manejar el error
    function handleError(error) {
        showToast(errorMessage(error.message || 'Error en el registro'));
    }

    // Obtener los datos del formulario
    function getFormData() {
        let formData = new FormData();

        formData.append('dni', $('#dniInput').val());
        formData.append('nombre', $('#nombreInput').val());
        formData.append('apellido', $('#apellidoInput').val());
        formData.append('nacido', $('#nacidoInput').val());
        formData.append('email', $('#emailInput').val());
        formData.append('contraseña', $('#contraseñaInput').val());

        const imageFile = $('#imagenInput')[0].files[0];
        if (imageFile){
            console.log(imageFile);
            formData.append('imagen', imageFile);
        }

        return formData;
    }

    function getFormDataGoogle() {
        return {
            dni: $('#id_dni').val(),
            nacido: $('#id_fecha_nacimiento').val(),
            contraseña: $('#id_password1').val(),
            contraseñaConfirmada: $('#id_password2').val()
        };
    }

    // Manejar el clic en el botón de registro
    $('#registrarButton').on('click', (e) => {
        e.preventDefault();

        const formData = getFormData();

        if (isFormDataValid(formData)) {
            fetch('/user/register/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getToken(),
                    'WithOut-google': 'true'
                }
            })
            .then(handleRegisterResponse)
            .catch(handleError);
        } else {
            showToast(errorMessage('Todos los campos son obligatorios'));
        }
    });

    // Toggle botón de Google
    function toggleGoogleButton() {
        const email = $('#id_email').val().trim();
        const fechaNacimiento = $('#id_fecha_nacimiento').val().trim();
        const contraseña = $('#id_password1').val().trim();
        const contraseñaConfirmada = $('#id_password2').val().trim();

        const isFormComplete = email && fechaNacimiento && contraseña && contraseñaConfirmada;
        $('#googleRegistrarButton').prop('disabled', !isFormComplete);
        $('#googleAccount').toggle(isFormComplete);
    }

    // Llamar a la función cuando se cambie algún campo
    $('#id_email, #id_fecha_nacimiento, #id_password1, #id_password2').on('input', ()=>{
        if (isFormDataValid(getFormDataGoogle())){
            toggleGoogleButton();
        }
        else{
            $('#googleRegistrarButton').prop('disabled', true);
            $('#googleAccount').hide();
        }
    });

    // Inicialmente, verificar el estado de los campos
    toggleGoogleButton();
});