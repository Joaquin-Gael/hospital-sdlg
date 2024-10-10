from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuarios

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'fecha_nacimiento']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email:'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Fecha nacimiento:'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña:'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña:'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Aquí podrías añadir cualquier lógica adicional relacionada con el usuario, pero sin Allauth
        if commit:
            instance.save()
        return instance
