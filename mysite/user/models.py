from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import (login, logout, authenticate)
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Ubicaciones(models.Model):
    ubicacionID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

class Departamentos(models.Model):
    departamentoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    ubicacionID = models.ForeignKey(Ubicaciones,on_delete=models.CASCADE)

class Especialidades(models.Model):
    especialidadID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=255)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)


class Medicos(models.Model):
    medicoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.dni} {self.especialidadID.nombre}"

class Horario_medicos(models.Model):
    horarioID = models.AutoField(primary_key=True)
    medicoID = models.ForeignKey(Medicos,on_delete=models.CASCADE)
    dia = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.medicoID} {self.hora_inicio} {self.hora_fin}"

class Usuarios(AbstractUser):
    userID = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(blank=True,null=True,unique=True)
    telefono = models.CharField(blank=True,null=True, max_length=15)
    contraseña = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(null=True, blank=True)
    last_logout = models.DateField(null=True, blank=True)

    def set_login(self, request):
        self.last_login = timezone.now()
        self.save()
        login(request, self)

    def set_logout(self, request):
        self.last_logout = timezone.now()
        self.save()
        logout(request)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.dni}"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    @classmethod
    def authenticate(cls, request, dni=None, password=None):
        user = cls.objects.filter(dni=dni).first()
        if user.check_password(password):
            user.set_login(request)
            return user
        return None
    
    @classmethod
    def logout(cls, request) -> bool:
        user = request.user
        if user.is_authenticated:
            user.set_logout(request)
            return True
        return False