from django.shortcuts import (render, redirect)
from django import views

class NotFound(views.View):
    def get(self, request):
        return render(request, 'NotFound404.html')