from django import forms
from .models import Location
from django_countries.fields import CountryField

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'pais', 'estado', 'ciudad', 'colonia', 'canton', 'cp', 'address', 'latitude', 'longitude', 'estatus']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'  }),
            'pais': forms.Select(attrs={'class': 'form-control', 'id':'country'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'id':'state'}),
            'ciudad': forms.Select(attrs={'class': 'form-control', 'id':'city'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control'}),
            'canton': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'estatus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }