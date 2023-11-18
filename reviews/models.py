from django.db import models
from users.models import Renter, User
from vehicles.models import Vehicle

class Review(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='reviews_vehicle', on_delete=models.CASCADE, null=True )
    rating = models.PositiveIntegerField()  # Calificación (de 1 a 5)
    comment = models.TextField()  # Comentario
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha de la valoración
    reviewed_by = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='reviews_given')
    create_add = models.DateField(auto_now=False, auto_now_add=False,  null=True)

