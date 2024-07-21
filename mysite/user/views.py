from django.shortcuts import (render, redirect)
from django import views
from . import models

# Create your views here.

class RegisterUser(views.View):
    def get(self, request):
        return render(request, 'user/register.html')
    
    def post(self, request):
        print(request.POST)
        return redirect('Home')
    
    
class LoginUser(views.View):
    def get(self, request):
        return render(request, 'user/login.html')
    
    def post(self, request):
        print(request.POST)
        return redirect('Home')
    
class PanelUser(views.View):
    def get(self, request):
        try:
            user:models.Usuarios = models.Usuarios.objects.get(userID=request.user.id)
            turnos:list | None = user.get_turnos()
            return render(request, 'user/panel.html', {'turnos':turnos})
    
        except Exception as err:    
           return render(request, 'user/panel.html', {'turnos':[]})
    
    def post(self, request):
        print(request.POST)
        return redirect('Home')