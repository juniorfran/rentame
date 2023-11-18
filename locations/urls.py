from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.location_list, name='location_list'),
    path('location/create/', views.location_create, name='location_create'),
    path('location/<int:pk>/', views.location_detail, name='location_detail'),
    path('location/update/<int:pk>/', views.location_update, name='location_update'),
    path('location/delete/<int:pk>/', views.location_delete, name='location_delete'),
    # Otros patrones de URL si los necesitas...
]