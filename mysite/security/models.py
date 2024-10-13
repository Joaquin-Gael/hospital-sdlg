from django.db import models
from datetime import timedelta
from django.utils import timezone
from user.models import Usuarios
from django.conf import settings
import uuid

# Create your models here.

class BlackListTokens(models.Model):
    tokenID = models.AutoField(primary_key=True)
    tokenJTID = models.CharField(max_length=55, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join(f'{k}: {v}' for k, v in vars(self).items() if not k.startswith('_'))

    @classmethod
    def set_blacklisted(cls, token):
        try:
            JTID:str = token['jti']
            EXP:str = token['exp'] - token['orig_iat']
            user = Usuarios.objects.get(
                userID=token['user_id']
            )
            cls(
                tokenJTID = JTID,
                expires_at = timezone.now() + timedelta(seconds=EXP),
                userID = user
            )
            return True
        except Usuarios.DoesNotExist as e:
            print(f'User does not exist: {e.__class__}\nData: {e.args}')
            return False
        except Exception as e:
            print(f'Error: {e.__class__}\nData: {e.args}')
            return False

    @classmethod
    def is_blacklisted(cls, token) -> bool:
        JTID:str = token['jti']
        token = cls.objects.filter(tokenID=JTID).exists()
        return token


class SessionTokens(models.Model):
    sessionID = models.AutoField(primary_key=True)
    tokenUUID = models.CharField(max_length=55, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    userID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join(f'{k}: {v}' for k, v in vars(self).items() if not k.startswith('_'))