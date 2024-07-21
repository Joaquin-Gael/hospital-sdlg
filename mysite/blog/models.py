from django.db import models
from user.models import Usuarios

# Create your models here.
class Testimonios(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)