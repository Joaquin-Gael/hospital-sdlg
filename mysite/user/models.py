from django.db import models
from django.contrib.auth.models import AbstractUser

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
    telefono = models.CharField(blank=True,null=True)
    contraseña = models.CharField(max_length=100)