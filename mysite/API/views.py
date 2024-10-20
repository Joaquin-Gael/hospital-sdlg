from rest_framework import (viewsets,status,response,decorators,permissions)
from .serializers import *
from turnero.models import * 
from medicos.models import (Ubicaciones,Medicos,Departamentos,Especialidades,Horario_medicos)
from user.models import Usuarios
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='turnos', detail=True)
    def get_by_user(self, request, pk=1):
        try:
            turnos:list = Turnos.objects.filter(userID=pk)
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
            return response.Response(list_turn, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err':err.__class__
            }, status=status.HTTP_404_NOT_FOUND)
    
    @decorators.action(['GET'], url_path='data', detail=True)
    def get_user_data(self, request, pk=1):
        try:
            user = Usuarios.objects.get(userID=pk)
            data = {
                'nombre':user.nombre,
                'apellido':user.apellido,
                'email':user.email,
                'telefono':user.telefono,
                'imagen':user.imagen,
                'dni':user.dni,
                'contrseña':user.get_contraseña
            }

            json.dumps(data)
            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return response.Response({
                'err':e.__class__
            },status=404)
    
class UbicationViewSet(viewsets.ModelViewSet):
    queryset = Ubicaciones.objects.all()
    serializer_class = UbicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Especialidades.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = Medicos.objects.all()
    serializer_class = DoctorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SchedulesViewSet(viewsets.ModelViewSet):
    queryset = Horario_medicos.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='horarios', detail=True)
    def get_by_service(self, request, pk=None):
        try:
            servicio_id = pk
            servicio = Servicios.objects.get(servicioID=servicio_id)
            especialidad_id = servicio.especialidadID
            medicos = Medicos.objects.filter(especialidadID=especialidad_id)
            horarios = Horario_medicos.objects.filter(medicoID__in=medicos)

            list_horarios = []
            for horario in horarios:
                data = {
                    'id': horario.horarioID,
                    'medico': {
                        'id': horario.medicoID.medicoID,
                        'nombre': horario.medicoID.nombre
                    },
                    'hora': str(horario.hora)
                }
                json.dumps(data)
                list_horarios.append(data)
            
            json.dumps(list_horarios)
            return response.Response(list_horarios, status=status.HTTP_200_OK)
        
        except Exception as err:    
            print(err)
            return response.Response({
                'err':err.__class__
            }, status=status.HTTP_404_NOT_FOUND)


class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = AppointmentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShiftsViewSet(viewsets.ModelViewSet):
    queryset = Turnos.objects.all()
    serializer_class = ShiftsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


