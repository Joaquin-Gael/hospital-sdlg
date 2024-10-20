from django import forms

class LoginUserForm(forms.Form):
    dni = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'DNI', 'id': 'floatingDNI'}
        ),
        label='DNI')
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'id': 'floatingPassword'}
        ),
        label='Contraseña')

    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input p-inputswitch custom-switch-container', 'role': 'switch', 'id': 'flexSwitchCheckDefault'}
        )
    )