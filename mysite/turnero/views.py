from django.shortcuts import (render, redirect)
from django.http import response
from django import views
from . import models
import json, io

# Create your views here.
class TurneroForm(views.View):
    def get(self, request):
        if request.user.is_authenticated:

            medicos:list[models.Medicos] = models.Medicos.objects.all()
            horarios:list[models.Horario_medicos] = models.Horario_medicos.objects.all()

            return render(request, 'turnero/form.html',{'medicos':medicos,'horarios':horarios})
        
        return redirect('LoginUser')
    
    def post(self, request):
        try:
            _json = json.loads(request.body)
            medico = _json.get('medico')
            motivo = _json.get('motivo')
            horario = _json.get('horario')
            fecha = _json.get('fecha')

            print(f"Medico: {medico}, Motivo: {motivo}, Horario: {horario}, Fecha: {fecha}")

            _turno = models.Turnos.create_turnos(
                medicoID=medico,
                horarioID=horario,
                motivo=motivo,
                fecha=fecha,
                userID=request.user.id
            )

            return response.JsonResponse({
                'msg':f'Medico: {medico}, Motivo: {motivo}, Horario: {horario}, Fecha: {fecha}'
            },status=200)

        except Exception as err:
            return response.JsonResponse({
                'error':'invalid JSON'
            },status=400)

class TurnoData(views.View):
    def get(self, request, id):
        try:
            turno = models.Turnos.objects.get(id=id)
            return render(request, 'turnero/turno-data.html',{'turno':turno})
        
        except Exception as err:
            return redirect('NotFound')
    
    def delete(self, request, id):
        turno = models.Turnos.objects.get(id=id)
        turno.delete()
        return redirect('Home')
    
    def post(self, request, id):
        try:
            pass

        except Exception as err:
            pass

class ComprobanteDownload(views.View):
    def get(self,request,*args,**kwargs):
        try:
            turno = models.Turnos.objects.get(userID=request.user.id)

            content = f'Fecha: {turno.fecha}\nMedico: {turno.medicoID.nombre}\nCita: {turno.citaID.horarioID.hora_inicio}-{turno.citaID.horarioID.hora_fin}'

            file_in_memori = io.BytesIO()

            file_in_memori.write(content.encode('utf-8'))

            file_in_memori.seek(0)

            response_file = response.FileResponse(file_in_memori, as_attachment=True, filename='comprobante.txt', status=200)

            return response_file
        except Exception as err:
            print(err)
            return response.JsonResponse({'error':f'{err}'},status=404)
