from django import forms
from django.contrib.auth.forms import UserCreationForm, password_validation
from django.contrib.auth import get_user_model
from .models import UserProfile, VehicleOwner, User
from vehicles.models import Vehicle


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

class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    is_owner = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_owner', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None  # Eliminar la ayuda predeterminada

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:
            password_validation.validate_password(password1, self.instance)
        return password1
##########################################################################################################
## FORMULARIOS PARA VEHICULO DEL USUARIO
class AddVehicleUserForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

#formulario para editar el vehiculo
class EditVehicleUserForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['user']
        fields = '__all__'
        