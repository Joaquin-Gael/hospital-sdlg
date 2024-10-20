from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

class UserDataMiddleware:
     def __init__(self, get_response):
         self.get_response = get_response

     def __call__(self, request):
         response = self.get_response(request)
         try:
             view_name = request.resolver_match.view_name if request.resolver_match else 'Unknown'
             if view_name == 'RegisterUser':
                 return response
             if request.user and request.user.dni is not None and request.user.is_superuser:
                 return response
             messages.warning(request, 'porfavor complete el formulario')
             return HttpResponseRedirect(reverse_lazy('RegisterUser'))
         except Exception as e:
             return response