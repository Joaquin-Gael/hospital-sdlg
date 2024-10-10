from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from ..forms import UsuarioForm

# Revisar o Refactorizar

def CachOauthGoogle(fun):
    @wraps(fun)
    def wrapper(request, *args, **kwargs):
        # Verificar si se está usando Google OAuth
        WithOut = request.META.get('HTTP_WITHOUT_GOOGLE')
        if not WithOut:
            # Crear la instancia del formulario con los datos del POST
            form = UsuarioForm(request.POST)
            # Validar el formulario
            if form.is_valid():
                # Intentar guardar el usuario con los datos de Google OAuth
                try:
                    usuario = form.save()
                    if usuario:
                        # Usuario creado con éxito
                        messages.success(request, message='¡Usuario creado con éxito!')
                        return redirect('Home')
                    else:
                        # Si no se puede guardar el usuario
                        messages.error(request, message="Ocurrió un error al crear el usuario. Por favor, intentelo nuevamente.")
                        return redirect('RegisterUser')
                except Exception as e:
                    # Capturar cualquier excepción que ocurra al guardar el usuario
                    messages.error(request, message=f"Error: {e}")
                    return redirect('RegisterUser')
            else:
                # Si el formulario no es válido, mostrar los errores
                print(form.errors)
                messages.error(request, message="Formulario inválido. Revise los campos e intente de nuevo.")
                return redirect('RegisterUser')
        # Si no es OAuth con Google, continuar con la vista normal
        return fun(request, *args, **kwargs) 
    return wrapper

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