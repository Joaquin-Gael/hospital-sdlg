export var getToken = ()=>{
    return document.getElementsByName('csrfmiddlewaretoken')[0].value
}