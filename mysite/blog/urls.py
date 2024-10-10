from django.urls import (path, include)
from . import views

urlpatterns = [
    path('', views.Home.as_view(),name='Home'),
    path('testimonios/', views.Testimonios.as_view(),name='Testimonios'),
    path('nosotros/', views.Nosotros.as_view(),name='Nosotros'),
    path('atencionalpaciente/', views.Atencion.as_view(),name='Atencion'),
    path('contacto/', views.Contactos.as_view(),name='Contactos'),
]