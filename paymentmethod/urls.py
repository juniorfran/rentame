# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    ## URL PARA METODO (TARJETA DE CREDITO)
    path('lista_tarjeta', views.list_creditcard_payment, name='lista_tarjetas'),
    path('agregar_tarjeta_credito',views.add_creditcard_payment,name='tarjeta_credito'),
    path('editar_tarjeta_credito/<int:pk>',views.edit_creditcard_payment,name='editar_tarjeta_credito'),    
    path('eliminar_tarjeta_credito/<int:pk>',views.delete_creditcard_payment,name='eliminar_tarjeta_credito'),
    
    ## URL PARA METODO (TRANSFERENCIA BANCARIA)
    path('agregar_transferencia_bancaria',views.add_bank_transfer_payment,name='transferencia_bancaria'),
    path('editar_transferencia_bancaria/<int:pk>',views.edit_bank_transfer_payment,name='editar_transferencia_bancaria'),
    path('eliminar_transferencia_bancaria/<int:pk>',views.delete_bank_transfer_payment,name='eliminar_transferencia_bancaria'),
    
    

    path('payments_methods/', views.lista_payment_method, name='list_payments'),

]