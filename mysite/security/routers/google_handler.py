from ninja import Router, Form
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from security.models import Usuarios
from asgiref.sync import sync_to_async
from django.contrib.auth import login
from django.urls import reverse_lazy
from urllib.parse import urlencode
from faker import Faker
import requests

google_router = Router(
    tags=['Security']
)

faker = Faker()

def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_data = user_info_response.json()

    return user_data.json()


def handler_login_user(request, user_data) -> Usuarios | None:
    email = user_data.get('email')
    username = user_data.get('name')
    password = faker.password(length=12, special_chars=True, upper_case=True, digits=True)
    name = user_data.get('give_name')
    last_name = user_data.get('last_name')
    image_url = user_data.get('picture')
    has_email_verificated = user_data.get('verified_email')

    user, created = Usuarios.objects.get_or_create(email=email)
    if created and has_email_verificated:
        user.update_data(
            nombre=name,
            apellido=last_name,
            email=user.email,
            contraseña=password,
            img_url=image_url,
            username=username
        )
        user.set_login(request)
        return user
    elif user:
        user.set_login(request)
        return user
    else:
        return None


@google_router.post('/oauth/login/', url_name='google_login')
async def google_login(request):
    """
        Initiate the Google OAuth login process.

        This endpoint redirects the user to the Google OAuth authorization
        page where they can log in and grant access to their account.
        The request includes the necessary parameters to initiate the OAuth
        flow.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.

        Returns:
        - HttpResponseRedirect: Redirects the user to the Google OAuth
          authorization URL.

        Raises:
        - Exception: If an error occurs while trying to initiate the login.

        Example response:
        Redirects to:
        https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_CALLBACK_URL&response_type=code&scope=openid email profile&access_type=offline&prompt=select_account
        """
    try:
        base_url = "https://accounts.google.com/o/oauth2/auth"
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': settings.CALLBACK_URL,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'select_account'
        }

        return HttpResponseRedirect('{}?{}'.format(base_url, urlencode(params)), status=302)

    except Exception as e:
        print('Error: {}\nData: {}'.format(e.__class__.__name__, e.args))


@google_router.post('/oauth/callback/')
async def oauth_callback(request):
    """
        Handle the Google OAuth callback.

        This endpoint is called by Google after the user has authorized
        access. It receives the authorization code, exchanges it for access
        and ID tokens, retrieves user information, and logs the user in.

        Parameters:
        - request: The HTTP request object. This is automatically provided
          by the FastAPI framework.

        Returns:
        - HttpResponseRedirect: Redirects the user to the index page after
          successful login.

        Raises:
        - Exception: If an error occurs during the token exchange or user
          information retrieval.

        Example response:
        Redirects to:
        /index
        """
    try:
        code = request.GET.get('code')
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.CALLBACK_URL,
            "grant_type": "authorization_code",
            "code": code,
        }
        response = await sync_to_async(requests.post)(token_url, data=data)
        token_data = response.json()

        access_token = token_data.get("access_token")
        id_token = token_data.get("id_token")

        user_data = await sync_to_async(get_user_info)(access_token)
        user = await sync_to_async(handler_login_user)(request, user_data)

        return HttpResponseRedirect(reverse_lazy('Index'))
    except Exception as e:
        print('Error: {}\nData: {}'.format(e.__class__.__name__, e.args))