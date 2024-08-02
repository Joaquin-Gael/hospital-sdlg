from rest_framework import (viewsets,status,response,decorators,permissions)
from .serializers import *
from turnero.models import * 
from medicos.models import (Ubicaciones,Medicos,Departamentos,Especialidades,Horario_medicos)
from blog.models import Testimonios
from user.models import Usuarios
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @decorators.action(['GET'], url_path='turnos', detail=True)
    def get_by_user(self, request, pk=1):
        try:
            turnos = Turnos.objects.filter(userID=pk)
            list_turn = []
            for x in turnos:
                print(x)
                data = {
                    'id': x.TurnoID, 
                    'medico': {
                        'id': x.citaID.medicoID.medicoID,
                        'nombre': x.citaID.medicoID.nombre
                    },
                    'horario': {
                        'id': x.citaID.horarioID.horarioID,
                        'hora': str(x.citaID.horarioID.hora_inicio)
                    },
                    'motivo': x.motivo, 
                    'estado': x.estado  
                }
                json.dumps(data)
                list_turn.append(data)
                
            json.dumps(list_turn)
            print(list_turn)
            return response.Response(list_turn, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err':err.__class__
            }, status=status.HTTP_404_NOT_FOUND)

    
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


class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = AppointmentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShiftsViewSet(viewsets.ModelViewSet):
    queryset = Turnos.objects.all()
    serializer_class = ShiftsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
