from django.db import models
from user.models import Usuarios
from medicos.models import (Medicos, Horario_medicos, Departamentos, Servicios)
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class BaseModelTurnos(models.Model):
    servicioID = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='%(class)s_user')
    medicoID = models.ForeignKey(Medicos, on_delete=models.CASCADE, related_name='%(class)s_medic')
    motivo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)
    fecha_created = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Citas(BaseModelTurnos):
    citaID = models.AutoField(primary_key=True)
    horarioID = models.ForeignKey(Horario_medicos,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)

    def __str__(self):
        return f"Motivo {self.motivo} estado {self.estado} medico {self.medicoID}"

class Turnos(BaseModelTurnos):
    TurnoID = models.AutoField(primary_key=True)
    citaID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    fecha_limt = models.DateField(default=timezone.now)
    
    def get_turno_data(self):
        return {
            'TurnoID': self.TurnoID,
            'Usuario': [self.userID.dni, self.userID.nombre, self.userID.apellido],
            'Médico': self.citaID.medicoID,
            'Motivo': self.estado,
            'Estado': self.estado,
            'Fecha': self.fecha,
            'Fecha de Creación': self.fecha_created,
            'Fecha Límite': self.fecha_limt
        }
    
    def set_fecha(self, fecha:str):
        """
        Método de clase para cambiar la fecha de un turno.

        Args:
            fecha (str): _description_

        Returns:
            _type_: _description_
        """
        self.citaID.fecha = fecha
        self.citaID.save()
        return True
    
    def set_rango_fecha(self, fecha_limt:str, fecha:str):
        """
        Método de clase para cambiar el rango de fecha de un turno.

        Args:
            fecha_limt (str): _description_
            fecha (str): _description_

        Returns:
            _type_: _description_
        """
        self.fecha_limt = fecha_limt
        self.fecha = fecha
        self.save()
        return True
    
    def set_status(self, status:int):
        """
        Método de clase para cambiar el estado de un turno.

        Args:
            status (int): _description_
            id (int): _description_

        Returns:
            _type_: _description_
        """
        status_list = [
            'pendiente',
            'atendido',
            'cancelado'
        ]
        try:
            self.estado = status_list[status]
            if status == 1:
                self.citaID.estado = status_list[status]
                self.citaID.save()
                self.citaID.fecha = timezone.now().date()

            elif status == 2:
                self.citaID.estado = status_list[status]
                self.citaID.save()
                self.citaID.fecha = timezone.now().date()
            self.save()
            return True
        except Exception as err:
            print(f'Error: {err}')
            return False

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
            departamentoID = medicoID.especialidadID.departamentoID.departamentoID
            cita = Citas(
                medicoID=medicoID,
                horarioID=horarioID,
                motivo=motivo,
                estado=estado,
                departamentoID_id=departamentoID
            )
            cita.save()
            instancia:cls = cls(
                medicoID=cita.medicoID,
                motivo=motivo,
                userID=userID,
                estado=estado,
                fecha=fecha,
                citaID=cita
            )
            instancia.save()

            return instancia


        except cls.ObjectDoesNotExist as e:
            print('Error: objeto no encontrado', e)

        except Exception as err:
            print('Error al crear el turno', err)
    
    def __str__(self):
        return f"Turno de {self.userID} el día {self.fecha}"

class CajaTurnero(models.Model):
    cajaID = models.AutoField(primary_key=True)
    citaID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    fecha_created = models.DateTimeField(auto_now=True)
    ingreso = models.FloatField(default=0)
    egreso = models.FloatField(default=0)
    saldo = models.FloatField(default=0)
    estado = models.CharField(max_length=25)
    fecha = models.DateField(default=timezone.now)
    horario_transaccion = models.TimeField(default=timezone.now)
 
    def clean(self):
        if self.egreso > self.saldo + self.ingreso:
            raise ValidationError("Saldo insuficiente.")
    
    def save(self, *args, **kwargs):
        self.saldo = self.ingreso - self.egreso

        self.clean()  
        super().save(*args, **kwargs)
    
    @classmethod
    def set_registro(cls, *args, **kwargs):
        try:
            cita = kwargs.get('citaID')
            instance = cls(
                citaID=cita,
                ingreso=kwargs.get('ingreso'),
                egreso=kwargs.get('egreso'),
                estado=kwargs.get('estado'),
            )
            instance.save()
            
        except cls.DoesNotExist as e:
            print('{}'.format(e.args))
        
        except Exception as e:
            print('{}'.format(e.args))
        
    
    def __str__(self):
        return f"Caja de {self.turnoID}"

class DetallesCaja(models.Model):
    detalleID = models.AutoField(primary_key=True)
    cajaID = models.ForeignKey(CajaTurnero,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto = models.FloatField(default=0)
    fecha_created = models.DateTimeField(auto_now=True)
    servicioID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    horario_transaccion = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"Detalle de {self.cajaID}"

    @classmethod
    def set_registro(cls, #pendiente de refactor
                     fecha = None,
                     monto = None,
                     descripcion = None,
                     caja = None):
        pass