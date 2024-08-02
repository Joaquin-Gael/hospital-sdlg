from django.contrib import admin
from django.urls import (path, include)
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('turnero/', include('turnero.urls')),
    path('user/', include('user.urls')),
    path('API/',include('API.urls')),
    path('',lambda request: redirect('Home')),
    path('not/found/404',views.NotFound.as_view(), name='NotFound')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
