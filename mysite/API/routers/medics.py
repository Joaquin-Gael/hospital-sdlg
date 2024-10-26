from ninja import Router, ModelSchema, Schema, File, Form, Field
from ninja.files import UploadedFile
from channels.db import database_sync_to_async
from django.http import JsonResponse
from API.models import Medicos
from API.serializers import BaseSerializer
from typing import Optional
from datetime import date


# Create your views here.
class MedicosSchema(ModelSchema):
    imagen: Optional[UploadedFile] = File(...)
    class Meta:
        model=Medicos
        exclude=['groups', 'user_permissions', 'date_joined', 'last_login', 'last_logout']

class MedicosSchemaPut(Schema):
    password: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    dni: Optional[str]
    fecha_nacimiento: Optional[date]  # Manejo de fechas
    email: Optional[str]
    telefono: Optional[str]
    contraseña: Optional[str]  # Si 'contraseña' es diferente a 'password'
    imagen_url: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]

medic_router = Router()

@medic_router.get('/')
async def list_medics(request):
    """
        Retrieve a list of all medical professionals.

        This endpoint returns a paginated list of all medical professionals
        registered in the system. It includes a count of the total number of
        medical professionals and their serialized data.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the Django Ninja framework.

        Returns:
        - JsonResponse: A JSON response containing the total count of
          medical professionals and their serialized details.

        Example response:
        {
            "count": 10,
            "value": [
                {
                    "medicoID": 1,
                    "nombre": "Dr. Juan Pérez",
                    "especialidad": "Cardiología",
                    "contraseña": "hashed_password_value",
                    ...
                },
                {
                    "medicoID": 2,
                    "nombre": "Dra. Ana López",
                    "especialidad": "Pediatría",
                    "contraseña": "hashed_password_value",
                    ...
                },
                ...
            ]
        }
        """
    medics_count:int = await database_sync_to_async(Medicos.objects.count)()
    medics_list:list = await database_sync_to_async(list)(Medicos.objects.all().order_by('medicoID'))
    medics_serializer = BaseSerializer(
        model_class=Medicos,
        instance=medics_list,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = medics_serializer.serialize()
    return JsonResponse({'count': medics_count, 'value': serialized_data}, status=200)

@medic_router.get('/{medic_id}/')
async def get_medic(request, medic_id:int):
    """
        Retrieve the details of a specific medical professional.

        This endpoint fetches the information of a medical professional
        identified by their unique ID. The details are serialized before
        being returned in the response.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.
        - medic_id: int - The unique identifier of the medical professional
          whose details are to be retrieved.

        Returns:
        - JsonResponse: A JSON response containing the serialized details
          of the specified medical professional.

        Example response:
        {
            "medic": {
                "medicoID": 1,
                "nombre": "Dr. Juan Pérez",
                "especialidad": "Cardiología",
                "contraseña": "hashed_password_value",
                ...
            }
        }

        Raises:
        - 404: If the medical professional with the given ID does not
          exist, a 404 Not Found error is returned.
        """
    medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
    medic_serialized = BaseSerializer(
        model_class=Medicos,
        instance=medic,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_medic = medic_serialized.serialized()
    return JsonResponse({'medic':serialized_medic}, status=200)

@medic_router.post('/')
async def create_medic(request, payload: Form[MedicosSchema], imagen: UploadedFile = File(None)):
    """
        Create a new medical professional.

        This endpoint allows for the creation of a new medical professional
        entry. It accepts form data for the professional's details, including
        an optional image. The password is handled securely by hashing it
        before storage.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.
        - payload: Form[MedicosSchema] - A form containing the medical
          professional's details such as name, specialty, and password.
        - imagen: UploadedFile (optional) - An optional image file
          associated with the medical professional.

        Returns:
        - JsonResponse: A JSON response containing the serialized details
          of the newly created medical professional.

        Example response:
        {
            "medicoID": 1,
            "nombre": "Dr. Ana Martínez",
            "especialidad": "Pediatría",
            "contraseña": "hashed_password_value",
            ...
        }

        Raises:
        - 400: If the required fields are not provided in the payload.
        """
    new_medic = Medicos()
    data = payload.dict()
    del data['contraseña']
    del data['imagen']
    if imagen:
        new_medic.imagen.save(imagen.name, imagen)
    for field_name, value in data.items():
        if field_name == 'password':
            new_medic.set_password(value)
            new_medic.set_contraseña(value)
        else:
            setattr(new_medic, field_name, value)
    user_serializer = BaseSerializer(
        model_class=Medicos,
        instance=new_medic,
        deal_for_field_list={'contraseña': 'get_contraseña'}
    )
    serialized_data = user_serializer.serialize()
    #new_user.save()
    return serialized_data

@medic_router.put('/{medic_id}/imagen/', tags=['Media Medic'])
async def update_medic_image(request, medic_id:int, imagen: UploadedFile = File()):
    """
       Update the image of a medical professional.

       This endpoint allows for updating the image associated with a specific
       medical professional identified by their `medic_id`. If an image is
       provided, it replaces the existing image for the medical professional.

       Parameters:
       - request: The HTTP request object. Automatically provided by the
         Django Ninja framework.
       - medic_id: int - The unique identifier of the medical professional
         whose image is to be updated.
       - imagen: UploadedFile - The new image file to be uploaded.

       Returns:
       - JsonResponse: A JSON response containing the serialized details of
         the updated medical professional.

       Example response:
       {
           "medic": {
               "medicoID": 1,
               "nombre": "Dr. Ana Martínez",
               "especialidad": "Pediatría",
               "imagen": "new_image_url",
               ...
           }
       }

       Raises:
       - 400: If no image is provided in the request.
       - 404: If the specified medical professional does not exist.
       """
    if imagen:
        old_medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
        old_medic.imagen = imagen

        user_serializer = BaseSerializer(
            model_class=Medicos,
            instance=old_medic,
            deal_for_field_list={'contraseña': 'get_contraseña'}
        )
        serialized_data = user_serializer.serialize()

        return JsonResponse({'medic': serialized_data}, status=200)
    else:
        return JsonResponse({'detail':'Almenos un campo tiene que estar cambiado'}, status=400)

@medic_router.put('/{medic_id}/')
async def update_medic(request, medic_id:int, payload: Form[MedicosSchemaPut]):
    """
        Update the details of a medical professional.

        This endpoint allows for updating the information of a specific
        medical professional identified by their `medic_id`. It accepts
        various fields of the `Medicos` model, and updates them accordingly.

        Parameters:
        - request: The HTTP request object. Automatically provided by the
          Django Ninja framework.
        - medic_id: int - The unique identifier of the medical professional
          to be updated.
        - payload: Form[MedicosSchemaPut] - A form containing the fields
          to be updated for the medical professional.

        Returns:
        - JsonResponse: A JSON response containing the serialized details of
          the updated medical professional.

        Example response:
        {
            "medic": {
                "medicoID": 1,
                "nombre": "Dr. Juan Pérez",
                "especialidad": "Cardiología",
                "imagen": "current_image_url",
                ...
            }
        }

        Raises:
        - 400: If no fields are provided in the request to update.
        - 404: If the specified medical professional does not exist.
        """
    data = payload.dict()
    if data:
        old_medic = await database_sync_to_async(Medicos.objects.get)(medicoID=medic_id)
        for key, value in data:
            setattr(old_medic, key, value)

        user_serializer = BaseSerializer(
            model_class=Medicos,
            instance=old_medic,
            deal_for_field_list={'contraseña': 'get_contraseña'}
        )
        serialized_data = user_serializer.serialize()

        return JsonResponse({'medic': serialized_data}, status=200)
    else:
        return JsonResponse({'detail': 'Almenos un campo tiene que estar cambiado'}, status=400)