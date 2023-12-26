from django import forms
from django.contrib.auth.forms import UserCreationForm, password_validation
from django.contrib.auth import get_user_model
from .models import UserProfile, VehicleOwner, User, Renter
from vehicles.models import Vehicle, Imagen, VehicleType


##FORM PARA EDITAR EL PERFIL
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('numero_telefono', 'direccion', 'nombre', 'imagen')
        
# class VehicleOwnerForm(forms.ModelForm):
#     class Meta:
#         model = VehicleOwner
#         fields = ('id_document', 'emergency_contact',  'availability_hours', 'rental_conditions', 'foto1_dui', 'foto2_dui', 'foto_licencia')


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
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),  # Queryset para obtener los tipos de vehículos
        empty_label=None,  # No muestra una etiqueta vacía en el select
    )
    images = forms.ModelMultipleChoiceField(
        queryset=Imagen.objects.all(),  # Reemplaza 'Imagen' con el nombre correcto de tu modelo de imágenes
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude = ['user', 'image', 'vehicle_type']
        
class DeshabilitarVehiculoForm(forms.Form):
    vehiculo = forms.ModelChoiceField(queryset=Vehicle.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.vehiculo = kwargs.pop('vehiculo')
        super(DeshabilitarVehiculoForm, self).__init__(*args, **kwargs)
        self.fields['vehiculo'].initial = self.vehiculo.id
        

##########################################################################################################
## FORMULARIOS PARA RENTER PERFIL DEL USUARIO
class RenterForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = ('id_document', 'emergency_contact', 'budget', 'preferred_rental_dates', 'required_documents', 'driving_history')
        widgets = {
            'id_document': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferred_rental_dates': forms.TextInput(attrs={'class': 'form-control'}),
            'required_documents': forms.TextInput(attrs={'class': 'form-control'}),
            'driving_history': forms.TextInput(attrs={'class': 'form-control'}),
        }



##########################################################################################################

class VehicleOwnerForm(forms.ModelForm):
    class Meta:
        model = VehicleOwner
        fields = ('id_document', 'emergency_contact', 'foto1_dui', 'foto2_dui', 'foto_licencia')
        widgets = {
            'id_document': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            # 'rental_price_hourly': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'rental_price_daily': forms.NumberInput(attrs={'class': 'form-control'}),
            #'availability_hours': forms.TextInput(attrs={'class': 'form-control'}),
            #'rental_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto1_dui': forms.FileInput(attrs={'class': 'form-control'}),
            'foto2_dui': forms.FileInput(attrs={'class': 'form-control'}),
            'foto_licencia': forms.FileInput(attrs={'class': 'form-control'}),
        }