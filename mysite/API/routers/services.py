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
    services_list = await database_sync_to_async(list)(Servicios.objects.all().order_by('servicioID'))
    serialized_data = []
    for object in services_list:
        serialized_data.append(ServiceSchema.from_orm(object).dict())

    return JsonResponse({'count':len(services_list), 'services':serialized_data}, status=200)

#TODO: Hacer el resto de las vistas de los servicios