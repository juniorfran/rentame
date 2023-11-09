from django.urls import path
from . import views  # Asegúrate de importar tus vistas

urlpatterns = [
    # Otras rutas de URL de tu aplicación

    # Ruta para la vista de reserva de vehículo
    path('create/<int:vehicle_id>/', views.reserva, name='create_reserva'),

    # Ruta para la vista de detalle de reserva
    path('detail/detalle/<int:reserva_id>/', views.detail_booking, name='detail_booking'),
]