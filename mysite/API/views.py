from medicos.models import (Ubicaciones, Medicos, Departamentos, Especialidades, Horario_medicos)
from rest_framework import (status, response, decorators, permissions)
from adrf.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework import viewsets
from asgiref.sync import sync_to_async
from user.models import Usuarios
from turnero.models import *
from .serializers import *
import json

class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all().order_by('userID')
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
                #json.dumps(data)
                list_turn.append(data)

            #json.dumps(list_turn)

            return response.Response(list_turn, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err': err.__class__
            }, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(['GET'], url_path='data', detail=True)
    def get_user_data(self, request, pk=1):
        try:
            user = Usuarios.objects.get(userID=pk)
            data = {
                'nombre': user.nombre,
                'apellido': user.apellido,
                'email': user.email,
                'telefono': user.telefono,
                'imagen': user.imagen,
                'dni': user.dni,
                'contraseña': user.get_contraseña()
            }

            return response.Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return response.Response({
                'err': e.__class__
            }, status=404)

class UbicationViewSet(ModelViewSet):
    queryset = Ubicaciones.objects.all().order_by('ubicacionID')
    serializer_class = UbicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        horarios = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(horarios, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        horario = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(horario)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horario = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(horario, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        await sync_to_async(horario.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentViewSet(ModelViewSet):
    queryset = Departamentos.objects.all().order_by('departamentoID')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        horarios = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(horarios, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        horario = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(horario)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horario = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(horario, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        await sync_to_async(horario.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SpecialtyViewSet(ModelViewSet):
    queryset = Especialidades.objects.all().order_by('especialidadID')
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        especialidades = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(especialidades, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        especialidad = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(especialidad)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        especialidad = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        especialidad = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(especialidad, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        especialidad = await sync_to_async(self.get_object)()
        await sync_to_async(especialidad.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class DoctorsViewSet(ModelViewSet):
    queryset = Medicos.objects.all().order_by('medicoID')
    serializer_class = DoctorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        medicos = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(medicos, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        medicos = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(medico)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medico = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        medico = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(medico, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        medico = await sync_to_async(self.get_object)()
        await sync_to_async(medico.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class SchedulesViewSet(ModelViewSet):
    queryset = Horario_medicos.objects.all().order_by('horarioID')
    serializer_class = SchedulesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        horarios = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(horarios, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        horario = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(horario)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horario = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(horario, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        await sync_to_async(horario.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    
    @decorators.action(['GET'], url_path='horarios', detail=True)
    async def get_by_service(self, request, pk=None):
        try:
            servicio = await sync_to_async(Servicios.objects.get)(servicioID=pk)
            especialidad_id = await sync_to_async(lambda:servicio.especialidadID)()
            medicos:list = await sync_to_async(Medicos.objects.filter)(especialidadID=especialidad_id)
            horarios:list = await sync_to_async(Horario_medicos.objects.filter)(medicoID__in=await sync_to_async(lambda:medicos)())
            
            list_horarios = []
            async for horario in horarios:
                data:dict = {
                    'id': horario.horarioID,
                    'medico': {
                        'id': await sync_to_async(lambda:horario.medicoID.medicoID)(),
                        'nombre': await sync_to_async(lambda:horario.medicoID.nombre)()
                    },
                    'hora': await sync_to_async(lambda:str(horario.hora))()
                }
    
                #print(data)
                list_horarios.append(data)
                #print(list_horarios)
            return response.Response(list_horarios, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return response.Response({
                'err': str(err.__class__)
            }, status=status.HTTP_404_NOT_FOUND)
            
class AppointmentsViewSet(ModelViewSet):
    queryset = Citas.objects.all().order_by('citaID')
    serializer_class = AppointmentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        horarios = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(horarios, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        horario = await sync_to_async(self.get_object)() 
        serializer = self.get_serializer(horario)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horario = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(horario, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        await sync_to_async(horario.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ShiftsViewSet(ModelViewSet):
    queryset = Turnos.objects.all().order_by('TurnoID')
    serializer_class = ShiftsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    async def alist(self, request):
        horarios = await sync_to_async(list)(self.queryset)
        serializer = self.get_serializer(horarios, many=True)
        return response.Response(serializer.data)

    async def aretrieve(self, request, pk):
        horario = await sync_to_async(self.get_object)()  
        serializer = self.get_serializer(horario)
        return response.Response(serializer.data)

    async def acreate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horario = await sync_to_async(serializer.save)()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    async def aupdate(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(horario, data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return response.Response(serializer.data)

    async def adestroy(self, request, pk):
        horario = await sync_to_async(self.get_object)()
        await sync_to_async(horario.delete)()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

