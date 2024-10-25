from ninja import Router, ModelSchema, Schema, File, Form
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Usuarios
from API.serializers import BaseSerializer
from typing import Optional
from datetime import date
from pydantic import Field

# Create your views here.
class UsuarioSchema(ModelSchema):
    imagen: Optional[UploadedFile] = File(...)
    class Meta:
        model=Usuarios
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout']


class UsuarioSchemaPut(Schema):
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

    # Este campo ahora acepta la carga de un archivo de imagen
    imagen: Optional[UploadedFile] = File(None)

    class Config:
        arbitrary_types_allowed = True

user_router = Router()

@user_router.get('/')
async def list_users(request):
    users_count:int = await database_sync_to_async(Usuarios.objects.count)()
    users_list:list = await database_sync_to_async(list)(Usuarios.objects.all().order_by('userID'))
    user_serializer = BaseSerializer(
        model_class=Usuarios,
        instance=users_list,
        deal_for_field_list={'contraseña':'get_contraseña'}
    )
    serialized_data = user_serializer.serialize()
    return JsonResponse({'count': users_count, 'value': serialized_data}, status=200)

@user_router.get('/{user_id}/')
async def get_user(request, user_id:int):
    user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
    user_serializer = BaseSerializer(
        model_class=Usuarios,
        instance=user,
        deal_for_field_list={'contraseña':'get_contraseña'}
    )
    serialized_user = user_serializer.serialize()
    return JsonResponse({"user": serialized_user}, status=200)

@user_router.post('/')
async def create_user(request, payload: Form[UsuarioSchema], imagen: UploadedFile = File(None)):
    new_user = Usuarios()
    data = payload.dict()
    del data['contraseña']
    del data['imagen']
    if imagen:
        new_user.imagen.save(imagen.name, imagen)
    for field_name, value in data.items():
        if field_name == 'password':
            new_user.set_password(value)
            new_user.set_contraseña(value)
        else:
            setattr(new_user, field_name, value)
    user_serializer = BaseSerializer(
        model_class=Usuarios,
        instance=new_user,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = user_serializer.serialize()
    #new_user.save()
    return serialized_data

@user_router.put('/{user_id}/')
async def update_user(request, user_id:int, payload: Form[UsuarioSchemaPut], imagen: UploadedFile = File(None)):
    data = {key:value for key, value in payload.dict(exclude_unset=True) if value}
    data['imagen'] = imagen
    old_user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
    for key, value in data:
        setattr(old_user, key, value)

    user_serializer = BaseSerializer(
        model_class=Usuarios,
        instance=old_user,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = user_serializer.serialize()
    return JsonResponse({'user':serialized_data},status=200)