from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, logout
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw,ImageFont
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from cryptography.fernet import Fernet
import io
import random

# Create your models here.

class UsuarioBase(AbstractUser):
    dni = models.CharField(max_length=100, unique=True,null=True,blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True,null=True,unique=True)
    telefono = models.CharField(blank=True,null=True, max_length=15)
    contraseña = models.CharField(max_length=125, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(null=True, blank=True)
    last_logout = models.DateField(null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True

    def set_login(self, request) -> None:
        self.last_login = timezone.now()
        self.save()
        login(request, self)

    def set_logout(self, request) -> None:
        self.last_logout = timezone.now()
        self.save()
        logout(request)
    
    def __str__(self) -> str:
        #return '\n'.join(f"{k}: {v}" for k, v in vars(self).items() if not k.startswith('_'))
        return f'<{self.__class__.__name__}>({self.get_full_name})'
    
    def __repr__(self) -> str:
        attrs = '\n'.join(f"{k}={v!r}" for k, v in vars(self).items() if not k.startswith('_'))
        return f'<{self.__class__.__name__}({attrs})>'

    @property
    def get_full_name(self) -> str:
        return f"{self.nombre} {self.apellido}"

    @property
    def DNI(self):
        return self.dni

    @DNI.setter
    def set_dni(self, new_dni:str):
        self.dni = new_dni
        self.save()

    @classmethod
    def authenticate(cls, request, dni=None, password=None):
        user = cls.objects.filter(dni=dni).first()
        if user.check_password(password):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
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
    
    def update_data(self,
                    nombre = None,
                    apellido = None,
                    email = None,
                    contraseña = None,
                    img = None,
                    telefono = None,
                    img_url = None,
                    username = None) -> None:

        fields_to_update = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'imagen': img,
            'imagen_url': img_url,
            'username': username,
        }

        for field, value in fields_to_update.items():
            if value is not None and getattr(self, field) != value:
                setattr(self, field, value)

        if contraseña is not None and self.get_contraseña != contraseña:
            self.set_contraseña(contraseña)
            self.set_password(contraseña)

        self.save()
        
    def gen_default_profile_picture(self,initials: str, size=(32, 32)):
        try:
           colors = ['#242742','#51A3A3','#DAB081','#ABE166','#B80300','#6F2DBD']
           light_colors = ['#242742', '#BBDDDD', '#DFCC74', '#7ABB25', '#FF7370', '#B38BE4']
            
           img = Image.new('RGB', size, color=random.choice(colors))

           draw = ImageDraw.Draw(img)
           font = ImageFont.load_default()
   
           _,_,text_width, text_height = draw.textbbox((0,0), initials, font=font)
           position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
    
           draw.text(position, initials, fill=random.choice(light_colors), font=font)
    
   
           buffer = io.BytesIO()
           img.save(buffer, format='PNG')
           buffer.seek(0)
           
           return buffer
    
        except Exception as e:
            print(f"Error: {e.__class__}\nData: {e.args}")
            
    def set_dpp(self):
        try:
            initials = f"{self.nombre[0].upper()}{self.apellido[0].upper()}"
            image_buffer = self.gen_default_profile_picture(initials)
    
            file_name = f"profile_{self.nombre}_{self.apellido}.png"

            self.imagen.save(file_name, ContentFile(image_buffer.read()), save=True)
        except Exception as e:
            print(f"Error: {e.__class__}\nData: {e.args}")

    def set_contraseña(self, value) -> None:
        cipher = Fernet(settings.FERNET_KEY)
        self.contraseña:str = cipher.encrypt(value.encode('utf-8')).decode('utf-8')

    @property
    def get_contraseña(self) -> str:
        if self.contraseña:
            cipher = Fernet(settings.FERNET_KEY)
            contraseña: str = cipher.decrypt(self.contraseña.encode('utf-8')).decode('utf-8')
            return contraseña

class Usuarios(UsuarioBase):
    userID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, default='usuario_sin_nombre')
    apellido = models.CharField(max_length=100, default='usuario_sin_apellido')
    imagen = models.ImageField(upload_to='user/',default=f'user/profile_{nombre}_{apellido}.png',null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permissions',
        blank=True,
    )

    class Meta:
        permissions:list[tuple[str,str]] = [
            ('view_panel_user', 'Can view panel user')
        ]