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
        'pay-turno/',
        views.PayTurnoView.as_view(),
        name='pay-turno'
    ),
    path(
        'mercado-pago-webhook/', 
         views.MercadoPagoWebhookView.as_view(), 
         name='mercado-pago-webhook'
    ),
    path(
        '',
        views.PaypalIPNView.as_view(),
        name='paypal-ipn'
    ),
    path(
        'payment-success/<int:servicioID>/',
        views.PaymentSuccessful.as_view(),
        name='payment-success'
    ),
    path(
        'payment-failed/<int:servicioID>/',
        views.PaymentFailed.as_view(),
        name='payment-failed'
    ),
]