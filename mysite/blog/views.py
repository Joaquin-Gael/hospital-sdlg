from django.utils.decorators import method_decorator
from .middlewares.antiSpam import antiSpamMiddleware
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django import views

# Create your views here.

class Home(views.View):
    def get(self, request):
        return render(request, 'blog/index.html')

class Testimonios(views.View):
    def get(self, request):
        return render(request, 'blog/testimonios.html')

class Nosotros(views.View):
    def get(self, request):
        return render(request, 'blog/nosotros.html')

class Contactos(views.View):
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)        

    def get(self, request):
        form = ContactForm()
        return render(request, 'blog/contacto.html', {'form':form})
    
    @method_decorator(antiSpamMiddleware)
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
                
            subject = f"Nuevo mensaje de {nombre}"
            message = f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]
        
            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, message='¡Mensaje enviado con éxito! Nos pondremos en contacto con usted.')
                return render(request, 'blog/contacto.html')
            except Exception as e:
                messages.error(request, message=f'Hubo un error al enviar su mensaje: {str(e)}')
                return redirect('Contactos')
        else:
            messages.error(request, message='Los datos del formulario no son válidos.')
            return redirect('Contactos')

class Atencion(views.View):
    def get(self, request):
        return render(request, 'blog/atencionalpaciente.html')