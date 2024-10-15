from django.db import models

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

