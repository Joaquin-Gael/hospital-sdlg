from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from user.models import Usuarios
from rest_framework import serializers
from rest_framework.response import Response

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