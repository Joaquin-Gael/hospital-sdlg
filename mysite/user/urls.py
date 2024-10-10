from django.urls import (path, include, re_path)
from . import views

urlpatterns = [
    path(
        'register/', 
        views.RegisterUser.as_view(), 
        name='RegisterUser'
    ),
    path(
        'login/', 
        views.LoginUser.as_view(), 
        name='LoginUser'
    ),
    path(
        'logout/', 
        views.LogoutUser.as_view(), 
        name='LogoutUser'
    ),
    path(
        'panel/', 
        views.PanelUser.as_view(), 
        name='PanelUser'
    ),
    path(
        'register/update/',
        views.UpdateUser.as_view(), 
        name='UpdateUser'
    ),
    path(
        'list/',
        views.UserList.as_view(), 
        name='ListUser'
    ),
    re_path(r'list/(?P<id>\d+)/',views.UserList.as_view(), name='ListUserWithParams')
]