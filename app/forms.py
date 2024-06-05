from django import forms
from .models import Usuario, SolicitudArriendo,Propiedad
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User




class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono', 'correo_electronico', 'tipo_usuario']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        exclude = ('propietario',)  # Excluimos el campo 'propietario' del formulario

    
    
        
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['propiedad', 'mensaje']
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']