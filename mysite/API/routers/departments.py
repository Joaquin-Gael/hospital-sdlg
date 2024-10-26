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
    """
        Retrieve a list of all departments.

        This endpoint returns a list of all departments available in the system,
        along with a count of the total number of departments. The response
        includes serialized department details.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.

        Returns:
        - JsonResponse: A JSON response containing the count of departments
          and the details of each department.

        Example response:
        {
            "count": 3,
            "locations": [
                {
                    "departamentoID": 1,
                    "nombre": "Recursos Humanos",
                    "descripcion": "Gestión de personal y recursos humanos"
                },
                {
                    "departamentoID": 2,
                    "nombre": "Tecnología",
                    "descripcion": "Soporte técnico y desarrollo de software"
                },
                {
                    "departamentoID": 3,
                    "nombre": "Finanzas",
                    "descripcion": "Gestión financiera y contabilidad"
                }
            ]
        }
        """
    department_count = await database_sync_to_async(Departamentos.objects.count)()
    department_list = await database_sync_to_async(list)(Departamentos.objects.all().order_by('departamentoID'))
    serialized_data:list = []
    for object in department_list:
        serialized_data.append(DepartamentSchema.from_orm(object).dict())

    return JsonResponse({'count': department_count, 'locations': serialized_data})

#TODO: hacer el resto de vistas