from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Departamentos)
admin.site.register(models.Medicos)
admin.site.register(models.Horario_medicos)
admin.site.register(models.Ubicaciones)
admin.site.register(models.Especialidades)