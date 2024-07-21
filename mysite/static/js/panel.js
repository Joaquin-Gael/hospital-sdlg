$(document).ready(()=>{

    var getToken = ()=>{
        return document.getElementsByName('csrfmiddlewaretoken')[0].value
    }

    var dataFalsa = [{
        id: 1,
        medico: {
            id: 1,
            nombre: 'Medico 1'
        },
        horario: {
            id: 1,
            hora: '08:00'
        },
        motivo: 'Motivo 1',
        estado: 'pendiente'
    }]

    var userDataFalsa = {
        dni: '00000000',
        nombre: 'Jonn',
        apellido: 'Doe',
        email: 'jonn@gmail.com',
        contraseña: '1234'
    }

    var testimonioDataFalsa = {
        content:'testimonio de Jonn Doe'
    }

    var userPerfilForm = (userData) => {
        if (userData) {
            return `
                <form id="perfilForm" class="box">
                    <div class="columns is-multiline">
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <label for="dniInput">DNI</label>
                                <div class="control">
                                    <input type="text" id="dniInput" class="input" placeholder="00000000" value="${userData.dni}">
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <label for="nombreInput">Nombre</label>
                                <div class="control">
                                    <input type="text" id="nombreInput" class="input" placeholder="Jonn" value="${userData.nombre}">
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <label for="apellidoInput">Apellido</label>
                                <div class="control">
                                    <input type="text" id="apellidoInput" class="input" placeholder="Doe" value="${userData.apellido}">
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <label for="emailInput">Email</label>
                                <div class="control">
                                    <input type="text" id="emailInput" class="input" placeholder="jonn@gmail.com" value="${userData.email}">
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <label for="contraseñaInput">Contraseña</label>
                                <div class="control">
                                    <input type="text" id="contraseñaInput" class="input" placeholder="00000000" value="${userData.contraseña}">
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <div class="control">
                                    <div class="file is-normal is-boxed has-name">
                                        <label class="file-label">
                                            <input class="file-input" type="file" name="resume">
                                            <span class="file-cta">
                                                <span class="file-icon">
                                                    <i class="fas fa-upload"></i>
                                                </span>
                                                <span class="file-label">
                                                    Seleccionar archivo
                                                </span>
                                            </span>
                                            <span class="file-name">
                                                imagen.jpg
                                            </span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="column is-full-mobile is-half-tablet is-one-third-desktop">
                            <div class="field">
                                <div class="control">
                                    <button id="actualizarButton" type="button" class="button is-fullwidth is-info">
                                        <span>Actualizar</span>
                                        <span class="icon">
                                            <i class="fa-solid fa-paper-plane"></i>
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            `;
        } else {
            return '';
        }
    }
    

    var turnosLink = (turnosData)=>{
        let turnos = ''
        if(turnosData){
            for(let i=0 ; i < turnosData.length; i++){
                data = turnosData[i]
                turnos += `
                <a id="turnoLink${data.id}" class="panel-block">
                    <span class="panel-icon">
                        <i class="fas fa-book" aria-hidden="true"></i>
                    </span>
                    ${data.id} ${data.horario.hora} ${data.medico.nombre} ${data.motivo} ${data.estado}
                </a>
                `
            }
            return `
            <div id="turnosList">
                ${turnos}
            </div>
            `
        }else{
            return ''
        }
    }

    var testimonioFomr = (testimonioData)=>{
        if(testimonioData){
            return `
            <form id="testimonioFomr" class="box">
                <textarea class="textarea is-info" placeholder="Info textarea">${testimonioData.content}</textarea>
            </form>
            `
        }else{
            return `
            <form id="testimonioFomr" class="box">
                <textarea class="textarea is-info" placeholder="Info textarea"></textarea>
            </form>
            `
        }
    }

    $('#contentPanel').append(turnosLink(dataFalsa))
    $('#contentPanel').append(userPerfilFomr(userDataFalsa))
    $('#contentPanel').append(testimonioFomr(testimonioDataFalsa))

    $('#perfilForm').hide()
    $('#testimonioFomr').hide()

    $('#perfilTab').click(()=>{
        $('#turnosTab').removeClass('is-active')
        $('#perfilTab').addClass('is-active')
        $('#testimoniosTab').removeClass('is-active')
        $('#perfilForm').show()
        $('#testimonioFomr').hide()
        $('#turnosList').hide()
    })
    $('#turnosTab').click(()=>{
        $('#turnosTab').addClass('is-active')
        $('#perfilTab').removeClass('is-active')
        $('#testimoniosTab').removeClass('is-active')
        $('#turnosList').show()
        $('#perfilForm').hide()
        $('#testimonioFomr').hide()
    })
    $('#testimoniosTab').click(()=>{
        $('#turnosTab').removeClass('is-active')
        $('#testimoniosTab').addClass('is-active')
        $('#perfilTab').removeClass('is-active')
        $('#testimonioFomr').show()
        $('#perfilForm').hide()
        $('#turnosList').hide()
    })
    $('.panel-block').click((Event)=>{
        let id = Event.currentTarget.id.split('turnoLink')[1]
        console.log(id)
        window.location.href = `/turnero/turnos/${id}/`
    })
    $('#actualizarButton').click((Event)=>{
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
            email: $('#emailInput').val(),
            contraseña: $('#contraseñaInput').val()
        }
        fetch('/user/perfil/',{
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
                    $('#responce').append(successMessage('Usuario actualizado'))
                }
            }
        ).catch(error => {
            $('#responce').append(errorMessage(error))
        })
    })
    $('#responce').on('click','.delete',()=>{
        $('#responceMsg').remove()
    })
})