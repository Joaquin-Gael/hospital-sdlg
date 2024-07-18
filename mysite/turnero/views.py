from django.shortcuts import render
from django import views

# Create your views here.
class TurneroForm(views.View):
    def get(self, request):
        return render(request, 'turnero/form.html')
    
    def post(self, request):
        return render(request, 'turnero/form.html')