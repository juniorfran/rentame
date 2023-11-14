# Create your models here.
from django.db import models
from users.models import Renter
from vehicles.models import Vehicle, Seguro
from paymentmethod.models import PaymentMethod

class Booking(models.Model):
    renter = models.ForeignKey(
        Renter,
        on_delete=models.CASCADE,
        related_name='reservas_realizadas',
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    paymentmethod = models.ForeignKey(
        PaymentMethod,
        related_name='metodo_pago', 
        on_delete=models.CASCADE,
        null=True
        )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_add = models.DateField(auto_now=False, auto_now_add=False, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    opciones_estado = (
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    )
    estado = models.CharField(max_length=20, choices=opciones_estado, default='Pendiente', null=True)
    descuento = models.ForeignKey('Descuento', on_delete=models.SET_NULL, null=True, blank=True)
    seguro = models.ForeignKey(Seguro, on_delete=models.SET_NULL, null=True, blank=True)
    # Otros campos como estado de reserva, precio, etc.
    
class Descuento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.codigo
