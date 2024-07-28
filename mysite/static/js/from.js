$(document).ready(() => {
    var getToken = () => {
        return document.getElementsByName('csrfmiddlewaretoken')[0].value;
    };
    
    var successMessage = (message) => {
        return `
        <div id="responceMsg" class="notification is-success">
                <button class="delete"></button>
                ${message}
        </div>`;
    };
    
    var errorMessage = (message) => {
        return `
        <div id="responceMsg" class="notification is-danger">
                <button class="delete"></button>
                ${message}
        </div>`;
    };
    
    $('#solicitarButton').click((e) => {
        e.preventDefault();
        
        var formdata = {
            medico: $('#medicoSelect').val(),
            motivo: $('#motivoTextarea').val(),
            horario: $('#horarioSelect').val(),
            fecha: $('#fechaInput').val()
        };
        
        var valid = true;
        
        for (let key in formdata) {
            if (formdata[key] == '' || formdata[key] == null) {
                valid = false;
                switch (key) {
                    case 'medico':
                        $('#medicoIcon').remove();
                        $('#medicoSelect').parent().append(`<i id="iconMedico" class="fas fa-exclamation-triangle"></i>`);
                        break;
                    case 'motivo':
                        $('#motivoIcon').remove();
                        $('#motivoTextarea').parent().append(`<i id="iconMotivo" class="fas fa-exclamation-triangle"></i>`);
                        break;
                    case 'horario':
                        $('#horarioIcon').remove();
                        $('#horarioSelect').parent().append(`<i id="iconHorario" class="fas fa-exclamation-triangle"></i>`);
                        break;
                    case 'fecha':
                        $('#fechaIcon').remove();
                        $('#fechaInput').parent().append(`<i id="iconFecha" class="fas fa-exclamation-triangle"></i>`);
                        break;
                    default:
                        break;
                }
            } else {
                switch (key) {
                    case 'medico':
                        $('#iconMedico').remove();
                        $('#medicoSelect').parent().append(`<i id="iconMedico" class="fas fa-check"></i>`);
                        break;
                    case 'motivo':
                        $('#iconMotivo').remove();
                        $('#motivoTextarea').parent().append(`<i id="iconMotivo" class="fas fa-check"></i>`);
                        break;
                    case 'horario':
                        $('#iconHorario').remove();
                        $('#horarioSelect').parent().append(`<i id="iconHorario" class="fas fa-check"></i>`);
                        break;
                    case 'fecha':
                        $('#iconFecha').remove();
                        $('#fechaInput').parent().append(`<i id="iconFecha" class="fas fa-check"></i>`);
                        break;
                    default:
                        break;
                }
            }
        }

        $('#responce').empty();  // Limpiar mensajes anteriores

        if (!valid) {
            $('#responce').append(errorMessage('Todos los campos son obligatorios'));
        } else {
            $('#comprobanteButton').toggleClass('is-static is-info');
            fetch('/turnero/', {
                method: 'POST',
                body: JSON.stringify(formdata),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getToken()
                }
            }).then(response => {
                $('#comprobanteButton').toggleClass('is-static is-info');
                if (!response.ok) {
                    $('#responce').append(errorMessage(response.statusText));
                    throw Error(response.statusText);
                } else {
                    $('#responce').append(successMessage('Solicitud enviada'));
                    return response.json();
                }
            }).then(data => {
                console.log(data);
            }).catch(error => {
                $('#responce').append(errorMessage(error));
                alert(error);
                console.log(error);
            });
        }
    });

    $('#responce').on('click', '.delete', () => {
        $('#responceMsg').remove();
    });

    $('#comprobanteButton').click(() => {
        console.log('pasa');
        $('#comprobanteButton').addClass('is-loading');
    });
});