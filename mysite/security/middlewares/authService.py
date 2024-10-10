from functools import wraps
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy

class SecurityMiddleware:
    @classmethod
    def AuthHeader(cls, fun):
        @wraps(fun)
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                #messages.error(request, 'No se proporcionó la autenticación')
                #return HttpResponseRedirect(reverse_lazy('LoginUser')
                pass
            return fun(request, *args, **kwargs)
        return wrapper
    
    @classmethod
    def UserAuth(cls, fun):
        @wraps(fun)
        def wrapper(request, *args, **kwargs):
            is_autenticate = request.user.is_authenticated
            if not is_autenticate:
                messages.error(request, 'No esta autenticado el usuario')
                return HttpResponseRedirect(reverse_lazy ('LoginUser'))
            return fun(request, *args, **kwargs)
        return wrapper

    @classmethod
    def AuthHeaderOrUser(cls, fun):
        @wraps(fun)
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            is_autenticate = request.user.is_authenticated
            if not token or is_autenticate:
                messages.warning(request, 'No se presento ninguna autenticación ')
                return HttpResponseRedirect(reverse_lazy(request.META.get('HTTP_REFERER')))
            return fun(request, *args, **kwargs)
        return wrapper
