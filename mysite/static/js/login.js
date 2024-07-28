import { successMessage, errorMessage } from './utils/messages.js';
import { getToken } from './utils/tokens.js';

$(document).ready(() => {
    $('#loginButton').click(() => {
        let formdata = {
            DNI: $('#dniInput').val(),
            contraseña: $('#contraseñaInput').val()
        };

        var valid = true;

        for (let key in formdata) {
            if (formdata[key] === '' || formdata[key] === null) {
                valid = false;
            }
        }

        $('#responce').empty();

        if (valid) {
            fetch('/user/login/', {
                method: 'POST',
                body: JSON.stringify(formdata),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getToken()
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        $('#responce').append(errorMessage(`Error: ${text}`));
                        throw new Error(text);
                    });
                }
                return response.json();
            })
            .then(data => {
                $('#responce').append(successMessage('Login successful'));
                console.log(data);  // Puedes hacer algo con los datos recibidos
            })
            .catch(error => {
                $('#responce').append(errorMessage(`Request failed: ${error.message}`));
                console.error(error);
            });
        } else {
            $('#responce').append(errorMessage('Please fill in all fields'));
        }
    });

    $('#responce').on('click','.delete',()=>{
        $('#responceMsg').remove();
    });
});
