from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer as BaseTokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import BlackListTokens

class SecurityTokenSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False)
    dni = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        """
        Personaliza el token con información adicional del usuario.
        """
        token = super().get_token(user)
        token['uui'] = user.userID
        token['ulli'] = user.last_login.isoformat() if user.last_login else None
        token['ullo'] = user.last_logout.isoformat() if user.last_logout else None
        return token

class TokenBlacklistRedisSerializer(BaseTokenBlacklistSerializer):
    def validate(self, attrs):
        print(attrs)
        refresh_token = attrs['refresh']
        token = RefreshToken(refresh_token)
        token_db = BlackListTokens().set_blacklisted(token)
        return attrs