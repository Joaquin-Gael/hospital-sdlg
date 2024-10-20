from rest_framework import serializers
from turnero.models import * 
from medicos.models import (Ubicaciones,Medicos,Departamentos,Especialidades,Horario_medicos)
from user.models import Usuarios

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def to_representation(self, instance):
        json_ = super().to_representation(instance)

        json_['contraseña'] = instance.get_contraseña

        return json_

class UbicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicaciones
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'
        
class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidades
        fields = '__all__'
        
class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicos
        fields = '__all__'

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario_medicos
        fields = '__all__'
        
class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citas
        fields = '__all__'

class ShiftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turnos
        fields = '__all__' 
        