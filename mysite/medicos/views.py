from django.template.response import TemplateResponse
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from user.models import Usuarios, ObraSociales
from turnero.models import Citas
from .models import Medicos, Ubicaciones, Horario_medicos, Departamentos

# Create your views here.

class MedicPanel(View):
    async def dispatch(self, request, *args, **kwargs):
        is_authenticated = await sync_to_async(lambda:request.user.is_authenticated)()
        has_perms = await sync_to_async(request.user.has_perm)('view_panel_medic')

        print(is_authenticated, has_perms)
        return await super().dispatch(request, *args, **kwargs)

    async def get(self, request):
        messages.success(request, message='Autorizado')
        return TemplateResponse(request, 'medicos/panel.html')