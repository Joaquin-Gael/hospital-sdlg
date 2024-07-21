$(document).ready(()=>{
    var getToken = ()=>{
        return document.getElementsByName('csrfmiddlewaretoken')[0].value
    }
    $('#solicitarButton').click(()=>{
        var successMessage = (message)=>{
            return `
            <div id="responceMsg" class="notification is-success">
                    <button class="delete"></button>
                    ${message}
            </div>
            `
        }
        var errorMessage = (messgae)=>{
            return `
            <div id="responceMsg" class="notification is-danger">
                    <button class="delete"></button>
                    ${messgae}
            </div>
            `
        }

        var formdata = {
            medico: $('#medicoSelect').val(),
            motivo: $('#motivoTextarea').val(),
            horario: $('#horarioSelect').val(),
            fecha: $('#fechaInput').val()
        }

        var valid = true

        console.table(formdata)

        for(let key in formdata){
            if(formdata[key] == '' || formdata[key] == null){
                valid = false
                switch(key){
                    case 'medico':
                        $('#medicoIcon').remove()
                        $('#medicoIcon').append(`<i id="iconMedico" class="fas fa-exclamation-triangle"></i>`)
                        break;
                    case 'motivo':
                        $('#motivoIcon').remove()
                        $('#motivoIcon').append(`<i id="iconMotivo" class="fas fa-exclamation-triangle"></i>`)
                        break;
                    case 'horario':
                        $('#horarioIcon').remove()
                        $('#horarioIcon').append(`<i id="iconHorario" class="fas fa-exclamation-triangle"></i>`)
                        break;
                    case 'fecha':
                        $('#fechaIcon').remove()
                        $('#fechaIcon').append(`<i id="iconFecha" class="fas fa-exclamation-triangle"></i>`)
                        break;
                    case 'csrfmiddlewaretoken':
                        break;
                    default:
                        break;
                }
            }else{
                switch(key){
                    case 'medico':
                        $('#medicoIcon').remove()
                        $('#medicoIcon').append(`<i id="iconMedico" class="fas fa-check"></i>`)
                        break;
                    case 'motivo':
                        $('#motivoIcon').remove()
                        $('#motivoIcon').append(`<i id="iconMotivo" class="fas fa-check"></i>`)
                        break;
                    case 'horario':
                        $('#horarioIcon').remove()
                        $('#horarioIcon').append(`<i id="iconHorario" class="fas fa-check"></i>`)
                        break;
                    case 'fecha':
                        $('#fechaIcon').remove()
                        $('#fechaIcon').append(`<i id="iconFecha" class="fas fa-check"></i>`)
                        break;
                    case 'csrfmiddlewaretoken':
                        break;
                    default:
                        break;
                }
            }
        }

        if (!valid){
            $('#responce').append(errorMessage('Todos los campos son obligatorios'))
        }else{
            $('#comprobanteButton').toggleClass('is-static')
            $('#comprobanteButton').toggleClass('is-info')
            fetch('/turnero/',{
                method: 'POST',
                body: JSON.stringify(formdata),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getToken()
                }
            }
            ).then(
                response => {
                    if(!response.ok){
                        $('#comprobanteButton').toggleClass('is-static')
                        $('#comprobanteButton').toggleClass('is-primary')
                        $('#responce').append(errorMessage(response.statusText))
                        throw Error(response.statusText)
                    }else{
                        $('#responce').append(successMessage('Solicitud enviada'))
                        response.json()
                    }
                }
            ).then(
                data => console.log(data)
            ).catch(error => {
                $('#comprobanteButton').addClass('is-static')
                $('#comprobanteButton').removeClass('is-primary')
                $('#responce').append(errorMessage(error))
                alert(error)
                console.log(error)
            })
        }
    })
    $('#responce').on('click','.delete',()=>{
        $('#responceMsg').remove()
    })
    $('#comprobanteButton').click(()=>{
        console.log('pasa')
        $('#comprobanteButton').addClass('is-loading')
    })
})