import { successMessage, errorMessage } from './utils/messages.js';
import { getToken, getUserID } from './utils/tokens.js';

$(document).ready(()=>{
    fetch(`/user/list/${getUserID()}/`,{
        method:'GET'
    }).then(response=>{
        if(!response.ok){
            throw Error(response.statusText)
        }else{
            $('#responce').append(successMessage('Usuario Auntenticado'))
            return response.json()
        } 
    }).then(
        data =>{
            data = JSON.parse(data)
            console.log(data[0])
            let userData = {
                dni: data[0].fields.dni,
                nombre: data[0].fields.nombre,
                apellido: data[0].fields.apellido,
                email: data[0].fields.email,
                contraseña: data[0].fields.contraseña,
                imagen:data[0].imagen
            }
            console.log(userData)
            $('#contentPanel').append(userPerfilForm(userData))
            $('#perfilForm').hide()
            $('#fileInput').on('change', function() {
                var fileInput = $(this)[0];
                var fileNameSpan = $('#fileName');
        
                if (fileInput.files.length > 0) {
                    var fileName = fileInput.files[0].name;
                    fileNameSpan.text(fileName);
                } else {
                    fileNameSpan.text('No file chosen');
                }
            });
            $('#actualizarButton').click((Event)=>{
                let formdata = new FormData();
                formdata.append('dni', $('#dniInput').val());
                formdata.append('nombre', $('#nombreInput').val());
                formdata.append('apellido', $('#apellidoInput').val());
                formdata.append('email', $('#emailInput').val());
                formdata.append('contraseña', $('#contraseñaInput').val());
        
                let fileInput = $('#fileInput')[0].files[0];
                if (fileInput) {
                    formdata.append('imagen', fileInput);
                }
                
                fetch('/user/register/update/',{
                    method: 'POST',
                    body: formdata,
                    headers: {
                        'X-CSRFToken': getToken()
                    }
                }).then(
                    response => {
                        if(!response.ok){
                            throw Error(response.statusText)
                        }else{
                            $('#responce').append(successMessage('Usuario actualizado'))
                            return response.json()
                        }
                    }
                ).then(
                    data =>{
                        console.log(data)
                    }
                ).catch(error => {
                    console.error(error)
                    $('#responce').append(errorMessage(error))
                })
            })
        }
    ).catch(error => {
        console.error(error)
        $('#responce').append(errorMessage(error))
    })

    fetch(`/API/users/${getUserID()}/turnos/`,{
        method:'GET'
    }).then(response => {
        if(!response.ok){
            throw Error(response.statusText)
        }else{
            return response.json()
        } 
    }).then(data => {
        let dataTurnos = data
        $('#contentPanel').append(turnosLink(dataTurnos))
        $('.panel-block').click((Event)=>{
            let id = Event.currentTarget.id.split('turnoLink')[1]
            console.log(id)
            window.location.href = `/turnero/turnos/${id}/`
        })
    }).catch(error => {
        console.error(error)
        $('#responce').append(errorMessage(error))
    })

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
                                            <input id="fileInput" class="file-input" type="file" name="resume">
                                            <span class="file-cta">
                                                <span class="file-icon">
                                                    <i class="fas fa-upload"></i>
                                                </span>
                                                <span class="file-label">
                                                    Seleccionar archivo
                                                </span>
                                            </span>
                                            <span id="fileName" class="file-name">
                                                ${userData.imagen}
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
            let data = null
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

    $('#contentPanel').append(testimonioFomr(testimonioDataFalsa))

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
    $('#responce').on('click','.delete',()=>{
        $('#responceMsg').remove()
    })
})