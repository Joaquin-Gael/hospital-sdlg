from django.urls import path
from .views import MedicPanel

urlpatterns = [
    path(
        'panel/',
        MedicPanel.as_view(),
        name='MedicPanel'
    )
]