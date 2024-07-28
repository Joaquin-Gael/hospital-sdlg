from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import (login, logout, authenticate)
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import os

# Create your models here.

class Usuarios(AbstractUser):
    userID = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True,null=True,unique=True)
    telefono = models.CharField(blank=True,null=True, max_length=15)
    contraseña = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(null=True, blank=True)
    last_logout = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='user/',null=True, blank=True)

    def set_login(self, request):
        self.last_login = timezone.now()
        self.save()
        login(request, self)

    def set_logout(self, request):
        self.last_logout = timezone.now()
        self.save()
        logout(request)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.dni}"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    @classmethod
    def authenticate(cls, request, dni=None, password=None):
        user = cls.objects.filter(dni=dni).first()
        if user.check_password(password):
            user.set_login(request)
            return user
        return None
    
    @classmethod
    def logout(cls, request) -> bool:
        user = request.user
        if user.is_authenticated:
            user.set_logout(request)
            return True
        return False
    
    def get_turnos(self):
        try:
            from turnero.models import Turnos
            return Turnos.objects.filter(userID=self.id)
        except:
            return None
    
    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        else:
            return os.path.join(settings.MEDIA_URL, 'imagenes/default_image.jpg')
    
    def update_data(self,nombre = None,apellido = None,email = None,contraseña = None,img = None):
        self.nombre = nombre if self.nombre != nombre and nombre is not None else self.nombre
        self.apellido = apellido if self.apellido != apellido and apellido is not None else self.apellido
        self.email = email if self.email != email and email is not None else self.email
        self.set_password(contraseña if self.contraseña != contraseña and contraseña is not None else self.contraseña)
        self.imagen = img if self.imagen != img and img is not None else self.imagen

        self.save()

    def __str__(self) -> str:
        return super().__str__()