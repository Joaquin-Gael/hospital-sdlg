from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Citas)
class CitasAdmin(admin.ModelAdmin):
    list_display = ('citaID', 'userID', 'medicoID', 'horarioID', 'departamentoID', 'motivo', 'estado', 'fecha', 'fecha_created')
    search_fields = ('motivo', 'estado', 'userID__nombre', 'medicoID__nombre')
    list_filter = ('estado', 'fecha', 'medicoID')
    ordering = ('-fecha_created',)

@admin.register(models.Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('TurnoID', 'userID', 'citaID', 'medicoID', 'motivo', 'estado', 'fecha', 'fecha_created', 'fecha_limt')
    search_fields = ('motivo', 'estado', 'userID__nombre', 'medicoID__nombre')
    list_filter = ('estado', 'fecha', 'medicoID')
    ordering = ('-fecha_created',)

@admin.register(models.CajaTurnero)
class CajaTurneroAdmin(admin.ModelAdmin):
    list_display = ('cajaID', 'citaID', 'ingreso', 'egreso', 'saldo', 'estado', 'fecha', 'horario_transaccion', 'fecha_created')
    search_fields = ('estado', 'citaID__motivo')
    list_filter = ('estado', 'fecha')
    ordering = ('-fecha_created',)
    readonly_fields = ('saldo',)

@admin.register(models.DetallesCaja)
class DetallesCajaAdmin(admin.ModelAdmin):
    list_display = ('detalleID', 'cajaID', 'descripcion', 'monto', 'fecha_created', 'servicioID', 'fecha', 'horario_transaccion')
    search_fields = ('descripcion', 'cajaID__citaID__motivo')
    list_filter = ('fecha', 'cajaID')
    ordering = ('-fecha_created',)