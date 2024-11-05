from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
    'userID', 'dni', 'fecha_nacimiento', 'email', 'telefono', 'contraseña', 'is_active', 'date_joined', 'last_login',
    'last_logout', 'obraID')
    list_filter = ('is_active', 'date_joined', 'last_login', 'last_logout')
    search_fields = ('dni', 'nombre', 'apellido', 'email', 'telefono', 'obraID')
    ordering = ('-date_joined',)
