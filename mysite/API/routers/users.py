from ninja import Router, ModelSchema, Schema, File
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
    userID: Optional[int] = 0
    nombre: Optional[str] = Field(None)
    apellido: Optional[str] = Field(None)

    # Este campo ahora acepta la carga de un archivo de imagen
    imagen: Optional[UploadedFile] = File(...)

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

@user_router.get('/{user_id}')
async def get_user(request, user_id:int):
    user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
    user_serializer = BaseSerializer(
        model_class = Usuarios,
        instance=user,
        deal_for_field_list={'contraseña':'get_contraseña'}
    )
    serialized_user = user_serializer.serialize()
    return JsonResponse({"user": serialized_user}, status=200)

@user_router.post('/')
async def create_user(request, payload:UsuarioSchema, imagen: UploadedFile = File(...)):
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

@user_router.put('/{user_id}')
async def update_user(request, payload:UsuarioSchemaPut, user_id:int, imagen: UploadedFile = File(None)):
    old_user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
    print(old_user)
    print(payload.dict(exclude_unset=True))
