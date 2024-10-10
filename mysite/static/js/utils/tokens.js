export var getToken = ()=>{
    return document.getElementsByName('csrfmiddlewaretoken')[0].value
}
export var getUserID = ()=>{
    return localStorage.getItem('user_id')
}