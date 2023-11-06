# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('credit_card_payments/', views.lista_credit_card_payments, name='lista_credit_card_payments'),
    path('credit_card_payments/crear/', views.crear_credit_card_payment, name='crear_credit_card_payment'),
    path('credit_card_payments/editar/<int:payment_id>/', views.editar_credit_card_payment, name='editar_credit_card_payment'),
    path('credit_card_payments/deshabilitar/<int:payment_id>/', views.deshabilitar_credit_card_payment, name='deshabilitar_credit_card_payment'),
]