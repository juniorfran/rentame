from django.contrib import admin
from .models import Booking, Descuento

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('renter', 'vehicle', 'start_date', 'end_date')
    
@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin')
    