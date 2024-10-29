from ninja import Router, ModelSchema, File, Form
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Usuarios,Turnos
import os


# Create your views here.
class UsuarioSchema(ModelSchema):
    class Meta:
        model=Usuarios
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout']


class UsuarioSchemaPut(ModelSchema):
    class Meta:
        model=Usuarios
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout', 'imagen']
        fields_optional='__all__'

user_router = Router()

@user_router.get('/')
async def list_users(request):
    """
        Retrieve a list of users from the database.

        This endpoint fetches all users, counts them, and returns their
        details in a serialized format. The users are ordered by their
        user ID. The password field is excluded from serialization for
        security reasons.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.

        Returns:
        - JsonResponse: A JSON response containing:
            - `count` (int): The total number of users in the database.
            - `value` (list): A list of serialized user data.

        Example response:
        {
            "count": 10,
            "value": [
                {
                    "userID": 1,
                    "nombre": "John Doe",
                    "email": "john.doe@example.com",
                    ...
                },
                ...
            ]
        }
        """
    users_count:int = await database_sync_to_async(Usuarios.objects.count)()
    users_list:list = await database_sync_to_async(list)(Usuarios.objects.all().order_by('userID'))
    serialized_data =[]
    for object in users_list:
        serialized_data.append(UsuarioSchema.from_orm(object).dict())
    return JsonResponse({'count': users_count, 'value': serialized_data}, status=200)

@user_router.get('/{user_id}/')
async def get_user(request, user_id:int):
    """
        Retrieve a specific user by their user ID.

        This endpoint fetches the user data associated with the provided
        user ID and returns the user's details in a serialized format.
        The password field is excluded from serialization for security
        reasons.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - user_id (int): The unique identifier of the user to retrieve.

        Returns:
        - JsonResponse: A JSON response containing:
            - `user` (dict): A serialized representation of the user data.

        Raises:
        - 404 Not Found: If the user with the specified ID does not exist.

        Example response:
        {
            "user": {
                "userID": 1,
                "nombre": "John Doe",
                "email": "john.doe@example.com",
                ...
            }
        }
        """
    user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
    serialized_user = UsuarioSchema.from_orm(user).dict()
    is_authenticated = await database_sync_to_async(lambda :request.user.is_authenticated)()
    user_request = await database_sync_to_async(lambda :request.user.userID)()
    if is_authenticated and user_request == user.userID:
        serialized_user['contraseña'] = user.get_contraseña
    return JsonResponse({"user": serialized_user}, status=200)

@user_router.post('/')
async def create_user(request, payload: Form[UsuarioSchema], imagen: UploadedFile = File(None)):
    """
        Create a new user in the system.

        This endpoint allows the creation of a new user by accepting a payload
        that includes the user's details. An optional image can also be uploaded
        for the user profile. The password is securely hashed before being stored.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the Django Ninja framework.
        - payload (Form[UsuarioSchema]): A schema containing the user data.
          This includes fields like 'nombre', 'email', 'password', etc.
        - imagen (UploadedFile): An optional file upload for the user's image.

        Returns:
        - dict: A serialized representation of the created user data.

        Example request:
        ```
        POST /users/
        Content-Type: application/x-www-form-urlencoded
        {
            "nombre": "John Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "imagen": <uploaded_image>
        }
        ```

        Example response:
        {
            "userID": 1,
            "nombre": "John Doe",
            "email": "john.doe@example.com",
            "imagen": "profile_image_path.jpg",
            ...
        }
    """
    new_user = Usuarios()
    data = payload.dict()
    del data['contraseña']
    del data['imagen']
    if imagen:
        new_user.imagen.save(imagen.name, imagen)
    for field_name, value in data.items():
        if field_name == 'password':
            new_user.set_password(value)
            new_user.set_contraseña(value)
        else:
            setattr(new_user, field_name, value)
    serialized_data = UsuarioSchema.from_orm(new_user).dict()
    await database_sync_to_async(new_user.save)()
    return JsonResponse({'user':serialized_data}, status=200)

@user_router.put('/{user_id}/imagen/', tags=['Media User'])
async def update_user_image(request, user_id:int, imagen: UploadedFile = File()):
    """
        Update the profile image of a specific user.

        This endpoint allows for updating the user's profile image
        associated with the provided user ID. If an image is provided,
        it will replace the existing image for that user. The password
        field is excluded from serialization for security reasons.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - user_id (int): The unique identifier of the user whose image
          is to be updated.
        - imagen (UploadedFile): The new image file to be uploaded. This
          is optional and should be provided as part of the request.

        Returns:
        - JsonResponse: A JSON response containing:
            - `user` (dict): A serialized representation of the updated user data.

        Raises:
        - 400 Bad Request: If no image is provided.

        Example request:
        ```
        PUT /users/1/imagen/
        Content-Type: multipart/form-data
        ```

        Example response:
        {
            "user": {
                "userID": 1,
                "nombre": "John Doe",
                "email": "john.doe@example.com",
                "imagen": "new_image_path.jpg",
                ...
            }
        }
        """
    if imagen:
        old_user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
        old_user.imagen = imagen
        serialized_data = UsuarioSchema.from_orm(old_user).dict()
        return JsonResponse({'user':serialized_data},status=200)
    else:
        return JsonResponse({'detail':'Almenos un campo tiene que estar cambiado'}, status=400)

@user_router.post('/{user_id}/imagen/', tags=['Media User'])
async def create_user_image(request, user_id: int):
    try:
        old_user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
        is_authenticated = await database_sync_to_async(lambda: request.user.is_authenticated)()
        user_request = await database_sync_to_async(lambda: request.user.userID)()
        if not is_authenticated and user_request == old_user.userID:
            return JsonResponse({'detail':'Not Authenticated'}, status=403)
        if not os.path.exists(old_user.imagen.path):
            await database_sync_to_async(old_user.set_dpp)()
            return JsonResponse({'detail':'Success'}, status=200)
        return JsonResponse({'detail':'User already has image'}, status=400)
    except Exception as e:
        return JsonResponse({'detail':f'{e}'}, status=500)

@user_router.put('/{user_id}/')
async def update_user(request, user_id:int, payload: UsuarioSchemaPut):
    """
        Update the details of a specific user.

        This endpoint allows for updating the information of a user
        identified by the provided user ID. The payload can include
        various fields such as the user's name, email, and password.
        If a password is provided, it will be securely set using the
        appropriate method.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.
        - user_id (int): The unique identifier of the user to be updated.
        - payload (UsuarioSchemaPut): A schema containing the data to update
          the user. This may include fields like 'nombre', 'email',
          'contraseña', and 'password'.

        Returns:
        - JsonResponse: A JSON response containing:
            - `user` (dict): A serialized representation of the updated user data.

        Raises:
        - 400 Bad Request: If no valid data is provided to update.

        Example request:
        ```
        PUT /users/1/
        Content-Type: application/json
        {
            "nombre": "Jane Doe",
            "email": "jane.doe@example.com",
            "contraseña": "newpassword123"
        }
        ```

        Example response:
        {
            "user": {
                "userID": 1,
                "nombre": "Jane Doe",
                "email": "jane.doe@example.com",
                "imagen": "existing_image_path.jpg",
                ...
            }
        }
        """
    data = {key: value for key, value in payload.dict(exclude_none=True).items() if value != 'string' and value == ""}
    if data:
        old_user = await database_sync_to_async(Usuarios.objects.get)(userID=user_id)
        for key, value in data.items():
            if key == 'contraseña':
                await database_sync_to_async(old_user.set_contraseña)(value)
            elif key == 'password':
                await database_sync_to_async(old_user.set_password)(value)
            else:
                setattr(old_user, key, value)

        await database_sync_to_async(old_user.save)()
        serialized_data = UsuarioSchema.from_orm(old_user).dict()

        return JsonResponse({'user':serialized_data},status=200)
    else:
        return JsonResponse({'detail':'Almenos un campo tiene que estar cambiado'}, status=400)
    
@user_router.get('/{user_id}/schedules/', tags=['Schedules Users'])
async def get_by_user(request, user_id: int):
    try:
        schedule_list = await database_sync_to_async(list)(Turnos.objects.filter(userID=user_id))
        serialized_data = []
        for schedule in schedule_list:
            data = {
                'id': schedule.TurnoID,
                'medico': {
                    'id': schedule.citaID.medicoID.medicoID,
                    'nombre': schedule.citaID.medicoID.nombre
                },
                'horario': {
                    'id': schedule.citaID.horarioID.horarioID,
                    'hora': str(schedule.citaID.horarioID.hora)
                },
                'motivo': schedule.motivo,
                'estado': schedule.estado
            }
            serialized_data.append(data)
        return JsonResponse({'Turnos':serialized_data}, status=200)
    except Exception as err:
        return JsonResponse({'err': str(err.__class__)}, status=404)