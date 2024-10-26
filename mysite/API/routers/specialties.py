from ninja import Router, ModelSchema, Form, Field
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Especialidades
from API.serializers import BaseSerializer


# Create your views here.

class SpecialtySchema(ModelSchema):
    nombre:str = Field(min_length=1)
    class Meta:
        model=Especialidades
        fields='__all__'

class SpecialtySchemaPut(ModelSchema):
    class Meta:
        model=Especialidades
        exclude=['especialidadID']
        fields_optional='__all__'

specialty_router = Router()

@specialty_router.get('/')
async def list_specialties(request):
    specialties_list = await database_sync_to_async(list)(Especialidades.objects.all().order_by('especialidadID'))
    serialized_data = []
    for object in specialties_list:
        serialized_data.append(SpecialtySchema.from_orm(object).dict())

    return JsonResponse({'count':len(specialties_list), 'specialties':serialized_data}, status=200)

#TODO: hacer el resto de vistas