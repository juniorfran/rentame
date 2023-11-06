
from django import views
from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import include, path
#from django.contrib.auth.models import User
from users.models import User
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    #path('lista_vehiculos/', views.vehicle_list, name='lista_vehiculos'),
    
    #url api
    #path('api/', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    
    #urls de users
    path('users/', include('users.urls')),
    
    #urls de reviews
    path('reviews/', include('reviews.urls')),
    
    #urls de vehicles
    path('vehicles/', include('vehicles.urls')),
    
    #urls de metodos de pago
    path('paymentmethod/', include('paymentmethod.urls')),
    
    
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


