from django.db import models
from user.models import UsuarioBase
from django.utils import timezone
from django.contrib.auth.models import Group, Permission

# Create your models here.

class Ubicaciones(models.Model):
    ubicacionID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre}"
    
    @classmethod
    def get_ubicaciones(cls):
        return cls.objects.all()

class Departamentos(models.Model):
    departamentoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    ubicacionID = models.ForeignKey(Ubicaciones,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"
    
    @classmethod
    def get_departamentos(cls):
        return cls.objects.all()

class Especialidades(models.Model):
    especialidadID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=255)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"
    
    @classmethod
    def get_especialidades(cls):
        return cls.objects.all()

class Servicios(models.Model):
    servicioID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    precio = models.FloatField()
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    
class Medicos(UsuarioBase):
    medicoID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, default='medico_sin_nombre')
    apellido = models.CharField(max_length=100, default='medico_sin_apellido')
    imagen = models.ImageField(upload_to='medic/',default=f'medic/profile_{nombre}_{apellido}.png',null=True, blank=True)
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)

    groups = models.ManyToManyField(
        Group,
        related_name='medicos_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='medicos_permissions',
        blank=True,
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.dni} {self.especialidadID.nombre}"
    
    @classmethod
    def get_medicos(cls):
        return cls.objects.all()

class Horario_medicos(models.Model):
    horarioID = models.AutoField(primary_key=True)
    medicoID = models.ForeignKey(Medicos,on_delete=models.CASCADE)
    dia = models.CharField(max_length=100)
    hora = models.TimeField()
    especialidadID = models.ForeignKey(Especialidades,on_delete=models.CASCADE)
    servicioID = models.ForeignKey(Servicios,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.medicoID} {self.hora}"
    
    @classmethod
    def get_horarios(cls):
        return cls.objects.all()

