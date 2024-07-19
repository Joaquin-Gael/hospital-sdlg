from django.shortcuts import (render, redirect)
from django import views

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
        return render(request, 'user/panel.html')
    
    def post(self, request):
        print(request.POST)
        return redirect('Home')