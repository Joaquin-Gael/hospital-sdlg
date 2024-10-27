from ninja import Router, ModelSchema, Schema, File, Form
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Horario_medicos,Servicios,Medicos
from django.shortcuts import get_object_or_404
from typing import Optional
from datetime import date

# Create your views here.
class ScheduleSchema(ModelSchema):
    class Meta:
        model=Horario_medicos
        fields = '__all__'

class ScheduleSchemaPut(ModelSchema):
    class Meta:
        model=Horario_medicos
        fields = '__all__'
        fields_optional = '__all__'

schedule_router = Router()

@schedule_router.get('/')
async def list_schedule(request):
    """
    Retrieve a list of medical schedules.

    This endpoint fetches all medical schedules from the database,
    orders them by `horarioID`, and returns a JSON response containing
    the count of schedules and the serialized data for each schedule.

    Parameters:
    - request: The HTTP request object. This is automatically provided
      by the FastAPI framework.

    Returns:
    - JsonResponse: A JSON response containing:
        - `count` (int): The total number of schedules retrieved.
        - `value` (list): A list of serialized medical schedule objects.

    Example response:
    {
        "count": 10,
        "value": [
            {
                "horarioID": 1,
                "otherField": "value",
                ...
            },
            ...
        ]
    }
    """
    schedule_list:list = await database_sync_to_async(list)(Horario_medicos.objects.all().order_by('horarioID'))
    serialized_data = []
    for object in schedule_list:
        serialized_data.append(ScheduleSchema.from_orm(object).dict())

    return JsonResponse({'count': len(schedule_list), 'value': serialized_data}, status=200)

@schedule_router.get('/{schedule_id}/')
async def get_schedule(request, schedule_id:int):
    """
        Retrieve a specific medical schedule by its ID.

        This endpoint fetches a medical schedule from the database
        using the provided `schedule_id`. If a schedule with the
        specified ID exists, it returns the serialized data for that
        schedule.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - schedule_id (int): The ID of the medical schedule to retrieve.

        Returns:
        - JsonResponse: A JSON response containing:
            - `schedule` (dict): The serialized medical schedule object.

        Raises:
        - 404 Not Found: If no schedule with the specified `schedule_id`
          exists.

        Example response:
        {
            "schedule": {
                "horarioID": 1,
                "otherField": "value",
                ...
            }
        }
    """
    schedule = await database_sync_to_async(Horario_medicos.objects.get)(horarioID=schedule_id)
    serialized_schedule = ScheduleSchema.from_orm(schedule).dict()
    return JsonResponse({'schedule':serialized_schedule}, status=200)


@schedule_router.post('/')
async def create_schedule(request, payload: ScheduleSchema):
    """
        Create a new medical schedule.

        This endpoint allows the creation of a new medical schedule
        in the database using the provided payload. The payload should
        contain the necessary fields to create a new schedule.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - payload (ScheduleSchema): The data required to create a new
          medical schedule, validated against the ScheduleSchema model.

        Returns:
        - JsonResponse: A JSON response containing:
            - `schedule` (dict): The serialized medical schedule object
              that was created.

        Raises:
        - 400 Bad Request: If the provided payload is invalid or
          if an error occurs during schedule creation.

        Example request body:
        {
            "field1": "value1",
            "field2": "value2",
            ...
        }

        Example response:
        {
            "schedule": {
                "horarioID": 1,
                "otherField": "value",
                ...
            }
        }
    """
    try:
        new_schedule = Horario_medicos(**payload.dict())
        new_schedule.save()
        serialized_data = ScheduleSchema.from_orm(new_schedule).dict()
        return JsonResponse({'schedule':serialized_data}, status=200)
    except Exception as e:
        pass
        #TODO: manejo de errores

@schedule_router.put('/{schedule_id}/')
async def update_scheduel(request, schedule_id: int, payload: ScheduleSchemaPut):
    """
        Update an existing medical schedule by its ID.

        This endpoint updates a specific medical schedule in the database
        using the provided `schedule_id` and the data from the payload.
        Only the fields provided in the payload will be updated.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - schedule_id (int): The ID of the medical schedule to update.
        - payload (ScheduleSchemaPut): The data containing the fields to
          update, validated against the ScheduleSchemaPut model.

        Returns:
        - JsonResponse: A JSON response containing:
            - `schedule` (dict): The serialized medical schedule object
              after the update.

        Raises:
        - 404 Not Found: If no schedule with the specified `schedule_id`
          exists.
        - 400 Bad Request: If no data is provided for the update.

        Example request body:
        {
            "field1": "new_value1",
            "field2": "new_value2",
            ...
        }

        Example response:
        {
            "schedule": {
                "horarioID": 1,
                "otherField": "updated_value",
                ...
            }
        }
    """
    data = payload.dict(exclude_defaults=True)
    if data:
        old_schedule = await database_sync_to_async(Horario_medicos.objects.get)(horarioID=schedule_id)
        for key, value in data.items():
            setattr(old_schedule, key, value)
        serialized_data = ScheduleSchema.from_orm(old_schedule).dict()
        return JsonResponse({'schedule':serialized_data}, status=200)
    else:
        return JsonResponse({'detail':'se nesesita algun dato para cambiar'}, status=400)

@schedule_router.get('/{service_id}/schedules', tags=['Service Schedules'])
async def schedules_list_from_service(request, service_id: int):
    """
       Retrieve a list of medical schedules for a specific service.

       This endpoint fetches all medical schedules associated with the
       specified `service_id`. It returns a JSON response containing
       the count of schedules and the serialized data for each schedule.

       Parameters:
       - request: The HTTP request object. This is automatically provided
         by the FastAPI framework.
       - service_id (int): The ID of the service for which to retrieve
         the medical schedules.

       Returns:
       - JsonResponse: A JSON response containing:
           - `count` (int): The total number of schedules retrieved.
           - `schedules` (list): A list of serialized medical schedule
             objects associated with the specified service.

       Raises:
       - 404 Not Found: If no schedules exist for the specified `service_id`.

       Example response:
       {
           "count": 5,
           "schedules": [
               {
                   "horarioID": 1,
                   "otherField": "value",
                   ...
               },
               ...
           ]
       }
    """
    schedules_list = await database_sync_to_async(list)(await database_sync_to_async(Horario_medicos.objects.filter)(servicioID=service_id))
    serialized_data = []
    for object in schedules_list:
        serialized_data.append(ScheduleSchema.from_orm(object).dict())

    return JsonResponse({'count':len(schedules_list), 'schedules':serialized_data}, status=200)

@schedule_router.get('/{service_id}/days', tags=['Service Days'])
async def get_available_days(request, service_id: int):
    """
    Retrieve a list of available days for a specific service.

    This endpoint fetches all available days associated with the
    specified `service_id`. It returns a JSON response containing
    the list of available days.

    Parameters:
    - request: The HTTP request object. This is automatically provided
      by the FastAPI framework.
    - service_id (int): The ID of the service for which to retrieve
      the available days.

    Returns:
    - JsonResponse: A JSON response containing:
        - `dias` (list): A list of available days for the specified service.

    Raises:
    - 404 Not Found: If no days are available for the specified `service_id`.

    Example response:
    {
        "dias": [
            {"dia": "Lunes"},
            {"dia": "Martes"},
            ...
        ]
    }
    """
    try:
        # Obtener el servicio
        servicio = await database_sync_to_async(get_object_or_404)(Servicios, servicioID=service_id)
        print("paso 1")

        # Obtener la especialidad del servicio
        especialidad_id = await database_sync_to_async(lambda: servicio.especialidadID)()
        print("paso 2")
        # Obtener los médicos que pertenecen a esa especialidad
        medicos = await database_sync_to_async(Medicos.objects.filter)(especialidadID=especialidad_id)
        print("paso 3")
        # Obtener los horarios de los médicos
        horarios = await database_sync_to_async(Horario_medicos.objects.filter)(medicoID__in=await database_sync_to_async(lambda: medicos)())
        print("paso 4")

        # Obtener los días disponibles
        dias_disponibles = set()
        async for horario in horarios:
            dia = await database_sync_to_async(lambda: horario.dia)()
            dias_disponibles.add(str(dia))
        print("paso 5")

        # Ordenar los días disponibles
        dias_disponibles = sorted(dias_disponibles)

        # Crear la lista de días disponibles
        list_dias = [{'day': dia} for dia in dias_disponibles]
        print("paso todo")

        return JsonResponse({'days_availables': list_dias}, status=200)
    except Exception as err:
        return JsonResponse({'err': str(err.__class__)}, status=404)
