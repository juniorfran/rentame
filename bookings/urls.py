from django.urls import path
from . import views  # Asegúrate de importar tus vistas

urlpatterns = [
    # Otras rutas de URL de tu aplicación

    # Ruta para la vista de reserva de vehículo
    path('create/<int:vehicle_id>/', views.reserva, name='create_reserva'),

    # Ruta para la vista de detalle de reserva
    path('detail/detalle/<int:reserva_id>/', views.detail_booking, name='detail_booking'),
    
    #path('realizar_pago/<int:booking_id>/', views.realizar_pago, name='realizar_pago'),
    
    #path('probar-autenticacion/', views.probar_autenticacion, name='probar_autenticacion'),
#     path('procesar_pago/', views.procesar_pago_y_mostrar_enlace, name='probar_autenticacion'),
#     path('procesar_pago_tarjeta/', views.procesar_pago_con_tarjeta, name='probar_autenticacion'),
#       path('detalles_pago/<str:id_transaccion>/', detalles_pago, name='detalles_pago'),

    path('listar_enlaces_pago_view/', views.listar_enlaces_pago_view, name='listar_enlaces_pago_view'),


]