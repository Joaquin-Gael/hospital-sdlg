from ninja import Router, ModelSchema, Schema, Form
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Departamentos
from API.serializers import BaseSerializer

# Create your views here.

class DepartamentSchema(ModelSchema):
    class Meta:
        model=Departamentos
        fields='__all__'

class DepartamentSchemaPut(ModelSchema):
    class Meta:
        model=Departamentos
        fields='__all__'
        fields_optional='__all__'

department_router = Router()

@department_router.get('/')
async def list_department(request):
    department_count = await database_sync_to_async(Departamentos.objects.count)()
    department_list = await database_sync_to_async(list)(Departamentos.objects.all().order_by('departamentoID'))
    serialized_data:list = []
    for object in department_list:
        serialized_data.append(DepartamentSchema.from_orm(object).dict())

    return JsonResponse({'count': department_count, 'locations': serialized_data})

#TODO: hacer el resto de vistas