from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from datetime import timedelta
from .redis_blacklist import TokenDBORM
from .models import SessionTokens
import uuid

# Create your views here.

class SecurityToken(TokenObtainPairView):
    """
    Vista para obtener el par de tokens (access y refresh).
    Utiliza SecurityTokenSerializer para personalizar los datos del token.
    """
    def post(self, request, *args, **kwargs):
        """Post
        Aunque en el swager te diga que el obligatorio pasar el username no lo es en la API

        Args:
            request (Request): request

        Raises:
            ValidationError: password
            ValidationError: dni
            ValidationError: email

        Returns:
            str: tokens
        """
        try:
            # Obtén los datos del request
            dni = request.data.get('dni', None)
            email = request.data.get('email', None)
            password = request.data.get('password', None)

            # Valida que se haya enviado un email o un dni
            if not dni and not email:
                raise ValidationError({"detail": "DNI or Email is required."})

            # Valida que se haya enviado la contraseña
            if not password:
                raise ValidationError({"detail": "Password is required."})

            # Buscar el usuario por DNI o Email
            if dni:
                user = Usuarios.objects.get(dni=dni)
            else:
                user = Usuarios.objects.get(email=email)

            # Validar la contraseña
            if not user.check_password(password):
                raise ValidationError({"detail": "Invalid password."})

            # Si el usuario y contraseña son correctos, generar el token
            token = SecurityTokenSerializer.get_token(user)

            # Devuelve el token en la respuesta
            return Response({
                'access_token': str(token.access_token),
                'refresh_token': str(token)
            }, status=status.HTTP_200_OK)

        except Usuarios.DoesNotExist:
            return Response({
                "error": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            # Errores de validación específicos
            return Response({
                "error": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Captura correctamente la excepción y muestra el error
            print('Error: {}\nData: {}'.format(e.__class__.__name__, str(e)))
            return Response({
                'error': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SecurityTokenRefresh(TokenRefreshView):
    """
    Vista para refrescar el token.
    Agrega un UUID al token de refresh y lo almacena en la base de datos.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh', None)
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                token_db = TokenDBORM(refresh)
                print(refresh)
                print(token_db)
                
                # Verifica si el token está en la blacklist
                if token_db.is_blacklisted():
                    return Response(
                        {'Error': 'Token is blacklisted'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Agrega el token a la blacklist
                TokenDBORM.set_blacklist(refresh)
                print('Listado')
                
                # Genera un UUID para la sesión
                uuid_token = str(uuid.uuid4())
                response.data['token_uuid'] = uuid_token
                
                # Guarda el UUID y la fecha de expiración en la base de datos
                SessionTokens.objects.create(
                    tokenUUID=uuid_token,
                    expires_at=timezone.now() + timedelta(seconds=refresh.access_token['exp'] - timezone.now().timestamp())
                )
                
            except Exception as e:
                print('Error: {}\nData: {}'.format(Exception.__class__, Exception.args))
                return Response(
                    {'Error': 'Invalid token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return response