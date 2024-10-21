from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

class UserDataMiddleware:
     def __init__(self, get_response):
         self.get_response = get_response

     def __call__(self, request):
         request.handler_redirection_value = True
         response = self.get_response(request)
         try:
             view_name = request.resolver_match.view_name if request.resolver_match else 'Unknown'
             if view_name == 'RegisterUser':
                 request.handler_redirection_value = False
                 return response
             if request.user and request.user.dni is not None:
                 request.handler_redirection_value = False
                 return response
             if request.user.is_superuser:
                request.handler_redirection_value = False
                return response
             messages.warning(request, 'Por favor complete el formulario')
             return HttpResponseRedirect(reverse('RegisterUser'))
         except Exception as e:
             return response