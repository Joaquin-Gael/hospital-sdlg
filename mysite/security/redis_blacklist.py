import redis
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer as BaseTokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import BlackListTokens
from user.models import Usuarios
from datetime import timedelta
from django.utils import timezone

redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

class TokenDBORM:
    def __init__(self, token: dict):
        self.token = token
    
    @classmethod
    def set_blacklist(cls, token):
        try:
            JTID: str = token['jti']
            EXP = token['exp'] - token['orig_iat']
            
            # Obtener el usuario basado en el ID del token
            USERID: Usuarios = Usuarios.objects.get(
                userID=token['user_id']
            )
            
            # Añadir el token a la blacklist en Redis
            redis_client.set(
                name=JTID,
                value='blacklisted',
                ex=EXP
            )
            
            # Crear un registro en la base de datos
            BlackListTokens.objects.create(
                tokenJTID=JTID,
                expires_at=timezone.now() + timedelta(seconds=EXP),
                userID=USERID
            )
            return True
        except redis.RedisError as e:
            print(f'Redis error: {e.__class__}\nData: {e.args}')
            return False
        except Usuarios.DoesNotExist as e:
            print(f'User does not exist: {e.__class__}\nData: {e.args}')
            return False
        except Exception as e:
            print(f'Error: {e.__class__}\nData: {e.args}')
            return False
    
    def is_blacklisted(self):
        JTID = self.token['jti']
        print(JTID)
        print(redis_client.get(JTID))
        return redis_client.get(JTID) == 'blacklisted'


class TokenBlacklistRedisSerializer(BaseTokenBlacklistSerializer):
    def validate(self, attrs):
        print(attrs)
        refresh_token = attrs['refresh']
        token = RefreshToken(refresh_token)
        token_db = TokenDBORM(token)
        token_db.set_blacklist(token)
        return attrs