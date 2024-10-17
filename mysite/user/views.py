from django.shortcuts import (render, redirect)
from django.http import response
from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from asgiref.sync import sync_to_async
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.core import serializers
from asgiref.sync import sync_to_async
from django import views
from django.urls import reverse_lazy
from . import models
from .middlewares.saveUserData import LoginUnRequired
import json

# Create your views here.

class RegisterUser(views.View):

    def get(self, request):
        return render(request, 'user/register.html')
    
    def post(self, request):
        try:
            user = models.Usuarios(
                dni = request.POST.get('dni'),
                nombre = request.POST.get('nombre'),
                apellido = request.POST.get('apellido'),
                fecha_nacimiento = request.POST.get('nacido'),
                email = request.POST.get('email'),
                contraseña = request.POST.get('contraseña'),
                username = request.POST.get('nombre') +' '+ request.POST.get('apellido')
            )
            user.set_password(request.POST.get('contraseña'))
            try:
                imagen = request.FILES.get('imagen')
                if imagen:
                    user.imagen = imagen
                else:
                    user.set_dpp()
            except Exception as e:
                print('Error: {}\nData: {}'.format(e.__class__, e.args))
                user.set_dpp()
            user.set_contraseña()
            user.save()
            user.authenticate(request,user.dni, request.POST.get('contraseña'))
            return response.JsonResponse({
                'msg':'¡Usuario creado con éxito! \nBienvenido {}'.format(user.username)
            })
        except Exception as e:
            print(f'Error: {e.__class__}\nData: {e.args}\n2')
            return response.JsonResponse({
                'error':'Error al crear el usuario \nInfo: {}'.format(e.args)
            },status=400)
            
class UpdateUser(views.View):
    async def get(self, request):
        return response.JsonResponse({
            'params':[
                'DNI',
                'Nombre',
                'Apellido',
                'Contraseña',
                'Email',
                'Imagen',
                'Telefono'
            ]
        })

    async def post(self, request):
        try:
            is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
            if not is_authenticated:
                return HttpResponseRedirect(
                    redirect_to=reverse_lazy('NotFound')
                )

            user = await sync_to_async(lambda:models.Usuarios.objects.get(userID=request.user.userID))

            await sync_to_async(user.update_data)(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                contraseña=request.POST.get('contraseña'),
                email=request.POST.get('email'),
                img=request.FILES.get('imagen'),
                telefono=request.POST.get('telefono')
            )

            user.set_password(request.POST.get('contraseña'))
            user.set_contraseña()

            return response.JsonResponse({
                'msg':f'{request.POST}'
            })

        except Exception as err:
            print(err)
            return response.JsonResponse({
                'error':f'{err}'
            },status=404)

class LoginUser(views.View):
    
    @method_decorator(LoginUnRequired)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'user/loginR.html')
    
    def post(self, request):
        try:
            _json = json.loads(request.body)
            user = models.Usuarios.authenticate(request, _json['DNI'], _json['contraseña'])
            if user is None:
                return response.JsonResponse({
                    'error':'credential not match'
                },status=401)
            return response.JsonResponse({
                'msg':f'{_json}'
            })
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__, e.args))
            #messages.error(request, message='Ocurrió un error al autenticar el usuario. Por favor, intentelo nuevamente.')
            #return redirect('LoginUser')
            return response.JsonResponse({
                'error':'Ocurrió un error al autenticarq el usuario. Por favor, intentelo nuevamente.'
            },status=401)
    

class PanelUser(views.View):
    async def get(self, request):
        try:
            is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
            if not is_authenticated:
                return HttpResponseRedirect(
                    redirect_to=reverse_lazy('NotFound')
                )
            #user:models.Usuarios = sync_to_async(models.Usuarios.objects.get)(userID=request.user.userID)
            return TemplateResponse(request, 'user/panel.html')
    
        except models.Usuarios.DoesNotExist:
            messages.error(request=request, message='Usuario no encontrado')
            return TemplateResponse(request, 'user/panel.html')

    async def post(self, request):
        try:
            is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
            if not is_authenticated:
                return HttpResponseRedirect(
                    redirect_to=reverse_lazy('NotFound')
                )

            user = await sync_to_async(models.Usuarios.objects.get)(userID=request.user.userID)

            await sync_to_async(user.update_data)(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                contraseña=request.POST.get('contraseña'),
                email=request.POST.get('email'),
                img=request.FILES.get('imagen'),
                telefono=request.POST.get('telefono'),
                request=request
            )

            user.set_password(request.POST.get('contraseña'))
            user.set_contraseña()

            messages.success(request, 'Datos actualizados correctamente')
            return HttpResponseRedirect(
                redirect_to=reverse_lazy('LoginUser')
            )

        except Exception as err:
            print(f'Error: {err.__class__}\nData: {err.args}')
            return response.JsonResponse({
                'error':f'{err}'
            },status=404)

class LogoutUser(LoginRequiredMixin,views.View):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        models.Usuarios.logout(request)
        messages.success(request, message='Sesión cerrada exitosamente')
        return redirect('Home')
    
    def post(self, request):
        models.Usuarios.logout(request)
        messages.success(request, message='Sesión cerrada exitosamente')
        return redirect('Home')