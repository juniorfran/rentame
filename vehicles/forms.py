# forms.py
from django import forms
from .models import VehicleType, Location

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name', 'capacidad', 'create_add']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'departamento', 'ciudad', 'canton', 'referencia', 'address', 'latitude', 'longitude', 'create_add']