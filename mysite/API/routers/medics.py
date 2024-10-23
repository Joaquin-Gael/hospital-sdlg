from ninja import Router, ModelSchema, Schema, File
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Medicos
from API.serializers import BaseSerializer
from typing import Optional
from datetime import date
from pydantic import Field



# Create your views here.
class MedicosSechema(ModelSchema):
    imagen: Optional[UploadedFile] = File(...)
    class Meta:
        model=Medicos
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout']

class MedicosSchemaPut(Schema):
    password: Optional[str] = Field(None)
    is_superuser: Optional[bool] = False
    username: Optional[str] = Field(None)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    is_staff: Optional[bool] = False
    dni: Optional[str] = Field(None)
    fecha_nacimiento: Optional[date] = Field(None)  # Manejo de fechas
    email: Optional[str] = Field(None)
    telefono: Optional[str] = Field(None)
    contraseña: Optional[str] = Field(None)  # Si 'contraseña' es diferente a 'password'
    is_active: Optional[bool] = True
    imagen_url: Optional[str] = Field(None)
    medicoID: Optional[int] = 0
    nombre: Optional[str] = Field(None)
    apellido: Optional[str] = Field(None)

    # Este campo ahora acepta la carga de un archivo de imagen
    imagen: Optional[UploadedFile] = File(...)

medic_router = Router()

@medic_router.get('/')
async def list_medics(request):
    medics_count:int = await database_sync_to_async(Medicos.objects.count)()
    medics_list:list = await database_sync_to_async(list)(Medicos.objects.all().order_by('medicoID'))
    medics_serializer = BaseSerializer(
        model_class=Medicos,
        instance=medics_list,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = medics_serializer.serialize()
    return JsonResponse({'count': medics_count, 'value': serialized_data}, status=200)