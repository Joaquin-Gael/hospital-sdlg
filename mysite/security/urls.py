from django.urls import path, re_path
from django.views.generic.base import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Security API",
        default_version='v1.0.5',
        description="Descripción: SubAPI Para El Servicio De Seguridad\nAunque en el swager te diga que el obligatorio pasar el username no lo es en la API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=settings.EMAIL_HOST_USER),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        '',
        RedirectView.as_view(
            url='/API/security/swagger/',
            permanent=False
        )
    ),
    path(
        'token/', 
        SecurityToken.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/', 
        SecurityTokenRefresh.as_view(), 
        name='token_refresh'
    ),
    path(
        'oauth/singup/google/',
        GoogleSingUp.as_view(),
        name='google_singup'
    ),
    path(
        'oauth/callback/google/',
        OauthCallback.as_view(),
        name='oauth_callback'
    ),

    # Swagger UI
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$', 
        schema_view.without_ui(
            cache_timeout=0
        ),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$', 
        schema_view.with_ui(
            'swagger', 
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    # Opción de Documentación ReDoc
    re_path(
        r'^redoc/$', 
        schema_view.with_ui(
            'redoc', 
            cache_timeout=0
            ),
        name='schema-redoc'
    ),
]