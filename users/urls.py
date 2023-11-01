from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import UserProfileViewSet, UserfileViewSet, VehicleOwnerViewSet, RenterViewSet, ReviewViewSet

# Crea un router
router = DefaultRouter()

# Registra la vista para el modelo UserProfile
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'user', UserfileViewSet)
router.register(r'vehicleowner', VehicleOwnerViewSet)
router.register(r'renter', RenterViewSet)
router.register(r'review', ReviewViewSet)




urlpatterns = [
    # Otras rutas de la aplicación
    path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('crear_perfil/', views.crear_perfil, name='crear_perfil'),
    path('perfil/', views.profileView, name='perfil'),
    path('become_owner/', views.become_owner, name='become_owner'),
    path('complete_verification/', views.complete_verification, name='complete_verification'),
    path('editar_perfil/', views.update_profile, name='editar_perfil'),
    path('ultimos_4_vehiculos/', views.ultimos_4_vehicle_list, name='ultimos_4_vehiculos'),
    
    
    # ... vehicle user URL ...
    path('lista_vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('ver_vehiculo/<int:vehiculo_id>/', views.ver_vehiculo, name='ver_vehiculo'),
    path('editar_vehiculo/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('deshabilitar_vehiculo/<int:vehiculo_id>/', views.deshabilitar_vehiculo, name='deshabilitar_vehiculo'),
    path('cargar_contenido_vehiculo/<int:vehiculo_id>/', views.cargar_contenido_vehiculo, name='cargar_contenido_vehiculo'),
    
    
    
    ##API RUTES
    path('api/', include(router.urls)),
    
    
]