from django.db import models
from users.models import User, UserProfile

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Nombre de la ubicación
    pais = models.CharField( max_length=50)
    estado = models.CharField(max_length=50)
    ciudad = models.CharField( max_length=50)
    colonia = models.CharField( max_length=50)
    canton = models.CharField(max_length=50)
    cp = models.CharField( max_length=50)
    address = models.CharField(max_length=200)  # Dirección de la ubicación
    latitude = models.DecimalField(max_digits=10, decimal_places=6)  # Latitud
    longitude = models.DecimalField(max_digits=10, decimal_places=6)  # Longitud
    create_add = models.DateField(auto_now_add=True)
    estatus = models.BooleanField(default=False)
