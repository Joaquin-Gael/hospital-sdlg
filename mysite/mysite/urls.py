from django.contrib import admin
from django.urls import (path, include)
from django.conf.urls import handler404
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from API.views import api
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('turnero/', include('turnero.urls')),
    path('user/', include('user.urls')),
    path('API/', api.urls),
    path('tinymce/', include('tinymce.urls')),
    path('',lambda request: redirect('Home')),
    path('not/found/404',views.NotFound.as_view(), name='NotFound'),
]

handler404 = views.NotFound.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += debug_toolbar_urls()