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

class CompleteUserData(forms.Form):
    dni = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'DNI', 'id':'user_dni'}
        ),
        label='DNI'
    )

    born_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha de Nacimiento', 'id':'id_fecha_nacimiento'}
        ),
        label='Fecha de Nacimiento'
    )

    def put_method(self): #metodo auxiliar
        try:
            pass
        except Exception as e:
            pass