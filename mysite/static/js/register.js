$(document).ready(()=>{
    var getToken = ()=>{
        return document.getElementsByName('csrfmiddlewaretoken')[0].value
    }
    $('#registrarButton').click(()=>{
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
            dni: $('#dniInput').val(),
            nombre: $('#nombreInput').val(),
            apellido: $('#apellidoInput').val(),
            nacido: $('#nacidoInput').val(),
            email: $('#emailInput').val(),
            contraseña: $('#contraseñaInput').val()
        }

        var valid = true

        for(let key in formdata){
            if(formdata[key] == null || formdata[key] == ''){
                valid = false
            }
        }

        if(valid){
            fetch('/user/register/',{
                method: 'POST',
                body: JSON.stringify(formdata),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getToken()
                }
            }).then(
                response => {
                    if(!response.ok){
                        throw Error(response.statusText)
                    }else{
                        $('#responce').append(successMessage('Usuario registrado'))
                    }
                }
            ).catch(error => {
                $('#responce').append(errorMessage(error))
            })
        }else{
            $('#responce').append(errorMessage('Todos los campos son obligatorios'))
        }
    })
    $('#responce').on('click','.delete',()=>{
        $('#responceMsg').remove()
    })
})