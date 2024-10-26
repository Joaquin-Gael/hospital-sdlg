from ninja import Router, ModelSchema, Schema, File, Form
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Ubicaciones
from API.serializers import BaseSerializer
from typing import Optional
from datetime import date


class LocationsSchema(ModelSchema):
    class Meta:
        model=Ubicaciones
        exclude = ['ubicacionID']

class LocatiosSchemaPut(ModelSchema):
    class Meta:
        model=Ubicaciones
        exclude = ['ubicacionID']
        fields_optional = '__all__'

# Create your views here.
location_router = Router()

@location_router.get('/')
async def list_locations(request):
    locations_count = await database_sync_to_async(Ubicaciones.objects.count)()
    locations_list = await database_sync_to_async(list)(Ubicaciones.objects.all().order_by('ubicacionID'))

    location_serializer = BaseSerializer(
        model_class=Ubicaciones,
        instance=locations_list
    )

    serialized_data = location_serializer.serialize()

    return JsonResponse({'count':locations_count, 'locations':serialized_data})

@location_router.get('/{location_id}')
async def get_location(request, location_id: int):
    location = await database_sync_to_async(Ubicaciones.objects.get)(ubicacionID=location_id)

    location_serializer = BaseSerializer(
        model_class=Ubicaciones,
        instance=location
    )

    serialized_location = location_serializer.serialize()

    return JsonResponse({'location':serialized_location}, status=200)

@location_router.post('/')
async def create_location(request, payload: LocationsSchema):
    new_location = Ubicaciones(**payload.dict())

    location_serializer = BaseSerializer(
        model_class=Ubicaciones,
        instance=new_location
    )

    serialized_data = location_serializer.serialize()

    return JsonResponse({'location':serialized_data})

@location_router.put('/{location_id}')
async def update_location(request, location_id: int, payload: LocatiosSchemaPut):
    data = payload.dict(exclude_unset=True)
    if data:
        old_location = await database_sync_to_async(Ubicaciones.objects.get)(ubicacionID=location_id)
        for key, value in data.items():
            setattr(old_location, key, value)
        location_serializer = BaseSerializer(
            model_class=Ubicaciones,
            instance=old_location
        )
        serialized_data = location_serializer.serialize()

        return JsonResponse({'location':serialized_data}, status=200)
    else:
        return JsonResponse({'detail':'Almenos un campo tiene que ser actualizado'}, status=400)