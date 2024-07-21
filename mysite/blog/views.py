from django.shortcuts import render
from django import views

# Create your views here.

class Home(views.View):
    def get(self, request):
        return render(request, 'blog/index.html')

class Testimonios(views.View):
    def get(self, request):
        return render(request, 'blog/testimonios.html')