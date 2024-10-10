from django.urls import (path, include)
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path(
        '', 
        views.TurneroForm.as_view(), 
        name='Turnero'
    ),
    path(
        'turnos/<int:id>/', 
        views.TurnoData.as_view(), 
        name='Turnos'
    ),
    path(
        'comprobantes/<int:id>/', 
        views.ComprobanteDownloadView.as_view(), 
        name='Comprobante'
    ),
    path(
        'turnoPago',
        views.PagarTurno.as_view(),
        name="turnoPago"
    )
]