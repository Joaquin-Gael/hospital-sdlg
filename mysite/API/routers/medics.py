from ninja import Router, ModelSchema, Schema, File, Form, Field
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Medicos
from API.serializers import BaseSerializer
from typing import Optional
from datetime import date


# Create your views here.
class MedicosSchema(ModelSchema):
    imagen: Optional[UploadedFile] = File(...)
    class Meta:
        model=Medicos
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout']

class MedicosSchemaPut(Schema):
    password: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    dni: Optional[str]
    fecha_nacimiento: Optional[date]  # Manejo de fechas
    email: Optional[str]
    telefono: Optional[str]
    contraseña: Optional[str]  # Si 'contraseña' es diferente a 'password'
    imagen_url: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]

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

@medic_router.get('/{medic_id}/')
async def get_medic(request, medic_id:int):
    medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
    medic_serialized = BaseSerializer(
        model_class=Medicos,
        instance=medic,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_medic = medic_serialized.serialized()
    return JsonResponse({'medic':serialized_medic}, status=200)

@medic_router.post('/')
async def create_medic(request, payload: Form[MedicosSchema], imagen: UploadedFile = File(None)):
    new_medic = Medicos()
    data = payload.dict()
    del data['contraseña']
    del data['imagen']
    if imagen:
        new_medic.imagen.save(imagen.name, imagen)
    for field_name, value in data.items():
        if field_name == 'password':
            new_medic.set_password(value)
            new_medic.set_contraseña(value)
        else:
            setattr(new_medic, field_name, value)
    user_serializer = BaseSerializer(
        model_class=Medicos,
        instance=new_medic,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = user_serializer.serialize()
    #new_user.save()
    return serialized_data

@medic_router.put('/{medic_id}/imagen/', tags=['Media Medic'])
async def update_medic_image(request, medic_id:int, imagen: UploadedFile = File()):
    if imagen:
        old_medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
        old_medic.imagen = imagen

        user_serializer = BaseSerializer(
            model_class=Medicos,
            instance=old_medic,
            deal_for_field_list={'contraseña': 'get_contraseña'}
        )
        serialized_data = user_serializer.serialize()

        return JsonResponse({'medic': serialized_data}, status=200)
    else:
        return JsonResponse({'detail':'Almenos un campo tiene que estar cambiado'}, status=400)

@medic_router.put('/{medic_id}/')
async def update_medic(request, medic_id:int, payload: Form[MedicosSchemaPut]):
    data = payload.dict()
    if data:
        old_medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
        for key, value in data:
            setattr(old_medic, key, value)

        user_serializer = BaseSerializer(
            model_class=Medicos,
            instance=old_medic,
            deal_for_field_list={'contraseña': 'get_contraseña'}
        )
        serialized_data = user_serializer.serialize()

        return JsonResponse({'medic': serialized_data}, status=200)
    else:
        return JsonResponse({'detail': 'Almenos un campo tiene que estar cambiado'}, status=400)