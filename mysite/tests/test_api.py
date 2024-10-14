from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse_lazy
from user.models import Usuarios
from API.serializers import UserSerializer
from faker import Faker
from datetime import timedelta
import random, string

faker = Faker()

class ApiUserViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url:str = reverse_lazy('usuarios-list')
        self.ids:list[int] = [id for id in range(100, 110)]
        self.dnis:list[str] = []

    @patch('user.models.Usuarios.objects.all')
    def test_get_users_list(self, mock_get_all):
        self.generate_dnis()
        mock_get_all.return_value = [
            Usuarios(
                userID=random.choice(self.ids),
                dni=random.choice(self.dnis),
                nombre=faker.name(),
                apellido=faker.last_name(),
                contraseña=faker.password(),
                fecha_nacimiento=faker.date_between(start_date=timezone.now()-timedelta(weeks=7_665), end_date=timezone.now()),
                email=faker.email(),
                telefono=faker.phone_number()
            ),
            Usuarios(
                userID=random.choice(self.ids),
                dni=random.choice(self.dnis),
                nombre=faker.name(),
                apellido=faker.last_name(),
                contraseña=faker.password(),
                fecha_nacimiento=faker.date_between(start_date=timezone.now() - timedelta(weeks=7_665),
                                                    end_date=timezone.now()),
                email=faker.email(),
                telefono=faker.phone_number()
            )
        ]

        response = self.client.get(self.url)

        mock_get_all.assert_called_once()

        expected_data = UserSerializer(mock_get_all.return_value, many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def generate_dnis(self):
        for i in range(10):
            self.dnis.append(''.join(random.choice(string.digits) for i in range(9)))