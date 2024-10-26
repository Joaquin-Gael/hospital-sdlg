from ninja import Router, ModelSchema, Schema, File, Form
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Horario_medicos
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
    schedule_list:list = await database_sync_to_async(list)(Horario_medicos.objects.all().order_by('horarioID'))
    serialized_data = []
    for object in schedule_list:
        serialized_data.append(ScheduleSchema.from_orm(object).dict())

    return JsonResponse({'count': len(schedule_list), 'value': serialized_data}, status=200)

@schedule_router.get('/{schedule_id}/')
async def get_schedule(request, schedule_id:int):
    schedule = await database_sync_to_async(Horario_medicos.objects.get)(horarioID=schedule_id)
    serialized_schedule = ScheduleSchema.from_orm(schedule).dict()
    return JsonResponse({'schedule':serialized_schedule}, status=200)


@schedule_router.post('/')
async def create_schedule(request, payload: ScheduleSchema):
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
    data = payload.dict(exclude_defaults=True)
    if data:
        old_schedule = await database_sync_to_async(Horario_medicos.objects.get)(horarioID=schedule_id)
        for key, value in data.items():
            setattr(old_schedule, key, value)
        serialized_data = ScheduleSchema.from_orm(old_schedule).dict()
        return JsonResponse({'schedule':serialized_data}, status=200)
    else:
        return JsonResponse({'detail':'se nesesita algun dato para cambiar'}, status=200)

@schedule_router.get('/{service_id}/schedules', tags=['Service Schedules'])
async def schedules_list_from_service(request, service_id: int):
    schedules_list = await database_sync_to_async(list)(Horario_medicos.objects.get(servicioID=service_id))
    serialized_data = []
    for object in schedules_list:
        serialized_data.append(ScheduleSchema.from_orm(object).dict())

    return JsonResponse({'count':len(schedules_list), 'schedules':serialized_data}, status=200)