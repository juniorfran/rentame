from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, VehicleOwner, User


##FORM PARA EDITAR EL PERFIL
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('numero_telefono', 'direccion', 'nombre', 'imagen')
        
class VehicleOwnerForm(forms.ModelForm):
    class Meta:
        model = VehicleOwner
        fields = ('id_document', 'emergency_contact',  'availability_hours', 'rental_conditions', 'foto1_dui', 'foto2_dui', 'foto_licencia')


##FORM PARA CREAR EL PERFIL
class UserProfilCreateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('numero_telefono', 'direccion', 'nombre', 'imagen')
        
        
##FORMULARIO PARA CREAR USUARIO
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField()
    is_owner = forms.BooleanField(required=False)

    # Campos que faltaban
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_owner', 'password1', 'password2')