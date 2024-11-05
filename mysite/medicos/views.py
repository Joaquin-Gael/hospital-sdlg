from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from user.models import Usuarios, ObrasSociales
from turnero.models import Citas
from .models import Medicos, Ubicaciones, Horario_medicos, Departamentos

# Create your views here.

class MedicPanel(View):
    #async def dispatch(self, request, *args, **kwargs):
    #    is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
    #    has_perms = await sync_to_async(request.user.has_perm)('view_panel_medic')
    #    if not is_authenticated:
    #        messages.error(request,'No estas autorizado')
    #        return HttpResponseRedirect(redirect_to=reverse_lazy('Home'))
    #    if not has_perms:
    #        messages.warning(request, 'No tiene permiso')
    #        return HttpResponseRedirect(redirect_to=reverse_lazy('Home'))
    #    return await super().dispatch(request, *args, **kwargs)

    async def get(self, request):
        #messages.success(request, message='Autorizado')
        #medic_id = request.user.medicoID
        #medic_with_user_and_schedules  = await database_sync_to_async(
        #    Medicos.objects.select_related('userID').prefetch_related('citas_set').get
        #)(medicoID=medic_id)

        #patient = medic_with_user_and_schedules.userID
        #schedules = medic_with_user_and_schedules.citas_set.all()

        #schedules_data = await sync_to_async(list)(
        #    schedules.values('citaID', 'fecha', 'motivo')
        #)

        schedules_data = [
            Citas(
                servicioID_id=1,
                userID_id=1,
                medicoID_id=1,
                motivo="Consulta general",
                estado="Pendiente",
                fecha=timezone.now().date(),
                horarioID_id=1,
                departamentoID_id=1,
            ),
            Citas(
                servicioID_id=2,
                userID_id=2,
                medicoID_id=2,
                motivo="Revisión cardiológica",
                estado="Confirmada",
                fecha=timezone.now().date(),
                horarioID_id=2,
                departamentoID_id=2,
            ),
            Citas(
                servicioID_id=3,
                userID_id=3,
                medicoID_id=3,
                motivo="Control de diabetes",
                estado="Pendiente",
                fecha=timezone.now().date(),
                horarioID_id=3,
                departamentoID_id=3,
            ),
            Citas(
                servicioID_id=4,
                userID_id=4,
                medicoID_id=4,
                motivo="Consulta de seguimiento",
                estado="Cancelada",
                fecha=timezone.now().date(),
                horarioID_id=4,
                departamentoID_id=4,
            ),
            Citas(
                servicioID_id=5,
                userID_id=5,
                medicoID_id=5,
                motivo="Evaluación de dolor crónico",
                estado="Reprogramada",
                fecha=timezone.now().date(),
                horarioID_id=5,
                departamentoID_id=5,
                ),
            ]

        return TemplateResponse(
            request,
            'medicos/panel.html',
            {
                'schedules':schedules_data,
            #    'patient':patient
            }
        )

    #TODO: hacer el resto de methods

#TODO: hacer mas vistas que tengan que ver con los medocos