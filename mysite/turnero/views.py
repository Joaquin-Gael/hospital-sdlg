from django.shortcuts import (get_object_or_404, render, redirect)
from django.http import Http404, HttpResponse, HttpResponseNotFound, response
from django.template.response import TemplateResponse
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.decorators import method_decorator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from . import models
from medicos.models import (Servicios, Medicos,Horario_medicos,Departamentos)
from .middlewares.userIDmiddleware import UserIDMiddleware
from asgiref.sync import sync_to_async
from rest_framework import status
from datetime import timedelta,datetime
from random import choice
import json, io

class PagarTurno(views.View):
    async def get(self,request):
        is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
        if not is_authenticated:
            return redirect('LoginUser')
        
        try: 
            turno_data = request.GET.get('turno_data')
            
            return TemplateResponse(request, 'turnero/pay-turno.html', {'turno_data': turno_data})
        
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__, e.args))
            return redirect('Home')
            
# Create your views here.
class TurneroForm(views.View):
    async def get(self, request):
        is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
        if not is_authenticated:
            return redirect('LoginUser')

        try:
            servicios = await sync_to_async(lambda: models.Servicios.objects.all())()
            return TemplateResponse(request, 'turnero/form.html', {
                'servicios': servicios
            })
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__, e.args))
            return redirect('Home')
    
    async def post(self, request):
        try:
            _json = json.loads(request.body)
            servicio = _json.get('servicio')
            motivo = _json.get('motivo')
            horario = _json.get('horario')
            fecha = _json.get('fecha')

            print(f"Servicio: {servicio}, Motivo: {motivo}, Horario: {horario}, Fecha: {fecha}")

            try:
                servicio = await sync_to_async(lambda: models.Servicios.objects.get(servicioID=servicio))()
                especialidad = servicio.especialidadID
                medicos = await sync_to_async(lambda: list(models.Medicos.objects.filter(especialidadID=especialidad)))()

                medico = choice(medicos)

                departamento = await sync_to_async(lambda: models.Departamentos.objects.get(departamentoID=medico.especialidadID.departamentoID.departamentoID))()

                _cita = {
                    'medicoID': medico,
                    'horarioID': horario,
                    'motivo': motivo,
                    'estado': 'Pendiente',
                    'departamentoID': departamento,
                }

                # Crear el turno
                _turno = {
                    'medicoID': medico,
                    'motivo': motivo,
                    'fecha': fecha,
                    'userID': request.user
                }

                print(_turno)

                # Renderizar la página de éxito
                return TemplateResponse(request, 'user/panel', {'turno_data': _turno})

            except models.Servicios.DoesNotExist:
                return response.JsonResponse({'error': 'Servicio no encontrado'}, status=404)
            except models.Medicos.DoesNotExist:
                return response.JsonResponse({'error': 'Médico no encontrado'}, status=404)
            except Exception as e:
                print(f'Error al generar turno: {e}')
                return response.JsonResponse({'error': 'Error al generar turno'}, status=500)
            
        except Exception as err:
            return response.JsonResponse({
                'error':'invalid JSON'
            },status=status.HTTP_400_BAD_REQUEST)

class TurnoData(views.View):

    @method_decorator(UserIDMiddleware)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def get(self, request, id):
        try:
            turno = await sync_to_async(models.Turnos.objects.get)(TurnoID=id)
            return render(request, 'turnero/turno-data.html',{'turno':turno})
        
        except Exception as err:
            return redirect('NotFound')
    
    async def delete(self, request, id):
        try:
            turno = await sync_to_async(models.Turnos.objects.get)(TurnoID=id)
            await sync_to_async(turno.delete)()
            return response.JsonResponse({
                'url':'/user/panel/'
            },status=status.HTTP_200_OK)
        except models.Turnos.DoesNotExist:
            return HttpResponseNotFound("Turno no encontrado",status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return HttpResponse("Error al eliminar el turno",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def post(self, request, id):
        try:
            pass

        except Exception as err:
            pass

class ComprobanteDownloadView(LoginRequiredMixin, views.View):

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
