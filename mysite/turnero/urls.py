from django.urls import (path, include)
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.TurneroForm.as_view(), name='Turnero')
]