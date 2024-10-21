from medicos.models import (Ubicaciones, Medicos, Departamentos, Especialidades, Horario_medicos)
from rest_framework import (status, response, decorators, permissions)
from django.http import JsonResponse
from adrf.viewsets import ViewSet
from asgiref.sync import sync_to_async
from user.models import Usuarios
from turnero.models import *
from .serializers import *
import json

class UserViewSet(ViewSet):
    queryset = Usuarios.objects.all().order_by('userID')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='turnos', detail=True)
    async def get_by_user(self, request, pk=1):
        try:
            turnos:list = await sync_to_async(Turnos.objects.filter)(userID=pk)
            list_turn = []
            for x in turnos:
                data = {
                    'id': x.TurnoID,
                    'medico': {
                        'id': x.citaID.medicoID.medicoID,
                        'nombre': x.citaID.medicoID.nombre
                    },
                    'horario': {
                        'id': x.citaID.horarioID.horarioID,
                        'hora': str(x.citaID.horarioID.hora)
                    },
                    'motivo': x.motivo,
                    'estado': x.estado
                }
                json.dumps(data)
                list_turn.append(data)

            json.dumps(list_turn)

            return response.Response({'result':list_turn}, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err': err.__class__
            }, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(['GET'], url_path='data', detail=True)
    async def get_user_data(self, request, pk=1):
        try:
            user = await sync_to_async(Usuarios.objects.get)(userID=pk)
            data = {
                'nombre': user.nombre,
                'apellido': user.apellido,
                'email': user.email,
                'telefono': user.telefono,
                'imagen': user.imagen,
                'dni': user.dni,
                'contraseña': user.get_contraseña()
            }

            return response.Response({'result':data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return response.Response({
                'err': e.__class__
            }, status=404)

class UbicationViewSet(ViewSet):
    queryset = Ubicaciones.objects.all().order_by('ubicacionID')
    serializer_class = UbicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DepartmentViewSet(ViewSet):
    queryset = Departamentos.objects.all().order_by('departamentoID')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SpecialtyViewSet(ViewSet):
    queryset = Especialidades.objects.all().order_by('especialidadID')
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DoctorsViewSet(ViewSet):
    queryset = Medicos.objects.all().order_by('medicoID')
    serializer_class = DoctorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SchedulesViewSet(ViewSet):
    queryset = Horario_medicos.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='horarios', detail=True)
    async def get_by_service(self, request, pk=None):
        try:
            servicio_id = pk
            servicio = await sync_to_async(Servicios.objects.get)(servicioID=servicio_id)
            especialidad_id = await servicio.especialidadID
            medicos = await sync_to_async(Medicos.objects.filter)(especialidadID=especialidad_id)
            horarios = await sync_to_async(Horario_medicos.objects.filter)(medicoID__in=medicos)

            list_horarios = []
            for horario in horarios:
                data:dict = {
                    'id': horario.horarioID,
                    'medico': {
                        'id': horario.medicoID.medicoID,
                        'nombre': horario.medicoID.nombre
                    },
                    'hora': str(horario.hora)
                }
                print(data)
                list_horarios.append(data)
                print(list_horarios)
            return response.Response({'result':list_horarios}, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err': str(err.__class__)
            }, status=status.HTTP_404_NOT_FOUND)
            
class AppointmentsViewSet(ViewSet):
    queryset = Citas.objects.all().order_by('citaID')
    serializer_class = AppointmentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShiftsViewSet(ViewSet):
    queryset = Turnos.objects.all().order_by('TurnoID')
    serializer_class = ShiftsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
