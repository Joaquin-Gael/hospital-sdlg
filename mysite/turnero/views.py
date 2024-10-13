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
from .middlewares.userIDmiddleware import UserIDMiddleware
from asgiref.sync import sync_to_async
from rest_framework import status
from datetime import timedelta,datetime
import json, io,random


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
     
    @staticmethod
    def generar_intervalos(hora_inicio, hora_fin, intervalo_minutos): # para que si se puponia que el datepiker ya se encargaba de eso
        hora_actual = datetime.strptime(hora_inicio, "%H:%M:%S")
        fin = datetime.strptime(hora_fin, "%H:%M:%S")
        intervalos = []

        while hora_actual + timedelta(minutes=intervalo_minutos) <= fin:
            siguiente_hora = hora_actual + timedelta(minutes=intervalo_minutos)
            intervalos.append(hora_actual.strftime("%H:%M"))
            hora_actual = siguiente_hora

        return intervalos

    async def obtener_horarios_disponibles(self, request): # esta funcion asincrona no se utiliza nunca
        if request.method == 'POST':
            servicio_id = json.loads(request.body).get('servicio')
            try:
                especialidad_id = await sync_to_async(lambda: models.Servicios.objects.get(servicioID=servicio_id).especialidadID_id)()
                medicos = await sync_to_async(lambda: models.Medicos.objects.filter(especialidadID=especialidad_id))()

                horarios_disponibles = []

                for medico in medicos:
                    horarios = await sync_to_async(lambda: models.Horario_medicos.objects.filter(medicoID=medico))()
                    for horario in horarios:
                        intervalos = self.generar_intervalos(horario.hora_inicio, horario.hora_fin, 25)
                        horarios_disponibles.extend(intervalos)

                return response.JsonResponse({'horarios': horarios_disponibles})
            except models.Servicios.DoesNotExist:
                return response.JsonResponse({'error': 'Servicio no encontrado'}, status=404)
            except Exception as e:
                print(f"Error al obtener horarios disponibles: {e}")
                return response.JsonResponse({'error': 'Error interno del servidor'}, status=500)

     
    async def get(self, request):
        is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
        if not is_authenticated:
            return redirect('LoginUser')

        try:
            #medicos:list[models.Medicos] = await sync_to_async(lambda:models.Medicos.objects.all())()
            horarios:list[models.Horario_medicos] = await sync_to_async(lambda:models.Horario_medicos.objects.all())()
            servicios:list[models.Servicios] = await sync_to_async(lambda:models.Servicios.objects.all())()
            
            return TemplateResponse(request, 'turnero/form.html',{'horarios':horarios, 'servicios':servicios})
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
                servicio_obj = await sync_to_async(lambda: models.Servicios.objects.get(servicioID=servicio))()
                especialidad = servicio_obj.especialidadID
                medicos = await sync_to_async(lambda: models.Medicos.objects.filter(especialidadID=especialidad))()

                if not medicos:
                    return response.JsonResponse({'error': 'No hay médicos disponibles para esta especialidad'}, status=404)

                medico = random.choice(medicos)

                horarios = await sync_to_async(
                    lambda: models.Horario_medicos.objects.filter(medicoID=medico)
                )()
                turnos_ocupados = await sync_to_async(
                    lambda: models.Turnos.objects.filter(horarioID__in=horarios)
                )()

                horarios_disponibles = [
                    horario for horario in horarios if not any(
                        turno.horarioID == horario for turno in turnos_ocupados
                    )
                ]

                if not horarios_disponibles:
                    return response.JsonResponse({'error': 'No hay horarios disponibles'}, status=404)

                _turno = {
                    'medicoID': medico,
                    'motivo': motivo,
                    'fecha': fecha,
                    'userID': request.user
                }

                print(_turno)

                return TemplateResponse(request, 'turnero/pay-turno.html', {'turno_data': _turno})

            except models.Servicios.DoesNotExist:
                return response.JsonResponse({'error': 'Servicio no encontrado'}, status=404)
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
