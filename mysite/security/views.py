from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .serializers import SecurityTokenSerializer, TokenBlacklistRedisSerializer
from user.models import Usuarios
from datetime import timedelta
from .models import SessionTokens, BlackListTokens
from urllib.parse import urlencode
from asgiref.sync import sync_to_async
from faker import Faker
import requests, uuid

faker = Faker()

# Create your views here.

class GoogleSingUp(APIView):
    permission_classes = [AllowAny]
    def post(self, request): # /oauth/login/google/
        try:
            url_google:str = 'https://accounts.google.com/o/oauth2/auth'
            params:dict = {
                'client_id':settings.GOOGLE_CLIENT_ID,
                'redirect_uri':settings.CALLBACK_URL,
                'response_type':'code',
                'scope':'openid email profile',
                'access_type':'offline',
                'prompt':'select_account',
            }
            return Response({'detail':'redirect...'}, status=302, headers={'Location':f'{url_google}?{urlencode(params)}'})
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__.__name__, e.args))
            return Response({'detail':'redurec...'}, status=302, headers={'Location':f'{reverse_lazy('Home')}'})

class OauthCallback(APIView):
    permission_classes = [AllowAny]
    async def post(self, request): # /oauth/callback/google
        try:
            code = request.GET.get('code')
            token_url = 'https://oauth2.googleapis.com/token'
            data:dict = {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': settings.CALLBACK_URL,
                'grant_type': 'authorization_code',
                'code': code,
            }
            response = await sync_to_async(request.post)(token_url, data=data)
            token_data = response.json()
            access_token = token_data.get('access_token')
            id_token = token_data.get('id_token')
            user_data = await sync_to_async(self.get_user_info)(access_token)
            user = await sync_to_async(self.handler_login_user)(user_data, request)
            if isinstance(user, Usuarios):
                messages.success(request,'Login Exitoso.\nRegrese al register para completar')
                return Response({'detail':'redirect...', 'token_id':f'{id_token}'}, status=302, headers={'Location': f'{reverse_lazy('Home')}'})
            messages.error(request,'No se a podido crear el usuario.\nIntentelo mas tarde o comuniquese con el servicio tecnico')
            return Response({'detail':'Error...','Usuario':'None'}, status=302, headers={'Location':f'{reverse_lazy('Home')}'})
        except Exception as e:
            print('Error: {}\nData: {}'.format(e.__class__.__name__, e.args))
            messages.error(request,f'Error...\nCpmunicarse con servicio tecnico\nCode: {e.__class__}')
            return Response({'detail':'Error...'}, status=302, headers={'Location':f'{reverse_lazy('Home')}'})

    def get_user_info(self, access_token):
        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_data = user_info_response.json()

        return user_data.json()

    def handler_login_user(self, user_data, request) -> Usuarios | None:
        email = user_data.get('email')
        nombre = user_data.get('given_name')
        apellido = user_data.get('family_name')
        img_url = user_data.get('picture')
        has_email_verificated = user_data.get('verified_email')

        user, created = Usuarios.objects.get_or_create(email=email)

        if created and has_email_verificated:
            user.username = user_data.get('name')
            user.nombre = nombre
            user.apellido = apellido
            user.imagen_url = img_url
            user.set_password(faker.password(length=16, special_chars=True, digits=True, upper_case=True))
            user.save()
            user.set_login(request)
            return user
        else:
            return None


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
                payload = UntypedToken(refresh_token)
                print(payload.payload)

                # Verifica si el token está en la blacklist
                if BlackListTokens.is_blacklisted(payload.payload):
                    print('Invalido')
                    return Response(
                        {'Error': 'Token is blacklisted'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Agrega el token a la blacklist
                listed = BlackListTokens.set_blacklisted(payload.payload)
                print('Listado') if listed else print('Error')
                
                # Genera un UUID para la sesión
                uuid_token = str(uuid.uuid4())
                response.data['token_uuid'] = uuid_token

                user = Usuarios.objects.get(userID=payload.payload.get('uui'))

                token = SecurityTokenSerializer.get_token(user)

                response.data['access'] = str(token.access_token)
                response.data['refresh'] = str(token)
                
                # Guarda el UUID y la fecha de expiración en la base de datos
                #SessionTokens.objects.create(
                #    tokenUUID=uuid_token,
                #    expires_at=timezone.now() + timedelta(seconds=payload.access_token['exp'] - timezone.now().timestamp()),
                #    userID=user
                #)

                return response
            except Exception as e:
                print('Error: {}\nData: {}'.format(e.__class__, e.args))
                return Response(
                    {'Error': 'Invalid token'},
                    status=status.HTTP_400_BAD_REQUEST
                )