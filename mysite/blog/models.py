from django.db import models
from user.models import Usuarios
from tinymce.models import HTMLField

# Create your models here.
class News(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    content = HTMLField()

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-created_at']

    def __str__(self):
        return self.title