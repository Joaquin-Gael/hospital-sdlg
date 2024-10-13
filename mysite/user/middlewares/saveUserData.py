from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# Revisar o Refactorizar

def CachOauthGoogleLogin(fun):
    @wraps(fun)
    def wrapper(request, *args, **kwargs):
        WithOut = request.META.get('HTTP_WITHOUT_GOOGLE')
        if not WithOut:
            
            return fun(request, *args, **kwargs)
        return fun(request, *args, **kwargs)
    return wrapper
 

def LoginUnRequired(fun):
    @wraps(fun)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, message="Ya estas logueado")
            #(request, message="No esta permitida esta accion")
            return redirect('Home')
        return fun(request, *args, **kwargs)
    return wrapper