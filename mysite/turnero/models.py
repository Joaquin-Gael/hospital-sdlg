from django.db import models
from user.models import Usuarios
from medicos.models import (Medicos, Horario_medicos, Departamentos, Servicios)
from django.core.exceptions import ValidationError
from asgiref.sync import sync_to_async
from django.utils import timezone
from datetime import timedelta


# Create your models here.

#servicioID = models.ForeignKey(Servicios, on_delete=models.CASCADE)

class Citas(models.Model):
    citaID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    medicoID = models.ForeignKey(Medicos, on_delete=models.CASCADE)
    horarioID = models.ForeignKey(Horario_medicos,on_delete=models.CASCADE)
    departamentoID = models.ForeignKey(Departamentos,on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=25)
    fecha = models.DateField(default=timezone.now)
    fecha_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Motivo {self.motivo} estado {self.estado} medico {self.medicoID}"

class Turnos(models.Model):
    TurnoID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    citaID = models.ForeignKey(Citas,on_delete=models.CASCADE)
    medicoID = models.ForeignKey(Medicos,on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=25)
    fecha_created = models.DateTimeField(auto_now=True)
    fecha = models.DateField(default=timezone.now)
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
                self.cita.fecha = timezone.now().date()

            elif status == 2:
                self.citaID.estado = status_list[status]
                self.citaID.save()
                self.cita.fecha = timezone.now().date()
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
            departamento = Departamentos.objects.get(departamentoID=medicoID.especialidadID.departamentoID.departamentoID)
            print(departamento)
            cita = Citas(
                medicoID=medicoID,
                horarioID=horarioID,
                motivo=motivo,
                estado=estado,
                departamentoID=departamento
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
            print(instancia)
            print(instancia.medicoID.especialidadID.especialidadID)

            return instancia

        except Exception as err:
            print('Error al crear el turno ',err)
    
    def __str__(self):
        return f"Turno de {self.userID} el día {self.fecha}"

    #@classmethod
    #def extra_data(cls,data:dict):
    #    try:
    #        horario_medico = Horario_medicos.objects.get(horarioID=data['horario'])
    #        medico = Medicos.objects.get(medicoID=data['medico'])
    #        print(medico.medicoID)
    #        print(medico.especialidadID.especialidadID)
    #
    #        return {'h':horario_medico,'m':medico}
    #   except Exception as err:
    #        print(f'Error: {err}')
    #        return None
    
    @classmethod
    def set_status(cls, status:int, id:int):
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
            instancia = cls.objects.get(TurnoID=id)
            instancia.estado = status_list[status]
            if status == 1:
                instancia.citaID.estado = status_list[status]
                instancia.citaID.save()
                instancia.cita.fecha = timezone.now().date()

            elif status == 2:
                instancia.citaID.estado = status_list[status]
                instancia.citaID.save()
                instancia.cita.fecha = timezone.now().date()
            instancia.save()
            return True
        except Exception as err:
            print(f'Error: {err}')
            return False

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
    
    def set_monto(self,monto:float):
        self.monto = monto
        self.save()
        return True
    
    def set_descripcion(self,descripcion:str):
        self.descripcion = descripcion
        self.save()
        return True
    
    def set_fecha(self,fecha:str):
        self.fecha = fecha
        self.save()
        return True
    
    def set_servicio(self,servicioID:int):
        self.servicioID = servicioID
        self.save()
        return True
    
    def set_caja(self,cajaID:int):
        self.cajaID = cajaID
        self.save()
        return True
    
    def set_estado(self,estado:str):
        self.estado = estado
        self.save()
        return True