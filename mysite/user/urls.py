from django.urls import (path, include)
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='RegisterUser'),
    path('login/', views.LoginUser.as_view(), name='LoginUser'),
    path('panel/', views.PanelUser.as_view(), name='PanelUser')
]