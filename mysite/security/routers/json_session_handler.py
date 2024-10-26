from ninja import Router, Form
from ninja.security import django_auth
from django.conf import settings
from django.http import JsonResponse
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta
from cryptography.fernet import Fernet
from security.models import Usuarios, Medicos
from API.utils import Status
from faker import Faker
import jwt, uuid, random, json

JWT_router = Router()
faker = Faker()
encrypter = Fernet(settings.FERNET_KEY)

@JWT_router.post('/user/login/')
async def user_login_handler(request, dni:Form[int], password:Form[str]):
    """
    dni: int 8 characters
    password: str 10>X characters
    """
    try:
        user = await database_sync_to_async(Usuarios.authenticate)(request,dni, password)
        if user:
            payload = {
                'name': user.nombre,
                'dni': user.DNI,
                'uid': str(uuid.uuid4()),
                'id': user.userID,
                'date_created': str(timezone.now()),
                'date_exp': str(timezone.now() + timedelta(days=1)),
                'type':'access'
            }
            payload = json.dumps(payload)
            payload = encrypter.encrypt(payload.encode('utf-8')).decode('utf-8')
            json_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_HASH)
            # TODO: Encriptar el contenido del JWT antes de enviarlo
            return JsonResponse({'access':json_token}, status=Status.HTTP_200_OK.value)
        else:
            raise Exception(detail='user not found')

    except Exception as e:
        return JsonResponse({'detail':f'{e.__class__}'}, status=Status.HTTP_400_BAD_REQUEST.value)


@JWT_router.post('/user/login/2/', tags=['Json Web Token Test'])
async def user_login_handler_2(request):
    """
    dni: int 8 characters
    password: str 10>X characters
    """
    try:
        user = True
        if user:
            payload = {
                'name': faker.user_name(),
                'dni': 12345678,
                'uid': faker.uuid4(),
                'id': random.randint(12,100),
                'date_created': str(timezone.now()),
                'date_exp': str(timezone.now() + timedelta(days=1)),
                'type': 'access'
            }
            payload = json.dumps(payload)
            payload = encrypter.encrypt(payload.encode('utf-8')).decode('utf-8')
            json_token = jwt.encode({'payload':payload}, settings.SECRET_KEY, algorithm=settings.JWT_HASH)
            # TODO: Encriptar el contenido del JWT antes de enviarlo
            return JsonResponse({'access': json_token}, status=Status.HTTP_200_OK.value)
        else:
            raise Exception(detail='user not found')

    except Exception as e:
        print(e.args)
        return JsonResponse({'detail':f'{e.__class__}'}, status=Status.HTTP_400_BAD_REQUEST.value)

@JWT_router.post('/user/')
async def load_payload(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_HASH])
        payload['payload'] = encrypter.decrypt(payload['payload'].encode('utf-8')).decode('utf-8')
        payload['payload'] = json.loads(payload['payload'])
        return JsonResponse(payload, status=Status.HTTP_200_OK.value)
    except Exception as e:
        print(e.args)
        return JsonResponse({'detail':f'{e.__class__}'}, status=Status.HTTP_400_BAD_REQUEST.value)