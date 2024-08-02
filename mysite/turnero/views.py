from django.shortcuts import (get_object_or_404, render, redirect)
from django.http import Http404, HttpResponse, HttpResponseNotFound, response
from django import views
from django.contrib.staticfiles import finders
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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

            try:
                data = models.Turnos.extra_data({'horario':horario,'medico':medico})
                print(data)
                _turno = models.Turnos.create_turnos(
                    medicoID=data['m'],
                    horarioID=data['h'],
                    motivo=motivo,
                    fecha=fecha,
                    userID=request.user
                )
                print(_turno)
            except Exception as err:
                print(f'Error al generar turno: {err}')

            return response.JsonResponse({
                'msg':{
                    'turnoID':_turno.TurnoID
                }
            },status=200)

        except Exception as err:
            return response.JsonResponse({
                'error':'invalid JSON'
            },status=400)

class TurnoData(views.View):
    def get(self, request, id):
        try:
            turno = models.Turnos.objects.get(TurnoID=id)
            return render(request, 'turnero/turno-data.html',{'turno':turno})
        
        except Exception as err:
            return redirect('NotFound')
    
    def delete(self, request, id):
        try:
            turno = models.Turnos.objects.get(TurnoID=id)
            turno.delete()
            return response.JsonResponse({
                'url':'/user/panel/'
            },status=200)
        except models.Turnos.DoesNotExist:
            return HttpResponseNotFound("Turno no encontrado")
    
    def post(self, request, id):
        try:
            pass

        except Exception as err:
            pass

class ComprobanteDownloadView(views.View):

    def get(self, request, id):
        try:
            print(id)
            turno = get_object_or_404(models.Turnos, TurnoID=id)
            cita = turno.citaID
            medico = cita.medicoID
            horario = cita.horarioID
            departamento = cita.departamentoID
            usuario = turno.userID

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Encontrar la ruta a los logos
            logo_path = finders.find('img/Logo-SDLG-name.png')

            p.drawImage(logo_path, 40, 700, width=80, height=80)

            p.setFont("Helvetica-Bold", 16)
            p.drawString(200, 750, "Comprobante de Turno")

            p.setFont("Helvetica", 12)
            p.drawString(40, 680, f"Código del Turno: YY-{turno.TurnoID}")
            p.drawString(40, 660, f"Paciente: {usuario.nombre} {usuario.apellido}")
            p.drawString(40, 640, f"Médico: {medico.nombre} {medico.apellido}")
            p.drawString(40, 620, f"Horario: {horario.hora_inicio}")
            p.drawString(40, 600, f"Departamento: {departamento.nombre}")
            p.drawString(40, 580, f"Fecha: {turno.fecha}")
            p.drawString(40, 560, f"Motivo: {cita.motivo}")
            p.drawString(40, 540, f"Estado: {turno.estado}")

            p.showPage()
            p.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="comprobante_turno_{id}.pdf"'
            return response

        except Http404:
            return redirect('NotFound')
