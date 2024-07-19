from django.shortcuts import (render, redirect)
from django import views
from . import models

# Create your views here.
class TurneroForm(views.View):
    def get(self, request):
        if request.user.is_authenticated:

            medicos:list[models.Medicos] = models.Medicos.objects.all()
            horarios:list[models.Horario_medicos] = models.Horario_medicos.objects.all()

            return render(request, 'turnero/form.html',{'medicos':medicos,'horarios':horarios})
        
        return redirect('Home')
    
    def post(self, request):
        turnoData = models.Turnos.create_turnos(
            medicoID=request.POST['medico'],
            horarioID=request.POST['horario'],
            motivo=request.POST['motivo'],
            userID=request.user
        )
        return render(request, 'turnero/form.html')