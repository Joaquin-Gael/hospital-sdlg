from django.db import models
from datetime import timedelta
from django.utils import timezone
from user.models import Usuarios
from django.conf import settings

# Create your models here.

REDIS_DB = 'REDIS_DB'

class BlackListTokens(models.Model):
    tokenID = models.AutoField(primary_key=True)
    tokenJTID = models.CharField(max_length=55, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    DB = models.CharField(max_length=18, default=REDIS_DB)
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join(f'{k}: {v}' for k, v in vars(self).items() if not k.startswith('_'))

class SessionTokens(models.Model):
    sessionID = models.AutoField(primary_key=True)
    tokenUUID = models.CharField(max_length=55, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join(f'{k}: {v}' for k, v in vars(self).items() if not k.startswith('_'))