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
    """
        Retrieve a list of all locations.

        This endpoint returns a list of all locations available in the system,
        along with the total count of locations. The locations are ordered by
        their unique identifier.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.

        Returns:
        - JsonResponse: A JSON response containing the count of locations
          and a list of their details.

        Example response:
        {
            "count": 3,
            "locations": [
                {
                    "ubicacionID": 1,
                    "nombre": "Sucursal Central",
                    "direccion": "Av. Principal 123",
                    "telefono": "123456789"
                },
                {
                    "ubicacionID": 2,
                    "nombre": "Sucursal Norte",
                    "direccion": "Calle Secundaria 456",
                    "telefono": "987654321"
                },
                {
                    "ubicacionID": 3,
                    "nombre": "Sucursal Sur",
                    "direccion": "Calle Tercera 789",
                    "telefono": "456789123"
                }
            ]
        }
        """
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
    """
        Retrieve a specific location by its ID.

        This endpoint returns the details of a location specified by its unique
        identifier (ubicacionID). If the location does not exist, a 404 error
        will be returned.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.
        - location_id (int): The unique identifier of the location to retrieve.

        Returns:
        - JsonResponse: A JSON response containing the details of the location
          specified by the location_id.

        Example response:
        {
            "location": {
                "ubicacionID": 1,
                "nombre": "Sucursal Central",
                "direccion": "Av. Principal 123",
                "telefono": "123456789"
            }
        }
        """
    new_location = Ubicaciones(**payload.dict())
    location_serializer = BaseSerializer(
        model_class=Ubicaciones,
        instance=new_location
    )

    serialized_data = location_serializer.serialize()

    return JsonResponse({'location':serialized_data})

@location_router.put('/{location_id}')
async def update_location(request, location_id: int, payload: LocatiosSchemaPut):
    """
        Update the details of a specific location by its ID.

        This endpoint allows for updating the details of a location specified
        by its unique identifier (ubicacionID). The request should include
        a payload with the fields to be updated. If no fields are provided
        for update, a 400 error will be returned.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.
        - location_id (int): The unique identifier of the location to update.
        - payload (LocatiosSchemaPut): The payload containing the updated
          details of the location.

        Returns:
        - JsonResponse: A JSON response containing the updated details of
          the location.

        Example request:
        PUT /locations/1
        {
            "nombre": "Nueva Sucursal",
            "direccion": "Av. Nueva 456",
            "telefono": "987654321"
        }

        Example response:
        {
            "location": {
                "ubicacionID": 1,
                "nombre": "Nueva Sucursal",
                "direccion": "Av. Nueva 456",
                "telefono": "987654321"
            }
        }
        """
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