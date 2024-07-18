from django.urls import (path, include)
from . import views

urlpatterns = [
    path('', views.Home.as_view(),name='Home'),
]