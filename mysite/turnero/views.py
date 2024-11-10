from django.shortcuts import (get_object_or_404, render, redirect)
from django.http import (Http404, HttpResponse, HttpResponseNotFound, response)
from django.template.response import TemplateResponse
from channels.db import database_sync_to_async
from django.views import View
from django.contrib.messages import (success,error)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.finders import find
from django.utils.decorators import method_decorator
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from . import models
from user.models import ObrasSociales
from .middlewares.userIDmiddleware import UserIDMiddleware
from asgiref.sync import sync_to_async
from random import choice
from .customButton import CustomPaypalmentsForm
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import json, io,uuid,mercadopago,qrcode

# Create your views here.
class TurneroForm(View):
    async def get(self, request):
        is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
        if not is_authenticated:
            return redirect('LoginUser')
        try:
            servicios = await sync_to_async(models.Servicios.objects.all)()
            obraID = await sync_to_async(lambda: request.user.obraID)()
            return TemplateResponse(request, 'turnero/form.html', {'servicios': servicios, 'obrasocial': obraID})
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__, e.args))
            return redirect('Home')

    async def post(self, request):
        try:
            obraID = await sync_to_async(lambda: request.user.obraID_id)()
            print(obraID)
            print("empieza aca")
            if obraID == 1:
                try:
                    print("inicio")
                    servicio = await sync_to_async(lambda: models.Servicios.objects.get(servicioID=request.POST.get('servicio')))()
                    print("paso 1")
                    especialidad = await sync_to_async(lambda: servicio.especialidadID)()
                    print("paso 2")
                    medicos = await sync_to_async(lambda: list(models.Medicos.objects.filter(especialidadID=especialidad)))()
                    print("se selecciona médico")
                    medico = choice(medicos)

                    departamento = await sync_to_async(lambda: models.Departamentos.objects.get(departamentoID=medico.especialidadID.departamentoID.departamentoID))()

                    print("inicia la creación de la cita")
                    cita = await sync_to_async(models.Citas.objects.create)(
                        servicioID=servicio,
                        userID=request.user,
                        medicoID=medico,
                        horarioID=await sync_to_async(lambda: models.Horario_medicos.objects.get(horarioID=request.POST.get('horario')))(),
                        motivo=request.POST.get('motivo'),
                        estado='Pendiente',
                        departamentoID=departamento,
                    )
                    print("cita creada")

                    print("inicia la creación del turno")
                    _turno = await sync_to_async(models.Turnos.objects.create)(
                        citaID=cita,
                        servicioID=servicio,
                        medicoID=medico,
                        motivo=request.POST.get('motivo'),
                        estado='Pendiente',
                        fecha=request.POST.get('fecha'),
                        userID=request.user,
                        fecha_limt=request.POST.get('fecha')
                    )

                    print(_turno)
                    print("solicitud realizada con éxito")

                    return TemplateResponse(request, 'user/panel.html')
                except Exception as e:
                    print(f'Error al generar turno: {e}')
                    return response.JsonResponse({'error': 'Error al generar turno'}, status=500)
            else:
                print("aca la lógica de pago empieza")
                servicio = request.POST.get('servicio')
                servicio_id = await sync_to_async(lambda: models.Servicios.objects.get(servicioID=servicio))()
                horario = request.POST.get('horario')
                fecha = request.POST.get('fecha')
                motivo = request.POST.get('motivo')
                obra_social = await sync_to_async(lambda: ObrasSociales.objects.get(obraID=request.user.obraID_id))()
                print(obra_social.discount)
                precio = servicio_id.precio * (1 - obra_social.discount / 100)

                try:
                    return redirect(reverse('pay-turno') + f'?servicio={servicio_id.nombre}&servicio_id={servicio_id.servicioID}&motivo={motivo}&horario={horario}&fecha={fecha}&precio={precio}')
                except Exception as e:
                    print(f'Error: {e.__class__}\nData: {e.args}')
                    return response.JsonResponse({'error': f'{e}'}, status=404)
        except Exception as err:
            print("un error we")
            print(f'Error: {err.__class__}\nData: {err.args}')
            return response.JsonResponse({
                'error':f'{err}'
            },status=404)

class PayTurnoView(View):
    async def get(self, request):
        servicio = request.GET.get('servicio')
        motivo = request.GET.get('motivo')
        horario = request.GET.get('horario')
        fecha = request.GET.get('fecha')
        precio = request.GET.get('precio')

        # Configurar las credenciales de MercadoPago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

        # Crear una preferencia de pago
        preference_data = {
            "items": [
                {
                    "title": servicio,
                    "currency_id": "ARS",
                    "quantity": 1,
                    "unit_price": float(precio)
                }
            ],
            "back_urls": {
                "success": "https://9457-181-228-78-24.ngrok-free.app/user/panel/",
                "failure": "https://www.google.com/",
                "pending": "https://www.youtube.com/"
            },
            "auto_return": "approved"
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # Verificar si la respuesta contiene la clave 'init_point'
            if 'init_point' not in preference:
                raise KeyError("La respuesta de MercadoPago no contiene la clave 'init_point'")

            # Obtener la URL de pago
            payment_url = preference["init_point"]

            # Generar el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(payment_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Guardar la imagen en un archivo temporal
            img_path = "mysite/static/qr/qr_code.png"
            img.save(img_path)

            # Crear la cita y el turno antes del pago
            servicio_obj = await sync_to_async(lambda: models.Servicios.objects.get(nombre=servicio))()
            especialidad = await sync_to_async(lambda: servicio_obj.especialidadID)()
            medicos = await sync_to_async(lambda: list(models.Medicos.objects.filter(especialidadID=especialidad)))()
            medico = choice(medicos)
            departamento = await sync_to_async(lambda: models.Departamentos.objects.get(departamentoID=medico.especialidadID.departamentoID.departamentoID))()

            cita = await sync_to_async(models.Citas.objects.create)(
                servicioID=servicio_obj,
                userID=request.user,
                medicoID=medico,
                horarioID=await sync_to_async(lambda: models.Horario_medicos.objects.get(horarioID=horario))(),
                motivo=motivo,
                estado='Sin Pagar',
                departamentoID=departamento,
            )

            turno = await sync_to_async(models.Turnos.objects.create)(
                citaID=cita,
                servicioID=servicio_obj,
                medicoID=medico,
                motivo=motivo,
                estado='Sin Pagar',
                fecha=fecha,
                userID=request.user,
                fecha_limt=fecha
            )

            return TemplateResponse(request, 'turnero/pay-turno.html', {
                'servicio': servicio,
                'motivo': motivo,
                'horario': horario,
                'fecha': fecha,
                'qr_code_path': img_path,
                'payment_url': payment_url
            })

        except Exception as err:
            print(f'Error: {err.__class__}\nData: {err.args}')
            return response.JsonResponse({'error': f'{err}'}, status=404)
            
@method_decorator(csrf_exempt, name='dispatch')
class MercadoPagoWebhookView(View):
    async def get(self, request):
        return HttpResponseRedirect(reverse('payment_success'))

    async def post(self, request):
        data = json.loads(request.body)
        print("Received data:", data)  

        try:
            payment_id = data['data']['id']
            payment_status = 'approved'  


            cita = await sync_to_async(lambda: models.Citas.objects.filter(estado='Sin Pagar').first())()
            turno = await sync_to_async(lambda: models.Turnos.objects.filter(estado='Sin Pagar').first())()

            if not cita or not turno:
                raise ValueError("Cita o turno no encontrados para el usuario actual")
            
            cita.estado = 'Pagado'
            await sync_to_async(cita.save)()

            turno.estado = 'Pagado'
            await sync_to_async(turno.save)()

            return HttpResponse(status=200)

        except Exception as e:
            print("Error:", e)  
            return HttpResponse(status=500)
        
class PaymentSuccessful(View):
    def get(self, request, servicio_id):
        success(request, '¡Pago realizado correctamente!')
        return redirect(request, 'user/panel.html', servicio_id=servicio_id) 

class PaymentFailed(View):
    def get(self, request, servicio_id):
        error(request, 'Error al realizar el pago.')
        return redirect(request, 'Home', servicio_id=servicio_id)

class PaypalIPNView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            transaccion = models.TransaccionPaypal(
                payer_id=request.POST['payer_id'],
                payment_date=request.POST['payment_date'],
                payment_status=request.POST['payment_status'],
                invoice=request.POST['invoice'],
                first_name=request.POST['first_name'],
                payer_status=request.POST['payer_status'],
                payer_email=request.POST['payer_email'],
                txn_id=request.POST['txn_id'],
                receiver_id=request.POST['receiver_id'],
                residence_country=request.POST['residence_country'],
                payment_gross=request.POST['payment_gross'],
                custom=request.POST['custom'],
            )
            transaccion.save()
            return HttpResponse(status=200)
        except Exception as err:
            print(f'Error: {err.__class__}\nData: {err.args}')
            return HttpResponse(status=404)

class TurnoData(View):

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
            turno = await database_sync_to_async(models.Turnos.objects.get)(TurnoID=id)
            await database_sync_to_async(lambda :turno.delete)()
            return response.JsonResponse({
                'url':'/user/panel/'
            },status=200)
        except models.Turnos.DoesNotExist:
            return HttpResponseNotFound("Turno no encontrado",status=404)
        except Exception as err:
            return HttpResponse("Error al eliminar el turno",status=500)
    
    async def post(self, request, id):
        try:
            pass

        except Exception as err:
            pass

class ComprobanteDownloadView(LoginRequiredMixin, View):
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
            p = Canvas(buffer, pagesize=letter)

            # Encontrar la ruta a los logos
            logo_path = find('img/Logo-SDLG-name.png')

            p.drawImage(logo_path, 40, 700, width=80, height=80)

            p.setFont("Helvetica-Bold", 16)
            p.drawString(200, 750, "Comprobante de Turno")

            p.setFont("Helvetica", 12)
            p.drawString(40, 680, f"Código del Turno: YY-{turno.TurnoID}")
            p.drawString(40, 660, f"Paciente: {usuario.nombre} {usuario.apellido}")
            p.drawString(40, 640, f"Médico: {medico.nombre} {medico.apellido}")
            p.drawString(40, 620, f"Horario: {horario.hora}")
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
