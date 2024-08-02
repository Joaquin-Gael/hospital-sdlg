from django.shortcuts import (render, redirect)
from django.http import response
from django.core import serializers
from django import (views)
from . import models
import json

# Create your views here.

class RegisterUser(views.View):
    def get(self, request):
        return render(request, 'user/register.html')
    
    def post(self, request):
        _json = json.loads(request.body)
        user = models.Usuarios(
            dni = _json['dni'],
            nombre = _json['nombre'],
            apellido = _json['apellido'],
            fecha_nacimiento = _json['nacido'],
            email = _json['email'],
            contraseña = _json['contraseña']
        )
        user.set_password(_json['contraseña'])
        user.save()
        return response.JsonResponse({
            'msg':f'{request.POST}'
        })

class UpdateUser(views.View):
    def get(self, request):
        return response.JsonResponse({
            'params':[
                'DNI',
                'Nombre',
                'Apellido',
                'Contraseña',
                'Email',
                'Imagen'
            ]
        })

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                redirect('NotFound')

            print(request.POST)
            print(request.FILES)

            user = models.Usuarios.objects.get(userID=request.user.userID)

            user.update_data(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                contraseña=request.POST.get('contraseña')
            )

            user.set_password(request.POST.get('contraseña'))

            return response.JsonResponse({
                'msg':f'{request.POST}'
            })

        except Exception as err:
            print(err)
            return response.JsonResponse({
                'error':f'{err}'
            },status=404)

class LoginUser(views.View):
    def get(self, request):
        return render(request, 'user/login.html')
    
    def post(self, request):
        _json = json.loads(request.body)
        print(_json)
        user = models.Usuarios.authenticate(request, _json['DNI'], _json['contraseña'])
        print(user)
        if user is None:
            return response.JsonResponse({
                'error':'credential not match'
            },status=401)
        return response.JsonResponse({
            'msg':f'{_json}'
        })
    

class PanelUser(views.View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('Home')
        try:
            user:models.Usuarios = models.Usuarios.objects.get(userID=request.user.id)
            turnos:list | None = user.get_turnos()
            return render(request, 'user/panel.html', {'turnos':turnos})
    
        except Exception as err:    
            return render(request, 'user/panel.html', {'turnos':[]})
    
    def post(self, request):
        _json = json.loads(request.body)
        print(_json)
        return response.JsonResponse({
            'msg':f'{_json}'
        })

class UserList(views.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return response.JsonResponse({
                'error':'not authenticate'
            },status=401)
        try:
            id = kwargs.get('id', None)
            if id != None:
                user = models.Usuarios.objects.get(userID=id)
                serialized = serializers.serialize('json',[user])
                return response.JsonResponse(
                    serialized,
                    status=200,
                    safe=False
                )
            
            
            userList:list = models.Usuarios.objects.all()
            
            serialized = serializers.serialize('json',userList)

            return response.JsonResponse(
                serialized,
                status=200,
                safe=False
            )

        except Exception as err:
            print(err)
            return response.JsonResponse({
                'error':f'{err}'
            },status=400)