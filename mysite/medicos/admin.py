from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Departamentos)
admin.site.register(models.Horario_medicos)
admin.site.register(models.Ubicaciones)
admin.site.register(models.Especialidades)

#TODO: mejorar como definimos admin de los medicos

@admin.register(models.Medicos)
class MedicAdmin(admin.ModelAdmin):
    list_display = (
    'medicoID', 'dni', 'fecha_nacimiento', 'email', 'telefono', 'contraseña', 'is_active', 'date_joined', 'last_login',
    'last_logout', 'especialidadID')
    list_filter = ('is_active', 'date_joined', 'last_login', 'last_logout')
    search_fields = ('dni', 'nombre', 'apellido', 'email', 'telefono', 'especialidadID')
    ordering = ('-date_joined',)