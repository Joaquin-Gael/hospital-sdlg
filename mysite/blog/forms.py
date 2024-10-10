from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.conf import settings

class ContactForm(forms.Form):
    nombre = forms.CharField(label='Nombre Completo', max_length=100)
    email = forms.EmailField(label='Correo Electrónico')
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'rows': 5}))
    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        widget=ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
            'data-size': 'compact',
        }
    )
    )