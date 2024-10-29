from ninja import Router, ModelSchema, Form
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Servicios

# Create your views here.

class ServiceSchema(ModelSchema):
    class Meta:
        model=Servicios
        fields='__all__'

class ServiceSchemaPut(ModelSchema):
    class Meta:
        model=Servicios
        fields='__all__'
        fields_optional = '__all__'

service_router = Router()

@service_router.get('/')
async def list_services(request):
    """
        Retrieve a list of all services.

        This endpoint returns a list of all services available in the system,
        ordered by their unique identifier.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.

        Returns:
        - JsonResponse: A JSON response containing the count of services
          and a list of their details.

        Example response:
        {
            "count": 2,
            "services": [
                {
                    "servicioID": 1,
                    "nombre": "Consulta Médica",
                    "descripcion": "Servicio de atención médica general."
                },
                {
                    "servicioID": 2,
                    "nombre": "Urgencias",
                    "descripcion": "Atención médica de emergencia."
                },
                ...
            ]
        }
        """
    services_list = await database_sync_to_async(list)(Servicios.objects.all().order_by('servicioID'))
    serialized_data = []
    for object in services_list:
        serialized_data.append(ServiceSchema.from_orm(object).dict())

    return JsonResponse({'count':len(services_list), 'services':serialized_data}, status=200)

@service_router.get('/{service_id}/')
async def get_service(request, service_id: int):
    service = await database_sync_to_async(Servicios.objects.get)(servicioID=service_id)
    serialized_data = ServiceSchema.from_orm(service).dict()

    return JsonResponse({'service':serialized_data}, status=200)

#TODO: Hacer el resto de las vistas de los servicios