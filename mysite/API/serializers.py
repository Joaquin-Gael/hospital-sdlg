from medicos.models import (Ubicaciones,Medicos,Departamentos,Especialidades,Horario_medicos)
from adrf.serializers import ModelSerializer
from user.models import Usuarios
from turnero.models import * 

class UserSerializer(ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def to_representation(self, instance):
        try:
            representation = super().to_representation()
            representation['contraseña'] = instance.get_contraseña
        except Exception as e:
            pass
        
class UbicationSerializer(ModelSerializer):
    class Meta:
        model = Ubicaciones
        fields = '__all__'
        
class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'
        
class SpecialtySerializer(ModelSerializer):
    class Meta:
        model = Especialidades
        fields = '__all__'
        
class DoctorsSerializer(ModelSerializer):
    class Meta:
        model = Medicos
        fields = '__all__'

class SchedulesSerializer(ModelSerializer):
    class Meta:
        model = Horario_medicos
        fields = '__all__'
        
class AppointmentsSerializer(ModelSerializer):
    class Meta:
        model = Citas
        fields = '__all__'

class ShiftsSerializer(ModelSerializer):
    class Meta:
        model = Turnos
        fields = '__all__' 
        