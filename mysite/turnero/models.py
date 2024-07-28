from django.db import models
from user.models import Usuarios
from medicos.models import (Medicos, Horario_medicos, Departamentos)
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Citas(models.Model):
    citaID = models.AutoField(primary_key=True)
    medicoID = models.ForeignKey(Medicos, on_delete=models.CASCADE)
    horarioID = models.ForeignKey(Horario_medicos,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=25)

class Turnos(models.Model):
    TurnoID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    citaID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    medicoID = models.ForeignKey(Medicos,on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=25)
    fecha_created = models.DateTimeField(auto_now=True)
    fecha = models.DateField(default=timezone.now)

    def get_medico(self):
        return {
            'nombre':self.medicoID.nombre,
            'id':self.medicoID.id
        }
    
    def get_motivo(self):
        return self.motivo
    
    def get_estado(self):
        return self.estado
    
    def get_fecha(self):
        return self.fecha
    
    def get_fecha_created(self):
        return self.fecha_created

    @classmethod
    def eliminar_registros_antiguos(cls, dias=0):
        """
        Método de clase para eliminar registros creados en la fecha y hora actual o en los últimos días especificados.
        :param dias: Número de días antes de la fecha y hora actual para incluir en la eliminación.
        """
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual - timedelta(days=dias)
        registros_actuales = cls.objects.filter(fecha_created__date=fecha_actual.date(), fecha_created__time=fecha_actual.time())
        if dias > 0:
            registros_actuales = registros_actuales.filter(fecha_created__gte=fecha_limite)
        registros_actuales.delete()
    
    @classmethod
    def create_turnos(cls, medicoID, horarioID, motivo, userID, fecha, estado='pendiente'):
        try:
            instancia:cls = cls(
                medicoID=medicoID,
                horarioID=horarioID,
                motivo=motivo,
                userID=userID,
                estado=estado,
                fecha=fecha
            )
            instancia.save()

            return instancia

        except Exception as err:
            print('Error al crear el turno ',err)
    
    def __str__(self):
        return f"Turno de {self.pacienteID} el día {self.fecha}"