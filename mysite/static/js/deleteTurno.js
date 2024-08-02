import { successMessage, errorMessage } from './utils/messages.js';
import { getToken } from './utils/tokens.js';
$(document).ready(()=>{
    var turnoID = localStorage.getItem('turnoID')
    var url = `/turnero/turnos/${turnoID}/`
    console.log(url)
    $('#deleteTurno').click(()=>{
        fetch(url,{
            method:'delete',
            headers: {
                'X-CSRFToken': getToken()
            }
        }).then(response => {
            if (!response.ok) {
                $('#responce').append(errorMessage(response.statusText));
                throw Error(response.statusText);
            } else {
                $('#responce').append(successMessage('Solicitud enviada'));
                return response.json();
            }
        }).then(data=>{
            window.location.href=data.url
        }).catch(error=>{
            $('#responce').append(errorMessage(error));
            alert(error);
            console.log(error);
        })
    })
})