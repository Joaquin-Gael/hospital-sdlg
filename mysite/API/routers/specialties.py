from ninja import Router, ModelSchema, Form, Field
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Especialidades


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
    """
        Retrieve a list of all medical specialties.

        This endpoint returns a list of all medical specialties available in
        the system. The specialties are ordered by their unique identifier.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.

        Returns:
        - JsonResponse: A JSON response containing the count of specialties
          and a list of their details.

        Example response:
        {
            "count": 3,
            "specialties": [
                {
                    "especialidadID": 1,
                    "nombre": "Cardiología",
                    "descripcion": "Estudio y tratamiento de enfermedades del corazón."
                },
                {
                    "especialidadID": 2,
                    "nombre": "Pediatría",
                    "descripcion": "Atención médica para niños y adolescentes."
                },
                ...
            ]
        }
        """
    specialties_list = await database_sync_to_async(list)(Especialidades.objects.all().order_by('especialidadID'))
    serialized_data = []
    for object in specialties_list:
        serialized_data.append(SpecialtySchema.from_orm(object).dict())

    return JsonResponse({'count':len(specialties_list), 'specialties':serialized_data}, status=200)

@specialty_router.get('/speciality_id/')
async def get_speciality(request, speciality_id: int):
    speciality = await database_sync_to_async(Especialidades.objects.get)(especialidadID=speciality_id)
    serialized_data = SpecialtySchema.from_orm(speciality).dict()

    return JsonResponse({'speciality':serialized_data}, status=200)

#TODO: hacer el resto de vistas